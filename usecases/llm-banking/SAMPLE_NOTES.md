# Sample notes — llm-banking (dozer#1690)

## Intent
Ship the credit-card / LLM / vector sample against **current** Dozer shape
(`sources` → `sql` → `sinks`), not the older blog-era REST table endpoints.

Path name is `usecases/llm-banking` on purpose — distinct from the
`*-chatbot` / `*-card-advisor` PRs already open on this repo.

## Verified 2026-09-15 (ET)
Offline path (no Dozer binary, no OpenAI key):

```bash
cd usecases/llm-banking
python3 -m unittest discover -s tests -v
# → 9 tests OK (1 skipped: json_schemas/dozer.json only in getdozer/dozer)
python3 app.py --customer-id cust_002 --no-vector
# → ranks Dozer Travel Signature first
python3 app.py --customer-id cust_003 --no-vector
# → ranks Dozer Starter Secure first
```

Full capture in `demo-output.txt`. `scripts/demo.sh` reproduces the same.

## With Dozer (optional)
```bash
dozer -c dozer-config.yaml build
dozer -c dozer-config.yaml run
```
Dummy sinks prove the pipeline. ClickHouse path is commented in
`dozer-config.yaml` + `docker-compose.yml` if you want a real sink query.

## Claim
`/claim #1690` in the PR body. Cross-link: getdozer/dozer#2511.
