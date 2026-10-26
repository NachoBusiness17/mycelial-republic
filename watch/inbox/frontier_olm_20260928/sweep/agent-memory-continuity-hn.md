# agent-memory-continuity sweep via Hacker News - source-fetched: 2026-09-28

Door: hn.algolia.com API (search_by_date + relevance search), 14 queries; deep reads on news.ycombinator.com threads and primary pages. Seat: sweep-agent-memory-continuity-hn. Branch: mag/run-beta1-factory-build-audi-20260806T231709Z.

## Method and counts

Pass 1 (broad sweep, last 30 days, numericFilters=created_at_i>1787961600): 14 Algolia queries over "agent memory", "LLM memory", mem0, MemGPT, CRDT, merkle, verkle, "append-only log", episodic memory, "context engineering", "session transcripts", LongMemEval, "graph memory", tamper-evident, plus a relevance pass on "agent memory". Result: roughly 60 distinct stories collected; the strong-relevance subset is 24 (listed under "Pass 1 candidates" below). MemGPT, "memory consolidation", and verkle doors were nearly empty (verkle returned only CUDA-verkle, listing-only). Mem0 returned zero story hits.

Pass 2 (deep reads, fetched and read end to end this session): calpaterson.com/memoryfields.html, news.ycombinator.com/item?id=49508317 (96-comment thread), notion.com CRDT blog, arxiv.org/abs/2502.12110, github.com/oleg-vdv/kepil README, ctx.rs/pro/, blog.getzep.com Konig post, github.com/docukit/docukit README, github.com/okf-memory/okf-agent-memory README, github.com/zackemannen81/docs-first_continuity-protocol README. That is 10 fetch-and-read units; 7 items banked.

## Degradations (never fabricated)

- Medium post "Five failure modes around fact retirement in agent memory, with measurements" (HN 49877124): WebFetch returned HTTP 403; web_reader MCP fallback returned MCP error -500 twice. NOT banked; listing-only. Directly relevant to fact retirement (= residual prune), needs a manual read.
- MemGPT and mem0 queries: zero story hits in window. "memory consolidation": zero hits.
- verkle query: only 49816163 "CUDA-verkle - GPU-accelerated 256-MSM for Verkle tree commitments" (github.com/Dyslex7c/cuda-verkle), not deep-read, listing-only. No published verkle-chained MEMORY LOG outside the estate surfaced through this door.

## Answers to the five research questions

1. 2026 agent-memory architectures vs residual-registry-leaf spine. The 30-day HN window shows the field converging on file-shaped memory: memoryfields (zip of markdown pages + YAML frontmatter + sqlite-vec index, ~8kb page cap = our leaf-size instinct), OKF git-native knowledge bundles, docs-first continuity protocol (authority-ordered entry points: status doc outranks README = our state/CURRENT.md live-truth law). What they do that the spine does not: (a) bi-temporal invalidation instead of overwrite (Zep invalid_at; sibling lane w3-research-memai already banked the concept 2026-09-28); (b) link generation and memory evolution across entries (A-Mem, already known to the estate at memory/steal/STEAL_CAUSAL_GRAPH_MOONSHOT_20260814.md:122); (c) structured authority ordering for stale-vs-live docs (docs-first). All adoptable without a new substrate: (a) is a registry column, (b) is edges in memory/knowledge_graph.json (currently zero-edge), (c) is a boot-doc law the estate already half-owns.

2. Knot-as-CRD (lens laws.md open question): YES, a published merge-friendly design exists. Notion's blog specifies RGA (Replicated Growable Array) where every operation carries a stable ID of session ID + Lamport clock, inserts reference an origin ID, concurrent same-origin items order by timestamp then session ID, deletions are tombstones, and IDs attach to character runs not characters. That grammar (session_id, logical_counter, origin_ref, tombstone) is directly adoptable as knot journal records without any new substrate: multi-writer merges become deterministic with no central lock. Peritext-style anchored annotations are the analogous pattern for doctrine-node revisions.

3. Law-to-module edge (lens graph.md): the window's concrete mechanisms are OKF code_refs (code-to-knowledge binding with --for-path constraint queries: knowledge nodes declare which code paths implement them, and the query direction "which knowledge covers this path" is first-class), ctx blame (code line -> producing agent session -> original transcript, with proven/possible/missing evidence states, all local), and the calpaterson thread's ADR pattern (stable decision IDs like R1/D4 referenced from code and docs). All three are edge grammars the estate can graft onto the existing knowledge_graph.json nodes; ctx's proven-vs-possible distinction is the honest-evidence twist our law-to-module edge should copy.

