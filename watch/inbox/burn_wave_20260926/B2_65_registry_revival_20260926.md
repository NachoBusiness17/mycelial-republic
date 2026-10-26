# B2-65 VERSION_REGISTRY trail revival (2026-09-26)

## Verdict
Landed. The release-gate + release_milestone trail died because its only writers were roadmap passes and manual training-set folds, and neither ran again after 2026-08-10; nothing ever wired them to a scheduler. Revival designed and landed as regime milestones: spec amended first in docs/ref/releases/VERSION_REGISTRY.md, then 3 backfilled milestones filed through the real writer CLI (main.py release record), verified in both trail files.

## Evidence
- mag/release_registry.py:209-258 record_gate appends gates.jsonl then emits release_milestone; its only callers are mag/roadmap_runner.py:278 (roadmap pass), mag/coding_session_loop.py:357 (v3 factory_pilot only), main.py:3038 (manual CLI).
- memory/runs/roadmap/: exactly 2 evidence files, both mtime 2026-08-06 (v5-gstd-t0-probe.json, v5-vast-train-dry.json). The pass never ran again.
- memory/improve/releases/gates.jsonl: 16 rows, all ts 2026-08-05/06.
- memory/training/events.jsonl: 551,607 lines; 18 release_milestone rows; last gate_record 2026-08-06T17:31:19Z; the last 2 milestones (2026-08-09/10) are training_set_build folds (mag/training_set.py:107-120), not gates.
- Fleet kept moving: 468,061 events carry ts 2026-08-10 or later (ts-prefix count); 243 August commits, shifting to backup/wip mega-commits (de29d49ea 2026-08-09 names "training set", the final fold).
- mag/improve.py:1354 only suggests reading release notes; grep over scripts/ and configs/ finds no roadmap-run scheduling. Who stopped: nobody was assigned; the August window-storm pivot moved work into receipt-filing sessions that never call record_gate.

## Work done
1. Read VERSION_REGISTRY.md, configs/releases.yaml, release_registry.py, training_set.py, and both trigger sites whole; byte-verified every date and count above.
2. Spec before behavior: amended docs/ref/releases/VERSION_REGISTRY.md (as-of 2026-09-26) with a Regime milestones section: durable, receipt-filed estate changes; gate_id prefix regime_; recorded against active era v5; writer is the landing session at close; trigger is receipt filing; weekly drift stamp is the staleness tripwire.
3. Backfilled 3 via .venv/Scripts/python.exe main.py release record v5 --gate regime_* --ok --evidence <receipt>: regime_violation_ratchet (landed 2026-09-24, corpus/steal/ZCODE_RATCHET_LANDED_20260924.md), regime_fanout_width_law (landed 2026-09-25, corpus/steal/TETHERED_LINK_STEAL_20260925.md), regime_drift_registry_t1_t6 (landed 2026-09-26, watch/inbox/burn_wave_20260926/B2_05_drift_pairs_20260926.md). Notes carry true landed dates; record ts is today by design.
4. Verified: 3 regime rows in gates.jsonl, 3 matching gate_record release_milestone events in events.jsonl, evidence paths intact.
5. Disclosed: release status counts regime rows into v5 gates_passed (mag/release_registry.py:116-124 reads the log unfiltered); self-feeds filed to split display and arm the tripwire.

## Falsifier
- If the W40 stamp recomputes the T5 referent and the 3 new rows do not register, the emit path is broken, not the design.
- If a regime row accretes whose evidence_path does not exist, the class is gamed: prune it and make receipt-first a hard check.
- If v5 ever flips shipped on regime rows alone (gates_passed math), the regime_ prefix must be excluded from _gates_passed_for (mag/release_registry.py:116-124).

## Bibliography closed
docs/ref/releases/VERSION_REGISTRY.md; configs/releases.yaml; configs/version_roadmap.yaml; mag/release_registry.py; mag/training_set.py; mag/roadmap_runner.py; mag/coding_session_loop.py; mag/improve.py; main.py; memory/improve/releases/gates.jsonl; memory/improve/releases/README.md; memory/training/events.jsonl; memory/runs/roadmap/; memory/burns/LEDGER.jsonl; corpus/steal/ZCODE_RATCHET_LANDED_20260924.md; corpus/steal/TETHERED_LINK_STEAL_20260925.md; watch/inbox/burn_wave_20260926/B2_05_drift_pairs_20260926.md; watch/inbox/burn_wave_20260926/QUEUE.md. All repo bytes read 2026-09-26. No web sources used, none owed.
