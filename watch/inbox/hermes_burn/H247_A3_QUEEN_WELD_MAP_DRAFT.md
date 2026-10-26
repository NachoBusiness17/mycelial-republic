# H247_A3_QUEEN_WELD_MAP_DRAFT (anthropic/claude-haiku-4.5, turn 1, channel: content)

# DRAFT-FOR-RACTOR-FOLD

## QUEEN Component to Estate Organ Mapping Card

| QUEEN Component | Candidate Estate Organs + File Paths | Fit Sentence | Falsifier |
|---|---|---|---|
| **Silent Expert Encoder** | Workflow gate (watch/inbox/QUEEN_CHESS_LM_20261006.md:L23-24, "deterministic instruments"), dice carrier (watch/inbox/QUEEN_CHESS_LM_20261006.md:L52, "the dungeon dice carrier"), GPS ledger (watch/inbox/QUEEN_CHESS_LM_20261006.md:S1) | The silent expert chess encoder maps to deterministic instruments that compute move strength without explanation; dice carrier and GPS ledger are candidate concrete seats. | Measure whether the nominated organ's output (move ranking, position score) has zero correlation with the language model's explanation quality on a fixed 100-position test set - a silent expert divorced from language signals would fail the weld. |
| **Cross-Attention Weld** | Context pack (watch/inbox/QUEEN_CHESS_LM_20261006.md:L33, "cross-attention mount (our context-pack)") | The cross-attention mechanism that integrates silent expert representations into the language model is the context pack's direct analogue in the estate's naming. | Run the language model decoder without the context-pack bridging step and measure explanation coherence on the same 100-position set; if explanation quality does not drop by at least 15% BLEU, the mapping is false. |
| **QA Curriculum** | Lane asks (watch/inbox/QUEEN_CHESS_LM_20261006.md:L33, "QA curriculum (our lane asks)") | The question-answering curriculum that extracts chess concepts from the encoder maps directly to the lane-ask mechanism for extracting decision justifications. | SPECULATIVE. Measure whether removing the curriculum reordering (random QA order vs. concept-progression order) degrades final model Elo by less than 50 points; if degradation is negligible, the curriculum is not the active component. |
| **Natural-Language Bellman Update Distill-Back** | Fold + quantizer pack (watch/inbox/QUEEN_CHESS_LM_20261006.md:L34-36, "natural-language analogue of the Bellman update: the model analyzes the positions after its top candidate moves and consolidates them into an explanation of the current position, which is then distilled back into the model") | The fold's iterative analysis of candidate outcomes and consolidation into explanations is the estate's distill-back loop; quantizer pack carries the model weight updates across iterations. | Run the distill-back loop for 3 iterations only (vs. the paper's 7) and measure total Elo gain; if the gain is linear in iterations (under 200 Elo per iteration), the Bellman consolidation mechanism is not the bottleneck and the mapping is false. |
| **Elo Ladder** | Arena batteries (watch/inbox/QUEEN_CHESS_LM_20261006.md:L44, "Elo ladder = arena batteries") | The Elo ranking metric that measures playing strength across iterations maps to arena battery win-rate measurements, the only repeated-bout measurement in the estate. | SPECULATIVE. Measure whether Elo gains correlate more strongly with win-rate than with explanation-length or explanation-token-perplexity on a held-out 50-game set; if explanation metrics correlate equally or better, the arena battery is not the true ranking signal. |

---

## Evidence Grounding (File:Line Citations)

- Silent expert encoder split: watch/inbox/QUEEN_CHESS_LM_20261006.md:L23-24 ("deterministic instruments...do the strong play; the seat explains")
- Cross-attention mechanism: watch/inbox/QUEEN_CHESS_LM_20261006.md:L28 ("cross-attention, which we train via a question-answering curriculum")
- QA curriculum: watch/inbox/QUEEN_CHESS_LM_20261006.md:L28-29 (curriculum to extract chess concepts from encoder representations)
- Bellman update: watch/inbox/QUEEN_CHESS_LM_20261006.md:L30-32 (analyzes positions, consolidates into explanation, distills back)
- Elo measurement: watch/inbox/QUEEN_CHESS_LM_20261006.md:L39 ("Over seven iterations, our model gains over 900 Elo points")

---

## Three Priority Mappings to Test First

1. **Cross-Attention Weld (Context Pack)** - Highest confidence, falsifiable in one forward pass. Removing the context pack baseline is operationally clean; explanation quality delta is directly measurable. File:watch/inbox/QUEEN_CHESS_LM_20261006.md:L33.

2. **Silent Expert Encoder (Workflow Gate or Dice Carrier)** - Second priority because it identifies the concrete seat that supplies move rankings. If the gate or dice carrier cannot be grounded as the "silent expert," the entire weld premise fails. File:watch/inbox/QUEEN_CHESS_LM_20261006.md:L23-24, S1.

3. **Elo Ladder (Arena Batteries)** - Third priority because it is the only measurement that ties distill-back iteration count to real playing strength, validating the 7-iteration claim. If Elo does not match arena win-rate ordering, the ladder metric is decoupled from the real output. File:watch/inbox/QUEEN_CHESS_LM_20261006.md:L39, S4.

---

**Card Falsifier (Meta):** This mapping card is falsified if any of the three priority tests show zero correlation between the mapped component and its estate organ's measured output, or if the arXiv id and repo URL (watch/inbox/QUEEN_CHESS_LM_20261006.md, "OWED" section) reveal that QUEEN's encoder is not a chess engine but a learned model, breaking the silent-expert assumption entirely.
