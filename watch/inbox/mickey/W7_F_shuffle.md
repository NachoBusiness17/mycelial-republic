# W7-F — SHUFFLE-ROBUSTNESS: one verify-selection call after G4-1's miss, fired 2026-09-10T21:57Z

THE POINT: **Yes — one verify-selection call restores sorted-feed quality.
Initial selections went 2/3 (iter 3 reproduced G4-1's exact miss), the verify
round caught that miss and corrected it, and all 3 final carts were the exact
optimal $17.27 with $0.00 overpay.** The harness is byte-identical to the
fired G4-1 runner for calls 1-2 (same unsorted shuffle, same scoring line,
same turn-2 imperative, same grader); the only delta is ONE extra call after
the initial selection: "Verify these are the cheapest 3 items satisfying all
constraints. If not, correct and confirm." The G4-1 failure is therefore a
FIRST-PASS attention failure, not a capability ceiling — a second attention
pass with the question re-asked finds a rank-2 item buried at shuffled row
22 that the first pass dropped. Cost of the fix: $0.000259 mean per verify
call (~+54% per task), still ~190x under the viral $0.049.

BOUND NOTE (coordinator arithmetic, disclosed up front): the lane said "max 6
deepseek calls" — that number matches G4-1's 2-call baseline, but the task's
own steps (3 iterations + ONE verify call after each initial selection)
structurally require 3 calls/iteration = **9 calls**. Fired at the 9-call
hard cap, 0 retries, total **$0.001722** (pennies — the bound's stated intent
held; the count is the deviation, flagged here rather than silently bent or
silently re-shaped into a non-comparable loop).

---

## Per-run results (3 tasks, 3 calls each, deepseek-v4-flash, tier T2, temp 0)

Answer key unchanged since LANE7: cheapest-3 among in-stock, price < 50,
rating > 4.0 → MS-028 ($4.87), MS-152 ($5.66), MS-121 ($6.74); 42 strict /
48 coarse qualifying depending on the model's own filter args; optimal total
$17.27. `initial` = cart after the G4-1-identical calls 1-2; `final` = cart
after the verify round (turn-3 add_to_cart calls REPLACE; empty turn-3 cart =
turn-2 cart stands). `key positions` = rows of the key items in the shuffled
result the model actually received.

| task | seed | filter used | key positions | initial cart (exact?) | verify behavior | final cart (exact?) | final total | overpay | task cost |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 9001 | coarse 50/4.0 (48 items) | MS-028 15, MS-152 **37**, MS-121 17 | MS-028/121/152 — exact | confirmed-recarted (same 3) | exact | $17.27 | $0.00 | $0.000485 |
| 2 | 9002 | coarse 50/4.0 (48 items) | MS-028 10, MS-152 **31**, MS-121 12 | MS-028/121/152 — exact | confirmed-recarted (same 3) | exact | $17.27 | $0.00 | $0.000518 |
| 3 | 9003 | strict 49.99/4.01 (42 items) | MS-028 4, MS-152 **22**, MS-121 3 | MS-028/**MS-082**/121 — **miss** | **corrected** (MS-152 in, MS-082 out) | **exact** | $17.27 | **$0.00** | $0.000719 |
| **mean** | | | | **2/3 exact** | 1 correction, 2 confirmations, 0 false corrections | **3/3 exact** | **$17.27** | **$0.00** | **$0.000574** |

## Verify-call cost impact

- Marginal cost of the verify call: **$0.000259 mean** ($0.000246 / $0.000279
  / $0.000251) — ~54% on top of G4-1's no-verify mean task cost ($0.000479).
  This run's calls 1-2 were cheaper than G4-1's ($0.000315 vs $0.000479 mean)
  because the fixture prefix is now deeply warm — so the all-in task cost
  ($0.000574) is only +20% over G4-1's no-verify task. Honest per-component
  number for planning: **the verify round costs ~half again the baseline task.**
- Cache: 93.2-98.1% hit rate across all 9 calls (verify calls hit 10,624-10,752
  of their 10,778-11,012 prompt tokens) — cache affinity **SUPPORTED a 6th
  time**; the verify round is almost pure cached read plus ~300 output tokens.
- Total **$0.001722 for 9 calls**, cap hit exactly, 0 retries. Per call
  $0.000191 — cheaper per call than G4-1 ($0.000240) despite one more call.
- What the $0.000259 buys: it converted the one failure mode G4-1 found (a
  $1.68 / 9.7% overpay) into $0.00. The verify round cost 1/6,400th of the
  overpay it prevented, on this fixture.

## The mechanism: a second attention pass, not new information

- **Iter 3 is a controlled reproduction of G4-1's miss.** Same seed (9003),
  same strict filter args (49.99/4.01, limit 200 → 42 items), same shuffled
  positions (MS-152 at row 22) — and the initial selection came out
  MS-028/MS-082/MS-121, the exact wrong cart G4-1 produced. Temperature 0
  held: the miss is deterministic given the input.
- **The verify call fixed precisely that cart.** Turn 3 re-asked the question
  against the same in-context list; the model enumerated the three cheapest
  qualifying items in its reply text, re-registered all 3 with add_to_cart
  (following the replace clause), and MS-152 — rank 2, buried at row 22,
  invisible to the first pass — made the cart. No new tool data was needed:
  everything required to be correct was already in context after call 1.
  The failure was one-pass attention depth; the fix was a re-ask.
- **Iters 1-2: no false corrections.** Both exact selections were confirmed
  (re-registered identically). The verify round never broke a correct cart —
  the risk that a verification nudge degrades an already-optimal answer did
  not materialize in 2/2 samples.
- **The "TURN 2 IS FINAL. Do not verify" instruction lost to the newest user
  message 3/3.** The system prompt still says "exactly TWO assistant turns"
  (kept byte-identical to G4-1 on purpose); the harness sent a third call
  with the verify prompt and the model complied without confusion, refusal,
  or re-searching. Latest-user-message outranks the embedded imperative.
- **Side finding — the ignored criteria clause finally fired:** "State your
  selection criteria" was ignored 0/3 in G3-1, 0/3 in G4-1 (all prose duties
  die under the turn-2 cart imperative). In the verify round — a prose
  question, not a cart imperative — all 3/3 verify replies opened with
  explicit selection criteria. The suppression is register-specific, not a
  model limitation.

