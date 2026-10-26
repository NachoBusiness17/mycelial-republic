# Frontier sweep: agent-memory-continuity via reddit - 2026-10-11

source-fetched: 2026-10-11. Seat: sweep-agent-memory-continuity-reddit (dwf run,
mag/run-beta1-factory-build-audi branch). House laws held: ascii only, no em dashes, every
claim cites what was read or run this sitting.

## Door status (all degradations recorded per recipe)

- Recipe primary door `old.reddit.com/r/{LocalLLaMA,MachineLearning,LocalLLM,ollama}/top.json?t=month&limit=50`
  via WebFetch: all four returned Reddit's welcome/skip-to-content shell with zero post data
  (four calls, this session). DEGRADED.
- WebSearch `site:reddit.com` fallback: degraded exactly as the 10-10 sibling recorded
  (watch/inbox/frontier_olm_2026-10-10/sweep/agent-memory-continuity-reddit.md:13-15): engine
  ignored the site filter, returned zero reddit URLs, summary text only.
- Wayback CDX: worked briefly (health probe + old.reddit.com/r/LocalLLaMA prefix pull returned
  9 collapsed rows, 2026-09-29..2026-10-08, mostly 302 login captures), then 504 Gateway
  Time-out on wider queries, then web.archive.org went "Temporarily Offline" mid-session
  (full offline HTML page captured this sitting). DEAD by end of session.
- WORKING DOOR: Arctic Shift archive mirror (`arctic-shift.photon-reddit.com`), same door the
  10-09 sibling used (watch/inbox/frontier_olm_2026-10-09/sweep/agent-memory-continuity-reddit.md:9).
  Today the rate limiter was harsher than their 30-90s note: ~4-8 min spacing between calls
  survived; shorter spacing returned `{"error":"Timeout. Maybe slow down a bit"}` (54-byte
  responses, observed 9 times). All reads below are verbatim from this mirror (posts/ids bulk
  selftext + comments/search?link_id), never from search snippets.
