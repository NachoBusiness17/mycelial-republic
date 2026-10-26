# swarm1-kimi-tools__reverse_map (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: call() uses hardcoded 600s timeout but fire_shard() passes 120s to probe_model() yet probe_model() ignores its timeout parameter and uses hardcoded 120s | EVIDENCE: tools/reverse_map.py:95 | FIX: respect timeout parameter in probe_model() call to call()
DEFECT 2: analyze_rows() lambda judge shadows max_tokens parameter but never uses it, causing confusion; worse, the lambda captures ANALYZE_TOKENS but call() signature has max_tokens before temp | EVIDENCE: tools/reverse_map.py:245 | FIX: remove unused max_tokens=0 parameter from lambda or use it
DEFECT 3: hash((sid, attempt)) % len(keys) for key selection is not stable across Python runs (hash randomization) breaking reproducibility | EVIDENCE: tools/reverse_map.py:173 | FIX: use hashlib.md5(f"{sid}:{attempt}".encode()).hexdigest() or deterministic index
DEAD-CODE: LEXICON list is defined but only used in lexical_fallback which is only called when parse_strategies returns None; lexical_fallback is marked fallback but never tested or instrumented | EVIDENCE: tools/reverse_map.py:231-232
ONE-SITTING FIX: Replace hash() with deterministic key selection using hashlib to ensure reproducible runs across Python invocations | EVIDENCE: tools/reverse_map.py:173
