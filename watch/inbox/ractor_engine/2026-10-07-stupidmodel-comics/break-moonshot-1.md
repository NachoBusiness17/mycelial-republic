# BREAK PASS: moonshot-1 (stupid-model comics lane, ractor 2026-10-07)

Seat: break-moonshot-1 (hostile second pass). Every byte below was read or
run this sitting. No em-dash. Artifacts banked beside this file:
break_moonshot_power50.py, break_moonshot_power50_results.json (150 calls,
3 seats x 50 prompts, local ollama, $0.00, fired 2026-10-07 ~17:55-18:32Z).

Meta-note before the verdicts: the ask copy I received truncated the lens's
finding M4 mid-evidence (cut at "bones_adapter MAX_MESSAGE 1"), the same
relay disease M4 itself documents (ractor-topic/break-communication.md:237-
243: "the ask's findings array truncated finding 4 mid-sentence"). Third
observed instance. The full M4 was byte-checked from moonshot-1.md:101-123.

## THE EXECUTED FALSIFIER ATTACK: the n=50 power run

M2's own falsifier ("if gemma4 regresses below gemma:2b at n=50 the ranking
flips") and accuracy F1's owed admission gate, fired by this seat. Same door,
same wrapper prompt, same grader as the lens's probe (score_json imported
from probe_moonshot_gemma4.py, not rewritten); 50 NEW session-summary
prompts (zero reuse from any sibling probe); temperature 0.3, num_predict
400, body["format"]="json". Full raws persisted this time (the lens banked
only 120-char heads). Results (break_moonshot_power50_results.json summary):

| seat | parses | spec_valid | mean | pose key present | pose value in-vocab |
|---|---|---|---|---|---|
| gemma4:latest | 50/50 | 40/50 (80 pct) | 30.8s | 154/154 (100 pct) | 0/154 (0 pct) |
| qwen2.5:3b-instruct | 50/50 | 48/50 (96 pct) | 5.5s | 176/176 (100 pct) | 0/176 (0 pct) |
| gemma:2b | 50/50 | 7/50 (14 pct) | 4.4s | 146/146 (100 pct) | 0/146 (0 pct |

Two laws fall out:

1. THE RANKING SURVIVES AND SHARPENS. The falsifier condition (gemma4 below
   gemma:2b) did not fire: 40/50 vs 7/50. qwen2.5:3b-instruct stays first
   (96 pct at 5.5s), gemma4 second (80 pct), gemma:2b COLLAPSES at scale:
   the lens's n=8 "gemma:2b 6/8" (itself a corrected-cell number; the banked
   probe_panel_spec_results.json reads 5/8 as-run) was small-n luck. Its 43
   failures: 24 bubble-shape violations, 18 panel-count violations (1-2
   panels), 1 caption-length. gemma4's 10 failures: 8 caption-length
   (13-18 words vs the 12-word bar, the same disease economics arm B cured
   with a deterministic trim), 1 panel-count, 1 bubble-shape.
