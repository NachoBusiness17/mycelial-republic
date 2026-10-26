# PA-D3-qwen38max (qwen/qwen3.8-max-prime @ nous, turn 1, channel: content)

# MOVEMENT 3 ADJUDICATION

## Conditions

- Instrument: pasted evidence blocks (00 through 04), no commands run.
- Moment: single pass, movement 3.
- Context assumptions: pasted bytes equal on-disk bytes; truncated blocks (skills.md, communication.md, D2 adjudication) mean some pins into their tails are UNVERIFIED.
- selfsteal and mcp chapter source files are NOT in evidence. All pins into them are UNVERIFIED.

---

## (1) T1: Amended L1 - Residue Remains

The cheap arm confirmed exit sites at named lines: return 1 (lines 216/298), return 2 (lines 269/313), return 0 (line 271). The trivalent contract exists in the code.

Amended L1 (from D2 adjudication): "logic.md states two mappings, and neither matches the code." T1 confirms the exit sites are byte-true. The amendment holds.

Residue that does NOT close:

- R1. The docstring at tools/workflow_gate.py:10 says "every submission registers a row." Three paths register none: the exit-1 read-error return, the --no-register flag path, and the --scenarios path. The docstring is stale relative to its own flags.
- R2. Whether any caller maps exit 1 to a blocking action is unanswerable from workflow_gate.py alone. The token "push" appears nowhere in the file. The caller surface is unexamined.
- R3. logic.md's two mappings remain wrong against the code (mapping 1 misplaces warn at exit 1; mapping 2 swaps 1 and 2). T1 settles that the exits exist; it does not settle that the documentation matches.

Verdict: amended L1 survives with residue R1-R3. The chapter's claim about exit codes is byte-true at the call sites but the surrounding documentation (docstring + logic.md mappings) is stale or wrong.

---

## (2) T2: UF-124 Confirmed - Landable Amendment

