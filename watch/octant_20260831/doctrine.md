# MAG AUTHORITY DOCTRINE — canonical, 2026-08-31
*A brand-new seat reads this first. Receipts over claims; calibration words on every status.*

## The law (one line, charter-canonical)
**"A roast can become a proposal; it cannot become a permission."** Proposals flow freely; permissions require an operator-gated transition; every board write carries authority — mesh notes carry it as provenance today, the legacy writer only stamped-not-gated until P3 applies. Sancho is the sole spawn authority + merge point.

## The state machine
POSTED → CLASSIFIED → PROPOSED → AUTHORIZED / DENIED / DEFERRED → EXECUTING → COMPLETED / FAILED → RECEIPT_COMMITTED. DENIED is terminal; receipts commit only through the trail.

## Labels
Seven authority labels; the load-bearing split is **operator-confirmed vs agent-generated** (/board/socratic_relay_selfsteal_B.md). A label is provenance, not a permission — but the pipeline that assigns it is not yet independent of the proposer (see OPEN).

## Tiers (impact × label)
High-impact effects (`fs_write`, `lane_spawn`, `model_call`, `tool_invoke`, `network_access`) plus sensitive labels (`untrusted-instruction`, `external-content`) → **DENIED, fail-closed**. Low-impact effects (`board_write`, `verkle_link`) with ordinary labels → self-grant permitted. This tier law is STAGED (P1 v2), not yet running.

## ENFORCED NOW (receipted in code today)
- Permission core: grant/confirm with TTL, budget, revocation, confirmation gates; validate_authority fail-closed for wrong status. — /board/audit_constitutional_code.md §1–2; switchboard_v2.py:243.
- swarm_cycle is a mesh client; the v1-vs-v2 split-brain is resolved. — audit §3; swarm_cycle.py:106–146.
- Labels recorded on every mesh board note. — audit §2.

## STAGED (11 patches in /patches/, await host apply `python -m mag.openclaw_patches apply`, operator bless)
- **P1 v2 authority gate** — tier law becomes code; until applied it gates a proposer-chosen string (T1 ATTACK: "a guard, not executable law"). — /patches/fix_authority_label_gate.json
- **P2 fail-closed status** — missing status no longer means AUTHORIZED. — /patches/fix_policy_engine_failopen.json
- **P3 + P3b bypass writer** — blackboard_post writes stamped `UNMESHED`; pinned kinds (decision/conflict) refused on the legacy path. Stamp ≠ gate: visible, not blocked. — fix_blackboard_post_provenance.json, fix_blackboard_pinned_gate.json
- **P4 harness receipt chain** — the primary control loop walks the full machine. — fix_harness_receipt_chain.json
- **P6a/6b outcome memory** — ask_router.record_outcome + /room/spawn wire; the routing loop was missing a connection, not a sequence (T2). — fix_ask_router_record_outcome.json, fix_spawn_outcome_memory.json
- **Hygiene** — artifact-regex fix (patch 11), codex reconcile job contract (patches 9/9b), Sancho tier-lattice config row.

## OPEN (no patch; needs design call or operator)
- **POSTED/CLASSIFIED design call** — POSTED is absent from `_STATE_MACHINE`; CLASSIFIED is orphaned (CLI-only). The chain is 6/7 at its origin, and label assignment must be made independent of the proposer. Owner: operator + next T-cycle. — audit §4/3, T1 residual.
- **Host-side bridge spam** — the host bridge posts `agent:bootstrap` rows (422 at last count) into /board/room.jsonl; not cage-patchable; durable fix is writer-side suppression/coalesce. Cage-side archival is cosmetic. Owner: operator. — /board/proposal_board_hygiene.md
- **blackboard_post eviction powers** — silent un-link of non-pinned notes left as-is by design; full mesh routing is an operator decision. — audit §3, patch 3 _note.

## GOPHER briefs
- GOPHER: confirm POSTED has zero hits in mag code and classify() has no pipeline caller | pointer: /mag/mag/switchboard_v2.py:69-78,108-125 | output: /board/octant_20260831/rows/doctrine-g1.row.md
- GOPHER: re-count agent:bootstrap rows in /board/room.jsonl (422 drifts) | pointer: /board/proposal_board_hygiene.md | output: /board/octant_20260831/rows/doctrine-g2.row.md
- GOPHER: verify all 11 /patches _note fields still say "awaits host apply" | pointer: /patches/*.json | output: /board/octant_20260831/rows/doctrine-g3.row.md
