"""Bank chatbot powered by Dozer REST APIs, LangChain, and a Chroma vector store.

Dozer serves customers, transactions, and a spending aggregate as REST APIs.
This script embeds card products into Chroma and lets an LLM recommend a card
against the unified customer profile fetched from Dozer.
"""

import argparse
import os

import requests
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

DOZER_API = os.environ.get("DOZER_API", "http://localhost:8080")


def fetch_records(endpoint, limit=1000):
    response = requests.get(
        f"{DOZER_API}{endpoint}", params={"$limit": limit}, timeout=30
    )
    response.raise_for_status()
    return response.json().get("records", [])


def build_vector_store(products):
    descriptions = [
        (
            f"{p['product_name']} (annual fee ${p['annual_fee']}, "
            f"min income {p['min_income']}): {p['description']}"
        )
        for p in products
    ]
    return Chroma.from_texts(
        descriptions,
        embedding=OpenAIEmbeddings(),
        collection_name="card_products",
    )


def customer_context(customers, spending, customer_id):
    customer = next(
        (c for c in customers if c["customer_id"] == customer_id), None
    )
    if customer is None:
        raise SystemExit(
            f"Customer {customer_id} not found at the /customers endpoint."
        )
    breakdown = [
        f"{s['category']}: ${s['total_amount']}"
        for s in spending
        if s["customer_id"] == customer_id
    ]
    return (
        f"{customer['name']}, age {customer['age']}, "
        f"income ${customer['income']}, "
        f"spending breakdown: {', '.join(breakdown) or 'no transactions'}"
    )


def main():
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("Set OPENAI_API_KEY before running the chatbot.")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--customer",
        default="C001",
        help="customer id from the Dozer /customers endpoint (default C001)",
    )
    parser.add_argument(
        "--question",
        default="Which card best fits this customer, and why?",
        help="question to ask the LLM about the customer",
    )
    args = parser.parse_args()

    customers = fetch_records("/customers")
    spending = fetch_records("/customer_spending")
    products = fetch_records("/card_products")

    vector_store = build_vector_store(products)
    chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model="gpt-4o-mini", temperature=0),
        retriever=vector_store.as_retriever(search_kwargs={"k": 2}),
    )
    prompt = (
        f"Customer context: "
        f"{customer_context(customers, spending, args.customer)}\n"
        f"Question: {args.question}"
    )
    print(chain.invoke(prompt)["result"])


if __name__ == "__main__":
    main()
