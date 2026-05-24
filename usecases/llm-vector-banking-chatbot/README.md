# Dozer + LLM + Vector Banking Chatbot

This sample turns the banking personalization idea from the Dozer LLM article into a runnable use case:

- Dozer sources multiple CSV datasets: customer profiles, accounts, transactions, and credit card products.
- Dozer exposes raw APIs and an aggregated `customer_spending_profile` API for category-level customer context.
- The Python chatbot reads Dozer APIs, builds a personalized customer prompt, and retrieves relevant card products through a LangChain-compatible vector store.
- The sample also has a deterministic offline fixture mode, so reviewers can verify the core flow without an OpenAI key or a running Dozer process.

## Architecture

```text
CSV customer/account/transaction/product data
        |
        v
Dozer LocalStorage sources + SQL aggregation
        |
        v
REST APIs: customer_profiles, accounts, transactions, card_products, customer_spending_profile
        |
        v
Python chatbot -> LangChain Chroma vector retrieval -> personalized card recommendation
```

## Files

| Path | Purpose |
| --- | --- |
| `dozer-config.yaml` | LocalStorage sources, SQL customer/category spending aggregation, and REST endpoints |
| `data/*.csv` | Deterministic mock banking data for five customers and five card products |
| `app/banking_chatbot.py` | Dozer REST client, customer context builder, LangChain/Chroma integration, offline fallback, and CLI |
| `app/test_banking_chatbot.py` | Fast verification for fixture loading, profile aggregation, recommendation ranking, and Dozer payload parsing |

## Run Dozer

With a local Dozer install:

```bash
cd usecases/llm-vector-banking-chatbot
dozer run -c dozer-config.yaml
```

Once Dozer is running, the REST API is available on `http://localhost:8080`. Example:

```bash
curl -X POST http://localhost:8080/customer_spending_profile/query \
  --header 'Content-Type: application/json' \
  --data-raw '{"$limit": 5}'
```

## Run the Chatbot

Create a virtual environment and install the optional LangChain/vector dependencies:

```bash
cd usecases/llm-vector-banking-chatbot
python3 -m venv app/.venv
app/.venv/bin/python -m pip install -r app/requirements.txt
```

Query Dozer-backed context:

```bash
app/.venv/bin/python app/banking_chatbot.py \
  --use-dozer \
  --customer C001 \
  --question "Which card is best for travel and dining rewards?"
```

For quick verification without Dozer or external services, run the deterministic fixture mode by omitting `--use-dozer`:

```bash
python3 app/banking_chatbot.py \
  --customer C001 \
  --question "Which card is best for travel and dining rewards?"
```

Expected result: Ava Sharma is matched to `Dozer Travel Signature` because her recent profile is travel and dining heavy.

## Optional LLM Layer

The CLI can also ask a hosted model to write the final response after Dozer context and vector retrieval have selected the product shortlist. Copy `.env.example` to `.env`, set `OPENAI_API_KEY`, and pass `--use-llm`:

```bash
app/.venv/bin/python app/banking_chatbot.py \
  --use-dozer \
  --use-llm \
  --customer C001 \
  --question "Which card is best for travel and dining rewards?"
```

If no API key is set, `--use-llm` falls back to the deterministic local recommendation and prints why the LLM layer was skipped. This keeps the sample reviewable without paid API access while still showing the LangChain/OpenAI integration path.

## Verify

```bash
python3 -m unittest discover -s app -p "test_*.py"
python3 -m py_compile app/banking_chatbot.py app/test_banking_chatbot.py
```

The tests intentionally avoid network and paid APIs. They validate the data contract that the Dozer APIs and the LangChain retrieval layer consume.
