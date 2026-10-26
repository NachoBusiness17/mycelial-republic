# Repo integrity + the 20 GB that was making everything stutter (2026-10-24)

**Trigger:** the background key-shape sweep returned `9` hits in tracked `memory/` and
`watch/`, and a `git grep` aborted mid-run with
`packed object 79dc1113… is corrupt`. Both were real findings.

## 1. Key-shaped strings: 9 hits, **0 live**

Method: every match was extracted, hashed (SHA-256), and compared against **67 live
values** parsed from `.env` and `Hermes/.env`, plus the gate's own substring rule.
Values were never printed — only `prefix…last4`, length, and a boolean.

| file | token shape | live |
|---|---|---|
| `memory/corpus/game_design_docs/koster_laws_of_online_world_design.html` | `AKIAIX…EISQ` 20 | no |
| `memory/corpus/shadertoy21k/…/3djSDD.fragment`, `MsfcRS`, `stf3zs` | `sk-14b…4d07` 35 | no |
| `watch/inbox/SECRET_GATE_BUILD_20260927.md` | `xai-RE…78ab` 33 | no |
| `watch/inbox/audit_20260926/GATE_DEFECT_ASSIGNMENT_BYPASS_20260927.md` | `xai-Kp…vY2w` 59 | no |
| `watch/inbox/burn_reset_20260927/flash50/deep-trust-game.md` | `xai-ab…9jkl` 25 | no |
| `watch/inbox/burn_wave_20260926/B2_73_secret_scan.py` | `AKIAIO…MPLE` 20 | no (literally EXAMPLE) |
| `watch/inbox/burn_wave_20260926/B2_88_crawl_map.json` | `sk-EGK…3VOD` 39 | no |

Conclusion: documentation placeholders, scanner pattern literals, and coincidental
shader strings. The gate is doing its job; the tracked tape has no live credential.

## 2. The object store was the stutter

`git gc --auto` had been spawning repacks against a **4.6 GB text file** and dying,
each death leaving a partial pack. Measured before the fix:

| fact | value |
|---|---|
| packs | 18 |
| pack size | **17.49 GiB** |
| loose objects | 53,071 = **4.43 GiB** |
| garbage | **6.60 GiB** (25 `tmp_pack_*` = abandoned repacks) |
| corrupt pack | `pack-24ddd365…` (727 MB) — `inflate returned -5` at offset 12 |
| objects in corrupt pack | **1** — `79dc1113…` |
| that object's path | `watch/inbox/lite_leak_audit_20261023/pc_repo_list.txt` (**4.6 GB on disk**) |
| reachable? | **yes** (HEAD tree) |

Ten further packs held exactly **one object each** (37–505 MB) — more aborted repacks
of single giant blobs. That is why commits took minutes to tens of minutes: every
sweep touched the object store, and every gc attempt restarted the thrash.

## 3. The data lake: 64 tracked blobs ≥ 32 MB = 14.9 GB

```
2523MB dashboard/data/ESTATE_INDEX.jsonl.retired-20261006
2318MB attic/20260923_mimosa_rotation/hook-state_stale_baselines.tar
2233MB dashboard/data/ractor_board.jsonl.runaway-evidence-20260903
 768MB watch/ESTATE_INDEX/ESTATE_INDEX.jsonl
 710MB dashboard/data/ractor_board.jsonl
 648MB catalog/catalog.jsonl
 525MB catalog/tags.jsonl
 506MB dashboard/static/index_data/ESTATE_INDEX.jsonl
 398MB training/events.jsonl
 268MB artifacts/vertigo_boat_20260908/tokyo_river_depth_1080p.mp4
 … 54 more
```

A public repo carrying 15 GB of regenerable output is not a repo; it is a slow
object store with a git interface.

## 4. Fixes applied

1. **`gc.auto=0`, `gc.autoPackLimit=0`** — no more background repacks while the
   store is in this state.
2. **Deleted 25 `tmp_pack_*`** — 6.7 GB of git-classified garbage.
3. **Untracked all 64 blobs ≥ 32 MB** (`git rm --cached`, files kept on disk),
   ignored them by exact path. Commit `932f4d1f1`. Nothing local broke: the
   console reads them from disk, not from git.
4. **Large-blob gate** in `tools/precommit_secret_check.py` — any staged file over
   `MAG_MAX_BLOB_MB` (default 32) is refused with its size and path. This is the
   prevention; without it the lake refills.
5. **`SKIP_AREAS`** in the sweeper (Temp/tmp/node_modules/.venv) — earlier today,
   after `git add -A -- Temp/` (7 GB, 6 tracked blobs) wedged a sweep for 36 min.
6. **Corrupt object: quarantined, not repaired.** The working file hashes to
   exactly `79dc1113…`, so the bytes are intact. `git hash-object -w` prints the
   right SHA but writes nothing — git's existence check consults the (corrupt)
   pack index and concludes the object is already there, and with the pack
   removed the 4.6 GB blob crosses the streaming threshold into a `tmp_pack_*`
   that never lands. The corrupt pack is therefore moved to
   `.git/pack_quarantine/` (727 MB, outside the object dir) rather than deleted:
   it is the forensic artifact, and the only thing that still holds the old
   history's blob. Deleting it is safe for daily work (the path is untracked at
   HEAD) but makes older commits un-cloneable, which they effectively already are.

## 5. What still has to be decided (history)

Untracking changed HEAD, not history: the 15 GB of blobs remain in old commits, so
`.git` stays ~20 GB and a full `git gc` cannot complete (it must read the corrupt
pack's object, now restorable, but also repack 17 GB of data-lake blobs).

Reclaiming the space needs a history rewrite:

```
git filter-repo --strip-blobs-bigger-than 32M   # rewrites every SHA
```

Consequences, stated plainly: all commit ids change, every clone must re-clone, and
the public remote must be force-pushed (or the repo recreated). That is an operator
decision, not a seat decision. The cheap alternative is to leave history as-is:
with `gc.auto=0` and the gate in place, the store stops growing and stops thrashing,
and the 20 GB just sits there.

## 6. Numbers after

- `git status`: **10.5 s** (was wedging for minutes during repacks)
- sweep: commits land again; no `tmp_pack_*` regeneration while `gc.auto=0`
- `.git` on disk: ~20 GB until the history decision; **6.7 GB freed** already
- live credentials in tracked tape: **0**
