# WIRE_PLAN - the party chat composes from shipped parts (wire, don't build)

- Replay of: `memory/plans/hermes_burn_playground_20261003/WIRE_PLAN/ask.json` (target model anthropic/claude-opus-5.5; replayed on the flash rail, 2026-10-03).
- Ground: only the six evidence paths. `mag/chan.py`, `mag/game_mud.py`, `tools/tavern.py`, `tools/dungeon.py`, `tools/hermes_burn.py`, `configs/kabuki_cast.json`. Every claim cites file:line from those bytes; anything not derivable from them is marked UNVERIFIED.
- Law: no em-dashes. A spec that cannot be built in one sitting is a survey; this is a spec.

---

## PART 1 - THE INVENTORY (what ships today, what it lacks for the party-chat loop)

### 1.1 mag/chan.py - the board (schema chan.v1)

Provides:
- One dual-read surface: `watch/room.jsonl` (chan.py:21) is at once an imageboard page and the Mag room log. `is_play_post` filters mill sludge via `HIDE_EVENTS` and demands thread+text (chan.py:24-32, 89-98).
- `post(slug, text, seat="anon", sage=False, reply_to="")` appends `{ts, seat, event: reply|sage, thread, text[:8000], reply_to?}` and returns schema `chan_post.v1` (chan.py:211-237). `_append` is a plain jsonl append (chan.py:121-125).
- `thread(slug)` and `catalog()` read views with stable post numbering (`no`) and per-seat trip ids (chan.py:128-135, 159-208). `slugify` is lowercase `[a-z0-9-]`, 40 chars max (chan.py:71-74).
- `PLAYER_SEATS` = {anon, anonymous, primer, heart, operator, nell, op}; a thread is "player" and catalog-visible when any seat is in that set (chan.py:34, 138-140, 177-179). `sage=True` posts do not bump (chan.py:171-173).
- `wake(slug)` fires one background deepseek-flash mouth (OpenClaw first, `chat_provider` flash fallback) writing `event=chan_post` (chan.py:240-306).
- `check_steer(target)` paints an operator steer card from the steer channel (chan.py:317-346).

Lacks for the party loop:
- Only one mouth exists and it is deepseek flash (chan.py:275-283). No per-seat model routing, no persona faces, no cost accounting on `post()`.
- No thread-open-from-artifact API: OPs are either the `keep` seed (chan.py:143-156) or a plain reply post. No fields for gap references, room bindings, or receipts (record shape is exactly chan.py:225-233).
- No linkage to any game state; a thread cannot say which MUD room it is.

### 1.2 mag/game_mud.py - the walkable world (schema game_mud.v2)

Provides:
- A closed 11-room map, each room with `role`, `question` (the frontier question), `prose`, `exits` (game_mud.py:62-199). `the Dungeon` is "rooms = tasks" (game_mud.py:115-126); `the Shadowlands` is stalled work (game_mud.py:187-198); `the Mycelial Library` is the laws (game_mud.py:91-102).
- Verkle-anchored state via `game_world.get_state/set_state`: keys `game.mud.player` (room, loot), `game.mud.claimed`, `game.mud.hall_record` (game_mud.py:56-58, 204-223). Caveat: `_set` swallows failures silently (game_mud.py:219-223).
- The deterministic Roshomon filter, `$0`, no LLM: `_statements` extracts labeled invariants and sentences (chan regex `INVARIANT|MECHANISM|SOLUTION|MOVE`, game_mud.py:265-284); `_overlap` token-overlap similarity (game_mud.py:287-295); `CORE_MIN_AGREE = 2` (game_mud.py:59).
- `survey(room, seats, threshold=0.55, route=True)`: tasks the party via `game_dm.party()` + `game_dm.ask_player`, groups statements, core = convergent, novel routed to `swarm_surface.route_novel` (game_mud.py:298-360).
- `claim(room)`: refuses without convergence, folds the core as loot, marks the room claimed (game_mud.py:363-386; refusal wording 372-375).
- `act(command)`: look / go / survey / claim / inv / map / help / status (game_mud.py:458-534); `go` validates exits and moves the single player (game_mud.py:493-501).

