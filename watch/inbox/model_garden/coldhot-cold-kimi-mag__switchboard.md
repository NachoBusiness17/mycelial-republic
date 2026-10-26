# coldhot-cold-kimi-mag__switchboard (moonshotai/kimi-k2 @ nous, turn 1, channel: content)



DEFECT 1: CLI drop command ignores steer_drop error return code | EVIDENCE: mag/switchboard.py:735-738 | FIX: Capture steer_drop result, print JSON, return 0 if ok else 1
DEFECT 2: route_intent recalculates importance after arena seat swap without rechecking api_ready flag | EVIDENCE: mag/switchboard.py:605-610 | FIX: Add importance -= 15 check after updating prof from arena recommend
DEFECT 3: status function calls find_orphans redundantly after mesh already invoked it | EVIDENCE: mag/switchboard.py:635-638 | FIX: Call find_orphans once in status and propagate count to mesh summary or reuse result
DEAD-CODE: tier_rank function is defined but never called | EVIDENCE: mag/switchboard.py:75-76
ONE-SITTING FIX: Fix drop command to exit with code 1 on steer_drop failure | EVIDENCE: mag/switchboard.py:735-738
