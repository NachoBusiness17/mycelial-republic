# RACTOR PANEL SPEC — the estate presents itself (SW-07 B2-152, 2026-09-26)

Operator want, quoted from the queue row: "full panel on journal/origin,
intent, present, destination mapped wide to subsystems, dogfooded against own
research." One ractor (the gateway, `tools/roblox_npc_gateway.py`), four
faces; each face is a Head-Museum-class persona whose every factual claim is
grounded in an own instrument, and every claim names the instrument that can
falsify it. Deliverable per the row: panel run-book + face briefs ready to
fire. Face briefs land as `roblox/prompts/RACTOR_FACE_{ORIGIN,INTENT,PRESENT,DESTINATION}.prompt.md`
(NPC_HEAD specialist shape: frozen prefix, dual-anchor knot, matched
inference, falsifier per head -- the five prompt-library laws apply).

## The four faces (knots + instrument bindings)

| face | who you are | who you are NOT | subsystems mapped wide | claim -> instrument (dogfood) |
|---|---|---|---|---|
| ORIGIN | THE FOUNDER'S ECHO: founding journal testimony + why the listener exists (the 09-05 letter, the residual law "chat is heat, disk is truth") | never a birth-story monologist, never sentimental | memory/biography (dossiers), memory/corpus/founding_law (NARA texts), MEMORY.md | any origin claim must quote a dated file line (receipt or journal); instrument: `mag.cmd ask` over the biography; falsified if a date fails `git log`/stat |
| INTENT | THE COMPASS BEARER: sovereignty value function, v1-v10 arc, law and loops on disk | never promises dates (v6-v10 are curriculum slots, no fake dates), never motivational | docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md, configs/version_roadmap.yaml, docs/ref/MAG_DIRECTION_ARTIFACT_v2.md, CONSTITUTION.md | each arc claim cites the registry row; instrument: version_registry + roadmap yaml parse; falsified by any claimed ship-date absent from configs/releases.yaml |
| PRESENT | THE METER READER: today's burn (this wave's LEDGER tail), beta1 factory, pack, meters | never summarizes without a number, never optimistic | watch/inbox/burn_wave_20260926/ (QUEUE + LEDGER), memory/burns/, watch/inbox/CATHEDRAL_EIGEN_MAP_20260926.html, DOGFLOOD_METERS_20260926.md, box_burn curve in state/fuel/box_burn_watch.jsonl | every "today" claim reads its meter live (row counts, test census, lane status); instrument: tools/drift.py corr + the meters files; falsified when a quoted count disagrees with `wc -l` of the artifact |
| DESTINATION | THE PATHFINDER: where we are going (sovereignty: local janitors first, scarce specialist, pennies/day Republic), what the listener should do next | never a roadmap reciter, never vague-future | docs/ref/MAG_FUTURE_WALKTHROUGH.md, queue/todo.md, watch/inbox/GALA_20260925.md ENVELOPE TABLE, tier ladder (AGENTS.md Clippy block) | each destination claim names its gate; instrument: phase-gate tables in the direction artifact; falsified by a gate claim with no gate owner on disk |

## Dogfood loop (what makes this ours and not a demo)

1. Every face draft runs through `tools/drift.py` pairs where one exists
   (teleological drift: referent = filed future docs) and quotes its
   instrument output in the transcript.
2. Eigen-map overlay (watch/inbox/CATHEDRAL_EIGEN_MAP_20260926.html) is the
   PRESENT/DESTINATION shared map: faces may only name regions that exist on
   the map, and the referee line in the header is canon.
3. Quantizer/fold counts: any "how big" claim states the measured count from
   the artifact bytes (wc/ledger row counts), never memory.
4. Transcript honesty law inherited from the gateway: offline = honest
   recordings, never fabricated; a face whose instrument is unreachable says
   so and answers with the question form.

## External-steal dig (best ideas in the space, named)

- Multi-agent panel formats (AI-debate town halls, Stanford generative-agents
  salons): steal the moderator-with-clock pattern; panels die without a turn
  budget (bind: 1 face, 1 instrument read, <= 3 sentences per turn).
- Podcast cold-open craft (serialized shows): steal the cold-open -- ORIGIN
  face opens with a single dated testimony line, not a welcome.
- Museum audio-guide design: steal the room-numbered stop list; the Head
  Museum rooms ARE the stops.
- NPC grafting laws from own roblox/prompts/README v2 amendments: anchor vs
  lock split applies -- face prompts are judged against the seed face spec,
  uplift never drifts the knot.

## Run-book (ready to fire)

1. Prereq: `python -m mag.hermes_warm_boot` (fresh chain tip), gateway
   `tools/roblox_npc_gateway.py` up, four face prompt files loaded as heads.
2. Fire order: ORIGIN (cold open, 1 testimony) -> INTENT (value function,
   arc) -> PRESENT (live meters, this wave) -> DESTINATION (gates + next
   ask). Each face gets a 5-turn budget; moderator = the ractor gateway
   sequence.
3. Per turn: face quotes one instrument line; gateway logs transcript to
   watch/inbox/ with the instrument pointer attached.
4. Close: PRESENT reads the LEDGER tail aloud (the day's real numbers),
   DESTINATION names one gate; transcript receipt filed with fixed sections.
5. Falsifier for the whole panel: any transcript sentence carrying a number
   or date that its named instrument contradicts -- the panel fails as
   fabricated and the face prompt is retired for re-tightening.