2. THE POSE-VOCABULARY LAW (universal, scoped: this sitting, 50
   prompts/seat, temp 0.3, generic format:json door): the pose KEY is
   present on 100 percent of panels (476/476 across all three seats) and
   the pose VALUE is in the dance vocabulary on 0 percent (0/476). No seat
   drops the key; every seat escapes the vocabulary. gemma4 writes full
   descriptive scene sentences as pose values ("patrol officer stands next
   to a visibly distressed census, who is slumped over a clipboard.");
   gemma:2b writes single drifting words ("sitting" x16, "standing" x13,
   "none" x8); qwen2.5:3b writes short stage directions ("thinking" x5,
   "smiling" x4). Vocabulary control belongs to the ENUM alone.

Latency correction: gemma4's mean at n=50 is 30.8s, not the lens's 12.3s
(its descriptive pose sentences inflate generation; same box, later moment).
The qwen-first decision strengthens: the gap is ~5.6x, not 1.8x.

## VERDICTS (per finding, byte-checked)

M1 (the comic is the light maze's third render face; register rows are panel
facts): CONFIRMED. Every cite byte-true: POSES at mag_dance.html:52-59 with
POSES.stomp added at :67 (7 poses, 10-float layout comment at :51),
drawSkeleton at :81, STYLES at :61-66 (the lens said :64-70, cite drift,
content true), volume_fidelity.py:1-38 (9,305 parts, GXxGZ, port note
naming shadow_walk.html lines 63-156 at :36-38), register re-censused by me
untruncated: 16 rows, families beat 8 / consensus 4 / dice 2 / metagame 2,
ZERO comic rows (quantifier law honored), keys ts/work_id/family/provider/
model/verdict/note/expensive_ref, the ROLL_SHAPE quote at receipt lines
108-110 (inside the lens's cited :107-111; economics corrected the
off-by-one to :108-110), game_entry.py:154-188 svg() exists as claimed.
CONDITION DROPPED (not fatal): register rows carry NO pose or panel fields
and STYLES names four dancers (saelis/grok/chatgpt/deepseek) none of which
match the register's model names (open-mistral-nemo, command-r7b-12-2024,
llama-3.2-11b-vision-instruct, qwen2.5:7b); the "zero model calls" face
owes a deterministic row-to-pose/panel mapping table that is a build
artifact, and "every register row IS a panel fact" is a design assertion
whose falsifier (10-row pure-telemetry render) remains unfired by any seat
including this one.

