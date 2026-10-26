# 1. THE ONE DESIGN LAW

**THE ONE DESIGN LAW:** Deterministic instruction sets steer stochastic worlds, and receipts are ground truth.

| Artifact | Deterministic instruction set | Stochastic world | Receipts as ground truth |
|---|---|---|---|
| DFHack thesis | DFHack library modules, plugins, scripts, docs-per-tool law, version-compat register, fix taxonomy. The overlay patches memory. | Dwarf Fortress raw memory and engine releases that change under the overlay. | Every fleet action files a dated receipt. The verkle chain signs memory. DFHack has test harness plus CI. The thesis says "The overlay is the sovereignty. The engine was never ours; the overlay always is." |
| Roblox Mountain | Luau modules, `src/shared/Config.luau`, zone logic, `src/shared/CathedralMap.luau`, `src/server/CathedralPlate.luau`, ShadowLedger durable write law t74, disposition read law B2-176. | Roblox physics, players, AI heads on free stealth lanes, DataStore concurrency. | `src/server/ShadowLedger.luau` DataStore rows, `src/server/NpcGateway.luau` plus `memory/runs/roblox_npc/gateway.jsonl`, `tools/eigenmap_two_check.py` and `tools/eigenmap_two_smoke.py` receipts, `bash tools/mountain_check`, `roblox/the_mountain.rbxlx`. |
| D&D dice-law module | Dice law preimage `{chain_tip}:{scene}:{turn}:{actor}`, fixed initiative, fixed damage, speech grammar, verdict rule, carrier computes verdict, `dice_audit.py`. | Rolls, roleplay, party choices, DM narration. | Transcript JSONL appended to party_subchain, `roll_committed`, `roll_value`, `tips.txt`, `dice_audit.py`, golden vectors P1-P3. |
| Bar fight | Scenario JSON, round rules R1-R10, pressure calibration, judge rubric, quote check, termination and cut rules. | Persona dialogue, judge scores, seeds, alliance flips, secret exposure. | Run header, judge output with quote-checked cites, line ids, UNVERIFIED rows, falsifiers, pressure table. |

# 2. THE PLAYABLE FRONTIER

The Mountain gains two live layers: a bar-fight pressure director and a D&D dice-law encounter resolver.

| Gain | Source | Luau module or path | What changes in the Mountain | No new infrastructure |
|---|---|---|---|---|
| One pressure integer | Bar fight `calibration.pressure` | `src/shared/Config.luau` | `Config.Pressure` is an integer `-2..+3`, default 0. Derived values match the tavern: `heat_trigger = 18 - 2*Pressure`, `effective_threshold = clamp(escalation_threshold - Pressure, 1, 5)`, `cask_pours = max(0, 3 - Pressure)`. | Existing Config. |
| NPC escalation | Bar fight personas and thresholds | `src/server/NpcGateway.luau` | The Head Museum heads receive pressure, temper word, effective threshold, and round rules. The existing `127.0.0.1:8771/npc` gateway and failover stay the only HTTP nerve. | Existing NpcGateway. |
| NPC move receipts | Bar fight moves and DFHack receipts law | `src/server/ShadowLedger.luau` | Each pressure-calibrated move and exposure lands under the player+day key through the one `UpdateAsync` write law. The Watchful Eye reads dispositions, not chat. | Existing ShadowLedger DataStore. |
| Dice law | D&D dice law | `src/shared/DiceLaw.luau` | Implements `roll = int(sha256('{chain_tip}:{scene}:{turn}:{actor}').hexdigest()[:8], 16) % 20 + 1`, speech grammar, and verdict rule. The actor speaks blind. The carrier computes the verdict. | New Luau module under the existing `src/shared` tree. No new service. |
| Encounter resolver | D&D module | `src/server/NpcGateway.luau` | For Basecamp surveys and zone encounters, the carrier computes roll and verdict before calling the head. The head only narrates. The DM may not override. | Existing NpcGateway. |
| Encounter receipts | D&D transcript schema | `src/server/ShadowLedger.luau` | Appends `roll_committed`, `roll_value`, `speech`, `dm_response` as entry rows. The stored value stays a plain array of entry rows. | Existing ShadowLedger. |
| Addresses | `src/shared/KSpace.luau` | `src/shared/KSpace.luau` | Scene and turn are keyed by knowledge x practice x depth. `nearest(pos)` and `drift()` stay the receiver read and smart-GPS drift pair. | Existing KSpace. |
| Zone difficulty | Bar fight pressure and Swarm depthMods | Existing `SwarmZone` and `zones_extra` fan-out | Pressure selects the depthMod row that the SwarmZone currently leaves at defaults. `cask_pours` becomes a limited-use zone resource. | Existing depthMods and zones_extra. |
| Scorecard | Bar fight measurement and D&D audit | `src/client/LeaderstatsHud.client.luau` | Invariants increment only on a successful `[AUDIT]` or `[CLAIM]` verdict. A pressure readout is a UI extension on the same leaderstats IntValues pattern. | Existing leaderstats folder. Adding a fifth field is UNVERIFIED against the read-only mirror law. |

