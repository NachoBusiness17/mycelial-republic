# R3 LANDING: trust-instrument teeth, moves 5, 6, 7

Filed by the R3-L4 landing lane (ouroboros round 3), 2026-10-05. Fold read
first: watch/inbox/ractor_engine/2026-10-05-ouroboros-r3-trust/SYNTHESIS.md
(rows 5, 6, 7 of the blindness table). Moves 1 through 4 landed by sibling
lanes (r3_land_gate.md, r3_land_fold.md, r3_land_seal.md in flight at
filing). Instruments: .venv\Scripts\python.exe only; no git commit; no
em/en dashes in landed text.

## MOVE 5: UNRESOLVED-SOURCE (both phantom engines)

The fold proved a 900M aggregate citing only a dead path passed check-master
exit 0, so the founding 191.8M class survived one line of prose
(watch/inbox/ractor_engine/2026-10-05-ouroboros-r3-trust/SYNTHESIS.md row 5).
Two landings:

- tools/citation_lint_numbers.py: sentence walk now collects record-suffix
  named paths that fail to resolve; when NO named source resolves, every
  notable number on the sentence files a warn-tier UNRESOLVED-SOURCE finding
  (counts in numbers-checked; never blocks by default; a resolvable sibling
  source keeps the strong PHANTOM-NUMBER path, so partial resolution is not
  an escape). Rule added to WARN_RULES in tools/citation_lint_io.py; class
  documented in tools/citation_lint.py.
- tools/mickey17_v2_fold.py unbound_aggregates: same shape at the fold's
  own skip; a number on a line whose named sources all fail to resolve
  returns kind unresolved-source and check-master exits 2 with an
  UNRESOLVED-SOURCE marker. Resolvable lines now carry kind unbound
  (labeled, never weakened).

Banked fixture (both engines, the NO_SUCH_FILE line):
tests/test_citation_lint.py DEAD_CITE_TEXT and
tests/test_mickey17_v2_fold_unbound.py DEAD_CITE_LINE. The named path
watch/inbox/NO_SUCH_FILE_20261005.md does not exist and must never be
created. Dogfood note: this receipt's first draft warned itself twice (its
two aggregate-bearing sentences cited the synthesis fold by bare basename,
which resolves nowhere deterministically); full-path cites cleared it, and
the final lint of this receipt reads ok with blocking 0.

## MOVE 6: credential shapes (tools/prepush_credential_shape.py)

Three families added to SHAPES, each with a value-length gate so prose
mentions stay silent: GITHUB-PAT (ghp_ + 30 or more alnum), AWS-AKIA
(AKIA + 16 uppercase alnum, the exact key-id shape), BARE-JWT (eyJ header
plus payload segment, signature optional for alg:none). scan_text switched
from rx.search to finditer: a line with two secrets now reports two
findings (one rode the push unreported before). OPERATOR-HOME-PATH now
allows repeated separators, so the JSON-escaped doubled-backslash home
path trips. Probes (tests/test_prepush_credential_shape.py): a ghp_ line
trips; an AKIA and bare-JWT pair on one line reports both shapes; a
two-sk line reports two findings with distinct masks; the doubled-backslash
path trips; family-name prose stays silent. Live changed set at filing:
zero new-family findings; the 23 standing WARNs are the home-path class in
changed data files (accept-by-name is the operator's call).

## MOVE 7: family secondaries

- tools/cache_kpi.py: _receipt ran bool(ok) on the verdict, so the string
  "false" counted a refused row as receipted (probe shape: 2 of 3 rows).
  New _ok_verdict coerces bool unchanged, string true/1/yes receipted,
  string false/0/no refused, unparseable strings carry no verdict.
  tests/test_cache_kpi_receipt.py (new): bool passthrough, both string
  spellings refused, unparseable nominal-only, compute banks receipt
  tokens from ok verdicts only.
- tools/prepush_workflow_metadata.py: ARG_HEADER_RE matched exactly two
  spaces, so a four-space-indented args block escaped TYPE-DEFAULT whole
  (the strike-1 shape re-spelled). The first arg header now fixes the
  block indent (two-space and four-space conventions parse), deeper bare
  name lines are nested default content, and a prop-indent lock stops
  nested block-default type:/default: lines from re-declaring the outer
  arg. Probes: the four-space quoted-number block trips, its clean boolean
  sibling stays silent, the nested map never re-declares, legacy two-space
  blocks parse identically. Live corpus: 93 files, 0 findings.

## GATES

- pytest consolidated: 56 passed across the five touched suites plus the
  two cache neighbors (tests/test_cache_receipt_law.py,
  tests/test_flight_recorder_receipt.py). An earlier transient run of the
  two neighbor suites errored 12/12 during a concurrent-rewrite window
  (below) and passed 12/12 unchanged on re-run.
- Founding 191.8M fixtures still trip: 4 of 4 (lint founding phantom, lint
  phantom control, fold unbound trip, fold gate exit 2). Never weakened;
  resolvable-line entries now labeled kind unbound.
- Ratchet: zero NEW from this lane's eleven files. Sole NEW at filing is
  tools/prepush_seal_patrol.py at 424 lines, the live seal lane's in-flight
  growth (fingerprint 0357434146875662), theirs to accept or fix. The
  fold's file-too-long debt was registered by the fold landing lane at 454
  lines (agent:r3-land-fold-20261005), which includes this lane's
  unbound-aggregate additions.
- No commit made (lane law).

## INCIDENT: mid-flight stash swept the tree (concurrent-lane hazard)

At 2026-10-05 19:00:39 EDT a git stash (not this lane) captured ALL
working-tree modifications on HEAD ebcd2583d, including every edit this
lane had landed to its five tools and four test files; the first full test
run (44 passed, cache_kpi suite 3 fail) straddled the sweep. The lane
re-applied its edits surgically onto the post-stash tree without touching
the stash; the untracked tests/test_cache_kpi_receipt.py survived. The
sibling fold lane then committed the de-blind work (4992d4085, JOIN-HIT
gate) which merged cleanly with this lane's re-applied unbound edits in
tools/mickey17_v2_fold.py, and registered the fold's size debt by name.
Operator note: stash@{0} from that sweep may still carry duplicate copies
of this lane's first-pass edits for the eleven files below; reconcile
against the working tree before popping.

Files touched by this lane: tools/citation_lint_io.py,
tools/citation_lint.py, tools/citation_lint_numbers.py,
tools/mickey17_v2_fold.py, tools/prepush_credential_shape.py,
tools/cache_kpi.py, tools/prepush_workflow_metadata.py,
tests/test_citation_lint.py, tests/test_mickey17_v2_fold_unbound.py,
tests/test_prepush_credential_shape.py,
tests/test_prepush_workflow_metadata.py, tests/test_cache_kpi_receipt.py
(new).
