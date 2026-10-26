# sweep: swarm-orchestration via x (frontier_olm 20260928)

source-fetched: 2026-09-28 (stamp per ask; fetches actually performed 2026-09-29)

## Method and door health

X door as specified: WebSearch with site:x.com queries, then resolution of single posts
through https://api.fxtwitter.com/<user>/status/<id>. Door health, honestly stated:

- site:x.com is largely unindexed by the search backend; most site-restricted queries
  returned empty or irrelevant sets, and the backend itself threw 429/1302-style rate
  limit errors repeatedly mid-sweep (the sweep instrument corroborated the fan-out law
  the hard way: bursty query shapes are what get capped).
- fxtwitter resolved 5 of 5 status URLs I attempted, returning full JSON (author,
  created_at, text, engagement). Two were article-share posts; fxtwitter surfaced the
  article attachment text. One /i/article/ path (ClaudeDevs 2026-09-08 cache post) and
  one profile-only URL (@steveliles) had no resolvable status id; those are
  snippet-banked per the recipe fallback and marked as such.
- Fallback non-X sources were read end to end where reachable: 3 GitHub READMEs and 2
  Anthropic posts. Four targets degraded and are OWED, not banked (list at bottom).

Pass 1 considered 34 candidate items (list retained in session trajectory); Pass 2 read
10 items end to end: Voxyz_ai, nateherk, PawelHuryn, sawyerhood (all fxtwitter);
claude_code_agent_farm, microsoft/fides-gateway, RonenMars/threadbase (READMEs);
claude.dev harness post + claude.com GA post; openclaw docs root + releases index.
Only items I read myself are banked.

Overlap greps: catalog/catalog.jsonl + memory/ (memory/rib, memory/rib_bus,
memory/briefs, memory/workflows, memory/attention.md, memory/live_from_grok.md),
excluding memory/trajectory/steps.jsonl which is the live trajectory log of this very
run and self-matches every phrase (first grep pass proved it by matching my own query
strings). Results are recorded per item below. One re-bank caught: OmniRoute is already
banked at watch/inbox/full_blast_20260926/L01_omniroute.md (catalog id b64787a69ea7,
2026-09-26), so the JulianGoldieSEO OmniRoute post was dropped as known work.

## Verdicts per research question

RQ1 dispatch shapes under provider caps vs the estate's retry-on-shape
(maxAttempts 0 workflow children, retries on the main-session path, AGENTS.md fan-out
width law): no published design I read puts retry ownership at the dispatch-shape
layer. Peers pace or shrink instead of re-shaping: agent_farm uses adaptive launch
stagger that halves on success and doubles on failure capped at 60s, plus batching for
50+; Voxyz_ai manually dropped concurrency from 8 at a time (hit usage limits twice,
12M tokens burned) to groups of 3 with zero errors in 24 agents; @steveliles asks for
pause-until-reset with auto-resume and estimates ~15% of his tokens lost to redone
subagent work, i.e. the retry-on-children-shape he lacks is precisely what the estate
has. Verdict: the estate's shape is matched by no read source; closest neighbors are
pacing (stagger) and shrinking (groups), both of which pay in wall-clock or in redo.

RQ2 handoff/dispatch protocol vs burn-lane + rib_bus: Threadbase (Temporal durable
pipeline) is the strongest read answer: worker -> reviewer -> sign-off stages, each
independently retriable, event-sourced, caller-facing workflow IDs, scale by adding
workers to one task queue. Its README explicitly positions against Claude Code dynamic
workflows as session-scoped and dying with the session. That durability + caller IDs is
what rib_bus's file rows do not carry. moltbook's admission thesis (below) matches the
estate's queue/gate instincts: failures blamed on coordination are usually admitted
before coordination ever runs. A2A-under-Linux-Foundation claims surfaced only in
search summaries (kodekloud) I did not deep-read: OWED.

RQ3 MCP multi-server orchestration vs the estate bridge (tools.TOOL_MAP,
ROLE_TOOLSETS in mag/mcp_server.py, effect_broker chain; R1-R5 unimplemented):
microsoft/fides-gateway is the pattern to steal from: one FastMCP proxy per upstream
mounted under /mcp/<server_id>/ on a single ASGI app, upstream identity hidden behind
the proxy's server_id, information-flow labels riding in _meta, and Rego policies that
can call upstream tools directly (upstream.<ToolName>(args)) so policy checks can fetch
live evidence. Contrast with the estate bridge's one-tool-per-verb estate_ prefix:
fides namespaces at the path layer and hides the upstream, while the estate exposes
verbs and keeps isError in-band. For R1-R5 the transferable idea is labels-in-_meta
plus policy-callable upstreams as the authority-chain enforcement point. Caveat: repo
last pushed 2026-07-10 (gh api, verified), 2 stars, research prototype.

RQ4 mid-run steering (reviewer feedback revising in-flight asks): the published
engines steer coarser than the estate's gate. Anthropic's harness post describes
interrupt + session resume ("pick up where it left off") and prompt-stated token
budgets; the GA post adds that coordination happens outside the conversation and org
admins can disable workflows. sawyerhood's middleman (Feb 2026, out of window, read
anyway) is the nearest peer shape: a manager agent as "an intelligent event bus", an
agentic merge queue as "the real star of the show", reviewer feedback looped back into
the manager, with the author flagging "you're ceding control to the model". None of the
read sources describe reviewer-driven revision of in-flight asks as a first-class
engine primitive; that remains estate-distinct (workflow_gate steering dogfood).

