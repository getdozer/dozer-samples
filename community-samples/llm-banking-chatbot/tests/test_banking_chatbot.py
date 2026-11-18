"""Comprehensive pytest suite for llm-banking-chatbot with a real local HTTP Dozer simulator."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np
import pytest
import yaml
from fastapi.testclient import TestClient

SAMPLE_ROOT = Path(__file__).resolve().parents[1]
if str(SAMPLE_ROOT) not in sys.path:
    sys.path.insert(0, str(SAMPLE_ROOT))

from app.chatbot import BankingChatbot  # noqa: E402
from app.dozer_client import DozerClient  # noqa: E402
from app.dozer_simulator import DozerSimulatorServer  # noqa: E402
from app.server import create_app  # noqa: E402
from app.vector_store import (  # noqa: E402
    CreditCardVectorStore,
    LocalTextEmbedder,
    cosine_similarity,
)

DATA_DIR = SAMPLE_ROOT / "data"


@pytest.fixture(scope="module")
def dozer_sim():
    """Spin up a real local HTTP Dozer endpoint simulator for the test module."""
    with DozerSimulatorServer(DATA_DIR, host="127.0.0.1", port=0) as server:
        yield server


@pytest.fixture()
def dozer_client(dozer_sim: DozerSimulatorServer) -> DozerClient:
    return DozerClient(base_url=dozer_sim.base_url)


@pytest.fixture()
def chatbot(dozer_client: DozerClient) -> BankingChatbot:
    bot = BankingChatbot(dozer_client=dozer_client)
    bot.refresh_catalog()
    return bot


def test_dozer_config_yaml_structure() -> None:
    """Verify dozer-config.yaml defines LocalStorage CSV connections, SQL join, and endpoints."""
    raw_text = (SAMPLE_ROOT / "dozer-config.yaml").read_text(encoding="utf-8")
    # PyYAML SafeLoader does not know custom tags (!LocalStorage, !Table, !CSV); use BaseLoader.
    config = yaml.load(raw_text, Loader=yaml.BaseLoader)

    assert config["app_name"] == "llm-banking-chatbot"
    assert len(config["sources"]) == 3
    assert "INTO customer_profiles" in config["sql"]
    assert "JOIN transactions" in config["sql"]
    endpoint_paths = {ep["path"] for ep in config["endpoints"]}
    assert endpoint_paths == {"/customer_profiles", "/credit_cards"}


def test_csv_datasets_integrity() -> None:
    """Verify customers, transactions, and credit_cards CSV files are non-empty and referentially valid."""
    with (DATA_DIR / "customers.csv").open("r", encoding="utf-8") as fh:
        customers = list(csv.DictReader(fh))
    with (DATA_DIR / "transactions.csv").open("r", encoding="utf-8") as fh:
        transactions = list(csv.DictReader(fh))
    with (DATA_DIR / "credit_cards.csv").open("r", encoding="utf-8") as fh:
        cards = list(csv.DictReader(fh))

    assert len(customers) >= 5
    assert len(transactions) >= 15
    assert len(cards) >= 5

    customer_ids = {c["customer_id"] for c in customers}
    for tx in transactions:
        assert tx["customer_id"] in customer_ids
        assert float(tx["amount"]) > 0.0


def test_dozer_simulator_health_and_credit_cards_http(dozer_client: DozerClient) -> None:
    """Verify real HTTP /health and /credit_cards responses from the Dozer simulator."""
    health = dozer_client.health()
    assert health["status"] == "SERVING"

    cards = dozer_client.list_credit_cards()
    assert len(cards) == 5
    card_ids = {c["card_id"] for c in cards}
    assert "CARD-TRV-01" in card_ids
    assert "CARD-CSH-02" in card_ids


def test_dozer_simulator_unified_customer_profile_aggregation(dozer_client: DozerClient) -> None:
    """Verify Dozer simulator computes exact SQL JOIN + GROUP BY aggregations for C001."""
    profile = dozer_client.get_customer_profile("C001")
    assert profile is not None
    assert profile["full_name"] == "Ayse Yilmaz"
    assert profile["transaction_count"] == 4
    assert profile["total_spend"] == pytest.approx(4230.00, rel=1e-4)
    assert profile["avg_transaction_amount"] == pytest.approx(1057.50, rel=1e-4)
    assert profile["max_transaction_amount"] == pytest.approx(1850.00, rel=1e-4)
    assert profile["top_category"] == "travel"


def test_dozer_simulator_query_filter_and_404(dozer_client: DozerClient) -> None:
    """Verify POST /customer_profiles/query filter and 404 on missing customer."""
    matched = dozer_client.query_customer_profiles({"customer_id": "C002"})
    assert len(matched) == 1
    assert matched[0]["full_name"] == "Mehmet Demir"

    missing = dozer_client.get_customer_profile("C999")
    assert missing is None


def test_local_embedder_unit_norm_and_cosine_bounds() -> None:
    """Verify LocalTextEmbedder produces L2-normalized vectors and valid cosine similarity."""
    embedder = LocalTextEmbedder(dimensions=128)
    v1 = embedder.embed("international airline flights airport lounge travel miles")
    v2 = embedder.embed("supermarket groceries everyday cashback zero annual fee")

    assert v1.shape == (128,)
    assert float(np.linalg.norm(v1)) == pytest.approx(1.0, abs=1e-5)
    assert cosine_similarity(v1, v1) == pytest.approx(1.0, abs=1e-5)
    sim = cosine_similarity(v1, v2)
    assert -1.0 <= sim <= 1.0
    assert sim < 0.8


def test_vector_store_ranks_travel_card_for_traveler(dozer_client: DozerClient) -> None:
    """Verify cosine search ranks Horizon Miles Infinite first for travel-focused affluent profile."""
    store = CreditCardVectorStore()
    store.index_cards(dozer_client.list_credit_cards())
    profile = dozer_client.get_customer_profile("C001")

    matches = store.search(
        query_text="best airline miles and airport lounge travel card",
        customer_profile=profile,
        top_k=3,
    )
    assert len(matches) >= 1
    assert matches[0].card["card_id"] == "CARD-TRV-01"
    assert matches[0].eligible is True
    assert matches[0].similarity_score > 0.0


def test_vector_store_ranks_cashback_card_for_grocery_shopper(dozer_client: DozerClient) -> None:
    """Verify cosine search ranks Everyday Cashback Plus first for grocery/no-fee query."""
    store = CreditCardVectorStore()
    store.index_cards(dozer_client.list_credit_cards())
    profile = dozer_client.get_customer_profile("C002")

    matches = store.search(
        query_text="zero annual fee cashback for supermarket groceries and fuel",
        customer_profile=profile,
        top_k=3,
    )
    assert len(matches) >= 1
    assert matches[0].card["card_id"] == "CARD-CSH-02"


def test_vector_store_enforces_credit_score_and_income_eligibility(dozer_client: DozerClient) -> None:
    """Verify C004 (score 615, income 36k) is filtered out from premium cards."""
    store = CreditCardVectorStore()
    store.index_cards(dozer_client.list_credit_cards())
    profile = dozer_client.get_customer_profile("C004")

    matches = store.search(
        query_text="airline miles lounge travel card",
        customer_profile=profile,
        top_k=5,
        enforce_eligibility=True,
    )
    returned_ids = {m.card["card_id"] for m in matches}
    assert "CARD-TRV-01" not in returned_ids
    assert "CARD-SEC-05" in returned_ids


def test_langchain_chatbot_personalized_recommendation_e2e(chatbot: BankingChatbot) -> None:
    """Verify LangChain BankingChatbot generates a grounded recommendation for C003."""
    res = chatbot.ask("C003", "Which travel card maximizes my airline miles?")
    assert res.profile is not None
    assert res.profile["customer_id"] == "C003"
    assert len(res.recommended_cards) >= 1
    assert res.recommended_cards[0].card["card_id"] == "CARD-TRV-01"
    assert "Zeynep Kaya" in res.answer
    assert "Horizon Miles Infinite" in res.answer
    assert "810" in res.answer


def test_langchain_chatbot_handles_unknown_customer(chatbot: BankingChatbot) -> None:
    """Verify BankingChatbot returns a clear message when customer_id is absent in Dozer."""
    res = chatbot.ask("UNKNOWN-999", "Recommend a card")
    assert res.profile is None
    assert res.recommended_cards == []
    assert "not found" in res.answer.lower()


def test_fastapi_server_chat_and_recommendations_endpoints(chatbot: BankingChatbot) -> None:
    """Verify FastAPI /health, /recommendations/{id}, and /chat with real Dozer simulator."""
    api = create_app(chatbot=chatbot)
    client = TestClient(api)

    health_resp = client.get("/health")
    assert health_resp.status_code == 200
    assert health_resp.json()["status"] == "ok"

    rec_resp = client.get("/recommendations/C005", params={"query": "online shopping rewards"})
    assert rec_resp.status_code == 200
    rec_data = rec_resp.json()
    assert rec_data["customer_id"] == "C005"
    assert rec_data["recommended_cards"][0]["card_id"] == "CARD-SHP-03"

    chat_resp = client.post(
        "/chat",
        json={"customer_id": "C005", "question": "What card is best for my online shopping?"},
    )
    assert chat_resp.status_code == 200
    chat_data = chat_resp.json()
    assert "Elif Sahin" in chat_data["answer"]
    assert chat_data["recommended_cards"][0]["card_id"] == "CARD-SHP-03"

    missing_resp = client.post(
        "/chat",
        json={"customer_id": "C404", "question": "Hello"},
    )
    assert missing_resp.status_code == 404
