# MUSEUM PLAN — art archive, riddlered (2026-09-02)

> **[AUDIT-TYPED 2026-09-08]** status: STAGED · claims: a riddlered public art archive (wash → riddler-compile → museum/Notion/HF doors) can be built almost entirely from existing bones (museum.py, lattice grammar, surface_render) at one beat per door — UNPROVEN (doors listed as GO menu, no build receipts in card) · falsifier: a door build needing new infra beyond the listed bones, or T0 content leaking through the wash into a public surface
*Operator order: treat the public surface as an archive of art that is riddlered so it never exposes secrets;
build a scrollable museum feed; Notion as cross-platform shelf; HF as public archive. Self-stolen: NOTION_API_KEY
exists in .env, OPENAI_API_KEY exists (imagegen CLI now possible), RIDDLER_PROTOCOL.md is the doctrine base.*

## STAGE 0 — THE WASH (every artifact passes before it crosses)
Deterministic, $0, one script (`mag/art_wash.py` v0):
1. STRIP — metadata/EXIF off images/audio/video.
2. SCAN — the vision organ reads text-in-image; any fleet-internal name/path/handle found = flagged.
3. RIDDLER-COMPILE — internal references replaced with surrogate-story names (seeded per artifact);
   the private decode map stays T0-local (`watch/art_riddler_map.jsonl`, never leaves).
4. RECEIPT — nonce + sha256 + what was disguised; appended to the museum manifest.
5. CROSS — only after operator GO (per artifact or themed batch). The hand is the gate; the wash is the wall.

## DOOR 1 — THE MUSEUM (local scroll, buildable tonight)
`http://127.0.0.1:8765/museum` — one static page reading `museum.jsonl` (title, era, caption, image URL, nonce).
Zero new infra: files already serve from /static/media (proven today with the song + poster). Phone-scrollable.
The riddlered caption under each piece tells the surrogate story; the real story stays in the T0 map.

## DOOR 2 — NOTION (cross-platform collaborative shelf)
NOTION_API_KEY is live. A sync script pushes WASHED artifacts to a Notion "Museum" database:
title, image, riddlered caption, era, nonce. You + collaborators scroll/comment from phone/anywhere.
Notion (cloud) only ever sees the disguise — T0 never leaves. This is the riddler lifecycle applied to publishing.

## DOOR 3 — THE SQUARE + THE VAULT (public)
- X: @GroundingWave, proven today — you post, your hand is the effect broker.
- HF: optional durable public archive (dataset or Space "fleet-museum"). NEEDS: an HF account token
  (default token file absent — UNKNOWN-OPERATOR-PULL). Models came from public repos; writes need auth.

## THE WAVE
Stochastic minds write the riddlered captions/stories (deepseek pennies or Claude).
Deterministic instruments do the wash and hold the map. Your hand crosses the square.

## GO MENU (independent, each ~one beat)
1. BUILD MUSEUM — door 1 page + manifest + wash v0
2. WIRE NOTION — door 2 sync (needs: which Notion workspace/page)
3. HF ARCHIVE — door 3 (needs: HF token from you)
4. SECOND ATELIER — imagegen CLI via OPENAI_API_KEY (found in .env)


## SELF-STEAL FINDINGS — the museum's bones already exist (dig 09-02 late)
- **mag/museum.py (v1, 08-24) IS the commit layer**: "the ROOM THAT REMEMBERS, applied to the stack" —
  retire/visit/rooms, verkle-committed museum_room.v1 leaves, archive at memory/archive/ (rooms already
  present: mining, museum). Door 1 exhibits extend it with a CURATE verb (acquire living art, not just
  retire dead surfaces) — small diff, same schema.
- **The visual grammar is ours, twice over**: lattice.html (Conspiracy lattice: #030806 bg, #7cf5ff accent,
  #3dffa8/#ff6b6b states) + fleet.html hypervisor tokens (#0b0f0d, #4fb3a8, Cascadia mono). Door 1 steals
  these tokens — no new design language, the museum wears the fleet's own skin.
- **Living-art renderers on the shelf**: surface_render.py (42KB bare-metal SVG: doctrine flow, agent mesh,
  VRAM lattice — deterministic plaques, zero deps), wave_gpu.js/wave_scene.js (the Entropium wave — a living
  background), tapestry.js, visual.js, story-parker-arc.png (narrative art precedent).
- **Knot renderers for chain exhibits**: verkle_knot.py (35KB), knot_math.py, knot_untangle.py,
  holographic_q.py, vram_hologram.py — the chain itself can be an exhibit wing.
- DOOR 1 revised build: static /museum page in lattice grammar + museum manifest + curate verb on
  museum.py + surface_render plaques. Still one beat, now mostly assembly of existing bones.
