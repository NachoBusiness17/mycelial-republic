# Sweep: agent-memory-continuity via X (frontier_olm_2026-10-07)

source-fetched: 2026-10-07

Seat: sweep-agent-memory-continuity-x. Doors used per the ask's recipe: WebSearch
(site:x.com and open-web queries) for Pass 1, then the fxtwitter door
https://api.fxtwitter.com/<user>/status/<id> (verified working this week by
watch/inbox/frontier_olm_2026-10-07/lens/doors.md:24-28) and direct WebFetch for Pass 2
deep reads. Door health honestly: WebSearch threw repeated 429/1302 rate-limit errors
mid-run (three consecutive queries at the "October 2026" sweep attempt all failed); it
recovered on retry with reworded queries. api.fxtwitter.com answered every call, zero
failures. The getzep.com temporal-KG blog URL returned HTTP 404; the Zep bi-temporal
material below is sourced from the yoheinakajima article instead. old.reddit.com stayed
closed (login gate, lens/doors.md:35-38), so no reddit items.

## Method

- Pass 1 (broad): 11 WebSearch queries (X and open web) + 2 hn.algolia.com API calls
  (verified door). Candidates considered: 60+ distinct items (roughly 30 from search
  snippets incl. X posts, 30 from the two HN API pages filtered to agent-memory topics).
  Date-window honesty: today is 2026-10-07, so the strict last-30-days window opens
  2026-09-07. Only ONE deep-read item is strictly inside it (RIME, 2026-09-28); funes
  (09-03) and memoryfields (08-31) sit just outside; the strongest X-land material for
  these five questions clusters Apr-Sep 2026. I banked on strength, and I state each
  item's real date rather than pretending recency.
- Pass 2 (deep read): 10 fetches, 9 distinct items read end to end this session:
  fxtwitter x6 (two _avichawla posts, neural_avb, yoheinakajima twice - second pass for
  verbatim quotes, iHarnoorSingh), arxiv.org/abs/2609.34438, calpaterson.com,
  huggingface.co/blog/funes, and liao.gg (read, then dropped as sibling-banked, below).
  liao.gg "Agents don't need memory, they need documentation" (2026-10-03, HN 49945933,
  380 pts) is genuinely strong for Q1/Q5 (its freshness pillar: the working agent writes
  docs while context is full, facts rewritten not appended) but
  memory/trajectory/steps.jsonl shows the frontier_olm_2026-10-04 sibling already
  fetched and banked it (page saved as
  watch/inbox/frontier_olm_2026-10-04/sweep/_am_page_49945933_doc_https_liao_gg_blog_agents_dont_need_memo.txt,
  bank file agent-memory-and-continuity-hn.md). Per the anti-rebank law it is cited
  here, not re-banked. Same disposition for sibling-banked SuperLocalMemory 4.0 (arXiv
  2608.08253) and the reduck browser-action memory layer (HN 49910148).
