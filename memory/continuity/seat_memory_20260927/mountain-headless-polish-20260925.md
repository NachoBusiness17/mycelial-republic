---
name: mountain-headless-polish-20260925
description: THE MOUNTAIN headless toolchain + wave COMPLETE 9/25 — all 12 games
  wired, gate pass, rbxlx rebuilt; v1.1 client polish landed (FOV kick, cooldown
  chips, leaderstats); LINKS id-collision lesson (renumber to verified-max+1);
  Studio hands pass pending (operator PC occupied)
metadata:
  node_type: memory
  type: project
  originSessionId: sess_d7f6f4b6-0b61-484e-8bea-0408db77ca4f
---

Operator: "polish it and play test" then "you have computer use and nobody on box, do overnight tasks anyway" then "knock out the rest of the weeks games, finish them all tonight, cook em". Delivered a headless pipeline instead of pixel-pushing, and it works:

**Toolchain (tools/bin/):** rojo 7.7.0 + luau-analyze + luau-lsp.exe + Roblox globalTypes.d.luau (851KB, from JohnnyMorganz/rojo-lsp main). Roblox's generic latest/download URLs 404 for rojo — query the GitHub API for the versioned asset name. **The place file BUILDS: roblox/the_mountain.rbxlx** (open in Studio, no sync needed). **`bash tools/mountain_check`** = one-command gate (luau_lint -> sourcemap -> filtered analyze -> build).

**Real bugs the pass caught and fixed:** Ossuary maze was SOLID ROCK (wall openings recorded with a random type tag so keys never matched — rewritten odd-cell/even-wall scheme with direction-derived midpoints + worldPos cell centers); double-sided border gaps; misaligned Court gate; sentinel `CFrame.Lerp` static-call (needs colon); Swarm fired ~9 pellets per press (per-player rate clock added); torch missing for pre-existing players; GetAttribute tonumber sweep (13 files). Accepted analyzer-noise classes documented inside mountain_check (new-solver `number?`/`number | unknown` on `tonumber(x) or 0` patterns; "Unknown require" without sourcemap).

**Rojo layout law:** folder with init.server.luau becomes ONE Script containing the sibling modules — project file must NOT set $className on those services; siblings require via `script.Parent:WaitForChild`, zones in subfolders via `script.Parent.Parent`. ContextActionService is client-only: input = client courier (src/client/init.client.luau) -> Remotes -> server-validated cooldowns.

**Wave 2 (games):** 6 background agents porting 12 estate games into roblox/src/server/zones_extra/. Landed with manifests: GalleryZone (0,8,-260; Isfahan Voronoi doors/spore fish/bad-apple field), FrontierSoulsZone (-200,8,-200; 3-phase boss rush), ToyBoxZone (200,8,-200), HardwarePrimerZone (220,8,220), IncidentDungeonZone (220,8,-220), RiddleMazeZone + SpectralMazeZone files present. mountain_check caught 3 files with missing `end`s + a require-path bug BEFORE Studio — the gate earns its keep.

**Overnight:** OffPeak task offpeak-c11e6552-d158-4553-bc7e-a8129977241d (queue #158) armed to repair broken zones, wire all manifests into init + portals, rerun mountain_check, rebuild rbxlx, update docs, LINKS receipt, commit. (Its prompt says LINKS-326, which is already taken by the codirector steal; the next free id is ≥333 — renumber at fold time.)

**RESOLVED same night:** the wave landed fully (all 11 zones_extra modules wired, commits d63a05cdf, 64bc0b076) — the offpeak backstop task later fired as a no-op verification pass and caught one real defect: a LINKS id collision (wave row claimed 326, already taken; renumbered to verified-max+1 = 334). The gate-honesty incident ([[gate-honesty-luau-20260925]]) also landed here: ArtifactLore invalid field annotations, init.server ambiguous-call print, GalleryZone tuple annotation, and a PARSE_FAILS regex that missed a SyntaxError class — all fixed, parse failures verified 0 in raw analyzer output before commit. v1.1 client polish shipped in the same window (commit dfcda53cc): dash FOV kick, ability cooldown chips (server attribute = clock), leaderstats (Virtue Marks/Rebirths/Invariants).

**Operator laws reinforced:** foreground subagents die when he posts mid-turn — background (run_in_background) agents survive; use them for any fan-out he watches from the phone. Roblox Studio IS installed on this box (AppData/Local/Roblox, mcp.bat present) but the human PLAYTEST.md 20-minute pass remains the acceptance gate; automate everything else. Studio pass still pending (operator PC occupied).

Related: [[the-mountain-roblox-20260924]], [[ossuary-wave-8x8-20260924]], [[mickey17-wave-protocol]], [[just-go-execute-dont-narrate]]
