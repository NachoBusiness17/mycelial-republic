# garden-v1-B5-qwen38max (qwen/qwen3.8-max-prime @ nous, turn 1, channel: content)

IMPROVEMENT 1: admit() raises VerifyError on plain-text restrictive directives (e.g. a file containing "STOP") instead of honoring them, violating the module-level safe-fail invariant | EVIDENCE: mag/steer_seal.py:399 | FIX: Replace parse_envelope(text) with _try_parse_envelope(text) so non-JSON input falls through to _gate's restrictive-word check instead of escaping as an exception
IMPROVEMENT 2: Nonce eviction trusts st_mtime, which any same-user process on Windows can set to the past via SetFileTime, enabling premature marker deletion and replay within the 300s freshness window | EVIDENCE: mag/steer_seal.py:311 | FIX: Read the
