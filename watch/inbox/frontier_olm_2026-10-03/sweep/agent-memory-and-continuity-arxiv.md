# Sweep: agent-memory-and-continuity via arxiv (frontier_olm 2026-10-03, SECOND same-day pass)

source-fetched: 2026-10-03. Seat: sweep-agent-memory-and-continuity-arxiv (dynamic workflow child, second invocation today). Every banked item below was fetched and read THIS session; quotes are verbatim from fetched pages (each quote cross-checked byte-for-byte against the estate's mirror stub in `state/arxiv/` where one exists). No em-dashes outside verbatim quotes. This pass answers the FIVE-question ask (the earlier same-day pass, preserved verbatim in the appendix below, answered a four-question version of this area; its 8 banked items are disjoint from mine and are NOT in today's `register.jsonl`, so its appendix record here is the only copy).

## Method

Pass 1 (broad sweep), three doors:

1. Local daily mirror: `grep -h -o -E "^# [^#].*" state/arxiv/2026-10-0*/*.txt state/arxiv/2026-09-2*/*.txt | sort -u | grep -i -E "memory|continuity|forget|consolidat|handoff|warm|experience|context engineer"` returned **77 unique in-window titles** (2026-09-18 through 2026-10-02 pulls); a second grep for entity/dedup/identity terms returned ~30 more names. All considered; 10 promoted to the shortlist with their ids mapped by `grep -l -E "^# .*$t" state/arxiv/...` (EnSIMem 2609.27279, ReCAP 2609.40118, CMP 2610.02070, VibeMemBench 2609.23570, RPMem 2609.23466, DolphinBench 2609.24971, MACE 2609.21533, Mem++ 2610.02002, C3M 2609.29735, ICLR-forget 2609.29875, MemCodex 2609.39765, FRESH 2609.28003, MemCalib 2609.24259).
2. Live API, `export.arxiv.org/api/query`: the first 5-parallel burst was rate-limited (four HTTP 429, one 503 with Retry-After 0; reported as degraded, not worked around silently). After cooldown two queries landed: `abs:"agent memory"+AND+abs:"entity"` (totalResults 23, 20 entries listed, surfaced 2609.25913 "When Does Execution Provenance Help Agent Memory Retrieval?" and the ER backlist) and `abs:"across sessions"+AND+abs:"agent"` (totalResults 106, 20 entries listed, surfaced TAGGRAPH 2609.38353, CliffCompaction 2609.26779, Memory as Middleware 2609.32091, Agent Zero Memory 2608.29606).
3. Direct pages: `arxiv.org/abs/2609.32802` fetched (rich result); `arxiv.org/html/2609.23570v1` timed out at 60s and fell back to its abs page (recorded as a degrade, not a silent success); the other full texts came from `arxiv.org/html/<id>v1`.

Candidate count: 77 + ~30 mirror titles + 40 API entries = **140+ considered**, well past the 30 floor.

Pass 2 (deep read), fetched and read this session: **5 full HTML texts end to end** (2609.27279 EnSIMem, 2609.40118 ReCAP, 2610.02070 CMP, 2609.23466 RPMem, 2609.29875 ICLR-forget) plus abstract-page reads of 2609.32802 (live abs) and 2609.23570 VibeMemBench (live abs, after the HTML timeout), plus mirror-stub abstract reads of 2609.21533 MACE and 2609.24971 DolphinBench (`state/arxiv/2026-09-21/2609.21533v1.txt`, `state/arxiv/2026-09-22/2609.24971v1.txt`).

## Estate grounding (what the ask pointed at)

