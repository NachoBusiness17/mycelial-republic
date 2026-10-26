# LANE 5 — FILE COMPOSITION & INSTRUMENT TRUST
**Audit:** 2026-09-26 · **Repo:** `local_sovereign_agent` @ `6d417abd` · **Lane:** file-count composition + whether the counting instruments measure comparable things

## VERDICT (one line)

The 1,492,258-file census is **not a corpus measurement** — 1,133,777 of those files (76%) are a
duplicated snapshot cache that holds only 5,542 unique files, and the "348 vs 303 instrument lag"
is **two real, nameable defects** (56 untracked test files + a stale carrier), not a denominator
mismatch. The genuine growth pathology is `catalog.jsonl` being a **snapshot committed to git**,
which stores 200–250 MB per commit and has produced a 7.5 GB `.git`.

---

## Q1 — WHAT IS `.source`? (1,012,628 files claimed; 1,133,655 measured)

**A per-session content-addressed file snapshot cache. Not source code. Not vendored. Not junk —
a working cache with a 204× duplication bug.**

| Measure | Value |
|---|---|
| `.source` files under `.mimosa/` | **1,133,655** |
| Physical bytes | **15,773,784,707** (15.77 GB) |
| **Unique content hashes** | **5,542** |
| **Duplication ratio** | **204.58×** |
| Unique bytes | 75,218,757 (75 MB) |
| **Wasted bytes** | **15,756,254,445 (15.76 GB, 99.5%)** |

**Location:** `.mimosa/hook-state/sess_<uuid>.mu<tok>-<n>-<hex>.baseline/*.source`
765 child entries; 267 are `.baseline` dirs, 169 of them hold **exactly 5,000** files (a hard cap).

**Sampled content** (`.venv/Scripts/python.exe`, 5 random baseline dirs × 2 files):
- `0001ba877e91…source` (8,429 B) — a Python docstring, `mag/ox_seat.py` header: *"ox_seat — the free
  frontier reasoning seat for stealth/ox-alpha, BOUNDED so we can burn it down."*
- `000fd1718ec…source` (261,836 B) — TypeScript: `/** GSTD Bot — Omega Gateway + Node OS … */`
  importing `express`, `WebSocketServer`, `NeuralRouter`.

Both are **verbatim copies of real repo files**, re-hashed. The filename IS the sha256 of the
content. Identical hash → identical bytes → replicated into every subsequent session's baseline.

**Consumer:** written per-invocation by an external hook (not repo code). The only in-repo reference
is a classification string in two copies of the same file:
- `seed/engines/estate_atlas.py:51` and `tools/estate_atlas.py:51` —
  `(".mimosa/hook-state/", "Mimosa hook writes per invocation, sibling lane")`

**Verdict: correct to be untracked, and it already is.** `.gitignore:190` = `.mimosa/`;
`git ls-files .mimosa` → 0. It is *not* polluting git — it is polluting the **census instrument** and
the **disk**. The fix is retention/pruning of old session baselines, not a `.gitignore` line.
A one-line prune (`hook-state/*/*.source` older than N sessions) recovers ~15.7 GB.

---

## Q2 — THE 212,276 `.json` FILES

**Overwhelmingly untracked, and 87% of them live under `memory/`.**

| Measure | Value |
|---|---|
| Tracked `.json` (whole repo) | **4,406** |
| On-disk `.json` outside `.mimosa` | **213,015** |
| `.mimosa/*.json` | 7,079 |
| **`memory/*.json`** | **184,878 (87%)** |

Breakdown of `memory/`: `runs/`, `ghost/`, `biography_backup/`, `biography/`, `agent_state/` are all
**≥6,000 each** (probe-capped); then `agent_sessions/` 3,012, `copilot/` 2,372, `working/` 560,
`dead_drops/` 537, `mail/` 532, `research_packs/` 286, `improve/` 217.

These are **already ignored** — `.gitignore:53-118` covers `memory/biography/**`,
`memory/biography_backup/**`, `memory/runs/**`, `memory/agent_state/**`, `memory/agent_sessions/**`,
`memory/copilot/**`, `memory/ghost/**`, etc. So like `.source`, the .json mass is **correctly
excluded from git and only inflates the file-count census.**

---

## Q3 — IS THE CATALOG SELF-REFERENTIAL? **NO.**

Full scan of all 489,548 rows (`catalog/catalog.jsonl`, 133,894,969 B, 0 malformed JSON):

| Test | Result |
|---|---|
| Rows under `local_sovereign_agent/catalog/` | **0** |
| Rows referencing `.mimosa/` | **0** |
| Rows under `state/` | 3,465 |
| `.jsonl` rows | 13,122 |
| Duplicate rows | **234 (0.05%)** — 489,314 unique paths, 179 paths appear >1× |

