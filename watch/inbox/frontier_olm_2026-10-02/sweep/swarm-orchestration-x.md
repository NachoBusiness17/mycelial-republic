# sweep: swarm-orchestration via x (frontier_olm 2026-10-02)

source-fetched: 2026-10-02. Seat: sweep gopher, x door, area swarm-orchestration.
Prior art honored: watch/inbox/frontier_olm_20260928/sweep/swarm-orchestration-x.md read in
full before banking (anti-rebank, questions.md:23-26). Estate map read: the four RQs come from
watch/inbox/frontier_olm_2026-10-02/lens/questions.md:156-168; the consensus-illusion law from
laws.md:19 and the owed decode redesign from laws.md:54; width + max-concurrency laws from
AGENTS.md.

## Method and door health

Pass 1: 9 WebSearch queries, all with site:x.com clauses; 80+ candidate items considered,
named below. Pass 2: 9 items fetched and read (7 article/note bodies at 1.2k to 18k chars
read, tails included; 2 partially, marked). Every banked quote was re-verified after reading
by re-fetching and asserting the quoted string is a byte substring of the JSON body
(8/8 SUBSTR, run 2026-10-02).

Door health, honestly stated:
- WebSearch site:x.com is again partially indexed; two queries returned mid-flight
  "MCP error -429 1302 Rate limit reached" from the search backend itself (bursty query
  shapes get capped; the fan-out law keeps corroborating itself).
- fxtwitter: curl instrument answered 10/10 with full JSON including article bodies for
  /status/ URLs that carry an article attachment. WebFetch instrument answered 1/1
  (omarsar0 2071964375125037343). No 403s on either instrument this run.
- eng_khairallah1 and nrslib and ZilongZheng articles came through fxtwitter's article
  attachment; theneurondaily 2095216879719919931 and corcoranwill 2104283555018731995
  resolved to bare article links whose bodies I did not pull (partially read, not banked
  as finds).

## Pass 1 register (considered; dates from snowflake or created_at)

In-window (2026-09-02..10-02): doodlestein 2104745145966920041 (Sep 29); eng_khairallah1
2104868464770863565 (Sep 29); swarms_corp 2105039598355447968 (Sep 29) + 2105378508705018317
(Sep 30); OrenMe 2105902729323327607 (Oct 2); corcoranwill 2104283555018731995 (Sep 27);
KyeGomezB 2104617869262680322, 2104753731673919579, 2105042330398986308, 2103978069346463967
(Sep 27-30, promo, dropped); zaibatsu 2103924116138987632 (off-topic); alexvoica
2095882699542032653 (Sep 4, essay, read no); theneurondaily 2095216879719919931 (Sep 2,
body unpulled).
Near-window (read anyway, dated honestly): ZilongZheng (Aug 27), nrslib (Aug 18), dair_ai
(Jun 30), advaita_labs (Feb 3), abuchanlife (Aug 24), StackDhruv (Aug 26), agihouse_org
(Aug 21), henrikhinai (Aug 17), PrajwalTomar_ (Aug 5), alex_prompter (Jul 21), spandan_madan
(Jun 17), Av1dlive (Jun 4), SentientAGI (Apr 22), nicbstme (May 4), rohit4verse (Apr 7),
DimitrisPapail (Feb 25), steipete (Sep 2025), omarsar0 (Jun 30).
Out-of-door finds surfaced by the queries and NOT banked (off-door): tianpan.co backpressure
and conflict-resolution posts, appliedtechnologyindex 2026 comparative analysis,
tamirdresher 9-agents-one-quota, DAFE arXiv 2503.08542, Concord ACL 2026.gem-main.46,
Committee-of-Judges (JITIE), MAD NeurIPS arXiv 2510.12697, Arbiter Agent arXiv 2606.10747.

## RQ verdicts

