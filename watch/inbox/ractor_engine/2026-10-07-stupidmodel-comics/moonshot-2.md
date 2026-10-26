# STUPID-MODEL COMICS LANE - MOONSHOT LENS 2 (ractor 2026-10-07)

Seat: moonshot-2. Every claim names bytes I read or commands I ran this
sitting. No em-dashes. Sibling receipts in this dir (accuracy, economics,
operations, communication, dogfood, moonshot-1) were read; convergences
marked, duplication avoided. My probe banked beside this file:
probe_moonshot2_imaging.py + probe_moonshot2_imaging_results.json.

## F1 THE COMIC WRITER LEG IS DONE ON LOCAL SEATS - 12/12 WITH THE POSE ENUM (CONVERGENT x4, and the door that is still missing)

I fired probe_moonshot2_imaging.py this sitting ($0, 12 calls, 4 free seats
x 3 session facts, FORMAT-SCHEMA arm only, temp 0, typed schema with the
mag_dance POSE enum added per moonshot-1 M5): gemma:2b 3/3, qwen2.5:3b-
instruct 3/3, qwen2.5:7b 3/3, gemma4:latest 3/3, ALL rows schema_ok AND
pose_ok (results JSON summary block). That is the third independent
confirmation of the typed-schema door on comic specs (sibling
comic_spec_probe.json: gemma:2b 0/3 schema_ok unconstrained vs 3/3 format;
economics arm B 10/10 poses; moonshot-1 gemma4 7/8 spec_valid), and it
extends the door to the POSE field at 4/4 seats: the enum + required keys
hold the vocabulary on every free local seat, 1.7GB to 9.6GB.

THE GAP my census found: the door exists ONLY on the local Ollama path.
The fleet queue contract carries no format field (tools/free_lane_fleet.py:16
"schema: {id, kind, prompt, max_tokens?}") and the gauntlet feeder stages
only {id, kind, prompt} (tools/gauntlet_feed.py:79), so the register's
remote seats (nvidia NIM meta/llama-3.2-11b-vision-instruct at
tools/free_lane_fleet.py:128-132, mistral, cohere, openrouter) can NEVER
receive a schema until the queue grows a format pass-through. The dogfood
probe's own docstring admits it: "the full trial rides the gauntlet feeder
once fire() carries the format door" (comic_spec_probe.py:11-12). The
stupid-model comic lane is one 45-minute wiring change away from 24/7 free
production across 7 providers; without it, it is a local-only demo.
FALSIFIER: add the format field, stage comic trials to 3 remote seats; if
NIM/mistral/cohere reject or ignore guided decoding (OpenAI-compat
response_format variance), the remote comic family stays unshippable and
the lane stays local, honestly.
MOVE (45 min): optional format passthrough in the fleet queue drain + one
comic family in gauntlet_feed.py + one probe cycle; grade with the
existing score() shape.

## F2 THE MOONSHOT SWING: THE COMIC PAGE IS A ROLL-SHAPE FINGERPRINT, NOT A RENDER (my measurement, new this sitting)

