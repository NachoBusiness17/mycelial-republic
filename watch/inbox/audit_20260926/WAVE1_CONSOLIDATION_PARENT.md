# WAVE 1 CONSOLIDATION — PARENT ADJUDICATION OF CONFLICTS
## 2026-09-26 — 9 of 10 lanes landed. This file settles what they disagree on.

*Wave 1: lanes 1,2,3,4,5,6,7,9,10 completed (5,101s). Lane 8 (canonicality)
was interrupted at 972s and is re-dispatched in wave 2. Several lanes reported
mutually contradictory numbers. Each conflict below was re-measured by the
parent seat with a fresh command, and the losing claim is recorded rather than
quietly dropped.*

---

## CONFLICT A — I was wrong about the xAI key. Lane 9 is right.

Earlier in this audit I examined `memory/trajectory/steps.jsonl:3310`, saw an
`xai-` token, and classified it as a **false positive — "pre-masked, matches the
tar finding."** Lane 9 reported it as a **real 84-char key, git-tracked.**

**Lane 9 is correct and my classification was wrong.** The discriminator is
decisive: a hand-redacted key contains literal dots (`xai-gO...qe6D`, which is
what the tar transcripts actually contain). This token does not:

```
token len=84   contains_literal_dots=False   head=xai-3I   tail=BLI
-> NO DOTS = REAL KEY
```

**And it is committed**, not just on disk:

```
git ls-files memory/trajectory/steps.jsonl          -> TRACKED
git show HEAD:memory/trajectory/steps.jsonl | sed -n 3310p
    -> xai-3I0w...MASKED...      (present in the committed object)
git log -1 -- memory/trajectory/steps.jsonl
    -> 6d417abd5  B2-479 reset-day exposure scoping
```

Lane 9's mechanism also holds: the step log captured the **stdout of a shell
command**, so a `cat .env`-style command wrote a live key into a tracked
ledger. **A filename filter cannot see this class of exposure, because the file
is named `steps.jsonl`, not `.env`.**

This is the same key lane 9 found in the tar. So the exposure is real in at
least two places, one of them committed. **My earlier "refuted" verdict on lane
9 was itself the error** — I checked the tar, generalized to the transcript,
and generalized again to `steps.jsonl` without re-measuring. Two generalization
steps too far.

**Correction to my own prior report:** I told the operator the xAI finding was
"refuted as stated." It was refuted *in the tar* (pre-masked there) and real
*in `steps.jsonl`*. Those are different files and I conflated them.

## CONFLICT B — the census moved again, live, during the audit

| when | instrument | count |
|---|---|---:|
| my first report | `pytest --collect-only -q` | 2,288 |
| wave 1, 4 separate probes | same | 2,288 |
| **re-measured just now** | same | **2,294** |

**+6 tests landed during the audit.** The carrier still says 1,910, so the
drift is now **+384, not +378**. Lane 5 and lane 10 both reported 2,294
independently before I re-measured — they were right and my stored figure was
stale.

This is the repo's own "census denominator law" made concrete: a count is a
snapshot of one tree at one moment. It also means **no test count in this audit
should be quoted without its timestamp**, including the ones I already gave you.

## CONFLICT C — ratchet NEW: 6, not 7. Lane 2's count is stale.

```
RATCHET check: scope=104 changed files; hits=70; registered=64; NEW=6
```
Six, confirmed. The scope moved 101 → 104 files as lanes wrote files. Lane 2
read 7 earlier in the run; the 7th was absorbed or the set shifted. **6 is
current.**

## CONFLICT D — config_seal: 6 modified, not 3.

```
CONFIG-SEAL verify: sealed=49 live=53 modified=6 missing=0 unsealed=4
```
Six MODIFIED + four UNSEALED = **10 problems**. Lane 6 reported 3 modified.
Six is current; the number has been climbing as configs are touched.

## CONFLICT E — dead tools: my 80 vs lane 2's 29. Both are right about different things.

| measure | parent | lane 2 |
|---|---:|---:|
| DEAD (no code, no doc, no test) | 80 | 29 |
| ORPHAN | 50 | 59 |
| LIVE | 34 | 75 |
| has a test | 34 | 20 |

The gap is definitional. My sweep restricted its haystack to first-party
surfaces (code, tests, docs, configs, hooks) and excluded `corpus/`, `attic/`,
`library/`, `mine/`. Lane 2 swept more broadly, so tools referenced only from
those trees moved from DEAD to LIVE/ORPHAN for it. **Both numbers are correct
for their scope; neither is the other's error.** The honest statement is
**34–75 wired depending on what counts as a caller**, against 164 tools.

