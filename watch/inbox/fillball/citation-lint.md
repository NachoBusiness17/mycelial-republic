# citation-lint.md - the citation lint landed (fillball-1001, lane fill-citation-lint, division B)

Landed 2026-10-01. Closes GAP_REGISTER rank 3: tools/citation_lint.py absent
from the whole estate while its spec sat written in ractor50's accuracy retro.
This receipt is the finish-line record; raw command output is banked at
watch/inbox/gala_20260925/fillball-1001/lanes/fill-citation-lint.check.txt.

## What landed

- tools/citation_lint.py (333 lines) - the anchor checker and CLI: every
  file:line anchor in a changed record must satisfy (a) the path resolves,
  (b) the line range is in bounds and non-blank, (c) the cited span mentions
  a token from the claim line. Entry point `check --changed` (staged +
  unstaged prose records vs HEAD) and `check --files` (explicit, wider
  suffix set). Exit contract 0/1/2; first-line output contract
  CITATION-LINT: ok / FAIL / ERROR per the B2-338 law.
- tools/citation_lint_numbers.py (251 lines) - the PHANTOM-NUMBER engine,
  sentence-scoped: a notable quantity (K/M suffix, comma-grouped, 4+ digits)
  must appear in at least one of its sentence's named record sources.
- tools/citation_lint_io.py (361 lines) - Finding/LintResult, the shared
  cite-path grammar, git-index resolution with a single-hit basename
  fallback, streamed source reads, changed-record discovery, baseline loader.
- tests/test_citation_lint.py (336 lines) - the founding fixture battery,
  8 pytest cases; the CLI `--selftest` runs it in-process under a recursion
  guard.
- githooks/pre-push - one enforcing block wired directly after the ratchet,
  per the register fill spec's "wire one line into githooks/pre-push after
  the ratchet".
- AGENTS.md build discipline - the gate law bullet beside the ratchet bullet.

## The founding fixture, and the errata that beat me to it

