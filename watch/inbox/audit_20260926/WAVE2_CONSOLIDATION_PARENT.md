# WAVE 2 CONSOLIDATION — PARENT
## 2026-09-26 — the 48 GB is finally accounted for. Read this one first.

*Wave 2: 3 lanes completed (disk, push-gates, rib compiler), 2 interrupted by my
stop order (test-shape, unversioned-verify). The disk lane replaced the
measurement I called "the biggest gap in my first report." It is closed.*

---

## THE 48 GB, ACCOUNTED

```
worktree proper   30.92 GiB
  + .git            7.50
  + .mimosa        15.70
  = TOTAL          54.12 GiB
```

| class | bytes | GiB | % |
|---|---:|---:|---:|
| (a) git-tracked | 14,744,042,190 | 13.73 | **44.4%** |
| (b) untracked tape | 6,735,741,620 | 6.27 | 20.3% |
| (c) regenerable | 10,937,349,153 | 10.19 | 32.9% |
| (d) unknown | 784,345,268 | 0.73 | 2.4% |

**Only 44% of the worktree is in git.** Method: one bounded `os.walk`
(573,759 files, 237 s) cross-referenced against `git ls-files -z`. No unbounded
du/find — which is why it finished where my attempts timed out.

## THE FINDING THAT REORDERS EVERYTHING: `watch/` is mostly media, not tape

I have been calling `watch/` the durable receipt surface. Measured, it is not:

```
watch/ total            6.2 GB
  of which TRACKED      4,440 MB
    mrpool_export/media_full/   3.4 GB  of committed .mp4
    qdrop_export/media_full/     585 MB  of committed .png
  receipts (.md)          ~19 MB
```

**~19 MB of receipts riding on 4.4 GB of committed media.** The "receipts or
it didn't happen" law has a 233:1 media-to-receipt ratio in its own directory.
That reframes the earlier "watch/ 7.1 GB" figure: the size was never about the
tape.

## Top 10 files — 9 of 20 largest are TRACKED (7.5 GB)

| # | size | tracked? | path |
|---|---|---|---|
| 1 | 2,357.8 MB | **Y** | `attic/20260923_mimosa_rotation/hook-state_stale_baselines.tar` |
| 2 | 2,241.9 MB | **Y** | `dashboard/data/ractor_board.jsonl.runaway-evidence-20260903` |
| 3 | 1,706.5 MB | n | `watch/inbox/ESSENTIALS_PACK_20260926.tar.gz.enc` |
| 4 | 1,244.1 MB | n | `memory/ingest/registry.jsonl` |
| 5 | 912.5 MB | n | `logs/kpi.jsonl` |
| 6 | 713.3 MB | **Y** | `dashboard/data/ractor_board.jsonl` |
| 7 | 590.2 MB | **Y** | `watch/ESTATE_INDEX/ESTATE_INDEX.jsonl` |
| 8 | 590.2 MB | **Y** | `dashboard/data/ESTATE_INDEX.jsonl` — byte-dup of #7 |
| 9 | 353.9 MB | n | `memory/runs/ghost/trail.jsonl` |
| 10 | 307.0 MB | n | `corpus/oral_history/.../rollout-2026-08-30-…jsonl` |

**A second byte-duplicate pair, sha256-confirmed:**
`training/events.jsonl` (tracked, 247 MB) ≡ `memory/training/events.jsonl`
(untracked, 247 MB). So the 590 MB ESTATE_INDEX pair was not a one-off.

**No log rotation exists anywhere** — grep for `RotatingFileHandler`,
`maxBytes=`, `logrotate` across `mag/ dashboard/ scripts/` returns nothing.
68 days retained unbounded: `logs/` 1.54 GiB + `watch/*.log` 414 MB.

## The reclaim decision splits in two — and this matters

**~19 GB is reclaimable, but not by the same action:**

- **Delete-only, immediate, no history rewrite:** `.mimosa` 15.7 GiB (the
  204× snapshot cache), `mine/raw/` 2.92 GiB (vendored public clones with their
  own `.git` dirs), log capping.
- **Requires history rewrite:** the 2.24 GB runaway snapshot, 4.0 GB tracked
  media, the 590 MB dup ledger, the attic tars. **These blobs already sit in
  `.git`'s 6.11 GiB of packs — `git rm --cached` alone frees nothing.** Anyone
  told "just untrack it" is being told something that won't work.

## `dashboard/` is generated — and the copies multiply

`dashboard/*.py` is source. `dashboard/static/` is **generated** (ships its own
generators, deterministic seed 1197, 110 generated `.html`). `dashboard/data/`
is 3.4 GiB of generated JSONL, all tracked. **`dashboard-deploy/static/` is a
375-of-376-file byte-copy.** (`site/` is a separate project, not a third copy.)

## The push-gate list, finally enumerated — 9 gates, 2 block

| # | line | gate | mode | rc | blocks |
|---|---|---|---|---|---|
| 1 | :10 | `violation_ratchet check --changed` | ENFORCING | **1** | **YES** |
| 2 | :12 | `config_seal verify` | ENFORCING | **1** | **YES** |
| 3 | :21 | `description_pin` | `\|\| true` | 0 | no |
| 4 | :49 | `freshness_gate` | `\|\| true` | 0 | no |
| 5 | :88 | `census_drift_patrol` | exit 2 blocks, **exit 1 warns** | 0 | not now |
| 6 | :113 | `checkbox_receipt_gate` | `\|\| true` | **1** | no |
| 7 | :157 | `caption_ledger_verify` | `\|\| true` | 0 | no |
| 8 | :225 | `refold_gate` | `\|\| true` | **1** | no |
| 9 | :296 | `workflow_gate --scenarios` | conditional | 0 | no |

