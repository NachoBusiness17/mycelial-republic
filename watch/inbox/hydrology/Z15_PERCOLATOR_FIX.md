# Z15 — percolator count laws landed (decay + MAX-merge + self-emission cap)

**Seat:** Z15 (hydrology) · **Date:** 2026-09-30 (UTC clock at apply time) · **No commit (file ownership working tree).**
**Diagnosis credit:** S15 (seeded in `configs/mates.yaml`: "the percolator's memorization is an exploit played by the loop on itself. Formalize it: who are the players, what is the equilibrium, what rule change moves it?" — 232,214 self-reinforcements = an exploit).

## The exploit, named (who/what/equilibrium)

- **Players:** the loop (pro_library.fire → operator_inbox.log_behavioral_event → percolate) vs the registry.
- **Move:** every `pro_library.fire` of the "[steer] Elevate with a deliberate ask…" move logs a `[steer] …` behavioral event; `mag/operator_inbox.py` routes EVERY behavioral event's detail through `percolate_signal`; each percolation of that text incremented the very invariant that tells seats to fire it. Plus the heal path SUM-merged seal+live counts on every auto-heal (`memory/percolator/heal.log`: 4 heals 2026-09-06→09-26 riding the same seal), inflating whatever it touched.
- **Equilibrium was:** count = repetitions × heal events, monotone up, never down. Top invariant 232,214 = 79.8% of all 291,336 counted events; nothing decayed.

## The rule change (mag/percolator.py, all three landed)

1. **Half-life decay** — `_decay_count()`: count halves every `half_life_days` (config `configs/percolator.json`, default **30**, optional file with in-code defaults, stdlib-only contract kept by using JSON not yaml). Elapsed time quantized to WHOLE cycles (UTC days — the same clock as law 3), floor at 1 (time alone never erases an observed invariant; only the false-positive path removes truth claims). Applied at increment time (decay-then-+1) and by the maintenance backfill. `decay_as_of` stamps the baseline so reruns never compound.
2. **Heal-merge takes MAX, not SUM** (dated comment at the merge site) — idempotent: N heals off the same seal leave the count unchanged. The cap ledger (`cycle_hits`) + `decay_as_of` ride along from the fresher side.
3. **Self-emission cap** — same source reinforcing the same invariant within one cycle (UTC day) counts ONCE per cycle, not once per repetition. Per-invariant `cycle_hits` map pruned to the current cycle (bounded; A/B/A alternation within a day still counts each source once). Capped observations still refresh `last_seen`/`decay_as_of` (decay measures absence) but cannot pump the count. Result surface carries `"capped": true`.

## Tests

- **New** `tests/test_percolator_z15.py` — 15 tests: exact halving math, cycle quantization, floor/disable, runtime decay-on-repeat (100 → 50 +1 = 51 after 30 idle days), MAX-merge both directions, idempotence across repeated partial-loss heals (the SUM falsifier: would read 10→20→40→80; holds 10), cap same-source/different-source/new-cycle/config-off, maintenance dry-then-apply (232,214 fixture → 25) + non-compounding rerun. All tmp_path-isolated (fact_bus + destructive_receipt stubbed); live registry never touched.
- **Amended** `mag/percolator_heal_test.py` — b2 (10+3=13 → max(10,3)=10) and d3 (10+10=20 → max=10) now assert MAX with dated Z15 comments; harness rerun ALL PASS.

## The run against the live registry (dry → apply)

`python -m mag.percolator --maintenance --dry` then `--apply` (backup: `memory/percolator/invariants.json.bak-z15-20260930`):

| | before | after |
|---|---|---|
| top count ([steer] Elevate…, `212719f4b54d06e9`) | **232,214** | **27** |
| new top (backend not reachable…, `1182ee5e2bc05248`) | 837 | **31** |
| total count sum (526 generations) | 291,343 | **1,066** |
| changed rows | — | 108 / 526 |

Backfill semantics (documented in `maintenance()` docstring): the retroactive cap is `min(count, distinct UTC days in [first_seen, last_seen])` — without per-hit source history that is the strongest provable bound on a cycle-deduped count; conservative for an invariant legitimately hit by several distinct sources in one day (accepted: the alternative is keeping a provably self-inflated number). Then one half-life decay pass from the observation baseline. All 526 generations + false_positives (13) preserved.

## Sane?

Yes: top count 31 ≈ "observed on ~31 distinct recent days", total 1,066 across 526 invariants, `status()` now surfaces `count_laws {half_life_days: 30, cycle: utc-day, self_emission_cap: true}`. Live-fire proof post-apply: percolating the real "[steer] Elevate…" text from source `behavioral_event` 3x in one cycle → counts 28/28/28, `capped: True` on hits 2-3 (`cycle_hits: {behavioral_event: 2026-09-30}`) — the exploit cannot re-inflate itself.

## Test runs (named instruments, per the census denominator law)

- `pytest tests/test_percolator_z15.py tests/test_desk_conductor.py -q` → **24 passed**; `python -m mag.percolator_heal_test` → **ALL PASS** (amended b2/d3).
- Full suite `pytest -q --ignore=tests/test_behavioral_awareness.py` (45:26): **3,054 passed / 12 skipped / 3 failed / 3 errors** — the 3 failures are foreign surfaces carrying no percolator reference (census_drift_patrol CLI gap, headless spawn-debt 22→34 listing tools/*.py offenders, oral_dedupe census 63≠33) and ride the same mid-merge debris as the ignored file (UU conflict `tests/test_behavioral_awareness.py`, parse-error `tools/rollup_delta.py`, both pre-existing this lane).

**Files:** `mag/percolator.py` · `tests/test_percolator_z15.py` (new) · `mag/percolator_heal_test.py` (b2/d3 amended) · `configs/percolator.json` (new, optional override) · `memory/percolator/invariants.json` (repaired, pre-edit backup alongside).
**Out of scope (other lanes' ownership):** the `operator_inbox → percolate_signal` fire-per-event routing itself — law 3 now neutralizes it at the registry, no caller changes needed.
