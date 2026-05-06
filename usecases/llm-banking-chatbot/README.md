# Hyper-Personalized Banking Chatbot with Dozer, LangChain, and a Vector Database

This sample implements the banking use case from the Dozer LLM chatbot article: Dozer materializes a unified customer profile from multiple datasets, a LangChain pipeline retrieves product and support knowledge from a vector database, and the assistant recommends credit card products with customer-specific context.

The example is intentionally runnable with local seed data first. You can run the assistant in deterministic offline mode for a quick smoke test, then switch it to the Dozer REST API once Dozer is running.

## Architecture

```
CSV datasets
  customers + transactions + card products + FAQ documents
        |
        v
Dozer local storage connector + SQL
        |
        v
REST endpoints:
  /customer-profiles
  /transactions
  /card-products
  /faq-documents
        |
        v
Python assistant
  - fetches customer context from Dozer
  - indexes FAQ/product knowledge with LangChain + Chroma
  - ranks products using customer profile and spend behavior
  - optionally sends the grounded prompt to OpenAI
```

## Files

| File | Purpose |
| --- | --- |
| `dozer-config.yaml` | Dozer local storage config and endpoint definitions |
| `data/` | Local CSV datasets for customers, transactions, products, and FAQ docs |
| `banking_assistant/clients.py` | Dozer REST client plus an offline fixture client |
| `banking_assistant/vector_store.py` | LangChain + Chroma retrieval with deterministic fallback |
| `banking_assistant/recommender.py` | Product ranking and grounded response generation |
| `app.py` | CLI entry point |
| `tests/` | Fast unit tests for recommendation and retrieval behavior |

## Run With Local Fixtures

```bash
cd usecases/llm-banking-chatbot
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python app.py --offline --customer-id 1001 --question "Which credit card should I use for travel and groceries?"
```

This path verifies the LangChain/vector retrieval and recommendation logic without requiring a Dozer binary or an LLM API key.

## Run With Dozer

Install Dozer, then run the config from this directory:

```bash
dozer -c dozer-config.yaml
```

In a second terminal:

```bash
python app.py --customer-id 1001 --question "Which credit card should I use for travel and groceries?"
```

The assistant reads Dozer REST endpoints from `DOZER_REST_URL`, defaulting to `http://localhost:8080`.

## Optional OpenAI Response Generation

By default, the assistant returns a deterministic grounded answer. To generate a natural-language response through LangChain and OpenAI, set:

```bash
export OPENAI_API_KEY=...
export USE_OPENAI_RESPONSE=true
python app.py --customer-id 1001 --question "Should I choose the travel card?"
```

The prompt is grounded with customer profile fields, recent transaction behavior, ranked card products, and retrieved FAQ/product documents.

## Test

```bash
python -m pytest tests
```

## Example Output

```text
Customer: Ana Silva (credit score 742, risk low)
Top recommendation: Horizon Travel Rewards
Reason: strongest match for travel spend, credit score eligibility, and low utilization profile.
Retrieved knowledge:
- Travel rewards card includes 3x points on flights and hotels...
- Customers with low risk and credit score above 700 can request premium cards...
```

