# REGISTRY AUTO-HEAL — the loader fix that closes the wipe-amnesia class (2026-09-06, seat heal)

Closes the RECURRING registry-wipe class from `watch/inbox/INVARIANTS_SHRINK_FORENSICS_20260906.md`
(Sep 5 21:40 → Sep 6 04:49 out-of-band wipe of `memory/percolator/invariants.json`, then a
merge-safe-but-blind rebuild from empty; prior art Aug 24 → Aug 26, same replace-not-merge
signature). This is the FIX TO THE LOADER — no data was restored, no one-time swap performed.
$0, no network, no daemons. Live `memory/percolator/invariants.json` is byte-identical before
and after this work (sha256 `61e0ba9bd95af7f1…aa06dc`, verified three times).

## The fix — `mag/percolator.py` (+57/−7 lines vs backup `memory/percolator.py.bak-heal-20260906`)

1. **AUTO-HEAL in `_load_registry`**: when the registry file is missing, empty (0 bytes),
   unparseable, OR its generation count is <50% of the newest seal's
   (`memory/seals/<latest>/memory/percolator/invariants.json`, seal dirs are UTC-sortable so
   "newest" = last on lexicographic sort), the loader merges the newest seal's generations
   into the returned registry BEFORE first use. Merge = union; shared IDs get count-summed +
   last_seen maxed (identical arithmetic to the operator-blessed restore — disjoint time
   windows by construction, since a sub-50% live file is a post-wipe fresh rebuild).
   Load NEVER writes the registry — the healed state persists through the normal
   merge-safe save path (load → update-or-insert → save) on the writer's next save.
2. **NEVER SILENT**: every heal appends a line to `memory/percolator/heal.log` (jsonl):
   `auto-healed N generations from <seal-dir>`. First live heal already on record
   (fired by a read-only `--status` call): 57 generations from `memory/seals/2026-09-06T01-40-13`.
3. **ATOMIC SAVE in `_save_registry`**: pid-suffixed temp file + `os.replace` — never
   truncate-in-place. The empty-file-from-crash wipe class is now structurally impossible.
4. Merge-safe behavior otherwise untouched; schema unchanged (`percolator.v1`); deterministic + $0.

Doctrine, one line: **the registry is append-only by law — a writer that finds it empty
merges the newest seal before its first save; replace-not-merge is structurally impossible.**

## Falsifiers — `python -m mag.percolator_heal_test` (temp-copy harness, 18 checks, ALL PASS)

- **(a) missing registry** → load auto-heals from newest seal: 6/6 generations restored,
  seal counts intact, heal logged, and the load did NOT write a live file. Plus (a2): a
  0-byte registry (the observed wipe signature) heals identically.
- **(b) shrunken registry** (2 gens vs 6-gen seal, <50%) → heals with union merge:
  shared count summed (10+3=13), live-only generation kept, seal generations intact,
  false_positives maxed, heal logged, live file untouched by the load.
- **(c) normal load** (healthy file, ≥50% of seal) → NO heal: exact live content returned,
  no heal log written, file byte-identical. No surprise overwrites.
- **(s) atomic save** → file valid + complete after save; zero `.tmp` leftovers.

## Verification receipt

- `python -m mag.percolator_heal_test` → ALL PASS (18 checks).
- `python -m py_compile mag/percolator.py mag/percolator_heal_test.py` → clean.
- Live `memory/percolator/invariants.json`: sha256 `61e0ba9b…aa06dc` before AND after the fix
  AND after the first live heal fired — code changed, data did not.
- Live `--status` now reports the healed view (`n_invariants: 57`) while the file still holds
  the 5-gen post-wipe rebuild — the merge becomes durable on the writer's next save.
- `python -m mag.tesuji_map verify` → PASS 257 cells, tip `f5e2216bc27c`
  (cells `R/incident/auto-heal/fix`, `R/incident/auto-heal/falsifiers`, seat `heal`).

## REMAINING OPERATOR-BLESSED STEP — the staged merged restore (DECISION + WARNING)

`research/corpus_triangulation/invariants_merged_restore.json` (57 gens / 47,716 counts =
Sep-6 seal + live post-shrink accrual) still awaits operator GO. **WARNING after this fix**:
the staged swap script re-merges seal + live at swap time by SUMMING shared counts. Once the
fixed writer performs its first save, live will already contain the seal's counts (auto-heal
persisted) — running the swap script then would DOUBLE-COUNT the seal side. If the operator
blesses the restore: either swap BEFORE any writer save lands, or re-derive the merge
(count = max, not sum) at swap time. The `.bak-preswap` copy remains the undo.

## Residual risks (tri-state, honest)

- SUPPORTED: repeated heals cannot inflate counts — after a heal persists, live ≥ seal gens,
  so the <50% gate stays closed; and while it fires, it merges from disk fresh each time.
- UNPROVEN (the wipe ACTOR): unchanged from the forensics — this fix removes the AMNESIA,
  not the out-of-band hand. An agent can still delete the file; the fleet now forgets nothing.
- OPEN: if a future design legitimately PRUNES generations, the seal-vs-live gate will
  resurrect them on the next seal — pruning must then also rotate/seal deliberately.

---
Run by seat `heal`, 2026-09-06. One builds, one verifies: shrink built the forensics, this
seat built the fix + falsifiers. Backup-first honored: `memory/percolator.py.bak-heal-20260906`.
