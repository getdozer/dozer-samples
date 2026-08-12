import unittest

from app.eligibility import evaluate_eligibility
from app.models import CardProduct, CustomerFeatures, DataContractError


def customer(**overrides):
    values = dict(
        customer_id="C", age=35, annual_income=80000, credit_score=750,
        risk_band="low", monthly_spend=2000, travel_spend=500,
        grocery_spend=500, active_account=True,
    )
    values.update(overrides)
    return CustomerFeatures(**values)


def card(**overrides):
    values = dict(
        product_id="P", name="Product", description="Rewards", annual_fee=0,
        min_income=50000, min_credit_score=700, min_age=21, max_age=75,
        allowed_risk_bands=("low",), reward_rate=.01,
        travel_multiplier=2, grocery_multiplier=1,
    )
    values.update(overrides)
    return CardProduct(**values)


class EligibilityTests(unittest.TestCase):
    def test_eligible_when_all_constraints_pass(self):
        self.assertTrue(evaluate_eligibility(customer(), card()).eligible)

    def test_accumulates_every_failure(self):
        decision = evaluate_eligibility(
            customer(age=18, annual_income=10, credit_score=300, risk_band="high", active_account=False),
            card(),
        )
        self.assertFalse(decision.eligible)
        self.assertEqual(len(decision.reasons), 5)

    def test_boundary_values_are_eligible(self):
        value = customer(age=21, annual_income=50000, credit_score=700)
        self.assertTrue(evaluate_eligibility(value, card()).eligible)

    def test_missing_constraint_fails_during_parsing(self):
        incomplete = {
            "product_id": "P", "name": "Card", "description": "cashback",
            "annual_fee": "0", "min_income": "1", "min_credit_score": "1",
            "min_age": "18", "max_age": "80", "reward_rate": ".01",
            "travel_multiplier": "1", "grocery_multiplier": "1",
        }
        with self.assertRaisesRegex(DataContractError, "allowed_risk_bands"):
            CardProduct.from_mapping(incomplete)


if __name__ == "__main__":
    unittest.main()