Lacks for the party loop:
- Single-player state: one `game.mud.player` (game_mud.py:56, 226-234). No per-seat positions for N walkers.
- Rooms are fixed fantasy rooms. No mapping from gap-register rows or thread slugs to rooms, no dynamic room creation.
- `survey`/`claim` ask `game_dm` seats (game_mud.py:307, 312, 369), a paid surface whose model and pricing are not in the evidence (UNVERIFIED cost).
- No receipt or gate linkage on a claim; the fold lives only in the verkle chain and loot list.

### 1.3 tools/tavern.py - the multi-persona carrier pattern

Provides:
- The exact reuse seam this plan needs: it imports `_bank, _call, _hermes_key, _now` from hermes_burn and prices via `PRICING` (tavern.py:37, 116-117).
- Deterministic estate law block `LAWS` including the no-em-dash rule and one-line-only output (tavern.py:42-52); per-persona system prompts assembled from name/register/want/secret/tell (tavern.py:145-148).
- Per-turn paid call `_paid(model, messages, max_tokens, tag)`: calls `_call`, computes cost from `PRICING`, banks a usage row with id `TAVERN_r<rnd>_<actor>` (tavern.py:107-127).
- Run discipline: run dir with transcript.jsonl + play.md + scenario.json (tavern.py:81-89), cumulative budget hard stop mid-round (tavern.py:132-134), DONE marker and no-refire law (tavern.py:20, 214-216), sha256 dice committed before the actor speaks (tavern.py:58-60).

Lacks for the party loop:
- Personas come from a scenario JSON file, not from the kabuki cast; no seat rotation.
- Writes only its own run dir; no chan/room.jsonl posting, no game state, no gate or red-team step beyond the escalation judge (tavern.py:164-182).
- Budget is per-run, not per-thread-hour; no cross-thread rollup.

### 1.4 tools/dungeon.py - the enforcement carrier pattern

Provides:
- Carrier-enforced law, never model manners: dice preimage carries the chain tip and is committed before speech (dungeon.py:110-111, 273-275); golden vectors must reproduce or the session refuses to start (dungeon.py:114-122); em-dash conversion + word cap enforced by `strip_and_cap` (dungeon.py:102-107); quirks void beats (grok length NOROLL dungeon.py:211-212, chatgpt over-claim tax 213-215, saelis claim-before-strike gate 220-221).
- THE GWAP RUNG: `REAL_SCROLLS` are real estate claims with carrier-run byte checks (`LINKS.jsonl` row count, `room.jsonl` size, census carrier presence); "the dice decide WHO gets to try; the bytes decide WHAT IS TRUE" (dungeon.py:77-100); `[AUDIT]` runs the real check in-verdict (dungeon.py:242-258).
- Budget as `SystemExit` (dungeon.py:159-160), content_filter retry-then-void (dungeon.py:164-174), `_bank` per call (dungeon.py:180-181), DONE json with verdict + spend + audits (dungeon.py:347-352).

Lacks for the party loop:
- One hardcoded scene (S0+S1), no navigation between rooms, initiative is a fixed list (dungeon.py:60).
- `REAL_SCROLLS` is a fixed 3-check list; no pluggable per-room verification.
- Roster fixed to 4 named actors (dungeon.py:43-56); no kabuki cast, no chan posting, no gate receipts.

### 1.5 tools/hermes_burn.py - the funded rails

Provides:
- `PRICING` (usd/token in,out): opus-5.5 (0.000004, 0.00002), sonnet-5.5 (0.000002, 0.00001), fable-5.1 (0.00001, 0.00005), haiku-4.5 (0.000001, 0.000005) (hermes_burn.py:71-76).
- `_call(model, messages, max_tokens, key, retries=1)` with an endpoint fence to exactly `inference-api.nousresearch.com` and DNS-resolved private-IP refusal (hermes_burn.py:67-68, 96-131).
- `_bank(row)` appends to `memory/runs/hermes_burn/usage.jsonl` through `doubled_key_check` (re-fire tripwire) (hermes_burn.py:65-66, 149-156).
- `_hermes_key()` reads HERMES_API_KEY_2 then _1 from .env (hermes_burn.py:83-93).
- The ask production line: ask dirs with ask.json + evidence preflight fail-closed + landed-skip + refusal-terminal markers + two-turn revision (hermes_burn.py:206-264, 267-392). Estate law block with file:line citation duty, UNVERIFIED marking, no em-dashes, and "name your own deliverable's falsifier" (hermes_burn.py:159-173).

