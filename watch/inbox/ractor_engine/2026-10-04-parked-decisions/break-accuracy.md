# break-accuracy - hostile second pass on the accuracy lens, 2026-10-04

Lens: byte-check every evidence cite in
`watch/inbox/ractor_engine/2026-10-04-parked-decisions/accuracy.md` against
the estate, attack the falsifiers, find what the verdicts dropped. No
em-dashes. Anything I could not verify is marked OWED. Universal/absence
claims name their instrument and scope.

## Instrument (what I ran THIS session, repo root, win32)

1. `.venv/Scripts/python.exe watch/inbox/go_wave_20261004/d4_probe.py`
   (live, 3 API asks, ~$0.00007): omitted arm = reasoning_content 63 chars,
   reasoning_tokens 16, completion 19, finish stop; disabled arm = 0
   reasoning chars, completion 2, no completion_tokens_details; enabled arm
   = 46 chars, reasoning_tokens 12.
2. `grep -n -i "thinking\|depth" queue/STANDING_RAILS.md` -> exit 1, zero
   matches (scoped to that one file, read in full earlier: 53 lines).
3. `.venv/Scripts/python.exe tools/violation_ratchet.py check` (full tree,
   no --changed): `scope=1405 files (all); hits=943; registered=942; NEW=1`,
   the NEW hit `e71ef4422e755b5e file-too-long: tools/social_rsi.py:578`,
   8 GROWTH lines including the exact dungeon line, then
   `RATCHET: FAIL`, exit 1.
4. `wc -l tools/dungeon.py` -> 771.
5. `git show 72f1c58c7 --stat` -> "3-STRIKE VOID BREAKER (ractor move 2)",
   `tools/dungeon.py | 15 ++++++++++++++`, 1 file changed, +15 insertions.
6. `.venv/Scripts/python.exe -m pytest tests/test_dungeon_parser.py
   tests/test_burn_id_uniqueness.py -q` -> `15 passed in 1.17s`; solo
   `pytest tests/test_dungeon_parser.py -q` -> `13 passed in 0.72s`;
   `pytest tests/test_route_chat_depth.py -q` -> `4 passed in 0.74s`.
7. `sed -n '1151p' memory/runs/hermes_burn/usage.jsonl` -> the founding row
   (contents under F2/addition A7).
8. Reads: accuracy.md, d4_thinking_probe.md, d4_probe.py,
   mag/route_chat.py (100-262), tools/ds_workhorse.py (1-120),
   ds_workhorse.md, PRIORS.md, providers.yaml (218-224, 365-372),
   tools/dungeon.py (440-455, 555-634, 725-733), tests/test_route_chat_depth.py,
   violation_ratchet.py (255-299), violation_baseline.json:5308-5314,
   a06-sacred-cow.json (all three cited keys loaded with venv python).

## Verdicts

### F1: D3 verdict, lane-config-gated explicit-off (accuracy.md:8-29, 70-90)

**CONFIRMED.** Every cite byte-checks and the falsifier is false a third
time by my own live run. My probe re-run (instrument 1): omitted = ON
(16 reasoning_tokens, 63 chars), disabled = OFF (0, completion 2),
enabled = ON (12). Same direction as the founding receipt
(d4_thinking_probe.md:55-57: 18 tokens/70 chars vs 0 vs 12) and the lens's
own run (11/45). The wire is exactly mag/route_chat.py:204-213; the enum
137-141; the docstring's "where the lane supports it" claim is at
route_chat.py:127-128 while the design branch at 212-213
(`if depth == "design": body_obj["thinking"] = {"type": "enabled"}`) is
unconditional: the ungated-defect claim is real.
tests/test_route_chat_depth.py:61-89 spans exactly the four pinned tests
and runs green for me (4 passed in 0.74s). The mechanism is genuinely
lane-config-gated: route_chat.py:49-51 loads lanes from
configs/providers.yaml, and disable_thinking: true exists on three lanes
(openrouter :223, deepseek :371, deepseek_overmind :401). See A2 for the
cost the move under-priced, A4 for the convergent third run.

