# ANTHROPIC API STUDY — the frontier lane's operating manual (2026-09-01, filed to corpus/research)

> **[AUDIT-TYPED 2026-09-08]** status: LIVE · claims: Anthropic Message Batches halves bulk cost, count_tokens meters free pre-flight, and the context-management beta is the first adoption — SUPPORTED (retrieved vendor docs, documented sources) · falsifier: vendor changes batch pricing/behavior or endpoints/headers above stop matching platform.claude.com docs

Sources: platform.claude.com/docs/en/api/overview + /api/beta-headers + /about-claude/pricing (retrieved, documented).

## 1. THE API SURFACE (what Claude can do)
| API | endpoint | fleet use |
|---|---|---|
| Messages | POST /v1/messages | the lane core |
| **Message Batches** | POST /v1/messages/batches | **50% cost reduction** — bulk async (the batch lever, Together-parity) |
| **Token Counting** | POST /v1/messages/count_tokens | FREE pre-flight cost checks — the water-gate's metering endpoint |
| Models | GET /v1/models | registry sync |
| Files | POST/GET /v1/files | corpus upload for long-context work |
| Skills | /v1/skills | vendor skills (Excel/PDF/PPT) — the WikiSkill counterpart |

## 2. THE AUTH MAP (shape 4 — final)
```
x-api-key: <key>                      # Console key
anthropic-version: 2023-06-01         # always required
anthropic-workspace-id: wrkspc_...    # REQUIRED for multi-workspace keys
anthropic-beta: <feature-name>        # optional, per-feature gate
```
Key types: standard (workspace-id optional) vs multi-workspace (required) vs Workload Identity Federation tokens (Bearer exchange via POST /v1/oauth/token; workspace selected at token exchange, no header).

## 3. BETA FEATURES (anthropic-beta header)
- **context-management-2025-06-27** — server-side context editing/compaction. THE one to adopt first: vendor-grade answer to our context-incident class.
- Others per-feature in docs; the header pattern: `anthropic-beta: <name-date>`.

## 4. THE BEHAVIORAL MODEL (what the pricing table reveals about how Claude behaves)
- **Cache tiers**: 5m writes (1.25× base), **1h writes (2× base)**, hits at 0.025× (Fable) / 0.10× (Opus) of base input. The 1h tier SOLVES the TTL asymmetry — long sessions hold H without keep-warm.
- **Output is the expensive channel**: $25–50/1M (1–2% of token volume, ~24% of bill on our DeepSeek data). Output discipline (max_tokens, effort levels) outweighs input optimization.
- **Two output price tiers on DS data** ($0.66/$1.32) — if Anthropic mirrors this (reasoning vs final tokens), effort control = 2× lever.
- **Batches at 50%** — the async lever for non-urgent volume.

## 5. FLEET MAPPING (recipe → organ)
| Anthropic pattern | Fleet organ | Note |
|---|---|---|
| Content policy → deterministic JSON rules | Switchboard CLASSIFY | vendor-validated code-as-law |
| Automatic context compaction | NO-SILENT-100% + watchdog | adopt the beta to compare |
| Programmatic tool calling | burst lanes | less token overhead than tool-JSON |
| Tool search w/ embeddings | MODEL_REGISTRY + ask_router | same architecture, vendor-scale |
| Claude Skills | WikiSkill law | same self-activation problem documented |

## 6. BEST-USE DOCTRINE (the Claude lane's role)
1. **Frontier lens** — the salon's adversarial-family seat (first non-open-weights reviewer of our tools/packs).
2. **W3 narrative arm** — 1h cache write holds the 70K static warm for the whole run; input-heavy/short-output = the ideal workload shape.
3. **Matrix anchor row** — the first frontier-family measurement on the gen B rubric.
4. **Cost gates**: $0.50/battery cap; output-discipline (max_tokens tight); batches for bulk; short-output calls only until the effort-tier question is measured.

## 7. OPEN
- workspace-id paste (the wrkspc_ gate) → first probe fires.
- Which output tier is reasoning vs final (measure: same prompt, effort levels, compare usage).
- cache_control port of our frozen-prefix architecture (the r=0.025 experiment — the best economics in the corpus).
