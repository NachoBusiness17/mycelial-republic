# INBOX EVENT LOG COMPACTION PLAN (20261021_143954)

- Source: `/mnt/c/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/index_events.jsonl`
- Total Logged Events: **15372**
- Active Retained Items: **8342**
- Redundant / Intermediate Rows: **7030**
- Potential Compaction Ratio: **45.73%**
- State Checkpoint SHA256: `5d6e82c788a0bd414d75d58d9be51a4a6b3ec809bd63d81f91e628655a838091`

## 1. Safety & Invariance Law
- Pure append-only preservation: Raw events 1..15372 are archived into `watch/inbox/_event_archive/epoch1_events.jsonl`.
- Zero unlinks: No data is destroyed.
- A single Genesis Checkpoint event is pinned at the head of the compacted log:
  ```json
  {"op": "checkpoint", "epoch": 1, "prior_event_count": 15372, "active_items": 8342, "state_hash": "5d6e82c788a0bd414d75d58d9be51a4a6b3ec809bd63d81f91e628655a838091"}
  ```
- Replay verified: Replaying active items yields exact SHA256 match `5d6e82c788a0bd414d75d58d9be51a4a6b3ec809bd63d81f91e628655a838091`.

## 2. Operation Breakdown
{
  "register": 9358,
  "note": 14,
  "invalidate": 241,
  "amend": 21,
  "unknown": 87,
  "repair": 1,
  "autoseal": 5644,
  "windowseal": 1,
  "filed": 1,
  "consume": 3,
  "ractor_run": 1
}

## 3. Authorization Gate
To execute:
```bash
INBOX_COMPACTION_GO=1 python tools/inbox_event_compaction.py --execute --plan /mnt/c/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/INBOX_EVENT_COMPACTION_PLAN_20261021_143954.md
```
