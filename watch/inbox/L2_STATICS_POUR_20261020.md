# L2 STATICS POUR RECEIPT - 2026-10-20

- date stamp: 2026-10-20
- observed_at: 2026-10-20
- receipt: watch/inbox/L2_STATICS_POUR_20261020.md

## Operator order this pour answers

"any big projects, make a big workflow mickey17 style, go full width on deepseek" - the pour ran the four
L2 game statics as one deepseek batch, mickey17 per-item shape, full width on the deepseek carrier.

## Pour products (the four statics)

1. watch/corpus/L2_games/chess.DRAFT.md
2. watch/corpus/L2_games/go.DRAFT.md
3. watch/corpus/L2_games/tafl.DRAFT.md
4. watch/corpus/L2_games/hanafuda.DRAFT.md

Synthesis over the four: watch/corpus/L2_games/_FOUR_STATICS_SYNTHESIS.md (crossmap over the L0 contract,
section 3 carries the falsifier rows copied below).

## Deepseek carrier outcome

Exit 0. Carrier tail, verbatim:

```text
chess ok_api=True ok_material=True $0.0019 cum
go ok_api=True ok_material=True $0.0030 cum
tafl ok_api=True ok_material=True $0.0042 cum
hanafuda ok_api=True ok_material=True $0.0058 cum
BATCH DONE 4 items $0.0058 -> memory\runs\l2_statics_pour_20261020\results.jsonl
```

Results at memory/runs/l2_statics_pour_20261020/results.jsonl. Byte-back check run this session: `wc -l` on
that file reads 4 rows, and a `.venv/Scripts/python.exe` read of the same file returns per row
id/model/ok_api/ok_material/cost_usd: chess deepseek-chat True True 0.001903, go deepseek-chat True True
0.001049, tafl deepseek-chat True True 0.001236, hanafuda deepseek-chat True True 0.001652. The cumulative
costs in the carrier tail match the row deltas, and every row clears the ok_api + ok_material bar (material
rendered, no hollow batch).

## Falsifier per game (taken from watch/corpus/L2_games/_FOUR_STATICS_SYNTHESIS.md, section 3)

- chess: learning/capture dissociation. Killing observation: a war/capture-organ run where learning events
  and capture events split apart - a full-value game decided with zero captures while the learning ledger
  still moves, or heavy capture exchange banking zero assumption-falsifications. Alternate kill: evidence the
  socratic gate needs the forced-capture form and a passive global filter does not instantiate it.
- go: liberty-to-dirty-radius identity break. Killing observation: one documented re-probe whose dirty set
  spans the whole board rather than a radius, or a cached read dying while its dirty radius is provably clean.
- tafl: numbers beat routing. Killing observation: outcome data in which swarm material ratio predicts
  solo-agent survival better than route or streak metrics do.
- hanafuda: tri-state collapse to binary. Killing observation: an estate surface where a claim's evidence
  state is fully decidable from one lane's visible record, hidden evidence recoverable, and no sibling
  contradiction possible - the tri-state ledger collapses and the information-set organ has nothing left to
  instantiate.

## Laws check

No em-dash and zero CJK in this file: scanned at write time with a `.venv/Scripts/python.exe` byte scan for
U+2014/U+2013 and the CJK unicode ranges, zero hits (run this session, the same verifier shape the synthesis
names).
