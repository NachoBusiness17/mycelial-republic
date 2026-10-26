# break-logic.md - hostile second pass on the instrument-theory lens (logic.md)

Moment 2026-10-04 (post-07:16Z, after the last sibling lens file mtime). Every
check below was read or run THIS sitting with `.venv/Scripts/python.exe` and
git on the mag tree. No em-dashes. Anything I could not verify is OWED, never
asserted. Universal claims are scoped to the search actually run.

Scope note: the ask handed me a truncated copy of logic.md (cut mid-move in
finding 2). I broke the FULL on-disk file
(watch/inbox/ractor_engine/2026-10-04-parked-decisions/logic.md, 293 lines),
which carries a third finding (DECISION 2, dungeon) the ask copy lost. All
three are verdicted here.

## VERDICTS

### Finding 1 (D3 verdict + evidence bundle): CONFIRMED

Every load-bearing cite byte-checked and reproduced:

- d4_thinking_probe.md:53-62: table reads omitted = 70 chars
  reasoning_content / 18 reasoning_tokens, disabled = 0 / block absent,
  enabled = 46 chars / 12 reasoning_tokens; arm-3 sanity paragraph at :64-65;
  $0.00007 spend at :26-28. Exact match to the lens's numbers.
- mag/route_chat.py:204-213: mechanical sends `thinking:{type:disabled}` only
  when `lane_cfg.get("disable_thinking")` (:204, key sent at :211); design
  sends `thinking:{type:enabled}` unconditionally (:212-213). Confirmed.
- mag/inference_budget.py:78: `forbidden_keys=("thinking", ...)` on the
  deepseek row; :84 note still reads "omitting it IS the off state (AH10)".
  Confirmed UNFIXED as of this sitting.
- memory/runs/hermes_burn/usage.jsonl:1151: byte-exact. model
  z-ai/glm-5.3-prime, completion 16000, reasoning_tokens 15998,
  finish_reason length, content_chars 1, ok true, cost_usd 0.2502604.
- a06-sacred-cow.json: key ee225394e567 at :37 (the zero-grep proof row); row
  1 quote (e6baa31db6c0, :11) = cow2-SUBSTANCE_48h_synthesis, content_chars 0,
  reasoning_chars 59103, completion 16000, ok false; row 2 (bd72a67f4a56, :20)
  carries "unjudged length ratio against a budget-confounded baseline" and
  arm-1 content_chars 12765/6746/17671/16770. All confirmed.
- watch/inbox/model_garden/PRIORS.md:25: row 8, "THINKING OFF MANDATORY",
  status "STILL-VALID (byte-confirmed mechanism, never refire thinking-on)",
  Condition column scopes it to the Nous gateway. Confirmed.
- Instruments re-run by me: `pytest tests/test_route_chat_depth.py
  tests/test_route_chat_banks.py -q` = 6 passed in 2.02s (lens claimed 6 in
  1.43s; count exact, time is machine-variance). `pytest
  tests/test_inference_budget.py -q` = 19 passed in 1.04s (lens: 19 in
  0.97s; count exact).
- Convergence cites: economics.md:8 is verbatim "explicit-off on the wire ...
  Omission is never a posture". accuracy.md:13-16 is the lane-config-carried
  variant. Both confirmed in their files.

Independent corroboration the lens did not have (strengthens the
carrier-enforced verdict over the accuracy/operations lane-config form):

