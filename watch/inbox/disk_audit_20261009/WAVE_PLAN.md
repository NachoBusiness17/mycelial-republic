# WAVE PLAN - disk-storm audit + ponytail cleanup (Lessig) - 2026-10-09

**Operator orders (this window, verbatim intent):** "go wave protocol on that wide" / "plan this out to make it go fast" / "clean everything ponytail lessig style after an audit of what happened, what was in that data, what can we learn, how do we avoid it, how do others handle it" / "wide i just dont want a 13 hour window that takes over the pc".

## The bound (hard, whole wave)

1. **ONE disk-bound process at a time.** No lane may walk the disk. The only local walks are the single harvester (Phase 0) and the cleanup ops themselves (Phase 3). The AV fight is fresh; a fan-out of walks re-creates the IO storm.
2. **Analysis lanes are remote-model only** - they eat a compact evidence pack (KBs to MBs), never live trees.
3. **Wall clock target: 4h or less to operator checkpoint, 2h or less cleanup after GO.** No overnight loops, no new dailies.
4. Destructive steps sit **behind the operator GO** (audit-first, per his own sequencing). Admin-elevated steps stay flagged for him (AV exclusions, Optimize-VHD, fixed pagefile).

## Phase 0 - serial harvest (disk-bound, one process, ~30-60 min)

`harvest_exec_forest.py` (receipt-space, NOT a repo tool): metadata-only walk (scandir/stat, no hashing, no bulk content reads) of `.zcode/cli/exec` producing `evidence_pack/`:

- age histogram (<1d / 1-3d / 3-7d / 7-14d / 14-30d / 30d+): count + bytes - sizes the purge prize exactly
- daily growth curve from mtimes - adjudicates the "700GB in days / 1.3TB in 36h" claims with bytes
- per-session top-30 sizes (the WHO), extension histogram, top-60 largest calls
- bounded content sample (~150 files x 2KB): what the data IS (json stdout? errors? binary?)
- secondary top-level tables: `.zcode` non-exec, `hermes_local`, AppData temp, HF model list

## Phase 1 - wave-1 lanes (fire immediately, zero disk impact)

- **Lane A - EXTERNAL PRIOR-ART** (the "how do others handle it" leg): how agent harnesses (Claude Code / Codex CLI / OpenHands / SWE-agent class) handle transcript + tool-call log growth; logrotate/journald SystemMaxUse precedent; WSL2 vhdx compaction practice; cache retention knobs (HF / pip / npm / ollama); fixed-pagefile practice. Cards with sources, STEAL/WATCH verdicts, to `external/`.
- **Lane B - INTERNAL TIMELINE + ESTATE PRIOR-ART** (Descent leg 1): reconstruct the storm causally from banked receipts (DISK_INVENTORY_20261008, DISK_CRISIS close doc, the three crisis commits, zknot prompt trail); list estate laws already touching this class (stash-sweep never-bulk-delete, ollama rotation-with-receipts, ReFold sheds, smith chart), to `internal/`.

## Phase 2 - wave-2 lanes (fire on evidence pack; eat pack + wave-1 outputs)

- **Lane C - CONTENT FORENSICS**: what the exec forest actually is; dupes/rot; the growth curve read; the 36h claim verdict.
- **Lane D - LAW PACK (the Lessig leg)**: code-ready retention/rotation spec - exec 7d expiry wired into the smith daily, prune mode + per-seat quota rows, growth-rate (GB/day) alerting, same-shape law for temp/HF. Spec precedes build per repo discipline.
- **Lane E - CLEAN RUNBOOK**: the ponytail sequence with exact commands, admin steps flagged, safety gates (fleet disabled verified), rollback receipts for everything re-downloadable, before/after smith rows.
- **Lane F - ATTRIBUTION**: join per-session exec sizes vs the zknot session registry - name the top-grower sessions/lanes (who did it, honestly).

## Phase 3 - operator checkpoint, then execute clean

One-page verdict (findings + law pack + runbook) gets **his GO**, then execute in the close-doc order: exec purge (7d+) -> docker compact (admin) -> fixed pagefile 32-48GB (admin) -> HF purge -> re-enable churn tasks (FreeLaneFleet / HermesBurn247 / GauntletFree30). Each step banks a smith before/after row as its receipt.

## Phase 4 - fold

Rib (RIB_DISK_BUDGET class: tokens-are-disk, monsters table, retention law), law code landed + tested, dawn-list line, zknot row.

## Vehicle

Task agents (main-session retry path, proven widths 3-12), width 4 or fewer concurrent, lanes pass off via this shared directory. No CreateWorkflow this wave (no gate subject); interagent pass-off still enforced by construction - wave-2 prompts cite wave-1 outputs.
