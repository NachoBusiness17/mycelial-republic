# Steal card: swarm-orchestration (frontier olm 2026-10-03)

Area: swarm-orchestration. Four confirmed finds, all supplied by the ask's confirmed-finds payload (Hacker News via hn.algolia.com API + news.ycombinator.com threads). Newness re-verified this session: `git grep -il` over the four finds' probe strings against tracked `catalog/` + `memory/` returned empty output (0 hits), matching each find's overlap claim.

## Find 1: agent-limit-retry, the salvage-failure census (HEADLINE)

- Source: https://news.ycombinator.com/item?id=49831324 (2026-09-24)
- Evidence (from the ask): 449 subagents cut off by usage limits, 8 resumed by id (all 8 before the reset, so they died again), 438 redone from scratch. The working mechanism: read `quotaLimits.resetsAt` from transcripts, write a handoff file at 90% usage, sleep to the reset, `--resume` the same session.
- Why headline: 97.5 percent of limit-killed work (438 of 449) was redone from zero. Salvage without reset-awareness is theater, measured in public at scale across 6 sessions.
- Estate map: gopher fleet + the workflow gate's G4-salvage check, `tools/workflow_gate.py:62` ("incremental report() inside the fan-out (work survives a dead run)"), which every gated workflow must pass; the latest registry row shows G4 ok:true (`memory/workflows/REGISTRY.jsonl`, last row, ractor-engine.dwf.ts 2026-10-02). The find names the half G4 lacks: G4 salvages partial OUTPUT, it never resumes the CHILD. Port move: on a limit-kill, the lane writes a handoff checkpoint (the lane runner_state already is one: `queue/lanes/builder/runner_state.json:2-6` holds inbox_offset, last_run, last_result, seat), reads resetsAt from the provider error payload, and re-enters the same child id after the reset instead of re-fanning.
- Honest nuance: the estate's width law deliberately runs workflow children at maxAttempts 0, die on first 429/1302, with Task agents riding the main-session retry path (`AGENTS.md:33`). Die-fast is a chosen retry strategy, not an accident. The probe below is what decides whether reset-aware resume has prey on this estate or stays a confirmation receipt for die-fast.

## Find 2: TCC durable execution, committed continuations without history replay

- Source: https://news.ycombinator.com/item?id=49635621 (2026-09-09)
- Evidence (from the ask): on crash, a fresh runtime loads the checkpoint, reconstructs the frame, and dispatches directly to the saved position, no history replay; measured 0.6-0.9ms flat versus a Temporal replay baseline growing from ~61ms to 1.7s over 50,000 generated cases; a Temporal SDK maintainer banked ~3.45B actions/month scale in-thread.
- Estate map: water graph / lane durability. Lane runner_state files already are committed continuations (`queue/lanes/builder/runner_state.json:2-6`). Port move: make lane resume dispatch to the saved position by default and demote trail.jsonl replay to fallback, then mint the percolator invariant "committed continuations at durable boundaries; replay is the fallback, not the default" into `memory/percolator/invariants.json` (invariant shape confirmed at `memory/percolator/invariants.json:3-13`: text + count + first_seen + decay_as_of).

## Find 3: what broke when you added the second agent

- Source: https://news.ycombinator.com/item?id=49924268 (2026-10-01)
- Evidence (from the ask): practitioner failure mode, inconsistencies/mistakes/bad assumptions/side quests compound across multiple agents with no human-in-the-loop breakpoints; default to a single implementation agent unless the ask justifies width.
- Estate map: percolator + deliberate-ask doctrine. Independent public confirmation of the estate's deliberate-ask plus interagent pass-off pair (the pass-off half is gate-enforced at `tools/workflow_gate.py:50-54`, G2-passoff). Port move: mint a candidate invariant in the percolator shape, "multi-agent asks carry a named pass-off breakpoint per hop; default single implementation agent unless the ask justifies width". Mint is the safe leg: I did not exhaustively check whether an equivalent invariant already exists in `memory/percolator/invariants.json` (read the first 60 lines only).

## Find 4: no organic thousand-agent fleets in production

- Source: https://news.ycombinator.com/item?id=49689454 (2026-09-13)
- Evidence (from the ask): no organic 1000s-of-agents production takeup surfaced, only OpenAI/Anthropic staff and vendors selling; the thread's only named stack is pods-per-N-agents with OTel+Prometheus observability.
- Estate map: quantizer / sovereign mirror positioning. Counter-signal receipt: the estate's measured envelope (width 10 Task agents, 109.4M tok/h, zero surfaced 1302s, `AGENTS.md:33`; receipts `watch/inbox/gala_20260925/AFTERPARTY_CLOSE_20260926.md` B2-476 amendment and `watch/inbox/burn_wave_20260926/B2_443_dwf_error_census_20260926.md`) is ahead of public practice. Port move: bank as a positioning receipt in the sovereign mirror dossier with the dated claim "no organic thousand-agent production fleet is publicly documented as of 2026-10-03".

## Headline probe (falsifiable, cheap, this week)

Run the estate's own salvage census, one grep pass: scan `queue/lanes/*/trail.jsonl` (and secondarily `memory/workflows/REGISTRY.jsonl`) for limit-kill markers (429, 1302, quota, usage limit) over the trailing 14 days, then classify each terminated child as redone-from-zero versus resumed-from-checkpoint (a runner_state advance or a G4 report() salvage row).

Feasibility grounded this session: markers exist in the corpus. `git grep -ci -e "429" -e "1302" -- queue/lanes memory/workflows/REGISTRY.jsonl` returned: elder trail 15, elder surface 21, elder inbox 1, harvest trail 12, research trail 722, research surface 1, research inbox 1, and zero hits in REGISTRY.jsonl itself (the registry carries gate verdicts, not provider errors, so the census lives on the trail files). Those counts include prose mentions, which is exactly what the census has to classify; the classification has NOT been run yet, so this stays an open probe.

Falsifier: fewer than 5 genuine limit-killed children in the window means reset-aware resume has no prey this week and the port defers to a die-fast confirmation receipt; a redo share above 50 percent reproduces the 438/449 shape and greenlights the handoff-file port into the lane runners.

## Secondary probes (banked, not the card probe)

- TCC: time the fattest lane's resume-from-tail replay (research lane's trail is the likely fattest, 722 marker hits); if resume is already under 10ms at current trail sizes, the replay-fallback invariant is premature and the port is falsified at today's scale.
- Find 4: one targeted search pass for an organic production fleet citation; a single counterexample falsifies the no-fleet claim.

## Session grounding ledger

- `git grep -n -i -e "salvage" tools/workflow_gate.py` → tools/workflow_gate.py:17, 62
- `git grep -n -e "109.4M" -e "maxAttempts" AGENTS.md` → AGENTS.md:33
- Newness grep (all four finds' strings, catalog + memory) → empty output, 0 hits
- `git grep -ci -e "429" -e "1302" -- queue/lanes memory/workflows/REGISTRY.jsonl` → counts above
- Read `memory/percolator/invariants.json` (first 60 lines) and `queue/lanes/builder/runner_state.json` (whole file)
- Not run this session: the salvage census itself, the TCC replay timing, the Find 4 fleet re-search (all named as probes, not claimed as done)
