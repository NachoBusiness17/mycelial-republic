# coldhot-hot-kimi-mag__preload_selector (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: `order_blocks` is a redundant alias that discards the scoring done by `score_blocks` by re-wrapping the already-scored list in a new list, wasting memory and confusing readers about whether scoring happens | EVIDENCE: mag/preload_selector.py:180-181 | FIX: delete `order_blocks` and have callers use `score_blocks` directly, or change to `return score_blocks(blocks)` without the redundant `list()` wrapper

DEFECT 2: `chat_logprobs` constructs `urllib.request.Request` without setting a User-Agent header, causing the request to fail or be blocked by servers that require one | EVIDENCE: mag/preload_selector.py:222-226 | FIX: add `headers={"Content-Type": "application/json", "User-Agent": "mag-preload-selector/1.0"}` to the Request constructor

DEFECT 3: `cmd_probe` appends to jsonl output without atomic tmp+replace, risking corruption if interrupted | EVIDENCE: mag/preload_selector.py:308-309 | FIX: write to `out.with_suffix('.tmp')` then `os.replace()` to final path

DEAD-CODE: the `ts_span == 0 and ts == ts_min and not known` branch in recency calculation is unreachable because `known` must be truthy for `ts_span` to be defined | EVIDENCE: mag/preload_selector.py:156-157

ONE-SITTING FIX: add User-Agent header to `urllib.request.Request` in `chat_logprobs` | EVIDENCE: mag/preload_selector.py:222-226
