# dogfood lens: stupid-model comics lane, 2026-10-07

Lens: organ mapper. Every finding maps onto an estate organ that already
exists and names the one-sitting port move. Jacket: the finding filed but
never wired. All bytes read and all probes fired this sitting (2026-10-07,
~15:2x-15:4xZ). No em-dashes per law. Artifacts in this dir:
probe_dogfood_arm_c.py, probe_dogfood_arm_c_results.json.

## The organ map (what composes vs what builds)

| lane stage | organ | status | port |
|---|---|---|---|
| subject source | dashboard/static/trails/day_work.jsonl rows {ts, actor, event, detail, artifacts} (read this sitting: day_work-cage CYCLE/HEARTBEAT rows); zknot recaps memory/zknot/*.md | EXISTS, structured | build a 30-line stager |
| dispatch | watch/inbox/free_lane_queue + tools/free_lane_fleet.py cycle | EXISTS (arm A fired 13 through it) | build: format passthrough (F1) |
| stupid seat | mistral/cohere/nvidia/openrouter free + local ollama (PROVIDERS tools/free_lane_fleet.py:114-137) | EXISTS, measured | none (config row only) |
| spec door | response_format json_object / ollama format:json | PROVEN, NOT WIRED into the fleet | build: ~10 lines (F1) |
| figures + poses | dashboard/static/mag_dance.html:52-67 POSES (7 poses, 10-float joint vectors) + STYLES + drawSkeleton:81 | EXISTS (MAG DANCE layer 2) | port to PIL (F2) |
| deterministic render | PIL ImageDraw (accuracy F4: PNG for discord; SVG for dashboard face) | PIL present, renderer owed | build 90 min (F2) |
| discord post | mag/phone_relay.py (approval lane, text-only, live-proven: state/phone_relay_channel.json cached 09-26, log row 09-28) + mag/surface_adapters.py:58-59,147-152 (slack webhook pattern) | pattern EXISTS, no discord row | build: webhook row (F3) |
| attention | memory/attention.md alert markdown | EXISTS | optional comic-event row |
| bank | memory/runs/free_lane_fleet/ledger.jsonl (provider/model/chars per row) | EXISTS | none |

## ARM C (this seat's probe, executed): the grammar door on REMOTE free seats

The missing arm. Arm A (econ): line grammar through the queue door = 2/13
PASS, because fire() carries no grammar door. Arm B + panel-spec probe
(accuracy): format door on LOCAL ollama = 5/5 and 7/8 spec_valid. Arm C
(mine): direct calls to the same PROVIDERS URLs with
response_format {"type": "json_object"}, JSON panel-spec prompt, same
spec_valid scorer as probe_panel_spec.py (bug-fixed). 12 calls, $0, zero
subprocess spawns. Results (probe_dogfood_arm_c_results.json):

- mistral open-mistral-nemo: 3/3 parses, 3/3 spec_valid, 3.1s mean.
  Arm A same seat: 0/4. THE DOOR FLIPS THE SEAT.
- cohere-free command-r7b: 3/3 parses, 3/3 spec_valid, 3.9s. Arm A: 0/3.
  FLIPPED.
- nvidia-1 llama-3.2-11b-vision: 3/3 parses, 1/3 spec_valid, 4.6s. Both
  failures are EMPTY caption strings ("caption": "" in raw heads), not
  parse breaks; a typed schema (minLength on caption) or renderer-side
  default cures it.
- openrouter google/gemma-4-26b-a4b-it:free (the operator's named stupid
  model): HTTP 429 x3, 0.3s. The :free variant is rate-capped at this
  moment; the seat could not be scored. OWED: retry or verify the local
  gemma4:latest tag identity.
- Zero HTTP 400s: no remote provider REJECTED response_format. The door is
  compatible with every answering seat.

## Findings

F1 (THE PORT; CONVERGENT, newly measured on remote seats). The M1 grammar
flip is filed (watch/inbox/48h_synth/m1_bench.json: gemma:2b unconstrained
0/30 vs format-schema 30/30) but never wired into the dispatch organ:
tools/free_lane_fleet.py:251-268 fire() hardcodes both provider bodies with
no response_format and no ollama format field, and queue_items() :238-248
accepts only {id, prompt} (kind is staged but unused by fire). Arm C proves
the fix's value: same remote seats, door added, mistral 0/4 -> 3/3 and
cohere 0/3 -> 3/3 spec_valid. One-sitting move: read item.get("format") in
the cycle, pass response_format for openai/cohere kinds and format:"json"
for ollama kind, stage comic asks as kind "comic-spec"; rerun arm A's 13
subjects through the queue door as the admission gate. Falsifier: a
post-patch queue-door run under 6/9 spec_valid on mistral+cohere+nvidia
kills the port; any provider starting to 400 on response_format (none did
in 9 answered calls this sitting) narrows it to per-provider rows.

F2 (THE ALPHABET IS ALREADY DRAWN; composes, not builds, the renderer's
hard part). dashboard/static/mag_dance.html:52-67 holds the pose alphabet:
POSES = flail/kick/shimmy/strut/pointy/spirit/stomp, each a 10-float joint
vector [torsoLean, headTilt, shL, elL, shR, elR, hipL, kneeL, hipR, kneeR],
plus POSES.stomp appended at :67; drawSkeleton(pose, jit, zone, heavy) at
:81 renders them; STYLES gives each model a signature (grok: jitter 2.2
overdramatic sweeps; deepseek: 0.6 pragmatic stomps). The comic panel = one
frozen pose per character; the econ arm A prompts already used exactly this
vocabulary and its one in_vocab failure (a09 "shrug") was a word outside
the table, proving the enum must ride the prompt. STYLES is the roll-shape
tie in bytes: a model's comic signature IS its dance fingerprint (ROLL_
SHAPE_TURING_CASTLE_20261007.md: gauntlet register = per-animal shape under
pressure). One-sitting move: port drawSkeleton + POSES to PIL ImageDraw
(lines, ellipses, text) for the PNG face; keep the lerp mix (:117-131) out
of v0. Falsifier: a side-by-side frozen-pose render test; if single poses
read stiff or ambiguous at panel scale, v0 needs the beat_map choreography
contract ({t, strength, downbeat}) driving pose SEQUENCES per panel instead,
which is the maze-imaging register the ask names.

F3 (THE POST ORGAN EXISTS AS A PATTERN, NOT A WIRING). mag/phone_relay.py
is the only discord code and is approval-lane BY LAW (DM-only,
DISCORD_ALLOWED_USERS fail-closed, 12 asks/hour, timeout=DENY, :41-218 all
text-only; live-proven: channel cache state/phone_relay_channel.json and
log rows through 09-28). Broadcasting comics through the approval DM
pollutes the decision surface. The broadcast pattern already exists:
mag/surface_adapters.py:58-59 (slack row: key_env SLACK_WEBHOOK_URL, kind
native, api webhook) + native_call :147-152 (one POST, ok row). One-sitting
move: add a discord_comic row (key_env DISCORD_COMIC_WEBHOOK_URL) + a
discord branch in native_call doing multipart/form-data payload_json +
files[0]=PNG; discord.com REST base already proven from this box. No env
var for it exists today (env name sweep on .env: zero discord/webhook/slack
matches; phone_relay's token lives in the hermes env per :29), so the
operator pastes one webhook URL. Falsifier: if the target server forbids
Manage Webhooks, the door falls back to a bot-token channel post extending
phone_relay's _api with an attachment body; one curl decides.

F4 (THE INPUT ORGAN IS THE TRAIL, ALREADY STRUCTURED). Every probe arm
hand-wrote session summaries; the estate already emits them mechanically:
dashboard/static/trails/day_work.jsonl rows {ts, actor, event, detail,
artifacts} (read this sitting), zknot session recaps, state/CURRENT.md Last
result. One-sitting move: a stager that picks N juiciest detail strings per
day and drops comic-spec queue asks ({id, kind:"comic-spec", format:"json"}),
reusing the fleet's banked-ok dedup for free. Falsifier: sample 20 trail
rows; if fewer than 5 yield comic-worthy subjects (heartbeat noise), the
stager switches source to zknot recaps + state Last-result blocks.

F5 (LANE ECONOMICS, measured; the named model is NOT today's seat). Per
comic at $0: mistral 3.1s, cohere 3.9s, nvidia 4.6s (arm C), local
qwen2.5:3b 6.8s / gemma:2b 5.8s (panel-spec probe), local qwen2.5:7b
9.1s median (arm B, 5/5). The operator's "google model that runs on
nothing" (gemma-4-26b-a4b per accuracy F3) is unscoreable today: :free
429s on openrouter this sitting, local gemma4:latest identity unverified
(OWED: one `ollama show gemma4:latest`). The lane SHIPS on seats already
on the payroll (mistral/cohere through the door at 100% spec_valid; local
qwen2.5:3b 7/8); gemma-4 joins when its door opens. No new spend at any
point. Falsifier: sustained 429s across a 24h openrouter window demote
gemma-4 to future-seat; conversely a verified local gemma4 tag makes it
the free-est seat same-day.

## The one-sitting port move (if only one lands)

F1. It is 10 lines in the organ that already drains the queue, its value
is measured (0/4 -> 3/3, 0/3 -> 3/3 on the same seats), and every later
stage (renderer, webhook, stager) is dead code without spec-valid specs
coming back through the fleet's own door. F2+F3 are the next two sittings.

## CORRECTIONS (post hostile-second-pass, same sitting, both re-verified
with this seat's own instruments before accepting)

C1 (F1 weakened -> corrected attribution; the flip is PROMPT-carried, not
door-carried). The critic's no-door control was reproduced first-hand:
probe_dogfood_control.py (this dir, 9 calls, $0, same JSON panel-spec
prompt as arm C, response_format removed). Results byte-identical to arm C
on spec_valid: mistral 3/3, cohere 3/3, nvidia 1/3. So arm A vs arm C
differed in TWO variables (prompt grammar + door) and the prompt carries
the spec flip. The door's residual value is real but smaller and measured:
(a) CLEAN BYTES: no-door mistral is 3/3 markdown-fenced (json_first_char
0/3) vs 0/3 fenced through the door (arm C raw heads all open with '{');
the banked ledger detail would carry fences every row. (b) LATENCY: mistral
mean 9.4s no-door vs 3.1s doored (3x; nvidia 5.2 vs 4.6; cohere wash 3.7
vs 3.9). (c) The LOCAL hard flip stands (m1_bench.json gemma:2b 0/30 ->
30/30) but is a local-seat fact, not a remote one. DOWNGRADE of the port:
the comics lane ships TODAY through the queue door with ZERO code change
(stage a JSON-spec prompt ask; arm A proved the queue carries arbitrary
prompts); the ~10-line format passthrough is fleet insurance (unfenced
banked bytes + mistral latency + local grammar), not the enabler. Falsifier
denominator corrected: arm A's 13 subjects put 11 on door-capable remote
providers (mistral 4, cohere 3, nvidia 4); the post-patch admission rerun
must score >=6/11 spec_valid to confirm prompt transfer through the organ,
and the door's residual must hold (0 fenced mistral rows; mean secs under
half the no-door mean) or the passthrough drops to per-seat rows.

C2 (F4 weakened -> withdrawn as stated, organ swapped). The critic's
falsifier execution was reproduced first-hand: day_work.jsonl (this
sitting, my command) reads 2587 rows; last 20 = 13 CYCLE + 7 HEARTBEAT +
0 narrative; last 200 = 100% day_work-cage (134 CYCLE / 63 HEARTBEAT / 3
SCHEDULER_UP); whole file 2585/2587 single-actor. Under my own
fewer-than-5-of-20 rule the trail fails. The sibling trails fail too
(surveyed this sitting): builder.jsonl non-noise rows are EXC OSError stack
traces, research.jsonl MONITOR rows are rc counters, night.jsonl CYCLE_FAIL
rows are the same OSError. The trails organ is scheduler telemetry, not
session narrative. CORRECTED primary input organ: memory/zknot session
recaps (operator-voice prompt digests, e.g. memory/zknot/
2026-10-06_sess_7318df04-6115-449d-b554-2f93d5ee2a6e.md "His prompts"
block: "Do it couple hours till morning design some workflows we need to
burn a couple hundred million") + state/CURRENT.md:63-72 Last-result
narrative + watch/inbox receipt titles. Cite correction: the fleet work
sources are tools/free_lane_fleet.py:13-21, not the :29-33 I wrote (that
range is the SSRF law text).

## Blind spots

- I did NOT patch tools/free_lane_fleet.py (gated organ; lens seats
  specify, the build phase lands). The port is specified with line cites,
  not landed.
- gala and MCP-bridge organs not deeply mapped; no comic-relevant bytes
  surfaced in my budget, and I name that as unsearched-in-depth, not absent.
- The voxel tie stays at SUBJECT level (arm A a12 drew the mountain as a
  joke); I found no voxel renderer organ under mag/+tools/ to compose with
  (voxel hits are corpus/docs), so the ask's "ties into our voxel rendering
  system" has no byte-level organ I can point to. OWED: the game seats'
  mountain renderer location.
- Discord webhook multipart post not fired live (no webhook URL exists;
  operator paste gate). The 429 wall on gemma-4 :free is a moment reading,
  not a 24h average.
- arm C is n=3 per seat; the admission rerun (post-patch, n=13 through the
  queue door) is the powered version.
- Sibling lenses' claims (accuracy.md F1-F5, econ arms A/B) are cited as
  their receipts, re-read but not re-executed by me beyond what I fired.
