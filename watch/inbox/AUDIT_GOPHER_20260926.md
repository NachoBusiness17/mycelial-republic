# AUDIT — gopher seat, 2026-09-26

**Scope:** read-only audit of `local_sovereign_agent` working tree + gate truth.
**Branch:** `mag/run-beta1-factory-build-audi-20260806T231709Z` @ `6d417abd5`
**Seat:** L2-Hermes (gopher). No repairs performed — this is a report, not a fix.

---

## Headline

Four findings. Two are live gate failures that will block a push. One is a
1.18 GB duplicated-pair tracked in git. One is the exact disease the repo's own
census bullet was written to prevent.

---

## F1 — Census carrier is 378 tests off byte truth (gate is FAILING, unwatched)

`AGENTS.md:27` claims:

    1,910 tests collected / 303 files (2026-09-26 census

Byte truth, `.venv\Scripts\python.exe -m pytest --collect-only -q`, same tree,
same day:

    2288 tests collected in 6.12s

Delta **+378** against a stated bar of 20. The gate already knows:

```
$ .venv\Scripts\python.exe tools/census_drift_patrol.py --collect
CENSUS-PATROL: COLLECT-DRIFT - collected drift: pytest holds 2288 vs carrier
               claim 1910 (delta +378, bar 20)
REAL_EXIT=1
```

**Why it survived:** the deep check is opt-in behind `--collect` and is
deliberately kept out of the default pre-push path (per its own B2-244 note,
because it needs the venv). The only scheduled runner is
`MagCensusPatrolDaily` at 08:30. So the detector works, the detector is armed,
and the detector was not consulted. This is the identical failure shape as the
retired 1,341 headline that B2-215 was written to kill — the tripwire caught the
symptom class and still shipped a stale number.

**Caveat that matters:** `census_drift_patrol` also reported
`disk 348 vs carrier 303` and called it *instrument lag*, evidence-only. Two
different denominators. The +378 collected-vs-collected gap is the real one;
do not "fix" 303 → 348 by editing the file count.

---

## F2 — Two byte-identical 590 MB ledgers tracked in git (1.18 GB duplicated)

```
7f3b2bc447d0cc43bb06b8e616063bf1dc6542ba7f8944c98097cd68873d0d1b  watch/ESTATE_INDEX/ESTATE_INDEX.jsonl
7f3b2bc447d0cc43bb06b8e616063bf1dc6542ba7f8944c98097cd68873d0d1b  dashboard/data/ESTATE_INDEX.jsonl
```

- identical sha256, not a symlink — two real files
- 590,246,188 bytes each, 1,700,130 lines each
- **both TRACKED** in git
- together the top churn line in the working tree: 526,260 ins / 47,188 del each

Also tracked and large:

| file | bytes | lines |
|---|---:|---:|
| `catalog/catalog.jsonl` | 133,894,969 | 489,548 |
| `catalog/tags.jsonl` | 100,786,698 | 489,548 |
| `training/events.jsonl` | 246,735,328 | 560,586 |

`.git` is **7.5 GB**.

---

## F3 — Root cause of F2: the .gitignore pattern is single-star

`.gitignore:142` reads `watch/*.jsonl`. Git's `*` does **not** cross `/`:

```
IGNORED       watch/foo.jsonl                          <- .gitignore:142  WORKS
NOT IGNORED   watch/ESTATE_INDEX/ESTATE_INDEX.jsonl    <- nested, misses
NOT IGNORED   dashboard/data/ESTATE_INDEX.jsonl
NOT IGNORED   catalog/catalog.jsonl
NOT IGNORED   training/events.jsonl
```

`catalog/` and `training/` have **no ignore coverage at all**. So the intent at
line 142 was plainly recursive, and the one-star spelling silently exempted
exactly the path that mattered most. This is a one-line root cause for the
whole 1.18 GB pair — fix the pattern, not the files.

---

## F4 — Ratchet: 6 NEW violations, pre-push will block

```
$ .venv\Scripts\python.exe tools/violation_ratchet.py check --changed
RATCHET check: scope=101 changed files; hits=70; registered=64; NEW=6
REAL_EXIT=1
```

The six, all in `tools/`:

| id | file | kind |
|---|---|---|
| `5ae40a2d` | `tools/ledger_lock.py:125` | silent `except: pass` |
| `3b1726de` | `tools/openrouter_free_gate.py:84` | silent `except: pass` |
| `f0d81bd3` | `tools/probe20_run.py:421` | file-too-long (>400 lines) |
| `e3b7845e` | `tools/queue_dupes_check.py:33` | cwd-relative Path |
| `0dfc0411` | `tools/transport_precheck.py:134` | silent `except: pass` |
| `f2ce896c` | `tools/visor.py:131` | silent `except: pass` |

Per the ratchet contract these are **not** to be absorbed silently — accept by
NAME or fix. `configs/violation_baseline.json` is a 3-key dict.

---

## Working-tree shape (context for the above)

- 1,313 dirty paths: **1,087 untracked**, 225 modified, 1 deleted
- 889 untracked files under `watch/` — receipt pile, uncommitted
- 225 modified files, 1,864,899 ins / 1,409,638 del
- **the churn is real, not CRLF**: `--ignore-cr-at-eol` still shows
  1,864,654 / 1,409,387. Only ~250 lines of the 2.8M-line diff is line endings.
  The diff is the F2 ledgers rewriting themselves.

## What is healthy

- **Hook wiring is correct.** `core.hooksPath` = `githooks`, `githooks/pre-push`
  present and executable (17,853 bytes). No stray `.git/hooks/pre-push`.
- **Freshness gate PASSES.** heartbeat 0.1d, `BOOT_4_7.md` 0.9d `[frozen-ok]`,
  all boot docs inside the 7d bar.
- **Ratchet itself works** — it caught its 6. It is the operator-loop that isn't
  running, same shape as F1.

## Catalog note (F2 adjacent, lower severity)

`catalog/catalog.jsonl` holds 489,548 rows, unique ids, no dupes. It indexes
**beyond this repo**: zones `lsa` (60,034), `ext:azerothcore-wow` (10,356),
`ext:ai-job-search` (96), `ext:field-strike-the-chord` (68). The repo itself
holds 1,519,630 files. 55 junk paths (`.bak`/`.tmp`/`.digtmp`) appear in the
first 20 MB alone. Not a correctness bug — a growth curve with no ceiling, and a
likely contributor to the 489k-line rewrite cost.

---

## Not measured

`du -sh --exclude=.git .` timed out at 300 s. **Total worktree size is unknown.**
Given the five tracked ledgers sum to ~1.66 GB, it is large; the exact figure
needs a longer budget before any disk-reclaim claim is made.

---

## Recommended order (operator call — not performed)

1. F3 first: one-line `.gitignore` fix (`**/*.jsonl` scoped) unblocks F2.
2. F2: decide the ledger policy — untrack, or make the second path a real
   symlink. Do NOT hand-delete; these are append-only tape.
3. F1: refresh the `AGENTS.md:27` carrier from the 2,288 figure and *name what
   landed between the census and now*, per its own unattributable-drift rule.
   Then decide whether the deep check should join the default pre-push path.
4. F4: six ratchet items — fix or accept by name. No silent baseline widening.
