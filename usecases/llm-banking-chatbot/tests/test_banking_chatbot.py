#!/usr/bin/env python3
"""Comprehensive unit and integration test suite for usecases/llm-banking-chatbot (#1690)."""

from __future__ import annotations

import json
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, Dict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
APP_DIR = PROJECT_ROOT / "app"
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from banking_chatbot import BankingChatbot, main as cli_main
from dozer_client import (
    DozerClient,
    DozerCustomerProfileTool,
    LocalDozerSQLPipeline,
    load_dozer_config,
)
from vector_store import CardProductVectorStore, DeterministicBankingEmbeddings


class _MockDozerRestHandler(BaseHTTPRequestHandler):
    """Lightweight mock HTTP server emulating Dozer's `POST /{endpoint}/query` and `/count` REST API."""

    pipeline: LocalDozerSQLPipeline

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        payload: Dict[str, Any] = json.loads(raw_body) if raw_body else {}
        filter_dict = payload.get("$filter", {})
        limit = payload.get("$limit")

        if self.path == "/customer_profiles/query":
            rows = self.pipeline.query_endpoint("customer_profiles", filter_dict, limit=limit)
            self._send_json(200, rows)
        elif self.path == "/customer_profiles/count":
            cnt = self.pipeline.count_endpoint("customer_profiles", filter_dict)
            self._send_json(200, {"count": cnt})
        elif self.path == "/category_spending/query":
            rows = self.pipeline.query_endpoint("category_spending", filter_dict, limit=limit)
            self._send_json(200, rows)
        else:
            self._send_json(404, {"error": "Endpoint not found"})

    def _send_json(self, status: int, data: Any) -> None:
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:
        return


