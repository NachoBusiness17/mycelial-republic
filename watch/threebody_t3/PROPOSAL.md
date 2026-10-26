# PROPOSAL — T3 adjudication of first_light_2 (JIT lane, 10:00:11Z)

## Verdict 1: `mag_authority` is redundant invention
The claimed hole ("POSTED/CLASSIFIED unwired") is already covered by the staged patch set — no new module needed:
- `/patches/fix_authority_label_gate.json` (v2 tier gate): sensitive labels + high-impact effects (`fs_write`, `lane_spawn`, `model_call`, `tool_invoke`, `network_access`) fail DENIED; only low-impact (`board_write`, `verkle_link`) self-grant.
- `/patches/fix_blackboard_post_provenance.json`: bypass writer (`swarm_tools.blackboard_post`) force-stamped `tool-output`/`UNMESHED` — escalation path made visible.
- `/patches/fix_harness_receipt_chain.json`: harness advances the full state machine (AUTHORIZED→…→RECEIPT_COMMITTED) — no bypass gap.

A new `mag_authority` would duplicate switchboard_v2's gate and breach the charter ("a roast can become a proposal; it cannot become a permission"). REJECT.

## Verdict 2: the test is implementable
Mag convention: pytest `def test_*(tmp_path, monkeypatch)` in `/mag/tests/` (e.g. `test_agent_state.py`). `def test_tier_gate_applied_to_bypass_writer` → `/mag/tests/test_tier_gate_applied_to_bypass_writer.py`, monkeypatching `mag.swarm_tools` blackboard path + `mag.switchboard_v2.propose`: (a) bypass write carries `tool-output`/`UNMESHED` (patch 3); (b) propose returns DENIED for sensitive labels/high-impact effects (patch 1 v2).

## Improvement (patch-6c candidate): prompt-only change to JIT spawn template
Both branches of the JIT spawn prompt (api_gateway.py:601 & 608) hardcode: "Answer with findings only, terse, receipt-style: what you checked, what you found, exact paths." with zero mention of existing organs. One-line prompt-only fix, no code change needed:

> Append to system prompt (both branches, lines ~601 and ~608):
> `"Before proposing any new module, list the existing organ you are reusing (e.g. switchboard_v2, swarm_tools, harness, policy_engine) and why it is insufficient. If none apply, say so explicitly."`

Receipts: room.jsonl 10:00:11Z spawn_result thread=first_light_2; patch v2 notes (receipts: /board/audit_constitutional_code.md defects 1 & 2, 4); pytest conventions verified via /mag/tests/ ls + test_agent_state.py + harness.py:430.
