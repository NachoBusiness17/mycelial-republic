# D2_movement2_adjudication (anthropic/claude-opus-5.5, turn 1, channel: content)

# Doctrine Roast, Movement 2: Adjudication

## Conditions of this read

These conditions apply to every verdict below.

- **Instrument.** I read three pasted evidence blocks: `MOVEMENT2_CHEAP_ANSWERS.md`, `D1_doctrine_roast_movement1.md`, and the full text of `tools/workflow_gate.py` and `memory/workflows/REGISTRY.jsonl`. I ran no commands.
- **Moment.** Single pass, movement 2, this session.
- **Context assumptions.**
  - The pasted bytes equal the on-disk bytes, with no reflow.
  - The registry block is the complete file at the cheap arm's read moment.
  - `logic.md`, `accuracy.md` and `operations.md` are NOT in evidence this session. Every quote from them is reused from my movement-1 receipt, not re-read. Every pin into them is therefore UNVERIFIED.
- **Line pins.**
  - `tools/workflow_gate.py:10-11` is my hand count of the pasted block, with line 1 being `#!/usr/bin/env python3`.
  - I did not hand-count other `workflow_gate.py` sites. A 300-line hand count is the "hand-copied count" class. Those sites are pinned by function name plus quoted bytes, with line UNVERIFIED until ticket T1 runs.
- **Registry row numbers.** These are my hand count of the pasted block, 1-indexed. My count agrees with the cheap arm's 45, so two counts by different instruments match.

---

## (1) EXIT SEMANTICS: L1 SURVIVES, AMENDED

### What the cheap arm got right

The docstring span is real, and it wraps across two lines:

> tools/workflow_gate.py:10-11: "pattern (exit 2 is the only hard block; every submission registers a row so / improvement is a ledger fact, amend-not-rewrite is visible in digests)."

This confirms the logic.md:85-87 claim that the 10-11 miss was a line-wrap artifact. That part of movement-1 ticket 1 is settled.

### Why "zero sys.exit(1) sites" does not settle L1

The instrument is blind to how this file exits. The file has exactly one `sys.exit` call:

> `if __name__ == "__main__":` / `sys.exit(main())`

Every exit code reaches the shell as a `return` value propagated through `main()`. A grep for `sys.exit(1)` therefore returns zero whether or not exit 1 exists.

This is the exact blind spot that law 4's own falsifier names: a text-caller count missing a load-bearing path. The cheap arm's answer is an instance of the class the doctrine warns about.

### Exit sites found in the quoted bytes

All lines below are UNVERIFIED pending T1.

| Exit | Site | Quoted bytes | Registers a row? |
|---|---|---|---|
| 0 | `main()` tail | `return 0` | yes |
| 0 | `main()`, `--no-register` | `return 2 if failed else 0` | no |
| 0 | `run_scenarios()` | `return 0` | no ("no registry row written") |
| **1** | `main()` | `print(f"GATE ERROR: cannot read script: {exc}")` / `return 1` | **no** (returns before the row block) |
| **1** | `run_scenarios()` | `print(f"SCENARIOS ERROR: no *.card.json cards under {scen_dir}")` / `return 1` | no |
| 2 | `main()` | `print("GATE: fix the FAIL items ...")` / `return 2` | yes |
| 2 | `main()`, `--no-register` | `return 2 if failed else 0` | no |
| 2 | `run_scenarios()` | `... cards red (read-only run, no registry row)` / `return 2` | no |
| 2 (UNVERIFIED) | `main()` | `ap.error("check requires --script PATH or --scenarios DIR")` | no |

The last row rests on Python stdlib behavior, not on corpus bytes: `argparse.error` exits with status 2. T1 captures this with a real run.

### Where soft warnings land

Soft warnings never reach exit 1. In `split_rows()`, soft rows are excluded from the failed set:

> `failed = [r["id"] for r in rows if not r["ok"] and not r.get("soft")]`

The G6 comment states the intent:

> "never a new hard-block exit (0/1/2 contract unchanged)"

A G3 or G6 soft finding prints `WARN` with a reason and exits **0**.

### The mapping the code implements

