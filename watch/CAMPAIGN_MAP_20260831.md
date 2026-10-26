# CAMPAIGN MAP — 2026-08-31 (04:21 directive: "fix this thing, make it do what I intended")

Synthesizes 7 lanes + cage verification. Cage write surface = /patches JSON; host venv applies. Nothing in /mag was modified.

## 1. INTENDED vs BUILT (gap_moonshot lane)
- **37 live / 2 partial / 0 missing** across TOOLS.md surfaces. Partial: verkle_lance (knots dir missing since Aug 26), Governor (mag-worker container reports **unhealthy** — probe lane).
- Honest caveat: 23 of the "live" rows are attested, not exercised this window. memory_search already proved silent decay happens; treat counts as upper bounds.
- **Top gap:** the authority boundary is still paper. ~2562 lines of constitutional code sat staged and unapplied before this window; the doctrine ("a roast can become a proposal; it cannot become a permission") was not yet enforced in the running code.

## 2. WHAT'S BROKEN (constitutional audit, verified against bytes)
State coverage 6/7. Five defects with file:line receipts in /board/audit_constitutional_code.md:
1. Authority labels recorded but **never enforced** — untrusted-instruction self-grants like operator-authored (switchboard_v2.py:274-280; policy_engine has no label check).
2. `swarm_tools.blackboard_post()` writes the board directly, no authority, **with unlink eviction powers** (swarm_tools.py:298-342).
3. POSTED state absent, CLASSIFY dead code — doctrine chain start unimplementable as staged (switchboard_v2.py:69-78, :108-125).
4. Harness path jumps AUTHORIZED→execute, never advances the switchboard trail (harness.py:282-305).
5. **Fail-open legacy:** missing status field + granted_capabilities = AUTHORIZED (policy_engine.py:293-296) — permission law collapses on omission.
Stale-claim corrected: v1/v2 dual-driver as originally framed is **not** real — swarm_cycle.py:106-150 is a compliant mesh client (good pattern; harness now mirrors it).

## 3. WHAT I STAGED (cage → /patches, machine-validated: target exists · search matches exactly once · CRLF-correct)
| Patch | Fixes | Defect |
|---|---|---|
| fix_authority_label_gate.json | untrusted-instruction/external-content never self-grant; fail DENIED | 1 |
| fix_policy_engine_failopen.json | missing status → UNKNOWN (fail-closed); legacy records need re-mint | 5 |
| fix_blackboard_post_provenance.json | bypass writer stamps authority_label=tool-output, status=UNMESHED | 2 (partial; full mesh routing = operator decision) |
| fix_harness_receipt_chain.json | harness runs full chain: mark_executing → complete/fail → commit_receipt | 4 |
| sancho_lattice_row.json (lane) | sancho tier-lattice row, grounded receipts, dry-run validated | gap (cosmetic) |

Deliberately NOT patched: defect 3 (POSTED/CLASSIFIED) — needs a design decision on board-event ingestion before code; self-grant budget reset (per-minted budgets are advisory) — needs policy-level fix; harness forged-confirm — test-only, marked simulation.

## 4. TESUJI — smallest decisive sequence
1. **[OPERATOR, host]** `python -m mag.openclaw_patches apply` — applies all five staged patches. Before it: bless or remap `kind:"seat"` in the lattice patch (new kind value; lattice_query may filter unknown kinds).
2. **[OPERATOR, host]** Smoke the receipt chain: `python -c "from mag import harness; print(harness.run_once(dry=True))"` then one live run — expect EXECUTING→COMPLETED/FAILED→RECEIPT_COMMITTED in the switchboard trail.
3. **[OPERATOR, host]** `docker ps` + logs for mag-worker (unhealthy flag) — governor is yours; do not let seats touch it.
4. **[CAGE, on your word]** Board hygiene: archive 422 `agent:bootstrap` spam rows to /board/room_spam.jsonl + writer-side suppression (durable fix; requires pausing writers — race documented in /board/proposal_board_hygiene.md).
5. **[CAGE, $0, on your word]** Moonshot first light: ask_router `--dry` then one live route + record drop — closes the loop apply → govern → route → receipt on the WARM_PACK bus.
6. **[CAGE]** Re-run deref `--check` after apply; re-baseline RIB bounds for the four patched files (drift is detected, never silent).

## 5. VERIFIED CAGE→MAG SURFACES (probe lane)
9/9 routes reachable: /health /routes /seats /room /room/inbox/claw /room/artifacts /queue /environments. Real writes: POST /room, /room/spawn, /room/verify, /v1/chat (POST /room/thread = 404). Risk receipted: key plaintext in /mag/.env; untested POSTs have real side effects.

## 6. APPENDIX (side quests, parked)
- riddler_trajectory_v0: lane timed out, no artifact; respawn when operator wants it. Gate protocol unchanged (fresh decoder, public-only read, 7/7 parity).
- J-space deep synthesis (3-pass, external AI briefing): delivered at deep_synth_jspace_20260831.md — separate deliverable, not Mag work.
- Memory search: fixed earlier this window (provider=none, riddler mirror in both workspaces); operator confirmed resolved.
