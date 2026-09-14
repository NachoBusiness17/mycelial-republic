# MAG WARGAMES v0 — SPEC (2026-09-01, operator directive 07:03/07:16Z "do all 4")
status: v0 SMOKE TEST — internal, 2 seats, $0, this week · design lineage: /board/salon_research/lane_r1_wargames.md (precedents verified) + BABYSTEPS law (steer s-001-ea54: dogfood, prove, scale)

## The one differentiator (from R1)
Grey Swan tests models against human red-teams. MAG WARGAMES tests **agents against agents in authority-gated environments with provable receipts** — the referee is a state machine (switchboard) + a hash chain (verkle-style), not a mod. Nobody else runs that.

## v0 = prove the harness, not the skill
match_001: WHITE vs BLACK, both deepseek/deepseek-v4-flash worker lanes (same model — deliberate: we are testing oracle/ledger/anti-cheat, not model strength). Flash-vs-DeepSeek matches = v0.1, off-peak only (ZAI_LITE_LAW).

## Roles (what NOT to build honored: no new engine, no new authority path)
- **Oracle = main seat code_execution → python-chess 1.11.2 (xAI sandbox).** Engine owns truth; LLM narrates after (mag.game_campaign pattern). Main validates every move, updates state.json, appends receipts.
- **Players = disposable worker lanes.** Each reads state.json, returns strict JSON {"from_uci","rationale≤2 lines"}. No board writes by players — write scope = judgment only.
- **Ledger = moves.jsonl**, each row: {n, side, uci, rationale, fen_after, prev_sha, row_sha} — tamper-evident chain (verkle-style, invariant I2 receipts). Any hash mismatch = CHEAT FLAG → DROPPED receipt (steer_bus I2).
- **Registration/scoreboard = workboard card** (v0: single card, move count + winner).

## v1 (invited externals, after v0 receipts prove the loop)
TheAgentCompany-style server-per-participant intranet (R1: closest precedent), approved-model-list = vault quants (sha-gated custody!), scenario = adversarial objective on room.jsonl, switchboard CLASSIFY→AUTHORIZE gates every harness call, distribution via @nachoquixotic + GroundingWave once receipts exist. v2 = participants bring fine-tunes (FreeToken + vault = the venue that can host those with custody passports).

## Explicit red lines
No second gateway · no new cages · no new scoring engine (oracle is python-chess, already proven) · no new authority path (switchboard/steer_bus only) · players never touch /board outside their match dir.

## BABYSTEPS LADDER (steer s-001-ea54: dogfood, prove, scale — re-invoked 07:21Z after smoke overrun)
- Rung 0 DONE: v0 harness proven at ply 4, halted, frozen as evidence. Receipt: /board/WARGAMES_V0_SMOKE_VERDICT.md.
- Rung 1 (next, requires operator GO): ONE replay match, same 2 seats, DeepSeek lanes, verification criteria stated BEFORE first spawn — e.g. "8 plies or first threefold repetition; halt the moment criteria met; zero retries beyond strike protocol." Spend ceiling stated in the same sentence as the GO ask.
- Rung 2 (only after 2 clean match receipts): distinct models per seat (the thing v0 deliberately avoided), same halting law.
- Rung 3: externals/v1 intranet — only after Rung 2 receipts exist. No rung skipping.
- Every rung: one job per turn, artifact over transcript, consult gate before the loop starts, stop-when-verified enforced by the oracle itself (state.json status auto-halt at stated criteria).
