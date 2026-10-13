# R3-training — corpus/training_materials triangulation (SHADOW WORK vol-2, night shift)

Seat R3 · 2026-09-06 · $0 · no network · read-only on corpus. Method: Astra abridged.
Cells: watch/TESUJI_MAP.jsonl axis R (first R rows) — R3 slice verified: all 4 rows
chain-link to live tips, hashes intact. Ledger-wide `mag.tesuji_map.py verify` is
currently blocked by ONE foreign row: 175 (seat R2, R/library/human_atlas) whose note
carries path-like tokens ("room/live/tesuji_map.html", "154MB/4.5GB") that don't exist
on disk. Append-only remedy filed to the blackboard (finding seq 183): R2 appends a
corrected row. No other row fails.

## 1. Inventory (16 entries, 110M)

MANIFEST.md (289 lines of table, rows 1-28) is complete and honest — sha256 provenance
per row, one FAIL row kept visible (mir COURSE book, Google-Drive-walled, later closed
by the PROBLEMS book). Subfolders have NO READMEs — MANIFEST is the single index.

| Material | What it is | Depth | Format | Intake |
|---|---|---|---|---|
| sparse_reward/2602.00986.pdf | sparse value + dopamine/RPE neurons as process-reward model (PRM) | research paper | PDF 1.9M | 09-04 |
| ppa_moroney/patterns_predictions_actions.pdf | "Patterns, Predictions, and Actions" foundations survey | 309pp book | PDF 2.6M | 09-04 |
| alphaevolve_omega/alphaevolve_omega.pdf | AlphaEvolve omega record — evolutionary program search | research paper | PDF 409K | 09-04 |
| slp3_hmm/slp3_hmm_appendix_A.pdf | Jurafsky/Martin SLP3 Appendix A — HMMs, forward/Viterbi | undergrad text | PDF 574K | 09-04 |
| sml_book/understanding_machine_learning_2ed_draft.pdf | Shalev-Shwartz/Ben-David, Understanding ML | grad theory, ~11M draft | PDF | 09-04 |
| lbdl_fleuret/lbdl.pdf | Fleuret, Little Book of Deep Learning | compact reference | PDF 4.7M | 09-05 |
| oxford_complex_numbers.pdf | Oxford Math Institute complex-numbers notes (polar, Argand, roots of unity) | undergrad exercises | PDF 279K | 09-05 |
| frontier_math_lean/ (2 html) | site-percolation + KN1 Lean formalization expositions | research-formal | HTML 59K | 09-05 |
| mir_mishchenko/fomenko_problems_...mir1985.pdf | Problems in Differential Geometry and Topology (Mir 1985) | hard problem book | PDF 6.2M | 09-05 |
| drawing_right_brain/ | Betty Edwards, Drawing on the Right Side of the Brain | perception training | PDF 22M | 09-05 (operator hand-carry) |
| zai_trajectory_window_sample_20260905.txt | this fleet's own z.ai trajectory export (step hashes, envelope) | primary artifact | TXT 75K | 09-05 |
| strace_edg · terminal_universe · tpr_discover · uno_diffusion · tesla (9 files) | tracing / terminal-envs / role-filler / diffusion-LLM / Tesla corpus | mixed | — | 09-04/05 (one-line coverage here; out of the named-10 core) |

Note: brief named 10 materials; folder holds 16 entries — extras listed above are
inventoried but get one-line treatment, not full mapping.

## 2. T5 capability-ladder map (docs/DASHBOARD_REORIENTATION_V2.md §"Progressive local coding curriculum")

The ladder mechanism is REAL and already live: configs/training_patterns.yaml carries
19 eval cases (eval-001..010, economics-003, ilap-001..003, steward-001,
desk-teaching-001) with fixtures. The missing half: **zero corpus-sourced eval cases**.
Every existing case is a fleet-discipline fixture. The 110M corpus has fed the ladder
nothing. That is the single sharpest finding of this pass.

