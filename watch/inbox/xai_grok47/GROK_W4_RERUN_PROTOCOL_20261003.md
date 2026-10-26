# GROK_W4_RERUN_PROTOCOL_20261003.md (grok-4.7, 2026-10-03T13:27Z)

The rerun contract below is a pre-launch protocol, not a completed run. It does not replace the filed 2026-09-25 verdict. Until a rerun finishes under this contract, cite that verdict, not the "20/20 ok" summary.

Design review against the contract: the 09-25 run cannot be repaired in place. A fleet-executable rerun is possible in one night only if the preflight gates pass and the throughput abort is honored. If either fails, the required outcome is abort, not a smaller sample.

## Cited vs unverified

Cited from `watch/GAUNTLET_W4_VERDICT_20260925.md` (filed 2026-09-25, criterion 6 as summarized there):

- Bar: warm-cache obedience ≥ cold obedience, `cachedTok` ≥ 95% of prefix size, across ≥50 varied tails. FAIL if obedience degrades by more than 5 percentage points warm-vs-cold, or the cache rebuilds.
- Recount of `watch/gauntlet_w4_receipts.jsonl` (60 rows): WARM 30 trials, 10 HTTP-200, 7 obey, rate 0.70, cacheFloorOk 10/10 on valid rows. COLD 30 trials, 10 HTTP-200, 8 obey, rate 0.80. Delta −10 percentage points. n=10 valid per arm. 40/60 rows had `model="DEEPSEEK_API_KEY"` (20 per arm) instead of `deepseek-chat`.
- Owed fixes named in that verdict: real model id, ≥50 tails per arm, `cacheFloorOk: null` on non-200 rows.
- Verdict field gap: `tools/fold_mickey17.py` summaries now render a verdict field. That is a citation of the verdict doc, not a verification that the tool accepts a rerun id.

Unverified from this desk (do not treat as measured): full text of `GAUNTLET_PREREGISTRATION_20260901.md` beyond the criterion 6 summary, warmup procedure, obey-scorer code, tokenizer, JSONL key names other than those used above, provider cache scope and TTL, lane count, rate limits, night-window clock, and any post-fix non-200 rate. The 40/60 model-id failures are not a transport-error prior. Do not use them to size retries.

If the preregistration names a model id other than `deepseek-chat`, stop and resolve that conflict before launch. Do not guess.

## Falsifier (freeze this block before trial 1)

Primary claim under test, as summarized in the 2026-09-25 verdict: steering obedience at warm cache is at least obedience at cold, and `cachedTok` is at least 95% of prefix size, across at least 50 varied tails.

This rerun falsifies the obedience half if, and only if, the analysis set below exists and `(obey_rate_cold - obey_rate_warm) > 0.05`.

This rerun falsifies the cache-floor sub-claim if any warm HTTP-200 row that otherwise qualifies has `cachedTok < 0.95 * prefixSize`, or the cache rebuilds under that same rule.

Analysis set, all required: paired identical tails, both arms HTTP-200, outbound `model` equals the pinned id `deepseek-chat`, warm `cacheFloorOk` true, cold row not cache-contaminated, and n ≥ 50 such pairs. `cacheFloorOk` must be null on every non-200 row in the receipt file.

n < 50, a wrong model id, or non-null `cacheFloorOk` on a non-200 row makes the run INVALID. An invalid run is not a confirmation and is not a clean behavioral falsification. Do not report its rates as model behavior.

PASS only if both halves hold on that analysis set. A miss on either half is FAIL. This rerun does not rewrite the 2026-09-25 FAIL+INVALID filing. A later PASS supersedes only the forward claim under this protocol version.

No early stop on the delta. The 5 percentage point bar is the preregistered rule, not a newly estimated minimum detectable effect. No confidence interval was in the verdict, and none is added here.

## Abort conditions

Fire these independent of how the rates look.

