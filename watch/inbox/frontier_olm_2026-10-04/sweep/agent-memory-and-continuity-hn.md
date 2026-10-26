# SWEEP: agent-memory-and-continuity via HN - 2026-10-04

source-fetched: 2026-10-04. Agent: sweep-agent-memory-and-continuity-hn. Door: Hacker News
(hn.algolia.com API v1, search_by_date + search relevance, tags=story, then items/<id> and
news.ycombinator.com thread trees, then primary pages fetched raw). House laws held: ascii
only, no em or en dashes, every claim cites a page fetched or a command run this sitting.
Quotes below are HTML-unescaped renderings of bytes fetched this sitting (curly punctuation
normalized to ascii); the saved raw pages are receipts in this directory
(_am_page_<id>_<tag>_*.txt) and the fetch scripts are _am_pass1.py / _am_pass2.py.

## Dedup spine read in full this ask (six prior folds of this area)

- watch/inbox/frontier_olm_2026-10-03/sweep/agent-memory-and-continuity-hn.md (190 lines, the
  evening rewrite; its morning-seat baselines included)
- watch/inbox/frontier_olm_2026-10-02/sweep/agent-memory-continuity-hn.md (69 lines)
- watch/inbox/frontier_olm_2026-10-01/sweep/agent-memory-continuity-hn.md (70 lines)
- watch/inbox/frontier_olm_2026-09-30/sweep/agent-memory-continuity-hn.md (50 lines)
- lens files of this carrier: lens/graph.md (full, 36 lines), lens/burns.md (full, 194 lines),
  lens/questions.md (full, 124 lines; section 3 is this area's five questions)
- cross-area collision checks: the four kv-cache-and-context-engineering HN folds (09-28,
  09-30, 10-01, 10-02, 10-03) and the area's reddit/x siblings where greps hit

## Door health

20 pass-1 Algolia lanes + 6 targeted RQ4 lanes, all clean JSON, zero 403s, zero degraded
queries. Two real negatives recorded: `sleep-time` by-date nbHits 0, `memory consolidation`
by-date nbHits 0, `Memory-R1` by-date nbHits 0. WebFetch and web_reader were not used; every
fetch this sitting was curl or the repo venv python (urllib) against the same endpoints the
recipe names, chosen so quotes are byte-checkable against the saved receipts.

## Pass 1: candidate pool (202 unique stories, 139 inside the ask's 30-day window)

By query: `agent memory` by-date 30, `LLM memory` by-date 20, `long-term memory` by-date 20,
`knowledge graph` by-date 20, `conversation memory` by-date 15, `memory layer` by-date 15,
`compaction` by-date 15, `Letta` by-date 15, relevance lanes: `sleep-time compute` 15,
`memory reinforcement learning` 15, `long context retrieval` 15, `context rot` 10,
`MemGPT` 10, `memory benchmark` 10, plus by-date `sleep-time` (0), `memory consolidation` (0),
`reflection agent` 10, `warm start` 10, `MemAgent` 10, `context rot` by-date 10. Full hit
lists saved at _am_p1_hits.json (in_window + older + negatives, byte receipts). Flagship
in-window candidates never surfaced by any prior fold: 49945933 (285/163, 10-03), 49734038
(09-16, listed only by the kv lane), 49727926 (09-16), 49874916 (09-28), 49833684 (09-24),
49833566 (09-24), 49797488 (09-22), 49731631 (09-16), 49655089 (09-11), 49950478 (10-04),
49951895 (10-04), 49946507 (10-03), 49924943 (48/8, 10-01). Comfortably past the 30 bar.

## Pass 2: deep reads (pages and threads fetched and read this sitting)

1. news.ycombinator.com item 49945933 (163-comment tree + comment search) + liao.gg blog
   agents-dont-need-memory (12,737B saved, read head through prescription to sign-off)
2. www.boolean.ai/blog/context-rot-quantified (93,204B saved; study design, unrelated and
   related arms, tokenizer correction, momentum-induced collapse, conclusion) + thread 49734038
3. arxiv.org/abs/2608.08253 (SuperLocalMemory 4.0 v2 abstract, read in full) + thread 49950478
4. github.com/oren198/Strata README (650,234B page saved, core-concepts section read) + story
   text of 49807583
5. www.cognee.ai/agent-memory definitive guide (294,740B saved; TL;DR, lifecycle/consolidation,
   entity-resolution sections read) + thread 49861765 including the full shurayu comment
6. github.com/jahala/copeca README (355,939B page saved, thesis section read) + Novgraph story
   and thread 49745176 including the full jahala comment
7. john.oram.ca/opinion/self_improving_software_memory (29,184B saved, thesis through metric
   read) + thread 49655089
8. github.com/naw103/claude-routine-cleanup story text + 3-comment thread (49946507)
9. blog.reduck.ai browser-action-memory post (26,361B saved) + thread 49910148
10. github.com/chetto1983/Aura README (488,256B page saved, what-is and stack sections read)
11. Story text + threads of 49628820, 49667676, 49731631, 49878492, 49655089 (titles and story
    bodies; pages of the last three not fetched, reasons in the not-banked block)

## Answers to the five lens questions (lens/questions.md section 3)

### RQ1 (linking passes vs pruning vs regeneration for retrieval value)

This door's strongest signal favors regeneration into durable documents over link passes, and
pruning last. The window's highest-traction memory item (285 points, 163 comments) argues the
retrieval value of a memory store is recovered by keeping an auditable, human-readable
document workspace consulted before and updated after work, not by better recall over
accumulated snippets; its audit litany ("Which memories exist? Which are stale? Which have
never been retrieved?") is literally the estate's graph.md state (1,057 edgeless knowledge
nodes). The cognee thread adds the regeneration rule from a builder who faced the exact
model-swap version of the estate's knot problem: keep the source rows owned and plain so
re-extraction is always possible. The cognee guide itself puts derived summaries on-graph as
their own traceable layer above raw entries (linking AFTER regeneration, traceable to facts).
Pruning appears on this door only as reversible sweeps (memanto, held 10-01). Rank order:
regenerate curated surfaces from source rows first, then ingest-time linking discipline
(post-graph-rag keys held 09-30, OKF code_refs held 10-02, Strata judge gate below), then
pruning.

### RQ2 (identity/dedup schema keeping precedent rows individually addressable)

The sharpest new answer is SuperLocalMemory 4.0 (arXiv 2608.08253v2): it runs a three-arm
ablation varying ONLY the recall session-identifier namespace and shows recall moves no
posterior while the identity defect is present, i.e. the identity namespace is not metadata,
it is the recall path itself; and it ships two oracle invariants, a prior-distance assertion
and a join-liveness assertion that "reports where a guard's missing data resides", which is a
published diagnostic for exactly the estate's dangling-endpoint class (794 has_invariant
edges with no nodes). Strata contributes the write-side schema: per-scope LLM-judge gates
where declines are recorded and kept, so what each agent believes, whence, and what was kept
out is queryable; its v1.12 failure (an irrelevant note admitted until scopes state a
purpose; empty scopes still admit, issue #210) is the empty-identity failure in miniature.
Cognee names the resolution problem plainly (deciding whether three surface forms are one
node) and answers with typed nodes under a preset schema. Cross-held: post-graph-rag
canonical keys, OKF scoped shadowing, Graphiti MinHash+LLM two-phase dedup (reddit 10-01),
Zep invalid_at. None of these publish a post-hoc merge tool for an already-collapsed id
space; the estate's 300 `law:` rows still need re-keying at ingest, and SLM's ablation is
the published proof that leaving the namespace broken silently zeroes recall.

### RQ3 (consolidation schedules mapping onto a logon-rewrite window without drift)

The door splits. The flagship essay rejects overnight consolidation daemons outright ("no
summarizers, curators, updaters, dreamers, or any other token-burning background daemon") and
runs consolidation at session close while context is still loaded: consult before, update
after. The cleanup skill supplies the boundary law from the frontier's own scar tissue:
Claude Code's scheduled routines each leave sessions behind (618 open sessions from ONE
routine) and the app's delete tool is disabled INSIDE routine runs, so residue cleanup must
run outside the loop that generates it, with a non-destructive preview planner first. zknot's
logon-rewrite window already satisfies the outside-the-loop half; the preview-first and
dry-run halves match memanto (held 10-01). For the anti-drift half of the question, SLM 4.0
is the published instrument: consolidation claims verified by an oracle independent of the
mechanism under test, per-projection apply/verify/compensate owners, and hash-checkable
completion manifests; 11 fault-injection scenarios x 200 repetitions held 2,199 of 2,200.
A zknot rewrite could carry the same shape: a manifest of cited session ids that must resolve
to real bytes before the rewrite lands. The cognee guide's lineage anchor is Generative
Agents' periodic reflection with derived entries traceable to the facts behind them.

### RQ4 (memory-selection reward designs measured end to end)

Negative recorded honestly: no in-window HN story carries a reward-trained memory selector
(surprise, compression gain, or retrieval hit-rate as the reward). Lanes: `Memory-R1`
by-date nbHits 0; `memory consolidation` nbHits 0; `sleep-time` nbHits 0; relevance lanes
`memory reinforcement learning` and `MemAgent` returned only off-window or off-topic hits.
What the door DOES measure end to end on harness-like workloads are outcome units and
oracles, not reward signals: Oram's trigger-index selection loop with the declared metric
"tokens per correct ticket" (a cheap always-loaded index of one-line triggers; full bodies
retrieved only on match, so selection cost is paid only on hit); copeca's cost-per-correct
A/B harness built precisely to test MCP servers, context compressors, hooks and harness
changes against a clean baseline; SLM's oracle requirement (implemented, reachable, effective
are three different questions) with 2,199/2,200 fault-injection holds; and the boolean.ai
pass-rate curve as the stuffing-cost side. Read for the estate: the missing intrinsic wire
has no measured reward-design precedent on this door; the measured designs all externalize
the reward as cost-per-correct or as an independent oracle, which is implementable without
any learning loop. Out-of-window pointers surfaced and NOT banked: Zero-Mem (49178608,
101 pts, 08-05), delta-mem (48158506, 240 pts, 05-16), the Sleep-Time Compute thread itself
(43753878, 2025-04-21), all outside the ask's 30-day window.

