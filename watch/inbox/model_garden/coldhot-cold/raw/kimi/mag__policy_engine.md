# coldhot-cold-kimi-mag__policy_engine (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: _collect_active_records yields from generator inside nested function but generator never returns list, causing expire() to iterate over None | EVIDENCE: mag/policy_engine.py:372-401 | FIX: Change `yield from _add(...)` to `active.append(rec)` and return `list(active)` at function end, or refactor to properly return list[dict]
DEFECT 2: revoke() appends to jsonl without atomic tmp+replace, violating the known wiring pattern and risking corruption on crash | EVIDENCE: mag/policy_engine.py:236-244 | FIX: Write to REVOCATIONS_FILE.with_suffix('.tmp') then atomic rename
DEFECT 3: cmd_set allows arbitrary key injection including underscore-prefixed keys like _load_error that save_policy then strips, creating confusing UX | EVIDENCE: mag/policy_engine.py:424-432 | FIX: Reject keys starting with underscore or match against known policy schema keys
DEAD-CODE: check_ttl_valid function is a thin wrapper around check_ttl with identical signature, unused anywhere in the file | EVIDENCE: mag/policy_engine.py:352-353
ONE-SITTING FIX: Fix _collect_active_records to actually return list[dict] instead of broken generator | EVIDENCE: mag/policy_engine.py:372-401
