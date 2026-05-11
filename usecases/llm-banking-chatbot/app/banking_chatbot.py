from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.prompts import ChatPromptTemplate


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


class HashingEmbeddings(Embeddings):
    """Tiny local embedding model for deterministic, keyless demos."""

    dimensions = 64

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)

    def _embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        for token in text.lower().replace(",", " ").replace(".", " ").split():
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            idx = digest[0] % self.dimensions
            vector[idx] += 1.0
        norm = sum(value * value for value in vector) ** 0.5 or 1.0
        return [value / norm for value in vector]


@dataclass
class DozerClient:
    base_url: str

    def query(self, endpoint: str, payload: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        response = requests.post(
            f"{self.base_url.rstrip('/')}/{endpoint}/query",
            json=payload or {},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        records = data.get("records", data if isinstance(data, list) else [])
        return [self._unwrap_record(record) for record in records]

    @staticmethod
    def _unwrap_record(record: Any) -> dict[str, Any]:
        if isinstance(record, dict) and "values" in record:
            return record["values"]
        if isinstance(record, dict):
            return record
        return {"value": record}


def load_product_documents() -> list[Document]:
    with (DATA_DIR / "card_products.csv").open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    documents: list[Document] = []
    for row in rows:
        page_content = (
            f"{row['product_name']} focuses on {row['reward_focus']}. "
            f"Annual fee: ${row['annual_fee_usd']}. "
            f"Minimum credit score: {row['min_credit_score']}. "
            f"APR range: {row['apr_range']}. {row['description']}"
        )
        documents.append(Document(page_content=page_content, metadata=row))
    return documents


def build_product_retriever(chroma_dir: str):
    vector_store = Chroma.from_documents(
        documents=load_product_documents(),
        embedding=HashingEmbeddings(),
        persist_directory=chroma_dir,
        collection_name="credit_card_products",
    )
    return vector_store.as_retriever(search_kwargs={"k": 5})


def rerank_products(
    question: str, context: dict[str, Any], products: list[Document]
) -> list[Document]:
    question_terms = set(question.lower().replace("?", " ").split())
    transactions = context["transactions"]
    spend_by_category: dict[str, float] = {}
    for transaction in transactions:
        category = transaction.get("category", "").lower()
        spend_by_category[category] = spend_by_category.get(category, 0.0) + float(
            transaction.get("amount_usd", 0)
        )

    credit_score = int(context["profile"].get("credit_score", 0))

    def score(product: Document) -> tuple[float, str]:
        metadata = product.metadata
        searchable = (
            f"{metadata['product_name']} {metadata['reward_focus']} "
            f"{metadata['description']}"
        ).lower()
        reward_terms = set(searchable.replace(",", " ").replace(".", " ").split())
        overlap = len(question_terms & reward_terms)
        category_fit = sum(
            amount
            for category, amount in spend_by_category.items()
            if category and category in searchable
        )
        eligible = credit_score >= int(metadata["min_credit_score"])
        eligibility_bonus = 50 if eligible else -100
        return (overlap * 25 + category_fit / 20 + eligibility_bonus, searchable)

    return sorted(products, key=score, reverse=True)[:3]


def fetch_customer_context(client: DozerClient, customer_id: str) -> dict[str, Any]:
    profile = client.query(
        "customer-profile",
        {"$filter": {"customer_id": customer_id}, "$limit": 1},
    )
    transactions = client.query(
        "transactions",
        {
            "$filter": {"customer_id": customer_id},
            "$order_by": {"transaction_date": "desc"},
            "$limit": 5,
        },
    )
    if not profile:
        raise SystemExit(f"No Dozer customer profile found for {customer_id}")
    return {"profile": profile[0], "transactions": transactions}


def load_offline_context(customer_id: str) -> dict[str, Any]:
    def rows(name: str) -> list[dict[str, Any]]:
        with (DATA_DIR / name).open(newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))

    customers = {row["customer_id"]: row for row in rows("customers.csv")}
    accounts = {row["customer_id"]: row for row in rows("accounts.csv")}
    transactions = [
        row for row in rows("transactions.csv") if row["customer_id"] == customer_id
    ]
    if customer_id not in customers:
        raise SystemExit(f"No fixture customer found for {customer_id}")

    total_spend = sum(float(row["amount_usd"]) for row in transactions)
    profile = {
        **customers[customer_id],
        **accounts[customer_id],
        "recent_spend_usd": round(total_spend, 2),
        "recent_transaction_count": len(transactions),
    }
    return {"profile": profile, "transactions": transactions}


def fallback_answer(question: str, context: dict[str, Any], products: list[Document]) -> str:
    profile = context["profile"]
    best = products[0].metadata
    spend_categories = ", ".join(
        sorted({transaction.get("category", "unknown") for transaction in context["transactions"]})
    )
    return (
        f"Recommend {best['product_name']} for {profile['full_name']}. "
        f"The customer is in the {profile['segment']} segment with credit score "
        f"{profile['credit_score']} and recent spend categories: {spend_categories}. "
        f"This matches the question '{question}' because the product focuses on "
        f"{best['reward_focus']} and requires a minimum score of {best['min_credit_score']}."
    )


def llm_answer(question: str, context: dict[str, Any], products: list[Document]) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return fallback_answer(question, context, products)

    from langchain_openai import ChatOpenAI

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a banking product assistant. Use only the provided "
                "Dozer customer context and retrieved card products. Explain why "
                "the recommendation fits and mention any risk or eligibility caveat.",
            ),
            (
                "human",
                "Question: {question}\n\nCustomer context:\n{context}\n\nProducts:\n{products}",
            ),
        ],
    )
    model = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), api_key=api_key)
    chain = prompt | model
    result = chain.invoke(
        {
            "question": question,
            "context": json.dumps(context, indent=2),
            "products": "\n\n".join(product.page_content for product in products),
        }
    )
    return result.content


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("--customer", default="C001")
    parser.add_argument("--question", required=True)
    parser.add_argument(
        "--offline-fixture",
        action="store_true",
        help="Read local CSV fixtures instead of querying a running Dozer API.",
    )
    args = parser.parse_args()

    if args.offline_fixture:
        context = load_offline_context(args.customer)
    else:
        dozer = DozerClient(os.getenv("DOZER_BASE_URL", "http://localhost:8080"))
        context = fetch_customer_context(dozer, args.customer)
    retriever = build_product_retriever(os.getenv("CHROMA_DIR", str(ROOT / ".chroma")))
    retrieved_products = retriever.invoke(
        args.question + " " + json.dumps(context["profile"])
    )
    products = rerank_products(args.question, context, retrieved_products)
    answer = llm_answer(args.question, context, products)

    print("Customer context")
    print(json.dumps(context, indent=2))
    print("\nRecommended products")
    for product in products:
        print(f"- {product.metadata['product_name']}: {product.page_content}")
    print("\nAnswer")
    print(answer)


if __name__ == "__main__":
    main()
