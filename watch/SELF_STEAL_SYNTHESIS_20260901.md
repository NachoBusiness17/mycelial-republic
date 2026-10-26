# SELF-STEAL SYNTHESIS — dissection chair, deep self-steal 20260901

Run: 2026-09-01 ~04:3xZ. Inputs: lane A organs + lane B board + lane C seat + catalog latest.json scanned_extra grep (17 ids). All grounded in those bytes; anything else = UNVERIFIED. /mag read-only, no execution. English, tables ok.

## 1. DISSECTION — the four masks (operator 04:19Z cluster)

| Mask (class) | cmd (catalog) | gloss (origin) | duplicates TODAY in live systems | UNIQUE invariant worth stealing |
|---|---|---|---|---|
| Orchestrator flywheel `agent_os_loop` | `python -m mag.agent_os_loop` | one deterministic agent-as-OS iteration; emergent > sum of parts; operator 08-11 | fuel_feed free-lane mill + seat_dispatch already drive organic iteration — this is the declarative cousin | **deterministic-as-OS iteration as a single documented turn** — the flywheel is a repeatable turn, not an ops event; steal the turn-shape, not a new scheduler |
| Governor `governor_autorun` | `python -m mag.governor_autorun` | fill queue, plan, route, execute; MAG_DRAINER=1 smart drain instead of blind orchestrator; origin 08-11 | cron mill + worker lanes already execute; governor as a supervisor duplicates them | **queue-fill → plan → route → execute as an ordered policy** — a decide-before-dispatch gate (what lane A/B/C measure and lane C's rnd_advisor_steering was built for but never fired) |
| Scrum master `scrum` | `python -m mag.scrum` | Scrum backlog + proof-first Socratic sprint + trusted surface; operator doctrine | workboard card + board receipts + FLEET_AUDIT serve as ad-hoc backlog; no formal sprint loop | **proof-first acceptance gate on a trusted surface** — LOW-COST PROOF FIRST doctrine is doctrine-only; the *gate* is unmatched |
| Tokenizer govener `cost_simulator` | `python -m mag.cost_simulator` | estimate token spend pre-dispatch from cost_rates.yaml; planning guardrail, not billing truth | ECONOMIST_ROUTE + SPEND_AUDIT receipts (lane B) plus water_ledger + fuel are spend-tracking after the fact | **pre-dispatch cost guardrail** — the only "estimate before you fire" organ; today cost is measured post-hoc only |

Not resurrecting governor/scrum/cost as separate daemons — their DUPLICATES are warm; only their UNIQUE invariants (turn-shape, decide-gate, proof-first gate, pre-dispatch cost guardrail) get stolen into live lanes. UNVERIFIED for any claim not in a lane file origin text above.

## 2. PONYTAIL GAP — the missing hook organ (3-line spec)

- **Event-fired:** on new board write (room.jsonl tail append), on cron delivery (archivist_feed_harvest/procurement_hunter), on inbox INDEX change (index_events.jsonl seq) → fires the owning organ's activation command; currently NO organ sees these events.
- **Where:** a standing watcher seat in the OpenClaw lane (workspace/skills or a live cron tail watcher), reading board/room.jsonl tail + INBOX_LINKS + ARCHIVIST_RECEIPTS, dispatching to per-surface activators — not a Mag venv module (Mag is read-only for this seat; $0 cage side).
- **$0 validation:** `percolator_out.md` (lane B special-pass: on-new-post render, wavelength prints) is the existing one-off proof-of-shape; make percolator.mjs standing on one surface (a new room.jsonl post → ONE organ's cmd) and count 3 successful auto-fires in 24h = PASS. (Lane B: "promotable = make percolator.mjs standing on new posts (hook-shaped → ponytail gap)".)

## 3. MINING ORDER — ranked moves across all three lanes

| # | Move | Why now | Cost | Acceptance test |
|---|---|---|---|---|
| 1 | Fix memory_search recall (lane C defect: index built fts-only, wants text-embedding-3-small; `openclaw memory status --index` / `memory index --force`) | recall organ DOWN — all mining here depends on recall | $0 | memory_search returns grounded hits for a known MEMORY.md term |
| 2 | Patch archivist_feed_harvest + procurement_hunter delivery error (announce step broken: "Channel is required") | two standing systems error every cycle; file work lands, announce drops | $0 | both jobs flips to ok across 2 consecutive cycles |
| 3 | Steal cost_simulator invariant into a pre-dispatch guardrail on the existing cron mill / rnd_advisor_steering (armed-never-run) | live spend is post-hoc only; only pre-dispatch estimate organ is dormant | $0 | a dispatch wave is cost-gated from cost_rates.yaml before firing, 1 cycle |
| 4 | Steal scrum/gov proof-first gate: wire rnd_advisor_steering (lane C ARMED-DORMANT) as decide-before-dispatch consumer of the governor invariants; endpoint exists per STEERING_SYNTHESIS 02:37Z | governor queue-fill/plan/route execute + proof-first acceptance are doctrine-with-no-runner; this is the empty slot | $0 | steering job produces its first armed run, 1 confirmed receipt |
| 5 | Stand up ponytail hook organ from percolator_out.md: percolator.mjs as standing on-new-post → one organ auto-fire | sole missing mechanism for self-activation (ponytail finding); unlocks all dormant scaffold | $0 | 3 auto-fires on 3 distinct room.jsonl posts within 24h |
| 6 | Recover dormancy cheapest: UNTOUCHED_SURFACE_20260831 (23 lanes, one-command each) — pick the 3 highest-value one-command activations and actually run them | 23 dormant activations never swept (lane B #1); highest count-to-cost unlock | $0 | 3 surfaces swept → receipts, then lift the 23-lane list into a standing sweep |

## 4. CONSOLIDATION LAW (one line)

Keep dead: **scrum, governor_autorun, cost_simulator, afk_orchestrator as daemons** — their live duplicates (cron mill, worker lanes, fuel_feed, ECONOMIST/water spend) already own execution, so resurrecting them adds a second scheduler over warm systems; only their four invariants (turn-shape, decide-gate, proof-first gate, pre-dispatch cost guardrail) get folded into the existing lanes, never as new supervisors. (Lane A: dormant mass is the 609 scanned_extra, not the warm crown — and of those four, only the invariants are worth stealing.)

VERIFY: wc -l
