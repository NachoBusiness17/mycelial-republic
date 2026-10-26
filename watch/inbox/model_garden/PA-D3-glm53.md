# PA-D3-glm53 (glm-5.3-flash @ zai, turn 1, channel: content)

# Movement 3: Adjudication

## Conditions of this read

- **Instrument.** Four pasted evidence blocks: `00__MOVEMENT2_CHEAP_ANSWERS.md`, `01__D2_movement2_adjudication.md`, `02__socratic2_results.jsonl`, and two full chapter heads (`03__skills.md`, `04__communication.md`) each truncated to head 6300 + tail 2100 of larger files. I ran no commands.
- **Moment.** Single pass, movement 3, 2026-10-01 class session.
- **Context assumptions.**
  - Truncation: any line of `03__skills.md` / `04__communication.md` outside the shown head/tail windows, and ALL bytes of the selfsteal and mcp chapters, are UNVERIFIED this session.
  - `logic.md`, `accuracy.md`, `operations.md`, `DAY_PACK.md`, `B2_16_uf_sweep_20260926.md`, `.gitignore` are not in evidence; every quote of them is reused from the cheap arm's receipt (00) or D2's movement-2 receipt (01), pinned to those receipts, not to fresh bytes.
  - The socratic outputs (02) are treated as objections to adjudicate, not as evidence.

---

## (1) T1: the amended L1 does NOT close. Residue named.

The exit-site half of L1 is settled. The cheap arm's M3 answer (00, section 1) confirms `return 1` at 216/298, `return 2` at 269/313, `return 0` at 271, and D2's movement-2 table (01, section 1) already showed the logic.md mappings are wrong, both of them. That half closes.

But the cheap arm calls the chapter "byte-true" (00, M3 item 1) on the strength of the call sites alone, and D2's C1 defect was never answered: the docstring itself, `tools/workflow_gate.py:10-11`, "exit 2 is the only hard block; every submission registers a row", is false of its own file. Three paths register no row: the exit-1 read-error path (`print(f"GATE ERROR: cannot read script: {exc}") / return 1`, 01 section 1 table), `--no-register`, and `--scenarios` (both `return 2 if failed else 0` / `return 0` with "no registry row written", same table). The docstring's "every" is contradicted by its own flag, whose help text dates the change to 2026-09-29 (01, C1). C2 also stands: "exit 1 never blocks a push" (00, M2 item 1) has no basis in the file; the token "push" appears nowhere in `workflow_gate.py` (01, C2).

**Verdict: L1 closes as "both logic.md mappings are wrong"; residue remains on the docstring.** Landable one-line patch (paste-able, applies at `tools/workflow_gate.py:10-11`):

```
-    pattern (exit 2 is the only hard block; every submission registers a row
+    pattern (exit 2 is the only hard block; every gate run registers a row
     unless --no-register, --scenarios, or an unreadable script exits early,
```

Falsifier of this residue: a `git log -p tools/workflow_gate.py` showing the docstring was amended when `--no-register` landed and my read of line 10-11 is stale.

## (2) T2: UF-124 CONFIRMED. Amendment to accuracy.md, one sentence.

The premise files exist (00, M3 item 2): `DAY_PACK.md` at `watch/inbox/union_fullsend_20260917/`, `B2_16_uf_sweep_20260926.md` at `watch/inbox/burn_wave_20260926/`. The bytes: UF-124's answer carried a literal placeholder id `"openreview.net/forum?id=XYZ"` AND misattributed Anthropic's Constitutional AI to OpenAI. Objection 1 stands as a non-hypothetical founding instance.

Paste-able amendment to accuracy.md:

> Every external citation in an accuracy verdict must resolve to quoted bytes with id, authors, and venue independently verified before the verdict lands; placeholder or misattributed citations void the verdict (founding instance: UF-124, DAY_PACK.md:2056 in watch/inbox/union_fullsend_20260917/, citing "openreview.net/forum?id=XYZ" and attributing Anthropic's Constitutional AI to OpenAI).

Falsifier: any later accuracy verdict landing with an unverified citation while this sentence stands in accuracy.md.

## (3) T3: O1 CONFIRMED. Minimal cure and trade-off.

Cure: track the one file, keep the single canonical path.

```
printf '!.gitignore\n!/.zcode/\n!/.zcode/workflows/\n!/.zcode/workflows/the-gala.dwf.ts\n' >> .gitignore
git add -f .zcode/workflows/the-gala.dwf.ts
```

(The negation entries are required because `.gitignore:198` ignores `.zcode/` (00, M3 item 3); git will not re-include a file inside an ignored directory unless the parent chain is negated first. `git add -f` alone works this window but decays on fresh clones.)

Standing law line (append to AGENTS.md, seat-law section):

> The saved workflows driving estate waves are tracked files; `.zcode/workflows/*.dwf.ts` is force-added at creation (`git add -f`), because gitignore coverage of `.zcode/` must never make the wave lineage single-disk-only.

**Trade-off.** Tracking under `.zcode/` via exception keeps one canonical path the gate and receipts already resolve to, at the cost of a decaying special case: the ignore rule now has a carve-out that future contributors will trip on, and any new workflow file silently re-enters the untracked gap unless the law is followed. Moving the canonical copy into the repo avoids the carve-out but forks the path: every receipt, gate reference, and session that reads `.zcode/workflows/the-gala.dwf.ts` (including the amend-not-rewrite lineage the cheap arm named) now has two candidate locations that WILL drift. I pick the carve-out; a known exception is cheaper than a hidden fork.

Falsifier: `git ls-files .zcode/ | wc -l` returning 0 after a fresh clone proves the cure did not take.

## (4) Socratic batch 2: adjudication on quoted bytes

### socratic-skills: REFUTED on its central premise, CONFIRMED on one defect

**The objection attacks a premise the chapter does not hold.** It claims "promotion keyed to wave pass rate" (02, socratic-skills item 2). The chapter's verdict ladder keys PROMOTE to wiring evidence, not wave survival: skill 1 is promoted because `mag/chord.py:66` probes it, `mag/invariant.py:197-200` hashes it into `instruction_sha`, and `scripts/lattice_render.py:26` parses its laws (03, table row 1); skill 4 because "its pass-off protocol is codified as gate G2 (tools/workflow_gate.py:51-53)" (03, row 4). Every promote row in the visible table carries a byte cite or a named artifact, and rows 6-12 show DEMOTE/killing on exactly the absence-of-signal ground the objection demands (salon's Door B "fired exactly once ever", 03 row 6; frontier-hr "zero invocation of any kind ever", row 9). The promotes are not absence-of-negative-signal verdicts; they are wired-surface verdicts. The fuzzer-false-negative attack lands on a chapter that did not run the argument attributed to it.

**Confirmed defect, absorbed:** the chapter's own census-drift section already concedes the instrument gap the objection's item 3 names: the +141 bytes of "unattributed micro-drift... not investigated further, named honestly" (03, section 0). The objection's demand is already partially met; the amendment below closes the rest.

### socratic-communication: UNVERIFIED against visible bytes, but one clause is confirmable and the amendment lands regardless

The objection's weakest-law claim quotes "only-deck-only-steps-die" and "severity-owns-retention" (02, socratic-communication item 2). Neither law's row is in the visible head/tail of `04__communication.md` this session; the visible bytes carry D1-D4 (owe-report contract, relay contract, alert-channel rule, fold debt) and the three breakages (04, section 7 summary and section 1). **The alleged contradiction between two laws I cannot read is UNVERIFIED.** What I CAN confirm from visible bytes is the objection's item 3 direction: severity IS assigned downstream of a writer, not intrinsic. The breakage-2 bytes show retention was decided by write position (prepend ring, "the bottom is the eviction zone", 04, breakage 2) and the repair is "whole-block eviction with a preserved alert tail below a seeded sentinel, flood metered" (04, breakage 2 tail). Position, not severity, has been the actual retention key twice. The objection's demand (name who assigns severity and what happens on mislabel) is therefore not refuted, it is already half-answered by the chapter's own breakage-2 receipt, and the amendment below forces the other half.

### socratic-selfsteal: CONFIRMED as stated, and out-done

The chapter's bytes are UNVERIFIED this session (not in evidence), so I cannot refute on quoted bytes, and the objection's own text (02, socratic-selfsteal) needs none: its item 3 states the chapter "never states a condition under which a mechanism was independently derived rather than stolen". A theft verdict with no stated falsifier violates the estate's own descent law (a verdict without its conditions is not a verdict) regardless of what the chapter's rows say. I out-do rather than merely confirm: the falsifier the chapter lacks is constructible and is the amendment below. First-arrival hash receipts turn "guilty by default" into "adjudicable": a mechanism is stolen only if a prior wave's ledger row carries an equal content hash with an earlier ts; equal hash with no prior row, or differing hash, is independent derivation. That is a decision procedure, which is what the objection showed was missing.

### socratic-mcp: REFUTED on the reorder clause, CONFIRMED on the missing tiebreaker

