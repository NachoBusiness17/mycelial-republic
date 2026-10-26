# LANE 10 — ADVERSARIAL RED TEAM (2026-09-26)

**Seat:** L10 adversarial. **Mode:** read-only. No repair, no rebuild, no GC, no baseline write.
**Target:** the audit-in-progress, the prior map, and the fleet's self-image.
**Branch:** `mag/run-beta1-factory-build-audi-20260806T231709Z` @ `6d417abd5`

**Verdict up front: the prior map is UNRELIABLE as a foundation.** Three of its
load-bearing claims are refuted by bytes, one of them by a factor of 115. The
audit must not inherit this map — it must re-derive from bytes and file the
re-derivations.

---

## PART 1 — THE MEASUREMENT IS THE AUDIT (hidden bad numbers)

The repo's law is `seed/TRUST_BYTES_LAW.md`: "never trust a hand-written count."
The census already found one bad number (1,910 vs 2,288). I found the other
instruments' bad numbers. All of them are **hand-copied between receipts whose
denominators moved underneath them.**

### M1. `chain_completion_stats.json` — a coverage note printed unconditionally

`memory/audit/chain_completion_stats.json` (run 2026-09-06T01:52:46Z) says:

```
"total_knots_found": 20951, "already_indexed_count": 20950,
"newly_indexed_count": 1, "parse_error_count": 0,
"coverage_note": "sidecar + main chain now cover every parseable knot"
```

`coverage_note` is a **hardcoded string literal** in
`scripts/chain_index_completion.py:172-173` — it is written on every run
regardless of what the run found. It is not a measurement. It is a slogan in a
JSON file, and readers (including prior audits) have been citing it as a
coverage result. Bytes today:

| quantity | value |
|---|---:|
| `.knot.json` on disk | **23,666** |
| sidecar rows | 13,678 |
| chain rows naming an on-disk knot | 6,431 |
| **on-disk knots indexed by NEITHER** | **3,557** |
| chain rows naming a file NOT on disk | **1,380** |

The stats file's own `total_knots_found: 20951` is already stale against
23,666 on disk — the tree grew ~2,700 knots since 09-06 and nothing re-ran.

### M2. The doctrine number 13,687 is not any instrument's number

The law text says "13,687 orphans reconciled by completion index." Grepping the
estate for `13,687` returns exactly two prose sites
(`audit_bundle/audit_bundle_manifest.md:56`,
`audit_bundle/verkle_chain_schema.md:108`) plus
`CELL_expansion_seams_VERIFY.md:22`. **No instrument ever produced 13,687.**
The sidecar holds 13,678 rows. 13,687 is a hand-typed number in a markdown
manifest, nine off from the only real count, and it has been copied forward into
at least three downstream documents. This is the 1,341 fossil in a new costume:
a hand-written count wearing a receipt's clothes.

### M3. The census carrier and its own scheduled detector disagree by 384

The scheduled deep check at 11:33 today **exited 1** (`COLLECT-DRIFT`, delta +31)
and appended an ALERT to `memory/attention.md`. At 11:34, one minute later, the
same script **exited 0** — "pytest 1910 vs carrier 1910, delta +0" — because
`AGENTS.md:27` had been rewritten to 1,910 in between. It is 1,910 now, and the
live deep check I just ran reads:

```
CENSUS-PATROL: COLLECT-DRIFT - pytest holds 2294 vs carrier claim 1910 (delta +384, bar 20)
REAL_EXIT=1
```

The gate is not lying. **The carrier is.** But the more damning structural fact:
the default (no-`--collect`) invocation that the pre-push hook actually runs
prints `CENSUS-PATROL: ok - census 0d old of 7d bar, disk 349 vs carrier 303`
and **exits 0**. The hook's own comment admits the deep check "is kept out of the
default pre-push path because it needs the venv" — and the venv is
`.venv/Scripts/python.exe`, the same interpreter the hook already uses on line 10
for the ratchet. The stated reason for the exclusion does not hold. The gate that
runs on every push is structurally blind to the exact number it exists to police.

### M4. The ratchet's "6 NEW violations" is scope-dependent, and the scope is a non-recursive glob

`tools/violation_ratchet.py:91` uses `base.glob("*.py")` — **top level only, not
`**/*.py`**. Bytes:

- ratchet scope: 1,188 files (it printed this itself)
- git-tracked `.py` in `mag/` or `tools/` at ANY depth: 1,157, of which **145 are nested** and therefore invisible
- git-tracked `.py` repo-wide: **3,043**

**The ratchet sees 39.0% of the repo's tracked Python.** 145 tracked files under
`mag/` and `tools/` have never been scanned by the estate's flagship debt gate.
The `file-too-long` rule (a 400-line cap) cannot fire on any of them. So "the
ratchet is green" and "the estate has no unregistered debt" are **incomparable
claims** presented as the same claim. The 6-vs-7 difference between the gopher
report and my run is not drift — it is `check --changed` (101 files) versus
`check` (1,188 files). Two different denominators, same headline word.

### M5. `disk 349 vs carrier 303` is not "instrument lag" — the tool's own deep check contradicts its excuse

`census_drift_patrol` classifies the 46-file gap as "instrument lag: disk counts
pytest-named candidates... same-window lag, evidence only." But its own
`--collect` leg then reports `files: collected 349 vs carrier claim 303` and
`instrument gap: none, every disk candidate collects items`. If every one of the
349 candidates collects items, then 349 files collect items and the carrier's
303 is **wrong**, not lagging. The tool explains away a discrepancy using an
excuse its own second instrument falsifies on the same run. That is a meter
grading its own homework.

---

## PART 2 — THE PRIOR-MAP TRAP: TWO CLAIMS REFUTED WITH BYTES

### ⛔ REFUTATION 1 — "12 missing knots" is off by 115×. The real number is 1,380.

**Prior claim** (`watch/astra_hold0/TASK_PACK_SKELETON_20260911.md:354`, dated
2026-09-11, presented as "two measurements, one answer" — the strongest-form
evidence in the prior map):

```
(7,377 chain refs / 7,365 present / 12 missing) independently confirms the
atlas F8 sample (3,035 / 3,023 / 12): two measurements, one answer.
```

**Bytes today** (reading `verkle_chain.jsonl` `filename` fields against
`os.listdir` of `memory/biography/knots`, then `git ls-files` on the misses):

```
chain rows                                    7,811
distinct knot filenames named                 7,811
present on disk                               6,431
MISSING on disk                               1,380     <-- was documented as 12
missing by month: 2026-08 = 1,199   2026-09 = 181
git log --diff-filter=D -- memory/biography/knots : no deletions
```

1,380 missing is **115× the documented figure**, and the 181 September misses
post-date the 09-11 receipt entirely — so this is not a stale number, it is an
**actively worsening** one. `git log` shows no committed deletion, so these
knots are not "lost in a known wipe with a known actor": they are uncommitted
bytes that vanished, or were never written, and the chain's append-only claim
names them as if they exist. The "documented recurring wipe / blessed seals"
story was accurate for 12 files on 09-11 and has silently failed to keep up.
**The prior map's headline chain-health claim is REFUTED.**

### ⛔ REFUTATION 2 — "Hook wiring is correct" is half-true and the half that is true is the load-bearing half.

`watch/inbox/AUDIT_GOPHER_20260926.md:130` asserts under "What is healthy":

> **Hook wiring is correct.** `core.hooksPath` = `githooks`, `githooks/pre-push`
> present and executable (17,853 bytes). No stray `.git/hooks/pre-push`.

All three sub-claims verify — I confirmed `core.hooksPath=githooks`, the file at
17,853 bytes, mode 755, and 0 CRLF (so it will execute under `sh`). **But the
sentence is about the wrong property.** The hook exists; the audit never asked
what it *enforces*. Reading the hook's own bytes: of its ~8 push-gate blocks,
only **three** can return nonzero. `ratchet check --changed || exit 1`,
`config_seal verify || exit 1`, and `census exit 2`. The other five —
`description_pin`, `freshness_gate`, `caption_ledger_verify`, `refold_gate`, and
**census STALE (exit 1)** — are each explicitly marked `WARN-ONLY ... this block
NEVER exits nonzero`, with `TODO-FLIP-TO-ENFORCE` comments. So:

- the census **drift** finding (M3) fires the WARN arm and does not block
- the config-seal **drift** the daily log recorded yesterday (`seal=1` on
  2026-09-26) would only block on the *push* path, and the daily task's own exit
  was `1` while the estate kept committing

"Hook wiring is correct" and "the hook enforces the estate's laws" are
**incomparable claims**. The prior map reported the first and let it stand in for
the second. Refuted as a health claim.

