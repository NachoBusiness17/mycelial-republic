# SALON1_RACTOR - the mesh-shaped ractor salon over the day's cross-model learnings (2026-10-01)

Lane SALON-1 (MESH RACTOR SALONS). Operator order: "lens some ractor salons through deepseek on
everything we're learning about our hermes burn across models" + "remember the higher dimensional
swarm shit and intercommunication? time to dogfood some theory". This file is the salon's landed
deliverable; the theory dogfooded is the mesh itself: blind units, then intercommunication, then
convergence.

## THE SHAPE (what fired)

| round | fires | what | cost |
|---|---|---|---|
| 1 blind | 6 | each unit ractored its own themed slice, star-free, no knowledge of siblings | $0.0346 |
| 2 intercommunication | 6 | each unit received TWO sibling round-1 sets; its only job was connections | $0.0148 |
| 3 convergence | 1 (+1) | one convener read all six round-2 sets and minted the final laws | $0.0045 + $0.0039 restage |

Instrument: tools/ds_workhorse.py (deepseek-chat, thinking off, temp 0.3), 14 fires total,
all attempts=1, zero empties, zero retries. Total cost $0.0577 of the $3 cap (1.9 percent).
The round-3 restage is not a refire: the first convergence fire was truncated by the harness
6000-char output cap mid F9, so the contract was re-staged tighter (7-8 laws, 5000-char
ceiling); the truncated fire is preserved in round3/results.jsonl.

Units and slices (self-contained; no unit could request more material):

- U1 model behavior (families, reasoning channels, fabrication): PRIORS, FABLE1, KIMI1_RUN,
  KIMI_DOSSIER, CHAN_ROAST_XMODEL, DUEL_JUDGE2, C1_censorship
- U2 instruments (carriers, swarms, graders): SWARM_1, CROSS_RACTOR_MATRIX, BATTERY, CENSUS,
  A2_duel_provenance, A3_corroboration_bootstrap, swarm1-kimi lens carrier
- U3 economics: ECON, DOLLAR_BURN_SWEEP, RUN_ANTHROPIC1, RUN_UNIQUE_X2, both GRID receipts,
  MOVEMENT2_CHEAP_ANSWERS, D1_doctrine_roast
- U4 operations: WAVE24_BOARD, WINDOW2_RACTOR, WINDOW1_STATE, LAST_MILE_AIM, DG1, T3R2,
  SP1_gate_exit_contract, B1_outbox, A1_steer ASSEMBLED
- U5 meta-laws: SELFSTEAL_53_ERA, DAY1_CROSS_RACTOR, B2_drift_rows, T1W1_TOVERIFY, D3_roast,
  CLARITAS_AB, STEERING_DOGFOOD
- U6 stranger view: WARMED_CONTEXT, DAY1_RIB_WARMTH, T1W1 stranger files, T1W2 S5-S8, T1W3 N1-N3

Mesh pairing (round 2): each unit received the next two units in the cycle, covering 12 of the
15 unit pairs. Round 2 minted 36 connection rows + 17 contradiction rows (53 total).

## THE LAWS (W2-Ln idiom; S1 = salon 1)

Each row: CLAIM / STEAL / FALSIFIER / SOURCE (byte-verified estate quotes; unit chain) /
LEVERAGE / CONVERGENCE (units whose round-1 laws independently support it, then the convener's
round-2 route). Quotes below were grep-verified byte-exact against the estate files this session.

