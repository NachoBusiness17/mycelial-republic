# SALON GAMES — L2: LAW + ECONOMICS (gpt-oss-120b @ cerebras, 8m31s)

> **Provenance:** lane salon-games-l2 completed 11:44Z but FAILED the file-write step
> (content delivered inline only — second lane to do this tonight; pattern logged).
> Parent persisted the content verbatim below. **One parent correction applied:**
> the lane's K_T3 kill criterion cited a "$500/month budget ceiling" — invented number,
> contradicts the charter's $3/day hard ceiling (~$90/month without operator word).
> Corrected inline below. All other numbers trace to E6 / Lite law as claimed.

## 1. LAW — Game-Build Farm Architecture

The game-build farm must satisfy an **OTel-aligned meter law** enforcing a single
immutable receipt per build-row. The receipt (the *build-row*) is the authoritative
source of truth for cost, caching, and verification; downstream documentation ("riders")
may only reference it.

**Build-row schema** (typed, one row per game build):

```json
{
  "game": "string",                // Human-readable game identifier
  "prefix_sha": "hex64",           // SHA-256 of the immutable L0 prefix (frozen prompt)
  "tokens_cached": "integer",      // Prompt tokens served from cache (≥0)
  "tokens_uncached": "integer",    // Prompt tokens charged as new input (≥0)
  "cost_usd": "float",             // Total USD charged for this build (incl. output)
  "verdict": "enum[PASS|FAIL|KILL]" // Outcome after meter-law evaluation
}
```

**Rail enforcement (must-have):**
1. **Immutability** — `prefix_sha` written once at build-time, never altered.
2. **Receipt-driven billing** — every cost derived from the row's token counts; no
   out-of-band charges.
3. **Meter-grade tagging** — each row carries a grade (`cached`/`uncached`/`output`)
   mapping to OTel `gen_ai.usage.*`.
4. **Audit-hook** — row appended to `/board/meter_readings.jsonl`, cross-referenced by
   `/board/ARCHIVIST_RECEIPTS.jsonl`.

*Riders* may only reference the receipt hash — never prescribe alternative cost
calculations or ad-hoc caching rules.

## 2. ECONOMICS — When to Farm a Game Build

E6-verified Together V4-Flash economics: cached input $0.03/M, uncached $0.14/M,
output $0.28/M.

**Threshold formula (farm if):**

> R > (C_u − C_c) × T_in + C_o × T_out

where R = replay value of the cached prefix (operator time/oversight saved),
T_in = total input tokens, T_out = output tokens. For typical short-output games
(T_out ≈ 0.2M), the right side ≈ $0.07 × T_in; if a cached run saves ≥ $0.10 × T_in
in time or oversight, the farm passes.

## 3. ADVERSARIAL — Rot Modes & Kill Criteria

| # | Rot | Kill criterion |
|---|---|---|
| 1 | **Prefix-drift cache thrash** — L0 prompt patches invalidate cached rows | **K_T2**: any game with tokens_cached < 0.5 × tokens_total on ≥3 successive builds → KILL |
| 2 | **Dead-game accretion** — no shed rule; builds pile up unused | **K_T3**: monthly farm cost_usd exceeds the charter ceiling ($3/day ≈ $90/month absent operator word — parent-corrected from lane's invented $500) while verdicts stay PASS → KILL |
| 3 | **Opaque shape (K_T6)** — receipt can't answer "what was held, when, why" in one line | any row lacking verdict or with mismatched prefix_sha → automatic KILL |

## 4. Q5 VERDICT

**YES.** Anchoring every game build to an immutable, OTel-metered receipt with the
economic threshold tied to real cached-vs-uncached pricing closes the loop on
prompts-as-games. It supplies the WHEN authority (temporal gate) while preserving WHAT
(game rules) and HOW (cached prefix) — sound as long as the two rot-guards
(prefix-drift, dead-game accretion) are actively policed via K_T2/K_T3/K_T6.