Lacks for the party loop:
- Batch/queue shaped: one ask dir = one fire of one deliverable. No interactive per-turn "post one line as persona X" entry, which is why tavern/dungeon bypass `run_ask` and ride `_call` + `_bank` directly (tavern.py:37, dungeon.py:37).
- PRICING covers only the four anthropic SKUs; no entry for the kabuki cast's free-tier models.

### 1.6 configs/kabuki_cast.json - the faces (schema kabuki_cast.v1)

Provides six actor faces, each with seat, model, account, word cap, persona:
- ARAGOTO (S2, 350 words): bold attacker, disagrees with receipts (kabuki_cast.json:9-15).
- WAKA (S3, 400): restates, names assumptions, rebuilds as n+1, ends with one killing falsifier (kabuki_cast.json:18-24).
- ONSEI (S4, 300): returns exactly four things (forbidden pattern, paid-rent claim, extension, disanalogy) (kabuki_cast.json:27-33).
- TACHIYAKU (S5, 350): the five hardest questions, answered Yes/No/Partly (kabuki_cast.json:36-42).
- ONNAGATA (S6, 350): claim-checkable synthesis for handoff (kabuki_cast.json:45-51).
- HANA-GUMO (S7, 400): splits material into fields, lists what experts must double-check (kabuki_cast.json:54-60).
- Rotation "is hashed per question" per the file note (kabuki_cast.json:4). Fallback model and per-actor models are `inclusionai/ling-3.0-flash-sante:free` on account `sdd` (kabuki_cast.json:5-6, 11).

Lacks for the party loop:
- The cast's models ride a free-tier account (`sdd`) that no evidenced tool dials; hermes_burn's fence pins exactly one Nous host and four anthropic SKUs (kabuki_cast.json:11 vs hermes_burn.py:67-76). How `sdd` free-tier calls would be dialable is UNVERIFIED from this evidence.
- Output contracts are prose inside personas (ONSEI's four returns, TACHIYAKU's Yes/No) with no machine-readable parser spec; the word caps are data but no code enforces them.
- No stage_name-to-funded-SKU mapping exists anywhere in evidence.

### 1.7 Two cross-cutting findings that collapse work

1. "Posts land as room.jsonl rows AND chan threads" is ONE write, not two: chan threads are views over `watch/room.jsonl` (chan.py:21, 121-125, 234). A single `chan.post` satisfies both halves of the contract clause.
2. The per-turn money pattern already exists twice: tavern `_paid` and dungeon `_paid` both ride `_call` + `PRICING` + `_bank` outside the batch queue (tavern.py:107-127, dungeon.py:158-185). The party chat copies that seam; it does not touch `run_ask`.

---

## PART 2 - THE GLUE SPEC: one new file, `tools/partychat.py`

Contract clause to function map:

| contract clause | function |
|---|---|
| thread opens from a gap-register row | `open_thread` |
| party members post via kabuki faces through hermes_burn rails | `post_as` (+ `_face_messages`, `_order`) |
| posts land as room.jsonl rows AND chan threads | `chan.post` inside `post_as` (finding 1.7.1) |
| claims map to game_mud rooms | `claim_thread` (+ `bind_room`, `thread_room`) |
| rival proposals fork into competing builds scored by the gate | `fork_builds` + `score_build` |
| landed builds ractor-red-teamed | `red_team` |
| everything composed, nothing rebuilt | `run_season` loop |

Module head and constants:

```python
"""partychat - THE WIRE: the party chat composed from shipped parts.
Opens chan threads over gap-register rows, walks game_mud rooms, posts
kabuki faces through hermes_burn rails, forks rival builds, scores with
the workflow gate, red-teams with byte checks, claims rooms on convergence.
CLI: python -m tools.partychat open|walk|post|survey|claim|season ..."""
SCHEMA = "partychat.v1"
THREADS = ROOT / "watch" / "inbox" / "partychat" / "threads.jsonl"
        # rows: {ts, slug, gap_id, room, budget_usd, spend_usd, gate_receipt, claim}
BUILDS  = ROOT / "watch" / "inbox" / "partychat"          # BUILDS/<slug>/build_A.md, build_B.md, gate_*.txt, DONE
CAST    = ROOT / "configs" / "kabuki_cast.json"
GAP_ROOM_HINTS = {...}   # keyword -> room, static; default "the Dungeon"
CAST_SKU = {   # stage_name -> hermes_burn.PRICING key; the cast's own sdd free-tier
               # models are not dialable from the fenced endpoint (1.6), so the FACE
               # is kabuki and the SKU is funded:
  "ARAGOTO":    "anthropic/claude-sonnet-5.5",
  "WAKA":       "anthropic/claude-sonnet-5.5",
  "ONSEI":      "anthropic/claude-haiku-4.5",
  "TACHIYAKU":  "anthropic/claude-fable-5.1",
  "ONNAGATA":   "anthropic/claude-opus-5.5",
  "HANA-GUMO":  "anthropic/claude-sonnet-5.5",
}
```

