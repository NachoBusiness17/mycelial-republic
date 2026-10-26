# D3_roast_adjudication (anthropic/claude-opus-5.5, turn 1, channel: content)

# Doctrine Roast, Movement 3: Adjudication

## Conditions of this read

These apply to every verdict below unless a section overrides them.

**Instrument.** I read five pasted blocks:
- `watch/inbox/hermes_burn/MOVEMENT2_CHEAP_ANSWERS.md`, including the appended "MOVEMENT 3, CHEAP-ARM ANSWERS" section
- `watch/inbox/hermes_burn/D2_movement2_adjudication.md`
- `memory/runs/hermes_burn/socratic2_results.jsonl`
- `watch/inbox/ractor50/skills.md`
- `watch/inbox/ractor50/communication.md`

I ran no commands.

**Moment.** Single pass, movement 3, this session.

**Context assumptions.**
- Pasted bytes equal on-disk bytes, with no reflow.

**Not in evidence this session.**
- `tools/workflow_gate.py`. Its quotes are reused from my movement-2 receipt.
- `logic.md`, `accuracy.md`, `operations.md`.
- The selfsteal and mcp chapters.
- `DAY_PACK.md`, `B2_16_uf_sweep_20260926.md`, `.gitignore`.

Every pin into these files is either the cheap arm's report or UNVERIFIED.

**Line pins.**
- `socratic2_results.jsonl:1-4` is countable: one JSON object per line, in the order skills, communication, selfsteal, mcp.
- Pins into `skills.md` and `communication.md` are section anchors plus quoted bytes. Their line numbers are UNVERIFIED, because the pasted blocks are wrapped and a hand count of wrapped prose is the hand-copied-count class.

**Arithmetic.** Two figures in this receipt are my own computation, shown in full so they can be recomputed: the skills byte delta and the gate return-site count.

---

## (1) T1: Amended L1 CLOSES on the gate side; four residues remain

### What the cheap arm's bytes settle

The cheap arm reports this (MOVEMENT2_CHEAP_ANSWERS.md, "MOVEMENT 3" item 1):

> "tools/workflow_gate.py returns 1 (soft, lines 216/298), 2 (block, 269/313), 0 (pass, 271)"

- **Two `return 1` sites.** My movement-2 table listed exactly two: the `main()` read error and the `run_scenarios()` empty card dir. The count matches.
- **My falsifier did not fire.** It read: "T1's grep finds a `return 1` I did not list, or my quoted `return 1` sites are absent on disk."
- **Amended L1 closes on the code side.** Exit 1 exists. It is the could-not-evaluate path, not a warn. Neither logic.md mapping matches.

### Residues, each with the reason it is open

| ID | Residue | Why it stays open |
|---|---|---|
| R1 | Return-site count mismatch: 5 lines reported, 7 expected. | My movement-2 table quotes 7 distinct return lines: `return 0` (main tail), `return 2 if failed else 0`, `return 0` (run_scenarios), two `return 1`, `return 2` (main), `return 2` (run_scenarios). A `grep -n "return [012]\b"` matches each of the 7 once. The cheap arm reports 5. Either its grep was narrower, or two of my quoted lines are absent on disk. |
| R2 | The cheap arm labels exit 1 "(soft ...)". | The label carries no quoted bytes. "Soft" is the mapping-1 reading that amended L1 rejects: soft rows exit 0 via `failed = [r["id"] for r in rows if not r["ok"] and not r.get("soft")]`, a movement-2 quote. The label is a report, not bytes. It is the same "report as verdict" defect as movement 2's C1. |
| R3 | Callers are unread. | No `rg workflow_gate` output exists. C2 ("exit 1 never blocks a push") is still unanswerable, and so is the clause of my amendment that reads "how any caller treats exit 1 is UNVERIFIED". |
| R4 | The amendment's three-run falsifier is unrun, and logic.md is unpinned. | There are no `wc -l` before/after deltas for exit 1/0 rows, 2/1 rows and 0/0 rows. logic.md's law-1 lines are still unpinned. |