### S1-L1: cap burn is harness fault, the fix is a floor
CLAIM: When a family burns its entire output cap on the reasoning channel and returns empty
content, the fault is the cap floor, not the animal; the fix is a per-family minimum viable cap
(measured reasoning burn plus content headroom), never a retry and never a bare cap.
STEAL: Before blaming a family for empty output, measure its reasoning burn and raise the cap
floor (the fable recipe: review-shape floor 24000).
FALSIFIER: A family landing clean content below its measured burn.
SOURCE: watch/inbox/model_garden/FABLE1.md "12000/12000 reasoning tokens"; convener chain
U1-r2 C1 + U2-r2 C4.
LEVERAGE: high
CONVERGENCE: U1 (L1 reasoning-cap burn, L2 deepseek thinking-on) + U3 (L4 "the floor is the
minimum viable cap", reached from the economics side); convener route U1+U2 via C1, U2+U3 via
C4, U5+U6 via C1.

### S1-L2: proxy checks pass wrong objects
CLAIM: Any gate that measures a proxy instead of the bytes themselves will pass a wrong object;
length-only provenance gates, field-name-mismatched readers, and self-consistency digests are
one failure class.
STEAL: Replace one proxy check tomorrow with a byte comparison against the expected content and
log what it catches.
FALSIFIER: A same-length different-byte text the current gate already rejects.
SOURCE: watch/inbox/hermes_burn/A2_duel_provenance.md "Same-length, different-byte"; convener
chain U2-r2 C3.
LEVERAGE: high
CONVERGENCE: U2 (rejudge length-only gate) + U4 (field-name mismatch read empty) + U6 (gate
proves only internal self-consistency); convener route U2+U3 via C3, U4+U5 via C1, U6+U1 via C3.

### S1-L3: unauthenticated seats inflate corroboration
CLAIM: A seat is an unauthenticated free string, so a len(seats)>=2 corroboration bar is
trivially satisfiable; a same-id re-fire is a second seat string for free, so the corroboration
count can be inflated by the same bug that inflates cost.
STEAL: Dedupe re-fired ids before counting seats, and authenticate seat strings to distinct
families before banking any CORROBORATED verdict.
FALSIFIER: Re-fires deduped before seat counting, so a re-fire cannot register as a distinct
seat.
SOURCE: watch/inbox/hermes_burn/A3_corroboration_bootstrap.md "unauthenticated free string";
convener chain U2-r2 C2.
LEVERAGE: high
CONVERGENCE: U2 (seat string) + U3 (2 of 5 rows are same-id re-fires, spend inflation);
convener route U1+U2 via C3, U2+U3 via C2, U6+U1 via C5.

### S1-L4: sha-locked verdicts freeze their flags
CLAIM: A verdict is true only against the sha it reviewed, and its UNVERIFIED flags are frozen
at that sha; retirement must re-stamp against a new sha or the flag outlives its surface.
STEAL: Before retiring any flag, check whether the surface sha has moved since the verdict was
stamped; re-stamp if it differs.
FALSIFIER: A verdict's flags auto-clear on surface change without a re-stamp.
SOURCE: watch/inbox/model_garden/CROSS_RACTOR_MATRIX.md "verdicts are sha-locked"; convener
chain U2-r2 C1.
LEVERAGE: high
CONVERGENCE: U2 (sha lock) + U5 (board verdicts drift from their own receipts) + U6 (boot pack
stale-trap class); convener route U2+U3 via C1, U4+U5 via C4, U6+U1 via C2.

### S1-L5: exit zero hides no-op loops
CLAIM: A command can exit 0 and report completed while landing nothing, and the re-fire that
follows is billed; billing and landing share one mechanism, so completion claims must be
cross-checked against a ledger diff, not an exit code.
STEAL: Cross-check every exit-0 receipt against a ledger diff before accepting completion.
FALSIFIER: Re-fired ids shown to be distinct asks rather than retries of a no-op.
SOURCE: watch/inbox/hermes_burn/WINDOW2_RACTOR.md "b50d6c999e59" (the identical digest the
fallback re-pulled while exit 0 said completed); convener chain U3-r2 C1.
LEVERAGE: high
CONVERGENCE: U4 (L1 exit code cannot certify landing) + U3 (re-fire spend) + U5 (fix claims the
ledger contradicts); convener route U3+U4 via C1, U4+U5 via C1 and X2.

### S1-L6: unpriced families bank zero structurally
CLAIM: An unpriced family banks $0.0 because no rate row exists to contradict the zero; the
blind spot is structural, and a version merge (family-level rollup) hides spend under a label
that spans different animals.
STEAL: Add per-version rate rows for every family currently banking $0.0 before trusting any
cost rollup.
FALSIFIER: A metered receipt appears for an unpriced family.
SOURCE: watch/inbox/model_garden/GRID_cheapgrid1_RECEIPT.md "qwen and grok costs bank $0.0";
convener chain U3-r2 C3.
LEVERAGE: medium
CONVERGENCE: U3 (L5 unpriced families) + U1 (L5 same family different animal); convener route
U1+U2 via C6, U3+U4 via C3, U6+U1 via C6.

### S1-L7: refusal and obedience are carrier properties
CLAIM: A REFUSED bank on one family says nothing about the same ask on another; refusal and
obedience are carrier-family properties, not ask properties. Same bytes, different carrier,
different outcome.
STEAL: Re-send one REFUSED-banked ask to a different carrier with identical bytes and compare
before treating the refusal as ask-level.
FALSIFIER: A REFUSED-banked ask on one family lands content when re-sent to another family with
identical bytes.
SOURCE: watch/inbox/model_garden/STEERING_DOGFOOD.md "same bytes, kimi executes, glm ignores";
convener chain U4-r2 C5.
LEVERAGE: medium
CONVERGENCE: U4 (L7 REFUSED banked as terminal) + U5 (L6 seals admit steers, families decide
obedience); convener route U4+U5 via C5, U3+U4 via X1.

### S1-L8: blind-judge wins need a byte walk (THE MESH-ONLY LAW)
CLAIM: A blind judge cannot verify citations, so a confident fabrication can win; a blind-judge
win is a convergence event, not a verdict, and must be byte-walked before it reaches the ledger.
STEAL: Byte-walk every blind-judge win (verify its citations against the named source sha)
before banking it as routing evidence.
FALSIFIER: A blind-judge win whose citations all verify at the named sha (the class survives;
the instance retires).
SOURCE: watch/inbox/hermes_burn/DUEL_JUDGE2.md "fabrication quoting invented clauses" +
watch/inbox/model_garden/SWARM_1.md "Convergence is corroboration, not adjudication"; convener
chain U6-r2 C4.
LEVERAGE: high
CONVERGENCE: U1 + U2 via mesh only.
MESH-ONLY PROOF: U1's slice held the fabrication risk (DUEL_JUDGE2: judge2 sees only question
and answers, cannot check quoted clauses); U2's slice held the convergence rule (SWARM_1:
cross-family agreement is corroboration, bytes arbitrate). Neither slice contained the other's
file. Neither unit's round-1 law states the synthesis; it exists only in the round-2 pair
(U6-r2 C4 welded U1's L6 to U2's convergence row). No single star unit could have minted it.

