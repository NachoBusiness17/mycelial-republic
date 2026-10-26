# W3G MOUNTAIN SYNC - 2026-09-29

Mickey17 W3 lane: close the W2-owed sync gap (W2_MOUNTAIN_CLONEPROOF_20260929.md
"Owed"): the estate twin `roblox_to_godot/` was ahead of the-mountain `game/`.
Owner seat: zcode (GLM-5.3). Repo C:\Users\foste\Documents\projects\the-mountain,
commit yes, push NO (lane order; not pushed).

## Path note (mission discrepancy, resolved)

Mission text placed the estate twin at `Documents\local_sovereign_agent\
roblox_to_godot\`; that path does not exist. The real twin lives in this repo
(the estate whose watch/inbox files this receipt): `Documents\projects\
local_sovereign_agent\roblox_to_godot\`. No ambiguity in the bytes, only in
the lane order's path spelling.

## What landed (commit dca3801, amended from bd835df, branch main)

7 files changed, 426 insertions(+), 23 deletions(-):

- `game/scripts/net_client.gd` (NEW, 146 lines): wire v0 transport, verbatim.
- `game/scripts/game.gd`: dual mode verbatim (probe at boot, welcome in 2s ->
  AUTHORITATIVE, else SOVEREIGN; staged proposals, score off the wire).
- `game/systems/flock.gd`: sim_time determinism fix verbatim.
- `game/systems/water_graph.gd`: siphon-snapshot fix verbatim. RIDE-ALONG
  beyond the mission's three files, justified two ways: W2's owed list names
  four items (this is the fourth), and game.gd `_draw()` reads `p["siphon"]`,
  so syncing game.gd without it would ship a first-frame dictionary-access
  error on every rendered pipe.
- `game/README.md`: new "Dual mode (server optional)" section (server present
  -> authoritative; absent -> sovereign), organs-table row for net_client,
  sync receipt, verification status rewritten.
- Root `README.md`: layout bullet + B0 status now say the dual-mode client
  ships here; only the server stays unpublished.
- `docs/ADAM_QUICKSTART.md`: stale claim fixed. Sibling lane 2fcda8f
  (ADAM_QUICKSTART pack) landed mid-flight saying the networked client is
  "NOT in this repo yet"; true when written, false after this sync. One
  paragraph now splits client half (IN) from server half (still OUT).
  Folded in via --amend so history keeps one W3 sync commit.

No `res://` path fixes were needed: the twin and `game/` share the project
layout (project.godot at game/ root, scripts/ + systems/); preloads resolve
identically. The estate files' comments still cite `server/protocol.py` and
`server/README.md` (provenance pointers to the unpublished server); left
byte-identical on purpose, and both READMEs state the server is not in this
repo.

## Verification (byte-real, 2026-09-29)

- Copy fidelity: `diff` estate vs mountain on all four .gd files after copy
  -> zero delta (ALL_BYTE_IDENTICAL).
- Headless on the synced tree, Godot 4.3 console build
  (`tools/godot/Godot_v4.3-stable_win64_console.exe`): `--quit-after 60`
  exit 0 zero errors; `--quit-after 300` exit 0 zero errors (exercises the
  no-server sovereign fallback: nothing listens on 127.0.0.1:8800).
- Pre-push gate dogfood: `bash hooks/pre-push` -> `[mountain-gate] clean.`
  exit 0, run twice (before commit and before the amend).
- Start-state partials check: `git -C the-mountain status` clean before the
  lane touched it (first command of the session).

## What Adam now has

A clone of the-mountain now carries the full dual-mode client: F5 plays the
sovereign slice offline, unchanged; with the estate world server running
(`python -m server.server` from the estate repo) the same build flips to
authoritative (shared mountain, server-checked moves, typed rejects) with
zero configuration. Only the server remains unpublished.

## JOURNEY

Threads followed: estate twin read (3 mission files + READMEs) -> mountain
twin read -> diff player/water_graph/project.godot to scope the sync ->
receipts (W1, W2, GODOT_SLICE) for conventions and the owed list -> copy ->
headless verify -> README updates -> gate -> commit -> sibling-lane check
(caught 2fcda8f's now-stale claim) -> amend -> this receipt.
Dead ends: the mission's estate path (`Documents\local_sovereign_agent\...`)
does not exist; resolved by locating the twin under `projects\`. Initial
mission scope said three files; the fourth (water_graph siphon) was tempted
to skip as out-of-scope until W2's owed list plus game.gd's own `_draw` read
made skipping it a knowingly broken landing.
Turns: amended once (ADAM_QUICKSTART fix) rather than a second commit, to
keep one W3 sync commit; gate re-run before the amend.

## Laws

- Em-dash 0 in authored text (the moved README lines keep pre-existing ones).
- Fix receipts in-file and here; trust bytes (diff + headless runs), not
  reports (the mountain's pre-sync "executed clean" claim was true of the
  estate twin's bytes, not the mountain's siphon-less water_graph.gd).
- Filed by the zcode W3 lane; index registration left to the md-record-seal
  writer (no hand-appended ledger rows).
