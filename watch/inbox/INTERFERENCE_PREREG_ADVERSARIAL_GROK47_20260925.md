# GROK 4.7 ADVERSARIAL PASS - interference prereg (filed 2026-09-25)

Chore: BOOT_LANE_INTERFERENCE_BURN_20260925.md Stone 5.1, adversarial pass on the
frozen prereg + Amendment 1 BEFORE Arms A/C run. Fan-out-suitable shape (same
review chore fans across prereg docs).

Path: grok CLI harness (harness/grok_cli.py, headless) -> cli-chat-proxy.grok.com,
auth.x.ai session. NOT the Nous Portal 50% lane; NOT the estate XAI cash lane.
Model: grok-4.7-build | cost $0.02908224 (proxy self-reported) | latency 120125ms | usage {"input_tokens": 26830, "cache_read_input_tokens": 1280, "cache_creation_input_tokens": 0, "output_tokens": 5206, "reasoning_tokens": 4110, "total_tokens": 33316}
Verbatim model output below; review-of-review is the driver seat's job, not this file's.

---

Arm C’s claim-bearing bar cannot show that gemma substitutes the trained judge. At the budget where a pass is still available, search already saturates, and the amendment relocated the decision after Arm B’s curve existed.

**1. Budget-200 PASS sits inside an already-saturated regime.**  
Quote: “At budget 200: one-line 70% (21/30 …), frontier-no-merge 100%, interference 100% (30/30).” And: “200 (added secondary reading, frozen bar >=15/30).”  
Arm C is “their search loop, their merge” with the judge swapped — the same family that already solved 30/30 at 200 states, including frontier-no-merge. A line at 15/30 is below the one-line judge (21/30) and below both search variants (30/30). Clearing it is compatible with merge-and-width doing the solving.  
Risk: a PASS is read as “gemma ranks the frontier.”  
Fix (15 stays): one null arm, same loop, both budgets, every score fixed at 0.5. Receipt prints gemma, null, one-line 21/30, and interference 30/30 side by side. The substitution sentence is allowed only when gemma’s solve count is strictly above the null. Otherwise the row stays a numeric pass or fail against 15 and the claim sentence is omitted.

**2. The 50-state bar was reinterpreted after the curve.**  
Quote: “PASS >= 15/30 at 50 states.” Then: “50 (frozen bar kept, now expected to FAIL; a fail there is the finding ‘no judge, dumb or trained, solves Countdown-30 at 50 states’).”  
Measured interference at 50 is 6.9/30. The original bar asked gemma to beat a rate the trained judge misses. Keeping the integer while changing what a fail means is a rescue reading of a bar that was pointed at the wrong quantity. The universal finding also overreaches: 8.1 and 6.9 are not integer outcomes on one seed-11 pass, so the curve is a different random variable than Arm C’s X/30.  
Risk: 50 becomes a guaranteed “finding” and 200 becomes the real test, chosen once Arm B showed where the mass sits.  
Fix (15 stays): the 50-state row is a checkpoint only. It may be filed FAIL against >=15. It may not be paraphrased as a theorem about all judges. The 8.1 and 6.9 figures stay labeled as whatever aggregate produced the fraction, and they are not treated as one-seed solve counts.

**3. Two budgets are a second life unless one is a prefix.**  
Quote: “No arm gets a second chance on a problem.” And: “Arm C runs at BOTH budgets.”  
Independent restarts let a dead 50-state trajectory be replaced, and the write-up can lean on the reading that cleared.  
Fix: one trajectory per problem. Record the solve bit at state 50, then continue that same search to 200. Two checkpoints, one life.

**4. Arm C decoding and the rank prompt are unfrozen.**  
Arm A locks “greedy, temperature 0.” Arm C does not. Parse-fail scores 0.5 and never prunes, so a model that emits unparsable text becomes the null judge while still spending budget. The batch prompt, frontier chunking, and answer span are unspecified.  
Risk: temperature, prompt edits, or which states enter the batch can be adjusted until 200 clears 15. High parse-fail plus merge can pass without a ranking.  
Fix: freeze before launch, in the receipt, the exact rank prompt, full-frontier batch rule, greedy temperature 0, one completion per batch, and the same answer extractor Arm A will use. Any later edit voids the arm. Parse-fail rate is printed next to the solve count. If it is high enough that the arm matches the null in (1), the substitution sentence stays omitted.

**5. Skip-later on the canon negatives.**  
Quote: “Each gets a replicate/skip decision in the close receipt, none retrofitted.”  
A skip chosen after the numbers exist is a retrofit.  
Fix: write the replicate-or-skip bit for each named negative in the receipt before Arm A or C starts. The close receipt only fills the observed number.

Arm A’s “report as-is, >8/30 flagged” and Arm B’s frozen >=27/30 (already matched at 30/30 and 21/30 one-line) can stand. They are not the steal claim.

VERDICT: UNSOUND — the decision that would license “gemma substitutes the trained judge” is a >=15/30 line at a budget where this stack’s own search already solves 30/30 with and without merge, installed after that curve was known.

SUMMARY: Adversarial review of the pasted pre-registration and Amendment 1 only; no files or tools. The Arm C substitution inference is unsound because the surviving pass line cannot separate the judge from saturated search.

DELIVERABLE: The review above, with VERDICT UNSOUND.
