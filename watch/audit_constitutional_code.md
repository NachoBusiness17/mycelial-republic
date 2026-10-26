# Constitutional Code Audit — staged v2 organs vs switchboard doctrine

Date: 2026-08-31 · Auditor: worker subagent (read-only on /mag) · Doctrine receipts: /board/socratic_relay_selfsteal_B.md, memory/riddler_common.md (authority-label law: operator-confirmed / agent-generated; "a roast can become a proposal, it cannot become a permission").

## Verdict

The v2 organs faithfully implement the doctrine's **decision core** (PROPOSED → AUTHORIZED/DENIED/DEFERRED, TTL/budget/revocation/confirmation gates, receipt commit) and the v1 `swarm_cycle` composite is now mesh-compliant — but the doctrine is **not fully honored**: POSTED does not exist, CLASSIFIED is orphaned, authority labels are recorded metadata with zero enforcement, and a legacy tool path still writes the board outside the mesh with eviction powers.

## 1. State-machine coverage table (doctrine vs code)

Doctrine chain: POSTED → CLASSIFIED → PROPOSED → AUTHORIZED/DENIED/DEFERRED → EXECUTING → COMPLETED/FAILED → RECEIPT_COMMITTED

| Stage | In code? | Receipt |
|---|---|---|
| POSTED | **ABSENT** | `grep POSTED /mag/mag/*.py` = 0 hits. `_STATE_MACHINE` (switchboard_v2.py:69-78) has no POSTED; board notes appear on disk with no origin state. |
| CLASSIFIED | Present, **orphaned** | In `_STATE_MACHINE` (switchboard_v2.py:70); `classify()` exists (switchboard_v2.py:108-125) but is CLI-only (`cmd_classify`, :788) — never called by propose/grant/execute, harness, or swarm_cycle. Label can also be bypassed via `propose(authority_label=...)`. |
| PROPOSED | ✅ | `propose()` sets `status: PROPOSED` (switchboard_v2.py:159). |
| AUTHORIZED | ✅ | `grant()` (switchboard_v2.py:250), `confirm()` → CONFIRMED → AUTHORIZED (:413-423). Gates: TTL (:213), budget preflight (:226), confirmation→DEFERRED (:231), validate_authority fail-closed (:243). |
| DENIED | ✅ terminal | `_denied` (:326-330), `deny()` (:434-446), deny short-circuit (:192-204), expired-confirm sweep `_flush_expired_deferred` (:808-820). |
| DEFERRED | ✅ | `_defer` (:302-330) + operator inbox write; confirm/deny round-trip real (:368-446). |
| EXECUTING | ✅ partial | `mark_executing()` (switchboard_v2.py:490) — called **only** by swarm_cycle.py:126. Harness `run_once` jumps AUTHORIZED → `eb.execute` (harness.py:282-291) without it. |
| COMPLETED / FAILED | ✅ partial | `complete()`/`fail()` (switchboard_v2.py:501, 511) — called **only** by swarm_cycle.py:132/138. Broker has its own internal ENQUEUED→RUNNING→COMPLETED/FAILED (effect_broker.py:367-426) but the switchboard trail never advances in the harness path. |
| RECEIPT_COMMITTED | ✅ split | Two ledgers: broker receipts (effect_broker.py:184-185, all effects) and switchboard trail `commit_receipt()` (switchboard_v2.py:519-541) — the latter driven only by swarm_cycle.py:144. |

**Coverage: 6/7** (POSTED missing entirely; CLASSIFIED present in table but dead in the live path; terminal trio fully wired only on the swarm_cycle path).

## 2. Authority-label enforcement

