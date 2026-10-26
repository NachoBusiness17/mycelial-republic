# stealth-sw-03: Economics of AI agent swarms (cost per useful output, free vs paid, the quality-price frontier)

Produced 2026-09-29 by seat stealth-sw-03 (dynamic-workflow gopher). Method: 3 asks
dispatched through the free-lane fanout pattern (`tools/stealth_fanout.py` lanes,
dispatch wrapper in `watch/inbox/burn_reset_20260927/flash50/_sw03_dispatch.py`) plus
WebSearch/WebFetch. Per RIB_DRIVING_LADDER_20260928.md:14-23, free-lane output below is
SENSING (banked as findings, never trusted work); anything load-bearing was verified
against a primary source in this session or is flagged OWED.

## 1. Cost per useful output: the agentic token multiplier

Primary source, fetched this session (WebFetch on
https://www.anthropic.com/engineering/built-multi-agent-research-system): Anthropic's
multi-agent research system writeup states agents consume "about 4x more tokens than
chat interactions" and multi-agent systems "about 15x more tokens than chats." Token
usage alone explained 80% of performance variance on BrowseComp; adding tool-call count
and model choice explains 95%. Two economic corollaries from the same post: upgrading
Sonnet 3.7 to Sonnet 4 yielded more than doubling the token budget on Sonnet 3.7, and
multi-agent architectures "burn through tokens fast" so they need tasks valuable enough
to justify the spend. Secondary writeups found by search put output tokens at a 3 to 8x
price premium over input across providers, which amplifies the multiplier because
agents are output-heavy.

A workable cost model (offered by the ling-3.0-flash-sante:free sensing lane,
_sw03_out_sw-econ-1_inclusionai_ling-3_ling.md): cost per useful output = (input
tokens + output tokens + tool-call tokens) x per-token price x retry/loop factor x
number of agents. The lane correctly declined to fabricate per-task dollar figures for
production swarms and marked them OWED; public vendor numbers are per-token rates, not
per-completed-task rates.

Local primary data grounds the throughput side. This estate's own receipts: Task
agents measured clean at widths 3, 6, 10, 12 with width 10 banking 109.4M tok/h and
zero surfaced 1302s (AGENTS.md fan-out width law; receipts watch/inbox/GALA_20260925.md
and watch/inbox/burn_wave_20260926/B2_25_envelope_remeasure_20260926.md). First
rate-limit contact on the workflow-child shape came at 5 gated workflows x
max_concurrency 10 (50 children) plus hourly cron plus offpeak tasks
(ENVELOPE_50W_HIT_20260926.md:3-9); the operator held width because children retry
429/1302s internally, making the limit a throttle rather than a loss. That is the
reliability axis of cost per useful output: paid capacity buys retry absorption, so
"cost per task" includes the failure tax.

## 2. Free-tier API models vs paid models for production

Provider-term findings from search: Cohere trial keys are documented as free but
rate-limited and "not for production," production requires pay-as-you-go; Gemini keeps
a genuinely free API tier with rate limits while paid Flash-class runs near $0.75 to
$1.50 per million input tokens at the low end; OpenRouter `:free` model terms are
inherited per-provider and can be retired without notice; frontier API usage is billed
separately from product tiers and "can scale quickly on agent-heavy workflows."

This session added a measured free-lane failure census (all commands run here, venv
python `watch/inbox/burn_reset_20260927/flash50/_sw03_dispatch.py`):

- Run 1: 0/3 banked. stealth/space-bunny-alpha returned empty content after 34.1s
  (completion budget burned as reasoning); meta/muse-spark-1.3 returned HTTP 403
  Forbidden on this key; ling-3.0-flash-sante:free hit finish_reason "length" at a 900
  max_tokens cap with all 977 completion tokens spent as reasoning and zero content
  (usage JSON shows cost $0 for the attempt, which is still 100% waste when the output
  is empty).
- Lane rot between runs: llm7's anonymous gpt-4o-mini is retired (HTTP 400
  model_unavailable; live GET /v1/models lists 40+ successors); glm-5.3 on the same
  anon lane now returns HTTP 401 Unauthorized, so the keyless free surface narrowed
  within one day of the last fanout.
- Run 2 after parser fix (read msg.reasoning fallback, 3000-token budget, lane
  remap): 2/3 banked, ling at 9.0s/2196 chars and stealth at 50.5s/11754 chars.
