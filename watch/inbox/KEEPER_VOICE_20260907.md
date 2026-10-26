# KEEPER'S VOICE — the orphaned narrator, wired as file-fed
**2026-09-07, builder "keeper" · Knock-out #10 · salon verdict executed: LOOT as file-fed narrator candidate (watch/SELF_STEAL_ORPHANS_20260906.md); resident-weights form DISPUTED — retired, prompts/laws stripped to filed artifacts.**

## WHAT LANDED
- `state/keeper_world/world.json` — the world-bible as structured data, extracted from
  `watch/maze_world/Modelfile` (qwen2.5:32b, orphaned whole per O4 in
  research/orphan_registry/maze_lineage.md): **7 cast** (Gophers, The Conductor, Whalers,
  The Economist, The Sherpa, Dragons, Ghosts), **6 laws**, **8 history beats** — the five
  Modelfile beats + the real 09-06 night: THE RUN (`watch/SELF_STEAL_SHADOW_WORK_20260906.md`),
  THE AMNESIA CURE (`watch/inbox/REGISTRY_AUTOHEAL_20260906.md`), THE ORPHAN TRIAL
  (`watch/SELF_STEAL_ORPHANS_20260906.md`). Every entry cites its source path. Parses clean.
- `dashboard/static/keeper_voice.html` — THE KEEPER'S VOICE, self-contained, house dark
  style (bg #070d0c / cyan #7cf5ff / amber #e8c96a). Dropdown (world, cast, laws, history,
  the-night, all 72 chunks, the-whole-lattice) + keyword query. Zero model calls: the keeper
  composes from deterministic templates over fetched files; every narration line carries its
  citation. Error-banner fixture wired (fetch fail = visible strip, no silent dark).
- `dashboard/static/keeper_voice_data.json` — the file-fed payload (world.json + chunk
  manifest + per-slab aggregates computed from slab_\*.csv), built by
  `dashboard/static/_build_keeper_voice.py` (rerunnable, same convention as _build_shadow_walk.py).
- `state/shadow_work/keeper_lines.json` — **137 narration lines over 72 chunks**
  (schema keeper_lines/v1) for shadow_walk's lore log to consume. Sample:
  "The keeper remembers slab 4: 220,287 characters of deep thought, 101 laws sworn, 215
  questions hanging — 186 rows of the model's own thinking." (src: state/shadow_work/slab_4.csv)

## MECHANICS (the cold-vertex law honored)
The narration engine is pure functions (`topics/lines/chunkLines/narrate`) inside the page,
extractable between `//<<JS` markers; the same engine emitted keeper_lines.json under node.
Variants pick by fnv1a hash of the topic id — deterministic, replayable, $0. The weights were
never the point; the files are.

## VERIFY (all PASS)
- `node --check` on extracted JS: PASS (harness: `dashboard/static/keeper_voice_harness.js`)
- world.json parses (7 cast / 6 laws / 8 beats); keeper_lines.json parses (137 lines)
- 3 sample narrations generated (the-world, law:0, chunk:c_00_00) — receipts in harness output
- serve check: page 200, data 200 (temp http.server on the static dir, killed after)
- $0, no network, no daemons

## NAV ENTRY (report only, not wired)
`["/static/keeper_voice.html", "Keeper's Voice"]`

## PROMOTION PATH
shadow_walk's lore log reads state/shadow_work/keeper_lines.json (chunk id join, already
keyed). Vision pass flips chunks to validated and the keeper's lines gain "the eyes have
passed over it." If a resident narrator is ever wanted again, the salon verdict stands:
file-fed first; weights are a render layer, not a memory.
