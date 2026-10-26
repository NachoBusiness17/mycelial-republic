# INTAKE — HarnessDev: LLMs building their own agent harness (2026-09-04)

SOURCE — @askalphaxiv tweet 2095708436977824220 (2026-09-04) → alphaxiv.org/abs/2609.01437.
Abstract receipted from arxiv.org/abs/2609.01437: benchmark shifts the unit of evaluation
from task outputs to runnable infrastructure; two stages (harness creation from scratch,
then self-evolution), model weights held fixed.

NAME — HarnessDev: can an LLM write and evolve its own execution harness?

## 5 axes
- FIT 5 — pure composition: eval loop, tools, context, recovery, verification are exactly
  the mag organs (queue, chain, seat_dispatch, watchdog). No new vendor.
- PULL 4 — directly feeds falsifier workbench (gives a falsifiable metric: harness delta
  at fixed weights) and agent-organs arc; validates the files-not-processes doctrine with
  external numbers. Not on tonight's critical path (Sep 20 proof deadline).
- COST 5 — read/steal is free; any bench port runs on free lanes + one premium judgment pass.
- WINDOW 3 — usable methodology, but the window is the promo wall; steal the eval frame,
  don't build the benchmark now.
- NOVELTY 4 — new paper, new surface; not a learned-and-lost re-find (echoes
  self-improving-scaffold ideas but with receipts).

SCORE — F:5 P:4 C:5 W:3 N:4 = **21/25 BUILD NOW**

VERDICT — BUILD (the steal, not the benchmark): port the two-stage eval
(create-from-scratch / self-improve at fixed weights) as a falsifier harness for our own
organs — measure OUR queue/watchdog/salon stack the same way. Builder spawns same turn
per LAUNCH LAW.

## Tri-state
- SUPPORTED: "harness changes substantially alter performance at fixed weights" — arXiv
  abstract directly states it (receipted).
- SUPPORTED: "competitive harnesses from scratch; self-improvement brittle, gains fail to
  generalize across unseen tasks/executor models" — abstract + tweet agree (double-attested).
- UNPROVEN (for us): that our own fleet harness would score well / where it'd fail —
  no measurement exists yet; that IS the falsifier to run.

DOGFOOD — Test 1 (invariants): reinforces files-over-processes and one-builds-one-verifies;
the "brittle generalization" claim matches our MAX_DISTILL epoch-1 floor-effect finding
(gains not transferring = same shape). Test 4 (Stockfish): sits on the tool lattice as a
measurement opcode, not a generation opcode — placement clean.

FILED — watch/INTAKE_HARNESSDEV_SELF_HARNESS_20260904.md + room.jsonl thread "intake".
