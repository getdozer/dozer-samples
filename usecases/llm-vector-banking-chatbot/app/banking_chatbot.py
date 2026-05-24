from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Optional
from urllib.error import URLError
from urllib.request import Request, urlopen

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DEFAULT_DOZER_BASE_URL = os.getenv("DOZER_BASE_URL", "http://localhost:8080")


@dataclass(frozen=True)
class CustomerContext:
    customer_id: str
    full_name: str
    segment: str
    income_band: str
    loyalty_tier: str
    risk_profile: str
    total_balance: float
    total_spend: float
    spend_by_category: dict[str, float]
    recent_merchants: list[str]

    @property
    def top_category(self) -> str:
        if not self.spend_by_category:
            return "unknown"
        return max(self.spend_by_category.items(), key=lambda item: item[1])[0]

    def prompt_summary(self) -> str:
        category_summary = ", ".join(
            f"{category}: ${amount:.2f}"
            for category, amount in sorted(
                self.spend_by_category.items(), key=lambda item: item[1], reverse=True
            )
        )
        merchants = ", ".join(self.recent_merchants[:5])
        return (
            f"Customer {self.full_name} ({self.segment}, {self.loyalty_tier}) has "
            f"${self.total_balance:.2f} in tracked balances and ${self.total_spend:.2f} "
            f"in recent cardable spend. Spend mix: {category_summary}. "
            f"Recent merchants: {merchants}. Risk profile: {self.risk_profile}."
        )


def read_csv_table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_local_tables(data_dir: Path = DATA_DIR) -> dict[str, list[dict[str, str]]]:
    return {
        "customer_profiles": read_csv_table(data_dir / "customer_profiles.csv"),
        "accounts": read_csv_table(data_dir / "accounts.csv"),
        "transactions": read_csv_table(data_dir / "transactions.csv"),
        "card_products": read_csv_table(data_dir / "card_products.csv"),
    }


