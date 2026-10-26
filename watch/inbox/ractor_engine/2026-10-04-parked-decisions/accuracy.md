# accuracy lens - the two parked decisions, byte-checked 2026-10-04

Lens: falsifier-hunter. Every claim below names what I read or ran THIS session.
No em-dashes. Anything I could not verify is marked OWED.

## DECISION 1 (D3): default thinking posture for arm-2 / short-output asks

### VERDICT

**Lane-config-gated EXPLICIT-OFF.** Omission is never the off state. Any ask
whose budget is small against the model's reasoning appetite (arm-2 shape)
sends the explicit off key on the wire, driven by the lane's
`disable_thinking` config flag; `depth="design"` is the only override and must
be capability-gated; budget sizing stays mandatory on lanes that ignore the
off switch. The landed mechanism (mag/route_chat.py:204-213) is the right
verdict and carries one ungated defect: the design leg.

### The evidence, independently reproduced

1. The omission default is measured and I reproduced it live this session.
   Command: `./.venv/Scripts/python.exe watch/inbox/go_wave_20261004/d4_probe.py`
   (3 live arms, ~$0.00007). My run: arm omitted = reasoning_tokens 11,
   reasoning_content 45 chars, head "We need answer single word pong. Need
   comply."; arm disabled = 0 reasoning, completion_tokens 2, no
   completion_tokens_details; arm enabled = 11 reasoning tokens. Direction
   identical to the founding receipt
   (watch/inbox/go_wave_20261004/d4_thinking_probe.md:53-62: 18/70 vs 0 vs 12).
   Sampling variance only. The probe's arm-3 sanity logic holds: the param
   drives the state in both directions, so omission is the default state, ON.

2. The founding budget-eating row byte-checks: memory/runs/hermes_burn/
   usage.jsonl:1151 = GALA_DD_SELFSTEAL_PRIME_JUDGMENT_20261003, model
   z-ai/glm-5.3-prime, completion_tokens 16000, reasoning_tokens 15998,
   finish_reason "length", content_chars 1, channel "reasoning-dump (content
   stub; raw reasoning banked)". Accuracy caveat the ask's framing misses:
   this row is GLM via hermes_burn, not deepseek via route_chat. It proves
   the failure FAMILY (thinking eats capped budgets, content dies), not the
   omission default. tools/hermes_burn.py:356-357 shows the carrier falls
   back to dumping reasoning when content is empty, consistent with the row.
   Whether that call's thinking was requested by staging or rode a vendor
   default is UNVERIFIED (hermes_burn FAMILY_TABLE staging not read): OWED.

3. The two law surfaces named in the ask are mis-cited. queue/STANDING_RAILS.md
   was read in full (53 lines): it carries NO route_chat depth law and zero
   occurrences of "thinking" or "depth" as law; route_chat appears only at
   lines 11, 26, 47 as the front-door/drop-in pointer. The depth law lives in
   the module itself: mag/route_chat.py:127-141 (docstring: enum, scoped
   arm-1/arm-2 numbers, budget guidance) and mag/route_chat.py:204-213 (the
   wire). The actual disagreeing pair per estate bytes is PRIORS row 8
   (watch/inbox/model_garden/PRIORS.md:25, "STILL-VALID (byte-confirmed
   mechanism, never refire thinking-on)") versus the depth=design override.
   The d4 receipt already rules the mechanism question: the probe CONFIRMS
   row 8's mechanism (arm 2 of the sacred-cow probe: 2/10 zero-content at
   exactly 16000 tokens, a06-sacred-cow.json key e6baa31db6c0, quote row
   byte-read) and REFUTES only the omission-as-off claim (a06 key
   ee225394e567).

4. The 3/28 vs 0/26 re-fire is a BUDGET-axis result, not a thinking-axis
   result. watch/inbox/go_wave_20261004/ds_workhorse.md:62 labels the re-fire
   "thinking-off", but it ran with the thinking key OMITTED: the explicit
   `"thinking": {"type": "disabled"}` landed at tools/ds_workhorse.py:93 only
   AFTER the probe (erratum comment at tools/ds_workhorse.py:86-92 says the
   prior batches "ran thinking-ON"). And the re-fire's model is "deepseek-chat"
   (tools/ds_workhorse.py:29), which the probe never tested (it tested
   deepseek-v4-flash). The "thinking-off" label on the 3/28 receipt is
   therefore UNVERIFIED: OWED. What the re-fire actually proves: a 2000-token
   harness cap scored 0/26 and the vendor-default budget scored 3/28
   (STANDING_RAILS.md:49-53 carries the corrected tally).

