# U3 — UNION HYDRAULIC SIM (sim kernel for C18's P1–P8)

Lane: physical_computing · wave-lane · worker = stealth/union-alpha (OpenRouter, $0), editor = ZCode
Date: 2026-09-16
Target: pack §3 Tier-$0 stone — the sim side of falsifier §4.5. Spec source: `C18_HYDRAULIC_THIRD_CHANNEL.md` (P1–P8, Appendix B) + `memory/game_modules/water_computer.v1.json` ("The Clear Pipes" hydraulic laws).
Deliverables: `mag/hydro_xor_sim.py` (deterministic tick-based two-bucket XOR simulator, outputs the P1–P8 measured analogs) + `tests/test_hydro_xor_sim.py` (determinism, P self-consistency, XOR truth table).

## Status
- [x] Receipt created first (wave-lane law)
- [x] (1) Read `memory/game_modules/water_computer.v1.json` — laws extracted: mark/tick transfer ("gravity takes a mark each wait"), check valve (no backflow), scripted fault "Open only after water has arrived, or both valves siphon", engine owns heights, DISPUTED anti-pour rule
- [x] (2) union-alpha drafts `mag/hydro_xor_sim.py`
- [x] (3) Editor pass: verify physics vs C18 (orifice discharge, crest 150 mL, prime/dump, read bands), determinism
- [x] (4) `tests/test_hydro_xor_sim.py` + pytest run
- [x] (5) Receipt ends with: test output verbatim + P1–P8 sim-vs-spec table + union-alpha contribution grade

## Log (appended as I go)

- Dispatch 1: union-alpha timed out OpenRouter-side (504, provider 301 s) — no output, no charge.
- Dispatch 2: OK. stealth/union-alpha, 1,897 in / 2,096 out tok, finish=stop, cost $0 (flight_recorder row in `watch/flight_recorder.jsonl`). Draft saved; skeleton (SimParams/SimResult/simulate/truth_table/p_report/main) adopted.
- Editor pass (ZCode), 7 fixes on the draft:
  1. P8 slope was `(w_read − crossing)/(T_read − prime)` — wrong-signed and not a drain slope. Replaced with least-squares slope over the actual primed drain interval, reported as positive drain rate (16.67 mL/s).
  2. P5 checked `max_w_ml <= 130` over ALL cases incl. (1,1), which peaks at the crest (~150) — P5 could never hold. Now filters to single-input cases, per C18's wording.
  3. `all_hold` filtered `locals().items()` by key prefix — matched nothing, so it was vacuously `True`. Replaced with explicit key list.
  4. `w_series` sampled via float `t % 1.0 < dt` (drift-prone) → integer step counter (every 20 steps of dt=0.05).
  5. Valve skew: draft opened B at negative t. Rewritten: signed skew — one valve at t=0, the other at |skew|, BOTH close at TICK_S (fixed trial window).
  6. Inflow now limited by available SOURCE (mass-exact to ~2e-12 mL); SOURCE monotonicity and backflow made real assertion channels instead of clamping artifacts.
  7. Sensor noise (seeded mode) now applied to the reported level only, after mass accounting; inflow noise drawn per line per sub-step.
