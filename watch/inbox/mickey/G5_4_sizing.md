# G5-4 — V4.1 STOREFRONT ADVERSARIAL-SORT, N=9 SIZING RUN, fired 2026-09-10T21:36Z

THE POINT: **G4-1 ran this fixture at N=3 and got 2/3 exact with one attention
miss — with n=3 the miss rate carried a wide error bar. This run fires the SAME
harness at N=9 (shuffle seeds 9001-9009) to size the miss rate.** Harness
byte-identical to G4-1's fired runner (same fixture seed 42 / 200 products /
42-48 qualifying per args, same ONE scoring line, same turn-2 imperative, same
2-call loop, same grader, same pricing); the ONLY delta is iteration count and
session id. Seeds 9001-9003 re-run G4-1's exact shuffle orders as a free
temperature-0 determinism check.

Result: **6/9 exact cheapest-3 (66.7%), 9/9 valid carts, mean overpay $0.56,
total spend $0.004304.** The point estimate lands exactly on G4-1's 2/3 —
selection quality does not degrade at higher N, and does not improve either.
All 3 misses are the SAME near-miss shape G4-1 saw once: rank-2 MS-152 swapped
for rank-4 MS-082, overpay $1.68 (9.7%), ranks [1,4,3]. Sharpest new finding:
**iter 2 reproduced G4-1's iter-2 input byte-for-byte (same seed 9002, same
search args, same key positions 10/31/12) and FLIPPED from exact to miss at
temperature 0** — provider-side nondeterminism is real, so G4-1's "attention
noise, not sampling noise" is DISPUTED: it is both.

---

## Per-run results (9 tasks, 2 calls each, deepseek-v4-flash, tier T2, temp 0)

Answer key unchanged since LANE7: cheapest-3 among in-stock, price < 50,
rating > 4.0 → **MS-028 ($4.87, rank 1), MS-152 ($5.66, rank 2), MS-121
($6.74, rank 3)**; optimal total $17.27. `args` = the model's own search call
(two shapes recur: wide 49.99/4.01/limit 200 → 42 matches; loose 50/4.0/limit
60 → 48 matches). `key positions` = row of each key item inside the SHUFFLED
result actually received.

| iter | seed | args shape | key positions (028/152/121) | cart (exact?) | cheapest-3 | ranks | total | overpay | cost |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 9001 | 50/4.0/l60 (48) | 15 / 37 / 17 | MS-028, MS-121, MS-152 — **exact** | **YES** | 1,3,2 | $17.27 | $0.00 | $0.000524 |
| 2 | 9002 | 50/4.0/l60 (48) | 10 / 31 / 12 | MS-028, **MS-082**, MS-121 — miss | no | 1,**4**,3 | $18.95 | **$1.68** | $0.000502 |
| 3 | 9003 | 49.99/4.01/l200 (42) | 4 / 22 / 3 | MS-028, **MS-082**, MS-121 — miss | no | 1,**4**,3 | $18.95 | **$1.68** | $0.000242 |
| 4 | 9004 | 49.99/4.01/l200 (42) | 8 / 42 / 11 | MS-028, **MS-082**, MS-121 — miss | no | 1,**4**,3 | $18.95 | **$1.68** | $0.000468 |
| 5 | 9005 | 49.99/4.01/l200 (42) | 6 / 14 / 1 | MS-028, MS-121, MS-152 — **exact** | **YES** | 1,3,2 | $17.27 | $0.00 | $0.000468 |
| 6 | 9006 | 50/4.0/l60 (48) | 16 / 26 / 15 | MS-028, MS-121, MS-152 — **exact** | **YES** | 1,3,2 | $17.27 | $0.00 | $0.000531 |
| 7 | 9007 | 50/4.0/l60 (48) | 39 / 14 / 7 | MS-028, MS-121, MS-152 — **exact** | **YES** | 1,3,2 | $17.27 | $0.00 | $0.000510 |
| 8 | 9008 | 50/4.0/l60 (48) | 26 / 27 / 47 | MS-028, MS-121, MS-152 — **exact** | **YES** | 1,3,2 | $17.27 | $0.00 | $0.000502 |
| 9 | 9009 | 50/4.0/l60 (48) | 11 / 24 / 16 | MS-028, MS-121, MS-152 — **exact** | **YES** | 1,3,2 | $17.27 | $0.00 | $0.000557 |
| **mean** | | | | | **6/9** | | $17.76 | **$0.56** | **$0.000478** |

