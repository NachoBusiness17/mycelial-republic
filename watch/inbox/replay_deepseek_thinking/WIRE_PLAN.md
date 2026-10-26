# 1. THE INVENTORY

## mag/chan.py
Provides the imageboard/room surface on `watch/room.jsonl`.
- `SCHEMA = "chan.v1"` at `mag/chan.py:20`. Room path at `mag/chan.py:22`.
- `HIDE_EVENTS` at `mag/chan.py:25`. `PLAYER_SEATS` at `mag/chan.py:34`. `PRIMER_THREADS` at `mag/chan.py:36`.
- `KEEP_OP` at `mag/chan.py:38`. `CHAN_SYSTEM` at `mag/chan.py:50`.
- `room_path()` at `mag/chan.py:63`.
- `_now()` at `mag/chan.py:67`.
- `slugify()` at `mag/chan.py:71`.
- `paint_tool()` at `mag/chan.py:76`.
- `trip_id()` at `mag/chan.py:81`.
- `is_play_post()` at `mag/chan.py:85`.
- `_load()` at `mag/chan.py:93`.
- `_append()` at `mag/chan.py:110`.
- `_number()` at `mag/chan.py:117`.
- `_is_player_thread()` at `mag/chan.py:125`.
- `seed_keep()` at `mag/chan.py:129`.
- `catalog()` at `mag/chan.py:144`.
- `thread()` at `mag/chan.py:184`.
- `post()` at `mag/chan.py:197`. Signature: `post(slug, text, *, seat="anon", sage=False, reply_to="", path=None)`. Writes a row to `watch/room.jsonl` with `ts, seat, event, thread, text, reply_to`.
- `_wake_run()` at `mag/chan.py:220`. Uses OpenClaw first, then `models.providers.chat_provider`.
- `wake()` at `mag/chan.py:275`.
- `check_steer()` at `mag/chan.py:282`. Reads `tools.steer_read`.
- `main()` at `mag/chan.py:315`.

State surfaces: `watch/room.jsonl` rows. Schemas: `chan.v1`, `chan_post.v1`, `chan_wake.v1`, `chan_steer.v1`.

LACKS for the party-chat loop: no concept of party members or kabuki seats. No claim mapping to `game_mud` rooms. No gap-register integration. No rival proposal forking. No gate scoring. No red-team step. No thread-to-room mapping.

## mag/game_mud.py
Provides the Roshomon MUD.
- `SCHEMA = "game_mud.v2"` at `mag/game_mud.py:51`. `PLAYER`, `CLAIMED`, `HALL`, `CORE_MIN_AGREE` at `mag/game_mud.py:52-55`.
- `ROOMS` dict at `mag/game_mud.py:58`. Ten rooms with `role`, `question`, `prose`, `exits`.
- `DIRS` at `mag/game_mud.py:252`.
- `_world()` at `mag/game_mud.py:255`.
- `_get()` at `mag/game_mud.py:259`.
- `_set()` at `mag/game_mud.py:267`.
- `_fresh_player()` at `mag/game_mud.py:273`.
- `_player()` at `mag/game_mud.py:277`.
- `_claimed()` at `mag/game_mud.py:284`.
- `_mark_claimed()` at `mag/game_mud.py:288`.
- `_desc()` at `mag/game_mud.py:293`.
- `_statements()` at `mag/game_mud.py:320`.
- `_tokens()` at `mag/game_mud.py:335`.
- `_overlap()` at `mag/game_mud.py:339`.
- `survey(room=None, *, seats=None, threshold=0.55, route=True)` at `mag/game_mud.py:345`. Uses `mag.game_dm.party()` and `mag.game_dm.ask_player()`. Filters accounts, routes novel to `mag.swarm_surface.route_novel`.
- `claim(room=None)` at `mag/game_mud.py:410`. Requires a survey, folds the first core statement, marks room claimed, appends to player loot.
- `_hall_action()` at `mag/game_mud.py:440`.
- `act(command="look")` at `mag/game_mud.py:520`. Handles `look`, `go <dir>`, `survey`, `claim`, `inv`, `map`, `help`, `status`.
- `status()` at `mag/game_mud.py:600`.
- `main()` at `mag/game_mud.py:610`.

