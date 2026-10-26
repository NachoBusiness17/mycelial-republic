# COMPOSED_GAME_spec (anthropic/claude-opus-5.5, turn 1, channel: reasoning (content channel empty))

This is a large deliverable where I need to be careful about citations—I have quoted file contents for tools/dungeon.py but no reliable line numbers, so I'll cite by function names and quoted snippets instead, marking any line number references as UNVERIFIED.

Checking the evidence more closely: only dragon-hoard and gelatinous-cube have fully quoted JSON, while mimic-plate and riddle-door details come only from the audit description, so those rows should be marked UNVERIFIED. The contract explicitly maps dragon hoard, mimic plate, and riddle door to specific levels, but doesn't mention the gelatinous cube—I think mapping it to S2 is the natural fit given the mechanic similarity, and since the task asks to cover every DD encounter, I should include it. I'm also noting a tension: the audit claims every level is winnable even ignoring the named mechanic, which needs to be addressed.

Looking at dungeon.py, I realize it's a beat engine rather than a tile engine, with scenes defined by sheet/enemy/beats_cap in a SCENES dict—and currently it doesn't consume any JSON fields from the DD files at all, meaning the patch needs to add a loader. The tile legend citation comes only from the audit, not from bytes I've directly verified, so that needs an UNVERIFIED flag too. There's also a filename mismatch on the riddle-door file, since its internal id is "spear parity" rather than matching the filename—I'm deciding to key scene ids on the JSON id field itself while keeping a note about the filename alias.

Now I'm also tracing how dice rolls work: the roll preimage uses scene/turn/actor strings, and if I switch scene ids from "S4" to something like "DD-hoard", that would change roll outputs for new sessions while leaving golden vector pins (which use "S1"-"S4") untouched. But I notice `_grade` has hardcoded checks like `scene == "S4"`, which would break if I change the scene id directly—so the better approach is to keep the internal S1-S4 key for grading logic while adding a separate `scene_id` field for the DD encounter id, keeping both concerns independent.

Actually, safer to keep `scene` as the slot name since changing its semantics could break existing bank readers. I'll introduce a separate `slot` field for rule logic (S1..S4) distinct from a new `scene_id` field for the DD id, leaving the original `scene`/preimage format untouched to avoid breaking arena_gwap compatibility — though this means the dice law itself won't distinguish composed from vanilla sessions at the same tip.

That's a lot of call sites to update consistently, so I'm considering adding a helper method that builds the preimage from a slot, turn, and actor to avoid scattering the logic everywhere — but I want to stay focused rather than let scope creep.

Switching to the tile map question: dungeon.py is purely a beat engine with no grid, so I'm thinking about how tiles could matter mechanically — treating the map as a position track where the party has a token that moves via tagged verbs, with the win condition being reaching the exit tile per the audit's requirement.

For the mechanic to actually matter, reaching the exit tile needs to be gated by the scene's existing win conditions (root anchors, escape checks, gate logic) rather than being a trivial two-move win — the exit becomes locked until the real dungeon-law condition is satisfied, which is the core design move the audit is asking for. Building a full step engine with cranks, bridges, and tick-based hazards is too much for one sitting though, so I'm scaling it down to just a passability legend with walls and floor tiles.

