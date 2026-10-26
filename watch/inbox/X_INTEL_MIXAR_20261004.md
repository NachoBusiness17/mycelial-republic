# X INTEL - mixar.app (operator drop, 2026-10-04)

Source: https://www.mixar.app/ -> github.com/Mixar-AI/mixar-app, cloned
at 2328de6194258c5c0ecd23e41f321090df8594dd to corpus/library/mixar (gitignored vendored home; 3,674 files).

## What it is

Open-source AI 3D editor built ON BLENDER (v3.2): agents do modelling,
texturing, RIGGING, ANIMATION, UV unwrap, retopology, video gen; every
result stays manually editable. "Each task gets an AI agent" (parallel
agents on one scene), "Direct the art. Skip the grunt work." BYO keys:
personal API keys, ONE OpenRouter key for 400+ models, or a Codex
subscription. License: GPL-3.0-or-later main (mixed LICENSES dir incl
Apache-2.0 components) - COPYLEFT: fine to run and study, derivative
shipping carries obligations image-blaster (MIT) does not.

## Where it sits in the estate's day

THE ARTICULATION MIDDLE of the chain this morning built:
photo -> splat+raw mesh (image-blaster, MIT, keys owed)
      -> RETOPO + RIG + ANIMATE (mixar, GPL, BYO openrouter = key we HOLD)
      -> playable zone (Mountain Roblox, gate-checked) + dice-law/gwap.
Their agent-per-task Blender orchestration is the same shape as our
fan-out doctrine in a GUI; the BYOK module
(src/scripts/mixar/modules/byok/) is the wiring surface if the estate
ever routes it through mag.route_chat (one-front-door law).

## Doors

- RUN (operator-gated install): needs Blender + the mixar addon on this
  box; AI rides OPENROUTER_API_KEY (funded lane) - spend-gated per the
  driving ladder, free :free models first.
- STEAL (free, now): their per-task agent decomposition of 3D grunt work
  is the checklist for MAG DANCE v0.6+ (rigging/retopo prompts); their
  CLAUDE.md + module layout is another skills-architecture specimen
  beside image-blaster.
- NOTE: GPL boundary recorded; do not copy mixar code into estate
  MIT-ish surfaces without a license pass.
