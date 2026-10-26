# R9 — MOUNTAIN SYNC: auth + rooms + netcode waves land in the-mountain (2026-09-30)

Lane R9 (last_mile). Mission: the-mountain was behind on the auth work.
(1) sync the estate server tree (SRP6, rooms, identity binding, protocol
updates) per the AD6 vendoring pattern; (2) sync the client (netcode
snapshot ring, title screen, parity-fixed water_graph.gd, event ring);
(3) ONBOARDING.md gets the auth section; (4) commit cold-readable, NEVER
push. This file is the receipt.

## Commit (the-mountain — committed, NEVER pushed)

- **Hash:** `c38ded6` (on `main`, parent `fa8b763`, the R6-followup lane's
  commit that landed mid-session)
- 29 files changed, +4,598 / −312. Working tree clean after;
  `origin/main..HEAD` = 6 (all local-only per the never-push law).

## What landed (byte-verbatim except marked lines, every copy cmp-verified)

| the-mountain file | estate source | wave |
|---|---|---|
| `server/auth_srp6.py` | `server/auth_srp6.py` | B4+**R5**: RFC 5054 2048-bit/SHA-256 DEFAULT (the 256-bit mangos variant behind `allow_mangos`), decoy challenges, single-use handshakes. 1 import line adapted (`tools.realmd_client` -> vendor) |
| `server/_vendor/realmd_client.py` | `tools/realmd_client.py` | NEW vendor: the LW4 realmd-proven SRP6 math, byte-identical, zero adapted lines |
| `server/frame_mac.py` | `server/frame_mac.py` | **R3**: post-auth per-frame MACs (HKDF from K, seq law, BAD_MAC + mac_tamper chain row). 1 import line adapted |
| `server/rooms.py` | `server/rooms.py` | B15: GameRoom/RoomBook, byte-identical |
| `server/identity_binding.py` | `server/identity_binding.py` | V7: GitHub-keys + sshsig identity binding, byte-identical |
| `server/protocol.py` | `server/protocol.py` (HEAD at sync) | SRP6 builders + MAC field law, byte-identical |
| `server/protocol_table.py` | `server/protocol_table.py` | SRP6 frozen rows, byte-identical (digest `4981f23e…` pinned) |
| `server/server.py` | `server/server.py` (HEAD at sync) | SRP6 dispatch + frame-MAC arming + rooms wiring; 1 import line adapted (the AD6 gwap line, re-applied) |
| `server/_vendor/water_graph.py` | `mag/water_graph.py` | R8 int-domain law, byte-identical |
| `server/_vendor/ledger.py` | `tools/gps_mcp/ledger.py` | LM7 positive arm (momentum badges), byte-identical |
| `game/network/net_client.gd` + `snapshot_buffer.gd` | twin `network/` | B3: 32-snapshot ring, t-100ms, freeze-never-extrapolate, exactly-once events |
| `game/scenes/title.gd` + `title.tscn` | twin `scenes/` | B14: the title door; `game/project.godot` main_scene -> title.tscn |
| `game/systems/water_graph.gd` | twin (see race note) | D1 probe-time reserve + R8 + Z10 hydrology geometry |
| `game/scripts/game.gd`, `hud.gd`, `juice.gd` | twin `scripts/` | B2 event ring (64-slot) + AJ4 water_event signal wiring + title wiring |
| `game/systems/game_constants.gd`, `fish_brain.gd`, `flock.gd`, `water_particles.gd` | twin | the game_constants extraction (synced by the sibling seat at 19:45, adopted here after cmp == twin) |

Docs: `ONBOARDING.md` auth section (register, the 3-message SRP6 flow,
decoys/replay laws, frame MACs, identity binding, rooms) + title-screen
run/controls updates; `server/README.md` re-measured surface (15 modules,
_vendor now 6 files / 2,770 lines); root `README.md` bullets; `.gitignore`
gains `logs/` + `server/srp_users.json`.

## Races handled (the AD6 law: never vendor a live lane's uncommitted bytes)

1. **R3 frame-MAC + R5 RFC-5054 raced this lane.** At session start
   `server/protocol.py`/`server.py` were working-tree M and
   `frame_mac.py` untracked; the first server sync took those two from
   estate **HEAD** (9ed2c153f-era). Mid-session commit `0b846c01f`
   (R12: "server bytes committed — existed NOWHERE ELSE") settled all of
   it; the sync then RE-TOOK auth_srp6/protocol/server/frame_mac from the
   committed tree. Final state = estate HEAD bytes everywhere.
2. **`roblox_to_godot/systems/water_graph.gd` is STILL uncommitted-M in
   the estate (Z10 hydrology lane).** A sibling seat synced the twin's
   working-tree bytes into the-mountain at 19:45:59. Kept (not reverted):
   stable 35+ min at sync close, parse-clean under the full Godot battery,
   byte-identical to the twin, and certified coherent with the vendored
   `.py` by the estate's own gate — `tools/rule_parity.py all --quick`
   -> **PARITY: ok, rows py=1220 gd=1220, zero divergence** (run this
   session). If the Z10 lane amends before committing, the next sync
   re-copies.
