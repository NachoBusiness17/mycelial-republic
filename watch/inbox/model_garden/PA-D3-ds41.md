# PA-D3-ds41 (deepseek-chat @ deepseek, turn 1, channel: content)

# ADJUDICATION, MOVEMENT 3

## Conditions of this read (apply to every verdict below)

- **Instrument.** Pasted bytes only. I ran no commands. Line pins are my hand count of the pasted blocks, 1-indexed, first line = line 1.
- **Moment.** This session, movement 3.
- **Context assumptions.** Pasted bytes equal on-disk bytes. Chapter files (`logic.md`, `accuracy.md`, `operations.md`) are NOT in evidence; every quote from them is reuse from movement-1 receipts and is therefore **UNVERIFIED**. `workflow_gate.py` and `REGISTRY.jsonl` are NOT in this movement's evidence; every pin into them is reuse from movement-2 receipts and is **UNVERIFIED**.
- **Governance.** No em-dashes used. Plain hyphens only.

---

## (1) T1: does amended L1 close, or does a residue remain?

**Verdict: amended L1 CLOSES. A named residue remains, but it is not load-bearing on the "neither mapping matches" claim.**

The cheap arm's T1 answers give exact sites:

> tools/workflow_gate.py returns 1 (soft, lines 216/298), 2 (block, 269/313), 0 (pass, 271).

Read against movement-2's hand-built table, the call-site picture is:

| Exit | Site (as claimed) | Registers a row? | Mapping 1 says | Mapping 2 says |
|---|---|---|---|---|
| 0 | 271 (`return 0` after pass) | yes | pass | pass |
| 1 | 216, 298 | no | "warns with reason" | undecidable |
| 2 | 269, 313 | yes (main) / no (`--no-register`, scenarios) | "blocks" | refutable |

Amended L1 claimed: **neither logic.md mapping matches the code.** Mapping 1 misplaces the warn (warn lives at 0 via soft rows, not 1). Mapping 2 swaps 1 and 2 (1 is undecidable-in-state, 2 is refutable-in-state).

The residue: the cheap arm confirms return 1 at **216 and 298**. Movement-2 hand-counted those as the read-error and empty-card-dir paths. If a future read shows those are "warn and continue" paths that also emit a soft row, mapping 1's misplacement narrows from "wrong code, wrong exit" to "wrong code only." **The falsifier is not yet triggered by T1 as answered. Amended L1 stands.**

Conditions of this verdict: instrument = T1 command output pasted in the cheap arm answer; moment = cheap arm's run; context = the command reads the same bytes as movement 2, and returns 216/298 are not warn-class sites. Named falsifier: a live `sed -n '210,222p'` and `sed -n '292,302p' tools/workflow_gate.py` showing a soft-row write at either site drops amended L1 to "mapping 2 only is wrong."

---

## (2) T2: the landable amendment to accuracy.md that UF-124 earns