The ask's founding test fixture: STORY.md:240's 191.8M-token headline must
FAIL the lint. While this lane built the tool, register row 4's errata landed
in a sibling lane: STORY.md now carries the strike note ("the clause '191.8M
tokens spent' that stood here is STRUCK; its named source DIGEST.md has zero
'191' hits"). The live file no longer carries the phantom, so the live-demo
run correctly stays silent on it. The fixture therefore lives VERBATIM
(STORY.md lines 225 to 243 as they stood) inside tests/test_citation_lint.py,
never read from the live file, and the fixture test proves the founding
failure: PHANTOM-NUMBER on 191.8M, exactly one, blocking, with the
seed_percolator.py:6-16 control cite clean in the same paragraph. This was a
design bet that paid: the fixture survives the errata.

The live STORY.md run is not empty anyway: the gate catches a different
untraced quantity in the same record ("zero of 46,531 biography files
binding it", STORY.md:72), absent from all three of its sentence's named
sources. That finding now belongs to whichever lane owns STORY.md's errata
follow-up: cite a source that carries 46,531, downgrade the claim, or accept
the finding by name in configs/citation_lint_baseline.json.

## The GAP_REGISTER proof run (fill spec 3)

Command: check --files over the six ractor50 chapters holding the 12
spot-checked cites, with --enforce-tokens. Result (check.txt CHECK 2):

- Drift 1 CAUGHT: watch/inbox/ractor50/mcp.md:44 and mcp.md:316 both fire
  TOKEN-MISS on mag/mcp_server.py lines 338-340 (the check_drift wiring
  moved to :344/:356/:358; lines 338-340 hold `return DEFAULT_LEDGER`).
- Drift 2 CAUGHT: watch/inbox/ractor50/communication.md:18 fires TOKEN-MISS
  on mag/biography.py lines 526-526 (the write moved to :390 via
  evict_for_prepend; line 526 is themes parsing).
- Blocking findings beyond the drifts: exactly two, both PATH-MISSING on
  accuracy.md:75/77 for core/src/tool/handlers/bash.ts and
  core/src/runtime/compact/policy.ts, the f-25 wrong-path defects the
  accuracy lane itself flagged as never folded back. True positives.
- Of the 10 clean cites: 8 produce zero findings; 2 produce warn-class
  TOKEN-MISS where the a05 lane's byte-read says the span content is right
  (workflow_gate.py lines 51-53, MCP_MANIFEST_SPEC.md lines 96-97) and the
  claim tokens just do not overlap the span words. Warn-only, never blocking.
- Shorthand forms (SKILL.md:26-29, ladder-02.md:73, biography.py:526 without
  dir) resolve through the single-hit git-index fallback where unique, and
  warn otherwise. ladder-02.md:73 and fold_gate.sh:14-24 resolve cleanly.

## Precision, paid for in live fires (the honest part)

The first whole-file runs manufactured thousands of false fires; every cut
below is named because a real record paid for it:

- Paragraph-level pairing fired on measurements of files (a file's byte size
  lives outside its own content: 18,212 bytes of w4-20.md) and on counts no
  source should contain. Pairing is now per SENTENCE.
- Co-sentential code paths hijacked pairing (a number beside a tools/*.py
  anchor is not attributed to that code file): phantom sources are record
  surfaces only (md/txt/rst/jsonl/json).
- Identifier shapes excluded: 8-digit date compounds, arXiv ids, floats with
  over 3 fractional digits, hyphen-attached ids (B2-125, UF-119), IP:port
  shapes, colon-attached ports (:8765), sed print ranges (238,242p),
  non-grouping comma id lists (2,3,4,7), line/row refs after a path or
  anchor, ref-list continuations, ref words before the number ("line 131
  (AGENTS.md)"), and disk/census unit nouns (records/rows/bytes/lines/tests
  and kin: the count class is B2-216's, census_drift_patrol is its carrier).
- The --changed scope scans untracked files NOT at all: two sibling lanes'
  untracked work logs carried 3,711 of the 3,805 fires in the first shared
  tree run, and untracked files are not push content. Staged-new records
  stay covered (git diff HEAD includes staged adds). Saved instrument
  output (*.check.txt, *.extract.txt) is evidence, not authored claims, and
  is skipped.
- Cost: the first --changed run took 9m34s and then 3m49s against the shared
  tree; final battery runs it in 5.8s (containment cache, one-read-per-source
  cache up to 16MB, oversize-source skip at 256MB where a number is
  unverifiable rather than phantom, resolution cache, 2.5GB index surfaces
  streamed never loaded).

## Enforcement posture

ENFORCING at the hook like the ratchet, on the deterministic classes only
(PATH-MISSING, LINE-OOB, EMPTY-SPAN, PHANTOM-NUMBER). TOKEN-MISS and
SHORTHAND-UNRESOLVED are warn-only heuristics (--enforce-tokens flips them;
that is the mode the proof run used). Escape hatch is the ratchet's own law:
accept a finding by NAME in configs/citation_lint_baseline.json (zero rows
day one; none needed for this landing). The tool's own output renders cited
spans in prose form ("lines 338-340") rather than colon-digit form, so saved
gate output does not re-arm the lint when the output lands in a scanned
record.

## Ratchet and gates

- Ratchet: the lane's three tool modules and the test file contribute ZERO
  new debt (file-too-long fixed by the module split, two except-pass sites
  replaced with explicit handling). The ratchet still exits 1 on THIS shared
  tree: the remaining NEW rows are sibling files (tools/code_swarm.py,
  tools/reverse_map.py, tools/tier_probe.py, all just over the 400-line cap,
  uncommitted at this landing) plus a GROWTH claim on mag/percolator.py
  (accepted at 580, now 745). Those belong to their own lanes; this lane did
  not accept another lane's debt. Evidence: check.txt CHECK 6 and the
  appended post-fix rerun.
- Census patrol after the AGENTS.md edit: ok (check.txt CHECK 7).
- pytest tests/test_citation_lint.py: 8 passed (check.txt CHECK 5 and the
  appended rerun).
- Em-dash scan over the lane's authored files: zero (check.txt CHECK 8;
  pre-push and AGENTS.md carry pre-existing em-dashes from earlier landings,
  the blocks this lane added scan clean).

## Shared-tree findings that are not this lane's (handed to their owners)

- watch/inbox/48h_synth/STORY.md:72, the 46,531 phantom (above).
- watch/inbox/model_garden/SWARM_1.md:55, EMPTY-SPAN: cites mag/gpu_ghost.py
  lines 174-174, a blank line.
- watch/inbox/model_garden/STOCHASTIC_LENSING.md:44, two phantom quantities
  (8062, 2419) absent from all three named sources.
- The mcp.md:166 and workflow_gate.py:51-53 token-warn FPs noted above, if
  they annoy, are baseline-able by name.

## Decision ledger

Closes GAP_REGISTER rank 3 (meta-gap 3, the phantom-citation class, at
pre-push). Changes one standing contract: pushes that touch prose records
now run a citation byte-check after the ratchet, enforcing on deterministic
defects, warning on heuristics, accepting debt by name only. Names one
follow-up outside this lane: f-25's three playbook citation fixes are still
never folded back into corpus/steal/ZCODE_OPERATING_PLAYBOOK_20260925.md
(the two wrong paths this gate now blocks on, in changed records, are the
proof that filing corrections is not applying them).