def extract_dozer_records(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [record for record in payload if isinstance(record, dict)]
    if not isinstance(payload, dict):
        return []

    candidates = payload.get("records") or payload.get("data") or payload.get("items")
    if candidates is None and "record" in payload:
        candidates = [payload]
    if not isinstance(candidates, list):
        return []

    normalized = []
    for item in candidates:
        if not isinstance(item, dict):
            continue
        record = item.get("record", item)
        if isinstance(record, dict):
            normalized.append(record)
    return normalized


class DozerRestClient:
    def __init__(self, base_url: str = DEFAULT_DOZER_BASE_URL) -> None:
        self.base_url = base_url.rstrip("/")

    def query(self, endpoint: str, limit: int = 1000) -> list[dict[str, Any]]:
        body = json.dumps({"$limit": limit}).encode("utf-8")
        request = Request(
            f"{self.base_url}/{endpoint}/query",
            data=body,
            headers={"content-type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return extract_dozer_records(payload)

    def load_tables(self) -> dict[str, list[dict[str, Any]]]:
        return {
            "customer_profiles": self.query("customer_profiles"),
            "accounts": self.query("accounts"),
            "transactions": self.query("transactions"),
            "card_products": self.query("card_products"),
        }


def amount(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def build_customer_context(
    customer_id: str, tables: dict[str, list[dict[str, Any]]]
) -> CustomerContext:
    customer = next(
        (
            row
            for row in tables["customer_profiles"]
            if row.get("customer_id") == customer_id
        ),
        None,
    )
    if customer is None:
        raise ValueError(f"Unknown customer_id {customer_id!r}")

    account_ids = {
        row["account_id"]
        for row in tables["accounts"]
        if row.get("customer_id") == customer_id
    }
    balances = [
        amount(row.get("balance"))
        for row in tables["accounts"]
        if row.get("customer_id") == customer_id
    ]
    transactions = [
        row
        for row in tables["transactions"]
        if row.get("customer_id") == customer_id or row.get("account_id") in account_ids
    ]

    spend_by_category: dict[str, float] = defaultdict(float)
    merchants = []
    for transaction in transactions:
        category = str(transaction.get("category", "uncategorized")).lower()
        spend_by_category[category] += amount(transaction.get("amount"))
        merchants.append(str(transaction.get("merchant", "")))

    return CustomerContext(
        customer_id=customer_id,
        full_name=str(customer["full_name"]),
        segment=str(customer["segment"]),
        income_band=str(customer["income_band"]),
        loyalty_tier=str(customer["loyalty_tier"]),
        risk_profile=str(customer["risk_profile"]),
        total_balance=sum(balances),
        total_spend=sum(spend_by_category.values()),
        spend_by_category=dict(spend_by_category),
        recent_merchants=[merchant for merchant in merchants if merchant],
    )


def product_text(product: dict[str, Any]) -> str:
    return " ".join(
        str(product.get(field, ""))
        for field in (
            "product_name",
            "reward_categories",
            "eligibility_notes",
            "description",
        )
    )


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


class HashingEmbeddings:
    """Small deterministic embedding adapter compatible with LangChain vector stores."""

    def __init__(self, dimensions: int = 64) -> None:
        self.dimensions = dimensions

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self.embed_query(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        for token in tokenize(text):
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:2], "big") % self.dimensions
            vector[index] += 1.0
        magnitude = math.sqrt(sum(value * value for value in vector))
        if magnitude == 0:
            return vector
        return [value / magnitude for value in vector]


def build_langchain_vector_store(
    products: list[dict[str, Any]], persist_dir: Optional[str] = None
) -> Optional[Any]:
    try:
        from langchain_core.documents import Document
    except ImportError:
        try:
            from langchain.docstore.document import Document
        except ImportError:
            return None

    try:
        from langchain_chroma import Chroma
    except ImportError:
        try:
            from langchain_community.vectorstores import Chroma
        except ImportError:
            return None

    documents = [
        Document(
            page_content=product_text(product),
            metadata={
                "product_id": product["product_id"],
                "product_name": product["product_name"],
            },
        )
        for product in products
    ]
    return Chroma.from_documents(
        documents,
        embedding=HashingEmbeddings(),
        persist_directory=persist_dir,
    )


def product_preference_boost(product: dict[str, Any], context: CustomerContext) -> float:
    categories = set(tokenize(str(product.get("reward_categories", ""))))
    boost = 0.0
    for category, spend in context.spend_by_category.items():
        if category in categories:
            boost += spend / max(context.total_spend, 1.0)

    annual_fee = amount(product.get("annual_fee"))
    if "fee" in context.risk_profile and annual_fee == 0:
        boost += 0.5
    if "travel" in context.risk_profile and "travel" in categories:
        boost += 0.5
    if "student" in context.segment.lower() and "student" in product_text(product).lower():
        boost += 0.75
    return boost


def rank_products(
    products: list[dict[str, Any]],
    context: CustomerContext,
    question: str,
    top_k: int = 3,
) -> list[tuple[float, dict[str, Any]]]:
    query_terms = Counter(tokenize(f"{question} {context.prompt_summary()}"))
    scored = []
    for product in products:
        product_terms = Counter(tokenize(product_text(product)))
        overlap = sum(
            min(count, product_terms[token]) for token, count in query_terms.items()
        )
        score = overlap + product_preference_boost(product, context)
        scored.append((score, product))
    return sorted(scored, key=lambda item: (item[0], item[1]["product_id"]), reverse=True)[
        :top_k
    ]


def select_products(
    products: list[dict[str, Any]],
    context: CustomerContext,
    question: str,
    top_k: int = 3,
    persist_dir: Optional[str] = None,
) -> list[dict[str, Any]]:
    vector_store = build_langchain_vector_store(products, persist_dir)
    if vector_store is not None:
        docs = vector_store.similarity_search(
            f"{question}\n{context.prompt_summary()}",
            k=min(len(products), max(top_k * 2, top_k)),
        )
        by_id = {product["product_id"]: product for product in products}
        selected: list[dict[str, Any]] = []
        seen_ids = set()
        for doc in docs:
            product_id = doc.metadata.get("product_id")
            if product_id in by_id and product_id not in seen_ids:
                selected.append(by_id[product_id])
                seen_ids.add(product_id)
        if selected:
            candidates = selected + [
                product for product in products if product["product_id"] not in seen_ids
            ]
            return [
                product
                for _, product in rank_products(candidates, context, question, top_k)
            ]

    return [product for _, product in rank_products(products, context, question, top_k)]


def render_recommendation(
    context: CustomerContext, question: str, selected_products: list[dict[str, Any]]
) -> str:
    best = selected_products[0]
    alternatives = ", ".join(product["product_name"] for product in selected_products[1:])
    top_category = context.top_category.replace("_", " ")
    return (
        f"Question: {question}\n\n"
        f"Dozer context: {context.prompt_summary()}\n\n"
        f"Recommendation: {best['product_name']} is the strongest fit for "
        f"{context.full_name}. The customer's largest recent spend category is "
        f"{top_category}, and this card is positioned for {best['reward_categories']} "
        f"with an annual fee of ${amount(best['annual_fee']):.0f}.\n\n"
        f"Why it is personalized: {best['description']}\n\n"
        f"Alternatives considered: {alternatives or 'none'}."
    )


def load_dotenv_if_available() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        return

    load_dotenv(Path(__file__).resolve().parents[1] / ".env")


def product_shortlist(selected_products: list[dict[str, Any]]) -> str:
    return "\n".join(
        "- {name}: rewards={rewards}; annual_fee=${fee:.0f}; notes={notes}".format(
            name=product["product_name"],
            rewards=product["reward_categories"],
            fee=amount(product["annual_fee"]),
            notes=product["eligibility_notes"],
        )
        for product in selected_products
    )


def render_with_optional_llm(
    context: CustomerContext,
    question: str,
    selected_products: list[dict[str, Any]],
    use_llm: bool = False,
    model: Optional[str] = None,
) -> str:
    deterministic_answer = render_recommendation(context, question, selected_products)
    if not use_llm:
        return deterministic_answer

    load_dotenv_if_available()
    if not os.getenv("OPENAI_API_KEY"):
        return (
            f"{deterministic_answer}\n\n"
            "LLM layer skipped: set OPENAI_API_KEY to generate final prose through "
            "LangChain. Retrieval, customer context, and ranking still ran locally."
        )

    try:
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_openai import ChatOpenAI
    except ImportError:
        return (
            f"{deterministic_answer}\n\n"
            "LLM layer skipped: install app/requirements.txt to enable LangChain "
            "chat model rendering."
        )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a bank assistant. Recommend one credit card using only the "
                "provided Dozer customer context and retrieved product shortlist. "
                "Keep the answer concise and explain why the choice is personalized.",
            ),
            (
                "human",
                "Question: {question}\n\nCustomer context:\n{context}\n\n"
                "Retrieved products:\n{products}",
            ),
        ]
    )
    chain = prompt | ChatOpenAI(
        model=model or os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0,
    )
    response = chain.invoke(
        {
            "question": question,
            "context": context.prompt_summary(),
            "products": product_shortlist(selected_products),
        }
    )
    return str(getattr(response, "content", response)).strip()


