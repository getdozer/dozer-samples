#!/usr/bin/env python3
"""
Dozer + LangChain RAG stub for credit-card personalization.

Modes
-----
* fixture (default): reads local CSVs — no Dozer binary, no API key required
* --use-dozer: fetch customer context from Dozer REST (http://localhost:8080)
* --llm: optional ChatOpenAI final answer when OPENAI_API_KEY is set

This is an overnight scaffold: vector retrieval + rerank work offline;
wire-up to a live Dozer process is the morning verification step.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SAMPLE_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = SAMPLE_ROOT / "data"
DEFAULT_DOZER = os.environ.get("DOZER_API_BASE", "http://localhost:8080")


@dataclass
class CustomerContext:
    customer_id: str
    full_name: str
    segment: str
    city: str
    spend_by_category: dict[str, float]
    total_spend: float

    def summary(self) -> str:
        top = sorted(self.spend_by_category.items(), key=lambda x: -x[1])[:3]
        top_s = ", ".join(f"{c}=${v:,.0f}" for c, v in top) or "n/a"
        return (
            f"{self.full_name} ({self.customer_id}), segment={self.segment}, "
            f"city={self.city}, total_spend=${self.total_spend:,.0f}, top=[{top_s}]"
        )


def _csv_rows(table: str) -> list[dict[str, str]]:
    path = DATA_DIR / table / f"{table}.csv"
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def load_fixture_context(customer_id: str) -> CustomerContext:
    profiles = {r["customer_id"]: r for r in _csv_rows("customer_profiles")}
    if customer_id not in profiles:
        raise SystemExit(f"Unknown customer_id={customer_id}")
    p = profiles[customer_id]
    spend: dict[str, float] = defaultdict(float)
    for txn in _csv_rows("transactions"):
        if txn["customer_id"] == customer_id:
            spend[txn["category"]] += float(txn["amount"])
    return CustomerContext(
        customer_id=customer_id,
        full_name=p["full_name"],
        segment=p["segment"],
        city=p["city"],
        spend_by_category=dict(spend),
        total_spend=sum(spend.values()),
    )


def load_dozer_context(customer_id: str, base: str) -> CustomerContext:
    """Fetch unified profile from Dozer REST once the binary is running."""
    try:
        import httpx
    except ImportError as exc:
        raise SystemExit("httpx required for --use-dozer; pip install httpx") from exc

    def get(path: str, params: dict[str, Any] | None = None) -> list[dict]:
        r = httpx.get(f"{base.rstrip('/')}{path}", params=params or {}, timeout=10.0)
        r.raise_for_status()
        payload = r.json()
        # Dozer historically returns {"data": [...]} or a bare list
        if isinstance(payload, dict):
            return payload.get("data") or payload.get("records") or []
        return payload

    profiles = get("/customer_profiles", {"customer_id": customer_id})
    if not profiles:
        # fallback: filter client-side
        profiles = [p for p in get("/customer_profiles") if p.get("customer_id") == customer_id]
    if not profiles:
        raise SystemExit(f"Dozer returned no profile for {customer_id}")
    p = profiles[0]
    spend_rows = [
        row
        for row in get("/customer_spending_profile")
        if row.get("customer_id") == customer_id
    ]
    spend = {row["top_category"]: float(row["total_spend"]) for row in spend_rows}
    return CustomerContext(
        customer_id=customer_id,
        full_name=p.get("full_name", customer_id),
        segment=p.get("segment", "unknown"),
        city=p.get("city", ""),
        spend_by_category=spend,
        total_spend=sum(spend.values()),
    )


def load_card_docs() -> list[dict[str, str]]:
    return _csv_rows("card_products")


def segment_ok(customer_segment: str, min_segment: str) -> bool:
    order = ["student", "mass_market", "mass_affluent", "premium"]
    try:
        return order.index(customer_segment) >= order.index(min_segment)
    except ValueError:
        return True


def keyword_retrieve(question: str, cards: list[dict[str, str]], k: int = 3) -> list[dict[str, str]]:
    q = question.lower()
    scored: list[tuple[int, dict[str, str]]] = []
    for card in cards:
        blob = " ".join(
            [
                card["name"],
                card["reward_categories"],
                card["perk_summary"],
                card["tags"],
            ]
        ).lower()
        score = sum(1 for token in q.replace("?", " ").split() if token and token in blob)
        scored.append((score, card))
    scored.sort(key=lambda x: -x[0])
    return [c for s, c in scored[:k] if s > 0] or [c for _, c in scored[:k]]


def vector_retrieve(question: str, cards: list[dict[str, str]], k: int = 3) -> list[dict[str, str]]:
    """LangChain + Chroma path when deps are installed; else keyword fallback."""
    try:
        from langchain_community.embeddings import FakeEmbeddings
        from langchain_community.vectorstores import Chroma
        from langchain_core.documents import Document
    except Exception:
        return keyword_retrieve(question, cards, k=k)

    docs = [
        Document(
            page_content=(
                f"{c['name']}. Rewards: {c['reward_categories']}. "
                f"{c['perk_summary']}. Tags: {c['tags']}"
            ),
            metadata={"product_id": c["product_id"], "name": c["name"]},
        )
        for c in cards
    ]
    store = Chroma.from_documents(docs, embedding=FakeEmbeddings(size=32))
    hits = store.similarity_search(question, k=k)
    by_id = {c["product_id"]: c for c in cards}
    out = []
    for h in hits:
        pid = h.metadata.get("product_id")
        if pid in by_id:
            out.append(by_id[pid])
    return out or keyword_retrieve(question, cards, k=k)


def rerank_for_customer(
    ctx: CustomerContext,
    candidates: list[dict[str, str]],
    question: str = "",
) -> list[dict[str, str]]:
    top_cats = {c for c, _ in sorted(ctx.spend_by_category.items(), key=lambda x: -x[1])[:3]}
    q_tokens = {t for t in question.lower().replace("?", " ").split() if len(t) > 2}

    def score(card: dict[str, str]) -> float:
        if not segment_ok(ctx.segment, card["min_segment"]):
            return -1.0
        rewards = set(card["reward_categories"].split("|"))
        overlap = float(len(top_cats & rewards))
        blob = f"{card['reward_categories']}|{card['tags']}|{card['name']}".lower()
        q_hit = sum(1.0 for t in q_tokens if t in blob)
        fee = float(card["annual_fee"])
        fee_penalty = 1.0 if fee >= 100000 else (0.2 if fee >= 40000 else 0.0)
        return overlap + 0.75 * q_hit - fee_penalty

    ranked = sorted(candidates, key=score, reverse=True)
    return [c for c in ranked if score(c) >= 0] or ranked


def deterministic_answer(ctx: CustomerContext, question: str, picks: list[dict[str, str]]) -> str:
    if not picks:
        return (
            f"No eligible card for {ctx.full_name} given segment={ctx.segment}. "
            "Ask about everyday cashback or student products."
        )
    best = picks[0]
    return (
        f"For {ctx.summary()}, given question «{question}», "
        f"recommend **{best['name']}** ({best['product_id']}): {best['perk_summary']} "
        f"(annual fee {best['annual_fee']} ARS)."
    )


def maybe_llm_answer(ctx: CustomerContext, question: str, picks: list[dict[str, str]]) -> str | None:
    if not os.environ.get("OPENAI_API_KEY"):
        return None
    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage, SystemMessage
    except Exception:
        return None

    catalog = "\n".join(
        f"- {c['name']}: {c['perk_summary']} (fee={c['annual_fee']})" for c in picks
    )
    llm = ChatOpenAI(model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"), temperature=0)
    msg = llm.invoke(
        [
            SystemMessage(
                content=(
                    "You are a bank product assistant. Use only the provided customer "
                    "context and card candidates. Be concise."
                )
            ),
            HumanMessage(
                content=(
                    f"Customer context:\n{ctx.summary()}\n\n"
                    f"Candidates:\n{catalog}\n\nQuestion: {question}"
                )
            ),
        ]
    )
    return str(msg.content)


def run(customer_id: str, question: str, use_dozer: bool, use_llm: bool, dozer_base: str) -> str:
    ctx = (
        load_dozer_context(customer_id, dozer_base)
        if use_dozer
        else load_fixture_context(customer_id)
    )
    cards = load_card_docs()
    candidates = vector_retrieve(question, cards, k=4)
    picks = rerank_for_customer(ctx, candidates, question=question)
    if use_llm:
        llm_text = maybe_llm_answer(ctx, question, picks)
        if llm_text:
            return llm_text
    return deterministic_answer(ctx, question, picks)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--customer", default="C001")
    parser.add_argument(
        "--question",
        default="Which card is best for travel and dining rewards?",
    )
    parser.add_argument("--use-dozer", action="store_true")
    parser.add_argument("--llm", action="store_true", help="Try ChatOpenAI if key present")
    parser.add_argument("--dozer-base", default=DEFAULT_DOZER)
    args = parser.parse_args(argv)
    print(run(args.customer, args.question, args.use_dozer, args.llm, args.dozer_base))
    return 0


if __name__ == "__main__":
    sys.exit(main())
