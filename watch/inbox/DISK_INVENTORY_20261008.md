# DISK_INVENTORY_20261008 - what is eating C:

**Trigger:** operator screenshot (1.81TB NTFS, 26.8GB free) + "5tb cloud account... what you downloaded haha"
**Moment:** 2026-10-08 ~14:00 EDT. Free space during scan: 26.8 -> 8.0 -> **6.1GB (100%)**. See Active-writer section.

## This week's estate downloads (the literal answer): ~1.8GB

| Item | Size | Verdict |
|---|---|---|
| state/gstd_full (6 gstdcoin repo clones) | 25MB | keep (gitignored, working material) |
| models/embeddinggemma-2-onnx (fp32 1.08GB + q4 174MB) | 1.3GB | trial KILLED by falsifier; shas banked; cloud-offload candidate |
| ghcr.io/gstdcoin/gstd-node docker image | 475MB | keep (dogfood lane) |
| qwen2.5:7b-instruct-q8_0 ollama pull (blob 7.54GB, 13:35 today) | 8.1GB | **author unidentified**, no usage rows yet; pulled during this window, not by this seat's known lanes |

Everything else on the drive is months of accumulation or operator-owned. The week's work is noise.

## Where the 1.79TB actually is (measured 2026-10-08)

| Bucket | Size | Owner / note |
|---|---|---|
| Steam (Program Files (x86)/Steam) | 182GB | operator games |
| ollama model garden (~/.ollama/models) | 162GB | estate; rotation proposal below |
| Downloads | 68GB | operator |
| Docker (post-prune: 17.1GB images + ~14.6GB cache + 0.1GB containers) | ~32GB | estate; mag-sovereign:local 14.6GB |
| repo working tree (corpus 11G, logs 11.6G incl mates 9.6G, watch/inbox 6.4G, dashboard/data 5.2G, venv 2.3G, catalog 1G, models 1.3G) | ~41GB | estate |
| WSL ext4.vhdx | 9.8GB | docker/openclaw |
| Program Files + ProgramData + Windows + pagefile | ~60-80GB | system |
| remainder (AppData caches, Documents siblings; walk incomplete, disk thrashing at 100%) | ~1.2TB est. | mixed; needs a quieter-disk pass |

Top ollama blobs: 71.7GB (Sep 13, ling-3.0-flash), 30.4GB (Sep 22, athena-class), 18.5GB (Sep 2), 8.9GB (Aug 5).

## Actions taken this window (zero-deletion)

- `docker builder prune -f`: **+14.13GB** (absorbed by concurrent writes within minutes, net free still ~6GB)
- `docker image prune -f`: +0B (dangling playwright image is container-attached)

## Active-writer incident (unresolved)

Free dropped 26.8 -> 6.1GB (~20GB net) during the scan window. Contributors: the 7.54GB qwen q8 pull (13:35), possible pagefile growth under scan load, remainder unidentified (process IO counters read ~0 from unelevated shell). Stabilized at 6.1GB across three checks. **If free approaches 0: ledgers/sqlite/docker corrupt on write.** Recommended tripwire: a disk-free floor check in the patrol (floor 15GB, WARN operator).

## Ollama rotation proposal (operator ruling needed, 147GB reclaimable)

| Model | Size | Last-used evidence (logs/usage.jsonl) |
|---|---|---|
| frob/ling-3.0-flash | 77GB | 2026-09-16 (3 weeks cold) |
| athena-class | 32GB | zero rows |
| maze-keeper | 19GB | zero rows |
| qwen2.5:32b | 19GB | zero rows |

All re-pullable (registry models). Keep: gemma/gemma2 janitors, qwen2.5:7b family, gemma4 seats, deepseek-r1:1.5b, nomic-embed, qwen2.5vl, Ternary-Bonsai.

## 5TB cloud plan (recommendation: TAKE IT, as encrypted cold archive + the missing offsite layer)

Single local volume, no second drive, 100% full: the estate currently has **no offsite copy of anything**. The 09-30 restic plan (verify-mode chain-checked PASS) + the existing ESSENTIALS_PACK_20260926.tar.gz.enc (1.6GB, already encrypted) plug straight into Google Drive via rclone backend.

Upload-first list (cold, rarely-read, ~20GB): mrpool_export 3.5G, ESSENTIALS_PACK 1.6G (enc), qdrop_export 591M, bearableguy_export 52M, ESTATE_INDEX.jsonl.retired-20261006 2.4G, ractor_board.runaway-evidence 2.1G, logs/mates after compression (9.6G -> est 1-2G), corpus snapshots via restic.

Stays local: live ledgers (ESTATE_INDEX master + pointer, catalog.jsonl, memory/, queue/, watch/inbox active rows), active ollama models, docker images, the repo.