class TestDozerBankingChatbotSample(unittest.TestCase):
    """End-to-end verification tests for getdozer/dozer#1690."""

    def test_01_dozer_configs_valid(self) -> None:
        """Verify both local CSV and Postgres Dozer configuration files parse and expose required endpoints."""
        local_cfg = load_dozer_config(PROJECT_ROOT / "dozer-config.yaml")
        self.assertEqual(local_cfg["app_name"], "dozer-llm-banking-chatbot")
        endpoint_names = {ep["name"] for ep in local_cfg["endpoints"]}
        self.assertEqual(
            endpoint_names,
            {
                "customers",
                "credit_accounts",
                "transactions",
                "card_products",
                "customer_profiles",
                "category_spending",
            },
        )

        pg_cfg = load_dozer_config(PROJECT_ROOT / "dozer-config.postgres.yaml")
        self.assertEqual(pg_cfg["app_name"], "dozer-llm-banking-chatbot-pg")
        self.assertEqual(pg_cfg["connections"][0]["config"]["_dozer_tag"], "!Postgres")

    def test_02_seed_datasets_integrity(self) -> None:
        """Verify all four CSV datasets exist, have non-empty rows, and preserve referential integrity."""
        pipeline = LocalDozerSQLPipeline(PROJECT_ROOT)
        customers = pipeline.query_endpoint("customers")
        accounts = pipeline.query_endpoint("credit_accounts")
        txs = pipeline.query_endpoint("transactions")
        products = pipeline.query_endpoint("card_products")

        self.assertEqual(len(customers), 5)
        self.assertEqual(len(accounts), 5)
        self.assertEqual(len(txs), 26)
        self.assertEqual(len(products), 5)

        cust_ids = {c["customer_id"] for c in customers}
        for acc in accounts:
            self.assertIn(acc["customer_id"], cust_ids)
        for tx in txs:
            self.assertIn(tx["customer_id"], cust_ids)

    def test_03_sql_pipeline_joins_and_aggregations(self) -> None:
        """Verify Dozer SQL pipeline accurately joins customers, credit_accounts, and transactions."""
        client = DozerClient(project_root=PROJECT_ROOT, offline_fixture=True)
        ava = client.get_customer_profile("C001")
        self.assertEqual(ava.full_name, "Ava Sharma")
        self.assertEqual(ava.credit_score, 790)
        self.assertEqual(ava.tx_count, 6)
        self.assertAlmostEqual(ava.travel_spend, 2800.00, places=2)
        self.assertAlmostEqual(ava.dining_spend, 575.00, places=2)
        self.assertAlmostEqual(ava.groceries_spend, 185.00, places=2)
        self.assertAlmostEqual(ava.total_spend, 3560.00, places=2)
        self.assertAlmostEqual(ava.utilization_pct, 7.50, places=2)

    def test_04_lookup_by_id_code_and_legacy_alias(self) -> None:
        """Verify customer lookup works by numeric ID (101), code ('C001'), and name alias."""
        client = DozerClient(project_root=PROJECT_ROOT, offline_fixture=True)
        p_id = client.get_customer_profile(101)
        p_code = client.get_customer_profile("C001")
        p_alias = client.get_customer_profile("Alice Johnson")
        self.assertEqual(p_id.customer_id, p_code.customer_id)
        self.assertEqual(p_id.customer_id, p_alias.customer_id)
        with self.assertRaises(KeyError):
            client.get_customer_profile("C999")

    def test_05_langchain_tool_wrapper(self) -> None:
        """Verify `DozerCustomerProfileTool` formats unified profile context for LangChain agents."""
        client = DozerClient(project_root=PROJECT_ROOT, offline_fixture=True)
        tool = DozerCustomerProfileTool(client)
        output = tool.invoke({"customer_id": "C001"})
        self.assertIn("Ava Sharma", output)
        self.assertIn("7.50% utilization", output)
        self.assertIn("Travel=$2,800.00", output)

    def test_06_embeddings_unit_norm_and_retriever(self) -> None:
        """Verify deterministic embeddings are L2-normalized and Retriever interface works."""
        emb = DeterministicBankingEmbeddings()
        vec = emb.embed_query("international flights airport lounge")
        norm_sq = sum(x * x for x in vec)
        self.assertAlmostEqual(norm_sq, 1.0, places=5)

        store = CardProductVectorStore(PROJECT_ROOT / "data" / "card_products.csv")
        retriever = store.as_retriever(search_kwargs={"k": 2})
        docs = retriever.invoke("cashback on groceries and fuel")
        self.assertEqual(len(docs), 2)
        self.assertEqual(docs[0].product_id, "P02")

    def test_07_vector_store_semantic_retrieval(self) -> None:
        """Verify Vector Database ranks credit card brochures accurately by semantic intent."""
        store = CardProductVectorStore(PROJECT_ROOT / "data" / "card_products.csv")

        travel_hits = store.similarity_search_with_score("international airline flights hotel lounge access", k=2)
        self.assertEqual(travel_hits[0][0].product_id, "P01")
        self.assertEqual(travel_hits[0][0].card_name, "Dozer Travel Signature")

        grocery_hits = store.similarity_search_with_score("supermarket groceries wholesale club family fuel cashback", k=2)
        self.assertEqual(grocery_hits[0][0].product_id, "P02")
        self.assertEqual(grocery_hits[0][0].card_name, "Dozer Everyday Cashback+")

        balance_hits = store.similarity_search_with_score("0% intro APR balance transfer debt consolidation high utilization", k=2)
        self.assertEqual(balance_hits[0][0].product_id, "P04")
        self.assertEqual(balance_hits[0][0].card_name, "Dozer Balance Shield 0% APR")

    def test_08_persona_recommendations_and_eligibility(self) -> None:
        """Verify all 5 customer personas receive hyper-personalized, eligibility-checked recommendations."""
        bot = BankingChatbot(project_root=PROJECT_ROOT, offline_fixture=True)

        # C001: Ava Sharma (high travel & dining spend, 790 credit score) -> Dozer Travel Signature
        res_ava = bot.answer("C001", "Which card is best for travel and dining rewards?")
        self.assertEqual(res_ava["recommended_card"], "Dozer Travel Signature")
        self.assertIn("Ava Sharma", res_ava["answer"])

        # C002: Liam Chen (student, 645 credit score, $29k income) -> Dozer Student Rise Cash
        res_liam = bot.answer("C002", "What credit card can I qualify for as a student to earn cashback?")
        self.assertEqual(res_liam["recommended_card"], "Dozer Student Rise Cash")

        # C003: Sofia Martinez (heavy grocery & fuel spender) -> Dozer Everyday Cashback+
        res_sofia = bot.answer("C003", "Which card gives me the highest cashback on groceries and gas?")
        self.assertEqual(res_sofia["recommended_card"], "Dozer Everyday Cashback+")

        # C004: Marcus Johnson (75.56% credit utilization, $6,800 balance at 24.99% APR) -> Dozer Balance Shield 0% APR
        res_marcus = bot.answer("C004", "How can I lower my credit card interest and pay down my balance?")
        self.assertEqual(res_marcus["recommended_card"], "Dozer Balance Shield 0% APR")

        # C005: Priya Patel (self-employed founder spending on AWS cloud, SaaS, coworking) -> Dozer Founders Business Elite
        res_priya = bot.answer("C005", "Best card for cloud computing, software subscriptions, and business travel?")
        self.assertEqual(res_priya["recommended_card"], "Dozer Founders Business Elite")

    def test_09_live_dozer_rest_api_client_integration(self) -> None:
        """Verify `DozerClient` communicates with a live HTTP REST endpoint (`/query` and `/count`)."""
        pipeline = LocalDozerSQLPipeline(PROJECT_ROOT)
        _MockDozerRestHandler.pipeline = pipeline
        server = HTTPServer(("127.0.0.1", 0), _MockDozerRestHandler)
        port = server.server_port
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            bot = BankingChatbot(
                project_root=PROJECT_ROOT,
                dozer_url=f"http://127.0.0.1:{port}",
                offline_fixture=False,
            )
            res = bot.answer(101, "Which travel card should I get?")
            self.assertEqual(res["customer_code"], "C001")
            self.assertEqual(res["recommended_card"], "Dozer Travel Signature")
            cat_rows = bot.dozer_client.get_category_spending(101)
            self.assertEqual(len(cat_rows), 3)
            total_profiles = bot.dozer_client.count_rest("/customer_profiles")
            self.assertEqual(total_profiles, 5)
        finally:
            server.shutdown()
            server.server_close()

    def test_10_realtime_cdc_transaction_shift(self) -> None:
        """Verify that streaming new travel transactions into Dozer dynamically shifts Sofia's recommendation."""
        bot = BankingChatbot(project_root=PROJECT_ROOT, offline_fixture=True)
        initial = bot.answer("C003", "Which card maximizes my rewards based on my recent transactions?")
        self.assertEqual(initial["recommended_card"], "Dozer Everyday Cashback+")

        bot.dozer_client.local_pipeline.insert_realtime_transaction(
            {
                "tx_id": 6001,
                "customer_id": 103,
                "tx_date": "2026-11-03",
                "merchant": "Emirates Airlines",
                "category": "travel",
                "amount": 3200.00,
                "currency": "USD",
                "is_international": "true",
            }
        )
        bot.dozer_client.local_pipeline.insert_realtime_transaction(
            {
                "tx_id": 6002,
                "customer_id": 103,
                "tx_date": "2026-11-04",
                "merchant": "Ritz-Carlton Paris",
                "category": "travel",
                "amount": 2400.00,
                "currency": "EUR",
                "is_international": "true",
            }
        )
        updated_profile = bot.dozer_client.get_customer_profile("C003")
        self.assertAlmostEqual(updated_profile.travel_spend, 5600.00, places=2)
        self.assertEqual(updated_profile.tx_count, 8)
        updated_res = bot.answer("C003", "I just booked international flights and hotels. Which card should I use now?")
        self.assertEqual(updated_res["recommended_card"], "Dozer Travel Signature")

    def test_11_augmented_prompt_contains_both_dozer_and_vector_context(self) -> None:
        """Verify the LangChain prompt injects both Dozer structured metrics and Vector DB unstructured brochures."""
        bot = BankingChatbot(project_root=PROJECT_ROOT, offline_fixture=True)
        res = bot.answer("C001", "Which card is best for travel and dining rewards?")
        prompt = res["prompt"]
        self.assertIn("REAL-TIME UNIFIED CUSTOMER PROFILE (FROM DOZER API)", prompt)
        self.assertIn("RETRIEVED CREDIT CARD PRODUCTS (FROM VECTOR DATABASE)", prompt)
        self.assertIn("Ava Sharma", prompt)
        self.assertIn("Dozer Travel Signature", prompt)

    def test_12_cli_entrypoint_runs_cleanly(self) -> None:
        """Verify CLI entrypoint exits with code 0 in both human-readable and JSON modes."""
        rc1 = cli_main(["--offline-fixture", "--customer", "C001", "--json"])
        self.assertEqual(rc1, 0)
        rc2 = cli_main(["--offline-fixture", "--customer", "C003", "--simulate-realtime-tx"])
        self.assertEqual(rc2, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