RQ1 (consensus mapped onto the actual output space, numbers/text): the strongest read is
ZilongZheng's belief-state essay plus its open-source artifact: it names the exact
consensus-illusion failure ("a flat summary ... can erase disagreement, merge copied claims
into apparent consensus") and demands agreement be scored by provenance structure
("independent corroboration from copied repetition") with an auditable log-odds confidence
update, shipped as github.com/bigai-nlco/belief-context-graph. dair_ai's DeepMind routing
paper (arXiv 2607.09197) supplies the complementary check from the other side: a society
that answers identically is vacuous regardless of accuracy, so behavioural differentiation
plus paraphrase stability, both orthogonal to task accuracy, are the tests that catch
agreement without information. OrenMe's Copilot Dynamic Workflows post shows the shipping
pattern the estate's gate already encodes: deterministic checks between stages and output
format enforcement, not trust in agent confidence.

RQ2 (backpressure/admission control vs AIMD + HiveMind 72-100 pct vs 0-18): three peer
shapes, none AIMD: (a) eng_khairallah1 relays Anthropic's Opus 5.5 guide result that an
elapsed-time budget on a team holds quality comparable to a single agent while finishing
sooner, i.e. budget-shaped admission, not error-shaped shedding; (b) doodlestein's swarm
post makes the resource being admitted BUILDS/TESTS, not API calls: file contention is
solved with advisory reservations (Agent Mail) and build contention by a "code first"
doctrine that stops each of 12 agents from building after every change, after GitHub
Actions cut him off past $5,000/month, i.e. admission control enforced as swarm doctrine;
(c) advaita_labs relays the NUS "Reaching Agreement Among Reasoning LLM Agents" paper:
consensus semantics + stopping conditions as the primitive, 20x latency / 11x P99 / 4.4x
tokens at unchanged accuracy. No read source extends or contradicts AIMD directly; the
neighborhood has moved to budget-shaped and doctrine-shaped admission.

RQ3 (tiebreak between two strong families, Cathedral class): no read source publishes a
family-vs-family tiebreak. What exists: nrslib's TAKT adds a dedicated adjudication ROLE
between review and fix ("decides, after a review, whether each finding actually needs to be
addressed this time") plus a merge gate, both staffed by the strongest affordable model,
with the stated rule "Anything planning-related should get the strongest model you can
afford"; eng_khairallah1's anatomy uses a critic that "sends weak work back" (rework loop,
not a verdict between families); ZilongZheng's environment-as-adjudicator clause (compiler,
test suite, linter: "The world can answer in green or red") matches the estate's
deterministic-registry law. Verdict: the frontier tiebreaks by routing the contest to the
strongest available judge or to a hard environment check, never by letting the two
contested families vote; Cathedral's pending tiebreaks should do the same.

RQ4 (small-model collectives vs one larger model, past debate-loses): nrslib is the
strongest measured evidence found: 7 controlled lineups on one 90k-line TypeScript task,
24-item weighted rubric, judge = GPT-5.6-Sol at reasoning high opening the repo and citing
file:line per item, scored 3 independent times and averaged, weight choices robustness
-checked (equal and correctness-heavy weights preserve rankings). Result: Sol solo, one
prompt one shot, landed FOURTH below the DeepSeek-V4-Flash-implements ensemble (70.3,
within 4 points of the all-frontier Sol ensemble at the top); local-only ensemble 49.1 with
zero missing correctness; nemotron lineups collapse (26.6 / 18.5). The mechanism is NOT
debate: "The level of the implementation role sets the floor; the caliber of the judgment
roles adds the polish", with Gemma4:31B running as 4-6 parallel review instances and the
strong model spent only on decomposition, adjudication, and merge. eng_khairallah1 adds the
boundary from Anthropic's own guide: teams only pay when the four benefits (context
isolation, parallelism, specialization, tool restrictions) do real work; otherwise a single
well-prompted agent wins.

## Item register (banked; strongest first)

1. eng_khairallah1, 2026-09-29, x.com/eng_khairallah1/status/2104868464770863565 (fxtwitter
   article body, 17,984 chars, read). Opus 5.5 team-building guide: elapsed-time budget on
   a team holds quality while finishing sooner; Terminal-Bench 4.0 66.4 pct vs Fable 5.1
   55.8; caps/budgets/stop conditions; critic sends weak work back; "Most Tasks Do Not Need
   a Team". Quote verified byte-true. Overlap: "Terminal-Bench 4.0" hits only prior sweeps'
   raw search dumps (frontier_olm_2026-09-30/sweep/_raw/, frontier_olm_20260928/sweep/_raw/),
   no banked holding; "elapsed-time budget" zero hits in catalog + watch/inbox + memory/rib
   + LINKS.jsonl. Confidence 0.85.
2. nrslib, 2026-08-18 (out of window; kept as genuinely new primary), x.com/nrslib/status/
   2089675861771559194 (fxtwitter article body, 30,487 chars, 3 sections read incl. results
   and lineups). TAKT local-ensemble-vs-frontier experiment, RQ4's strongest primary; also
   supplies the RQ3 adjudication role. Quote verified. Overlap: "TAKT" hits only unreadable
   binaries (tar.gz.enc, pdf, unrelated palworld wiki json); no banked holding. Confidence 0.85.
