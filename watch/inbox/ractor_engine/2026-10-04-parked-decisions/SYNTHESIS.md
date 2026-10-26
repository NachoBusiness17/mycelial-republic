# SYNTHESIS - the two parked decisions, ruled 2026-10-04

Ractor fold over 8 lens files + 8 hostile break files in this directory. Every
claim below is either (a) a byte I re-verified THIS sitting with the command
named, or (b) a lens finding cited as path:line into that lens's own receipt.
No em-dashes. Anything I could not verify is OWED, never asserted. Start at
the end, because the end is the only part the operator needs:

## THE VERDICTS

**D3: carrier-enforced explicit-off.** For depth=mechanical / short-output
asks the carrier sends `thinking:{type:disabled}` on the wire UNCONDITIONALLY,
regardless of lane config; omission is named in law as never a posture;
depth=design stays the only ON path, gated on lane capability attestation AND
max_tokens >= 32000; and the posture is closed-loop: the ledger banks depth +
reasoning_tokens so the off state is verified from the response, not assumed
from the request.

**D2: accept-the-debt-standing, re-specified as a governed debt.** Do not
split tools/dungeon.py this sitting. One cure sitting now (delete the dead
generation, re-stamp the baseline by name at the honest count, pre-register
the executable split trigger with its golden-vector precondition); the split
itself is deferred behind a named trigger and spends its premium on the D3
wire fix instead.

## D3 - why carrier-enforced wins, from the bytes

The evidence core is CONVERGENT at 3 independent live runs of the same probe
(per duplication-is-emphasis, this outranks every single-source finding):
d4_thinking_probe.md:53-62 (omitted key = 70 reasoning chars / 18 reasoning
tokens on a one-word "pong"; disabled = 2 completion tokens, no reasoning
block; enabled = 12 reasoning tokens, the both-directions sanity arm, at
~$0.00007), accuracy.md:21-29 (live re-run: 11 / 0 / 11), and
break-accuracy.md instrument 1 (16 / 0/2 / 12). Three invocations, same
direction. Omission is a measured ON state, so "omit = off" is dead as law,
and every route_chat lane relying on omission is silently thinking-on.

Why not lane-config-gated (the losing posture, held by accuracy.md and by
operations.md and communication.md BEFORE their hostile passes): the founding
failure rode a lane with no flag. I re-verified this sitting: my run of
`.venv/Scripts/python.exe -c` over memory/runs/hermes_burn/usage.jsonl lines
1151-1152 returns `1151 z-ai/glm-5.3-prime ct 16000 rt 15998 cc 1 fin length
ok True cost 0.2502604` and `1152 ... ct 14759 rt 9826 fin stop ... cost
0.2137336` - one judgment, $0.4639940, hollowed at cap then re-fired. And my
`grep -n disable_thinking configs/providers.yaml` returns exactly three hits
(:223, :371, :401); the nous lane block that carries glm-5.3-prime carries
NONE. Config-gating (mag/route_chat.py:204, verified this sitting:
`if lane_cfg.get("disable_thinking") and depth == "mechanical":`) leaves the
founding failure mode on vendor-default ON. It failed open twice already:
route_chat carried a disable_thinking lane while never reading the flag until
go-wave lane 1 wired it (comment at mag/route_chat.py:205-210), and
mag/inference_budget.py:75-84 STILL strips the off switch
(`thinking_control={}`, `"thinking"` in forbidden_keys) while its notes teach
the refuted "omitting it IS the off state (AH10)" law - verified by my sed
read this sitting. Fail-open silent loses to fail-loud; the disabled key 400s
loudly if a lane rejects it, and an error row banks (mag/route_chat.py:254-266).

