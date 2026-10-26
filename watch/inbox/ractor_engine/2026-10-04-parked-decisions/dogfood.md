# dogfood lens - the two parked decisions (2026-10-04)

Lens: organ mapper. Question for every finding: is the estate's own medicine
actually swallowed, or is it a receipt filed next to a patient who never took
it? Instruments run THIS sitting (all via `.venv/Scripts/python.exe` after one
bare-`python` seat-law trip at the start, AGENTS.md python-env law):

1. `pytest tests/test_dungeon_parser.py tests/test_burn_id_uniqueness.py -q -p no:cacheprovider` -> **15 passed in 1.19s** (the dungeon receipt's own instrument, rerun by me).
2. `python tools/violation_ratchet.py check` (full tree, no --changed) -> `RATCHET: PASS` plus **8 GROWTH claim lines**, incl. `GROWTH claim af1d7045681fee89: tools/dungeon.py accepted at 756 lines, now 771 (+15) - re-audit or re-accept by name`.
3. mtime census: `memory/runs/ds_batches/frontier_delta_results_v3.jsonl` = 2026-10-04T08:38:32Z; `watch/inbox/go_wave_20261004/d4_probe.py` = 10:00:41Z; `tools/ds_workhorse.py` (fix landing) = 10:11:38Z.
4. Reads: queue/STANDING_RAILS.md (full 53 lines), mag/route_chat.py (full 273), mag/inference_budget.py:55-104, tools/ds_workhorse.py thinking lines, watch/inbox/model_garden/PRIORS.md:22-27+56-57, memory/runs/mickey17_v2/runs/run-0/lanes/a06-sacred-cow.json (all 5 rows + verdict, venv json parse), memory/runs/hermes_burn/usage.jsonl:1145-1160, watch/inbox/go_wave_20261004/{d4_thinking_probe.md,ds_workhorse.md,dungeon.md}, tools/dungeon.py structure census + targeted reads.

## DECISION 1 (D3) VERDICT: depth-gated explicit-off; omission is banned as a posture

**The default thinking posture for arm-2/short-output asks is: an explicit
`thinking:{type:disabled}` byte on the wire for depth=mechanical on every
thinking-capable lane; `depth=design` stays legal but only with an explicit
`thinking:{type:enabled}` plus a >=32000 max_tokens budget, gated on a lane
capability field.** Omission must be named in law as NOT an off state.

Why depth-gated and not the other two, from bytes I read:

- Not explicit-off everywhere: the judgment tier is built on thinking models
  (PRIORS.md:22 row 5 glm-prime judgment, PRIORS.md:44 row 27 routing law), and
  the same usage.jsonl:1151 judgment ask RE-RAN clean at STAGE_B (line 1152:
  14759 completion tokens, reasoning_tokens 9826, finish stop, ok true) once
  the budget fit the thinking. The hollowing is a budget-shape failure, not a
  proof that thinking is worthless on judgment asks.
- Not lane-config-gated alone: the same lane needs disabled (mechanical) and
  enabled+32K (design), which a per-lane boolean cannot express; and lane
  config is exactly what let two organs drift apart (finding 2 below).
- The measured core, all read this sitting: d4_thinking_probe.md:53-57 table
  (omitted key -> reasoning_content 70 chars / 18 reasoning tokens on a
  one-word pong; explicit disabled -> 2 completion tokens, no reasoning block;
  enabled -> reasoning 46 chars; arm 3 is the both-directions sanity arm).
  memory/runs/hermes_burn/usage.jsonl:1151: glm-5.3-prime arm at the 16000 cap
  banked reasoning_tokens 15998, finish length, content_chars 1 - the burn is
  cross-family. a06-sacred-cow.json row e6baa31db6c0: arm 2 banked 2/10
  zero-content at exactly 16000, 7/14 cap-pinned.

**Falsifier:** a live 3-arm probe (the d4 shape, judge-scored) on any
thinking-capable lane where a mechanical/short ask with explicit
`thinking:{type:disabled}` scores materially worse than omission, or any lane
that errors on the disabled key (making explicit-off unsendable). Either
result flips the verdict to per-lane capability-gated posture. I ran no live
probe myself this sitting; the verdict rests on the banked d4 probe receipt
plus ledger rows, and re-running it costs ~$0.00007 per d4_thinking_probe.md:26-28.

**Amendment text for the losing law surface (PRIORS.md:25 row 8, status cell
"STILL-VALID (byte-confirmed mechanism, never refire thinking-on)"), append
never rewrite:**

> AMENDED 2026-10-04 (ractor D3, watch/inbox/go_wave_20261004/d4_thinking_probe.md
> + memory/runs/hermes_burn/usage.jsonl:1151): "never refire thinking-on" scopes
> to mechanical/short-output asks. Omission is NOT the off state (deepseek
> 3-arm probe: an omitted thinking key banked reasoning_content and 18 reasoning
> tokens on a one-word ask; explicit thinking:{type:disabled} banked 2 completion
> tokens). Thinking-on stays legal at depth=design with an explicit thinking
> object and a >=32000 max_tokens budget (16000-cap arms banked 2/10
> zero-content rows; a glm prime judgment at the 16000 cap banked 15998
> reasoning tokens and content_chars 1). The byte-confirmed mechanism stands;
> the absolute ban downgrades to: never refire thinking-on without an explicit
> thinking object and a design-tier budget.

**Pointer rot in the topic itself:** the brief names "the route_chat depth law
in queue/STANDING_RAILS.md". grep -i "depth|thinking|route_chat" over that file
hits only :11 (front-door mention), :26 (drop-in row), :47 (debt note) - there
is no depth law byte in STANDING_RAILS.md. The operative depth law lives in
mag/route_chat.py:127-141 (docstring + enum) and :204-213 (wire). Worse, the
drop-in row a dropper-in actually reads (STANDING_RAILS.md:26) carries zero
thinking-posture bytes: the rails surface is silent on the exact law D3
settles. Companion amendment, one clause on STANDING_RAILS.md:26:
"depth=mechanical sends explicit thinking:{type:disabled} on thinking lanes
(omission is NOT off, d4_thinking_probe.md); depth=design enables it, budget
>=32000".

## DECISION 2 (dungeon) VERDICT: split now, ONE seam, verbatim move; do not re-accept

**Split the pure rules layer out of tools/dungeon.py into
tools/dungeon_rules.py in one sitting (verbatim move + re-export), delete the
dead shadowed `play`, keep `Dungeon` as the I/O carrier.** Reviewer-derivable
reasoning:

1. The debt is compounding, not parked: accepted 2026-10-04 at 756 lines
   (configs/violation_baseline.json:5309-5316, `accepted_lines: 756`, by
   go-wave-20261004-coordinator); the ratchet's B2-273 growth law
   (tools/violation_ratchet.py:264-276) printed `now 771 (+15)` on my full
   check this sitting. The file blew past its accepted size the same day.
2. The safety net exists and is fast: the parser was already extracted
   verbatim into `Dungeon._grade()` (dungeon.md:11) and my rerun of the
   receipt's own instrument read **15 passed in 1.19s**. The verbatim-move
   pattern is proven on this exact file, this wave.
3. The file already exceeds single-file review capacity: `Dungeon.play` is
   defined twice in one class, tools/dungeon.py:447-449 (dead, silently
   shadowed) and :727-731 (live, adds campaign on --full). A reader at :447
   believes --full is a no-op. Nothing caught this; the split surface is where
   it lives.
4. The seam is pre-cut by the tests: the pure layer (strip_and_cap :103,
   extract_tag :114, roll :133, check_golden :137, SCENES :454,
   _enemy_sheet/_scene_sheet/_beat_outcome/_find_scroll/_phantom_count/
   _packs_str/_wyrm_regrowth/_mimic_wipe :488-563, _verdict :243, _grade :565)
   is I/O-free and is exactly what tests/test_dungeon_parser.py replays.
   Importer census (grep this sitting): only tests/test_dungeon_parser.py,
   tests/test_burn_id_uniqueness.py, tools/prepush_golden_vector.py,
   tests/test_prepush_golden_vector.py - all import via tools.dungeon public
   names, so re-exports keep every importer green untouched.
5. Honest cost: one seam does NOT clear the >400-line ratchet rule (carrier
   lands ~540). The file stays registered debt; what changes is that the
   churn-prone logic layer stops compounding into the carrier. The second seam
   (campaign engine :612-733) is a follow-up only if the GROWTH line re-fires.

**Falsifier:** if the verbatim move cannot keep 15/15 parser + burn-id tests
and the golden-vector pre-push instrument green in the sitting (plus the dry
smoke dungeon.md:51 documents), `git checkout` the move and accept the debt
standing with a fresh `baseline-update --by` re-stamp; that outcome falsifies
"the split is a one-sitting safe move" and justifies standing debt until churn
settles.

## Findings (the filed-but-never-wired census)

**F1. The erratum landed in one of its two wrong-source organs.**
tools/ds_workhorse.py:86-93 now carries the dated erratum and sends explicit
`"thinking": {"type": "disabled"}`. mag/inference_budget.py:73-77 still carries
`thinking_control={}` with `"thinking"` in forbidden_keys (the harness strips
the off-switch and sends default = ON per the d4 measurement), and :83-84 still
asserts "omitting it IS the off state (AH10)" - the exact claim
d4_thinking_probe.md:8-9 marked WRONG. Any model-garden/budget run on deepseek
rides thinking-ON while its own notes claim off. Falsifier: a byte-read of
inference_budget.py:69-93 showing an explicit disabled object in
thinking_control (absent today; I read it). Move: one-sitting row fix plus
dated erratum comment, then `pytest tests/test_inference_budget.py -q`.

**F2. The 3/28 "uncapped" ds arm rode thinking-ON; its receipt label is
wrong. CONVERGENT with d4_thinking_probe.md:78-81 (consequence 1), which I
independently re-derived from mtimes:** frontier_delta_results_v3.jsonl written
08:38:32Z, d4_probe.py landed 10:00:41Z, the ds_workhorse fix 10:11:38Z. The
refire predates both, so omission = thinking-ON by the probe's own finding.
ds_workhorse.md:62 labels the run "uncapped, thinking-off, file-backed" - the
thinking-off word is false for that run. The tally itself stands (capability,
not cap), and the capability conclusion actually strengthens: a thinking-ON
uncapped arm still went 3/28. Falsifier: a send-time wire log of the v3 batch
showing a thinking object present (no such log exists; the batch predates the
fix). Move: one erratum line in ds_workhorse.md item 6 and a law-note that no
surface may inherit "thinking-off" for the v3 arm (STANDING_RAILS.md:49-53 is
clean: it says "uncapped" only).

**F3. The accepted dungeon debt is already stale by the estate's own
instrument.** My full `violation_ratchet.py check` printed the GROWTH line for
tools/dungeon.py (756 -> 771, +15) and PASSed anyway: growth is a print, not a
block. Dungeon is 1 of 8 GROWTH claims in that one run (percolator.py +442,
env_contract.py +180, concept_predictor.py +154, duel_harness.py +120,
gps_mcp/ledger.py +112, estate_bridge.py +102, hermes_burn.py +6), so the
accept-by-name valve is becoming a parking lot estate-wide. Scope: one full
check, this sitting, this tree. Falsifier: a re-run printing no GROWTH line for
dungeon.py. Move: the D2 split above; separately, the coordinator should
re-audit or re-stamp all 8 names, not just dungeon.

**F4. Dead shadowed method in the live carrier.** tools/dungeon.py:447-449 vs
:727-731, details under D2. Falsifier: grep showing one `def play` in class
Dungeon, or a documented intentional re-bind (none exists in dungeon.md or the
a02 lane rows I read). Move: delete :447-449 in the split sitting; net is the
1.19s suite plus the dry smoke (dungeon.md:51).

**F5. The rails drop-in surface is silent on the thinking posture.**
STANDING_RAILS.md:26 (the row droppers-in read) names route_chat's outputs but
not its posture; the law lives in module docstring bytes a drop-in user never
opens. Falsifier: a grep of STANDING_RAILS.md for "thinking" returning a hit
(today it returns none). Move: the one-clause amendment quoted under D3.

## Blind spots

- No live API probe this sitting: the thinking-default verdict rests on the
  banked d4 receipt and ledger rows, not a probe I paid for.
- I read dungeon.py's structure census plus targeted ranges (:440-484,
  :724-771), not all 771 lines; other latent defects could sit in the unread
  middle (campaign :612-733).