- Session bill: 6 dispatch attempts, 4 failed or needed repair, 2 clean. The repairs
  (parser, budget, model names, NTFS path bug) are unpaid engineering labor that paid
  lanes do not charge. The fanout pattern itself has a win32 defect:
  tools/stealth_fanout.py:135 slugs output filenames replacing only "/", so model
  "ling-3.0-flash-sante:free" writes to an NTFS alternate data stream and leaves a
  0-byte base file; recovered here by reading the ":free.md" stream.

The estate already encodes the operating conclusion: RIB_DRIVING_LADDER_20260928.md:8-23
makes funded Nous credits the workhorse/judgment tier and free stealth lanes a sensing
tier whose outputs are "banked as findings, never as done-work," with the climb rule
that sensing may feed judgment but never substitute for it. This session proved the
rule empirically: the ling lane declined to verify Anthropic's 4x claim and marked it
OWED; the same claim was verified at the primary source minutes later.

## 3. The quality-price frontier

Corroborated by four independent search hits: FrugalGPT (Chen, Zaharia, Zou;
arXiv:2305.05176, TMLR 2024) matches the best individual model with up to 98% cost
reduction via prompt adaptation, approximation, and cascades, or improves accuracy
about 4% at equal cost, escalating only roughly 1 in 6 queries to the large model.
Successors in the search corpus: RouteLLM (LMSYS, preference-data routers),
RLM-Cascade, AgentRouter, PILOT contextual-bandit routing, AutoMix.

Artificial Analysis makes intelligence-per-dollar the headline production metric:
"a model that's slightly less capable but 10x cheaper may win for many production use
cases" (artificialanalysis.ai microeval page, fetched via search) and its Intelligence
Index v4.1.1 publishes cost-per-task comparisons (about $27,500 per 10,000 tasks for
one frontier model vs about $15,400 for another, per its LinkedIn announcement). Epoch
AI publishes performance-per-dollar trends. The frontier's price floor keeps collapsing
(2026 comparison guides rank "maximum intelligence per dollar" as the dominant axis).

Sensing-lane contribution (stealth/space-bunny-alpha, 11.7k chars of reasoning,
unverified): DeepSeek-R1 paper distillation numbers (R1-Distill-Qwen-32B near o1-mini
on math/code benchmarks at a fraction of serving cost), Orca, Distilling Step-by-Step,
Phi-3 as the small-model-value lineage. Caveat that validates the sensing tier: the
same lane misattributed FrugalGPT's first author and hedged its own recall of the 98%
figure, so every number it emitted stays OWED until checked against the named papers.

## 4. Synthesis

The frontier is three-axis, not two. Quality-per-dollar (FrugalGPT lineage, AA value
index) says route cheap models to easy steps; the Anthropic budget finding says model
quality can dominate raw token budget at the top end; and this session's failure census
says reliability and repair labor are the hidden third axis. Practical shape for swarm
economics: free tiers win sensing (broad, cheap, disposable asks whose outputs get
verified), paid funded tiers win production judgment (SLA-free free tiers + retry
absorption + no silent endpoint retirement), and cost per useful output should be
accounted as tokens x price x retry-factor x agent-count x verification-labor, with the
last term dominating exactly when lanes are free and flaky.

## Provenance and OWED

Ran this session: `./.venv/Scripts/python.exe watch/inbox/burn_reset_20260927/flash50/_sw03_dispatch.py`
(twice, heartbeat _sw03_heartbeat.jsonl), the inline single-ask rerun on the ling lane,
GET https://api.llm7.io/v1/models (40+ live models listed), NTFS ADS recovery of the
two 0-byte ling base files, WebFetch on the Anthropic engineering post, and 6 WebSearch
queries (3 first-hit 429/1302 rate-limited, 3 returned results). Banked lane outputs:
_sw03_out_sw-econ-1_inclusionai_ling-3_ling.md (2041 chars),
_sw03_out_sw-econ-2_inclusionai_ling-3_ling.md (2317 chars),
_sw03_out_sw-econ-3_stealth_space-bunny-alpha.md (11968 chars).

OWED (not verifiable in this session): exact current Gemini free-tier training-use and
Groq free-tier commercial clauses; RouteLLM's exact savings percentages; all DeepSeek-R1
distill benchmark figures (sensing-lane recall only); Artificial Analysis per-model
index values beyond the quoted microeval sentence; any standardized public "cost per
completed agent task" table, which the ling lane correctly called unsourced.
