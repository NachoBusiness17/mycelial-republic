# MOONSHOT LENS - parked decisions 2026-10-04 (D3 thinking posture + dungeon.py debt)

Lens: moonshot (no sacred cows, the 10x version or the honest reason it is
not the move). Every claim below was read or run THIS sitting, cited
path:line or command:output. No em-dashes. Anything I could not verify is
marked OWED. Derivation order on record: all findings marked MINE below were
in hand BEFORE I opened the sibling lens files (communication.md,
economics.md); my read order is visible in the session tool calls. Findings
independently re-derived from a sibling are flagged CONVERGENT and the
sibling named.

## The one-line resolution of both decisions

D3 and D2 are the same decision wearing two coats: the estate's model-call
posture must live in ONE place (the depth layer of the front door), and
every carrier that predates it is carrying a fork of the OLD law. D3's
winner: depth-gated, wire-explicit, OFF by default for mechanical. D2's
winner: accept the debt standing on the file split; the real debt is the
call path, not the line count.

## D3 VERDICT: depth-gated, wire-explicit, unconditional OFF for depth=mechanical; the design arm gets the capability gate mechanical never gave it

Verdict, one sentence: depth=mechanical sends thinking:{type:disabled}
unconditionally on the wire (flip mag/route_chat.py:204 from
`lane_cfg.get("disable_thinking") and depth == "mechanical"` to
`depth == "mechanical"` behind a ~$0.001 capability probe), depth=design
sends thinking:{type:enabled} ONLY on lanes whose config declares the
capability (route_chat.py:212-213 is currently UNGATED), and lane-config
gating is demoted from law to capability cache.

Why lane-config-gating loses (MINE, the census neither sibling ran to this
conclusion): providers.yaml carries disable_thinking on exactly 3 lanes
(:223 openrouter, :371 deepseek, :401 deepseek_overmind; my grep census this
sitting). But the d4-measured think-by-default MODEL is the default model on
FIVE lanes, and two of them carry no flag:

- vast: default_model deepseek-v4-flash (configs/providers.yaml:434), no
  disable_thinking in the block (:416-450). Under lane-gating, route_chat
  mechanical on vast rides omission = measured ON (d4 probe arm 1,
  d4_thinking_probe.md:55). vast is in the scut and hard_code/hard_reason
  chains (providers.yaml:836, :839-840), so it is reachable, not decorative.
- together: default_model deepseek-ai/DeepSeek-V4-Flash-0731
  (configs/providers.yaml:528), no flag in the block (:521-535). Same hole.
