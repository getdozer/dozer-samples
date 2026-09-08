# Dozer + LLM + Vector DB + LangChain (Banking Chatbot)

Sample for [getdozer/dozer#1690](https://github.com/getdozer/dozer/issues/1690) ($250 Algora).

Inspired by the Dozer hyper-personalization banking chatbot write-up: unify customer
profiles, accounts, and transactions in Dozer, then pass that context into a LangChain
retrieval flow over credit-card products (vector store + optional LLM).

## What this sample includes

| Piece | Path | Role |
| --- | --- | --- |
| Dozer config | `dozer-config.yaml` | LocalStorage CSV sources + spend-profile SQL + REST endpoints |
| Seed data | `data/*/*.csv` | customers, accounts, transactions, card products |
| RAG stub | `app/rag_chatbot.py` | fixture mode (offline) + `--use-dozer` + optional `--llm` |
| Deps | `app/requirements.txt` | LangChain / Chroma / OpenAI (optional) |

## Prerequisites

- [Dozer installed](https://getdozer.io/docs/installation) (`dozer` on `PATH`) for the live path
- Python 3.10+
- Optional: `OPENAI_API_KEY` for the ChatOpenAI answer path

## Quick start (offline fixture — no Dozer binary)

```bash
cd usecases/llm-vector-banking-chatbot
python3 app/rag_chatbot.py \
  --customer C001 \
  --question "Which card is best for travel and dining rewards?"
```

Expected shape: a recommendation for **Dozer Travel Signature** (or another eligible
card) grounded in C001's travel/dining spend.

Student example:

```bash
python3 app/rag_chatbot.py \
  --customer C003 \
  --question "I need a no-fee student card for education"
```

## Live Dozer path

```bash
cd usecases/llm-vector-banking-chatbot
rm -rf .dozer
dozer run -c dozer-config.yaml
# elsewhere:
pip install -r app/requirements.txt
python3 app/rag_chatbot.py --use-dozer --customer C001 \
  --question "Which card is best for travel and dining rewards?"
```

Dozer REST is expected at `http://localhost:8080` (override with `--dozer-base` or
`DOZER_API_BASE`).

Optional LLM polish:

```bash
export OPENAI_API_KEY=sk-...
python3 app/rag_chatbot.py --use-dozer --llm --customer C001 \
  --question "Which card is best for travel and dining rewards?"
```

## APIs exposed (once Dozer is up)

- `GET /customer_profiles`
- `GET /accounts`
- `GET /transactions`
- `GET /card_products`
- `GET /customer_spending_profile` — SQL aggregate used as chatbot context

## Architecture (sample)

```
CSV seeds ──► Dozer LocalStorage ──► SQL spend profile ──► REST/gRPC APIs
                                                                  │
                     LangChain retriever (Chroma / FakeEmbeddings) │
                     + customer-aware rerank ◄─────────────────────┘
                                                                  │
                     deterministic answer  or  ChatOpenAI (--llm)
```

## Status / honesty

See [`SAMPLE_NOTES.md`](./SAMPLE_NOTES.md) for claim template, known gaps (demo video,
live `dozer` binary not exercised in this environment), and morning checklist.
