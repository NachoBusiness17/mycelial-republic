---
name: free-resource-scout-cron-20260918
description: Daily free-resource scout automation-8fdc1a77 09:00 (operator-authored prompt verbatim); first pass filed LINKS 256-262; ALERT gemini auth-key migration kills standard keys Sept 2026; NOTE possible duplicate with automation-5affac13 (07:30) from another window — fold or delete one
metadata:
  node_type: memory
  type: project
  originSessionId: sess_c424b80a-5f44-4511-bcdb-8dcec10fdce9
---

Operator dropped a full task spec for a daily free-resource scout (open-weights
models under 30B, free API tiers, free compute programs, open datasets/game
code → file to LINKS.jsonl, writer 'free-resource-scout', end with best-find
paragraph). Created automation-8fdc1a77 daily 09:00 with the prompt verbatim +
house conventions appended.

**DUPLICATION RISK:** lead-check memory says another window armed
automation-5affac13 daily 07:30 for the same purpose — TWO scout crons may
now exist. Fold or delete one at next opportunity.

**First pass findings (LINKS rows filed 2026-09-18):**
- ALERT: Gemini API rejects STANDARD API keys from Sept 2026 — mandatory
  auth-key migration; our gemini-flash lane at silent-death risk until the
  operator regenerates keys in the new format (needs operator hand on console).
- Cerebras free tier: ~1M tokens/day, context capped ~8K, ~5 req/min — fits
  the deliberate-ask signature (frozen prefix + tight tail); candidate
  short-dig lane.
- Free compute for Rocinante Oct-27: NVIDIA Academic Grants (up to 30K H100
  hours), Google Cloud research credits (~$5K), NAIRR/NSF ACCESS, Thunder
  Compute 14-program roundup (~$250K+).
- Local model: Qwen3-Coder 30B MoE (3.3B active, ~19GB Q4_K_M) coding
  leader — local build-janitor upgrade path; gpt-oss family Apache-2.0 on
  Ollama already proven via groq lanes.
- The Google Form link the operator dropped = a fast-inference demand survey
  (Codex Pro raffle); zcode_ai post = our own public harness claim ("strongest
  harness for GLM-5.3", 82.2% at ~$1.98/pass, cited by z.ai's lead).

**Second pass (first scheduled fire, 2026-09-18 09:00; LINKS 263-265):**
- Jev "System One" resurfaced (Latent Space, 2 days old): >100x faster,
  >200x cheaper than small frontier on classification/routing/scoring —
  action filed: benchmark against lane_runner gate_drop heuristics on 100
  real inbox drops, wire behind switchboard if it holds (see
  [[jev-system-one-decision-model-20260916]]).
- DeepSeek newest open-weight release: 180B total with 51B N-gram weight
  pool, efficiency-first (The Register); watch Ollama/OpenRouter availability
  + license before treating as a lane.
- Standing watch sources adopted (replaces one-off searching): GitHub
  awesome-free-models tracker (updated daily-ish), costgoat + teamday
  verified OpenRouter free lists (~21-23 models).
- No ALERT rows today: Groq free tier stable (30 req/min, up to 14,400
  req/day), OpenRouter free steady ~23 models. The gemini auth-key ALERT
  from pass 1 remains OPEN (operator console action).
Related: [[compute-wealth-inventory-20260918]], [[lead-check-v2-steals-ledger-20260916]]

**Reset-day pass (2026-09-20, run in-session on operator prompt; LINKS +7
incl. 2 ALERTs, commit 0e18df07b):**
- **ALERT lane-breaking: NVIDIA NIM purged 82 models** in one sweep (yi-large,
  fuyu-8b, jamba-1.5 + 79 more gone from the build API model list) — the
  nvidia lane needs a full re-probe before any dispatch references it.
- OpenRouter ADDED z-ai/glm-5.3-flashx (paid, not free) — flashx generation
  rolling out to aggregators; watch for a :free variant.
- **Qwen3.6-27B = best Ollama model for most machines** (BenchLM Sept 2026:
  77.2 SWE-bench Verified, 16GB Q4_K_M, single 24GB GPU) — leading candidate
  to upgrade the judgment tier beyond the janitors.
- **Cerebras Cloud swapping Gemma 4 31B → Qwen3.6-27B this month** — makes
  the standing missing-Cerebras-key gap more valuable to fill (fast judgment
  lane pending operator key).
- UNVERIFIED watch-item: Google AI Studio free tier "ending soon" (Facebook
  claim, not Google-confirmed; OmniRoute says free tier still live mid-2026
  with tightened limits). Quarantined, no action.
- Ollama v0.33.1 (Aug 26 2026); six open-weight families cover nearly every
  local use case, free licenses permitting modification/redistribution.
- **GLM reset confirmed ALIVE** (probe call returned "AWAKE"); the 138-task
  deep-read rerun fired uncapped on fresh quota the same morning.
Related: [[compute-wealth-inventory-20260918]], [[lead-check-v2-steals-ledger-20260916]],
[[glm-burn-pre-reset-20260919]]
