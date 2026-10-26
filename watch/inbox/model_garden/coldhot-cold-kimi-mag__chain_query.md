# coldhot-cold-kimi-mag__chain_query (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: Unbounded regex search in exists() allows ReDoS via crafted pattern | EVIDENCE: mag/chain_query.py:180-186 | FIX: Pre-compile pattern with timeout or reject regex metacharacters before search

DEFECT 2: breadcrumb() and exists() scan full JSON text including values, not just IDs, causing false positives | EVIDENCE: mag/chain_query.py:165-166,180-181 | FIX: Search only specific hash/id fields instead of full JSON dump

DEFECT 3: cost_window() parses ISO timestamps with string comparison instead of datetime, fails across timezone formats | EVIDENCE: mag/chain_query.py:228-229 | FIX: Parse both cutoff and knot["ts"] to datetime objects before comparison

DEAD-CODE: _log_query and _log_fallback increment counters but never persist or expose them beyond stats() | EVIDENCE: mag/chain_query.py:95-100

ONE-SITTING FIX: Add re.escape() or literal-only mode to exists() to prevent ReDoS | EVIDENCE: mag/chain_query.py:180-186
