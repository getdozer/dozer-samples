"""Fail-closed eligibility decisions made before semantic ranking."""

from __future__ import annotations

from dataclasses import dataclass

from .models import CardProduct, CustomerFeatures


@dataclass(frozen=True)
class EligibilityDecision:
    eligible: bool
    reasons: tuple[str, ...]


def evaluate_eligibility(customer: CustomerFeatures, card: CardProduct) -> EligibilityDecision:
    """Evaluate every hard constraint; uncertainty never becomes approval."""
    reasons: list[str] = []
    if not customer.active_account:
        reasons.append("customer account is inactive")
    if customer.age < card.min_age or customer.age > card.max_age:
        reasons.append("age is outside the product range")
    if customer.annual_income < card.min_income:
        reasons.append("income is below the product minimum")
    if customer.credit_score < card.min_credit_score:
        reasons.append("credit score is below the product minimum")
    if customer.risk_band not in card.allowed_risk_bands:
        reasons.append("risk band is not allowed")
    return EligibilityDecision(not reasons, tuple(reasons))
