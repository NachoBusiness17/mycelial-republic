# logic.md - the instrument-theory lens on the two parked decisions

Lens: instrument theorist. I extract the inference rules the estate actually
runs (0/1/2-exit contracts, trivalent verdicts, alpha-budget promote gates)
and name where instruments are redundant, contradictory, or blind. Every
claim below was read or run THIS sitting, cited path:line or
command:output. No em-dashes. Anything I could not verify is OWED, never
asserted. Universal claims are scoped to the search actually run.

## DECISION 1 (D3): default thinking posture for arm-2/short-output asks

### VERDICT

**Explicit-off on the wire for every depth=mechanical / short-output ask, on
every carrier. Omission is never a posture. Lane config (`disable_thinking`)
is demoted from law to capability attestation. depth=design stays the only ON
path and must be gated on BOTH a lane capability field AND a 32000-token
budget floor.**

Why the three candidate postures rank this way, from the instruments:

1. Omission is measured ON, so "omit and default off" is dead as law.
   watch/inbox/go_wave_20261004/d4_thinking_probe.md:53-62: 3 arms on
   deepseek-v4-flash, $0.00007, arm 3 sanity-proves the param drives state in
   both directions: omitted = 18 reasoning tokens + 70 chars
   reasoning_content on a one-word ask; disabled = 2 completion tokens, no
   reasoning block in usage; enabled = 12 reasoning tokens. providers.yaml
   (deepseek block, comment at configs/providers.yaml:366-371) was right;
   tools/ds_workhorse.py's old "omitting it IS the off state" was wrong and
   now carries a dated erratum plus the wire fix
   (tools/ds_workhorse.py:86-93, `"thinking": {"type": "disabled"}` at :93).
2. Lane-config gating has already failed open twice, so config presence is
   attestation, not enforcement: (a) route_chat carried a
   `disable_thinking: true` lane while never reading the flag until lane 1 of
   go_wave_20261004 wired it (mag/route_chat.py:204-211; the a06-sacred-cow#3
   row, memory/runs/mickey17_v2/runs/run-0/lanes/a06-sacred-cow.json key
   ee225394e567, documents the zero-grep proof); (b) mag/inference_budget.py:75-84
   STILL strips the off switch (`forbidden_keys=("thinking", ...)` at :78)
   while its notes (:84) still teach the refuted omission law. Two of three
   carriers failed the same way: the config existed and the wire did not.
3. Explicit-off everywhere (including design) over-rotates: the sacred-cow
   probe's arm 1 ran 4/4 clean with thinking-ON at the 16000 cap
   (a06-sacred-cow.json rows 1-2, content_chars 12765/6746/17671/16770), so
   ON has measured value at adequate budget. The hollow failure is a BUDGET
   mechanism: reasoning tokens count against max_tokens, so short-output asks
   are arithmetically guaranteed to starve. The founding row
   memory/runs/hermes_burn/usage.jsonl:1151 is the mechanism in its purest
   form: z-ai/glm-5.3-prime, 16000 completion tokens, 15998 of them
   reasoning, finish_reason length, content_chars 1, banked ok:true at a
   $0.2502604 cost. Note precisely: 1151 is a GLM judgment row through
   hermes_burn, NOT a deepseek cow2 row; the deepseek arm-2 hollow rows are
   separately banked (a06-sacred-cow.json row 1 quote: cow2-SUBSTANCE_48h_synthesis,
   content_chars 0, reasoning_chars 59103, completion 16000, ok false). The
   mechanism is cross-family and cross-carrier; the off posture must be
   carrier-enforced, not family-scoped.

