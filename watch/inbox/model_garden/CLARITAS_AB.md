# CLARITAS A/B - the face's value per family (2026-10-01, lane X3)

Mission: measure the claritas face's VALUE per family - the "primers are
dials, setting mechanism was missing" question - now that the garden
battery's machine checks exist. Design: N families x 1 ask x 2 arms (BARE =
no system prefix at all vs CLARITAS = face_for(model) + the fixed
estate-law block, the production `_system_for` composition), same ask body
through tools/model_garden.py series staging, graded by the battery's
machine checks; DELTA = face minus bare per family. Budget $1, one ask, one
shot per arm: a cheap first probe whose winners the full burn scales.

Spec: BATTERY.md amendment X3-1 (staged before the code change, build
discipline). Knob: ask.json `system: "bare"` (tools/model_garden.py; absent
or null = production `_system_for` bytes unchanged; any other value fails
loud - verified by a knob test before firing).

## Design history (honesty ledger)

- Operator family list: kimi, glm-5.3-flash, deepseek-flash, haiku-4.5.
- Mid-flight G2 steer (same-mask law): kimi has NO matcher in
  mag/claritas.py `_MATCHERS`, glm/deepseek vendors resolve to FACE_NEUTRAL
  by design, so their bare-vs-face cell cannot be a face-delta. All three
  arms were DROPPED BEFORE ANY FIRE (dry runs only, zero spend) and the
  confirmed distinct-face substitutes fired instead: grok-4.7 (grok face),
  anthropic/claude-haiku-4.5 + anthropic/claude-sonnet-5.5 via Nous
  (anthropic face). Final shape: 3 families x 2 arms = 6 staged, 4 fired.
- Staging defect caught by the arm-integrity check before firing: the
  grok/sonnet face arms inherited `"system": "bare"` from the template and
  would have silently zeroed those deltas; fixed, all 6 cells re-verified
  (bare arms carry the knob, face arms carry nothing).
- WARMED_CONTEXT.md was named by the steer but is NOT on disk in this tree
  (checked twice); the steer's substance was verified directly against
  mag/claritas.py bytes instead.
- Parallel kimi/qwen matcher lane had NOT landed in claritas.py at fire
  time (grep-verified); kimi stays out of this series.

## The ask (garden-x3, byte-identical across all cells)

B2's REVIEW-CONTRACT over mag/switchboard_v2.py (sha256 92573eac8effd6f7,
byte-verified unchanged at fire, no re-freeze needed) + B6's exactness laws
appended to the contract (no markdown fences, no trailing whitespace) and
to the grader. 7 machine checks: B2's SHAPE / CITES-RESOLVE /
LINES-IN-RANGE / NO-EM-DASH / DISTINCT-EVIDENCE (via
tools.garden_grade.grade_review_item) + B6's NO-FENCE / NO-TRAILING-WS.
Series staged at memory/plans/garden_battery/claritas1/<fam>/{bare,face}/.

## The grid (family x arm x machine score)

| family | model (base) | bare | face | machine DELTA | tokens bare (in/out/reas) | tokens face (in/out/reas) |
|---|---|---|---|---|---|---|
| haiku | anthropic/claude-haiku-4.5 (Nous) | 7/7 | 7/7 | 0 | 10331 / 313 / 0 | 10512 / 468 / 0 |
| sonnet | anthropic/claude-sonnet-5.5 (Nous) | 7/7 | 7/7 | 0 | 14323 / 7154 / 6406 | 14596 / 12322 / 11478 |
| grok | grok-4.7 (api.x.ai, XAI_SD) | DNF | DNF | no cells | 0 rows | 0 rows |

CHANNEL RESULT: the machine checks CEILING for anthropic-class families -
both arms pass all 7 on both families. The mechanical instrument cannot
resolve face value here; the measurable deltas moved to the token channel
and the byte-truth layer below. This ceiling is itself the headline finding
of the probe.

## Byte-truth layer (hand-verified against mag/switchboard_v2.py bytes)

The grader only bounds cites by file length; these spot-checks judge
whether each cite brackets the bytes that ground its claim:

