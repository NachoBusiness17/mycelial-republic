# D6 - ask-bank duel: first live hidden draw (2026-09-30)

Owner of record: D6 (file ownership per dispatch). Draw: **ask_bank v1 draw
v1h-0002** (`ab1-coremem-safeguard`, shape `safeguard`, 4777 rendered chars).
Per the AJ2 convention only the first line is quoted here:

> You are an adversarial specification reviewer hunting the missing guardrail. Below is the full text of docs/ref/CORE_MEM

The full ask never touched a prompt-visible path: the driver
(`d6_askbank_duel.py` in this directory) captured the `draw --hidden --reveal`
subprocess output in memory and piped it straight into the contender prompts.
The bank verified clean before the run (`ask_bank.py verify`: ok, 20/14/6).

## Series result: glm-prime 3 - 0 gemini-3.8-flash

3 rounds, both contenders fired FRESH per round (streaming SSE calls, V1
shape), ember blind judge, slot swap alternating by ledger parity. No DNF.
All rows share corr_id `c76e6d0e` (AH14 series mint), mode `askbank`.

| round | ask_id | winner (logical) | swap | glm cost | gem cost | judge | glm chars/headers | gem chars/headers |
|---|---|---|---|---|---|---|---|
| 1 | d6ab-r1-glm-gem | A (glm-prime) | true | $0.0174 | $0.0400 | $0.0156 | 5766/5 | 5626/6 |
| 2 | d6ab-r2-glm-gem | A (glm-prime) | false | $0.0168 | $0.0296 | $0.0151 | 4293/3 | 5971/6 |
| 3 | d6ab-r3-glm-gem | A (glm-prime) | true | $0.0146 | $0.0287 | $0.0157 | 4990/3 | 5172/6 |

Judge criteria went to glm 9 of 12 (r1: A wins 3 of 4; r2: 4 of 4; r3: 3 of
4). glm won under BOTH slot layouts (swap true and false), so position bias
cannot explain the sweep. Judge-quirk disclosure, honestly banked: in rounds
1 and 3 the ember rationale prose praises B's clause-tracing style while the
criteria table and verdict still favor A on severity and citations; the
verdict is scored, not vibes. Both models converged on the same missing
safeguard finding (a write-back mandate gap in the material's law set), glm
pairing it with runnable test code, gemini with step-by-step clause walks.

## The clean-signal value (the contamination question)

This is the first duel where the ask was provably unseen: hidden half is
gitignored, never in any prompt-visible path, drawn for the first time. The
contrast arm is V1 multifamily (W8 material in plain sight): there
gemini-3.8-flash swept glm-prime 3-0 (v1mf-r1/r2/r3-glm-gem, winner B each
time, with glm carrying a disclosed ask-mismatch handicap). On fresh hidden
material, handicap-free both sides, the result fully inverts: glm-prime
3-0. One draw at n=3 proves nothing about the models in general, but it
demonstrates exactly what AJ2 was built to expose: plain-sight-ask duel
verdicts are contamination-suspect, and the hidden bank can flip them. Also
price-relevant: glm won at $0.0146-0.0174/answer vs gemini $0.0287-0.0400.

## gps ledger rows (real traffic, the meter feeding itself)

6 verdict rows (3 winner-pass, 3 loser-fail) recorded via
`CapabilityLedger.record_verdict`, evidence_hash = sha256 of each exact
banked duels.jsonl line (verified joining byte-true: `011ce6662de92145`,
`c09b03bcb298b99c`, `d7bc6062c4ddb1e8`). TIE/UNPARSED would have fed
nothing; none occurred. Resulting capability rows:

```
model_id                  task_shape               pass_rate  n
z-ai/glm-5.3-prime        askbank-v1-safeguard     1.0        3
google/gemini-3.8-flash   askbank-v1-safeguard     0.0        3
```

Incident + fix (receipt-carrying): the driver's tally loop shadowed the
bank `ask_id` variable, so the rows first landed under task_shape
`askbank-v1-gem` (the duel id's model suffix, not the ask shape). Cause:
`for ask_id in duel_ids:` reused the bank ask id name. Fix: loop variable
renamed to `did` in the driver, and the 6 verdict_log + 2 capability rows
were relabeled `askbank-v1-gem` -> `askbank-v1-safeguard` by surgical
UPDATE preserving every value (before/after dump in the run log; zero
residual mislabeled rows). A duplicate `feed_gps` call introduced during
the edit was caught and removed before any rerun (no double feed).

## Budget (cap $0.50, absolute)

- Series spend: **$0.1935** (contenders $0.1471 + judges $0.0464). Cap never
  approached; round projections $0.16 each, 3 x 0.16 = 0.48 pre-cleared.
- Preflight (disclosed): 3 ember probe calls totaling about $0.0011 (first
  probe starved at 16 max_tokens and returned empty content twice; 512
  tokens answered OK).
- Total mission spend: ~$0.2046 against the $0.50 cap.

## Artifacts

- Driver: `watch/inbox/last_mile_20260930/d6_askbank_duel.py` (dry mode
  computes the would-be draw without appending; idempotent on banked
  ask_ids; contender cache `d6_contenders.jsonl`; run log `d6_run.log`).
- Duel rows: `logs/duel/duels.jsonl` rows d6ab-r1/r2/r3-glm-gem (ledger
  now 76 rows).
- Draw ledger: `configs/ask_bank/v1/hidden/draws.jsonl` v1h-0002.
- gps db: `tools/gps_mcp/gps_ledger.db3`.
