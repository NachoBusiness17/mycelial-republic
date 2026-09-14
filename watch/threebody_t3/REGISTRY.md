# T3 REGISTRY — first_light_2 pointer audit

- `/patches/fix_authority_label_gate.json` — **OK** (exists)
- `/patches/fix_blackboard_post_provenance.json` — **OK** (exists)
- `/patches/fix_harness_receipt_chain.json` — **OK** (exists)
- `/mag/tests/test_agent_state.py` — **OK** (exists; `test_commit_chain_and_load(tmp_path, monkeypatch)` confirms the cited pytest convention)
- `api_gateway.py:601` — **OK** (line 601 = mill-branch system prompt, hardcoded identical string)
- `api_gateway.py:608` — **OK** (line 608 = chat_provider-branch `system=(...)` prompt, identical string). Both branches match; appended instruction lands on both. **Span supports the claim.**
- `mag.swarm_tools` — **OK** (as `/mag/mag/swarm_tools.py`)
- `mag.switchboard_v2` — **OK** (as `/mag/mag/switchboard_v2.py`)
- `/board/audit_constitutional_code.md` — **OK** (exists)
- `/board/room.jsonl` — **OK** (exists)
- `harness.py:430` — **OK** (resolved `/mag/mag/harness.py`, line 430 = `def test_scenario_1()`; test-function convention supported)
- `/mag/tests/test_tier_gate_applied_to_bypass_writer.py` — **NEW** (proposed, not yet present; not a claim of existence)

No MISSING, no WRONG-SPAN. One note: two python-module pointers (`swarm_tools`, `switchboard_v2`, `harness`) are abbreviated without the `/mag/mag/` prefix; harmless, resolves correctly.

**VERDICT: ALL POINTERS OK.** The api_gateway.py:601/608 span is exact and the improvement text lands on both spawn-prompt branches unchanged.
