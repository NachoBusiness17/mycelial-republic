---
name: audit-our-way-game-medium
description: Operator directive — audits run "our way" (N-wide task fan-out, ractor panels, dogfood fleet tools, no sacred cows) and findings surface through the games medium
metadata:
  node_type: memory
  type: feedback
  originSessionId: sess_0014179a-6f14-415b-b3dd-21996c202983
---

For the 2026-09-14 full audit the operator specified: "in our way, 50 wide, touching every file, update the map relationally to ourself, sherpa the next version of us with no sacred cows — the 5 Ws, the ractors, everything dogfooded and thrown at it — and use the games as the medium to surface what you find."

**Why:** The fleet's own mechanisms are the audit instruments — ractor-style persona panels, the lane chassis, the game engine. Findings delivered as prose die (the "kifu fate: written, never rendered"); findings encoded as playable game state get walked.

**How to apply:** Fan out N tasks (this time 50) to parallel persona subagents (ractors: CLERK facts/5Ws, ARCHIVIST relations, SKEPTIC kill-list, GAMES-MASTER medium, SHERPA continuity), dogfood the fleet's tools on the repo (doctor, verkle-audit --dry, autorun --dry, shared_surface validate, pytest targeted), state no verdict without a path. Surface findings as a `mag_game_module.v1` JSON in `memory/game_modules/` — the only zero-code ingestion path into `mag/game_campaign.handle_game` (rooms=findings, encounters=dead code with hp≈KB, hooks=quoted verdicts); moves verkle-fold into world_state.json and render on the dashboard. "Launch 25/50 wide" = seed that many tasks onto `queue/lanes/<lane>/inbox.jsonl`, matching each lane's existing schema (pointer-style vs day_work-style). See [[full-audit-20260914-findings]], [[rashomon-surfacing-style]].

**Follow-up directive, same session:** "Self steal — find what you missed and broke. Do it again. Iterate on the 50." A big delivery is not done until a self-steal pass runs against it: re-read your own commits' side effects (the audit's smoke test had folded +86 lines into live world_state.json and left 2 stray campaigns), fix what broke, execute the safe kill-list items (untrack verified-dead bloat, patch doctrine lies), and re-seed the remainder. Practical gotchas learned: `handle_game` session state lives per-process — pin `campaign_id` and run the whole playthrough in one process; smoke-test folds into live verkle world_state are legitimate engine behavior but seal the campaigns and file the mutation in the commit message. See [[drift-patrol-cron-a7c71ad1]].

**Sequence directive (2026-09-14 evening, MUD ramp):** when a big ambiguous ask lands, the operator rejected the fan-out-first plan TWICE and demanded "**start with a salon about the full ask as we understand it, dogfooding, then begin**" — a 7-shape salon (blind divergence, tri-state claims, S6 fold-as-charter) runs FIRST to pin the understanding, THEN the N-wide sweep, THEN the deliverable. The salon's fold is the sweep's charter; the sweep's findings are the article's grounding. Fifty-wide v2 ran 13 witnesses under the S7 handoff card (tri-state, anchors, one-stone culture) and its charter became the next sweep's lanes. The sequence is: salon → fifty-wide → deliverable → self-steal.
