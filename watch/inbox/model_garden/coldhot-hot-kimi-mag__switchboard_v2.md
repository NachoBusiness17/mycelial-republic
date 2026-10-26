# coldhot-hot-kimi-mag__switchboard_v2 (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: _GRANTED_EVENT_IDS replay protection only tracks AUTHORIZED grants, allowing replay of DENIED/DEFERRED proposals | EVIDENCE: mag/switchboard_v2.py:311-315 | FIX: Track all terminal states in _GRANTED_EVENT_IDS, not just AUTHORIZED
DEFECT 2: _implicit_authority allows self-grant AUTHORIZED for low-impact effects even when proposal status is already DENIED | EVIDENCE: mag/switchboard_v2.py:343-362 | FIX: Check proposal.get("status") not in terminal states before legacy self-grant path
DEFECT 3: confirm() reuses stale ts from DEFERRED record without rechecking TTL expiry at confirmation time | EVIDENCE: mag/switchboard_v2.py:437-446 | FIX: Call policy_engine.check_ttl(rec, pol) before validate_authority in confirm()
DEAD-CODE: cmd_expire imports import_module but never uses it | EVIDENCE: mag/switchboard_v2.py:847
ONE-SITTING FIX: Add TTL recheck in confirm() before authority validation | EVIDENCE: mag/switchboard_v2.py:437-446