5. The winner surface carries one ungated leg. route_chat.py:212-213 sends
   `thinking:{type:enabled}` to EVERY lane when depth="design", while the
   docstring at route_chat.py:127-128 claims "where the lane supports it".
   a06-sacred-cow.json (key ee225394e567) named exactly this gap pre-wiring;
   the wiring closed disable_thinking and the enum (route_chat.py:137-141,
   tests/test_route_chat_depth.py:61-89 covers enum + both wire forms + the
   omission case) but left design ungated by lane capability.

### Falsifier

The verdict flips if any of these measure true: (a) a re-run of d4_probe.py
where the omitted arm returns reasoning_tokens 0 (vendor flipped the default)
or the disabled arm errors (the off key refused); (b) a probe of the
deepseek-chat alias showing omission = OFF, which would restore the 3/28
"thinking-off" label and narrow the ON-default finding to deepseek-v4-flash;
(c) a lane where explicit `thinking:{type:disabled}` degrades short-output
material at matched budget versus omission. Today all three are false by my
own run. Note the boundary case: providers.yaml:220-223 records an OpenRouter
deepseek variant that IGNORES thinking:{type:disabled} ("Flag kept: harmless,
helps non-/auto models"), not re-measured today: on that surface explicit-off
is necessary but NOT sufficient and the budget law is the backstop.

### Amendment text for the losing law surfaces

To ds_workhorse.md item 6, append:
"ERRATUM 2026-10-04 (accuracy lens): the 'thinking-off' label on this re-fire
is unverified. The run carried NO thinking key (omission); omission is
measured ON for deepseek-v4-flash
(watch/inbox/go_wave_20261004/d4_thinking_probe.md) but this batch ran model
deepseek-chat (tools/ds_workhorse.py:29), never probed. The 0/26 vs 3/28
delta is a budget-axis result (harness 2000 cap vs vendor default), not a
thinking-axis result. The explicit disabled key landed post-run at
tools/ds_workhorse.py:93."

To PRIORS row 8 (watch/inbox/model_garden/PRIORS.md:25), append the post-datum
the a06 lane itself prescribed (a06-sacred-cow.json key b91883ff6f87):
"POST-DATUM 2026-10-04: mechanism re-confirmed upstream (sacred-cow arm 2:
2/10 zero-content at exactly 16000 tokens; omission default ON measured live,
d4_thinking_probe.md). 'Never refire thinking-on' narrows from a model law to
a budget law: mechanical/short-output sends explicit thinking:{type:disabled}
on lanes carrying disable_thinking (route_chat.py:204-211); design-depth may
run thinking-ON only on lanes declaring thinking capability, at 32K+
(mag/route_chat.py:135-136; the vendor thinking-mode default is 64K)."
Per the append-never-rewrite law the a06#3 omission claim itself stays
unrewritten; the d4 receipt is its erratum carrier.

## DECISION 2: tools/dungeon.py, split or keep the debt

### VERDICT

**SPLIT NOW, two mixins + dead-code prune, gated by the existing replay
harness.** Not a rewrite: a method-granularity lift that keeps self
references verbatim.

### The reasoning, re-derivable

1. The debt is real and already compounding: configs/violation_baseline.json
   (key af1d7045681fee89) accepted tools/dungeon.py at `accepted_lines: 756`,
   `by: go-wave-20261004-coordinator`, rule `file-too-long`, 2026-10-04. The
   file reads 771 lines today (wc -l). The +15 is commit 72f1c58c7 (3-strike
   void breaker), landed hours after acceptance.
2. The gate cannot hold the line: my full-tree run
   `./.venv/Scripts/python.exe tools/violation_ratchet.py check` printed
   "GROWTH claim af1d7045681fee89: tools/dungeon.py accepted at 756 lines,
   now 771 (+15)" and still exited "RATCHET: PASS" (growth is print-only,
   tools/violation_ratchet.py:272-281). The same run showed SEVEN more
   accepted files growing (percolator.py +442, env_contract.py +180,
   concept_predictor.py +154, duel_harness.py +120, gps_mcp/ledger.py +112,
   estate_bridge.py +102, hermes_burn.py +6). Keeping the debt means keeping
   a claim with no enforcement floor behind it.