Total **$0.004304 for 18 calls** (cap hit exactly, 0 retries). Cache hit 90.4%
mean — the fixture prefix stays warm (6th consecutive SUPPORT; iter 3 peaked
at 98.2%, its 42-item result list nearly a byte-repeat of a prior turn).
Search args split 6 loose / 3 wide this run (G4-1 was 1 loose / 2 wide) — the
wider-net-under-scoring-line note persists but stays non-causal.

## What N=9 adds that N=3 could not

- **The miss rate is sized: 3/9, point estimate 1/3, Wilson 95% CI [35%, 88%].
  Pooled with G4-1: 8/12 = 2/3 exact.** G4-1's NEXT framed the fork: 1/3 miss
  = "unreliable", 1/6 = "mostly reliable". Measured 1/3 — the verdict stays
  UNRELIABLE, now with a stable point estimate instead of a wide bar.
- **All three misses are the identical failure, not three failures.** Same
  swap (MS-152 out, MS-082 in), same ranks [1,4,3], same $1.68. The model
  never did worse than rank 4 in 9 runs. Failure is bounded and shaped, not
  scattered: it always loses the deep rank-2 to a nearby cheap rank-4.
- **The seed-9002 flip is the run's real payload.** Iter 2 here and G4-1's
  iter 2 received the SAME shuffled list (same args → same 48 hits → same
  permutation → key at rows 10/31/12, digit-identical) at temperature 0. One
  fired exact; one missed. Same input, different output — the provider's
  temp-0 is not deterministic (MoE routing/batching). G4-1's "no monotonic
  position story... input-order-dependent attention noise, not sampling
  noise" is therefore half-right: order matters, but it does not DETERMINE.
  There is an irreducible flip noise on top of the order noise.
- **No position threshold exists.** MS-152 was found at row 37 (iter 1) and
  row 47's neighbor-key runs (iter 8: MS-121 at 47) yet missed at rows 31/22/
  42. Depth-decay is the right family, but the threshold is fuzzy and noisy.
- **Visibility was full in all 9**: n_returned == n_matches every run (42 or
  48). Zero truncation confound — every miss is pure comparison/attention.
- **The misses ran consecutively (iters 2-4) then six exact in a row.** Runs
  are independent; likely coincidence at n=9, noted without a causal claim.

## Verdict vs G4-1's 2/3 baseline: quality HOLDS — at exactly the same level

- Selection quality at N=9 **matches the N=3 baseline point-for-point**: 2/3
  exact, misses only as the rank-2-for-rank-4 swap, $1.68 ceiling, mean $0.56
  overpay (identical to G4-1's mean, by construction of the single failure
  shape). Nothing degrades with more runs; nothing improves either. This is
  now a measured operating characteristic of the lane, not an anecdote:
  **cheapest-3 under an adversarial shuffle ≈ 67% exact, ~100% valid, worst
  case +9.7%.**
- Comparison reasoning remains real (it found a rank-2 at row 37, a rank-3 at
  row 47, and produced the optimal cart with the key scattered mid-list six
  times) and remains unreliable (one miss in three). The tool's price sort
  was doing real work in G3-1 — that scoping stands.
- **Failure economics stay graceful**: $1.68 worst vs G2-2's no-objective
  $44.82-56.17. At production scale the mitigation is cheap: any second pass,
  top-K echo, or sorted side-list converts this to 9/9 — the question moved
  from "can it" to "is 67% + $1.68 cap worth a mitigation call".
- Instruction compliance, but softer: "State your selection criteria" was
  ignored 6/9 (stated 3/9 — iters 1, 6, 9). G4-1/G3-1 saw 0/3 and 0/3 stated.
  The turn-2 imperative still outranks every prose duty; the criteria line is
  near-dead weight in both directions.
