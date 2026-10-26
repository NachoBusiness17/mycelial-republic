# INTAKE CARD — TURBOINDEX_REPOSEARCH (2026-09-04, card-worker)

NAME — Applied Compute trains Qwen3.6-35B-A3B (MoE, 3B active) over a precomputed
turbopuffer vector index to answer repo-search questions across ~9,000 repos;
claims 100x lower cost than a frontier model, tops needle-in-a-haystack outright
at 2-10x lower latency. Demo video shows the real pipeline: ripgrep sweep +
index lookup + Qwen3 Reranker 4B — deterministic tools doing the sweep, small
models doing the judgment. Source: x.com/appliedcompute/status/2095932022799609928
(2026-09-04, 164 likes/122 bookmarks; author = Applied Compute, SF, "built not
bought", Agent Cloud private beta — this post is also marketing for it).

SCORE — F:4 P:4 C:4 W:4 N:3 = 19/25 (BUILD, WINDOWED)
- FIT 4: pure composition of parts we already run — lumen/Ollama local embedding,
  ripgrep, free-lane small models, the accumulator primitive. No new vendor needed
  (turbopuffer is THEIR infra; ours is pgstore/lumen).
- PULL 4: hits the inference-optimization arc dead center (small trained model
  beats frontier on a narrow task = the thesis), feeds QLoRA campaign Stages 2-5
  with a worked example, and hands the 20-lab sweep a ready-made needle-eval shape.
- COST 4: stealing the pattern is pennies; the needle-eval falsifier is $0
  (our own corpus, our own index). The full train would ride existing QLoRA lanes.
- WINDOW 4: falsifier workbench + 20-lab sweep are live NOW; this is a same-week
  calibrator. roc-infra (Rocinante) makes local rerank-serving trivial later.
- NOVELTY 3: small-model-beats-frontier is a known shape in the shelf, but this
  instance is new concrete surface: hybrid ripgrep+index+4B-reranker with public
  cost/latency numbers at 9k-repo scale.

VERDICT — BUILD (windowed, lane named: falsifier workbench). TRI-STATE: **Unproven**
— vendor's own eval, no independent receipt, no paper/methodology linked in the
root; the demo video is self-reported. Falsifier: rebuild the needle-in-a-haystack
eval on OUR corpus (repo + memory index), ripgrep+index+small-reranker vs current
semantic_search — if a 3B-active model doesn't clear our baseline, the 100x claim
dies on our surface. Per Amendment 2: thread/replies not mined this pass
(time-box) — mine before any build spawn.

DOGFOOD — Test 1 (invariants): reinforces free-lane doctrine + "tools for sweep,
model for judgment" lattice; no contradictions found. Test 4 (Stockfish): sits on
the tool lattice as a SEARCH opcode — candidate replacement for the code-discovery
slot the driver burns premium tokens on.

NEXT WIRE (for the window's judgment, not mine to launch): $0 needle-eval
falsifier on our corpus first; QLoRA campaign borrows the "train the searcher,
not the answerer" framing.

FILED — watch/INTAKE_TURBOINDEX_REPOSEARCH_20260904.md + room.jsonl thread "intake"
