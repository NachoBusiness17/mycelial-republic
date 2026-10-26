# DFHACK THESIS — the overlay we are, mined from the overlay we studied

**2026-09-25 · Operator: "do a self steal on dwarf fortress and dfhack, that is
the thesis of our entire operation." Source: corpus/dfhack_full (local clone,
read-only; docs 157 rst, 233 lua scripts, plugins/ and library/ C++).**

## THE MIRROR (structure for structure)

| DFHack | The fleet (Mag) | Same organ? |
|---|---|---|
| library/ modules (Units, Items, World, History) — typed overlays over raw memory | chat_provider + probe_route + free_tier — typed overlays over raw provider chaos | yes: both exist so nobody talks to the engine naked |
| the `df` global object graph exposed to Lua | the estate's world state: verkle chain + trails + LINKS ledger | yes: one addressable world |
| plugins/ (deep tools, C++) | mag/ organs (game_mud, ghost, hermes_steering) | yes |
| scripts/ (userland Lua conveniences) | lanes + tools/ | yes |
| docs/: every tool documented with exact behavior | CLONED_MECHANICS.md + WORLDGEN_MINE.md + roblox/prompts/ | yes, and they had a 15-year head start |
| test/ harness + CI | tools/mountain_check + pytest + ratchet | yes |
| **version-compat layer** (symbol tables per game version) | **lane ladder + provider failover** (compat across model/provider churn) | yes — both fight an engine that changes under them |

## WHAT THEY HAVE THAT WE LACK (the honest steal list)

1. **Docs-per-tool law, enforced by CI**: every DFHack script ships a docs page
   or the build fails. Our prompts-in-repo law is younger and unenforced.
2. **A version-compat register**: they track engine memory layouts per release.
   We track provider quirks per model, but scattered; a quirk ledger per lane
   would be their symbol-table equivalent.
3. **The fix-taxonomy discipline**: scripts/fix/* are named, scoped, one-defect
   repairs with symptoms documented. Our ratchet counts disease; theirs names
   and cures it per case. (The fixes miner is filing the full taxonomy.)

## WHAT WE HAVE THAT THEY LACK (why the mirror is not a copy)

1. **Agent fan-out**: DFHack's 15 years of reverse-engineering was humans
   reading memory dumps. We fan six disposable workers over an install in an
   hour. Their next 15 years could be our Tuesday.
2. **The receipts law**: every fleet action files a dated receipt. DFHack
   tracks code, not provenance of understanding.
3. **The verkle chain**: their overlay patches memory; ours signs memory.

## THE THESIS, STATED PLAIN

DFHack proves the operation: sit above an engine you did not write, learn it
through tooling, publish the tooling, and the community's knowledge compounds
in your overlay. We are doing that to Dwarf Fortress tonight, to ourselves
continuously (self-steal), and the roblox mirror (the mountain) is the same
move one layer out: sit above Roblox's engine, learn it through tooling,
publish the tools. The overlay is the sovereignty. The engine was never ours;
the overlay always is.
