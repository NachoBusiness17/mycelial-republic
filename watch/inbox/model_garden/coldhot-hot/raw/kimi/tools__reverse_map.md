# coldhot-hot-kimi-tools__reverse_map (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: race condition in Ledger.bank: multiple threads append to same file without fsync or atomic rename, corrupting jsonl on crash | EVIDENCE: tools/reverse_map.py:111-116 | FIX: use tmpfile+rename pattern with exclusive create flag
DEFECT 2: analyze_rows ignores dh.fire return signature mismatch: caller=judge returns (text, cost) but judge lambda discards max_tokens param and returns raw call() dict | EVIDENCE: tools/reverse_map.py:234-236 | FIX: fix lambda to unpack dh.fire properly or remove indirection
DEFECT 3: fire_shard uses hash((sid, attempt)) % len(keys) for key rotation which collides across sids, violating V9 law 5's "never rotate mid-run" intent | EVIDENCE: tools/reverse_map.py:141 | FIX: use deterministic shard-key assignment: keys[i % len(keys)]
DEAD-CODE: dh.REASONING_CAP reference in body_for | EVIDENCE: tools/reverse_map.py:65 | EVIDENCE: dh.REASONING_CAP not defined in duel_harness imports shown (line 19-20 only show dh imported, no attr list)
ONE-SITTING FIX: Ledger.bank atomic write | EVIDENCE: tools/reverse_map.py:111-116
