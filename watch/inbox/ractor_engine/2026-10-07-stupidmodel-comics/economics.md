# STUPID-MODEL COMICS LANE - ECONOMICS LENS (ractor 2026-10-07)

Seat: economics (EV-per-cost pricer, free-lane pricing, falsifier firing).
Every claim below names the bytes I read or the command I ran this sitting.
No em-dashes. OWED marked where it lives.

## THE PROBE (fired, not designed; $0.00 total, both arms)

The fold demanded one falsifiable probe: can the free seats emit valid
panel specs at useful rates. I fired it in two arms, both scored
mechanically (parseable / in-vocabulary / minimal), scripts and raw rows
banked beside this receipt.

ARM A, the queue door (what the gauntlet can ship TODAY, unconstrained):
13 line-grammar trials staged into watch/inbox/free_lane_queue/ (same door
the feeder uses; schema {id, kind, prompt}), drained by two hand-run
cycles of `.venv/Scripts/python.exe -m tools.free_lane_fleet --cycle`
(documented usage, tools/free_lane_fleet.py:33). Result: 13/13 fired
$0.00, 2/13 PASS. By seat: mistral 0/4 (drops the PANEL scaffold
entirely), cohere 0/3 (banked shape unparseable + doubles poses, e.g.
"POSE: flail kick"), llama-3.2-11b 1/4, qwen2.5:7b 1/2 (the miss invented
"shrug", a pose the dance library lacks). Files:
econ_probe_results_arm_a.json, probe_comics_arm_a.py.

ARM B, the format-schema door (the M1 door, direct local Ollama,
body["format"] = comic JSON schema with pose and who as enums): 10 trials
on the two local seats. Result: json_ok 10/10 (schema door guarantees
parseability - M1 reproduced with a comic schema), qwen2.5:7b 5/5 FULL
PASS, median 9139 ms, ~330-char specs; gemma:2b 2/5 full PASS, 5/5
json_ok, all 3 failures are captions of 11-13 words against a 10-word
bar (poses, who, structure all valid; a schema cannot count words, a
deterministic trim or maxLength cures it). Sample full spec (qwen t5, the
dice-suspend subject): three panels, strut/pointy/shimmy, captions
"Colleague: Dice claim?" / "Stickman: Not verifying." / "Operator: Why
not?" - that is the estate's trust-bytes law as a punchline, emitted free
in 9 seconds. Files: econ_probe_results_arm_b.json, probe_comics_arm_b.py.

## E1 THE FALSIFIER IS SETTLED BY MEASUREMENT: the format door ships, the queue door does not

Answer: YES, free seats emit valid panel specs - but only through the
format-schema door. Arm B (local, $0.00) parses 10/10 and full-passes 7/10
(10/10 after the caption-trim cure); Arm A (the queue every gauntlet trial
rides today) full-passes 2/13. This is CONVERGENT with the operations
sibling's F2 (their 2026-10-07-stupidmodel-comics/operations.md:31-49
predicted from code reading that fire() sends no format/response_format,
verified by me at tools/free_lane_fleet.py:260-268, and that the JSON arm
would ride the 0/30 unconstrained path, verified by me at
watch/inbox/48h_synth/m1_bench.json:5-8 with the door itself at
tools/m1_grammar_bench.py:36-38): they predicted, I measured. Production
carrier consequence: the comic generator fires the LOCAL Ollama format
door (works today, zero amendments), and the fleet queue is reserved for
sensing/competition, never for shipping specs.
FALSIFIER: rerun Arm A with 30 trials; if unconstrained full-pass exceeds
50 percent on any seat, the format-door amendment to fire() is unnecessary
for API seats.
MOVE: 0 min (measurement banked); the fire() response_format amendment is
a separate 25-min build only if API-seat comics are ever wanted.

## E2 THE MARGINAL COST OF A COMIC IS $0.00 PLUS NINE SECONDS OF AN ALREADY-LIT GPU

Priced from measured bytes: qwen2.5:7b emits a full valid 3-panel spec at
median 9139 ms on the box whose Ollama server is a 24/7 longrunner
(GPU_LADDER_20261007.md rung 1, gemma:2b 84.7 tok/s 100 percent GPU,
qwen 19.8 tok/s partial; ollama serve alive this sitting, /api/tags
answered). The GPU burns whether or not the comic is drawn, so marginal
cost is queue latency, not money or watts. No paid organ is needed
anywhere in the carrier: the renderer is deterministic (POSES library
dashboard/static/mag_dance.html:52-67 verified: flail kick shimmy strut
pointy spirit stomp; panel-grid SVG pattern per operations F5), and the
paid image organs are gated off anyway (image-blast keys ABSENT from
.env, their F5, path .agents/skills/image-blast/SKILL.md:14-21). EV
ranking is therefore total: deterministic renderer + dumb local writer
dominates every alternative at every margin that matters (cost, latency,
parseability, auditability - the spec is the receipt).
FALSIFIER: if the renderer's SVG output exceeds Discord-lane needs and
forces a paid raster organ, the $0 lane claim dies; operations F4 already
shows the honest shape (SVG banks, PNG twin renders deterministically).
MOVE: build order is renderer first (60-90 min, operations F5's
comic_renderer.py), generator second (30 min: prompt + schema + trim,
already 80 percent written as probe_comics_arm_b.py).

## E3 THE FREE-FLEET PAYROLL IS 5/7 LIVE, NOT 7/7 - an honest pricing correction