4. Longitudinal session-transcript studies: NO published study predicting next-session success from transcript mining surfaced through this door in the window. Closest artifacts: ctx blame (attribution of code to sessions, not outcome prediction) and Gage (HN 49566640, Claude-session scanner, listing-only). The 14,858-row session oral history corpus can support an estate-side equivalent (predict next-session success from filed day summaries), but no external template was found; this stays an estate-first study. Honest gap.

5. Verifiable append-only log designs outside the estate's chain: Kepil is the strongest find. Hash-chained append-only JSONL (not merkle), values never enter the journal (only types, counts, hashes), chain head is witnessed OUTSIDE the writer process (confirmation cards quote the head they saw; "Records written after the last witnessed head stay unprotected"), and the verifier is a deliberately independent implementation in another language ("Proof that only its own author can check is not proof"). Versus the estate's repair-and-verify loop: the adoptable pieces are (a) external head witnessing between writes, (b) an independent verifier (the estate's verifier is in-repo), (c) content-blind journal rows. No merkle/verkle-chained published memory log was found (see Degradations); the estate's verkle chain remains more advanced than anything the door surfaced.

## Banked items (7, strongest first)

### 1. Notion: How Notion handles concurrent editing with CRDTs (HN 49881416, 2026-09-28)
Quote (verbatim): "As the number of collaborators grows, the chance that one person's change gets overwritten by someone else's increases."
Why: the knot-as-CRD open question gets a full published answer here: RGA operation log where IDs are session ID + Lamport clock, origin-referenced inserts, timestamp-then-session-ID tiebreak, tombstone deletes, run-length-compressed IDs. This is the merge-friendly log grammar the lens laws.md question asked for, adoptable as knot journal records with zero new substrate.
Overlap: git grep "Replicated Growable Array" and "Lamport" over catalog/ + memory/: "Replicated Growable Array" zero hits; "Lamport" hits are our own Lamport Part-Time Parliament receipts (docs/report_v1/sources, catalog rows 78320-78342), not this design. Notion hits in catalog are MCP integrations only. NEW.

### 2. Kepil: passport, mandate and tamper-evident journal for AI agents (HN 49692366, 2026-09-14)
Quote (verbatim): "Proof that only its own author can check is not proof."
Why: the strongest published verifiable-log design of the window and a direct critique-in-advance of any self-verifying chain: append-only hash-chained JSONL, content-blind rows (types/counts/hashes only), external witness of the chain head, independent verifier in another language, and an honestly stated limit ("Records written after the last witnessed head stay unprotected").
Overlap: "Kepil"/"proofbyte" zero real hits (only substring noise in corpus shader files); "tamper-evident" hits are the estate's own embassy integrity suite (memory/embassy/AOS/integrity_suite/). Adjacent holding, distinct design. NEW as a design.

### 3. Cal Paterson: Agent memory as a file format + HN thread (HN 49508317, 2026-08-31, 191 pts / 96 comments)
Quote (verbatim, from the article): "memories work best when they include citations, ideally in the form of URLs"
Why: the biggest memory story of the window converges on the estate's own shape: zip of markdown pages, ~8kb soft cap per page (leaf-scale), frontmatter metadata, agent-writable. The thread adds the weed-the-garden law ("You have to constantly tend the garden and weed these things out." - iamflimflam1), the ADR-with-stable-IDs pattern (hombre_fatal), and mofosyne's git-as-log argument: "incremental writes, commit hash pinning and diffs for free" with the sqlite index gitignored as rebuildable cache (exactly our FTS-decays-to-scan-fallback situation, B2-465).
Overlap: "memoryfields"/"calpaterson" over catalog/ + memory/: zero real hits (steps.jsonl hits are sibling-run command echoes, not holdings). NEW.

### 4. OKF Agent Memory: Git-native persistent memory for AI coding agents (HN 49581240, 2026-09-05, 81 pts / 32 comments)
Quote (verbatim): "Inspect, audit, and review your agent's memory using standard git diff and git log."
Why: the concrete implementation of a format the estate already adjudicated (OKF v0.2 = ADOPT/ALIGN per memory/continuity/seat_memory_20260927/llm-internals-syllabus-arc.md:29). The new, graftable parts: code_refs code-to-knowledge binding + --for-path constraint queries (the missing law-to-module edge), trust tiers (generated vs verified = our tri-state discipline), stale_after freshness metadata, and the Search-Before-Write Principle ("prevents concept duplication and hallucinated divergence").
Overlap: concept KNOWN (ADOPT/ALIGN note above); the Go implementation, MCP server, and code_refs mechanism are the new increment. PARTIAL overlap, banked for the implementation delta.

### 5. Zep: We built a graph database service for agent memory (Konig) (HN 49712610, 2026-09-15)
Quote (verbatim): "General-purpose graph databases often assume one large graph" (the post contrasts this with agent memory as "millions of smaller graphs, most cold at any moment")
Why: the per-subject-graph architecture (graph = unit of storage, access, encryption, retention) and fused ranking (vector + full-text + graph + pattern, reciprocal rank fusion) are adoptable design points for knowledge_graph.json without a new substrate. Bi-temporal facts with invalid_at-not-overwrite are the retention mechanic for the registry.
Overlap: PARTIAL. The bi-temporal invalid-not-delete concept was already banked TODAY by sibling lane w3-research-memai (watch/inbox/burn_reset_20260927/flash50/w3-research-memai.md:215, commit 8c28b5aaa, 2026-09-28), and the estate mirrors the older Zep repo (catalog rows 351314-351317: mine/raw/agent_bleeding_edge/getzep/zep/benchmarks/longmemeval/, Graphiti service_ce.go at 351934). The Konig data-plane post (2026-09-15) post-dates that mirror; per-subject graph storage and fused ranking are the new content. Rank lowered accordingly.

### 6. ctx: git blame that returns the original agent transcript (HN 49727859, 2026-09-16)
Quote (verbatim): "git blame tells you which commit last changed a line. ctx blame tells you which agent session produced that commit."
Why: the working published implementation of code-to-session provenance edges, including the honest evidence tri-state (proven / possible / conflicting / missing attribution, refuses to prove what is not on-disk, all local indexing). This is the shape the estate's missing law-to-module edge should copy: line -> producing session -> doctrine, with the evidence grade stored on the edge. Also the nearest tool to transcript mining (Q4) though it does not predict outcomes.
Overlap: "ctx blame"/"ctx.rs" hits over catalog/ + memory/ are only steps.jsonl command echoes from sibling runs. NEW.

### 7. docs-first continuity protocol (HN 49516682, 2026-09-01)
Quote (verbatim): "A continuity protocol whose own repository cannot be picked up by a stranger has answered its own question."
Why: independent articulation of the estate's warm-boot doctrine: known entry point (AGENTS.md), one owner per truth, explicit authority ordering ("If they disagree, the status document is right and this one is stale"), frozen tag-verified baseline, dated change records. Thin repo ("extraction in progress", spec and validator unpublished) but validates that boot-freshness law is a felt industry problem, not an estate eccentricity.
Overlap: "docs-first" hits in memory/MEMORY.md + MEMORY_resolved.md are generic phrases, not this repo; title zero hits. NEW but low mass.

## Deduped (known holdings, not re-banked)

- A-Mem: Agentic Memory for LLM Agents (arXiv 2502.12110, HN 49877747): already known at memory/steal/STEAL_CAUSAL_GRAPH_MOONSHOT_20260814.md:122 ("A-MEM (2502.12110): derived bead/forest links are allowed").
- Zep bi-temporal invalidation: sibling lane w3-research-memai.md:215, committed 8c28b5aaa 2026-09-28.
- OKF v0.2 spec: adjudicated ADOPT/ALIGN, llm-internals-syllabus-arc.md:29 (only the implementation delta banked).
- docukit (HN 49830033): read its README; the About-line claim "Faster than any CRDT" carries no methodology on the page (comparison tables deferred to docukit.dev); CRDT-agnostic transport. Too thin to bank.

## OWED

- Five failure modes around fact retirement (Medium, 49877124): 403 on WebFetch, -500 x2 on web_reader; needs a browser or authenticated fetch. Directly on-topic for residual pruning.
- CUDA-verkle (49816163): listing-only; if the estate wants GPU acceleration for chain verification, a deep read is owed.
- Gage session scanner (49566640): listing-only; adjacent to the Q4 corpus study.
- No published longitudinal next-session-success study found through this door; other doors (arxiv/web) should be tried before declaring none exists.
- HN thread for Kepil and ctx not fetched (few comments per Algolia: 0-2); deep reads were of the primary pages.

## Pass 1 candidates (strong subset, 24)

49508317 memoryfields (191/96), 49581240 OKF (81/32), 49881416 Notion CRDT (3/0), 49692366 Kepil (2/0), 49712610 Zep Konig (2/0), 49727859 ctx (3/2), 49516682 docs-first (3/0), 49861765 cognee guide (3/0), 49628820 Four Kinds (4/0), 49807330 retention policy (2/0), 49749689 agentmemoryleaderboard (2/0), 49703919 Backpass (2/0), 49701788 Polign typed memory (1/1), 49721941 Context Freshness Ledger (1/0), 49594849 Awareness-Market LongMemEval 96% (1/0), 49535102 MLM what works (2/0), 49504689 Shapes of Agent Memory (3/0), 49887024 memory poisoning (2/0), 49877124 fact retirement (1/0), 49830033 docukit (1/0), 49699591 Rebuno (3/0), 49571131 context-engineering-kit (44/4), 49566640 Gage (4/2), 49816163 CUDA-verkle (3/0).
