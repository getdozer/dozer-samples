from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from .clients import BankingDataClient
from .vector_store import retrieve_relevant_documents


@dataclass(frozen=True)
class ProductScore:
    product: dict[str, Any]
    score: float
    reasons: list[str]


def build_grounded_answer(client: BankingDataClient, customer_id: str, question: str) -> str:
    customer = find_customer(client.customer_profiles(), customer_id)
    transactions = [tx for tx in client.transactions() if str(tx.get("customer_id")) == str(customer_id)]
    products = client.card_products()
    documents = faq_texts(client.faq_documents(), products)
    retrieved_docs = retrieve_relevant_documents(question, documents, top_k=3)
    ranked = rank_products(customer, transactions, products)
    prompt_context = render_context(customer, transactions, ranked, retrieved_docs, question)

    if os.environ.get("USE_OPENAI_RESPONSE", "").lower() == "true" and os.environ.get("OPENAI_API_KEY"):
        generated = try_openai_response(prompt_context, question)
        if generated:
            return generated

    return deterministic_answer(customer, ranked, retrieved_docs, question)


def find_customer(customers: list[dict[str, Any]], customer_id: str) -> dict[str, Any]:
    for customer in customers:
        if str(customer.get("customer_id")) == str(customer_id):
            return customer
    raise ValueError(f"customer_id {customer_id} was not found")


def rank_products(
    customer: dict[str, Any],
    transactions: list[dict[str, Any]],
    products: list[dict[str, Any]],
) -> list[ProductScore]:
    category_spend: dict[str, float] = {}
    for transaction in transactions:
        category = str(transaction.get("category", "")).lower()
        category_spend[category] = category_spend.get(category, 0.0) + float(transaction.get("amount_eur", 0))
    total_spend = sum(category_spend.values()) or 1.0
    credit_score = int(float(customer.get("credit_score", 0)))
    risk_band = str(customer.get("risk_band", "")).lower()
    scored: list[ProductScore] = []

    for product in products:
        minimum_score = int(float(product.get("min_credit_score", 0)))
        focus = str(product.get("reward_focus", "")).lower()
        annual_fee = float(product.get("annual_fee_eur", 0))
        apr = float(product.get("apr_percent", 99))
        score = 0.0
        reasons: list[str] = []

        if credit_score >= minimum_score:
            score += 40
            reasons.append(f"credit score {credit_score} meets minimum {minimum_score}")
        else:
            score -= 50
            reasons.append(f"credit score {credit_score} is below minimum {minimum_score}")

        if focus in category_spend:
            spend_share = category_spend[focus] / total_spend
            score += 35 * spend_share
            reasons.append(f"reward focus matches {focus}, {spend_share:.0%} of recent spend")
        elif focus == "cashback":
            score += 15
            reasons.append("cashback is a flexible fallback for mixed spend")

        if risk_band == "low":
            score += 10
            reasons.append("low risk profile supports premium product eligibility")
        elif risk_band == "medium":
            score += 5

        score += max(0, 15 - annual_fee / 10)
        score += max(0, 10 - apr / 4)
        scored.append(ProductScore(product=product, score=round(score, 2), reasons=reasons))

    return sorted(scored, key=lambda item: item.score, reverse=True)


def faq_texts(faqs: list[dict[str, Any]], products: list[dict[str, Any]]) -> list[str]:
    faq_docs = [f"{item.get('topic')}: {item.get('content')}" for item in faqs]
    product_docs = [
        f"{item.get('name')}: {item.get('description')} Reward focus: {item.get('reward_focus')}."
        for item in products
    ]
    return faq_docs + product_docs


def render_context(
    customer: dict[str, Any],
    transactions: list[dict[str, Any]],
    ranked: list[ProductScore],
    docs: list[str],
    question: str,
) -> str:
    top_transactions = ", ".join(
        f"{tx.get('category')} {tx.get('amount_eur')} EUR at {tx.get('merchant')}"
        for tx in transactions[:5]
    )
    product_context = "\n".join(
        f"- {item.product.get('name')}: score {item.score}; {'; '.join(item.reasons)}"
        for item in ranked[:3]
    )
    doc_context = "\n".join(f"- {doc}" for doc in docs)
    return (
        f"Question: {question}\n"
        f"Customer: {customer}\n"
        f"Recent transactions: {top_transactions}\n"
        f"Ranked products:\n{product_context}\n"
        f"Retrieved knowledge:\n{doc_context}"
    )


def deterministic_answer(
    customer: dict[str, Any],
    ranked: list[ProductScore],
    docs: list[str],
    question: str,
) -> str:
    best = ranked[0]
    primary_reason = next(
        (reason for reason in best.reasons if reason.startswith("reward focus")),
        best.reasons[0] if best.reasons else "best overall score",
    )
    return "\n".join(
        [
            f"Question: {question}",
            f"Customer: {customer.get('name')} (credit score {customer.get('credit_score')}, risk {customer.get('risk_band')})",
            f"Top recommendation: {best.product.get('name')}",
            f"Reason: {primary_reason}",
            "Retrieved knowledge:",
            *[f"- {doc}" for doc in docs],
        ],
    )


def try_openai_response(context: str, question: str) -> str | None:
    try:
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_openai import ChatOpenAI
    except ImportError:
        return None

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a compliant banking product assistant. Use only the supplied context. "
                "Explain product fit, eligibility, and caveats without making guarantees.",
            ),
            ("human", "Context:\n{context}\n\nQuestion: {question}"),
        ],
    )
    chain = prompt | ChatOpenAI(model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"), temperature=0)
    return str(chain.invoke({"context": context, "question": question}).content)
