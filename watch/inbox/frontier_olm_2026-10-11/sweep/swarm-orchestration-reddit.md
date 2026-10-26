# Frontier sweep: swarm-orchestration via reddit (2026-10-11)

source-fetched: 2026-10-11. Seat: sweep-swarm-orchestration-reddit (dynamic workflow child).
Lane context: this is the FOURTH reddit pass over this area (10-03 window 1: 8 items,
10-03 window 2: 8 items, 10-10: 8 items, all read + registered). The burn lens
(frontier_olm_2026-10-11/lens/burns.md:110-111) says a fourth pass needs a named new
window. This pass's named new windows: (a) PRE-SEPTEMBER threads the three prior sweeps
could never see (their crawl windows were 2026-09-03..10-05 and 09-10..10-10), surfaced
through the search fallback; (b) the r/AI_Agents below-cut tier; (c) held-thread deltas.

## Door status (degraded, no fabrication)

- Recipe door `old.reddit.com/r/LocalLLaMA/top.json?t=month&limit=50` via WebFetch:
  returned Reddit's "Welcome to Reddit" shell, zero JSON. Same for the HTML top listing
  and `www.reddit.com/r/LocalLLaMA/top/?t=month` via web_reader (login-walled, ~3 posts
  rendered). `old.reddit.com` via web_reader: "Log in to use old Reddit". DEGRADED.
- WebSearch with `site:reddit.com`: the backend ignored the site filter and returned
  generic non-reddit pages on strict queries; broader phrasings DID surface reddit thread
  leads (the pre-window set below came from these searches). Used as the recipe's
  fallback door, with degraded-door status recorded.
