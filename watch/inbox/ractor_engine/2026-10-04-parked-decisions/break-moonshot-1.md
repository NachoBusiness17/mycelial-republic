# BREAK PASS: moonshot-1 (hostile second pass, 2026-10-04)

Breaker: break-moonshot-1. Target: moonshot-1.md in this directory. Method:
every path:line in the lens report re-opened and byte-read this sitting;
every test re-run with the same instrument the lens named; the two
load-bearing counts the lens marked OWED (manifest census, ratchet) run by
me. No em-dashes. Anything I could not verify is OWED, never asserted.

## Checks run this sitting (exact commands, real outputs)

1. `./.venv/Scripts/python.exe -m pytest tests/test_route_chat_depth.py -q`
   -> 4 passed in 0.88s (lens claimed 4 passed 0.79s; count matches, moment differs)
2. `./.venv/Scripts/python.exe -m pytest tests/test_dungeon_parser.py -q`
   -> 13 passed in 0.84s (lens: 13 passed 0.67s)
3. `./.venv/Scripts/python.exe -m pytest tests/test_route_chat.py -q`
   -> 4 passed in 0.89s (lens: 4 passed 0.78s)
4. `./.venv/Scripts/python.exe -m pytest tests/test_dungeon_parser.py tests/test_burn_id_uniqueness.py tests/test_prepush_golden_vector.py -q`
   -> 21 passed in 2.15s (lens: 21 passed 1.98s)
5. `./.venv/Scripts/python.exe tools/violation_ratchet.py check --changed`
   -> `RATCHET check: scope=1 changed files; hits=0; registered=0; NEW=0;
   expired-exceptions=0` then `RATCHET: PASS - no unregistered debt.`
   INSTRUMENT NOTE: this is the changed-scope instrument (scope=1). The
   economics lens's run (economics.md:135-140) was the FULL `check`
   (scope=1404) which is what prints the dungeon GROWTH line (accepted 756,
   now 771, +15, key af1d7045681fee89). I did not re-run the full-scope
   instrument; the +15 GROWTH print rests on economics.md:135-140, my
   contribution is the changed-scope PASS plus `wc -l tools/dungeon.py` = 771
   and the baseline entry at configs/violation_baseline.json:5313
   ("file": "tools/dungeon.py").
