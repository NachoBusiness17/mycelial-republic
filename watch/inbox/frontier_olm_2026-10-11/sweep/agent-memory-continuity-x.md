# SWEEP: agent-memory-continuity via x (2026-10-11)

source-fetched: 2026-10-11. Seat: sweep-agent-memory-continuity-x (dynamic workflow child,
branch mag/run-beta1-factory-build-audi-20260806T231709Z). Area: agent-memory-continuity
(research questions RQ1-RQ4 from lens/questions.md:101-117, read in full this sitting).
House laws held: ascii only, no em or en dashes, every claim cites what was read or run
this sitting; anything not verified is marked OWED.

## Door status (honest degradation, declared per recipe)

- X door DEGRADED: 9 WebSearch calls total (site:x.com phrasings for agent memory
  continuity/persistence, Letta/Mem0/Zep October 2026 announcements, NachoQuixotic agent
  memory, x.com/status + agent memory October 2026, Simon Willison October 2026, Claude
  memory tool). The backend ignored the site: operator, substituted general web results,
  and said so ("no matching posts on X were found", "search engines generally don't index
  x.com content well"). ZERO x.com status URLs or snowflake IDs surfaced, so the fxtwitter
  door (api.fxtwitter.com/<user>/status/<id>) had nothing to resolve; resolving a guessed
  ID would be fabrication. This matches the 10-10 sibling's 15-call zero (its own file,
  line 8) and the day-9 sibling's hard rate limits (its file, lines 9-12). No 429 storm
  hit this sitting; the door simply gave no X surface.
- Fallback doors used and green: hn.algolia.com (search_by_date + items API, 2 calls),
  arctic-shift.photon-reddit.com (posts/ids + comments/search + date-filtered
  posts/search, 5 calls), mcp web_reader on medium.com (1 call; WebFetch 403'd the same
  URL first and the fallback succeeded - never claimed as a WebFetch success).
- One primary page UNREAD: HN 49877124's linked Medium article was 403 on WebFetch,
  then READ IN FULL via web_reader (listed in Banked items). HN 49814947's article 404
  was already the HN sibling's known negative (its file line 204).

## Estate side (read or run this sitting)

- **RQ1 builder OWED discharged (Q1).** mag/knowledge_graph.py located and read in full
  (750 lines + head). Findings: (a) build() (mag/knowledge_graph.py:602-623) regenerates
  edges ONLY from node fields via _edges() (:297-339), whose four branches are
  superseded_by, module has_invariant, landscape already_inside (py-shaped only), and
  maps_to; kind knot/doctrine/steal get NO edge branch, so 400/400, 217/217, 140/140 are
  structurally islands. (b) Hand-appended edges are WIPED on rebuild: the builder's own
  comment (:229-236) documents "a rebuild wipes manual edges (measured 2026-10-07 on a
  copy: 117 why_context edges -> 0 after build())". I verified the wipe is LIVE this
  sitting: census run (.venv/Scripts/python.exe over memory/knowledge_graph.json) reads
  ts 2026-10-11T09:09:54Z, 2,944 nodes / 1,141 edges, rel counts {has_invariant 817,
  maps_to 300, already_inside 18, superseded_by 6}, why_context PRESENT: FALSE, zero-degree
  by kind {module 450, knot 400, steal 140, landscape 2, doctrine 217} = 1,209 (41%). The
  adhoc run's census (its sweep file line 13) read the same file at ts 2026-10-06 with
  why_context 117 and 1,256 edges; 1,256 - 117 + 2 has_invariant drift = 1,141. So the
  JSON DID carry 117 why_context links and the builder dropped them; what the JSON never
  carried is any knot/doctrine/steal edge at all. (c) The verkle reader caps at the last
  400 knots (:128) and skill_ledger at 300 rows (:152) while the chain has 3,415 leaves
  (memory/warm_state.json:10), so ~3,015 knots never enter the graph. (d) Warm-boot
  organs are DISJOINT from the graph: memory/warm_state.json read in full (989 bytes,
  schema hermes_warm_state.v1: chain tip + verkle root + Vercel URLs + a pointer to the
  FROZEN memory/briefs/latest.md, memory/warm_state.json:27-32) and memory/rib_boot.json
  head read (43,672 bytes, schema rib_boot.v1: chain anchor + 26 ribs / 58 vault md + law
  ribs mounted + SUPERSEDED register pointer). Neither file references the graph; the
  warm-boot chain restores continuity through brief + ribs + chain tip, not through the
  graph; the 41 percent islands are a builder wiring gap, not lost warm-state data. The
  same-run HN sibling independently discharged the same OWED (its file lines 49-65) and
  agrees on every point.
