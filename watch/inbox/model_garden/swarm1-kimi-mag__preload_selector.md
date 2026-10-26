# swarm1-kimi-mag__preload_selector (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: chat_logprobs constructs urllib.request.Request without timeout parameter passed to urlopen, using fixed 180s timeout that cannot be overridden | EVIDENCE: mag/preload_selector.py:267-275 | FIX: add timeout parameter to chat_logprobs signature and pass to urlopen

DEFECT 2: cmd_probe appends to jsonl file without atomic tmp+replace (known violation pattern repeated) | EVIDENCE: mag/preload_selector.py:376-378 | FIX: write to temp file in same directory, then os.replace

DEFECT 3: pick_model and ollama_health use bare except Exception without logging the specific error condition | EVIDENCE: mag/preload_selector.py:228-238 | FIX: log exception details to stderr before returning fallback

DEAD-CODE: recency calculation branch `ts == ts_min and not known` is unreachable because `known` is truthy when ts_min is set | EVIDENCE: mag/preload_selector.py:176-177

ONE-SITTING FIX: add timeout parameter to chat_logprobs and propagate through run_arm to cmd_probe args | EVIDENCE: mag/preload_selector.py:267-275
