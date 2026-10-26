# REPO-MAP STEAL: the landscape + what we build that they do not have (2026-10-12)

Operator: "Look up mapify your repository from hacker news and steal."
Context: the truth-hunt architecture (rooms/belts/machines as walkable
exploration for humans AND agents). The repo-mapping field is the closest
existing industry to that - this card maps it, then names the gap.

## The landscape (all first-hand fetched, scores live from HN API)

- Repomap ("Google Maps but for your repo", HN 46933360, Feb 2026, 7 pts):
  Rust engine (tree-sitter + petgraph + rayon), Hono/Bun API, React+D3 map,
  module clusters, snapshots. One comment asked the load-bearing question
  (call-pattern clustering? star-import/dynamic-require resolution?) - NEVER
  ANSWERED. Dead thread.
- GitDiagram (222 pts, Dec 2024 - the field's giant): public GitHub repos,
  file tree + README through Claude, interactive Mermaid, click-through to
  files. The swap-a-letter trick (hub -> diagram in any GitHub URL) is the
  distribution genius.
- Graphify: the one that actually spread - but the HN record is a graveyard
  of resubmits (8 submissions Apr-Aug 2026, 1-4 points each, two different
  repos as ownership moved safishamsi -> Graphify-Labs). What moved it was
  NOT HN: Karpathy's "LLM Knowledge Bases" post (22M views, "there is room
  for a product instead of a hacky pile of scripts") landed Apr 2; the repo
  existed 19 hours later; "someone built the thing Karpathy just described"
  traveled the sentence; the 12,000-stars-in-48h claim followed.
- Onboard-CLI (24 pts): AST + LLM, local React map. CodeBoarding: control-flow
  graph, LLM checked against static analysis, recursive zoom system ->
  component. graf: Rust+SQLite rewrite. Noodles: entry points -> execution
  flow. Mapstr/Eulix/Cartograph: the LLM-assisted class.

## What NONE of them do (the estate's gap, named per tool)

1. ARCHITECTURE AS PREMISE: every tool maps the code that EXISTS (files,
   calls, deps). None treat the architecture as the designed PREMISE - our
   truth-hunt inverts it: the room/belt/machine schema is authored first
   (factory, library, vault, chamber), and the code must justify its place
   in the building. Map-after vs map-as-blueprint.
2. WALKABLE EXPLANATION: their maps are for developers onboarding to a
   codebase. Ours are for humans AND agents exploring a SYSTEM's laws - the
   invariant hunt, the machloket displayed, the ground receipts visible at
   each machine. No tool maps DISPUTES and PROVENANCE, only structure.
3. AGENT-NATIVE OUTPUT: their output is visual/D3/Mermaid for human eyes.
   Ours needs the same map parseable by agents as a route (the seed-MCP
   join_protocol pattern: a cold agent walks the building via bounded
   pointers). None serve agent-walkable maps.
4. THE ECONOMY LAYER: none show settlement on the map (the rail's visible
   85/10/5 particle split is ours alone - the tokenization-MCP law).
5. THE RE-BANK LESSON APPLIED: Graphify's 8 dead resubmits prove Karpathy's
   law - distribution rides an existing wave ("someone built the thing just
   described"), never self-submission. Our wave: the perimeter paid real TON
   this week; the factory walk-through posts AFTER the next real settle, not
   before.

## The steal (ranked)

1. TREE-SITTER CLUSTERING (one sitting): Repomap's Rust engine pattern
   (tree-sitter parse -> petgraph module clusters) compiles any estate system
   into the truth-hunt architecture format - the room/belt/machine schema
   gains an automatic draft generator; humans curate, not draw.
2. THE GITDIAGRAM URL TRICK (one sitting, distribution): our explainer maps
   reachable by a URL convention on any estate repo (explained.<org>/<repo>
   or the hub->diagram swap) - zero-install discovery.
3. ZOOM-RECURSION (one wave, CodeBoarding's shape): system -> component ->
   file recursive diagrams, so the truth-hunt building has floors and the
   floors have rooms and the rooms have machines - the coldest-vertex human
   lands at machine level; the agent routes at floor level.
4. THE UNANSWERED QUESTION AS OUR SPEC: Repomap's dead comment (does
   clustering follow call patterns? how do star-imports resolve?) is the
   spec question our format must answer first - because our rooms are
   AUTHORED, the import problem is smaller; we answer it in the schema doc.

## Falsifier

If tree-sitter clustering + authored schema cannot coexist (the generated
map contradicting the authored rooms), the truth-hunt architecture layer
fails its own test: the map must be both generated and authored or it is
one or the other - and the format needs the machloket field to hold the
difference openly.