UF-124 CONFIRMED at `watch/inbox/union_fullsend_20260917/DAY_PACK.md:2056`, per cheap-arm T2: placeholder id `openreview.net/forum?id=XYZ` plus the misattribution "Constitutional AI - OpenAI" (the paper is Anthropic's). Movement-1 objection 1 stands: the proposed citation-resolution gate would have caught this.

**Paste-able sentence for accuracy.md (one sentence, imperative voice, no hedge):**

> **Any answer that cites an external artifact must resolve to a fetched URL or a repo path with a byte-verifiable author and year; a citation whose URL matches `forum?id=XYZ` or whose author is inferred from topic is REJECTED at gate time, not filed.**

Falsifier for this amendment: a run of the amended gate over the UF-124 answer in `watch/inbox/burn_wave_20260926/B2_16_uf_sweep_20260926.md:12` that returns PASS. Any PASS falsifies the gate's coverage.

---

## (3) T3: the-gala wiring cure and its trade-off

Cheap-arm T3 confirms O1: `.zcode/workflows/the-gala.dwf.ts` is untracked; `.gitignore:198` covers `.zcode/`. The saved workflow driving the estate's waves lives on one disk.

**Minimal cure (recommended): move the canonical copy into the repo, track it, keep `.zcode/` ignored.**

Concrete: `git mv` is impossible (untracked); instead:

```
mkdir -p workflows/estate
cp .zcode/workflows/the-gala.dwf.ts workflows/estate/the-gala.dwf.ts
git add workflows/estate/the-gala.dwf.ts
```

Plus one standing law line in the operations chapter:

> **`workflows/estate/` is the tracked canonical home of every `.zcode/workflows/*.dwf.ts` that drives a saved wave; `.zcode/` remains a runtime staging area only and MUST NOT be the sole copy.**

Trade-off: the file moves out of `.zcode/`'s runtime convenience, so any tool that reads `.zcode/workflows/` directly (loader, courier, mcp) needs a copy-back step or a symlink at wave start. A symlink under `.zcode/` is gitignored and does not survive clone; a copy-back in the wave boot is one line but can drift if a seat edits one copy and not the other. The rejected alternative (force-track under `.zcode/` via `git add -f`) keeps the runtime path but bakes a gitignored runtime directory into the repo, which is against `.gitignore:198`'s intent and will surprise any seat reading the ignore list.

Named falsifier: after the cure, `git ls-files | grep the-gala.dwf.ts` returns the tracked path, and `git log --oneline -1 -- workflows/estate/the-gala.dwf.ts` shows the add commit. If the file is still absent from `git ls-files`, the cure did not land.

---

## (4) Adjudicating socratic batch 2, chapter by chapter (refute or out-do on quoted bytes)

### 4a. socratic-skills

Claim S1: "waves are the fuzzer, cards are the commits" does not make verdicts falsifiable because coverage is unmeasured.

**Refute, on bytes.** `skills.md` line 1: "the estate's 18 census skills" get "a live-loop verdict each (promote / demote / kill)". The verdict ladder is byte-quoted: "PROMOTE = give the skill work or teeth this week; DEMOTE = keep, strip investment...; KILL = delete or freeze the card." Every row carries an "evidence (byte-cited)" column. So the falsifier is not "wave survival alone": it is the byte cited in the evidence column (e.g. row 1: `mag/chord.py:66`, `mag/invariant.py:197-200`, `scripts/lattice_render.py:26`, `scripts/build_fleet_imprint.py:264`). S1's premise ("counts wave survival as evidence") is not the chapter's method.

But S1 lands a partial hit the chapter should absorb: for row 3 (agent-harness), row 4 (mesh-comms), row 5 (zai-reference), the evidence column cites liveness (daily use, gate G2 codification) rather than a probe of a failure mode. S1's asymmetry claim is true for those three rows, not for the promote column as a whole. The correct amendment is narrower than S1.

**S2 (weakest verdict: the 5 promotes).** Partially out-done: row 1 operator-corrections has a stronger byte trail (five call sites) than the other four; collapsing all five promotes into one weakest-verdict claim is over-broad. The honest weakest is row 5: "name it in the dispatch-seat boot line" is a proposed action, not evidence the skill's content shapes a wave.

**S3 (fuzzer false-negative rate).** S1's strongest hit. `skills.md` has no section measuring whether the wave *could have* detected a failure the verdict classified as pass. This is a real gap the chapter should name as its own falsifier.

### 4b. socratic-communication

Claim S1: "content" is not a stable relay unit because severity owns retention.

**Refute: the chapter already treats content as tagged, not neutral.** `communication.md` section 1 breakage 2 states: "severity anti-correlated with retention probability." That is exactly the smuggling S1 charges. The chapter names it. S1's premise ("treats severity as given") is a strawman on this chapter.

Claim S2: only-deck-only-steps-die contradicts severity-owns-retention.

**Out-do, on bytes.** These are not two competing laws. Section 5's D3 (alert-channel rule) is a retention *surface* law; the deck-vs-kill outcome rule operates on the *doctrine* layer (what a wave's report declares dead), not on the memory surface. They are consistent once you name the layers. S1's contradiction is a category error the chapter did not pre-empt.

Claim S3: who assigns severity.

**Refute, then out-do.** `communication.md` section 3 gives the reader census: "Zero reader modules; the dead-channel claim stands on the current tree." So severity is assigned by a writer with no reader. S3 lands a real signal but points it at the wrong question. The right question is: if no module reads `attention_flag`, what forces a severity label to be actionable? The chapter does not answer. That is the gap to file.

### 4c. socratic-selfsteal

Claim S1: unreferenced "self" is constituted by the mechanisms, so re-steal is re-description.

**Refute: the chapter's rows pin referents at line granularity.** The evidence file names "8 line-pinned defects" against "9 prior-wave mechanisms." Line pins are a concrete referent, not a rhetorical one. S1's "nothing in the row pins that" is false for the rows cited.

Claim S2: 8 defects vs 9 steals reads as padding.

**Refute, on bytes.** The 8-defect list is offered as *how the seat read its own prior asks*, not as the steals. The steals are the 9 mechanisms. S1 conflates the two columns. The near 1:1 ratio is a coincidence of the sample, not a triangulation claim.

Claim S3: no falsifier for theft.