M2 (the named seat is already on the payroll and holds the lane): CONFIRMED.
All seven metadata fields re-verified by my own live calls this sitting:
curl /api/show gemma4:latest -> general.architecture gemma4,
general.parameter_count 7996157674, gemma4.vision.block_count 16,
gemma4.audio.block_count 12, gemma4.block_count 42, gemma4.context_length
131072, Apache-2.0 license text; /api/tags size 9,608,350,718 (9608 MB);
gemma4:latest and qwen2.5:3b-instruct both present ("already pulled" true);
AGENTS.md header "gemma4 short worker" confirmed. Probe numbers byte-match
probe_moonshot_gemma4_results.json exactly (8/8 parses, 7/8 spec_valid,
12.3s; 4/8, 0/8, 3 empty rows 1/6/7, keyword-drop rows 0/5, near-miss rows
2/3/4). The n=50 falsifier fired by me does NOT flip the ranking (above).
WEAKENING NOTES, none fatal: (a) "three probes now agreeing" overstates:
economics arm B tested qwen2.5:7b (5/5), agreeing on the DOOR, not on this
hierarchy whose qwen is the 3b; (b) the hierarchy's "gemma:2b 6/8" is the
corrected-cell figure, banked JSON says 5/8 (accuracy disclosed; at n=50 it
is 7/50, so the correction is now moot); (c) the optional 15-min openrouter
move ("config row only") is DEAD as written: accuracy.md's hostile
CORRECTION (landed 13:18, AFTER moonshot-1.md's 11:41 write) shows both
openrouter providers health-fenced dark (consecutive_fails 6 and 5, skipped
at fails>=5, tools/free_lane_fleet.py:306-308), so the config row would
silently never fire; the move needs the live curl + health reset first;
(d) the GAUNTLET_FREE cite is :32-33, not :33-37 (content true).

M3 (the line-grammar door is dead; only the typed schema ships): CONFIRMED
ON THE VERDICT, MECHANISM KILLED. The 0/8 with three failure shapes is
byte-true in the rows; economics arm A 2/13 and arm B 10/10 json_ok with
10/10 in-vocab are byte-true; the arm B schema (pose enum + required keys)
verified by my read of probe_comics_arm_b.py:20-45. KILLED: the mechanism
claim "generic format:json -> gemma4 DROPPED the pose key on 8/8 rows"
(moonshot-1.md:90-91). My full-raw n=50 shows the pose key present on
476/476 panels (100 percent, all three seats); nothing drops it. The lens
over-read its own 120-char-truncated telemetry (its raw_head row 5 even
shows a pose key). The correct law: the key is always present, the VALUE is
never in vocabulary (0/476). Consequence for the move: the required-key
clause is redundant for pose; the ENUM is the sole load-bearing constraint
(the move's wording "enum poses + required keys" stays safe, but the
required clause should not be credited with the vocabulary lock). ALSO: the
M3 falsifier ("stage line-grammar twins on mistral/cohere through the
queue") was ALREADY FIRED by economics arm A (mistral 0/4, cohere 0/3,
total 2/13, far under 50 percent): the line door is dead on the API seats
too, not just the local seat. The lens presented an already-settled
falsifier as open while citing the very probe that settled it.

M4 (the DAWN REPORT as the 10x product face): WEAKENED, one byte error, the
structure stands. Verified: bones_adapter.py:66 MAX_MESSAGE = 1900 (exact),
fmt_block truncation :99-105; phone_relay.py:165/168/177 prompt[:200]
(exact) and the JSON-only door at :93-95; 403-locked since 09-15 and DM
lane dead 9 days stand on communication F3/F2 (internally consistent: 22
days / 9 days from 09-28); the ask-truncation incident is byte-real at
ractor-topic/break-communication.md:237-243 and reproduced again in THIS
ask; economics E5's ~2-3h + ~9s pricing byte-true. THE ERROR: the DAWN LIST
is 11 numbered items, not 9 (awk census, watch/inbox/DAWN_REPORT_20261006.md
lines 70-127, "THE DAWN LIST (needs your signature)" heading at :68). A
product-face finding whose input list is miscounted by 2 must be re-counted
before the spec input adapter is wired; the finding's relay-law core
(size-bounded, caption-carries-content, dashboard-first) is unaffected.

M5 (one pose-vector interface, three deterministic faces): CONFIRMED.
BASECAMP B0 "Mountain slice ... DONE 2026-09-29" at docs/ref/
GAME_PLATFORM_BASECAMP.md:17; mag/worldgen.py (42,545 bytes) and
mag/river.py (16,116 bytes) exist; probe row 6 (hydrology prompt) spec_valid
true in the lens's banked JSON; the SVG-as-Discord-payload kills are real in
accuracy F4 + operations F4 (both read by me); the cmx.js steal is honestly
attributed to accuracy F5 (not re-verified by this seat, not re-verified by
the lens, correctly marked). The joint-angle-to-voxel extrusion falsifier
stays unfired; the lens itself scopes extrusion as an owed door, not v1.

## BLIND-SPOT CHECKS (the lens's honesty audit)

- "imaging-turing frame (sess_7318df04 msg 346) remains unsourced": the lens
  was right to stand on the receipt bytes, and the pointer is now RESOLVED
  by this seat via a read-only sqlite probe of the session DB
  (~/.zcode/cli/db/db.sqlite, message table, sequence 346): msg 346 is the
  operator at 2026-10-07T13:54:04Z ordering "we need an electron app, a
  terminal script that installs this into whatever cli. im trying to attend
  a hermes conerence in nyc on the 30th maybe we start there." NOT the
  imaging-turing frame. The frame's actual homes: seq 343 (operator: "this
  is our light maze."), seq 345 (assistant synthesis: "the environment that
  makes minds legible by how they walk it"), and ROLL_SHAPE receipt
  :108-110 ("The maze does not teach the model - it images it..."). The
  ractor ask's msg-346 pointer was wrong; no flat file carries "msg 346"
  (git grep zero rows, confirmed). Side catch: the operator's real msg 346
  is adjacent comics-lane context (the electron-app lineage the order
  mentions: "i played with something like that using electron apps").
- "no live openrouter/nvidia calls fired": still true for this seat too; and
  now known worse (accuracy correction): the openrouter lane is fenced dark.
- "wit unscored by every probe": still true after my run (my grader also
  measures form only).
- "gauntlet comic family unstaged in the free-lane queue": confirmed, the
  queue directory is empty (0 files) this sitting.
- Census note spot-check: tree-wide git grep -l -i counts re-derived
  exactly for 2 of the lens's 4 terms (comic 194, mermaid 215); voxel and
  electron not re-counted by this seat.

## INSTRUMENT DEFECT CARRIED FORWARD (does not affect the lens's banked
claims)

