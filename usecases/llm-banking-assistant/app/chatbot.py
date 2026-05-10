import argparse
import csv
import os
from operator import itemgetter
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Hyper-personalized banking assistant using Dozer, LangChain, and Chroma."
    )
    parser.add_argument("question", help="Question to ask the banking assistant.")
    parser.add_argument("--customer-id", required=True, help="Customer identifier.")
    parser.add_argument(
        "--dozer-url",
        default="http://localhost:8080",
        help="Base URL for the local Dozer REST API.",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        help="OpenAI chat model name.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print assembled context and heuristic recommendations without calling the LLM.",
    )
    return parser.parse_args()


def dozer_query(base_url: str, endpoint: str, filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    try:
        import requests
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "The requests package is required. Install the sample dependencies with "
            "`pip install -r requirements.txt`."
        ) from exc

    payload: dict[str, Any] = {}
    if filters:
        payload["$filter"] = filters

    response = requests.post(f"{base_url.rstrip('/')}/{endpoint}/query", json=payload, timeout=30)
    response.raise_for_status()
    body = response.json()
    records = body.get("records", [])
    normalized: list[dict[str, Any]] = []
    for item in records:
        record = item.get("record", item)
        normalized.append(record)
    return normalized


def fetch_customer_context(base_url: str, customer_id: str) -> dict[str, Any]:
    customer_rows = dozer_query(base_url, "customers", {"customer_id": customer_id})
    if not customer_rows:
        raise ValueError(f"No customer found for {customer_id}")

    context = {
        "customer": customer_rows[0],
        "owned_products": dozer_query(base_url, "customer_products", {"customer_id": customer_id}),
        "spending_summary": dozer_query(base_url, "spending_summary", {"customer_id": customer_id}),
        "transaction_summary": dozer_query(base_url, "transaction_summary", {"customer_id": customer_id}),
        "eligible_cards": dozer_query(base_url, "eligible_cards", {"customer_id": customer_id}),
    }
    return context


def load_cards() -> list[dict[str, str]]:
    cards_path = DATA_DIR / "credit_cards.csv"
    with cards_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def describe_card(row: dict[str, str]) -> str:
    return (
        f"Card Name: {row['card_name']}\n"
        f"Reward Style: {row['reward_style']}\n"
        f"Minimum Income: {row['min_income']}\n"
        f"Annual Fee: {row['annual_fee']}\n"
        f"Key Benefit: {row['key_benefit']}\n"
        f"Description: {row['description']}"
    )


def retrieve_card_knowledge(question: str, context: dict[str, Any]) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    eligible_names = {row["card_name"] for row in context["eligible_cards"]}
    cards = load_cards()

    if not api_key:
        filtered = [row for row in cards if row["card_name"] in eligible_names]
        if not filtered:
            filtered = cards
        return "\n\n".join(describe_card(row) for row in filtered[:3])

    try:
        from langchain_chroma import Chroma
        from langchain_core.documents import Document
        from langchain_openai import OpenAIEmbeddings
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "LangChain, Chroma, and OpenAI dependencies are required for the full LLM flow. "
            "Install them with `pip install -r requirements.txt`, or run with `--dry-run`."
        ) from exc

    documents: list[Document] = [
        Document(
            page_content=describe_card(row),
            metadata={
                "card_id": row["card_id"],
                "card_name": row["card_name"],
                "min_income": row["min_income"],
                "reward_style": row["reward_style"],
            },
        )
        for row in cards
    ]

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=OpenAIEmbeddings(api_key=api_key),
        collection_name="llm-banking-assistant-cards",
    )
    retrieved = vector_store.similarity_search(question, k=4)
    filtered = [doc for doc in retrieved if doc.metadata["card_name"] in eligible_names]
    if not filtered:
        filtered = [doc for doc in documents if doc.metadata["card_name"] in eligible_names]
    return "\n\n".join(doc.page_content for doc in filtered[:3])


def format_lines(lines: list[str]) -> str:
    return "\n".join(lines) if lines else "- none"


def to_float(value: Any) -> float:
    return float(value)