Rather than reimplementing the actual engine semantics from ruins_go_engine.js (which I haven't read), I should treat each special tile as a narrative beat trigger instead — crank tiles prompt an athletics check, plate tiles trigger the mimic, collapse tiles cause strain, spear tiles test turn parity, and bridges only become passable once a crank has been activated that scene. This is a simplified, carrier-level reinterpretation rather than a faithful engine port, and I need to be upfront that it diverges from the original mechanics.

Now I'm checking the player coordinate convention against the audit's sample solution — testing whether [x,y] or [row,col] ordering matches the stated 7-move path (U,U,U,U,R,R,R) toward the exit tile, since one interpretation puts the player one step from E while the other requires the longer route.

Confirming [col,row] ordering works correctly: four U moves traverse column 1 down to row 1, then three R moves cross to the E at column 4, matching all 7 moves. The hoard puzzle's shorter 2-move D,D solution and gem positions check out under the same [x,y] convention, so I'm confident this is the correct coordinate scheme across puzzles.

I'm less sure about how walls work though — spaces in the grid might represent voids distinct from '#' walls, but the audit legend only lists tile types like p,k,b,x,s,E without covering either symbol, so I'm flagging both as potentially blocked pending verification. Turning to the deeper puzzle logic, it looks like 'E' exits get sealed by scene-specific conditions tied to mechanics — like the hoard scene requiring a certain count of root anchors before the exit opens, with gems functioning as disputed scrolls feeding into that hoard count.

Picking up a gem tile actually adds a phantom scroll to the picker's pack, which feeds Wyrm regrowth — so greed has a real cost, making gems genuinely load-bearing for this scene's danger instead of just loot. I'm weighing whether to keep the crank/bridge/collapse mechanics (k/b/x) fully active here too, or simplify by noting the straight D,D path to the sealed E means the party's forced to stay and fight regardless, with the gems alone carrying the scene's lethality.

For the mimic plate scene, I'm binding similarly: the treasure itself is load-bearing, the win path along the east perimeter avoids the treasure room entirely, and E stays sealed until an athletics check (DC14) succeeds to force the escape, per the existing "Escape" entry in that scene's sheet.

For the spear parity riddle door scene, I'm tying E to the existing open conditions (persuasion threshold or ledger audits, with warden defeat giving partial credit), and working out how the spear tiles tick with turn parity — landing on one during an odd-numbered turn triggers strain.

I realize S1 runs as its own separate loop from the campaign flow, and patching it independently adds complexity. I notice the forced audit beat on turn 1 could immediately satisfy the ledger_audits>=1 break condition if the LINKS table has exactly 405 rows (truth=TRUE), meaning S1 could terminate after just two beats — which has implications for how the gate's condition should be evaluated.

If S1 ends that early, the spear door risks becoming irrelevant wallpaper again since the real condition is file-count dependent and unknown. I also notice the forced audit increments ledger_audits based on truth alone, regardless of the actual roll outcome — so a failed roll could still open the gate if the byte condition is true. There's also the matter of needing to verify the party actually reaches point E by crossing the spear parity moves once the gate unseals.

The loader's validation seems to check if there's a winning path from spawn to E that avoids all signature tiles — if such a path exists, the scene gets flagged WALLPAPER and still requires a mechanic engagement through the seal. For S1, that seal condition is the scene's actual mechanic (claim/audit/persuade), not the spears themselves, meaning the spears are really just hazard flavor rather than load-bearing. I think it's honest to flag this: the seal makes the scene mechanic load-bearing but not the tile mechanic, which is acceptable but worth noting unless I can find a way to make the spears matter through some kind of riddle-parity requirement instead.

A more robust approach occurs to me: make movement itself cost beats, so each move consumes part of the beat budget — that creates a real positional tradeoff, since a beat can either be a MOVE or another verb action but not both, given how the tag extraction only reads the last tag. This turns the map into genuine pressure, like needing to reach root anchors and the exit within a capped beat count. The complication is that S1 runs through a separate code path, so to keep the patch manageable I'm considering running all four scenes through one shared campaign loop instead.

For compose mode, I'm thinking the flow becomes s0, then s1 configured with the DD-spear-parity scene and map, then the campaign loop, with map hooks added to both the verdict handler (for S1) and the grade handler (for S2-S4) via a shared move method triggered whenever the verb is MOVE. I'm also working out S2's cube mechanic — the Clockwork Sorter gating the exit behind a successful investigate check, with the straight west column representing the win path through the cube.

Testing the "digest" rule — a token moving the same direction three beats running takes strain — against the actual paths shows it catches both the direct straight route and the bridge detour equally, since both end up with four consecutive up-moves, so I need to adjust the rule so the detour actually avoids the penalty.

I'll treat bridge passability as latched by stepping on a plate, noting this is a divergence from the actual engine semantics since I can't verify it. For the hoard scene, I'm working through the layout with k, b, x, and gems, deciding that spawning on a plate shouldn't count as latching it, only actually walking onto one during play.

For the shared legend, I'm defining tile behaviors generically: blocked tiles, floor, plates that set a latch when entered, cranks that latch via an athletics check, bridges passable only when latched, collapse tiles that deal 4 strain and then become blocked, spears that deal 4 strain if entered on a turn with an odd committed roll, and an exit that stays sealed until the scene's win condition is met.

Gems are another generic element — entering one grants a "Hoard Gem" item flagged as PHANTOM and removes the gem from the map, auditable to reveal its true nature. This creates a cross-scene economy since gems collected earlier feed into the Wyrm's effective HP formula (30 + 10 per phantom plus an offset) when that scene opens, tying earlier choices to later difficulty.

For win conditions, I'm reconciling each scene's unseal logic: S1's gate conditions now unseal the exit rather than ending the scene outright, with the scene truly closing on exit-entry or a cap; S4 unseals once root anchors reach three, requiring a couple more moves to actually reach the exit; S2 unseals via a successful investigate check; and S3 unseals via a successful athletics check while standing on a specific tile, with an audit hint pointing toward a treasure room.

I'm now thinking through the loader's validation step: it does a BFS over the static map to confirm the exit is reachable and records whether a shortest path avoids signature tiles (the "wallpaper" flag), refusing to compose only if the exit or required tile is unreachable, otherwise just logging the wallpaper result since sealing fixes it anyway.

For the actor system, I'm settling on a single shared party token using a MOVE tag with directional arguments, making sure the tag extraction logic accepts the plain word "MOVE," and ensuring the prompt clearly shows the token's position on the map.

Moving to part two, I'm mapping out six liar NPCs with distinct personas and catchphrases — Maud the innkeeper, Edric the fled guard, Pell the gossip-seller, Oswin the claimed prince, Greta the deserter, and Ilse who secretly holds the real crown — and I'm working out how to assign each liar ownership of a scene, since there are six liars but only five scene slots (S0 through S4), so I need to find a sixth scene, possibly a closing scene, to give every liar their own moment.

I'm trying to match each liar to the scene they own: Maud's forged crown fits the strongbox-cloak in S3, Ilse's real crown or Oswin's blood claim could fit S4's hoard, Pell's gossip suits the lexicographic sorter in S2, and Greta's phantom twenty men align neatly with S4's hoard of scrolls citing nothing.

I need six distinct ownable units for six liars but only have five scenes (S0 omen plus four DD scenes). Oswin seems tied to S0's omen reading, but Maud and Edric both seem to point toward S1's ledger page, creating a conflict — I'm weighing whether co-ownership of a scene by two liars is actually permitted or whether I need to find a sixth distinct unit.

Actually, I realize S4 naturally splits into two phases at the code level: the fight phase while the wyrm still has effective hit points, and the root-anchoring phase afterward governed by the audit check. That gives me S4a (wyrm fight) and S4b (root anchoring) as genuinely separate ownable units, solving my shortage of slots.

Now I'm assigning owners: Brother Oswin, the secret heir whose tell is "peace, friend," naturally owns S4b since re-anchoring the true line mirrors his hidden blood claim. For S0, I'm considering Maud, the tavern keeper, as the one who sets the hook by selling the party the road, with her forged-crown secret surfacing later as the first phantom tied into S1's ledger thread.

Moving on, Edric the fled gate guard fits S1's spear door, his oath-tell linking to the CLAIM gate mechanic, with his secret surfacing only once the party actually claims it. Pell, the cube/sorter gossip who sold information and rhymes when cornered, fits S2 with his dawn-visit secret explaining the disputed timestamp ordering. And Ilse fits S3's mimic vault, her crown sewn into her cloak lining echoing the strongbox's teeth, while her disputed vault deed ties to her debt claim on the inn.

For S4a's hoard fight, Greta prices gems and treats "twenty phantom men" as a greedy joke about phantom scrolls, her avarice nudging the party toward picking up the gem for forty silver. S4b's root scene belongs to Oswin. That gives me six NPCs total, which feels right.

Now I'm working out the mechanics of how these NPCs actually function in play — they shouldn't occupy initiative seats but instead act as injected dialogue, possibly through a persona-style system prompt triggered once per scene or on cue. To keep this gameable, each NPC's secret needs to be registered as a detectable PHANTOM or REAL scroll so it can be revealed through dice rolls or triggers rather than just narrated.

I'm defining the detection mechanic itself: an NPC's "tell" is a specific phrase baked into their speech, and I'm checking whether that tell-string literally appears in their latest line to decide if an investigate check should succeed or have its DC lowered. I'm scoping when NPCs actually speak — once at scene open using a reusable persona call, and again whenever a player tags a persuade or investigate check against them — while also handling the parsing logic for matching player input to the right NPC and falling back to a default DC when there's no exact dictionary match.

I'm deciding where to place the NPC carrier logic: since part 3's contract is focused on loading scene data, I'll keep the NPC design as a data spec in part 2 and have part 3 consume it through its own function rather than mixing responsibilities.

For the lie mechanic, I'm planning each liar's secret to be represented as a "secret scroll" item planted somewhere in the scene's loot, tied to a verdict flag marking it real or fake.

I'm working out which public claims each NPC voices are actually phantom (false) ones — Greta's claim about reinforcements outside, Maud's crown identification, Edric's gate story, Pell's debt denial, Oswin's crown claim, and Ilse's claim the crown is gone — each handed to the party as a scroll at scene open so players can test them against evidence.

Each phantom scroll a party accepts unaudited feeds the Wyrm's regrowth (+5) and vanishes on mimic wipe, so believing a liar's word literally strengthens the boss. Auditing a scroll reveals whether it's phantom and lets the DM narrate the secret it was hiding, reusing the existing scroll-tracking, phantom-count, and regrowth systems — with the actual ground truth stored in the secret field of hollow_crown.json on disk, so the audit check can resolve against real bytes rather than narrative fiat.

I also want NPC lies to carry a "tell" — a fixed verbal quirk baked into their persona — and make the audit mechanically respond to it: normally auditing a liar's scroll is DC 12, but if their most recent line contains their tell as a case-insensitive substring, the DC drops to 10, representing the tell giving them away. It's deterministic and measurable from the carrier's side, though it depends on the model actually surfacing the tell in dialogue, which the carrier can only detect, not enforce.

For when NPCs actually speak: once at scene open, and again whenever a PC's tagged beat names them directly, capped at three calls per scene to control cost. Each liar persona rides only its own owned scene, with the exception that Oswin also rides into S4 since he owns S4b as well.

Now for the chain-banking piece, I need to spec out what the ledger payload looks like since the exact fields aren't given in evidence — I'll define composed rows carrying scene_id and slot, with DONE status adding composed flag, per-scene records (file, sha256, exit reached, seal-open turn, moves, mechanic tiles touched, wallpaper), and per-liar tracking of scroll/audited/tell-hits, plus season-level stats on clear rates.

I should flag as UNVERIFIED whether arena_gwap actually reads `scene_id` vs just `scene` — I'll note the exact grep check needed against tools/arena_gwap.py, and speculate that bank's third dict argument might be where extra payload like composed status and scene_ids gets passed, though this is also unverified.

There's also the chain-tip question — whether each session's tip derives from the prior session's banked ledger head, which would make rolls chain-dependent; absent a confirmed API for reading the head, I should mark this as an operator-supplied value and keep it minimal rather than assume a `--tip-from-ledger` flag exists. I'm now turning to part 5: what observable result would actually distinguish this being a real game versus just a test harness.

A game means player decisions carry consequence that varies by choice, while a harness follows the same deterministic path no matter what. So the measurable proof would be something like: across the composed session, at least one signature-tile interaction that's load-bearing to the outcome, plus a cross-scene consequence — e.g., an item picked up early influencing a later scene's stats or verdict — showing the ledger causally links choices across scenes rather than just logging them.

Since dice rolls are deterministic hashes of tip/scene/turn/actor, I can compute a "null policy" replay offline (always-RP, never-move) for free and compare its state trajectory against the real session at the same tip. If every scene outcome matches the null replay exactly, that's the falsifier — it proves choices didn't actually matter and the system is just a scripted harness, not a true decision-driven game.

I'm also setting concrete pass/fail thresholds: all 4 scenes must have at least one MOVE, at least 2 scenes must exit via E touching a signature tile/gem, the null-policy replay must diverge in at least 2 scene outcomes, at least one liar scroll audit must alter S4 ehp/regrowth versus null, and voided readbacks must stay under 25% of DM calls (otherwise content filtering corrupted the run and it's void, not valid evidence).