Functions (signatures are the deliverable; each body is composition only):

1. `def _load_cast() -> list[dict]`
   Reads `kabuki_cast.json`; asserts every `stage_name` has a `CAST_SKU` entry present in `hermes_burn.PRICING` (hermes_burn.py:71-76, the dungeon model guard shape, dungeon.py:289-290); returns `{stage_name, seat, max_words, persona}` per actor.

2. `def _order(slug: str, rnd: int) -> list[dict]`
   Deterministic rotation honoring the cast note "rotation is hashed per question" (kabuki_cast.json:4): `sorted(cast, key=lambda a: sha256(f"{slug}:{rnd}:{a['stage_name']}"))`.

3. `def open_thread(gap_id: str, gap_text: str, room: str = "the Dungeon") -> dict`
   Validates `room in game_mud.ROOMS` (closed world, game_mud.py:62-199). `slug = "gap-" + chan.slugify(gap_id)` (chan.py:71-74). Idempotence first: if `slug` is already in threads.jsonl, return the existing row unchanged (the no-refire law, tavern.py:20). Otherwise: `chan.post(slug, OP, seat="operator")` where OP carries gap_id, gap_text verbatim, and the room binding; `operator` is a PLAYER_SEAT so the thread is catalog-visible (chan.py:34, 177-179). Appends the threads.jsonl row with `budget_usd=1.5, spend_usd=0.0`. The gap register file itself is NOT opened by this module; the row arrives as arguments (see Part 5 on why: UNVERIFIED location).

4. `def bind_room(slug: str, room: str) -> dict` and `def thread_room(slug: str) -> str | None`
   The thread-to-room map lives in threads.jsonl (one small wire-local surface; posts themselves need no second write, finding 1.7.1). `bind_room` validates the room key then `chan.post(slug, f">the party moves to {room}", seat="primer", sage=True)` so the walk is on the board without bumping (chan.py:171-173, 216).

5. `def _face_messages(stage_name: str, slug: str, instruction: str) -> list[dict]`
   system = persona verbatim from the cast + word cap + a deterministic law block in the tavern.LAWS shape (one post, stay in face, no machinery, no em-dashes; tavern.py:42-52, chan.CHAN_SYSTEM register chan.py:51-60). user = the room's `prose` + `question` read straight from `game_mud.ROOMS[room]` (public dict, game_mud.py:62-199) + the thread tail: last 20 posts of `chan.thread(slug)` rendered as `>>no seat: text` (chan.py:196-208) + the instruction. Default instruction when empty: the room's frontier `question`, so walking into a room re-aims the party for free (game_mud.py:117-119 et al.).

6. `def post_as(stage_name: str, slug: str, instruction: str = "", max_tokens: int = 400) -> dict`
   The money path, the tavern `_paid` pattern (tavern.py:107-127):
   - `model = CAST_SKU[stage_name]`; `resp = hermes_burn._call(model, _face_messages(...), max_tokens, hermes_burn._hermes_key())` (hermes_burn.py:106-131, 83-93).
   - Cost from `PRICING`; `hermes_burn._bank({"id": f"PARTY_{slug}_r{rnd}_{stage_name}", "model": model, "turn": 1, "prompt_tokens": pin, "completion_tokens": pout, "cost_usd": cost, "ok": True})` (hermes_burn.py:149-156). The `PARTY_` id namespace keeps the doubled-key tripwire working for chat refires.
   - Carrier enforcement on the speech: em-dashes to hyphens and cap at the actor's `max_words`, the `strip_and_cap` law (dungeon.py:102-107).
   - Land it: `chan.post(slug, speech, seat=stage_name)` (chan.py:211-237). Seat sanitization lowercases and keeps `[a-z0-9_-]` (chan.py:224), so `hana-gumo` is a legal seat.
   - Add cost to the threads.jsonl `spend_usd`; refuse the call when `spend_usd >= budget_usd` (mid-round hard stop, tavern.py:132-134).

