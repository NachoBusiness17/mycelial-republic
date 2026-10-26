# W4/AA1 OPUS RETURN: anthropic/claude-opus-5.5 (Nous), 2026-09-30 refire (stream)

Status: ok. Metered cost: $0.6909. Seconds: 362.4. Usage: {"prompt_tokens": 12729, "completion_tokens": 32000, "total_tokens": 44729, "prompt_tokens_details": {"cached_tokens": 0, "cache_write_tokens": 0, "audio_tokens": 0, "video_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 29476, "image_tokens": 0, "audio_tokens": 0}, "cost": 0.690916, "cost_details": {"source": "openrouter_list", "floor_applied": false, "rate_source": "openrouter_catalog"}}. Finish: length.
Full return below, verbatim. Em-dash count in return body: 0.

---

## A. VERDICT ON THE BASELINE

| Section | Verdict | One-line reason |
|---|---|---|
| 0 Provisional authority | KEEP | Correct stance: the instrument survives every kill rule, and routing must be earned. |
| 1 Definitions | TIGHTEN | lb95 does not say which n it uses (weight sum or raw count), and "model" is a string, not bytes (see B-D5, B-D8). |
| 2 Schema | TIGHTEN | The signature scope conflicts with Am2 rebase. pass_rate_raw and cost_usd_last are redundant or cross-clock. The PK lacks environment identity. |
| 2 Wilson formula | KEEP | The arithmetic is correct. Only the choice of n is undefined. |
| 3.1 Gate classes | TIGHTEN | G0 checkers are not bound to code. G1 treats "agreement" as pass even when both raters agree it failed. The G3 cap is satisfied by 1 G0 verdict plus 999 G3 verdicts. |
| 3.2 Who can write | TIGHTEN | The G0 exemption lets an answerer self-grade with an unregistered checker. G1's second scorer is never recusal-checked. |
| 3.3 Artifact | TIGHTEN | It correctly names the (model, version, environment) triple, but section 2 aggregates by model_id string. |
| 3.4 Attribution | TIGHTEN | "No verdict for low-confidence stops" is right for ungated stops. When a G0 gate exists it creates survivorship bias in cell rates and in ECE. |
| 4.1 Selection | TIGHTEN | Decay raises cells below 0.5. Fail verdicts refresh freshness. The fallback routes to the cheapest model even when it is known-bad. n_min = 20 is dead at threshold 0.85. |
| 4.2 Exploration | KEEP | Mandatory gating of exploration traffic is the right graduation path. The bandit deferral is correct. |
| 4.3 Triggers | TIGHTEN | There is no gate-fail trigger. T2 is dominated as a post-answer trigger. T3 and T4 are unreachable except via the fallback. The T1 verification sample is drawn from the wrong region (section C). |
| 4.4 Probe budget | TIGHTEN | A USD leash does not bind a fleet that is 95% local at near-zero USD. |
| 5 Receipts | TIGHTEN | ledger_snapshot_hash is not replayable unless the snapshot is stored. The chain tip is. |
| 6 Scope fences | KEEP | Falsifiable and well chosen. F-S1 "order 300" is consistent with the graduation arithmetic in B-D5. |
| 7 Harness | TIGHTEN | K3 fires by construction under 4.1 arithmetic (section D, attack H2). K2 is underpowered at n = 200 (section F). |
| 8 Falsifiers | TIGHTEN | Missing: silent weight swap, hot-input inflation, fail-refreshed drift, future-dated timestamps. |
| 9 Non-goals | KEEP | Honest. |
| 10 Diff contract | KEEP | Usable. Section F notes its bias. |
| Am1 | TIGHTEN | T1 is now reachable in name. ECE at n = 20 is near noise (UNPROVEN magnitude, predicate in E). |
| Am2 | TIGHTEN | A rebase that changes prev_sha256 invalidates any signature covering it. |
| Am3 | TIGHTEN | Operators are inferred from requesters. With the default operator_id 'estate', the result is a G1/G2/G3 deadlock. |
| Am4 | TIGHTEN | Predicate 3 is wrong as written (section F). Predicates 2 and 5 need rewriting after B-D4 and C. |

**Where it is actually weak.** The write side is strong: chain, keys, idempotency, recusal intent. The read side is statistically fragile in three ways:

- **Drift is invisible within the K3 budget.** Cumulative counts with age-since-last-verdict decay cannot detect drift inside the harness's own budget. A fail verdict refreshes the clock it should be alarming.
- **Calibration is certified from the wrong region.** T1 acts on answers below min_confidence, but calibration evidence is sampled almost entirely above that threshold, because low-confidence stops go ungated.
- **Identity is a label, not bytes.** The unit of truth is a model tag. The lab's own law says to trust bytes, yet the ledger's key is a string any operator can repoint to different weights.

A production fleet needs detection latency measured in single-digit verdicts and identity bound to weights. The baseline delivers neither.

## B. SPEC DELTAS

Every delta's predicates are specified in section E.

| # | Change | Section | Clause | Why better, not merely different |
|---|---|---|---|---|
| D1 | Principal signs verdict_id only (content hash over the row minus verdict_id, prev_sha256, row_sha256, signature). The writer's row_sha256 covers content, signature and prev_sha256. A rebase changes only prev_sha256 and row_sha256. | 2, Am2 | 5 | As written, an Am2 rebase either breaks signatures (quarantine storm under contention) or forces the writer to hold principal keys, which collapses 3.2. |
| D2 | eff_lb95 = w*lb95 + (1-w)*min(lb95, p0) | 4.1(3) | 5 | The baseline blend lifts any cell with lb95 < 0.5 toward 0.5 as it ages. That violates "decay only demotes" and Am4 predicate 3, and it feeds T2 an optimistic P(fail). One-token fix. |
| D3 | RECENT-WINDOW GUARD (RWG). Over a cell's last r = 10 counted verdicts (G0 to G2), suspend if fails >= f, with f the smallest integer satisfying P(Binom(r, 1-threshold) >= f) <= 0.05. At threshold 0.85: f = 4 (computed tail 0.0500). A suspended cell does not qualify, gets reason_code rwg_suspended, and has a probe round scheduled. | 4.1, 7 K3 | 3 | New falsifier F6: fail-refreshed drift. Under the baseline, total collapse of a 300-verdict cell at 0.95 needs about 21 fresh fails to demote (section D, H2), so K3's 10-verdict ceiling is breached by arithmetic. RWG demotes at the 4th fresh fail. False suspension per window is about 0.1% at a true rate of 0.95 and 5% at exactly the threshold (binomial, computed). r and alpha are DESIGN DEFAULTS measured by M4/K3. This is a pre-registered fixed test, not a bandit. |
| D4 | G3 verdicts are written, chained and reported, but excluded from the passes, fails and n read by 4.1 and 4.3. Delete the G3 CAP clause and Am4 predicate 2. G3 re-enters routing only with a weight equal to its measured agreement with G0 on shapes where both run (a query over verdict, no new table). | 3.1 | 4, 2 | The cap as written lets 1 G0 verdict plus any number of G3 verdicts qualify. Weight