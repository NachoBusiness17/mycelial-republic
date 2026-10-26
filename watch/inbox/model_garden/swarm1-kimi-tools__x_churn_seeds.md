# swarm1-kimi-tools__x_churn_seeds (moonshotai/kimi-k2 @ nous, turn 1, channel: content)



DEFECT 1: Non-atomic overwrite of OUT_MD causes irreversible loss of the anchor map if the script crashes mid-write | EVIDENCE: tools/x_churn_seeds.py:165 | FIX: Write to a temporary path first, then os.replace(OUT_MD, tmp)
DEFECT 2: pull_post extracts "rts" from d.get("retweets") but the vxtwitter API schema uses "retweet_count", causing engagement sorting for Round 2 seeds to always tie on None | EVIDENCE: tools/x_churn_seeds.py:77 | FIX: Change d.get("retweets") to d.get("retweet_count")
DEFECT 3: known_ids() ignores OUT_JSONL when building the exclusion set, causing duplicate harvests and repeated work across subsequent script runs | EVIDENCE: tools/x_churn_seeds.py:57-62 | FIX: Append OUT_JSONL to INVENTORY_FILES or read harvested IDs from it before seed selection
DEAD-CODE: from datetime import datetime, timezone | EVIDENCE: tools/x_churn_seeds.py:12
ONE-SITTING FIX: Patch atomic write for OUT_MD to prevent crash-induced data loss | EVIDENCE: tools/x_churn_seeds.py:165
