# STEAL -- table play-as-work (2026-08-14)

Operator AFK painting. Ghost/Mag is DM. /wave is the table. World/party simulate until the player speaks. Player speech = character action AND Mag work (attention map). Then one socratic question (not a menu) + mapped work. Seats already in the party. Player is one member who takes a turn when they step in. Live room stays keep_gate. Calcifer is the named hearth. Babel = rib_bus_babelfish-turtles / fish_ear.decompile. Dock is the operator's real paint — not a module room. Mag stays keep_gate until they walk.

Hang on existing organs only. No sixth storytelling engine. No idle_tick.py. No game_dm.turn / ask_player (those spawn speakers). No 8765 restart.

## Mapping

- **game_dm.turn (party)** — already the frontier table. Do not call it from /wave AFK; it asks seats. Mag DMs by FILE beats + extract_narrator. Seats remain party_subchain lights.
- **dungeon_dev coding-task rooms** — Mag-work rooms. table_turn.handle, if the utterance is a coding-task seam, reads dungeon_state / ROOMS. Never invent a dock room. primer.play_rooms() is the training example (the example IS the training). Do not LLM a tutorial.
- **chasm** — mag.chasm_state.persist + recall. AFK tick in wave.snapshot: if last event older than ~20s, one short beat (donjon sense, Calcifer/torch if in room, non-rumor hook, chasm recall line) then persist. Never dump session_ids (percolator theater).
- **wave poll** — dashboard/static/wave.html polls ~4s. snapshot speak_text = mag.game_dm_voice.extract_narrator (Narrator section only). speechSynthesis speaks that string once; cancel previous; do not fight PTT. LAN http !isSecureContext bounces to https.
- **table_turn** — the door. conversation:true from /wave. parse + apply_action. fish_ear.decompile -> percolator.partition. If player text looks like work (patch, hang, steal, fix, cook, file) also party_subchain.append or steer.emit. swarm_emerge.detect only if still a seam. No fanout. No publish_rib.
- **persona_recall socratic** — optional AFK voice: persona_recall.recall(archetype=trickster, region=keep_gate) voice only, never the session dump. One real question: socratic_research.frame() / SOCRATIC_TURNS[0]. ask(enqueue=False) still routes — do not cadence-enqueue. Do not write plot into the DAG.
- **fish_ear** — Babel decompile on player speech. rib_bus/babelfish-turtles.json is the liquid familiar, not a pet on the floor.

## Hang (this patch)

1. mag/wave.py snapshot(): cheap FILE AFK tick (chasm persist/recall + optional persona_recall). extract_narrator -> speak_text. Stop. Wait for the player.
2. mag/table_turn.py handle(): door + work attention map on existing APIs.
3. dashboard/static/wave.html: 4s poll; TTS speak_text only.
4. mag.primer primer()/play_rooms() mapped, not invoked as a new tutorial engine.
