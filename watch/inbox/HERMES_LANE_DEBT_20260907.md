# HERMES LANE DEBT — 2026-09-07 (salon S5/S7 HTTP 401, closed headlessly)

**Verdict:** FIXED. Zero operator steps required. The "Nous Portal auth suspect"
was a red herring — the salon lane never touches hermes.exe or Nous OAuth. The
401 was an empty bearer token from a phantom env-var name in salon_runner.py.

## What broke (Supported)

`watch/salon_runner.py` `_hermes()` read `_env("HERMES_API_KEY")`. No such name
exists anywhere: repo `.env` holds `HERMES_API_KEY_1` / `HERMES_API_KEY_2`
(repo convention: keys get `_N` suffixes; mapping per
`mag/hermes_steering.py:56` — `_2` = S:D $220 work budget, `_1` = Nacho $10
petty). `_env()` of a missing key returns `""` →
`Authorization: Bearer ` (empty) → Nous inference API → **HTTP 401**. The lane
was also the only one in `build_lanes()` WITHOUT a key-presence gate
(grok/gemini/cohere/ollama all return None when unarmed) — so S7 got hermes as
a guaranteed-401 primary instead of falling through, and S5 lost its fallback.
Secondary staleness: model was `inclusionai/ling-3.0-flash-fin:free` while the
helm's canonical $0 lane is `inclusionai/ling-3.0-flash-sante:free` (probe:
`-fin` burns its whole token budget on reasoning and returns empty content;
`-sante` replies cleanly).

## Nous Portal OAuth suspect (Disputed as root cause)

- `hermes auth status nous` → "logged out" — that is the **OAuth (Portal) lane
  only**; cosmetic for this debt.
- `hermes auth list` pool: `nous` → "SDD-220-work-budget" (api_key, manual);
  `custom:nous-sdd` → 2 credentials. All present and valid.
- Key/model smoke matrix, direct HTTP, names only, keys never echoed —
  **all four candidate keys HTTP 200** on both `-fin` and `-sante` models:
  - repo:HERMES_API_KEY_1 → 200 (-sante: reply "OK")
  - repo:HERMES_API_KEY_2 → 200
  - hermes.env:NOUS_SDD_API_KEY → 200 (-sante: reply "OK")
  - hermes.env:NOUS_NACHO_API_KEY → 200 (-sante: reply "OK")
- No re-add/reset grind needed: the setup card of this morning
  (`watch/HERMES_SETUP_20260907.md`, failed-attempt #3) already receipts that
  the built-in `nous` provider is OAuth-gated regardless of pooled api keys.
  Nothing staged for the operator — **no HERMES_NOUS_FIX file required.**

## Hermes itself (Supported: healthy)

- Default-lane smoke (hermes.exe v0.21.0, config default =
  `inclusionai/ling-3.0-flash-sante:free` @ Nous via `${NOUS_SDD_API_KEY}`):
  `chat -q ... -Q` → `HERMES DEFAULT LANE OK`, exit 0. Only the salon's
  direct-HTTP lane was broken, and only by the key NAME.

## What I fixed (repo-side, backup-first)

`watch/salon_runner.py` `_hermes()`:
1. Key reads `HERMES_API_KEY_2` (S:D work budget) with fallback
   `HERMES_API_KEY_1` — same mapping as the helm organ.
2. Model repointed to `inclusionai/ling-3.0-flash-sante:free`.
3. Added the key-presence gate (lane absent + honest fall-through when
   unarmed, matching every other lane's convention).
4. Comment block records the mapping + the -fin reasoning-burn trap.
- Backup: `watch/salon_runner.py.bak-hermes-401-20260907` (pre-edit bytes).
- No other stale references: repo grep for `HERMES_API_KEY|ling-3.0-flash`
  hits only `mag/hermes_steering.py` (already correct), the HERMES_SETUP card,
  and the INTAKE card.

## Verification

- `build_lanes()` sanity: S5 = [gemini, hermes], S7 = [hermes, groq, ollama].
- Fixed lane, direct: `{'lane': 'hermes/ling', 'secs': 1.0, 'tokens': 44}` → 'OK'.
- Dogfood through the trajectory spine (`python -m mag.bash_local`): envelope
  row `0157a8cd2380971b` (session bl-f3c30461) captured the fixed lane firing —
  output `{'lane': 'hermes/ling', 'secs': 2.1, 'tokens': 43}` → 'OK'.
  `bash_local verify`: all rows valid, chains intact.
- Cost: $0 (BYOK `:free` model; metered smoke = a few dozen tokens of free
  inference, per HERMES_SETUP receipt #2).

## Residual (Unproven → next watch, not this debt)

- If Nous ever rate-limits the free lane mid-salon, S7 falls to groq/ollama and
  S5 stands alone on gemini — existing behavior, unchanged by this fix.
- `-fin` vs `-sante` naming: `-fin` 200s but returns empty content under small
  max_tokens (reasoning eats the budget). If a future lane wants `-fin`, give
  it max_tokens headroom. Not a defect in anything shipped today.
