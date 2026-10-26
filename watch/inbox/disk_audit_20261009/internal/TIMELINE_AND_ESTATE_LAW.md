# TIMELINE_AND_ESTATE_LAW - Lane B: internal timeline + estate prior-art (disk-storm audit 2026-10-09)

Sources: state/DISK_CRISIS_20261008_CLOSE.md (CLOSE), watch/inbox/DISK_INVENTORY_20261008.md (INV), memory/zknot/LATEST.md (ZK), git 0b9980351 / cd118ed70 / 72caa1a3a, configs/longrunner_policy.json (POLICY), tools/*.py. All quantities cite their file; growth-rate claims not yet byte-backed are marked UNVERIFIED (Phase 0 harvester adjudicates).

## Timeline

Preconditions (silent growth window, before 10-08):

| When | What | Citation |
|---|---|---|
| Sep 13 | ollama blob ling-3.0-flash 71.7GB lands in garden | INV:30, INV:45 |
| Sep 16 | ling-3.0-flash last used (3 weeks cold by crisis) | INV:45 |
| Sep 22 | athena-class blob 30.4GB lands | INV:30 |
| Sep-Oct | .zcode/cli/exec grows to 310GB: one stdout log per tool call, no rotation, across every seat and every 100M-token burn | CLOSE:11, 72caa1a3a |
| continuous | system-managed pagefile balloons to 132.9GB under fleet memory pressure | INV:86, CLOSE:14 |
| continuous | docker_data.vhdx reaches 132GB, ~90GB never-compacted dead space | CLOSE:15, tools/disk_smith.py:8-9 |
| undated | HF cache 66GB dead experiments; no disk instrument exists at all ("no instrument attributing any of it") | CLOSE:18, tools/disk_smith.py:4-10 |
| 09-26 22:22 | AV-fight precedent: "anti malware is fucking us again on hermes give me the exclude" | ZK:203 |

Standing automation writing to the single C: volume during the window (cadence, from zknot session registry): 24x7 free burn churn every 2h (ZK:173), flash-lane burn dispatcher every 20 min (ZK:92), OLM mine daily burn 10:00 (ZK:9), forge daemon 20-min cycle (ZK:257), night shift 23:00/02:00/05:00 (ZK:265), drift patrol 08:00 / estate index 09:00 / Hermes intel 09:15 / free-resource scout 09:00 (ZK:258-264), plus MagFreeLaneFleet / MagHermesBurn247 / MagGauntletFree30 churn tasks (CLOSE:35). Receipt-write volume in the overlapping zknot windows: 7,513 / 9,234 / 9,685 files under watch/inbox (ZK:72, ZK:153, ZK:234). Operator scale setting: "we burn a few billion tokens a day" (ZK:35, 10-07 20:15).

Storm day 2026-10-08 (EDT):

| When | Event | Citation |
|---|---|---|
| 13:32 | Operator surfaces the problem: 5TB cloud idea "to free up whatever the fuck is happening on our drive" | ZK:40 |
| ~14:00 | Inventory begins on operator screenshot: 1.81TB NTFS, 26.8GB free; free falls 26.8 -> 8.0 -> 6.1GB (100%) during the scan | INV:3-4 |
| 13:35 | qwen2.5:7b-instruct-q8_0 blob 7.54GB pulled, author unidentified | INV:13 |
| 16:34 | "the c drive is nearly full whats going on" | ZK:41 |
| 16:37 | Modelfile receipts banked BEFORE any deletion (4 files) | ZK:248-249, INV:66 |
| 16:43 | Commit 0b9980351: relief + tripwire. docker builder prune +14.13GB; ollama rm ling-3.0-flash +77GB; maze-keeper + qwen2.5:32b shared-blob pair +19GB; free 6.1 -> 97GB; patrol disk floor 15GB + 5 tests; athena-class 32GB held | commit 0b9980351, INV:68-73 |
| 16:44 | "why have you added 700gb In days" | ZK:42 |
| 17:02 | "My Si has populated 1.3 terabytes in 36 hours" | ZK:43 |
| 17:24 | Operator orders the smith chart ("we really should have a fucking smith chart of the hdd") | ZK:44, tools/disk_smith.py:4-5 |
| 19:45 | Commit cd118ed70: tools/disk_smith.py + MagDiskSmithDaily 08:50 + 7 tests; first live row (22:59Z) solves the missing 700GB: .zcode = 335.3GB, invisible to the first pass's non-dot globs | commit cd118ed70, INV:81-83 |
| 19:49 | "inherently unsustainable at my current income" | ZK:45 |
| 20:12 | Operator's theory: "balooned to my entire harddrive because there was room... is this alive?" | ZK:46 |
| 20:16 | "we are now fighting my anti malware lets shut everything down and reboot" | ZK:47 |
| 20:21 | Commit 72caa1a3a: close doc + shutdown handoff; churn tasks disabled (fleet/hermes247/gauntlet), dailies left armed; exec-log monster named (.zcode/cli/exec = 310GB); next-window order AV exclusions -> exec purge 7d+ -> re-enable -> docker compact -> fixed pagefile -> HF purge | commit 72caa1a3a, CLOSE:31-38 |

Books at close: 1.75TB used (foste profile ~915GB incl .zcode 335.3 + hermes_local 67.1 + temp 55; system-side ~390GB incl Steam 182 + pagefile/hiberfil 158) (INV:87, CLOSE:7). Free readings across the evening: 97GB post-rotation -> 95GB at close-doc write -> 92.5GB in the first smith row (22:59Z), pagefile still creeping 132.9 -> 135.1GB under load (INV:71, CLOSE:23, INV:81, INV:86).

## Root causes

1. **No-rotation exec exhaust from the burn fleet.** .zcode/cli/exec = 310GB, one stdout log per tool call, written by every seat on every cron and every 100M-token burn, with no expiry anywhere (CLOSE:11, 72caa1a3a, INV:83). The multi-seat 24/7 automation stack above is the write engine; disk was the unbounded sink.
2. **Zero disk instrumentation before 10-08.** No tool measured free space, attributed growth, or alerted: the operator was the tripwire, via OS screenshot at 26.8GB free (INV:3, tools/disk_smith.py:4-10). The first inventory pass also walked non-dot globs only, so the single biggest estate item (.zcode, 335.3GB) stayed invisible until the smith chart's first row (INV:81-83).
3. **Unrotated model garden + caches.** Garden hit 162GB with ling-3.0-flash 77GB three weeks cold and athena/maze-keeper/qwen2.5:32b at zero usage rows (INV:41-50); HF cache 66GB dead experiments (CLOSE:18). usage evidence (logs/usage.jsonl) existed but nothing polled it (INV:43-48).
4. **System monsters with no compaction path.** System-managed pagefile ballooned to 135GB under five-seat memory pressure (only a reboot returns it); docker_data.vhdx held ~90GB never-compacted dead space after prunes (CLOSE:14-15, INV:86).
5. **AV real-time scanner versus the fleet's file churn.** Five seats writing thousands of files/min into a live scanner = the IO storm fought during the scan and reboot (CLOSE:33, ZK:47); precedent already on record 09-26 (ZK:203).
6. **Everything shared one volume with no offsite.** Single local volume, no second drive, no offsite copy of anything at 100% full (INV:52-54).

## Estate law already held

| Law | Where | What it already rules | Gap it leaves for this storm |
|---|---|---|---|
| Cache-vs-durable boundary | watch/inbox/SHARED_SURFACE_CONTRACT.json laws[] | Client-local session dirs (.zcode class) are cache only, never the sole copy of durable work; classify before reuse | Declares the class but sets no lifecycle: no expiry, quota, or purge path, so 335GB of "cache" accumulated legally (INV:83) |
| Never bulk-delete under live seats (stash-sweep class) | tools/stash_sweep_watch.py:2-23; founding watch/inbox/ouroboros_20261005/r3_land_teeth.md:92-105; DAWN_REPORT_20261006.md:117-118; applied to exec purge in CLOSE:34 | A sweep may carry an unlanded lane's only copy; HOLD-RECONCILE, never drop; the patrol "never kills" for the same reason (tools/longrunner_patrol.py:16) | Watcher covers git stash refs only; no live-seat gate exists for filesystem cache purges - the exec purge must import the class by hand ("NEVER while seats mid-flight", CLOSE:34) |
| Ollama rotation with modelfile receipts | watch/inbox/model_modelfiles_20261008/ (4 files); POLICY reversible_relief_playbook; INV:66-73 | Rotation is reversible: bank the modelfile BEFORE ollama rm; unreconstructible FROM-blobs (athena-class, local blob, no registry) held for operator ruling | Reactive, crisis-minted: no scheduled cold-model eviction polling logs/usage.jsonl; the garden reached 162GB before anyone looked |
| Disk-free floor tripwire 15GB | POLICY disk_free_floor_gb; tools/longrunner_patrol.py disk_floor_rows(); tests/test_longrunner_patrol_disk.py; INV:75 | Patrol exit 1 + memory/attention.md alert below 15GB, with a reversible relief playbook embedded in policy | Daily 08:45 cadence, detect-only: a 36h storm completes long before morning; no attribution of who wrote the bytes |
| Smith chart | tools/disk_smith.py; MagDiskSmithDaily 08:50; thresholds free<15GB / vhdx>100GB / pagefile>40GB (tools/disk_smith.py:69-72); INV:91-92 | Daily monsters/seats/estate/free snap to logs/disk_smith.jsonl with deltas and alerts | Measures but never rotates (alert text only names the relief playbook); daily cadence; first row 10-08 22:59Z so no growth curve exists yet to delta against |
| Longrunners-caged | POLICY tiers + founding incident run_armC (11-day runaway) | Processes that outlive a sitting run in capped compose services; bare-host long-runners are violations | Caps CPU/mem/time but has no disk-write dimension: a process can write unbounded GB and stay compliant |
| Reversible-shed / retention patterns (nearest held) | tools/enqueue_law.py:27-28,203-216 (prune writes a COPY, original never touched, epitaphs to a graveyard); SUPERSEDED.md (amend-never-rewrite demotion) | Retirement of dead ledger rows is evidence-preserving and reversible by construction | No general log-rotation law: logs/mates 9.6GB stayed uncompressed only because five live tools read it (INV:77); exec logs had zero lifecycle until the crisis named a 7d purge (CLOSE:34) |
| "ReFold sheds" (as named in WAVE_PLAN Phase 1) | Not found as a banked law | grep over repo prose/tools finds "refold" only as a verb for re-running INDEX fold scripts (corpus/steal/MASTER_MICKEY17_V2.md:221), unrelated | OPEN: the wave-plan name has no prior instrument; the modelfile-receipt rotation and prune-to-copy rows above are the actual held equivalents - fold into RIB_DISK_BUDGET (Phase 4) rather than re-invent |

## Open questions

1. Growth-rate claims "700GB in days" / "1.3TB in 36h" (ZK:42-43) are UNVERIFIED: the smith ledger holds one row; the estate's own measured week-of-downloads was ~1.8GB (INV:6-15) against months of accumulation (INV:15). Phase 0's age histogram + daily growth curve from mtimes adjudicates.
2. Repo size discrepancy: 297GB by projects du vs ~78GB direct walk + 17GB .git, hardlink double-count suspected (CLOSE:13, CLOSE:39).
3. Active-writer incident: the ~20GB free drop during the scan (26.8 -> 6.1GB) is only partly explained (qwen pull 7.54GB + suspected pagefile growth); process IO counters read ~0 from an unelevated shell, remainder unidentified (INV:37-39).
4. Who pulled qwen2.5:7b-instruct-q8_0 at 13:35, 8.1GB, no usage rows (INV:13).
5. athena-class 32GB: local FROM-blob, no known registry source; deletion may be unreconstructible - operator ruling owed (INV:73).
6. .zcode composition beyond exec: 335.3GB total vs 310GB exec leaves ~25GB of transcripts/plugin caches not itemized (INV:83 vs CLOSE:11).
7. No instrument maps exec-log files to live vs closed sessions yet - the 7d purge needs that map to honor the stash-sweep class (CLOSE:34).
8. Fixed-size pagefile 32-48GB (admin) not yet executed, so the balloon class can recur at the next memory-pressure event (CLOSE:37).

Lane B close. Quantities above are byte-cited or marked UNVERIFIED; no disk walks were performed for this lane.
