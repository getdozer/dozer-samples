import json
import unittest
from pathlib import Path
from unittest.mock import patch

from app.gateway import CustomerNotFoundError, DozerGateway, FixtureGateway, GatewayError


ROOT = Path(__file__).resolve().parents[1]


class FixtureGatewayTests(unittest.TestCase):
    def setUp(self):
        self.gateway = FixtureGateway(ROOT / "data")

    def test_computes_features_across_three_datasets(self):
        features = self.gateway.get_customer_features("C001")
        self.assertEqual(features.monthly_spend, 2000)
        self.assertEqual(features.travel_spend, 900)
        self.assertEqual(features.grocery_spend, 480)
        self.assertTrue(features.active_account)

    def test_closed_account_is_not_active_and_has_no_spend(self):
        features = self.gateway.get_customer_features("C005")
        self.assertFalse(features.active_account)
        self.assertEqual(features.monthly_spend, 0)

    def test_unknown_customer_raises(self):
        with self.assertRaises(CustomerNotFoundError):
            self.gateway.get_customer_features("UNKNOWN")

    def test_loads_products(self):
        self.assertEqual(len(self.gateway.list_card_products()), 5)


class FakeResponse:
    status = 200

    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def read(self, *_):
        return json.dumps(self.payload).encode()


class DozerGatewayTests(unittest.TestCase):
    def test_accepts_records_envelope(self):
        gateway = DozerGateway()
        row = {
            "customer_id": "C", "age": 30, "annual_income": 50000,
            "credit_score": 700, "risk_band": "low", "monthly_spend": 100,
            "travel_spend": 10, "grocery_spend": 20, "active_account": 1,
        }
        gateway._post = lambda *_: {"records": [row]}
        self.assertEqual(gateway.get_customer_features("C").credit_score, 700)

    def test_rejects_unknown_response_shape(self):
        with self.assertRaisesRegex(GatewayError, "response shape"):
            DozerGateway._records({"result": {}})

    def test_rejects_non_object_records(self):
        with self.assertRaisesRegex(GatewayError, "record shape"):
            DozerGateway._records({"records": ["not-an-object"]})

    def test_customer_query_uses_post_filter(self):
        gateway = DozerGateway()
        requests = []
        gateway._post = lambda path, body: requests.append((path, body)) or []
        with self.assertRaises(CustomerNotFoundError):
            gateway.get_customer_features("customer/id")
        self.assertEqual(
            requests,
            [("/customer_features/query", {"$filter": {"customer_id": "customer/id"}})],
        )

    def test_post_sends_json_body_and_content_type(self):
        captured = []

        def open_request(request, timeout):
            captured.append((request, timeout))
            return FakeResponse([])

        with patch("app.gateway.urlopen", side_effect=open_request):
            DozerGateway(timeout=2)._post(
                "/customer_features/query", {"$filter": {"customer_id": "C001"}}
            )
        request, timeout = captured[0]
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(request.get_header("Content-type"), "application/json")
        self.assertEqual(
            json.loads(request.data), {"$filter": {"customer_id": "C001"}}
        )
        self.assertEqual(timeout, 2)

    def test_sql_aggregates_mixed_accounts_to_one_customer_row(self):
        config = (ROOT / "dozer-config.yaml").read_text(encoding="utf-8")
        self.assertIn("MAX(CASE WHEN a.status = 'active'", config)
        group_by = config.split("GROUP BY", 1)[1].split(";", 1)[0]
        self.assertNotIn("a.status", group_by)
        self.assertIn("CASE WHEN a.status = 'active' THEN COALESCE(t.amount, 0)", config)

    def test_rejects_oversized_response(self):
        with patch("app.gateway.urlopen", return_value=FakeResponse([{"large": "value"}])):
            with self.assertRaisesRegex(GatewayError, "size limit"):
                DozerGateway(max_response_bytes=2)._get("/card_products")


if __name__ == "__main__":
    unittest.main()