The health table I ran this sitting (`.venv/Scripts/python.exe -m
tools.free_lane_fleet --health`) reads openrouter-free-1
consecutive_fails 6 (last_ok absent, last_fail 2026-10-05T14:33:10Z) and
openrouter-free-2 consecutive_fails 5 (last_ok 2026-10-05T07:00:27Z):
both dead since 10-05, skipped by the >=5 gate (free_lane_fleet.py:306-308).
The GAUNTLET_FREE_LANDED receipt's "7 free providers" headline
(GAUNTLET_FREE_LANDED_20261006.md:12-13) is 5 live today. The five live
seats still over-cover the comics need (two local + mistral + cohere + 2
x nvidia llama). The known caps did NOT bite on real specs: 1200-char
banked truncation (free_lane_fleet.py:296) and ollama num_predict 300
(:267) sit far above the measured 298-433-char outputs.
FALSIFIER: re-provision the OpenRouter keys and the payroll reads 7/7
again; if they stay dead a week, strike them from the gauntlet headline
permanently (a dead free lane priced as live is hoarding theater).
MOVE: 10 min - either re-provision or amend the receipt's headline to
"5 live" with the health-table receipt.

## E4 THE POSE VOCABULARARY IS THE LOAD-BEARING COMPOSITION, AND IT IS TWO POSES SHORT (pointing already exists)

The schema enum made in-vocabulary 100 percent by construction (Arm B:
every pose and who legal, 10/10) - the dumb model CANNOT leave the dance
library, which is the carrier pattern entire: model proposes within
walls of light, deterministic instrument renders, the dice never lie.
The light-maze frame holds verbatim: "The maze does not teach the model -
it images it. Every gauntlet run, every dice-honesty trial, every
beat-grid combo is a photon returning with the walker's shape printed on
it" (ROLL_SHAPE_TURING_CASTLE_20261007.md:108-110; cite corrected
2026-10-07 second pass, was off-by-one at :109-111);
this probe just imaged six walkers through a comic grammar. Two gaps,
one measured and one register-need: MEASURED - comics pull a shrug shape
the dance library lacks (qwen invented "shrug" unprompted, Arm A a09,
the only vocab miss on a parseable output); REGISTER-NEED - no seated
shape exists among the 7 standing dance poses (flail/kick/shimmy/strut/
pointy/spirit/stomp, mag_dance.html:53-59 + stomp :67), which the
mountain-climb comic wants for a seated-on-summit panel. Pointing is NOT
a gap: pointy at mag_dance.html:57 is commented "q-infused point" with
both arms extended (elbows -160/-150) - already the pointing shape. The
voxel/mountain tie lands here: the missing shapes are renderer
constants, not model outputs.
FALSIFIER: render the three canonical joke shapes cold; if the 7+2
vocabulary cannot land an xkcd-register joke, add props (sign, laptop)
before widening the model side.
MOVE: 15 min - add shrug/sit to the renderer's POSES as static angle
rows (pointy already covers pointing); rerun probe_comics_arm_b.py
(already model-agnostic) to confirm 100 percent stays 100 percent.

## E5 DISCORD DELIVERY OWES 90 MIN OF BUILD, ZERO RUNNING COST - and nothing else is owed money

Converging with operations F4 (SVG not on the Discord embed whitelist,
multipart door absent: mag/phone_relay.py:93-95 JSON-only, bones_adapter
MAX_MESSAGE 1900): the economics addendum is that every owed item on the
delivery leg is a BUILD cost, not a RUN cost - PNG twin render is
deterministic CPU, the multipart post is one HTTP call. Total lane
estimate at the format door: 0 dollars, ~2-3 h one-time build (renderer
60-90, generator 30, discord door 90), then ~9 s GPU per comic forever.
The operator's "keep everything cheap" order is satisfied by
construction, not by discipline.
FALSIFIER: the first 30 production comics; if any leg demands a paid
call (vision model, hosted raster, image API), the construction claim
dies and the lane needs a repricing.
MOVE: none this sitting (build belongs to the dogfood lens's one-sitting
list; the economics seat prices it, dogfood builds it).

## OWED

- The Google "runs-on-nothing" model is NOT identified by this seat
  (accuracy lens leads). Economics note only: the format door is
  model-agnostic (any Ollama-pulled model takes body["format"]); adding
  it is a pull plus a rerun of probe_comics_arm_b.py, ~10 min, $0.00.
  If it is a gemma-3n-class tier, it lands between gemma:2b (funnier,
  sloppier) and qwen2.5:7b (reliable) on a 6 GB card.
- Joke QUALITY is eyeballed on 3 samples, not scored; the mechanical
  grader measures form, not wit. A wit grader would need the funded tier
  (judgment climbs), estimated <$0.01 per 30 comics if ever wanted.
- The cohere envelope question (fleet extraction vs model echo for the
  list-repr shape in a03) is unresolved by one byte-look; it does not
  affect the verdict (pose-doubling fails independently).
- n is small (13 + 10 trials, one sitting, temp 0.3): free-lane law
  applies, these rates are sensing findings, not production statistics.

## Sources (this sitting)

Commands run: two fleet cycles + --health (outputs quoted above), probe
scripts --stage/--score (results JSONs banked beside this file), ollama
/api/tags, the ledger greps. Bytes read: watch/inbox/48h_synth/m1_bench.json,
tools/m1_grammar_bench.py, tools/free_lane_fleet.py (:115-137 providers,
:251-296 fire, :299-358 cycle), tools/gauntlet_feed.py,
tools/gauntlet_grade.py, watch/inbox/GAUNTLET_FREE_LANDED_20261006.md,
watch/inbox/gauntlet/GAUNTLET_REGISTER.jsonl, dashboard/static/mag_dance.html
(POSES + drawSkeleton), watch/inbox/GPU_LADDER_20261007.md,
watch/inbox/ROLL_SHAPE_TURING_CASTLE_20261007.md:100-126, state/CURRENT.md,
sibling watch/inbox/ractor_engine/2026-10-07-stupidmodel-comics/operations.md
(convergence marked where I re-derived their claims).