- I did not recount the 3/28 judge tally bytes; delta_judge_results_v3.jsonl is
  taken on receipt, not recounted.
- mtimes are write-moments by assumption; an out-of-band touch could in
  principle disturb the F2 ordering (no evidence of one).
- Ownership of the inference_budget fix is unresolved: d4_thinking_probe.md:85
  assigns it to "the a10-ds-batches owning lane"; I did not confirm who holds
  that claim, and STANDING_RAILS.md:26-27 is a sibling-claimed surface this wave.

## ERRATUM 2026-10-04 (second pass): the D2 split verdict is WITHDRAWN as specified

The hostile second pass verdicted finding-3 (D2 split now, one verbatim
pure-rules seam) weakened, and re-reading the bytes sustains it on every
count. Corrections, all verified this pass:

1. WITHDRAWN: "the pure layer (… _verdict :243, _grade :565 …) is I/O-free".
   False. _verdict binds self.tip/self.turn (:246) and mutates self.pc_hp
   (:256), self.claims (:259), the module global ROSTER (:267; ROSTER defined
   :44), self.warden_hp (:274), self.persuades (:282), self.audits (:295),
   self.ledger_audits (:297). _grade binds self.tip/turn (:578) and mutates
   self.last_roll (:579) and self.root_anchors (:601-602). _mimic_wipe reads
   self.last_verdict (:558). None of the three is verbatim-movable; their
   extraction is an explicit-state refactor, out of one-sitting scope.