7. `def roshomon(slug: str, threshold: float = 0.55) -> dict`
   The `$0` survey of the thread itself: per post, `statements = game_mud._statements(text)` (game_mud.py:265-284, deterministic, "no LLM, $0" at 266); group across seats with `game_mud._overlap >= threshold` (game_mud.py:287-295); core = statements agreed on by `>= CORE_MIN_AGREE` seats (game_mud.py:59, 333-334); the rest is novel. No swarm routing by default; `game_mud.survey`'s `route_novel` path (game_mud.py:344-349) remains available for seasons with budget headroom. This is the party-chat replacement for the paid `act("survey")` (game_mud.py:502-519).

8. `def fork_builds(slug: str, core_statement: str) -> dict`
   Rival proposals fork into exactly two competing builds. Two `post_as` calls with the core in context: ARAGOTO writes `build_A.md` (the strong direct build) and WAKA writes `build_B.md` (the rebuilt n+1), the two faces the cast defines for attack and reconstruction (kabuki_cast.json:14, 23). Files land at `BUILDS/<slug>/`. Each fork call is a normal banked dispatch (`PARTY_<slug>_fork_<side>`).

9. `def score_build(slug: str, path: Path) -> dict`
   Runs `python tools/workflow_gate.py check --script <path>` via subprocess; captures exit code and output tail to `BUILDS/<slug>/gate_<name>.txt`; returns `{path, exit, passed: exit == 0}`. The gate file is NOT in the evidence set: the CLI shape above comes from the repo's build-discipline card (AGENTS.md, workflow gate section), and the gate's internal checks and its registry row behavior are UNVERIFIED from this evidence. If the gate rejects a build it stays rejected; the wire never loosens the hook.