6. Manifest census (the lens's OWED item, closed by me):
   `./.venv/Scripts/python.exe -c` over
   memory/runs/ds_batches/sacred_cow_thinking_on.jsonl -> total 14 rows;
   arm 1 (cow-): 4 rows, 0 ok:false; arm 2 (cow2-): 10 rows, 2 ok:false with
   content_chars 0 (SUBSTANCE_48h_synthesis ct=16000, KABUKI_FACES_fold
   ct=16002); arm-2 rows at-or-over 16000: 5 (the 2 zeroed + play_findings,
   THE_ROOM_REMEMBERS, SEASON_design all at exactly 16000); all rows
   at-or-over 16000: 7.
7. Greps: disable_thinking census over configs/providers.yaml (full file:
   exactly 3 hits, :223, :371, :401); `def |class ` census over
   tools/dungeon.py; `.get("reasoning")` census over tools/ mag/ tests/
   main.py; tools.dungeon importer census over mag/ main.py tools/ tests/
   scripts/.

## VERDICTS

### Finding 1 (D3 verdict: depth-gated, wire-explicit, unconditional
### thinking:{type:disabled} on depth=mechanical; design arm capability-gated;
### lane-config-gating loses): CONFIRMED

Every evidence byte checked and intact:
- disable_thinking census: exactly 3 flags, configs/providers.yaml:223
  (openrouter), :371 (deepseek), :401 (deepseek_overmind). Full-file grep,
  this sitting.
- vast default_model deepseek-v4-flash at :434, block :417-450, no flag;
  together default_model deepseek-ai/DeepSeek-V4-Flash-0731 at :528, block
  :521-535, no flag. The lane-config-gating kill argument holds where it
  must: on the d4-measured model's flagless lanes.
- openrouter comment :219-222 verbatim ("IGNORES thinking:{type:disabled} -
  it thinks anyway and eats small budgets (600 -> empty, 2000 -> content)").
- mag/route_chat.py:204 gate byte-read
  (`if lane_cfg.get("disable_thinking") and depth == "mechanical":`);
  :212-213 design arm byte-read, ungated, sends enabled to every lane;
  :21 docstring "fail-loud" confirmed.
- a06-sacred-cow.json key ee225394e567 at :37-44 carries the exact design-arm
  and dead-fallback flags the lens cites.
- d4_thinking_probe.md:55 arm 1 omitted = 18 reasoning tokens; :26-28 the
  $0.00007 3-arm probe; usage.jsonl:1151-1152 the founding pair byte-read
  (16000 completion / 15998 reasoning / length / content_chars 1 / $0.2502604;
  then 14759 / 9826 / stop / content / $0.2137336).

Caveats carried, none flip the verdict:
(a) PRIORS.md:32 row 15 says qwen3.7-flash "rejects the reasoning param
    outright (HTTP 400, fires without)" - the 400 was for the reasoning
    param, not the thinking key. The design-gate urgency is by-analogy
    across param names, and the lens's own probe-first leg already covers it.
(b) "vast is reachable, not decorative" rests on providers.yaml:836/:839-840
    (scut, hard_code, hard_reason chains list vast). I did not trace
    model_pick -> vast end-to-end; an explicit lane= call suffices for the
    front-door law either way.
(c) The disabled key's wire behavior on vast/together (accept vs ignore vs
    400) remains unmeasured; the lens says so itself and the probe leg exists
    for exactly that.

### Finding 2 (the refuted omission law is pinned GREEN by this wave's own
### tests and actively enforced by the budget harness): CONFIRMED

- mag/inference_budget.py:77 `thinking_control={}`, :78-79 forbidden_keys
  strip "thinking", :84 the note "omitting it IS the off state (AH10)" -
  all byte-read this sitting; the row is unamended post-d4 and its comment
  (:72-73) still says "thinking-off via omission, AH10 byte-confirmed".
- tests/test_route_chat_depth.py:83-89 byte-read:
  test_lane_without_flag_omits_thinking asserts `"thinking" not in body`.
  My run (instrument above): 4 passed in 0.88s. The green pin is real.
- d4_thinking_probe.md:83-87 names the inference_budget fix as owed; nothing
  has landed it. The finding's falsifier (a byte trace of a post-d4
  amendment) did not fire.

### Finding 3 (no thinking-OFF quality score exists; the ds re-fire rode ON;
### the "thinking-off uncapped" label is false on the wire): CONFIRMED,
### with one correction to the move

- Ordering byte-verified: ds_workhorse.md:62 is the item-6 header
  "ds arm re-fired, uncapped, thinking-off, file-backed"; :63-66 the carrier
  `.venv/Scripts/python.exe -m tools.ds_workhorse run ...`; tools/ds_workhorse.py:86-92
  is the dated erratum comment citing d4_thinking_probe.md, :93 the explicit
  `"thinking": {"type": "disabled"}` key; d4_thinking_probe.md:43-46 quotes
  the pre-erratum omission form; d4:78-81 (consequence 1) states the refire
  rode ON. queue/STANDING_RAILS.md:49-53 cites the receipt exactly as the
  lens says.
- The 3/28 arithmetic the lens declined to re-verify, verified by me from
  ds_workhorse.md:71-87: 26 published pairs + 2 gaming_corpus pairs = 28;
  refire judging frontier 12 - ds 2 and flash 13 - ds 1; ds total 3/28.
  The arithmetic is sound.
- CORRECTION: the move says the item-6 erratum text is "drafted in
  moonshot-1.md, matching communication.md's independent draft". The draft
  exists only in communication.md:29 (a ready-to-append blockquote). Grep of
  moonshot-1.md finds no drafted ds_workhorse.md erratum text anywhere in
  that file; its only "erratum" mention (moonshot-1.md:94) is the CODE
  erratum at tools/ds_workhorse.py. The finding stands; the self-attribution
  in the move is false and the synthesis should lift the text from
  communication.md:29.
