---
name: image-blast
description: Turn one photo into an explorable 3D world (splat environment + meshed objects + SFX) via the vendored image-blaster engine. Use when the operator provides an image and asks for a world, a zone, a 3D object, or scene SFX.
argument-hint: <image-path> [world-slug] [--stage world|objects|sfx|all]
---

Blast one image into a world under `worlds/$0/` in the vendored engine at
`corpus/library/image-blaster` (MIT, cloned 2026-10-03 from
github.com/neilsonnn/image-blaster per operator GO; intel receipt
`watch/inbox/X_INTEL_IMAGE_BLASTER_20261003.md`).

- If `$0` (the image path) is missing, ask for exactly one source image.
- If no world slug is given, derive one from the image filename.
- PAID-ORGAN GATE (hard): the engine calls World Labs marble-1.1 (worlds)
  and FAL (hunyuan-3d meshes, sfx, image edit). Both keys are ABSENT from
  the estate `.env` as of 2026-10-03. Do NOT fire any paid call until the
  operator has provided `WORLD_LABS_API_KEY` and `FAL_KEY` (set them in
  `.env`; the engine's own `loadDotEnv` also reads
  `corpus/library/image-blaster/.env`) AND confirmed the blast in-chat.
  With keys absent, this skill runs PLANNING ONLY: stage plan, expected
  organs, per-stage cost guess, and the exact commands it would run.

## Commands (engine cwd = corpus/library/image-blaster, node v22, no bun needed)

```bash
cd corpus/library/image-blaster
node .claude/scripts/world/generate-world.mjs --image <image-path> --slug <world-slug>   # marble-1.1 splat world
node .claude/scripts/asset-pipeline/generate-single-asset.mjs --world <slug> --image <image-path> --object-name <name> --description <desc> --image-edit-prompt "<isolate-one-object prompt>"   # hunyuan-3d mesh
node .claude/scripts/sfx/fal-elevenlabs-sfx.mjs --world <slug> --description "<ambient or object sound>"   # SFX via FAL
```

Stage order (the engine's own): world splat -> uncover objects -> per-object
clean plate -> mesh -> SFX. Object cards live at
`worlds/<slug>/output/<object>/object.json`; never hand-write generated
status into them. The extraction prompt template for objects is in
`corpus/library/image-blaster/.claude/skills/image-blast-3d/SKILL.md` (isolate one atomic instance,
white background, tight crop, no neighbors).

## Mountain import leg (owed operator Studio gate)

Output `.glb`/`.obj` import into Roblox as MeshPart zones rides the SAME
operator Studio pass the board already owes (roblox/docs/PLAYTEST.md
publish + SKU ids). When that gate opens: blast a photo zone, import the
glb, hang dice-law + gwap organs on it (the Mountain gets an image->zone
front door).

Final response: report the world slug, stages fired vs skipped (key gate),
output paths under `worlds/<slug>/`, per-organ spend if fired, and the
exact resume command for the first skipped stage.
