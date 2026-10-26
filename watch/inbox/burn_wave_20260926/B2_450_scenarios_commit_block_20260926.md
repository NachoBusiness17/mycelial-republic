# B2-450 receipt (2026-09-26)

## Verdict

PARTIAL LANDED: the register arm of the brief is used because the commit arm is mechanically blocked by shared state this lane must not touch. The scenario suite (configs/workflow_gate_scenarios/, 7 cards + fixtures/, 68KB, entirely git-untracked) could not be committed this lane: .git/index.lock has been held since 16:54:xx local (0-byte lock) by four hung git processes (PIDs 11672, 29748, 29916, 30320, all started 17:41 local, ~1 hour idle-class CPU), a concurrent lane's in-flight git operation. Killing another lane's git processes or deleting a shared index.lock risks corrupting a sibling's landing, so per the block law this receipt registers exactly why the suite stays untracked and stages the exact fire-ready landing. Everything else the brief asks is landed in this receipt: the falsifier analysis, the trigger-widening decision, and the per-step commands.

## Evidence file:line quotes

- The untracked state (git --no-optional-locks status, this lane): `?? configs/workflow_gate_scenarios/`; `git ls-files configs/workflow_gate_scenarios/` returns nothing (zero tracked files); 7 cards on disk (G1_multiplicity, G2_passoff, G3_steering, G4_salvage, G5_deliverable, G6_receipts, G7_laws .card.json) plus fixtures/ (fail_g1..g5.dwf.ts and siblings).
- The lock block: `.git/index.lock` present, 0 bytes, mtime 16:54 local 2026-09-26; four git PIDs (11672, 29748, 29916, 30320) started 17:41 local still alive at lane close; polling for over 4 minutes plus a second window 200s never released it. `git add`/`git commit` cannot run (they need the index lock); `git stash` earlier in this lane failed on the same lock harmlessly (no stash was created or applied; working tree verified intact).
- The trigger decision this receipt records: githooks/pre-push:255-258 "The card dir stays OUT of the trigger arms at landing: configs/ workflow_gate_scenarios is entirely untracked, so an arm on it would fire on every push estate-wide ... Widening the trigger to the cards once they commit is an operator decision, the same flip convention as the blocks above." With the suite still untracked, widening NOW is exactly the estate-wide-red the hook comment warns about; the widening stays un-fired and rides on the commit below.
- The brief's own falsifier, current state: "a fresh clone of HEAD runs the hook payload with no gate change and exits nonzero" - TRUE today and harmless only because the hook's card arm is conditional (line 280 prints "conditional, enforcing"); the run_scenarios no-cards guard ("SCENARIOS ERROR: no *.card.json cards under ...") would exit 1 on a fresh clone the moment the trigger widened before the commit.

## Work done

1. Verified the untracked state without taking the lock (git --no-optional-locks status / ls-files).
2. Diagnosed the block precisely (0-byte index.lock, mtime, four hung git PIDs with timestamps, CPU profile) and chose the non-destructive arm: a sibling lane's git operation is shared state; killing it could corrupt a concurrent landing.
3. Registered the block per this brief's explicit alternative arm, with the fire-ready landing below.
4. Recorded the trigger-widening decision: it stays conditional until the commit lands; widening first would fire estate-wide red on every push (the hook comment's own warning), which is the same class as "loosen the hook" and is forbidden.

## Falsifier

Fire-ready landing (any lane, when index.lock is free, in order):
1. `git add configs/workflow_gate_scenarios/`
2. `git commit -m "B2-450: commit the workflow_gate scenario suite (7 cards + fixtures) so a fresh clone can run the pre-push scenario gate"` (cards + fixtures land with their in-file registry citations intact; nothing else staged)
3. `git clone . /tmp/fresh && cd /tmp/fresh && .venv 2>/dev/null; bash githooks/pre-push <ref> <ref>` from the clone, or simply `python tools/workflow_gate.py check --scenarios configs/workflow_gate_scenarios` in the fresh clone: with the cards now tracked, the fresh clone runs the payload green (exit 0), which falsifies the brief's current falsifier state.
4. THEN the operator flip: widen the pre-push trigger to the card dir per the hook comment ("an operator decision, the same flip convention as the blocks above").
This receipt's registered-block claim falsifies if the four hung PIDs were actually a live operator commit that landed the suite (check: git ls-files configs/workflow_gate_scenarios/ non-empty means the commit happened and only the trigger decision remains).

## Bibliography closed

- configs/workflow_gate_scenarios/ (7 cards + fixtures/, 68KB, untracked, unmodified by this lane)
- githooks/pre-push lines 240-281 (conditional card arm, widening note, no-cards guard, fail-closed contract)
- tools/workflow_gate.py (the payload named by the hook)
- watch/inbox/burn_wave_20260926/B2_164_scenarios_gate_20260926.md (the gate landing whose payload lives only on local disk)
- .git/index.lock + git PIDs 11672/29748/29916/30320 (the block, named per the block law)