| Material | Task class it can graduate | First eval case to write |
|---|---|---|
| sparse_reward | reward-shaping / process-reward scoring | eval-rl-001: score the eval-004 fixture trace (hundred_rounds_no_leaf) with an RPE-style per-step prediction-error proxy; PASS = proxy rank-correlates with the human theater verdict |
| oxford_complex_numbers | math-prose (bounded, machine-checkable) | eval-math-001: 3 exercises (Cartesian→polar, roots of unity, geometric locus) answered by model, answers verified deterministically in python |
| frontier_math_lean | formalization prose (Lean↔English round-trip) | eval-form-001: restate the percolation Lean statement in plain prose, back-translate, diff against source |
| alphaevolve_omega | evolutionary search | eval-search-001: evolve a tesuji probe schedule, fitness = $0 cache-read yield from TESUJI_MAP.jsonl |
| drawing_right_brain | vision-interpretation (the seat's EYES — eyes_receipt arc) | eval-vision-001: orientation-invariance pair — describe inverted vs upright image, score against upright ground truth |
| lbdl_fleuret | ML-explanation/teaching (Library destination) | eval-teach-001: 5 bounded explain-with-example prompts, rubric-scored |
| sml_book | ML theory QA | eval-theory-001: end-of-chapter problems with known answers |
| slp3_hmm | sequence-model implementation | eval-seq-001: implement forward algorithm, check against book's worked numbers |
| ppa_moroney | overlaps sml+lbdl — lowest marginal value; survey only | defer |
| mir_mishchenko | geometry/topology problem-solving — no task class exists yet; frontier, not graduateable now | shelve (d=16 leading-zero discipline: don't fake a class) |

## 3. Usage check — SUPPORTED near-zero

Grep watch/ notebooks/ mag/ dashboard/ docs/ configs/, INTAKE cards excluded:
- oxford_complex_numbers: **0** files. frontier percolation/kn1: **0**.
- lbdl: 1 · ppa: 1 · sml: 1 · slp3: 2 · mir/fomenko: 3 · drawing_right_brain: 1.
- alphaevolve: 13 — but spot-check shows all are topic_index/digest/room mentions
  (indexed as a TOPIC, never used as a SOURCE).
- sparse/RPE: 20 — false positive; "RPE" collides with game/arena contexts, zero real
  uses of the paper.
- Acquisition is rich (202 INTAKE cards in watch/); conversion is ~zero. The corpus is
  a banked shelf, not yet a training surface.

## 4. Promotions (top-3, exact next use)

1. **sparse_reward → eval-rl-001** — highest leverage: it aims the reward model at the
   fleet's OWN sparse-leaf problem (knots as dopamine hits), tying the paper to
   training_patterns.yaml fixtures that already exist. Trajectory-lens compatible.
2. **oxford_complex_numbers → eval-math-001** — cheapest first win: small PDF,
   deterministic answer-checking, graduates the math-prose class at T1 before Sep 20.
3. **drawing_right_brain → eval-vision-001** — extends the VERIFIED eyes_receipt into a
   standing task class; the seat's eyes are a task class too.
   (Honorable mention: alphaevolve → eval-search-001, fitness from free cache reads.)

Falsifier for this card: if eval-rl-001/eval-math-001/eval-vision-001 are not filed
(Training-EVAL section appended to training_patterns.yaml or a successor) by Sep 20,
this mapping is DISPUTED as shelf-decoration.

## 5. Active-arc connections

- TESUJI: corpus = free field-samples; alphaevolve cell feeds the probe-scheduler idea.
- Trajectory lens: sparse_reward's RPE frame IS a scoring envelope for steps —
  {input, tool_result, output, reasoning} per step with a per-step prediction error.
- Rocinante (Oct 27): this corpus is the graduation quarry — T5 ladder is the road;
  local models attempt corpus-derived eval cases in sandbox before owning a class.
- The room that remembers: MANIFEST rows are already chain-adjacent (sha256 per row);
  promotion should cite the row, not re-derive it.

## 6. Cells posted

- R/training/inventory — SUPPORTED
- R/training/utilization — SUPPORTED
- R/training/eval-map — SUPPORTED
- R/training/promotions — UNPROVEN (until first eval case lands)
