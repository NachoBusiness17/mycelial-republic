# SWAP RUNBOOK — coding-plan → API keys (2026-09-07, pre-exhaustion)

> **[AUDIT-TYPED 2026-09-08]** status: STAGED · claims: the key swap cannot go dark because it fills the dead API-Key lane while coding-plan stays PASS as fallback, with a typed-RESTORE snapshot rollback — SUPPORTED for the probe state and snapshot grounding (live probe 08:19:33Z, 4 files hashed) / UNPROVEN for the swap completion (no PASS receipt in card) · falsifier: a post-paste probe failing while coding-plan also dark, or the registry row/snapshot known_good not landing after a PASS

**Operator order:** "swap to our api keys before our pro runs out completely... we have api key
usage just for this. i'll gladly pay to keep 5.3 flash running full steam." Sanctioned spend.

**Live truth at probe 08:19:33Z (python -m mag.auth_switchboard status):**
- `builtin:zai-coding-plan` — PASS HTTP 200 (the burning "pro" lane; stays untouched = fallback)
- `builtin:zai` (API Key entry) — ENABLED but **FAIL code=1000** — dead key fp cf3e4c0a (len 49)
  still sitting in the slot
- `builtin:zai-start-plan` — disabled (coding_plan_not_entitled) — **the hydrate-trace landmine,
  do not touch**
- family selected key in setting.json: zai fp 901a03288a6a (len 35) — distinct from the dead
  entry key; may be the funded key the operator means
- Backup: snapshot `20260907T082019Z_pre_apikey_swap_20260907` (4 files hashed, marker set)

## The operator's three moves (his hand — seats never run `use`)

1. **Fund the slot.** z.ai dashboard → copy the funded API key ("api key usage just for this").
2. **Paste.** Any ZCode window → provider picker → **API Key entry** → replace the dead key.
   Do NOT touch Start Plan; do NOT disconnect Coding Plan (it stays PASS as the safe fallback
   while the API lane verifies — this is the exact mistake that broke window auth on 09-05).
3. **Say "pasted."** Seat re-probes; on PASS: windows point at the API Key lane, registry row
   updated, `snapshot known_good` frozen. Rollback any time:
   `python -m mag.auth_switchboard use pre_apikey_swap_20260907` (typed RESTORE).

## Why this ordering is safe

The live lane never goes dark during the swap — we are FILLING a dead lane, not draining the
live one. Worst case mid-swap: windows stay on coding-plan exactly as now. LAW-15 honored:
the plan's daily quota becomes the reserve instead of the fuel; PAYG takes the burn.

## After PASS (seat's work)

- re-probe + registry row in configs/auth_tracks.yaml (zai-apikey-entry → PASS + date)
- `snapshot known_good` so forever-after is `use known_good`
- quota/clamp reading for the metered keys (LAW-15 pacing guard before any rescue talk)