- configs/providers.yaml:151-170: the nous block (z-ai/glm-5.3-prime, the
  founding burn's lane) carries NO disable_thinking flag; its own comment at
  :157 states the mechanism. Under lane-config gating the founding lane sends
  no off key and rides vendor-default ON. operations.md:54-64 already
  conceded this and WITHDREW its lane-config verdict; with operations amended,
  the posture is majority-carried (logic, economics, operations-amended;
  moonshot-1/2 and dogfood per operations.md:62, which I read but did not
  line-verify beyond operations' quote; accuracy holds the minority form).
- The current wire provably still rides omission on flagless lanes:
  tests/test_route_chat_depth.py:83-91 (`test_lane_without_flag_omits_thinking`)
  asserts `"thinking" not in body` for a flagless mechanical ask, and it
  passes. The hole the verdict closes is pinned green in the suite today.

Three amendments the verdict must carry (none fatal):

1. The move's test churn is under-priced. Under the proposed gate,
   tests/test_route_chat_depth.py:77-81 (`test_design_wires_thinking_enabled`)
   fires depth="design" at the route_chat default max_tokens=4000
   (mag/route_chat.py:122) and would start raising; :83-91 pins flagless
   mechanical omission as CORRECT and must be rewritten to expect the
   disabled key. So the move is "rewrite two existing cases + add two", not
   "add the two depth-test cases".
2. Cite defect inside the falsifier: logic.md attributes the "funded lane
   rejects the thinking key" flip family to accuracy.md:59. accuracy.md:59 is
   the re-fire-label line; that flip family lives at economics.md:59-60
   ("a funded lane that REJECTS the top-level thinking key with a 400").
   Substance true, anchor wrong.
3. The inference_budget flip's blast radius is 3 carriers, not the module
   alone: `plan_call` is called at tools/hermes_burn.py:344,
   tools/model_garden.py:348, and tools/code_swarm.py:133 (my grep of mag/,
   tools/, main.py, tests/; those are the only callers found). "Active
   think-enabler" is confirmed and wider than the lens scoped it.

Falsifier state: not met by any byte I ran. The n>=5 judged A/B does not
exist anywhere I searched (the only ON-quality datapoints remain arm 1 n=4
unjudged budget-confounded, a06-sacred-cow.json:20); no funded lane is
measured 400-ing on `thinking:{type:disabled}` (PRIORS row 15's HTTP 400 is
the `reasoning` param, PRIORS.md:32); accuracy.md's one live re-run read
omission = 11 reasoning tokens (accuracy.md:23-25), same direction, so the
two-confirmation base stands. OWED (unchanged from the lens): nobody has
re-run the probe a third time; I spent no paid calls this sitting.

### Finding 2 (re-fire posture label unevidenced): CONFIRMED, strengthened

All cites byte-checked:

- memory/runs/ds_batches/frontier_delta_results_v3.jsonl row 1: keys are
  exactly {attempts, cost_usd, id, model, ok_api, ok_material, out,
  prompt_tokens}, id delta-BARFIGHT_spec, model deepseek-chat. My census went
  further than the lens's row-1 read: NO row of the 14 carries any
  thinking or reasoning key (python key-walk over all rows, output "False").
  The posture label is unevidenced at the batch level, not just row 1.
- The command rode `-m tools.ds_workhorse` directly
  (watch/inbox/go_wave_20261004/ds_workhorse.md:63-66), not route_chat.
- tools/ds_workhorse.py:86-92 carries the landed erratum comment ending
  "every batch before the erratum ran thinking-ON"; the explicit
  `"thinking": {"type": "disabled"}` is at :93; MODEL = "deepseek-chat" at
  :64. Confirmed. (Side note: accuracy.md cites ds_workhorse.py:29 for the
  model constant; :29 is a docstring line. logic.md's :64 is the right
  anchor.)
- ds_workhorse.md:62 headlines item 6 "uncapped, thinking-off"; the cap/slice
  removal is documented at :51-57 and the refire spread "5788-31000 chars,
  0 rows at 6000" at :67 (the lens bundled :67's figures into its :51-57
  cite; content present, range one line short). d4_thinking_probe.md:78-82
  (consequence 1) folds the item-6 refire into the rode-thinking-ON census.
  Confirmed.

The falsifier is crisp and runnable (a pre-refire diff showing a thinking
key, or a 3-arm probe on deepseek-chat reading omission = zero). Neither
exists in any byte I read; the alias posture remains the estate's cheapest
open measurement (~$0.0001) and stays OWED: I did not fire it from a break
pass.

### Finding 3 (DECISION 2, dungeon: accept-the-debt-standing): CONFIRMED with amendments

Present only in the on-disk logic.md (the ask's copy truncated it). All
instrument cites reproduced by me:

- configs/violation_baseline.json:5313: tools/dungeon.py, accepted_lines 756,
  by go-wave-20261004-coordinator, rule file-too-long. Confirmed.
- tools/violation_ratchet.py:44: FILE_LINE_CAP = 400. Confirmed.
- `pytest tests/test_dungeon_parser.py tests/test_burn_id_uniqueness.py -q
  -p no:cacheprovider` = 15 passed in 1.41s (lens: 15 in 1.19s; count exact).
  The ask's "under a second" is false on my run and on the lens's; the count
  arithmetic 13 parser + 2 burn-id reproduces (parser fixtures assert len ==
  14 at tests/test_dungeon_parser.py:61; import at :26).
- AST census (my run, tools/dungeon.py): one class Dungeon at :148 (end 731),
  DUP METHODS {'play': [447, 727]}, _grade at :565, campaign at :612.
  Confirms the shadowed-play finding and the seam anchors. Counting-key nit:
  22 unique method names, 23 raw defs; the lens's "23 methods" is true only
  counting the duplicate twice, and it does not say so.
- queue/STANDING_RAILS.md: `grep -in "thinking|depth"` exit 1, zero hits
  (file is 53 lines by wc; logic.md's correction 1 says 54, accuracy.md says
  53; the byte count is 53). The per-lane-call-laws phrase is at :11-12 and
  the ds re-fire debt note at :49-53 carries the 3/28 tally with no posture
  claim. Confirmed.
- dungeon.md (watch/inbox/go_wave_20261004/dungeon.md) cites :49 (15-test
  pair, 1.08s), :51 (dry smoke), :64 (ratchet NEW-debt FAIL history,
  627 to 756), :65 (open a02#3 de-glob retry leg), :70 (mag/dungeon_dev is a
  different surface). All confirmed verbatim.
- Convergence: economics.md:122 ("ACCEPT THE DEBT STANDING") and
  operations.md:21 (same verdict) confirmed.

Amendments:

1. THE GIT ARCHEOLOGY THE LENS MARKED OWED IS NOW SETTLED, AND OPERATIONS
   MD'S ARITHMETIC IS WRONG. operations.md:25 claims "exactly 3 commits after
   the acceptance commit d349ce7d2 (c3ff9d1bd, eabf0f67f, 72f1c58c7)". My git
   run: d349ce7d2 (2026-10-04T05:50:05-04:00, message carries "dungeon.py:756
   ... debts accepted by name") holds 756 lines; c3ff9d1bd is dated
   2026-10-03T23:16:59-04:00 and PREDATES acceptance; the real second hash is
   eabf0d67f (operations typo "eabf0f67f"), dated 05:55:59, and holds 756
   lines (+0 net on this file); 72f1c58c7 (06:03:08, 3-strike void breaker)
   holds 771. So: 2 commits after acceptance, not 3; the entire +15 is ONE
   commit. This STRENGTHENS logic.md's hardening premise (one commit, +15)
   while killing operations' supporting arithmetic. logic.md leaned on
   operations for this leg with the blind-spot caveat; the leg now stands on
   my git output instead.
2. The dead-code rider under-counts: dungeon.py:623 reads
   `if self.warden_hp <= 0 or self.persuades >= 2 or True:` (my sed; the
   first two disjuncts are dead). accuracy.md:143-146 found it; logic.md's
   "one free rider (delete the shadowed duplicate play())" misses it. The
   re-stamp sitting should sweep both.
3. THE LENS'S "RATCHET: PASS" QUOTE IS STALE AT MY MOMENT. My full-tree run
   `python tools/violation_ratchet.py check` reads: scope=1405, hits=943,
   registered=942, NEW=1,
   `NEW e71ef4422e755b5e file-too-long: tools/social_rsi.py:578`,
   RATCHET: FAIL. Every sibling lens reported PASS earlier this sitting; the
   tree has since grown an unrelated unregistered debt and the pre-push gate
   is RED now. Dungeon's own debt still only GROWTH-flags (its line is
   present in my output verbatim), so the lens's "the debt cannot silently
   grow" leg HOLDS, but the synthesis must cite the gate as FAIL, not PASS,
   and the re-stamp sitting inherits a social_rsi.py:578 acceptance too.
4. The importer census is loose. My scoped grep
   (`grep -rlnE "from tools import dungeon|import tools\.dungeon|tools\.dungeon"
   --include="*.py" .` minus attic/corpus/.venv/dungeon_dev/worldline) hits
   exactly the 2 test files. tools/prepush_golden_vector.py references
   dungeon.py in docstring prose and by design consumes its bytes (a token
   tripwire, its own :18-20), it does not import it. "The real importers are
   prepush_golden_vector + the three test files" does not reproduce under my
   instrument; the blast-radius CONCLUSION (small) survives.
5. The three split-trigger alphas (logic 800 lines / economics ~871 / 
   operations +50) are all unratified proposals; logic.md pre-registered
   exactly that (blind spot 3) and deserves the credit.

Falsifier state for the D2 verdict: the replay pair is green on my run, so
the primary falsifier (red replay) is not met; the growth-pace falsifier
(>30 lines/week sustained) is not met (+15 in one hardening commit, ~3h
after acceptance, nothing since: my git log shows no dungeon.py commit after
72f1c58c7).

## What the lens missed (additions)

1. Gate-state drift: ratchet full check now FAILs with NEW=1 on
   tools/social_rsi.py:578 (unrelated to dungeon). All four lens PASS quotes
   went stale within the hour. Move cost for the synthesis: zero minutes of
   re-derivation, one line of corrected gate state; the social_rsi acceptance
   is the coordinator's call, not this decision's.
2. tests/test_route_chat_depth.py:83-91 is the in-suite carrier of the
   refuted omission law: it pins flagless-mechanical omission as correct
   behavior. The D3 move must rewrite it, and its comment line is the place
   the d4 erratum should also land (the module docstring and ds_workhorse
   errata do not cover the test's own claim).
3. plan_call callers census: tools/hermes_burn.py:344,
   tools/model_garden.py:348, tools/code_swarm.py:133. The inference_budget
   recipe flip touches three carriers' fire paths, which is exactly why it
   needs its assertion replay (19 tests green on my run) after the edit.
4. The nous providers block (configs/providers.yaml:151-170) is the byte that
   ENDS the posture dispute: the founding $0.46 double burn rode a flagless
   lane, so lane-config gating provably fails on the founding evidence
   itself. logic.md argued this from instrument theory; the config bytes
   prove it.
5. Literal-caller census for the proposed 32K design gate: the only
   depth="design" call site in mag/, tools/, tests/, main.py is
   tests/test_route_chat_depth.py:79. The gate's caller blast radius is that
   one test plus new cases (scope: literal grep; a dynamic depth= variable
   caller would not be caught by this instrument, named as such).

## OWED (not asserted by me)

- No live API call was fired this sitting: vendor drift between the d4 runs
  (lens moment) and now remains invisible; the deepseek-chat alias probe and
  the third d4 re-run remain owed, still ~$0.0002 total.
- I did not apply the proposed route_chat gate (a break pass never edits), so
  fence-test compatibility of the PROPOSED code is untested; I only ran
  tests/test_route_chat_fence.py on the CURRENT tree: 5 passed in 1.02s.
  That closes half of logic.md's blind spot 2 (the fence path is green
  standalone) and none of the compatibility question.
- operations.md:62's tally of moonshot-1.md:21 / moonshot-2.md:41 /
  dogfood.md:13 siding carrier-enforced is taken from operations' quote; I
  read operations.md in full but not those three files' lines. Their
  convergence flags stay second-hand here.
- mag/route_chat.py:254-266 (the fail-loud raise path operations.md:56 cites)
  was outside my read range; not confirmed, not used in any verdict above.

## Instrument ledger (what I ran, this sitting)

- wc -l: usage.jsonl 2200, tools/dungeon.py 771, mag/route_chat.py 273,
  queue/STANDING_RAILS.md 53.
- pytest: depth+banks 6 passed (2.02s); inference_budget 19 passed (1.04s);
  dungeon pair 15 passed (1.41s); route_chat_fence 5 passed (1.02s).
- python tools/violation_ratchet.py check: FAIL, NEW=1 social_rsi.py:578,
  8 GROWTH lines incl. dungeon +15.
- git log/show on tools/dungeon.py across d349ce7d2 / eabf0d67f / 72f1c58c7
  (756 / 756 / 771) and c3ff9d1bd's date (pre-acceptance).
- AST census tools/dungeon.py; key-walk of frontier_delta_results_v3.jsonl;
  greps: supports_thinking (0 hits in providers.yaml), disable_thinking
  (3 hits: :223, :371, :401), rails thinking/depth (0 hits), plan_call
  callers (3), depth="design" callers (1).
