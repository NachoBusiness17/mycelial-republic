# V2 GROK JUDGMENT (2026-09-30)

Lane: last-mile V2. File ownership: this receipt. Budget $1.00, spent **$0.1462** (3 calls, all finish=stop, zero retries).
Driver: `watch/inbox/last_mile_20260930/v2_grok_burn.py` (night_burn_20260930.py pattern: pinned host, SSRF guard, reasoning cap 6000, usage.cost meter). Raw: `v2_grok_raw.jsonl` beside it.

## The three verdicts

### V2a. OCEAN.md, N1's anti-hagiography frame (identical prompt + LAWS)
Verdict: **AGREEABLENESS is the hagiographic axis; change it to LOW, drop the "high loyalty" qualifier.** That is *the same change glm-5.3-prime's N1 recommended* (cross-family agreement on the one-rating change, unprompted). Grok's sharpest lines: law 12 ("THE STANDARD BINDS BOTH WAYS") is "self-written doctrine and praise for pleasing artifacts"; "challenging-as-affection is the author's gloss, not the corpus"; double-counting kill (idea-starts raise OPENNESS, then get excused under CONSCIENTIOUSNESS). Also flags machine-directed speech as UNPROVEN as a human-personality measurement. $0.0274, 55s, 793 completion tokens.

### V2b. FINAL_PIECE.md, N6's adversarial-grade frame
Verdict: **power 3/10** (glm's N6 said 6/10; Grok is the harsher grader), **"none" of the three dumb rules survive** (glm: rule 1 survives, 2 partial, 3 weakest). New kills glm did not make: rule 1's cold-start paradox (no row means no work means no row, contradicting the essay's own "it never rations what walks out"); the words=1200 byte-check is scoped to before the appended CORRECTION block so the pasted doc is not 1200 words; the Scrouting/SuperScout naming slip inside the Y7 fix itself. Shared catches: 16 logos asserted, 15 named (both families); "best 2026 result" superlative unlicensed by one DIGEST row; DIGEST.md not visible so every number UNPROVEN. glm kept one unique catch Grok missed (the 1-in-6 collusion-odds math, should be 1-in-4). $0.0548, 125s.

### V2c. Novel: TIE_IT_ALL + "what is this estate missing that nobody asked today?"
Verdict: three ranked omissions, each pinned to a cited line: (1) **self-sample treated as judgment** ("receipts re-enter the ledger as verdict rows": the organ that did the work scores itself; no disqualification law on which rows may move Wilson LB / n_min / G0-G3); (2) **live drive and determinism sold as one tie** (a live byte outside the hash chain cannot underwrite an authoritative price; the synthesis never splits the claims); (3) **no principal outside the payoff** (the only planned stop depends on a mate reading STEER.md, which the doc itself says has no reader). Framing kill: "closure is false on this document's own terms." $0.0641, 159s.

## The $0.77/M claim does not survive the meter

Trust bytes: the models endpoint lists grok-4.7 at **$2.00/M prompt, $6.00/M completion**. Measured blend this run: 31,255 billed tokens / $0.1462 = **$4.68/M** (reasoning tokens bill as output; they were ~71% of billed tokens). The $0.77/M figure appears nowhere in the API price list. Per token it is still ~0.71x glm-5.3-prime's listed $2.80/$8.80, but per *ask* it ran ~2.5x glm's night-burn cost ($0.049 avg vs $0.020) because it burns more reasoning.

## Seat call

**Yes: good enough to be the default judgment seat when this account is busy**, with two named caveats: (1) it is a $2/$6 seat, not $0.77/M; still cheap enough that judgment at scale is real ($0.05 per adversarial grade). (2) it is slow: 55 to 159s vs glm's 17 to 20s; fine for batch judgment, wrong for interactive lanes. Strongest evidence: unprompted cross-family convergence with glm on the OCEAN one-rating change, plus kills glm missed on both shared frames. Recommended shape: glm-5.3-prime stays the workhorse judge; grok-4.7 becomes the second-opinion / account-busy judgment lane, exactly the role this test simulated.

Meter: spent $0.1462 of $1.00. Receipt filed in the shared inbox per the surface contract.
