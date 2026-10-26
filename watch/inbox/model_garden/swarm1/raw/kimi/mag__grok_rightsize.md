# swarm1-kimi-mag__grok_rightsize (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: `probe_xai_keys` uses `urllib.request` without browser User-Agent header, violating the KNOWN wiring violation (b) that the file already carries | EVIDENCE: mag/grok_rightsize.py:142-154 | FIX: Add `"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"` to the headers dict at line 149

DEFECT 2: `log_grok_call` writes to shared jsonl surface without atomic tmp+replace, violating KNOWN wiring violation (c) | EVIDENCE: mag/grok_rightsize.py:622-623 | FIX: Use `tempfile.NamedTemporaryFile` with `dir=LEDGER_PATH.parent`, write, then `os.replace` to `LEDGER_PATH`

DEFECT 3: `call_grok` uses `json.dumps` without ensuring non-ASCII handling for API body, risking encoding mismatches with xAI API | EVIDENCE: mag/grok_rightsize.py:396 | FIX: Add `ensure_ascii=False` to `json.dumps(body, ensure_ascii=False).encode("utf-8")`

DEAD-CODE: `_key_env` local variable assigned but never used after latency calculation | EVIDENCE: mag/grok_rightsize.py:434

ONE-SITTING FIX: Add atomic write pattern to `log_grok_call` to prevent ledger corruption on concurrent writes or crashes | EVIDENCE: mag/grok_rightsize.py:622-623