Same session fact, four seats, one schema wall. Measured cross-seat
authorial agreement (my probe's agreement block, Jaccard over caption
digits and source keywords, 6 seat-pairs per source): digit Jaccard means
0.333 / 0.5 / 0.25, keyword Jaccard means 0.297 / 0.292 / 0.292, pose
vocabulary spread across 6-7 of the 7 POSES on every source, with pair
extremes at 1.0 AND 0.0 inside the same source. That is the fingerprint
middle band: the seats partially converge on WHICH facts carry the strip
(digits/keywords) while style is walker-chosen (poses). This is the
imaging-turing frame made mechanical: the schema wall is the light maze,
the panel choices are the path, and the page DIFF is the walker's shape
printed on the photon (the frame's own bytes: ROLL_SHAPE_TURING_CASTLE_
20261007.md:107-111 "the maze does not teach the model - it images it").
moonshot-1's M1 made the comic a render face of telemetry (zero model
calls); this is the complementary half: the comic as an AUTHORING probe
(the maze interrogating the reader). A comic family in the gauntlet
register would give the roll-shape cards (ROLL_SHAPE receipt first probe,
:46-51) their visualization for free: per-animal strip galleries where
the expensive-vs-cheap delta column (GAUNTLET_FREE_LANDED_20261006.md:48-54)
becomes visible, not just numeric.
FALSIFIER: the n=50 power run (accuracy F1's owed gate); if mean digit or
keyword agreement rises above ~0.8 the seats are indistinguishable and the
fingerprint claim dies; below ~0.1 it is noise with no fact anchor. 6 pairs
per source at n=3 is a pilot, not a verdict.
MOVE (90 min): stage comic as the 5th gauntlet family (feeder family +
grade with score() + jaccard agreement) and let the 30-min free clock
build the register column.

## F3 EXTERNAL VERDICT: THE NAMED SEAT IS REAL, ALREADY PAID FOR, AND NOT EVEN THE BEST WRITER; NOBODY OUTSIDE HAS SHIPPED THIS COMBINATION

Google's "new model that runs on nothing": the Gemma 4 E-tier. Web-verified
this sitting: Gemma 4 is Google DeepMind's open-weight natively multimodal
family released April 2026, variants E2B / E4B / 12B / 31B / 26B-A4B,
Apache 2.0 (ai.google.dev, blog.google, deepmind.google via search); the
on-device "runs on nothing" lineage descends from gemma-3n (announced
2025-05-20, runs at ~2GB RAM, developers.googleblog.com). The local box
already runs the family: my /api/show this sitting reads family gemma4,
general.parameter_count 7,996,157,674 (8.0B, Q4_K_M, 9.6GB on disk), 42
blocks, vision tower 16, audio tower 12, context 131072; the ~8B total
matches the E4B effective-4B shape (gemma-3n's E4B also carried ~8B total).
Variant naming beyond param count is interpretive, /api/show carries no
variant field. Decision data: in MY probe gemma4:latest scored 3/3 but so
did qwen2.5:3b-instruct at 1.9GB (5x smaller, faster per moonshot-1's
latency ladder); CONVERGENT with moonshot-1 M2's ranking. The operator's
named seat is on payroll and free; the default writer recommendation stays
qwen2.5:3b-instruct with gemma4 fallback.
Prior art (my search + accuracy.md F5 composed): no product combines LLM
generation + JSON panel spec + deterministic renderer; the pieces exist:
Comix I/O (xkcd-style SVG API, davidwalsh.name - NEW find, steal the SVG
API shape), cmx.js (2013 markup vocabulary, prototype-dead, accuracy.md
:116-121), SVGBob (text-to-SVG instrument class), xkcd-mcp (sandraschi,
fetch-side only, cannot draw), raster AI xkcd tools (Scribd overview) -
the raster route this lane rejects (paid, edit-locked, resolution-bound).
Sources: developers.googleblog.com Gemma 3n announcement; ai.google.dev
Gemma 4 overview; github.com/sandraschi/xkcd-mcp; davidwalsh.name Comix
I/O post; scribd.com AI-xkcd overview.
FALSIFIER: a shipped product doing session -> cheap model -> typed panel
spec -> deterministic SVG/PNG renderer would demote this lane from novel
to a steal; none found by two seats' independent searches (accuracy F5 +
mine).
MOVE (20 min, decision only): adopt Comix I/O + cmx field vocabulary into
the renderer spec; bank the seat decision (qwen2.5:3b default writer).

## F4 THE WIRING POINT: DISCORD IS THE LAST LEG, AND THE COMIC ORDER ITSELF IS THE VEHICLE TO UNBLOCK IT

Verified bytes this sitting: the only proven-live discord door is the
phone DM relay, approvals-only by founding law, never a shared channel
(mag/phone_relay.py:137-159 area, the "Never a shared guild channel" law,
:1-18 docstring), JSON-text-only (no multipart, :93-95); the guild channel
#game-c-overview is 403-locked since setup with the FW30 two-click cure
filed 09-28 (communication.md F3, receipts cited there); discord embeds
cannot render SVG inline (discord-api-docs issue #25935 per accuracy.md
F4:101-110, PNG twin required). So the comic's operator-facing faces today
are the dashboard (SVG canonical) and watch/inbox receipts (PNG twin +
the spec itself as the durable record). The build order stands: render
first, discord last.
FALSIFIER: a live post to #game-c-overview after 09-28 (none found by the
communication lens; not re-probed from this seat, the token is
operator-gated).
MOVE (10 min): the next DAWN_REPORT carries the comics order with the FW30
two-click dependency ON the lane itself - the operator's own order now
carries its unblock ask back to him (communication F3's move, endorsed).

## F5 NO SACRED COWS ON THE CARRIER: THE POSE VECTOR CLOSES THE CHAIN MODEL -> RENDERER -> VOXEL, AND THE SVG-vs-PNG DEBATE WAS THE WRONG CUT

Bytes I read myself this sitting: POSES are 10-float joint-angle arrays
keyed by name (dashboard/static/mag_dance.html:52-67, drawSkeleton :81);
the estate's bare-metal deterministic svg() pattern (zero deps, same input
-> same image) is mag/game_entry.py:154-188; the voxel system is an
imaging instrument in its own right (mag/volume_fidelity.py:1-27: SHADOW
WALK quantizes 9,305 behavioral parts into a voxel grid with a seeded
carve, and its four gauntlet tests grade which structures are real - a
null-model control included). My probe closes the model leg: the pose
ENUM survives generation at 4/4 seats, so the interface is closed
end-to-end: model emits pose NAME, renderer maps name -> joint angles
(POSES dict), the voxel face extrudes the same angles into the SHADOW WALK
grid (a stick figure IS a skeleton the voxel grid can extrude, moonshot-1
M5's point, now byte-verified on my side). ONE spec, THREE faces: SVG
canonical, PIL PNG twin, voxel extrusion owed its own window if the
angle -> voxel glue exceeds one sitting.
FALSIFIER: extrude one comic pose (pointy) into the mountain slice; if the
transform exceeds a one-sitting glue script the third face is its own
window, not v1 scope (moonshot-1 M5's falsifier, adopted unchanged).
MOVE (30 min): freeze the panel spec with pose NAME (enum) + joint-angle
table as the renderer constant; cmx/Comix field names for the spec keys.

## COMPOSITION MAP (Part A delta over moonshot-1's)

Composes unchanged (verified this sitting): POSES + drawSkeleton
(mag_dance.html:52-81), svg() deterministic pattern (game_entry.py:154+),
SHADOW WALK voxel grid + gauntlet tests (volume_fidelity.py:1-27), the
free fleet + gauntlet feeder/grader/clock (free_lane_fleet.py,
gauntlet_feed.py, gauntlet_grade.py), the M1 typed-schema door
(m1_grammar_bench.py; result byte-verified m1_bench.json:5-9), phone
relay door law (phone_relay.py:137-159). Builds new: the fleet queue
format pass-through (F1's 45 min), the comic gauntlet family + agreement
grader (F2's 90 min), the renderer itself (moonshot-1 M1's 60-90 min),
the dawn input adapter (moonshot-1 M4). Nothing in this lane needs a new
engine; every leg is a wire between existing organs.

## BLIND SPOTS (honest)

- My probe is n=3 per seat, one arm, one prompt set, temp 0; the
  agreement means ride 6 pairs per source. The n=50 gate supersedes.
- No remote free-seat calls fired from this seat (no NIM/mistral/cohere
  comic measurement; F1's gap claim rests on the queue schema bytes and
  the register's provider table, not on a failed remote attempt).
- msg 346 (sess_7318df04) remains unsourced: filename search for
  *7318df04* under ~/.zcode returned no transcript file (exit 1); the
  imaging-turing frame stands on ROLL_SHAPE_TURING_CASTLE_20261007.md's
  own bytes :107-111, same as moonshot-1 concluded.
- Gemma 4 variant naming (E4B vs other) is interpretive: /api/show gives
  family + param count only; the web results name the family variants
  but I did not match a local variant label.
- Discord behavior (SVG non-embedding, 403 lock) rests on sibling doc
  fetches + the FW30 receipt; I did not re-fetch the discord API docs.
- Wit is unscored by every probe including mine (form only); the local
  qwen2.5vl:3b vision seat (3.2GB, seen in /api/tags this sitting) is an
  obvious render-grader door, not fired.

## F2 CORRECTION (hostile second pass, same sitting, appended not rewritten)

The pass weakened F2's digit leg and pose leg. I re-derived from the banked
rows with my own recompute (command in the sources line below) and CONFIRM
the hit, then the correction:

- WITHDRAWN: the digit "middle band" (0.333/0.5/0.25 means). My jaccard()
  scored empty-empty pairs as 1.0 (probe_moonshot2_imaging.py:91-92, the
  `if not a and not b: return 1.0` line). Data-pair-only means are
  0.2 / 0.0 / 0.1 - at or below the noise floor I myself set (~0.1).
  merkle's 0.5 was entirely 3 empty-empty pairs of 6.
- WITHDRAWN: pose vocab spread 6-7 of 7 as evidence - chance baseline at 45
  uniform draws over a 7-enum is 6.99 of 7 (saturated, zero discrimination).
- ALSO corrected beyond the pass: merkle's keyword mean 0.292 carried one
  empty-empty 1.0 too; clean keyword means are 0.297 / 0.15 / 0.292.
- WHAT SURVIVES (same rows, stronger shape than the withdrawn means):
  three per-seat categorical traits, i.e. a fingerprint PROFILE, not a
  pairwise mean:
  1. DIGIT-CARRIAGE LADDER (rows of 3 carrying source digits):
     gemma:2b 0, qwen2.5:3b-instruct 0, qwen2.5:7b 2, gemma4:latest 3 -
     the exact in_character ladder of the sibling probe
     (comic_spec_probe.json summary: gemma:2b 0/3, qwen2.5:7b 2/3,
     gemma4 3/3). CONVERGENT x2, two probes, two sittings.
  2. PANEL ECONOMY: gemma:2b drew 3 panels on 3/3 rows; every other seat
     drew 4 on 4/4 rows each - the smallest seat is the minimalist,
     bimodal by seat.
  3. POSE-CORE REUSE: each seat reuses a 2-4 pose core across all three
     sources (gemma:2b {kick,pointy}; qwen3b {flail,pointy,shimmy};
     qwen7b {flail,pointy,strut}; gemma4 {pointy,shimmy,stomp,strut},
     identical full sets on two sources) - style is seat-consistent
     across different facts, which IS the walker signature the vocab
     number could not show.
  Plus one clean datum: on gauntlet-selfstrike the two digit-carrying
  seats quoted the IDENTICAL set {0,243,4,8} (Jaccard 1.0 on a real data
  pair).
- GRADER FIX (one line, law: fix the instrument first): jaccard returns
  None on empty-empty (flag and exclude); carriage-rate per seat becomes
  the primary statistic. Correction block appended to
  probe_moonshot2_imaging_results.json (original agreement block stands
  as artifact history, the gauntlet grader-self-strike precedent,
  GAUNTLET_FREE_LANDED_20261006.md:43-47).
- TIGHTENED FALSIFIER: the n=50 run must report (a) per-seat carriage
  rate, (b) clean data-pair keyword means, (c) panel-economy and
  pose-core consistency. If carriage rates converge across seats at n=50,
  or clean keyword means sit below 0.1, the comic-probe dies as a
  fingerprint instrument. The 5th-gauntlet-family move (90 min) carries
  the fixed grader.

## Sources (commands run this sitting)

probe_moonshot2_imaging.py fired (12 calls, $0.00, results banked);
curl /api/tags + /api/show (gemma4 identity); git grep censuses (xkcd/
comic/voxel/mermaid/stickfigure scoped to text organs); reads:
state/CURRENT.md, ROLL_SHAPE_TURING_CASTLE_20261007.md, GAUNTLET_FREE_
LANDED_20261006.md, tools/m1_grammar_bench.py + m1_bench.json, tools/
free_lane_fleet.py (queue contract + PROVIDERS), tools/gauntlet_feed.py,
mag/phone_relay.py, mag_dance.html (POSES), mag/game_entry.py (svg),
mag/volume_fidelity.py (head), sibling receipts accuracy/communication/
moonshot-1 + comic_spec_probe.py/.json, memory/zknot/LATEST.md (7318df04
section). Web: Gemma 3n announcement, Gemma 4 overview, xkcd-mcp,
Comix I/O, AI-xkcd Scribd overview. Hostile-pass correction sitting:
venv python recompute over probe_moonshot2_imaging_results.json (digit
data-pair means, clean keyword means, per-seat carriage/panel/pose-core
tables, chance baseline 7*(1-(6/7)^45)); correction block appended to the
results JSON; this section appended to this receipt.