- Scope note the verdict must carry (the lens already carries it): the
  post-erratum refire falsifier (~$0.13, communication.md:17) was not run by
  anyone; the estate-scope claim "every ds batch through 2026-10-04 06:11Z
  rode ON" rests on the mtime + carrier chain, which I verified at the
  receipt level, not by re-running the batch.

### Finding 4 (dungeon.py:211 dead fallback; the parser seam is cut and
### pinned; blast radius small): CONFIRMED

- tools/dungeon.py:211 byte-read: `content = msg.get("content") or
  msg.get("reasoning") or ""`; mag/route_chat.py:231-235 byte-read: the
  reasoning_content fix with the a06-sacred-cow#3 comment. Same bug class,
  pre-fix generation, exactly as claimed.
- tests/test_dungeon_parser.py:61 `assert len(FIXTURES) == 14` and :119 the
  replay test, both byte-read; my run 13 passed in 0.84s. The ask's "replays
  14/14 logged verdicts green" is instrument-accurate (13 tests replay 14
  fixtures).
- Importer census, mine: zero tools.dungeon importers in mag/ or main.py
  (the mag/game_*.py and mag/primer.py grep hits are mag/dungeon_dev, a
  different module; mag/abundance_rogue.py's own dungeon() is unrelated).
  Real importers: tools/prepush_golden_vector.py, tests/test_dungeon_parser.py:26,
  tests/test_burn_id_uniqueness.py:19, tests/test_prepush_golden_vector.py,
  plus subprocess callers. GAP: the lens's blast list named only
  prepush_golden_vector and "subprocess callers"; tests/test_burn_id_
  uniqueness.py:19 is an importer it omitted (immaterial to the verdict,
  blast radius stays small).

### D2 verdict (accept the debt standing; migration over split): CONFIRMED

- Shadowed play(): defs at :447 (short, s0+s1 only) and :727 (full, with
  campaign) confirmed by my def-census and by reading both bodies; :727
  later in the class body wins, :447 is dead.
- The stale citation confirmed by my grep: tools/dungeon.py:618 comments
  "# party-wide dict (dungeon.py:447 at HEAD 37e2fba7e)" - it points the
  reader at the now-dead :447 play. Real citation rot.
- _grade at :565 with the verbatim-extraction docstring naming both fixed
  defects; _paid at :200-231 with budget gate + dry return + the dead
  fallback and no fence/depth posture visible in the bytes I read
  (:200-215).
- Line count: `wc -l tools/dungeon.py` = 771 (the ask's "756" is stale;
  baseline entry configs/violation_baseline.json:5313; accepted-by-name
  key af1d7045681fee89 per economics.md:135-140, whose full-scope GROWTH
  print I did not reproduce, see instrument note above).
- The two-seam arithmetic (economics.md:161-170: cutting campaign()+SCENES
  leaves ~493 > 400 rule) rests on the economics lens's line math; I
  confirmed the structure (campaign at :612, second play at :727, main at
  :734) but did NOT re-derive the 278/493 split myself. The verdict's
  direction (two seams of import churn for zero behavior delta against a
  registered, metered debt) does not depend on the exact split.
- Flip conditions and the migration-over-split reasoning re-derive cleanly
  from STANDING_RAILS.md:46-48 (the one-per-sitting migration debt) plus the
  byte findings above.

### Count-drift finding (brief said 756 lines / 15 dungeon tests under a
### second): CONFIRMED

- 771 is the byte truth (my wc -l). "15 dungeon tests" reconstructs only by
  name-census: 13 in tests/test_dungeon_parser.py +
  test_dungeon_ids_unique_across_sessions at
  tests/test_burn_id_uniqueness.py:35 + test_vector_tokens_all_present_in_
  live_dungeon at tests/test_prepush_golden_vector.py:29 (both defs
  confirmed by my greps). Under-a-second holds only file-scoped (my parser
  run: 0.84s; my 3-file set: 2.15s; communication.md:48's third instrument
  `-k dungeon` suite-wide: 16 passed in 15.50s). All instruments named.

## WHAT THE LENS MISSED (additions, each byte-checked this sitting)

1. The dead-reasoning-fallback class is NOT dungeon-only, and the lens's own
   blind-spot list asked exactly this question and never ran it. My census
   (`grep -rn '\.get("reasoning")' tools/ mag/ tests/ main.py`):
   - tools/tavern.py:137-138: `content = resp["choices"][0]["message"].get
     ("content") or ...get("reasoning") or ""` - the identical pre-fix
     vendor-message fallback, in the other hourly-cron carrier.
   - tools/hermes_burn.py:356: `content = msg.get("reasoning") or ""` - the
     same dead vendor name in the funded descent carrier (downstream of its
     EMPTY_REASONING guard, :351-354).
   - mag/ox_seat.py:144 banks `"reasoning": msg.get("reasoning") or msg.get
     ("reasoning_details")` - the dead vendor read at the banking layer the
     ox_* family and mag/aos_agent.py:261, mag/fuel_feed.py:440,
     mag/seat_probe.py:68 all consume downstream.
   Scope caveat: "dead" is byte-proven for the openai_compat/deepseek family
   the a06#3 fix names (reasoning_content is the vendor field); openrouter-class
   gateways do return a `reasoning` field on some models, so these copies are
   same-class-by-the-estate's-own-ruling, and each needs its own lane-level
   check before the same one-line fix. Cite the a06#3 fix comment at
   mag/route_chat.py:231-233 for the ruling.
2. The arm-2 cap census is sharper than the ask's shorthand: 2/10 zeroed
   (confirmed by my count), but "4/10 cap-pinned" matches only the
   exactly-16000 cut (play_findings, THE_ROOM_REMEMBERS, SEASON_design +
   the zeroed SUBSTANCE_48h_synthesis at exactly 16000; KABUKI_FACES_fold is
   16002). The clean byte numbers: arm 2 = 5/10 at-or-over 16000; all rows =
   7/14 at-or-over, which matches a06 row 1's own "7/14" claim
   (a06-sacred-cow.json:10). The D3 verdict's load-bearing number (2/10
   zero-content at the cap) survives my independent count exactly.