**Out-do: correct and under-used.** This is the chapter's real hole. Independent derivation of a mechanism (a fresh seat builds it without seeing the prior wave's version) is exactly the test that would separate theft from convergence, and the chapter names neither such a test nor its absence. This S3 sentence is worth pasting into the chapter as an open falsifier.

### 4d. socratic-mcp

Claim S1: schema-edit-repin makes the never-crosses table a snapshot, not a law.

**Refute: the table's rows are keyed by schema, and repin is a version bump.** A snapshot under a version key is still a law over that version; it is just a scoped law. S1 treats "scoped" as "not a law." That is a category error, and the chapter's R2.0/R2.5 rows (cited by S2) show version-independence as a *finding*, not a repeal.

Claim S2: four-clause metering reduces to one threshold under the R2.0/R2.5 reorder.

**Out-do: this is the strongest socratic objection in the batch.** If reordering clauses preserves admission, the metering is order-invariant, which is a real theorem the chapter has not stated. Either the reorder is a proof of invariance (chapter should cite it as such) or the clauses are not independent (chapter should say so). Silence is the defect.

Claim S3: no tiebreaker named.

**Out-do: correct and actionable.** Section 1 has "which mechanism runs last" nothing. The chapter owes a tiebreaker rule. This is the mcp chapter's missing line.

---

## (5) ONE landable amendment per chapter

**skills.md:**
> **Every PROMOTE verdict must cite one probe of the skill's declared failure mode; where no such probe exists in this wave, the verdict is "PROMOTE-UNTESTED" and the next wave must construct the probe before the skill can carry the verdict forward.**

**communication.md:**
> **A severity label written to memory/attention.md MUST be accompanied by a named reader module in the same wave; a label with no reader is not a retention rule and MUST NOT be cited as one in a fold.**

**selfsteal.md (or selfsteal chapter):**
> **Every re-steal claim MUST name a control: for each mechanism, a seat that built an equivalent without reading the prior wave's version, or the claim is documented as RE-DESCRIPTION, not THEFT, and is not counted in the steal tally.**

**mcp.md:**
> **The never-crosses table is versioned: each row carries the schema-edit-repin SHA it holds under; a row with no current schema-edit-repin SHA is UNENFORCED and its admission is decided by the named tiebreaker in the fold ledger, which is the mechanism whose order clause is lowest in the current run.**

---

## (6) Next 3 dig tickets

**D-1 (settles T1 residue).** Whether returns 1 at lines 216 and 298 are soft-row writes or hard no-row writes.

```
sed -n '210,222p' tools/workflow_gate.py
sed -n '292,302p' tools/workflow_gate.py
sed -n '260,275p' tools/workflow_gate.py
```

**D-2 (settles T3 cure).** Whether the canonical move is clean and what reads `.zcode/workflows/` at wave start.

```
grep -rn --hidden --no-ignore -E "\.zcode/workflows|zcode/workflows" . \
  --include="*.py" --include="*.ts" --include="*.ps1" --include="*.md" \
  | grep -v node_modules | head -50
ls -la .zcode/workflows/ 2>/dev/null
```

**D-3 (settles socratic-mcp S2, the strongest objection).** Whether clause reorder under R2.0/R2.5 preserves admission.

```
git log --oneline -20 -- mcp/ configs/mcp* 2>/dev/null
rg -n --hidden --no-ignore "R2\.0|R2\.5|reorder|repin" mcp/ configs/ docs/ 2>/dev/null | head -80
rg -n --hidden --no-ignore "schema-edit-repin" . | head -40
```

---

## Falsifier for this deliverable

This adjudication is wrong at each point if:

- **(1)** `sed -n '214,218p' tools/workflow_gate.py` shows a `soft=True` row write adjacent to the return-1 at 216, and `sed -n '296,300p'` shows the same at 298. Amended L1 then drops to "mapping 2 only is wrong."
- **(2)** The amended accuracy.md sentence, run against the UF-124 answer bytes, returns PASS. The gate would then not catch the case it earned on.
- **(3)** A tracked path under `.zcode/` in this repo appears in `git ls-files` without an explicit `-f` add. The "move-to-`workflows/estate/`" recommendation loses its premise that `.zcode/` is uniformly ignored.
- **(4)** Quoted bytes in the socratic rollbacks do not appear in the four chapter files at the cited locations. Any pin I marked by reuse-from-movement-1 is UNVERIFIED and returns to UNVERIFIED at every read until I re-open the chapter.
- **(5)** Any proposed amendment duplicates a law already present in its chapter. Ambiguity between an existing law and a new one falsifies the "landable" claim.