- **RQ2 corpora (Q2).** ms-agents-beginners lesson 13 sampled: 13-agent-memory.ipynb
  markdown headers extracted this sitting via .venv/Scripts/python.exe: "Types of Agent
  Memory", "Working Memory with Sessions", "Long-Term Memory Pattern", "Scenario 1 -
  First-time user books an anniversary trip", "Scenario 2 - Sarah returns weeks later".
  The missing-from-estate pattern the lesson sells is identity-scoped return-visit
  continuity (per-user profile keyed on the human, recalled weeks later); the estate keys
  continuity on seats and the chain, never on a human's return. library_parked/agentmemory:
  catalog rows exist (grep pulled library_parked/agentmemory/.env.example, id 5b770ed1de33,
  mtime 2026-10-04) but `ls library_parked/agentmemory` returns "No such file or
  directory" this sitting - the same catalog-drift the HN sibling measured at depth 4
  (its OWED, its file lines 239-240); the corpus bytes were not readable, so the
  which-patterns-absent half of Q2 stays OWED for the mirror, answered instead from the
  live door (banked items 1, 3, 5, 6).
- **RQ3 oral_history second card miner (Q3).** Read: memory/rib/RIB_BEHAVIOR_CARDS_
  20260928.md in full (line 9: "New cards get appended as the transcript miners
  (x_history_mine, oral_history) dig"; lines 77-94: the R4b amendment found zero boot
  consumers and one miner, tools/behavior_cards_x.py). Read: tools/behavior_cards_x.py
  head (570 lines total): the X miner's pipeline is snapshot read of
  memory/mycelium/nodes.jsonl filtered to label == nachoquixotic_post, dedupe, per-card
  regex families, local ollama (qwen2.5:7b, temp 0) judge, a card ships only with
  >= MIN_CITED = 3 verified posts, card_class restricted to
  {reasoning, heuristic, decision, value, stance, method} with no voice class
  (tools/behavior_cards_x.py:37-49). oral_history sampled: corpus/oral_history holds
  15,749 files (find -type f | wc -l this sitting); seat_pools/ carries
  session_index.jsonl (7,728 bytes, rows {id, thread_name, updated_at}, sample read:
  "Fix meta agent handler stack" 2026-08-04, "Strike the chord" 2026-08-12),
  history.jsonl (13,082 bytes), codex_sessions/2026/, grok_sessions/;
  nacho_archaeology/ holds 10+ zipped archives of the operator's pre-estate chats
  (conversation-blobs.db, store.db, agents-meta). Verdict: viable, because the v1 deck
  itself was mined from the session record (RIB_BEHAVIOR_CARDS_20260928.md:7
  "demonstrated repeatedly in the record"), so session mining is the original card
  source, not a new idea. The instrument needs three things the X miner gets free:
  (1) a per-row label for operator turns (session_index rows carry no speaker label;
  the X miner filters on label == nachoquixotic_post), (2) the same regex-family +
  local-judge + MIN_CITED evidence discipline, and (3) the served-vs-cited ledger the
  same-run HN sibling named as the R4b objection's cure (its file lines 79-85, 229-231):
  without counting whether a card was ever served and then cited, a second producer's
  cards are unfalsifiable.
