# LLM Banking Assistant

This sample implements the bounty idea from `getdozer/dozer#1690`: a hyper-personalized banking assistant that combines:

- Dozer for real-time APIs over multiple customer datasets
- LangChain for orchestration
- Chroma as the vector database for product knowledge
- An LLM for personalized card recommendations

The use case mirrors the Dozer blog post about a virtual bank teller. Customer profile data, owned products, spending behavior, and transactions are exposed through Dozer. Credit card knowledge is embedded into a vector database and retrieved dynamically at question time.

## What this sample shows

- `Dozer` sourcing multiple datasets from local CSV files
- `Dozer SQL` producing precomputed `eligible_cards`, `spending_summary`, and `transaction_summary` views
- `LangChain` fetching customer context from Dozer and combining it with retrieved card knowledge
- `Chroma` storing vectorized product documents for semantic retrieval

## Project structure

```text
usecases/llm-banking-assistant/
├── app/
│   └── chatbot.py
├── data/
│   ├── credit_cards.csv
│   ├── customer_products.csv
│   ├── customers.csv
│   ├── spending.csv
│   └── transactions.csv
├── dozer-config.yaml
└── requirements.txt
```

## Setup

1. Install Dozer by following the official installation guide:
   [https://getdozer.io/docs/installation](https://getdozer.io/docs/installation)

2. Create a Python virtual environment and install the app dependencies:

```bash
cd usecases/llm-banking-assistant
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Export an OpenAI API key if you want the full LLM + embedding flow:

```bash
export OPENAI_API_KEY=your_key_here
export OPENAI_MODEL=gpt-4o-mini
```

`OPENAI_MODEL` is optional. If no API key is set, the sample still works in `--dry-run` mode and prints the fully assembled customer context plus a heuristic shortlist.

## Run Dozer

Start Dozer from this directory:

```bash
dozer run
```

This exposes the following APIs:

- `POST /customers/query`
- `POST /customer_products/query`
- `POST /spending/query`
- `POST /transactions/query`
- `POST /eligible_cards/query`
- `POST /spending_summary/query`
- `POST /transaction_summary/query`

## Run the chatbot

Ask which card fits a specific customer:

```bash
python app/chatbot.py \
  --customer-id CUST-001 \
  "Which credit card fits me best for travel and groceries?"
```

Compare another customer with a lower income:

```bash
python app/chatbot.py \
  --customer-id CUST-002 \
  "Recommend the best cashback card I qualify for."
```

Preview the assembled context without calling the LLM:

```bash
python app/chatbot.py \
  --customer-id CUST-001 \
  --dry-run \
  "Which card should I choose?"
```

## How it works

1. Dozer ingests multiple banking datasets from `data/*.csv`.
2. Dozer computes:
   - `eligible_cards` by joining customers to cards on `annual_income >= min_income`
   - `spending_summary` by aggregating spend per category
   - `transaction_summary` by aggregating recent purchases per merchant category
3. The LangChain app fetches those views from Dozer at runtime.
4. Credit card descriptions are loaded into a Chroma vector database and semantically retrieved against the user question.
5. The LLM receives both:
   - structured customer context from Dozer
   - unstructured product knowledge from the vector store

This keeps personalized customer state in Dozer while using vector search only for general product knowledge.

## Example questions

- `Which travel card should I choose given my current income and spending?`
- `Do I qualify for the premium card?`
- `Which card is better for groceries and fuel?`
- `Which eligible card gives me the best fit based on my recent transactions?`

## Notes

- The dataset is intentionally small so reviewers can inspect the full flow quickly.
- Chroma is used as the vector database because it keeps the sample lightweight.
- The `eligible_cards` view demonstrates that Dozer can enforce simple business rules before the LLM step.