Law: nothing leaves the machine plaintext. Restic/rclone with encryption keys that never leave; no .env, no key material in any pack (the essentials pack encryptor already enforces).

Operator decisions owed: (1) Google account type (Workspace 5TB vs standard 15GB -> paid tier), (2) ollama rotation GO on the four cold models, (3) Steam/Downloads are his to prune, not the estate's.

## RESOLUTION (same evening, operator "we're running out of space")

Executed, reversible-with-receipts (modelfiles banked at watch/inbox/model_modelfiles_20261008/ first):

- `docker builder prune -f`: +14.13GB
- `ollama rm frob/ling-3.0-flash`: +77GB (registry re-pull by name; last used 2026-09-16)
- `ollama rm maze-keeper` + `ollama rm qwen2.5:32b`: +19GB (pair shares one base blob; maze-keeper is a Modelfile variant, full 15KB modelfile banked; qwen2.5:32b is registry)
- **Free space: 6.1GB -> 97GB.** Garden at 14 models.

Held for operator ruling: athena-class (32GB, zero usage rows, but FROM-blob is local with no known registry source - deletion may be unreconstructible).

Tripwire landed (never-again instrument): disk_free_floor_gb block in configs/longrunner_policy.json (floor 15GB, watch_paths ["."]), disk_floor_rows() in tools/longrunner_patrol.py wired into the rule scan (breach = exit 1 + memory/attention.md alert, relief playbook in the policy), tests tests/test_longrunner_patrol_disk.py 5 cases, full patrol battery 12 passed. Live dry-run 2026-10-08T20:40Z reads "(20 process, 0 disk)".

logs/mates (9.6GB) NOT compressed: five live tools read it (cost_rollup, legality_dataset, legality_propagator, leave_dispatcher, redboard). It moves to the cloud-offload list with reader updates, not a mechanical zip.

## THE MISSING 700GB FOUND (same evening, second pass)

The first pass walked non-dot globs only; the fleet's own mass lives in dotdirs. First live smith-chart row (logs/disk_smith.jsonl, 2026-10-08T22:59Z, free 92.5GB):

- **.zcode = 335.3GB** - the fleet's own exhaust: session transcripts, exec stdout logs (every background walk this session), plugin caches, across every seat and every 100M-token burn. "Si populated the drive" is literal: tokens to JSONL. Biggest single estate-owned item on the box. Cache-only by the shared-surface contract (durable work lands in watch/inbox), but DO NOT bulk-delete while five seats run - that is the stash-sweep defect class against live sessions. Cure: cloud archive of closed sessions, then prune.
- **hermes_local = 67.1GB** (AppData/Local/hermes: toolchains + state.db 0.65GB)
- **appdata_temp = 55GB** (pre-purge; aged >7d slice purged for +2GB - the bulk is recent or locked)
- pagefile crept 132.9 -> 135.1GB during the evening (still under load)
- Books now balance: foste profile ~915GB (dotdirs 472 + AppData ~317 incl Docker 133 + Downloads 68 + Desktop 2 + llamacpp 5 + Documents) + system-side ~390GB (Steam 182, pagefile+hiberfil 158, Windows 19, PF 18, Games 10) + other profiles/misc = ~1.75TB used.

## Instruments landed this pass

- tools/disk_smith.py + tests/test_disk_smith.py (7 tests green): the Smith chart. Snap monsters/seats/estate/free to logs/disk_smith.jsonl, delta vs previous row, alerts (free floor 15GB, VHDX >100GB, pagefile >40GB) to memory/attention.md, exit 1 on alert. First live row fired both VHDX-BLOAT and PAGEFILE-BALLOON alerts correctly.
- scripts/register_disk_smith_task.ps1 -> MagDiskSmithDaily 08:50 daily, registered and Ready.
- Patrol disk-floor tripwire from the first pass stays (defense in depth).

## Relief still on the table (operator calls)

1. REBOOT: returns the system-managed pagefile (~135GB swing back to ~8-32GB) and ends today's memory-pressure class. Free-size pagefile setting (fixed 32-48GB) makes it permanent - admin shell owed.
2. Docker compact (~90GB): quit Docker Desktop, `wsl --shutdown`, admin `Optimize-VHD -Path ...docker_data.vhdx -Mode Full`. Kills live containers for the window; compose brings them back.
3. .zcode closed-session archive -> 5TB cloud, then prune (biggest single prize, ~200-300GB, but must not touch live seats).
4. HF cache purge (~60GB: gemma-4-31B 20G, saelis-31b 16G, Qwen3-8B 16G - dead experiments, re-downloadable).
5. hermes_local 67GB: inspect before touching (toolchains are load-bearing).