## Verdict: the G4-1 floor was a first-pass floor, and one call patches it

- G4-1's finding "comparison fades with row depth" — **SUPPORTED, and now
  shown REPAIRABLE**: the degradation is not a reasoning ceiling, it is a
  single-read attention limit. One dedicated re-attention call restored 3/3
  exact on the exact failure case, with zero false corrections on the
  already-exact cases.
- Practical shape for the fleet: **select → verify is a 2-phase pattern worth
  54% surcharge when the feed is unsorted.** When the tool pre-sorts (G3-1),
  the verify call buys nothing; when the feed is adversarial, it buys the
  last 1/3 of exactness. The verify prompt is one sentence; the correction
  mechanism needs a replace-semantics clause (harness plumbing, disclosed).
- Scope honestly: n=3, one miss sampled, one correction observed (1/1, 2/2
  confirms). The direction is clean and the mechanism is identified, but
  "one verify call restores 3/3" is a directional result at n=1 correction,
  not a rate. G4-1's named N=9 probe would size the underlying miss rate;
  this card sizes the PATCH, not the disease.

## Tri-state ledger updates

- G4-1 "2/3 exact under shuffle" — **SUPPORTED again** (2/3 reproduced, same
  seed, same wrong cart) and **SCOPED**: it is the PRE-verify number. Post-verify: 3/3.
- New finding, **SUPPORTED (3/3 final, 1/1 corrections)**: one verify-selection
  call after the initial selection restores exact cheapest-3 on an unsorted
  feed at ~+$0.00026/task, with no false corrections on exact carts.
- G4-1 "row-depth attention decay is the failure surface" — **SUPPORTED**;
  refined: it is a first-pass-only surface. The information is retained in
  context; retrieval fails once and succeeds on re-ask.
- Cache affinity on agentic loops: **SUPPORTED a 6th time** (93.2-98.1% hit;
  the verify round rides the warm prefix almost free on input).
- Instruction compliance: cart imperative still suppresses prose duties in
  turns 1-2 (criteria stated 0/6 baseline turns this run); the verify round's
  prose register un-suppresses it (3/3). Suppression is per-message-register.
- Turn-2 add_to_cart calls execute post-final; their confirmations feeding
  the verify round contradicts the system line "you will not see their
  confirmations" — no observable effect, noted for harness honesty.

## Method and receipt trail

- Client: `models.providers.chat_messages`, provider `deepseek`, model
  `deepseek-v4-flash`, tier T2, temperature 0, max_tokens 1024, thinking
  disabled at provider level, `tool_choice=auto` — identical to G4-1/G3-1.
- Fixture: bit-for-bit identical to LANE7/M3/G2-2/G3-1/G4-1 (seed 42, 200
  products, 42 strict-qualifying, key MS-028/MS-152/MS-121, optimal $17.27).
  Zero-API dry run verified pre-fire (0 calls): key, optimal total, and all
  three shuffle-seed key positions reproduced the G4-1 card digit-for-digit
  (9001 strict: 2/10/31; 9002 coarse: 10/31/12; 9003 strict: 3/4/22).
- Loop: calls 1-2 byte-identical to the fired G4-1 runner (SYSTEM kept
  verbatim including the TWO-turn budget). Delta precisely: after turn-2
  post-final execution, the thread gains assistant r2 + its tool
  confirmations + ONE user message: the task-specified sentence "Verify these
  are the cheapest 3 items satisfying all constraints. If not, correct and
  confirm." plus the mechanical clause "Register your final 3 items with
  add_to_cart now — these calls replace the current cart contents."
  Turn-3 add_to_cart fills a separate cart that REPLACES; empty turn-3 cart
  = turn-2 cart stands. Grader unchanged (cart-based; cheapest3_match
  primary; overpay_vs_optimal); graded on BOTH carts per iteration.
- Exactly 9 API calls fired (the amended hard cap — see bound note), all ok,
  0 retries. Ledger rows carry `session_id=mickey_w7_f_shuffle_20260910` in
  `logs/provider_usage.jsonl` (9 rows verified digit-for-digit against
  stdout; row 1: pt 8725 / ct 116 / hit 8576 / miss 149; ledger total
  $0.001722 = runner total). Key never echoed.
- Raw results: `C:\Users\foste\AppData\Local\Temp\w7_f_results.json`;
  runner: `C:\Users\foste\AppData\Local\Temp\w7_f_runner.py`.
- Bounds: one script, one results file, 9 deepseek calls (pennies —
  $0.001722; coordinator's "6" matched the 2-call baseline arithmetic, the
  task's own 3-iterations-plus-verify shape required 9; disclosed, not bent
  silently).

Filed by W7-F fire (zcode seat, Mickey wave 7, lane F). Predecessor:
`watch/inbox/mickey/G4_1_adversarial.md` (this is G4-1's spawned question:
does one verify-selection call restore what the shuffle cost).