- openrouter: the flag is present but the lane's own comment says
  openrouter/auto "IGNORES thinking:{type:disabled} - it thinks anyway and
  eats small budgets (600 -> empty, 2000 -> content). The real fix is a
  bigger budget per lane" (configs/providers.yaml:219-222). So NO wire
  posture defends the router lane; only budget does. This kills the fantasy
  that any single posture is sufficient: the wire law needs the budget law
  riding shotgun, exactly as the route_chat docstring already says
  (mag/route_chat.py:133-136: "reasoning burns max_tokens; design asks need
  32K+ or a smaller ask").

Why unconditional-off is still the right default despite the openrouter
limit: the OFF arm is recoverable (a lane that ignores the key loses
nothing; a lane that rejects it 400s loudly, which the probe catches for
$0.001), while the omission arm fails silently (the d4 finding itself:
d4_thinking_probe.md:5-13). Silent failure modes cannot be defaults on a
front door whose own docstring sells fail-loud (mag/route_chat.py:21).

The design arm is the half-law (MINE, neither sibling caught it): a06#3
flagged "depth='design' sends thinking:{type:enabled} to EVERY lane though
the docstring says 'where the lane supports it'"
(memory/runs/mickey17_v2/runs/run-0/lanes/a06-sacred-cow.json, key
ee225394e567), and the landed wiring still does exactly that
(mag/route_chat.py:212-213, no capability condition). PRIORS row 15 has a
lane rejecting vendor reasoning params with HTTP 400
(watch/inbox/model_garden/PRIORS.md, row 15: qwen3.7-flash "rejects the
reasoning param outright (HTTP 400, fires without)"). A gate on one arm and
not the other is not a law, it is a mood. The verdict therefore pairs the
mechanical flip with a design gate in the same sitting.

The founding row pair, byte-read this sitting
(memory/runs/hermes_burn/usage.jsonl:1151-1152): 1151 =
GALA_DD_SELFSTEAL_PRIME_JUDGMENT_20261003, z-ai/glm-5.3-prime,
completion 16000, reasoning 15998, finish length, content_chars 1,
cost $0.2502604; 1152 = the STAGE_B re-fire, completion 14759, reasoning
9826, finish stop, channel content, cost $0.2137336. The pair is the whole
D3 argument in two bytes: the same judgment, same posture, hollowed at 16K
and delivered at 30K. Judgment asks do not need thinking OFF; they need
budget sized to it. Mechanical asks need OFF because their budget is the
point. That is depth-gating, and it is what the landed enum already encodes;
the fix is the gate form, not the posture.

Falsifier (what flips the verdict): (1) a funded lane measured 400-ing on
thinking:{type:disabled} where omission was clean - the unconditional form
retreats to probe-written capability cache, off-default preserved; (2) a
judged equal-budget A/B on a mechanical shape where ON beats OFF on the
register rubric - the default flips. Honest basis note (CONVERGENT with
communication.md:15 and economics.md:103-120, both derived from d4
consequence 1, which I also derived independently from the file bytes):
there is NO thinking-OFF quality score anywhere in the estate; every ds
batch through 2026-10-04 06:11Z rode ON by omission (ds_workhorse.py's
explicit key landed after the v3 refire; the erratum comment in
tools/ds_workhorse.py:85-97 cites the d4 receipt as its evidence). The OFF
default rests on the ON failure class (usage.jsonl:1151; a06#0's 2/10
zero-content arm-2 rows; PRIORS row 8's zero content at 4500/8000/16000)
plus cost asymmetry (d4 table: 21 vs 2 completion tokens). That is a
sufficient standard for mechanical and it must be WRITTEN as that, never as
if a quality A/B existed.

### Amendment text for the losing law surfaces

Surface 1, watch/inbox/model_garden/PRIORS.md row 8 (the a06-sacred-cow#2
surface; append-only, the row is cited not edited, per the append-never-
rewrite law d4_thinking_probe.md:73-74):

> POST-DATUM 2026-10-04 (ractor D3; d4_thinking_probe.md + usage.jsonl:1151-
> 1152): row 8's mechanism is confirmed cross-vendor (reasoning eats
> max_tokens; hollow at cap) and its scope is now RULED: THINKING OFF is the
> sent default for depth=mechanical, wire-explicit (omission is not off, d4
> 3-arm probe), budget-explicit for depth=design (thinking-ON judgment asks
> succeed at 32K+ tokens: usage.jsonl:1152 finish stop after :1151 hollowed
> at 16K). "Never refire thinking-on" reads as: never refire thinking-on
> UNBUDGETED. Falsifier: a judged equal-budget mechanical A/B where ON beats
> OFF flips the default.

Surface 2, queue/STANDING_RAILS.md law 1 (the per-lane-call-laws clause
loses to the depth clause; CONVERGENT with economics.md:69-85 who drafted
the same amendment shape):

> 1. Default to the rails. A bespoke model-call path requires a written
> reason in its docstring. The front door is mag.route_chat (lane + goal;
> dormant gate; endpoint fence; depth-gated thinking: depth=mechanical sends
> thinking:{type:disabled} on the wire for every lane that accepts the key -
> omission is not the off state (d4 probe 2026-10-04,
> watch/inbox/go_wave_20261004/d4_thinking_probe.md); depth=design is the
> only ON path, capability-gated per lane, budgets 32K+; openrouter-class
> router lanes that ignore the key are defended by budget, not by the wire;
> usage banked).

Surface 3 and 4 are CODE, and they are the part the two named surfaces hid
(see next finding).

## The refuted law is not just unamended, it is pinned GREEN by this wave's own tests (MINE, neither sibling caught it)

Two live carriers of the refuted omission law, both verified byte-level this
sitting:

1. mag/inference_budget.py:75-84: the FAMILY_TABLE deepseek row carries
   thinking_control={} (:77) and forbidden_keys stripping "thinking"
   (:78-79) with the note "omitting it IS the off state (AH10)" (:84) - the
   exact sentence d4 refuted. The budget harness does not merely omit the
   off-switch, it actively STRIPS it from any caller that tries to send it,
   forcing the ON default on every budget-governed deepseek ask while its
   own note claims OFF. d4_thinking_probe.md:83-87 names this fix as owed;
   no lane has landed it. Amendment: thinking_control={"thinking":
   {"type": "disabled"}}, drop "thinking" from forbidden_keys, replace the
   :84 note with the d4 citation.
2. tests/test_route_chat_depth.py:83-89: test_lane_without_flag_omits_
   thinking ASSERTS that a flag-less lane must not grow a thinking key
   ("thinking" not in body). My run this sitting:
   `.venv/Scripts/python.exe -m pytest tests/test_route_chat_depth.py -q`
   -> 4 passed in 0.79s. The wave that proved omission-is-ON also wrote a
   green test enshrining omission as correct behavior. Under the D3 verdict
   this test is the law's negative image and must be rewritten to assert
   the unconditional mechanical key (it will fail until route_chat.py:204
   flips - which is the point: the test is the flip's enforcement).

One-sitting move (costed, ~75 min total): probe the funded lanes with the
disabled key (~3 calls, ~$0.001); flip route_chat.py:204 to unconditional
mechanical-off + gate design on a lane capability field; fix
inference_budget.py:77-84; rewrite test_route_chat_depth.py:83-89; land the
two prose amendments above; add "depth": depth to the route_chat _bank dict
(mag/route_chat.py:242-249 banks no depth field today, so the decision is
unauditable post-hoc at its own surface - CONVERGENT with
communication.md:39, who found the same gap independently).

## D2 VERDICT: ACCEPT THE DEBT STANDING on the file split. The real debt in dungeon.py is the call path, not the line count

Verdict: do not split tools/dungeon.py this sitting. Reasoning a reviewer
can re-derive:

1. The seam that mattered is already cut and pinned. The parser lives
   verbatim in Dungeon._grade() (tools/dungeon.py:565-610, docstring names
   the extraction from the campaign loop and both fixed defects), and the
   replay net is real: tests/test_dungeon_parser.py:61 asserts
   len(FIXTURES) == 14 and :119 replays all 14 logged S4 verdicts. My run:
   `.venv/Scripts/python.exe -m pytest tests/test_dungeon_parser.py -q` ->
   13 passed in 0.67s. The bug class a file split would guard (verdict-text
   parsing drifting from game law) is the one class already under replay.
2. The split does not clear the rule in one seam (CONVERGENT with
   economics.md:161-170): campaign() plus the SCENES tables is the bulk;
   cutting the engine seam leaves the file over the 400-line rule, so the
   "fix" is two seams of import churn for zero behavior delta, against a
   registered debt (configs/violation_baseline.json, accepted by name
   go-wave-20261004-coordinator) that the ratchet already governs - my run
   of the full check was executed by the economics lens this sitting
   (economics.md:135-140: PASS, scope 1404, dungeon now 771, +15 over the
   756 accepted). I did not re-run the ratchet myself (OWED); my own wc -l
   confirms 771.
3. The file's actual live defect is its call path (MINE, neither sibling
   caught the byte): tools/dungeon.py:211 reads `content = msg.get("content")
   or msg.get("reasoning") or ""` - the same dead fallback name a06#3 killed
   in route_chat (the vendor field is reasoning_content; route_chat.py:231-235
   now reads it with the fix comment). Dungeon's copy is the pre-fix
   generation of the same bug: if a model ever returns reasoning-only
   content, dungeon's void machinery cannot see it for the same reason
   route_chat's could not. _paid (dungeon.py:200-231) is a fork of old
   route_chat: no depth posture, no fence, dead fallback. The estate already
   ruled the remedy: "tavern/dungeon/hermes_burn/grok_burn still self-call;
   each migrates to route_chat or documents its reason ... one per sitting"
   (queue/STANDING_RAILS.md:46-48). Migration, not split, is the sitting
   that buys behavior: it deletes the dead byte, imports the depth law D3
   just ruled, and inherits the exception-path banking.
4. Blast radius is small and testable (my census this sitting): zero mag/
   importers (grep over mag/ + main.py: only mag/abundance_rogue.py's own
   unrelated dungeon() function); importers are tools/prepush_golden_vector
   .py, tests/test_prepush_golden_vector.py, and subprocess callers. So the
   migration or a later split is cheap WHEN triggered - optionality is
   preserved, which is the strongest argument for not paying the split now.

Flip conditions (convert to SPLIT in the following sitting): (a) a second
collapse-class bug in dungeon.py within 2 waves; (b) the next substantive
campaign edit landing (split-while-touching beats split-for-its-own-sake);
(c) dungeon.py becomes the ratchet GROWTH cohort's top grower (it is +15 in
a cohort led by percolator +442, economics.md:145-151).

One-sitting move (~45 min): fix dungeon.py:211 to read reasoning_content
(the route_chat:231-235 fix verbatim), delete the dead shadowed play() at
dungeon.py:447 (CONVERGENT with communication.md:48 and economics.md:171-
176, both derived it independently; my structure grep saw both defs at :447
and :727), fix the stale :618-era citation that points into the dead block,
and either migrate _paid to route_chat mechanical or land its written
reason as the rails debt requires.

## Ask-brief count drift (the census laws apply to the brief too; CONVERGENT with communication.md:46)

The brief said "756 lines" (byte truth this sitting: 771) and "15 dungeon
tests pass in under a second". My instruments: the parser file alone is
13 tests / 0.67s; the 15th and 16th dungeon-named tests live elsewhere
(tests/test_burn_id_uniqueness.py:35, tests/test_prepush_golden_vector.py:29,
found by grep); the combined 3-file run is 21 passed in 1.98s (8 of those
are not dungeon-named). So "15 dungeon tests" is reconstructible only by
name-census across files, and "under a second" holds only for the
file-scoped instrument. Every count above names its instrument; none of
these numbers may be quoted without it.

## What I could not verify (OWED, never asserted)

- No paid probe fired this sitting: omission=ON is the wave's banked d4
  measurement, not mine; GLM prime's thinking wire shape on the z.ai/Nous
  gateway is unmeasured (the usage.jsonl:1151 row proves the PHENOMENON on
  a glm judgment ask, not the vendor default).
- I did not open memory/runs/ds_batches/sacred_cow_thinking_on.jsonl; the
  arm-2 counts (2/10 zero-content, 4/10 cap-pinned) rest on a06#0's
  byte-quoted census.
- I did not re-run tools/violation_ratchet.py check myself; the PASS +
  GROWTH lines are the economics lens's run this sitting, and my own wc -l
  (771) corroborates the number it printed.
- I did not re-verify the 3/28 judge-tally arithmetic; that number is the
  ds_workhorse.md receipt's (:71-87).
- The exact wire behavior of thinking:{type:disabled} on vast/together
  (accept vs ignore vs 400) is unmeasured; the verdict's probe-first leg
  exists precisely because of this.

## Checks run this sitting (exact commands)

1. `.venv/Scripts/python.exe -m pytest tests/test_dungeon_parser.py -q` ->
   13 passed in 0.67s
2. `.venv/Scripts/python.exe -m pytest tests/test_route_chat.py -q` ->
   4 passed in 0.78s
3. `.venv/Scripts/python.exe -m pytest tests/test_route_chat_depth.py -q` ->
   4 passed in 0.79s
4. `.venv/Scripts/python.exe -m pytest tests/test_dungeon_parser.py
   tests/test_burn_id_uniqueness.py tests/test_prepush_golden_vector.py -q`
   -> 21 passed in 1.98s
5. sed/grep reads: mag/inference_budget.py:60-145; tools/ds_workhorse.py
   :40-110; watch/inbox/model_garden/PRIORS.md:20-35; configs/providers.yaml
   (disable_thinking census, :200-240, :420-445, :521-535, lane list);
   memory/runs/hermes_burn/usage.jsonl:1149-1153; tools/dungeon.py (full
   structure, :1-80, :148-310, :548-617, :720-771); tests/test_route_chat_
   depth.py (assertion census); a06-sacred-cow.json (full); d4_thinking_
   probe.md + ds_workhorse.md (full)
6. Blast-radius grep: `grep -rn dungeon mag/ main.py --include=*.py` (zero
   tools.dungeon importers) + `grep -rln tools.dungeon tools/ tests/`
