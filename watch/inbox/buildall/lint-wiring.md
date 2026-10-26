# lint-wiring receipt (gala build-it-all, division B, 2026-10-03)

Lane: lint-wiring. Owed work as asked: wire `tools/citation_lint.py` into `githooks/pre-push` over changed
prose records with the ratchet's hard-block contract, zero baseline rows day one, the 191.8M phantom as the
founding fixture. All commands and raw outputs: `watch/inbox/gala_20260925/build-it-all/lanes/lint-wiring.check.txt`
(cited below by section tag).

## Byte finding: the owed work is already banked

The ask's premise ("tool is built but unwired") is stale. The wiring is committed, live, and enforcing:

- `githooks/pre-push:25` runs `.venv/Scripts/python.exe tools/citation_lint.py check --changed || exit 1`,
  the exact enforcing shape of the ratchet line at `githooks/pre-push:10` (`... violation_ratchet.py check
  --changed || exit 1`). Block comment `githooks/pre-push:11-23` documents the a05-r2 wiring and the
  deterministic blocking classes (PATH-MISSING, LINE-OOB, EMPTY-SPAN, PHANTOM-NUMBER; TOKEN-MISS and
  SHORTHAND-UNRESOLVED warn-only).
- The hook is installed: `git config core.hooksPath` returns `githooks` (evidence [A]), and
  `githooks/pre-push` is tracked (exit 0).
- Provenance: `tools/citation_lint.py` (+ `citation_lint_io.py`, `citation_lint_numbers.py`,
  `tests/test_citation_lint.py`) landed in commit `3c83da5b0` 2026-10-02T02:54:04-04:00 (FILL-BALL 1001:
  "Citation lint LANDED ... zero baseline rows day one", evidence [B2]). The founding fixture
  lives in the tool's self-test battery per the tool docstring (`tools/citation_lint.py:11-15`).
- Zero-baseline day one holds at landing; the current `configs/citation_lint_baseline.json` carries 3
  accepted rows, all `accepted_by: drift-patrol-cron` for gala-night prose committed 2026-10-01
  pre-gate-adoption with the prose fix flagged owed (evidence [C]). That is the accept-debt-by-NAME law
  working as designed, not a day-one violation.

No edit was made to `githooks/pre-push` or the lint tool: they are byte-identical to HEAD
(`git status --porcelain` on `githooks/ tools/citation_lint.py configs/.config_seal.json docs/DNA.md`
empty, evidence [H3]). Re-adding a hook line would have duplicated a working gate.

## Finish line, byte-checked

Controlled rig: a throwaway detached worktree at HEAD (`git worktree add --detach /tmp/lint_wt_cite HEAD`,
evidence [H0]) with the repo venv junctioned in; the worktree's changed set is exactly the fixture record
(`docs/DNA.md`), so gate verdicts attribute cleanly.

1. Phantom record FAILS at pre-push. Fixture appended to `docs/DNA.md`:
   "The beta factory burn spent 877.3M tokens this arc (AGENTS.md)." (877 appears zero times in AGENTS.md,
   grep -c = 0, evidence [H0]). `sh githooks/pre-push < /dev/null`: ratchet PASS (scope=0), then
   `CITATION-LINT: FAIL records=1 ... blocking=1` with
   `docs/DNA.md:151 PHANTOM-NUMBER 877.3M number appears in none of the sentence's named sources (AGENTS.md)`,
   HOOK-EXIT=1, and the hook never reached the config_seal line: the block happened at the citation gate,
   the same `|| exit 1` contract as the ratchet. Standalone tool exit 1. Evidence [H1].
2. Clean record PASSES. `docs/DNA.md` reset, clean line appended citing a real anchor
   (`tools/citation_lint.py:47`). Tool standalone exit 0 (records=1 anchors=4 blocking=0 warns=0). Full hook
   run: every gate green, HOOK-EXIT=0 (ratchet, citation lint ok, config seal PASS, description_pin,
   freshness, census patrol, checkbox WARN-only, caption/refold/workflow/parity skipped as unchanged, secret
   gate clean). Evidence [H2].
3. Hook line in `githooks/pre-push`: `githooks/pre-push:24-25`, evidence [B].
4. Receipt: this file.

Not run: an actual `git push` to a remote. The hook was invoked directly (`sh githooks/pre-push < /dev/null`),
which is the same script git executes; git's stdin ref lines feed only the pushed-range arms (the caption
block captures them at `githooks/pre-push:167`, later blocks reuse the value), and with empty refs those arms
skip while the dirty-vs-HEAD arms that drive the enforcing gates still fire. The fail and pass verdicts above
are therefore gate-faithful, not transport-faithful.

## Live gate state on the real tree (context, not fixtures)

- `tools/citation_lint.py check --changed` over the current 18 changed prose records: exit 0, 1 warn
  (temp_violation.txt RECORD-UNREADABLE, warn-only). Evidence [D].
- `tools/citation_lint.py --selftest` (in-process pytest over tests/test_citation_lint.py, includes the
  191.8M founding fixture): exit 0, 7 passed, 1 skipped (the inner-battery env guard, by design). Evidence [I].
- `tools/violation_ratchet.py check --changed` on the main tree: exit 0 (scope=1, registered, NEW=0). This
  lane touched no code under mag/ or tools/, so the conditional ratchet duty did not trigger; it was run
  anyway for the record. Evidence [G].

## Operator-facing incident found en route (not this lane's to fix)

`tools/config_seal.py verify` fails in EVERY tree right now: main tree exit 1 with `MODIFIED mirrors.json`
(evidence [F]); pristine HEAD worktree exit 1 with `MODIFIED mirrors.json` + `MISSING providers.yaml`
(evidence [H0b]). The committed seal matches neither HEAD nor the working tree, so any push from the main
tree currently blocks at the config_seal gate regardless of the citation gate. Re-seal is a NAMED act
(`tools/config_seal.py update --by WHO --note WHY`) owned by whoever drifted `configs/mirrors.json` and
`configs/providers.yaml`; this lane did not re-seal the main tree. To demonstrate the end-to-end green hook,
the throwaway worktree received a scratch seal
(`update --by lint-wiring-lane --note "scratch seal inside throwaway worktree ..."`, evidence [H2]); the
main-tree seal file is untouched.

## Teardown

Worktree removed (`git worktree remove --force`, exit 0, evidence [H3]); `git worktree remove` left the venv
junction reparse point behind but did not descend through it (venv verified alive after:
`.venv/Scripts/python.exe` runs, 3.11.15, evidence [H3b]); the junction was then deleted reparse-point-only
via PowerShell `(Get-Item ...).Delete()` and the temp dir removed (evidence [H3c]). Main tree integrity:
`git status --porcelain` empty for `docs/DNA.md configs/.config_seal.json githooks/
tools/citation_lint.py` (evidence [H3]).

## Decision ledger

No new decision. The owed-work premise is retired as stale: the wiring decision (a05-r2, landed in commit
`3c83da5b0`, 2026-10-02) stands and was verified end-to-end here. The one handoff is the pre-existing
config_seal drift named above, which blocks main-tree pushes until its owner re-seals by name.
