# STEALTH_TRIAGE_20260930 — v0 (first triage of the mined-findings haul)

**Scope:** `watch/inbox/STEALTH_MINED_FINDINGS.jsonl`, rows with `ts` starting `2026-09-30` (UTC).
**Method:** repo venv, JSON parsed (429 rows total: 09-28=154, 09-29=153, **09-30=122**); answer files byte-checked (all 12 present, `watch/inbox/burn_reset_20260927/work/`); repo claims spot-verified against `mag/` + `tools/` bytes. Ribs loaded for law-contrast: `memory/rib/RIB_FREE_USAGE_POLICY_20260823.md`, `memory/rib/RIB_DRIVING_LADDER_20260928.md`.
**Register status:** no "MINED findings register" exists anywhere under `memory/` (grepped: `mined`, `findings register`, `MINED_FINDINGS`). **This doc is v0 of the register.** The JSONL's own note admits the gap: "no percolator/quantizer ingester exists, so the old note named modules that never read this file" (x92 rows). This triage is the missing consumer.

## 1. Shape of today's haul (dedupe + classification)

- **Cadence:** 00:00–18:43 UTC, 4–8 rows/hour every hour, no gap >1h — the "findings every few minutes" claim holds in the bytes.
- **Works (dedupe):** 122 rows collapse to **3 topics × 4 lanes** (12 distinct answer files, overwritten per cycle — the JSONL is the only history):
  - `w-water-display` 67 rows (last cycle ~12:07)
  - `w-kabbalah-epistemics` 44 rows (last cycle ~18:43)
  - `w-schmidhuber-estate` 11 rows (last cycle ~01:44)
- **Lanes:** openrouter `stealth/space-bunny-alpha` 31 · openrouter `inclusionai/ling-3.0-flash-sante:free` 31 · openrouter `meta/muse-glimmer-30b` 30 · hermes `ling-3.0-flash-sante:free (via nous)` 30.
- **Classes:** model-dispatch intel (all rows carry lane/model/finish/cached_tokens) · cache measurements (cached_tokens per lane) · free-tier behavior (finish/empty/429 evidence) · topic findings (the 12 answer bodies).

## 2. TOP 5 actionable findings (ranked for driving ladder + gps meter)

**F1 — Compression-progress reward is missing from the estate pipeline (judgment-class, repo-verified).**
`w-schmidhuber-estate` hermes lane (last row `2026-09-30T01:26:41Z`, file `w-schmidhuber-estate_hermes.md`): percolator/quantizer/fossil arm run feedforward, no reward anywhere; proposes `log(count)` reward at the REPEAT/NOVEL branch + boredom signal on NOVEL + cross-stage bits-derivative in the quantizer + fossil-arm escalation when the registry outruns pack compression.
Byte-verified: `mag/percolator.py:353` `def _compile_invariant` (finding's cited line range 264-289 has drifted; function real), `EXPLORE_QUEUE = memory/percolator/explore.jsonl` is plain append, `tools/fossil_check.py` is mtime+WARN only, **`memory/percolator/rewards.jsonl` does not exist**. Action: implement on the funded tier; free-lane output stays a proposal.

**F2 — Lane quality ranking for dispatch (feeds `tools/gps_mcp` ledger directly).**
Answer substance by lane (3 works): space-bunny-alpha 6.7/4.4/8.0 KB (structured, most complete) > hermes 6.1/4.2/3.1 KB (verified sources + explicit OWED honesty) > muse-glimmer 1.5/1.8/2.2 KB (generic) > ling:free 1.3/1.6/1.5 KB (terse but honest: "exact titles are not cited here to avoid fabrication").
Action: seed `record_verdict` rows for space-bunny-alpha + hermes on `research_synthesis` shapes; keep ling:free/muse-glimmer at sensing-only shapes.

**F3 — Water-compute STEALABLEs map to live repo code.**
`w-water-display` hermes (row `2026-09-30T11:49:44Z`): graded-head fixed-point dHead for `mag/water_graph.py` (claimed 20 lines, no floats, determinism intact) + siphon-crest primitive as a zero-RNG deterministic sync gate; verified real papers (Adamatzky 2019 Phil Trans, Paik 2012 PNAS, MONIAC 1949, Cardola/Cardona 2024 Euler flows). Both lanes flag "SILL" as hydraulics jargon, not fluidic-logic terminology — `mag/water_graph.py` (387 lines) and `mag/hydro_xor_sim.py` (294 lines) use it uncited. Action: dHead rung is implementable now; rename or cite SILL.

**F4 — Verified NEGATIVE: no formal Kabbalah-framing treatment exists in mech-interp (2023-2026); two lanes converged independently.**
Both hermes (`18:25:00Z`) and space-bunny (`18:30:57Z`) on `w-kabbalah-epistemics`: closest real work is Othello-GPT world representations (Nanda/Hazineh), induction heads (Kissane), syntax/semantics centroid decoupling. Stealable: **centroid ablation** (syntax vs semantics centroids per layer, subtract to decouple) as a cheap local probe. Action: adopt the probe, drop the Kabbalah framing from future asks — 44 rows today re-derived one answer (rib law: N copies collapse to one opinion).

**F5 — Ponytail audit caught a dead citation; audit coverage is thin.**
Row `2026-09-30T17:20:16Z` (space-bunny, kabbalah): `ponytail_audit: {"//transformer-circuits.pub/2021/framework.html": false}` — the Anthropic framework URL check failed; that citation must not propagate. Only 1/122 today-rows carries any ponytail entry (4 all-time). Action: require funded-tier verification (per ladder: banked ≠ verified) before any citation from these files enters corpus/ribs; widen the audit if it's meant to gate.

## 3. CONTRADICTIONS WITH STANDING LAW (flag loudly)

- **C1 — "Free lanes throttle when forced" does NOT hold today.** RIB_FREE_USAGE_POLICY_20260823: "the moment you try to force them, they throttle into empty (429)... substance_chars=0 is the norm." Today: 92 free-lane rows, **100% finish=stop, zero 429/empty rows, 1.3-8.0 KB answers**, sustained ~10-min-per-lane cadence inside a 69+ hour forced mining loop. Caveat before amending the rib: this register may log successes only — check the impfeed error path before rewriting law.
- **C2 — The ~98% cache-hit FROZEN_PREFIX claim is invisible in today's bytes.** Same rib: "~144 reliable parallel agents riding the warm FROZEN_PREFIX (~98% cache-hit)." Measured today: `ling-3.0-flash-sante:free` reports **cached_tokens=0 on all 62 rows** (both openrouter and nous routes); space-bunny mean 147, muse-glimmer mean 77. Either the prefix no longer warms on these models or they don't report cached tokens — either way the meter cannot bank savings it cannot see. Re-measure before trusting cache economics on ling:free.
- **C3 — Alignment confirmed (not a contradiction):** hermes/funded lane produced every verified-content row; free lanes banked findings with explicit OWED — exactly the DRIVING_LADDER sensing/judgment split. But note the ladder's SPEND-THE-MONEY addendum: 92/122 rows were free-lane re-derivations of 3 topics while the judgment rung sat idle after 01:44 (schmidhuber) — fan-out dedupe (n* law) is running hot.

## 4. Register continuation

Next triage: append a dated section to this file (v1+), or promote to `memory/` once an ingester exists (the arch-03 D6 gap named in the rows' own note). Row evidence is addressable as `ts` in `STEALTH_MINED_FINDINGS.jsonl`.
