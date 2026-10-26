# W2 MOUNTAIN CLONE-PROOF - 2026-09-29

Re-fire of the 1302-dead lane (original agent 8a1e3b07, died in the
2026-09-29 burst; death logged in MICKEY17_WAVE_LEDGER_20260929.md).
Fixes the M17 miner finding (ledger RETURN 2/24, agent ef38bcc3): the
repo's only enforced law evaporated on first clone.

## Partials check before re-fire (per the death receipt's instruction)

`git -C the-mountain status` -> working tree clean; exactly one commit
existed (4708986, the B0 seed). The dead lane left no partial commits.
Re-fire started from clean.

## What landed (commit 035a5e3bc71fb8173dbb68808ee10b729793bb1d, branch
main, NOT pushed per lane order; repo
C:\Users\foste\Documents\projects\the-mountain)

1. Gate survives the clone:
   - `git update-index --chmod=+x hooks/pre-push` -> index mode now
     100755 (was 100644), ships with every clone.
   - Bootstrap one-liner in README ("First command after cloning"):
     `git config core.hooksPath hooks && chmod +x hooks/*`
   - CONTRIBUTING.md (new): same line as step one; MIT contribution
     terms; hard rule that CMaNGOS-derived (GPL-2) material and
     client-derived game data must never be committed (gitignore
     already blocks the client-data shapes).
2. Ghost paths: game/README.md run line `roblox_to_godot/` -> `game/`;
   docs/GODOT_SLICE_20260929.md build + filing sections -> `game/`;
   the historical 9/28 mention is annotated (folder renamed), not
   rewritten. Also fixed the stale core/network/water placeholder-dirs
   line (those empty dirs never shipped; git drops empty dirs).
3. LICENSE (new): MIT, "The Mountain contributors", 2026.
4. README contradiction resolved: B0 status now states the slice
   EXECUTED headless clean on 2026-09-29 (60 and 300 frames, zero
   script errors, exit 0) and the net_client transport completed the
   live smoke against the authoritative server (welcomed with sid,
   staged boil, typed DRY_POOL reject, ticks parsed), sourced from
   W1_NET_CLIENT_20260929.md. PLAYED-by-no-one still true.
   "Private by intent" reworded to "Public-safe by intent" (it
   contradicted the new MIT + CONTRIBUTING).
5. .github/workflows/ci.yml (new): minimal honest v0, labeled
   no-engine in workflow + job names. Python syntax check over tracked
   .py (prints the honest count; 0 today since server code is not
   synced here), UTF-8 text integrity over tracked text files, gate
   wiring check (hook present + index mode 100755 + executable on
   disk), and a gate dogfood run of hooks/pre-push over the whole
   tree. Green means files parse and the gate wires up, never that the
   game runs.

## Verification (byte-real, run from the repo root before commit)

- python py-compile step: `tracked .py files: 0`, exit 0.
- text integrity step: `text files checked: 15`, exit 0.
- `git ls-files -s hooks/pre-push` -> `100755 ...` post-update-index.
- `bash hooks/pre-push` (with all new files staged) ->
  `[mountain-gate] clean.`, exit 0.
- Commit stat: 7 files changed, 164 insertions(+), 10 deletions(-),
  `mode change 100644 => 100755 hooks/pre-push`.

## Owed (next lanes, not this one's scope)

- SYNC GAP: the estate twin `roblox_to_godot/` is ahead of the
  mountain's `game/`: net_client.gd (160 lines), dual-mode game.gd,
  flock.gd wall-clock fix, water_graph.gd siphon-field snapshot fix.
  Byte-diffed before writing the README claim; the README states the
  networked half is the next sync rather than implying it ships.
- Push to origin is the operator's call (lane order: commit yes, push
  no). CI proves itself on the first pushed commit.