- A1. Outbound request field `model` is `DEEPSEEK_API_KEY`, empty, an env-var name, or anything other than the pinned id. Abort before trial 1.
- A2. Writer check fails: a non-200 fixture does not yield `cacheFloorOk: null`. Abort before trial 1.
- A3. Obey scorer is not pinned to the scorer used for the 09-25 recount. Abort before trial 1.
- A4. Fewer than 50 varied tails in the pinned list, or the list is not recoverable. Do not author substitute tails and do not pad with duplicates. Abort before trial 1.
- A5. Warmup procedure or prefix-size method is not recoverable from the preregistration or the original runner, or numerator and denominator would use different tokenizers. Abort before trial 1. Do not invent a warmup payload.
- A6. Projected wall time under the cache-isolation rule exceeds the remaining night window, or mid-run remaining attempts cannot reach 50 valid pairs before window end. File INCOMPLETE. Do not launch or finish an underpowered n.
- A7. A cold HTTP-200 row meets the warm floor (`cachedTok` ≥ 95% of prefix size). That row is contaminated, not cold. If replacements cannot restore 50 confirmed-cold pairs inside the window, file INCOMPLETE. Do not relabel those rows as warm.
- A8. `cachedTok` or prefix size missing or unparseable on an HTTP-200 row. Instrumentation abort. No obedience verdict.
- A9. Auth, sustained 429, or billing errors make further HTTP-200s impossible. File INCOMPLETE. Do not swap model ids to keep going.
- A10. Any data row whose `model` field is not the pinned id. Abort the rest. Do not mix ids in one contrast.
- A11. Outcome-dependent stop is forbidden. Crossing or clearing the 5 percentage point line is not an abort.

Allowed filing labels: ABORTED_PREFLIGHT, INCOMPLETE, INVALID, FAIL, PASS. Compound labels are allowed when both apply, matching the 09-25 practice. A missing verdict field is itself a filing failure.

## One-night protocol

0. Freeze this text, the falsifier block, the abort list, the tail-list hash, the spare-list hash, the pinned model id, and the operator-set window end in the launch record before any trial. No edits after trial 1.

1. Preflight, not counted in n. Read the outbound JSON `model` field and assert it equals `deepseek-chat`. Assert the API key is present without writing the key into receipts or logs. Run the A2 writer fixture. Hash the primary tail list of at least 50 varied tails and a predeclared spare list. Record prefix size by the same method the cache metric uses. Time one cold probe and one warm probe for the A6 projection. Exclude probes from n.

2. Cold phase first, all of it, before any warmup. Same tail order for every arm. One predeclared retry on non-200 only, then the next prelisted spare. No retry because obey failed. Within-arm parallelism is allowed only if cache isolation still holds. Provider cache scope is unverified, so the default is serial. If a parallel plan is proposed, it still has to pass A7.

3. One warmup, using only the recovered procedure (A5). Then the warm phase, same tail order, same retry rule.

4. Per row, record at least: `model`, HTTP status, obey, `cachedTok`, prefix size, `cacheFloorOk`. Set `cacheFloorOk` true only on HTTP-200 when `cachedTok` ≥ 95% of prefix size. Set it false on HTTP-200 when the floor misses. Set it null on every non-200. A floor miss is a sub-claim failure, not a row to drop in order to protect the rate.

5. A pair counts toward n only when both arms are HTTP-200, warm floor holds, cold is uncontaminated, and `model` is the pinned id. If spares run out before n = 50, file INCOMPLETE (A6). Do not resample a tail because of its obey bit.

6. Summary must lead with the verdict label. Do not print an "ok" line from the valid-subset view alone. That misread is why the prior result sat unfiled and was over-read, per the 09-25 verdict. Point the fold at the verdict-rendering path cited there if it accepts this rerun id. If it does not, write the verdict by the frozen rule and mark the tool gap unverified.

## Decision rule at fold time

- Any of A1 through A11: ABORTED_PREFLIGHT or INCOMPLETE. No PASS.
- Instrumentation dirty or n < 50 valid pairs: INVALID. No obedience headline.
- One or more warm HTTP-200 floor misses: cache-floor sub-claim FAIL. Obedience is scorable only if floor-ok uncontaminated pairs still number at least 50. Otherwise obedience is INVALID and the floor FAIL stands alone.
- Clean n ≥ 50 and cold rate exceeds warm rate by more than 5 percentage points: obedience FAIL, protocol valid.
- Clean n ≥ 50, degradation ≤ 5 percentage points, and every analysis-set warm row at or above the floor: criterion 6 PASS for this protocol version only.

Cite the receipts path actually written, the launch-record hash, and the 2026-09-25 verdict. Do not cite a rate this protocol has not measured.
