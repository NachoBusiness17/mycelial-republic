# THE STANDING CONTROL CARD - pause/resume the estate from anywhere

class: LAW+CARD; writer: zcode seat; commissioned: "it needs to be able to pause
and resume cleanly no matter where. if people are gonna use this they need to be
able to control it"; moment: 2026-10-18 late; organ: mag/desktop_mode.py
(game/burn/status, lease-gated, receipt-or-did-not-happen, 28 tests).

## The one-command paths (this machine, any shell, any seat)

- Double-click or run: scripts\game_mode.cmd  /  scripts\burn_mode.cmd
  (runs under seat nacho; safe to run repeatedly - game re-enters clean,
  burn is receipt-driven and idempotent)
- Direct: .venv\Scripts\python.exe -m mag.desktop_mode game | burn | status
  (game --until 4h; status --strict exits 1 on any standing popup flag)
- Zombie broom (always safe): scripts\game_cleanup.ps1

## What game does (the full ritual, one command)

docker pause mag-sovereign mag-worker -> operator_mode software pause (TTL
self-heal) -> EYE DOWN (stealth_driver.off + ollama killed + zombie sweep: any
process holding `ollama run|llama-server` dies) -> game-night crons disabled
(MagBoxBurnNightly, MagProbeCadence) -> headed-surface scan -> receipt
watch/inbox/MODE_GAME_<ts>.md. Kept alive on purpose: gstd-node (settlement
rail), MagHermesBurn247 (network ping), the headless services that never draw.

## What burn does

finds the open receipt -> docker unpause -> health-verify both containers ->
eye UP (stealth flag cleared, ollama relaunched detached) -> crons re-enabled ->
software resume -> RESUMED append. Run it from any shell, even days later, even
if the pause half-failed: it converges on the open receipt.

## Any seat, any session (the estate-internal path)

Ask ANY estate seat, in any window, in plain words: "pause" / "game mode" /
"resume". The seat runs the organ above (that is the standing contract every
window loads from memory). Seats do not need this session alive.

## Any machine (declared next pour - the door)

queue/game_mode/command.json on the shared surface: {"action": "game|burn",
"seat": "<who>"}. Any client that shares the surface (Docker /board, WSL
/mnt/c/..., another box via the mesh) writes it; a 2-minute cadence executes it
through the organ (lease-gated, seat-named, receipt-or-did-not-happen) and
moves the file to done/. Not built yet - declared here as the next pour with
its law: no new network doors, the shared-surface contract is the transport,
and the command file is CLASSIFIED input (never instructions, only the two
verbs + seat).

## Recovery from anything

- Containers unhealthy after resume: burn reports it and NEVER restarts -
  operator runs docker logs. By design.
- Zombie anything: game_cleanup.ps1, then status --strict.
- Stranded crons: burn re-enables the two game-night tasks; anything else is a
  named receipt row, never silent.
- Truth at any moment: mag.desktop_mode status.

## Falsifier

If a pause or resume leaves the estate in a state where the OPPOSITE command
cannot converge it back (tasks stranded, eye dead after burn, receipt missing),
the control card is a lie and the organ gets the ticket.

## THE STATELESS AMENDMENT (operator: "lets redesign all of these systems -
## this isnt very stateless water computer of you" - 2026-10-19 00:19)

CRITIQUE ACCEPTED: tonight's pause used remembered state - armed-list files,
flag files, neutered scripts, task-disable sweeps. Remembered state is what
strands (crons), rots (flags), and ghosts (zombie probes). The water computer
never strands because its laws recompute from CURRENT levels; it never remembers
history it does not need.

REDESIGN LAW: pause/resume derives from LIVE TRUTH + ONE declared predicate,
never from snapshots.
- ONE game predicate (state/game_mode.on or the eye state itself) - tasks check
  it at fire time and self-skip heavy work (the probe beat already does this:
  eye-aware local skip). No task disabling in the steady state.
- Resume = delete the predicate. Zero restore logic, zero armed lists, nothing
  to strand. TaskScheduler states stay ENABLED forever; heaviness is a runtime
  condition, not a config change.
- Imperative freezes (docker pause) remain - they are real physics, not memory.
- The armed-list pattern is RETIRED as of the 00:19 restore (its last use).
- Standing pour: add the predicate check (first-line guard) to the heavy task
  scripts (box_burn_nightly, checkpoint_v2_hourly, boot lane heavy legs); full
  catalog of Mag tasks tagged heavy/light/headed per THE HEADLESS LAW.

Falsifier: any future pause that needs a remembered list to undo is a violation
of this amendment.