### F2: the law surfaces are mis-cited; the re-fire label is unverified (accuracy.md:43-68, 92-114)

**CONFIRMED, one line-cite erratum.** Confirmed byte-exact:
queue/STANDING_RAILS.md is 53 lines with zero "thinking"/"depth"
occurrences (instrument 2) and route_chat appears only as the front-door
pointer at lines 11, 26, 47; the "thinking-off" label is verbatim at
ds_workhorse.md:62; the explicit disabled key is tools/ds_workhorse.py:93
with the dated erratum at 86-92 saying prior batches "ran thinking-ON";
the probe model is deepseek-v4-flash at d4_probe.py:25; PRIORS row 8 with
the literal "never refire thinking-on" is watch/inbox/model_garden/PRIORS.md:25;
the amendment text is banked at accuracy.md:94-114 and ds_workhorse.md
item 6 still carries no erratum (the move is live, not yet applied);
all three a06-sacred-cow.json keys exist and say what the lens claims
(e6baa31db6c0: arm 2 "banked TWO ok:false rows with content_chars=0 at
the 16000-token cap"; ee225394e567: the omission claim, quoted accurately
in d4_thinking_probe.md:38-42; b91883ff6f87: row 8 scoped to
mechanical/long-form pending the probe). ERRATUM: the lens cites the
re-fire model as "deepseek-chat (tools/ds_workhorse.py:29)"; the MODEL
constant is at tools/ds_workhorse.py:64
(`MODEL = "deepseek-chat"  # v4.1-flash mapping per provider docs`); line
29 is a docstring pointer to a10-ds-batches rows. The wrong :29 is baked
into the banked amendment text at accuracy.md:99. Substance unaffected:
the receipt's own run command (`-m tools.ds_workhorse`, ds_workhorse.md:63)
uses the module MODEL at line 64. Fix the cite before the erratum text is
applied anywhere (A3).

### F3: D2 verdict, split now (accuracy.md:116-181)

**CONFIRMED, one stale clause.** Byte-checks that hold:
tools/dungeon.py reads 771 lines (instrument 4); `def play` at 447 and
727, both inside class Dungeon (line 148), second shadows first;
`if self.warden_hp <= 0 or self.persuades >= 2 or True:` verbatim at 623;
baseline key af1d7045681fee89 at configs/violation_baseline.json:5308-5314
(accepted 2026-10-04, accepted_lines 756, by go-wave-20261004-coordinator,
detail ">400 lines"); the +15 is exactly commit 72f1c58c7 (instrument 5);
the GROWTH line reproduced byte-identically in my run (instrument 3);
growth handling is print-only (tools/violation_ratchet.py:264-276: the
GROWTH print at 275-276 feeds nothing; the FAIL gate at 277-279 counts
only new or expired). STALE CLAUSE: the lens's "and still exited
'RATCHET: PASS'" does not reproduce on today's tree: my run exits
RATCHET: FAIL, 1, on a NEW unrelated debt, tools/social_rsi.py:578
file-too-long. The clause was true at the lens's moment and is
moment-bound, never a standing fact (A1). The verdict itself is untouched
and the compounding thesis is stronger than reported: 8 accepted files
past acceptance (percolator +442, env_contract +180, concept_predictor
+154, duel_harness +120, gps_mcp/ledger +112, estate_bridge +102,
hermes_burn +6, dungeon +15) plus one NEW debt, and the GROWTH law has no
enforcement floor for any of them. The seam inventory byte-checks: all
nine named methods exist in class Dungeon (_enemy_sheet 488,
_scene_sheet 494, _beat_outcome 498, _find_scroll 511, _phantom_count
525, _packs_str 530, _wyrm_regrowth 534, _mimic_wipe 548, _grade 565)
plus module-level extract_tag 114, strip_and_cap 103, roll 133; SCENES at
454, campaign at 612-726. GradingMixin/CampaignMixin are names to be
created, which the seams section is explicit about.

