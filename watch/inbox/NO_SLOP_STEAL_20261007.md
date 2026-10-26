# NO_SLOP_STEAL_20261007 - the no-ai-slop steal, the patrol, and the honest self-audit

source-fetched: 2026-10-07

Operator GO: "Love it brother... lets tighten up yes" (2026-10-05, on
petergyang/no-ai-slop). This lane stole the skill, built the deterministic
patrol, wired it WARN-only, and pointed it at our own prose. Audit only, no
fixes. The numbers below stand as the baseline.

## 1. The steal

- Source: `https://raw.githubusercontent.com/petergyang/no-ai-slop/main/skills/no-ai-slop/SKILL.md`
  (10,853 bytes) and the sibling `eval.md` (3,214 bytes), MIT license.
- Banked near-verbatim at `.agents/skills/no-slop/SKILL.md` (12,749 bytes)
  and `.agents/skills/no-slop/eval.md` (3,311 bytes, one provenance comment
  prepended). Source frontmatter name `no-ai-slop` renamed `no-slop`; the
  body is unchanged source text.
- Estate prelude (`.agents/skills/no-slop/SKILL.md:5-40`) carries the credit
  plus the additions. The em-dash law stays absolute (zero em-dash
  characters in estate-written files, stricter than the source's 1-2
  allowance), the marathon-law outcomes-first rule applies, and the estate
  prose targets are named (dawn reports, LINKS rows, receipts, dossiers,
  paste-ready comms). Both banked files carry zero em-dash bytes (held by
  test in `tests/test_prepush_slop_patrol.py`).

## 2. The patrol

`tools/prepush_slop_patrol.py` is a DETERMINISTIC detector, no model calls,
holding the regexable subset of the skill:

| Class | Shape |
| --- | --- |
| BANNED-WORD | the operator's list (`delve`, `foster`, `leverage`, `utilize`, `facilitate`, `empower`, `streamline`, `robust`, `cutting-edge`, `paradigm shift`, `game changer`, `tapestry`, `realm`, `beacon`, `multifaceted`, `meticulous`, `paramount`, `transformative`, `elevate`, `embark`, `supercharge`, `ever-evolving`, `this is huge`, `this changes everything`), word-boundary, case-insensitive |
| BINARY-CONTRAST | `not just X but Y`, `it's not X, it's Y` (cross-sentence form included), `the question isn't X` |
| THROAT-CLEAR | `here's the thing`, `let me be clear`, `the uncomfortable truth`, `what nobody tells you`, `the part everyone misses` |
| COLON-REVEAL | noun-phrase (2+ words) colon lowercase clause, structural heuristic; single-word label rows (`Spec:`), markdown structure, table pipes, and URLs are excluded |
| FAKE-PROFOUND | the `future-isn't-coming-it's-already-here` and `that's-it-that's-the-whole-thing` kickers |

