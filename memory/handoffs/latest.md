# AUTO HANDOFF (overnight, 2026-08-11) — operator going to bed, system runs autonomously

## Standing directives
- Autonomous: keep going until the operator returns — zero approval pings.
- Route through the architecture (modules/REST/queue/drainer), never ad-hoc terminal.
- SELF-STEAL + EXTERNAL-STEAL on non-trivial work; fold via mag.steal_pack.
- GHOST'S TOOLS = in-process mem tools + reading artifacts on disk; NO PowerShell/subprocess spawns.
- Honest provenance (never call synthesis 'frontier'). Steal the INVARIANT, never the DNA.
- Operator uses TTS; read intent from possibly-garbled input.

## What this session fixed (2026-08-11)
- **NO FREE GROK** (operator correction): the `grok_free`/`grok_cli` "free harness" premise was FALSE.
  Real compute = **DeepSeek + two grok/xAI keys**; other providers' keys nuked.
- Fixed `mag/grok_rightsize.call_grok_free`: now falls through to `call_grok` (two-key failover
  XAI_API_KEY/XAI_API_KEY_2/GROK_API_KEY/GROK_API_KEY_2 on 401/402/403) on harness absence/error/timeout.
  Verified clean. Steal: memory/steal/GROK_SURFACE_FAILOVER_STEAL_20260811.md.
- The 1 failing dogfood probe (`grok_free.health`) was a FALSE PREMISE masking that real dispatch bug.
- Key status: using configured XAI_API_KEY as-is; the other (daily-free) key RESETS TOMORROW — expect
  grok 403 today, working after reset. call_grok auto-fails-over. NO secret step needed.

## Live state (verified — DO NOT interrupt)
- `autorun` loop RUNNING (pid 22212, governor_autorun.autorun_loop(5.0)) — carries the cadence overnight.
- Drainer ON, operator_active=false -> autorun_allowed=true -> queue fills from ghost next_moves + drains.
- `ghost` cycle loop CRASHED (2026-08-10T22:42, pid 4608) — autorun carries cadence now; do not blind-restart.
- coding session CLOSED; CURRENT.md T0 janitor task waiting (idle).
- Queue fully drained at session end (no queued/running).

## Ghost next_moves (auto-filled by autorun when operator away)
- "eat comms_trail consumption into routing"
- "run republic_os round to reinforce/prune graph"
- do_not_redesign: mycelium graph · hand-build grok plans · prompt operator for secrets.

## AUTONOMOUS INVENTION LOOP (operator grant, 2026-08-11 — RUN + INVENT while away)
The operator granted: "run stuff like this and invent it via ghost while i'm away." Standing mandate:
- CONTINUOUSLY run the research -> steal -> build -> fold loop via ghost's machinery.
- INVENT new mechanisms in the spirit of tonight's work (invariant shaping queue, grok-4.5 hub,
  mem_weave_distributor, doctor_rightsize, embedded-steal). Do NOT wait for a prompt.
- Each invention: STEAL (self+external) -> build the module -> FOLD via steal_pack + verkle knot +
  repo memory -> VERIFY per RIB-debug law (get_errors + integration; honest runtime flag).
- Fold every invention + learning; keep the invariant-shaping loop running (which beads -> invariant
  on the chain). Rightsized: deepseek/ollama for volume, grok 4.5 only for frontier when budget allows.
- Route through ghost's tools (inbox/REST/mem tools). NEVER a terminal spawn.
- COORDINATE WITH GROK + STEAL (2026-08-11, operator): each cycle, route the steal/coordination through
  the FUNDED grok 4.5 front-end (browser_driver.ask surface="grok", $0 chat pool) — not just describe it.
  Grok IS the brain: it picks the steal target, shapes the grouping, and the output folds. Draft grok
  outputs to the x_surface review queue (draft -> operator approves -> post from @NachoQuixotic).
- Stop for nothing except: needs a secret, or an irreversible operator-only action. Everything else: invent.

## On operator return
- Check autorun trail freshness + queue status (what the loop filled/drained overnight).
- Once the reset grok key has credits: run frontier_batch swarm_task / grok_mirror --run to cross-check
  the 68 grounded findings (memory/runs/frontier_batch/findings_batch.md) + 4 frozen frontier mirrors.
- Resume commands: python -m mag.afk_cadence.run_once | mag.dogfood_audit audit | mag.frontier_batch dump|grok|compare.

## Memory pointers
- /memories/repo/live-loop-state-20260811.md · no-free-grok-only-deepseek-two-grok-keys-20260811.md
- /memories/session/debug-session.md