- **RQ4 three unbanked olm runs (Q4).** Read in full this sitting:
  frontier_olm_2026-10-10/sweep/agent-memory-continuity-x.md (6 banked items + 5 RQ
  answers), frontier_olm_adhoc/sweep/agent-memory-continuity-x.md (8 banked + door log),
  frontier_olm_2026-10-09/sweep/agent-memory-continuity-x.md (8 banked + 5 RQ answers).
  Total ~22 banked continuity items across the three unbanked runs, PLUS the 10-04
  reddit fold's 8 (read in full this sitting for overlap: watch/inbox/frontier_olm_
  2026-10-04/sweep/agent-memory-and-continuity-reddit.md). The adhoc DIGEST's
  zero-confirmation row (lens/burns.md:107) is a confirmation-pipeline gap, not a
  findings gap: the sweeps hold banked material that was never registered or committed.
  Fold-before-sweep (burns.md anti-rebank rule 3) is therefore the right order and this
  sweep obeyed it: every banked item below was overlap-checked against all four prior
  folds, and three of my pass-2 candidates were DROPPED as prior banks (details below).

## Pass 1 census (35+ candidates considered; window 2026-09-11..2026-10-11)

- WebSearch yield (9 calls): mastra.ai agent-memory-layers; focused.io LangGraph
  persistent memory; blogs.oracle.com memory-approach comparison; mem0.ai library guide;
  getzep.com persistent memory tutorial; learn.microsoft.com foundry persist-memory;
  community.openai.com persistent thread referencing; dataaspirant/agentscamp/rohitraj/
  vectorize.io/devtoollab/ecorpit/digitalapplied Mem0-vs-Letta-vs-Zep cluster;
  skool.com Claude dual-mode memory; mindlock.co chatbot memory ranking (Jul 19 2026);
  BigGo Claude Code sleep-feature leak (Apr 2026); intoai.pub weekly (Jun 2026);
  letta.com sleep-time pages (Apr 2025, out); charlespacker highlights (out);
  skillsdirectory "Fetch Tweets (Grade A)" skill (Sep 3 / Oct 2 2026, snippet only,
  never deep-read); simonw.substack 2026-in-LLMs (Sep 28); letta-ai/letta GitHub;
  docs.mem0.ai. Reddit-named candidates (8): 1rdkngw, 1rzq1ye, 1qiu675, 1skur2q,
  1txj7uw, 1r2qkx8, 1rqnv3a, 1u92my7 - ALL dated Jan-Jun 2026 by the Arctic Shift
  records (created_utc decoded this sitting), i.e. search-engine recency was FALSE for
  every one of them; all dropped from banking.
- Arctic Shift date-filtered search (subreddit=AI_Agents, title=memory,
  after 2026-09-11): 24 in-window posts returned, of which the strongest were deep-read
  or overlap-dropped (below): 1x1u5jp, 1x0vjr7, 1wx6lib, 1wv80qv, 1wu31ir, 1wwd5rd,
  1wtmf7y, 1wtjxz2/1wtht9k (Hindsight pair), 1wy21mt.
- HN algolia search_by_date (17 hits in window): 50026431 Memdebug, 49993820 vector-RAG
  alternative, 49877124 fact retirement, 49861765 detailed guide, 49807330 retention
  policy, 49766795 still-current eval, 49749689 add/search eval, 49721941 Context
  Freshness Ledger, 49701788 typed memory with corrections, 49712610 graph db service,
  49703919 Backpass, 49685398 rate your memory, 49911995 Magnitude (194 pts).
- Dating instrument: created_utc decoded against the 2026-01-01 epoch 1,767,225,600;
  the search engines' implied recency was wrong for 8 of 8 named reddit threads.

## Pass 2 deep reads (7 banked, all read end to end this sitting)