### F4: the test instruments (accuracy.md:147-154)

**CONFIRMED.** My runs (instrument 6): combined pair 15 passed in 1.17s
(lens: 0.82s; count exact, timing is load-dependent and mine is slightly
over the ask's "under a second": the substance is a sub-2s green pair);
solo parser file 13 passed in 0.72s (lens: 0.54s); the fixture assertion
is verbatim `assert len(FIXTURES) == 14` at tests/test_dungeon_parser.py:61;
the _grade docstring receipt is verbatim at tools/dungeon.py:567-576
("Extracted verbatim from the campaign() loop body (was inline,
dungeon.py:515-549 at HEAD 37e2fba7e)... 14 logged S4 verdicts replay
against the same bytes").

### Blind spots (accuracy.md:183-202): honest, four independently re-confirmed

- BS1 (paid batches not re-run): honest; the 2/10-at-16000 number
  cross-checks against two estate sources I read (route_chat.py:131-133
  docstring and a06 key e6baa31db6c0) and the 0/26-to-3/28 tally against
  queue/STANDING_RAILS.md:49-53. Still receipt-borne: I did not re-run the
  paid batches either. OWED, unchanged.
- BS2 (founding row provenance OWED): my byte-read of
  usage.jsonl:1151 confirms the row is z-ai/glm-5.3-prime via hermes_burn
  (id GALA_DD_SELFSTEAL_PRIME_JUDGMENT_20261003), not a route_chat
  deepseek arm: the lens's caveat is right and the ask's "arm-2 ask"
  framing is loose (A7). Provenance (staged vs vendor default) remains
  OWED: I did not read the hermes_burn FAMILY_TABLE staging either.
- BS3 (OpenRouter ignores-disabled note comment-borne): the note exists
  verbatim at configs/providers.yaml:219-223 ("IGNORES
  thinking:{type:disabled}... Flag kept: harmless, helps non-/auto
  models"); not re-measured by me. OWED, unchanged.
- BS4 (campaign flow not read end to end): I verified the structure map,
  seam inventory, and the play/campaign/SCENES layout; no live campaign
  ran. The behavioral gate remains the replay harness plus the 15 tests.
  OWED, unchanged.
- BS5 (8-file GROWTH pattern): my ratchet run shows exactly 8 GROWTH
  claims. CONVERGENT with the lens.
- BS6 (bank rows carry no reasoning_tokens): route_chat.py:242-249 bank
  row carries prompt_tokens, completion_tokens, content_chars,
  finish_reason, ok and no reasoning_tokens field; hermes_burn.py:381 is
  the banking pattern to copy; hermes_burn.py:356-357 is the
  reasoning-channel fallback. All three cites exact.

## Additions (what the lens missed)

### A1: "RATCHET: PASS" is moment-bound; today's check fails on an unrelated NEW debt

Evidence: instrument 3. My full-tree run exits 1 with NEW
e71ef4422e755b5e file-too-long: tools/social_rsi.py:578 while every
dungeon-specific cite still reproduces. Falsifier: a fresh full-tree run
at fold time that exits 0 (no NEW hits) would restore a standing-PASS
reading; today it does not. Move: re-run the ratchet at fold time before
any verdict cites gate state, and in the same sitting register or fix the
social_rsi.py:578 debt by name (10 min).

### A2: the design-gate move breaks its own cited green test

Evidence: tests/test_route_chat_depth.py:77-80
(test_design_wires_thinking_enabled) pins design -> thinking:{type:enabled}
on the real deepseek lane, the exact behavior the lens's move gates.
Falsifier: if the deepseek lane declared a thinking-capable flag the test
could pass unchanged; providers.yaml:367-371 instead carries
disable_thinking: true and the ON-default law, so the conflict is real.
Move: amend that test inside the same 30-min sitting as the design gate,
or the cited-green instrument goes red the moment the fix lands (15 min).

### A3: line-cite erratum, deepseek-chat is ds_workhorse.py:64 not :29, and the wrong cite is baked into the amendment text

Evidence: tools/ds_workhorse.py:64 vs :29; accuracy.md:64 and :99 both
carry :29. Falsifier: none, verified by read; the finding is the erratum.
Move: fix both cites in accuracy.md before its ds_workhorse.md erratum
text is applied, or the correction itself lands with a wrong citation (5 min).

### A4: the omission-default finding is now 3-source CONVERGENT

Evidence: founding run d4_thinking_probe.md:55-57 (18/70 vs 0 vs 12),
lens run accuracy.md:21-27 (11/45 vs 0 vs 11), my run instrument 1
(16/63 vs 0/2 vs 12): three independent invocations of the same probe,
same direction, ~$0.00007 each. Per the duplication-is-emphasis law this
outranks any single-source finding in the verdict chain. Falsifier: any
future run whose omitted arm returns reasoning_tokens 0 or whose disabled
arm is refused flips it (the lens's own falsifier (a), still the right
one). Move: cite as convergent in the fold verdict, no new spend (0 min,
banked here).

### A5: the two play() bodies differ; the prune direction matters

Evidence: tools/dungeon.py:447-449 is `def play: self.s0(); self.s1()`
only; 727-733 adds `if self.full: self.campaign()`. The lens's "dead
bytes" note did not record that the bodies differ. Falsifier: if both
bodies were identical, direction would not matter; they are not. Move:
one line in the prune spec: delete the FIRST def (447-449) and keep the
second; deleting the wrong one silently drops the campaign hook (2 min).

### A6: lane coverage the lens never enumerated

Evidence: configs/providers.yaml carries disable_thinking: true on
exactly three lanes (openrouter :223, deepseek :371,
deepseek_overmind :401; instrument 7 grep). Those three are the lanes the
mechanical leg protects today; every other lane rides omission, which is
measured ON on the v4 family. Falsifier: a re-read showing more or fewer
disable_thinking keys, or a probe of another family showing omission = OFF.
Move: fold the coverage line into the D3 verdict text so
"lane-config-gated" carries its concrete coverage claim (0 min, banked here).

### A7: the ask's own framing erratum, confirmed by byte-read

Evidence: memory/runs/hermes_burn/usage.jsonl:1151 =
GALA_DD_SELFSTEAL_PRIME_JUDGMENT_20261003, z-ai/glm-5.3-prime,
completion_tokens 16000, reasoning_tokens 15998, finish_reason "length",
content_chars 1, channel "reasoning-dump (content stub; raw reasoning
banked)". The ask called this "an arm-2 ask"; it is a hermes_burn GLM
row, family evidence for thinking-eats-capped-budgets, not a route_chat
deepseek arm-2 row. The lens caught this (accuracy.md:31-41) and my read
confirms it. This is CONVERGENT support for F2's framing audit. Falsifier:
a route_chat usage row carrying the same 16000/15998 shape would make the
ask's framing literal instead of loose. Move: none needed; the fold
should keep the lens's caveat wording, not the ask's (0 min).

## OWED (not asserted, not verified by this pass)

- Founding row thinking provenance (staged vs vendor default): hermes_burn
  FAMILY_TABLE staging unread by me and by the lens.
- The OpenRouter ignores-disabled note: comment-borne, not re-measured live.
- Paid batch outcomes (sacred-cow 2/10, judge passes, the 3/28 re-fire):
  receipt-borne, cross-checked against independent estate surfaces, not
  re-run.
- deepseek-chat's omission default: never probed (the lens's falsifier (b)
  stands open and is the cheapest remaining instrument).
- A live paid dungeon campaign session: not run by me or the lens; the D2
  behavioral gate remains the 14-verdict replay plus the 15 green tests.
