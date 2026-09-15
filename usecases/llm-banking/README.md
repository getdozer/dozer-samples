# LLM banking sample (Dozer + LangChain + vector store)

Bank-ish credit card advisor. Dozer pulls profile + txn CSVs, SQL builds a
unified `customer_profile`, sinks it (Dummy by default, ClickHouse optional).
The Python app does retrieval over card docs with Chroma and picks a card.

Matches the old blog use case, against **current** Dozer (sources → sql → sinks).
Dozer no longer ships REST table APIs — the app owns that layer.

## Layout

```
dozer-config.yaml   # LocalStorage CSVs + SQL + Dummy sinks
data/               # profiles, transactions, card products
app.py              # CLI: profile → rank → vector retrieve → answer
load_data.py        # CSV loaders + profile builder (mirrors the SQL)
recommend.py        # offline ranking
vector_rag.py       # Chroma + local hash embeddings
docker-compose.yml  # optional ClickHouse
```

## Quick path (no Dozer binary needed)

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
# optional for real LangChain/Chroma/OpenAI — uncomment lines in requirements.txt
python app.py --customer-id cust_002
python -m unittest discover -s tests -v
```

`cust_002` is travel-heavy — expect Dozer Travel Signature near the top.

## With Dozer

Needs a Dozer binary (build getdozer/dozer or grab a release).

```bash
# from this directory
dozer -c dozer-config.yaml build
dozer -c dozer-config.yaml run
```

Dummy sinks just prove the pipeline. To actually query the sink:

```bash
docker compose up -d
# swap the Dummy sinks for the commented ClickHouse block in dozer-config.yaml
dozer run -c dozer-config.yaml
python app.py --customer-id cust_002 --use-clickhouse
```

## LLM

Set `OPENAI_API_KEY` if you want ChatOpenAI for the final blurb. Without it the
local ranker prints the answer. Fine for CI.

## Why this shape

Tracks getdozer/dozer#1690 (Dozer + vector DB + LangChain, credit-card scenario).
Current Dozer moves data into sinks — so this sample wires that shape instead
of inventing `/customer_profiles` REST endpoints the binary no longer serves.
Same sample also lives on getdozer/dozer#2511 under `examples/llm-banking/`.

## Demo

`demo.mp4` is a short capture of `scripts/demo.sh` / `app.py` on cust_002 and cust_003. Or just run the script yourself.

## Reviewer notes

See `SAMPLE_NOTES.md` for the 2026-09-15 offline verification log and why this path differs from the chatbot-named PRs.