2. WITHDRAWN: the "~540 residual" arithmetic. Measured this pass: the truly
   pure verbatim set is the module band :103-145 (strip_and_cap, TAG_RE,
   extract_tag, roll, check_golden; 43 lines), SCENES :454-486 (33), and the
   seven self-cosmetic or static methods :488-546 (59 lines; _enemy_sheet/
   _scene_sheet read only self.SCENES, _wyrm_regrowth's self is delegation
   only) = ~135 lines. Residual = 771 - 135 ~= 636, still over the 400 cap
   (tools/violation_ratchet.py:44). The debt survives any one-sitting split.
3. NEW decisive byte my first pass missed: tools/prepush_golden_vector.py:50-63
   pins 7 of its 11 tokens to bytes that live in SCENES (:454-486) and the
   campaign band, with DEFAULT_TARGET "tools/dungeon.py" (:43). I ran it this
   pass: `GOLDEN-VECTOR: ok - 11/11 golden tokens in tools/dungeon.py` exit 0.
   Moving SCENES without retargeting the vector lands the split with a red
   pre-push instrument whose own contract reads "a token that stops matching
   means the law it pins left the bytes" (:48-49).

CORRECTED D2 VERDICT: accept-the-debt-standing, respecified. (a) Re-stamp the
baseline entry at the measured 771 today (baseline-update --by, honest count;
my ratchet rerun this pass reproduces `GROWTH claim af1d7045681fee89: tools/
dungeon.py accepted at 756 lines, now 771 (+15)`). (b) Delete the dead
shadowed play (:447-449) now - behavior-identical (Python last-wins), net is
my rerun `15 passed in 1.18s` plus the dry smoke. (c) The rules/engine split
is DEFERRED behind a named precondition: retarget prepush_golden_vector.py to
the new module (or split the vector across both files) in the same sitting,
which is a coordinator-gated pairing touching a sibling-owned WARN-ONLY
instrument (receipt watch/inbox/go_wave_20261004/prepush_instruments.md), not
a lens one-sitting move.

TIGHTENED FALSIFIER: the deferred-split ruling flips to split-now iff (1) the
golden vector is retargeted first (or its owner co-signs the sitting) and (2)
the pure-set census above re-verifies at ~135 lines before the move. Any
claim that a one-sitting split clears the 400-line cap is falsified by the
measured ~636 residual. Instruments rerun under this pass: prepush_golden_vector.py (11/11, exit 0), pytest tests/test_dungeon_parser.py
tests/test_burn_id_uniqueness.py -q (15 passed in 1.18s), violation_ratchet.py
check (GROWTH line reproduced).