### ✅ VERIFIED — claims that survive

I tried to break these and could not:

- **F2 duplicate ledgers** — exact. Both files sha256
  `7f3b2bc447d0cc43bb06b8e616063bf1dc6542ba7f8944c98097cd68873d0d1b`, both
  590,246,188 bytes, both `git ls-files`-tracked. Not a symlink. 1.18 GB.
- **F4 ratchet catches its 6** — my independent `check --changed`-equivalent full
  run reproduced 6 of the 6 by fingerprint (`5ae40a2d`, `3b1726de`, `f0d81bd3`,
  `e3b7845e`, `0dfc0411`, `f2ce896c`). The ratchet's *detection* is sound. Only
  its *scope* is broken (M4).
- **"13,687 orphans reconciled by completion index"** — the sidecar is not a
  lie in the narrow sense: all 13,678 sidecar rows resolve to on-disk files, and
  all 13,678 `leaf_hash` values **match the knot bytes** (0 mismatches across
  13,678 reads). The index is real. The word "reconciled" is doing work the
  bytes don't do — the sidecar rows carry **no `verkle_root` and no
  `parent_verkle_root`** (field set is exactly `knot_file, session_id, ts,
  dominant_theme, leaf_hash, indexed_by, indexed_ts`). They are a flat list, not
  a chain. A row with no parent link cannot be part of any hash chain, so
  "reconciled by completion index" describes a **lookup table**, not a
  reconciliation. The script's own docstring is honest about this ("INDEX-ONLY
  row", "sidecar is merge-later") — the prose that grew on top of it was not.

---

## PART 3 — THE GATE THAT CANNOT FAIL

**The strongest single finding of this lane.**

`tools/violation_ratchet.py:280-301`, `cmd_baseline_update`:

```python
def cmd_baseline_update(by: str, note: str) -> int:
    viols = all_violations()
    ...
    for v in viols:
        fp = fingerprint(...)
        if fp not in accepted:
            accepted[fp] = {...}   # accepts EVERYTHING it finds
            added += 1
    save_baseline(baseline)
    return 0                        # <-- ALWAYS ZERO
```

The machine **can widen its own gate in one command**, and that command's only
input is the debt it just found. The docstring's law is "The register can only
grow by a human/agent running baseline-update, never silently" — but
`baseline-update` is not gated by anything: no `--by` requirement (it defaults to
`by = "operator"`, line 340, **forging operator consent** for any claim written
without an explicit flag), no diff preview, no limit, no confirmation, and an
exit code that is unconditionally 0 so no caller can detect it ran. The
pre-push hook's remedy text points operators straight at it.

The gopher audit's F4 said "these are **not** to be absorbed silently — accept by
NAME or fix" and "No silent baseline widening." **That framing is refuted by the
code**: accepting by name and absorbing everything silently are the *same
command*. The name goes in a `by` field that `main()` defaults to `"operator"`.

### ✅ CONFIRMED, NOT THEORETICAL — the self-widening already fired once

I went looking for proof the machine had actually used the command on itself,
and the register confesses in its own bytes. `configs/violation_baseline.json`
was last written **2026-09-26 19:14:22** (not by me — my writes were 21:10), and
the uncommitted diff on that file contains this note, verbatim:

> "Register repair in the same landing: **an accidental baseline-update
> invocation (argparse ran the subcommand on --help) added 5 foreign claims under
> by=operator** (0dfc04119a40f245 transport_precheck, 3b1726dec4670996
> openrouter_free_gate, 8d41e611f98d3fa5 census_drift_patrol,
> e3b7845ea79cf553 queue_dupes_check, f0d81bd311a1a15e probe20_run); all 5
> removed here, their lanes owe their own named acceptance."

I verified all five fingerprints are now **absent** from the register — the
repair is real. But read what the incident proves:

1. **It fired.** Five claims from five unrelated lanes were written into the
   estate's debt register in one command, stamped `by=operator` (the forged
   default), by an invocation the operator never intended.
2. **Nothing caught it.** The command exits 0. The pre-push hook's own remedy
   text points operators at it. The register was only made honest because **one
   lane happened to read its own diff** and noticed five fingerprints it had
   never written. That is not a control. That is luck with a receipt.
