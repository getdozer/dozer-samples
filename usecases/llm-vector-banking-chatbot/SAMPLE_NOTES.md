# SAMPLE_NOTES — getdozer/dozer#1690 overnight scaffold

**Branch:** `bounty/1690-llm-vector-banking-scaffold`  
**Repo:** `getdozer/dozer-samples` (local clone under `/workspace/bounty-night/dozer-samples`)  
**Issue:** https://github.com/getdozer/dozer/issues/1690  
**Bounty:** $250 Algora — Dozer + LLM + Vector DB + LangChain sample  

## Do NOT claim money earned

This overnight work is a **local scaffold + offline smoke only**. No payout, no merged
PR, no maintainer acceptance. Algora currently lists `dozer#1690` under **Completed**
with **2 claims**, while the GitHub issue remains **open** with multiple competing
attempts/PRs (`dozer-samples` #141/#142/#143, `dozer` #2492/#2511, etc.). Treat reward
eligibility as **uncertain** until a maintainer confirms funding + preferred submission.

## What was built tonight

- `usecases/llm-vector-banking-chatbot/` following existing LocalStorage CSV + SQL
  `INTO` + `endpoints` patterns (`connectors/javascript`, `sql/join`, `connectors/local-storage`)
- Four seed datasets + `customer_spending_profile` aggregate in `dozer-config.yaml`
- `app/rag_chatbot.py` stub: fixture CSV mode (verified), `--use-dozer` REST client,
  LangChain/Chroma path with FakeEmbeddings fallback, optional `--llm`
- Root README row linking the usecase
- Local commit(s) on the branch above only (no push)

### Offline smoke (ran)

```text
python3 app/rag_chatbot.py --customer C001 --question "Which card is best for travel and dining rewards?"
python3 app/rag_chatbot.py --customer C003 --question "I need a no-fee student card for education"
python3 -m py_compile app/rag_chatbot.py
```

## Honest gaps (blockers for a real /claim)

1. **No demo video** — Algora guidelines for this bounty require a short demo video in the PR.
2. **No live Dozer binary** in this environment — `dozer run -c dozer-config.yaml` was
   **not** executed; REST payload shapes for `--use-dozer` are best-effort and may need
   tweaks against a real Dozer version.
3. **Blog URL 404** — `https://getdozer.io/blog/llm-chatbot` did not resolve when fetched;
   sample follows the issue text + historical LocalStorage API sample shape.
4. **Architecture drift** — recent issue comments note current Dozer may emphasize sinks
   over built-in data APIs; if maintainers require sink→app-API, config must be adapted.
5. **Crowded claim field** — multiple open PRs/claims already; submitting another without
   maintainer confirmation risks wasted work.
6. **No focused unit tests / CI green against live Dozer** yet.
7. **GitHub auth** for this agent path was deferred (waiting on autorouting#92 auth);
   nothing was pushed or `/attempt`/`/claim` posted.

## /claim template (for morning PR body — only after live verify + video)

```markdown
/claim https://github.com/getdozer/dozer/issues/1690

## Summary
- Add `usecases/llm-vector-banking-chatbot`: Dozer LocalStorage over customer profiles,
  accounts, transactions, and card products; SQL `customer_spending_profile`; REST endpoints.
- LangChain/Chroma (FakeEmbeddings) retrieval + customer-aware rerank; fixture mode and
  `--use-dozer` live mode; optional ChatOpenAI via `--llm`.

## Demo
<!-- attach ≤30s video showing: dozer run + rag_chatbot.py --use-dozer -->

## Verification
- `dozer run -c usecases/llm-vector-banking-chatbot/dozer-config.yaml`
- `python3 usecases/llm-vector-banking-chatbot/app/rag_chatbot.py --use-dozer --customer C001 --question "Which card is best for travel and dining rewards?"`
- `python3 -m py_compile usecases/llm-vector-banking-chatbot/app/rag_chatbot.py`

## Notes
Offline fixture path works without API keys. Live Dozer verified on <version>.
Competing PRs acknowledged; happy to rebase or close if another submission is preferred.
```

Also comment on the issue (if still eligible):

```text
/attempt #1690

Plan: finish live Dozer verification + demo video for the dozer-samples scaffold on
branch bounty/1690-llm-vector-banking-scaffold, then open PR with /claim.
```

## Confidence

**~0.55 / 1.0** that this is a *credible starting PR* after morning polish.  
**~0.20 / 1.0** that it would win the $250 given Completed/2-claims Algora state + many
existing submissions — **do not bank on payout**.

## Left for morning

1. Confirm with `@snork-alt` / maintainers: bounty still funded? prefer `dozer-samples`?
2. Install/run real `dozer` against `dozer-config.yaml`; fix REST parsing if needed.
3. Add a short demo video (screen capture of Dozer boot + chatbot recommendation).
4. Add a few unit tests (fixture load, rerank, segment gate).
5. Open PR from this branch; put `/claim …` in body **only** after (2)+(3).
6. Re-check Algora claim table / competing PRs before posting `/attempt`.