State surfaces via `game_world`: `game.mud.player`, `game.mud.claimed`, `game.mud.hall_record`.

LACKS for the party-chat loop: no party chat thread linkage. No chan integration. No `post` verb. No rival build forking. No gate scoring. No red-team step.

## tools/tavern.py
Provides multi-agent multi-turn scenes on `hermes_burn` rails.
- `PLAY_DIR = ROOT / "watch" / "inbox" / "playground"` at `tools/tavern.py:40`. `ESC_BRAWL = 18` at `tools/tavern.py:41`.
- `LAWS` at `tools/tavern.py:43`. `TEMPER` at `tools/tavern.py:52`.
- `_roll(chain, scene, turn, actor)` at `tools/tavern.py:55`. Deterministic sha256 dice.
- `class Run` at `tools/tavern.py:59`. Methods:
  - `__init__(scenario, rounds, budget_usd, dry, judge_model, chain_tip)` at `tools/tavern.py:60`.
  - `row(**kw)` at `tools/tavern.py:75`. Writes to `transcript.jsonl` and `play.md`.
  - `_paid(model, messages, max_tokens, tag, **row_kw)` at `tools/tavern.py:88`. Calls `hermes_burn._call`, banks usage via `_bank`.
  - `bar_round(rnd)` at `tools/tavern.py:110`.
  - `judge_round(rnd)` at `tools/tavern.py:150`.
  - `_lines()` at `tools/tavern.py:175`.
  - `play()` at `tools/tavern.py:190`. Writes `DONE`.
- `main()` at `tools/tavern.py:210`.

State surfaces: `watch/inbox/playground/<kind>_<stamp>/transcript.jsonl`, `play.md`, `scenario.json`, `DONE`.

LACKS for the party-chat loop: no thread opening from gap register. No direct chan post. No `game_mud` room mapping. No workflow gate scoring. No red-team step.

## tools/dungeon.py
Provides dice-law D&D carrier, FIGHT CLUB arena session 0.
- `PLAY_DIR` at `tools/dungeon.py:44`. `MODULE` at `tools/dungeon.py:45`. `GENESIS` at `tools/dungeon.py:46`.
- `ROSTER` at `tools/dungeon.py:48`. `DM_MODEL` at `tools/dungeon.py:60`. `WARDEN` at `tools/dungeon.py:61`. `S1_BEATS_CAP` at `tools/dungeon.py:62`. `INITIATIVE` at `tools/dungeon.py:63`.
- `S0_HOOK` at `tools/dungeon.py:65`. `S1_SHEET` at `tools/dungeon.py:70`.
- `_check_links_405()` at `tools/dungeon.py:80`. Counts `watch/inbox/LINKS.jsonl` rows, expects 405.
- `_check_room_big()` at `tools/dungeon.py:90`. Checks `watch/room.jsonl` size > 1MB.
- `_check_zombie_budget()` at `tools/dungeon.py:95`. Counts `4,156` in `AGENTS.md`.
- `REAL_SCROLLS` at `tools/dungeon.py:100`. Three real byte checks: Ledger Page, Room Deed, Census Stub.
- `strip_and_cap(speech, cap=120)` at `tools/dungeon.py:110`.
- `roll(pre)` at `tools/dungeon.py:115`.
- `check_golden()` at `tools/dungeon.py:120`.
- `class Dungeon` at `tools/dungeon.py:125`. Methods:
  - `__init__(tip, dry, budget)` at `tools/dungeon.py:126`.
  - `row(**kw)` at `tools/dungeon.py:142`.
  - `_paid(model, messages, max_tokens, tag)` at `tools/dungeon.py:158`. Calls `hermes_burn._call`, banks usage.
  - `_dm(beat)` at `tools/dungeon.py:185`.
  - `_verdict(actor, speech)` at `tools/dungeon.py:210`. Parses tags, applies quirks, dice law.
  - `_pc_beat(actor)` at `tools/dungeon.py:280`.
  - `_warden_beat()` at `tools/dungeon.py:320`.
  - `_tail()` at `tools/dungeon.py:345`.
  - `s0()` at `tools/dungeon.py:360`.
  - `s1()` at `tools/dungeon.py:380`.
  - `play()` at `tools/dungeon.py:420`.
- `main()` at `tools/dungeon.py:430`.

