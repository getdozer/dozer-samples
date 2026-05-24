import os
import unittest
from pathlib import Path
from unittest.mock import patch

import banking_chatbot
from banking_chatbot import (
    build_customer_context,
    extract_dozer_records,
    load_local_tables,
    rank_products,
    answer_question,
    select_products,
)


class BankingChatbotSampleTest(unittest.TestCase):
    def setUp(self):
        self.tables = load_local_tables()

    def test_loads_all_fixture_datasets(self):
        self.assertEqual(
            {"customer_profiles", "accounts", "transactions", "card_products"},
            set(self.tables),
        )
        self.assertGreaterEqual(len(self.tables["transactions"]), 10)
        self.assertGreaterEqual(len(self.tables["card_products"]), 5)

    def test_customer_context_aggregates_spend(self):
        context = build_customer_context("C001", self.tables)

        self.assertEqual("Ava Sharma", context.full_name)
        self.assertEqual("travel", context.top_category)
        self.assertAlmostEqual(2020.50, context.spend_by_category["travel"])
        self.assertAlmostEqual(91040.40, context.total_balance)

    def test_travel_question_ranks_travel_signature_first(self):
        context = build_customer_context("C001", self.tables)
        ranked = rank_products(
            self.tables["card_products"],
            context,
            "Which card is best for travel and dining rewards?",
        )

        self.assertEqual("Dozer Travel Signature", ranked[0][1]["product_name"])

    def test_vector_candidates_are_reranked_with_customer_context(self):
        class FakeVectorStore:
            def similarity_search(self, query, k):
                self.query = query
                self.k = k
                return [
                    type("Doc", (), {"metadata": {"product_id": "P002"}})(),
                    type("Doc", (), {"metadata": {"product_id": "P001"}})(),
                    type("Doc", (), {"metadata": {"product_id": "P005"}})(),
                ]

        context = build_customer_context("C001", self.tables)
        with patch.object(
            banking_chatbot,
            "build_langchain_vector_store",
            return_value=FakeVectorStore(),
        ):
            selected = select_products(
                self.tables["card_products"],
                context,
                "Which card is best for travel and dining rewards?",
            )

        self.assertEqual("Dozer Travel Signature", selected[0]["product_name"])

    def test_fee_sensitive_customer_gets_no_fee_card(self):
        answer = answer_question(
            "C003",
            "I want practical grocery rewards without an annual fee.",
        )

        self.assertIn("Dozer Everyday Cash", answer)
        self.assertIn("annual fee of $0", answer)

    def test_optional_llm_mode_falls_back_without_api_key(self):
        original_key = os.environ.pop("OPENAI_API_KEY", None)
        try:
            answer = answer_question(
                "C001",
                "Which card is best for travel?",
                use_llm=True,
            )
        finally:
            if original_key is not None:
                os.environ["OPENAI_API_KEY"] = original_key

        self.assertIn("Dozer Travel Signature", answer)
        self.assertIn("LLM layer skipped", answer)

    def test_extract_dozer_records_accepts_common_payload_shapes(self):
        self.assertEqual([{"id": 1}], extract_dozer_records([{"id": 1}]))
        self.assertEqual(
            [{"id": 2}], extract_dozer_records({"records": [{"record": {"id": 2}}]})
        )
        self.assertEqual([{"id": 3}], extract_dozer_records({"data": [{"id": 3}]}))

    def test_dozer_config_declares_all_fixture_sources(self):
        config_path = Path(__file__).resolve().parents[1] / "dozer-config.yaml"
        config = config_path.read_text(encoding="utf-8")

        for table_name in (
            "customer_profiles",
            "accounts",
            "transactions",
            "card_products",
            "customer_spending_profile",
        ):
            self.assertIn(table_name, config)


if __name__ == "__main__":
    unittest.main()
