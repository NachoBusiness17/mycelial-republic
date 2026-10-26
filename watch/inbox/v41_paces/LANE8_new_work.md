# LANE 8/8 — NEW WORK DISCOVERY: the undone list, ranked

Date: 2026-09-11 (box 09-10) | Lane: discovery only — no building, one file.
Sources: watch/inbox/SESSION_ORPHANS_20260911.md (28 orphans), watch/LIBRARIAN_REPORT.md
(1,893 docs audited), TODO-grep of 10 newest mag/*.py, NEXT STEP sweep of all inbox
cards from the last 48h, CONVO.md tail (tonight's operator asks).

## THE POINT

The operator said "find new shit to do." Here it is: the code layer is CLEAN (zero
TODO/FIXME/HACK in the 10 newest mag organs) — every loose end lives in the cards.
Twenty-two pieces of unfinished work are registered and unclaimed. Five are one-sitting
fixes on standing systems (the chain janitor, the librarian, the skill). The biggest
staged item is the retro-knotter read-only step — half the night's discovery (21,479
lost knots) is still waiting to be folded into the index. Everything gated on operator
GO is listed separately so the free work is visible at the top.

## RANKED — the operator would want these next

Rank rule: standing-system fixes first (they compound), then record work (the moat),
then spec'd-but-unbuilt organs, all free-lane, all inside the build freeze (cards and
small organs only).

| # | Task | Source | Effort | Impact |
|---|------|--------|--------|--------|
| 1 | **Chain janitor fix pair**: (a) `verkle_audit --fix` flag doesn't exist — the one auto-healer has been firing at a missing switch; (b) sweep the `except-Exception: pass` swallower pattern that silently dropped 145+ knots for 5 days | CONVO 09-09T17:10Z "STILL OWED (c)" | S | The chain's self-heal actually works; kills the silent-drop class at its exhibit #1 |
| 2 | **Retro-knotter step 1 (READ-ONLY)**: verify the orphan ledger landed in estate-index data; stage step 2 as the GO-gated card. 21,479 off-chain knots + 5 days of unknotted sessions depend on this path | CONVO 09-09T16:15Z + NIGHT_FOLD; MORNING_REPORT "retro-knotter GO (staged)" | M | The lost-record find becomes usable record; step 2 is one operator GO away |
| 3 | **Librarian v1 upgrades + triage**: PULLED/HASHED state per row, Tier-3-first sort, triage the 192 unregistered citations top-cited-first, consult-or-cut the 27 dust rows (5 rows also lack status stamps: row48/65/79/88/97) | LIBRARIAN_REPORT v0 + ORPHANS #6,9,10 | M | The bibliography becomes a real instrument; 192 zombie citations become registered or cut |
| 4 | **File the playbook-first dissection law in the corrections skill**: every dissection wave OPENS with "which named playbook does this match" (Bezmenov/Bernays/AGM/Goodhart) before firing fresh masks | WRONGTHINK_ROW_SEEDWAVE_20260911 meta-row | S | Stops re-running dissections the record already holds; law is stated but not yet in the skill (same gap moon-speak had) |
| 5 | **Gateway wiring**: 4 tools (padout, invariants, bibliography, kvos stats) onto mag/mcp_http.py — backup-first | ORPHANS #4 | M | Spec'd organs become reachable from the workspace; MCP topology already closed and proven |
| 6 | **Registry generalization**: seed the 5 registers (claims-witness, falsifier ledger, datasets, decisions, model pins) | ORPHANS #5 | S-M | One registry shape instead of five ad-hoc ledgers |
| 7 | **DSV4.1-Flash desk follow-through**: pull full benchmark tables from the 51pp report (tri-state the K3 claim); dig the `encoding/` folder in the HF repo; draft the Rocinante sizing note (4-bit/FP8/FP4-KV ladder, memory map per Studio, llama.cpp/MLX CED+Engram timeline) | DESK_DSV41FLASH_20260911 Next steps | M | Rocinante (Oct 27) gets its runtime plan early — "the runtime is the long pole, not the memory" |
| 8 | **Dogfood the Sep-4 eight-page visual deck set**: verify they still render, retire or refresh | DESK_DOGFOOD_VISUAL_DECK_20260911 Next steps | S | The desk's own surfaces stop rotting silently |
| 9 | **Perplexity follow-up feed**: one free-lane prompt post-wave ("from these findings, 5 follow-up queries") so follow-ups stop dying in fold cards | steal_research_pipeline/BOT_A_perplexity.md row 6 | S | Every wave self-generates its next wave |
| 10 | **Ghost autonomous_fixes probe**: did the orc asks actually execute — checks whether hollow-mass bodies were real work | GHOST_AUTONOMOUS_FIXES_PROBE_20260911 "next probe" | S-M | Closes the hollow-mass question with a receipt |
| 11 | **Seat-pool mining lanes**: .grok 411MB transcripts + .codex 634MB rollouts + proto-era vault dating — filed as "new top lanes for the standing cycle's next tick", not yet ticked | CONVO 09-09T19:21Z SEAT POOLS RESCUED | M-L | The silence window gains its fifth witness in depth; founding-week record |
| 12 | **Percolator v2 refutation column** (scite steal) on invariant_surface | ORPHANS #7 | S-M | Invariants become falsifiable-in-place |
| 13 | **Cascade stopping + academic mask in the research seam** (Perplexity steal) | ORPHANS #8 | M | Research waves stop spiraling; already spec'd |
| 14 | **LMCache prefix-sharing receipt mining** (free lane) + Raschka writeup read (math wing pile) | DESK_FOLD_ZEITGEIST_WAVE_20260911 triage rows | S | Cache-identity moat gets its primary-source receipt |
| 15 | **Slipstream compaction judge spec card**: async summary validated against the agent's actual next steps — we already hold the ground truth (trajectory envelope + GROUNDING_WAVE chain). Spec only during freeze | NIGHT_EXTERNAL_MEMORY_20260911 | M | Compaction becomes verified, not trusted; measured +8.8pp/-39.7% in the wild |
| 16 | **Grok canon summon fusion**: 12 dated entries retrieved, strikes drafted (3 fired?) — finish folding into the standing strike corpus | ORPHANS #12 | S | Canon work stops dangling half-fired |
| 17 | **Defense-factory invariant rows**: file OPEN-WEIGHT-AS-THREAT in the wrongthink map; log the defender's-window chart for the coastline index; read the HF forensic timeline | DESK_DEFENSE_FACTORY_20260911 Next steps | S | Enemy doctrine becomes map rows before it hardens into policy |
| 18 | **KPI re-knot pass**: 192 orphaned knot files with leaf_hash+session_id (73-minute transient resolved, content recoverable) | KPI_LEAVES_RECON_20260911 | M | Chain-adjacent record completeness |

## GATED — staged, waiting on operator word (not free work; listed so they don't rot)

- Eye dark: host ollama down since before 07:46 — ONE command, awaiting word. (ORPHANS #17)
- Retro-knotter step 2 GO — needs truth-gate append-lock + second witness first. (CONVO 17:10Z)
- MAX_DISTILL epoch 2 — spec filed, awaiting GO; transport gate = flywheel valve. (MAX_DISTILL_EPOCH2_SPEC)
- HOLD 2 launches (6 irreducible + 6 sham instances) — file-work, gated on coldest-vertex read. (CONVO 18:38Z)
- Lane 2 replication organ (~100 lines, build GO); Lane 7 live cost fires ($0.25 cap, spend GO); Lane 8 runtime call (V4.1 port vs V4-Flash GGUF); Lane 4 P3 streaming+72h retention. (ORPHANS #13-16)
- Beacon dawn reading — the gate; waits on the operator's voice, nobody else's. 
- Attribution ruling: Bernays (headerless) vs loudness doctrine (the name is the point). (FIRST_SCRUM_SPRINT open contradiction)
- Cynthia round-2 strikes — operator fired or not, unconfirmed. (ORPHANS #11)
- V4.1 API probe when live (price, cache discount, vision). (DESK_DSV41FLASH)

## COUNTED / in work (not re-listed)

ACTIVE orphans #1-3 (fish-horse ID, free-lane game build, Claude sandbox triage) are
already picked up; COUNTED #19-28 closed as dust.

## Method note

- mag TODO grep: 10 newest files (fire_horse, librarian, invariant_surface, kvos_block,
  burn_steer, space_ear, telegram_desk, thread_eye, ractor_vessels, percolator) —
  0 hits. Finding: unfinished work is registered in cards, not littered in code.
- 48h inbox sweep: 8 cards carry NEXT STEP/TODO directives; all folded above.
- Box clock skew observed (files stamp 09-10, operator date 09-11) — both on record.