def format_context(context: dict[str, Any]) -> str:
    customer = context["customer"]
    owned_products = sorted(context["owned_products"], key=lambda row: row["product_name"])
    spending_summary = sorted(
        context["spending_summary"],
        key=lambda row: to_float(row["total_amount"]),
        reverse=True,
    )
    transaction_summary = sorted(
        context["transaction_summary"],
        key=lambda row: to_float(row["total_amount"]),
        reverse=True,
    )
    eligible_cards = sorted(
        context["eligible_cards"],
        key=lambda row: (to_float(row["min_income"]), to_float(row["annual_fee"]), row["card_name"]),
    )

    products = format_lines([
        f"- {row['product_name']} ({row['product_type']}), balance={row['balance']}, outstanding_balance={row['outstanding_balance']}, status={row['status']}"
        for row in owned_products
    ])

    spending = format_lines([
        f"- {row['spend_category']}: {row['total_amount']}" for row in spending_summary
    ])

    transactions = format_lines([
        f"- {row['merchant_category']}: count={row['transaction_count']}, total_amount={row['total_amount']}"
        for row in transaction_summary
    ])

    eligible = format_lines([
        f"- {row['card_name']} (min_income={row['min_income']}, annual_fee={row['annual_fee']}, reward_style={row['reward_style']}, key_benefit={row['key_benefit']})"
        for row in eligible_cards
    ])

    return (
        f"Customer ID: {customer['customer_id']}\n"
        f"Name: {customer['first_name']} {customer['last_name']}\n"
        f"Annual Income: {customer['annual_income']}\n"
        f"Address: {customer['address']}\n"
        f"Phone: {customer['phone']}\n\n"
        f"Owned Products:\n{products}\n\n"
        f"Spending Summary:\n{spending}\n\n"
        f"Transaction Summary:\n{transactions}\n\n"
        f"Eligible Cards:\n{eligible}"
    )


def heuristic_shortlist(context: dict[str, Any]) -> list[str]:
    spending_rows = context["spending_summary"]
    eligible_cards = sorted(
        context["eligible_cards"],
        key=lambda row: (to_float(row["min_income"]), to_float(row["annual_fee"]), row["card_name"]),
    )
    if not spending_rows:
        return [row["card_name"] for row in eligible_cards[:2]]

    category_totals = {
        row["spend_category"]: float(row["total_amount"]) for row in spending_rows
    }
    dominant_categories = {
        name
        for name, _ in sorted(
            category_totals.items(), key=lambda item: item[1], reverse=True
        )[:2]
    }

    suggestions: list[str] = []
    for row in eligible_cards:
        reward_style = row["reward_style"]
        card_name = row["card_name"]
        if "travel" in reward_style and ("travel" in dominant_categories or "foreign_spend" in dominant_categories):
            suggestions.append(card_name)
        elif reward_style == "cashback" and (
            "groceries" in dominant_categories
            or "fuel" in dominant_categories
            or "food_and_beverages" in dominant_categories
        ):
            suggestions.append(card_name)
        elif reward_style == "online_rewards" and "online_shopping" in dominant_categories:
            suggestions.append(card_name)

    if not suggestions:
        suggestions = [row["card_name"] for row in eligible_cards[:2]]
    return suggestions[:3]


def build_chain(model_name: str):
    try:
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.runnables import RunnableLambda, RunnableParallel
        from langchain_openai import ChatOpenAI
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "LangChain and OpenAI dependencies are required for the full LLM flow. "
            "Install them with `pip install -r requirements.txt`, or run with `--dry-run`."
        ) from exc

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a virtual bank teller. Use only the supplied customer context and card knowledge. "
                "Recommend only cards listed as eligible. If the user asks about a card that is not eligible, "
                "explain why based on minimum income or fit. Keep the answer practical and personalized.",
            ),
            (
                "human",
                "Customer context:\n{customer_context}\n\n"
                "Card knowledge:\n{card_knowledge}\n\n"
                "Question: {question}\n\n"
                "Answer with a short recommendation, why it fits, and any eligibility caveats.",
            ),
        ]
    )

    llm = ChatOpenAI(model=model_name, temperature=0.2)

    return (
        RunnableParallel(
            {
                "question": itemgetter("question"),
                "customer_context": RunnableLambda(
                    lambda payload: format_context(payload["context"])
                ),
                "card_knowledge": RunnableLambda(
                    lambda payload: retrieve_card_knowledge(payload["question"], payload["context"])
                ),
            }
        )
        | prompt
        | llm
        | StrOutputParser()
    )


def main() -> None:
    args = parse_args()
    context = fetch_customer_context(args.dozer_url, args.customer_id)

    if args.dry_run or not os.getenv("OPENAI_API_KEY"):
        print("Customer context")
        print("================")
        print(format_context(context))
        print("\nHeuristic shortlist")
        print("===================")
        for card_name in heuristic_shortlist(context):
            print(f"- {card_name}")
        print("\nCard knowledge preview")
        print("=====================")
        print(retrieve_card_knowledge(args.question, context))
        if not os.getenv("OPENAI_API_KEY"):
            print(
                "\nOPENAI_API_KEY is not set. Export a key and rerun without --dry-run to execute the full LangChain flow."
            )
        return

    chain = build_chain(args.model)
    answer = chain.invoke({"question": args.question, "context": context})
    print(answer)


if __name__ == "__main__":
    main()
