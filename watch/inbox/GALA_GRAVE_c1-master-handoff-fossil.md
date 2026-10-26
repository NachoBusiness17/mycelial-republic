# GALA GRAVE: HANDOFF_MAG_AGENT_TODOS.md buried as FOSSIL

Lane: c1-master-handoff-fossil (division C, GRAVEDIGGER, THE GALA battery, night of 2026-09-25).
Verdict: **FOSSIL as of 2026-09-25.** The file stays on disk at the repo root; this is a receipt-only burial. Nothing was deleted or edited.

## What the handoff was

`HANDOFF_MAG_AGENT_TODOS.md` (repo root), commitment `handoff-mag-agent-todos-001`, stamped **As-of 2026-08-05**. It was the single operational handoff of its era: merge order for PRs #8 through #11, Verkle audit automation, the A1-A12/P/B agentic steal list, reconciled open tickets, the v2 phase checklist, the seat transition of 2026-08-05 (Cursor cloud access ending, DeepSeek + Grok + Ollama forward stack), and the multi-seat build factory plan.

## Staleness evidence (all commands and raw output: `watch/inbox/gala_20260925/w2/lanes/c1-master-handoff-fossil.check.txt`)

- File last touched by git: `1c156e2fa 2026-08-06 "Checkpoint Direct Mag cheap handoff control plane"`. Today is 2026-09-25: about 7 weeks with no update while HEAD sits at `a741defc5 2026-09-25`.
- Its own activation framing ("v2 ships when merge #8-#11 land") is overtaken: all four branches are ancestors of HEAD, so the entire "do first" section is finished work.

## Per-item disposition

| Item in the handoff | Disposition | Evidence |
|---|---|---|
| PR #8 unified router (`cursor/unified-router-e2ce`) | **MERGED** | `git merge-base --is-ancestor cursor/unified-router-e2ce HEAD` exits 0; commit `43d4e689c 2026-08-04 "Add unified router with honest failures and routing smoke"`; `tests/test_router.py` on disk |
| PR #9 Failure KB (`cursor/failure-kb-e2ce`) | **MERGED** | ancestor of HEAD (exit 0); `f462b3986 2026-08-05 "Add Failure Knowledge Base (FKB) with agent and pack wiring"`; `tests/test_failure_kb.py` on disk |
| PR #10 Mag Autorun v1 (`cursor/mag-autorun-v1-e2ce`) | **MERGED** | ancestor of HEAD (exit 0); `0af61c1c1 2026-08-05 "Mag Autorun v1: intelligent drainer + operator pause + FKB wiring"`; `tests/test_autorun_v1.py`, `mag/governor_autorun.py` on disk |
| PR #11 v2 plan + verkle-audit (`cursor/mag-v2-plan-e2ce`) | **MERGED** | ancestor of HEAD (exit 0); branch tip `e8d75c33c 2026-08-05`; `mag/verkle_audit.py`, `tests/test_verkle_audit.py` on disk; verkle-audit is a standing command per AGENTS.md |
| Verkle audit automation (MagImproveDaily / MagVerkleWeekly / autorun fill) | **SUPERSEDED, partially still live** | `MagImproveDaily 08:00` is current doctrine in AGENTS.md; the 2026-09-25 regime adds the ratchet gate, workflow gate, and freshness gate (AGENTS.md "Build discipline"); verkle tip repaired under operator GO in `544bc7b84` |
| Agentic steal list A1-A12 / P1-P3 / B3, B5, B6 | **MOSTLY SUPERSEDED** by later receipts: guardrails, compaction (context-pack), promote gate, human-in-loop, tracing all shipped as standing doctrine (AGENTS.md commands). Open-listed items (MCP surface, workspace-per-seat, trail replay, hierarchical memory) were NOT individually verified in this lane; the living queue is `queue/todo.md` and the living ledger is `docs/ref/MAG_v3_BACKLOG.md` | receipt-only claim: no per-item check run here |
| Open tickets O3 (n_leaves >= 20), 2.0 (verify-leaf) | **STILL-OWED, moved where**: `queue/todo.md` + `python main.py verkle-audit` reconcile (not re-run in this lane, so status not re-verified) | |
| Roadmap tickets A2-A4, B1-B2 | **SUPERSEDED / absorbed** by v2+ merges and later phases; not individually re-verified | |
| v2 phase checklist (phases 0-5) | **SUPERSEDED**: repo is far past the v2 gate (seed v3.3.0 per `watch/inbox/SEED_WINDOW_CLOSE_20260925.md`; version arc in `configs/version_roadmap.yaml`, `docs/ref/releases/VERSION_REGISTRY.md`) | |
| Section 9 seat transition (2026-08-05 stack: DeepSeek + Grok + Ollama) | **SUPERSEDED** by the current tier ladder in AGENTS.md (ollama -> free tiers -> deepseek flash -> pro/grok; thinking-mode axis; fan-out width law) | |
| Section 10 virtual desk + v3 research pointers | **SUPERSEDED** by `docs/ref/MAG_v3_BACKLOG.md`, `docs/ref/MAG_V3_DISPATCH_PLAN.md`, and the 2026-09-25 interference-search replication (boot lane STATE in `memories/session/next-window-handoff.md`) | |
| Section 11 build factory pilot epics (1-3, all "draft/not started" on 08-05) | **SUPERSEDED / folded** into the factory run this branch is named for (`mag/run-beta1-factory-build-audi-20260806T231709Z`) and the build discipline of 2026-09-25; epic-level status not re-verified | |
| Test ritual (section 6, "39 deterministic green" era) | **SUPERSEDED**: the fossil count is called out in AGENTS.md Clippy (1,341 tests / 264 files census 2026-09-14; 1305 passed / 34 failed / 9 skipped; "never trust a hand-written count") | |

## What superseded it

1. `memories/session/next-window-handoff.md` (exists since 2026-09-15, states "This IS the spec now"; STATE entries updated through 2026-09-25 boot lane) is the activation and procedure of record for new windows.
2. `watch/inbox/SEED_WINDOW_CLOSE_20260925.md` is the most recent window-close handoff of record (seed v3.3.0, evidence arc, standing burns).
3. `AGENTS.md` build discipline (2026-09-25) + `AGENTS.md` Clippy block carry the standing laws this file's sections 2/3/6 tried to carry.
4. `queue/todo.md` is the living queue; `docs/ref/MAG_v3_BACKLOG.md` is the living feature ledger.

## Burial verdict

**FOSSIL, buried 2026-09-25.** The file's only forward-looking content (merge #8-#11) verifiably landed on 2026-08-04/05, seven weeks ago; every other section has a named living successor. Do not activate from this file. New windows load `memories/session/next-window-handoff.md` instead.

Note: AGENTS.md still lists `HANDOFF_MAG_AGENT_TODOS.md` in its load order ("if implementing"). That pointer is operator-gated to change and is left untouched by this lane; the grave receipt is the correction of record.

## Receipt-only law

The file `HANDOFF_MAG_AGENT_TODOS.md` remains on disk at the repo root, byte-identical (commit `1c156e2fa`, 2026-08-06). Deletions are operator-gated; this lane buried nothing by removal.