**The reorder is not the objection's smoking gun; it is the metering law's strongest support.** The objection reads the R2.0/R2.5 reorder as "clause order is negotiable under load" (02, socratic-mcp item 2), concluding metering collapses to "one threshold wearing four hats". But if reordering the clauses under load preserves admission outcomes, that is commutativity: the four clauses are order-independent conjuncts, which is a STRONGER law than ordered clauses, not a weaker one. A single threshold wearing four hats would also survive reordering, so the evidence underdetermines the conclusion; the objection's own inference is the circular step it accuses MCP-2 of. (The chapter's R2.0/R2.5 row itself: UNVERIFIED, outside visible evidence; the refutation stands on the objection's own quoted characterization.)

**Confirmed defect:** item 3 names no tiebreaker when schema-edit-repin legitimizes what the never-crosses table forbids. From the objection's own quote of the chapter's mechanisms, "admission is decided by whichever mechanism runs last" (02, socratic-mcp item 3). A scheduling-order adjudicator is not doctrine. The amendment below names one.

## (5) ONE landable amendment per chapter

**skills.md:**

> Every PROMOTE verdict must carry a measurable falsifier with a date (a command and an expected outcome whose failure demotes the skill within 7 days), and any verdict resting on wave survival must state the fuzzer's false-negative rate for that skill's failure mode or be downgraded to CANDIDATE.

**communication.md:**

> Retention is owned by severity stamped by a named assigner at emit time (writer and ts in the row); no surface may retain by write position alone, and every mislabel drill must show a severity=LOW alert relaying anyway and a deck step surviving a LOW stamp, with the assigner's identity recorded per row.

**selfsteal.md (chapter file, currently UNVERIFIED bytes; amendment applies wherever the tri-state table lands):**

> A re-steal claim is adjudicable only against first-arrival content-hash receipts (equal hash plus earlier ts = stolen; equal hash with no prior row, or differing hash = independent derivation); any claim without a hash receipt is recorded as re-description, not theft.

**mcp.md:**

> Four-clause metering is restated as an order-independent conjunction (clause permutation must not change admission outcomes, tested by running both orders per schema edit), and the admission tiebreaker is fixed: a schema-edit-repin forces re-adjudication against the never-crosses table BEFORE any payload crosses, with the repin's exit code as the sole adjudicator; last-writer-wins is abolished.

Each amendment's falsifier: the next chapter verdict that omits its required field (falsifier+date, assigner+ts, hash receipt, repin exit code) is invalid on its face and demotes the chapter's pass count.

## (6) NEXT 3 DIG TICKETS (commands only)

**T4 - close the L1 docstring residue and pin logic.md's actual bytes:**

```
sed -n '1,20p' tools/workflow_gate.py
grep -n -E "no-register|scenarios|return [012]" tools/workflow_gate.py
find . -name "logic.md" -not -path "*/node_modules/*" 2>/dev/null
sed -n '80,95p' "$(find . -name logic.md | head -1)"
git log --oneline -3 -- tools/workflow_gate.py
```

**T5 - land the T3 cure and prove it survives a clone:**

```
git add -f .zcode/workflows/the-gala.dwf.ts
git ls-files .zcode/ ; echo "tracked_count=$(git ls-files .zcode/ | wc -l)"
git check-ignore -v .zcode/workflows/the-gala.dwf.ts; echo "ignore_exit=$?"
grep -n "the-gala" AGENTS.md memory/*.md 2>/dev/null | head -5
git status --short | head -5
```

**T6 - pull the disputed socratic-law rows into evidence (selfsteal tri-state table, mcp R2.0/R2.5 row, communication deck/severity law):**

```
find . -path "*ractor50*" -iname "*selfsteal*" -o -path "*ractor50*" -iname "*mcp*" -o -path "*ractor50*" -iname "*communication*" 2>/dev/null
rg -n --hidden --no-ignore "only-deck|severity-owns|tri-state|R2\.0|R2\.5|never-crosses" watch/inbox/gala_20260925/ 2>/dev/null | head -40
```

## Falsifier for this deliverable

- **(1)** If `sed -n '1,20p' tools/workflow_gate.py` shows the docstring already carries the no-register carve-out, my residue is stale and L1 closes in full.
- **(2)** If the UF-124 bytes at `DAY_PACK.md:2056` show a real id and correct attribution, the amendment's founding instance is fabricated and objection 1 dies.
- **(3)** If T5's fresh-clone `git ls-files .zcode/` returns empty after the cure lands, the carve-out failed and the minimal cure must move to the copy-into-repo branch.
- **(4)/(5)** If T6's `rg` output shows the selfsteal chapter already states a hash-receipt falsifier, my "CONFIRMED, out-done" verdict is wrong (the chapter met the bar and the objection missed it); likewise if the mcp chapter already names the repin exit code as tiebreaker.
- **(4, skills)** If the skills chapter's promote rows outside the visible head/tail are keyed to wave pass rate with no byte cites, my refutation fails and the socratic objection stands against the full text.