| Code | Code meaning | logic.md mapping 1 ("exit 1 warns with reason") | logic.md mapping 2 (pass / refutable / undecidable, in order) |
|---|---|---|---|
| 0 | pass, including soft WARN rows | wrong: warns live here, not at 1 | match |
| 1 | gate could not evaluate (unreadable script, empty card dir); no row | wrong: not a warn | wrong: this is undecidable, not refutable |
| 2 | refutable violation (non-soft check failed, or a red card) | "blocks": match | wrong: this is refutable, not undecidable |

### Verdict on L1

L1 survives, amended.

- **Original L1:** logic.md states two mappings that are incompatible with each other.
- **Amended L1:** logic.md states two mappings, and **neither matches the code.**
  - Mapping 1 misplaces the warn.
  - Mapping 2 swaps 1 and 2.
- **My movement-1 falsifier did not fire.** It required the file to document exit 1 as "warn" and exit 2 as "undecidable". The bytes show neither.

### Defects in the cheap arm's answer

- **C1. The docstring is not byte-true of the code.** The cheap arm called it "byte-true". Line 10 says "every submission registers a row". Three paths in the table above register none: the exit-1 read error, `--no-register`, and `--scenarios`. The docstring is stale relative to its own `--no-register` flag, whose help text dates the change to "2026-09-29".
- **C2. "Exit 1 never blocks a push" has no basis in this file.** The token "push" appears nowhere in `workflow_gate.py`. The docstring says "The gate runs BEFORE CreateWorkflow submission" (tools/workflow_gate.py:9, hand count). Whether any caller blocks on exit 1 is unanswerable from this file.
  - I own part of this. My movement-1 ticket asked "Does exit 1 ever block a push?", which aimed the question at the wrong surface. T1 re-aims it at the callers.

---

## (2) REGISTRY ORDER: ARITHMETIC HOLDS; A4 AND O7 SURVIVE AS MOMENT-STAMP DEFECTS

### What the registry bytes show

- **Row count.** 45 rows. Row 40 is `"ts": "2026-09-30T01:18:10Z", "name": "frontier-olm-mine.dwf.ts"`. Rows 41-45 run from `2026-10-01T01:13:49Z` to `2026-10-01T01:16:55Z`.
- **Ordering.** `ts` is non-decreasing across all 45 rows. This is consistent with append-only, but it is not proof of append-only. Monotone timestamps do not exclude a rewrite.
- **Verdict split.** I hand-counted 11 FAIL rows: rows 1, 3, 5, 10, 12, 16, 18, 20, 26, 36 and 39. That gives PASS 34 / FAIL 11, which reproduces accuracy.md's "PASS 34 / FAIL 11" exactly.
- **Rows 41-45 are all PASS.** So FAIL = 11 at every moment from row 40 to row 45. Only PASS moves, from 29 to 34.

### As census-law arithmetic

The reconciliation holds. An order exists in which both counts are true:

1. "40 rows" is true in the window [2026-09-30T01:18:10Z, 2026-10-01T01:13:49Z).
2. "45 rows" is true from 2026-10-01T01:16:55Z onward.

No contradiction. My movement-1 statement that "45 followed by 40 is impossible" still stands, and the bytes show that order did not occur.

### As census law, it does not "HOLD, no census violation"

**The reconciliation is CONSISTENT, not PROVEN.** Neither chapter stamps its census moment. The cheap arm inferred the moments from the counts, which is the reverse of the moment law. A4 and O7 both survive, downgraded from "possible contradiction" to "unstamped census".

**O7 sharpens.** Movement 1 quoted operations.md as minting its own row at "ts 2026-10-01T01:16:55Z". That is row 45.

- For "holds 40 rows" to be true, operations.md's census had to be taken before row 41 (01:13:49Z).
- So one chapter carries two moments, at least 3 minutes apart, without labels.
- It reports a pre-edit census beside a post-edit mint.

**C3. Attribution not in bytes.** The cheap arm says rows 41-45 are "the ractor50 lanes' own submissions + the-gala". All five rows have `"name": "the-gala.dwf.ts"`. No row names a ractor50 lane, so this attribution is UNVERIFIED.

