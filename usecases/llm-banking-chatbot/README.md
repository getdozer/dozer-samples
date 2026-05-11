# Dozer + LangChain Banking Chatbot

This sample turns the banking chatbot idea from the Dozer LLM article into a
runnable local demo. Dozer materializes customer, account, transaction, and
credit-card product data as low-latency APIs. A LangChain app then combines:

- a Dozer-backed unified customer profile,
- recent customer transaction context,
- a local Chroma vector index over credit-card products,
- an optional OpenAI chat model, with a deterministic local fallback.

The result is a hyper-personalized card recommendation assistant that can answer
questions such as:

```text
Which credit card should we recommend to customer C001 for travel rewards?
```

## Architecture

```text
CSV files -> Dozer local-storage connector -> REST APIs
                                      |
                                      v
Python LangChain app -> Chroma product vector index -> personalized answer
```

## Files

```text
usecases/llm-banking-chatbot/
  app/
    banking_chatbot.py
    requirements.txt
  data/
    accounts.csv
    card_products.csv
    customers.csv
    transactions.csv
  docker-compose.yml
  dozer-config.yaml
  .env.example
```

## Run Dozer

From this directory:

```bash
docker compose up dozer
```

Dozer exposes REST APIs on `http://localhost:8080`.

Smoke-test the materialized customer profile:

```bash
curl -X POST http://localhost:8080/customer-profile/query \
  --header "Content-Type: application/json" \
  --data-raw "{\"$filter\":{\"customer_id\":\"C001\"},\"$limit\":1}"
```

## Run The Chatbot

In another terminal:

```bash
cd app
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env
```

Optional: add `OPENAI_API_KEY` to `.env`. Without it, the sample still runs with
a deterministic local answer generator so reviewers can verify the data flow.

Ask for a personalized recommendation:

```bash
python banking_chatbot.py \
  --customer C001 \
  --question "Which card is best for travel and dining rewards?"
```

If you want to verify the LangChain/vector path before starting Dozer, use the
offline fixture mode:

```bash
python banking_chatbot.py \
  --offline-fixture \
  --customer C001 \
  --question "Which card is best for travel and dining rewards?"
```

Expected shape of the output:

```text
Customer context
...
Recommended products
...
Answer
...
```

## What Dozer Provides

The Dozer config sources four datasets:

- `customers`
- `accounts`
- `transactions`
- `card_products`

It exposes raw product/transaction APIs plus a joined `customer_profile` endpoint
that is used as live customer context for the LangChain app.

## Verification

The Python module can be syntax-checked without running Dozer:

```bash
python -m py_compile app/banking_chatbot.py
```

Full end-to-end verification:

1. Start Dozer with `docker compose up dozer`.
2. Confirm `customer-profile/query` returns customer `C001`.
3. Run `python app/banking_chatbot.py --customer C001 --question "..."`
4. Confirm the answer cites Dozer customer context and product matches from the
   vector index.