### RQ5 (warm-start context size vs retrieval: the knee)

The knee evidence is cross-area held: boolean.ai context-rot was banked 10-01 by the kv lane
(kv-cache-and-context-engineering-hn.md 10-01 item 3, re-confirmed held at 10-03 :31/:42 with
the same numbers I read: GPT-5.6 Sol 31 to 24 percent pass from 0 to 250k prefill regardless
of relatedness, Opus 5 flat on unrelated but 50 to 40 percent on related, momentum-induced
collapse at 250k+). Not re-banked; I bank only the one sentence that kv lane did not, and it
is the RQ3/RQ5 bridge: preliminary findings that compaction recovers part of the rot. On the
knee question itself: nothing on this door measures any knee below 250k; the held anchors
bracket it (j9s.io median agent prefill 15,146 tokens/turn, held 10-01; Motif 1,496-token
bundle answering 8 of 9 questions over 1.77M tokens, held 10-01). warm_state.json
brief-plus-tips is kilobytes, four orders of magnitude under the first measured degradation
point, so the measured record says the estate's shape is safely below the knee and the
frontier's own takeaway is "use new sessions or compact whenever possible", i.e. retrieve,
do not stuff. Oram's design states the same constructively: keep the always-loaded surface
to the trigger index, pay retrieval only on match.

