# FRONTIER SWEEP: agent-memory-continuity via X - 2026-10-10

source-fetched: adhoc. Seat: sweep-agent-memory-continuity-x (workflow child). Two passes run as ordered: Pass 1 considered 40+ candidates (15+ inside the 30-day window 2026-09-10..10-10); Pass 2 deep-read 9 items end to end (birkin-mnemosyne README, 28naem-del/mnemosyne README, cognee eval page, AML repo, claude-code #98483, claude-code #89733, mem0 DolphinBench post, Kevin Liao essay, Memento arXiv 2508.16153 abstract via curl) plus 5 X posts resolved whole through the fxtwitter JSON door.

## Door log (honest)

- site:x.com WebSearch: hit 1302 rate limits repeatedly (5+ consecutive 429s twice); between decays it returned usable crops. fxtwitter door https://api.fxtwitter.com/<user>/status/<id> worked clean on every direct resolve (routemap, pachaar, pauliusztin, yohei, witcheer, memfactory, AgentMemoryL x2); raw JSON saved under watch/inbox/frontier_olm_adhoc/sweep/_fx/.
- X articles (tricalt "How I Run 47 AI Agents on One Brain", yoheinakajima "State of AI memory systems"): fxtwitter returns empty text with article media; our tools cannot open X articles (same class as memory/runs/gapwave/agent_memory_challenge_2026.md S4 UNFETCHABLE). Snippet-banked in Pass 1 only, NOT deep-read, NOT in the final 8.
- agentmemoryleaderboard.ai/evaluation returned HTTP 522 (origin down, Retry-After 120). OWED: live Cycle-2 standings; the AML GitHub repo was read instead and then dropped as a dupe of our own holdings.

## Estate ground truth this sweep feeds (verified here by running it)

memory/knowledge_graph.json: 2,938 nodes / 1,256 edges; isolated-by-degree 1,066 (steal 122, knot 379, module 374, doctrine 190); edge rels: has_invariant 815, maps_to 300, why_context 117, already_inside 18, superseded_by 6 (python over the JSON, this session). The why/evidence layer is the thin one. Route-map claim held locally at watch/inbox/night_cools_20261010/NIGHT_COOLS_INDEX.md:11 and :22 (45,128 -> 1,781 tokens, "25x"). gala holdings for the four named systems: watch/inbox/gala_20260925/rung/lanes/mcp-memory-servers.check.txt (README-level only).

## RQ answers (cited)

**RQ1 (evidence linking vs name-only nodes).** Three convergent patterns from independent authors: (a) Liao's essay: snippet-vector stores are unauditable, similarity search cannot tell you which snippet is "correct, current, or what's missing"; the fix is documents with a discovery catalog (https://liao.gg/blog/agents-dont-need-memory). (b) 28naem-del/mnemosyne: every memory record carries source uri, trust, dependencies, status; "a corrected requirement can retire a dependent procedure" (https://github.com/28naem-del/mnemosyne). That is precisely a why-edge with invalidation semantics, the thing our 122 isolated steals lack. (c) cognee: "hybrid graph-plus-chunk retrieval" scored 0.79 vs Mem0 0.49/0.63 on BEAM, "a long-horizon memory benchmark where relevant evidence is scattered across many turns" (https://www.cognee.ai/research-and-evaluation-results). Common thread: link the claim to its evidence chunk at write time; never mint free-floating nodes.

**RQ2 (rivals/conditions for the 25x boot cut).** The claim's own fine print (read tonight in the repo): synthetic fictional large-note corpus, o200k_base tokenizer, no model named, exact lexical triggers only, "small-note task costs can increase", full INDEX re-read after compaction (https://github.com/ashmoonori-afk/birkin-mnemosyne). Independent boundary measurement: claude-code #98483, 481,186-byte CLAUDE.md = about 120k tokens; gotchas were 54% of file; "the memory file is itself the dominant cause of the compaction it then has to survive"; roughly 68% cut possible via symptom-named index lines because entry size and firing-risk are inversely correlated (https://github.com/anthropics/claude-code/issues/98483). So: the 25x holds when payload mass sits in rarely-firing large entries (cold start, big corpus, exact triggers); it shrinks toward parity on small notes or semantically-triggered needs, and DolphinBench shows the cue-free case is the real test ("We avoid cues that announce a stored preference").

**RQ3 (in-context vs weight updates).** The 2025 anchor read tonight: Memento formalizes Memory-augmented MDPs; "low-cost continual adaptation via memory-based online reinforcement learning" beats training-based SOTA on DeepResearcher while leaving LLM weights frozen (arXiv 2508.16153, submitted 2025-08-22). Everything 2026 I read (DolphinBench, Liao, AML) competes on the context/memory side; the weights-side continuation is RL-training the memory manager (MemFactory, GRPO, claims 14.8% relative gains over Memory-R1/RMM/MemAgent baselines; Apr 2026 post, out of window, not deep-read). No 2026 in-window paper comparing the two tiers directly surfaced; that stays OPEN for the living-weights rib.

**RQ4 (compaction preserving evicted facts).** Darkest evidence: claude-code #89733, 163-session audit: "Violations cluster right after context compaction"; compaction preserves narrative while losing governing constraints; only a mechanical repo test held; commenter law "Findable != obeyed"; remedy shape: rules as closeable records current/superseded/rejected with citations (https://github.com/anthropics/claude-code/issues/89733), isomorphic to our superseded_by rel + citation lint. Compatible recipe for the 7-day standing wave: keep procedural rules as failing-tests/hooks (mechanical), flush durable facts to linked records BEFORE eviction (zeroclaw issue class), and keep recipes in a resident index while mass goes to on-demand docs (98483 admission-by-firing-time, 3-miss promotion counter).

## Banked items (8, strongest first; full JSON in the SweepResult)

1. Liao essay (Oct 3): RQ1/RQ2/RQ4 convergence; NEW (no overlap: rg "agents-dont-need-memory|Operator Memory|liao\.gg" empty in catalog+memory).
2. claude-code #98483 (Sep 30): 25x boundary conditions measured; NEW (98483 hits were coincidental SQL/tsx files).
3. claude-code #89733 (Aug 26, OUT OF WINDOW, flagged): compaction vs governance; NEW (89733 hits coincidental).
4. 28naem-del/mnemosyne (pushed Sep 22): evidence-linked records with invalidation; NEW (rg "28naem" empty).
5. mem0 DolphinBench (Sep 22): cue-free eval, cost+latency Pareto; PARTIAL dupe: arXiv abstracts 2609.24971 v1/v2 already in catalog (state/arxiv/2026-09-22, 1,321 bytes); delta banked = full results + verification gate.
6. birkin-mnemosyne repo v0.6.0 (Oct 10): honest conditions of OUR night-cools claim; post already banked in night_cools_20261010, repo writeup is the delta.
7. cognee BEAM eval numbers: graph+chunk evidence retrieval; overlap: cognee READMEs held under gala lanes (readme-level), benchmark numbers are the delta.
8. Memento arXiv 2508.16153 (2025-08-22, OUT OF WINDOW, flagged): RQ3 anchor; NEW (rg for title empty).

## Dropped as dupes (waste avoided)

- Agent Memory Challenge Cycle 2 / AML repo: our own memory/runs/gapwave/agent_memory_challenge_2026.md (Sep 20, 18KB, first-hand fetch log) already covers Add/Search, tracks, competency model, CSIG.
- Mem0 Dream: watch/inbox/frontier_olm_2026-10-05/sweep/_raw/mem0_dream.txt (banked Oct 5).

## OWED

- Live Cycle-2 standings (522 door). X-article content (tricalt/yohei). In-window direct context-vs-weights comparison paper for RQ3: none found; flag stands.
