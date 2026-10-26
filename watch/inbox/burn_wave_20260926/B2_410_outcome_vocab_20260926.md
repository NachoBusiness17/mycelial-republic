# B2-410 skill_ledger outcome vocabulary registry (2026-09-26)

## Verdict

LANDED. The `outcome` field is now a registered vocabulary in
mag/skill_ledger.py: OUTCOME_WIN ("ok", the only winning value),
OUTCOME_REGISTRY giving every known value a meaning line (ok, fail, the
icon_drop fold spellings failed/skipped_no_powershell/unknown, and generic
skipped), normalize_outcome() mapping aliases (failed -> fail) and passing
unknown strings through so new writers surface instead of vanishing, and
is_win() as the strict consumer predicate. The one counting site
(proven_moves, the function the brief calls best_moves) now uses is_win
instead of a bare == "ok" comparison. Tests pin the registry, the alias
mapping, strict win semantics (a skip is not a win and not a failure), and
the 4-row ok_rate arithmetic (0.25 when one ok / one skip / one failed /
one decision-only).

## Evidence file:line quotes

- The disease, mag/skill_ledger.py (pre-edit): record_decision comment
  "outcome: None=decision only · ok/fail (verified)" while proven_moves
  counted `if row.get("outcome") == "ok"`; and mag/icon_drop.py:255-262
  (B2-378 block) documented writing ("failed", "skipped_no_powershell")
  into the same field - an open vocabulary with exactly one special value.
- Post-edit mag/skill_ledger.py: module docstring gains the "Outcome
  vocabulary (B2-410...)" section naming the registry pattern and the
  events-key-registry precedent; OUTCOME_WIN + OUTCOME_REGISTRY (6 values,
  each with a meaning line, including "skipped_no_powershell": "attempt
  never ran ... NOT a failure, must not count as either a win or a fail");
  normalize_outcome(); is_win(); proven_moves uses is_win; record_decision's
  inline comment points at the registry.
- Pins, tests/test_skill_ledger_outcome_vocab.py (4 passed): registry
  coverage of all six values; normalize maps failed->fail and keeps
  skipped_no_powershell distinct; is_win strict (the "failed" alias is NOT
  a win); proven_moves over {ok, skipped_no_powershell, failed, None} gives
  count 4 ok_rate 0.25.
- One test-name correction mid-lane, named: the function the brief calls
  best_moves is spelled proven_moves in the module; the test was renamed to
  the real name after the first run failed on the guess.

## Work done

1. Read record_decision, proven_moves, and the icon_drop B2-378 block;
   confirmed the field had no registry and the skip/fail distinction had no
   surface.
2. Landed OUTCOME_WIN/OUTCOME_REGISTRY/normalize_outcome/is_win with the
   events-key-registry pattern; switched proven_moves to is_win; updated
   the docstring and the field comment (spec before behavior change).
3. Wrote 4 pins; fixed the import placement and the function-name guess;
   4 passed.
4. Filed this receipt; LEDGER row; QUEUE pointer; INDEX registration.

## Falsifier

This registry is inverted if any of the following holds: (a) a consumer that
must distinguish skip from fail still imports icon_drop literals (grep
mag/ tests/ for "skipped_no_powershell" outside icon_drop and this registry:
a hit means the surface was bypassed); (b) icon_drop starts writing a NEW
outcome string that is absent from OUTCOME_REGISTRY for more than the landing
day of whatever introduced it (registry feedback loop broken; the
pass-through in normalize_outcome is the tripwire, not a license);
(c) proven_moves starts counting a skip as a win (is_win regressed to a bare
string compare; the ok_rate pin catches the shape).

## Bibliography closed

mag/skill_ledger.py (read: header, proven_moves, record_decision; edited as
above); mag/icon_drop.py:255-281 (B2-378 status pass-through, read);
watch/inbox/burn_wave_20260926/B2_378_fold_outcome_20260926.md (accepted from
the brief as the cause receipt); mag/events_key_schema.py (registry pattern
named by the brief, read for the shape). No network calls.
