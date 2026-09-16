# A3 — THE TOY: CORE VERB (strike S6 extraction)

- Lane: A3, wave 2026-09-16 · Status: **FILED**
- Receipt-first per wave-lane law. No git, no paid APIs, $0. All claims below verified against file bytes.
- Mission: extract the TOY's 7-item build order from strike S6 and make it concrete for OUR game stack.

## Source files consumed (bytes, not citations)

| File | What it gave |
|---|---|
| `watch/GAP_PROBE_FOLD_20260908.md` (lines 468–520) | **SIXTH STRIKE verbatim**: the toy problem ("Zelda starts as fun movement with 1 verb… no core verb that feels good in 3 seconds") + THE BUILD ORDER (7 items) + the kill-test ("1 external non-AI playtester per week, fun <60s. Skip for 3 weeks = project is already dead.") |
| `watch/inbox/journal_mark_202609/JOURNAL_20260916_ANSWERS.md` | **The Exanima honest-start law.** NOTE: the mission cited `watch/inbox/HONEST_START_20260916.md` — that path does not exist. The law lives in journal answer 5 + reading 5: *"An honest start. Basic systems — like the progression in Exanima, that physics dungeon — MUD + our basic game mechanics on a repeatable, reusable path."* Trust bytes, not pointers. |
| `dashboard/static/games/mud.html` (2311 ln) | The souls grammar is already shipped. Line 1091: `// wind-up telegraph: the swing is dodgeable — souls grammar`. Constants: enemy windup 0.35s / telegraph 0.35s / attackCd 1.2s; roll = ShiftLeft, 30 stamina, rollT 0.28s, rollCd 0.5s, **iframes 0.35s**; swing = Space/mouse, 15 stamina, cd 0.35s; shout = F, interrupts windup, cd 5s; stamina regen 25/s. |
| `dashboard/static/games/frontier_souls.html` (1828 ln) | window.FS, ring progression, Adam's storyboard lanes (canyon wake → scorpion waits; nell strongest-and-slowest), the walk=level law, seeded `hash2` decor. |
| `scripts/test_mud_fifty.js` | The 51-lane gate: DOM shim → `new Function(...)` → `window.MUD` → `pump(n,dt)` + `keys[...+'_p']`. Deterministic headless play already exists — the toy CI rides this pattern unchanged. |
| `scripts/test_frontier_souls.js` | Same harness pattern for FS — proves the pattern is reusable. |
| `watch/inbox/HERMES_DIRECTIVE_BONES_REFEREE_20260916.md` | **The bones replay law** (OUTPUT CONTRACT): determinism falsifier + divergence falsifier. Cited verbatim in §4. |
| `mag/wow_bones_session.py` (lines 131–147) | `wow_session.v1` receipt: `{schema, session_id, seed, draw_index, moves, verdict, sha256}` — canonical body, byte-stable, session+receipt files are the only writes. |
| `memory/game_modules/water_computer.v1.json` | The honesty pattern to keep: *"height is the computation; pouring the bucket is not a win"* — physics calls it DISPUTED. The toy's equivalent: a hit without a telegraph is the bucket-pour. |

---

## 1. THE CORE VERB: the i-frame roll (read → roll → punish)

**One sentence:** every ~3 seconds the player reads a 0.35s telegraph, rolls THROUGH the swing (ShiftLeft), and punishes the 1.2s recovery with Space.

**Why this one, against fun-in-3s:**
- **The first fun moment fits inside 3 seconds.** Spawn next to a walker: it winds up at t≈0.4s, you roll at t≈0.5s, i-frames carry you through the bite, your swing lands in its recovery, it dies inside 3s. The dopamine unit is "I was going to be hit and wasn't" — the toy-sized version of "Zelda starts as fun movement with 1 verb."
- **One verb, real timing depth, zero new code.** windup 0.35 vs roll 0.28 → a late-roll window; stamina 100 / cost 30 caps spam at ~3 rolls → a resource rhythm of ~3 decisions per 10s; attackCd 1.2s is the punish window. It is literally commented into mud.html as *souls grammar* — this is the verb our stack already speaks.
- **Adam's honest start names it.** His answer 5: "MUD + our basic game mechanics on a repeatable, reusable path." The verb IS the repeated unit; rooms/doors/sigils are the wrapper, and the wrapper comes AFTER the toy (locked rule: toy before more systems).
- **It is CI-checkable today** — the fifty-lane harness already drives roll/swing deterministically.

