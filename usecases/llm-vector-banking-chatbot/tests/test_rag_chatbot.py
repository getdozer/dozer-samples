"""Unit tests for the offline fixture / ranking path (no Dozer binary required)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "app"))

from rag_chatbot import (  # noqa: E402
    CustomerContext,
    deterministic_answer,
    keyword_retrieve,
    load_card_docs,
    load_fixture_context,
    rerank_for_customer,
    segment_ok,
)


def test_segment_ok_ordering() -> None:
    assert segment_ok("premium", "student")
    assert segment_ok("student", "student")
    assert not segment_ok("student", "premium")
    assert segment_ok("mass_affluent", "mass_market")


def test_load_fixture_context_c001() -> None:
    ctx = load_fixture_context("C001")
    assert ctx.full_name == "Ava Chen"
    assert ctx.segment == "premium"
    assert ctx.spend_by_category["travel"] == pytest.approx(283000.0)
    assert ctx.total_spend == pytest.approx(364500.0)


def test_load_fixture_unknown_customer() -> None:
    with pytest.raises(SystemExit):
        load_fixture_context("NOPE")


def test_keyword_retrieve_travel() -> None:
    cards = load_card_docs()
    hits = keyword_retrieve("travel dining lounge rewards", cards, k=3)
    assert hits
    assert hits[0]["product_id"] == "P_TRAVEL"


def test_rerank_prefers_travel_for_premium_spender() -> None:
    ctx = load_fixture_context("C001")
    cards = load_card_docs()
    ranked = rerank_for_customer(ctx, cards, question="travel and dining rewards")
    assert ranked[0]["product_id"] == "P_TRAVEL"


def test_rerank_gates_student_away_from_luxury() -> None:
    ctx = load_fixture_context("C003")
    cards = load_card_docs()
    ranked = rerank_for_customer(ctx, cards, question="no-fee student education")
    ids = [c["product_id"] for c in ranked]
    assert "P_LUXURY" not in ids
    assert "P_TRAVEL" not in ids
    assert ranked[0]["product_id"] == "P_STUDENT"


def test_deterministic_answer_mentions_card() -> None:
    ctx = CustomerContext(
        customer_id="C001",
        full_name="Ava Chen",
        segment="premium",
        city="Buenos Aires",
        spend_by_category={"travel": 100.0},
        total_spend=100.0,
    )
    cards = load_card_docs()
    text = deterministic_answer(ctx, "travel?", [cards[0]])
    assert "Dozer Travel Signature" in text
    assert "C001" in text