1. Dat Do fact-retirement Medium article - full body via web_reader after WebFetch 403.
2. juraj-jumic/memdebug GitHub README - full, via WebFetch (DROPPED from bank: already
   banked by the 10-10 HN fold, named in the 10-11 HN sibling's anti-rebank spine).
3. mastra.ai/blog/agent-memory-layers - full, via WebFetch.
4. dataaspirant.com mem0-vs-letta-vs-zep - full, via WebFetch.
5. Reddit 1x1u5jp selftext + 13 comments - via Arctic Shift posts/ids + comments/search.
6. Reddit 1wx6lib, 1wv80qv, 1wu31ir, 1wtmf7y, 1wwd5rd, 1x0vjr7, 1wy21mt selftexts - via
   Arctic Shift posts/ids (1wx6lib and 1wwd5rd and 1wu31ir then DROPPED: banked by the
   10-04 reddit fold / 10-09 register; 1x0vjr7 kept as candidate only, toy format,
   below the bar).
7. HN item 50026431 + author comment (Memdebug) - via Algolia items API (bank dropped,
   read kept for the record).
DROPPED as prior banks (waste avoided): memdebug (10-10 HN fold bank, named in 10-11
HN sibling spine line 39); 1wwd5rd + 1wu31ir (10-04 reddit fold items 5 and 6);
1wx6lib (10-09 register's "reddit three-architectures test", named in the 10-11 HN
sibling spine line 43); all 8 WebSearch-named reddit threads (out of window, dated by
Arctic Shift); 49877124's HN story alone (article was the read target).

## Banked items (7, strongest first; full JSON in the SweepResult)

1. **Dat Do: Five failure modes around fact retirement in agent memory, with
   measurements** (medium.com/@dat999zx/...-55148df8b7e0, HN 49877124, 2026-09-28).
   Quote: "Provenance is unset on 73% of writes to the production store." Why: the
   measured supersession mechanics this area's RQ1 line needs - raw cosine AUC 0.972 on
   stratified data but 0.836 and 0 percent recall at the shipped fire rate on uniform
   negatives, so the write-time contradiction check ships as CSLS + a store-derived
   percentile threshold in warn-only mode; corrected facts mark sibling batch rows
   needs_review and sibling ranking drops 6 percent; file-change staleness is 5 percent
   signal (44 of 867) after filtering; cross-session code drift handled by read-set
   locators with hash-at-read-time and a shadow-mode precision gate (>=95 percent over
   >=40 adjudicated findings) before any hard refusal. Overlap: the author's own Knowl
   system is already banked (10-10 HN fold, line 38-42 of its sweep file); the ARTICLE
   is not (grep "fact retirement"/"dat999zx" over memory/ + watch/inbox hits only
   pass-1 hit files and HN sweep files whose anti-rebank spines do not list it; catalog
   0). New claim, first-hand.
2. **Reddit 1x1u5jp: We gave our agents a shared company memory in plain markdown**
   (r/AI_Agents, 2026-10-09, u/Vektoris_AI_Workflow, 14 comments; selftext + comments
   read). Quote: "the git diff approval is what makes 600 notes trustworthy, agents
   write and humans decide". Why: an operator-side continuity design that independently
   reinvents the estate's md-record law and adds the three pieces the estate's record
   law leaves implicit: agent writes land as git diffs awaiting human approval; notes
   must cite sources or say "not verifiable" (the citation-lint instinct as a household
   rule); decisions get their own notes with rationale AND reversal conditions (21 so
   far) - which is the fold outcome-stamp shape (mag/knowledge_graph.py:675-696
   held/falsified/pending) arrived at by a German AI studio with no graph at all.
   Overlap: grep "1x1u5jp"/"Vektoris" over catalog (1,136,889 rows) + memory/ +
   watch/inbox: zero everywhere. New.
3. **Reddit 1wv80qv: The Hard Part of AI Memory Is the Write, Not the Read**
   (r/AI_Agents, 2026-10-01, u/Tiwaryswarnim, 10 pts, 23 comments; selftext read).
   Quote: "The Hard Part of AI Memory Is the Write, Not the Read". Why: the write-side
   taxonomy the estate lacks: a transcript contains facts, observations, preferences,
   decisions and unresolved items that file at different levels (deal, company, person),
   organized Work -> Event -> Interpretation -> Change -> State -> History -> Recall
   with current state AND history kept - the interpretation layer is the one the
   estate's knot reader never had before its 2026-10-05 defect fix, and the state/history
   split is the keyed-slot law the 10-04 fold's item 3 derived. Complements banked
   MemFit (write cost) with write semantics. Overlap: author id + "MindPalace" appear
   ONLY in the 10-03/10-04 pass-1 harvest pools (never banked, never in any register);
   catalog 0. Harvested-unclaimed; first claim with the 10-04 pool stated.
4. **dataaspirant: Mem0 vs Letta vs Zep - Choosing Your AI Agent's Memory Layer**
   (2026-09-12, in window by one day; read end to end). Quote: "a vendor benchmarking
   its competitor is an adversarial act, and a vendor benchmarking itself is marketing".
   Why: corroborates the instruments-only law (RIB_MODEL_GARDEN_ROUTING.md:47-53, "No
   cell fills from vendor claims... Hand-copying a vendor number into an empty cell is
   fabrication") from the memory-benchmark front: Mem0's LOCOMO numbers vs Zep's
   rebuttal, both vendors now publishing self-chosen setups, resolution = run a private
   benchmark on your own query shapes. Also the article's own line: "Configuration
   choices, retrieval depth, judge prompts and benchmark selection each move scores by
   margins larger than the gaps being advertised." Overlap: dataaspirant domain known
   only via the 10-07 kv-cache sibling's DIFFERENT article (LC-vs-RAG, its raw html in
   catalog rows 5f5e20393f71, judged listicle-tier); this comparison post: catalog 0,
   memory/watch 0. New.
5. **Reddit 1wtmf7y: Should an agent keep state in memory or rebuild it each run?**
   (r/AI_Agents, 2026-09-30, u/LowMixture1084, 16 comments; selftext read). Quote:
   "Should an agent keep state in memory or rebuild it each run?" Why: the 03902
   store-vs-reconstruct economics (banked 10-09 as When Evidence Changes) surfacing as
   a practitioner's exact dilemma, with the asker's stated worry being the fold-rot
   falsifier in one sentence: stale state surviving a bad branch makes the next
   approval look reasonable when it is not - i.e. pending-stamped folds being consumed
   as if held. Overlap: id + author only in 10-03/10-04 pass-1 pools; catalog 0.
   Harvested-unclaimed; first claim.
6. **Mastra: AI Agent Memory - Persistence, Layers, and Tradeoffs** (mastra.ai/blog/
   agent-memory-layers, 2026-07-25, OUT OF WINDOW by 47 days, flagged; read end to
   end). Quote: "Use the smallest layer that answers the problem." Why: the four-layer
   taxonomy (message history / working memory / semantic recall / observational memory)
   with a per-layer benefit-cost table is the cleanest mapping onto the estate's organs
   found this window: ribs+rib_boot = working memory, catalog/FTS = semantic recall,
   zknot LATEST = observational; the table's observational-memory cost line
   ("Observations must be verified against original messages") is the census-carrier
   disease stated as a design constraint. Banked out-of-window because the taxonomy is
   unheld anywhere and prices RQ2's which-patterns-are-absent answer. Overlap:
   "agent-memory-layers" zero in catalog + memory/watch; catalog "mastra" rows (151)
   are the ai-engineering-from-scratch agno-and-mastra-runtimes course files, not
   this blog. New, date flagged.
7. **Reddit 1wy21mt: Same system, very different scores depending on the judge**
   (r/AI_Agents, 2026-10-04, u/Efficient_Joke3384, 8 comments; selftext read). Quote:
   "Same system, very different scores depending on the judge. How do you read memory
   benchmarks?" Why: the judge-variance datum for memory benchmarks (the fetch records
   the cited post's spread: 51.4 token-overlap F1 vs 75.8 LLM judge on the same
   answers), closing the loop with item 4's vendor-benchmark critique and the 10-04
   fold's judge-truncation findings; memory-area numbers need judge preflight + fixed
   known-verdict cases before they enter any estate cell. Overlap: id zero everywhere;
   author only in 10-03/10-04 pass-1 pools (unbanked). Harvested-unclaimed; first
   claim.

