# UNCONFIRMED BANK: bnjmn_marie quantized-agentic run-variance finding

Status: UNCONFIRMED-AS-POST-10-01, CONFIRMED-AS-2026-09-14-CONTENT. Banked 2026-10-02 by the fold seat so the finding has a citable landing spot (cold-reader issue 3). Deliberately NOT a register.jsonl row: the register mirrors the confirmation pass's confirmed set, and this item failed it on one label.

## Source

- URL: https://x.com/bnjmn_marie/status/2099579957207048696
- Title: "Quantized Qwen3.8 27B for agentic coding: Same Score, 42 Different Outcomes"
- Correct date: 2026-09-14 (see dating evidence below). The originating sweep (quantization-compression via x, sweep/quantization-compression-x.md) labeled it "Post-10-01"; that label is false.

## What is verified (confirmation-pass evidence, relayed verbatim from the fold input; the fold did not re-fetch the page this sitting)

- Quote VERIFIED verbatim in two independent WebFetch fetches: "Don't trust anyone reporting a quantized model's accuracy on agentic tasks without also reporting the run-to-run standard deviation."
- Numbers VERIFIED against the page: two identical-setting 4-bit AWQ runs scored 38.94% vs 31.86% Reward (a 7.08-point spread); 32 of the 113 task outcomes flipped between them (20 previously solved tasks failed, 12 previously failed tasks passed); NVFP4 scored 31.86% - exactly AWQ run 2's aggregate - while 42 task outcomes flipped, both configs solved 36 tasks with only 15 successes in common; DeepSWE 1.1 with the Pi harness and thinking mode; BF16 baseline 43.36%.

## Dating evidence (why it fails the post-10-01 label)

- Page-displayed timestamp: 7:24 PM - Sep 14, 2026.
- Independent snowflake decode run during the confirmation pass: `python -c "ts_ms = ((2099579957207048696 >> 22) + 1288834974657); import datetime; print(datetime.datetime.fromtimestamp(ts_ms/1000, datetime.timezone.utc).isoformat())"` -> `2026-09-14T19:24:04.764000+00:00`.

## Disposition

- The variance substance is real and load-bearing: any single-run quantized-agentic score cell within ~7 points is one sample, not a ranking. Use it as a 2026-09-14 finding.
- NEVER cite it as post-10-01 evidence. If a future digest needs a post-10-01 run-variance primary, PostTrainBench v1.2 (register row 2) is the verified in-window one.
- The "extends rather than overturns the estate's 3-bit floor" framing in the original sweep item is estate-internal interpretation, not page content.