State surfaces: `watch/inbox/playground/dnd0_<stamp>/transcript.jsonl`, `session.md`, `golden_vectors.json`, `DONE`.

LACKS for the party-chat loop: no party chat thread linkage. No chan integration. No gap register. No workflow gate scoring.

## tools/hermes_burn.py
Provides paid dispatch to Nous inference API.
- `OUT_DIR` at `tools/hermes_burn.py:64`. `USAGE` at `tools/hermes_burn.py:65`. `API_HOST` at `tools/hermes_burn.py:66`. `API` at `tools/hermes_burn.py:67`.
- `PRICING` at `tools/hermes_burn.py:70`. Per-token USD: opus-5.5 (0.000004, 0.00002), sonnet-5.5 (0.000002, 0.00001), fable-5.1 (0.00001, 0.00005), haiku-4.5 (0.000001, 0.000005).
- `_now()` at `tools/hermes_burn.py:78`.
- `_hermes_key()` at `tools/hermes_burn.py:82`. Reads `.env`, prefers `HERMES_API_KEY_2`.
- `_assert_public_endpoint()` at `tools/hermes_burn.py:92`.
- `_call(model, messages, max_tokens, key, retries=1)` at `tools/hermes_burn.py:100`. Performs HTTP POST with endpoint fence.
- `_read_evidence(paths)` at `tools/hermes_burn.py:130`.
- `_bank(row)` at `tools/hermes_burn.py:145`. Appends to `USAGE`, checks doubled keys.
- `_system_for(model)` at `tools/hermes_burn.py:155`. Uses `mag.claritas.face_for` plus estate laws.
- `_refusal_state(ask_id)` at `tools/hermes_burn.py:170`.
- `_mint_refused_marker(ask_dir, ask_id, snippet)` at `tools/hermes_burn.py:185`.
- `_landed_skip(meta, ask_dir, out_path)` at `tools/hermes_burn.py:195`.
- `_assert_evidence_in_body(meta, messages)` at `tools/hermes_burn.py:215`.
- `run_ask(ask_dir, key, execute=True)` at `tools/hermes_burn.py:235`. Atomic claim, calls `_fire_ask`.
- `_fire_ask(ask_dir, key, execute=True)` at `tools/hermes_burn.py:250`. Stages prompt, evidence preflight, calls `_call`, banks usage, writes output.
- `main(argv)` at `tools/hermes_burn.py:340`.

State surfaces: `memory/runs/hermes_burn/usage.jsonl`, `watch/inbox/hermes_burn/<id>.md`, ask dirs with `ask.json`, `revision.md`, `REFUSED`.

Schemas: usage row `{ts, id, model, turn, prompt_tokens, completion_tokens, cost_usd, ok, ...}`.

LACKS for the party-chat loop: no party-chat-specific ask staging. No direct integration with `chan` or `game_mud`.

## configs/kabuki_cast.json
Provides rotating cast for Hermes salons.
- `schema: "kabuki_cast.v1"` at `configs/kabuki_cast.json:2`.
- `fallback_model` at line 5. `default_account` at line 6.
- `actors` at line 7. Each actor has `stage_name`, `seat`, `model`, `account`, `max_words`, `persona`, `tier_note`.
- First actor ARAGOTO at line 9. Last HANA-GUMO at line 54.
- Default model for all actors: `inclusionai/ling-3.0-flash-sante:free`. Tier notes mention `anthropic/claude-fable-5.1:batch`, `google/gemini-3.8-flash`, `openai/gpt-6-astra`.

LACKS for the party-chat loop: no runtime code. No integration with `hermes_burn` or `chan`. No gap register. No claim mapping. No build forking.

# 2. THE GLUE SPEC

New file: `tools/partychat.py`. It composes the six surfaces into one party-chat loop. It is buildable in one sitting.

## Module constants
```python
SCHEMA = "partychat.v1"
ROOT = Path(__file__).resolve().parents[1]
GAP_REGISTER = ROOT / "watch" / "inbox" / "gap_register.jsonl"  # UNVERIFIED: file not in evidence
PARTY_ROOT = ROOT / "watch" / "inbox" / "partychat"
KABUKI_CAST = ROOT / "configs" / "kabuki_cast.json"
ROOM_PATH = ROOT / "watch" / "room.jsonl"
USAGE_PATH = ROOT / "memory" / "runs" / "hermes_burn" / "usage.jsonl"
```