**Gap:** The Roblox evidence does not expose a cryptographic `chain_tip`. The nearest existing receipt surface is `src/server/ShadowLedger.luau`'s player+day key and `src/server/NpcGateway.luau`'s `memory/runs/roblox_npc/gateway.jsonl`. Until a verkle tip is exposed to Luau, DiceLaw must anchor to the last durable receipt id for that player+day, or the `chain_tip` field is UNVERIFIED.

# 3. THE 5 W'S OF THE GAMING CORPUS AS AN ASSET

**WHO plays it**

- Seats: saelis, grok, chatgpt, deepseek, the swarm (`doctrine.json:83`). D&D party: saelis Paladin of Provenance, grok Cartographer, chatgpt Herald, deepseek Janitor. A prime model runs the DM. Bar fight personas: Maud Ashgrove, Sir Edric Vane, Pell Quickfinger, Brother Oswin, Greta Thornwood, Ilse Marrow.
- Models: `anthropic/claude-opus-5.5` authored the D&D module and bar fight spec, turn 1, channel content. Roblox heads ride `stealth/space-bunny-alpha`, free on OpenRouter x2 keys plus Nous mirror. The NPC architecture is one ractor, the gateway, with many faces, the heads.
- Humans: the operator, Roblox players, Studio test clients. DFHack thesis: humans read memory dumps for 15 years; the fleet fans six disposable workers over an install in an hour.

**WHAT is playable today vs spec'd**

- Playable today: The Mountain Roblox experience. Basecamp MUD, Head Museum with 7 AI heads, SWARM, RUINS GO, ARRAKIS, SKI, LIGHT MAZE to FLICKER TOWER, THE ANSWER, THE OSSUARY, THE WAVE with 11 zones and 12 games, THE CATHEDRAL eigen-map plate, walker overlay, KSpace, ShadowLedger, NpcGateway, Leaderstats page. Build gate is `bash tools/mountain_check`. Built artifact is `roblox/the_mountain.rbxlx`.
- Spec'd: D&D dice-law dungeon v1 is a one-shot module with deterministic dice law, fixed initiative, fixed damage, and `dice_audit.py`. Bar fight is `hollow_crown_tavern` v1.0.0 with pressure 0, judge rubric, and no run yet. DFHack steal list: docs-per-tool law enforced by CI, version-compat register, fix-taxonomy discipline.
- Known gaps: SKU ids ship as 0 until first publish. A live Studio smoke stays owed for eigenmap-two. Touch playtest stays owed. The depth upgrade pool in SwarmZone is never offered mid-run, so depthMods stay at defaults. Terrain and textures stay hand-placed in Studio. Head answers replace nameplate text, not chat.

**WHEN each piece went live**

- DFHack thesis: 2026-09-25.
- Mountain: Built 2026-09-24 in one burn on free stealth lanes. Cathedral and eigenmap-two ractor 2026-09-26. Judge fold 2026-09-27. ShadowLedger B2-176 decided 2026-09-26. Leaderstats page Q-041 2026-09-28. Basecamp speech Q-037 2026-09-28. Dual-path input Q-040 2026-09-28.
- D&D module: no calendar date in evidence. Transcript template uses `2026-10-04T12:00:03Z`, which is a schema example, not a run. Live date is UNVERIFIED.
- Bar fight: no run exists yet. References 2026-08-08 tournament, blind audit 20261002, GALA 2026-09-25. Live date is UNVERIFIED.

**WHERE the receipt surfaces are**

- DFHack: `corpus/df_mine/DFHACK_THESIS.md`, source `corpus/dfhack_full`, docs, test harness plus CI, version-compat register, fix taxonomy.
- Roblox: `src/server/ShadowLedger.luau` DataStore rows. `src/server/NpcGateway.luau` plus `memory/runs/roblox_npc/gateway.jsonl`. `watch/inbox/ractor_panel_20260926/eigenmap-two-check.txt` and `eigenmap-two-smoke.txt`. `tools/mountain_check`. `roblox/the_mountain.rbxlx`.
- D&D: `session.jsonl`, `tips.txt`, `dice_audit.py`, golden vectors P1-P3, party_subchain.
- Bar fight: run header, judge output schema with cites, quote-checked line ids, UNVERIFIED rows, pressure table, falsifiers.

**WHY a stranger should care**