3. OrenMe, 2026-10-02, x.com/OrenMe/status/2105902729323327607 (fxtwitter, 4,670 chars, read
   end to end). GitHub Copilot Dynamic Workflows just introduced; "The agents handle the
   reasoning. The code handles the orchestration."; validation stage = agents review each
   other's findings, output formats enforced, deterministic checks between stages; explicit
   comparison to Claude Code's version. Overlap: prior sweep (0928) banked Anthropic's
   claude.dev dynamic-workflows post as its item 7; Copilot's announcement and the
   comparison are new; "Dynamic Workflows" phrase hits only raw input dumps
   (burn_wave_20260926/B2_130_session_inputs_raw.txt, prior sweep raws). Confidence 0.85.
4. ZilongZheng, 2026-08-27 (near-window), x.com/ZilongZheng/status/2092998098431930624
   (fxtwitter article body, 8,853 chars, read in full). Belief Context Graph: the
   consensus-illusion redesign direction; "independent corroboration from copied
   repetition"; flat summaries "merge copied claims into apparent consensus"; auditable
   log-odds confidence; Anthropic multi-agent system quoted as breadth-first-only.
   Quote verified. Overlap: "belief-context-graph" zero hits everywhere grepped.
   Confidence 0.8.
5. doodlestein, 2026-09-29, x.com/doodlestein/status/2104745145966920041 (fxtwitter note,
   2,405 chars, read end to end). 12-agent swarm: file contention solved by advisory
   reservations (Agent Mail); build/test frequency is the real bottleneck; "code first"
   doctrine as swarm-level admission control; $5,000/month GitHub Actions cutoff. Quote
   verified. Overlap: same author as prior sweep item 2 (claude_code_agent_farm README,
   Dicklesworthstone) and a name hit in BURN_world-models-multi-agent_20260928_c.md; the
   Agent Mail reservations + dsr + code-first doctrine post is a new artifact at a
   different layer than the farm README's launch staggering. Confidence 0.8.
6. dair_ai, 2026-06-30 (out of window; genuinely new primary arXiv 2607.09197),
   x.com/dair_ai/status/2077048984812896677 (fxtwitter, full text read). DeepMind routing
   validity: differentiation + paraphrase stability decide whether routing means anything,
   orthogonal to accuracy; "routing is vacuous" clause. Quote verified. Overlap: "2607.09197"
   zero hits in catalog + memory. Confidence 0.85.
7. advaita_labs, 2026-02-03 (out of window; genuinely new primary: NUS paper "Reaching
   Agreement Among Reasoning LLM Agents"), x.com/advaita_labs/article/2018576622048473241
   (fxtwitter article body, partial read ~2.2k chars of longer piece). Consensus semantics
   + stopping conditions + tail-latency control; 20x/11x/4.4x at unchanged accuracy.
   Quote verified. Overlap: "Reaching Agreement Among Reasoning" zero hits.
   Confidence 0.75 (paper itself not read, only the relay).
8. swarms_corp, 2026-09-30, x.com/swarms_corp/status/2105378508705018317 (benchmark post)
   + 2105039598355447968 (release post, both fetched, read). Swarms Rust v0.3.0: sub-agents,
   agent handoffs, typed tool outputs as first-class features; vendor self-benchmark vs
   LangChain/LangGraph/CrewAI. BANKED AS FINDING ONLY, never a verdict: vendor-run numbers
   under the instruments-only law (laws.md:15). Quote verified. Overlap: "Swarms Rust" zero
   hits. Confidence 0.7 (vendor claim, unreplicated).

## OWED (not verified; not banked, not asserted)

- theneurondaily Sep 2 article body and corcoranwill Sep 27 "autoresearch" article body:
  links resolved, bodies unpulled this sitting.
- eng_khairallah1 article: 17,984 chars read only in part (first ~5k + targeted greps);
  steps 2-10 of the course unread.
- nrslib: cost-and-time section of the Sol ensemble ("More on that later") sits past the
  slice I read; the hardware appendix unread.
- advaita_labs: the NUS paper itself unread; every number above is the relay's claim.
- Kye Gomez "Graph Workflow" orchestration engine: profile-level mention in a search
  summary only; no status resolved.
- The prior sweep's four OWED degradations (towardsai cancellation semantics, TrueFoundry
  managed agent layer, code.claude.com <50 agents line, openclaw 429 release note) carry
  forward unresolved.
