# Personalized Banking Chatbot with Dozer, Local Vector Search, and LangChain

A real-time personalized banking assistant built on **Dozer**, **local cosine-similarity vector search**, and **LangChain**.

Dozer ingests raw customer, transaction, and credit-card CSV streams via `!LocalStorage`, joins and aggregates them in real time using Dozer SQL into a unified `customer_profiles` materialized view, and exposes low-latency REST/gRPC APIs. The chatbot queries Dozer over HTTP, matches eligible credit-card products via local vector similarity search, and synthesizes personalized recommendations with LangChain.

## Architecture

```text
  data/customers.csv    ─┐
  data/transactions.csv ─┼─▶ Dozer SQL (JOIN + GROUP BY) ─▶ /customer_profiles (HTTP)
  data/credit_cards.csv ─┴─▶ Dozer Catalog Endpoint      ─▶ /credit_cards      (HTTP)
                                                                   │
                                                                   ▼
  User Question ──▶ LangChain BankingChatbot ──▶ CreditCardVectorStore (Cosine Similarity + Eligibility)
```

## Project Structure

```text
llm-banking-chatbot/
├── app/
│   ├── __init__.py
│   ├── chatbot.py           # LangChain ChatPromptTemplate + BaseChatModel pipeline
│   ├── dozer_client.py      # HTTP client for Dozer REST endpoints
│   ├── dozer_simulator.py   # Local HTTP Dozer endpoint simulator for dev/testing
│   ├── server.py            # FastAPI server (/health, /recommendations/{id}, /chat)
│   └── vector_store.py      # NumPy cosine similarity vector search + eligibility filter
├── data/
│   ├── customers.csv        # Customer demographics, income, and credit scores
│   ├── transactions.csv     # Customer card transactions across categories
│   └── credit_cards.csv     # Credit card product catalog and eligibility rules
├── tests/
│   └── test_banking_chatbot.py
├── dozer-config.yaml        # Dozer LocalStorage + SQL + REST endpoint configuration
├── docker-compose.yml       # Multi-container setup (Dozer + FastAPI Chatbot)
├── requirements.txt
├── LICENSE
└── README.md
```

## Quick Start

### 1. Run with Docker Compose

```bash
# Optional: set OPENAI_API_KEY to use live OpenAI chat completion instead of local deterministic synthesis
export OPENAI_API_KEY="sk-..."

docker compose up --build
```

- Dozer REST API: `http://localhost:8080` (`/customer_profiles`, `/credit_cards`)
- Chatbot FastAPI server: `http://localhost:8000` (`/chat`, `/recommendations/C001`)

### 2. Run Locally (with Dozer Simulator + Pytest)

```bash
pip install -r requirements.txt
pytest -v
```

### Example Chat Request

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"customer_id": "C001", "question": "Which travel credit card fits my airline spending?"}'
```

## License

MIT License — see [LICENSE](./LICENSE).
