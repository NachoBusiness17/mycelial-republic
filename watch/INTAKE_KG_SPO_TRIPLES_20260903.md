# INTAKE — KG SPO Triple Extractor (ai-knowledge-graph)

Date: 2026-09-03. Intake lane, card 22-ish (post-rubric window).

## ITEM
https://x.com/tom_doerr/status/2095482993779363951 — @tom_doerr, Sep 3 2026 12:04 PM:
"Extracts Subject-Predicate-Object triplets from unstructured text to generate interactive knowledge graphs."
Points at github.com/robert-mcdermott/ai-knowledge-graph. Single-tool showcase, NOT a directory
listicle (the REMEMBER-by-default rule for this account does not trigger; the tool is corpus-unknown).

## RECEIPTS
- mcp web_reader on x.com: MCP 500 error (transport dead). WebFetch on x.com: SUCCESS for root post —
  text, link, engagement (9.1K views; 18/162/196 unlabeled ≈ replies/reposts/likes). Replies: login-walled.
- WebSearch for replies/community notes: X reply threads are not indexed; nothing retrievable. No
  community note found. Reply sentiment = Unproven.
- Search WRINKLE: tom_doerr has posted this SAME repo before — Apr 23 2026
  (status/2047485918966059451, 33.2K views), plus likely 2 more re-posts (statuses 2082808…,
  2086176…; one of those may be a different Gemini-based KG tool — Unproven which). This Sep 3 post
  is a re-surface of a months-old, world-visible tool (2.9k stars).
- Repo verified via GitHub fetch: Apache-2.0, Python 3.11+, NetworkX + PyVis, three passes
  (triple extraction → entity standardization → relationship inference), "Works with Any OpenAI
  Compatible API Endpoint: Ollama, LM Studio, OpenAI, vLLM, LiteLLM"; default config = LOCAL Ollama
  + gemma3 at localhost. 64 commits, 11 open issues, no tagged releases. Demo numbers (216 triples →
  564 after inference, 9 communities / 161 nodes) = vendor demo, Unproven on our corpus.
- Corpus sweep: MEMORY.md index + watch/ file names + full-repo grep ("knowledge graph", SPO,
  triplet, ontology, mcdermott, ai-knowledge-graph). ZERO prior mention of this tool.

## CORPUS INTERSECTION (the load-bearing find)
- mag/knowledge_graph.py EXISTS (560 lines, schema v2 "GraphRAG communities + Mem0 multi-signal +
  Letta dream") — born from the operator's 2026-08-10 ask ("accurate knowledge graph so things are
  just known spookily"). But its law is explicit: "Deterministic, $0, no LLM. Every node carries a
  SOURCE" — it builds from STRUCTURED substrates (verkle chain, code_map, skill_ledger, steals).
  The fleet has a KG organ; it has NO unstructured-prose→triples ingest arm.
- watch/GRAPH/graph_20260901.jsonl = live seed graph (node/kind/label/source rows; includes
  "the private knowledge graph is the product" as an insight node).
- watch/TITOR_STACK_20260903.md explicitly queues KG-mining builds ("Shadertoy library mining: the
  52k-shader rule lattice into the KG — wings format, free gophers, memlance-grounded").
- Coverage thesis ("action without record never happened"): 48 unmined sessions, 66 VS Code
  transcripts (~700MB), hermes backlog (v1 target 80%), 15.8% evidence_lost — the dark matter this
  tool's method turns into graph rows.

## SCORE
F:4  P:4  C:4  W:4  N:3  = 19/25 → BUILD WINDOWED (one under BUILD NOW)

## READ
The honest why: this is not a new idea to the world (tom_doerr's own April post out-performed this
one 3:1; the tool has 2.9k stars and no releases), and it is not a new organ to the fleet — the KG
organ already exists. What it IS: the missing INGEST ARM for that organ. knowledge_graph.py builds
from structured sources by law; the fleet's richest knowledge (unmined sessions, wings, backlog) is
unstructured prose it cannot touch. This tool's three-pass method (extract → standardize → infer)
runs on exactly our free lanes (any OpenAI-compatible endpoint; local Ollama default = the $0 path)
under Apache-2.0. The steal is the passes, not the product: bind them as a new collector kind in
knowledge_graph.py, keep PyVis out (our room renderer already serves static surfaces). It misses
BUILD NOW by one point for one reason: the grounding amendment (below) is a real design decision,
not plumbing — an LLM triple with no source anchor violates the organ's founding law, so v0 must
prove precision on a known row before any scale-up. Driver queue position decides build order.

## TRI-STATE
- Supported: repo exists, Apache-2.0, local-model-first, OpenAI-compatible interface. (GitHub fetch.)
- Supported: fleet lacks unstructured-prose→triples ingest; corpus has zero prior mention of this
  tool; Titor stack already queues KG-mining builds. (grep + doc reads.)
- Unproven: extraction precision on fleet-corpus text (vendor demo numbers only).
- Unproven: reply sentiment / community note on the post (login-walled, unindexed).
- Unproven: whether 2 of tom_doerr's other KG posts are this same repo vs a Gemini-based rival.
- Disputed: nothing located — no pushback found anywhere (absence of evidence, noted as such).

## VERDICT
BUILD (windowed) — 19/25.

## ROUTE
WIRE. Concretely:
- Opcode: kg_extract_arm_v0.
- Steal the passes, bind into mag/knowledge_graph.py as a new collector kind ("prose"), source-
  anchored triples only (span + row hash per triple) — that anchor is what keeps the organ's
  "grounded, not hallucinated" law intact under LLM extraction.
- Lane: free flash gophers via their OpenAI-compatible endpoint (the tool's exact interface);
  hands-box Ollama as the fully-local $0 lane. One premium judgment pass to design the binding.
- First probe (eyes-receipt pattern): one KNOWN session row → triples → precision check against the
  actual record; only then scale to the 48 unmined sessions / hermes backlog / Titor KG queue.
- PyVis output optional/likely dropped — static-render law + existing room surfaces.
- Typed room row for the driver pull (per INTAKE_RUBRIC amendment 1: background spawn by default).
  NOT appended to room.jsonl by this sub-agent (uncoordinated write to a live shared surface that
  just survived a runaway incident); ready in-card:
  {"type":"intake_card","card":"watch/INTAKE_KG_SPO_TRIPLES_20260903.md","verdict":"BUILD_WINDOWED","score":19,"opcode":"kg_extract_arm_v0","lane":"free:glm-4.7-flash","status":"PROPOSED"}

## DOGFOOD
1. INVARIANT PASS: reinforces cheapest-lane routing (local/free-lane-first is the tool's own
   default), files-are-data (JSON graph out), loopback/static render; EXTENDS the coverage thesis
   with a concrete record-recovery arm. ONE TENSION, named: the KG organ's founding law is
   "Deterministic, no LLM, source-backed" — LLM triples breach it unless every triple carries a
   verifiable source anchor. That amendment IS the build.
2. STOCKFISH PASS: placed without strain — lane = free flash/OpenAI-compatible gophers; opcode =
   kg_extract_arm_v0; consumers = knowledge_graph.py build(), Titor KG-mining queue, hermes v1
   80% target, dungeon wings (unmined sessions → NPC minds). Placement succeeded; the finding is
   the fit, not the failure.