- WORKING READ DOORS this sitting: (a) Reddit RSS via WebFetch -
  `https://www.reddit.com/r/SUB/top/.rss?t=month` returned full 22-25-entry listings for
  LocalLLaMA, ollama, LocalLLM, and thread `.rss` feeds returned OP + comments for 7 of
  8 threads attempted (one 429, one CAPTCHA shell via web_reader, both then fetched via
  the RSS door); (b) web_reader MCP on thread pages (worked until Reddit CAPTCHA'd it).
- r/MachineLearning: top-month thread list retrieved through WebSearch (its .rss read
  March-dated entries = stale/slow sub); no in-window ML-subreddit thread banked.

## Pass 1 (broad sweep, last 30 days)

Candidates considered: 25 (r/LocalLLaMA top-month RSS) + 22 (r/ollama top-month RSS) +
25 (r/LocalLLM top-month RSS) + ~10 search-surfaced threads (r/AI_Agents, r/vibecoding,
r/LLMDevs, LLM-council and debate threads) = ~82. Well over the 30-candidate floor.
Key pass-1 finding: the in-window top-feed candidate pool is TRIPLE-COVERED - the three
prior sweeps already hold the strongest in-window orchestration threads (Slow Vale 800
agents 1x0ms0m, agent swarm coordination 1wu3rio, 18 RAG pipelines 1wv0lww, speculative
reward hacking 1wsuag0, KV transplant 1wq76f6, 400-agent MMO 1wt0tot, concurrency
envelope 1wb35xo, subagent economics 1wbc03f, wave scheduling 1wpxh2g, session resets
1wvpffv, handoff files 1wui0hj, quota fencing 1woj7dv, retry-safety 1wv66mt, Opus
self-review 1wqnjkp, tool timeout tri-state 1wv66mt, cheap-tier demotion 1wtmhgw).

## Pass 2 (deep reads this sitting: 9 threads end to end via thread .rss, OP + comments)

Held re-confirmation reads (NOT re-banked; already in prior sweeps' registers):
1. 1wt0tot 400-agent MMO (r/ollama 09-29; already in 10-03 w2 item 7 + 10-10 item 7;
   raw also at frontier_olm_2026-09-30/sweep/_raw/deep_1wt0tot_*.json).
2. 1whqwdq Qwen 30-day run (r/LocalLLM 09-16; already 10-03 kv-cache sweep finding 5).
3. 1wj0arv Six-days Mac assistant (r/ollama 09-17; already 10-03 kv-cache sweep finding 2).

Genuinely NEW items banked below: 6.

---

### 1. "When running multiple agents in parallel... how do you stop them from stepping on each other?"
r/AI_Agents | 2026-03-19 | https://www.reddit.com/r/AI_Agents/comments/1ry7qmc/
Read: full OP (via web_reader page fetch) + 19 comments (via thread .rss). OUTSIDE the
30-day window (pre-dates the prior sweeps' crawl windows); dated from the feed.
> "stop trying to coordinate and just isolate."

Practitioner census of shared-state failure at width: single agents fine, 3-5 parallel
(planner/researcher/implementer/reviewer) redo work, contradict each other, lose state
on restart/compaction; OP's diagnosis: "If each agent has its own private context window,
the system has no consistent reality." Convergent fixes across 19 comments:
(a) isolation over coordination - git worktrees per agent, agents read a shared md at
repo root but rarely write, file locks for exclusive resources, 30s wait-and-retry on
build errors in untouched files (u/Deep_Ad1959, runs 5-6 agents on one codebase daily,
shared DB became "a junk drawer in 3 days"); (b) task-claiming as mutex - ticket/token
so only one agent works a project (u/EntertainmentAOK); (c) namespace per workflow run,
workers read-only on shared state, only the coordinator writes canonical state, persist
to KV/disk because "Context windows are scratch pads, not storage", knowledge graphs
"only needed past ~10 agents" (u/Sudden-Suit-7803); (d) no shared state at all -
planner splits dependency-ordered areas, one main writer consolidates (u/Map7928);
(e) the P2P counter-case (u/P0orMan: central DB is a bottleneck and single point of
failure, pitch ClawNet github.com/chatchattech/clawnet) met with the exact
consensus-illusion question: "how do you keep consensus from agreeing on wrong
conclusions?"
Estate read: the five-axis emergent-vs-deterministic question (lens/laws.md:61) in
practitioner form - what survives width is isolation + claim-by-ticket + a single
canonical writer, i.e. deterministic structure carrying stochastic workers. Directly
feeds the flock decode redesign (lens/laws.md:87): decode must map to actual task
output space, and this thread says the same about shared state - the shared surface
must carry task-space artifacts, not conversation. Bank as the strongest new find.

### 2. "The biggest mistake I see in multi-agent systems"
r/AI_Agents | 2026-02-24 | https://www.reddit.com/r/AI_Agents/comments/1rdmrfu/
Read: full OP + 12 comments via thread .rss. OUTSIDE the 30-day window.
> "Agents don't fail because they're not smart enough. They fail because we over-LLM the pipeline."

The deterministic-core law, practitioner edition: "the stable pattern is: Deterministic
core - AI only at uncertainty boundaries - Explicit state machine - Logged transitions";
retrieval should be "boring and deterministic" because "LLM for structured retrieval is
paying for randomness you don't need"; synthesis/cross-signal interpretation is where
the model earns its keep ("this renewal risk correlates with support ticket volume from
3 weeks ago"). OP on scope: "The key is controlling transitions, not the model" - a
deterministic core is just an explicit state machine, strict tool schemas, clear
success/failure transitions, logged state; "controlled autonomy tends to survive longer
than pure systems." The dissent (u/LegitimateNerve8322: "I wouldn't call that an agent
but instead an llm assisted workflow") and the synthesis (u/GeeBee72: agentic processes
mine past behavior for deterministic patterns and an "architect agent" updates the
deterministic core bus) are both worth keeping - the second is the estate's
mechanism-improves-itself falsifier (RIB_TEN_MINUTE_SELF) in outside form.
Estate read: RQ4 (would the GSTD runners pass the five-axis gates vs a deterministic
single seat) - this thread is the practitioner prior that the deterministic core is the
baseline to beat, and names the exact axes (debuggability, reproducibility, cost
control) that an A/B harness should measure. Zero overlap on grep.

### 3. "8 local LLMs on a single Strix Halo debating whether a hot dog is a sandwich"
r/LocalLLaMA | 2025-12-03 | https://www.reddit.com/r/LocalLLaMA/comments/1pdh0sm/
Read: full OP comments + ~80 comments via thread .rss. OUTSIDE the 30-day window (10
months old) but the most directly GSTD-relevant artifact found on any reddit door:
AMD shipped the harness OPEN SOURCE (Apache-2.0, Lemonade v9.0.7, Debate Arena v2 in
PR #659, 8 llama-server processes, models 3-8B, --max-loaded-models 8).
> "Rounds 2 and 3 they're supposed to react to each other (shared chat history). Rounds 4 and 5 they're supposed to vote."

Heterogeneous 8-model consensus, run live, tie outcome ("Just like people!"). The
comment thread contains the exact design fork the GSTD consensus harness and the
consensus-illusion rib sit on: u/r4in311 - "letting each model form an independent
opinion before seeing others' takes to avoid influence" (independent-then-vote) vs the
shared-history debate rounds; u/Practical-Hand203 - "Congrats, you've reinvented
ensembling"; u/JaceBearelen asked for spawn-agents-until-k-votes; u/NodeTraverser
wanted 9 voters ("like the Supreme Court") for tie-breaking. The shared-history rounds
are precisely the style-attraction hazard the banked personas paper measures
(adhoc register, Disentangling Models from Personas, 2610.07535: base-model identity
drives engagement and gpt-oss is a universal attractor as mixture widens).
Estate read (RQ1 + RQ3): runnable Apache-2.0 code for heterogeneous model debate+vote
that the flock decode redesign could fork instead of hand-rolling; its
independent-first-then-vote comment is a decode-space design the consensus-illusion rib
predicts should beat shared-history rounds on grounded tasks - a concrete A/B the
GSTD runners could run against the dead-salmon null. Zero overlap on grep.

### 4. "Tried a 'multi-agent debate' approach with LLMs and the answers were surprisingly better"
r/LocalLLaMA | 2026-03-09 | https://www.reddit.com/r/LocalLLaMA/comments/1rowsgc/
Read: full OP + 4 comments via thread .rss. OUTSIDE the 30-day window.
> "the critic agent needs a different system prompt than the generator, otherwise it just rubber-stamps everything"

Practitioner debate-loop doctrine from a production multi-agent operator (u/Ok_Diver9921):
critic needs a different system prompt from the generator or it rubber-stamps; critic
temperature set "slightly higher... so it actually pushes back"; mid-tier models
(Qwen3, Llama 3.1 70B) work "surprisingly well as critics even if your generator is a
bigger model" - family/size separation of critic from generator. Plus tiered routing
(cascadeflow, github.com/lemony-ai/cascadeflow) and event-sourced coordination ("each
agent writes its response as an event, the orchestrator reads the event stream to
decide who goes next", github.com/fastpaca/starcite).
Estate read (RQ1 + RQ5): the critic-separation rule is the cheap fix for the
consensus-illusion's rubber-stamp failure mode (flock consensus strength does not
predict correctness, lens/laws.md:60): consensus quality depends on the critic being a
DIFFERENT animal/prompt, not on vote count. Zero overlap on grep; the two tool repos
(cascadeflow, starcite) are new tool leads.

### 5. "Built an SQLite-based memory system for Ollama that doesn't eat all your VRAM" (Hillock, v0.7-era)
r/ollama | 2026-10-01 | https://www.reddit.com/r/ollama/comments/1wuv6oh/
Read: full OP + 2 comments via thread .rss. IN-WINDOW.
> "it stores bound triples instead of loose text chunks"

Delta over the already-held Hillock rows (10-03 agent-memory sweep holds 1vnhojf
"Hillock v0.4 SQLite SPO triples"; 10-03 open-models pool lists 1wwn7xf "Hillock
hypervectors"): this post names the mechanism that makes the hypervector check work -
bound triples (ProjectA -> uses_db -> Postgres) whose hyperdimensional binding makes
Project A's database hypervector "practically orthogonal to Project B's", Hebbian links
keeping clusters separate, and a v0.7 disambiguation mode that "stops and asks which
project you mean rather than hallucinating or blending both". Facts extracted by
sub-300MB models (~5s/doc), knowledge-existence check before answering, <1.2GB VRAM.
Estate read: fills part of the adhoc DIGEST's gap (agent-memory-continuity had zero
confirmed finds, burns.md:107-108): the anti-hallucination gate is a pre-answer
knowledge-existence test - the same shape as the claims desk (a claim is sat only when
a primary record is on the table). The ask-before-guess disambiguation mode is the
empty-claim law implemented in a consumer tool.

### 6. "Deterministic vs. flexible agent orchestration - how are you drawing the line?"
r/AI_Agents | 2026-02-13 | https://www.reddit.com/r/AI_Agents/comments/1r3wxal/
Read: full OP + available comments via thread .rss; TWO SUBSTANTIVE COMMENTS WERE
DELETED (only the OP's replies to them survive) - caveats recorded, quotes taken only
from surviving text. OUTSIDE the 30-day window.
> "Hard caps (5 LLM calls, 15 tool calls, 2 replans)"

A stateful-ops practitioner moving from an unbounded tool loop ("great for demos,
nightmare in production") to a deterministic graph: LLM picks capability and plans,
validation/execution stay deterministic; the escape hatch is finite by design ("you
have 3 calls to route yourself or escalate" - bounded exploration); hard caps framed
as SECURITY, not cost; rollback rejected as automatic, checkpoint snapshots +
user-initiated recovery preferred; confidence thresholds (high -> proceed, medium ->
clarify with context, low -> must clarify).
Estate read (RQ4 + RQ5): independent practitioner statement of the workflow-gate's
exit-2 hard-block shape and of the fan-out width law's cap (per-invocation bounded
calls). Weakest of the six (deleted answers), but the surviving OP text alone carries
the finding.

---

## MASS / RQ2 note (honest zero)

No reddit thread discussing MASS (arXiv 2610.12176) surfaced on any door this sitting
(search returned the arXiv abstract, pub.sakana.ai, alphaxiv, and the already-held
awesome-rsi map only). The MASS body-read debt is already covered by the adhoc
register's first-hand row (frontier_olm_adhoc/register.jsonl, swarm-orchestration row 1,
quote-verified with the synthesized-paraphrase erratum recorded there). Do not re-open.

## Overlap record (commands run this sitting)

- `grep -c -i <term> catalog/catalog.jsonl` for: 1ry7qmc, 1rdmrfu, 1r3wxal, 1pdh0sm,
  1rowsgc, "over-LLM the pipeline", "uncertainty boundaries", "stepping on each other",
  "rubber-stamp", "cascadeflow", "starcite", "ClawNet", "bound triples", "controlled
  autonomy", "Debate Arena" - ALL 0 hits.
- Bounded memory grep (`memory/frontier memory/press memory/lenses memory/improve
  memory/rib memory/briefs memory/knowledge_graph.json` +
  frontier_olm_adhoc/register.jsonl + frontier_olm_2026-10-05/register.jsonl): all 0,
  EXCEPT "stepping on each other" -> memory/knowledge_graph.json, which is the estate's
  own line_builder purpose string ("builds a file LINE BY LINE without stepping on each
  other") - coincidental phrase, not prior art.
- Held-thread checks (dedup, not banking): 1wt0tot/Hillock/Dflash greps against
  catalog.jsonl surfaced the prior sweeps' own raw files (frontier_olm_2026-09-30/
  sweep/_raw/deep_1wt0tot_*.json, frontier_olm_2026-10-03/sweep/tmp/sw2_item_1wt0tot.json,
  state/tmp_sweep/*hillock*.html) and register mentions (10-05 register.jsonl,
  10-03 swarm + kv-cache + agent-memory sweep files) - read and honored, those threads
  are NOT re-banked.
- A full `grep -r` over all of memory/ was started and KILLED as too slow (>9 minutes on
  the first pattern); the bounded research-dir set is the same instrument the 10-10
  sweep's overlap record used. Recorded per the counts law (different instrument than
  the killed run; no counts differenced across instruments).

## Method notes

- Instruments: WebFetch against Reddit RSS endpoints (top/.rss?t=month for 3 subs; 7
  thread .rss feeds end to end), web_reader MCP (thread pages + top listings until the
  CAPTCHA wall), WebSearch fallback (lead discovery only), repo greps as listed.
- Dates are the post dates the fetched feeds/pages show; three banked items predate the
  30-day window and are marked OUTSIDE THE WINDOW - they were surfaced by this sitting's
  fallback door and are new to the estate's holdings, which is the banked-value
  criterion, stated rather than hidden.
- Not run: no pytest/census instruments - research sweep only; no code executed against
  estate surfaces. No fresh read of the MASS paper (covered by the adhoc register).
