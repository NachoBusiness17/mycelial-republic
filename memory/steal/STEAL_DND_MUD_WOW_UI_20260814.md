# STEAL -- D&D to MUD to WoW UI, hung on the wave (2026-08-14)

## Journey (interface, not lore)

1. D&D table (1974): theater of mind. DM voice = room card. Sheet = unit frame. Graph paper = map. Minis optional.
2. MUD (1978+): those objects become tagged streams. LOOK replaces room. Talk appends. Exits are a graph. Who is presence.
3. EQ / early 3D: a viewport appears. Chat, bags, radar survive around it.
4. WoW (2004): the viewport is optional chrome. Default UI is frames: player, target, minimap, quest tracker, bags, action bar, chat, party. Addons (ElvUI) = mudlib mods.
5. Mag wow_manifest: WORLD=verkle, MOD=RIB, SAVED=rib_bus domain, EVENT=verkle bus. Not a 3D client.

## Map onto Mag

- sheet -> campaign player HP/inventory
- graph paper / Mudlet mapper -> room_svg + mermaid (exits as edges)
- MUD who -> party_subchain seats (down stay ok=false)
- MUD look -> scene_context prose (replace)
- MUD talk -> voice_turn log (append)
- WoW action bar -> list_legal_actions
- WoW quest tracker -> room hook
- WoW addon API -> rib_bus (not this layer)
- DF tileset / world_rib field -> roguelite tier later

## Proof on /wave (this hang)

Vanilla frames from campaign bytes. No 3D. No ElvUI. Prove: unit, quest, map, party, bags, action bar, chat. Complexity layers (target frame, addon mount, tileset grid) wait until these six work.

Ramp still: tabletop frames readable -> MUD survey/who as mechanic -> roguelite tiles.