## Research-question verdicts

- Q1: answered (builder read; islands are missing knot/doctrine/steal edge builders;
  the JSON DID carry 117 why_context links that a rebuild dropped; warm organs disjoint
  from the graph). Frontier items 2 and 5 both independently choose the rebuild-from-
  record side of the store-vs-rebuild question.
- Q2: ms-agents-beginners sells identity-scoped return continuity the estate lacks;
  agentmemory mirror is catalog-drifted (rows exist, disk absent) and stays OWED; the
  live door answers instead: write-side taxonomy (item 3), judge-clean benchmarking
  (items 4, 7), human-readable layer with reversal conditions (item 2).
- Q3: viable; needs operator-turn labels + regex/local-judge/MIN_CITED discipline +
  served-vs-cited ledger. The v1 deck's own origin (session record) is the precedent.
- Q4: yes - the three unbanked runs hold ~22 banked continuity items; the zero-
  confirmation gap is the missing confirmation pipeline, and this sweep's 7 items were
  checked against all of them before banking.

## Checks run / not run this sitting

Run: lens files graph/corpus/burns/laws/questions read in full; mag/knowledge_graph.py
read in full; live graph census (.venv/Scripts/python.exe, outputs quoted above);
memory/warm_state.json read in full; memory/rib_boot.json head read;
RIB_BEHAVIOR_CARDS_20260928.md read in full; tools/behavior_cards_x.py head read;
corpus/oral_history structure sampled (find count, session_index rows);
ms-agents-beginners lesson-13 header extraction; three prior continuity X sweeps +
10-04 reddit fold + 10-11 HN sibling read in full; 9 WebSearch calls; Arctic Shift 5
calls; HN algolia 2 calls; web_reader 1 call; WebFetch attempts: 2 x 403 (reddit json,
Medium), rest green; overlap greps: 27 needles over catalog.jsonl (1,136,889 rows,
grep -a single pass each) + rg over memory/ and watch/inbox/ (biography trees excluded,
today's run dir excluded), per-needle results quoted above.
Not run: pytest (no code changed); no fxtwitter resolution (no IDs surfaced; not
fabricated); no full read of 1wu31ir/1wtmf7y/1wy21mt/1x0vjr7 comment trees (selftext
only); Medium article facts are single-sourced to its author (no independent
replication fetched); the 10-04 fold's harvested-unclaimed precedent is quoted from
its own file (line 39), not re-derived.

## OWED / note for the fold

- library_parked/agentmemory catalog drift now confirmed by two seats this run
  (HN sibling depth-4 find + this seat's ls failure): reconcile before any Q2 mirror
  read.
- Medium fact-retirement numbers are author-claimed; the Knowl repo (same author) is
  the nearest estate-verifiable artifact and is already banked.
- The X door has now degraded identically across three consecutive runs (10-10: 15
  calls zero; 10-11: 9 calls zero); the named cure stays the x-history miner
  (HERMES digest e8eedd8eb), which is exactly the instrument Q3 proposes to clone for
  oral_history.
- Banked item 6 is out-of-window by design and flagged in place; do not refresh its
  date claim silently.
