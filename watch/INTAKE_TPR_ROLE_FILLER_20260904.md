# INTAKE — TPR role-filler probes (DISCOVER) — filed 2026-09-04

NAME — "The Emergent Symbolic Structure of Artificial Neural Networks" (McCoy, Soulos,
Linzen, Smolensky — Yale/JHU/NYU/MSR; arxiv 2608.29530, 30 Aug 2026). Tweet by
@fnruji316625 (Mingyu_Jin19), 2026-09-04, 70 likes / 9 RT / 53 bookmarks.

ITEM — DISCOVER trains a linearly-transformed TPR (Tensor Product Representation:
roles x fillers) encoder to approximate a target model's hidden states; plugging E_TPR
back into the target decoder keeps behavior largely unchanged. Holds on small nets AND
LLMs, across four symbolic domains (arithmetic, logic, code, language); causal edits to
role-filler bindings change LLM outputs. Framed as a mech-interp <-> symbolic-reasoning
bridge. Media: 4 figures (title page, DISCOVER pipeline, Fig 4.1 approximation-accuracy
bars, one more) — all read.

HANDLE CLASS — numeric-suffix handle (fnruji + 9 digits) = possible bot/scraper class
per genre rules. Per-item rule applied; the account reads scholar-amplifier, not scraper:
verified individual, 955 followers, 23 media total, personal site, Mingyu Jin
(steering/mech-interp, NEC + Adobe intern). Thread/replies NOT mined (3-min box): only
1 reply, no community note — wall noted, low signal expected.

SCORE — FIT:2 PULL:1 COST:3 WINDOW:2 NOVELTY:4 = 12/25 CALIBRATE
- FIT 2 — paper, not an organ. But the DISCOVER pattern (approximate an internal state,
  substitute it, measure the behavior delta) IS the falsifier-workbench shape; role+filler
  rows echo the verkle chain's thesis (symbolic structure over vector memory). Conceptual
  compose, no file-level bolt-on.
- PULL 1 — touches nothing on the critical path this week (coverage thesis, QLoRA
  Stages 2-5, shadow fields, Desk). Mild MAX_DISTILL relevance (what internal structure
  distillation must preserve) — that arc is parked after inconclusive epoch 1.
- COST 3 — intake free. Any replication needs hidden-state access = local GPU; no API
  lane can probe internals. Executable only post-Rocinante (Oct 27); the falsifier DESIGN
  itself is $0 now.
- WINDOW 2 — feeds nothing by the Sep 20 proof wall. Lands now only as a pattern on the
  falsifier-workbench aisle.
- NOVELTY 4 — no TPR / role-filler / Smolensky surface in boot memory or watch shelf
  (quick sweep only — full corpus sweep not run inside the 3-min box). Genuinely new.

VERDICT — CALIBRATE. Tri-state: Unproven on fleet surface; Supported by the paper's own
receipts (Fig 4.1 approximation accuracy across MLP/GRU/Transformer/bottleneck on
copying/reversing/interleaving; causal-edit claims in abstract). Evidence: arxiv
2608.29530 + tweet figures.

DOGFOOD — Test 4 (Stockfish): opcode = "approximate-internal-state-and-substitute" — a
measurement opcode; slots onto the falsifier workbench lattice cleanly. Test 1
(invariant): reinforces the fold's symbolic-structure-over-vectors stance (chain rows as
role-filler bindings); contradicts nothing filed.

ROUTE — File the law; design-note a "TPR-probe swap test" (can a role+filler structural
approximation of a fleet organ's internal state be substituted with behavior held?) for
the falsifier workbench, gated on Rocinante GPU. No driver wire.

FILED — watch/INTAKE_TPR_ROLE_FILLER_20260904.md + room.jsonl thread "intake".

## EMPHASIS PASS (operator duplicate paste, 2026-09-04)
Operator re-pasted — under the duplication law, emphasis confirmed by
attention. Status unchanged: 12/25 CALIBRATE, source preserved
(corpus/training_materials/tpr_discover/). The paper's stock note: role-filler
TPR = external evidence for the accumulator's typed feature-store schema
(mag/accumulator.py); state-swap falsifier = workbench-compatible, Rocinante-
gated for hidden-state access.