3. **The current `--help` path is now safe** (I re-checked: `argv[1]="--help"`
   is not in the command set, so it returns 2 and writes nothing — mtime
   unchanged at 19:14 through my run). The *trigger* was fixed. **The
   ungated zero-exit write path itself was not** — `cmd_baseline_update` is
   byte-identical in shape to what caused the incident, and the fix addressed
   the typo, not the hole.

So `F-GATE-SELF-WIDENS` is not a hypothetical. The estate has a demonstrated
history of the machine widening its own gate, and the only reason the register is
currently honest is a human-adjacent agent reading a diff.

Two more of the same shape:

- **No exceptions ever expire.** The comment at line 70-71 promises "exceptions
  rot into violations instead of silently living forever." Bytes:
  `configs/violation_baseline.json` has **933 accepted claims and 0 with an
  `expires` field.** The expiry mechanism is not a safety net; it is a code path
  no claim has ever entered. The promise is theatre. (The B2-273 growth law is
  the same story: 194 `file-too-long` claims, and the check prints `GROWTH` lines
  as *non-blocking* text.)
- **The register is 72% self-written.** Of 933 claims: 673 by
  `agent:ratchet-v2-0925`, 191 by `operator:bootstrap 2026-09-24`, and 0 by
  anything reading `operator` alone. The "human accepted this by name" story is
  an agent's `--note` string.

**And the daily meter that would have caught it:** `logs/ratchet_daily.log` has
**2 `END` lines total, both with `ratchet=1`.** The gate has been failing since
it was registered and the log records two days of continuous failure with no
change in state. `MagCensusPatrolDaily` (08:30) and `Estate Ratchet` (09:45) are
Windows scheduled tasks; a failing meter that nobody reads is the same object as
no meter.

---

## PART 4 — THE SELF-REFERENCE: WHICH OF OUR FINDINGS STAND ON A BROKEN TOOL

This audit is run by the fleet, on the fleet, with the fleet's instruments. Naming
the dependency is the only way to keep the finding honest.

| our conclusion | depends on | if that tool is wrong |
|---|---|---|
| M1 coverage note, M2 13,687, R1 1,380 orphans | `os.listdir` + `json.loads` + git. **No fleet tool.** | Survives. These are the strongest findings precisely because they use no estate instrument. |
| M3 census drift | `tools/census_drift_patrol.py` | If the collector mis-parses pytest's tail, the 2,294 is wrong. **Mitigated:** I can re-derive with raw pytest. |
| M4 ratchet scope | `Path.glob("*.py")` semantics — stdlib | Survives. |
| PART 3 gate-can't-fail | reading `violation_ratchet.py` source | Survives. |
| "Ratchet works" (F4 verified) | the ratchet's own scanner | **This is the one that inherits a broken tool.** The ratchet detects via `ast.parse` and a hardcoded `SCANNER_RULES` set of 9 rules. Any disease not in those 9 rules is invisible *by construction*. The 652 `except-pass` claims prove the rule fires; nothing proves the rule set is the right 9. |

**The fleet instrument other lanes are citing, and it is broken:**
`.mimosa/` is the security/finding scanner. Of **2,046 recorded runs, 312
contain `scanner_failed: spawnSync ... ETIMEDOUT` (15.2%)**. By day: 09-25
33%, **09-26 40%**, 09-27 11%. A scanner that fails 40% of the time and records
the failure *in its own history* produces a coverage number that silently
excludes the failed runs. Any "mimosa found N findings, coverage is good" claim
from the last two days is computed over a denominator that dropped 40% without
announcement. **This is the same failure class as the 1,341 fossil and the 13,687
prose number, in a security tool.**

---

## PART 5 — WHAT NOBODY WILL ASK: 5 structurally-absent questions

Method: extracted every question-shaped sentence from 1,447 markdown files under
`watch/inbox/` (1,414 question sentences, 844 top-level `.md`), then tested 16
interrogative themes for presence. Twelve themes appear. **Four have zero hits
across the entire archive** — and they are not peripheral; they are the four the
prior art already gestures at *in its own "On missing itself" section* without
ever once being asked as a question the estate must answer.

**Q1 — This is the absent question, stated plainly: _If every instrument in this
estate was built inside the hall of mirrors, what experiment could distinguish
"the estate is healthy" from "the estate's instruments are consistently
agreeing with each other because they all share the same blind spot"?_
Nobody in 1,414 archived questions asks for a **cross-instrument disagreement
test** — two independently-implemented meters that must be able to contradict
each other. Zero hits on `would your instruments even notice`. Every meter here
is derived from the same `os.walk` + `json.loads` + the same tree. The estate has
N instruments and 1 viewpoint. A second opinion is not a gap in coverage; it does
not exist.