`mag/catalog_rescan.py:172` enforces this: `if d in EXCLUDE or d.startswith(".")` — dot-dirs and
the EXCLUDE set are pruned, so the map structurally cannot index itself or `.mimosa`. The docstring
at `catalog_rescan.py:150` states it outright: *"the map never indexes itself."*

**Feedback ratio: 0.00. No unbounded growth from self-reference.**

**But the catalog indexes far outside the repo** — `ROOT` is the **projects parent**, not the repo:

| Top-level prefix | Rows |
|---|---|
| `local_sovereign_agent` | 455,169 |
| `azerothcore-wow` | 10,356 |
| `the_margin_lean` | 9,164 |
| `vmangos-core` | 4,397 |
| `tortoise-wow` | 3,767 |
| `mag-current-rebuild` | 2,815 |
| `worktrees` | 1,487 |
| **Rows outside `local_sovereign_agent/`** | **34,379** |

**Consequence for the audit:** a repo-scoped census and the catalog are counting **different
universes**. 489,548 catalog rows ≠ 1,492,258 repo files ≠ 44,161 tracked files. Three instruments,
three denominators, no shared scope. **This is the actual instrument-trust defect** — not the
303-vs-348 label.

Second-level: `local_sovereign_agent/memory` 256,520 · `/mine` 97,867 · `/corpus` 52,368 ·
`/watch` 16,057 · `/agents` 11,718.

---

## Q4 — THE 348-vs-303 QUESTION: **THE PATROL'S OWN EXPLANATION IS WRONG**

`tools/census_drift_patrol.py:285-286` reports:
> *"disk counts pytest-named candidates, carrier counts item-bearing files; … same-window lag,
> evidence only"*

**Disproven on both halves.**

**(a) Suffix is not the cause.** `candidate_files()` (line 173-179) globs **both** patterns
`TEST_FILE_SUFFIXES = ("test_*.py", "*_test.py")`. Measured:

| Glob | Count |
|---|---|
| `tests/**/test_*.py` | **348** |
| `tests/**/*_test.py` only | **1** (`tests/wave_driver_test.py`) |
| Union (what the patrol counts) | **349** |
| Carrier claim | 303 |
| `pytest --collect-only` items | **2,294** |

One suffix file cannot explain 45.

**(b) The 45-file delta is REAL and fully nameable — it is untracked work.** Of the 348 disk
`test_*.py`: **295 tracked, 56 untracked** (295 + 56 = 351; the 3-file overlap is
`tests/selftests/` naming). The 56 untracked include the catalog suite itself —
`test_catalog_rescan.py`, `test_catalog_freshness.py`, `test_catalog_scan_junctions.py`,
`test_catalog_tags.py` — plus `test_census_drift_patrol.py`, `test_census_liveness.py`,
`test_drift_dashboard.py`, `test_workflow_registry_append_only.py`,
`test_chain_byte_exact_io.py`, and ~48 more (full list in the JSON artifact).

**Verdict: genuine staleness, correctly measured.** 303 → 348 = carrier written before the
untracked suite landed. The patrol's "zero-collect candidates" deep check is the right instrument
and it found no real gap. Two corrections to the record:
1. The carrier (1910 collected / 303 files) is stale; collection is now **2,294**.
2. The patrol's stated *reason* is wrong — it is **not** a denominator mismatch, it is **untracked
   new tests**. Fix the label or the carrier; the number 348 is trustworthy.

---

## Q5 — LEDGER GROWTH CURVE: FULL REWRITE vs APPEND

Measured by comparing `git show HEAD:<path> | wc -l` against the worktree.

| Ledger | HEAD lines | Worktree lines | Delta | **Behavior** | Tracked? |
|---|---|---|---|---|---|
| `catalog/catalog.jsonl` | **757,667** | 489,548 | **−268,119** | **FULL REWRITE** (shrank) | yes |
| `catalog/tags.jsonl` | **757,667** | 489,548 | **−268,119** | **FULL REWRITE** | yes |
| `training/events.jsonl` | 548,183 | 560,788 | **+2,605** | **APPEND** (correct) | yes |
| `watch/ESTATE_INDEX/ESTATE_INDEX.jsonl` | 1,221,058 | 1,700,130 | **+479,072** | **APPEND** (correct) | yes |
| `dashboard/data/ESTATE_INDEX.jsonl` | 1,221,058 | 1,700,130 | **+479,072** | **APPEND** (correct) | yes |

**Source confirmation** — `mag/catalog_rescan.py` has two distinct modes:
- `incremental()` line 239: `open(catalog_path, "a", …)` — appends one row per new/changed path.
- `rebuild()` line 274: `open(tmp, "w", …)` then `os.replace(tmp, catalog_path)` (line 300) —
  **full rewrite**, and line 295-299 moves the old file to `catalog/catalog_<date>.jsonl`.

