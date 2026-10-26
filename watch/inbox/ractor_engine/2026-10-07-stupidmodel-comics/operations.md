# STUPID-MODEL COMICS LANE - OPERATIONS LENS (ractor 2026-10-07)

Seat: operations (dispatch shapes, fold integrity, silent failures, cadence
health). Every claim below names the bytes I read or the command I ran this
sitting. No em-dashes. OWED items marked.

## F1 THE FALSIFIER RIG IS LIVE AND IDLE - the comic probe lands on it same day, $0.00

The MagGauntletFree30 clock fires every 30 min RIGHT NOW (logs/gauntlet_free.log
tail: fires stamped 12:15:05Z, 12:45:02Z, 13:15:01Z, 13:45:11Z, 14:16:44Z today,
each "gauntlet cycle done (exit 0)") and every cycle stages ZERO new trials:
"GAUNTLET-FEED: staged 0 trials (queue 0 pending, 12 already graded)". The
register census I ran (grep -o family over GAUNTLET_REGISTER.jsonl) reads 16
rows in exactly 4 families: beat 8, consensus 4, dice 2, metagame 2. No comic
family exists. The free fleet is also hot (ledger.jsonl tail rows at
14:34:54Z-14:35:22Z, corridor probes banking ok). This is the standing
operations shape the comics lane should compose: the fold's falsifiable probe
(format-schema panel-spec trial on 3 free seats) is ONE new family in
tools/gauntlet_feed.py build_batch() (gauntlet_feed.py:99-138) plus one
grade_comic() mechanical check in tools/gauntlet_grade.py - no new clock, no
new engine, no new provider wiring. The rig was BUILT for exactly this class
of trial (operator order 2026-10-06 quoted verbatim at
watch/inbox/GAUNTLET_FREE_LANDED_20261006.md:3-7).

FALSIFIER: stage the comic family and watch two cycles; if the register does
not grow comic rows within 60 min, the rig has a silent failure my log read
missed.
MOVE: 45 min - add COMIC variants to build_batch(), a parseable/in-vocabulary
grader, run `python -m tools.gauntlet_feed --count 6`, wait one clock cycle.

## F2 M1 DOES NOT TRANSFER AS-IS: no format schema rides the fleet drain

The ask's falsifier premise cites the M1 grammar bench: banked bytes verified
this sitting, watch/inbox/48h_synth/m1_bench.json reads unconstrained_valid
0/30 vs format_schema_valid 30/30 on gemma:2b ("M1 CONFIRMED"). BUT the bench
talks to Ollama DIRECTLY with body["format"] = schema (tools/m1_grammar_bench.py:36-38),
and the fleet drain does NOT: fire() at tools/free_lane_fleet.py:260-268 sends
{model, stream, max_tokens: 700, temperature: 0.3, messages} for openai/cohere
kinds and {model, prompt, options} for ollama - no format, no response_format,
for any provider. A JSON panel-spec trial through the queue rides the
UNCONSTRAINED arm, which M1 measured at 0/30 on the 2B tier. The gauntlet's
one proven structured-output family (beat) survived precisely because its
grammar is LINE-BASED plain text ("FORM on <ms>"), not JSON: corrected register
rows show mistral 8/8 and cohere 6/6 onsets exact (GAUNTLET_REGISTER.jsonl rows
12-14, ts 00:15:05Z). OPERATIONS VERDICT: the comic panel spec must ship as a
line grammar (PANEL n / speaker / pose-name / caption lines) to inherit the
beat family's proven parseability, OR fire() gets a response_format amendment
first - the JSON-braces spec as-is would test the wrong arm and manufacture a
false negative for the whole lane.

FALSIFIER: stage one JSON-braced comic trial through the queue and one
line-grammar twin; if the JSON arm parses at high rates on mistral/nvidia
seats, the constraint is unnecessary and the line-grammar caution dies.
MOVE: 20 min - write the trial prompts both ways; the probe scores the delta
for free on the same seats.

## F3 THE 1200-CHAR TRUNCATION WILL EAT PANEL SPECS - a known grader-artifact class

