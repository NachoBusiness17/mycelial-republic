# DESKTOP PAUSE - 2026-10-17 ~21:45 EDT (deliberate, operator ask)

The operator asked to pause the desktop to play a game. NOT an incident.

**What was done:** `docker pause mag-sovereign mag-worker` (SIGSTOP, not stop/down - no
restart, no port rebind, instant `docker unpause` resume). mag-sovereign had been running
at ~101% CPU / 4.3GB (active lane/loop work); mag-worker is the 45s drain-beat.

**Left running on purpose:** gstd-node (~2% CPU, settlement rail), tortoise-db (~0.5%),
mag-mcp + mag-redis (idle), cluster-factorio (~15%, the game server), host ollama
(no models loaded, zero VRAM), llama-server (resident, carrying nothing).

**Expected while paused:** mag-sovereign and mag-worker healthchecks go stale and the
containers show `(Paused)` then may read `unhealthy` - that is the pause, not a failure.
Unpause with `docker unpause mag-sovereign mag-worker` and they recover in one health
interval (~15-30s).

**Cron note:** it is 21:43 EDT - today's MagImproveDaily (08:00), MagCensusPatrolDaily
(08:30), MagFtsIndexDaily (09:00), MagGstdDrainDaily (08:00) all already fired. Only
MagHermesBurn247 (hourly, free-lane OpenRouter ping) ticks overnight and it is a
short-lived host python doing one HTTP call - left enabled.

**Owed:** unpause when the operator says the game session is over. If the pause runs
past 08:00 EDT tomorrow, unpause BEFORE the drain cron or expect the drain to no-op and
self-heal on the next cycle.

## RESUMED - 2026-10-18 01:16 EDT

Operator called the session. `docker unpause mag-sovereign mag-worker` - mag-sovereign
came out of pause cleanly (healthy within one healthcheck interval, ~28% CPU and
climbing, 4.05GB resident). Worker heartbeat live again (beat 3189, draining).

**ANOMALY (unresolved, harmless):** mag-worker was found ALREADY UNPAUSED at 01:15,
before this seat touched anything. Cause unidentified: no repo code path unpauses it
(tools/hermes_burn.py has zero docker calls; the only sanctioned freeze tool,
scripts/lab_ctl.py, targets mag-sovereign, which stayed frozen). Candidates: a Docker
Desktop-side event during the game session or an external manual unpause. Uptime was
never reset (Up 2 days), so the daemon did not restart. If it recurs, stream
`docker events` during the next pause window to catch it live.

Net: desktop fully restored at 01:16 EDT, ~6.7 hours before the 08:00 cron wave.

## SECOND PAUSE - 2026-10-18 ~21:45 EDT (PSO-clone alpha session)

Operator: "i wanna play pause shit" (The Last Relay alpha - browser action RPG,
PSO-style). Same pause as 10/17: docker pause mag-sovereign mag-worker. PLUS two
task disables the last run did not need: MagBoxBurnNightly (its 22:00 fire was 15
min out; the CPU burner would run all night under the game) and MagProbeCadence
(the new 10-min water beat runs LOCAL ollama inference = periodic game hitches;
was mid-beat at disable - that beat dies out, no respawn). RE-ENABLE when the
session ends: schtasks /Change /TN MagBoxBurnNightly /ENABLE and /TN
MagProbeCadence /ENABLE. Kept: gstd-node (law), MagHermesBurn247 (network ping),
morning wave (hidden, fires 08:00+). Watch note: The Last Relay = PSO-style alpha
v0.1.0, operator rates it "worth watching" - relay watch continues, noindex site
+ Discord = updates land off-index.

### ADDENDUM (22:00): OLLAMA KILL - the real Friday culprit

Operator recall: "last time i played the ollama server slowed everything down."
Root cause understood: this host has NO GPU - ollama loads models into system RAM
and infers on CPU, so any lane touching the eye (stealth driver probe cycles)
hitches the machine. Fix applied: state/stealth_driver.off created (sanctioned
kill switch, driver stops at next check) + ollama.exe terminated (2 PIDs), 11434
confirmed dead. Nothing can load a model tonight. Auto-restore: boot lane
(mag_boot_lane.cmd) relaunches ollama at next logon; delete
state/stealth_driver.off to re-arm the driver. gstd-node stays headless-up
(operator fine with it).

### ROOT CAUSE FOUND + CLEANED (22:4x): THE CHURN WAS OUR OWN ZOMBIE PROBE

"ollama still churning" - truth: the athena-class probe this seat "stopped" at
~22:00 did NOT die (TaskStop killed the bash wrapper, the python child survived
on Windows). It looped `ollama run athena-class:latest` asks for an hour, each
ask reloading the 32.6GB model + respawning ollama app/serve/llama-server.
Killed: zombie python 29264 + full spawn chain (6 PIDs) + 55 headless scrum
chrome processes. Verified ZERO ollama/llama/headless-chrome remaining.
STANDING FIXES BORN: scripts/game_cleanup.ps1 (the broom: llama/ollama/LM Studio
+ headless chrome fleet) + game mode _eye_down now runs a zombie sweep (any
process holding an `ollama run|llama-server` command line dies with the eye).
Operator is right: the smith chart is the map for this - game_cleanup is its
broom; a live-process lane on the smith vislab is the standing watch (owed).
