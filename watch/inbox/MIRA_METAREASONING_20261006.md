# LINK-DROP receipt: MIRA, meta-reasoning for long-horizon research agents

- Dropped: 2026-10-06, arXiv https://arxiv.org/abs/2610.02525
- Fetched: arXiv abs page first-hand (43,673 bytes HTML), same sitting
- LINKS row: seq 1791314529958091, canonical sha256 0CF18F180D63C3E4...
- Authors: Ankur Samanta, Yonathan Efroni, Paul Sajda, Kaveh Hassani, Anirudh Goyal. cs.AI, submitted 1 Oct 2026.
- Verdict: STEAL, high leverage. Independent authorship, real convergence data point.

## What it IS (from its own bytes)

Verbatim, the architecture: "We introduce Meta-reasoning for Iterative Research Agents (MIRA), a hierarchical architecture separating research allocation from execution. An outer-loop meta-reasoner curates context from a persistent research record, then writes a work order for the next investigation or ends the episode. A fresh inner-loop executor carries out each work order, making execution part of the transition between meta-reasoning actions."

Verbatim, the wire: "At each boundary, we train a generative critic to forecast expected remaining return from partial states, outperforming token-level alternatives." And: "meta-reasoning can be learned as an explicit policy for directing long-horizon autonomous research."

## Estate mapping (why the operator said oh you)

1. The outer loop is the OUROBOROS loop and the driver-file pattern: read the persistent record, write the work order (lane table), fire a fresh executor per order, fold, repeat. MIRA is that loop with the two halves named research allocation vs execution, exactly the estate's driver vs lane-runner split.
2. The persistent research record curated for context is the estate's chain + context-pack + rib vault; "or ends the episode" is a stop-cert for research episodes, which the estate has for workflows and lacks for research windows.
3. THE MISSING WIRE, named 10-04 (Schmidhuber compression-progress mirror memory): the estate already IS the two-module agent, A = receipt/compression, B = lane selection, and the missing wire was intrinsic reward. MIRA's generative critic forecasting expected remaining return from partial states IS that wire, derived independently and measured: it beats token-level alternatives, and cross-environment pretraining yields "a transferable prior for valuing partial progress."
4. Credit assignment at decision boundaries answers the R5 finding that attribution is null for the memory organs: MIRA's boundaries are natural attribution units; the estate's fold amendment tables are the same boundaries without the value function.
5. The estate already holds MIRA's training corpus: steps.jsonl (~37k execution trace rows, never joined per the r01 read-the-estate lane) plus every lane archive under memory/runs/ with outcomes. The critic trains on partial states -> outcomes; the estate has partial states and outcomes unjoined.

## Steal rows (one seat one sitting each)

- S1, high: Lane-value forecaster v0 - train (or few-shot) a generative critic on the estate's own traces: partial lane state (lane id, what, rows so far) -> forecast remaining return (rows landed, defects found), validated on steps.jsonl slices where outcomes exist. The percolator's curiosity-scored lane selection candidate then consumes the forecast instead of a hand-tuned score. Corpus: steps.jsonl + memory/runs/*/lanes/.
- S2, high: Episode stop-cert for research windows - MIRA ends the episode from the record; port the workflow stop-cert clause shape to the research loop (a research episode ends when the record's own forecast says remaining return is below the seat's burn floor), wired next to the fold gate.
- S3, medium: Work-order contract tightening - MIRA's work order carries the curated context explicitly. The estate's lane asks embed `what` + `start`; add the curated-record pointer (chain tip, fold section) as a first-class work-order field so fresh executors stop re-bootstrapping.
- S4, medium: imp002 bridge - the actor-reward self-play orchestrator (landed yesterday, llama.cpp bridge + bottleneck hooks) is this paper's actor-reward shape at self-play scale; MIRA-AC is it at research-allocation scale. One sitting: write the two-page mapping and name the shared reward schema so the two doors inherit one instrument.
- S5, watch: "Training on the model's own proxy hill-climbing signals" is self-steal formalized; WATCH for the follow-up work on reward contamination (the estate's fabrication-frontier doctrine says a closed corpus turns consumers into fabulators - a critic trained on its own hill-climbing is the same disease class; the falsifier writes itself).

## Watch / owed

- OWED: none for fetch; the PDF full text was not read this sitting (abs page only) - the five steal rows are built from the abstract's own sentences, which the page carries verbatim.
- The dogfood burn (dwfrun-5de02c51) lane d13-selfplay-run and d04-graph-orphan run adjacent to S1/S4; no file collision (this receipt banked standalone).
