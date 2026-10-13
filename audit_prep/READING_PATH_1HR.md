Goal: a deterministic 1-hour reading path for an external auditor to reach the first verifiable claim along STACK_V1 -> boot -> chain -> fanout -> grounding -> tavern.

Prereqs (5 min)
- Clone repo and use repo's interpreter: `.\.venv\Scripts\python.exe` or `mag.cmd` helper.
- Open these files in order: docs/ref/STACK_V1.md, AGENTS.md, memory/briefs/latest.md.

Step 1 — Boot (10–15 min)
- Inspect mag/boot.py and mag/boot_check.py and run boot smoke: `mag.cmd lab` or `.\.venv\Scripts\python.exe main.py clippy`.
- Confirm last run: watch/boot_latest.json and logs/boot.jsonl.

Step 2 — Chain (15 min)
- Read audit_prep/verkle_chain_READING_GUIDE.md and memory/biography/verkle_chain.jsonl (pointer file).
- Run verification script: `.\.venv\Scripts\python.exe mag\_verify_chain_now.py` (or mag/_verify_chain_now.py in dist_audit bundle).
- Expected artifacts: memory/biography/verkle_chain.jsonl, memory/seals/* (timestamps).

Step 3 — Fanout (10 min)
- Open mag/fanout.py and audit_prep/fanout_organ_width_ladder_receipt.md.
- Run unit checks: `pytest -q tests/test_tripartite_boot.py tests/test_token_chain.py`.

Step 4 — Grounding (5–10 min)
- Read mag/grounding_wave.py and dashboard/static/grounding_wave.md.
- Review handoff: handoff/OX_MEGA_claim_grounding_gate.json.

Step 5 — Tavern (5 min)
- Open mag/tavern_chat.py and dashboard/static/tavern_brawl.html. Confirm UI file present and tavern_summon_guests.py.

Validation (last 5 min)
- Collect receipts: memory/briefs/latest.md, watch/inbox/INDEX.json, and run `pytest -q` to ensure tests green.

If any step fails, capture a single-line failure receipt in audit_prep/READING_PATH_FAIL.txt and escalate to the operator.

Files referenced (exact paths)
- docs/ref/STACK_V1.md
- mag/boot.py, mag/boot_check.py
- mag/_verify_chain_now.py, mag/chain_guard.py, mag/chain_query.py
- audit_prep/verkle_chain_READING_GUIDE.md
- mag/fanout.py, audit_prep/fanout_organ_width_ladder_receipt.md
- mag/grounding_wave.py, dashboard/static/grounding_wave.md, handoff/OX_MEGA_claim_grounding_gate.json
- mag/tavern_chat.py, dashboard/static/tavern_brawl.html
- memory/biography/verkle_chain.jsonl, memory/briefs/latest.md

Author: zcode-lane cell — produce a single-file checklist for the auditor; file created for audit prep.