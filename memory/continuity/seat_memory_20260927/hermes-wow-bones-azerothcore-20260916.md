---
name: hermes-wow-bones-azerothcore-20260916
description: Hermes session "hello" (325 msgs, deepseek-flash) — cloned AzerothCore
  (upstream renamed azerothcore-wow→azerothcore-wotlk, why the 09-02 stub 404'd),
  authored wow_bones.v1 (bones as data — 725 client/587 server opcodes, kernels
  Dispatch/Instance/Stream seeded-RNG replay law) + 15-row six-slot L0 steal map
  byte-verified 15/15; 24/24 tests pass (independently re-run by zcode); NT-ACv2
  guild = AzerothCore v2 — tonight's bot is the front door, the kernel is the room;
  safeguard commit 30e5ec7e2; handoff unpicked → zcode built the referee
  wow_bones_session.py (35/35, both falsifiers pass); /bones adapter + channel
  click still open
metadata:
  node_type: memory
  type: project
  originSessionId: sess_727c2fc5-be79-4f45-a7a4-229c471b2b9b
---

"Look what hermes is cooking" — operator handed over the Hermes session export
(`Desktop/New folder/hello-20260915.json`, session `20260915_201711_4c0831`,
325 messages, deepseek-flash). Arc: "hello" → "how can we map it to our game"
(in `projects/azerothcore-wow`, an empty stub) → steer "self steal wow clone" →
"what's it take to launch a server for one person" → "self steal we want the
BONES of this thing and the ability to test against it, not the client — like
rebuilding photoshop from scratch without the bullshit" → "who else has done
this, look at turtle wow. steal."

**What Hermes shipped (verified independently — 24/24 tests pass in 4.09s on
my own pytest run):**

1. **The clone:** 10,409 files, 1,210 MB (`.git` 331, `data/` 825, `src/` 32),
   HEAD `f68a9759`. 73% SQL, 1,212 `.cpp` — "the huge project is mostly data
   and content, not machinery." **Gotcha:** upstream RENAMED
   `azerothcore/azerothcore-wow` → `azerothcore-wotlk` (the old URL 404s —
   why the 09-02 stub never fetched).
2. **`mag/wow_bones.py` (366 lines) — wow_bones.v1:** the laws as DATA, parsed
   not built: 725 client verbs / 587 server verbs (byte-checked, self-caught
   its own 726→725 `#define` off-by-one), 6 session statuses, 3 processing
   places, 6 encounter states → `bones.json` + `bones_digest`. GPL-2.0 clean:
   "we copy no code — contracts only, cited by path + symbol."
3. **Three kernels (claims are passing tests):** Dispatch = the ORDERING law
   (status gate evaluated BEFORE the verb; proven at `WorldSession.cpp:436`);
   Instance = the ENCOUNTER law (NOT_STARTED/IN_PROGRESS/FAIL/DONE/SPECIAL +
   TO_BE_DECIDED; a load is not a transition; DONE refused while a world-boss
   minion lives); Stream = the RNG law — seeded stream where every draw records
   its index, with the night's best line: AzerothCore's `urand()` is
   process-global/unseeded/unrecorded so "replay or RNG_DIVERGE can never be
   proven — **we test against their design by proving the property theirs
   cannot have.**"
4. **15-row six-slot L0 steal map** (`docs/ref/WOW_ACORE_STEAL_MAP_20260915.md`):
   stance ledger 7 steal / 3 adapt / 3 reject / 2 content; `mag/wow_steal.py
   verify` = 15/15 rows, 33/33 citations byte-checked, digest `ec40594529b7`.
   Signature rejects: R07 global RNG (unreplayable ⇒ divergence unprovable),
   R12 MySQL-as-authority ("the world state IS the verkle protocol"), R15
   scale machinery ("our world proves 37 entities on a self-verifying root").
   R14 confirms the switchboard: identity ≠ world authority, "model text
   proposes, only the broker authorizes."
5. **`docs/ref/WOW_FAMILY_LINEAGE_20260915.md`** + `mag/wow_family.py`,
   `mag/wow_manifest.py` + tests. Executes the [[from-mud-to-wow-article]] gap
   analysis.

**The connection:** the Discord guild wired tonight is **NT-ACv2 = AzerothCore
v2** — the bot was the front door, wow_bones is the room. Obvious next move:
Mag bot referees headless bones-kernel sessions in #game-c-overview
(replayable, divergence-provable, Discord-visible).

**Open flags:** two game engines now exist (mud.html + wow_bones kernel) —
convergence question, but bones-as-data is cheap and non-colliding. Hermes'
files were UNTRACKED at session end — safeguard checkpoint `30e5ec7e2` (my
commit, attributed). Hermes session may still be live/cooking.

**DIRECTED (2026-09-16, operator teaching moment — "take what it is doing and
direct it at our goals"):** bones-as-referee directive issued —
`watch/inbox/HERMES_DIRECTIVE_BONES_REFEREE_20260916.md` +
`queue/handoff/HANDOFF-2026-09-16-bones-referee.json` (handoff.v1; queue/
handoff is disk-resident/gitignored — durable copy lives in watch/inbox).
One artifact: `wow_bones session` runner (start/turn/status/receipt,
`wow_session.v1` receipt = {session_id, seed, draw_index, moves[], verdict,
sha256}) + thin `/bones` Discord surface on the Mag bot in #game-c-overview =
the Sep-20 end-to-end proof demo. Falsifiers: same seed+moves twice =
byte-identical receipt sha256; flipped draw names RNG_DIVERGE. Anti-goals =
its own map rows R07/R09/R12/R15. Commit c6b3f5ba0. Lesson filed at
[[directing-seats-lesson]].

## FAN-OUT ROUND (same session continued — operator relayed Hermes' report)

Hermes then ran a 50-wide research fan-out + corpus self-steal and reported
with exemplary receipt discipline (3 of its own broken metrics + a buggy probe
written down, not swept):

- **Fan-out:** 50 questions / 5 themes, 9 free lanes, **50/50 answered, $0**
  (pass 1: 25/50 — free reasoning models burn the whole budget in the
  reasoning channel and return `empty_content`; pass 2 raised budget to 3,000
  + backoff, recovered all 25). Lanes: groq-oss 9 · cerebras-oss 7 ·
  mistral-min8 7 · or-nemotron 6 · groq-qwen 5 · zai-47 5 · or-ling3 4 ·
  zai-air 4 · groq-oss20 3. Dead Gemini key (401, stale); mistral-small +
  or-glm52 429 at concurrency. Artifacts: `mag/research_fanout.py`,
  `memory/runs/research_50_wow/` (raw.jsonl 79,718 chars, receipt.json).
- **Corpus self-steal:** 1,203 files / 9.5 MB indexed+hashed (only 1 duplicate
  group — corpus isn't rotting); 425 game/steal/world material files. Verdict:
  **"doctrine-rich, data-poor"** — only 3 of 50 leads (A01, B06, E09) are
  defensible in-house; three of its own calibrations disagreed (loose 9/41,
  strict-broken 0/50, normalized 45/5/0) and it said so. Artifacts:
  `mag/corpus_selfsteal.py`, `memory/runs/corpus_selfsteal/`.
- **Lead check BLOCKED (receipted, not swept):** GitHub unauth API 60/hr
  exhausted; its probe printed 404 for 403s; no token exists (.env has only a
  commented placeholder), `gh` not logged in. 15 repos confirmed (TrinityCore,
  OpenMW, OpenRA, OpenRCT2, ServUO, EQEmu, Paper, Fabric, MinecraftForge,
  Bukkit, DarkPlaces, xash3d, AFLplusplus), 59 unchecked. Proof leads need
  checking: fan-out said mod-playerbots GPL-3.0, API says **GPL-2.0**.

**DECISIONS ISSUED (2026-09-16):** (1) GitHub token = operator hand —
fine-grained read-only public PAT → `GITHUB_TOKEN=` line in the hermes .env
(credentials from env only, never source); then the lead check can promote/kill
all 74 named repos. (2) Distill = **YES** — the 94 KB raw pack becomes a scored
byte-checked ledger: one row per repo → license via API → stance
(steal/adapt/reject/content, I4 map vocabulary) → six-slot link. Rationale:
raw leads confabulate (the GPL discrepancy is the proof); the ledger is the
only form that survives. Hermes' own conclusion: "the corpus's job is to
record which solved problem we took and refuse the rest." **"Doctrine-rich,
data-poor" is the corpus's first real self-knowledge** — the doctrine is the
three-year asset; the data gaps are what the fan-out exists to fill.

## SEP-20 GAP CHECK (2026-09-16, Explore-verified on disk)

Foundation real: bones.json fixture (229,534 bytes, digest efeb905b…), three kernels,
15-row steal map + wow_steal.py, live bot, clone at f68a9759. NOT BUILT (the thing the
demo is named after): `mag/wow_bones_session.py` (the session runner/referee),
`tests/test_wow_bones_session.py`, and ANY /bones Discord surface — the repo has zero
Discord command code (the bot's 169 slash commands are generic Hermes gateway tools;
discord.py-in-venv unverified; %LOCALAPPDATA%\hermes-agent\venv absent, only compiled
hermes.exe). Handoff HANDOFF-2026-09-16-bones-referee.json was NEVER picked up —
queue/handoff/hermes/INBOX holds only a Sep-12 note. Operator-side blockers:
#game-c-overview still 403 "Missing Access" (awaiting an operator click); decision gaps:
full-vs-demo scope (OPERATOR_ASK_20260916 item 4), who builds the adapter (hermes seat
silent vs reassign), gateway-native command vs standalone discord.py process. "24/24
tests" = 12 bones + 8 family + 4 manifest. An Adam demo script (what to type, what he
sees) is written nowhere.

## REFEREE BUILT (2026-09-16 burn window, zcode seat)

Handoff still unpicked + operator ordered compute burned wide/hard → zcode took the
contract over, falsifiers unchanged. **`mag/wow_bones_session.py` +
`tests/test_wow_bones_session.py` — 35/35 across the wow suite (11 new + 12 bones +
8 family + 4 manifest).** BOTH directive falsifiers pass: same seed+moves twice =
byte-identical receipt sha256; flipped draw → RNG_DIVERGE at the exact index. Bonus
proofs: CLI-splice determinism (play 3 turns, save, load, play 3 more → receipt
byte-identical to uninterrupted — exactly what the /bones adapter will do); world-boss
guard (--world-boss can never COMPLETE → EXHAUSTED at turn 8); receipt self-hash verified.
Game laws stated in module docstring (AUTHED→LOGGEDIN promotion draws nothing; first
LOGGEDIN verb = the load, no draw; every 3rd draw attempts DONE; TURN_LIMIT 8).
`wow_bones.py main()` now parse_known_args with `session` passthrough —
`python -m mag.wow_bones session start --seed S` works. **/BONES ADAPTER BUILT (2026-09-16
night):** `mag/bones_adapter.py` — standalone thin process, slash group /bones (start with
optional seed + world_boss / move / status / receipt / verbs), maps in-process to
BonesSession, ZERO game logic (a test scans the source to keep kernel internals out of the
adapter), guild-scoped 799817554549800982 + channel-gated #game-c-overview
1050760558883913780 (constants cite the setup receipt), token read at runtime from
%LOCALAPPDATA%\hermes\.env (never printed/stored), `--check` dry-run registers+prints
without reading the token. **17/17 tests** (offline, connect mocked). Launch:
`.venv\Scripts\python.exe -m mag.bones_adapter` (dry: `--check`). REMAINING for Sep-20:
the #game-c-overview 403 operator click, token rotation, Adam demo script (one paragraph,
written nowhere). **GATES DEFERRED (2026-09-16 evening):** operator explicitly put the
channel click + Netlify auth on hold — "wife is at the desk" — and confirmed the wave
doesn't block on them ("it's shit that you don't need to move forward"); don't push for
desk clicks, the adapter waits built and dry-run-verified.