fire() truncates every banked output to 1200 chars (free_lane_fleet.py:296,
text.strip()[:1200]) and the grader scores the ledger detail VERBATIM
(gauntlet_grade.py:153, text = str(row.get("detail", ""))). A 3-4 panel JSON
spec with captions and character lists can exceed 1200 chars; a mid-JSON cut
grades as a parse failure that is the FLEET's artifact, not the model's - the
exact disease the register already caught once (the BEAT_ONSET ms-suffix
grader artifact, confessed in-code at gauntlet_grade.py:66-71: mistral's
perfect grid graded 0/4 until the regex was fixed; corrected rows appended,
never rewritten). Second cap: the ollama seat gets num_predict 300
(free_lane_fleet.py:267) - the local qwen2.5:7b seat physically cannot emit a
long spec. The line-grammar spec from F2 doubles as the size cure: pose NAMES
+ short captions for 4 panels fit comfortably under both caps, and the pose
vocabulary keeps the dumb model's output tiny by construction.

FALSIFIER: measure the char length of real emitted specs in the first comic
register rows; if any land in 1100-1200 (truncation zone), raise the cap for
this family or shorten the grammar - the number decides, not the design.
MOVE: 10 min - add a length column to grade_comic() so the artifact zone is
visible forever.

## F4 THE DISCORD POST LEG HAS NO FILE DOOR - and SVG is not embeddable

Both estate Discord surfaces are text-only. phone_relay._api sends JSON bodies
only (mag/phone_relay.py:93-95, Content-Type application/json, no multipart
path) and is DM-only by law (mag/phone_relay.py:137-159). bones_adapter is the
full bot (discord.py 2.7.1 verified importable in the venv this sitting:
`.venv/Scripts/python.exe -c "import discord"` -> discord.py present 2.7.1)
but formats TEXT into code fences, MAX_MESSAGE 1900 (mag/bones_adapter.py:66,
99-105), guild-pinned to #game-c-overview (bones_adapter.py:60-61). Discord
docs fetched this sitting (https://docs.discord.com/developers/reference):
file upload requires multipart/form-data with files[n] fields, and embed
attachments whitelist ONLY .jpg/.jpeg/.png/.webp/.gif - SVG is not on the
list. CONSEQUENCE for the carrier design: keep the SVG as the CANONICAL
artifact (deterministic, resolution-free, dashboard/estate_walk face, banks to
watch/inbox), but the Discord post needs a PNG twin rendered from the same
spec (deterministic twin render - the dice never lie) plus a multipart upload
door that does not exist yet. The SVG-carrier shape is not WRONG for the
voxel/mountain tie; it is wrong as the Discord payload format.

FALSIFIER: post an SVG file to the pinned channel via the amended door; if
Discord previews it inline acceptably, the PNG twin is unnecessary and only
multipart remains owed.
MOVE: 90 min - comic_relay.py mirroring phone_relay's pinned-host door with a
files[0] multipart leg + a spec->PNG rasterizer step; SVG banks alongside.

## F5 WHAT COMPOSES: the drawing engine and the SVG pattern already exist - image-blast is the wrong leg

MAG DANCE holds the stick-figure engine: dashboard/static/mag_dance.html:52
POSES = named joint-angle pose library (stomp/strut/flail...), :81
drawSkeleton() canvas renderer, per-model control schemes, 138 lines total
(commit dde94595d names the Napoleon pose library and the Ossuary Luau
skeleton - the Mountain tie). Bare-metal zero-dep SVG rendering is proven in
mag/game_entry.py:154-188 (svg() builds the region grid) and
mag/console_render.py:8-10 (swarm_map.svg, oscillating.svg). The comic
renderer COMPOSES both: panel grid from the game_entry pattern, figures from
the POSES vocabulary - the model emits pose NAMES + captions from a fixed
vocabulary and never pixels. image-blast is NOT the comics path: it is a
paid-organ pipeline gated off (.agents/skills/image-blast/SKILL.md:14-21:
World Labs + FAL keys ABSENT from .env, planning only) - routing comics
through it would violate the operator's keep-everything-cheap order.

FALSIFIER: if a POSES-named spec cannot express an xkcd-register joke (test:
render 3 canonical joke shapes from the vocabulary and read them cold), the
vocabulary needs poses or props added before any model trial.
MOVE: 60 min - comic_renderer.py: POSES + panel grid + caption text ->
SVG/PNG twin; dogfood by rendering yesterday's session summary as a 4-panel.

## BLIND SPOTS (honest)

## CORRECTION APPENDIX (hostile second pass, 2026-10-07; F2 weakened - rows
appended, never rewritten, the gauntlet's own practice)

F2's code cites stand but its RECOMMENDATION was wrong, contradicted by fired
sibling probes in THIS directory (landed after my first write):

- econ_probe_results_arm_a.json (queue door, unconstrained line grammar,
  13 fired): n_pass 2/13 - mistral 0/4, cohere 0/3, llama-3.2-11b 1/4,
  qwen2.5:7b 1/2. The line-grammar-through-queue route I ranked first is
  MEASURED WEAK on the free API seats.
- econ_probe_results_arm_b.json (format-schema direct door, and at FLEET
  temperature 0.3 per probe_comics_arm_b.py:67, killing the temp-0 confound):
  json_ok 10/10 (gemma:2b 5/5, qwen2.5:7b 5/5); qwen2.5:7b full PASS 5/5;
  gemma:2b 2/5 pass failing only caps_ok.
- comic_spec_probe.json: gemma4:latest FORMAT-SCHEMA 3/3 on all four axes
  (parseable/schema_ok/in_character/minimal); gemma:2b and qwen2.5:7b
  UNCONSTRAINED schema_ok 0/3 each vs FORMAT 3/3; note qwen2.5:3b-instruct
  held schema_ok 3/3 UNCONSTRAINED - the format door may be unneeded at 3B.
- My beat citation is corrected to the full picture: mistral 8/8 twice and
  cohere 6/6 on the 6-count trial, but the 12-count v4 FAILED 3/12
  (GAUNTLET_REGISTER row 15) - line grammar holds only for SHORT constrained
  outputs on some seats.
- NEW (un-named by the pass): arm A's cohere 0/3 is partly a FLEET defect,
  the third instance of the instrument-artifact class. The content-block join
  at tools/free_lane_fleet.py:286-288 sits on the choices path
  (msg.get("content")) which cohere's native v2 response never takes (no
  "choices" key); cohere falls to the :292-293 fallback where str(list) banks
  the repr "[{'type': 'text', 'text': 'PANEL 1...'}]" - visible verbatim in
  arm A rows a03/a04/a13 raw. The beat grader survived this because its regex
  is substring-based; a panel-grammar line parser cannot.