- Labels defined: switchboard_v2.py:47-54 and policy_engine.py:53-61 (mirrored). Written into every mesh board note via the embedded `authority` dict (switchboard_v2.py:~605-612 payload `"authority": authority`).
- **Enforcement: NO.** `policy_engine.validate_authority` (policy_engine.py:267-330) checks status, capabilities, revocation, TTL, budget — never `authority_label`. No gate maps label → capability.
- `_implicit_authority` (switchboard_v2.py:270-286): the else-branch (:279) yields AUTHORIZED **regardless of label** — an `untrusted-instruction`-labeled proposal self-grants exactly like an operator-authored one. The classify() imperative-detector that would assign that label never runs in the pipeline.
- Conclusion: labels are provenance metadata, not law. The riddler_common charter's authority taxonomy is represented in data but not enforced at any checkpoint.

## 3. Dual-driver risk (v1 swarm_cycle vs v2 harness)

- Lane B's receipt (socratic_relay_selfsteal_B.md) is **stale in one respect**: swarm_cycle.py:106-109 no longer writes `bb-*.json` directly; it routes propose → grant → mark_executing → eb.execute → complete/fail → commit_receipt (swarm_cycle.py:109-146). The v1-vs-v2 split-brain as originally framed is **mitigated** — v1 is now a mesh client.
- **But a residual dual-writer exists**: `swarm_tools.blackboard_post()` (swarm_tools.py:298-342) writes `bb-NNNNN.json` **directly** to the same namespace (`BLACKBOARD_DIR = SCRATCH_DIR.parent / "blackboard"` = `memory/runs/swarm_worker/blackboard`, swarm_tools.py:47) with no grant, no authority field, no label, and performs best-effort **eviction (unlink)** of non-pinned notes (:329-339). Exposed as a swarm tool at agent_cli.py:949 ("blackboard_post") and used by _demo_telepathy.py:94. board_directive.py:11 independently documents this exact gap and confirms it was verified in bytes.
- Harness `run_once` + v1 `swarm_cycle` coexisting is therefore not double-writing today, but any seat invoking `blackboard_post` re-opens the un-labelled, unauthorized write surface the doctrine forbids.

## 4. Top 5 defects (file:line receipts)

1. **Authority labels unenforced at the gate** — switchboard_v2.py:274-280 (self-grant ignores label, incl. untrusted-instruction), policy_engine.py:267-330 (validate_authority has no label check), switchboard_v2.py:108-125 (classify() orphaned, CLI-only).
2. **Bypass board writer with eviction powers** — swarm_tools.py:298-342 (direct `bb-*.json` write :316-322; silent `p.unlink` eviction :329-339), exposed via agent_cli.py:949. No authority, no label, no trail record; breaks "every board write carries authority."
3. **POSTED absent, CLASSIFIED dead** — switchboard_v2.py:69-78 (state table lacks POSTED), :108 (classify unused in pipeline); doctrine chain start is unimplementable from code as staged.
4. **Harness path never reaches switchboard terminal states** — harness.py:282-305 calls `eb.execute` straight from AUTHORIZED; `mark_executing/complete/fail/commit_receipt` (switchboard_v2.py:490-541) have exactly one caller: swarm_cycle.py:126-146. The switchboard trail is a discontinuous chain in the primary control loop.
5. **Fail-open legacy authority** — policy_engine.py:293-296: an authority record with **no status field** is treated AUTHORIZED if it merely carries `granted_capabilities`; combined with `cmd_execute` accepting an arbitrary authority JSON file (effect_broker.py:469-474), any process can mint a passing authority by omission. Fail-closed claim (switchboard_v2.py:185) holds only for wrong-status, not missing-status.

## Risks not in top 5 (one line each)

- Reconcile self-grants every pass with fresh `budget={"max_calls":1}` (switchboard_v2.py:~710-724) — budget bounds are per-minted-authority, so they reset and are advisory, not global.
- Harness "operator confirm" scenario forges a confirmed authority in-process (harness.py:413-420) — safe today only because it is `test-`-prefixed and marked `evidence_class: simulation` (harness.py:180-184).

## Bottom line

Doctrine's permission core is real and fail-closed where it runs; its provenance law (labels, POSTED origin) is decorative, and one legacy tool still walks around the wall. State coverage 6/7. Dual-driver as framed (v1 vs v2): no; residual unauthenticated second writer: yes (swarm_tools.blackboard_post).