- Overlap instrument (exact commands run this session):
  grep -o -E "2609\.34438|Retrieval-Induced Memory|memoryfields|calpaterson|funes|yoheinakajima|2606\.06036|MRAgent|GNN-RAG|hallucinations of the past|_avichawla|2047222861614686589|2084909858386792674|Hindsight|bi-temporal|MemDelta|LongMemEval|sleep-time" catalog/catalog.jsonl
  -> hits ONLY: Hindsight x3, LongMemEval x3, _avichawla x10, sleep-time x1 (an svg).
  The _avichawla hits are two OTHER posts already banked (article 2096491130489872479
  from the 10-01 sweep, status 2075888860115120424 from the 10-05 sweep); neither of my
  two status IDs appears. Hindsight hits are two unrelated papers plus one banked "Zep
  vs. Vectorize Hindsight: A Neutral Look" page. A recursive grep of memory/ timed out
  unbounded; rerun bounded to --include *.md/*.jsonl it returned zero hits for every
  item phrase except the liao.gg/okf/SuperLocalMemory family in
  memory/trajectory/steps.jsonl (sibling step journal, handled above). Mem0/Letta/Zep
  as NAMES were banked in the one-computer steal map (commit 70508dcf6, via
  lens/burns.md:134); the yoheinakajima item's measured numbers are new on top of those
  names.

## Banked items (8, strongest first; full quotes verbatim from pages I fetched)

1. _avichawla status 2084909858386792674 (2026-08-05, ~link into @akshay_pachaar
   "Pydantic fixed my Agent's Memory"). A 12-system study across
   representation/extraction/retrieval/maintenance finds WRITE time, not query time,
   determines correctness; graph systems that impose structure at write stay reliable
   under fact updates; append-only stores return outdated facts, which the paper calls
   "hallucinations of the past"; heavy structure costs orders of magnitude more query
   time, so maintenance must stay local. Core line: "Retrieval only ranks what the
   extraction chose to keep." This is the direct successor reading to banked arXiv
   2610.03902 (adoption-at-use 8-9/13 vs re-read 13/13): the answer shape is neither
   pure write-time nor pure use-time, but typed structure at write + local maintenance.
   Estate graft: mag/memlang.py knots should carry write-time typing, and the
   zknot/context-pack write path is where correctness is decided.

2. arXiv 2609.34438 RIME "Remember by Asking: Retrieval-Induced Memory Evolution for
   LLM Agents" (submitted 2026-09-28; Zhou, Lu, Wang, Xing, Chen, Han, Shi). Abstract:
   existing systems retrieve at read time while write-time memory formed by "direct
   extraction or compression" can miss "locally important details that may matter
   later"; RIME uses self-questions to retrieve dialogue evidence and builds an
   "evolving memory bank with temporal and provenance information"; at inference it
   retrieves source dialogue with local context instead of full history; best on all
   three LoCoMo quality metrics (Qwen3-235B-A22B and GPT-5.6 Sol backbones) at
   substantially fewer query-time tokens. Only strictly in-window item; answers Q1
   (re-read the source with local context beats both) and Q2 (temporal + provenance
   fields on the bank).

3. yoheinakajima status 2037201711937577319 (2026-03-26, X article "The state of AI
   memory systems"). The one page with measured numbers for Q2/Q3: Hindsight 91.4%
   LongMemEval Medium, temporal queries "from a 31.6% baseline to Medium 91.0%, a
   nearly 60-point gain" via four parallel retrievals (cosine, BM25, graph traversal,
   temporal) fused by cross-encoder reranking, MIT licensed; Zep/Graphiti "Every entity
   edge tracks four timestamps: valid_at (when the fact became true in the world),
   invalid_at (when it was superseded)" and "Contradicting facts are invalidated
   rather than deleted, preserving the complete temporal record." at 71.2%
   LongMemEval, tradeoff slow LLM-heavy ingestion; "Mem0 achieves 66.9-68.5% on LoCoMo
   (base and graph variants respectively) with excellent latency - 1.40s p95 versus
   17.12s for full-context Mem0", weak temporal; "Letta demonstrated that a simple
   filesystem approach (agent + file tools) achieved 74.0% on LoCoMo with GPT-4o-mini,
   outperforming Mem0's best score" of 68.5. For the estate: temporal-aware retrieval
   is the single biggest measured lever (31.6 -> 91.0), and a plain filesystem beats a
   vendor layer, which fits the no-throne flock law.

4. iHarnoorSingh status 2085186877095862283 (2026-08-06, X article "GraphRAG is
   getting pretty expensive.."). Three bills of graph memory: construction (LLM calls
   before any question), LLM traversal (ToG up to 21 retrieval LLM calls, RoG 3,
   graph-native zero; cutting LLM-generated paths dropped hit rate 8.3-9.9 points),
   maintenance ("Storage is cheap. Keeping the graph trustworthy is the product.").
   Recommended shape: cheap vector/lexical neighborhood first, bounded graph traversal
   second, "the smallest sufficient subgraph"; GNN-RAG 87.2% hit rate with zero
   retrieval LLM calls vs RoG 85.7% / ToG 76.2% on WebQSP. Directly answers Q4 for the
   estate's star forest (1,066 of 2,938 nodes orphaned, lens/graph.md:30): stitch
   orphans with a cheap embedded-neighborhood pass, validate edges with a small local
   scorer (GNN-style), never pay per-hop LLM calls, and budget for maintenance as the
   real cost.

5. calpaterson.com/memoryfields.html (2026-08-31, HN 49508317, 191 pts). "Memory is
   data! The less fixed machinery we put between the agent and that data, the better
   the agent can be." A memoryfield is an open zip of Markdown pages (optional YAML
   frontmatter: title/created/updated/uuid/summary) plus optional SQLite vector index
   on nomic-embed-text-v1.5 (270MB, non-GPU); retrieval = 2 tool calls (search, then
   parallel read) vs N+1 serial graph traversal; transports local file/S3/GitHub/
   HTTP/Syncthing; explicitly anti-lock-in ("vendor-lock-in mechanisms" named as the
   failure mode of existing memory systems). Q3 answer for a local-first no-throne
   flock: format, not service.

6. huggingface.co/blog/funes (2026-09-03, HN 49552053). "A memory is a dataset, not a
   service" - single binary, local embedding + reranking, Lance dataset append-only
   locally, shared memory as a private HF dataset you own; hybrid vector+BM25 + cross-
   encoder rerank + recency reweighting; nothing distilled into facts, recall returns
   original text with provenance (agent, timestamp, session, turn); "Recall was the
   cheapest of the three on both tasks, 8x cheaper than a written handoff on one and
   4x on the other" (beating both compaction and written handoffs; compaction FAILED a
   task via flattened summaries - a direct temporal-flattening datapoint for Q2).
   Falsifier-grade community number in the comments: on ~19k sessions funes 1.3.0 hit@1
   9/100 with defaults vs 19/100 with recency OFF (a BM25-only tool did 18/100 in 29s
   vs funes 2h03m index) - i.e. recency reweighting HURT there; recency policy is
   workload-dependent, not free. License not stated on the page (OWED: check
   github.com/huggingface/funes before grafting).

7. neural_avb status 2067950104062181740 (2026-06-19, X article on MRAgent, arXiv
   2606.06036). In typical systems "memory retrieval is a one-shot process"; MRAgent
   treats memory as "reconstructed, not retrieved": a Cue-Tag-Content graph (cues =
   atomic hints, tags = semantic bridges, content = raw memory) in episodic/semantic/
   topic layers, built by an LLM pipeline that rewrites dialogue, segments episodes,
   extracts cues/tags/topics; multi-turn Navigate/Answer search loop over an Active
   Set; strong LoCoMo + LongMemEval scores at ~118k tokens/sample vs 632k for A-Mem;
   ablations attribute multi-hop gains to structure + multi-turn reasoning. Q4: this is
   the measured automatic induction pipeline shape for turning flat stores into a web
   (rewrite -> segment -> extract -> link), and the tag layer is exactly the
   bridge-node mechanism the estate's orphan knots lack.

8. _avichawla status 2047222861614686589 (2026-04-23, ~194K views). "A bigger window
   is not the same as better memory." Three-layer memory (relational for
   provenance/timestamps/access control, vector for semantics, graph for reasoning);
   the multi-hop failure example (library-closes-before-exams bridge fact missed by
   similarity); Cognee ECL pipeline (Extract, Cognify, Load) writing all three stores
   at once, entity resolution via domain vocabulary files, local-first single install.
   Note the cognee.ai agent-memory guide page was fetched by the 10-04 sibling sweep
   (_am_page_49861765); THIS post is a different artifact and was not in catalog or
   memory/. Q3/Q4: the domain-vocabulary entity-resolution trick is the concrete
   anti-generic-node mechanism for stitching orphan nodes without fabricating edges.

## Question-by-question summary

- Q1 (write-time vs use-time): convergence across items 1, 2, 6 - typed/structured
  write-time formation decides correctness; use-time re-read of SOURCE with local
  context (RIME) or of original undistilled text (funes) beats both compression and
  full re-read; recall measured 8x/4x cheaper than written handoffs. Zero-memory-call
  sessions (40%, 1wlbqnl row 20): the only policy-shaped evidence found is structural
  - session-start injection of a lean catalog/discovery doc (liao.gg, sibling-banked)
  and funes' per-session retrieval; no paper in this sweep measured a before/after on
  zero-memory-call rate. OWED.
- Q2 (temporal flattening, 244/381 banked): bi-temporal edges (valid_at/invalid_at +
  created/expired) with invalidate-not-delete (Zep/Graphiti, item 3) is the
  demonstrably measured design (temporal queries 31.6 -> 91.0 with a temporal
  retrieval lane); funes adds the counter-weight that naive recency reweighting can
  hurt (9/100 vs 19/100).
- Q3 (local-first layers): filesystem/format approaches beat vendor layers on the same
  benchmark (74.0 vs 68.5, item 3); memoryfields (item 5) and funes (item 6) are the
  two local-first, no-throne designs with measured or at least honest numbers; Mem0's
  measured latency (1.40s p95) is the production-speed reference point.
- Q4 (stitching 1,066 orphans): cheap-first embedding neighborhood + bounded traversal
  + small scorer, zero per-hop LLM calls (GNN-RAG 87.2%, item 4); LLM pipeline shape
  rewrite->segment->extract->link with typed ontology and capped schemas (MRAgent item
  7; Zep caps 10 entity/10 edge types per item 2's article) prevents generic-node
  fabrications; domain vocabulary files sharpen entity resolution (item 8).
- Q5 (keyed belief retirement): invalidate-not-delete on keyed bi-temporal edges
  (item 3) preserves still-valid neighbors by construction; append-only stores
  demonstrably produce "hallucinations of the past" (item 1); rewrite-not-append at
  freshness time (liao.gg, sibling-banked) is the doc-shaped version. Falsifier shape
  for wrongful retirement: retire a belief, then test recall of its still-valid graph
  neighbors; a design that deletes neighbors when invalidating one edge fails.

## Not run / not found

No pytest (none named by this ask). The WebSearch X-door returned snippets without
status IDs on most site:x.com queries; only queries that surfaced full x.com URLs
yielded resolvable posts (5 resolved through fxtwitter, all read). The getzep.com
blog 404 and the reddit door closure are stated above. MemDelta (arXiv, 2026-06-29)
and LongMemEval-V2 (2605.12493) surfaced in snippets as benchmark-validity work but
were not deep-read this session; flagged as candidates for the next pass, not banked
here.
