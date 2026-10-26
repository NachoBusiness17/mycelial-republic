# W3 FRONT DOOR - regenerated clone landed (2026-09-29)

**Lane:** Mickey17 Wave 3, return 12 improvement (docs + zeitgeist, agent 30e12767).
**Ask:** FRAMEWORK_LOAD.md as a REGENERATED CLONE, auto-rendered from live truth at
each wave close. Landed. No git commit (lane law).

## The rival self-stories it kills

The old hand-written door narrated the August estate (Ollama/DeepSeek office) while
DNA.md pointed at the live ghost-self chain; a cold seat loaded an estate that no
longer exists. The door now dies and is reborn from bytes every regen.

## Files

- `tools/regen_front_door.py` - NEW. Parses truth, renders, writes. Determinism law:
  no wall clock, no dict order; every auto section's `generated_at` is keyed to the
  newest mtime of its own truth sources (reruns over an unchanged tree are
  byte-identical; `--at` pins stamps for receipts). Em-dash law: U+2014 anywhere in
  the render fails closed exit 2 naming the line. Flags: `--stdout`, `--check`
  (0 fresh / 1 stale / 2 error), `--at`, `--repo`.
- `docs/templates/FRONT_DOOR_TEMPLATE.md` - NEW. Stable prose (what this repo is,
  office metaphor, load-order table, three doors, FILE block, anti-patterns,
  regeneration contract) + four `<!--REGEN:SECTION-->` placeholders.
- `docs/FRAMEWORK_LOAD.md` - REGENERATED (8,471 bytes, LF). Auto sections: current
  era (003 - THE POUR, from `docs/archive/ZEITGEIST.md` line 1), version + gates
  (from `memory/improve/releases/gates.jsonl`, final row per gate wins; v2 3/3,
  v3 5/5, v4 4/4, v5 5/5, latest row regime_drift_registry_t1_t6 ok 2026-09-26, with
  the return-12 inverse-trap note: bytes beat a still-planned registry label),
  agent-state tip (ghost-self n=20523, anti-reinvention, next moves), top-level
  layout (82 dirs, ls semantics, 791 root files elided).
- `tests/test_regen_front_door.py` - NEW. 14 tests.

## Verification (bytes, not claims)

- `pytest tests/test_regen_front_door.py -q` -> **14 passed** (includes
  two-runs-byte-identical on the fixture AND on the live repo, era parse canonical +
  variant + fail-closed, em-dash fail-closed, `--at` pinning, gates final-row-wins +
  open-gate surfacing, placeholder integrity).
- Live regen: wrote 8,471 bytes; `--check` after -> fresh, exit 0.
- Fresh-build vs on-disk byte compare: identical. Em-dash count in render: 0.
- Root `LOAD.md` pointer still resolves to the door (unchanged).

## Rerun at every wave close

```text
.venv\Scripts\python.exe tools/regen_front_door.py
.venv\Scripts\python.exe tools/regen_front_door.py --check   # patrol arm: 1 = stale
```

Staleness is now a property of truth, not of prose: the door goes stale exactly when
gates.jsonl / LATEST.md / the zeitgeist era line / the root moves without a regen.
