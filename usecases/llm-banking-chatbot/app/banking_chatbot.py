#!/usr/bin/env python3
"""Hyper-Personalized Banking Chatbot integrating Dozer, Vector Database, and LangChain.

Reference Architecture:
- Dozer blog post: https://getdozer.io/blog/llm-chatbot
- GitHub Issue: https://github.com/getdozer/dozer/issues/1690

Usage:
  python usecases/llm-banking-chatbot/app/banking_chatbot.py \
    --offline-fixture --customer C001 \
    --question "Which card is best for travel and dining rewards?"
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

# Ensure local package imports work whether invoked as script or module
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from dozer_client import CustomerProfile, DozerClient
from vector_store import CardProductDocument, CardProductVectorStore

PROMPT_TEMPLATE_TEXT = """You are an AI Banking Advisor powered by Dozer real-time customer context and a Vector Database of credit card brochures.

=== REAL-TIME UNIFIED CUSTOMER PROFILE (FROM DOZER API) ===
{customer_profile_context}

=== RETRIEVED CREDIT CARD PRODUCTS (FROM VECTOR DATABASE) ===
{retrieved_cards_context}

=== CUSTOMER QUESTION ===
{user_question}

=== INSTRUCTIONS ===
1. Recommend the single best credit card from the retrieved products that matches the customer's real-time spending categories, credit score ({credit_score}), annual income (${annual_income:,.0f}), and credit utilization ({utilization_pct:.2f}%).
2. Explicitly verify whether the customer meets the card's minimum credit score and income eligibility criteria.
3. Quantify the estimated rewards or interest savings based on their actual Dozer category spend.
4. Provide a concise secondary option if applicable.
"""


class BankingChatbot:
    """Orchestrates Dozer real-time customer profile lookup, Vector DB retrieval, and LangChain LLM generation."""

    def __init__(
        self,
        project_root: Optional[Union[str, Path]] = None,
        dozer_url: str = "http://localhost:8080",
        offline_fixture: bool = False,
        openai_api_key: Optional[str] = None,
    ) -> None:
        self.project_root = Path(project_root) if project_root else PROJECT_ROOT
        self.offline_fixture = offline_fixture
        self.openai_api_key = openai_api_key or os.environ.get("OPENAI_API_KEY")
        self.dozer_client = DozerClient(
            base_url=dozer_url,
            project_root=self.project_root,
            offline_fixture=offline_fixture,
        )
        self.vector_store = CardProductVectorStore(
            csv_path=self.project_root / "data" / "card_products.csv"
        )

    def _estimate_annual_benefit(self, profile: CustomerProfile, card: CardProductDocument) -> str:
        """Compute grounded annual rewards / interest savings estimate from Dozer spend metrics."""
        if card.product_id == "P01":  # Dozer Travel Signature (5x travel, 3x dining, 1x other)
            monthly_pts = (
                profile.travel_spend * 5.0
                + profile.dining_spend * 3.0
                + (profile.total_spend - profile.travel_spend - profile.dining_spend) * 1.0
            )
            annual_pts = int(monthly_pts * 12)
            dollar_val = annual_pts * 0.0125
            return f"~{annual_pts:,} points/year (~${dollar_val:,.0f} travel value) + $300 travel credit (net ${dollar_val + 300 - card.annual_fee:,.0f}/yr after ${card.annual_fee:.0f} fee)"
        if card.product_id == "P02":  # Dozer Everyday Cashback+ (4% groceries, 3% fuel, 2% dining, 1% other)
            other = max(0.0, profile.total_spend - profile.groceries_spend - profile.fuel_spend - profile.dining_spend)
            monthly_cb = (
                profile.groceries_spend * 0.04
                + profile.fuel_spend * 0.03
                + profile.dining_spend * 0.02
                + other * 0.01
            )
            return f"~${monthly_cb * 12:,.2f}/year in direct cashback with $0 annual fee"
        if card.product_id == "P03":  # Dozer Student Rise Cash (3% dining/bookstores/utilities, 1.5% other)
            boosted = profile.dining_spend + profile.online_shopping_spend + profile.utilities_spend
            other = max(0.0, profile.total_spend - boosted)
            monthly_cb = boosted * 0.03 + other * 0.015
            return f"~${monthly_cb * 12:,.2f}/year in cashback + $100 statement credit with $0 annual fee"
        if card.product_id == "P04":  # Dozer Balance Shield 0% APR
            annual_interest_saved = profile.current_balance * (profile.current_apr / 100.0)
            return f"~${annual_interest_saved:,.2f}/year in avoided interest over 21 months at 0% intro APR on ${profile.current_balance:,.2f} balance"
        if card.product_id == "P05":  # Dozer Founders Business Elite
            biz_spend = profile.online_shopping_spend + profile.utilities_spend
            travel_dining = profile.travel_spend + profile.dining_spend
            other = max(0.0, profile.total_spend - biz_spend - travel_dining)
            annual_pts = int((biz_spend * 4.0 + travel_dining * 3.0 + other * 1.0) * 12)
            dollar_val = annual_pts * 0.012
            return f"~{annual_pts:,} business points/year (~${dollar_val:,.0f} value, net ${dollar_val - card.annual_fee:,.0f}/yr after ${card.annual_fee:.0f} fee)"
        return "Custom rewards aligned with monthly spend"

    def build_augmented_prompt(
        self,
        profile: CustomerProfile,
        retrieved_cards: List[Tuple[CardProductDocument, float]],
        question: str,
    ) -> str:
        """Construct the LangChain prompt combining Dozer profile context and Vector DB brochures."""
        cards_lines: List[str] = []
        for rank, (card, score) in enumerate(retrieved_cards, start=1):
            eligible = (
                profile.credit_score >= card.min_credit_score
                and profile.annual_income >= card.min_annual_income
            )
            elig_status = "ELIGIBLE" if eligible else "INELIGIBLE (below min score/income)"
            est_benefit = self._estimate_annual_benefit(profile, card)
            cards_lines.append(
                f"[{rank}] {card.card_name} (ID: {card.product_id}) | Similarity Score: {score:.4f} | Status: {elig_status}\n"
                f"    Segment: {card.target_segment} | Annual Fee: ${card.annual_fee:.0f} | APR: {card.apr_range}\n"
                f"    Eligibility Requirement: Credit Score >= {card.min_credit_score}, Income >= ${card.min_annual_income:,.0f}\n"
                f"    Rewards: {card.primary_rewards}\n"
                f"    Sign-up Bonus: {card.signup_bonus}\n"
                f"    Projected Customer Value: {est_benefit}\n"
                f"    Brochure Summary: {card.description}"
            )

        return PROMPT_TEMPLATE_TEXT.format(
            customer_profile_context=profile.format_for_prompt(),
            retrieved_cards_context="\n\n".join(cards_lines),
            user_question=question,
            credit_score=profile.credit_score,
            annual_income=profile.annual_income,
            utilization_pct=profile.utilization_pct,
        )

    def _synthesize_grounded_response(
        self,
        profile: CustomerProfile,
        retrieved_cards: List[Tuple[CardProductDocument, float]],
        question: str,
    ) -> str:
        """Generate a hyper-personalized recommendation grounded in Dozer + Vector DB context."""
        eligible_cards = [
            (card, score)
            for card, score in retrieved_cards
            if profile.credit_score >= card.min_credit_score
            and profile.annual_income >= card.min_annual_income
        ]
        top_card, top_score = eligible_cards[0] if eligible_cards else retrieved_cards[0]
        projected_value = self._estimate_annual_benefit(profile, top_card)
        top_cats = ", ".join(
            f"{cat.replace('_', ' ')} (${amt:,.2f}/mo)" for cat, amt in profile.top_spending_categories[:2]
        )

        lines = [
            f"Personalized Recommendation for {profile.full_name} ({profile.customer_code}): **{top_card.card_name}**",
            "",
            "1. Why This Card Matches Your Real-Time Dozer Profile:",
            f"   - Spending Alignment: Your Dozer transaction stream shows ${profile.total_spend:,.2f} in recent spend across {profile.tx_count} transactions, led by {top_cats}.",
            f"   - Rewards & Value Fit: {top_card.card_name} offers {top_card.primary_rewards}. Based on your real-time spend, this yields {projected_value}.",
            f"   - Eligibility Verification: Approved fit — your credit score ({profile.credit_score}) and annual income (${profile.annual_income:,.0f}) exceed the card's minimums (score >= {top_card.min_credit_score}, income >= ${top_card.min_annual_income:,.0f}).",
            f"   - Current Account Context: You currently hold {profile.existing_card_type} with a ${profile.current_balance:,.2f} balance on a ${profile.credit_limit:,.0f} limit ({profile.utilization_pct:.2f}% utilization at {profile.current_apr:.2f}% APR).",
        ]

        if len(eligible_cards) > 1:
            runner_up, _ = eligible_cards[1]
            runner_value = self._estimate_annual_benefit(profile, runner_up)
            lines.extend(
                [
                    "",
                    f"2. Alternative Eligible Option: **{runner_up.card_name}** (${runner_up.annual_fee:.0f} annual fee)",
                    f"   - Highlights: {runner_up.primary_rewards} ({runner_value}).",
                ]
            )
        return "\n".join(lines)

    def answer(
        self,
        customer_identifier: Union[int, str],
        question: str,
        top_k: int = 3,
    ) -> Dict[str, Any]:
        """Run the end-to-end Dozer + Vector DB + LangChain pipeline for a customer query."""
        profile = self.dozer_client.get_customer_profile(customer_identifier)
        retrieved = self.vector_store.similarity_search_with_score(
            query=question,
            k=top_k,
            customer_profile=profile,
        )
        prompt_text = self.build_augmented_prompt(profile, retrieved, question)

        llm_mode = "deterministic_offline_chain"
        response_text: Optional[str] = None

        if self.openai_api_key and not self.offline_fixture:
            try:
                from langchain_openai import ChatOpenAI
                from langchain_core.prompts import PromptTemplate

                prompt = PromptTemplate.from_template("{full_prompt}")
                llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1, api_key=self.openai_api_key)
                chain = prompt | llm
                res = chain.invoke({"full_prompt": prompt_text})
                response_text = getattr(res, "content", str(res))
                llm_mode = "langchain_openai"
            except Exception:
                response_text = None

        if response_text is None:
            response_text = self._synthesize_grounded_response(profile, retrieved, question)

        eligible_ranked = [
            card.card_name
            for card, _ in retrieved
            if profile.credit_score >= card.min_credit_score
            and profile.annual_income >= card.min_annual_income
        ]

        return {
            "customer_id": profile.customer_id,
            "customer_code": profile.customer_code,
            "customer_name": profile.full_name,
            "question": question,
            "llm_mode": llm_mode,
            "customer_profile": profile.to_context_dict(),
            "retrieved_products": [
                {
                    "rank": idx + 1,
                    "product_id": doc.product_id,
                    "card_name": doc.card_name,
                    "similarity_score": score,
                    "eligible": (
                        profile.credit_score >= doc.min_credit_score
                        and profile.annual_income >= doc.min_annual_income
                    ),
                    "estimated_annual_benefit": self._estimate_annual_benefit(profile, doc),
                }
                for idx, (doc, score) in enumerate(retrieved)
            ],
            "recommended_card": eligible_ranked[0] if eligible_ranked else retrieved[0][0].card_name,
            "prompt": prompt_text,
            "answer": response_text,
        }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Dozer + Vector DB + LangChain Hyper-Personalized Banking Chatbot"
    )
    parser.add_argument(
        "--customer",
        default="C001",
        help="Customer ID (e.g. 101) or code (e.g. C001). Default: C001",
    )
    parser.add_argument(
        "--question",
        default="Which credit card should I apply for to maximize my rewards?",
        help="Customer question for the banking chatbot.",
    )
    parser.add_argument(
        "--dozer-url",
        default=os.environ.get("DOZER_URL", "http://localhost:8080"),
        help="Dozer REST API base URL (default: http://localhost:8080)",
    )
    parser.add_argument(
        "--offline-fixture",
        action="store_true",
        help="Execute Dozer SQL pipeline locally over CSV fixtures without requiring a running Dozer server or OpenAI key.",
    )
    parser.add_argument(
        "--simulate-realtime-tx",
        action="store_true",
        help="Demonstrate how a real-time transaction stream update in Dozer dynamically shifts the chatbot's recommendation.",
    )
    parser.add_argument(
        "--show-prompt",
        action="store_true",
        help="Print the full LangChain augmented prompt containing Dozer profile and Vector DB context.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit output as formatted JSON.",
    )
    args = parser.parse_args(argv)

    bot = BankingChatbot(
        dozer_url=args.dozer_url,
        offline_fixture=args.offline_fixture,
    )

    result = bot.answer(args.customer, args.question)

    if args.json and not args.simulate_realtime_tx:
        output_payload = dict(result)
        if not args.show_prompt:
            output_payload.pop("prompt", None)
        print(json.dumps(output_payload, indent=2))
        return 0

    print("=" * 78)
    print("DOZER + VECTOR DB + LANGCHAIN HYPER-PERSONALIZED BANKING CHATBOT")
    print("=" * 78)
    prof = result["customer_profile"]
    print(
        f"Customer: {prof['full_name']} ({prof['customer_code']} / ID {prof['customer_id']}) | "
        f"Income: ${prof['annual_income']:,.0f} | Credit Score: {prof['credit_score']} | "
        f"Utilization: {prof['utilization_pct']:.2f}%"
    )
    print(f"Total Spend (Dozer Stream): ${prof['total_spend']:,.2f} across {prof['tx_count']} transactions")
    print(f"Question: {result['question']}")
    print("-" * 78)
    print("Vector DB Top Retrieved Credit Cards:")
    for item in result["retrieved_products"]:
        status = "ELIGIBLE" if item["eligible"] else "INELIGIBLE"
        print(
            f"  #{item['rank']} {item['card_name']} ({item['product_id']}) "
            f"[score={item['similarity_score']:.4f}, {status}] -> {item['estimated_annual_benefit']}"
        )
    if args.show_prompt:
        print("-" * 78)
        print(result["prompt"])
    print("-" * 78)
    print(result["answer"])
    print("=" * 78)

    if args.simulate_realtime_tx:
        print("\n>>> SIMULATING REAL-TIME CDC TRANSACTION EVENT IN DOZER (`transactions` stream)...")
        target_id = int(prof["customer_id"])
        new_txs = [
            {
                "tx_id": 5901,
                "customer_id": target_id,
                "tx_date": "2026-11-01",
                "merchant": "Singapore Airlines",
                "category": "travel",
                "amount": 2850.00,
                "currency": "USD",
                "is_international": "true",
            },
            {
                "tx_id": 5902,
                "customer_id": target_id,
                "tx_date": "2026-11-02",
                "merchant": "Four Seasons Tokyo",
                "category": "travel",
                "amount": 1950.00,
                "currency": "JPY",
                "is_international": "true",
            },
        ]
        for tx in new_txs:
            bot.dozer_client.local_pipeline.insert_realtime_transaction(tx)
            print(f"    + Ingested CDC Event: tx_id={tx['tx_id']} | {tx['merchant']} | {tx['category']} | ${tx['amount']:,.2f}")

        updated = bot.answer(
            args.customer,
            "I just booked international flights and hotels. Which card should I use now?",
        )
        u_prof = updated["customer_profile"]
        print("-" * 78)
        print(
            f"Updated Dozer Profile for {u_prof['full_name']}: Total Spend=${u_prof['total_spend']:,.2f} "
            f"(Travel Spend=${u_prof['travel_spend']:,.2f} across {u_prof['tx_count']} transactions)"
        )
        print(f"Updated Top Recommendation: {updated['recommended_card']}")
        print("-" * 78)
        print(updated["answer"])
        print("=" * 78)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
