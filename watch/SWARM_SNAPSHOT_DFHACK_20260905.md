# SWARM SNAPSHOT — DFHACK DAY ONE (Sep 5, 2026)

*Operator: "we downloaded the flash model to the harddrive — how can we use our swarm flash
snapshot using vision to give us a better understanding of our environment… api, behavioral
data, the full archeology… then think about dwarf fortress and dfhack."*

## THE FRAME (why Dwarf Fortress is the right map)
Dwarf Fortress is a living simulation the player can only see through overlays; **DFHack is
the third-party lens that reads the game's RUNNING MEMORY and renders what the engine knows
but doesn't show** — dwarf thoughts, pathfinding, hidden events. The fleet is the same shape:
a living system (seats, lanes, chains, rituals) whose true state lives in memory surfaces the
operator can't casually see. **Our DFHack already exists — it's our own toolsets pointed at
ourselves:** db tables = process memory, room.jsonl = the announcements feed, the chain = the
engravings, the trajectory envelope = the thoughts screen.

## THE DFHACK MAPPING (our toolsets → fortress overlays)
| DFHack | Fleet organ (exists / day-one) |
|---|---|
| reveal (unhide the map) | **mag/swarm_snapshot.py** — the fortress board (built today) |
| look / k over a tile | auth_switchboard status — inspect any lane at the bytes |
| thoughts screen (dwarf moods) | the trajectory envelope / thought-bank (9,305 parts) |
| announcements feed | watch/room.jsonl (5,905 events in-window) |
| engravings / history | verkle chain (7,269 knots) |
| autopsy (death cause) | window-death class cards, incident forensics |
| workflow manager | automations registry + night shift (a5e12eea) |
| heat map (stress) | errors/day panel + burn board |
| prospect (what's in the rock) | the corpus + library (555 cards in 14d) |

## WHAT WAS BUILT (same turn, $0, all local)
`mag/swarm_snapshot.py` — collect → render → read → bank:
- **collect**: 14 days from the memory surfaces — model_usage (burn by model/agent/day +
  error counts), distinct sessions/day, room.jsonl events/day/seat, chain knots/day, cards/day.
- **render**: one 960x640 PNG fortress board, 4 panels (burn stacked bars / seats+error
  ticks / room events / chain knots), stdlib PNG (technique stolen from burn_steer — sacred
  cow reused). No text drawn: **the eye reads pattern, the digest anchors numbers.**
- **read**: the local vision model on the drive (ollama **qwen2.5vl:3b**, 3.2GB) gets board +
  digest together and reports shape, anomalies, one recommendation.
- **bank**: memory/runs/swarm_snapshot/<ts>/ (board.png, digest.txt, vision_read.md).
- Fence: ollama endpoint allowlisted (loopback-only, fleet law), Mimosa-gated.

## FIRST LIGHT — WHAT OUR OWN MEMORY SHOWS (the digest, 16:31Z)
- **3.6B tokens in 14 days** on this seat alone; 5.3-Flash 1.94B vs GLM-5.3 1.62B — and the
  **model handoff is visible in the bars**: 5.3 carries 378M on 09-04, then 0.0 on 09-05 while
  Flash carries 320M. The pool-death → promo switch is IN the data.
- **834 errors in 14 days** — the tantrum-spiral indicator, now measured daily.
- **5,905 room events, 7,269 chain knots, 555 cards in 14 days** — the fortress is LOUD.
- Only 3 seats burned — this meter reads THIS seat; other seats' meters are their own dbs
  (the multi-seat fan law, visible in the data).

## THE EYE CALIBRATED (falsifier run 1 — honest table)
| Overseer claim (qwen2.5vl:3b) | Verdict vs digest |
|---|---|
| Burn rising with spikes; Flash+5.3 dominate | **SUPPORTED** |
| "Peaks on days 10, 20, 28" | **REFUTED** — no day 28 in a 14-day window |
| "Day 5 seat spike; day 10 zero room events" | **REFUTED** — not in the data |
| Missed the real anomalies (two zero-days, 834 errors) | **MISS** |

**Verdict: the 3B eye reads SHAPE (rising/spiky/stacked) at better than chance but
hallucinates specifics — it's an overseer's glance, not an accountant.** Standing design law
from this: deterministic code owns NUMBERS, the eye owns PATTERNS, and every eye claim gets
scored against the digest before it steers anything. Upgrade path when needed: a text-capable
7b pass over the digest (qwen2.5:7b, on the drive, 24h fresh) + the 3B eye on the board, two
keys of the same chord.

## FALSIFIERS STANDING
1. Eye-vs-digest scoring every run (today: shape SUPPORTED, specifics REFUTED — recorded).
2. The board must change visibly when the fortress changes (a quiet day must LOOK quiet).
3. $0 forever: every surface read is local; the only model calls are on-disk weights.

## NEXT RUNGS (DFHack roadmap, continue this card — never a sibling)
1. Burn-by-agent split panel (model_usage.agent) — who's carrying the fortress.
2. ~~Serve the board on dashboard/static~~ DONE (second dogfood 16:37Z: HTTP 200 + nav.js "Swarm Board" wired).
3. thoughts-screen overlay: trajectory envelope counts/day beside chain knots.
4. Weekly overseer read in the night shift's morning brief (the eye rides the 23:00 pass).

## SECOND DOGFOOD (16:37Z, same hour — the board eats its own birth)
- **Falsifier 2 PASSED — the board moves when the fortress moves:** between two runs minutes
  apart the census ticked room 5905->5906 (the room row this arc landed), chain 7269->7270 (a
  knot sealed), cards 555->556. Self-observation is real, not decoration.
- **THE TANTRUM IS VISIBLE:** errors/day series `... 86 133 216` — today's 216 = window
  maximum, 3.6x average. The auth swap, the concurrency kills, the lane rejects — the fortress
  board shows the bad day WITHOUT being told. DFHack's promise, kept: the state was always in
  memory; now it renders.
- **The era shift is visible:** sessions/day `... 4 80 152 84` — the multi-window fan-out era
  (Sep 3→5) vs 3-10 seats/day before. ROOM's 1,909-event day and CHAIN's 1,910-knot day = the
  backfill/genesis seals, dated by the bars.
- **Second key scored (falsifier 3, qwen2.5:7b text pass over the digest):** totals right
  (3.56B ≈ census 3.6B), error count + clustering right (834, day-13 max = 216, >2x average),
  anomaly named right; ONE cross-table misattribution (called the seat total 3,290M a "model")
  and one invented daily number. Verdict: 7b = numbers chord, 3B-vl = shape chord — two keys,
  one chord, both scored, neither trusted blind. This is the two-key design the card named,
  now measured.
- **Wired:** dashboard/static/swarm_board.png (HTTP 200), nav.js Swarm Board entry, the door
  on OPERATOR_DRIVE. Maze-keeper note: 19GB local model on the drive — unexamined shelf.