## Function-by-function spec

### `def _load_gap(gap_id: str, path: Path | None = None) -> dict`
Read `gap_register.jsonl` (UNVERIFIED path). Find the row where `id == gap_id`. Return the row. Required fields: `id`, `title`, `question`, `room`, `evidence` (list of repo-relative paths). Raise `KeyError` if missing.

### `def _room_for_gap(gap: dict) -> str`
Return `gap["room"]` if it is a key in `mag.game_mud.ROOMS`. Else map by heuristic: if `"ledger"` in title, return `"the World-Memory"`; if `"room"` in title, return `"the Hall of Shared Supper"`; else default `"the Hall of Shared Supper"`. Validate against `mag.game_mud.ROOMS`.

### `def open_thread(gap_id: str, *, gap_path: Path | None = None, room_path: Path | None = None) -> dict`
- Load gap row.
- Slug = `mag.chan.slugify(gap["id"] + "-" + gap["title"])`.
- If thread already has posts in `watch/room.jsonl`, return `{"ok": True, "thread": slug, "existing": True}`.
- Post OP via `mag.chan.post(slug, text=gap["question"], seat="primer", path=room_path)`.
- Map thread to room: store mapping in `watch/inbox/partychat/<slug>/room.txt` with the room name.
- Return `{"ok": True, "schema": SCHEMA, "thread": slug, "room": room, "gap_id": gap_id}`.

### `def _kabuki_cast(path: Path | None = None) -> dict`
Load `configs/kabuki_cast.json`. Return the parsed dict. Validate `schema == "kabuki_cast.v1"`.

### `def _face_for(seat: str, cast: dict) -> dict`
Find actor where `actor["seat"] == seat`. Return actor dict. If not found, return fallback actor with `stage_name="ANON"`, `seat=seat`, `model=cast["fallback_model"]`, `persona="You are Anonymous on /keep/."`, `max_words=350`.

### `def _stage_ask(thread: str, seat: str, *, contract: str, evidence: list[str], model: str | None = None, max_tokens: int = 800) -> Path`
Create ask dir `watch/inbox/partychat/<thread>/<seat>/`. Write `ask.json` with:
```json
{
  "id": f"PARTYCHAT_{thread}_{seat}",
  "model": model or face["model"],
  "system": face["persona"] + "\n\nESTATE LAWS: no em-dashes. Cite file:line for claims. One post, no markdown headings.",
  "evidence": evidence,
  "contract": contract,
  "max_tokens": max_tokens
}
```
If `revision.md` exists in the dir, keep it. Return ask dir.

### `def _paid_post(thread: str, seat: str, *, contract: str, evidence: list[str], model: str | None = None) -> dict`
- `ask_dir = _stage_ask(...)`.
- `key = hermes_burn._hermes_key()`.
- `result = hermes_burn.run_ask(ask_dir, key, execute=True)`.
- Read output from `watch/inbox/hermes_burn/PARTYCHAT_<thread>_<seat>.md`.
- Return `{"ok": True, "text": content, "cost_usd": result.get("cost_usd", 0.0), "ask_dir": str(ask_dir)}`.

### `def party_post(thread: str, seat: str, *, text: str | None = None, model: str | None = None, room_path: Path | None = None) -> dict`
- If `text` is None:
  - Load cast, get face.
  - Evidence = `["watch/room.jsonl", "watch/inbox/partychat/<thread>/gap.json"]` plus any files named in gap row.
  - Contract = `f"You are in thread {thread}. The gap is: {gap['question']}. As {face['stage_name']}, post one message. If you have a proposal, start a line with 'PROPOSAL: '. If you have a claim, start a line with 'CLAIM: '. Otherwise shitpost or lurk."`
  - `out = _paid_post(thread, seat, contract=contract, evidence=evidence, model=model)`.
  - `text = out["text"]`.
- Post via `mag.chan.post(thread, text, seat=face["seat"].lower(), path=room_path)`.
- Return `{"ok": True, "schema": SCHEMA, "thread": thread, "seat": seat, "text": text, "posted": True}`.