Why closed-loop: explicit-off is necessary but NOT sufficient.
configs/providers.yaml:219-223 records openrouter/auto measured IGNORING
`thinking:{type:disabled}` (600 -> empty, 2000 -> content; moonshot-2.md F1).
The request byte cannot defend an ignore lane; the response census can. My
census confirms the ledger is blind today: mag/route_chat.py:242-249 banks
lane/model/goal/key_env/tokens/content_chars/finish_reason/ok and neither
depth nor reasoning_tokens (hermes_burn.py:381 already banks reasoning_tokens,
the copy pattern).

The dissent is recorded, not erased: accuracy.md:10-16 holds lane-config-gated
explicit-off and re-ran the probe live; its own falsifier set (accuracy.md
:80-90) stands unmet. It is outranked by the 5-3 second-pass majority
(operations.md:54-66 concession; communication.md:72-86 concession; logic.md
:14-18 and :57-58; economics.md:8-14; moonshot-1.md:21-29; dogfood.md:13-19;
moonshot-2.md:41-50) because the config-gated form fails on the founding
evidence itself: the lane that burned $0.464 has no flag to gate on.

### D3 falsifier (what flips this verdict)

(1) A MEASURED HTTP 400 on `thinking:{type:disabled}` from any funded-lane
model on a depth=mechanical ask forces capability-scoped off (send only to
attesting families). (2) A judged equal-budget A/B at mechanical caps where
thinking-ON wins material_chars per dollar with zero hollow rows flips the
default back. (3) A d4_probe.py re-run where the omitted arm returns
reasoning_tokens 0 (a vendor flipped the default; urgency drops, the explicit
byte stays). Honest basis note (CONVERGENT: communication.md:15,
economics.md:103-120, moonshot-1.md:89-100, moonshot-2.md:79-82): the estate
has NEVER banked a thinking-OFF batch score; every ds batch through
2026-10-04 06:11Z rode ON by omission (mtime ordering, communication.md:9-14,
re-run by dogfood.md instrument 3). The OFF default rests on the ON failure
class plus cost asymmetry; it must be written as that, never as if a quality
A/B existed.

### D3 amendment text for the losing law surfaces (append-never-rewrite)

Loser 1, the ABSOLUTE clause in PRIORS row 8
(watch/inbox/model_garden/PRIORS.md:25, "STILL-VALID (byte-confirmed
mechanism, never refire thinking-on)"). Append the merged POST-DATUM
(operations.md:17 as re-aimed carrier-enforced by communication.md:86; logic
.md:93-110 and moonshot-2.md:112-123 carry compatible variants, bank ONE):

> POST-DATUM 2026-10-04 (parked-decision D3; d4_thinking_probe.md;
> hermes_burn usage.jsonl:1151-1152): row 8's mechanism is confirmed
> cross-family (deepseek-v4-flash 3-arm probe: omitted key = 18 reasoning
> tokens on a one-word ask; glm-5.3-prime: 15998 of 16000 completion tokens
> reasoning, content_chars 1). Scoped ruling: THINKING OFF is the SENT
> default for depth=mechanical/short-output asks, enforced BY THE CARRIER:
> route_chat sends thinking:{type:disabled} unconditionally on mechanical
> (mag/route_chat.py:204, lane-config condition removed); omission is NOT
> the off state (d4 3-arm probe 2026-10-04, three independent runs). Lane
> config (providers.yaml disable_thinking) is demoted from enforcement to
> design-depth capability attestation. "Never refire thinking-on" holds as:
> thinking-on rides ONLY depth=design on attested lanes at max_tokens >=
> 32000, substance-gated (mag/route_chat.py:238-249). The off state is verified
> from response-side reasoning_tokens banked per row, not assumed from the
> request (openrouter/auto measured ignoring the key, providers.yaml
> :219-223). Falsifier: a judged equal-budget mechanical A/B where
> thinking-ON wins material_chars per dollar with zero hollow rows flips the
> default back; a measured 400 on the disabled key from a funded lane forces
> capability-scoped off.

