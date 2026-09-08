# SAMPLE_NOTES — getdozer/dozer#1690

**Branch:** `bounty/1690-llm-vector-banking-scaffold`  
**PR:** https://github.com/getdozer/dozer-samples/pull/144  
**Issue:** https://github.com/getdozer/dozer/issues/1690  
**Bounty:** $250 Algora — Dozer + LLM + Vector DB + LangChain sample  

## Do NOT invent payout success

No maintainer acceptance, no Algora payout confirmation. Multiple competing open PRs
(`dozer-samples` #139–#145 and others). Algora may already show claims/completed —
treat reward eligibility as **uncertain**.

## What works now (verified locally)

| Check | Result |
| --- | --- |
| Offline fixture chatbot | OK (C001→Travel Signature, C003→Campus Starter) |
| `dozer build/run` **0.3.0** against `dozer-config.yaml` | OK (`--ignore-pipe`; needs `protoc` + OpenSSL 1.1) |
| REST `GET /customer_profiles`, `/customer_spending_profile`, `/card_products` | 200, bare JSON lists |
| `rag_chatbot.py --use-dozer` | OK after client-side customer filter fix |
| Unit tests `tests/test_rag_chatbot.py` | 7 passed |
| Text demo log | `demo-log.txt` |
| Demo **video** | **Still missing** |

### Commands that succeeded

```text
dozer --ignore-pipe build -c dozer-config.yaml   # dozer 0.3.0
dozer --ignore-pipe run -c dozer-config.yaml
python3 app/rag_chatbot.py --use-dozer --customer C001 --question "Which card is best for travel and dining rewards?"
python3 app/rag_chatbot.py --use-dozer --customer C003 --question "I need a no-fee student card for education"
pytest -q tests/test_rag_chatbot.py               # 7 passed
```

## Config / client fixes in this follow-up

1. Explicit `api.rest` / `api.grpc` host+port (8080 / 50051).
2. Composite PK on `customer_spending_profile`: `customer_id` + `top_category`
   (matches `GROUP BY customer_id, category`).
3. `--use-dozer` no longer trusts `?customer_id=` (0.3 ignores it and would always
   pick the first profile); always filter client-side on bare lists.
4. Document that **Dozer ≥0.4.0 rejects `endpoints`** (`unknown field endpoints`;
   sinks-only era). This sample targets the API-era 0.3.x binary that matches the
   historical LocalStorage samples in this repo.

## Remaining gaps

1. **No demo video** (Algora often wants ≤30s screen capture).
2. **Architecture drift:** issue comments note current main may prefer
   Dozer→sink→app API. This PR intentionally stays on 0.3-style REST endpoints to
   match existing `dozer-samples` patterns; maintainers may ask for a sink rewrite.
3. **Blog URL** `https://getdozer.io/blog/llm-chatbot` still 404 when last checked.
4. **Crowded claims** — many open PRs; confirm with maintainers before banking on $250.
5. Optional Chroma/LangChain path needs `pip install -r app/requirements.txt`; tests
   and live demo use keyword retrieve + fixture/Dozer context without Chroma.

## Confidence

**~0.70** that this is a credible, runnable sample PR after live verify + tests.  
**~0.20** that it wins $250 given competition + possible architecture preference for
sinks — **do not bank on payout**.
