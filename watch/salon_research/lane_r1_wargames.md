# LANE R1 — WARGAMES VENUE RESEARCH (2026-09-01 ~07:1xZ)
Task: operator 07:03Z "server-per-participant, approved-model list, write agents, shared scenario, evolves to fine-tuned." ≤50 lines. Fetch log: /board/salon_research/fetch_log.md.

## 1. PRECEDENT SCAN (receipts; web_search transcript, cites in fetch_log)
- **Grey Swan Arena** — VERIFIED. Crowdsourced red-team competitions; researchers attack llama> agents (jailbreak, prompt-injection, agent compromise); data fine-tunes defensive/offensive models (Shade, Cygnal). UK AISI event: ~1.8M attempts, 62K breaks, 22 models, $171K prizes. Closest to "bring your fine-tune." Not seat-vs-seat; it's attacker-vs-model.
- **AgentBench** (THUDM) — VERIFIED. 8 envs (OS shell, DB, KG, games, shopping, browsing) multi-turn, SR metrics. No arena; single-agent task completion.
- **tau-bench** — VERIFIED. Tool-Agent-User customer service; DB-state objective eval; pass^k reliability. Single agent vs simulated user/API. No competition.
- **OSWorld** — VERIFIED. Real-OS computer-use, 369 tasks, GUI grounding, execution-based eval. Single agent; human 72% vs SOTA ~12%. Not competitive.
- **TheAgentCompany** — VERIFIED. Docker intranet, 175 tasks, GitLab/ownCloud/Plane/RocketChat + 16 LLM NPCs. Spawns agents onto a company server = closest to "server-per-participant." Not scored head-to-head.
- **AI Village (DEF CON)** — VERIFIED. Security venue; HalCTF = agent security challenges. **Smallville** — VERIFIED (separate): 25 believable agents in a town; social emergent behavior, NOT a competition.
- **CATArena** — VERIFIED (arXiv 2510.26852). Board-game tournaments where agents CODE strategies, compete, revise from outcomes (iterative). Closest to "write agent, test, iterate."
- **AgentStakes/Arena.ai/SC2Arena/ChatArena** — VERIFIED (via cites). Poker/ELO arenas; ChatArena deprecated 2025-08.
- **UNVERIFIED:** exact CATArena iteration cadence; OSWorld exact count (369 vs 361); Grey Swan v1 pre-2025 timing.

## 2. THREE FORMATS MOST COMPATIBLE WITH OUR INFRA
1. **Switchboard-arena (tape that fits state machine):** each participant submits agent code as a workboard card; card rides POSTED→CLASSIFIED→AUTHORIZED→EXECUTED→RECEIPT; every move logged to verkle chain (tamper-evident like SALON_GLM53 I2/I3). **Best fit** — reuses our only proven-path authority.
2. **TheAgentCompany-style server-organic:** each server is a clean Docker instance; agent acts on intranet tools (agent_arena + room.jsonl tail). Compatible with room.jsonl public square. **2nd** — matches "server per day," heavy setup.
3. **Grey-Swan-evolved (bring your fine-tune):** participants pre-register model on approved list (vault quants); scored via shared scenario. **3rd** — needs later, is the v1→v2 evolution, not v0.

## 3. MAG WARGAMES v0 (THIS WEEK, internal, 3-5 seats, $0)
- **Format:** format 1 (switchboard-arena) + format 2 server hygiene. Seats: fleets seats (driver/hands/swarm) each submit an agent script.
- **Scenario:** shared chess-oracle arena (agent_arena + python-chess, already EXERCISED-7d) — agents play N games vs a fixed GM baseline + each other; plus 1-turnroom objective (e.g., "award the grant to the agent that most advances X"). Scoring: win-rate vs baseline (oracle) + receipts traceability.
- **Scoring:** verkle-logged per-move hashes; anti-cheat = agent can only call the approved harness API (switchboard-gated), no raw file edits to scoring state; tamper = receipt chain mismatch detects.
- **Registration:** workboard card `R1-MAG-WG-<seat>` → CLASSIFIED → AUTHORIZED (operator countersign) → spawn server. Same card threads receipts.
- **Distribution:** none external (internal); results to /board/room.jsonl public square + one steer_bus closed-enum directive after.
- **Verdict gate:** every gate PASS/FAIL logged; two-strike bail if harness fails twice.

## 4. MAG WARGAMES v1 (INVITED EXTERNALS, 1-DAY SERVER)
- Scenario: TheAgentCompany-style intranet + one adversarial objective; scoring = task completion + anti-cheat integrity (verkle).
- Approved-model list = MODEL_VAULT_PASSPORTS.jsonl quants (qwen2.5-coder-32b, gpt-oss-120b); externals register via operator X surfaces: @nachoquixotic (project main) + @GHOST_HANDLE (physics face). Registration = public post → operator drops link → workboard card.
- Distribution: X post from @nachoquixotic announcing open registration + scenario brief; @GHOST_HANDLE signals the physics/harness side.
- Gates: registrations deduped vs ARCHIVIST_RECEIPTS; two-strike bail on spam.

## 5. WHAT NOT TO BUILD
- NO second gateway, NO new cages — reuse orchestrator (sessions_spawn + workboard + seat_dispatch), room.jsonl, agent_arena. Bare servers are Docker runs, not new infra.
- NO new scoring engine — reuse python-chess oracle. NO new authority path — switchboard states ARE the arena referee.
- DO NOT bake fine-tune-upload into v0 (Grey-Swan-evolution is v1/v2, per edge-not-scaling).

## 6. BABYSTEPS LAW HONORED (s-001-ea54)
v0 is the dogfood: 3-5 internal seats, prove the receipt-chain-as-referee + anti-cheat + workboard registration at $0, THEN open v1 to externals. Process first, scale second.