Exemptions: fenced code blocks and inline backtick spans (quoting a banned
word as an example is the skill's own sanctioned move). CLI
`check --changed` (prose records vs HEAD, the citation_lint discipline; data
`.jsonl` never enters through `--changed`) or `check --files` (explicit
paths; a `.jsonl` is scanned by `title` field only, the LINKS audit shape).
ALL classes WARN; zero baseline day one
(`configs/prepush_slop_baseline.json`, absent = zero accepted); accept a
finding by FINGERPRINT (class + file + offending line text), never
mass-import. Wired append-only at the tail of `githooks/pre-push:553-591`
as a WARN-ONLY block (findings print, the push is never blocked; output
contract first line `SLOP-PATROL: ok` / `SLOP-PATROL: WARN`).

## 3. THE SELF-AUDIT (audit only, no fixes)

Instrument (named per the census denominator law): the tool above, one run
per target, 2026-10-07 evening, commands verbatim below. The counts are one
moment's snapshot of a moving tree.

| Target | BANNED-WORD | BINARY-CONTRAST | THROAT-CLEAR | COLON-REVEAL | FAKE-PROFOUND | total |
| --- | --- | --- | --- | --- | --- | --- |
| `watch/inbox/DAWN_REPORT_20261006.md` | 0 | 0 | 0 | 4 | 0 | 4 |
| `watch/inbox/DAWN_REPORT_20261007.md` | absent | absent | absent | absent | absent | absent |
| `watch/inbox/LINKS.jsonl` last 200 titles | 1 | 0 | 0 | 25 | 0 | 26 |
| `memory/corpus/LINKS.jsonl` last 200 titles | 4 | 0 | 0 | 28 | 0 | 32 |

Commands and verbatim head lines:

```
.venv/Scripts/python.exe tools/prepush_slop_patrol.py check --files watch/inbox/DAWN_REPORT_20261006.md
SLOP-PATROL: WARN - scanned 1 file(s), 4 finding(s) (0 accepted by fingerprint); by class: BANNED-WORD=0 BINARY-CONTRAST=0 THROAT-CLEAR=0 COLON-REVEAL=4 FAKE-PROFOUND=0
```

```
tail -200 watch/inbox/LINKS.jsonl > $TEMP/links_inbox_last200.jsonl
.venv/Scripts/python.exe tools/prepush_slop_patrol.py check --files $TEMP/links_inbox_last200.jsonl
SLOP-PATROL: WARN - scanned 1 file(s), 26 finding(s) (0 accepted by fingerprint); by class: BANNED-WORD=1 BINARY-CONTRAST=0 THROAT-CLEAR=0 COLON-REVEAL=25 FAKE-PROFOUND=0
```

```
tail -200 memory/corpus/LINKS.jsonl > $TEMP/links_corpus_last200.jsonl
.venv/Scripts/python.exe tools/prepush_slop_patrol.py check --files $TEMP/links_corpus_last200.jsonl
SLOP-PATROL: WARN - scanned 1 file(s), 32 finding(s) (0 accepted by fingerprint); by class: BANNED-WORD=4 BINARY-CONTRAST=0 THROAT-CLEAR=0 COLON-REVEAL=28 FAKE-PROFOUND=0
```

Worst offenders, named shamelessly (quoted in backticks; verbatim title or
line text):

- Genuine reveal-shaped slop in our own titles:
  `THE PARABLE OF THE FIELD AND THE STONES: value lies in the emptiness the stones define`
  (watch/inbox/LINKS.jsonl, slice row 6) and
  `the mirror thesis: the overlay is the sovereignty`
  (memory/corpus/LINKS.jsonl, slice row 48).
- Banned words by the seat's own hand:
  `batch-elevate to grok` (`elevate`, corpus slice row 65) and
  `leverage` in a steal shortlist title (corpus slice row 118). The other
  `robust` hits (inbox slice row 152, corpus slice rows 13 and 70) sit
  inside quoted third-party paper or wave titles.
- COLON-REVEAL noise, honestly split: most of the 57 colon hits are the
  seat's functional label-row title convention
  (`Lanes stable: openrouter 464, groq 11, mistral 46`), which is a tic, not
  drama; a minority are real dramatic reveals like
  `Gate honesty: the gate's PASS is a narrow, inspectable predicate`
  (corpus slice row 37) and the dawn report's
  `one input from you: wallet addresses.` (watch/inbox/DAWN_REPORT_20261006.md:59).
- Clean classes: BINARY-CONTRAST, THROAT-CLEAR, and FAKE-PROFOUND read
  ZERO across all three audited surfaces. The operator's instincts were
  right about which disease we actually have.

The wired `--changed` path also ran once on the working tree at filing time
(29 changed prose files, 14 findings; the 2 BANNED-WORD hits are `beacon`
rows in the elder lane docs, the 12 COLON-REVEAL rows include this steal's
own audit targets). None were fixed by this lane; the baseline stays zero
and the findings stand for triage.

## 4. Voice versus slop (the classification)

Operator-voice, PROTECTED (his coined lines, never to be sanded):

- `Trust bytes, not reports.` lives as the bolded test-discipline law in the
  AGENTS.md Tests bullet (AGENTS.md:29, 492 `trust bytes` grep rows across
  the estate's prose surfaces). Not matched by any detector class.
- `the cave keeps repeating`: zero exact hits on disk (grepped across
  watch/, state/, memory/, docs/, queue/, corpus/steal/, AGENTS.md). His
  spoken coin from prompts; it lives in his voice, not our prose.
- `the machine working`: zero exact hits. `the machine` reads 2,204 rows,
  overwhelmingly functional estate vocabulary (machine room, machine
  contract, machine-readable). Operator register plus estate function, not
  slop.

Seat-slop, OUR tics (named shamelessly; grep surfaces over watch/, state/,
memory/, docs/, AGENTS.md, which include harvested third-party prose under
memory/, so these are surfaces, not verdicts):

- The label-colon-payload title convention (the 57 COLON-REVEAL audit hits
  above): functional, but it is also the shape the skill warns about; worth
  thinning in paste-ready comms.
- The X-disease metaphor (`the same byte disease`, `stale-trap disease`):
  1,256 `disease` rows. Seat tic.
- `in a new costume` (1,040 rows), `in silence` (243 rows),
  `in money form` (14 rows), and `the honest X` opener (3,961 rows, worst
  surface count of the set). All seat tics; none are on the detector's
  lists (they resist a word list, which is exactly what the judgment-layer
  skill is for).

## 5. Gate numbers

- Tests: 13 passed in the new battery
  (`tests/test_prepush_slop_patrol.py`: slop fixture trips every class with
  exact per-class counts, clean estate prose passes, fence and backtick
  exemptions hold, fingerprint stable under line shift, baseline accepts by
  fingerprint, jsonl title mode with malformed-row tolerance, CLI
  cannot-verify shapes, em-dash law held on the tool and skill bytes).
- Full-suite `pytest -q` at filing: 4,371 passed, 42 failed, 8 skipped in
  1,814s (instrument `pytest -q` with the pytest.ini default testpaths,
  moment 2026-10-07T22:05-22:35 EDT local; the 42 reds are pre-existing
  sibling-lane and environment failures on the shared tree, none in
  `tests/test_prepush_slop_patrol.py`; the census carrier in AGENTS.md owns
  the tree-wide collected count and was NOT refreshed by this lane).
- citation_lint on this receipt: clean (run logged in the session).

## 6. Blockers

None. Open operator calls: (a) triage or accept the standing findings into
`configs/prepush_slop_baseline.json`; (b) the WARN-to-enforce flip after a
few clean weeks; (c) whether the label-colon title convention gets thinned
or formally accepted as estate voice.