score_json (probe_moonshot_gemma4.py:90-105, reused by my run) initializes
pose_ok True and only falsifies it inside the panel loop; rows that fail
before the loop (panels not a list, count violation short-circuiting) keep
a spurious poses_ok=True (my telemetry flags 18 such gemma:2b rows as
rows_poses_ok=18 while their actual in-vocab count is 0). Harmless to the
lens's format_json rows (all parsed with panels), but grade_comic() in the
gauntlet build must initialize pose_ok False or gate it on the loop having
run.

## WHAT THE LENS MISSED (the additions, priced)

1. The n=50 gate is CLOSED (fired by this seat, above): the ranking holds,
   gemma:2b demotes to distant third at 14 pct, and the caption-trim cure
   economics named is now gemma4's dominant failure mode too (8 of 10
   fails). Move: 0 min, the numbers are banked; the dogfood build proceeds
   on qwen-default + gemma4-fallback as decided.
2. The pose law (key 100 pct present, value 0 pct in-vocab, all seats,
   generic door): the schema constant must carry the enum as the ONLY
   vocabulary mechanism; drop any belief that required-keys or prompt
   wording can hold poses. Falsifier: a typed-schema run at n=50 showing
   in-vocab below 100 pct (economics arm B measured 10/10 at n=10; the
   power-scale typed run is now the only owed probe).
3. msg 346 resolved (above): no estate surface owes the imaging-turing
   frame a source anymore; M1's receipt cite is the canonical one.
4. The line door is dead EVERYWHERE measured (local 0/8, queue API 2/13);
   operations' staged-twin falsifier and the lens's restaging clause are
   both moot. Move: strike the line grammar from v1 permanently, as the
   lens's move already says, now with the API-side numbers attached.
5. The openrouter gemma-4-26b-a4b seat addition requires the health reset +
   live curl first (accuracy's correction); the 15-min config-row-only move
   as written would silently never fire.
6. The DAWN input adapter must be pointed at an 11-item list (or the list
   recounted at render time), never a hardcoded 9.

## Sources (commands run this sitting)

curl /api/tags + /api/show (gemma4 metadata, live); sqlite read-only probes
of ~/.zcode/cli/db/db.sqlite (session 7318df04, sequences 343-347, part
table); .venv/Scripts/python.exe break_moonshot_power50.py (150 calls,
$0.00, results JSON banked); git grep -l -i censuses (comic 194, mermaid
215, tree-wide); awk DAWN LIST count (11); reads: moonshot-1.md,
accuracy.md, economics.md, operations.md, communication.md,
probe_moonshot_gemma4.py + results, probe_panel_spec_results.json,
probe_comics_arm_b.py, GAUNTLET_REGISTER.jsonl (full), ROLL_SHAPE receipt
:95-130, DAWN_REPORT_20261006.md (head + list),
mag_dance.html:40-109, mag/game_entry.py:140-199, mag/volume_fidelity.py:1-
40, mag/bones_adapter.py:55-109, mag/phone_relay.py:88-101 + 158-182,
GAME_PLATFORM_BASECAMP.md (grep), GAUNTLET_FREE_LANDED_20261006.md:28-42,
ractor-topic/break-communication.md:237-243, free_lane_queue ls (empty).