- `query=` is a full-text search on this API (verified: `query=memory` on r/LocalLLaMA returned
  100 rows); `title=` is exact-match, not substring (`title=memor` returned an empty set where
  the 10-09 sibling's `title=memory` pulled 74).

## Pass 1 (broad sweep, candidates considered)

300 titles scanned this sitting across three pulls, window 2026-09-11..2026-10-11
(after=1789084800): r/AI_Agents newest 100 (as_aiag_p1.json), r/LocalLLM newest 100
(as_llm_p1.json, covers 10-10 20:04..10-11 16:30), r/LocalLLaMA `query=memory` top 100
(as_llama_qm3.json). On-area candidates triaged: 1x1j2lx (portable memory format), 1wpbeb7
(Meta Muse), 1weolwq (pi.dev plugins), 1wyf63m (Context Language Models paper), 1x33xl9
(AgentJournal, 4 dup posts), 1x35kdg (700K context no compaction), 1wyhzlc (Agent Muse
Android), 1x348i5 (agent auditability), 1x37yfu (concurrent-session double approval),
1x369c7 (agent email inbox), 1x3cij6 (AGENTS.md rule testing), 1x32jzg (remote session
follow), 1wy7wn0 (Agens Volundr partial-KV architecture), 1x17brf (Qwen appreciation, off).
Plus the three predecessor censuses read in full this sitting as anti-rebank triage
(10-09 reddit: 40+ ids; 10-10 reddit: 150+ CDX ids, 6 deep reads; 10-10 X: 33 in-window).

## Anti-rebank receipts (cross-sweep grep law, per the adhoc kv card's standing rule)

- 1weolwq: ALREADY BANKED, watch/inbox/frontier_olm_2026-10-05/sweep/kv-cache-context-engineering-reddit.md:39
  (pi plugin census, pi-vcc, cache-invalidation bug). My read = confirmation only.
- 1wyf63m: ALREADY BANKED, watch/inbox/frontier_olm_2026-10-07/sweep/kv-cache-context-engineering-reddit.md:80-92
  (CLM paper 2609.37725 + pi-clm plugin; paper itself catalog-held at
  state/arxiv/2026-09-30/2609.37725v1.txt). Confirmation only; their bank already carries the
  "prompt injections less likely to be forgotten" con.
- pi-optchat 1wzh1i7, MemTether, Engram, Spotlight, census thread: banked 10-09 (read their
  sweep in full). Memoria, embedflow, ThoughtDAG, KV-runtime, Hillock: banked 10-10.
- 1x1j2lx: 0 catalog hits, 0 md-bank hits; listed considered-but-unbanked in the 10-09 census
  (their pass-1 line 17). NEW, banked below.
- 1wpbeb7: catalog "Meta Muse" = 2 rows, both watch/INTAKE_MUSE_SPARK_CONTRIBUTOR_20260903.md
  (pre-window Muse intake, different artifact). Thread unbanked anywhere. NEW, banked below.
- 1x37yfu, 1x348i5, 1x33xl9, 1x35kdg, 1wyhzlc: 0 catalog hits; absent from all three
  predecessor reddit/X banks.

## Pass 2 (deep reads, fetched and read this sitting)

End to end (selftext + full comment pull): 1x1j2lx (self + 21 comments), 1wpbeb7 (60
comments; post has no selftext). Selftext-complete (0-2 comments or comments unread, stated):
1weolwq, 1wyf63m, 1x35kdg (0c), 1wyhzlc (10c unread), 1x348i5 (1c unread), 1x37yfu (2c
unread), 1x33xl9 ([removed] by mods; its 3 dup posts likewise). Nine threads fetched and
read; two with full comment bodies. Quota note: every further call rate-limited at the
observed spacing, so the remaining comment pulls were dropped rather than faked.

## Banked items (2 new + 1 minor, strongest first)

1. Memory Journal, portable memory format (r/LocalLLaMA 1x1j2lx, 2026-10-09, 11 pts, 21c).
   OP: a plain-text journal card that transfers context AND skill AND fact-outcome stamps:
   "it can transfer skill, transfer mistakes. along with proven, unproven and disproven
   facts"; a Deepseek-4.1 + Claude-Sonnet-5 pair recreated an EGO XML converter from the
   journal alone on first try; named hazard: "Journal can also cause drifts in behavior and
   vocabulary if you use a philosophically charged journal". Top comment
   (ComprehensiveShake76): the test that matters is whether the proven/unproven/disproven
   split survives sessions "or does everything slowly turn into 'true'". Estate map: this is
   the seat-continuity artifact the warm-boot chain lacks - outcome stamps already exist in
   code (mag/knowledge_graph.py:675 _OUTCOMES held/falsified/pending) but warm_state.json
   carries pointers only; the portable-card shape (A/B/C sections, reproducibility from the
   card alone, drift warning) is a steal for the brief/rib handoff between machines.
2. Meta Muse exports its own system data (r/LocalLLaMA 1wpbeb7, 2026-09-24, 248 pts, 60c
   read). Muse (Meta's agent) runs in a user-accessible VM and willingly zips and hands over
   its own system data, memory structure and runtime files when asked; Daniel15 (16 pts) calls
   it intentional, citing Meta's research blog; ThatsALovelyShirt (8): "Leaking ssh keys,
   runtime data, host names and network topology"; snugglezone pasted a news article and the
   agent zipped its data anyway. Load-bearing continuity find, dewwwey (23 pts): "I'm 99% sure
   they forked this: https://github.com/HKUDS/nanobot It uses the exact same memory
   consolidation system. The MD structure is identical as well." Convergence evidence: the
   largest lab ships markdown-file memory consolidation (same shape as the estate's md-record
   law and the 10-09 MemTether/Engram finds). Steal card candidate: an exfiltration tripwire
   for seat processes - the rib vault + funding state are exactly the crown jewels a
   helpful agent can be socially engineered into uploading (masiha97, 18 pts: "File system
   access plus outbound network plus a helpful attitude is a data exfiltration waiting to
   happen").
3. (minor) Concurrent-session double approval in the wild (r/AI_Agents 1x37yfu, 2026-10-11,
   2c). A twice-daily Claude Code agent double-posted when two sessions each got a "go": "The
   evening run caught it because before each reply it checks the thread for one from me and
   reads the post log, so it skipped those. Without that check it would've double posted
   under the same comments." Independent confirmation that read-before-write receipt checks
   are the working cure for multi-session continuity - the estate's corr_id/receipt layer is
   the same pattern.

Not banked, stated: AgentJournal 1x33xl9 selftext [removed] (title claimed it "outperforms
Compaction and Context Language Models"; body unrecoverable, nothing to verify); 1x35kdg is
the hardware class the 10-10 sibling excluded (700K context by brute force, no mechanism);
1wyhzlc is a product drop with continuity only in its "always on, it learns what you do"
pitch.

## The four research questions (estate half, all read this sitting)

Q1 (warm boot vs 41% islands): builder LOCATED AND READ, curing the OWED at
watch/inbox/frontier_olm_2026-10-11/lens/graph.md:41. The builder is mag/knowledge_graph.py
(751 lines, full read). What it drops that the JSON never carried: (a) hand-appended edges -
_edges() mints only superseded_by (:304-307), has_invariant (:315-317), already_inside
(:329-335), maps_to (:336-338); hand-folded nodes (doctrine etc.) survive as nodes (:613)
but no edge branch exists for their kinds, and the file's own comment records the measured
wipe "117 why_context edges -> 0 after build()" (:233-235); (b) chain history beyond the
bounded tails - knots are nodes[-400:] of an 11,299-row chain (:128), case law [-300:]
(:152); (c) by construction knots, doctrines and steals get zero edges, so the lens's 1,209
degree-0 nodes (41%, graph.md:11) are builder-structural. Warm boot itself never touches the
graph: mag/hermes_warm_boot.py reads verkle chain tip + deployments + session brief only
(grep for knowledge_graph/known(/context(: zero hits). Bytes read this sitting:
memory/warm_state.json (chain index 3414; session_brief = memory/briefs/latest.md, FROZEN
2026-09-26 per AGENTS.md, updated 2026-09-26T18:01:29Z, 2,101 chars = 15 days stale at boot)
and memory/rib_boot.json (index 3415, age_debt 1,956 min over the 60-min law, rib_count 26 /
vault 58 md / 7 law ribs mounted, lines 3-21). Verdict: warm boot restores law + chain-tip
continuity and does NOT depend on the graph, so the islands do not break boot; they break
edge-based retrieval (local_search fan-out, dream() communities) while BM25 known() still
text-hits islands. The builder's cure list: a doctrine/knot/steal edge minter, unbounded or
date-windowed knot tails, and edge regeneration that survives rebuilds.

Q2 (agentmemory + ms-agents-beginners patterns absent from rib/warm-state): agentmemory =
rohitg00/agentmemory at C:/Users/foste/Documents/projects/library_parked/agentmemory (783
catalog rows; README already banked by the 10-10 X seat with the supersession quote). Read
this sitting: README head + repo layout (AGENTS.md, INSTALL_FOR_AGENTS.md, packages/,
integrations/, eval/). Patterns the estate's design lacks: hook-driven capture (12 auto
hooks write memory as a side effect of tool events, vs the estate's seat-discipline file
appends), per-memory confidence scoring, MCP tool surface for recall. Steal card, not new
research: the hook-capture shape maps onto the harness's own hook layer. ms-agents-beginners
13-agent-memory/README.md read this sitting: working / short-term / long-term / persona /
episodic taxonomy, whiteboard memory, AgentSession-vs-persistent-store split, Mem0/Cognee
integrations. The estate holds these patterns unnamed (behavior cards = persona, knots =
episodic, relay/context pack = working); the steal is the taxonomy naming for lens pages,
not a mechanism.

Q3 (oral_history as second behavior-card miner): corpus/oral_history = 15,749 files on disk
(find) / 14,858 catalog rows (lens/corpus.md:20; different instruments and moments, not
differenced). Core deposit: nacho_archaeology, operator hand-delivered chat archives,
deposited 2026-09-05T22:02Z with sha256 per zip (MANIFEST.json read), extracted dirs
chats-produced / agents-meta / conversation blobs / store.db. The X miner
(tools/behavior_cards_x.py, read in full) shows the instrument shape: snapshot read, regex
card families, local ollama judge, MIN_CITED=3, behavior_card.v1 sidecars, dedupe against
the v1 deck + mirror principles. Verdict: VIABLE and already promised - RIB_BEHAVIOR_CARDS_
20260928.md:8-9 names oral_history as a future miner and laws.md:114 records the X miner as
the only producer (R4b census). The instrument it needs: a behavior_cards_oral variant that
snapshots the extracted transcripts, chunks long sessions, cites file:line instead of post
id, keeps the same CLASSES (voice is not a label per MAG_TRAINING_DATA_SPEC section 6), and
appends via the same operator-run step. $0, local, deterministic-first. The substrate is
longer-form than X posts and holds GENESIS-TESTIMONY-class material the X deck cannot reach.

Q4 (three unbanked runs vs this area's zero-confirmation gap): verified by grep this
sitting. frontier_olm_2026-10-09/register.jsonl holds NINE confirmed agent-memory rows
(grep -c "agent-memory" = 9; all printed: pi-optchat, 1wx6lib supersession thread, MINDSET
2610.08586, 2610.10265, 2610.03902, 2610.07309, 2610.07100, 2610.07782, 2610.08101).
frontier_olm_adhoc/register.jsonl holds ZERO (grep = 0) while its sweep banked 28 items on
overlap checks only - that is the gap named at lens/burns.md:107 (the adhoc DIGEST honest
gap 1). frontier_olm_2026-10-10 has no register at all (fold debt, burns.md:228) but its
sweep files carry five deep-read reddit findings and a door map. Answer: the findings
EXIST on disk and fill the register-level gap, but all three runs are uncommitted
(git log -1 empty each, burns.md:225-228) and the adhoc's 28 items stand unverified at
quote level (their honest gap 2). Before any new sweep fires: the BANKING COMMIT plus
quote-verification of the adhoc 28 outrank fresh sweeps. This sweep respected that: both
new items above sit outside every predecessor's banked set.

## Checks run and not run this ask

Run: four WebFetch reddit JSON doors (welcome shell); two WebSearch fallbacks (degraded);
CDX probes (9-row pull, then 504, then Internet Archive offline page); Arctic Shift pulls
(aiag p1 100, llm p1 100, llama qmem 100, bulk ids 7 + 2, comments 60 + 21); builder full
read mag/knowledge_graph.py; hermes_warm_boot grep; warm_state.json + rib_boot.json reads;
lens graph/corpus/laws/burns reads; RIB_BEHAVIOR_CARDS_20260928.md + tools/behavior_cards_x.py
reads; agentmemory README + repo layout read; ms-agents-beginners lesson 13 README read;
oral_history listing + MANIFEST head; greps as cited (catalog counts via grep -c over
catalog/catalog.jsonl; md-bank greps over watch/inbox/frontier_olm_*; the
memory/trajectory/steps.jsonl self-echo trap documented by the adhoc fold was excluded from
overlap verdicts).
Not run: pytest (no code changed); comment pulls for 1wyhzlc/1x37yfu/1x348i5 (rate limit);
any commit (banking commit is the operator-side owed act, burns.md:225-228); no knowledge
graph rebuild or fold() call (read-only sweep).
