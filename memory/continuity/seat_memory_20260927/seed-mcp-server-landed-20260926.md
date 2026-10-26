---
name: seed-mcp-server-landed-20260926
description: 9/26 seed-MCP server built and falsified — cold agent boots from
  kilobytes via MCP stdio, 10/10 cold-join pass, strict schema consumer, B2-164
  ENFORCING scenario gate
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

Seed-MCP server (B2-181) built 9/26 and falsified live: `tools/seed_mcp.py` (371 lines) serves seed://current, seed://law-registry, seed://brief-pointers as MCP resources + rebuild_subtree, verify_hash, fetch_bounded_pointer, join_protocol tools. Cold client `tools/seed_mcp_cold_client.py` ran 10/10 COLD JOIN PASS over real stdio; mutated-source and void-path refusals hold. Real seed `SEED_RIB_CURRENT_20260926.json` (42,727 bytes, 13 entries, 11 law_refs) built by B2-180's `tools/seed_rib.py`. 15 hermetic pins in tests/test_seed_mcp.py. Falsifier mutation caught by pin: flipped content_b64 named and refused. Join protocol is the 7-step machine-checkable cold boot. Honest gap: cold-of-knowledge not cold-of-machine (fresh-clone join = B2-539). Related: [[seed-rib-mickey17-panel-20260926]], [[essentials-pack-disaster-recovery]], [[width24-go-execution-fcfs-20260926]]. Also landed same night: B2-164 ENFORCING scenario suite gate at pre-push (workflow_gate.py change cannot push while configs/workflow_gate_scenarios is red; 7/7 cards green; falsifier executed live, push REJECTED exit 1 naming BLOCKS the push; trigger = tools/workflow_gate.py only, card dir deliberately out of trigger, widening = operator flip).