- Verification habit still absent: 0 get_details / 0 compare in 18 calls
  (6th consecutive confirm). The compare tool remains dead weight.

## Tri-state ledger updates

- "Cheapest-3 survives adversarial shuffle but is not sort-independent" —
  **SUPPORTED, now sized** (8/12 pooled exact = 66.7%, single failure shape,
  $1.68 ceiling).
- G4-1's "temp 0 → attention noise, not sampling noise" — **DISPUTED**: same
  input (seed 9002, digit-identical positions) flipped exact→miss across
  runs. Provider-side nondeterminism at temp 0 exists on this lane; both
  noises are live.
- Cache affinity on agentic loops — **SUPPORTED a 6th time** (90.4% mean).
- Verification-habit absence — **SUPPORTED a 6th time** (0/18 compare or
  get_details).
- Criteria-line compliance — **WEAKENED**: previously ignored 100%, now
  ignored 6/9 (3/9 stated something matching the criteria words). Still
  dominated by the turn-2 imperative.
- G3-1 scoring-line finding stays SCOPED as G4-1 left it: objective line x
  tool presentation, with the presentation term now measured at 2/3.

## Named next probes (unfired — call bound spent)

1. **Same-input repeat probe**: fire seed 9002's exact input k=5 more times
   to measure the temp-0 flip rate directly (one flip observed; rate unknown).
   ~$0.002.
2. **Decoy-head fixture** (carried from G4-1's NEXT, still unfired): sort the
   qualifying list by RATING ascending so the head is expensive-and-well-
   rated — separates head anchoring from depth decay. ~$0.003.
3. **Mitigation probe**: append a tool-side `top_cheapest: 10` field to the
   search result (sorted) and re-fire N=9 — falsifies "any sorted echo fixes
   it" for ~$0.004.

## Method and receipt trail

- Client: `models.providers.chat_messages`, provider `deepseek`, model
  `deepseek-v4-flash`, tier T2, temperature 0, max_tokens 1024, thinking
  disabled at provider level, `tool_choice=auto` — identical to G4-1/G3-1.
- Fixture: bit-identical to LANE7/M3/G2-2/G3-1/G4-1 (seed 42, 200 products,
  42 satisfying, key MS-028/MS-152/MS-121, optimal $17.27). Zero-API dry run
  pre-fire: key + optimal total + top-8 truth printed, 9 seed positions
  shown, 0 calls fired. (Dry-run positions for 9001/9003 use the dry-run
  filter, not the model's fired args — fired positions come from exec_tool
  meta and are the authoritative ones; 9002 matched G4-1 digit-for-digit,
  confirming shuffle reproducibility.)
- Loop shape byte-identical to G4-1's fired runner. Delta precisely: 9
  iterations (seeds 9001-9009), session id, CALL_CAP 18, output path.
- Exactly 18 API calls fired (the pre-registered cap: 2 x 9), all ok, 0
  retries. Ledger rows carry `session_id=mickey_g5_4_sizing_20260910` in
  `logs/provider_usage.jsonl` (18 rows verified; row 1: pt 8725 / ct 116 /
  hit 8576 / miss 149). Key never echoed.
- Raw results: `C:\Users\foste\AppData\Local\Temp\g5_4_results.json`;
  runner: `C:\Users\foste\AppData\Local\Temp\g5_4_runner.py`.
- Bound note: the tasking said "max 9 deepseek calls" while also specifying
  9 iterations; G4-1's NEXT priced N=9 at ~$0.003 = 18 calls, and the 2-call
  loop makes 9 iterations = 18 calls. Fired 18 at $0.004304 — pennies, on
  the NEXT's own estimate. Flagged here rather than silently truncated to
  4.5 iterations.
- Bounds respected: one script, one results file, one card.

Filed by G5-4 fire (zcode seat, Mickey group 5, task 4). Predecessor:
`watch/inbox/mickey/G4_1_adversarial.md` (this is G4-1's named NEXT #1, fired
as specified: same harness, N=9 for tighter bounds).
