# FRONTIER SWEEP: swarm-orchestration via reddit (2026-10-06)

source-fetched: 2026-10-06
Sweeper: sweep-swarm-orchestration-reddit (OLM day-6 frontier mine, sweep lane)
Area: swarm-orchestration via reddit. Estate map target: queue/lanes rotation, watch/inbox receipts, memory/rib_bus/doctrine.json, knot/doctrine/steal layers of memory/knowledge_graph.json.

## Doors, honestly

- old.reddit.com is LOGIN-WALLED as of today: `https://old.reddit.com/r/LocalLLaMA/top/?t=month` returns "Log in to use old Reddit" (fetched via mcp web_reader, no_cache). The recipe's primary door is dead for reads.
- reddit .json and .rss endpoints are hard-blocked: `https://www.reddit.com/r/LocalLLaMA/top/.rss?t=month` and `.../comments/<id>/.json` both return "You've been blocked by network security" (web_reader, no_cache).
- www.reddit.com HTML renders for web_reader but comment pages are JS shells for both fetchers (WebFetch on `/comments/1rrisqn/` returned only "Reddit").
- redlib mirrors: redlib.perennialte.ch 403, redlib.catsarch.com 429.
- pullpush.io works for single-id lookups but 429s on search queries (three retries across 10 minutes).
- WORKING DOOR used for all deep reads: `https://arctic-shift.photon-reddit.com/api/posts/ids?ids=...` and `/api/posts/search?subreddit=...&after=...&sort=...` (no auth). Caveats from its own API docs (github.com/ArthurHeitmann/arctic_shift, api/README.md): no uptime guarantees, scores/num_comments are placeholders (1 or 0) until ~36h after posting, and all content passed through a reader model, so quotes below are reader-copied verbatim from the JSON, not raw byte dumps.
- WebSearch degraded intermittently (HTTP 429 on several queries; retried). Search-engine dates proved unreliable (one "Sept 2026" thread was actually March 2026 by created_utc), so every banked item was date-checked through the arctic-shift API.

## Pass 1 (breadth)

40+ candidate posts considered across r/LocalLLaMA (five windows: newest-100 on Oct 6; Oct 1-2 full-page sample; Sep 30 page; Sep 21-22 page; plus search-found threads), r/ollama, r/LocalLLM, r/MachineLearning via search. Coverage caveat: arctic-shift cannot sort by score and `title=` keyword search 422s, so mid-month days (Sep 12-20, Sep 23-29) are only partially sampled (one page per window edge). Strongest-of-month cannot be claimed; strongest-of-what-was-sampled can.

## Pass 2 (deep reads, six threads end to end + two title-only)

