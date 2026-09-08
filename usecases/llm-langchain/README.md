# Dozer + LLM + Vector Database + LangChain

This sample implements the flow from the [LLM chatbot blog post](https://getdozer.io/blog/llm-chatbot): a bank chatbot that hyper-personalizes credit card recommendations.

Dozer sources multiple datasets (customer profiles, transactions, card products) from local CSV files, builds a real-time spending aggregate in SQL, and serves it all as low-latency REST APIs. LangChain embeds the card products into a Chroma vector database and passes the unified customer profile as context to an LLM.

## Prerequisites

- [Dozer](https://getdozer.io/docs/installation)
- Python 3.9 or higher
- An OpenAI API key

## Run

### 1. Install the Python dependencies

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
```

### 2. Start Dozer

```bash
dozer run -c dozer-config.yaml
```

Dozer exposes REST APIs on port 8080: `/customers`, `/transactions`, `/card_products`, and `/customer_spending` (per-customer spending aggregated by category).

### 3. Chat

```bash
python chatbot.py --customer C001 --question "Which card best fits this customer, and why?"
```

The chatbot fetches the customer profile and spending breakdown from Dozer, retrieves the most relevant card products from the Chroma vector store, and asks the LLM for a personalized recommendation.