### Verdict

Amended L1 stands as stated in movement 2: neither mapping matches the code. The gate-side half is closed. The amendment sentence in D2_movement2_adjudication.md section (4) is landable today with its final UNVERIFIED clause intact. It must not be shortened until R3 closes. T4 below runs R1-R4.

**Negative example of closing early.** Deleting "how any caller treats exit 1 is UNVERIFIED" on the strength of "D2's amended L1 settles" would convert a cheap-arm report into doctrine. That is the move estate law 1 forbids ("Trust bytes, not reports").

---

## (2) T2: Objection 1 CONFIRMED; the accuracy.md amendment it earns

### What the bytes split into

The cheap arm quotes two defects inside one UF-124 answer (MOVEMENT2_CHEAP_ANSWERS.md, "MOVEMENT 3" item 2). Their exact line inside DAY_PACK.md is UNVERIFIED beyond the cheap arm's 2056.

| Defect | Quoted bytes | Would an id-existence resolver catch it? |
|---|---|---|
| D-a | "openreview.net/forum?id=XYZ" | **Yes.** A placeholder id fetches nothing real. |
| D-b | "Constitutional AI - OpenAI" | **No.** Existence cannot see attribution. If the claim carries the real paper's id, the id resolves and the wrong organization passes. |

### Out-doing the cheap arm

The cheap arm writes "the accuracy chapter's proposed citation-resolution gate would have caught it." That is true of the answer, but only by co-occurrence: D-a fails, so the answer fails. D-b, which is objection 1's actual target, would pass alone.

- **Negative example.** Strip the placeholder, cite the real Constitutional AI paper id, and keep "OpenAI". The id-only gate returns PASS.
- **Status of the paper id.** I take the id as arXiv 2212.08073, Bai et al. 2022, Anthropic. That comes from my training, not from corpus bytes, so the id is UNVERIFIED in-estate until T5 fetches it.

So objection 1 stands on D-b. The resolver's value on D-a is real and not hypothetical. That is the second half of the cheap arm's finding, and it holds.

### Placement

Replace the existence-only wording that movement 1 quoted from accuracy.md: "each id must resolve to fetched bytes". Its line in accuracy.md is UNVERIFIED and is re-pinned by T5.

### Paste-able sentence

> A citation resolves only when its id fetches real bytes in the same session (a placeholder such as `openreview.net/forum?id=XYZ` fails here) AND every attribute the claim asserts about that source (author, organization, year, venue, effect size) appears in those fetched bytes; an id that resolves while an asserted attribute is absent from or contradicted by the fetched bytes is a FAIL, as in UF-124, where "Constitutional AI - OpenAI" attributes an Anthropic paper to OpenAI (watch/inbox/union_fullsend_20260917/DAY_PACK.md:2056, per the cheap-arm read).

### How the sentence sorts cases

| Case | Input | Under the old wording | Under the amendment |
|---|---|---|---|
| Positive | Real CAI id, claim says "Anthropic" | PASS | PASS (the attribute is present in the fetched author/affiliation bytes) |
| Positive | `id=XYZ` | FAIL | FAIL (clause 1) |
| Negative, the gap closed | Real CAI id, claim says "OpenAI" | **PASS** | **FAIL** (clause 2) |
| Negative, scope limit | Claim asserts no attribute beyond the title | PASS | PASS. The amendment checks asserted attributes only, so it does not invent checks for claims that make none. |

### Falsifier for this amendment

The amendment is not landed, or is wrong, if either of these happens:

1. The gate is fed the UF-124 answer with `id=XYZ` replaced by the fetched CAI id and "OpenAI" kept, and it returns PASS.
2. T5's fetch shows that the CAI paper's own bytes list OpenAI affiliation.

---

## (3) T3: O1 confirmed; minimal cure is force-track plus one law line

### Bytes relied on

