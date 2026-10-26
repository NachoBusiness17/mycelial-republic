# genlive1-g0-2-glm-flash (glm-5.3-flash @ zai, turn 1, channel: content)

DEFECT 1: recency contradicts its own spec: when ts_span == 0 every known-ts block gets 0.0, not 1.0, because the branch requires `not known` while `ts` is truthy (dead condition), so all blocks tie on score via heat only | EVIDENCE: mag/preload_selector.py:168-170 | FIX: `recency = 1.0 if ts and ts_span <= 0 else ((ts - ts_min).total_seconds() / ts_span) if ts else 0.0`
DEFECT 2: verdict is emitted on empty evidence: when zero shared tokens, mean_lp = 0.0 forces rel_pct = 0.0, which classifies as DECORATIVE (kill) though nothing was measured | EVIDENCE: mag/preload_selector.py:307-311 | FIX: return `verdict: "NO_SHARED_POSITIONS"` and skip the threshold classification when `not dlp`
DEFECT 3: em-dash characters in emitted output violate the no-em-dash law ("no trajectory blocks found — aborting", plus the `— down is a result` comment) | EVIDENCE: mag/preload_selector.py:356-357 | FIX: replace with plain hyphens in both strings
DEFECT 4: model selection is env-sensitive: `pick_model` compares exact names against /api/tags, but ollama returns tags like `qwen2.5:3b-instruct:latest`, so the intended model misses and `sorted(names)[0]` silently picks an arbitrary specimen, changing the instrument | EVIDENCE: mag/preload_selector.py:215-226 | FIX: match on name or `name.split(":")[0]` before falling through

DEAD-CODE: `order_blocks` is defined and never called anywhere in the file | EVIDENCE: mag/preload_selector.py:183-184

ONE-SITTING FIX: repair the recency branch per DEFECT 1 and add a selftest case with two blocks sharing one timestamp asserting recency == 1.0 for both; falsifier: `selftest` must FAIL before the patch and PASS after, with `ok_recency_span_zero=True` printed | EVIDENCE: mag/preload_selector.py:167-170