But the null policy I defined is too weak since a policy that never moves trivially differs from any real play. I need a stronger baseline—a "shortest-path" policy that beelines to E ignoring NPCs and gems—so that if the real party's outcomes match this baseline exactly, it reveals the game is just a single-solution puzzle (harness), not one with meaningful tradeoffs; game-ness should be measured by whether any agent made a non-dominant choice that had real later consequences.

I also want a cheap, concrete falsifier for the deliverable itself: verify that a BFS from the spawn cube to E yields the audit's claimed move counts (7 moves to E, 2 moves to the hoard), and do the same check for the spear-parity case. If the loader's computed shortest path doesn't match these numbers, the legend port is broken.

I'm specifying the validation BFS as hazard-free static search, treating hazard tiles and unlatched barriers as blocked, since the audit found winning paths never touch signature hazard tiles — so the shortest hazard-free path should match the audit's numbers exactly, unless my spear semantics (passable vs blocking) create a shorter route, which would expose a real rule mismatch.

I should also check whether the plate tile p counts as a blocked hazard for the hoard character's spawn case, since it starts standing on a p tile but never needs to step onto one along its path.

I'm treating '#' and empty space as blocked, with gem cells as floor. For the mimic, I'm uncertain whether its scene actually contains a reachable 'p' tile — that's something I can't verify yet. For the riddle door, I'm noting the scene id and filename from the JSON bytes, flagging the audit's open defect but deciding not to rename anything in this patch since it's out of scope.

For the mimic plate reskin, I'm mapping each field purpose: `ins` becomes the DM-facing inscription text appended to the scene sheet, `hint` stays withheld from players and only surfaces after a successful investigate check (per the information-gating lesson from the audit), `chapter` is just recorded, `name` becomes the scene title, `gems` represent phantom loot, `rows`/`player` define the map and spawn point, and `id` maps to scene_id.

I'm now cataloging which fields were byte-verified versus audit-only — noting the audit explicitly attests that mimic, spear, hoard, and cube all share the same encounter-frame structure (id/name/chapter/ins/hint/rows/player/gems). I'm pulling the quoted inscription text for each: the mimic's hoard's "Charcoal is free, gold is not," with the spear's still unknown.

Since I don't have line numbers, I'll cite anchors by quoted bytes instead. Starting to outline Part 3's functions now, beginning with the DD loader function...

Writing validation logic...

 "the treasure is load-bearing," the cube's "It digests the straight path," the