def answer_question(
    customer_id: str,
    question: str,
    use_dozer: bool = False,
    dozer_base_url: str = DEFAULT_DOZER_BASE_URL,
    persist_dir: Optional[str] = None,
    use_llm: bool = False,
    model: Optional[str] = None,
) -> str:
    if use_dozer:
        try:
            tables = DozerRestClient(dozer_base_url).load_tables()
        except (OSError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise RuntimeError(
                "Could not query Dozer REST APIs. Start Dozer first or run with "
                "--offline-fixture for local fixture mode."
            ) from exc
    else:
        tables = load_local_tables()

    context = build_customer_context(customer_id, tables)
    products = tables["card_products"]
    selected = select_products(products, context, question, persist_dir=persist_dir)
    return render_with_optional_llm(context, question, selected, use_llm, model)


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Dozer + LangChain banking chatbot sample"
    )
    parser.add_argument("--customer", default="C001")
    parser.add_argument(
        "--question",
        default="Which card is best for travel and dining rewards?",
    )
    parser.add_argument(
        "--use-dozer",
        action="store_true",
        help="Read context and products from Dozer REST APIs instead of local fixtures.",
    )
    parser.add_argument("--dozer-url", default=DEFAULT_DOZER_BASE_URL)
    parser.add_argument(
        "--persist-dir",
        default=os.getenv("CHROMA_PERSIST_DIR"),
        help="Optional Chroma persistence directory when LangChain dependencies are installed.",
    )
    parser.add_argument(
        "--use-llm",
        action="store_true",
        help="Use LangChain ChatOpenAI for final answer prose when OPENAI_API_KEY is set.",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        help="OpenAI chat model used with --use-llm.",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    print(
        answer_question(
            customer_id=args.customer,
            question=args.question,
            use_dozer=args.use_dozer,
            dozer_base_url=args.dozer_url,
            persist_dir=args.persist_dir,
            use_llm=args.use_llm,
            model=args.model,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
