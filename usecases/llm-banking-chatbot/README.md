# Hyper-Personalized Banking Chatbot with Dozer, Vector DB, and LangChain

This sample implements the hyper-personalized banking chatbot architecture described in the [Dozer LLM Chatbot blog post](https://getdozer.io/blog/llm-chatbot) and [getdozer/dozer#1690](https://github.com/getdozer/dozer/issues/1690).

## Architecture Overview

Modern AI banking assistants require both **static unstructured product knowledge** and **real-time structured customer context**:

1. **Dozer Real-Time Data Pipeline (`dozer-config.yaml` / `dozer-config.postgres.yaml`)**:
   - Ingests four datasets across customer accounts and activity:
     - `data/customers.csv`: Demographics, annual income, credit score, employment status, and reward preferences.
     - `data/credit_accounts.csv`: Existing card holdings, current balances, credit limits, APR, and late payment history.
     - `data/transactions.csv`: Multi-category transaction streams (`travel`, `dining`, `groceries`, `fuel`, `online_shopping`, `utilities`).
     - `data/card_products.csv`: Credit card catalog with eligibility thresholds, reward multipliers, and product brochures.
   - Executes streaming SQL joins and aggregations to materialize two low-latency endpoints (REST on port `8080`, gRPC on port `50051`):
     - `/customer_profiles`: Unified customer profile with real-time credit utilization (`utilization_pct`) and per-category spend totals.
     - `/category_spending`: Granular transaction counts and spend per category.
2. **Vector Database (`app/vector_store.py`)**:
   - Indexes the credit card product brochures and reward rules for semantic similarity retrieval (`similarity_search_with_score`), supporting both ChromaDB (`chromadb`) and a deterministic domain-concept + character 3-gram cosine retriever for zero-key offline verification.
3. **LangChain Orchestration (`app/banking_chatbot.py`)**:
   - Queries Dozer's `/customer_profiles` API for the active customer, retrieves matching credit card brochures from the Vector Database, checks credit score and income eligibility, and injects both contexts into the LangChain prompt template (`ChatOpenAI` when `OPENAI_API_KEY` is set, with automatic fallback to a deterministic grounded synthesis engine).

## Directory Layout

```text
usecases/llm-banking-chatbot/
├── README.md
├── requirements.txt
├── .env.example
├── dozer-config.yaml
├── dozer-config.postgres.yaml
├── docker-compose.yml
├── sql/
│   └── init_postgres.sql
├── data/
│   ├── customers.csv
│   ├── credit_accounts.csv
│   ├── transactions.csv
│   └── card_products.csv
├── app/
│   ├── __init__.py
│   ├── dozer_client.py
│   ├── vector_store.py
│   ├── banking_chatbot.py
│   └── requirements.txt
└── tests/
    └── test_banking_chatbot.py
```

## Quick Start

### Option A: Instant Offline Verification (No Docker or API Keys Required)

Run the chatbot using `--offline-fixture`, which parses `dozer-config.yaml`, executes its exact `SELECT ... INTO` SQL transformations over the CSV datasets, queries the vector store, and generates a hyper-personalized recommendation:

```bash
python3 usecases/llm-banking-chatbot/app/banking_chatbot.py \
  --offline-fixture \
  --customer C001 \
  --question "Which card is best for travel and dining rewards?"
```

Simulate a real-time CDC transaction burst (streaming international airline and hotel bookings into Dozer and watching the recommendation dynamically shift from `Dozer Everyday Cashback+` to `Dozer Travel Signature`):

```bash
python3 usecases/llm-banking-chatbot/app/banking_chatbot.py \
  --offline-fixture \
  --customer C003 \
  --simulate-realtime-tx
```

### Option B: Live Dozer Engine + REST API (`localhost:8080`)

1. Start Dozer with the multi-CSV configuration:
   ```bash
   cd usecases/llm-banking-chatbot
   dozer -c dozer-config.yaml
   ```
   Or start PostgreSQL (with `wal_level=logical` CDC) + Dozer via Docker Compose:
   ```bash
   cd usecases/llm-banking-chatbot
   docker compose up -d
   ```

2. Query the Dozer `/customer_profiles` REST endpoint directly:
   ```bash
   curl -X POST http://localhost:8080/customer_profiles/query \
     -H "Content-Type: application/json" \
     -d '{"$filter": {"customer_id": 101}}'
   ```

3. Run the LangChain chatbot against the live Dozer API (optionally setting `OPENAI_API_KEY` for `ChatOpenAI`):
   ```bash
   export OPENAI_API_KEY="sk-..."  # Optional
   python3 app/banking_chatbot.py --customer C001 --question "Which credit card should I apply for to maximize my rewards?"
   ```

## Running the Automated Test Suite

```bash
python3 -m unittest discover -s usecases/llm-banking-chatbot/tests -v
```