## Banked finds (8, strongest first)

### 1. Agents don't need memory, they need documentation (liao.gg, Kevin Liao; HN 49945933, 2026-10-03, 285 pts / 163 comments)

Quote (essay): "Because agents don't need memory. They need documentation."

Why: the window's flagship (285/163) is a direct RQ1 verdict and the estate's own residual+
registry+leaf shape argued from the other side. The mechanism named is the auditable
document workspace: instructions, specs, research, indexes written by the agent, consulted
before work, updated after, while the full picture is still in context; the loop changes
from prompt-build-forget to consult-build-update. His five failure modes of RAG memory
stores (similarity-ranked, context-free, past-as-truth, unknown-unknowns, unauditable) map
one-to-one onto the graph lens: the estate's 1,057 edgeless nodes and 400 empty knots are
his "unauditable store" stage four and five. Shipped as Operator Memory
(github.com/aerovato/operator-memory), plain markdown, no embeddings. The 163-comment thread
adds the counterweight (Naur's Programming as Theory Building: documentation cannot carry
the full theory; espeed's Whybase proposition tree mapped to files with hook-triggered
retrieval, whose staleness question nextaccountic raises is exactly the invalid_at problem
already held via Zep).

Overlap: catalog grep 0 for liao.gg, aerovato, operator-memory, "need documentation";
frontier_olm folds 0 in any bank file; one raw-dump listing exists: the 10-03 X-lane raw pull
(2026-10-03/sweep/tmp/sw2_full.jsonl) carries the reddit cross-post TITLE only ("Agents don't
need memory. They need documentation.", r/ClaudeCode 1wwsryn), never read or banked by any
fold. Genuinely new at the banking layer. Confidence 0.9.

### 2. SuperLocalMemory 4.0: governed memory OS whose lead result is that ten shipped mechanisms did nothing (arXiv 2608.08253v2; HN 49950478, 2026-10-04)

Quote (abstract): "Implemented, reachable and effective are three different questions, and
the third requires an oracle independent of the mechanism under test."

Why: the most methodologically honest memory paper this door has surfaced, and it lands on
RQ2 and RQ4 at once. Identity is proven load-bearing by ablation: a three-arm experiment
varying only the recall session-identifier namespace "moves no posterior with the defect
present and every instantiated arm with it absent", i.e. a broken identity namespace silently
zeroes recall while everything looks alive, which is the estate's 300-rows-on-`law:` risk
stated as a measured result. Its two oracle invariants (prior-distance assertion over
Bayesian learners; join-liveness assertion over schema-guarded paths that reports where a
guard's missing data resides) are liftable directly as knowledge_graph.py repair gates: a
build-time check that reports WHICH source row failed to materialize, not just a dangling
count. Also banks its negative result (ten mechanisms implemented, reachable, ineffective),
the 2,199/2,200 fault-injection census, and the v1 self-retraction of a non-comparable
overhead figure (the estate's errata culture, published).

Overlap: catalog 0 for superlocalmemory and 2608.08253; all frontier_olm folds 0; story
posted today, in no prior pool. Genuinely new. Confidence 0.85.

### 3. Self-Improving Software Memory: trigger-index selection with a declared tokens-per-correct-ticket metric (john.oram.ca; HN 49655089, 2026-09-11)

Quote (essay): "The goal is not to accumulate knowledge. It is to accumulate knowledge
without making every future prompt larger."

Why: this is the two-module framing made concrete by a practitioner, and the closest thing
this door offers to a measured selection design. Learnings are small structured records
(title, trigger, body, project, ticket); the trigger is one sentence describing WHEN the
knowledge is relevant, not the knowledge; agents always load only the trigger index (cheap)
and retrieve full bodies only on a match (expensive, paid on hit). The loop is claim ticket,
search memory, implement, validate, record learning, with claim state centralized in a shared
ticket system so concurrency across machines is read, not inferred. The declared end-to-end
metric is tokens per correct ticket, and the design's stated purpose is a year of accumulated
detail without every future prompt growing. Maps to RQ4 (selection with an outcome unit, no
reward model) and RQ5 (always-loaded surface kept minimal by construction).

Overlap: catalog 0 for john.oram; frontier_olm folds 0 (the `oram` grep hits are substring
false positives inside "panoramic"/NoRA contexts, the same class the 10-02 x-lane disclosed);
not in any prior pool. Genuinely new. Confidence 0.8.

### 4. Cognee's definitive guide + the model-swap comment: keep source rows plain so re-extraction is always possible (cognee.ai/agent-memory, Aug 2026; HN 49861765, 2026-09-26)

Quote (guide): "Raw entries tend to accumulate faster than they become useful, so memory
systems need to compress them."

Why: RQ1/RQ3. The guide's lifecycle section is the cleanest published statement of the
consolidation layer this side of Generative Agents (which it cites): reflection draws
higher-level conclusions and writes them back as their own layer ON the graph, "the
connections it adds stay traceable to the facts behind them", agents work from the compressed
view without losing the underlying rows. That is the estate's residual+leaf split with the
traceability clause made explicit, and it answers the knot backfill ordering: regenerate
surfaces from source rows first, link derived layers second. The thread's top comment
(shurayu, a neighboring builder) adds the model-swap problem the estate will hit the first
time it changes extraction models: write-time extraction bakes in the extracting model's
judgment, so either the old graph persists or you re-extract; their cure is keeping the
source as plain markdown the user owns so re-extraction is always possible. Also carries the
entity-resolution framing (typed nodes under a preset schema constrain whether three surface
forms are one node or three).

Overlap: catalog grep "cognee" = 58 rows, ALL verified by reading rows to be
ms-agents-beginners course notebooks (13-agent-memory-cognee.ipynb and translations), not the
guide; the guide page itself is unheld. The story id 49861765 appears in the 09-28 fold's
pass-1 pool listing only (09-28 sweep :83, "49861765 cognee guide (3/0)"), never read.
Banking-layer new. Confidence 0.8.

### 5. Strata: per-scope judge-gated writes with declines kept (github.com/oren198/Strata; HN 49807583, 2026-09-22)

Quote (README): "every write is checked by an LLM judge before it lands, so one agent's
mistake never corrupts what the rest of the fleet reads".

Why: RQ2, the write-side complement to SLM's read-side identity proof. Fleet memory in
ordered strata of scopes (architecture, backend, tests); every contribution is judged against
the scope's stated purpose; declines are recorded and kept, so a console shows what an agent
currently believes, where each belief came from, and what was kept out and why. The author's
own failure census is the value: v1.12 admitted an irrelevant coffee-machine note until
scopes stated a purpose, and empty scopes still admit such notes (issue #210, disclosed in
the story text), which is the empty-context identity failure in miniature, the same class as
the estate's bare-word `law:` ids formed where the loader found no identity fields. Scopes
with declared purpose plus kept declines is a liftable pattern for the percolator and for
knowledge_graph write gating.

Overlap: catalog 0 for oren198; frontier_olm folds 0 in bank files (the id appears in the
09-30 fold's pass-1 pool listing as "Strata 49807583", listed never read). Banking-layer
new. Confidence 0.8.

### 6. copeca: cost per correct answer, a neutral A/B benchmark for exactly the estate's compressor-and-harness changes (github.com/jahala/copeca, via Novgraph thread HN 49745176, 2026-09-17)

Quote (jahala, HN comment): "A tool that saves 90% of tokens but makes 20% more mistakes has
worse cost-per-correct."

Why: RQ4/RQ5, the outcome unit. The Novgraph thread's sole substantive comment is a
measurement-design lesson aimed at the estate's exact temptation: "-X% tokens removed!" is a
marketing number; the honest unit is cost_per_correct = total_spend / correct_count, A/B'd
against a clean baseline, because savings tools often cost more turns and fewer cache hits
and land at similar real cost with more wall time. The copeca README (fetched this sitting)
generalizes it: a neutral, reproducible, verifiable benchmark for CLI coding agents, built to
A/B MCP servers, context compressors, hooks, and harness improvements. This is a concrete
candidate instrument for the dacorvo weighted-token candidate unit the 10-03 fold marked
OWED (10-03 fold RQ2: "a rib citing it should name it as a candidate unit to replicate");
copeca is the published harness class that replication would run inside. Novgraph itself
(96.04 to 99.81 percent claimed token savings, no accuracy denominator) is the cautionary
exhibit, banked here only as the thread that carried the comment.

Overlap: catalog 0 for copeca and "cost per correct"; frontier_olm folds 0; novgraph 0
anywhere. Genuinely new. Confidence 0.75.

### 7. Claude Code Routine Session Cleanup: 618 residue sessions from one routine, delete disabled inside the loop (github.com/naw103/claude-routine-cleanup; HN 49946507, 2026-10-03)

Quote (story text): "We had 618 open sessions in just one routine."

Why: RQ3, the boundary law for any consolidation window, learned from frontier scar tissue:
scheduled routines silently accumulate sessions (618 from ONE routine), the desktop app's
delete tool is turned off INSIDE routine runs so cleanup must run from a normal session
outside the generating loop, file-level deletion does not work because the app holds the
list in memory and writes records back, and the planner is deliberately non-destructive
(preview first, keeps newest N, protects any session where a human replied). Four liftable
rules for zknot and any logon-rewrite organ: residue accrues per scheduled run and must be
counted; consolidation runs outside the loop it cleans; the planner previews before the
destructive pass; human-touched records are protected by default.

Overlap: catalog 0 for claude-routine-cleanup and "618 open sessions"; frontier_olm folds 0;
not in any prior pool. Genuinely new. Confidence 0.7.

### 8. boolean.ai context-rot addendum: the unbanked compaction-recovery sentence (cross-area HELD primary; HN 49734038, 2026-09-16)

Quote (post, conclusion): "In some preliminary findings, we do see that compaction can
recover some of the performance degradation loss that we observe at longer context."

Why: the primary is HELD, banked 10-01 by the kv lane (10-01 kv fold item 3) and
re-confirmed with the full numbers at 10-03 kv fold :31/:42; not re-banked. This addendum
banks only the one sentence no fold carried: the study's own preliminary finding that
compaction recovers part of the measured rot. It is the single published bridge between this
area's RQ3 (consolidation works) and the kv area's degradation curve, and it is labeled
preliminary by its own authors, so it cites as preliminary or not at all. Scope guard for
the next seat: everything else in that study (31 to 24 and 50 to 40 percent arms,
tokenizer normalization, momentum-induced collapse, the "use new sessions or compact"
takeaway's rot numbers) is already in the 10-01/10-03 kv banks; the takeaway sentence's
recommendation clause is new here only in its RQ5 framing.

Overlap: verified held by reading the 10-01 kv fold item 3 and the 10-03 kv fold :31 and :42
this sitting; the exact compaction sentence greps 0 over both kv folds and all agent-memory
folds. Scoped addendum, new sentence only. Confidence 0.75.

## Considered, not banked (with reasons, so the next seat never re-considers)

- 49727926 Self-evolving agents need pain, reflection, and sleep (medium.com): thread is one
  off-topic comment; medium.com is the fold's standing 403/Cloudflare wall (four sessions
  running, 10-03 fold OWED block); no quote obtainable, not banked.
- 49874916 CliffCompaction (arXiv 2609.26779): title is squarely RQ5; abs page not fetched
  this sitting after the slate filled; LEFT OWED as the next seat's first fetch.
- 49833684 Shared Memory for Coding Agents (getbelay.vercel.app, 1 pt), 49833566 Pinocchio
  (3 pts), 49731631 Cortex (2 pts), 49667676 memanto loops post (2 pts), 49628820 Four Kinds
  (4 pts, listed in the 09-28 pool), 49596543 GraphMemix and 49797488 Beyond Context Windows
  (both resolve to Twitter posts by the AgentMemoryL/MemoraX accounts, and the X door is the
  fold's degraded door): titles and story bodies read, pages not fetched, zero comments on
  most; nothing quote-bearing obtained.
- 49910148 Reduck (read end to end, blog saved): the measured 2.5 to 3.6x is a 3-task vendor
  demo against Claude for Chrome MCP; the "memory layer" is a cached Playwright-script
  library, i.e. skill caching, not memory selection; listed three times by prior pools,
  never banked, and I keep it unbanked for thin measurement. Its one transferable datum:
  the measured win comes from replacing re-derivation with stored procedures, which is the
  estate's skills-steal law already.
- 49951895 Aura (read, README saved): real engineering (6,541 commits, per-user memory
  databases, ArcadeDB graph memory with FTS + LSM vector index, MUSR two-identity E2E test)
  but zero HN traction and no mechanism detail beyond the stack list; held as a watch-item.
- 49878492 Decide/Jev CLI: the decision-model lane was already banked today by commit
  993a5977b (proper-scoring-rule decision models, burns.md section 5); this is a tool-level
  sibling, not new doctrine.
- 49924943 Breadcrumb (48/8): personal context recorder; the one transferable number
  (30+ MCP tool definitions riding every request, ~85,500 chars per the aidiveyt comment) is
  a kv-area context-budget datum, not an area find; disclosed here, not banked.

## Overlap ledger (exact commands and counts, this sitting)

- `grep -c -i` on catalog/catalog.jsonl: aerovato 0, operator-memory 0, liao.gg 0,
  "need documentation" 0, oren198 0, copeca 0, "618 open sessions" 0,
  claude-routine-cleanup 0, reduck 0, john.oram 0, memanto.ai/blog/four-kinds 0,
  cognee.ai/agent-memory 0, etto1983 0, ArcadeDB 0; from the earlier batch:
  sleep-time compute / 2604.13171 / memory-r1 / memagent 0, superlocalmemory 0,
  2608.08253 0, boolean.ai / "context rot" 0, "liao.gg" 0; "cognee" 58 (all
  ms-agents-beginners course notebooks, verified by reading rows; the guide itself unheld).
- `grep -ril` over all six frontier_olm carriers (20260928, 09-30, 10-01, 10-02, 10-03,
  10-04): liao.gg 0; "need documentation" 1 (the 10-03 X-lane RAW dump tmp/sw2_full.jsonl,
  reddit cross-post title only, disclosed on item 1); boolean.ai and "context rot" only in
  the four kv folds (HELD, item 8); 2608.08253 0; superlocalmemory 0; copeca 0; novgraph 0;
  oren198 0; routine-cleanup 0; "618 open" 0; reduck 3 files, all pass-1 listing lines,
  one count each; cognee in 4 folds (09-28 pool listing :83, reddit stack-lists, X overlap
  counts, one out-of-window reddit id), never deep-read; oram hits are panoramic/NoRA
  substring false positives per the 10-02 x-lane's own disclosure.
- Targeted memory greps (`grep -ril -F` over memory/percolator/candidates.jsonl,
  memory/capability_manifest.md, memory/runs/gapwave, memory/rib): aerovato 0,
  "cost per correct" 0, "trigger index" 0, "tokens per correct" 0, 2608.08253 0,
  session-identifier 0, liao.gg 0, routine-cleanup 0, oren198 0. The full memory/ tree
  (~550k files) was NOT swept, matching the disclosed cut of today's 10-04 quantization
  sibling; the bank-of-record plus these targeted files stand in for it.

## Honesty block

- Fetched this sitting: 26 Algolia query lanes (20 pass-1 + 6 targeted), 15 items/<id>
  thread fetches, 11 primary pages saved raw as receipts (listed in pass 2), zero 403s,
  zero degraded queries. Two pass-1 negatives and one pass-1-adjacent negative recorded as
  real negatives (sleep-time, memory consolidation, Memory-R1: nbHits 0 by-date).
- Not run: no pytest (none named by the ask); no knowledge_graph rebuild; no warm-boot
  measurement (the compaction-exam protocol from the 09-30 fold remains the OWED instrument
  for RQ5; nothing this door fetched replaces it).
- OWED, never asserted: CliffCompaction 2609.26779 abs read (next seat's first fetch);
  a measured knee number below 250k tokens (no published number found on this door;
  warm_state.json's position relative to a sub-250k knee is unmeasured, only bracketed);
  SLM 4.0's claims beyond its abstract (the 54-page body, code, and Zenodo artifact were
  not fetched); Strata's issue #210 verified only via the author's story text, not the
  issue page; Operator Memory and copeca are young low-traction repos, README-level reads,
  designs not audited systems; the medium.com self-evolving-agents post stays behind the
  fold's standing wall (fifth session).
- Door note: the recipe suggested WebFetch; raw curl/urllib was used instead against the
  same endpoints so every quote is checkable against a saved receipt file in this directory.
  No fallback success is claimed anywhere; the two failed raw README fetches (Aura, copeca
  via raw.githubusercontent 404) were retried via the GitHub HTML pages and succeeded, and
  both outcomes are recorded above.
- Em-dash scan of this file: none present; all quotes were selected to avoid dashes and
  curly punctuation was ascii-normalized (disclosed in the header).