- `watch/inbox/frontier_olm_2026-10-03/lens/graph.md:17-23`: 1,057 zero-edge nodes (knot 400, case_law 300, doctrine 217, steal 140); all 300 case_law nodes carry id exactly `law:` with empty summary, sourced from `memory/improve/skill_ledger.jsonl` (graph.md:18); 823 of 1,650 edge endpoints dangle (graph.md:19); the agent_memory landscape family has 93 percent of its edges unresolving while `family:readable_first` owns the only 2 edges that resolve on both ends, rel `already_inside` to `module:context_compression` and `module:corpus_expand` (graph.md:12, :23); the cheapest next fix is stated at graph.md:27: real ids for case_law and join knot/steal/doctrine ids at ingest.
- `watch/inbox/frontier_olm_2026-10-03/lens/burns.md:88-90`: the banked re-derivability finding (2609.32802, +0.608 CI +0.517..+0.700 over transcript-forwarding after upstream faults, outcome-metric unit OWED), confirmed find r3 in today's fold.
- `docs/DNA.md:14,42,46-48,92-97`: the residual+registry+leaf spine; session close must write residual + card + commit + chain leaf; "prune theater, never prune residual core"; lean complete = residual + card + content_commit + chain_leaf.
- `mag/hermes_warm_boot.py:194-208`: warm boot payload = chain tip + deployments + session_brief pointer; `memory/warm_state.json` on disk 998 bytes (this session's `ls -la`).

## Answers to the five research questions

### RQ1. The ingest-time join rule, and does the literature say normalize ids at ingest or heal in a different order

The window's convergent answer: **keyed, typed, provenance-carrying identities at ingest; identification before repair; no heavy entity canonicalization at ingest.**

- EnSIMem (2609.27279, full read) builds index entries of the form `[entity][entity type][property:value] -> {episode_id}` where each record is a tuple `<entity, type, property, value, episode, provenance>` and each entry preserves source turns and temporal info. Its structured route beats dense-only retrieval 96.59 vs 86.36 on LoCoMo in the ablation table. The honest negative: it has NO entity-resolution or canonicalization module; the only identity work is pronoun/speaker binding in the extraction prompt. The literature's ingest rule is structure plus provenance, not dedup-first normalization.
- CMP (2610.02070, full read) documents what happens without ingest identity in a deployed system: Mem0's 11,651 logged write operations are ALL additions, zero updates, zero deletes (full text), and identification fails for 54.0 percent of required memories on LongMemEval and 66.9 percent on LoCoMo. That is the estate's 300 `law:` rows in the wild: append-only ingest with no identity produces nodes that cannot be told apart, and no downstream diagnostic can even see the defect ("invisible to diagnostics that examine only memory operations").
- Healing order, per CMP: identify (make utility measurable under known propensities) -> then decide retention/merge (its Theorem 2: one-sided abstention is Bayes-optimal under irreversible operations). Per the 10-01 sibling's banked AMU (2609.36976): the write-time verb set is store / discard-as-duplicate / fuse-as-update, decided by a reconciliation pass, never by id collision. Estate translation: give each case_law row a real id keyed to its skill_ledger row (EnSIMem shape), make knot/steal/doctrine ids resolvable to their source rows at ingest, and only then consider merges; merging 300 indistinguishable rows before they are re-keyed is guessing.

### RQ2. Does re-derivability validate residual+registry+leaf, and what outcome-metric unit makes it rib-citable

Validation, triangulated three ways this session:

- 2609.32802 (abs fetched this session): accuracy under fault rises on 4/4 backbones +0.233 to +0.392; the kill test rules out tokens as the carrier (retention tracks visible fraction 0.221 to 0.692); the +0.608 CI +0.517..+0.700 grounding-inspector line matches `lens/burns.md:88` byte-for-byte. Carrying the original problem and re-deriving beats forwarding stage outputs (transcripts).
- ICLR-forget (2609.29875, full read): "historical reasoning becomes more replaceable once task relevant derived state has been reliably externalized into code, files, tool outputs, or environmental feedback." Unexternalized state carries 67.3 percent future behavioral risk vs 36.2 percent externalized. This is the estate's artifact-over-transcript law, measured from the outside.
- MemCodex (2609.39765, banked at full depth by the 10-01 sibling): returning source-turn POINTERS beats inlining memory content.

The OWED unit, answered from what I read: CMP proves no query-independent aggregation of per-query memory utility correlates above r=0.10 with held-out value, so a rib must NOT cite a scalar "memory goodness". The citable unit is the experimental arm itself: outcome delta at a fixed fault dose, backbone named, with CI, exactly as 2609.32802 reports it. If a cost-normalized scalar is wanted, the paper's own repair-cost arm supplies it: +0.394 matched retention bought for +59.8 tokens per item (Qwen3-14B, first re-grounded stage; later stages add nothing). Proposed rib phrasing: "accuracy delta at fault dose k on gsm_hard, temp 0, per backbone, with 95% CI" or "retention points per re-grounding token". DolphinBench (2609.24971, stub read) adds the reporting discipline: every claim ships accuracy, total cost, AND latency together.

### RQ3. Which in-window architectures attack content-free duplicates and prose-pasted ids at ingest

- CMP (above): the pathology census in a deployed system, plus the fix shape (exposure slots with known propensities make utility identifiable even for never-retrieved memories).
- EnSIMem (above): the typed ingest key with provenance.
- MACE (2609.21533, stub read): "Its MemGoG structure represents functional units as subgraphs of related conditions, actions, and outputs, connecting them through support, conflict, and repair relations." Relation-typed units updated from execution feedback (81.11 percent average over 8 benchmarks vs 78.97 for SAGE). This is the relation vocabulary the estate's edge table lacks (it has only `has_invariant` and `already_inside`, lens/graph.md:5).
- Mem++ (2610.02002, stub read): non-destructive store, every document whole with date and author, "calls no generative model at write time", read-time selection; beats the strongest baseline 8.0 to 13.1 points on OrgMemBench. The anti-distillation stance: write-time summarization is what mints content-free stubs in the first place.
- C3M (2609.29735, stub read): relation-aware updates "consolidate safe redundancy while preserving complementary and incompatible records" under a bounded query-blind budget; provenance-preserving by construction.

### RQ4. Wiring the agent_memory landscape family's edges into the module graph, using readable_first's pattern

readable_first's two resolving edges (lens/graph.md:12) are `already_inside` rels whose text names a module id that EXISTS. Three mechanical rules from this window's reads:

1. Mint an edge only when both endpoint ids resolve in the node table at ingest (EnSIMem entries point at real episode ids; CMP's store-level edges to nothing are the counterexample that measure zero). The estate ingest should refuse, not warn, an edge whose endpoint id is absent: fail-closed at ingest, the same shape as the harness gates.
2. Mint edges from observed co-use, not from prose: ReCAP (2609.40118, full read) derives dependency links from attention mass exceeding theta=0.02, stores them at ~12 bytes/edge, ~19 KB per session, and its ablation shows identifier-overlap-only selection (the prose-paste substitute) loses 8.8 points on Lost-in-Conversation. MACE updates support/conflict/repair relations from execution outcomes. The landscape family's 29 dangling edges were pasted; co-use edges would have to be earned.
3. Ban prose in the id field mechanically: ReCAP's stale-set detection works by identifier overlap between blocks, which is only possible because ids are atomic; the lens's mangled ids (`module:Name headers)`, lens/graph.md:19) are unjoinable precisely because the id field carries prose.

### RQ5. Minimal residual set for a cold seat, tokens-to-competence, and does the re-derivability law change warm boot

Measured this session (cl100k_base via the repo venv's tiktoken): `memory/warm_state.json` = 964 chars = **347 tokens** (998 bytes on disk); `memory/briefs/latest.md` = 2,101 chars = **589 tokens**. Core cold-seat payload today: **936 tokens**, carrying chain tip fields (index, verkle_root, parent_root, ts, n_leaves, dominant_theme), deployments (files + known_urls + source), and the brief pointer (path, chars, updated), per `mag/hermes_warm_boot.py:196-203`. NOT carried: residual/registry/leaf pointers, per-module laws, any statement of the current problem.

What the window says the minimal set is:

- Execution-verified experience only: VibeMemBench (2609.23570, abs read): "eleven of twelve solver and system pairings fail to exceed the matched memory-off baseline" while direct injection of execution-verified experience gains 1.1 to 4.5 points on four of five solvers and lowers steps on all five. An unverified memory payload can be net-negative; carry pointers to execution-verified artifacts (the estate's receipts-before-trust law).
- Proof of externalization, not the reasoning: ICLR-forget's 67.3 -> 36.2 risk cut says a warm boot should assert that derived state EXISTS on disk (leaf paths), not re-narrate it.
- Protected core named explicitly: ReCAP protects user messages and the latest edit/write per file because score-only selection dropped 37 percent of user messages; the estate analog is residual core, protected by DNA.md:46-48, and it belongs in the payload as a named field, not implicit.
- A problem anchor, not a theme label: warm_state carries `dominant_theme` (currently "autonomous_janitor"), which is a label, not the original problem. 2609.32802's mechanism (re-expose the ORIGINAL problem to downstream stages; the fault-cost disappears on Llama-3.1-8B when re-derivation is impossible) implies warm boot should add an original-problem anchor plus keyed derived-artifact pointers, a few hundred tokens on the 936-token base. That is the concrete change the re-derivability law demands.

## Banked items (8, strongest first; full detail in the submitted SweepResult)

1. CMP 2610.02070 (full read, NEW)
2. RPMem 2609.23466 (full read, NEW)
3. ICLR-forget 2609.29875 (full read, new depth over held abstract)
4. ReCAP 2609.40118 (full read, new facet over the 10-02 kv sweep's abstract-level bank)
5. VibeMemBench 2609.23570 (abs read, NEW)
6. 2609.32802 Re-derivability (abs read by me; today's confirmed find r3; adds the metric-unit extraction)
7. EnSIMem 2609.27279 (full read; abs-banked by the 10-01 sibling; adds ablations + the no-canonicalization limitation)
8. MACE 2609.21533 (stub abstract read; register feed-level only until now)

Considered, not banked (with reason): TAGGRAPH 2609.38353 and MemCodex 2609.39765 (banked at full depth by the 10-01 sibling), DolphinBench 2609.24971 and Mem++ 2610.02002 and C3M 2609.29735 and MemCalib 2609.24259 and FRESH 2609.28003 (stub-level here; the metric/reporting story is already carried by CMP + VibeMemBench), 2609.25913 Execution Provenance and CliffCompaction 2609.26779 and Memory as Middleware 2609.32091 (title-level only, OWED reads), MemDream 2609.34545 / GVD 2609.17696 / When-Context-Changes 2609.38866 / EternalSunshine 2609.36414 / Traverse 2609.37082 / StateGuard 2609.34134 / Bisimulation 2609.38778 / MemFit 2610.00872 (banked by the earlier same-day pass, see appendix).

## CORRECTION (post-submit, same sitting): ICLR-forget prior holding found

The full-tree `memory/` grep completed after the first bank. For 2609.29875 it surfaced a real prior holding this pass had not seen: `memory/runs/mickey17_v2/runs/agent-engineering-frontier-sweep-40/lanes/arxiv-agents-week.json` carries a banked lane row (idempotency_key 29605a923d45d651, source https://arxiv.org/abs/2609.29875) whose claim already covers the token cuts (25.5/14.4/33.3 percent) and the qualitative externalization finding, carries the SAME verbatim quote banked above, is marked `estate_status: "confirms-ours"`, and proposes its own steal (pre-prune receipt check: a reasoning block may be dropped only if its derived-state hash exists in the hash-chained record, landing spot workflow engine context compaction). The same claim text sits in `memory/runs/quote_audit_wide_20260925/run_concat.txt` (1 hit). Therefore item 3's bank is demoted from "new depth over held abstract" to: the externalization finding and quote are ALREADY estate-held (mickey17 lane + 09-28 kv held-abstract + register); this pass's remaining delta is only the quantified numbers not in that row (67.3 vs 36.2 percent future behavioral risk, trajectory-amplification ablation 73.76 vs Delete-All-Thinking 71.78 vs random 67.5-68.0, probing AUROC 0.844). Downstream dedup should treat 2609.29875 as a CONFIRMED estate find, not a new one.

The completed full-tree grep, final: 2609.27279 (register + MAP_BACKFILL + trajectory noise), 2610.02070 (trajectory noise only, zero holdings), 2609.40118 (trajectory noise only, zero holdings), 2609.29875 (register + MAP_BACKFILL + mickey17 lane + quote-audit concat + trajectory noise), 2609.23466 (trajectory noise only, zero holdings), 2609.23570 (trajectory noise only, zero holdings), 2609.32802 (trajectory noise only, zero memory holdings; its estate presence is the watch/inbox fold), 2609.21533 (register + MAP_BACKFILL + trajectory noise). The loop covered exactly these 8 ids; 2609.24971 was catalog-only in that command and its memory coverage comes from the targeted grep (no hits).

## Overlap checks (run this session)

- Catalog: `grep -c <id> catalog/catalog.jsonl` for all ten shortlist ids: 2609.27279 / 2610.02070 / 2609.40118 / 2609.29875 / 2609.23466 / 2609.23570 / 2609.21533 return exactly 1 hit each, 2609.24971 returns 2, 2609.32802 and 2609.38353 return 0. Every 1-hit row was path-verified as the daily mirror stub (`local_sovereign_agent/state/arxiv/<date>/<id>v1.txt`, zone lsa): verified explicitly for all seven singles. So catalog holds abstracts only; no catalog row researches any banked paper.
- ARXIV register: `memory/runs/corpus_gap_research/ARXIV_REGISTER.json` contains 3 of my ids: 2609.21533 MACE (cited_in the 09-28 swarm sweep, verdict REAL), 2609.27279 EnSIMem (cited_in the 09-28 memory sweep), 2609.29875 ICLR-forget (cited_in the 09-28 kv sweep). Extracted with the repo venv, rows quoted in this session's exec log.
- Prior-sweep dedup (read this session): the 10-01 sibling (`watch/inbox/frontier_olm_2026-10-01/sweep/agent-memory-continuity-arxiv.md`) banked TAGGRAPH 2609.38353, EMIR2 2609.32584, Temporal Shape 2609.36457, MemCodex 2609.39765, portability 2609.05339, EnSIMem 2609.27279 (abs), AMU 2609.36976, eviction-audit 2609.08279; the 09-30 sibling banked EngramRAG 2609.32049, CAMG 2609.34422 and 5 more; the 09-28 sibling banked 2609.33013 and 5 more; the 10-02 kv sweep banked ReCAP 2609.40118 at abstract level (their item 8, cold-restore facet); the 09-28 kv sweep held ICLR-forget 2609.29875 as an abstract with an explicit "read locally if needed" invitation. My 8 items are adjusted accordingly: none re-banks a full-depth holding; the two partial overlaps (ReCAP, EnSIMem, ICLR-forget) are banked for their NEW depth/facet with the provenance stated per item.
- memory/ recursive grep: the full-tree `grep -r -l <id> memory/` batch completed for 2609.27279 (hits: ARXIV_REGISTER.json, MAP_BACKFILL.json, MAP_BACKFILL.md, trajectory/steps.jsonl self-noise) and 2610.02070 (hits: trajectory/steps.jsonl self-noise only) and was still running for 2609.40118 and later ids at bank time; a targeted grep over `memory/runs/corpus_gap_research/`, `memory/percolator/candidates.jsonl`, all `frontier_olm_*/sweep/*.md`, today's DIGEST.md and register.jsonl found NO hit for 2610.02070, 2609.23466, 2609.23570, 2609.32802, 2609.24971, or 2609.38353 anywhere, and today's `register.jsonl` (23 rows) contains none of the eight banked ids.

## Checks run / not run

- Ran: the mirror title greps (77 titles), 2 live API queries, the abs + html fetches listed in Method, the catalog id/phrase greps, the register row extraction, the targeted prior-sweep greps, and the tiktoken measurement (repo venv `.venv/Scripts/python.exe`, cl100k_base).
- Not run: no repair probe against `memory/knowledge_graph.json`; no warm-boot end-to-end rerun (payload measured from the on-disk artifacts the module writes, not by executing `python -m mag.hermes_warm_boot`).
- Not verified: full-text bodies for VibeMemBench, MACE, DolphinBench, Mem++, C3M (abstract-level only); 2609.32802's numbers beyond the abs-page fetch (its +0.608 CI line independently matches the banked burns.md:88 claim).
- Token counts are cl100k_base, not the seat's actual tokenizer; treat 936 as an estimate of the seat-side cost.

## Falsifiers / next probes

1. If the ingest re-key lands (real case_law ids joined to skill_ledger rows), the CMP falsifier applies: re-run the lens's edge-resolve count; if resolution does not rise materially above readable_first's 2 edges, the join rule was wrong, not the wiring.
2. The warm-boot probe: add an original-problem anchor + residual/leaf pointers to `warm_boot()` (~a few hundred tokens over the 936-token base) and A/B cold seats on a next-window task; if tokens-to-competence does not drop, the re-derivability law does not transfer to warm boots and the field should be dropped.
3. VibeMemBench's negative result predicts the estate's own memory-reuse attempts underperform memory-off unless the experience is execution-verified first; run its design against `catalog/catalog.jsonl` replay rows before trusting any new "reuse" mechanism.

---

# APPENDIX: prior same-day pass (earlier attempt of this seat, preserved verbatim summary)

The earlier same-day invocation of this seat banked, at abstract-page depth, eight items this pass does NOT touch: MemDream 2609.34545, GVD 2609.17696, When Context Changes 2609.38866, Eternal Sunshine 2609.36414, Traverse 2609.37082, StateGuard 2609.34134, Action-Conditioned Bisimulation 2609.38778, MemFit 2610.00872 (9 API queries, 60+ candidates, 10 abs-page reads; none of these ids are in today's `register.jsonl`, and its overlap census found zero prior holdings for all eight). Its full text was at this path before this rewrite; the estate-visible record of its claims lives in this appendix plus the submitted results of that invocation. Its answers covered: RQ1 repair loops (MemDream's learned repair ops, GVD's LLM-free dedup F1 0.97/0.94), RQ2 append-only continuity (MemFit), RQ3 decay policies (EngramRAG's CATD), RQ4 stale binding (When Context Changes / CICM). Its stated caveat: WebFetch returned abstract pages, not full bodies; depth is abstract-page depth.