3. The two STANDING_RAILS Law 1 amendment drafts are NOT the same text.
   economics.md:69-85 drafts unconditional every-lane mechanical-off with no
   design gate and no openrouter rider; moonshot-1.md's surface-2 draft adds
   "for every lane that accepts the key", the capability-gated design arm,
   and the openrouter budget defense. The synthesis must merge (moonshot's
   is the superset); quoting either alone loses a clause the other carried.
4. moonshot-1.md's surface-3/4 move includes adding "depth" to the _bank
   dict, and communication.md:39 independently found the same gap (my
   route_chat.py:242-249 read confirms the banked fields carry no depth).
   CONVERGENT, correctly flagged by the lens. No correction.
5. My ratchet run contributes a second PASS but on a DIFFERENT instrument
   (changed-scope, scope=1) than the economics lens's full check (scope=1404
   with the GROWTH print). Both instruments PASS this sitting; the
   GROWTH-signal reproduction remains economics's run only.

## Still OWED (unverified by anyone, including me)

- No paid probe fired this sitting by any lens: omission=ON is the wave's
  banked d4 measurement; the disabled key's behavior on vast/together and
  GLM prime's vendor default remain unmeasured.
- The ~$0.13 post-erratum ds refire (finding 3's own falsifier) is unrun.
- The full-scope ratchet GROWTH print (scope=1404) is the economics lens's
  run; I ran the changed-scope instrument only.
- The 278/493 two-seam line math is economics.md:161-170's arithmetic, not
  independently re-derived by me.

## Bottom line

Six of six findings CONFIRMED on byte evidence; zero killed; zero weakened
below confirmation. Two corrections ride along: the erratum draft lives at
communication.md:29, not in moonshot-1.md (finding 3's move), and the
"4/10 cap-pinned" shorthand resolves to 5/10 at-or-over / 4 at-exactly-16000
under my census. The D3 verdict (depth-gated, wire-explicit, unconditional
mechanical-off, design capability gate, probe first) and the D2 verdict
(accept the debt standing; fix :211, delete the dead :447 play, fix the :618
citation, migrate _paid per STANDING_RAILS.md:46-48) both survive the
hostile pass.
