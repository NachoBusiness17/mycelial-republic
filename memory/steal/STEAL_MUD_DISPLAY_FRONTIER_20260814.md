# STEAL -- MUD display frontier (2026-08-14)

Operator: steal frontier on how to display the wave. Think MUDs, map to them, our tools, their foundations.

## MUD glass (Evennia / Mudlet) -- contracts, not skins

- Evennia webclient: tagged streams to panes. LOOK *replaces* the room pane. Talk *appends* the log. Map is a separate tagged stream. Input is its own pane. GoldenLayout is optional chrome; the contract is the tags.
- Mudlet mapper: rooms are nodes, exits are edges. Standard mode = graph. Grid mode = ASCII wilderness (LPC). Zoom is per-area. The map is not the room card.
- xtermia: map cached on the right; narrative is the terminal. Map updates on `map` command, does not scroll away.

So a MUD is four channels, not one postcard:
  ROOM (replace) | MAP (graph or grid) | WHO (presence) | LOG (append) + INPUT

## Mag already holds the underpinnings (mud_steal 2026-08-12)

- persistent world -> game_world (wave already shows ents/changes)
- mudlib -> RIBs / party_subchain
- MUSH shared hallucination -> holographic_q / vram_hologram
- take/north -> game_campaign parse + game_mud look/go/survey/claim/inv/map
- world-as-places -> game_world_map (World-Memory, Library, Forge-Hive, Crystal Vault...)
- Roshomon MUD -> game_mud.v2: survey the PARTY on one scene; overlap is loot; unique is novel
- ramp -> tabletop perfect, then MUD, then roguelite (game_ramp)
- DF tileset -> df_tileset.py (CP437 sheet) -- that is the *roguelite* grid, not the MUD room card
- surface_render -> mermaid + bare-metal SVG (the mapper pane)

## What the wave is doing wrong

It mashed MUD channels into one postcard: tiny ASCII (grid-mode wilderness) + orange log (room card scrolling away) + hashes. That is neither Evennia nor Mag's own MUD. game_mud rooms (World-Memory, Observatory, Crystal Vault) are not on the glass. survey/who is missing. DF tileset is attached to table REST and unused as a pane.

## Best display (soil, small)

Keep tabletop lantern as the *room card* until that tier is actually readable.
Split the wave like a MUD client, using organs we have:

1. ROOM -- game_passage / scene_context prose. REPLACE on look/move. Large type. Never LLM geometry.
2. MAP -- Mudlet node graph: wave.room_svg / room_mermaid from exits. When ramp.tier == roguelite, swap in df_tileset + game_world_render field.
3. WHO -- party_subchain recent seats in this room + game_mud survey witnesses. Down seats stay ok=false rows.
4. LOG -- voice/turn append only. Does not overwrite ROOM.
5. INPUT -- existing parser (look, go north, survey, claim, inv, map).

Do not import GoldenLayout. Do not make the lantern a WoW clone. The MUD is the shared hallucination; the hologram is already that. The glass just has to stop scrolling the room away.

Frontier question the party should survey (game_mud): what one pane, if split first, makes the standing wave readable as a MUD without leaving Mag's organs.
