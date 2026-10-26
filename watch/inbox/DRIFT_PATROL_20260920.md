# DRIFT PATROL — 2026-09-20

- **class:** RECEIPT · **writer:** drift-patrol-cron · **automation:** automation-a7c71ad1 (daily 08:00)

| check | result | verdict |
|---|---|---|
| backup exposure | **143 unpushed commits — PATROL PUSHED THEM** (`9d316bf92..4c28af571`) — largest exposure yet, closed | FIXED BY PATROL |
| fleet vitals | all three containers Up 13h (fleet was bounced ~yesterday evening; restarted healthy) | CLEAN |
| inbox fold | self-healed + refolded: 351→354 events → 115 active items | CLEAN |
| surface integrity | caught 2 drifts at check time (LINKS.jsonl + WHAT_REMAINS overnight writes), refreshed, plus one **seq time-unit collision** (ns-writer 1.79e18 vs us-writer 1.79e15 — ns sorted last despite being older) re-filed above max seq → **0 errors, ok: True** | CLEAN (steady state holds) |
| link ledger | 3 duplicates on file (stable) | CLEAN |

**What the 143 overnight commits were:** the two-machine union reconciliation (local = rebased continuation +229; remote was the frozen Aug-9 shadow; seen.json hash-union absorbed the 100 remote-only dedupe hashes), THE 50 content review (9 reviewers, 44 artifacts: 25 PASS / 19 NOTES / 0 FAIL), the full-tree audit reconciling **1,200,905 files / 42.6GB** (fleet proper ≈ 4,000 files; ~79% debris: .mimosa 390K, knot backups+ghost 441K, run exhaust ~95K; warmed-RIB travel kit supersedes whole-folder sync), travel kit carved (134.9MB zip, sha-verified 15,517/15,517, sacred-cow bet PAID: ~80% of kit files untouched 3+ weeks), MICKEY 17 row (ghost.py TASKS NameError fixed), steal-library burn organs, and a durability receipt: **backup remote DIVERGED (local-only 338, remote-only 110) — deliberate merge owed**.

**Top risks (boldest first):**
1. **Backup remote has genuinely DIVERGED** (local-only 338 commits, remote-only 110, base 5d20144e) — the push-branch pattern kept both lines alive but a deliberate merge is now owed so there is one lineage, not two shadows.
2. **Seq time-unit collision is systemic** — writers mix ns/µs/ms epoch seqs, so "last by seq" ≠ "last by time"; the fold should normalize seq to a single unit (or writers use nextSeq). Today it silently resurrected a stale hash.
3. The 12-item operator ask — day 5; three "now" items still gate forward work.
