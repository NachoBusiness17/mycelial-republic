# Sweep write-up: evals-self-improvement via reddit (2026-10-11)

source-fetched: adhoc

Seat: sweep-evals-self-improvement-reddit (dynamic workflow gopher). Feed targets named in the ask: evals shelf of corpus/CURRICULUM.md, model-gates and routing ribs (judge-two, hidden bank, 30-day cell rot), graders and checkers dogfooded at the workflow gate.

## Door report (degraded-door record, per recipe)

Every canonical reddit door degraded from this vantage on 2026-10-11:

- old.reddit.com .json and HTML: serves the login wall ("Log in to use old Reddit"), verified via both WebFetch and the webReader MCP.
- www.reddit.com .json and api.reddit.com: HTTP 403 Blocked.
- www.reddit.com HTML via webReader: "Please wait for verification" interstitial.
- api.pullpush.io (Pushshift successor): hard paywall ("This website does not provide free scraping resources for agents").
- redlib.catsarch.com 429, redlib.perennialte.ch 403, safereddit.com anubis block, reddit.nerdvpn.de Gandalf JS challenge, redlib.zaggy.nl/private.coffee/ducks.party/cow.rip/artemislena also bot-gated or dead for plain fetchers.

Working doors (used for all banking below):

1. redlib.nadeko.net via the webReader MCP (its JS execution passes the anubis challenge). Full thread pages, post bodies verbatim, comments where rendered.
2. www.reddit.com search.rss and per-thread .rss via WebFetch (RSS endpoints bypass the 403 wall). Used for ID harvest and dates.
3. WebSearch site:reddit.com fallback per recipe: weak (the engine's reddit index is shallow; several queries returned dictionary noise). It surfaced thread IDs for older threads and non-reddit leads only.

## Pass 1: broad sweep census

Candidates considered, last 30 days: 25 from r/LocalLLaMA top/month (RSS, 2026-09-11 to 2026-10-06 range), 16 from r/MachineLearning top/month (redlib render), ~12 from r/LocalLLaMA search "LLM judge" top/month, ~8 from search "FRAMES" top/month, 6 from search "known-correct solution" top/month. Total considered: 60+; well past the 30-item floor. Most top-of-month items in both subs are hardware/model news and were screened out. Eval-relevant candidates shortlisted: the 8 banked below plus the overflow leads listed after them.

## Pass 2: deep reads performed

Thread pages fetched and read end to end via redlib.nadeko.net (webReader): 1wv0lww (with substantial comment render), 1wqag1i, 1x0etwe, 1x1tf1t (with top comments), 1wiag69, 1wy9q9e (full post including the correction edit plus the full comment thread). RSI thread 1wgazy4 read as full post body (r/ML listing render) plus post-and-comment digest via its .rss feed. tuieval thread 1x0gaqv read as full post body (search-page render; thread page not fetched, its comments not read).

## Banked items (strongest first)

### 1. FRAMES dual-judge thread (r/LocalLLaMA, 2026-10-01, u/Effective-Ad2060)

URL: https://www.reddit.com/r/LocalLLaMA/comments/1wv0lww/we_benchmarked_18_rag_pipelines_against_an_agent/
Fetched via: redlib.nadeko.net thread page (post + comments).
Quote: "we added a second, independent judge (Gemini Flash 3.8) and measured Cohen's kappa between the two judges (0.93 - 0.98)"
Why it matters: the judge-two design in one community thread. Primary judge Claude Sonnet 5 using the benchmark paper's own grading prompt verbatim; second judge from a different family (Gemini); agreement reported as Cohen's kappa, not vibes. Separately, a grounding checker distinct from the correctness judge: for every judge-correct answer, a second pass gives the checker the text the system actually read (not the citations) and asks whether the answer follows from that text alone; "correct but not grounded" is a separate reported state (accuracy 92.7% vs grounded accuracy 84%; no-retrieval baseline 64.9% from memory). The comment thread carries the sharpest lesson for our gate: the checker initially saw only about 6k tokens of evidence and flagged many correct answers wrongly (u/Rachel_talks: "a grounding checker that sees less than the model did is just another claim-maker with its own filling-in problem"); full-text recheck cut false flags from 55 to 2. Cost/latency reported as p50/p90/p99 distributions with the costliest 10% of traces eating 43% of spend. Caveat recorded: commenters accuse the account of LLM-generated posts with clanker bot upvotes; treat numbers as a design pattern to re-run ourselves, not as settled truth.
Steal: (a) judge-two = cross-family quorum with kappa reported per bench; (b) grounding check separated from correctness check, checker must see everything the model saw; (c) two-number accounting (accuracy + grounded accuracy) on every verdict surface.

### 2. tau2-bench pass^3 reliability thread (r/LocalLLaMA, ~2026-09-14, u/FantasticNature7590)

URL: https://www.reddit.com/r/LocalLLaMA/comments/1wiag69/qwen38flashnext_on_the_official_sglang_nvfp4/
Fetched via: redlib.nadeko.net thread page. Date derived from the mirror's "27d ago" stamp (exact date not shown on the render; OWED if precision matters).
Quote: "tau2-bench: Running all 114 tasks three times per model, pass^3 41.2% vs single-attempt 68.1%"
Why it matters: RQ2's core number pair, community-measured. Reliability gap quantified three ways on one stack: (a) pass^3 vs single-attempt on all 114 tau2-bench telecom tasks (41.2% vs 68.1%); (b) multi-turn 49.5% vs single-turn 85.2% on BFCL v4 (114 frozen cases, one run per day to dodge cache contamination, disagreement logged per case); (c) 254K-context recall 81/81 correct after a 16-hour session sim, with repetition-failure observed elsewhere ("got one digit wrong on the same request later"). The author's own conclusion mirrors our law: "Benchmarks tell you what a model can do once. Production is about what it does every time."
Steal: adopt pass^k (k=3) and multi-turn-vs-single-turn delta as the two reliability columns for any model-gate rib; one-run-per-day freezing against cache contamination is exactly our 30-day cell-rot concern.

### 3. Mica v0.1 held-out decision model (r/LocalLLaMA, 2026-09-25, u/Top-Evidence174)

URL: https://www.reddit.com/r/LocalLLaMA/comments/1wqag1i/mica_v01_4b_open_jevstyle_decision_model_yesno/
Fetched via: redlib.nadeko.net thread page.
Quote: "This set was held out (written after the training data was frozen and not opened until training finished)"
Why it matters: a contamination-blind protocol for a cheap non-frontier judge. 7,328 held-out decisions written after the training data freeze and not opened until training ended; sealed JevBench run mentioned; abstention gate (min_confidence, rejects low-confidence instead of guessing); calibration ECE 5.4% (claims to beat Jev's); prompt-injection robustness 69% in-data vs Jev 18%. The whole decision-model-as-judge wave (Jev, Mica, Jeff, d1-3B) is a cheaper judge-two candidate for our family problem: a 4B cross-family decision model with abstention is a second opinion that never shares ember's family.
Steal: the freeze-then-write held-out discipline is the exact protocol the hidden ask bank owes (bank asks written after, and sealed from, the models being gated); abstention thresholds belong in the judge-two quorum rule.

### 4. Small models write tests and code; known-correct gate (r/LocalLLaMA, 2026-10-05, u/deadatreides1)

URL: https://www.reddit.com/r/LocalLLaMA/comments/1wy9q9e/let_small_local_models_write_both_the_tests_and/
Fetched via: redlib.nadeko.net thread page (post + correction edit + full comment thread).
Quote: "A model can propose tests, it doesn't get to be the judge."
Why it matters: grader honesty with a public correction loop. The 77% false-rejection headline got honestly re-split in the edit after u/RobWattx's mutation-score critique: 42% of generated suites did not run at all; of the suites that did run, 60% rejected the known-correct solution ("59 wrong asserts out of 98"); wrong asserts, not coverage, are the dominant failure. The author's fix is our FIND/FILE/LOAD doctrine in miniature: "the check that decides comes from the spec or from examples a human wrote"; validated on an edit where tests passed while behavior visibly broke.
Steal: every hidden-bank ask should carry a known-correct reference answer (the 100+ bank design); never let the model that wrote the work grade the work; log did-not-run as its own failure class in the gate's grader census.

### 5. Blind human preference study, 2 months, 7 models (r/LocalLLaMA, 2026-10-08, u/Altruistic_Heat_9531)

URL: https://www.reddit.com/r/LocalLLaMA/comments/1x0etwe/2_months_memed_research_do_people_notice_the/
Fetched via: redlib.nadeko.net thread page.
Quote: "the complaints don't start when the model starts making mistakes. They start around the 9B parameter mark"
Why it matters: RQ4 evidence from real human workloads, not lab benches. 7912 requests, 8 users, 7 models, blind A/B with randomized branding, users deceived into thinking it was plain ChatGPT. Request distribution is task-class dominated: half document-writing, a third grammar polishing, then search-style questions, almost no coding; only 51/7912 requests were marked high-reasoning. Perception threshold at ~9B; request categorization done by LLM with uncertainty carried in the report. This is the workload shape our router actually serves: the estate's 36.3 pct task-class-dominates-family claim points the same direction (small-model sufficiency for most classes, judgment only for the tail).
Steal: task-class mix should be a first-class column in routing ribs; blind A/B with randomized branding is the operator-facing analog of our hidden bank.

### 6. tuieval domain-specific eval post (r/LocalLLaMA, 2026-10-08, u/norenEnmotalen)

URL: https://www.reddit.com/r/LocalLLaMA/comments/1x0gaqv/comparing_qwen3827b_finetunes_and_baselining_vs/
Fetched via: redlib search-page render (full post body; comments not read).
Quote: "gpt-oss-120b shat the bed on my pandas/numpy tasks. Only domain specific evals can uncover cases like that and warn you which models/fine-tunes to steer clear of for particular tasks"
Why it matters: RQ4 replication direction with per-domain inversions. 469-question domain eval via open-source tuieval (github.com/ashe-wb/tuieval); frontier models near-ceiling (Opus 5.5 at 99.6%) but gross per-task failures hide behind headline scores (gpt-oss-120b on pandas/numpy); a PTA index KPI measures grounding vs source; provider-masking of reasoning tokens (Astra) flagged as a reproducibility hazard.
Steal: domain-slice evals before any routing promotion; log providers that mask reasoning as an eval-integrity risk in the model-gates rib.

### 7. Open-weight community benchmark with domain filters (r/LocalLLaMA, 2026-10-09, u/EmilPi)

URL: https://www.reddit.com/r/LocalLLaMA/comments/1x1tf1t/just_another_purely_openweight_models_benchmark/
Fetched via: redlib.nadeko.net thread page (post + top comments).
Quote: "No model rules them all. DeepSeek-V4-Vision-Exp rules, but other models have their rule areas."
Why it matters: RQ4 at community-benchmark scale. beta.locallm.top runs per-domain/intent filters over 900+ questions and 700+ tasks, human domain-expert grading on purpose (no LLM-as-judge in the loop), acceptance tracking, and full JSON export of every run. The stated philosophy is task-class rule areas rather than one champion model; the OP explicitly wants third-party runs to check their numbers.
Steal: per-domain leaderboards plus exportable raw runs is the shelf shape for our evals domain extension beyond openai/evals, promptfoo, HELM; human domain-expert grading as the arbiter of last resort.

### 8. RSI is not happening, author-graded held-out tasks (r/MachineLearning, 2026-09-14, u/we_are_mammals)

URL: https://www.reddit.com/r/MachineLearning/comments/1wgazy4/rsi_is_not_happening_r/
Fetched via: r/ML top/month listing render (full post body) + per-thread .rss digest (post + top comments). Underlying paper: arxiv.org/abs/2607.27191 (paper itself not fetched; OWED if the protocol detail matters).
Quote: "Each problem was graded by the original paper authors, giving a more reliable signal than automated benchmarks."
Why it matters: RQ3's held-out protocol at research scale. Accepted-but-unpublished NeurIPS papers given to agents (Codex/GPT-5.6 Sol, OpenClaw/Opus 4.8) as genuinely unseen tasks, graded by the papers' own authors; agents failed to reproduce. The comment thread adds the bias caveat that matters for us: u/Physical_Vehicle7714 names possible grader bias (authors grading reproductions of their own work), the same self-interest class as self-grading in LLM judges. Companion survey linked in-thread: arxiv.org/pdf/2607.07663v1 (bounded self-refinement only).
Steal: unpublished-but-accepted work is the cleanest unseen-task supply for a contamination-blind bank; but pair author-grading with a non-interested second grader, the same quorum rule as judge-two.

## Overflow leads (read but not banked, kept for the shelf)

- Routing with Jev over regex, 3B/4B/12B/26B tiers (1wk0st3, r/LocalLLaMA 2026-09-18): post-hoc answered/refused/non_answer checker on routed replies catches silent refusals that gateways count as success; full post read via search render.
- Jeff 0.8B/2B System 1 decision models (1wspn24, 2026-09-28): JudgeBench numbers, "Benchmarks don't predict play" conclusion; full post read.
- 50+ hours, 100M+ tokens open-source agent on an open math problem (1wmqkx4, 2026-09-21): long-horizon autonomous reliability narrative; surfaced via RSS, body not deep-read.
- Two 96GB Ascend cards Qwen3.8-flash-next benchmarks (1wvt1m4, 2026-10-02): additional BFCL/tau2 datapoints on different hardware; surfaced via RSS, not deep-read.
- Swift-1.5 M5 Max llm-bench post (1wte7n0, 2026-09-29): agent-workflow token accounting with judge-variance caveat; full post read.
- LHTB Long-Horizon Terminal-Bench (github.com/zli12321/LHTB) and Surge AI long-horizon training (Toolathlon, tau2, BFCL-V4 disjoint evals): surfaced by the WebSearch fallback, NOT reddit threads, not fetched, so banked nowhere. Follow-up candidate for the evals shelf owner.

## Research-question verdicts

- RQ1 (bias-resistant judge protocols): reddit 2026 validates cross-family dual-judge with kappa reporting (item 1), judge/checker role separation with full-evidence visibility (item 1), known-correct human-authored gates (item 4), and small decision-model judges with abstention and calibration (item 3). Position-bias controls (order swap) did NOT appear in any 2026 reddit thread I read; that leg stays OWED.
- RQ2 (long-horizon reliability): pass^3, multi-turn deltas, frozen case sets, session-length recall all demonstrated in item 2; tau2-bench/BFCL v4/Terminal-Bench are the names the community actually runs. LHTB and the 100M-token math agent are the unbanked follow-ups.
- RQ3 (contamination-blind): freeze-then-write held-out sets (item 3), unpublished-paper unseen tasks with author grading (item 8), known-correct reference answers (item 4), blind branding (item 5). Directly shapes the 100+ hidden ask bank: asks written post-freeze, sealed, each carrying a reference answer, graded by non-interested second parties.
- RQ4 (task class dominates family): three independent community datasets converge on task-class dominance (items 5, 6, 7). None replicates the estate's exact 36.3 pct statistic; direction supported, exact-number replication remains unfulfilled, so the named replication falsifier stays open.

## Overlap method (commands run, 2026-10-11)

- grep -rl for distinctive phrases over catalog/catalog.jsonl and curated memory/ dirs (frontier, rib, improve, press, workflows, briefs, lenses, game, zknot): "FRAMES", "agent loop", "Mica v0.1", "Do People Notice", "tuieval", "known-correct solution", "tau2", "locallm.top", "JudgeBench", "RSI is not happening", "position bias", "EmilPi": zero hits except generic "agent loop" phrases in three memory/improve files that predate these works (2026-06/07/08) and are unrelated phrase collisions. memory/agent_sessions was excluded from the loop grep for cost; those are ephemeral session logs, not holdings.
- Case check: grep -c "FRAMES" catalog/catalog.jsonl returned 0 (the case-insensitive hit was generic "frames" text).
- "ember" in catalog.jsonl hits ember.sql only (unrelated artifact); "36.3" hits in frontier files are timestamp fragments ("13:21:36.388"), not the routing claim.

## Fabrication ledger (OWED)

- Exact calendar date for item 2 is derived from the mirror's relative "27d ago" stamp; not independently confirmed.
- Comments on items 3, 5, 6 (Mica, Do People Notice, tuieval) were not read (thread renders carried the post; comment sections did not surface in those fetches).
- RSI underlying paper arxiv 2607.27191 and survey 2607.07663v1 not fetched; claims rest on the thread bodies only.
- LHTB / Surge AI leads not fetched (non-reddit surfaces, out of this sweep's door).
- No independent replication of the estate's 36.3 pct routing statistic was found; RQ4 support is directional only.
