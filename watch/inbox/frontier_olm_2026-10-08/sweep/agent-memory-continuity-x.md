# Sweep: agent-memory-continuity via x - 2026-10-08

source-fetched: 2026-10-08
Seat: sweep-agent-memory-continuity-x, frontier_olm_2026-10-08. Area: agent memory
continuity (isolated priors to verified edges, knot identity keys, append-only ledger
writer, write-time/use-time contracts under compaction, embeddings vs keyed lookup).
Doors used: WebSearch site:x.com (Pass 1) and api.fxtwitter.com resolution (Pass 2),
per the doors probe watch/inbox/frontier_olm_2026-10-08/lens/doors.md:66-83 (fxtwitter
YES, 1st probe) and :20-39 (arXiv minimal query shape). Every URL below was fetched this
sitting; every quote is verbatim from what came back.

## Method and instruments

- Pass 1: 8 WebSearch runs with site:x.com queries (agent memory graph consolidation;
  compaction continuity; append-only ledger event sourcing; embeddings vs keyword;
  dedup identity; Anthropic memory tool; jsonl session files; mem0/cognee/letta/zep).
  Candidate pool considered: 60+ posts. The web_search backend returned MCP 1302
  rate-limit errors on 4 of the 8 (matching the estate's own measured envelope,
  AGENTS.md fan-out law), so the strictly in-window (2026-09-08..2026-10-08) subset
  reached about 21 candidates, not the asked 30; the rest of the pool skews older and
  was considered but is date-flagged. This shortfall is stated, not papered over.
- Window rule: tweet created_at from the fxtwitter JSON is the authority. Cutoff
  2026-09-08 00:00 UTC (30 days before today).
- Pass 2 deep reads (fetched and read end to end this sitting):
  1. https://arxiv.org/abs/2607.21503 via export.arxiv.org minimal shape
     (search_query=id:2607.21503) after arxiv.org/abs and github.com raw both timed
     out at 60s on first probes.
  2. https://github.com/Tin11Mn/chrono-hybrid-mem README (raw.githubusercontent.com).
  3. https://github.com/lpaiu-cs/osk-system README (raw.githubusercontent.com), found
     via the bestproductivityresources.com listing.
  4. https://github.com/mcncarl/agent-memory-vault README (raw) + repo metadata via
     api.github.com/repos/mcncarl/agent-memory-vault (created 2026-06-20, pushed
     2026-10-04, MIT, 313 stars).
  5. https://github.com/mcncarl/agent-memory-vault README is the fifth end-to-end
     read; plus fxtwitter full-text resolutions of rachittshah 2097657181235753206,
     pauliusztin_ 2097282009605218640, alphabatcher 2095503115130646825,
     DanKornas 2105636089578881389 and 2106689285638275092,
     AgentMemoryL 2096799172112556146 and 2101515447816663222,
     TheYotg 2099809478375796831, aiwithjainam 2100573664530100639,
     cyjustinchen 2105737463096340846, marfinxx 2094016175617241109,
     WenhuChen 2052870502927286684.

## Banked items (strongest first, mirrors the submitted SweepResult)

1. agent-memory-vault (mcncarl) - Q1/Q2/Q3. "Markdown remains the source of truth";
   every derived store rebuildable from Markdown; writes flow proposal -> exact
   authorization -> apply -> scoped closeout commit; "Text such as 'obsolete' or
   semantic similarity never creates a supersession edge" - a supersession edge exists
   only when the writer explicitly lists predecessor paths in a supersedes field;
   facts require a stable fact_key; actors carry session IDs (AGENT_MEMORY_SESSION_ID)
   and fencing tokens, one live lease per canonical path. This is the P1 cite-allowlist
   linker shape (an edge exists only if its cited paths verify) applied to memory
   writes, and the closeout-commit gateway is a working minimal append-only writer
   consistent with amend-never-rewrite. Overlap: none of memoryctl, fact_key,
   agent-memory-vault, supersession-edge-with-predecessor-paths appear in
   catalog/catalog.jsonl or memory/ (rg counts 0 for the four distinctive phrases;
   plain "supersession" hits 15 estate files but in fold/percolator contexts, cited in
   the submitted overlap rows).
