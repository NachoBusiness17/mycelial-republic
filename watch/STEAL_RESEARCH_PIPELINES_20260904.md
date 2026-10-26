# STEAL — RESEARCH PIPELINES: how the field harvests (2026-09-04)

Competitive steal, GO 2026-09-04. Question: how do research labs, OSINT teams, and
AI-native indie researchers automate RESEARCH HARVESTING today — beyond X? Seven pattern
families swept: arXiv-sanity/alphaXiv feeds, HN firehose watchers, RSS-Bridge setups,
paper-tweeting bots, agentic browsing researchers, newsletter-digest pipelines,
citation-graph crawlers. Tri-state throughout, every claim sourced.

Organ mapping used below (per AUTONOMY_WHEEL_20260904.md): **SCOUT** = active queries into
sources (grok complex research, For You, grok CLI) · **MONITOR** = standing passive
watchers (the harvest spoke's zero-touch lane) · **INTAKE** = scoring → tri-state verdict
cards · **WHEEL** = the loop itself — build/verify/refit/remember.

Headline finding: **every serious pipeline in the field has the same skeleton — free
standing pipes → cheap lexical prefilter → LLM only on survivors → idempotent archived
state → scheduled re-run. The premium tokens burn at the SCORING layer; the pipes
themselves cost nothing.** The fleet owns the expensive half (intake genome, march-228
triage at ~$0.09/window) but its scout half still routes through a paid deck. The field
runs scouts on keyless public APIs. That is the steal.

---

## 1. ARXIV-SANITY / alphaXiv-STYLE FEEDS — the personal paper radar

**What it does.** Karpathy's arxiv-sanity-preserver: a personal radar over the daily
arXiv firehose — keep track of recent papers, search, sort by similarity, and a
"recommended for you" feed learned from what you liked
([karpathy/arxiv-sanity-preserver](https://github.com/karpathy/arxiv-sanity-preserver)).
alphaXiv is the institutional successor shape: discussion layer on every arXiv paper (swap
"arxiv"→"alphaxiv" in any URL), AI blog summaries per paper, and an MCP server that
returns a paper as a **structured AI report optimized for LLM consumption** — no PDF
parsing ([alphaxiv.org](https://www.alphaxiv.org/), [alphaXiv MCP docs](https://www.alphaxiv.org/docs/mcp)).

**Mechanism.** No deep learning: crawler pulls recent submissions → extracts text →
TF-IDF vectors → a linear **SVM trained on your liked papers vs. the corpus** scores
everything new (Wang 2024, [arXiv:2404.06364](https://arxiv.org/pdf/2404.06364); Synced on
covid-sanity, [syncedreview.com](https://syncedreview.com/2020/03/31/covid-sanity-interface-elegantly-and-efficiently-organizes-web-covid-19-papers/)).
A 2021 systematic study of scholarly recommenders found classic TF-IDF/BM25 **beat modern
embeddings** for this task ([PMC8378599](https://pmc.ncbi.nlm.nih.gov/articles/PMC8378599/)).

**The steal.**
- INTAKE — we already produce labeled verdicts at scale (376 KEEP / 142 ACTION / 139
  DISCARD in march 228). That is a training set. Stand up the same cheap ranker: TF-IDF
  over our own KEEP corpus, score each new harvested item **before** it burns premium
  tokens; lexical prefilter decides who reaches the LLM scorer. Supported mechanism,
  fleet-side application Unproven until flown.
- SCOUT — the alphaXiv URL-swap: any arXiv id intake flags gets its structured alphaXiv
  report fetched instead of parsing the PDF. Supported (official MCP docs).

## 2. HN FIREHOSE WATCHERS — standing keyword alerts on a free firehose

**What it does.** Keyword-alert services and trend watchers monitor HN's public story +
comment stream continuously (Syften: [syften.com/hackernews](https://syften.com/hackernews);
a weekend trend tracker with keyword alerts:
[dev.to guide](https://dev.to/badmonster0/i-built-a-real-time-hacker-news-trend-tracker-in-one-weekend-step-by-step-guide-57n4)).

**Mechanism.** HN ships two public APIs: Algolia search (`hn.algolia.com/api`) and the
Firebase real-time firehose; practitioners note the API is effectively **non-rate-limited**
([HN thread](https://news.ycombinator.com/item?id=47115009); endpoint guides:
[Cotera](https://cotera.co/articles/hacker-news-api),
[Agent37](https://www.agent37.com/blog/hacker-news-api)). Watchers poll search-by-date for
a keyword window, diff against last-seen, alert on match.

**The steal.**
- MONITOR — a new scout lane that costs **$0 and touches no grok key**: nightly (or
  sub-hourly on a free lane) poll `hn.algolia.com` for the fleet's watch terms + terms
  mined from the starvation list, diff against a last-seen store, spool matches as raw
  intake signals. Directly diversifies the scout stack off single-vendor (deck) risk.
  Supported (API documented, free); the specific fleet query set Unproven until it
  starves or feeds.
- Bonus mechanism from the field: the signal is often in the **comments**, not the story —
  the Algolia API searches comments natively. Supported (endpoint documented).

## 3. RSS-BRIDGE SETUPS — normalize every source into one shape

**What it does.** [RSS-Bridge](https://github.com/rss-bridge/rss-bridge): self-hostable
PHP app with community-maintained per-site "bridges" (scrapers) that emit RSS/Atom for
sites that don't have feeds; lighter kin: [rsspls](https://github.com/wezm/rsspls) (Rust,
config-file page→feed).

**Mechanism.** Per-site scraper → uniform feed → any reader. One ingest contract for N
heterogeneous sources; new source = pick or write one bridge, nothing downstream changes.

**The steal.**
- SCOUT/INTAKE boundary — the fleet's version is a **bridge shelf**: every new source
  must land in the intake spool as the SAME shape (a dated markdown item with source/
  url/ts/verdict-pending header), whether it comes from grok, a native feed, an RSS-Bridge
  instance, or a 20-line scraper. The scorer never special-cases sources; a source that
  can't be bridged is a source that can't be scored. Supported pattern (field-standard),
  fleet adoption Unproven until the spool contract is written down.

## 4. PAPER-TWEETING BOTS — our own nightly harvest, mirrored by the field

**What it does.** Daily arXiv digests auto-published: twXiv tweets daily submissions
([github topics/arxiv-daily](https://github.com/topics/arxiv-daily)); keyword/category
watchers on GitHub Actions cron every 12h merging results into JSON archives
([monologg/nlp-arxiv-daily](https://github.com/monologg/nlp-arxiv-daily),
[zhuwenxing/daily_arxiv](https://github.com/zhuwenxing/daily_arxiv)); GPT-scored daily
scanner with **author matching** ([tatsu-lab/gpt_paper_assistant](https://github.com/tatsu-lab/gpt_paper_assistant)).

**Mechanism.** arXiv API query by category → keyword/LLM filter → post via API → merge
into idempotent JSON archive. Scheduler = GitHub Actions cron (free, no server).
Tutorials confirm the skeleton end-to-end
([FeederBot](https://wangcongcong123.github.io/FeederBot/),
[LangChain summarizer bot](https://levelup.gitconnected.com/build-a-twitter-bot-for-arxiv-paper-summarization-by-openai-and-langchain-in-10-minutes-e57de6b32e03)).

**The steal.** Validation first: our nightly harvest (query → triage → archive → room row)
**is** the field-standard shape. The three add-ons the field has that we don't:
- INTAKE — **author matching**: watch a person list, not just keywords
  (gpt_paper_assistant). Our Tier kit exists on the deck; port it into harvest queries.
- WHEEL/REMEMBER — **the output is a public artifact**: bots publish their digest; ours
  files internal cards. The nightly digest could double as public content on the operator's
  X surface (doctrine-as-marketing, already operator-endorsed direction). Fleet version
  Unproven until operator picks a format.
- SCOUT infra — **GitHub Actions as free cron** for any fleet tick that needs no local
  state (pure API pulls). Supported.

## 5. AGENTIC BROWSING RESEARCHERS — the judge-loop and the evidence registry

**What it does.** AI-native indie researchers run Claude + MCP servers as **custom,
transparent, extensible** research workflows instead of one-button deep research —
Aaron Tay's thesis is that generic LLM+academic-MCP setups underperform without custom
plumbing ([aarontay.substack.com](https://aarontay.substack.com/p/creating-your-own-research-assistant)).
Multi-agent systems automate systematic literature reviews as staged sequential workflows
([arXiv:2403.08399](https://arxiv.org/html/2403.08399v2)). OSINT teams run staged,
**resumable** collection with centralized evidence/entity registries
([SYNINT](https://github.com/gs-ai/SYNINT)).

**Mechanism.** The agentic loop: LLM + tool calls in a loop until a stop condition
([Temporal cookbook reference](https://docs.temporal.io/ai/cookbook/agentic-loop-tool-call-claude-python)).
browser-use adds the distinctive piece — an **auto-research loop where a separate judge
scores agent trajectories and the verdicts feed the next iteration**
([browser-use.com](https://browser-use.com/posts/online-mind2web-benchmark)); "best
browser agent" is a vendor benchmark claim — mechanism Supported, superiority Disputed/
vendor-sourced.

**The steal.**
- WHEEL — browser-use's judge-loop is our VERIFY spoke formalized by someone else: the
  build's own word is never the receipt; a separate judge pass scores every run and the
  scores steer the next turn. Evidence the pattern scales to production browsing agents.
- WHEEL — SYNINT's three properties are our room/chain, stated as requirements: staged
  execution (our burst gates), resumable runs (our spool+state files), centralized
  evidence registry (room.jsonl → verkle knots). Field confirmation we are not
  over-engineering the REMEMBER spoke.
- Doctrine check (Disputed-relevant): Aaron Tay's finding that monolithic deep-research
  underperforms custom organ pipelines is an argument FOR the wheel's decomposition —
  cite it when the "why not just buy Deep Research" question comes.

## 6. NEWSLETTER-DIGEST PIPELINES — the digest is the operator surface

**What it does.** RSS set → LLM per-item summaries → assembled digest delivered where the
human already lives: [00sapo/better-morning](https://github.com/00sapo/better-morning)
(self-hosted RSS→LLM→digest), an OSS digester posting AI summaries to Slack
([mfyz.com](https://mfyz.com/oss-newsletter-digester-ai-slack-summaries/)), an n8n builder
scraping ~100 AI stories/day into a **markdown data lake** before processing
([r/n8n build log](https://www.reddit.com/r/n8n/comments/1l9pff8/i_built_an_ai_system_that_scrapes_stories_off_the/) —
single-builder anecdote, Unproven at scale).

**Mechanism.** Cron fetch → dedupe → per-item LLM summary → assemble one digest → deliver
to the existing attention channel. The markdown-data-lake step lands raw items as files
with metadata BEFORE any scoring.

**The steal.**
- INTAKE — formalize the **spool law**: every harvested item hits a dated markdown spool
  before it enters any context window; scoring reads from the spool, never from memory.
  (March 228 did this ad hoc; the field does it by default.)
- WHEEL — the digest artifact: N per-item verdict cards are machine food; the operator
  reads ONE assembled digest per window (phone-readable law). Emit a digest artifact from
  intake alongside the cards. Unproven until format chosen.
- Delivery principle: the field delivers where attention already is (Slack/email). Ours =
  OPERATOR_DRIVE paste-lines. Steal the principle, not the channel.

## 7. CITATION-GRAPH CRAWLERS — every KEEP generates questions

**What it does.** Expand from seed papers backward (references) and forward (cited-by) to
map a literature — snowballing with inclusion criteria
([CASRAI guide](https://casrai.org/guides/citation-chaining-and-snowballing),
[PMC methodology](https://pmc.ncbi.nlm.nih.gov/articles/PMC8474097/)). Commercial mappers:
Connected Papers / ResearchRabbit / Litmaps
([comparison](https://effortlessacademic.com/litmaps-vs-researchrabbit-vs-connected-papers-the-best-literature-review-tool-in-2025/)).
Open source: [JoaoFelipe/snowballing](https://github.com/JoaoFelipe/snowballing), IPBES's
OpenAlex snowballing protocol ([ipbes-data.github.io](https://ipbes-data.github.io/IPBES_TG_Snowballing/)),
Snowih (newer, single source — Unproven).

**Mechanism.** Seed set → citation edges from a scholarly graph API → iterative expansion
with a filter → graph/map. The APIs are free and open:
[Semantic Scholar S2AG](https://www.semanticscholar.org/product/api) (REST + GraphQL) and
[OpenAlex](https://openalex.org/) (~1.1B API calls/month, MAG successor) —
[practitioner guide](https://dev.to/agenthustler/scraping-openalex-and-semantic-scholar-for-research-intelligence-2cc4).

**The steal.**
- SCOUT + WHEEL(REFIT) — the sharpest one in this file: the refit tick currently
  regenerates the scout search set from DISPUTED items and starvation heads. **Citation
  snowballing makes KEEP items generate questions too**: every KEEP fires a one-shot
  backward/forward neighborhood query against OpenAlex/S2, and the neighbors queue into
  the next night's harvest. Signal becomes questions, on both verdict poles.
- MONITOR — OpenAlex/S2/arXiv APIs are keyless free lanes: scholarly scout coverage that
  spends zero grok quota. Supported (documented free APIs).

---

## SYNTHESIS — what the field has that we don't

| # | Pattern | Organ | Fleet gap it fills | State of steal |
|---|---|---|---|---|
| 1 | Verdict-trained lexical ranker | INTAKE | cheap prefilter before premium scoring | buildable tonight |
| 2 | Keyless HN watcher | MONITOR | $0 standing lane, de-risks deck dependence | buildable tonight |
| 3 | Bridge shelf (uniform source shape) | SCOUT→INTAKE | one ingest contract for all sources | contract needs writing |
| 4 | Author matching + public digest artifact | INTAKE/WHEEL | person-lane harvest; digest as content | person-list exists on deck |
| 5 | Judge-loop + resumable registry | WHEEL | VERIFY spoke formalization; field confirms REMEMBER design | doctrine, not build |
| 6 | Spool law + one-digest-per-window | INTAKE/WHEEL | operator surface, context hygiene | format needs picking |
| 7 | Snowball-on-KEEP via OpenAlex/S2 | SCOUT+REFIT | KEEP items generate questions; keyless scholarly lanes | highest-leverage |

The meta-pattern: **the field's pipelines are free at the edges and expensive only in the
middle.** Ours is the inverse today — expensive at the edge (grok keys), nearly free in
the middle (march-228 triage at $0.09). Stealing the standing free pipes (HN Algolia,
OpenAlex/S2, arXiv API, RSS bridges) rebalances the fleet toward the field's shape and
removes the deck as a single point of harvest failure.

ADOPT TOMORROW: keyless standing watch lanes — a nightly MONITOR pass polling HN Algolia
+ OpenAlex/S2 + arXiv APIs against the fleet's watch terms, diffing last-seen, spooling
into intake; then snowball-on-KEEP (pattern 7) as its second turn.

---
Filed: watch/STEAL_RESEARCH_PIPELINES_20260904.md · room row kind: steal.pipelines ·
swept 2026-09-04 via web search (sources inline per claim).
