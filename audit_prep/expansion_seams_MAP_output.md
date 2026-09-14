## Finding — what your cell yields

**Disputed.** "Safe by architecture" is enforced by convention, not code. The 480-wide wave temperature test simulates lanes in-memory and passes but never fires real parallel calls; the fanout purity law is a docstring comment, not a tested invariant. The seam holds because the operator enforces the gate, not because the architecture makes violations impossible.

## Evidence — what in the repo supports it (file/shape, no invention)

- `mag/fanout.py` (107 lines, 5,336 B): purity law lines 9–14 as comment only; `os` imported for `os.environ` (line 66) — no `open`/`os.path`/`makedirs` calls, but no guard prevents adding them; `===FANOUTJSON===` marker (line 102) is the sole contract enforcement.
- `mag/context_pack.py` (1,075 lines): pack modes define janitor/route/build/audit/plan/full; packs carry `width` + `lanes` + `model` keys (see `packs/p160_matthew_20260913.json`).
- `test_480_wave_temperature.py`: simulates 480 lanes in-memory via `temperature_stack.registry()`; reports `verifier_pass` but zero API calls — the 480-wide claim is untested at runtime.
- `mag/bay_organs.py` (339 lines): three stdlib-only organ primitives; downstream `window_throttle.py`, `race_harness.py`.
- Existing `CELL_expansion_seams_VERIFY.md` claims "Supported" — this cell overrides to Disputed on the enforcement gap.

## Risk if wrong — what the audit breaks on if this is missed

Steiniger's abliteration instinct targets the docstring-only purity law. He will add `open()` to fanout.py and ask whether the gate catches it — if "the comment says no," the "safe by architecture" reading collapses, and every organ depending on fanout (race_harness, window_throttle) becomes suspect. The temperature test passing without real fire is the second crack: he will demand a live 5-wide run; the `HOST_ALLOW` + global-IP gate in `guarded_fetch()` (lines 41–54) is the only runtime enforcement.

## The act — the concrete prep step (file/spec/number)

1. Turn fanout purity law from comment to test: `tests/test_fanout_purity.py` — AST scan of `mag/fanout.py` for `open`/`os.path`/`makedirs` after line 14, assert none exist. ~20 lines.
2. Run a live 5-wide pack through `mag/fanout.py` with `packs/p160_matthew_20260913.json`; capture STDOUT/STDERR receipt appended to `audit_prep/fanout_organ_width_ladder_receipt.md`.
3. Patch `test_480_wave_temperature.py` to add runtime enforcement: fire one lane via `fanout.fire()` against a real key and assert `guarded_fetch` rejects a non-allowlisted URL — gives Steiniger a falsifiable runtime claim.

## Falsifier — what would prove this wrong

- `open(`, `os.path.`, or `makedirs` appearing in `mag/fanout.py` after line 14 (static scan catches it).
- A live 5-wide pack run where `guarded_fetch` does NOT reject a non-allowlisted host or non-global IP — the gate is the only runtime enforcement; if it leaks, the purity law is decorative.
- The temperature test's `verifier_pass` being true while a real 480-wide wave produces a timeout or token-budget collision the in-memory simulation never caught — proves the simulation is not a proxy for the real wave.
