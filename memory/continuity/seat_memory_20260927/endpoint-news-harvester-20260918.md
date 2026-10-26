---
name: endpoint-news-harvester-20260918
description: Standing endpoint/API news sensor built 2026-09-18
  (scripts/endpoint_news.py, commit 9733cab57) — HN front page + model-churn
  diffing across OpenRouter/Groq/Cerebras/Mistral/NVIDIA; SSRF-hardened; first
  pass already caught new free lanes
metadata:
  node_type: memory
  type: project
  originSessionId: sess_c424b80a-5f44-4511-bcdb-8dcec10fdce9
---

ENDPOINT NEWS HARVESTER built 2026-09-18 on operator directive ("we need to be harvesting all our endpoints and apis for news like nvidia and open router and Hermes as well as hacker news and the equivalent"). `scripts/endpoint_news.py`, commit 9733cab57.

Design: one lean pass = fetch, diff against stored snapshot, append diff rows to watch/inbox/endpoint_news/endpoint_news.jsonl, refresh snapshots. Sources: HN front page (Algolia API, free no-auth), model lists for OpenRouter (public, with :free flag detection), Groq, Cerebras, Mistral, NVIDIA (env keys). SSRF-hardened per Mimosa: https-only, fixed host allowlist, resolved-IP non-global rejection, redirects disabled — this hardening was REQUIRED to pass the Write hook.

Baseline pass results: 35 rows. OpenRouter 446 models / 25 free, including NEW free lanes not yet in the fleet (nex-agi/nex-n2.5-pro + mini free, dots-studio/dots-3-note-preview free, ling-3.0-flash-vl/fin) — lane candidates for the standing drive. HN front page was on-theme same night: OpenJev 524 points (same Jev our VERB DSL steal is built on), Claude Code now reads AGENTS.md, US-military AI hallucinated-intelligence story (cliff-scalar thesis on national news).

**Why:** model-list churn is the cheapest actionable intel in the fleet — new/retired/free models change the tier ladder and lane economics before any news article does.

**How to apply:** run `scripts/endpoint_news.py` as a lean scheduled pass (patrol or standing automation; no context bleed). **Pass 2 (idle bench, commit 7e795dab1): no churn (446/13/46 stable); NVIDIA FIXED — correct key env name is NVIDIA_API_KEY (NVIDIAB_API_KEY did not exist), 82 models now snapshotted; script edited accordingly. Cerebras: NO key exists in root .env or hermes .env — lane stays empty until the operator adds CEREBRAS_API_KEY (flagged to operator).** Hermes/z.ai endpoints not yet wired. Related: [[free-resource-scout-cron-20260918]], [[verb-dsl-rib-language-20260918]], [[lite-free-window-schedule]].