The bytes do fit the operations lane's own the-gala edits:

- Rows 44 and 45 share digest `2285b0104993`.
- Rows 41-44 use an absolute script path and row 45 a relative one.
- That fit is my inference, also UNVERIFIED.

---

## (3) UF-124: OPEN, NOT CONFIRMED

### What stands without the instance

The design form of A1 stands on accuracy.md's own wording, as quoted in movement 1: "each id must resolve to fetched bytes". That is an existence test by construction.

The **in-chapter instance** is what is OPEN. That instance is my claim that UF-124 is a misattributed citation the resolver would pass.

### Evidence that would close it

All of these are mechanical:

| Step | Closing evidence |
|---|---|
| E1 | The path of `DAY_PACK.md` and of `B2_16_uf_sweep_20260926.md`, from an estate-wide search covering tracked and untracked files. |
| E2 | Quoted bytes at `DAY_PACK.md:2056` and `B2_16_uf_sweep_20260926.md:12`. |
| E3 | The exact id string the UF-124 answer cites for the "misattributed" paper. |
| E4 | Fetched bytes for that id, with author list and effect-size span captured in the same session. |

### Outcomes

| Result | Effect on objection 1 |
|---|---|
| **CONFIRMED** | E4 resolves, and its author or effect-size span contradicts the UF-124 claim. The id-only resolver would have passed a misattribution. |
| **DIES** | E3's id does not resolve. The id-only resolver would have caught it. |
| **MUTATES** | E1 finds neither file anywhere. accuracy.md §Incident 1 then quotes files the corpus cannot produce. Its "byte-verifies 34 quote spans against their named source files" self-check either ran on bytes outside the corpus or is false. That is a new defect, A8: an UNVERIFIED citation inside the accuracy doctrine itself. |

### Scope gap in the cheap arm's sweep

The sweep covered only "corpus/steal + the burn receipts". That scope cannot distinguish "absent" from "elsewhere". T2 widens it.

---

## (4) LANDABLE AMENDMENT: logic.md, Law 1

### Why this one is due now

The movement-1 logic amendment parked law 1 as UNVERIFIED "until a quote from tools/workflow_gate.py byte-verifies". The code is now in evidence, so the parking sentence can be replaced by the verified mapping.

### Placement

Replace the law 1 exit-mapping sentences:

- "exit 0 banks, exit 1 warns with reason, exit 2 blocks with its own evidence file" (logic.md:16-17)
- "pass, refutable violation, undecidable" (logic.md:29-30)

Both pins are UNVERIFIED hand counts from movement 1. T1 re-pins them.

### Paste-able sentence

> Law 1's trivalent exit contract, as tools/workflow_gate.py implements it: exit 0 is pass, including soft-warn rows (G3 judge-model, G6 dated stamp) that print WARN with a reason but never change the exit; exit 1 is undecidable, the gate could not evaluate (unreadable --script, or no *.card.json under --scenarios), and registers no row; exit 2 is refutable violation (a non-soft check failed, or a scenario card is red) and is the only hard block (tools/workflow_gate.py:10), with its evidence in the appended memory/workflows/REGISTRY.jsonl row, not its own file, and no row at all under --no-register or --scenarios; how any caller treats exit 1 is UNVERIFIED until its caller is quoted.

### How the sentence sorts cases

| Case | Run | Result under the amendment |
|---|---|---|
| Positive | `check --script configs/workflow_gate_scenarios/fixtures/fail_g1.dwf.ts` | Exit 2, one new row with `"G1-multiplicity", "ok": false`. Consistent with registry row 18 (`scenario-g1-fixture`, FAIL). |
| Positive | A script whose only defect is a missing `fetched: YYYY-MM-DD` stamp | Exit 0 with a `WARN G6-receipts` line, verdict PASS. Matches registry row 27's shape. |
| Negative | A reader applying the old mapping 1 to that same G6 case | Predicts exit 1. The code returns 0. |
| Negative | A reader applying the old mapping 2 to the fail_g1 fixture | Predicts "undecidable". The code returns 2, a refutable FAIL with named failing checks. |