### 1. r/LocalLLaMA 1wu3rio "Agent swarm coordination" (2026-09-30, score 4, 22 comments read all)
https://www.reddit.com/r/LocalLLaMA/comments/1wu3rio/ (fetched via arctic-shift /api/comments/search?link_id=1wu3rio)
The ask: "recommendations of tools for agent coordination and messaging to get them to collaborate on hard problems?" The comment section is a free field survey of lock/receipt contracts for exactly the estate's multi-seat write-seam wound:
- Atomic-rename claiming: "a shared markdown folder with YAML headers per task; claiming via rename (atomic on one filesystem), done/failed folders, timeout reassignment", with the cross-machine caveat that moves are "non-atomic across synced machines" (u/EnvironmentalLeg8506).
- Boring-protocol contract: "task queue with states plus an event log; leases/heartbeats, cloud model for planning/review, structured artifacts, and max-hop/dead-letter paths to avoid infinite loops" (u/Salt_Hyena5896).
- Pass artifacts not chat: two roles (local worker, cloud reviewer) exchanging "plans/diffs/logs rather than chat history", cap iterations, compare against a single-model baseline (u/No_Product_5759).
- Forgejo/Gitea as the coordination bus: Claude + Codex + a local model discuss/plan/implement/review through issues and PRs (u/TastesLikeOwlbear, and mirrored roles by u/CalligrapherFar7833: codex implements, claude reviews, after qwen 3.8).
- Sweep consensus, top comment at score 9: "An agent 'swarm' is just hype at this point. What you need is handful (at most) of carefully coordinated agents." (u/Last_Mastod0n). Killswitch/overwatch framing from u/geldonyetich (sorcerer's apprentice).
- One commenter compared "~100 agent harnesses" via a manager/workflow-graph pool (u/devoidfury).
Estate read: the general lock/receipt contract that ends the R3/stash/LIVE_REPORT seam class already exists in folk form: claim-by-atomic-rename + state folder + lease/heartbeat + event log + dead-letter, with the named defect that renames are only atomic within one filesystem (our stash and inbox live on the same NTFS volume, but WSL/docker views are the synced-machine case). This is the outside pattern to fold into the fold_gate serializer conversation, not a new mechanism to hand-roll.

### 2. r/LocalLLaMA 1wvmps7 MemTether, "23 AI coding agents sharing one SQLite file" (2026-10-02)
https://www.reddit.com/r/LocalLLaMA/comments/1wvmps7/ (fetched via arctic-shift /api/posts/ids)
Local-first memory hub: "a memory hub that works via file-level pointers (junction/symlink). No cloud, no API fees, no abstraction layer." 23 client adapters with auto-detection; per-write SOURCE ATTRIBUTION (which agent wrote each memory); bi-temporal tracking (what was true vs when the system learned it); Q-value use-ranking; FTS5 + local bge-m3 vectors; ships an MCP server. Stack Python/SQLite/ChromaDB/FastAPI.
Estate read: this is the wiring contract the knot/doctrine/steal layers lack: one shared store, every row carries writer identity and two clocks, retrieval is multi-strategy. Direct counter to the skills_pack monoculture failure (285/300 case laws on one module) because attribution makes cross-module edges first-class data. Zero comments at fetch, so unvetted; steal the contract shape, not the code.

### 3. r/LocalLLaMA 1wmkr01 "Gemma 4 E2B verbalized confidence 99.6% on {0.00, 1.00, 0.50}" (2026-09-21, 13 comments read all)
https://www.reddit.com/r/LocalLLaMA/comments/1wmkr01/ (fetched via arctic-shift posts/ids + comments/search)
Measured: "The judged pipeline scored 0.612 [0.562, 0.662]. The no-judge version ... scored 0.740 [0.688, 0.792]." Adding a small-model judge HURT by ~0.13 with overlapping-ish CIs, and the judge's verbalized confidences collapsed to 0.00/1.00/0.50 (99.6% of judgments). Comment-thread practice (all read): small classifiers should answer in natural-language reasons, not numbers ("The reason is 2 to 3 sentences justifying its decision", u/triynizzles1); "Have it write the feedback first, then true/false" (u/stoppableDissolution); "the score drives the cutoff and gets tracked against actual outcomes, the reason is the audit trail" (u/ShowerAnnual9741); distrust self-scores without a calibration set, and "the policy consuming the score is the bottleneck" when ranking improves but end-to-end drops (u/khiladi1729).
Estate read: direct measured evidence for the question-class split on the mesh boundary: a gemma-class judge is miscalibrated as a NUMBER source but usable as a REASON source feeding a typed oracle. Our holdings already carry the arXiv spine on this (catalog rows 36f7f48a72e9 "Rethinking Verbalized Confidence", aa972b654e1b "The Mirage of Calibrated Confidence", d31f7a13306e "Beyond Verbalized Confidence", plus memory/research_packs/THE50_W3_T11_TYPED_DECISION_ORACLES.md), but the -0.128 judged-vs-no-judge delta with CIs and the feedback-first ordering are new measured points from the field.

### 4. r/LocalLLaMA 1wz1rsy "Reduce thinking w/ zero quality loss ... 664 agent runs, up to 29% less thinking" (2026-10-06, 0 comments)
https://www.reddit.com/r/LocalLLaMA/comments/1wz1rsy/ (fetched via arctic-shift posts/ids)
9 thinking-discipline rules for AGENTS.md/CLAUDE.md/system prompts, tested across 4 models x 664 runs (same 9-challenge exam, with/without rules, 5 reps each, hidden check script). Report: zero task losses, up to 29% thinking reduction at equal results. The adversarial leg: a "tech lead" urging revert with no evidence; with the rules, models noted the fix was correct but still reverted; without them, "two runs wrongly wrote that claim into the project's AGENTS.md".
Estate read: (a) external corroboration for thinking-mode as the axis and for steering-under-unevidenced-pressure as the measurable failure; (b) a wild-type instance of our no-fabrication disease: a false claim written into a shared law file by an unsupervised run. The rules list is foldable as a candidate prompt-pack amendment; the revert-every-time result says nod-gates (operator approval) still beat model-side discipline, which supports the planning-mode gate promotion.

### 5. r/LocalLLaMA 1wmxx9w "Kev: tiny Jev-like decision models (0.8B/4B/9B)" (2026-09-22, score 23, 11 comments)
https://www.reddit.com/r/LocalLLaMA/comments/1wmxx9w/ (fetched via arctic-shift posts/ids)
Apache-2.0 judge family on Qwen3.5 with training code and frozen evals; the 9B fits a 32GB Mac in bf16; API-compatible with a commercial System One endpoint so an SDK can repoint at a local server unchanged. Verbatim: "The web playground is worth a look on its own, it shows how option order shifts the answers". The same window carries a whole decision-model wave: ARC-1 1.7B pick/score/yes-no at ~20ms (1wz14pv, Oct 6), NIRNAY 450M on CPU (1wv51nt, Oct 1), Clef by Cloudflare (1wv4zzi, Oct 1), Perplexity Decider 27B (1wvfz9n, Oct 1), stuntd multi-field heads (1wu8x61, Sep 30), Jeff-0.8B router at 38x faster decisions (1wv05u1, Oct 1), laya mention (1wm0cn0, Sep 22).
Estate read: the estate's day-5 mine dominant find ("decision models create a rung UNDER gemma:2b", NIGHT_CLOSE commit d5f89d97b) is independently confirmed by at least seven separate releases in 15 days. Our overlap: memory/continuity/seat_memory_20260927/jev-system-one-decision-model-20260916.md already tracks Jev; the new facts are (a) the wave's breadth (it is now a commodity, not a novelty) and (b) option-order bias as a live measurable in judge outputs, which belongs in our legality/verdict feed tests.

### 6. r/LocalLLaMA 1wu9wfm "I ran 4 agent harnesses on the same 2B model ... 0.017 vs 0.821" (2026-09-30, TITLE-ONLY: selftext [removed], 0 comments)
https://www.reddit.com/r/LocalLLaMA/comments/1wu9wfm/ (fetched via arctic-shift posts/ids)
The title is the entire remaining evidence: same 2B model, four harnesses, success 0.017 vs 0.821, "The model was never the problem." Selftext was removed by the author, so no method, harness names, or task definition survive; the number pair cannot be re-derived from this source. Banked as a lead, not a measurement.
Estate read: if even half true, harness choice explains ~48x more variance than model choice at the 2B rung, which would reshape the mesh boundary question: before re-running the 17-question battery on more models, re-run it on more harness/wrapper configurations of the same model. Treat as OWED replication, never as a banked measurement.

### 7. r/LocalLLaMA 1wm2fpf JevGraph "evidence-backed knowledge graphs" (2026-09-21, 0 score proxy, 9 comments read all)
https://www.reddit.com/r/LocalLLaMA/comments/1wm2fpf/ (fetched via arctic-shift posts/ids + comments/search)
A decision model benchmark for KG relation extraction: 160 frozen FewRel cases; p95 latency 431ms (decision model) vs 1242ms (DeepSeek V4.1 Flash) vs 1699ms (Luna); cost per 100 decisions 0.410c vs 1.225c vs 1.462c; accuracy 87.5% vs 93.125% vs 89.375% with uncovered counted wrong. Verbatim: "so the result isn't \"Jev wins everything.\" it is much faster and cheaper on this task, with a real accuracy tradeoff." Top comment (score 16): "Neither Jev or Luna are local models... how is this relevant here?"; the useful frame (score 6): "Knowledge graphs are logic, embeddings are statistics. Both have their uses, sometimes on the same kinda task" (u/cagriuluc).
Estate read: gives a price/latency point for wiring the 400-knot/217-doctrine/140-steal layers through a decision model instead of the big model: roughly 3x cheaper and 3-4x faster per extraction at a measured 5-7pt accuracy cost. That trade is exactly the graph-wiring economics question, with a benchmark recipe (frozen cases, identical ordering, uncovered-counted-wrong) we can copy for our own knot extraction evals.

### 8. r/LocalLLaMA 1wz28xr "zero-dependency checkpoint protocol to stop autonomous AI agents from destroying code on refactors" (2026-10-06, TITLE-ONLY: selftext [removed], 0 comments)
https://www.reddit.com/r/LocalLLaMA/comments/1wz28xr/ (fetched via arctic-shift posts/ids)
Title-only evidence; author removed the body before anyone replied. Kept because the title names the same seam class as our burns.md:127-129/183-186 write-seam wounds (agents destroying work mid-refactor) and independently re-derived the fix shape (checkpoint protocol, zero dependencies). Nothing beyond the title is verifiable from this source; treat as a pointer, not a finding.

## Also seen, not banked (leads)
- 1wz1bo9 "Releasing Markov: pi-style harness in a single Bash script with sub-agent support" (Oct 6, selftext empty, 0 comments at fetch): a minimal subagent harness to skim for dispatch-shape ideas.
- 1wufl88 "Local Subagent for Codex Luna (CoderX, Nex2.5, Qwen3.8, Ornith)" (Sep 30, selftext removed): evidence others are wiring local models as subagent tiers under frontier CLIs, which is the driving-ladder shape.
- 1wyyx0z "I found 24 places in my agent repo where a failed API call looks like 'no results'" (Oct 6): our false-success/ok_material law in the wild; worth a full read when the archive has its comments.
- 1wttc3w "121 runs, 18 PASS, public log of every failure" (Sep 30, selftext removed): the 14.9% autonomous-build pass rate would be a good mesh-boundary anchor if the log resurfaces.
- 1wmqkx4 "50+ hours and 100M+ tokens ... autonomous agent on an open math problem" (Sep 22): long-horizon budget shape, unbanked (not read end to end).

## Overlap check receipts
Grep run 2026-10-06 over catalog/catalog.jsonl and memory/ (bg task exec_7729618a, exit 0):
- "verbalized confidence": catalog rows 36f7f48a72e9, aa972b654e1b, d31f7a13306e; memory/research_packs/THE50_W3_T11_TYPED_DECISION_ORACLES.md; memory/runs/gps_50/GPS_PACK.md -> item 3 overlaps thematically, adds new measured delta.
- "decision model": memory/continuity/seat_memory_20260927/jev-system-one-decision-model-20260916.md + catalog hits -> item 5 partially known; wave breadth + option-order bias new.
- "MemTether", "JevGraph", "thinking discipline", "0.017 vs 0.821", "checkpoint protocol": only generic/false-positive hits (trajectory self-log, percolator noise, timestamp coincidences at catalog lines 586469/870312) -> genuinely new.
- "swarm coordination", "lease", "heartbeat", "atomic", "sub-agent": generic session-log hits only -> no direct prior bank of the 1wu3rio contracts.

## Falsifiers / what this sweep could NOT do
- Could not read any thread on reddit.com itself (all direct doors blocked; everything came through the arctic-shift archive via a reader model).
- Could not produce a score-ranked top-of-month (arctic-shift lacks score sort; pullpush search 429s): "strongest" here means strongest-by-relevance within the sampled windows.
- 1wu9wfm and 1wz28xr selftexts are author-removed; their numbers are title-level claims only, marked as leads.
- Scores for posts younger than ~36h (items dated Oct 6) are placeholders per the API docs.