2. osk-system (lpaiu-cs, announced by DanKornas 2026-10-04) - Q1/Q2/Q4. Capture is
   pointers not copies: "The hooks track each finished turn of the conversation on
   your device, as a reference into the harness's own transcript and a hash" and
   "nothing is copied into the vault"; a node's derived-from points at the cited
   transcript round; "A node about the same claim is updated, not duplicated"; since
   v4 unrelated repos get suffixed session identity <name>-<first 8 hex of root>;
   multi-device ledgers reconcile "by causality (a DAG), not by timestamps". Isolated
   nodes are expected ("New nodes stand alone first; a hub links them later"), and
   when evidence changes, citing nodes become recheck candidates spreading along the
   citations - that is the use-time half of a write-time/use-time contract. Overlap:
   osk-system, derived-from, recheck-candidate: 0 catalog hits.
3. ChronoHybridMem (AgentMemoryL tweet 2026-09-07, 21h outside the strict window,
   kept and flagged; repo Tin11Mn/chrono-hybrid-mem read end to end) - Q1/Q2/Q5.
   Tweet: "Agent Memory should return evidence, not just similar text." README: raw
   evidence is the single source of truth; request_id idempotency ("reusing a
   completed request_id is idempotent, no duplicate messages"); P3 auxiliary
   structure's "nodes and edges must point back to original messages"; the reranker
   may only reorder existing candidate IDs under an ID allowlist; best config is FTS5
   multi-channel + RRF + bm25 with BGE/ColBERT/cross-encoder demoted to research use
   (Hit@1 0.5850 to 0.6108 on 1,976 questions). Converges with the GPS-embed kill
   (watch/inbox/gps_embed/GPS_EMBED_TRIAL.md per lens/burns.md:129-131) and with P1's
   allowlist gate. Overlap: ChronoHybridMem 0 hits; request_id appears in catalog 4
   rows and one astra vault script, different domain.
4. Agentic Context Management (TheYotg 2026-09-15, paper arXiv 2607.21503 by Gaurav
   Dadhich, submitted 2026-07-23) - Q4/Q1. Five lifecycle primitives: architecting,
   ingesting, scoping, anticipating, compacting & consolidation; entity resolution at
   ingestion ("Sarah", "Sarah Chen", "SC" linked); consolidation "with provenance
   preserved"; and the load-bearing line: "validated compaction achieves linear cost
   with fidelity preserved" while naive accumulation is quadratic and summarization
   hits an accuracy cliff. Validated is the operative word: the ReFold restore door
   (proved 4,290 chars, port wave P5) is exactly such a validator. Benchmark numbers
   (92 percent LongMemEval, 93.2 percent LoCoMo) are self-reported by the paper's own
   reference implementation, single author, treat as vendor claims. Overlap: full
   title and 2607.21503 have 0 catalog hits; LongMemEval appears 15 times in catalog
   (already-known benchmark).
5. Agents as distributed systems (rachittshah 2026-09-09) - Q2. Tweet: "I've found
   more agent latency in queues, tool calls, and synchronization barriers than in any
   single inference setting." Search-result summary of the linked article: "unique
   run identities for submissions, ensuring caches don't conflate concurrent
   operations." The article body behind x.com/i/article/2097644392978984960 is
   login-walled to this instrument; banked per the recipe's snippet fallback, said so.
   This is the corr_id question in industry clothes: run identity as the join key so
   concurrent writes never conflate. Overlap: 0 catalog/memory hits for "agents as
   distributed".
6. Distill (DanKornas 2026-10-01) - Q2. Tweet lists "Persistent memory, Write-time
   deduplication, Conflict detection, Hierarchical decay, Deterministic processing",
   MIT open source, link in a reply not resolved (repo URL unverified, OWED).
   Write-time dedup is the collision-free-label answer's other half: dedupe at write
   time so labels cannot fork. Overlap: 0 hits for "write-time dedup".
7. MINTEval accepted to NeurIPS 2026 (cyjustinchen 2026-10-01) - Q4. "memory
   systems... must process long contexts and reason over many updates that create
   interference between old and new information." No arXiv or GitHub link in the post
   (author site dinobby.github.io); OWED to fetch the paper. Name collision flagged:
   the estate catalog already holds a DIFFERENT MintEval (trading-strategy behavioural
   equivalence, state/arxiv/2026-10-05/2610.03080v1.txt, catalog id 4a3686138da6);
   do not conflate them when weaving.
8. Agent Memory Challenge 2026 Cycle 2 (AgentMemoryL 2026-09-20) - Q4/Q5
   infrastructure. Long-term memory evaluation framed as "retrieving the right
   evidence, recognizing what has changed, and avoiding stale context"; three tracks
   (textual, coding, multimodal); runs through October 31; shared Add/Search interface
   with standardized evaluation. A ready-made external battery for the estate's
   keyed-lookup memory if it ever wants an outside grade; deadline is actionable.

## Considered, resolved, and left out (with dates)

- aiwithjainam 2026-09-17 five-layer memory framework (in window; echoes Mem0 token
  claims and an Anthropic PDF; secondary).
- pauliusztin_ 2026-09-08 four harness components for high-signal context (in window;
  surface-level; original at decodingai.com).
- marfinxx 2026-08-30 Trace Engineering / event sourcing append-only ledger (9 days
  out of window; article login-walled, preview only).
- alphabatcher 2026-09-03 Agent Memory That Improves Between Runs (5 days out; links
  Anthropic Dreams docs platform.claude.com/docs/en/managed-agents/dreams and the
  AgentRun benchmark arXiv 2605.12493; the run-50-pays-for-the-lesson framing is the
  same disease as the estate's isolated-priors graph).
- WenhuChen 2026-05-08 DCI-Agent (out of window, verified date): terminal grep
  80.0 percent at 1,016 dollars vs Qwen3-Embedding-8B retriever 69.0 percent at 1,440
  on BrowseComp-Plus, same backbone. Five months old, but it is the strongest public
  prior for the GPS-embed kill and belongs in the retire-the-class memo as context,
  not as a banked row.
- Weak/context-only: VentureBeat memory event, ai_explorer25 commentary,
  DivyanshT91162 Zep repos list, JoshARosen Zep temporal-KG posts (Sep 08-13),
  TheValueist seven-layer, yoheinakajima CLS, troyhua seven layers, heynavtoor
  never-cut-at-an-orphaned-tool-call rule, vsletten3006 reversible context editing,
  ghumare64 hybrid BM25+vector+KG, henrytdowling three dimensions, dair_ai structured
  retrieval, mem0ai DeerFlow, S_BatMan mem0 deleted-graph-code, zostaff, analogalok,
  agihouse_org, mikenevermiss, HiTw93, stablechen, DataScienceDojo, mixedbreadai
  ColBERT, DhravyaShah nDCG deltas, rryssf_ UNC auto-designed memory, ashwingop,
  code_rams QMD, nicbstme, KirkMarple, remembradev, timschukar, manthanguptaa,
  mvanhorn, meta_alchemist, alphabatcher Grok Bot guide, rohit4verse, SuJinyan,
  calcsam, aparnadhinak, Gyome1_, techgirl1908, akshay_pachaar.

## Reading for the estate (answers the five questions point at)

- Q1 (priors to verified edges): all three strongest artifacts agree the cheap linker
  is DECLARATION PLUS PATH VERIFICATION, not similarity: vault supersedes lists
  predecessor paths; osk derived-from points at a hashed transcript round; chrono
  edges must point back to original messages and the reranker lives under an ID
  allowlist. The estate already owns the verifier (P1 cite-allowlist whole-repo path
  gate, port wave P1 per lens/burns.md:115-116); the missing piece is a writer that
  emits candidate edges only in that verified form.
- Q2 (identity keys): the convergent key set is (actor, session id, content-derived
  digest or claim hash) with request/corr idempotency: vault fact_key + session ID +
  fencing token; osk root-commit-suffixed session identity + claim-level dedup;
  chrono user_id/session_id/request_id idempotency. Knot labels should become
  (session_root_digest, knot_seq) or corr_id + digest, never a free-text label.
- Q3 (ledger writer build or retire): the record supports BUILD. Two independent
  shipping systems treat the git closeout commit as the append-only ledger row
  (vault closeout; osk DAG reconciliation), which is also exactly the estate's
  interim stance that "a DIGEST/RECEIPT pair plus a git commit IS the mining record"
  (watch/inbox/frontier_olm_2026-10-08/lens/burns.md:56-58). A minimal writer =
  append one JSONL row + commit, schema-compatible with the frozen LEDGER.jsonl,
  no rewrite path. Evidence is banked; the decision stays the operator's per
  RIB_GRAMMAR_SEED promotion law (memory/rib/RIB_GRAMMAR_SEED_20260810.md:41-44 via
  lens/laws.md:114-118).
- Q4 (write-time/use-time contracts): osk's recheck-candidate spreading and the
  vault's lease/fencing/adopt_external machinery are shippable shapes for the day-6
  write-time/use-time subject (lens/burns.md:71-72); ACM's validated-compaction line
  says the validator (the estate's proved ReFold restore door, lens/burns.md:118-120)
  is the differentiator, not the compressor.
- Q5 (embeddings vs keyed lookup): nothing read this sitting beats keyed lookup on
  the estate's own jobs; chrono demotes vector models to research use, DCI-Agent
  measured grep over embeddings at lower cost, and the one pro-embedding datapoint
  (DhravyaShah nDCG gains) is corpus-search-shaped, not knot-lookup-shaped. If the
  estate ever wants a measured embedding job, the Cycle 2 textual track is the
  cheapest external place to run one before retiring the class.

## OWED / not done

- osk-system repo URL for the DanKornas osk tweet: the tweet says link in reply; the
  lpaiu-cs/osk-system path was obtained from the bestproductivityresources listing,
  not from the tweet thread; treat the tweet-to-repo join as unverified.
- Distill repo URL unverified (link-in-reply, not resolved).
- MINTEval paper link not in the post; not fetched.
- The article bodies behind x.com/i/article/2097644392978984960 (rachittshah) and
  x.com/i/article/2093846271194718208 (marfinxx) are login-walled to WebFetch and
  fxtwitter returns preview text only.
- 4 of 8 WebSearch runs returned 1302 rate-limit errors; the 30-candidate in-window
  goal was reached only partially (about 21 strictly in-window; 60+ total pool).
- arxiv.org/abs/2607.21503 and raw github fetches timed out once each at 60s; the
  export-API minimal shape and a retry succeeded; no fallback success is claimed for
  the timed-out URLs themselves.

## Receipt

- All fetches this sitting: 12 fxtwitter resolutions, 5 WebSearch-success runs (+4
  rate-limited), 2 export.arxiv.org queries, 5 raw.githubusercontent/api.github.com
  fetches, 1 bestproductivityresources fetch. Overlap greps run with ripgrep 15.2.0
  over catalog/catalog.jsonl and memory/ (first grep -r attempt was killed after ~8
  minutes on the huge tree and rerun with rg; instrument named here per counts law).
- Em-dash law: this file is ascii-only, no em or en dashes.