### Falsifier for the amendment

Run three commands, recording `wc -l memory/workflows/REGISTRY.jsonl` before and after each:

1. `check --script <nonexistent path>` must give exit 1 and add 0 rows.
2. `check --script <the fail_g1 fixture>` must give exit 2 and add 1 row.
3. `check --script <G6-stamp-only fixture> --no-register` must give exit 0 and add 0 rows.

Any mismatch kills the sentence.

---

## (5) NEXT 3 DIG TICKETS

Each ticket is commands only. Each answer is bytes or exit codes.

### T1. Exit sites, callers, and the logic.md re-pin

Settles: amended L1, C2, the amendment's falsifier, and the stdlib row in the exit table.

```
grep -n -E "return [012]\b|sys\.exit|ap\.error|registers a row" tools/workflow_gate.py
rg -n "workflow_gate" --hidden -g '!memory/workflows/REGISTRY.jsonl' .
python tools/workflow_gate.py check; echo "exit=$?"
wc -l memory/workflows/REGISTRY.jsonl; python tools/workflow_gate.py check --script /nonexistent.dwf.ts; echo "exit=$?"; wc -l memory/workflows/REGISTRY.jsonl
rg -n "exit 1 warns|refutable violation, undecidable|undecidable middle" -g 'logic.md' .
```

Questions, answered from the output:

- What are the line numbers of every exit site?
- Which files invoke the gate?
- For each caller, what does it do on exit 1? Quote the branch.
- Does the usage error exit 2?
- Does the read error exit 1 and add 0 rows?
- At what lines does logic.md state law 1's mappings?

### T2. Locate the UF-124 premise files

Settles: objection 1, giving CONFIRMED, DIES or MUTATES.

```
git ls-files | grep -i -E "day_pack|b2_16_uf_sweep"
find . -iname "DAY_PACK*.md" -o -iname "B2_16_uf_sweep*" 2>/dev/null
rg -n --hidden --no-ignore "UF-124|misattribut" .
sed -n '2050,2062p' <path-to-DAY_PACK.md>
sed -n '8,16p' <path-to-B2_16_uf_sweep_20260926.md>
```

Questions, answered from the output:

- Do the files exist, tracked or untracked?
- What bytes sit at the cited lines?
- What id does UF-124 cite?

The id fetch for E4 follows as a separate receipt.

### T3. Is the-gala wiring tracked?

Settles: operations objection 1 (O1). This is my movement-1 falsifier, never ticketed.

```
git ls-files --error-unmatch .zcode/workflows/the-gala.dwf.ts; echo "tracked_exit=$?"
git check-ignore -v .zcode/workflows/the-gala.dwf.ts
sed -n '198p' .gitignore
git grep -n "rateLimitHold"
git log --oneline -3 -- memory/workflows/REGISTRY.jsonl
```

Questions, answered from the output:

- Is the file tracked, and which ignore rule matches it?
- Does any tracked path carry the `rateLimitHold` bytes?
- Is the registry under git? That decides whether "append-only" in section (2) can ever move from CONSISTENT to PROVEN.

---

## Falsifier for this deliverable

This adjudication is wrong at each point if:

- **(1)** T1 shows a caller of `workflow_gate.py` mapping exit 1 to "warn with reason" and treating it as non-blocking, and logic.md's law 1 is documented as describing that caller rather than the gate. Amended L1 would then drop to "mapping 2 only is wrong".
- **(1)** T1's grep finds a `return 1` I did not list, or my quoted `return 1` sites are absent on disk.
- **(2)** My hand count of FAIL rows is not 11, or row 41's `ts` is not `2026-10-01T01:13:49Z`. A `jq -r .verdict memory/workflows/REGISTRY.jsonl | sort | uniq -c` disagreeing with 34/11 falsifies it.
- **(3)** T2 finds the files, and the UF-124 id resolves with authors and effect size matching the claim. There would then be no misattribution, and objection 1's instance dies outright, not merely stays open.
- **(4)** The three-run falsifier in section (4) returns any exit or row delta other than 1/0, 2/1, 0/0.
