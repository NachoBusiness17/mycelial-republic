# AUDIT — working vs intended (2026-08-24, grounded from code + feed + terminal)

Operator intent (session 7e653ed7): "use these fucking seats instead of looking at them,
make the dashboard not suck, be stateless not a cron job."

Machine state (team_knot.feed + loop_health, verified):
- cpu ~91% busy · loop_health overall = degraded · seats 5/7 up · cadence idle 85 min.
- lab + dashboard peg ~100% CPU; autorun 0%. This is the SAME CPU-spin that got shelved.

## WORKING (verified, real bytes)
| Component | Evidence |
|---|---|
| Provider lanes (deepseek, nvidia, openrouter, together) | keys present; nvidia chat verified end-to-end (deepseek-v4-flash-0731, 3.4s) |
| Seats 5/7 available | grok-nacho, grok-sd, ox-account2, deepseek, openrouter-lanes |
| ox_resident --drill 8 | exit 0 (one-shot, completes) |
| cadence_learn, real_swarm, loop_health, fleet view | per shelved record, verified working |
| team_knot (shared reality + feed) | built + anchored (leaf f08483e1, root e3e9c077) |
| NVIDIA build key | 102 models, 18 wired, default deepseek-v4-flash-0731 |

## NOT WORKING (the gap)
| Intended | Actual | Cause (grounded) |
|---|---|---|
| ox runs steady to USE the seats | ox watch/swarm/megaburn exit 1 | Both watch() loops are designed to NEVER exit (catch-all + loop). exit 1 = EXTERNAL KILL, not code error. The CPU-ceiling governor kills mag processes pegging >70% — it whacks the long-running ox loops; --drill 8 survives because it's one-shot |
| machine has room / stateless, not cron | cpu 91%, degraded | lab + dashboard spin ~100% (shelved carrier problem, prior lead: drain_once ~15s on empty queue; plan_pending/reconcile every tick) |
| cadence fires | idle 85 min | the carrier spinning starves the cadence; or the cadence itself isn't scheduled while the loop is shelved |

## THE CHORD (one root cause, one gap)
The seats CAN'T be used because the machine is pinned at ~91% by the carrier spin, which
(a) leaves no room and (b) trips the CPU ceiling that kills the steady ox loops. The operator's
intent ("use the seats") is blocked by the shelved carrier's CPU spin. Fix the spin and ox can
run steady without being killed, and the machine has room.

## Highest-value gap-close (ranked)
1. Root-cause + stop the carrier spin (governor_autorun.autorun_once -> plan_pending / drain /
   reconcile each tick; prior lead: drain_once ~15s on EMPTY queue). This unblocks everything.
2. Let ox watch loops run only when machine has headroom (respect the CPU ceiling) instead of
   being silently killed -> surface "killed by cpu ceiling" honestly in the feed/health.
3. Wire team_knot.feed into the chat window default (done) + into the dashboard so it's the
   standing read anywhere.

## Open items / not root-caused (honest)
- Exact line of the carrier spin (plan_pending vs drain_once vs reconcile) not yet isolated —
  needs one focused read of governor_autorun.autorun_once + orchestrator.drain_once/plan_pending.
- Whether cadence idles because the loop is shelved or because the spin starves it.
