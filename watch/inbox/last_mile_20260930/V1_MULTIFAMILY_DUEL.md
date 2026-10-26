# V1 - MULTIFAMILY DUEL: first multi-family calibration of the meter (2026-09-30)

Lane: last_mile_20260930. Ownership: this receipt + the 18 `v1mf-*` rows in
`logs/duel/duels.jsonl` + driver `watch/inbox/last_mile_20260930/v1_multifamily_duel.py`
+ contender cache `v1_contenders_20260930.jsonl` + run log `v1_run_20260930.log`.
Mission (operator): same 3 adversarial-review asks at 4 families, ember judges
all blind, per-family verdict + cost. Budget $2.00.

## Design

- THE ASK (identical text, 25,962 chars, full `watch/inbox/gps_baseline_ractor_20260929/BASELINE_SPEC.md`
  pasted inline): name the 3 weakest sections (KILL or KEEP-WITH-REWRITE, exact
  failing wording, in-spec evidence) + the 5 most important missing predicates
  (testable checks with falsifying measurement), both ranked by damage. LW9 LAWS
  suffix (no em-dash, path cites, UNPROVEN marks, no praise).
- Families: glm = `z-ai/glm-5.3-prime` via the banked G3 answer (operator: "just
  reuse existing G3 content"; `GOPHER_BURN_output3_healthy_20260929.jsonl`,
  already-paid $0.0264 on 09-29, no new spend). Fresh fires: `x-ai/grok-4.7`,
  `google/gemini-3.8-flash`, `deepseek/deepseek-v4.1-flash` (IDs verified against
  the live /v1/models list, 426 models).
- 3 rounds x 6 pairs round-robin = 18 duels, ember judge (`fireworks/ember-1`)
  blind via `tools/duel_harness.py run_duel` (v1.1 anonymized judge, parity slot
  swap, style fields). Swap pattern landed perfectly alternating
  T/F x 18. Rubric: section coverage, defect severity, evidence citations,
  actionability.

## RESULTS (18/18 banked, 0 UNPARSED, 0 em-dash bytes)

Perfectly transitive, every head-to-head a 3-0 sweep:

| rank | family | W-L | avg criterion (0-5) | contender cost (3 fires) | per answer |
|---|---|---|---|---|---|
| 1 | x-ai/grok-4.7 | 9-0 | 4.92 (36 scores) | $0.6934 | $0.231 |
| 2 | google/gemini-3.8-flash | 6-3 | 4.47 | $0.1299 | $0.043 |
| 3 | deepseek/deepseek-v4.1-flash | 3-6 | 4.33 | $0.0295 | $0.010 |
| 4* | z-ai/glm-5.3-prime (G3 reuse) | 0-9 | 2.67 | $0.0000 new ($0.0264 paid 09-29) | - |

*HANDICAP, not a family verdict: G3 answered a sibling ask (kill/keep each
section + weakest numeric defaults), not this ask; every judge flagged it
("answered a different question / self-invented review task"). glm's 0-9
measures ask-mismatch, not glm quality. Clean signal is the fresh-family
ordering grok > gemini > deepseek. Fresh same-ask glm answers remain OWED DEBT
(same debt LW9 named: glm side from this account's own agents, no Nous glm pay).

## COST (budget $2.00)

- Contender fires: $0.8528 (grok 0.6934 + gemini 0.1299 + ds 0.0295), all
  `usage.cost` metered.
- Judge fires: 18 x avg $0.0399 = $0.7185.
- MISSION TOTAL: $1.5713. Fits cap with $0.43 headroom.
- Unknown server-side billing (client-metered $0): 6 whole-read timeouts (2x300s,
  2x900s grok, runs 1-2) + 5 empty-content SSE attempts, all retried successfully.
- Operator price frame vs meter: grok "$0.77/M CHEAP" is misleading here:
  reasoning tokens bill as output (V9 law) and grok reasons long, so grok was
  the MOST expensive family at $0.23/answer vs gemini $0.043 vs ds $0.010
  (ds "$0.63/M CHEAPEST" confirmed; gemini's short answers beat grok's per-answer
  cost despite the higher per-M rate).

## QUALITATIVE VERDICTS (answers read, not just scores)

- grok-4.7: deepest spec-internal contradiction hunting. r1 kills section 4 via
  the decay-clock flaw (last_verdict_utc refreshed by every gated step, so T4
  staleness cannot fire on hot cells; a 5-verdict probe snaps eff_lb95 back and
  cancels T4). Verified arithmetic, exact quoted wording. Slow (646s/498s) and
  pricey per answer.
- gemini-3.8-flash: best format fidelity + the qualification-impossibility find
  (eff_lb95 decays to the 0.5 prior while threshold is 0.85; a perfect cell
  un-qualifies in ~4.3 days, conflicting with T4's own definition). Compact,
  cheap, fast. The value pick for this shape.
- deepseek-v4.1-flash: sharpest single find (Wilson lb95 computed on RAW
  sample_size while rates are weighted: 100 G3 passes + 1 G0 fail yields lb95
  ~0.904 vs the honest ~0.811, so G3 flooding qualifies a doomed cell; the G3
  cap demands one non-G3 verdict, not one non-G3 pass). Shortest answers,
  cheapest by 4-23x, occasionally shallower on coverage (judges: "correct but
  shallower").
- glm/G3: high-quality adversarial content (its 09-29 review still holds up)
  but off-ask for this instrument; excluded from the clean ranking.

## INCIDENTS (all in v1_run_20260930.log)

1. grok-4.7 cannot answer a 26K-char ask over the harness's non-streaming call:
   4 whole-read timeouts (300s x2, 900s x2), zero-spend aborts. Fix: streaming
   SSE contender caller (params byte-same, per-read 900s socket timeout, usage
   from final chunk), now in the driver. Nous streams also throw intermittent
   empty-content first attempts (5x); the harness retry law (same model, next
   key) absorbed every one.
2. External edit to this driver between write (06:28) and process start
   (06:32:32): FAMS key `gem` renamed `gemini`, PAIRS untouched, so run 3 fired
   and PAID for gemini answers (cached `gemini#rN`) then skipped all gem pairs.
   Fix: key restored + import-time `assert all(f in FAMS for p in PAIRS for f
   in p)` + CACHE_ALIAS so run 4 reused the paid rows (no re-fire). Sibling
   lanes share this directory (w8 rows, aa1_refire, V6-V10 landed during this
   run); the shared `logs/duel/duels.jsonl` stayed clean (ask_id prefixes
   partition the lanes).
3. Run 3 killed externally (exit 137) after caching grok r3 + gemini r3; run 4
   resumed idempotently from cache (only ds r3 re-fired, $0.0162... exact cache
   total $0.8528 governs).

## Meter notes for the router row

- First multi-family calibration: instrument works beyond 2 families; round-robin
  x 3 rounds gave a fully transitive ordering at n=18 with zero UNPARSED.
- Cheap tier is real: deepseek delivered a top-tier find at 1/23rd grok's cost;
  the router's cascade law (cheap first, escalate on evidence) is supported.
- Contender transport must stream for slow reasoners; consider adding a stream
  option to `tools/duel_harness.py` (that file is not this lane's fence).
- Blind-era ledger now 49 rows total; v1mf rows are 18 of them (V8 boundary at
  row 31 documented in V8_DUEL_FINAL.md; w8 sibling rows 32-35 are a different
  series with grok-4.3/qwen3.7-flash).
