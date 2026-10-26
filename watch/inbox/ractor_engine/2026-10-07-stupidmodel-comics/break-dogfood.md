# break-dogfood: hostile second pass on the dogfood lens (stupid-model comics lane)

Date: 2026-10-07. Seat: break-dogfood. Law: never edit, only fire and cite.
No em-dashes. Every claim below is something I read or ran this sitting. Artifacts
this pass fired (all $0, free lanes, urllib only, zero subprocess spawns so the
win32 CREATE_NO_WINDOW law holds by construction):

- break_dogfood_armc_rerun.py + break_dogfood_armc_rerun_results.json (12 calls:
  the lens's arm C re-fired, output to a NEW path, lens artifact untouched)
- break_dogfood_nodoor.py + break_dogfood_nodoor_results.json (12 calls: the
  confound control, arm C prompt byte-identical, response_format REMOVED)

## Verdicts

### F1 (grammar door filed, never wired; "adding it flips remote free seats 0% to 100%"): WEAKENED

Byte-checks that PASSED (all evidence cites intact):

- tools/free_lane_fleet.py fire() :251-268: bodies hardcoded, no response_format,
  no ollama format. Stronger than the lens's cite: I grepped the whole 400-line
  file, the only queue-field read is item.get("id") and item.get("prompt") at
  :244, and the strings response_format/format appear NOWHERE in the file. The
  "filed but never wired" claim and the "not patched" blind spot are both
  byte-true.
- queue_items() :238-248 confirmed; the cycle consumer :310-312 pops id+prompt
  only, so a format field staged today would be silently dropped.
- watch/inbox/48h_synth/m1_bench.json byte-true: gemma:2b, 30 prompts,
  unconstrained_valid 0/30, format_schema_valid 30/30. Provenance traced to
  commit 0e4ef3c95; the pre-registration card is watch/inbox/48h_synth/steals.md
  :29-44 (LOCAL ollama format=schema, GBNF class, a HARD grammar, mechanically
  different from remote response_format json_object).
- econ_probe_results_arm_a.json byte-true: 13 fired, 2 PASS (a08 nvidia, a10
  qwen2.5:7b); mistral 0/4, cohere 0/3.
- probe_dogfood_arm_c_results.json byte-true and REPRODUCED: my rerun (12 calls)
  got mistral 3/3 spec_valid (3.3s mean), cohere 3/3 (4.1s), nvidia 3 parses +
  2/3 spec, gemma4 HTTP 429 x3. Zero HTTP 400s anywhere. The lens's numbers are
  honest.

The kill: the FLIP ATTRIBUTION is false. Arm A (0%) used the LINE-grammar
prompt; arm C (100%) used a JSON-spec prompt PLUS the door: two variables moved.
My control holds the prompt byte-identical to arm C and removes only
response_format: mistral 3/3 spec_valid, cohere 3/3 spec_valid, nvidia 1/3
(same empty-caption failures), gemma4 429 x3. IDENTICAL outcomes without the
door (break_dogfood_nodoor_results.json). The arm A to arm C delta is carried
by the PROMPT, not the door. The lens's falsifier ("post-patch queue-door rerun
under 6/9 kills the port") can never fire on a no-door run either, because the
door is not the operative variable on these seats.

What survives: the port is still ~10 lines of cheap insurance for fleet-wide
traffic (M1's local gemma:2b 0/30 shows the format family matters for the
weakest seat), and the door does buy a clean envelope: my no-door mistral raw
heads come back wrapped in ```json fences (rescued only by the scorer's regex
fallback at probe_dogfood_arm_c.py:127-133), while the door arm returns bare
JSON. That is parser robustness, not validity. Minor internal tension the lens
should fix: the falsifier says "rerun of arm A's 13 subjects" but scores
"under 6/9"; 13 subjects on those three providers is /11.

### F2 (POSES + drawSkeleton + STYLES is the stick-figure alphabet organ): CONFIRMED

Every cite byte-exact: dashboard/static/mag_dance.html :52-59 POSES (6 poses,
10-float vectors, legend comment at :51), POSES.stomp appended at :67 (7 total),
STYLES :61-66 (grok jitter 2.2 "overdramatic sweeps", deepseek 0.6 "pragmatic
stomps", exact), drawSkeleton at :81, lerp mix :117-131. The vocabulary claim is
byte-true: probe_comics_arm_a.py:27 POSES = {flail, kick, shimmy, strut, pointy,
spirit, stomp} and :53 puts the enum in the prompt; econ a09's in_vocab failure
is exactly "shrug" (econ_probe_results_arm_a.json, poses [pointy, shrug],
fail_reason [in_vocab]). watch/inbox/ROLL_SHAPE_TURING_CASTLE_20261007.md exists
(6993 bytes, Oct 7) and carries the per-animal roll-shape frame. One cost
undercount, not an evidence defect: drawSkeleton renders ONE centered figure;
multi-figure panels, bubbles, and captions are new code, so "40 lines of JS"
measures the port of one skeleton, not a panel.

### F3 (discord post organ exists as a pattern, not a wiring): CONFIRMED

Content all byte-true with two line-drifts: the law block is :5-13 (cited
:10-20; timeout=DENY :7, DM-only :8, 12/hour :11 and :54), and HERMES_ENV is
:32 (cited :29). Function census verified: every post in mag/phone_relay.py is a
JSON {"content": ...} body (_api :87-103, ask :162-215, test :218-229), so
text-only and approval-only is correct. mag/surface_adapters.py :58-59 slack row
(key_env SLACK_WEBHOOK_URL, api webhook) exact; native_call slack branch
:144-156 with the webhook POST at :149-152. I REPRODUCED the env sweep: 56 var
names in .env, ZERO matching discord/webhook/slack (names only, no values
read out), DISCORD_BOT_TOKEN absent from the repo .env (it lives in the hermes
env per phone_relay.py:32,:64-73). state/phone_relay_channel.json mtime Sep 26;
watch/inbox/phone_relay_log.jsonl last rows 2026-09-28 with real msg_ids, which
is the live proof that the discord.com REST base works from this box
(phone_relay.py:34-36 records why discord.com, not api.discord.com).

### F4 (the comic lane's input organ is the trail stream): WEAKENED

The row-shape claim is byte-true: dashboard/static/trails/day_work.jsonl rows
are {ts, actor, event, detail, artifacts}. But I EXECUTED the lens's own
pre-registered, never-fired falsifier ("sample 20 trail rows; if fewer than 5
yield comic-worthy subjects, switch source"): last 20 rows = 14 CYCLE + 6
HEARTBEAT + ZERO narrative rows; the last 200 rows are 100% actor day_work-cage
(134 CYCLE, 62 HEARTBEAT, 4 SCHEDULER_UP); the whole 2583-row file is 2581
day_work-cage + 1 zcode-manager + 1 flash-drive-seat. The switch condition
FIRES on the bytes: the trail is a single-actor scheduler log this sitting, not
a session-narrative stream. The lens even read these rows (its organ-map row
says "day_work-cage CYCLE/HEARTBEAT rows") yet still ranked the trail as the
primary source with the noise caveat buried in the falsifier. By the lens's own
rule the primary source must be zknot recaps + state/CURRENT.md Last-result
blocks, with the trail as a fallback. Also note the finding's move cites
free_lane_fleet.py:29-33 for the work sources; the actual work-source block is
:14-22 (:29-33 is the laws tail + usage), content correct, cite drifted.

### F5 (lane economics; the named model is not today's seat): CONFIRMED

All cited numbers reproduce from the receipts: econ_probe_results_arm_b.json
qwen2.5:7b 5/5 pass, median_ms 9139 (=9.1s); probe_panel_spec_results.json
qwen2.5:3b format_json 7/8 spec_valid, mean 6.8s; gemma:2b format_json 5.8s
mean (5/8 spec_valid, and note its UNCONSTRAINED arm was 6/8, a local no-flip
data point consistent with my F1 control); arm C means 3.1/3.9/4.6s. The gemma-4
:free 429 wall now persists across THREE independent firings today (lens arm C
15:23Z, my rerun, my control), which strengthens "wall" past a single moment
but is still not the 24h window the lens names. The OWED ollama show
gemma4:latest identity check remains unrun (I did not run it either; local
ollama was not queried this pass).

## Blind-spot audit

- "No byte-level voxel renderer organ found under mag/+tools/ (voxel hits are
  corpus/docs)": HALF FALSE. No renderer under mag/+tools/ is true, but the
  hits are NOT corpus/docs: git grep -li voxel over mag+tools returns
  mag/lattice_distance.py (validate_voxel_coords :94, Z^3 invariant on voxel
  grids), mag/perturbation_battery.py (p2_voxels :166), mag/volume_fidelity.py,
  plus toolchain binaries. And the lens's OWED ("game seats' mountain renderer
  location") is answerable from volume_fidelity.py's own header: the voxel
  carve is dashboard/static/shadow_walk.html :63-156 (fnv1a32 + mulberry32 +
  BFS leak field + carve), line-faithfully ported into mag/volume_fidelity.py.
  The lens grepped the wrong subtree; the organ is in dashboard/static, the
  same subtree as its own F2 organ.
- "gala and MCP-bridge not deeply searched": quick census this pass, git grep
  -li "comic|xkcd|stickfig|stick figure|stick-figure" over mag+tools returns 4
  files, all binaries or data (rojo.exe, Godot exe, llama-vulkan.zip,
  pain_replication sadness dataset): no missed comic code organ in that scope.
- "free_lane_fleet not patched": confirmed by whole-file grep (zero
  response_format/format strings).
- "discord webhook not fired live": still true; my env sweep confirms no
  webhook URL exists on the box to fire it with.

## Additions (what the lens missed)

1. THE CONFOUND CONTROL (sharpest): the comic lane's admission numbers hold
   WITHOUT the door. Same JSON panel-spec prompt, response_format removed:
   mistral 3/3, cohere 3/3 spec_valid. Evidence:
   break_dogfood_nodoor_results.json vs break_dogfood_armc_rerun_results.json
   and probe_dogfood_arm_c_results.json. Falsifier: no-door rerun at n=8 per
   seat; if mistral/cohere hold at 7/8 or better (my prediction: they do), the
   port drops OUT of the comic lane's critical path and stays as fleet
   insurance only. Move: 15 min (the control script already exists; widen
   PROMPTS and rerun).
2. THE VOXEL ORGAN ANSWERED: dashboard/static/shadow_walk.html:63-156 is the
   estate's voxel renderer (seeded carve, BFS corridors, fnv1a32 ladder),
   ported line-faithfully into mag/volume_fidelity.py for gauntlet grading.
   The mountain tie composes: a comic panel can silhouette the SAME seeded
   carve the game digs, one deterministic function, two faces. Evidence:
   mag/volume_fidelity.py header (this sitting). Falsifier: a second carve()
   implementation elsewhere (git grep "def carve" across the tree finds the
   authoritative site; if shadow_walk is a copy of a mag/ original, cite that
   instead). Move: 10 min grep + one render test drawing a panel background
   from the carve heightmap.
3. F4's SWITCH IS MANDATORY, NOT OPTIONAL: executed this sitting, 0 of the
   last 20 trail rows are comic-worthy by the lens's own standard; the stager's
   primary source is zknot recaps + state Last-result blocks TODAY. Evidence:
   the day_work census numbers above. Falsifier: a future trail where non-cage
   actors reappear (watch actor distribution; if day_work-cage falls under 50%
   of a 200-row window, the trail re-qualifies). Move: 0 min (change the
   stager's source order when built).
4. THE DOOR'S REAL REMOTE VALUE IS THE ENVELOPE: without response_format,
   mistral wraps output in ```json fences (raw heads in
   break_dogfood_nodoor_results.json); the scorer's regex fallback rescued
   them. A naive downstream parser (the future fleet path) would choke. The
   honest F1 rewrite is "the door buys clean top-level JSON on chatty seats
   and hard guarantees on the weakest local seat (M1), not validity on the
   remote comic seats." Falsifier: a seat that emits fences AND fails the
   regex rescue at n=8. Move: fold into addition 1's rerun, same 15 min.
5. NVIDIA's EMPTY-CAPTION FAILURE IS STABLE ACROSS ALL THREE ARMS (lens door
   1/3, my door rerun 2/3, my no-door 1/3; every failure is an empty caption
   string, never a parse break). It is model-side, so the typed-schema cure
   (minLength on caption) or renderer-side default is the right fix and the
   door will not cure it. Evidence: caption "" in raw heads of all three
   results files. Falsifier: a nvidia run at n=8 where empty captions vanish
   with the door on (would contradict my no-door equivalence). Move: 5 min,
   add minLength to the staged spec when the queue lands.

## Bottom line for the fold

The organ map survives (F2, F3 fully; F5 numbers honest). The load-bearing
correction is causal, not factual: everything the lens measured is real, but
the thing that makes remote free seats emit valid comic specs is the JSON
panel-spec PROMPT, which costs zero lines of fleet patching. Land the prompt as
the lane's spec door, keep the F1 port as separate fleet insurance, pull comic
subjects from zknot/state (not the trail), and draw the mountain with
shadow_walk's own carve.
