# riblive1-U3-r1-glm-flash (glm-5.3-flash @ zai, turn 1, channel: content)

L1: zero-span recency never reaches 1.0
CLAIM: The spec says "span<=0 -> 1.0 for all" but the code branch `(1.0 if ts and ts_span == 0 and ts == ts_min and not known else 0.0)` can never yield 1.0, because `not known` is always False whenever `ts` parsed successfully. All same-timestamp blocks therefore get recency 0.0, not 1.0.
STEAL: Run `score_blocks` on two blocks sharing one valid ts and assert `recency == 0.0`; if confirmed, patch the branch to `(1.0 if ts and ts_span == 0 else 0.0)` and re-version the instrument.
FALSIFIER: A unit test where two blocks with identical valid timestamps score recency 1.0 under the current bytes.
SOURCE: mag/preload_selector.py score_blocks, "1.0 if ts and ts_span == 0 and ts == ts_min and not known else 0.0"
LEVERAGE: high

L1: empty shared set still yields DECORATIVE verdict
CLAIM: In `compare`, when arms share zero tokens (`dlp` and `scale` both empty), `mean_lp` is 0.0, so `rel_pct` is set to 0.0, and the verdict function maps that to "DECORATIVE" (kill). The instrument can emit its kill verdict from a measurement of nothing.
STEAL: Add a guard before verdict assignment: if `shared_positions == 0`, emit "UNMEASURABLE" instead of scoring rel_delta_pct.
FALSIFIER: A probe run where `shared_positions: 0` appears in the row together with `verdict: "DECORATIVE"`.
SOURCE: mag/preload_selector.py compare, "rel_pct = (100.0 * mean_dlp / mean_lp) if mean_lp > 1e-12 else 0.0"
LEVERAGE: high

L1: shuffled control differs by order only, seeded
CLAIM: The control arm uses `random.Random(seed)` with fixed default seed 20260907 over the same block list, so conditioned vs shuffled differ in ORDER ONLY, never content; selftest asserts determinism and multiset equality offline at $0.
STEAL: Run `python -m mag.preload_selector selftest` and read the five booleans; all must be True before any probe row is trusted.
FALSIFIER: `probe_subset_invariant=False` in selftest output, meaning arms no longer share the same block multiset.
SOURCE: mag/preload_selector.py shuffle_blocks, "The control: SAME block set, fixed-seed randomized order."
LEVERAGE: medium

L1: verdict scope is PROXY instrument only
CLAIM: Every row is labeled PROXY and uses a 2-3B local specimen (qwen2.5:3b-instruct, fallback gemma:2b) through host ollama; the F-W5 verdict answers only "does preload order move the field at all," never production resurrection fidelity on GLM-5.3-flash Max.
STEAL: Treat any DECORATIVE/LARGE_EFFECT verdict as an instrument-level ordering-sensitivity claim only; cite the honesty field in the row when reusing it downstream.
FALSIFIER: A row lacking `"label": "PROXY"` or claiming production fidelity from this instrument's metrics.
SOURCE: mag/preload_selector.py header, "it is NOT the production GLM-5.3-flash Max session."
LEVERAGE: medium

L1: position-wise alignment is documented-conservative
CLAIM: Shared-continuation metric aligns tokens by position index only; the spec itself notes this is "conservative when churn realigns later," so churn_rate and rel_delta_pct upper-bound disorder effects under realignment.
STEAL: When reporting churn, append the caveat or add an order-insensitive multiset overlap metric as a second column before trusting high churn numbers.
FALSIFIER: A run where a multiset-overlap metric shows high shared token content despite top1_churn_rate near 1.0.
SOURCE: mag/preload_selector.py metrics block, "position-wise alignment; conservative when churn realigns later"
LEVERAGE: low