10. `def red_team(slug: str, build_path: Path) -> dict`
    Landed-build attack with the dungeon audit law. TACHIYAKU and HANA-GUMO each `post_as` with the build text in context and the instruction: name one defect, and every defect MUST carry a runnable byte check (a file:line that exists or a command that runs); a finding without a check is struck (the REAL_SCROLLS pattern: the bytes decide WHAT IS TRUE, dungeon.py:77-79; the AUDIT verdict path, dungeon.py:242-258). Each surviving finding re-enters the pipeline as a new gap thread via `open_thread(finding_id, finding_text)` at recursion depth 1 per season. (The contract's word "ractor" is not defined in the six evidence files; this spec grounds red-team in the evidenced byte-check pattern. Anything more a "ractor" implies is UNVERIFIED.)

11. `def claim_thread(slug: str) -> dict`
    Claims map to game_mud rooms, gated by convergence:
    - `$0` pre-check: `core = roshomon(slug)`; if empty, refuse with the no-convergence wording shape (game_mud.py:372-375). This guard exists because `game_mud.claim(room)` internally runs its own paid `survey` (game_mud.py:369, 307-312); never pay for a survey when the thread already shows no core.
    - Otherwise: `r = game_mud.claim(thread_room(slug))` (game_mud.py:363-386), which folds the core into the verkle chain (`CLAIMED` at 241-244, loot at 378-380). The internal survey's model and cost are UNVERIFIED from the evidence; Part 4 carries it as a capped budget line.
    - Land the receipt on the board: `chan.post(slug, "CLAIM FOLDED: " + r["claimed"], seat="primer")`; write `gate_receipt` + final spend into the threads.jsonl row; return `r`.

12. `def run_season(slug: str, rounds: int = 8, budget_usd: float = 1.5) -> dict`
    The loop, all composition:
    ```
    for rnd in 1..rounds:
        for actor in _order(slug, rnd):        # 6 posts per round
            post_as(actor, slug)               # spend-checked inside
        core = roshomon(slug)
        if core:
            fork_builds(slug, core)            # two rival specs
            sa, sb = score_build(A), score_build(B)
            winner = higher of the two gate scores (tie: smaller file; both fail: keep talking)
            red_team(slug, winner)
            claim_thread(slug)
            break
    write BUILDS/<slug>/DONE {"spend_usd", "rounds", "core", "gate_pass", "claim"}
    ```
    DONE marker semantics per tavern/dungeon (tavern.py:214-216, dungeon.py:347-352); a DONE dir never replays (tavern.py:20).

13. `def main(argv: list[str] | None = None) -> int`
    CLI: `open GAP_ID ROOM`, `walk SLUG DIR`, `post SLUG STAGE [TEXT]`, `survey SLUG`, `claim SLUG`, `season SLUG [--rounds N --budget-usd X]`. Exit 0 ok / 1 any fail / 2 usage (the hermes_burn main shape, hermes_burn.py:395-424).

New surface count: one code file (`tools/partychat.py`), one wire-local data file (`threads.jsonl`), one receipt dir (`watch/inbox/partychat/<slug>/`). Everything else is an existing shipped surface written through its existing functions.

---

## PART 3 - THE MUD VERB LAYER (the party chat is walkable)

Binding law: `game_mud.ROOMS` is a closed 11-room world (game_mud.py:62-199); no dynamic rooms exist in evidence, so threads bind to existing rooms only and `bind_room` refuses unknown keys. Default landing `the Dungeon` (rooms = tasks, game_mud.py:115-126). Static `GAP_ROOM_HINTS` routes by keyword: stalled/aged gaps to `the Shadowlands` (game_mud.py:187-198), doctrine/law gaps to `the Mycelial Library` (game_mud.py:91-102), memory/anchor gaps to `the World-Memory` (game_mud.py:63-74), swarm/worker gaps to `the Forge-Hive` (game_mud.py:103-114). Unmapped gaps default to the Dungeon.

The three verbs, each against an existing game_mud function:

- `go` - `def go(slug: str, direction: str) -> dict`
  `r = game_mud.act(f"go {direction}")`: the existing move branch validates the exit, updates the verkle-committed player, and returns the entering description (game_mud.py:493-501, state write 219-223, description 247-258). On success `bind_room(slug, r["room"])`. Invalid doors refuse with the game's own line (game_mud.py:501) and change nothing. Helper `def exits(slug: str) -> list[str]` reads `game_mud.ROOMS[room]["exits"]` so the board can paint ways out (the `_desc` exit line shape, game_mud.py:256-257). The walk is visible in exactly two places: the chain (player room) and the board (a sage post).

- `claim` - `def claim_thread(slug: str) -> dict` (Part 2, function 11)
  Rides `game_mud.claim(room)` (game_mud.py:363-386). The MUD's own law, survey before claim and no fold without convergence (game_mud.py:369-375), maps onto the party chat's law: `roshomon(slug)` must show `>= 2` agreeing seats (game_mud.py:59) before the paid claim fires. After the fold, `game_mud.status()` lists the room under `claimed` (game_mud.py:537-543) - that read is the receipt check.

- `post` - `def post_as(stage_name, slug, instruction="")` (Part 2, function 6)
  With empty instruction it defaults to the bound room's frontier `question` (every ROOMS entry carries one, e.g. game_mud.py:117-119). So "walk to a problem room and post" needs zero new code: the room aims the party. The board post and the room brief are the same loop: read `ROOMS[room]` for context, write `chan.post` for the record.

Deliberate omission: `act("survey")` (game_mud.py:502-519) exists but pays `game_dm` per seat; the wire's default witness step is the `$0` `roshomon(slug)` over thread posts (game_mud.py:265-295). Seasons with budget headroom may call `act("survey")` for a second, independent witness set.

---

## PART 4 - THE COST ENVELOPE

Per-post assumptions (worst case): ~2,500 prompt tokens (persona ~200 + law block ~150 + 20-post thread tail ~2,000 + room brief ~150) and ~200 completion tokens (cap 400). Prices are the captured table, usd per token (hermes_burn.py:71-76).

| SKU | prompt $ | completion $ | per post |
|---|---|---|---|
| claude-haiku-4.5 | 0.00250 | 0.00100 | 0.00350 |
| claude-sonnet-5.5 | 0.00500 | 0.00200 | 0.00700 |
| claude-fable-5.1 | 0.02500 | 0.01000 | 0.03500 |
| claude-opus-5.5 | 0.01000 | 0.00400 | 0.01400 |

CAST_SKU cost per round (6 posts): 4 sonnet + 1 haiku + 1 opus = 0.0280 + 0.0035 + 0.0140 = $0.0455.

Per thread (8 rounds = 48 posts + close-out):
- 48 party posts: $0.364
- fork_builds: 2 sonnet calls at ~2k in / 1k out: $0.028
- red_team: 2 fable posts: $0.070
- claim internal survey: capped at $0.25 (cost UNVERIFIED: `game_dm.ask_player`'s model is not in the evidence, game_mud.py:307-312)
- roshomon, gate subprocess, threads.jsonl, chan reads/writes: $0.00
- Typical total: ~$0.71. Hard cap: $1.50 per thread (mid-round stop, tavern.py:132-134).

$0 surfaces, named: the chan board itself (post/catalog are file appends, chan.py:121-125, 159-208), the Roshomon filter (game_mud.py:266), the gate subprocess (local), dungeon-style byte checks (local, dungeon.py:80-100). `chan.wake()`'s deepseek flash fallback (chan.py:273-283) is NOT in the party path (party mouths ride hermes_burn); its T2 cost is UNVERIFIED and excluded from the envelope.

Hourly season cadence: at the top of each hour, `run_season` drains the highest-priority open gap thread (rounds 8, cap $1.50).
- Typical: 24 threads/day x $0.71 = ~$17.04/day.
- Cap-bound worst case: 24 x $1.50 = $36.00/day.
- Anchors from evidence: one dungeon session caps at $4.00 (dungeon.py:363) and one tavern run at $5.00 (tavern.py:223); a party thread caps under both, so the hourly cadence costs roughly one dungeon session per 5-6 threads at typical spend.
- Audit rule: every call banks a `PARTY_*` row (hermes_burn.py:149-156), so the usage ledger is the invoice and `doubled_key_check` (hermes_burn.py:153) is the re-fire alarm. The envelope is enforced twice: `spend_usd` in threads.jsonl per thread, and the ledger total per day read before each season fires.

---

## PART 5 - THE FALSIFIER

The first thread to run end to end:

- Which gap row: UNVERIFIED. The gap register is not among the six evidence files; its path and row ids cannot be cited from this evidence. (Repo context outside the evidence set, AGENTS.md's citation-lint card, names a GAP_REGISTER with a rank-3 citation-defect row; if that is the intended register, the falsifier takes its lowest-rank unclaimed citation-defect row.) The deterministic selection rule that does not depend on the register's location: take the lowest-rank unclaimed row whose defect is byte-checkable, meaning reproducible by reading bytes or running one command, the `REAL_SCROLLS` standard (dungeon.py:77-100). Open it with `open_thread(gap_id=<row id>, gap_text=<row text verbatim>, room="the Mycelial Library")`, the laws-as-lore room (game_mud.py:91-102).
- Run: `python -m tools.partychat season gap-<id> --rounds 8 --budget-usd 1.5`.

What measured outcome lands it as real (all five, or the thread is struck):

1. The thread exists end to end in `watch/room.jsonl`: OP + 48 kabuki posts + fork posts + red-team posts + the claim fold line, all appended by `chan.post` (chan.py:121-125, 211-237).
2. The ledger: at least 50 rows in `memory/runs/hermes_burn/usage.jsonl` carrying `PARTY_` ids, summed cost within the $1.50 cap, zero doubled keys (hermes_burn.py:149-156).
3. The gate receipt: the winning build's `score_build` exit 0 output filed at `watch/inbox/partychat/<slug>/gate_*.txt` (gate internals UNVERIFIED from this evidence; the receipt is the captured bytes of the run).
4. The landed fix: the winning spec applied as a real patch whose fix comment names the cause and the evidence it was fixed on, verified by a passing red-team byte check - the AUDIT law, the bytes decide WHAT IS TRUE (dungeon.py:77-79, 242-258). A thread that ends in conversation with no landed fix FAILS this clause by definition.
5. The MUD state: `game_mud.status()` lists the bound room under `claimed` (game_mud.py:537-543) and the fold is quoted in the thread.

Struck condition (the negative test): if any of the five is missing after the season, or `roshomon(slug)` never reaches `CORE_MIN_AGREE = 2` witnesses (game_mud.py:59), the season writes `DONE {"verdict": "STRUCK", ...}` and the gap row returns to the register. Tokens banked with no landed artifact is exactly the failure the estate law block demands each deliverable name a falsifier against (hermes_burn.py:171). One sitting, one wire, one measured fix: that is the whole plan.
