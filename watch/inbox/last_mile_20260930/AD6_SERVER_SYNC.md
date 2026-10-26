# AD6 — SYNC: the estate's LW5-LW8 server waves land in the-mountain (2026-09-30)

Lane AD6. Mission: AC11's named out-of-scope gap — the estate `server/`
tree (LW5-LW8: persistence/replay, anti-cheat rate caps, innkeeper bot,
chat say/whisper, the Z1 weld verdict feed) was ahead of the Y5 snapshot
vendored in `the-mountain/server/`. Sync it, update the README, commit
(NEVER push), verify the demo entry point. Receipt-first: every number
below is from executed commands, run 2026-09-30.

## Commit (the-mountain repo — committed, NEVER pushed)

- **Hash:** `cf2ec7d` (full `cf2ec7d` on `main`, parent `d99b9ea`/AC11)
- 13 files changed, +2,886 / −68. Working tree clean after;
  `origin/main..HEAD` = 2 (AC11 + AD6, local-only per the never-push law).

## Diff census (estate server/ vs the-mountain/server/, pre-sync)

- SAME (untouched since Y5, cmp-verified): `auth.py`, `protocol.py`,
  `room.py`, `ws_door.py`, `__init__.py`, `verdict_feed.py` (the X11 file
  itself was already current; only its imports needed the vendor rewrite)
- DIFF: `world.py` (chat channel + snapshot hooks), `protocol_table.py`
  (motion dialect X9 + chat LW6 + anticheat LW7 contracts + ReceiptGate),
  `server.py` (nonce law, dispute routing, verdict-feed wiring, stats)
- NEW: `innkeeper.py` (LW8), `persistence.py` (LW5/S18)
- Vendored physics `_vendor/water_graph.py`: byte-identical to estate
  HEAD at sync time (cmp PASS).

## What landed in the-mountain (byte-verbatim except marked lines)

| the-mountain file | estate source | bytes vs estate |
|---|---|---|
| `server/world.py` | `server/world.py` | 1 import line adapted (Y5 pattern carried forward) |
| `server/protocol_table.py` | `server/protocol_table.py` | byte-identical (cmp PASS) |
| `server/server.py` | `server/server.py` | 1 import line adapted |
| `server/innkeeper.py` | `server/innkeeper.py` | byte-identical (cmp PASS) |
| `server/persistence.py` | `server/persistence.py` | 1 import line adapted |
| `server/verdict_feed.py` | `server/verdict_feed.py` | 4 import lines adapted |
| `server/_vendor/gwap_payload.py` | `mag/gwap_payload.py` | ROOT-fallback line adapted (vendored one level deeper) |
| `server/_vendor/gwap_mud.py` | `mag/gwap_mud.py` | 2 import lines adapted |
| `server/_vendor/gwap_to_gps.py` | `mag/gwap_to_gps.py` | ROOT fallback + 3 import lines adapted |
| `server/_vendor/ledger.py` | `tools/gps_mcp/ledger.py` | byte-identical (cmp PASS) |
| `server/_vendor/__init__.py` | — | rewritten: documents the five-file vendor set + re-sync law |

Vendoring law (AC11's, extended): every adapted line carries an inline
`# AD6 2026-09-30` comment naming the estate original; re-sync = copy the
estate file over, re-apply the marked lines. All 14 adaptations applied
by a count-asserted script (each replacement verified to occur exactly
once); `diff` against the estate originals shows ONLY the marked hunks.
A first text-mode pass flipped line endings (universal-newline read +
os.linesep write); caught by whole-file diff, redone in binary mode —
the committed bytes preserve the estate's line endings byte-for-byte.

README updates in the-mountain: root `README.md` server bullet (Layout)
now describes the LW5-LW8 surface + vendor closure; B1 Status de-staled
("blocked on the bots port" was false since Y5). `server/README.md`:
vendored-copy note rewritten for AD6, size table re-measured (wc -l,
2026-09-30: protocol_table 662, world 362, persistence 309, innkeeper
369, server 503, verdict_feed 388, _vendor 5 files 2041), verbs +
reject codes now carry say/whisper/BAD_TEXT/RATE_CAP/STALE_NONCE,
v1-owes marks persistence + rate caps landed, Tests section names the
estate-side suites and the AD6 in-repo measured runs.

## Verification (estate venv, the-mountain as cwd — the Y5/AC11 idiom)

- `.venv/Scripts/python.exe -m server.server --demo` → **exit 0**,
  `THE CROWN FILLS. WIN at tick 4; boiler boiled 4, tagger tagged 30.`
  (same WIN-at-tick-4 as the Y5 and AC11 proofs), and the LW7 counters
  are live in the stats line: `{'clients': 2, 'ticks': 30,
  'actions_staged': 34, 'rate_capped': 0, 'stale_nonce': 0,
  'tag_disputes': 0}` (the demo client rides the nonce path).
- `-m server.protocol_table` → exit 0, prints the frozen contract JSON.
- Import smoke: all 15 modules (11 server + 5 _vendor) import clean;
  CHAT_TABLE verbs = boil/join/say/tag/valve/whisper; ANTICHEAT_TABLE
  carries RATE_CAP + STALE_NONCE.
- Functional smoke: `Innkeeper.attach()` registers the socket-less
  session at spring; `pump()` on a live tick returns
  {memory, motion, say, tick}; `persistence.save()` → `load()` replays
  the chain (volumes equal = True).
- Re-ran the demo on the exact committed state before `git commit`.

## Out of scope, named

- **AC2 fracture (in-flight, uncommitted on the estate):** DURING this
  sync, estate `mag/water_graph.py` + `roblox_to_godot/systems/
  water_graph.gd` gained the pipe-fracture law as UNCOMMITTED working-
  tree edits (mtime 2026-09-30 07:14 EDT, mid-session — the vendored
  copy compared CURRENT at session start, then diverged). Verified:
  the-mountain's `_vendor/water_graph.py` == estate **HEAD**
  (`git show HEAD:mag/water_graph.py` cmp PASS). Racing a live lane's
  uncommitted bytes would vendor a torn copy, so the fracture stays out;
  the next physics sync lane copies it once AC2 commits.
- Tests: the estate suite owns all server tests (test_server_p0/v0,
  test_server_persist, test_anticheat, test_chat, test_innkeeper,
  test_protocol_table, test_motion_rows, test_verdict_feed);
  the-mountain ships no tests, per Y5.
- `server/users.json` (estate runtime artifact) not synced, per Y5.

— AD6 sync seat, 2026-09-30