- **Protocol finding (pre-build, for C18's M7):** under per-valve 60 s pulses (skewed valve closes 5 s late), the trailing valve adds ~8.3 mL AFTER the siphon breaks and (1,1) lands at ~37 mL — outside the pre-registered [0,30] bit-0 band. C18's P7 is only satisfiable under the fixed-window reading (both valves close at T=60; skew shortens the trailer's pulse). The sim implements the fixed window; the physical protocol must pin closing skew as well as opening skew or P7 is ambiguous.
- Sim truth table (noise off): (0,0)→W=0.00 bit 0 · (0,1)→100.00 bit 1 · (1,0)→100.00 bit 1 · (1,1)→prime@44.95 s, W@t_read=26.00, waste 174.00, bit 0. XOR holds. P1–P8 all_hold=True (details in final table below).
- SIPHON_RATE default set to 20.0 mL/s (C18's "20+ mL/s" floor). Sensitivity note: post-break residual ≈ INTAKE_BREAK_ML + (T − prime − drain_time)·inflow_rate, so a faster siphon paradoxically raises the (1,1) residual (more refill time after break). At 22 mL/s it is ~29 mL — inside the band but with <1 mL margin; at 25 mL/s it fails. The (1,1) ≤30 mL band is the tightest pre-registered constraint; the build's siphon must dump 200 mL in ~9–11 s, not faster.

---

## APPENDIX A — pytest output (verbatim)

Command: `.venv\Scripts\python.exe -m pytest tests/test_hydro_xor_sim.py -q`

```
...............                                                          [100%]
15 passed in 0.43s
```

Tests cover the three mission laws: determinism (bit-identical `asdict` equality, same-run and cross-run; seeded noise deterministic per seed, differs from noise-off, never breaks a band or mass balance), P-statement self-consistency (`p_report()["all_hold"]` plus each P individually, P6 residual asserted to <= 1e-6 mL), and the XOR truth table under the pre-registered read bands (plus never-prime on singles, prime <= 90 s + dump on doubles, and a non-default `SimParams` variant).

## APPENDIX B — P1–P8 sim-vs-spec table (the graded contract for the physical build)

Sim: `mag/hydro_xor_sim.py`, defaults (`SimParams()`), noise off, dt = 0.05 s, t_read = 150 s.
Spec: C18 Appendix B, pre-registered 2026-09-16.

| P | Statement (spec) | Sim measured | Hold |
|---|---|---|---|
| P1 | one line, one tick → W gains 100 ± 20 mL | 100.00 mL both (1,0) and (0,1) | TRUE |
| P2 | single input = bit 1: W ∈ [70,130], siphon never primes | W = 100.00 mL, primed = False, both cases | TRUE |
| P3 | double input = bit 0: primes ≤ 90 s, W ≤ 30 at t_read | prime @ 44.95 s, W = 26.00 mL, waste 174.00 mL | TRUE |
| P4 | zero input = bit 0: W ≤ 30 | W = 0.00 mL | TRUE |
| P5 | max single-input ≤ 130; min double crossing ≥ 140 | 100.00 mL; 150.00 mL (margin 50 mL) | TRUE |
| P6 | S only decreases, no backflow, mass reconciles ±10 mL | monotonic True, backflow False, residual 2.3e-12 mL | TRUE |
| P7 | ±5 s valve skew changes no read-band outcome | all six skew trials match skew-0 bits (1,1,0 / 1,1,0) | TRUE |
| P8 | post-prime drain ≥ 3 mL/s | 16.67 mL/s net (20 mL/s dump − 3.33 mL/s inflow) | TRUE |
| — | **all_hold** | | **TRUE** |

Truth table: (0,0)→0 · (0,1)→1 · (1,0)→1 · (1,1)→0. The sim is XOR.

**Build-relevant margins the water will be graded inside:** (1,1) post-break residual is 26.0 mL against a 30 mL band — the tightest number in the contract. It equals INTAKE_BREAK (5) + refill-during-remaining-pulse (~21), so a faster physical siphon is NOT safer (faster dump → more refill time → higher residual; 25 mL/s would breach the band). The physical siphon should dump 200 mL in ~9–11 s. Closing-time skew must be pinned in M7 (see log finding): a trailing valve closing late adds ~8.3 mL and breaches the band.

## APPENDIX C — union-alpha contribution grade

- **Delivered:** complete module skeleton in one shot (attempt 2; attempt 1 was an OpenRouter-side 504 provider timeout, no output, no charge). 2,096 output tokens, $0.00. `stealth/union-alpha`, latency 127.6 s (row in `watch/flight_recorder.jsonl`, 2026-09-16T20:05:29Z).
- **What it got right:** correct API shape (SimParams/SimResult/simulate/truth_table/p_report/main), the siphon state machine (prime at crest / dump / break at intake with hysteresis), check-valve one-way structure, noise-seed gating, read-band function, P1–P4/P6/P8 tolerance checks, and the required disclaimer sentence.
- **What the editor had to fix (7):** P8 slope formula wrong-signed and not a drain slope (hard fail); P5 max-level check included the (1,1) case so P5 could never hold (hard fail); `all_hold` was vacuously True via a `locals()` filter (hard fail — the report would always claim success); float-modulo series sampling; negative-time skew openings; inflow not limited by SOURCE availability; sensor noise polluting mass balance. It also silently assumed the ambiguous P7 protocol where only the fixed-window reading is satisfiable — it did not notice the ~8 mL post-break refill effect.
- **Grade: B.** Sound hydraulic intuition and a clean interface draft at $0; not shippable unedited — all three of its self-grading paths (P5, P8, all_hold) contained errors that would have made the report lie in the sim's favor. Exactly why the worker/editor split exists: the worker built the pipe, the editor checked the water.
- **Receipt ends here.** Files: `mag/hydro_xor_sim.py` · `tests/test_hydro_xor_sim.py` · 15/15 pass. Sim passing is NOT substrate evidence (§4.5) — this table is what the water will be graded against.