Loser 2, queue/STANDING_RAILS.md - PREMISE CORRECTION first, verified by
three lenses independently (accuracy.md:43-49, operations.md:36,
dogfood.md:65-68) and by my read of the lens receipts: the file carries NO
depth law at all; the law the ask cited lives only in mag/route_chat.py
:127-141 (docstring) and :204-213 (wire). The amendment is an ADDITION to
law 1 (economics.md:70-78 + moonshot-2.md:130-134 merged):

> Depth-gated thinking: depth=mechanical sends thinking:{type:disabled} on
> the wire for every lane, sent by the carrier (omission is not the off
> state, d4 probe 2026-10-04); depth=design is the only enabled path,
> capability-attested per lane, budgets 32K+; usage rows bank depth +
> reasoning_tokens so the posture is auditable.

Loser 3, watch/inbox/go_wave_20261004/ds_workhorse.md item 6 ("uncapped,
thinking-off, file-backed" is false on the wire). Append the accuracy.md
:94-102 erratum WITH the break-accuracy cite fix applied (:64, not :29 -
`MODEL = 'deepseek-chat'` sits at tools/ds_workhorse.py:64; :29 is a
docstring pointer; the uncorrected text is baked at accuracy.md:99 and D1.4
and must be fixed before it is applied):

> ERRATUM 2026-10-04: the 'thinking-off' label on this re-fire is unverified
> and false-by-ordering: the run (04:38:32Z) predates the d4 probe
> (06:00:41Z) and the explicit-key fix (06:11:38Z), so its ask() OMITTED the
> thinking key; omission is measured ON for deepseek-v4-flash
> (d4_thinking_probe.md) though this batch ran model deepseek-chat
> (tools/ds_workhorse.py:64), never probed. The 0/26 vs 3/28 delta is a
> budget-axis result (harness 2000 cap vs vendor default), not a
> thinking-axis result. The explicit disabled key landed post-run at
> tools/ds_workhorse.py:93.

Loser 4 is CODE, and it is the part the prose hid (moonshot-1.md:135-158,
CONVERGENT with dogfood.md F1 and logic.md:136-149): the refuted law is
pinned GREEN by this wave's own tests. My sed read this sitting confirms
tests/test_route_chat_depth.py pins `{"type": "enabled"}` for design on the
deepseek lane (~:77-80) and `"thinking" not in body` for a flagless lane
(~:83-89, the omission-as-contract assertion). These flip WITH the code or
they enforce the bug; note the design-pin test conflicts with any
capability-gate that declares deepseek non-attested (providers.yaml:371
carries disable_thinking: true), so the test edit is part of the wire sitting,
not a follow-up (break-operations finding).

## D2 - why accept-standing wins, from the bytes

Final tally 6-2 (operations.md:21, economics.md:122, logic.md:177,
communication.md:41, moonshot-1.md:169, dogfood.md:214 corrected verdict;
against accuracy.md:120 and moonshot-2.md:161). The hostile pass is what
decided it, and it is the honest core of this fold: dogfood.md:185-232
WITHDREW its own first-pass split-now verdict on three measured grounds.
(1) The "I/O-free pure layer" is false: _verdict binds self.tip/self.turn
(:246) and mutates self.pc_hp (:256), module global ROSTER (:267),
self.warden_hp (:274) and more; _grade mutates self.last_roll (:579) and
self.root_anchors (:601-602) - none verbatim-movable. (2) The truly-pure
verbatim set is ~135 lines (module band :103-145, SCENES :454-486, seven
self-cosmetic methods :488-546), so the residual carrier is ~636 lines and
one seam cannot clear the 400-line rule. (3) The decisive byte:
tools/prepush_golden_vector.py:50-63 pins 7 of its 11 golden tokens to bytes
in SCENES and the campaign band with DEFAULT_TARGET "tools/dungeon.py"
(:43); dogfood ran it green this sitting (11/11, exit 0). Moving SCENES
without retargeting the vector lands the split with a red pre-push
instrument. accuracy.md's own falsifier concedes this class: "if campaign()
cannot be lifted without semantic change, accept-the-debt-standing wins" -
the hostile pass found exactly that. Even moonshot-2's split-now plan adopts
the golden-vector re-point and re-accepts the residual by name at the new
count, which IS governed-debt mechanics.

What both camps converged on (every lens found it independently - CONVERGENT
across dogfood F4, economics rider, communication.md:48, moonshot-1.md,
moonshot-2.md F4, operations.md:28, accuracy.md:140-146, break-dogfood): the
file's real rot is debris, not size. I re-verified every cited line this
sitting with `wc -l` (771) and sed: tools/dungeon.py:447-449 is a first
`def play` (s0+s1 only) silently shadowed by the second at :727-731 (adds
`if self.full: self.campaign()`); the bodies DIFFER, so the prune deletes the
FIRST def only (break-dogfood's direction note) or the campaign hook dies;
:617-619's fix-comment cites "tools/dungeon.py:447 at HEAD 37e2fba7e", which now
lands the reader on the dead method; :623 reads `if self.warden_hp <= 0 or
self.persuades >= 2 or True:` (first two disjuncts dead); :211 reads
`msg.get("content") or msg.get("reasoning") or ""` - the same dead fallback
name lane 1 killed in route_chat this wave (mag/route_chat.py:231-235, verified
by my read: the vendor field is reasoning_content). Debris discovery rate ~1
per 190 lines on one full read (moonshot-2.md F4) is the standing argument
for the seam discipline the trigger encodes.

Why the debt can stand governed: the ratchet cannot silently compound it. My
run this sitting, `.venv/Scripts/python.exe tools/violation_ratchet.py check`,
prints `GROWTH claim af1d7045681fee89: tools/dungeon.py accepted at 756
lines, now 771 (+15) - re-audit or re-accept by name` among 8 GROWTH lines,
dungeon the SMALLEST grower (percolator +442 leads the cohort) - and exits
FAIL on NEW=1, `e71ef4422e755b5e file-too-long: tools/social_rsi.py:578`.
Growth is print-only by design; every audit re-flags the debt by name. The
+15 (3-strike void breaker, hours after acceptance) is hardening, not sprawl
(operations.md:25 git evidence). The replay net is real and I ran it this
sitting: `pytest tests/test_dungeon_parser.py tests/test_burn_id_uniqueness.py
-q -p no:cacheprovider` = **15 passed in 2.01s** (13 parser functions
replaying the 14 logged S4 verdicts, fixture-count assert at
tests/test_dungeon_parser.py:61, + 2 burn-id). The ask's "15 dungeon tests
pass in under a second" reproduces in the count but NOT the time on my
instrument (operations.md got 13-in-0.74s on the file-only instrument and
16-in-8.72s on `-k dungeon`; name the instrument whenever the count moves).

### D2 falsifier (what flips this verdict to split-now)

Any ONE of: (a) a second engine-loop correctness bug inside one wave (the
parser collapse was the first; operations.md:32, economics.md:178-180);
(b) growth past +50 over the accepted 756 (operations.md:30) or the file
becoming the GROWTH cohort's top grower (economics.md:184-185); (c) the next
substantive campaign edit landing - split-while-touching beats
split-for-its-own-sake (economics.md:181-182, moonshot-1.md:213-215). AND
any split sitting MUST first satisfy the dogfood precondition: retarget
tools/prepush_golden_vector.py (DEFAULT_TARGET :43, 7/11 tokens pinned to
SCENES/campaign bytes) to scan both files, and re-census the ~135-line
truly-pure ceiling before lifting (dogfood.md:214-224). One seam never
clears the 400 rule; the split's return is the dice-law layer as a stable
importable module plus a buried dead generation, not a ratchet line.

## The honest residue (OWED, never asserted)

1. The deepseek-chat alias's omission default is UNMEASURED (the probe tested
   deepseek-v4-flash only; ds_workhorse.py:64 maps the alias): a ~$0.0001
   3-arm probe against MODEL=deepseek-chat settles the refire-posture label
   for good (logic.md:169-172).
2. GLM prime's thinking wire shape on the nous gateway is UNVERIFIED; the
   hermes_burn fix's first leg is a ~$0.001 probe across funded lanes
   (economics.md:189-192, moonshot-2.md:293-295). The founding rows prove the
   budget mechanism on a glm ask, not the vendor default (accuracy.md:31-41).
3. hermes_burn computed the cure and dropped it one hop before the wire:
   plan_call merges thinking_control into plan.extra_body
   (mag/inference_budget.py:262-283), tools/hermes_burn.py:344 calls plan_call
   but :345 passes only plan.max_tokens into _call, whose body is
   {model, messages, max_tokens} (:106-116) - the nous-primes
   reasoning:{max_tokens:6000} rails never reached the request that burned
   15998 reasoning tokens (communication.md:80). Merge-the-computed-plan is
   the same verdict in carrier form.
4. The ratchet is RED tree-wide right now (my run: FAIL, NEW=1
   tools/social_rsi.py:578); any verdict citing RATCHET: PASS is banking
   stale tree state from the earlier lens sittings (moonshot-2.md F5,
   break-operations). Accept or fix that debt by name separately; do not
   bundle it with either decision.
5. tools/tavern.py and other carriers were not audited for the
   shadowed-method / stale-label class (operations.md:51, communication.md:68).
6. Post-gate hermes_burn rows were not censused for ok:false hollow stamps
   (economics.md:198-199); the $0.464 is pre-gate history.
7. The 191.8M-token-class instrument hygiene note: every count in this fold
   names its instrument and moment; the ask's own counts drifted (756 vs 771
   lines; 15 tests reproducing in count, not always in time). The SYNTHESIS
   re-banks none of them without the instrument named.