**Rejected candidates (and why):**
- *Mud walking* — substrate, not a decision; no failure state.
- *Skating (wipeout htmls)* — momentum is fun but is a rebuild, not $0-from-existing; parked.
- *Frontier walk=level* — instant gratification but zero skill expression in the verb; it is a **progression wrapper**, and it's already Adam's own storyboard. Keep it for the toy's meta layer later; it is not the 3-second unit.

**Toy v0 spec:** strip mud.html to ONE arena + ONE walker + roll/swing + seeded RNG + receipt writer (~200 lines). No sigils, doors, loot, shout, traps, lore, soul orbs, boss. Session <60s. First telegraph within 3s of spawn, guaranteed.

---

## 2. THE EXECUTABLE PREDICATE (doctrine → code)

**Doctrine sentence:** *You are never hit without a telegraph you could have rolled through.*

**P-LEGAL (the invariant, checked per receipt; CI fails if broken):**
For every damage event at time `t_hit` in a replay, there must exist a telegraph event with `windup ≥ 0.35` starting at `t_hit − windup`, with the hitbox overlap present before `t_hit − 0.28` (roll duration) — i.e. a roll initiated anywhere in `[t_hit − 0.35, t_hit]` grants i-frame coverage across `t_hit`. Field `hits_no_telegraph` in the receipt MUST be `0`.