Confirmed bytes: DAY_PACK.md:2056 carries "openreview.net/forum?id=XYZ" (literal placeholder) and "Constitutional AI - OpenAI" (misattributes Anthropic's paper to OpenAI).

Landable amendment to accuracy.md (one paste-able sentence):

```
Every citation that carries a URL must resolve to a non-placeholder id and its attributed author list must match the paper's actual author list before the citation enters any digest, receipt, or doctrine line; a citation failing either check is marked UF-UNRESOLVED and excluded from downstream claims until resolved.
```

Falsifier for this amendment: a single legitimate citation that uses a placeholder id by design (e.g., an internal DOI scheme) and still carries correct attribution would break the rule. If such a scheme exists in the estate, the amendment needs a carve-out naming it.

---

## (3) T3: the-gala.dwf.ts - Minimal Cure

Confirmed: .zcode/workflows/the-gala.dwf.ts is untracked; .gitignore:198 covers .zcode/; the file is single-disk-only.

Two cures, one trade-off:

**Cure A (recommended): git add -f + standing law line.**

```
git add -f .zcode/workflows/the-gala.dwf.ts
```

Standing law line (add to AGENTS.md or equivalent boot doc):

```
.zcode/workflows/*.dwf.ts files that drive estate waves are tracked via git add -f; the .gitignore exclusion of .zcode/ does not apply to wave-driving workflows.
```

Trade-off: the file enters git history despite the directory-level ignore. Future .zcode/ files that are NOT wave-driving still need the -f flag to land, which is friction. The alternative (negating the ignore rule for a subpath) is cleaner but requires a .gitignore edit that may surprise other seats.

**Cure B: move the canonical copy into a tracked path.**

```
cp .zcode/workflows/the-gala.dwf.ts memory/workflows/the-gala.dwf.ts
git add memory/workflows/the-gala.dwf.ts
```

Trade-off: the workflow runner must now resolve from the new path. If the runner hardcodes .zcode/workflows/, the copy is a dead mirror that drifts. This cure is only safe if the runner is patched to read from the tracked path.

Recommendation: Cure A. It is one command, one law line, and does not require runner changes.

---

## (4) Socratic Batch 2: Adjudication

### socratic-skills

Objection 1: "waves are the fuzzer, cards are the commits" assumes coverage it never measures.

Adjudication: OUT-DO. The chapter itself names this gap. skills.md section 0 states the census drift (+2 skills, +9,112 bytes) and names the 141-byte micro-drift as "unattributed... not investigated further, named honestly." The chapter does not claim coverage; it claims verdicts from observed evidence and names what it did not measure. The socratic objection attacks a premise the chapter does not hold.

However, the objection's core survives in a narrower form: the 5 PROMOTE verdicts rest on liveness evidence (engine exists, test exists, registered in yaml) but none of them cite a wave that exercised the skill's failure mode. The chapter's own verdict ladder says PROMOTE = "give the skill work or teeth this week" - the promotes are forward-looking commitments, not backward-looking proofs. The socratic objection is right that promotion keyed to wave pass rate without failure-mode probing is weak, but wrong that the chapter is unaware of this.

Objection 2: The 5 promotes are the weakest column.

Adjudication: CONFIRMED. The chapter's own evidence column for promotes cites wiring (chord.py:66, skills.yaml registration, gate G2 codification) but not failure-mode exercise. The demotes and kills at least cite negative signals (zero invocations, unmet promotion gates, dead doors). The asymmetry is real and the chapter does not name it.

Objection 3: False-negative rate of the fuzzer never validated.

Adjudication: CONFIRMED. No byte in the skills chapter measures whether the wave instrument can detect the failures it claims to screen for. The chapter verdicts 18 skills without instrument validation.

### socratic-communication

Objection 1: "content" as a stable relay unit is unexamined.

Adjudication: OUT-DO. The chapter explicitly documents that content identity is NOT stable. Breakage 3 shows the same decision expressed under different key names (events-door used `decision`, patrol-fix used `decision_ledger`), causing the fold gate to undercount (10 vs 12). The chapter's own Doctrine D2 (relay contract) addresses this by requiring a content-total in the fold. The socratic objection names a problem the chapter already found and partially repaired.

Objection 2: only-deck-only-steps-die contradicts severity-owns-retention.

Adjudication: CONFIRMED with nuance. The chapter documents that severity was anti-correlated with retention in the attention.md surface (w4-09 finding: prepend-ring beheads at 40,441 bytes; appended alerts at the bottom are evicted first). The chapter names this as a bug and banks a repair (wave5 attention-channel lane). But the doctrine laws D2/D3 do not explicitly resolve the contradiction between position-based retention (deck steps die) and severity-based retention. The contradiction is documented but not legislated away.

Objection 3: Who assigns severity, and can that assigner be wrong?

Adjudication: CONFIRMED. The chapter does not name the severity assigner or a dispute mechanism. The attention.md surface was written by multiple agents (biography.py prepends, improve.py appends, census_patrol_daily.ps1 appends) with no arbiter. The chapter's repair (whole-block eviction with preserved alert tail) mitigates the symptom but does not name who decides what is severe.

### socratic-selfsteal

Objection 1: The "self" is assumed to exist prior to the mechanisms that constitute it.

Adjudication: CANNOT ADJUDICATE. The selfsteal chapter source is not in evidence. The socratic objection's claim about "9 prior-wave mechanisms" and "tri-state finish-line table" cannot be checked against bytes. Marked UNVERIFIED.

Objection 2: 8 line-pinned defects against 9 steals reads as padding.

Adjudication: CANNOT ADJUDICATE. No source bytes available. The ratio claim (8:9 near 1:1) is plausible as a structural observation but cannot be confirmed or refuted without the chapter text. UNVERIFIED.

Objection 3: No falsification condition for the theft claim.

Adjudication: CANNOT ADJUDICATE on bytes. However, the objection is structurally sound: any claim of theft that lacks a stated condition under which independent derivation would be recognized is unfalsifiable by construction. This holds regardless of the chapter's specific content. The objection stands as a structural critique even without byte confirmation.

### socratic-mcp

Objection 1: "never-crosses" boundary moves with schema edits, making the table a snapshot not a law.

Adjudication: CANNOT ADJUDICATE. The mcp chapter source is not in evidence. The objection's logic is sound (a boundary that moves with routine edits is not a stable law) but cannot be confirmed against chapter bytes. UNVERIFIED.

Objection 2: Four-clause metering is circular if reordering preserves admission.

Adjudication: CANNOT ADJUDICATE on bytes. The structural critique (if clause order is negotiable, the clauses are not independently load-bearing) is valid as logic but unconfirmed against source. UNVERIFIED.

Objection 3: No tiebreaker named when bridge admits what never-crosses forbids.

Adjudication: CANNOT ADJUDICATE on bytes. Same structural validity argument as selfsteal objection 3: an admission system without a named tiebreaker resolves by scheduling, not doctrine. UNVERIFIED against source, structurally sound.

---

## (5) Landable Amendments (one per chapter)

**skills.md:**

```
Add after the verdict table: "PROMOTE verdicts require at least one wave that exercised the skill's failure mode, not merely its liveness. A skill that passes because the fuzzer never probed its edge is indistinguishable from one that passes because it is sound; the promote column must name the probe or carry the tag UNPROBED."
```

**communication.md:**

```
Add to Doctrine D2 (relay contract): "Severity is assigned by the producing seat and may be disputed by any consuming seat; a severity dispute freezes the affected content's eviction until the next fold adjudicates. No single writer owns the severity label."
```

**selfsteal.md (UNVERIFIED - no source bytes; amendment is structural):**

```
Add: "A re-steal claim is falsifiable if and only if it names a condition under which the mechanism would be recognized as independently derived. A theft claim without that condition is confirmation, not triangulation, and is marked UNFALSIFIABLE."
```

**mcp.md (UNVERIFIED - no source bytes; amendment is structural):**

```
Add: "The never-crosses table is a snapshot at schema version N. Any schema edit that changes the boundary must re-run the admission test and log the delta. Admission disputes between the bridge and the table are resolved by the schema version timestamp: the table at the admission moment governs, not the table at the dispute moment."
```

---

## (6) Next 3 Dig Tickets (commands only)

**Ticket D3-T1: Caller surface of workflow_gate.py exit 1.**

```
grep -rn "workflow_gate" --include="*.py" --include="*.sh" --include="*.ts" --include="*.dwf.ts" . | grep -v "workflow_gate.py" | grep -v __pycache__ | head -30
grep -rn "exit_code\|returncode\|\.returncode" --include="*.py" --include="*.sh" . | grep -i "gate\|workflow" | head -20
```

**Ticket D3-T2: Severity assignment surface in attention.md writers.**

```
grep -n "severity\|SEVERITY" mag/biography.py mag/improve.py mag/act.py scripts/census_patrol_daily.ps1 memory/attention.md 2>/dev/null | head -20
grep -n "attention_flag\|attention\.md" mag/*.py scripts/*.py scripts/*.ps1 tools/*.py 2>/dev/null | head -20
```

**Ticket D3-T3: Selfsteal and mcp chapter bytes (locate and pin the lines the socratic batch cites).**

```
find . -path "*selfsteal*" -o -path "*self_steal*" -o -path "*self-steal*" 2>/dev/null | head -10
find . -path "*mcp*" -name "*.md" 2>/dev/null | grep -v node_modules | grep -v __pycache__ | head -10
```

---

## Falsifier for this deliverable

This adjudication is wrong if:

- (1) A caller of workflow_gate.py maps exit 1 to "warn and continue" and logic.md's mapping 1 is documented as describing that caller, not the gate itself. Amended L1 then reduces to "mapping 2 only is wrong."
- (2) A citation scheme exists in the estate that legitimately uses placeholder ids with correct attribution. The T2 amendment then needs a carve-out.
- (3) The selfsteal or mcp chapter bytes, once located, contain an explicit falsification condition or tiebreaker that the socratic objections missed. The UNVERIFIED marks on those objections would then flip to REFUTED.
- (4) The skills chapter's tail (truncated in evidence) contains a failure-mode probe citation for any of the 5 PROMOTE verdicts. The "UNPROBED" amendment would then be overstated for that skill.
