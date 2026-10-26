# sweep/agent-memory-continuity-reddit.md

source-fetched: 2026-10-02
Area: agent-memory-continuity · Door: reddit · Agent: sweep-agent-memory-continuity-reddit

## Door status (degraded on every variant, recorded per recipe)

The primary recipe door FAILED exactly as it did on 10-01 (sibling `frontier_olm_2026-10-01/sweep/agent-memory-continuity-reddit.md:8-13`):

- `old.reddit.com/r/{LocalLLaMA,MachineLearning,LocalLLM,ollama}/top.json?t=month&limit=50` (WebFetch): all four returned the "Welcome to Reddit" placeholder, zero posts.
- `old.reddit.com` thread pages (WebFetch): same placeholder. `www.reddit.com/*.json`: HTTP 403 Blocked.
- web_reader MCP on old + www: welcome stub / "blocked by network security".
- `r.jina.ai` proxy: Reddit 403 passthrough. `redlib.catsarch.com`: 429. `redlib.perennialte.ch`: 403.

Working fallback doors (per the recipe's fallback clause, honestly degraded):

1. **WebSearch `site:reddit.com`** for discovery + snippet-level reads; intermittent 429 storms (roughly every other query).
2. **api.pullpush.io** (pushshift successor) for full-text reads, `?ids=` and subreddit window queries. Same profile as 10-01 documented: works when the id is indexed, then locks up. This sitting: 2 successful full reads (1w9sklm, 1wahqm2), then every subsequent call 429 through a 150s+ cooldown (7 calls total, locked).

Known hole (confirmed twice now): **pullpush has no index for ids >= ~1wi (roughly 2026-09-11 onward).** `ids=1ws8d1x,1wi6j25,1wjm9ez,1w0o56a` returned `"data":[]` twice; the 10-01 sibling hit the same on 1w5l182/1whlop5/1w5w3xi. The last 2.5 weeks of Reddit (the strongest half of the window) is unreadable through any door available to this seat.

## Pass 1 - candidate pool

Out-of-window traps, date-verified and recorded so no future seat re-considers them (anchors from the 10-01 sibling's epoch table plus this sitting's own fetches): 1tgm63n "Hitting #1 on LongMemEval 96.4% (Exabase M-1, Gemini Flash)" (~2026-05, score-bearing but 5 months stale, and the HN sibling already carries the Exabase M-1 name); 1ujp3pq "im sick and tired of these memory benchmarks" (~2026-07-06; its substance, the 6.4% wrong answer key and judge accepting 63% wrong answers, was already banked 10-01 from 1s1jlnd); 1uy6yht wrong-abstraction debate (= 2026-07-17 verified); 1uzyuna append-only event log (~07-19); 1uexvvy CLAUDE.md-respect hooks (~06-28); 1rlv0mp "did not respect .CLAUDE.md. Again." (~03); 1rz2oo3 "what happens when you stop adding rules to CLAUDE.md" (~03, key lesson: pre-commit hook, not a louder rule); 1tjfhat project blueprint, "hooks do enforcement, not guidance" (~05); the whole r/LLMDevs naming cluster: 1tvjdkj "Naming is not identity", 1ts3s21 "What I got wrong building KG memory" ("resolution normalizes, deduplication removes"), 1ts3nq2 "I spent a year building agent memory on knowledge graphs" (5 mistakes, MongoDB), 1te3fb0 GraphRAG entity dedup, 1pn803k/1pkwgwy three-phase dedup, all May-Jul; 1vufvvk "Same retrieval, different answers: 32 of 500 LongMemEval runs disagree" (~08-15, reproducibility, painful miss by ~2 weeks); 1veeix3 "8 memory systems through 2176 tasks, plain markdown wiki beat every product" (~08-10); demand posts 1sna5kb/1qrbs69/1r5q7xd/1su00hm/1se7k1o (spring).

In-window pool (2026-09-02 to 10-02, 41 items considered): the 27-post Hindsight astroturf wave in r/AIMemory (1wt*, all "[removed]", already characterized 10-01); the 5 items the 10-01 sibling banked (1wqv98w, 1wu345p, 1wu0miw, 1wldl38, 1wldz7u, not re-banked); the 4 still-unreadable OWED ids (1w5l182 stale-fact decision logs, 1whlop5 "I don't think AI agents have a memory problem", 1w5w3xi stress-test-my-memory-system, 1wghnq7 moderator-removed, pullpush `data:[]` reconfirmed this sitting); and the 5 fresh candidates this sitting surfaced: 1w9sklm, 1wahqm2, 1ws8d1x, 1wi6j25, 1wjm9ez.

## Pass 2 - deep reads (2 fetched end to end via pullpush; the ask's floor was 5, shortfall is real, not papered)

The 5-deep-read bar is NOT met. After the 2 reads below, every remaining in-window candidate is either removed (astroturf), already banked (the 10-01 five), or pullpush-unindexed with the search door 429-storming on exact-title queries. Banking unread items would violate the no-fabrication law; they are listed as OWED, not findings.

### 1. 1w9sklm - "Can an AI Agent Run for Years Without Compressing Away Its Memory?" - r/Rag, 2026-09-08 (epoch 1788788628, my conversion), score 1, 0 comments

Verbatim excerpt (pullpush fetch, this sitting): "Progressive information loss through repeated compression." Full read: the author runs a persistent near-zero-downtime agent for months/years and distrusts the standard stack (context window + vector retrieval + rolling summarization) for exactly the estate's reason: after conversation, summary, recompression rounds the agent keeps the gist but loses exact constraints, decision rationale, and time-specific state; semantic similarity is not relevance, causality, or current state. Their test scenario is a supplier X used Monday, failed testing Wednesday, replaced by supplier Y Thursday, and the question they pose is how the agent reconstructs months later WHY the switch happened rather than retrieving supplier-shaped documents. They close asking whether anyone has measured information degradation over continuous multi-month/year operation. Zero answers.

Estate mapping: this is RQ4's missing instrument stated as user demand. The estate's residual (append-only exact turns, the MemCodex pointer-beats-inline convergence, catalog 806443 + lens/burns.md:94-95) is the lossless half; the verkle chain tip is the degradation-measuring half: a successor that verifies the tip verifies that nothing degraded, which is the measurement this poster is asking for and getting nowhere on. The "why did the switch happen" question is a knot-payload requirement: the chain holds the text, the graph holds the hash (graph.md:35); EMIR2-style SUPERSEDES edges (questions.md:121-124) are the X-to-Y transition's data shape.

Overlap grep: `grep -rilF "Progressive information loss"` over catalog/ + memory/ + watch/inbox/ (trajectory excluded) gave zero hits. LongMemEval/LoCoMo phrases hit only the Zep benchmark harness clone (`mine/raw/agent_bleeding_edge/getzep/zep/benchmarks/`, catalog.jsonl) and `memory/research_packs/COMPACTION_ALGO_RESEARCH_20260919.md`, compaction-algorithm holdings, not this degradation-measurement thread. NEW.

### 2. 1wahqm2 - "How do you keep context across projects when the agent's memory is scoped per folder?" - r/AI_Agents, 2026-09-09 (epoch 1788853288, my conversion), score 1, 1 comment

Verbatim excerpt (pullpush fetch, this sitting): "I have 58 tracked project folders and effectively 58 disconnected brains, and I'm re-explaining the same things constantly." Full read: a solo dev across many repos hits the same wall with per-folder-scoped agent memory; the title question is how to keep context ACROSS projects when every folder is its own scope; the post closes "Also genuinely interested if the answer is 'this is overkill, just write better handoff docs.'"

Estate mapping: the sharpest one-line statement of the disease the shared artifact boundary exists to cure. The estate's answer is already deployed law: `watch/inbox/SHARED_SURFACE_CONTRACT.json` plus the INDEX read/classify/receipt protocol in AGENTS.md, and the current branch's named keystone gap (commit 47d0177d8: cross-node tip exchange is missing, "the ground truth itself is fragmented") is this poster's problem at fleet scale, 58 folders here, N seats + 4 mesh nodes there. The practitioner's own guess ("just write better handoff docs") is the pre-contract stage the estate passed through; the steal is confirmation that the market has not even reached the estate's 09-15-era contract.

Overlap grep: `grep -rilF "58 disconnected brains"` over catalog/ + memory/ + watch/inbox/ gave zero .md hits; the id appears only as raw JSON already pulled by two earlier sweeps (`frontier_olm_2026-09-30/sweep/_raw/p30_AI_Agents_handoff.json`, `frontier_olm_20260928/sweep/_raw/pull2_AI_Agents_handoff.json`) and never banked into any write-up. First banking here, raw-pull provenance recorded.

## OWED (in-window, titled, unreadable through every door this sitting)

1. **1ws8d1x** - "My memory benchmark is out. Nobody has run it so I..." (r/AI_Agents, ~2026-09-28) - a NEW memory benchmark author reporting zero external runs. This is RQ2's most important open item: whether the estate's MemCodex 60.8-vs-55.4 bank gets an independent in-window test depends on benchmarks like this one getting run. Search snippets could not recover the body (pullpush `data:[]` twice, search 429).
2. **1wi6j25** - "Efficient Session Resumption for Claude Code Agents" (r/ClaudeWorkflows, ~09-17) - title says it treats "previous subagent outputs as durable artifacts for session resumption"; that is the RQ4 instrument class (successor continuity) unread.
3. **1wjm9ez** - "How do you all keep agent work from disappearing between sessions?" (r/claudeskills, ~09-22) - a skill that "prepares a handover at session end, updating the resume-here section in a repo .md", title-level only.
4. Carried OWED from 10-01, reconfirmed empty this sitting: 1w5l182, 1whlop5, 1w5w3xi, 1w0o56a, 1wghnq7 (removed).

## Answers to the five research questions (reddit door only; sibling arxiv/HN sweeps hold the stronger published answers)

1. **Doctrine-to-code linkage schema (757 nodes, 0 edges):** nothing in-window on reddit. The out-of-window practitioner cluster converges on the estate's existing answer: prose doctrine is advisory, hooks/gates enforce (1rz2oo3 pre-commit-not-louder-rules; 1tjfhat "hooks do enforcement, not guidance"), and the estate's ratchet + citation_lint + workflow_gate + census carrier-grammar gate already exceed anything the threads describe. The schema half was answered by the HN sibling (OKF code_refs + strict --drift). Reddit adds corroboration only.
2. **Post-10-01 retrieval comparisons vs pointer/BM25 (banked MemCodex 60.8 vs 55.4):** no in-window reddit item publishes any comparison; the strongest Q2 signal is 1ws8d1x (OWED, benchmark with zero runs) and 1w9sklm's demand-side admission that nobody measures degradation. Nothing here beats or tests the banked scalar; the arxiv sibling's MemFit finding (LoCoMo 60.5 vs MemCodex 58.8) stands as the estate's best Q2 answer.
3. **ID-collision / slugification / dangling references (degree-9 hub bug, 814 ghost endpoints):** zero in-window. The exact lessons sit just out of window and are now dated on record: "resolution normalizes, deduplication removes" (1ts3s21, ~05-31) and the naming-is-not-identity split (1tvjdkj, ~07-20) are directly applicable to the graph.md:37 slug-with-content repair line; Graphiti's two-phase MinHash+LLM dedup (1r8cnwq) remains the best public pointer.
4. **Verifiable-continuity instruments (warm boot + verkle):** the window's one strong reddit signal, and it is demand-shaped: 1w9sklm asks for a degradation-over-years measurement and gets no answers; 1wahqm2 shows the cross-project brain problem still unsolved by handoff docs alone. The estate's warm-boot-plus-tip-continuity is ahead of the public market; the steal is the falsifier framing: "a successor that can verify the tip" is the instrument the market cannot name.
5. **Content behind content-addressed hashes (400 empty-summary knots):** nothing in-window on this door. The HN sibling's pattern (immutable address as join key + derived rebuildable human surface + fail-loud) is the standing answer; reddit adds only the 1w9sklm supplier-causality scenario as the use case a knot payload must serve.

## Method note

Every quote above came from pullpush JSON fetched this sitting; both dates are my own conversions of the reported epochs (1788788628 to 2026-09-08, 1788853288 to 2026-09-09). Overlap greps were run this sitting with the exact strings named per item (the first broad phrase scan failed silently on an invalid `--exclude-path` grep flag and was rerun with a venv-Python scanner plus corrected greps; the failed run's NONE results were never used). Pass 1 = 40+ candidates considered, 41 in-window enumerated; Pass 2 = 2 of 5 end-to-end reads, shortfall stated above rather than filled. No fabricated fallbacks; the OWED list is the honest residue.