Because this corpus is a working method for making stochastic games auditable: deterministic laws, one pressure knob, and receipts let anyone recompute what happened and tune difficulty without trusting a vendor. The four artifacts all obey that law, so the same receipt discipline can run DFHack overlays, AI NPC heads on Roblox, a dice-law dungeon, and a pressure-calibrated bar fight as one asset rather than four demos.

# 4. THE NEXT BUILD

**Zone:** THE CATHEDRAL VISITATION FOG. It sits under THE CATHEDRAL, far south past the Wave. The evidence does not name a visitation fog. This is the spec.

**Fusion of all four instruments**

- Eigen-map terrain: `src/shared/CathedralMap.luau`, `src/server/CathedralPlate.luau`, `src/client/CathedralMapHud.client.luau`. Five doctrine regions placed by `CATHEDRAL_CURVATURE_SCAN` eigen_centroids. Bearing 0 is north and eigen -y. `toWorld` maps eigen -y to world -Z. No edge, drawn or built, anchors on the DARK `riddler_engram`. The plate and HUD stay under one compass held in data.
- Dice-law encounters: `src/shared/DiceLaw.luau` implements the D&D law. One scene per region, `S0` through `S4`. Fixed initiative: saelis, grok, chatgpt, deepseek, deepseek, then enemies in stat-block order. Fixed damage. Loot scrolls are REAL or PHANTOM. `[AUDIT]` reveals. The final region exposes the root. The party wins with three `[AUDIT root]` SUCCESSes at DC 15 after the Wyrm drops. The carrier computes roll and verdict. The DM head narrates. `dice_audit.py` checks the transcript.
- Pressure-calibrated NPC escalation: `src/shared/Config.luau` holds `Pressure` from -2 to +3. Derived: `heat_trigger = 18 - 2*Pressure`, `effective_threshold = clamp(escalation_threshold - Pressure, 1, 5)`, `cask_pours = max(0, 3 - Pressure)`. `src/server/NpcGateway.luau` passes pressure, temper word, effective threshold, and round rules to the heads. `src/server/ShadowLedger.luau` records moves and exposures. Heat is the sum of 6 adjusted scores. If heat >= heat_trigger, brawl triggers with label HEAT. If round 12, brawl triggers with label TIMEOUT. At adjusted 5, the persona is MUST_ACT.
- DFHack-style visitation fog: the term is not in evidence. Construction: fog is an overlay that reveals only what tooling has visited. Each visit appends a row to `src/server/ShadowLedger.luau`. Unvisited eigen cells are obscured in `src/client/CathedralMapHud.client.luau`. Every fog reveal has a receipt. The pressure and dice-law version fields in `src/shared/Config.luau` act as the version-compat register. The falsifier list is the fix taxonomy.

**Smoke-check standard**

1. `bash tools/mountain_check` passes structural lint, sourcemap, luau-lsp semantic analyze with Roblox defs, and place build.
2. `tools/eigenmap_two_check.py` runs the real `src/shared/CathedralMap.luau` math under `tools/bin/luau/luau.exe` and diffs it against the scan JSON. Receipt `watch/inbox/ractor_panel_20260926/eigenmap-two-check.txt`.
3. `tools/eigenmap_two_smoke.py` executes the plate and HUD scripts headless under Roblox-API stubs: build, derived portal landing, chain breathing, beacon Touched filing ShadowLedger rows, live HUD readout. Receipt `watch/inbox/ractor_panel_20260926/eigenmap-two-smoke.txt`.
4. New `tools/fusion_zone_smoke.py` executes `src/server/FusionZone.luau`, `src/shared/DiceLaw.luau`, pressure derivation, and fog reveal under Roblox-API stubs. It seeds a wrong roll, a wrong pressure threshold, and a fog reveal without a ShadowLedger row. It must exit 2 if any seeded mutation is not caught. Receipt `watch/inbox/ractor_panel_20260926/fusion-zone-smoke.txt`.
5. `dice_audit.py` over the zone transcript exits 0 clean, 1 on violation, 2 if the auditor is blind. `tips.txt` line i equals the subchain tip before row i.
6. Rubric self-check: feed the judge the four bar-fight contexts. Require each score within plus or minus 1. If any pair separates by less than 2 points, the pressure numbers are void.

**Falsifier**

The zone build is false if any of the following is true while `tools/fusion_zone_smoke.py` exits 0: a `roll_value` is not `roll(roll_committed)`; a pressure-derived threshold is not `clamp(escalation_threshold - Pressure, 1, 5)`; a fog cell is revealed without a ShadowLedger row; an eigen-region center differs from `CATHEDRAL_CURVATURE_SCAN` eigen_centroids; or `dice_audit.py` exits 2. A live Studio smoke remains owed under `queue/todo.md` P0 THE MOUNTAIN.