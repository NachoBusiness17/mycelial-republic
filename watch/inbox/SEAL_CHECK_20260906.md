# SEAL CHECK — gap-2 closed: the heal trigger is now a per-generation ID diff (2026-09-06, seat sealcheck)

Kills Astra's gap-2 falsifier (`memory/runs/salons/astra_gap_v2_20260906/ANSWER.md`,
"recovery presented as conservation"): *"removing one sealed generation leaves a silently
healthy load."* The auto-heal landed by the heal builder (`watch/inbox/REGISTRY_AUTOHEAL_20260906.md`)
triggered only when the live registry shrank **>50% by count** vs the newest seal — a file
missing 1 of 57 sealed generations (98% by count) passed the gate and stayed silently broken.
$0, no network, no daemons. Live `memory/percolator/invariants.json` byte-identical through
the fix (sha256 `4b3b4644955358b0…9079`, mtime + size unchanged).

## The fix — `mag/percolator.py` `_load_registry` (backup: `mag/percolator.py.bak-sealcheck-20260906`)

- **NEW TRIGGER — ID DIFF**: after loading, diff the live registry's generation IDs against
  the newest seal's (`memory/seals/<latest>/…`, UTC-sortable dirs). **Any sealed generation
  MISSING from live triggers the merge-heal** — not just count shortfalls. A file can no
  longer be "healthy" while missing sealed generations.
- **KEPT, unchanged**: union merge (shared IDs count-summed + last_seen maxed — the heal
  builder's arithmetic), the `heal.log` jsonl line (never silent), atomic save
  (temp + `os.replace`), load never writes the registry, healthy files untouched.
- The 50%-by-count gate remains only as a **redundant fast-path pre-check** (the ID diff
  subsumes it: fewer IDs than the seal ⟹ some seal ID is missing) — it is never the sole trigger.

## Falsifier — `python -m mag.percolator_heal_test` (25 checks, ALL PASS)

- **(d) NEW — the gap-2 falsifier**: live copy = seal minus exactly ONE generation
  (5/6 = 83% by count — d0 proves the OLD 50% gate passed it) → load → the missing
  generation is **RESTORED** 6/6 from the seal, survivors kept, heal logged, live file
  untouched by the load.
- **(a/a2) re-run** — missing / 0-byte registry → heal from seal, intact counts, logged,
  no live write. PASS.
- **(b) re-run** — <50% shrunken file → union merge (shared 10+3=13), live-only gen kept,
  false_positives maxed, logged. PASS.
- **(c) re-run, fixture tightened** — "healthy" under the new law means live ⊇ seal IDs
  (all 6 seal gens + a live-only gen) → NO heal, exact content, no log, byte-identical.
  Note: the OLD (c) fixture (4/6 gens = 67%) was itself a partial loss the 50% gate
  blessed — under gap-2 it is case (d)'s class and now heals.
- **(s) re-run** — atomic save valid, zero `.tmp` leftovers. PASS.

## Verification receipt

- `python -m py_compile mag/percolator.py mag/percolator_heal_test.py` → clean.
- Harness → ALL PASS (25 checks, incl. d0: `5*2 >= 6` — the old gate provably missed case d).
- Live `memory/percolator/invariants.json`: sha256 `4b3b4644955358b0f2c908909f5ab94764846f3afb11556a26b87f7cd7799079`
  before AND after (62 gens / all 57 seal IDs present / 16,582 B / mtime unchanged) — the
  live diff is quiet because the live file is a full superset of the seal.
- `memory/percolator/heal.log`: 10 lines before and after — no live heal fired, nothing new to heal.
- `python -m mag.tesuji_map verify` → PASS (cells `R/incident/sealcheck/fix`,
  `R/incident/sealcheck/falsifier`, seat `sealcheck`).

## Residual risks (tri-state, honest)

- SUPPORTED (the catch): the diff makes partial loss loud + self-repairing; removal of any
  sealed generation heals on next load with a `heal.log` receipt.
- SUPPORTED (kept-contract cost): for partial loss the time windows are NOT disjoint, so
  shared-ID counts SUM (d3: 10+10=20) — counts read HIGH after a partial-loss heal, never
  low. Counts are repeat-mass, not money; conservation of generations is the guarantee.
- OPEN (unchanged from the heal card, now sharper): legitimate PRUNING of a generation will
  be resurrected by the diff on the next load — pruning must rotate/seal deliberately.
- UNPROVEN (unchanged): the wipe ACTOR. The fleet forgets nothing AND loses nothing silently
  now; the hand that wipes is still unnamed.

---
Run by seat `sealcheck`, 2026-09-06. One builds, one verifies: heal built the 50% loader fix,
sealcheck killed its gap-2 falsifier. Backup-first honored:
`mag/percolator.py.bak-sealcheck-20260906`.