CORRECTED VERDICT: the disjunction resolves toward the FORMAT-SCHEMA door.
Move: amend fire() to pass a queue-item schema (response_format for openai
kinds, format for ollama) AND move the block join to cover the cohere
fallback path, then restage the 13 arm-A subjects as schema trials and
compare per-seat to arm B. Falsifier: if queue-door schema pass rates do not
approach arm B's direct-door rates per seat, the drain path itself is the
bottleneck and the comic lane needs a direct door.

- The Google "runs-on-nothing" model identity is NOT verified by this seat
  (Part B, accuracy lens leads); I made no external check of gemma-3n vs the
  sub-1B tier and assert nothing about it.
- The comic probe is DESIGNED, not fired - no register row exists until the
  F1 amendment lands, so all rate predictions above are design-time only.
- schtasks enumeration failed from this git-bash shell (path mangling on
  /TN); clock liveness is evidenced by their own logs instead (gauntlet
  fire stamps, fleet ledger mtimes), not by the task registry.
- Whether Discord previews an SVG FILE attachment (non-embed) inline is not
  verified; only the embed whitelist (no SVG) is doc-verified. F4's falsifier
  covers it.
- Consumption of the gauntlet register downstream (the weekly
  driving-ladder rib fold named in GAUNTLET_FREE_LANDED "Owed" as not yet
  built) was not audited for theater - 16 rows banked, zero folded out yet;
  the comics lane should not add a second unfolded register.
- chan/board surfaces (mag/chan) were only skimmed; whether the chan board
  already renders images that a comic could ride was not checked this sitting.