## Checks run this sitting (exact commands, this tree)

1. `.venv/Scripts/python.exe tools/violation_ratchet.py check` -> scope=1405,
   hits=943, registered=942, NEW=1 (tools/social_rsi.py:578), 8 GROWTH lines
   (dungeon 756 -> 771, +15), RATCHET: FAIL.
2. `.venv/Scripts/python.exe -m pytest tests/test_dungeon_parser.py
   tests/test_burn_id_uniqueness.py -q -p no:cacheprovider` -> 15 passed in
   2.01s.
3. `.venv/Scripts/python.exe -m pytest tests/test_route_chat_depth.py -q
   -p no:cacheprovider` -> 4 passed in 1.07s.
4. `wc -l tools/dungeon.py` -> 771; sed reads of :211-212, :447-450,
   :617-624, :727-734 (all debris lines byte-confirmed as cited above).
5. venv python read of memory/runs/hermes_burn/usage.jsonl lines 1151-1152
   (the $0.4639940 double burn, quoted in D3 above).
6. `grep -n disable_thinking configs/providers.yaml` -> :223, :371, :401
   (three lanes; nous block bare).
7. sed reads: mag/inference_budget.py:73-85 (thinking_control={} +
   forbidden_keys stripping + the refuted omission note, live);
   tests/test_route_chat_depth.py:61-90 (both pins live); mag/route_chat.py
   :110-269 (config-gated mechanical :204, ungated design :212-213, bank
   without depth/reasoning_tokens :242-249).

## Repair note (2026-10-04, second write)

The consuming harness reported this file missing after the first write; a
direct Read of the path showed the first write's bytes present, so this file
was rewritten verbatim this sitting and existence was re-verified with
`ls -la` + `wc -c` (outputs in the session transcript). If a downstream
checker still cannot see it, the discrepancy is in that checker's path or
sandbox view, not on this tree.