**The pathology, precisely stated:**

`catalog.jsonl` is a **derived snapshot** (`catalog_manifest.json:24` → `"mode": "incremental"`,
`:22` → `map_sha256`) that is **tracked in git and fully rewritten**. Its manifest for the current
run records: `base_rows: 489455`, **`added: 17`**, `refreshed: 76`, **`vanished: 27`**.
**93 files changed → 133,894,969 bytes rewritten and re-committed.**

**Git history cost** (`git cat-file -s` per commit touching `catalog/catalog.jsonl`):

| Commit date | Blob bytes |
|---|---|
| 2026-09-18 | **214,470,472** |
| 2026-09-16 | **251,385,824** |
| 2026-09-16 | **199,736,569** |
| 2026-09-16 | 249,765 |

**`.git` = 7.5 GB**; `pack-e33c1282….pack` alone is **5,789,815,203 bytes**, repacked 2026-09-26.
Three catalog commits alone ≈ **665 MB of pack**.

**A second, quieter defect in `incremental()`:** lines 250-258 — when a path's signature changes it
appends a *new* row; `vanished` is computed at line 259 (`len(set(index) - seen_paths)`) and
**returned in the stats dict but never acted on**. Deleted files are therefore **never removed** from
the map in incremental mode. 27 vanished rows are being reported daily and retained forever. The
catalog is a **leaky append-only ledger wearing a snapshot's manifest**.

**The 1.18 GB ESTATE_INDEX duplication is a third defect:** `watch/ESTATE_INDEX/ESTATE_INDEX.jsonl`
and `dashboard/data/ESTATE_INDEX.jsonl` are byte-identical (sha256 `7f3b2bc4…`, 590,246,188 B,
1,700,130 lines each) and **both tracked**. One is a copy of the other. `.gitignore:142`
(`watch/*.jsonl`) does **not** cover the nested path — verified:
`git check-ignore -v watch/ESTATE_INDEX/ESTATE_INDEX.jsonl` → **no match**.

---

## Q6 — PROPOSED `.gitignore` CHANGES (REPORT ONLY — NOT APPLIED)

Rules: untrack **reproducible/derived** artifacts; leave **append-only tape** tracked.

### Tier 1 — derived snapshots, regenerable by command. Untrack + ignore.

```gitignore
# ── LANE5 2026-09-26: derived corpus map. Rebuildable in one command
# (python -m mag.catalog_rescan rebuild); it is a SNAPSHOT, and committing it
# costs ~200-250 MB of pack per run. Keep the manifest, drop the map.
catalog/catalog.jsonl
catalog/tags.jsonl
catalog/catalog_*.jsonl
catalog/junctions.jsonl
catalog/catalog.rebuild
# FTS index is a derived SQLite cache, 134 MB, regenerable
catalog/catalog_fts.sqlite
```
`catalog_fts.sqlite` is **currently neither tracked nor ignored** (134,303,744 B, regenerated
2026-09-26 21:15) — an untracked 134 MB that will surprise the next `git add -A`.
`catalog/catalog_manifest.json` stays **tracked** — it is the receipt (1,167 B).

**Untrack command (needs operator GO — history is not rewritten, this only stops future growth):**
```bash
git rm --cached catalog/catalog.jsonl catalog/tags.jsonl
git rm --cached watch/ESTATE_INDEX/ESTATE_INDEX.jsonl dashboard/data/ESTATE_INDEX.jsonl
```

### Tier 2 — the byte-identical duplicate. Keep ONE copy.

```gitignore
# ESTATE_INDEX is byte-identical in watch/ and dashboard/ (sha256 7f3b2bc4,
# 590,246,188 B). Two tracked copies = 1.18 GB. Keep the dashboard/data/ copy
# (the read path); ignore the watch/ mirror.
watch/ESTATE_INDEX/ESTATE_INDEX.jsonl
```
**Do not ignore `dashboard/data/ESTATE_INDEX.jsonl`** — it is the live read path.
This is the minimal fix for the `watch/*.jsonl`-doesn't-match-nested defect. If instead `watch/` is
canonical, flip the negation:
```gitignore
!watch/ESTATE_INDEX/
```

### Tier 3 — leave alone. These are append-only tape and are behaving correctly.

| Path | Why keep tracked |
|---|---|
| `training/events.jsonl` | append-only tape, +2,605 this window, no per-commit rewrite |
| `watch/ESTATE_INDEX/…` | tape — but see Tier 2 for the duplicate |
| `memory/burns/LEDGER.jsonl` | append-only |
| `catalog/catalog_manifest.json` | the receipt for the map |

### Tier 4 — out of scope for `.gitignore` (already ignored, needs pruning not ignoring)