3. The file is accreting structure, not just length: `def play` exists twice
   (tools/dungeon.py:447 and :727, both inside class Dungeon); Python keeps
   the second, so the 447 body (s0+s1) is dead bytes. And
   tools/dungeon.py:623 reads `if self.warden_hp <= 0 or self.persuades >= 2
   or True:` where the first two disjuncts are dead (always true via the
   third). Dead code inside a live hourly-cron carrier is the cost the debt
   note ("": empty) never priced.
4. The split risk is bounded by instruments that already exist and that I ran
   this session: `pytest tests/test_dungeon_parser.py tests/test_burn_id_uniqueness.py -q`
   = **15 passed in 0.82s**. The "14/14" claim is the fixture count
   (tests/test_dungeon_parser.py:61 `assert len(FIXTURES) == 14`) replayed by
   13 test functions against Dungeon._grade (tools/dungeon.py:565-610, whose
   docstring carries the verbatim-extraction receipt at HEAD 37e2fba7e and
   the two fixed defects). The ask's "15 dungeon tests pass in under a
   second" verifies exactly, with the file split named.

### The seams (one sitting, ~90 min)

- tools/dungeon_grading.py: `GradingMixin` carrying _grade, _beat_outcome,
  _find_scroll, _phantom_count, _packs_str, _wyrm_regrowth, _mimic_wipe,
  _enemy_sheet, _scene_sheet, plus module-level extract_tag, strip_and_cap,
  roll. Mixin methods keep their self.* references untouched: verbatim at
  method granularity, not a signature rewrite. Dungeon becomes
  Dungeon(GradingMixin, CampaignMixin).
- tools/dungeon_campaign.py: `CampaignMixin` carrying SCENES + campaign
  (tools/dungeon.py:449-486, 612-726).
- Prune in the same sitting: the shadowed play() at 447-449 and the dead
  disjuncts at 623 (keep behavior: the condition stays, only `or True` and
  the unreachable arms go, with the receipt comment).
- Acceptance gate: re-point tests/test_dungeon_parser.py; 14/14 verdicts must
  reproduce byte-identical; the burn-id pair must stay green; dungeon.py must
  land under 400 or the remainder re-accepts by name with the split named in
  the note.

### Falsifier

If the replay does not reproduce 14/14 byte-identical verdicts after the
move, or the burn-id tests fail, the split reverts and the debt re-accepts at
the then-current count with the failure named: the verdict is reversible by
its own gate. If instead a review shows campaign() cannot be lifted without
semantic change (hidden cross-attribute coupling I did not find in the read),
accept-the-debt-standing wins and the prune still lands.

## Blind spots (honest)

- I re-measured the probe and the tests but NOT the paid batch outcomes: the
  sacred-cow arm-2 2/10 tally, the judge passes, and the 3/28 re-fire are
  receipt-borne, not re-run (paid asks, out of a lens sitting).
- glm-5.3-prime's omission default is UNMEASURED; the explicit-off extension
  to non-deepseek families is inference from the failure family, not from a
  probe. The founding row's thinking provenance (staged vs default) is OWED.
- The OpenRouter "ignores disabled" note (providers.yaml:220-223) is
  comment-borne, not re-measured today.
- I did not read the full dungeon campaign flow end to end (only the
  structure map and the cited ranges); a live paid campaign run did not
  happen, so the split's behavioral gate rests on the replay harness and the
  15 tests.
- The estate-wide GROWTH pattern (8 files) suggests a gate-law fix (make
  GROWTH fail or expire) that is OUT of this decision's scope; I designed and
  tested nothing for it.
- Route_chat ledger rows bank no reasoning_tokens (route_chat.py:242-249),
  so the front door cannot meter the exact failure mode D3 rules on;
  hermes_burn.py:381 shows the pattern to copy. Proposed, not implemented.

ERRATUM 2026-10-04 (coordinator, per break-accuracy A3): the two
tools/ds_workhorse.py:29 cites above are wrong - MODEL lives at :64 (sed-proven;
:29 is docstring prose). Verified and banked in break-accuracy.md:179-182;
the ds_workhorse.md item-6 erratum in the LAND_laws landing carries the
corrected cite. Original lens bytes above unchanged by this append.
