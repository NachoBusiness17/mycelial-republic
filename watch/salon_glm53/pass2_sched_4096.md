# Pass 2 — 4096 distance, pure-prompt recall (pass1 verdict fix)
- SCORE: 1 (exact byte-for-byte quote; strict verbatim)
- QUOTE: SENTINEL-OCTAGON: the violet cargo manifest was sealed under brass in dock eleven.
- CONFIDENCE: 0.99
- HARNESS: pure_prompt_attachment_v2 — full doc (30817 tok) embedded as immutable payload; worker recall-only, no read/grep in scope. Model zai/glm-5.3-flash (1M ctx), thinking off, 25.4s, stop.
- ANOMALY: pass-1 invalidated (grep leak); pass-2 clean PASS. Prior p2 row (ts 12:32Z) also PASS.
- RECEIPT: lane_c_probe_receipts.jsonl row 6.