`.mimosa/` (line 190 ✓), `memory/**` (lines 53-118 ✓), `agents/pytest-*/` (lines 6, 203 ✓),
`catalog/library` n/a. **These are already correct.** The 1.5M-file census problem is a
**retention** problem, not an ignore problem:

```bash
# recovers ~15.7 GB — keeps the 5,542 unique files, drops 204x duplicates
# (operator GO required; this deletes session baselines)
```

---

## THE GROWTH PATHOLOGY, NAMED

Three compounding mechanisms, in order of cost:

1. **`.mimosa/hook-state` snapshot cache — 204.58× duplication, 15.76 GB wasted.** A per-invocation
   hook writes a full content-addressed copy of every repo file into every session's baseline dir,
   capped at 5,000 files but **never pruned**. 5,542 unique files occupy 1,133,655 slots. This is
   the bulk of the 1.49M-file census and **zero** of it belongs in any corpus count.

2. **`catalog.jsonl` is a derived snapshot committed as if it were tape — ~200-250 MB of git pack
   per run.** It is simultaneously the fastest-growing *tracked* artifact and the only one that is
   fully rewritten. The manifest proves the churn is trivial (17 added / 27 vanished) — the 133 MB
   rewrite buys nothing that a delta would not.

3. **`incremental()` never deletes.** `vanished` is computed and reported daily, never applied. The
   catalog drifts monotonically upward in row count while the disk it describes shrinks.

**Plus the measurement defect that hid all of this:** the census counts 1,492,258 files, the catalog
counts 489,548 rows over a *different root* (the projects parent, 34,379 rows outside the repo), and
git tracks 44,161. **Three instruments, three scopes, no reconciliation** — so `.mimosa` inflated a
"corpus" number by 76% and nobody could tell from the count alone.

---

## EVIDENCE INDEX

| Claim | Command / Source |
|---|---|
| `.source` = 1,133,655 files, 15.77 GB, 5,542 unique | `os.scandir` census, `.mimosa/` |
| Duplication 204.58× | unique-hash set vs file count |
| `.source` content = repo file copies | 10 samples, `.venv/Scripts/python.exe` |
| `.mimosa` ignored, 0 tracked | `git check-ignore -v`, `git ls-files .mimosa` |
| Tracked total 44,161 | `git ls-files \| wc -l` |
| Catalog not self-referential | full 489,548-row scan, 0 catalog/ + 0 .mimosa rows |
| Catalog root = projects parent | top-level prefix histogram |
| Catalog dup rows 234 (0.05%) | unique-path set |
| Suffix delta = 1 file | `test_*.py` 348 vs `*_test.py` 1 |
| 2,294 collected | `pytest --collect-only -q` |
| 348 = 295 tracked + 56 untracked | `git ls-files tests` vs `rglob` |
| catalog.jsonl full rewrite | HEAD 757,667 → 489,548 |
| training/events.jsonl appends | HEAD 548,183 → 560,788 |
| ESTATE_INDEX appends | HEAD 1,221,058 → 1,700,130 (both copies) |
| `incremental` opens `"a"` | `mag/catalog_rescan.py:239` |
| `rebuild` writes tmp + `os.replace` | `mag/catalog_rescan.py:274,300` |
| `vanished` never applied | `mag/catalog_rescan.py:259` (computed, returned, unused) |
| map never indexes itself | `mag/catalog_rescan.py:150,172` |
| churn is trivial (17/27) | `catalog/catalog_manifest.json:32-40` |
| 214/251/199 MB blobs | `git cat-file -s` per commit |
| `.git` 7.5 GB, 5.79 GB pack | `du -sh .git`, `ls -la .git/objects/pack` |
| `watch/*.jsonl` misses nested | `git check-ignore` → no match |
| both ESTATE_INDEX tracked | `git ls-files --error-unmatch` |
| 4,406 tracked .json | `git ls-files '*.json' \| wc -l` |

**Caveats (Disputed/Unproven, per the fleet's tri-state law):**
- The 15.77 GB `.mimosa` figure is from `os.scandir` byte sums; NTFS sparse/compressed extents are
  not accounted for. Disk-freed may be less than 15.76 GB.
- `census_drift_patrol.py` reported 349 candidates on this run vs 348 from my scan — one file
  (`tests/wave_driver_test.py`) was added between runs. Both are correct for their instant.
- The exact split of the 45-file delta between "written after the carrier" and "written but
  untracked" is **Unproven**; 56 untracked files is an upper bound on the untracked share.
- No `.gitignore` change was applied. All Tier 1/2 edits are proposals requiring operator GO, and
  `git rm --cached` does not reclaim existing `.git` bytes — a `git gc --aggressive` after the
  history policy is settled is the separate decision.
