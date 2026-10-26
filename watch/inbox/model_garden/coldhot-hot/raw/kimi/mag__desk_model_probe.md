# coldhot-hot-kimi-mag__desk_model_probe (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: _bench_model catches all exceptions without distinguishing retryable vs permanent failures, masking GPU OOMs as generic errors | EVIDENCE: mag/desk_model_probe.py:127-147 | FIX: Catch urllib.error.HTTPError separately to surface 5xx/4xx vs timeout/OOM

DEFECT 2: _gpu_pct_for divides by zero when size is zero, returning None silently instead of error | EVIDENCE: mag/desk_model_probe.py:98 | FIX: Add guard `if not size: return None` before division

DEFECT 3: run_probe calls _tags() fresh in loop iteration, causing redundant HTTP requests | EVIDENCE: mag/desk_model_probe.py:156-161 | FIX: Reuse `tags` variable from line 152 instead of calling _tags() again

DEAD-CODE: from __future__ import annotations | EVIDENCE: mag/desk_model_probe.py:2

ONE-SITTING FIX: Add atomic write for REPORT_PATH to prevent corrupted JSON on crash | EVIDENCE: mag/desk_model_probe.py:189 | FIX: Use temp file + replace pattern: write to REPORT_PATH.with_suffix('.tmp') then Path.rename