## The findings that no lane disputes

These were measured independently by multiple parties and survived
adjudication:

1. **`memory/tls/lan.key`** — 1675-byte RSA private key, mode 644, tracked,
   in `Mag-backup.git` across 39 refs. Found by me, independently rediscovered
   by wave-2 lane 7's scanner.
2. **The suite is not green** — lane 7 measured **33 failed, 2,246 passed, 9
   skipped** in 54:47. Cause: 11 stale baseline pins, **14 real bugs**, 4
   missing assets, 0 flaky. This is new information no prior audit had.
3. **`config_seal` RED (10) + ratchet NEW (6) both block push** with
   `|| exit 1` at `githooks/pre-push:10,12`.
4. **The hook has likely never run against a real push** (lane 3): local HEAD
   `6d417abd5` is **absent from the backup object store**, the backup's newest
   ref on this branch is **2026-09-19 — six days before the hook was armed**,
   and `git_backup.cmd:25` gates push on `findstr /i "origin"`, which never
   matches. The reflog's newest entry reads `first zero-push morning`.
5. **`.mimosa` is ~15.8 GB at 204× duplication** (lane 5), 1,133,655 `.source`
   files holding 5,542 unique. Already gitignored; the defect is retention.
6. **The ratchet's escape hatch is routine** (lane 6): 933 accepted debts in
   `configs/violation_baseline.json`; `cmd_baseline_update` returns
   unconditional 0 and defaults its author to `by="operator"`.
7. **The ratchet only scans top-level `glob("*.py")`** (lane 10) — 39% of
   tracked Python, **145 nested files never scanned**.
8. **No secret-scanning gate exists** (lane 9, confirmed by me).
9. **Worktree `worktrees/` holds 44 uncommitted entries across 2 real git
   worktrees, neither prunable** (lane 4) — including 5 never-committed core
   modules in `sovereign-mirror-scaffold`. A cleanup sweep would destroy work
   with no git warning.

## The claim lane 10 refuted with bytes

**"12 missing knots"** — sold in the prior map as *"two measurements, one
answer"*, the strongest-form evidence it had:

```
CLAIM 09-11:  7,377 refs / 7,365 present / 12 missing
BYTES 09-26:  7,811 rows -> 6,431 present / 1,380 MISSING   = 115x
missing by month: 2026-08 = 1,199   2026-09 = 181
git log --diff-filter=D -- memory/biography/knots : no deletions
```

**181 September misses post-date the receipt** — this is worsening now, not
stale documentation. And git records no committed deletion, so these are
uncommitted bytes that vanished while the append-only chain names them as
existing. This bears directly on the operator's standing ruling that the missing
knots are a "documented recurring wipe"; the count is 115× the documented one.

**Two more refuted:** "13,687 orphans reconciled by completion index" is a
hand-typed prose number sitting 9 off the sidecar's real 13,678, on rows that
carry **no `verkle_root` and no `parent_verkle_root`** — a lookup table, not a
reconciliation. And my own "hook wiring is correct" verified all three
sub-claims and still fails: 5 of 8 push-gate blocks are self-declared
`NEVER exits nonzero`.

## Confidence ledger

| claim | status |
|---|---|
| `lan.key` exposed | **CONFIRMED** (2 independent finders) |
| xAI key in `steps.jsonl` (committed) | **CONFIRMED** — my earlier refutation was wrong |
| suite has 33 real failures | **CONFIRMED** (lane 7, full 54-min run) |
| census 2,294 / carrier 1,910 | **CONFIRMED**, drift +384 and growing |
| config_seal 10 problems | **CONFIRMED** (re-measured) |
| ratchet 6 NEW | **CONFIRMED** (re-measured) |
| hook never fired on a real push | **STRONG** (HEAD absent from backup; reflog says so) |
| 1,380 missing knots | **CONFIRMED by lane 10**, contradicts operating law |
| 80 vs 29 dead tools | **SCOPE-DEPENDENT**, both correct |
| `steps.jsonl:1994` telegram token | **OPEN** — needs a human eye |
| `mag/lab_episode.py:117` `sk-` token | **OPEN** — likely a false positive, unconfirmed |
| git-history secret scan | **NOT DONE** — wave-2 lane 7's harness failed after enumerating 64,816 blobs |