RQ5 50-wide failure modes vs first-contact-as-HOLD: peers report width ceilings
backed by numbers, not HOLD doctrine. agent_farm: 20 default, 50 max_agents default
cap, "Consider running in batches for 50+ agents", ~500MB RAM per agent, restart loops
backed off 10s doubling to 5min, agents disabled after max_errors=3, heartbeats stale
at 2 minutes. Voxyz: 71 agents at width 8 burned the weekly limit too fast; groups of 3
threw zero errors. The official GA post says "tens to hundreds of parallel subagents"
with no numeric cap and recommends scoped first runs. @steveliles's ~15% token-loss
estimate is the clearest published cost of the failure mode HOLD exists to prevent.
Verdict: the estate's first-contact-as-HOLD (children retry internally, nothing lost)
diverges from peers, who treat first 429 as a pacing problem to avoid via stagger or
shrinking; nobody I read publishes the HOLD-first rule.

## Item register (banked; strongest first)

1. Voxyz_ai, 2026-09-27, x.com/Voxyz_ai/status/2104254744722383210 (fxtwitter
   resolved, in-window). 105-agent Opus 5.5 skill-mining run: 71 agents 8-at-a-time,
   12M tokens, limits hit twice, then groups of 3 with zero errors, done-marker files
   for resumable reruns, effort dial per stage (low mine / medium write / high review /
   xhigh decide), script shown before run. Overlap: "8 at a time" 0 in catalog, 0 in
   memory (trajectory excluded). Confidence 0.9.
2. claude_code_agent_farm README (github.com/Dicklesworthstone/claude_code_agent_farm,
   pushed 2026-09-21 per gh api). Adaptive stagger halving on success and doubling on
   failure capped 60s; batches for 50+; restart backoff 10s to 5min; max_errors=3
   disable; 2-minute stale heartbeat. Overlap: 0 catalog, 0 memory. Confidence 0.85.
3. @steveliles reply to @ClaudeDevs (x.com/steveliles; status id absent from search
   result, unresolvable via fxtwitter: snippet-banked per recipe fallback, date
   unknown, reply-context 2026-09-08). Pause-until-reset + auto-resume feature ask;
   ~15% of tokens lost through subagents redone on rate limit. Overlap: "pause until
   the limit" 0/0. Confidence 0.75.
4. moltbook post 7a1ada2c-0d8d-4af9-8841-a912ecb8b769 (title-only; body is
   JS-rendered and unreadable by fetch: degraded, snippet-banked). Thesis: "multi-agent
   systems don't fail at coordination, they fail at admission"; sibling post: orchestration
   is "distributed debugging with better branding". Date unknown. Overlap: 0/0.
   Confidence 0.6.
5. microsoft/fides-gateway README (pushed 2026-07-10, flagged out-of-window; gh api
   verified). Multi-server MCP proxy, proxy-per-upstream under /mcp/<server_id>/,
   IFC labels in _meta, Rego eval_policy on every proxy, policies may call upstream
   tools. Overlap: 0/0. Confidence 0.9.
6. RonenMars/threadbase-multi-agent-orchestration README (pushed 2026-06-22, flagged
   out-of-window). Temporal durable pipeline, worker -> reviewer -> sign-off, per-stage
   retries, deterministic workflow code with effects confined to activities, explicit
   contrast table vs dynamic workflows. Overlap: 0/0. Confidence 0.9.
7. Anthropic, "A harness for every task: dynamic workflows in Claude Code"
   (claude.dev, 2026-06-02, flagged out-of-window; foundational for RQ4/RQ1 framing).
   Names the three model-driven-orchestration failure modes: agentic laziness,
   self-preferential bias, goal drift; interrupt + resume; per-agent model and
   worktree choice. Overlap: "harness for every task" 0/0, "agentic laziness" 0/0,
   "goal drift" 0/0 in catalog/memory doctrine dirs. Confidence 0.9.

Dropped as re-bank: JulianGoldieSEO OmniRoute post (2026-09-15, fxtwitter resolved) —
OmniRoute already deep-read in estate at watch/inbox/full_blast_20260926/L01_omniroute.md.
Dropped as out-of-window though read: nateherk (2026-05-30, 41 Haiku agents, 5M input
tokens, "One prompt cost me half my monthly plan in 30 minutes"), PawelHuryn
(2026-06-08, 113 agents / 1.95M tokens / 12 minutes, "Agents cost tokens. The glue is
fast, free, and deterministic.", three failure modes credited to the Anthropic post
above), sawyerhood (2026-02-27, middleman/merge queue). All three corroborate items 1,
7 and the RQ4 verdict.

## OWED (could not verify; not banked, not asserted)

- towardsai "How Do You Stop It? Cancellation Semantics for Long-Running Agents"
  (Shrashti Singhal, 2026-09-16): WebFetch 403, web_reader 500, freedium DNS fail.
  Metadata only.
- TrueFoundry "The Managed Agent Layer and Runtime Separation" (2026-09-11 snippet:
  backoff, circuit breakers, dead-letter queue): correct URL never located; first slug
  404'd. Snippet only.
- code.claude.com "fewer than 50 agents" guidance: docs URL not found (dynamic-workflows
  path 404s); claim exists only in a search summary.
- openclaw v2026.8.1 "429 provider errors" + "malformed Retry-After" release-note line:
  from a search snippet; the releases index page (read) shows v2026.9.6..v2026.6.11 but
  carries no such line; release is also outside the 30-day window.
- smithers.sh "Live UIs and the Gateway": page is a JS app, no readable content.
- kodekloud / gurusup A2A-vs-handoff claims: search summaries only, not read.
