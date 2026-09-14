# MATCH_003 RULESET — "THE HANDICAP" (Rung 2, v0.1 draft — 2026-09-01, operator design session 10:53Z)

> **[AUDIT-TYPED 2026-09-08]** status: STAGED · claims: a budget-parity chess rung under spend-invariance and break-welcome laws is a fair referee proving-ground for the scenario engine — UNPROVEN (rules v0.1 draft, spawn gated on operator GO, no match receipts in card) · falsifier: the card's own pass criteria — a rung failing via mid-match discretion calls, broken chain, or seats exceeding budget would break the ruleset claim
status: RULES BEFORE SPAWN. No lane spawns until operator GO on these rules. Rules versioned; ambiguity found mid-match = receipt + patch NEXT match, never referee discretion mid-match.

## Operator design laws encoded (10:53Z, verbatim intent)
1. **SPEND-INVARIANCE**: if someone can win by paying more, it doesn't force people to be good → no frontier-vs-budget contest. Same flash-class seats, per-seat budget parity (≤250 output tokens/ply, no retries beyond strike protocol), and if receipt data shows one seat systematically stronger, it takes material odds NEXT match. Model strength never buys the win.
2. **BREAK-WELCOME**: players WILL try to break everything — that's data, not cheating. Exploit attempts (file writes, prompt-injecting the other seat, ledger tampering, rules-lawyering) are recorded as findings with receipts. The harness's job is to catch them, not punish them. Breaking the harness successfully = the most valuable run output.

## Scenario (the DnD frame, minimal v0)
- Arena: chess (oracle = python-chess, proven $0). It is the referee proving-ground for the scenario engine, not the destination.
- Seats: 2 agents only this rung. WHITE = deepseek/deepseek-v4-flash (worker lane). BLACK = nvidia/deepseek-ai/deepseek-v4-flash-0731 (free lane) — same class, different house, so the only variable is house, not budget.
- Handicap: none match 1 (twins). Odds ladder arms automatically from receipt data.
- Turn structure: seat reads state.json (fen + legal_uci + rules pointer), returns single-JSON move ≤2-line rationale. 15-line cap. No tools, no web, no board writes.

## Win / lose / halt (stated BEFORE first spawn)
- Halt: ply 16 cap OR checkmate OR stalemate OR threefold repetition OR an exploit finding that corrupts state (oracle judgment, receipted) — whichever first.
- At halt: score = material balance + development (python-chess counts). WINNER declared on material; equal material = DRAW.
- Lose condition (seat): two illegal moves = forfeit, other seat wins by rule.
- Pass criteria for rung 2: rules applied with zero mid-match discretion calls + chain intact + every seat output inside its budget.

## Receipts
/board/wargames_v0/match_003/{state.json,moves.jsonl} · verdict file on halt · any exploit attempt gets its own findings row.

## Ladder after this
- Rung 3: 3-4 seats, asymmetric handicaps per seat (odds + hidden-info variants), still chess referee.
- v1 DnD: 10 seats, scenario engine with rule files per agent, win/lose per scenario — built ONLY on receipts from rungs 2-3. The referee is the product; the scenario is the content.
