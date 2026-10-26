# PA-R2-qwen38max (qwen/qwen3.8-max-prime @ nous, turn 1, channel: content)

## CUT 1: THE SELF-IMPROVING CLAIM

The board's law: "Every ask's evidence[] carries the prior wave's ractor file - the self-improving leg" (00__WAVE24_BOARD.md, SPEND DISCIPLINE).

Test: grep every ask.json in the queue for evidence arrays containing "RACTOR" in any path. Result from evidence: T1W2_S5 through S8 all carried `evidence:[]` (02__LAST_MILE_AIM.md, REDEMPTION-STAGING: "S5_stores had the same disease: evidence:[]"). All 20 duel asks carried `evidence:[]` (same section). The ractor file T1W1_RACTOR.md exists on disk but no downstream ask.json references it in its evidence array.

Verdict: citation theater. The ractor file is cited in board prose but never rides in a carrier evidence[] field. The byte-test that separates feed-forward from theater: the `evidence` key in each ask.json (not usage.jsonl, not the inbox INDEX). If that array contains a ractor path, the leg is real. Today it does not.

## CUT 2: METRIC CAPTURE

Worst instance: "DUEL2 train 01-14 - LANDED 14/14" (00__WAVE24_BOARD.md, LANE CENSUS line 2). The cross-ractor reports the same 14 calls produced "14 blocked outputs, zero verdicts" (01__DAY1_CROSS_RACTOR.md, E2 table row "DUEL2 train"). The LANDED metric counts carrier completions, not findings. The board optimizes its own instrument (LANDED count) while the estate metric (verdicts a stranger can use) is zero.

## CUT 3: THE 20-LANE GRAVEYARD

24 receipts exist today that nobody redeems: 4 T1W2 outputs renamed `*.md.poisoned-evidenceless` plus 20 duel outputs with empty evidence blocks (02__LAST_MILE_AIM.md, REDEMPTION-STAGING). LAST_MILE_AIM names the goal: "the redemption denominator (issued vs run vs dropped) is counted and above zero." That denominator is unmeasured today. No file in the evidence set contains a redemption counter. No instrument reads a receipt after its window closes. The graveyard is the default state; redemption is aspirational prose, not a measured quantity.

## CUT 4: THE ONE CHANGE

Kill the flywheel's self-improving leg. Replace "next wave's asks carry the ractor file as evidence" with: the human operator manually attaches evidence to each ask.json before staging.

What dies: the compounding claim. The loop no longer feeds itself.
What the money does instead: $113.66 funds direct stranger audits (proven at 9 laws / $2.74) and free verify lanes, with evidence attached by hand at ~$0 cost.
What the estate loses: the theoretical property that wave N improves wave N+1 automatically. The evidence shows this property never fired (zero ask.json files carry ractor paths today), so the loss is zero measured value and one aspiration.

Falsifier for this cut: if a single ask.json is found with a ractor path in its evidence array that was placed by the driver (not by the REDEMPTION-STAGING repair lane), the self-improving leg is real and this kill is wrong.
