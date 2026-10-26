# STEAL-BOT A — Perplexity: research-grounding teardown

Lane: PERPLEXITY only. Zero-shared-context triangulation wave, 2026-09-10.
Method: public sources only — Perplexity's own engineering blog, Vespa case study,
docs.perplexity.ai (Sonar/Agent API), help center, community forum, one third-party
teardown (ziptie.ai). Claims below are tri-state where the source was thin.

## THE POINT

Perplexity's real moat is not the model — it is a search layer that ranks PASSAGES
(not pages) through a cheap-to-expensive cascade (lexical filter, then embedding
retrieval, then cross-encoder rerank in the serving path) over a 200B+ URL index
whose recrawl schedule is learned per-URL, so freshness is predicted rather than
polled. Citations stay attached because retrieval assembles the prompt as chunk
records and the model emits inline numbered citations bound to those records, with
a search-use classifier deciding when retrieval is worth the latency. Everything
expensive in that stack is infrastructure we cannot steal, but the three shapes we
can steal — sub-document passage indexing, cascade ranking on local models, and
their open-source eval harness (perturb, side-by-side, LLM-judge verbatim) — all
run at $0 on our free lanes and host ollama.

## Mechanism table

| # | Mechanism | How it works (source) | Steal cost for us | What our pipeline does instead today |
|---|-----------|----------------------|-------------------|--------------------------------------|
| 1 | Query decomposition | Pro Search Classifier decides standard vs multi-step search (docs.perplexity.ai/docs/sonar/pro-search/classifier); multi-step breaks a complex query into sub-queries and retrieves targeted evidence per sub-question into a 200K context (ziptie teardown, help center). Sonar standard = one search; Sonar Pro/agent = many. API exposes `enable_search_classifier` to gate this. | Near-zero: one classifier prompt on the free lane ("does this need N sub-queries?") + a loop calling mag/research per sub-query. | Workers decompose ad hoc inside their own turns. No deterministic router, no sub-query fan-out record. |
| 2 | Multi-source retrieval + ranking/dedup | Own crawler + 200B+ URL index on Vespa: hybrid lexical+semantic+structured retrieval, PASSAGE-level ranking ("relevant passages within documents, not entire pages"), cascade ranking — lightweight ranker narrows candidates, richer cross-encoders rerank the survivors, inference runs in-serving (vespa.ai/case-studies/perplexity). Dedup at the retrieval-filter stage (ziptie: search, filter, rank, dedupe, assemble). Scale: 200M+ queries/day, 358ms median. | Full index impossible. Steal the SHAPE: grep/lexical pass over corpus -> ollama embeddings (the eye, host:11434) -> LLM rerank of top-k only, all local $0. | WebFetch/WebSearch direct hits, no ranked candidate set; retrieval quality rests on the search tool, not us. |
| 3 | Citation-grounded synthesis | Retrieval assembles a structured prompt of chunk records; the generator emits inline numbered citations bound to those records; citation insertion is a discrete pipeline stage (ziptie six-operation model: query processing, retrieval, ranking, generation, citation insertion). `enable_search_classifier` decides when to search at all. (Chunk-record internal format: UNPROVEN — inferred from API citation + search_results fields.) | Low: one-claim-one-anchor discipline. Our cite_gate already verifies post-hoc; add memlang-style anchor ids per claim so every claim is addressable. | cite_gate.py does deterministic primary-source verify BEFORE rightsize (rotation 3/3), but claims are not addressable tokens and verification is batch-level, not claim-level. |
| 4 | Academic mode / focus filters | Product: Focus -> Academic restricts the retrieval stage to scholarly sources (retrieval filter, not a model change); community reports Semantic Scholar dominates the cited backend (Supported-by-reports, not confirmed). API: `search_mode: "academic"` plus the cookbook's domain-allowlist pattern (arxiv.org etc. via `search_domain_filter`). Known bug: academic mode ignores `search_after_date_filter` (community.perplexity.ai/t/539) — proof the filter is just a domain mask bolted to the pipeline. | Trivial: domain allowlist (arxiv, PubMed, Semantic Scholar API, DOI resolvers) wired into our research seam before any LLM sees results. | No primary-literature restriction organ. cite_gate checks sources after fetch; nothing steers retrieval toward primary literature up front. |
| 5 | Freshness/recency | Recrawl scheduling is ML-driven — models predict how often each URL changes, and recrawl frequency follows predicted change frequency ("Higher freshness: ML models predicting change frequency", their engineering blog); real-time continuous indexing on Vespa. API surface: `search_recency_filter` (hour/day/week/month/year) + date-range filters. | Low: a change-frequency-weighted revisit queue for watched sources (cron, $0). Corridors that change fast get refetched; stable ones decay slowly. | No revisit schedule anywhere. Freshness = whatever the fetch happened to return. |
| 6 | Related/follow-up questions | `return_related_questions: true` generates suggested follow-up queries from the search results server-side (docs.perplexity.ai/api-reference/sonar-post). Pro/agent mode chains these into the next search step. | Trivial: one free-lane prompt post-wave: "from these findings, 5 follow-up queries" -> queue rows or fold candidates. | Workers propose NEXT STEP ad hoc per the wave protocol; there is no generated follow-up feed and follow-ups die in the fold card. |
| 7 | Under-documented / inferable from API + changelog | (a) Sonar is sunset Sept 27, 2026 -> "Agent API": multi-step tool-using search is becoming the default shape (docs changelog). (b) They ship an Embeddings API + a full RAG cookbook — they document the architecture they believe in (docs.perplexity.ai cookbook). (c) Their eval framework search_evals is open-source: perturbation categories, side-by-side comparisons, LLM judge with verbatim-copy instruction (github.com/perplexityai/search_evals). (d) Media classifier on sonar-pro: modality routing is a flag, not a pipeline change. | search_evals pattern is the direct steal: define perturbation categories, run side-by-side, judge on verbatim fidelity — maps 1:1 onto grounding_wave's tri-state ledger. | We have falsifiers and GROUND ledger but no standing perturbation suite; evals are ad hoc per-arc. |

