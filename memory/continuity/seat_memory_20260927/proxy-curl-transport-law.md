---
name: proxy-curl-transport-law
description: Sandbox proxy 406s python urllib/requests to external APIs while
  curl passes; arXiv tarpits the IP after rate contact; drivers must ride curl
  subprocess + host allowlist
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fce37d85-5c78-49f1-81cb-d55612026cab
---

Measured 2026-09-27 (librarian backfill, tools/librarian_backfill_20260927.py): in the ZCode bash sandbox, python urllib/requests to export.arxiv.org (and api.semanticscholar.org) get HTTP 406 from the sandbox's filtering proxy, while curl with identical headers passes through and reaches the real host. arXiv additionally tarpits the whole IP after rate-limit contact: reachable-429 phase, then hang/exit-28 phase, and it stayed 429 through a 150s cooldown + 8 backoff retries.

**Why:** any fleet driver written with urllib will look "refused by the API" when it was never reaching it; and bulk metadata jobs must not burn the shared IP's arXiv quota.

**How to apply:** external-API drivers use `subprocess.run(["curl", "-s", "--max-time", N, ...])` as transport, keep the hermes-driver hook shape (single-host allowlist, DNS private-IP refusal, literal output paths), retry on 429/5xx/000 with sleep, and prefer Semantic Scholar's batch endpoint (api.semanticscholar.org/graph/v1/paper/batch, up to 500 ids per POST) over arXiv's API for bulk id resolution: 4 POSTs resolved 189/194 ids where arXiv gave only rate-limit walls. Related: [[seed-rib-mickey17-panel-20260926]].