### `def claim(thread: str, room: str | None = None) -> dict`
- Load thread-to-room mapping. If `room` is None, use mapped room.
- Call `mag.game_mud.claim(room)`.
- Post the result to the thread via `mag.chan.post(thread, text=f"CLAIM: {result['claimed']}", seat="primer")`.
- Return `{"ok": True, "schema": SCHEMA, "thread": thread, "room": room, "claim": result}`.

### `def fork_builds(thread: str, proposals: list[dict], *, build_root: Path | None = None) -> dict`
- `build_root = build_root or PARTY_ROOT / thread / "builds"`.
- For each proposal (dict with `id`, `proposal`, `seat`):
  - Create `build_root / proposal["id"]`.
  - Write `spec.md` with the proposal text and the gap question.
  - Write `build.json` with `{"thread": thread, "proposal_id": proposal["id"], "seat": proposal["seat"], "created": _now()}`.
- Call `tools.workflow_gate.score_build(build_dir)` for each build. **UNVERIFIED**: `tools/workflow_gate.py` is not in the evidence. Expected signature: `score_build(build_dir: Path) -> dict` returning `{"ok": bool, "score": float, "receipt": str, "gates": list}`.
- Return `{"ok": True, "schema": SCHEMA, "thread": thread, "builds": [{"id": ..., "score": ..., "receipt": ...}]}`.

### `def red_team(build_dir: Path, *, thread: str, actor: str = "ractor") -> dict`
- Evidence = `[str(p) for p in build_dir.rglob("*") if p.is_file()]`.
- Contract = `f"Red-team the build at {build_dir}. Find a false claim, a non-reproducible step, or a security hole. Output FINDINGS: <one line per finding>. If none, output CLEAR."`
- Use `_paid_post(thread, actor, contract=contract, evidence=evidence, model="anthropic/claude-opus-5.5")`.
- Write `red_team.md` into `build_dir`.
- Return `{"ok": True, "schema": SCHEMA, "build_dir": str(build_dir), "findings": text, "clear": "CLEAR" in text}`.

### `def run_thread(gap_id: str, *, rounds: int = 3, budget_usd: float = 0.25) -> dict`
- `thread_info = open_thread(gap_id)`.
- `thread = thread_info["thread"]`.
- Copy gap row to `watch/inbox/partychat/<thread>/gap.json`.
- Load cast. `seats = [a["seat"] for a in cast["actors"]]`.
- `spend = 0.0`.
- For `rnd in range(rounds)`:
  - For `seat in seats`:
    - `out = party_post(thread, seat)`.
    - `spend += out.get("cost_usd", 0.0)`.
    - If `spend >= budget_usd`: break all.
- Collect proposals: read all posts in thread, extract lines starting with `PROPOSAL: `. If >=2, `fork_builds(thread, proposals)`.
- For each build, if `score >= 0.8` (UNVERIFIED threshold), `red_team(build_dir, thread=thread)`.
- If any build is `clear` and `score >= 0.8`, call `claim(thread, room)`.
- Write `watch/inbox/partychat/<thread>/DONE` with `{"spend_usd": spend, "rounds": rounds, "landed": bool}`.
- Return `{"ok": True, "schema": SCHEMA, "thread": thread, "spend_usd": spend, "landed": landed}`.

### `def main(argv: list[str] | None = None) -> int`
CLI:
```
python -m tools.partychat open GAP_ID
python -m tools.partychat post THREAD SEAT [TEXT]
python -m tools.partychat claim THREAD [ROOM]
python -m tools.partychat run GAP_ID [--rounds N] [--budget-usd X]
```
Dispatch to the functions above. Return 0 on success, 1 on error.

# 3. THE MUD VERB LAYER

Map `chan` threads onto `game_mud` rooms so the party can walk between problem rooms.

## Thread-to-room mapping
Each party-chat thread has a `room` field in its OP row. `open_thread` writes a mapping file at `watch/inbox/partychat/<thread>/room.txt`. The room must be a key in `mag.game_mud.ROOMS` (`mag/game_mud.py:58`). Example: gap `GAP-LINKS-405` maps to `"the World-Memory"` because the claim is about `LINKS.jsonl` (the ledger).

## Verb: `go <room>`
Signature: `def go(thread: str, target_room: str) -> dict`
- Load current room from `game_mud._player()["room