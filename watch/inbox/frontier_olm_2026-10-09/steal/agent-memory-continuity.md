# STEAL CARD: agent-memory-continuity (frontier_olm 2026-10-09, round 1, first draft)

Ten confirmed finds, one mechanism behind most of them. Quotes below are taken from the ask's
finds material (miner source-fetched 2026-10-09 per each find's own record); this seat did not
re-fetch the sources this session and marks every quote as ask-carried, not re-verified. Estate
bytes cited were read and counted in this session.

## Headline steal (mechanism, not a link dump)

Supersession is a read-path contract, not a write-path edit. Keep the old memory as an inactive
node that carries its replacement's id plus why-evidence; only let the replacement drive actions
after it can explain the change; and the read side (pack builders, recall, node lookup) must
select active over superseded by default, because unresolved supersession is the expensive
failure (frontier datum: 70.3% of prompts expose a superseded value without update resolution,
https://arxiv.org/abs/2610.10265). The estate already owns the write half: the m6 lane wired six
superseded_by edges into the live graph with a rebuild-surviving collector
(memory/runs/mickey17_v2/runs/morning-block-20261007/lanes/m6-graph-supersession.json rows 1-4,
quote: "RESULT: PASS wired_edges=6 add_nodes=12 graph_nodes=2938 graph_edges=1256"). The port
move is the read half plus the activation gate, not more edges.

## Estate bytes verified this session (my own reads and counts)

- memory/knowledge_graph.json: exactly 6 edges with rel "superseded_by" out of 1,256 edges
  (counted by json load this session), and 12 endpoint nodes kinded superseded (6) / superseder
  (6) out of 2,938 nodes. Node kinds ready as a conditioning axis: knot 400, case_law 300,
  doctrine 217, steal 140.
- The collector is collector-kind, rebuild-safe: mag/knowledge_graph.py SUPERSEDED_REL +
  superseded_rows/_superseded_wire/_nodes_superseded/_edges branch (m6 lane row 1 names lines
  237-309, _COLLECTOR_KINDS at 55-61, build() at 609).
- Residual gap, already registered: graph_heal's why_context edges are still wipe-on-rebuild
  (m6 lane row 5, estate_status "blocked", quote: "AFTER BUILD: nodes 2928 edges 1134
  why_context edges surviving: 0", source mag/knowledge_graph.py build() regenerates
  _edges(nodes) only, tools/graph_heal.py:232-238 appends manually).
- The percolator has ONE global gate: _compile_invariant (mag/percolator.py:385) runs the same
  decay-then-increment count path for every invariant regardless of kind; memory/percolator/
  invariants.json rows carry count/decay_as_of with no per-kind threshold anywhere in the file.
- The context pack already is the bounded-view-plus-zoom pattern: MAG_FULL_CONTEXT_MAX_CHARS
  default 48000 (mag/context_pack.py:666), shed sections render as stubs with a fold marker
  (mag/context_pack.py:69,108) and restore_shed_section re-renders from SHED_SOURCES with a
  sha check that "turns drift into a refused restore instead of silent corruption"
  (mag/context_pack.py:225-240); list_shed_stubs at :326.
- The log-everything half exists flat: memory/trajectory/steps.jsonl measured this session at
  68.7 MiB / 73,768 lines (the find's 71.7MB figure differs from my measurement; OWED which
  unit or tree moment explains the delta).
- Read-side joins exist: corr_id appears in tools/estate_query.py, mag/effect_broker.py,
  mag/state_snapshot.py, mag/trajectory_step.py (grep -rln corr_id, this session).

## Find-by-find estate map

1. pi-optchat "never compact" memory tree
   (https://www.reddit.com/r/LocalLLaMA/comments/1wzh1i7/) -> organ: context pack +
   trajectory + zknot. Quote (ask-carried): "instead of compacting, every message is logged
   and summarized into a binary tree. Each turn starts from a fresh context with a bounded
   memory view (128 KB)". Port move: the estate needs the TREE, not the slogan: a parent-child
   summary hierarchy over memory/trajectory/steps.jsonl where each summary node cites its
   children's byte ranges (a citation is the re-read trigger), joining restore_shed_section's
   sha-verified zoom as the leaf. The thread's own failure mode (small-model summarizers
   invent details that merge upward) is exactly what tools/citation_lint.py PHANTOM-NUMBER
   already hunts: run the summarizer under citation lint.
2. Superseded-not-overwritten + explain-why activation gate
   (https://www.reddit.com/r/AI_Agents/comments/1wx6lib/) -> organ: knowledge graph +
   SUPERSEDED register (memory/fold_history/SUPERSEDED.md). Quote (ask-carried): "I would
   keep the old memory as inactive or superseded, store the new one with source/date/
   confidence, and only let it drive actions after the agent can explain why it changed".
   Port move: activation flag on the superseded/superseder kind pair so plain recall skips
   superseded nodes unless the superseder rides along; the write half is done, the read half
   is the gap.
3. MINDSET energy-based schema evolution (https://arxiv.org/abs/2610.08586) -> organ: the
   superseded_by collector. Quote (ask-carried): "Each incoming episode may reinforce,
   supersede, split or create a schema... while hysteresis prevents isolated contradictions
   from prematurely rewriting stable memory". Port move: turn the collector from
   register-row-passive into a gated transition (reinforce/supersede/split/create with a
   hysteresis counter), so the graph-maintenance lane wires edges by decision instead of hand
   registration.
4. 70.3% stale exposure + missed-merge vs false-merge asymmetry
   (https://arxiv.org/abs/2610.10265) -> organ: context pack read side. Port move: pack
   builders filter or demote superseded nodes; the asymmetry says prefer missed merges over
   false merges when bulk-wiring, i.e. only auto-wire when both endpoints and the why-evidence
   are byte-resolvable.
5. When Evidence Changes: repair vs re-read (https://arxiv.org/abs/2610.03902) -> organ: ribs
   + git as source of truth ("trust bytes, not reports" law). Quote (ask-carried): "local
   repair uses 5-10x fewer revision tokens than rebuilding, yet every memory pipeline costs at
   least twice full re-reading in held-out conditions". Port move: when the source is still
   readable, re-read beats wiring more derived edges; edges must earn their keep. This bounds
   finds 3-4: bulk superseded_by wiring is NOT the first move.
6. Retrieval admissibility (https://arxiv.org/abs/2610.07309) -> organ: context pack
   namespace scoping. Quote (ask-carried): "Top-20 anchor recall increases from 0.432 to
   0.533" from filtering off-namespace memories at frozen scores. Port move: seat/lane scope
   tags on pack sections so cross-lane organs (mirror voice, clue chain, zeitgeist excerpts,
   mag/context_pack.py:568-651) are admissible by scope, not by score.
7. Category-conditioned retention (https://arxiv.org/abs/2610.07100) -> organ: percolator.
   Quote (ask-carried): "only 77.9% of value and belief assertions are supported by their
   source, versus 96.2% for all other categories". Port move: per-kind confidence bars on the
   kind axis the graph already carries (knot/case_law/doctrine/steal, counted above) instead
   of the one global count gate at mag/percolator.py:385.
8. Persistent-memory cost null (https://arxiv.org/abs/2610.07782) -> organ: mesh/sovereign
   mirror verdict evidence. Quote (ask-carried): "+0.368 MiB ... and produces no detectable
   accuracy change". Port move: banked as Q2 evidence that the shared persistent tier bought
   nothing while per-call decomposition did; the single-controller law blocks no measured
   benefit, knot-as-CRD stays live only for multi-host mesh. No port action.
9. Execution consistency beats record truth (https://arxiv.org/abs/2610.08101) -> organ:
   corr_id/receipt layer. Quote (ask-carried): "identical retained records can correspond to
   compliant and violating executions under the same task rule" (82.4% indistinguishable
   without receipt evidence, 97.9% separable with restoration). Port move: correction
   downstream of memory must join receipts (corr_id already in tools/estate_query.py), not
   rewrite records.

## Probes (one per find-group, all cheap)

- Headline probe (finds 2+3+4, read-side demotion): build a pack the normal way
  (mag.cmd context-pack), then check whether any superseded:row-N node id or SUPERSEDED.md
  register content renders into the pack or its shed stubs without the superseder named
  alongside. Prediction if the steal is true and unported: at least one section surfaces
  superseded material undemoted. Falsifies the "read side is fine" null.
- Activation-gate probe (find 2): plain node lookup on a superseded:row-N id still returns
  the node with full weight and no pointer to its replacement (graph JSON has no activation
  field at all; the 6 superseded nodes are ordinary nodes today).
- Hysteresis probe (find 3): from memory/percolator/invariants.json, count invariants whose
  text contains a contradicted erratum but whose count kept climbing; zero such rows would
  falsify the need for a hysteresis gate.
- Re-read-first probe (find 5): re-read the source receipt for each of the 6 superseded_by
  edges and verify the edge's evidence still matches bytes; any drift is a falsified edge and
  proves re-read auditing cheap (6 edges, one sitting).
- Namespace probe (find 6): render two packs for one seat, one with cross-lane excerpts
  suppressed via the pack's own env flags, and measure the byte fraction that is off-seat;
  no measurable fraction falsifies the admissibility port.
- Per-kind support probe (find 7): sample one day of invariant firings and compute support
  rate per kind against the named source; if knot/doctrine rows support at the same rate as
  behavioral rows, the per-kind gate buys nothing.
- Summarizer-invention probe (find 1): run a local janitor summarizer over 100 trajectory
  steps, then run tools/citation_lint.py checks over the summary; invented quantities are the
  merge-upward failure the reddit thread warns about.

## OWED / not verified this session

- Source quotes: carried from the ask's finds (miner fetched 2026-10-09 per find records);
  not re-fetched by this seat.
- 71.7MB vs 68.7 MiB on memory/trajectory/steps.jsonl: unexplained; my measurement is the
  one cited above.
- The reddit find 2's post body contains an off-topic residential-proxy paragraph, likely
  stealth promotion, per the find's own note; evidence was taken from its comments.