## Top-3 stealable, ranked

1. **Cascade ranking on local models.** Cheap lexical filter -> ollama embeddings ->
   LLM rerank of the top-k only. Perplexity's proof: 358ms median at 200M queries/day
   came from refusing to run the expensive model on everything. Our corpus is small
   enough that this is hours of work, $0, and it gives retrieval quality we currently
   rent from the search tool.
2. **Sub-document passage indexing.** Rank and cite PASSAGES, not cards. Our
   topic_index.py (1,040 cards / 23 buckets) indexes whole cards; splitting to
   passage records with stable anchor ids (memlang tokens) turns cite_gate from
   batch verification into claim-level verification, and every claim becomes
   addressable in the chain.
3. **The search_evals harness pattern.** Perturb the input, run side-by-side,
   judge on verbatim fidelity. Perplexity open-sourced exactly the discipline our
   grounding_wave ledger wants as a standing suite. Cost: one free-lane worker run
   per wave; feeds the same GROUND ledger.

## Sources

- Perplexity engineering blog: "Architecting and Evaluating an AI-First Search API" (perplexity.ai/hub/blog/architecting-and-evaluating-an-ai-first-search-api — read via reader; direct fetch 403s to bots)
- Vespa case study: vespa.ai/case-studies/perplexity/
- API docs: docs.perplexity.ai/api-reference/sonar-post; /docs/sonar/filters; /docs/search/best-practices; /docs/sonar/pro-search/classifier; /docs/cookbook/articles/academic-search/README; /docs/resources/changelog
- Help center: "What is Pro Search?" (perplexity.ai/help-center/en/articles/10352903)
- Community: community.perplexity.ai/t/date-filtering-not-working-for-academic-search-mode-sonar-api/539
- Third-party teardown: ziptie.ai/blog/how-perplexity-ai-answers-work/ (six-operation pipeline; direct fetch timed out, claims taken from indexed excerpts — thinner confidence)
- Open-source evals: github.com/perplexityai/search_evals (referenced via engineering blog; not fetched directly)

Bounded: one file, nothing fixed, nothing spawned.
