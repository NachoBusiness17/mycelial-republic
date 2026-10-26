# X INTEL - image-blaster (operator drop, 2026-10-03)

Source: https://x.com/liambraus/status/2106383264282026459 (self-reply with
the repo link; parent 2106383261089849825). Author: liam. (@liambraus,
verified, ex-ElevenLabs CMO, ~144K followers). Posted 2026-10-03T13:57Z.
Parent stats: 3,335 likes / 374 RT / 135K views / 3.8K bookmarks and
climbing. Framing: "a whole industry lost meaning today" (the Blender
dig). Fetched via fxtwitter embed API (the declared $0 X door class).

## What it is

github.com/neilsonnn/image-blaster - MIT, 5.2k stars / 529 forks / 72
commits at fetch. "An image-to-world skillset for Claude": drop one photo
in input/, ask Claude to "blast it", get a fully meshed 3D environment in
under 5 minutes. NOT a model and NOT an app: a Claude Code SKILLSET
(.claude/ skills dir + CLAUDE.md, plus .cursor/rules) orchestrating four
rented organs with user confirmation at each stage:

- World Labs marble-1.1 - explorable environment (gaussian splat, .spz)
- nano-banana - image cleanup / clean plates (gpt-image-2 alt)
- hunyuan-3d via FAL - mesh gen (.glb/.obj, 40K-1.5M faces, PBR, LowPoly)
- elevenlabs-sfx - ambient + object physics SFX

Outputs are engine-agnostic (Unity/Unreal/Godot/Blender/Three.js). Needs
World Labs + FAL API keys (both absent from our .env - operator-gated
doors). Bun-based React viewer for the output.

## Why it matters to THIS estate (three direct hits)

1. **The skills-carrier thesis, proven in public.** The operator's own
   doctrines: "the capability gap is a TOOLS gap not a weights gap"
   (2026-10-02) and the ractor50 skills verdict (waves fuzz, cards commit).
   A stranger just took a skills DIR to 5.2k stars in ~a day with ZERO
   novel models - all value captured at the orchestration/skill layer.
   External validation data for the estate's skill census (5 promote /
   10 demote / 3 kill): the promote class looks like exactly this shape -
   concrete organ + short card + one command verb ("blast it").
2. **"Wire don't build" again, in 3D.** Same pattern as Strata: the
   estate's architecture (agent + MCP senses + rented organs) shipped by
   someone else first. Claude orchestrating four paid APIs step-by-step
   with per-stage confirmation IS the descent-protocol ask shape with
   tools. Nothing here we would build - everything here we would WIRE.
3. **THE MOUNTAIN front door.** We hand-build zones (19 in
   roblox/the_mountain.rbxlx; Godot port live; DF/worldgen mines). This is
   image -> playable zone in minutes: photograph a place (the Pixel 11 is
   the body), blast it, import the .glb as a Roblox MeshPart zone, hang
   the estate's dice-law + gwap organs on it. The Mountain's
   Ossuary/Halloween spearhead could get photo-real zones this way.

## Honest skepticism (the hype-cycle read)

The claim "industry lost meaning" is marketing: marble/splat worldgen
shipped in 2025, hunyuan-3d and banana are old news; the NEW thing is the
packaging + sub-5-min orchestration discipline. 10-year Blender veterans
are not obsolete - hand-authored worlds still out-class splat captures
for anything interactive (no collision meshes on splats, fixed lighting,
no interior geometry behind surfaces). The durable steal is the SHAPE,
not the models.

## Doors (all operator-gated; nothing fired)

- ADOPT: clone into corpus/library, add World Labs + FAL keys, blast one
  photo into a Mountain test zone (falsifier: .glb imports through the
  existing mountain gate and a room is playable in Roblox same-sitting).
- STEAL: the skill-card format (SKILL.md brevity, one verb, per-stage
  confirmation) against our 18-skill census - a one-lane diff.
- WATCH: liam. (ex-ElevenLabs CMO) as an amplification surface for the
  estate's own skill-carrier plays (the gwap useful-shit law gives us
  chain-verified artifacts worth showing).

Filed by the 5.3 strategy window; no paid doors opened (driving ladder:
this is sensing + judgment, the money legs wait for operator GO).