- haiku BARE: IMP1 claim self-contradictory ("persists across process
  restarts" vs "allowing replay attacks after service restart") and cites
  56-57 (EFFECTS list region; real replay anchors are 81-84, 267-292):
  WRONG. IMP3 cites 579-585 (receipt-commit region; the budget arithmetic
  it names lives at 593-620): WRONG. 2 of 3 cites wrong-on-bytes.
- haiku FACE: IMP1 names the symbol exactly, cites 78-80 (the state-map
  rows 3 lines short of the 81-84 comment/declaration): near-miss. IMP2
  (narrow_capabilities subset gap) is true in substance at line 213 but the
  cite points at proposal construction 152-157 rather than grant(): cite
  partially off. 0 wrong-home cites, no garbled claims.
- sonnet BARE: 3/3 cites true (238-258 self-authorization chain,
  536-545 mark_executing overwrite, 84,267-292 replay incl. the confirm()
  gap). Convergent with RUN_ANTHROPIC1's banked finds.
- sonnet FACE: 3/3 cites true AND deeper: chains 237-251 + 300-302
  (_implicit_authority operator-authored auto-AUTHORIZE), adds the
  _rewrite_inbox_rec first-match overwrite (516-520, verified true: the
  loop replaces the first event_id match regardless of status) and the
  DEFERRED-branch replay ordering (246-252 verified true:
  proposal-supplied require_confirmation short-circuits the gate).

FACE SIGNATURES (present ONLY in face arms, replicating DAY1_RIB_WARMTH X2
under A/B): the estate-law block's fingerprints - sonnet-face self-labels
"UNVERIFIED, since policy_engine is not in the source shown" (the
cite-or-mark-UNVERIFIED law) and haiku-face's DIFFERENT-BUILD ends with
its own falsifier ("The falsifier is: ..."). Bare arms show neither.

## Token channel (the face's cost)

- haiku: face +181 in / +155 out (+50% out). No reasoning tokens either arm.
- sonnet: face +273 in / +5168 out (+72% out, nearly all reasoning:
  11478 vs 6406). At implied exact rates (2.0/10.0 perM, ECON): +$0.052
  per fire. The anthropic face text ("Be clear and detailed... Reason
  step-by-step") is the visible cause.

## grok-4.7: transport DNF (instrument finding)

Fire started 2026-10-01T23:21:56Z, held 55 minutes with ZERO bytes
returned on BOTH arms (bare first, never concluded), then stopped. The
endpoint was healthy in the same window: a sibling lane's
garden-v1-B2-grok47 fire landed at 23:34:39Z (10818 in / 352 out /
3123 reasoning). Root instrument gap: `_call`'s urlopen timeout=900 is a
PER-RECV bound, not a whole-response fence - a held/trickling connection
never trips it, so the "900s whole-response fence" documented at the
cheapgrid landing does not bind on xAI holds. Single-shot policy honored:
no re-fire; the full burn retries grok with a hard wall-clock leash.

## Budget

Ledger rows banked cost_usd 0.0 for all 4 completed fires (Nous and grok
unpriced in garden PRICING). Real-credit bounds at ECON implied rates:
haiku pair $0.0495 + sonnet pair $0.2526 = $0.3021 Nous credits; the two
abandoned xAI requests bound at the metered $0.23-0.27/answer class =
$0.55 worst case. Lane total <= $0.86 of the $1 cap.

## Honest confounds (all of them)

1. Single ask, one shot per arm. n=1 per cell; a single unlucky draw per
   family. This is a cheap first probe, not a verdict.
2. Machine-check ceiling: the B6+B2 instrument saturates at 7/7 for
   anthropic-class models in BOTH arms, so the reported machine DELTA of 0
   is a property of the instrument's difficulty, not proof the face does
   nothing. The deltas that did move (cite-truth, chain depth, token burn)
   are hand-graded layers with n=1 each.
3. haiku and sonnet share ONE vendor face (anthropic): two families, one
   face text, so the per-family rows are not independent draws of the face.
4. The face arm = face_for + the fixed estate-law block (the production
   composition); the two ride together in every real fire, so the delta
   prices the composition, not the vendor text alone.
5. Nous gateway prompt inflation (~4k tokens vs the haiku pair's ~10.3k)
   is shared by both arms and does not confound the delta, but absolute
   token columns are gateway-shaped, not model-native.
6. grok contributes no cells; its distinct-face value stays unmeasured.
7. Original operator families kimi/glm/deepseek carry no vendor-distilled
   face in the canon (G2 law), so no face value exists to measure for them
   until the matcher lane lands (kimi) or the corpus gains their pages.
8. Byte-truth spot-checks were graded by this seat against the same file
   the models read; no second family judged the replies.

## Verdict and scaling recommendation

PER-FAMILY DELTAS:
- haiku-4.5: machine 0 (7/7 vs 7/7); byte-truth STRONGLY PRO-FACE (bare
  2/3 wrong cites + 1 self-contradictory claim; face 0 wrong homes) at
  +155 output tokens (~+$0.002).
- sonnet-5.5: machine 0 (7/7 vs 7/7); byte-truth MILDLY PRO-FACE (both
  true; face deeper chains + UNVERIFIED discipline) at +5168 output
  tokens (+72%, ~+$0.05/fire).
- grok-4.7: unmeasured (transport DNF).

DOES THE FACE PAY? Yes for haiku-4.5: strictly better cite-truth for
near-zero cost - keep the face on for every haiku fire. Conditionally for
sonnet-5.5: it buys depth and self-labeled uncertainty, not compliance
(both arms already 7/7), at +72% output cost - route the face to
adversarial-review seats, drop it for format-carrier work. The primers
question gets a measured answer only where a distinct face exists; for the
operator's cheap workhorses (kimi/glm/deepseek) the canon currently has no
dial to turn.

FULL-BURN SCALING: do NOT scale a wide face-on/face-off grid on the B6+B2
machine checks - the instrument ceilings and every cell would read delta 0.
Scale instead: (1) harden the grader first with a CITE-TRUTH check (the
cite must bracket the bytes grounding the named symbol - that is where the
haiku delta lived) and a seeded-error extraction axis where format law
actually bites; (2) land the kimi/qwen matchers, then add kimi as the
cheap fourth family; (3) give xAI fires a hard wall-clock leash (the
per-recv timeout does not bound holds) and retry the grok pair once under
it; (4) spend the saved width on cheap-family replicates (5 asks x 2 arms
on haiku + kimi) rather than more premium families - n=1 per cell is the
binding weakness of this probe.

## Files

- Spec: watch/inbox/model_garden/BATTERY.md amendment X3-1
- Knob: tools/model_garden.py (system "bare", fail-closed)
- Series: memory/plans/garden_battery/claritas1/{haiku,grok,sonnet}/{bare,face}/ask.json
- Replies: watch/inbox/model_garden/garden-x3-{haiku,sonnet}-{bare,face}.md
- Ledger: memory/runs/model_garden/usage.jsonl rows garden-x3-* (4 ok rows, 0 refusals)
- Behavioral rows: tools/animal_profiles.py observe (this series) + --distill
