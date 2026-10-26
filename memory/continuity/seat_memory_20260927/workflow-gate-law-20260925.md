---
name: workflow-gate-law-20260925
description: OPERATOR LAW 9/25 — no ungated workflow pings;
  tools/workflow_gate.py enforces dogfood (Mickey17 gophers, interagent
  pass-off, steering, salvage, receipts, laws) before any CreateWorkflow; save
  gated workflows, improve by amendment
metadata:
  node_type: memory
  type: feedback
  originSessionId: sess_fce37d85-5c78-49f1-81cb-d55612026cab
---

2026-09-25 operator rejected an ungated workflow confirmation ping: "stop pinging me for workflows, we need a gate that makes sure workflows are improved, enhanced, dogfooded, and using our systems like Mickey17 gophers, interagent communication and steering. Self steal."

**Why:** every ad-hoc CreateWorkflow pings him for approval (harness contract, cannot be removed); the fix is the ratchet pattern self-stolen onto workflows: gate first, save gated workflows, improve by amendment (amendments don't ping; rewrites do).

**How to apply:** before ANY CreateWorkflow run `python tools/workflow_gate.py check --script <path>` (exit 2 = hard block). G1 Mickey17 gopher fan-out (per-item named actors), G2 interagent pass-off (outputs feed later asks), G3 steering (reviewer feedback drives revision), G4 incremental report() salvage, G5 published deliverable + report shape, G6 receipt lands in watch/inbox/, G7 no-fabrication + em-dash laws inside asks. Every check appends to memory/workflows/REGISTRY.jsonl (digest = improvement ledger). After gate pass, SaveWorkflow so reruns are saved-name runs amended in place, never rewritten. Law line lives in AGENTS.md Build discipline. First subject: tree-doctrine-dig (saved, 50-wide doctrine dig, run dwfrun-15738edf). Related: [[tree-doctrine-20260925]], [[just-go-execute-dont-narrate]].

**Live proof the gate has teeth (09-25 boot lane):** at fire time the gate FAILED the SAVED mickey17-v2 on G3/G4/G7 — saved workflows rot too, the gate checks the shelf, not just new scripts. The predicates are string shapes (G3 wants "Previous critique" or `.feedback` near `ask<`, G4 wants a bare `report(ident);` inside the fan-out, G7 wants "no em-dashes" + a fabrication phrase in ask text) but the fixes were real: bankLane() reports every lane on landing (dead runs keep finished work), the reviewer's bullets route into the fold-repairer ask as named critique, LANE_SYS names the laws. Amend-not-rewrite on `.zcode/workflows/mickey17-v2.dwf.ts` → PASS 7/7 digest 9b51b8e2ee05 → wave 1 fired clean (dwfrun-217c37f5). Also learned: CreateWorkflow `saved` args go INSIDE `saved: {name, args}` — a stray top-level `args` is rejected, and missing required args are caught before compile.

**Day-2 evolution (09-26, cross-window + this seat):** other windows upgraded the gate substantially — LAW-12 genesis clause gave it SCENARIO MODE (`check --scenarios configs/workflow_gate_scenarios`: one card per gate G1-G7, each citing a real REGISTRY.jsonl FAIL row, fixtures must reproduce the card's expected verdict/exit, read-only), a G6 dated-stamp soft-warn (t69 prefilter family), and a G3 judge-independence soft-warn (B2-206: fresh-reader seats run same-session-model; declare `judge-model: <provider/model>` or eat the warn). This seat extended G3 with the "cold reader reported" variant after it missed a valid steering shape in the game-dig script — and per LAW-12 the change was re-proven: scenario suite 7 cards + pass_control GREEN after the edit. Standing rule: every gate change re-runs the scenario suite before submission. The gate also now registers every check to memory/workflows/REGISTRY.jsonl and separates failed vs soft-warned ids in output. Second saved gated workflow: game-mechanics-deep-dig (see [[game-dig-workflows-20260926]]).
