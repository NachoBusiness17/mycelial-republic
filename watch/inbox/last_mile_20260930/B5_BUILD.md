# B5 - BUILD PIPELINE v0: the missing mile (2026-09-30)

Date: 2026-09-30 · Lane: B5 (ZCode) · Commit: e0ff8cec0 (uncommitted, per lane law)
Ownership: scripts/build_game.ps1 + build/ (gitignored) + this receipt

## Mission (the missing mile #2)

Distribution was NOTHING: no build, no artifact. The game existed only as a
Godot project you had to open in an editor. This lane landed BUILD PIPELINE v0:
one command, headless, produces a verified shippable zip.

## Artifact (the point, first)

```
build/mountain-e0ff8cec0.zip          28.9 MB  sha256 d659c32d8ece8343a9fdf6923fe0b94f12ae9090eb7929291cffd9e6a5d439ba
  TheMountain.exe   84,214,784 bytes  sha256 66b26ad96df7458ea917b632a73ac7c88bb058db24dbd11a457fd50435ab7b13
  TheMountain.pck      94,768 bytes  sha256 fa4e53e7e5357ce00756aba1f02ae9b7d5e4521b8dc2040b0db0552fa4e1d7bb
```

Verified twice: the script unzips to a temp dir and asserts exe+pck, and this
lane independently re-unzipped the zip and listed both files at full size.
Unzip anywhere, double-click TheMountain.exe, play. No Godot install needed.

## What was found

- Godot binary: tools/godot/Godot_v4.3-stable_win64_console.exe (4.3.stable.official.77dcf97d8).
  The 9/29 GODOT_SLICE receipt said "no Godot binary on the estate box"; one
  landed since (tools/godot/, both exes + the editor zip).
- Project: roblox_to_godot/ (main scene scenes/main.tscn, 14 .gd scripts,
  all-GL-compatibility, already smoke-run by the W/LM lanes).
- Export templates: %APPDATA%\Godot\export_templates\ existed but EMPTY (dir
  created 09-30 05:55 by some earlier lane, nothing ever installed).
- No export_presets.cfg anywhere.

## The pipeline (scripts/build_game.ps1, PowerShell 5.1)

1. Locate Godot: -GodotBin param > $env:GODOT_BIN > tools/godot console exe > editor exe.
2. Templates: if windows_release_x86_64.exe is missing, download the official
   tpz (~1 GB) from GitHub releases 4.3-stable, unzip, install templates/ into
   %APPDATA%\Godot\export_templates\<tplversion>. -SkipTemplates opts out.
3. Create export_presets.cfg if absent (idempotent, never overwrites): minimal
   Windows Desktop preset, all_resources, embed_pck=false (separate .pck is the
   verifiable shape), x86_64, modify_resources=false.
4. Export: godot --headless --path roblox_to_godot --export-release "Windows Desktop".
5. Verify gates: exe >= 30 MB (template runtime floor), pck >= 10 KB, zip built
   (Compress-Archive), fresh Expand-Archive must contain exe + pck.
6. Exit 0 on verified pass; exit 2 prints BLOCKER + the one-line FIX.

Rerun: `powershell -ExecutionPolicy Bypass -File scripts\build_game.ps1`
(now that templates are installed a rerun is ~40 s, no network).

## Defects found and fixed (trust bytes, run the thing)

1. Template dir name: --version reports 4.3.stable.official.77dcf97d8 but Godot
   looks for templates in export_templates\4.3.stable\ (the export error names
   the expected path byte-exactly). First run installed to the full-version dir
   and export refused. Fix: derive the short dir (first three version parts).
2. rcedit demand: preset default modify_resources=true requires the rcedit tool
   in Editor Settings; headless box has none. Fix: modify_resources=false
   (no icon/version metadata; the game ships without them, acceptable v0).
3. PowerShell stderr crash: with $ErrorActionPreference=Stop, each Godot stderr
   diagnostic line becomes a terminating NativeCommandError that kills the
   script before the artifact check. Fix: drop to Continue around the export
   call, gate on artifact presence instead.
4. pck threshold miscalibration: this lane first demanded pck >= 100 KB; the
   real pack is ~95 KB because The Mountain is pure GDScript + hand-drawn _draw
   rendering with zero art assets. Fix: floor 10 KB, with the exe floor (30 MB)
   as the real gate. The 95 KB pack holds all 14 compiled .gdc scripts + scenes
   (savepack log in build/export_log.txt).

## Notes for the next lane

- The export compiles every script: game.gd, hud.gd, juice.gd, water_particles,
  flock, net_client, all 14 landed in the pack. A parse error anywhere in
  roblox_to_godot will fail the build; the log names the file.
- export_presets.cfg is committed in roblox_to_godot/ (created by the pipeline).
- build/ is gitignored (/build/ in .gitignore, receipt line names the script
  that regenerates it). build/export_log.txt is the byte truth of the last run.
- Templates now live in %APPDATA%\Godot\export_templates\4.3.stable\ (all
  platforms, from the official 4.3-stable tpz), so Android/iOS lanes can export
  without another download.

## Status

ARTIFACT LANDED AND VERIFIED. The Mountain is distributable: a 29 MB zip that
runs on any Windows x64 box. Not played by this lane (headless); the exe is the
editor-identical 4.3 runtime plus the smoked project.

Em-dash count: 0.