So the ONE verdict: depth-gated with an explicit wire floor. Mechanical /
short-output = `thinking:{type:disabled}` sent unconditionally by the carrier
(route_chat, ds_workhorse, hermes_burn), regardless of lane config. Design =
ON only where the lane attests thinking support AND max_tokens >= 32000 (the
route_chat docstring's own number, mag/route_chat.py:135). This is
CONVERGENT with economics.md:8 ("explicit-off on the wire ... Omission is
never a posture") and partially convergent with accuracy.md:13 (same
explicit-off, but carried by lane config; my two-failures-open census is the
argument for carrier enforcement instead).

### Falsifier (what flips this verdict)

A judged, repeated A/B (n>=5 per arm, same max_tokens, same asks) where
thinking-ON renders full material non-inferior to thinking-OFF on
arm-2-shaped asks. The nearest existing counter-evidence does not meet the
bar: arm 1 is n=4, unjudged, and budget-confounded (a06-sacred-cow.json row
2: "an unjudged length ratio against a budget-confounded baseline"). Second
flip family: a funded lane that rejects the `thinking` key on the wire, or a
vendor that does not count reasoning tokens against max_tokens; the verdict's
mechanism premise (reasoning eats the completion budget) breaks there and the
posture would scope to families that conflate the budgets (accuracy.md:59
names the same flip family; CONVERGENT). Third: a live re-run of d4_probe.py
reading omission = zero reasoning_content on v4-flash; accuracy.md:15-19
already re-ran it once this sitting (omitted = 11 reasoning tokens, same
direction), so one deviating re-run would need n>=3 to overturn two
independent confirmations.

### Exact amendment text for the losing law surface

Under this verdict the a06-sacred-cow#2 surface (PRIORS row 8,
watch/inbox/model_garden/PRIORS.md:25, "THINKING OFF MANDATORY ... never
refire thinking-on") loses its ABSOLUTE form: thinking-on is ruled legal for
design at budget, so the row's scope must widen and except at once. Append
to PRIORS.md:25 (append-never-rewrite; DISPUTED-tier operator signature per
the a06#2 steal):

    POST-DATUM 2026-10-04 (ractor logic lens,
    watch/inbox/ractor_engine/2026-10-04-parked-decisions/logic.md): scope
    amended by measurement. The mechanism is family-general, not
    gateway-specific: omission of the thinking key resolves to THINKING-ON on
    api.deepseek.com deepseek-v4-flash
    (watch/inbox/go_wave_20261004/d4_thinking_probe.md:53-62, 3 arms,
    $0.00007; independently re-run live by the accuracy lens), and
    z-ai/glm-5.3-prime burned 15998 of 16000 completion tokens on reasoning
    at content_chars 1 through a different carrier
    (memory/runs/hermes_burn/usage.jsonl:1151). Row 8's verdict STANDS for
    the mechanical/short-output class and widens to every carrier: the off
    state is the explicit wire key thinking:{type:disabled}, never omission,
    never config presence alone. The design exception is legal only at a
    32K+ max_tokens budget on lanes that attest thinking support
    (mag/route_chat.py:127-136); arm 1's 4/4 at a 16000 cap is n=4 and
    unjudged (a06-sacred-cow.json row 2) and does not widen the exception
    further. Status: STILL-VALID, scope amended; DISPUTED-tier operator
    signature remains owed.

And the winning surface's one ungated defect (accuracy.md:16 names it too,
CONVERGENT): mag/route_chat.py:212-213 sends `thinking:{type:enabled}` on
design to EVERY lane with no capability check and no budget floor, exactly
the shape that produced arm 2's 2/10 zero-content rows at the 16000 cap.
Replace lines 212-213 with:

    if depth == "design":
        if not lane_cfg.get("supports_thinking"):
            raise ValueError(
                f"route_chat: lane {lane} does not attest thinking support; "
                "depth='design' refused")
        if max_tokens < 32_000:
            raise ValueError(
                "route_chat: depth='design' needs max_tokens >= 32000; "
                "reasoning burns the completion budget (2/10 zero-content at "
                "a 16000 cap, a06-sacred-cow#0; d4_thinking_probe.md)")
        body_obj["thinking"] = {"type": "enabled"}

plus `supports_thinking: true` on the deepseek/hermes-thinking blocks in
configs/providers.yaml, and two new cases in tests/test_route_chat_depth.py
(design without capability raises; design under 32000 raises). My depth
instrument check this sitting: `pytest tests/test_route_chat_depth.py
tests/test_route_chat_banks.py -q` = 6 passed in 1.43s.

## The contradiction the fold must also carry (still live)

**mag/inference_budget.py:75-84 is an active think-enabler teaching a
refuted law.** Row 1 (`key="deepseek"`, :75) sets `thinking_control={}` and
strips `thinking` via `forbidden_keys` (:78), which forces the omitted-key
body = the measured ON state, while its notes (:84) still read "omitting it
IS the off state (AH10)" and its notes cite tools/ds_workhorse.py:50-60 as
source. The d4 receipt assigned this fix ("Fix owed there too",
d4_thinking_probe.md consequence 2); it is unfixed as of this sitting. One
sitting: flip the recipe to send the explicit disabled key (or stop stripping
`thinking` and let the carrier set it), rewrite the notes naming the d4
probe, replay `pytest tests/test_inference_budget.py -q` (my run this
sitting: 19 passed in 0.97s; the recipe flip will need its assertions
updated, so run it after the edit).

## The re-fire's posture label is unevidenced (OWED, not asserted)

ds_workhorse.md item 6 (watch/inbox/go_wave_20261004/ds_workhorse.md:62)
headlines the v3 refire "uncapped, thinking-off, file-backed". The bytes do
not carry a posture: frontier_delta_results_v3.jsonl row 1 reads
`{"id": "delta-BARFIGHT_spec", "model": "deepseek-chat", "ok_api": true,
"ok_material": true, ...}` with NO thinking or reasoning_tokens field; the
run rode tools.ds_workhorse directly (its command, ds_workhorse.md:63-66),
not route_chat; ds_workhorse.py:86-92's own landed comment says "every batch
before the erratum ran thinking-ON"; and the explicit disabled key landed in
the body only after the d4 erratum (d4_thinking_probe.md consequence 1
explicitly folds the item-6 refire into the rode-thinking-ON census). Also
the refire model is the `deepseek-chat` alias (ds_workhorse.py:64, "v4.1-flash
mapping per provider docs"), and the omission default is MEASURED only on
`deepseek-v4-flash` (d4 probe); the alias's omission default is UNMEASURED.
Therefore the 0/26 -> 3/28 movement is attributable to the CAP removal (the
2000-token override + 6000-char slice, deleted per ds_workhorse.md:51-57),
not to a thinking toggle, and the ask's framing "thinking-off scored 3/28"
is not byte-backed. One sitting, ~$0.0001: run the 3-arm d4 probe against
MODEL=deepseek-chat, stamp the measured posture into
watch/inbox/frontier_delta_register_20261003.json meta, and annotate the
item-6 "thinking-off" phrase in ds_workhorse.md as OWED-then-measured.

## DECISION 2: tools/dungeon.py, split now or keep the debt

### VERDICT

**Accept-the-debt-standing, with a re-stamp at the current 771 lines, one
free rider (delete the shadowed duplicate `play()`), and a pre-registered
split trigger naming the seam.** CONVERGENT with economics.md:122 and
operations.md:21; the dead-method finding is CONVERGENT with dogfood.md F4.

Reasoning a reviewer can re-derive, each leg independently checked this
sitting:

1. The debt is already accepted by name, and the growth law is the standing
   meter, so "keep standing" is not free but is also not unguarded.
   configs/violation_baseline.json:5313 registers tools/dungeon.py; my full
   ratchet run `python tools/violation_ratchet.py check` prints "GROWTH
   claim af1d7045681fee89: tools/dungeon.py accepted at 756 lines, now 771
   (+15) - re-audit or re-accept by name" and "RATCHET: PASS - no
   unregistered debt". The file cap is 400 (tools/violation_ratchet.py:44).
   So the debt CANNOT silently grow: every audit re-flags it. The B2-273
   growth law is the instrument that makes a split-now urgent-only-if-growing;
   operations.md:24-25 shows the +15 is hardening (their git evidence: 3
   commits after acceptance d349ce7d2), not sprawl.
2. The replay pin that makes a split cheap PERSISTS, so splitting now buys
   nothing that splitting at the trigger will not. tests/test_dungeon_parser.py
   replays the 14 logged S4 verdicts against `Dungeon._grade()`
   (tools/dungeon.py:565) and imports the live module
   (tests/test_dungeon_parser.py:26, `from tools import dungeon`). My run of
   the receipt's own instrument: `pytest tests/test_dungeon_parser.py
   tests/test_burn_id_uniqueness.py -q -p no:cacheprovider` = **15 passed in
   1.19s**. Instrument arithmetic (quantifier law): 15 = 13 parser + 2
   burn-id, and it reproduces ONLY under the receipt's pair command
   (dungeon.md:49); the ask's "under a second" is off by 0.19s on my run;
   operations.md:24 got 13 (file alone) and 16 (-k dungeon suite-wide) from
   its two instruments. Name the instrument when citing the count.
3. The scarcest resource this sitting is a landed wire fix, not churn with
   zero behavior change. economics.md:124-126 prices the D3 leak at $0.46
   per hollowed double judgment (usage.jsonl:1151 + :1152, its read); a split
   spends the same sitting on provable no-op movement. The estate's own
   descent law: cheap-first, one landed deliverable per premium turn.
4. The one defect that MUST NOT ride the debt standing is the shadowed
   duplicate entrypoint: `play` is defined twice in class Dungeon at
   tools/dungeon.py:447-449 and :727-731 (AST census this sitting: DUP
   METHODS: {'play': [447, 727]}, 23 methods, one class at :148); Python
   keeps the last, so :447 is dead and any future edit landing there
   silently no-ops. Three deleted lines, zero behavior change, pinned by the
   1.19s suite plus the dry smoke (dungeon.md:51). Fold it into the
   re-stamp sitting.
5. The seam is named NOW so the trigger is executable, not vibes: move the
   S2-S4 campaign engine (SCENES through the second `play`, current
   dungeon.py:451-731: _enemy_sheet, _scene_sheet, _beat_outcome,
   _find_scroll, _phantom_count, _packs_str, _wyrm_regrowth, _mimic_wipe,
   _grade, campaign) into tools/dungeon_campaign.py; keep strip_and_cap /
   TAG_RE / extract_tag / roll in dungeon.py; have play() import the campaign
   lazily inside the method (breaks the import cycle; the S0/S1 dry path
   never pays it); re-export moved names from tools/dungeon.py so the
   `from tools import dungeon` test contract (:26) and
   tools/prepush_golden_vector.py hold unchanged. Blast radius checked: the
   mag/game_*.py and mag/primer.py hits in my importer grep import
   `mag.dungeon_dev`, a different surface (dungeon.md:70 says the same), so
   the real importers are prepush_golden_vector + the three test files.
   Trigger: split when EITHER the open a02#3 de-globbed DM retry leg lands
   (dungeon.md:65, the next engine growth) OR the file crosses 800 lines,
   whichever comes first; acceptance gate = the 15-test pair plus the dry
   smoke, and any changed verdict aborts the split.
6. Falsifier for this verdict: if the replay pair goes red or any of the 14
   logged verdicts changes under the riders, the accept-standing call is
   wrong and the file is split immediately instead. Second falsifier: a
   fourth feature landing in the engine inside one week (growth >30
   lines/week sustained) would falsify operations.md's "slow and
   hardening-shaped" premise and pull the trigger early.

## Citation corrections the synthesis must carry (quantifier law)

1. The ask locates the "route_chat depth law in queue/STANDING_RAILS.md". I
   read STANDING_RAILS.md in full (54 lines) and grepped it: zero hits for
   "thinking" and "depth". The depth law lives at mag/route_chat.py:127-136
   (docstring) and :204-213 (wire). The nearest rails text is the Law-1
   phrase "per-lane call laws" (queue/STANDING_RAILS.md:11-12, the surface
   economics.md:18 cites) and the ds re-fire debt note
   (queue/STANDING_RAILS.md:49-53, which carries the 3/28 tally WITHOUT any
   thinking-off claim; only ds_workhorse.md:62 headlines the posture).
2. usage.jsonl:1151 is a glm-5.3-prime GALA DD selfsteal judgment row
   (hermes_burn carrier), not a sacred-cow arm-2 row; the arm-2 hollow rows
   are deepseek cow2 rows quoted in a06-sacred-cow.json row 1. Both prove
   the same budget mechanism; they are different carriers and the synthesis
   should not merge them into one artifact class.
3. The ratchet `check --changed` in this working copy scoped 0 files (no
   git-diff basis here; output verbatim: "scope=0 changed files; hits=0"),
   so the receipt's "NEW debt blocks pre-push" state (dungeon.md:64) is
   receipt-trusted, not re-proven by me; my full-tree `check` run is the
   instrument that DID reproduce the registered-debt + growth state.

## Blind spots (what this lens could not see)

1. I did not re-run the live d4 probe myself; my omission-default leg rests
   on the founding receipt's verbatim usage blocks plus the accuracy lens's
   independent live re-run. Vendor-side behavior drift between those runs
   and now is invisible to me.
2. I ran the named dungeon pair (15 tests) and the route_chat depth+banks
   pair (6 tests) and inference_budget (19 tests); I did NOT run the full
   suite (census 4,358) or tests/test_route_chat_fence.py, so my proposed
   design-leg gate is verified against 6 route_chat tests, not the fence
   path.
3. The split trigger thresholds (800 lines, next engine leg) are my
   proposal; they are not operator-ratified, and the alpha for "how much
   growth justifies churn" is a judgment call this lens cannot measure, only
   pre-register.
4. I read the verdict heads of the sibling lenses (accuracy, economics,
   operations, dogfood excerpts) for convergence flags, not their full
   bytes; a divergence hiding deeper in those files would be missed by my
   CONVERGENT labels.
5. The deepseek-chat alias omission default is unmeasured (my F3 move closes
   it); until then, the refire-posture question stays OWED and any D3
   argument built on the 3/28 arm's thinking state is built on sand.
6. I did not verify the git archeology operations.md cites (acceptance
   commit d349ce7d2, the three follow-on commits); the harness reports this
   working copy as not a git repository and my ratchet --changed run
   scoped 0 files, so commit-level claims remain theirs, not mine.
