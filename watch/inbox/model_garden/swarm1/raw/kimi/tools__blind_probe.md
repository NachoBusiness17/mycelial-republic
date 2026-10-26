# swarm1-kimi-tools__blind_probe (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: Hardcoded model "openai/gpt-oss-120b" in groq lane is incorrect provider/model mismatch | EVIDENCE: tools/blind_probe.py:82 | FIX: Change to "llama-3.3-70b" per lane docstring or remove hardcoding
DEFECT 2: Gemini API key embedded in URL query parameter exposes secret to logs/proxies | EVIDENCE: tools/blind_probe.py:98 | FIX: Move key to Authorization header like other lanes
DEFECT 3: NOW captured at import time causes stale timestamps across probe runs | EVIDENCE: tools/blind_probe.py:29 | FIX: Compute NOW inside probe() and judge() instead of module level
DEAD-CODE: _canon variable in guard() is never used | EVIDENCE: tools/blind_probe.py:54
ONE-SITTING FIX: Move Gemini key from URL query to Authorization header | EVIDENCE: tools/blind_probe.py:98 | FIX: Restructure gemini URL construction to use header-based auth
