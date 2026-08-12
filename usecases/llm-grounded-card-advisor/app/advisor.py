"""Grounded recommendation pipeline: gate, retrieve, constrain, rank, explain."""

from __future__ import annotations

from typing import Any

from .eligibility import evaluate_eligibility
from .explainer import CardExplainer, ExplanationContext
from .gateway import CardDataGateway
from .models import Provenance, Recommendation
from .security import validate_query
from .vector_search import DeterministicVectorSearch, ProductSearch


class NoEligibleProductsError(LookupError):
    pass


class GroundedCardAdvisor:
    def __init__(
        self,
        gateway: CardDataGateway,
        search: ProductSearch | None = None,
        explainer: CardExplainer | None = None,
    ) -> None:
        self.gateway = gateway
        self.search = search or DeterministicVectorSearch()
        self.explainer = explainer

    @staticmethod
    def _annual_value(customer: Any, card: Any) -> float:
        generic = max(customer.monthly_spend - customer.travel_spend - customer.grocery_spend, 0)
        monthly_rewards = (
            generic * card.reward_rate
            + customer.travel_spend * card.reward_rate * card.travel_multiplier
            + customer.grocery_spend * card.reward_rate * card.grocery_multiplier
        )
        return monthly_rewards * 12 - card.annual_fee

    def recommend(self, customer_id: str, query: str, *, limit: int = 3) -> dict[str, Any]:
        if limit < 1 or limit > 10:
            raise ValueError("limit must be between 1 and 10")
        safe_query = validate_query(query)  # security gate precedes retrieval
        customer = self.gateway.get_customer_features(customer_id)
        cards = self.gateway.list_card_products()

        eligible = []
        rejected = []
        for card in cards:
            decision = evaluate_eligibility(customer, card)
            if decision.eligible:
                eligible.append(card)
            else:
                rejected.append({"product_id": card.product_id, "reasons": list(decision.reasons)})
        if not eligible:
            raise NoEligibleProductsError("no product satisfies every hard eligibility rule")

        recommendations = []
        for hit in self.search.rank(safe_query, eligible)[:limit]:
            value = self._annual_value(customer, hit.product)
            evidence = (
                Provenance(
                    source=self.gateway.source_name,
                    endpoint="customer_features",
                    record_id=customer.customer_id,
                    fields=("monthly_spend", "travel_spend", "grocery_spend"),
                ),
                Provenance(
                    source=self.gateway.source_name,
                    endpoint="card_products",
                    record_id=hit.product.product_id,
                    fields=("annual_fee", "reward_rate", "travel_multiplier", "grocery_multiplier"),
                ),
            )
            reason = (
                f"Eligible under all published constraints; query relevance {hit.score:.3f}. "
                f"Estimated rewards minus annual fee: {value:.2f}/year."
            )
            recommendations.append(
                Recommendation(
                    product_id=hit.product.product_id,
                    product_name=hit.product.name,
                    score=hit.score,
                    reason=reason,
                    estimated_annual_value=value,
                    provenance=evidence,
                ).to_dict()
            )

        if self.explainer is not None and recommendations:
            selected = recommendations[0]
            selected["llm_explanation"] = self.explainer.explain(
                ExplanationContext(
                    query=safe_query,
                    product_id=selected["product_id"],
                    product_name=selected["product_name"],
                    deterministic_reason=selected["reason"],
                    estimated_annual_value=selected["estimated_annual_value"],
                    monthly_spend=customer.monthly_spend,
                    travel_spend=customer.travel_spend,
                    grocery_spend=customer.grocery_spend,
                )
            )

        return {
            "customer_id": customer.customer_id,
            "query": safe_query,
            "gateway": self.gateway.source_name,
            "disclaimer": "Illustrative recommendation, not a credit decision or financial advice.",
            "recommendations": recommendations,
            "rejected_products": rejected,
        }
