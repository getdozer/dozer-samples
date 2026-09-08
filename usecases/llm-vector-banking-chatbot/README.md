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
| Unit tests | `tests/test_rag_chatbot.py` | fixture load, segment gate, keyword/rerank |
| Deps | `app/requirements.txt` | LangChain / Chroma / OpenAI (optional) |
| Demo log | `demo-log.txt` | text capture of live Dozer REST + chatbot (no video yet) |

## Prerequisites

- **Dozer 0.3.x** on `PATH` for the live path (API-era binary with `endpoints`).
  Dozer **≥0.4.0** removed built-in `endpoints` / `dozer-api` — that binary will reject
  this config. See [`SAMPLE_NOTES.md`](./SAMPLE_NOTES.md).
- Python 3.10+
- `protoc` (`protobuf-compiler`) for `dozer build` on 0.3.x
- Optional: `OPENAI_API_KEY` for the ChatOpenAI answer path

## Quick start (offline fixture — no Dozer binary)

```bash
cd usecases/llm-vector-banking-chatbot
python3 app/rag_chatbot.py \
  --customer C001 \
  --question "Which card is best for travel and dining rewards?"
```

Expected shape: a recommendation for **Dozer Travel Signature** grounded in C001's
travel/dining spend.

Student example:

```bash
python3 app/rag_chatbot.py \
  --customer C003 \
  --question "I need a no-fee student card for education"
```

## Live Dozer path (verified on 0.3.0)

```bash
cd usecases/llm-vector-banking-chatbot
rm -rf .dozer
dozer --ignore-pipe build -c dozer-config.yaml
dozer --ignore-pipe run -c dozer-config.yaml
# elsewhere:
python3 -m venv .venv && .venv/bin/pip install -r app/requirements.txt
.venv/bin/python app/rag_chatbot.py --use-dozer --customer C001 \
  --question "Which card is best for travel and dining rewards?"
```

Dozer REST listens at `http://localhost:8080` (override with `--dozer-base` or
`DOZER_API_BASE`). Responses are bare JSON lists; the client filters by `customer_id`.

Optional LLM polish:

```bash
export OPENAI_API_KEY=sk-...
.venv/bin/python app/rag_chatbot.py --use-dozer --llm --customer C001 \
  --question "Which card is best for travel and dining rewards?"
```

## Tests

```bash
cd usecases/llm-vector-banking-chatbot
python3 -m venv .venv && .venv/bin/pip install pytest httpx
.venv/bin/pytest -q tests/test_rag_chatbot.py
```

## APIs exposed (once Dozer 0.3.x is up)

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

See [`SAMPLE_NOTES.md`](./SAMPLE_NOTES.md). Live `dozer run` (0.3.0) + `--use-dozer`
chatbot verified; text demo log attached. **No payout claimed.** Demo *video* and
maintainer confirmation of bounty eligibility remain open. Crowded claim field
(`dozer-samples` #139–#145, etc.).
