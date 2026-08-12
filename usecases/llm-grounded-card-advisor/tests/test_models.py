import math
import unittest

from app.models import CardProduct, CustomerFeatures, DataContractError, Recommendation


CUSTOMER = dict(
    customer_id="C", age=35, annual_income=80000, credit_score=750,
    risk_band="low", monthly_spend=2000, travel_spend=500,
    grocery_spend=500, active_account=True,
)
CARD = dict(
    product_id="P", name="Product", description="Rewards", annual_fee=0,
    min_income=50000, min_credit_score=700, min_age=21, max_age=75,
    allowed_risk_bands=("low",), reward_rate=.01,
    travel_multiplier=2, grocery_multiplier=1,
)


class NumericContractTests(unittest.TestCase):
    def test_customer_rejects_every_non_finite_numeric_field(self):
        fields = (
            "age", "annual_income", "credit_score", "monthly_spend",
            "travel_spend", "grocery_spend",
        )
        for field in fields:
            for bad in (math.nan, math.inf, -math.inf):
                with self.subTest(field=field, bad=bad):
                    values = {**CUSTOMER, field: bad}
                    with self.assertRaises(DataContractError):
                        CustomerFeatures(**values)

    def test_card_rejects_every_non_finite_numeric_field(self):
        fields = (
            "annual_fee", "min_income", "min_credit_score", "min_age", "max_age",
            "reward_rate", "travel_multiplier", "grocery_multiplier",
        )
        for field in fields:
            for bad in (math.nan, math.inf, -math.inf):
                with self.subTest(field=field, bad=bad):
                    values = {**CARD, field: bad}
                    with self.assertRaises(DataContractError):
                        CardProduct(**values)

    def test_recommendation_rejects_non_finite_outputs(self):
        for field in ("score", "estimated_annual_value"):
            for bad in (math.nan, math.inf, -math.inf):
                with self.subTest(field=field, bad=bad):
                    values = dict(
                        product_id="P", product_name="Product", score=0.5,
                        reason="grounded", estimated_annual_value=10,
                        provenance=(),
                    )
                    values[field] = bad
                    with self.assertRaises(DataContractError):
                        Recommendation(**values)

    def test_rejects_cross_field_and_range_violations(self):
        with self.assertRaisesRegex(DataContractError, "category spend"):
            CustomerFeatures(**{**CUSTOMER, "monthly_spend": 10})
        with self.assertRaisesRegex(DataContractError, "min_age"):
            CardProduct(**{**CARD, "min_age": 80, "max_age": 20})


if __name__ == "__main__":
    unittest.main()
