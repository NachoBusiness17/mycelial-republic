# TASK-SHAPE CENSUS v1 (2026-10-08) - real-world shapes for the router

Lane: task-shape-census. Operator order: "hermes has real world use cases we
should steal all of those on the net and keep a database of how these tasks
are shaped so we can have those shapes in us automatically and make that a
standing job."

Database: `task_shapes.jsonl` in this directory (40 rows, one per shape,
every row evidence-cited, deduped by verb+object, built and validated by
`_build_task_shapes.py` with the repo venv interpreter). Directory name
`task_shapes_20260109` is the operator's given path; the landing date is
2026-10-08.

## Prior mines consulted (do not re-mine)

- `watch/inbox/HERMES_ECOSYSTEM_MINING_20261008.md` - the 371-story gallery
  mining receipt (convergence census + G1..G5 gap rows + NOT-BUILD column).
- `watch/inbox/LINK_DROP_HERMES_ECOSYSTEM_20261008.md` - the link-drop card
  that verified the gallery page and banked the story census (371 stories,
  15 categories, 11 sources).
- `watch/inbox/ml_moonshot_20261007/ml3_route_table.json` - the EXISTING
  vocabulary: 25 task_shapes x 17 animals, evidence-gated. The 17 animals:
  x-ai/grok-4.7, legality-propagator-v1, mountain-world-v0,
  anthropic/claude-haiku-4.5, anthropic/claude-opus-5.5,
  anthropic/claude-sonnet-5.5, anthropic/claude-fable-5.1,
  z-ai/glm-5.3-prime, deepseek/deepseek-v4.1-flash, qwen/qwen3.8-max-prime,
  qwen2.5:7b, meta/llama-3.2-11b-vision-instruct, open-mistral-nemo,
  command-r7b-12-2024, google/gemini-3.8-flash, x-ai/grok-4.3,
  qwen/qwen3.7-flash.
- `queue/results/` sampled: internal estate dispatch machinery (harness and
  hermes lane results), not real-world user asks; contributes zero rows.

## Sources this pass

1. Banked bytes: the two 2026-10-08 receipts above (all their named stories
   are rows ts001..ts010).
2. Live primary gallery: https://hermes-agent.nousresearch.com/docs/user-stories
   (fetched 2026-10-08; the 155+ story extraction cross-validated against the
   banked receipts on every story both carry: kabira121, mayuronx,
   Barnet1123, fxa3bah, Razorpay, pacmanpill, humanth-shashani, DeRonin_,
   lauratom, Synapse all match).
3. One web sweep (two live sources):
   https://openclaw.ai/showcase and
   https://github.com/hesamsheikh/awesome-openclaw-usecases

## Census counts

Total shapes: 40 (at the mission's ~40 cap; quality held: every row cites
banked bytes or a live URL, zero fabricated stories).

By cadence class:

| cadence | count | reading |
|---|---|---|
| watch | 17 | the plurality of real use is event-driven standing attention, not one-shot asks |
| cron | 12 | the scheduled digest/report class |
| one-shot | 11 | classic ask-and-done |

## Coverage vs the 17 animals

11 of 17 animals carry at least one real-world shape: haiku, sonnet, opus,
fable, glm-5.3-prime, grok-4.7, deepseek-v4.1-flash, legality-propagator-v1,
llama-3.2-11b-vision, open-mistral-nemo, qwen2.5:7b.

6 animals received zero real-world shapes: mountain-world-v0,
qwen3.8-max-prime, gemini-3.8-flash, grok-4.3, qwen3.7-flash,
command-r7b-12-2024. Reading: real-world work concentrates on cheap-scut
(haiku/flash/local) plus premium-judgment (grok/opus/prime) animals; the
mid-tier and specialist-sim animals have no user-facing demand signal. That
is router evidence, not a culling proposal.

## Top-10 most common real shapes (ranked by distinct evidence rows)

1. ts014 morning brief (mail + calendar + feeds) - 5 evidence rows
2. ts001 keep a self-decaying memory graph - 4
3. ts020 research and score leads nightly - 4
4. ts005 always-on caged agent fleet - 3
5. ts010 trade a market automatically - 3
6. ts012 filter new listings into a daily email - 3
7. ts013 boil group chats down to 3 lines - 3
8. ts021 scan competitors on a schedule - 3
9. ts025 organize a file pile into a system - 3
10. ts030 coordinate agents on one kanban - 3

The single most common real shape in the wild is the MORNING BRIEF family
(cron digest of mail + calendar + feeds into one short message), and the
broader digest/watch class dominates the census (29 of 40 rows are watch or
cron). One-shot asking, the shape our own queue is built around, is the
minority of real use.

## What our vocabulary CANNOT express yet (the NEW list)

5 rows carry fits_our_17_animals = NEW:

- ts026 voice notes to docs - no audio-in animal (STT is tool-side; the 17
  are text plus one vision reader).
- ts037 summarize videos instead of watching - no video/audio-in animal.
- ts039 generate media assets (thumbnails, UGC videos) - no generation
  animal at all.
- ts040 place voice calls - no voice-out animal, no telephony shape.
- ts006 zero-token cron - by design below all 17: script tier, no animal
  should ever touch it (the estate's G1 gap row already assesses the port).

Honest split: 4 capability holes the animal set cannot express (audio/video
in, media generation, voice out) plus 1 deliberate no-animal tier. Any of
the 4 holes is a future animal-class decision (a STT/media/telephony
rung), not a route-table tweak.

## Honest limits

- Gallery totals (371 stories, 15 categories) are carried from the banked
  LINK_DROP receipt, not recounted this pass.
- The gallery extraction is a model-read of the live page, not a byte dump;
  the 10 cross-validated stories are the anchor, and every row that names a
  user carries that user's handle for re-verification.
- Web-sweep rows (openclaw showcase, awesome list) cite URLs only; the
  awesome list itself warns its linked skills are unaudited.
- fits_our_17_animals mappings for shapes without a route-table analogue
  are reasoned from the animal rankings, not measured; the standing job's
  auto-wire (see STANDING_JOB.md) is what converts them into measured rows.

## Files

- `task_shapes.jsonl` - the database (40 rows).
- `_build_task_shapes.py` - the builder + validator (rerun to regenerate;
  asserts dedupe by shape_id and verb_object, cadence enum, non-empty
  evidence, zero em/en dashes).
- `STANDING_JOB.md` - the refresh spec (spec only; nothing registered).