## VERIFICATION (the bytes leg)

Quote census through the chain, grep-run by this seat after landing:

- Round 1 (42 quotes in SOURCE lines vs the estate files): 39 byte-hits (22 exact, 17
  line-wrap forms that match after whitespace collapse), 1 case-only near-hit, 2 misses.
- Round 2 (110 EVIDENCE quotes vs the round-1 outputs the unit actually saw): 105 byte-hits;
  the 5 non-hits are 2 compressions of U4's claim line (inner quotes around "completed"
  dropped), 1 case variant, 1 backtick punctuation variant, 1 nine-char fragment.
- Round 3 (16 quotes vs the round-2 outputs): 16 byte-hits, 16 exact, zero misses.
- The two round-1 MISSES stay misses (ractor50 precedent: rejected, not repaired): U3
  "Slim variant for anthropic-class cells: 4 items, not 8" (paraphrase tail; the estate text
  ends the span at the colon), U6 "is doctrine, not a control. Nothing enforces it." (not
  found in the slice pool). No law above cites either.
- Em-dash census: zero em-dash characters in every authored file of this salon (prompts,
  landings, this artifact); model outputs measured 0 across all 14 fires.
- Instrument honesty: ds_workhorse truncates outputs at 6000 chars; all landed outputs are
  under that except the first round-3 fire, which is preserved truncated and named above.

## FALSIFIER (for the salon itself)

If the next routing decision or harness change cites none of S1-L1..L8 within three sessions,
the salon was mesh theater. The concrete next test: S1-L3 (seat dedupe before corroboration
counts) and S1-L8 (byte-walk before banking blind-judge wins) are both one-sitting steals onto
live instruments; run one and file the receipt.

## RAW ROUNDS

All fires, verbatim: memory/runs/salon1/ (inputs: slices + items + prompts; round1, round2,
round3 with results and per-unit landings). Slices are byte-copies of the estate files, cropped
at line boundaries; crop points marked in-file.