**Q2 — _Which of the numbers we are about to publish would still be true if the
estate's own definitions changed tomorrow — and who is allowed to change a
definition without invalidating the number?_**
The archive asks about drift of *values* (M3, the 12→1,380 case) and never about
drift of *units*. `disk 349 vs carrier 303` was dismissed as "instrument lag"
when it is a units dispute. `13,687` is a units dispute (prose count vs sidecar
rows). The B2-249 "carrier shape law" in `AGENTS.md:27` makes the census number
*depend on the exact English grammar of the bullet* — rewording the sentence
breaks the gate. **The estate's most-cited number is hostage to a markdown
wording.** Nobody has asked who owns the definition.

**Q3 — _If the only remedy the enforcement point offers is "run this other
command," and that other command always exits 0 and defaults its own author to
"operator," is the enforcement point an enforcement point?_**
The archive's own `SOCRATIC_GAPS_20260918.md` asks "who audits the auditor's
corrections?" — 2 hits, both rhetorical, never followed by an answer. It does
not ask the sharper structural form: **not "who audits" but "is the audit
trail's own write path the thing being audited."** A gate whose FAIL remedy is a
self-certifying zero-exit write, wired into a hook that points operators at it,
is a gate with a pull toward opening. Zero hits on `widen its own` outside my
own document.

**Q4 — _What is the estate's rate of un-receipted reality — bytes that changed
with no card, no queue row, and no chain knot — and is that number being measured
at all?_**
Every instrument here counts **artifacts** (cards, knots, claims, files). Not one
counts **silence**. 1,380 vanished knots produced no receipt; 1,379 untracked
paths and 889 untracked `watch/` files in the gopher audit produced no drift
alarm; the census carrier moved 1,910→2,294 with no card. The absence of a
receipt is treated as the absence of an event. A meter that can only see what was
written down is structurally incapable of noticing what wasn't. This is the
sharpest form of the SOCRATIC "close-rate died at 0.0" observation — and the
archive never converts it into "**we have no instrument for unrecorded change,
and unrecorded change is the class of thing that has actually happened.**"

*(bonus, structurally absent: Q5 — _whose decision is it to keep a number?*
`state/CURRENT.md` is frozen 09-08 and still cited as live status; the census
carrier is hand-edited within a minute of its own detector firing. The estate has
no expiry on its own claims and no named owner. Who is allowed to say "this
number is now wrong, retire it" — and is that ever recorded? The 933-claim
baseline with 0 expiries is the same disease in the ratchet, and the two are
never connected in any document.)*

---

## WHAT WOULD FALSIFY THIS LANE

- A knot-restore receipt dated after 2026-09-11 that re-creates the 1,199 August
  filenames as bytes would refute R1's "actively worsening" and reduce this to
  "stale documentation" (still a finding, a smaller one).
- If the 1,380 chain-named-but-absent files resolve to a *second* store
  (a mounted cage copy, a `.mimosa` snapshot) rather than being gone, R1 becomes
  a **naming** bug, not a **loss** bug. I checked `git ls-files` and found no
  copy; I did not search the desktop corpus.
- If `configs/violation_baseline.json` gains a non-empty `expires` population,
  PART 3's second bullet drops to a weaker "the expiry path is unused today."

---

## Verdict

**The prior map is NOT a safe foundation.** Of its load-bearing claims, one is
refuted 115×, one is refuted as a category error ("correct wiring" ≠
"enforces"), and one — the census drift — is real but is *invisible to the very
hook the prior map certified as healthy*. The chain's health story ("13,687
orphans reconciled by completion index") is a **comforting fiction built on a
hardcoded string literal**, and the "12 missing knots" story understates the
damage by two orders of magnitude and is getting worse this month.

The audit should be rebuilt on bytes, not on this map. The three findings that
survive every tool-substitution I could apply are: **1,380 missing knots
(R1)**, **the ratchet sees 39% of tracked Python (M4)**, and **`baseline-update`
is an ungated self-widening zero-exit write that forges `by="operator"` (PART 3).**
Those three use no fleet instrument. They are the ones I'd bet the audit on.
