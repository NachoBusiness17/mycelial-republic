# F1 - FLASH VS MAX: glm-5.3-flash vs glm-5.3-prime head-to-head - 2026-09-30

Mission (operator): "can we functionally tell whether 5.3 flash is any
better than our 5.3 max". Nous lists no glm-5.3-max; z-ai/glm-5.3-prime
is the estate's proven top GLM rung (V9 table rank 6, duel-proven) and
the sanctioned max stand-in. Same family both sides, so this is the
intra-family convergence test the G2 gate needs.

Fence honored: tools/duel_harness.py used unmodified (v1.1 blind judge,
slot swap by ledger parity, corr_id minting); logs/duel/duels.jsonl
appended (76 -> 80 rows); this receipt is the durable copy. Keys: Nous
(NOUS_SDD_API_KEY from hermes .env, 1 key live). Cap $0.30; total lane
spend $0.1152 (banked contender+judge $0.1151 + liveness probes
$0.0001). No em-dash in any F1 output.

## Design

- 3 HIDDEN asks drawn clean: ask_bank v1 draws v1h-0003, v1h-0004,
  v1h-0005 (subprocess draw --hidden --reveal captured to memory,
  piped into contender prompts only; first lines quoted below, the AJ2
  secrecy law). Three different shapes: safeguard, defects, falsify.
- Duel shape: flash = logical A, prime = logical B, fixed; ember blind
  judge; swap alternated per round by ledger parity (F, T, F, T) so
  flash won 2 rounds from slot A and 2 from slot B: position bias
  (LW9 p=0.0436) cannot explain the sweep.
- Code task (real building, not prose): both wrote duelsum, a stdlib
  CLI summarizer for duels.jsonl-shaped ledgers (spec
  f1_code_spec.md). Graded BYTE-exact against the lane owner's
  reference (f1_ref_impl.py, not a model) on 4 fixtures: the in-ask
  example, empty file, edge pile (invalid rows, missing fields, empty
  criteria, UNPARSED, tie, two pairs with ordering), missing path.
  Functional pass counts are a hard metric independent of the judge;
  the ember duel then scored both codes blind with the factual test
  results in the shared context (slot-terms, blind-safe).
- Series scripts: f1_series.py (prose duels) + f1_code_duel.py (code
  duel), budget gate before every fire, contender cache resume,
  streaming contenders (V1/D6 shape), width 1.

## RESULT: flash sweeps 4-0, at 1/19th the contender cost

Prose rounds (rubric: section coverage, defect severity, evidence
citations, actionability; scores flash vs prime, logical terms):

| round | draw / shape | swap | winner | scores flash vs prime | flash chars/hdr | prime chars/hdr | costs flash/prime/judge |
|---|---|---|---|---|---|---|---|
| f1ab-r1 | v1h-0003 safeguard | F | FLASH | 5-4, 5-5, 5-4, 5-4 | 5088/4 | 4112/6 | $0.0006/$0.0116/$0.0127 |
| f1ab-r2 | v1h-0004 defects | T | FLASH | 4-4, 5-4, 5-5, 5-4 | 5547/5 | 5310/4 | $0.0009/$0.0181/$0.0166 |
| f1ab-r3 | v1h-0005 falsify | F | FLASH | 5-4, 4-4, 5-4, 5-4 | 6606/10 | 5384/3 | $0.0009/$0.0166/$0.0190 |
| f1ab-code | duelsum CLI | T | FLASH | 5-5, 5-5, 5-5, 5-3 | 2152/0 | 2022/0 | $0.0003/$0.0077/$0.0101 |

Code task hard functional result: BOTH passed 4/4 fixtures
byte-exact (100 percent functional equivalence). The only judged gap
is style: prime's solution calls `__import__("json").loads(line)`
inline instead of a normal import; flash's is idiomatic throughout
(judge note, prime is slot A there). Outputs: f1_code_out/flash.py,
f1_code_out/prime.py, f1_code_out/results.json.

Hidden-ask first lines (AJ2 convention, at most the first line):
- v1h-0003: "You are an adversarial specification reviewer hunting the
  missing guardrail. Below is the full text "
- v1h-0004: "You are an adversarial specification reviewer. Below is
  the full text of docs/ref/COMMON_LANGUAGE_SP..."
- v1h-0005: "You are a falsification engineer. Below is the full text
  of docs/ref/CHAIN_V2_ANCHOR_REGISTRY_SPEC.m..."

## The metrics asked for

1. WIN/LOSS: flash 4, prime 0, ties 0. Criterion point sums: flash
   78/80, prime 68/80.
2. PER-CRITERION: flash dropped exactly one point per prose round
   minus r2 severity tie (flash prose 58/60, prime 50/60); code task
   flash 20/20, prime 18/20.
3. LENGTH: max does NOT out-write flash. Prose answers: flash avg
   5747.0 chars (19 headers), prime avg 4935.3 (13 headers); flash
   +16.4 percent longer and richer-structured. Code: 2152 vs 2022
   (par).
4. CONVERGENCE (same family, do they agree?): score ties 7 of 16
   criteria = 43.8 percent (prose 4/12 = 33.3, code 3/4 = 75).
   Semantic convergence is far higher: judge rationales record both
   models finding the SAME core defect in all 3 prose rounds ("Both
   find the same gap", "Both identify C2 as weakest") and 100 percent
   byte-identical functional behavior on code. They disagree on
   polish, not findings: prime consistently loses points on thinner
   clause citation and less concrete predicates.
5. COST/SPEED: flash $0.0007 avg/answer vs prime $0.0135 (19.3x);
   whole lane $0.1152 of the $0.30 cap. Prime's ONLY measured win is
   wall-clock: ~2x faster generation (13-20s vs 23-46s prose), it
   just produces less per answer.

## Verdict

Functionally telling them apart: yes, easily, and flash wins every
quality axis measured (4-0 sweep, +10 rubric points, longer richer
answers, 19x cheaper, byte-perfect code). Prime showed NO measurable
quality advantage over flash anywhere in this lane; its sole edge is
latency. G2 gate data: same-family convergence is high on substance
(same core findings, identical functional behavior), low on polish
(43.8 percent score-tie rate).

Disclosures: n=4 duels, one cheap judge (ember-1); flash's longer
answers could pull judge affinity (style control: it also won the
code duel where answers were equal length and results were
byte-adjudicated). All verdicts are single-judge; LW9/AJ1 law says
router-feeding verdicts want an alternate-judge replay before they
are trusted as final. No DNFs, no retries needed.

## Artifacts

- Ledger rows (corr_id): f1ab-r1/r2/r3 198b396b, f1ab-code da7f900d
  in logs/duel/duels.jsonl rows 77-80.
- Scripts/spec/fixtures: f1_series.py, f1_code_duel.py,
  f1_code_spec.md, f1_ref_impl.py, f1_fixtures/, f1_code_out/,
  f1_contenders.jsonl. Run logs: logs/duel/f1_run_20260930.log,
  logs/duel/f1_code_run_20260930.log.
- Liveness probes: glm-5.3-flash and glm-5.3-prime both live,
  metered usage.cost honored (V9 law 1).