**Gates 1 and 2 are the complete set of hard blocks.** A push dies at :10;
2–9 never execute. **Four gates are red right now and three of them are
non-blocking** — including the census gate, whose exit-1 (the exact
`+384` STALE state) is WARN-ONLY by design.

**`checkbox_receipt_gate`'s `|| true` is deliberate**, justified in-hook at
:108-111 with an explicit operator-deferral note. Not a bug. The same rationale
covers all 7 non-blocking sites.

**Two real fail-open edges:** the census block tests only `-eq 2`, so a missing
venv turns the blind detector into a silent warn; and `prepush_paths_changed.py`
returns 2 on git failure while the caption block tests only `-eq 1` → false
all-clear.

## A correction to my own report — the ratchet fingerprint moved

I reported `tools/visor.py:131`. It is now **`tools/visor.py:250`**. The file's
mtime is 21:57:48 — a sibling lane edited it mid-audit and the fingerprint moved
:131 → :249 → :250. **Implication: the baseline stores `accepted_lines`, so a
concurrent edit invalidates any acceptance.** Re-run `check` before accepting
debt by name.

## The rib compiler: the "0 ribs" figure is a lie of age

`trajectory_rib.py` projects trajectory JSONL into portable ribs, accepting a
row only if its `metadata` claims the exact byte range it occupies **and** its
`bodySha256` matches. The 28 rejected rows are OpenClaw compaction counters with
no `metadata` — **they cannot pass a provenance gate and shouldn't. The gate is
correct.**

But the receipt is from 2026-09-02 against a 28-line tape hashing `40fffe33`.
The live tape is **30 lines, `ccde6556`** — run to a temp path it compiles **2
ribs**. The two passing rows were appended after the compiler last ran. And they
are **empty** (`anchors: 0`, `text_len: 0`, `acceptance: unproven`): the gate
verifies provenance and never checks content.

`"metricGate": "not_run"` at line 169 is a **dict literal**, and repo-wide grep
finds that one line only. `"ok": True` is also hard-set and `main.py:2776`
returns `0` — **the exit code is a constant, so a green run carries zero
information.**

The input is severed: the bounded-row writer lives in the retired OpenClaw
deploy (port 8787 refuses connections), so the tape can never grow again.

## Scheduled tasks: 23 fleet tasks, and the honest scoreboard

- **14 firing clean** (result 0, real timestamps)
- **2 failing by design** — `Estate Ratchet` (`seal=1 ratchet=1`, refuses to
  auto-re-seal: the operator's name is the point) and `MagImproveDaily`
  (exited 1 on a *declared* trust abstention)
- **5 never fired** (`267011`) — MagSecretScanWeekly, MagCorpusRescanDaily,
  MagQCaptionVerifyDaily, MagArmC200, MagMimoWatchClose
- **2 disabled, 56 days stale** — MagLabKit8765, MagPrivateOffice8765, which
  contradict the "no scheduled tasks" law by existing

**`MagSecretScanWeekly` has never run once.** A weekly secret scanner that
exists in the task scheduler and has never fired is a gate that does not exist.

## Refold pins are a Windows artifact, not a break

The 4 red `refold_gate` pins assert a bare filename; the host prints a full
`C:\…` path. **They would pass on POSIX.** Fix the pins at
`tests/test_index_fold_host.py:497` — and note the gate's own "revert or fix the
comparator edit" message points the operator the *wrong* way, toward editing
`index_fold_host.mjs`, which is correct code.

## Ranked operator decisions, cheapest first

1. **`config_seal update --by WHO --note WHY`** — one decision, no code
   judgment. 5 modified are uncommitted edits; 4 unsealed are untracked files
   never sealed. Clears blocker 2 outright.
2. **`violation_ratchet`** — 6 named acceptances, **re-run `check` first** (the
   `visor.py` fingerprint moved).
3. Decide on `.mimosa` (15.7 GiB) and log capping — pure delete, no history.
4. Decide on `mine/raw/` (2.92 GiB) — re-clonable vendored clones.
5. History-rewrite decisions are separate and larger: 2.24 GB runaway, 4.0 GB
   media, 590 MB dup ledger, attic tars. `git rm --cached` frees nothing.
6. Add an off-host remote — everything rests on one disk.
7. `MagSecretScanWeekly` has never fired.

## Audit accounting — my errors, all corrected

| my claim | correction |
|---|---|
| xAI key "refuted" | **wrong** — real, committed in `steps.jsonl` |
| 18,733 private files | **wrong** — real surface is 225 |
| 80 dead tools | **80 − 1** — `roblox_npc_gateway.py` is a false DEAD (HTTP server, caller is Lua) |
| census 2,288 | **2,294** — moved mid-audit; drift is +384 |
| `visor.py:131` | **`:250`** — file edited mid-audit |
| worktree size "not measured" | **closed** — 54.12 GiB total |
| "hook wiring is correct" | **fails anyway** — 3 of 9 gates red and non-blocking |