- The cheap arm reports "`.zcode/workflows/the-gala.dwf.ts` is NOT git-tracked (pathspec error; .gitignore:198 covers .zcode/)" (MOVEMENT2_CHEAP_ANSWERS.md, "MOVEMENT 3" item 3).
- `.gitignore:198`'s bytes are not quoted. The pattern is therefore UNVERIFIED as exactly `.zcode/`.

### The two options compared

| | Option A: `git add -f` the one file, plus a law line | Option B: move the canonical copy into a tracked path |
|---|---|---|
| Cost | One command and one sentence. | A path change, plus either a tool reconfiguration or a sync step. |
| Continuity | Once tracked, ignore rules stop applying to that file. This is git behavior, documented in gitignore(5); it is stdlib-class and not corpus bytes. Every later edit is visible in `git diff`. | Tracked from birth. |
| Failure mode | The exception is invisible in `.gitignore`. Sibling drafts named in skills.md section 6 stay untracked: "Read: .zcode/workflow-drafts/firehose.dwf.ts ..., mickey17-wave3.dwf.ts, mirror-mine.dwf.ts". | Two copies, one read by the tool and one by git. That creates a new "which copy is canonical" census question. It is the relay-overwrite class that communication.md D2 forbids: "no relay surface may overwrite its predecessor while untracked". |
| Lineage | The path is unchanged, so registry rows naming `the-gala.dwf.ts` keep pointing at the same file. | Another path change. D2 already noted rows 41-44 absolute versus row 45 relative. A third path form adds to the drift. |

**Why the negation alternative does not work.** A negation such as `!.zcode/workflows/the-gala.dwf.ts` cannot re-include a file whose parent directory is excluded by a directory pattern. This is also gitignore(5) behavior. So "just un-ignore it" requires restructuring line 198, which is a larger edit than Option A.

### Verdict

Option A is the minimal cure. It is one file, it keeps the path, and its trade-off (an invisible exception) is cured by the law line itself.

### The cure as landable steps

1. **Pre-flight.** Run a secret scan of the file, in T6. `.zcode/` may be ignored for a reason.
2. **Track.** `git add -f .zcode/workflows/the-gala.dwf.ts && git commit -m "track the-gala.dwf.ts (O1 continuity cure)"`
3. **Paste the law line into operations.md.** Its section is UNVERIFIED because the chapter is not in evidence:

> Any saved workflow that has a row in memory/workflows/REGISTRY.jsonl and lives under the gitignored .zcode/ tree is force-tracked with `git add -f` in the same commit as its first registry row, and `git ls-files --error-unmatch <path>` exiting nonzero for a registered workflow is a continuity defect.

### Examples

- **Positive.** A fresh clone runs `git ls-files --error-unmatch .zcode/workflows/the-gala.dwf.ts` and gets exit 0.
- **Negative.** A new registered wave workflow is saved under `.zcode/workflows/` with no `-f` commit. The law names this as a defect, not as tolerated drift.

### Falsifier for the cure

The cure has not worked if either of these holds:

1. A fresh clone lacks the file.
2. The tracked blob's content disagrees with the registry digest for row 45 (`2285b0104993`, from D2 section 2).

How the gate computes that digest is UNVERIFIED, so T6 reads it first. If the digest is not content-derived, this half of the falsifier is void and only the clone check stands.

---

## (4) Socratic batch 2: adjudication on quoted bytes

### A pattern across all four outputs

None of the four socratic outputs quotes a single byte of the chapter it attacks (`socratic2_results.jsonl:1-4`). The communication output even instructs "Quote the row pairing them and the contradiction is visible" (`:2`) without quoting it.

The cost fields are $0.000282-0.000303 per chapter. That cost fits a reader of a summary row rather than the chapter. The fit is my inference and is UNVERIFIED, but it predicts the law-name mismatch found in C-2 below.

### Skills (`socratic2_results.jsonl:1` against `watch/inbox/ractor50/skills.md`)

**S-1. Premise: "waves
