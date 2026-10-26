# W3 DUEL HARNESS - Receipt (2026-09-29)

Mickey17 Wave 3 lane: fix wave-ledger return 8 (watch/inbox/
MICKEY17_WAVE_LEDGER_20260929.md, RETURN 8/24 hermes integration): "THE
DUEL WAS FIRED BUT NEVER JUDGED: G1 (qwen) vs G3 (glm-prime) same-ask
cross-family comparison - the diff was promised in the prompt, never
computed. No scoring artifact exists."

## What landed

- `tools/duel_harness.py` (new): clones the gopher driver's call pattern
  (watch/inbox/game_platform_basecamp_20260929/hermes_gopher_burn_20260929.py:
  Nous inference API, keys from the hermes .env, reasoning cap 6000, cost
  metering preferring real `usage.cost` with the published-price table as
  fallback). Fires ONE ask to TWO models, then a THIRD cheap call
  (fireworks/ember-1) judges A-vs-B against a rubric embedded in the
  judging ask under a strict machine-parsed contract (WINNER line, per-
  criterion `CRIT | name | A=n | B=n | note` table, RATIONALE line).
  Appends one row to `logs/duel/duels.jsonl`: {ask_id, a_model, b_model,
  a_cost, b_cost, judge, winner, rubric, ts} plus mode, judge_cost,
  criteria, rationale, answer sizes. `--judge-rubric` overrides the
  default rubric (section coverage, defect severity, evidence citations,
  actionability). `--dry` prints the plan without calls or writes.
  Unparseable judge output banks winner=UNPARSED (never a fabricated
  verdict) and exits 1.
- Retroactive mode `--from-jsonl --a-id --b-id`: loads two already-paid
  answers from a burn output, fires only the judge, banks the verdict row
  with the real already-spent contender costs. One deliberate deviation
  from the gopher retry law, documented in the source: no model rotation
  on retry (rotating a contender corrupts the A-vs-B comparison); retries
  reuse the same model with the next key.
- `tests/test_duel_harness.py` (new): 8 tests, full pipeline on injected
  fake responses, zero network and zero spend (caller injected).

## The retroactive judgment (the duel that was never judged)

Contenders loaded from watch/inbox/game_platform_basecamp_20260929/
GOPHER_BURN_output3_healthy_20260929.jsonl (both answered the same
adversarial-review ask against BASELINE_SPEC.md in the 2026-09-29 burn):
G1 qwen/qwen3.8-max-prime (9,136 chars, $0.0674, paid in the burn) vs
G3 z-ai/glm-5.3-prime (6,773 chars, $0.0264, paid in the burn). Judge:
fireworks/ember-1, given the reconstructed ask plus the baseline spec as
reference document.

### VERDICT: WINNER B (G3 glm-prime), 19-16 on rubric points

| criterion | A (qwen) | B (glm) | judge note |
|---|---|---|---|
| section coverage | 4 | 5 | B covers 4.2, 5, cross-cutting; A skips exploration |
| defect severity | 5 | 5 | A's weighted-Wilson mismatch vs B's T2 algebra flaw; both deep |
| evidence citations | 3 | 4 | B cites doc paths and section numbers more precisely |
| actionability | 4 | 5 | B gives predicates and falsifiable tests per fix |

Judge rationale (verbatim): "Both find the n_min/threshold contradiction;
B adds T2 formula error, G1 tolerance gap, ECE variance, and testable
predicates."

Banked row: logs/duel/duels.jsonl line 1, ask_id
`retro-g1-vs-g3-adversarial-baseline-20260929`, ts 2026-09-30T00:25:36Z
(20:25 EDT 2026-09-29). Router-training consequence per the return 8
clause: on adversarial-review shapes, glm-prime won at 0.39x the qwen
token cost.

## Real costs (metered from usage.cost, not estimated)

- New spend this lane: exactly one ember judge call, $0.0248
  (prompt+completion metered by the API; 20.2 s).
- Contender costs ($0.0674 + $0.0264) were paid in the earlier gopher
  burn, only cited into the row; they are NOT new spend.
- Lane total: $0.0248 of the $0.50 budget.

## Tests (real line)

`./.venv/Scripts/python.exe -m pytest tests/test_duel_harness.py -q`
-> `8 passed in 0.55s` (2026-09-29, this seat; re-run after the parser
fix, first run was 3 failed / 5 passed on a case-sensitive WINNER regex).

Em-dash count in new files: 0.

## v1.1 - Judge blinding (S5 Arena audit) - 2026-09-29

Follow-up mission: the S5 steal-lane (Arena methodology) audited
tools/duel_harness.py and found a real v1.0 bug: judge_prompt() leaked
a_model/b_model NAMES to the judge inside the ANSWER_A/ANSWER_B tags.
LMSYS anonymizes contenders until after the vote because judge models are
biased by model identity; the v1.0 G1-vs-G3 verdict above was therefore
produced by a name-aware judge and is flagged accordingly (see honesty
note below).

What changed (all inside tools/duel_harness.py + its test):

- BLIND PROMPT: judge_prompt() no longer takes model names as parameters
  at all (a future edit cannot re-leak them); contenders appear as
  "anonymous models, A and B", identities logged in the ledger row only.
- POSITION-BIAS SWAP: slot A carries logical B's text whenever the ledger
  already holds an odd number of rows (parity alternation), so position
  bias cancels across consecutive duels; the banked winner and per-
  criterion scores are remapped to logical a_model/b_model terms, and the
  row carries "swap": true/false.
- STYLE-CONTROL SIGNALS: every row now logs markdown-header counts
  (a_headers/b_headers) alongside the existing lengths (a_chars/b_chars)
  for future volume-vs-content regression.
- README NOTE: the anonymization law lives in the tool's README section
  (module docstring, "Judge blinding (v1.1)" paragraph): blind judging,
  alternating presentation order, no identities in the judge context.
- Tests grown 8 -> 11: no-name-leak pin on the judge ask, swap verdict
  remap (judge votes slot A, row banks logical B), per-ledger parity
  alternation, header counting.

Tests (real line): `./.venv/Scripts/python.exe -m pytest
tests/test_duel_harness.py -q` -> `11 passed in 0.54s` (2026-09-29, this
seat; first run of the new suite was 1 failed / 10 passed on a test-side
call-index bug, fixed before landing).

Honesty note on the banked v1.0 verdict: the retro-g1-vs-g3 row in
logs/duel/duels.jsonl was judged name-aware (pre-fix). Re-judging it
blind costs one more ember call (about $0.02); left to the operator since
this mission's budget line covered only the fix.
