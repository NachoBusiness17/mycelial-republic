# DELTAS.md — falsifier index row 44, linked-logs evidence (2026-10-15)

Thesis 44 under test: "verification pays +6.1 where disputed, +0.6 where agreed."
Method: tools/consensus_harness.py (5-model local council, temp 0, strict
modal-consensus over normalized answers) run twice on purpose-built 6-question
sets, one designed to agree, one designed to split. Run closes falsifier row 44
by producing the dispute-vs-consensus delta on our own fleet.

Instrument note: the harness previously built tasks only from
memory/corpus/LINKS.jsonl. It gained a backward-compatible `--questions` flag
(JSONL rows of prompt/truth/shape) on 2026-10-15 for this run; receipt: this
file + run_id consensus-20261015T223909Z / consensus-20261015T223957Z.

Council: gemma:2b, gemma2:2b-instruct-q5_K_M, deepseek-r1:1.5b,
qwen2.5:3b-instruct, qwen2.5:7b (ollama localhost:11434, 30 dispatches per set).

## Headline deltas

| Set | run_id | consensus_rate | consensus_correct_rate | dead-salmon null | verdict |
|---|---|---|---|---|---|
| CONSENSUS (6 stable facts) | consensus-20261015T223909Z | 1.0000 (6/6) | 1.0000 (6/6) | 0.0483 | STRUCTURE |
| DISPUTE (6 ambiguous) | consensus-20261015T223957Z | 0.3333 (2/6) | 0.3333 (2/6) | 0.0667 | STRUCTURE |
| DELTA (dispute minus consensus) | | -0.6667 | -0.6667 | +0.0184 | |

Mean single-model strict-correct (computed from the receipts, 5 models x 6):
CONSENSUS set 20/30 = 0.667; DISPUTE set 14/30 = 0.467.
Council lift over mean single model: CONSENSUS +0.333 (0.667 -> 1.000);
DISPUTE -0.133 (0.467 -> 0.333).

## Where the split actually happened (DISPUTE set, per-question)

- q1 tomato fruit/vegetable: 4x fruit bare + gemma:2b fruit sentence. Majority formed, matched botanical referent. (consensus, correct)
- q2 Pluto: gemma:2b yes vs 3x no + 1 empty (qwen2.5:7b ask error). 2 votes, no majority. Split reproduced.
- q3 continents: 2x "7" vs deepseek "five" + gemma:2b sentence + empty. No majority. Split reproduced.
- q4 largest desert: gemma2 "antarctica" (referent) vs 3x sahara content (2 bare + 1 sentence) + deepseek "colorado river deserts". Strict modal got 2x "sahara" bare, no majority; the SEMANTIC majority (sahara) is the wrong answer. This is the thesis in miniature: the crowd would have crowned the wrong king.
- q5 hot dog sandwich: 3x no vs 2x yes sentences. Majority formed, matched referent. (consensus, correct)
- q6 virus alive: 2x yes sentences vs no/maybe/no. No majority. Split reproduced.

## CONSENSUS set failure modes (why lift is +0.333 and not +0)

gemma:2b answered every question correctly in PROSE; strict norm matching
scores it 0/6 (e.g. "7 multiplied by 8 is 56" != "56"). deepseek-r1:1.5b
box-reasoned to a wrong 32 on q6 and "earth" on q5. The council majority
absorbed all of it: 6/6 correct despite two of five members individually
damaged. On stable ground the council is already at ceiling; verification has
almost nothing left to buy (only member-rescue, not answer-change).

## Verdict on thesis 44 (one line)

DIRECTION PARTIALLY REPRODUCED: errors concentrate exactly where models
dispute (consensus_rate -0.667, 4/6 no-majority, 1 wrong-content majority),
while the agreed set sits at ceiling, so that is where verification/escalation
budget pays; but raw modal voting itself paid NEGATIVE (-0.133) on disputed
ground, so thesis 44 holds only for real verification (escalation, referent
check, tiebreak), not for "re-ask and take the majority."

Caveats: strict norm matching undercounts verbose models (gemma:2b 0/6 both
sets on strict match); dispute-set "correct" is against a chosen referent, not
unique truth (q5, q6 have no official answer); qwen2.5:7b threw two ask errors
(empty answers, q2/q3) logged as model_error rows in the dispute receipt.

## Log paths (for the falsifier index to link)

- Runs (harness OUT_ROOT): watch/inbox/gstd_perimeter_build_20261010/runs/20261015T223909Z/ and .../20261015T223957Z/ (each: summary.json, receipt.jsonl with per-model answers, consensus_ledger.jsonl with per-model rows)
- Local evidence copies + inputs: watch/inbox/gstd_soak_20261014/dispute_evidence/ (consensus_set.jsonl, dispute_set.jsonl, consensus_summary.json, consensus_receipt.jsonl, dispute_summary.json, dispute_receipt.jsonl, consensus_run_stdout.json, dispute_run_stdout.json)
- Instrument: tools/consensus_harness.py (--questions flag added 2026-10-15, backward compatible)
