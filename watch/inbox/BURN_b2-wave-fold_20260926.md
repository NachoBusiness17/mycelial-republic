# BURN b2-wave-fold 2026-09-26

## Verdict

steal

## Evidence

- memory/burns/LEDGER.jsonl: 178 rows total, 114 B2-* rows, all timestamped 2026-09-26.
- Row 66 (b2-13): "check --scenarios landed read-only in tools/workflow_gate.py ... tests 7/7 in tests/test_workflow_gate.py".
- Row 78 (b2-28): "watch/inbox/EVENTS.jsonl minted as the canonical event ledger (schema event.v1), 51 rows".
- Row 43 (steering-theory): "runner EXECUTED: tools/probe20_run.py live-verified importing tools/drift.py".
- Row 90 (b2-53 correction): "self-feeds first claimed B2-125/126/127 against a stale census (true highest was B2-132) and collided again mid-flight".
- Row 177 (B2-279 erratum): "a concurrent B2-280 lane had CLAIMED scripts/index_fold_host.mjs ... and was writing the shared file through the window".

## Steal or Vacuous

Inventory (114 B2 rows): 103 landed or verified builds, 5 corrections, 5 erratums, 1 hold (B2-59 MIPROv2 dig).

Verification, all three hold:
1. tools/workflow_gate.py runs: check --script tools/probe20_run.py exits 2 with six FAIL + one WARN, all genuine detections (probe20 is a linear runner with no fan-out or report salvage), so the gate bites rather than rubber-stamps.
2. watch/inbox/EVENTS.jsonl: valid JSONL, 51 rows, 0 malformed. First row ALERT-NVIDIA-PURGE (event.v1, origin provenance); last ts 2026-09-26T11:53:49Z.
3. tools/probe20_run.py --demo: exit 0. Demo2 shows the raw INVERTED corr -0.5748 overridden to INSUFFICIENT by the 0.1 net-movement noise floor: the one-flip escape is blocked in the shipped bytes.

Regression pattern: 10 same-hour self-corrections (5 corrections + 5 erratums, each 1 to 18 minutes after the parent row). 7 of 10 are self-feed queue-number collisions under concurrent lanes (b2-35, b2-53, B2-50, B2-70, B2-72, B2-256, B2-246): a check-then-append race on QUEUE.md, the known proposal-slot collision genus at fleet scale. Substantive receipts held every time ("config surgery and receipt untouched", "triage work itself unchanged"). Two fresh species: B2-279 interleaved writes to a shared file produced a transient wrong census (2087 events vs 561) at receipt registration, and B2-247 appended the ledger while the QUEUE card still read [ ] on disk.

Adopt: (a) manifest pointers: steering-theory += tools/probe20_run.py and watch/inbox/PROBE20_steering_v1.jsonl; queue-field += watch/inbox/EVENTS.jsonl; judge-lane-spec += watch/inbox/burn_wave_20260926/B2_08_judge_lane_20260926.md. (b) self_steal_fold gains the concurrent-claim law: claims take highest+1 at append time, and every ledger append is followed by a disk-state truth check.

Act: fire the b2-53 Grok 4.7 packet card (fire-ready, seat unfired); arm the b2-54 cron card; chase B2-24's missing window 21/22 rubric scoring receipt; b2-30 ShadowLedger live proof; B2-59 stays held pending F1.

## Falsifier

ADOPT-1 (concurrent-claim law): if the next 50 B2 ledger rows contain more than 2 self-feed renumber corrections or erratums, the convention failed and the claim protocol needs a real lock (single-writer QUEUE.md), not a convention.

## Bibliography

memory/burns/LEDGER.jsonl; memory/burns/MANIFEST.json; watch/inbox/EVENTS.jsonl; tools/probe20_run.py (read and executed); tools/workflow_gate.py (executed, not read).
