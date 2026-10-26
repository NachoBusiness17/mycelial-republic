# swarm1-kimi-tools__stealth_driver (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: _mark_work and t_selfimp write jsonl without atomic tmp+replace, risking corruption on crash | EVIDENCE: tools/stealth_driver.py:337-341 | FIX: Use atomic write pattern: tmp.write_text() + tmp.replace() like _write_mirrors_if_changed
DEFECT 2: t_verify updates WORK_STATE before dispatching hermes, losing verify_last_ts on hermes failure | EVIDENCE: tools/stealth_driver.py:1118-1121 | FIX: Update state only after successful dispatch, or use tmp+replace for state writes
DEFECT 3: _llama_guard creates no_redirect class but never uses it, using _NoRedirect instead | EVIDENCE: tools/stealth_driver.py:622-627 | FIX: Remove dead no_redirect assignment or use it
DEAD-CODE: no_redirect variable assigned but never used in _llama_guard | EVIDENCE: tools/stealth_driver.py:625
ONE-SITTING FIX: Make _mark_work atomic with tmp+replace pattern | EVIDENCE: tools/stealth_driver.py:337-341 | FIX: Replace direct write with tmp = WORK_QUEUE.with_suffix(".jsonl.tmp"); tmp.write_text(...); tmp.replace(WORK_QUEUE)