Sub-invariants (each already lane-shaped in the fifty-lane pattern):
- **P1 telegraph law** — every melee hit is preceded by windup 0.35/telegraph 0.35 (the shout-interrupt lane proves windup is real state).
- **P2 i-frame law** — roll at windup start ⇒ iframes 0.35 ≥ windup 0.35 ⇒ zero damage.
- **P3 stamina law** — no roll below 30, no swing below 15, regen 25/s: no infinite spam (same family as the existing "souls paid ONCE / AFK farm dead" lane).
- **P4 determinism law** — same seed + same input tape ⇒ identical events ⇒ identical sha256. **This needs the one genuinely new thing:** replace `Math.random` with a seeded LCG carrying a draw index (frontier_souls' `hash2` is the pattern). Without it there is no replay, no predicate, no fork test.

A hit without a readable telegraph is the water-computer's bucket-pour: the physics (replay) calls it DISPUTED.

---

## 3. PROOF-OF-PLAY SHAPE: `toy_play.v1`

Mirror of `wow_session.v1` (mag/wow_bones_session.py). Byte-stable, deterministic, $0; session + receipt files are the only writes; lands in `watch/inbox/toy_plays/` (shared inbox = durable write root).

```json
{
  "schema": "toy_play.v1",
  "session_id": "toy-<sha256(game_hash:seed)[0:12]>",
  "game_hash": "<sha256 of the toy html bytes — gitless content commitment>",
  "seed": "<str>",
  "draw_index": 41,
  "inputs": [[420, "ShiftLeft", 1], [455, "ShiftLeft", 0], [700, "Space", 1]],
  "events": [
    {"t": 0.40, "e": "telegraph", "enemy": 1},
    {"t": 0.52, "e": "roll"},
    {"t": 0.75, "e": "hit_dodged"},
    {"t": 0.80, "e": "swing"},
    {"t": 0.86, "e": "kill", "enemy": 1}
  ],
  "hits_taken": 2,
  "hits_no_telegraph": 0,
  "first_punish_s": 2.8,
  "verdict": "win",
  "duration_s": 41.2,
  "sha256": "<canonical body hash>"
}
```

**Admission cost (S6 item 5, sybil resistance):** a receipt is admissible only if local re-execution of `(game_hash, seed, inputs)` reproduces `sha256`. Proof of play = you paid the replay. No server, no token, no account.

---

## 4. THE FORK TEST (divergent replay — bones replay law, cited)

Law source: `watch/inbox/HERMES_DIRECTIVE_BONES_REFEREE_20260916.md`, OUTPUT CONTRACT, applied verbatim to the toy:

1. **Determinism falsifier:** same seed + same moves (input tape), played twice, MUST produce byte-identical receipt `sha256`. Any difference = the toy failed (our own R07 law turned on our own code).
2. **Divergence falsifier:** flip ONE input frame at `t_k` (or one RNG draw at index `i`) → replay from the same tail MUST diverge, and the receipt pair must name the fork at the exact index: `INPUT_FORK @ t_k` / `RNG_DIVERGE @ draw i` — first differing event reported, not just "different."

**CI shape (3 lanes, fifty-lane shim pattern, `scripts/test_toy.js`):**
- (a) replay same tape twice → `eq(sha, sha)`;
- (b) mutate one keypress at t=2.0s → assert the first differing event is exactly the first post-fork event;
- (c) two tapes from one seed → each individually P-LEGAL. Divergence is legal play; the fork proves the tape is load-bearing.

This answers S6 build-order item 4 ("two fleets from same tail, do they diverge?") in game terms: **yes — at the exact frame, provably.**

---

## 5. EXTERNAL PLAYTESTER PLAN — Adam, week 1

Adam is player one (already canon: the fold's cold-start witness names him; frontier_souls was built to his three laws). Week 1 = one session, ≤10 minutes of his time, $0:

1. **Setup:** `mag.cmd lab` → Adam opens the toy URL on his own machine (:8765 static). No login, no wrap, no tutorial — the wrap-stripped rule from GAP_PROBE fold action #2.
2. **Play ≤3 min.** Session auto-writes a `toy_play.v1` receipt to `watch/inbox/toy_plays/`.
3. **Measured gates (observed, not asked):** `first_punish_s < 60` (S6 law); an unprompted "one more run" = fun-in-3s gate passed; zero questions asked before his first roll = the telegraph reads.
4. **Three questions, after play only, his own words:** What did you do? / When did you know what to do? / What did you want to do that the game didn't let you? Answers append as an addendum row on the receipt — bytes on the tail, no LLM recall (the stateless-window law).
5. **Cadence law (S6, verbatim):** 1 external non-AI playtester per week; skip 3 weeks = the project is already dead. Adam is week 1; weeks 2–4 recurse to one new stranger each; receipt count lands in the next wave capsule.

**Honesty clause:** if Adam's receipt shows `hits_no_telegraph > 0` or `first_punish_s ≥ 60`, the verb failed its gate — fix the verb before ANY new system (the locked rule).

---

## S6 build-order mapping (7 items → this receipt)

| # | S6 item | Where |
|---|---|---|
| 1 | doctrine → executable predicate | §2 P-LEGAL |
| 2 | core verb (before more systems) | §1 roll-punish |
| 3 | prune_to_invariants | chain lane's job; the toy feeds it: each receipt prunes to `P-LEGAL bit + verdict` |
| 4 | chain fork test | §4 bones replay law, 3 CI lanes |
| 5 | proof-of-play cost / sybil | §3 replay-pays rule |
| 6 | stateless window | §3+§5: read-only receipt tail + hashes; questions appended, never recalled |
| 7 | 1 playtester/week, fun <60s | §5 Adam week 1 |

## Build cost

$0. New code: one `toy.html` (~200-line strip of mud.html: roll/swing/walker/telegraph + seeded LCG + receipt writer) + `scripts/test_toy.js` (3 fork lanes on the existing shim). Everything else is already in the tree. No git ops, no paid APIs.

## Log
- [x] receipt skeleton written
- [x] S6 verbatim extracted from `watch/GAP_PROBE_FOLD_20260908.md` (sixth strike at line 468)
- [x] HONEST_START path corrected → journal answer 5 (bytes over citations)
- [x] mud.html / frontier_souls.html / fifty-lane gate / bones directive / bones session kernel read
- [x] 5 deliverables filed (this file is the deliverable)