3. **the-mountain itself moved mid-session**: R6's `56be431` (BootIntegrity
   autoload + export_presets) landed with an explicit "main_scene is the
   sync lane's set" note — this lane set it — plus `fa8b763` followup;
   both stack under this commit cleanly.

## Verification (bytes; estate venv + Godot 4.3 console exe, the-mountain cwd)

- `-m server.server --demo` -> exit 0, **WIN at tick 4**; stats carries
  the new counters (`rooms:1, srp_sessions:0, bad_proof:0,
  stale_challenge:0, mac_sessions:0, mac_tampers:0`).
- 14 server modules import clean (incl. frame_mac + the 6-file vendor).
- **Live SRP6 TCP roundtrip on the vendored bytes**, client side an
  INDEPENDENT RFC 5054 §2.6 mirror (per the estate test's
  `rfc_client_session` formula): challenge -> proof ->
  `welcome{auth:"srp6", m2 (mutual match), room:"summit"}` -> boil `ack`
  (nonce path) -> tick; replayed proof -> `STALE_CHALLENGE`; unknown user
  -> byte-shaped decoy challenge; `stats.srp_sessions == 1`.
- Store law: register writes salt+verifier only; password absent from disk.
- Digests pinned: `SRP6_AUTH_DIGEST 4981f23e…`, `IDENTITY_AUTH_DIGEST
  9de8ad04…`, `PROTOCOL_DIGEST d41f7cba…` (B4/V7/LW7 values, unmoved).
- Godot 4.3 headless (after a clean `.godot` rebuild): `--import` x2 ->
  0 script/parse errors; title boot 300f -> exit 0, 0 errors (ARTIFACT_ID
  line from R6's autoload); `scenes/main.tscn` 300f solo AND against a
  live `--port 8811` server -> exit 0, 0 errors; `MAG_HYDROLOGY=1` 300f ->
  exit 0; gravity demo 300f -> exit 0, both AH15 probes. Import cache
  deleted after (AH15 idiom).
- My serve-mode smoke's runtime artifacts (`logs/`, `server/users.json`,
  `server/srp_users.json`) deleted from the-mountain before commit (Y5
  law); `.gitignore` now guards the first two paths.

## Owed next (not this lane)

- Estate: identity_challenge/identity_proof op-ladder wiring into
  server.py (V7's "owed next"); commit the Z10 .gd lane; GDScript bignum
  client for the 2048-bit group (F4.2 benchmark owed); s2c broadcast
  sealing; room selection on the SRP6 door; flip `allow_plaintext_hello` /
  `require_frame_mac` defaults when soaked.
- the-mountain: no tests shipped (Y5 law — the estate suite owns them:
  test_auth_srp6, test_frame_mac, test_rooms, test_identity_binding,
  test_server_v0 …).

— R9 sync seat, 2026-09-30

## Refire addendum (2026-09-30 ~20:05 EDT, independent refire session)

The refire seat verified the landed commit `c38ded6` file-by-file AFTER the
close above (its own staged set was committed by the sync seat in the
concurrent window; contents re-proven regardless of who typed `git commit`):

- **Full-twin sweep:** every estate `roblox_to_godot/` file under
  `scripts/ systems/ scenes/ network/` plus `project.godot` is content-identical
  to the mountain's committed `game/` (flock.gd on-disk differs CRLF-only;
  0 content diff with CR stripped; `core.autocrlf` normalizes at commit).
- **Server tree:** all files 0 content diff vs estate except the three marked
  vendor-import lines (auth_srp6, frame_mac, server.py gwap). `DEFAULT_GROUP
  = "rfc5054-2048"` verified in the committed bytes.
- **Committed `game/systems/water_graph.gd` has 0 tab-indented lines** — the
  first attempt's copy had carried the twin's mid-flight tab mixture (39 tab
  lines, the B2-named parse killer); the 19:45 sibling re-copy (credited in
  race note 2) landed the space-indent truth, and this addendum pins it in
  HEAD.
- **Parse-tree proof beyond title smoke:** direct `res://scenes/main.tscn`
  headless load (120f) exit 0 zero errors — forces game.gd's preload chain
  through game_constants.gd, the closure the first attempt left broken (the
  B2 lesson: title-only smokes do not surface main-scene parse breaks).
- `python -m server.frame_mac` (mountain cwd): self-check digest
  `f3b3e79a1af50d75e1112bd87582c79602847484ce5c1398336c335f16f90917`
  (R3's pin). Demo re-run: WIN tick 4, exit 0, new counters present.
- `game/README.md` doc drift repaired in-commit: ESC control row, title-door
  dual-mode paragraph, the falsified "network/ not carried" line, R9 sync
  receipt appended (house pattern).

— R9 refire seat, 2026-09-30
