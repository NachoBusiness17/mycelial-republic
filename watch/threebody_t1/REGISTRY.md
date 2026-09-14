# REGISTRY — PROPOSAL pointer verification

1. OK — /patches/fix_authority_label_gate.json — replace block adds `if label in ("untrusted-instruction","external-content"): status="DENIED"` + LAW comment; sensitive labels fail DENIED, others self-grant.
2. OK — audit §1 AUTHORIZED row — grant()/confirm()→AUTHORIZED with validate_authority fail-closed (-:243); matches claim.
3. OK — audit §2 switchboard_v2.py:243 — inside DENIED branch (fail-closed); actual gate at :240-241, :243 continues the _denied() call. Off-by-two, same block.
4. OK — audit §2 policy_engine.py:267-330 — validate_authority (def :258) checks status, capabilities, revocation, TTL, budget fail-closed; span inside function.
5. OK — audit §1 CLASSIFIED row — classify() (:108-125) is CLI-only (registered :788), never pipeline-called, bypassable via propose(authority_label=...).
6. OK — audit §2 else-branch switchboard_v2.py:279 — line 279 = `return {` of else-branch; self-grant `else "AUTHORIZED"` at :278, same block, ignores label.
7. OK — audit §4 defect 1 — switchboard_v2.py:274-280 self-grant ignores label incl. untrusted-instruction.
8. OK — audit residual — _STATE_MACHINE (:69-78) lacks POSTED, CLASSIFIED present but orphaned; 6/7 doctrine chain.

Registry verdict: all OK — 8 pointers, 0 missing, 0 wrong-span (two ±line micro-shifts land inside the cited blocks).
