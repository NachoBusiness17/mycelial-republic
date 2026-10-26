# pre-push instruments - lane 10 (pre-push-instruments), GO wave 2026-10-04

Lane: 10 of the coordinator-partitioned GO wave. Mandate: fold's first
alternate plus register ranks 16-17 (corpus/steal/MASTER_MICKEY17_V2.md
section 9, "Further alternates"): the golden-vector pre-push check
(a11-commits#3), the credential-shape pre-push scan (a11-commits#4), and the
last-seal-vs-bytes patrol check (a12-ractor-legs#3). Evidence rows read in
full: memory/runs/mickey17_v2/runs/run-0/lanes/a11-commits.json and
a12-ractor-legs.json. House pattern followed: WARN-ONLY first landing, flip
to enforce is an operator call (the census tripwire B2-215 precedent, the
t40 lesson restated in every existing hook block).

Row-numbering note: the master doc's a11-commits#3/#4 are 0-indexed rows - #3
is key cc33f22dcafe (FULL CAMPAIGN) and #4 is key dd44a33dcafe (the leak
audit), consistent with the credential row carrying the credential mandate.

## Instrument 1: golden-vector check (a11-commits#3, key cc33f22dcafe)

File: tools/prepush_golden_vector.py

Catches: a tools/dungeon.py edit that silently drops a FULL CAMPAIGN
known-answer the a11 lane byte-verified at commit a7d7d313d. The vector is 11
fixed byte tokens: the S2 Lexical Stair, S3 Wiping Vault, and S4 Phantom Wyrm
scene names, the scroll-hoard/regrowth docstring law, the unaudited-scrolls
law, the 3x [AUDIT root]-at-DC-15 win gate, the HP-0-does-NOT-win law, the
WON verdict line, the --full flag wiring, the ("S2", "S3", "S4") loop, and
the root_anchors counter. Each token was verified present at landing on BOTH
surfaces, 11/11 on each, by:
  `for s in ...; do grep -cF -- "$s" tools/dungeon.py; done` and the same
  loop over `git show a7d7d313d:tools/dungeon.py` (11/11 both).

Why bytes and not a live run: campaign() calls models (tools/dungeon.py:489,
self._paid) and writes a session DONE file (tools/dungeon.py:577); a push
hook must never write shared state or spend budget (the B2-328 law stated in
the hook's refold block). The row's known answers are byte facts.

Trigger: tools/dungeon.py ONLY (dirty vs HEAD, untracked, or the pushed
range), decided by tools/prepush_paths_changed.py with the caption block's
captured stdin, the same shape as the rule_parity block.

Live verdict at landing:
  `.venv/Scripts/python.exe tools/prepush_golden_vector.py`
  -> `GOLDEN-VECTOR: ok - 11/11 golden tokens in ...tools/dungeon.py`, exit 0.

Exit contract: 0 all tokens present, 1 miss (names each lost law plus the
restore state `git show a7d7d313d:tools/dungeon.py`), 2 cannot verify.

## Instrument 2: credential-shape scan (a11-commits#4, key dd44a33dcafe)

File: tools/prepush_credential_shape.py

Catches: credential SHAPES riding changed/staged content. The shape set is
the row's own grep battery (sk- 16+, xai-, AIza, gsk_, Bearer 15+,
api_key/password assignment, BEGIN PRIVATE KEY) plus the row's own steal
mandate: the operator home path (C: + separator + Users + separator + foste),
the leak class the first scan missed (3 committed hits in
watch/inbox/hermes_burn/SUBSTANCE_48h_synthesis.md, the row's quote names
line 34). Deviations are named per-rule in the tool: value-length gates on
the bare prefixes (xai- 12+, AIza 30+, gsk_ 20+, assignments 8+) so the
row's literal greps quoted as prose in receipts do not WARN.

Scope: the secret_gate --changed fast path (upstream..HEAD when configured,
plus staged, unstaged, untracked). Masking law: findings print a 4-char
masked head plus length, never the full value (secret_gate convention).

Baseline: zero day one (configs/prepush_credential_baseline.json absent at
landing; accept-by-NAME via fingerprint, the citation_lint precedent;
fingerprints are shape + file + masked head, printed with each finding).

Live verdict at landing (final run, moment 2026-10-04 late UTC):
  `.venv/Scripts/python.exe tools/prepush_credential_shape.py --changed
  --baseline configs/prepush_credential_baseline.json`
  -> `CRED-SHAPE: WARN - scanned 228 changed file(s), 35 finding(s) (0
  accepted by name), skipped 4 binary / 7 >2MB`, exit 1.
Notable true positives: OPENAI-SK + BEARER-TOKEN len-73/80 shapes in
dashboard/static/lanes/elder.md:345 and queue/lanes/elder/surface.md:345.
An earlier run at a slightly earlier moment read 155 files / 30 findings;
the changed set grew between runs because sibling lanes keep landing files
(denominator law: each number names its run, never difference them).

Self-trip history (cause + evidence, the masking discipline in miniature):
the first landing tripped the gate on its own docstring because it spelled
the operator home path literally (hook comment lines and tool docstring both
warned, 30-finding run). Fix: the citation now spells the path as
C:/Users/<name> and points at the OPERATOR-HOME-PATH regex rule as the
canonical form; the grep in tests/test_prepush_credential_shape.py
test_tool_source_does_not_self_trip holds the regression:
  `.venv/Scripts/python.exe -m pytest
  tests/test_prepush_credential_shape.py -q` -> the test scans the tool's
  source bytes and requires zero findings.
The test file's own fixtures are runtime-concatenated for the same reason
(the first draft's source-byte literals were findings 31-32 of the 34 run).

Exit contract: 0 clean or all-accepted, 1 findings, 2 git failure.

## Instrument 3: last-seal-vs-bytes patrol (a12-ractor-legs#3)

File: tools/prepush_seal_patrol.py

Catches: post-seal drift on watch/inbox boards - a file present on disk whose
bytes no longer match the latest sha256-bearing seal row named for it in
watch/inbox/index_events.jsonl. The query is the a12 lane's CHECK3
(preserved in memory/runs/mickey17_v2/runs/run-0/lanes/tmp_a12_verify.py),
standing at pre-push per the row's own steal: "add a last-seal-vs-bytes
check ... so post-seal drift on watch/inbox boards alarms instead of waiting
for an audit lane."

Two laws inherited from the row's own measurements:
- Sealed-but-deleted files are NOT a defect (the row ruled 42 sealed paths vs
  21 on disk "expected seal-chain behavior"): only present-and-mismatched is
  a finding.
- Malformed ledger rows are counted, never fatal (the row measured exactly 3
  pre-existing template rows; the live ledger reads 3 malformed today).

Cost law (measured at landing with the inline python census over the ledger):
10,071 lines, 5,404 distinct sha files, 1.81 GB to hash - a push hook may not
hash that, so the default window is the last 150 sha-bearing rows (51
distinct files at landing), --rows widens it. Path resolver handles the
ledger's three field shapes (bare under watch/inbox, absolute-in-estate, and
the Docker /board/inbox surface, which is skipped as other-surface).

Live verdicts (denominator law: two moments, both named):
  Run 1 (earlier): `SEAL-PATROL: DRIFT - ... (9805 sha rows, 3 malformed),
  window last 150: 51 distinct file(s), 44 match, 1 missing-on-disk` with 6
  drift files, exit 1.
  Final run: `9807 sha rows, 3 malformed ... 43 match, 1 missing-on-disk`
  with 7 drift files (the boards are live; sibling lanes edit sealed files
  between runs), exit 1.
Findings at landing (WARN, never blocking): the 2026-10-02-workflow-dogfood
board (moonshot-2, accuracy, operations, dogfood .md) and frontier_olm
RECEIPT/steal files moved after their last seal. Not my lane to wash; the
WARN names the fix: re-seal through the owning writer or restore bytes, never
hand-edit the ledger.

Exit contract: 0 all windowed on-disk files match, 1 drift, 2 ledger missing.

## WARN-ONLY wiring (githooks/pre-push)

All three blocks sit at the hook tail, after the existing ratchet +
citation_lint + config_seal + description_pin + freshness + census +
checkbox + caption + refold + workflow_gate scenarios + rule_parity +
secret_gate blocks. Each block: captures the tool output, case-matches the
green first-line prefix (the B2-338 lowercase-ok convention), prints its WARN
with the fix command on red, and NEVER exits nonzero. Each carries a
TODO-FLIP-TO-ENFORCE note (operator call). Golden-vector is conditional on
its trigger; credential_shape always runs (--changed); seal_patrol is
conditional on the ledger existing.

Wiring proof (never-blocking under live red findings):
  `sed -n '/^# golden-vector gate/,$p' githooks/pre-push >
  /tmp/prepush_tail.sh && CAPTION_PUSH_INPUT="" sh /tmp/prepush_tail.sh`
  -> tail_rc=0 with `PUSH-GATE: golden_vector ok ...`,
  `PUSH-GATE: credential_shape WARN ...`, and
  `PUSH-GATE: seal_patrol WARN ...` plus both fix lines printed.
  `sh -n githooks/pre-push` -> syntax OK.
The golden_vector hook WARN arm (tool exit 1 -> case red arm) is covered by
the CLI tamper test (tests exit-1) and mirrors the census/parity case-arm
shape; the hook's golden block was exercised green end-to-end above.

## Tests (known-bad trips, clean passes silent)

Files: tests/test_prepush_golden_vector.py (6 tests),
tests/test_prepush_credential_shape.py (7 incl a git-repo --changed test and
the self-trip regression), tests/test_seal_patrol.py (6).

  `.venv/Scripts/python.exe -m pytest tests/test_prepush_golden_vector.py
  tests/test_prepush_credential_shape.py tests/test_seal_patrol.py -q`
  -> first full run: 4 failed, 15 passed in 9.40s; final: **19 passed in
  5.13s**.

The 4 first-run failures were all real catches, filed with their causes:
1-2. The seal-patrol clean and drift fixtures sealed with sha(b"v1\n") while
Path.write_text had written b"v1\r\n" (Windows newline translation): the
patrol flagged its own test's byte drift. Fix: fixtures write_bytes + seal
the same bytes; the fixture law is documented in the test docstring.
3. The core test wrote the file at tmp root while the resolver correctly
joins bare paths under watch/inbox (the CHECK3 surface): fixture moved.
4. The self-trip test caught the tool docstring's verbatim steal quote
carrying the literal operator home path: docstring fixed, test kept as the
regression pin.

## Gates run before claiming done

  `.venv/Scripts/python.exe tools/violation_ratchet.py check --changed`
  -> first run FAIL with 4 NEW: 2 were mine (cwd-relative-path on the
  module-level Path literals in prepush_credential_shape.py:59 and
  prepush_seal_patrol.py:50) - FIXED by anchoring both constants to
  ESTATE_ROOT (fix comments in the tools name the cause and the ratchet
  class). Final run: `scope=14 changed files; hits=4; registered=2; NEW=2`
  with the remaining NEW being mag/route_chat.py:174 except-pass and
  tools/dungeon.py:756 file-too-long - both files are MODIFIED IN THE
  WORKING TREE BY SIBLING LANES, not by this lane (proof:
  `git status --porcelain mag/route_chat.py tools/dungeon.py` -> both ` M`;
  `git show HEAD:tools/dungeon.py | wc -l` -> 605 vs on-disk 756; this lane
  never edited either file). My three tools scan ZERO ratchet hits:
  `.venv/Scripts/python.exe -c "...vr.violations_in(...)"` over the three
  files -> `my-tools hits: ZERO`.
  `.venv/Scripts/python.exe tools/citation_lint.py check --changed` -> first
  run exit 0 (WARN-class rows on sibling files only); a later run in the
  same session exited 1 with 5 blocking PHANTOM-NUMBER findings, ALL in
  sibling/surface files, none this lane's: AGENTS.md:29 (three findings,
  the census bullet), watch/inbox/frontier_olm_2026-10-03/steal/
  quantization-and-compression.md:15, watch/inbox/GATE_DIGEST.md:16. Proof
  none are mine: `.../tools/citation_lint.py check --changed | grep -i
  "go_wave\|prepush"` -> no matches. The changed set grew continuously
  during this session (155 -> 228 files across credential-scan runs), so a
  sibling lane modified those surfaces mid-session; resolution belongs to
  the owning lanes or an accept-by-name, not to this lane (AGENTS.md is
  explicitly outside my file ownership).

## Files touched

- tools/prepush_golden_vector.py (new)
- tools/prepush_credential_shape.py (new)
- tools/prepush_seal_patrol.py (new)
- githooks/pre-push (three WARN-ONLY blocks appended at the tail; no
  existing block touched)
- tests/test_prepush_golden_vector.py, tests/test_prepush_credential_shape.py,
  tests/test_seal_patrol.py (new)
- this receipt

Not touched: AGENTS.md, queue/STANDING_RAILS.md, any other lane's files
(the pre-existing em-dashes in the hook's D2 rule_parity comment block are
that lane's bytes and were left alone; this lane's added lines are
em-dash-free, verified by `grep -rnP "\x{2013}|\x{2014}"` over all six new
files -> no matches).

## Blockers

None for the lane. Shared-tree notes filed, not blockers: the ratchet FAIL
on the two sibling-dirty files (exact reason above, resolution belongs to
the lanes that modified route_chat.py and dungeon.py or to the operator's
baseline-update); the 7 live seal-drift findings and 35 credential-shape
findings are day-one WARN channel content (zero baseline day one means the
baseline file starts empty; findings stay visible until triaged or accepted
by name).
