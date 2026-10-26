# SWEEP: agent-memory-continuity via Hacker News (2026-10-11)

source-fetched: 2026-10-11. Seat: sweep-agent-memory-continuity-hn. Door: Hacker News
(hn.algolia.com API v1 search_by_date + search, then items/<id> comment trees via the same
API, then primary pages via urllib). House laws held: ascii only, no em or en dashes, every
claim cites a page fetched or a command run this sitting. Quotes below are verbatim from
byte receipts saved this sitting in this directory (_amh_p2_*.txt, _amh_p1_hits.json);
curly punctuation in sources is normalized to ascii in the quotes.

## Door health

30 Algolia lanes, all clean JSON, zero 403s, zero degraded queries, no fallback needed.
Real negatives recorded: zettelkasten by-date 0 in window, memory consolidation by-date 0 in
window (same negative the 10-04 fold saw). One primary page 404'd (blog.szypowi.cz article;
the HN thread 49814947 is the record and was fetched instead). One instrument event: the
Mimosa hook intercepted the first pass-1 script write (SSRF heuristic on dynamic URLs); the
fix was a real guard, every fetch now passes an https-plus-host allowlist check
(_amh_pass1.py / _amh_pass2.py `guard()`), and the scripts ran clean after it.

## Pass 1 (broad sweep)

30 lanes: 20 fresh angles no prior fold of this area used (agent handoff, AGENTS.md,
episodic memory, memory palace, second brain, scratchpad, context engineering, memory
poisoning, experience replay, procedural memory, working memory, memory decay, agent
checkpoint, LLM journal, AI diary, world model memory, conversation summary, sleep
learning), 3 relevance lanes (HippoRAG 298 total hits, A-MEM agentic memory, Memento LLM
agent), Letta, and a 6-lane catch-up battery filtered created_at_i > 1791388800
(2026-10-10T00:00Z, after the 10-10 sweep's moment) so stories no prior fold could have
seen were surfaced. Output: 315 unique stories, 248 inside the 30-day window
(2026-09-11T00:00Z cutoff = 1789084800), 143 in the filtered relevance pool. The 30-candidate
floor is cleared by an order of magnitude; full receipts in _amh_p1_hits.json.

## Anti-rebank spine (read in full this sitting)

Eight prior HN folds of this area were read before sweeping: 2026-10-04, 10-09, 10-10, and
the adhoc run's sweep files, which themselves inherit 09-30, 10-01, 10-02, 10-03. Already
banked, do not re-confirm: Knowl, Agent Memory Repo spec, Motif, Singularity, Memdebug, CTWM,
galahad-kv 2610.10845, Zep Konig, Polign recall, Minigraf, Durable Actors, Temporal Pi,
Context Freshness Ledger, turbopuffer, funes/dacorvo 150k-token post, calpaterson
memoryfields, codepointer four-systems comparison, OKF Agent Memory, StructMemEval
2602.11243, cognee, SuperLocalMemory, Aura, reduck, Skillsync, Omnesis, Magnitude, and the
10-09 register's agent-memory rows (2610.08586, 2610.10265, 2610.03902, 2610.07309,
2610.07100, 2610.07782, 2610.08101, pi-optchat memory tree, the reddit three-architectures
test; register.jsonl read this sitting). None of the eight items below appears in any
register, DIGEST, or the 10-04 cached pages.

## Estate-side answers the ask ordered (read or run this sitting)

- **Q1 builder OWED discharged.** lens/graph.md:41 says "The builder script was not located
  or read this session." Located and read in full this sitting: mag/knowledge_graph.py
  (751 lines). What the builder drops that the JSON never carried: memory/warm_state.json
  and memory/rib_boot.json are not collector sources at all; the collector kinds are
  module/invariant/knot/case_law/steal/landscape/superseded/superseder
  (mag/knowledge_graph.py:60-61), fed from module docstrings, verkle_chain.jsonl,
  skill_ledger.jsonl, memory/steal, mag/ai_landscape, and the SUPERSEDED register. The
  warm-boot chain and the knowledge graph are disjoint organs; nothing in warm_state or
  rib_boot ever enters the graph. The 41 percent islands are structural: _edges()
  (mag/knowledge_graph.py:297-339) has edge branches only for superseded_by, module
  has_invariant, landscape already_inside, and maps_to; kind "knot" gets no branch, so all
  400 knots are islands (lens/graph.md:29 knot 400/400), and doctrine (217) and steal (140)
  likewise carry no edge builders. The verkle reader caps at the last 400 knots
  (mag/knowledge_graph.py:128) and skill_ledger at 300 rows (mag/knowledge_graph.py:152).
  Answer: the warm-boot chain restores seat continuity through brief + ribs, not through the
  graph; the graph's islands are a wiring gap (no knot/doctrine/steal edge builders), not a
  coverage gap the JSON could have filled.
- **Q4 three unbanked runs.** frontier_olm_2026-10-09 register.jsonl carries 9 agent-memory
  rows (read this sitting, listed above), uncommitted; frontier_olm_2026-10-10 holds 4
  agent-memory sweep files and no register or DIGEST (fold debt, burns.md:96-99);
  frontier_olm_adhoc is folded on disk and its own DIGEST names agent-memory-continuity as
  a zero-confirmation gap (lens/burns.md:106-108). So yes, prior continuity findings exist
  but sit uncommitted; the zero-confirmation gap is specific to the adhoc run. This sweep's
  eight items are new confirmations that duplicate none of them (overlap greps below).
- **Q2 parked corpus.** catalog.jsonl carries 783 rows matching agentmemory
  (sample: library_parked/agentmemory/.env.example, line 11423; control grep counted this
  sitting), but no live directory matches *agentmemory* at any depth-4 find under the repo
  root this sitting; the bytes were not readable, so the "which patterns are absent from
  rib/warm-state design" half is OWED, not answered. The HN-door half of Q2 is answered by
  item 1 (five 2026 studies absent from the estate's vendor-curriculum holdings).
- **Q3 oral_history miner.** No HN item this window speaks to oral-history card mining
  directly. One instrument shape recurs across two reads (inference, not a finding): Harbor
  counts per-rule served-vs-cited (item 1), Rutter gates its stateful behavior behind an
  append-only usage log and was prepared to conclude it is unused (item 4). An oral_history
  behavior-card miner would need that same served-vs-cited ledger or its cards are
  unfalsifiable, which is exactly the R4b census objection (lens/laws.md:114) to a second
  producer with no measurement.

## Pass 2 (deep reads, 8 items fetched and read end to end)

Primary pages read in full: swarmagent.dev plans essay (20,049 chars extracted),
gethrbr.com research post (10,487), ruttermemory.com essay (23,864), IHMT README
(29,083), jotbus.com (7,419). Comment trees read via the Algolia items API, flattened and
read: 49760187 (286 lines, 741 pts), 49783133 (85 lines, 277 pts), 49814947 (286 lines,
486 pts), plus the four thin threads (49867329 author comment, 50038733 zero comments,
49828496 two comments, 50029798 one comment). Receipts: _amh_p2_*.{raw,txt}.

## Banked items (strongest first; JSON in the SweepResult)

1. **Is AGENTS.md useful? What the research found** (gethrbr.com/blog/is-agents-md-useful,
   HN 49867329, 2026-09-27; article dated September 23, 2026; author comment read).
   Quote: "Each additional function the agent generated came with about 5.6 percent lower
   odds of following the rule." Why: the first measured decay law for boot-file continuity,
   from McMillan arXiv:2605.10039 over 1,650 Claude Code sessions: file size, rule position,
   file splits, and neighboring contradictions produced no detectable compliance difference;
   compliance falls as the session goes on. The meta post also carries ETH Zurich
   arXiv:2602.11988 (hand-written +2.4 / generated -2, neither significant, both about +20
   percent cost), Vercel's evals (compressed docs index in AGENTS.md 100 percent vs 53
   percent for a skill the agent never invoked in 56 percent of cases), Cai et al.
   arXiv:2606.12231 (7,310 rules from 83 projects: rules grow by addition, nothing is ever
   removed; updates raised compliance 49.14 to 72.13 percent), and Codified Context
   arXiv:2602.20478 (660-line always-on core plus on-demand specs across 283 sessions).
   Directly prices the estate's rib-boot design: injection timing, not file structure, is
   the lever; law decks that only accrete are the expected failure shape.
   Overlap: zero hits in catalog.jsonl (1,136,889 rows scanned) and the scoped memory tree
   for gethrbr, is-agents-md-useful, and all four arXiv ids. New.
2. **Why agent harnesses need plans, and why you shouldn't compact context**
   (swarmagent.dev/resources/engineering/plans-harnesses-and-final-handoffs/, HN 49828496,
   2026-09-24; vendor piece, claims single-source). Quote: "Checkpoint 2 inherits 100% of
   the verified technical signal while discarding 99.6% of the token weight." Why: a
   complete no-compaction continuity design: the plan is a typed JSON state machine of the
   harness; each checkpoint ends in a structured final_handoff contract
   (handoff_overview, impact_bullets, changed_files, validation, about 350 tokens) that is
   the only context the next checkpoint inherits; three named corruption guards (strict
   schema validation, parent verification barriers where children cannot declare their own
   tests passing, on-demand deep recall into durable plan history). Vendor-claimed
   telemetry: 80.2 to 92.4 percent prompt-cache hit rate, 7.89M prompt tokens for 100
   agents at $9.97. Maps onto the estate's pile habit and state_snapshot summaries: the
   estate already does this by discipline; the frontier productizes it as the runtime
   contract. Q4 evidence that the alternative to compaction is a handoff schema, not better
   summaries.
   Overlap: swarmagent, Final Handoff, Century Run all zero. New.
3. **IHMT, Infinite Hierarchical Memory Tree** (github.com/gonzaroman/IHMT-MEMORY, HN
   50038733, 2026-10-11; README read end to end). Quote: "the old memory is kept as
   history, flagged `OUTDATED`, and searches answer with the current one first." Why:
   supersession as a first-class feature of a plain-file memory (replaces links,
   mark_outdated, a conflicts command, a fact timeline in state/facts.json); ambiguity
   returns an AMBIGUOUS candidate block instead of a guess; retrieval walks a tree at
   beam x log_B(n) file reads. The bankable negative result: in an A/B test with 22 real
   headless Claude Code sessions the model preferred batched grep and never called the
   in-session project tools on its own, and forcing them made sessions 42 to 71 percent
   more expensive; the honest value of memory is between sessions, not inside one. That is
   a priced warning for the estate's known()/context() auto-consult and any plan to force
   graph consults into every turn.
   Overlap: IHMT and Hierarchical Memory Tree zero. New.
4. **Rutter, shared decision memory across AI tools** (ruttermemory.com, HN 50029798,
   2026-10-10; essay read end to end). Quote: "A summary plus the hash of the files it
   cited is a record, because it gives you a fingerprint to compare against." Why: the
   sharpest continuity-mechanism essay found this window: append-only decision lines
   captured by a Stop hook with no model call, each cited note stored with its sha256 at
   capture; renames rebind by hash, and a reference the tool cannot place is shown
   unresolved with candidates rather than dropped or guessed; identity-confirm is a local
   terminal command, never an MCP tool, because "a model must not be able to decide what a
   dead reference means"; positions carry formed and revised dates; an honest
   can-and-cannot-establish list (a reference shows what was listed, not that the model
   read it; same-path edits are not flagged today). Its anti-consolidation argument is a
   direct caution for the estate's dream()/zknot merge passes: merging is exactly what
   flattens the sequence of positions. Note: its named neighbor "Recall" may be the
   Polign/recall banked 10-09; identity unverified this sitting.
   Overlap: ruttermemory, robin-cannon, librarian-session all zero. New.
5. **Mini-AGI continual learning claim, plus an independent replication thread**
   (news.ycombinator.com/item?id=49783133, 2026-09-21, 277 pts / 80 comments, thread read
   end to end). Quote: "the finding is that slowing down the LR or the trunk, while keeping
   the LR of the experts is enough to eliminate most of the forgetting." Why: Q3
   living-weights calibration. The author's own mechanism admission in-thread is that there
   is no special algorithm; a commenter (jmatthews) reports a replication: "Most of your
   claims prove out but the lever is essentially Biderman et als 'learn less forget less'.
   My first pass actually made this mistake initially and the findings didn't replicate.
   After controlling for step density I replicated your findings." The genuinely novel
   engineering is batch-1 single-stream training with a grow/prune expert pool on 8GB VRAM;
   the forgetting result reduces to known LR-differential effects. The estate's ASTRA
   distillation door (lens/laws.md:108) should budget for learn-less-forget-less-class
   gains, not a new mechanism; the chess-only 524K-character degradation experiment is the
   falsifier shape worth stealing.
   Overlap: volotat, Mini-AGI, Biderman, learn less forget less all zero. New. OWED: the
   replication write-up (huggingface.co/spaces/dreddnafious/mini-agi-replicat) not fetched.
6. **Claude Code reads AGENTS.md, the 741-point thread** (news.ycombinator.com/item?id=
   49760187, 2026-09-18, 285 comments read). Quote: "IMPORTANT: this context may or may not
   be relevant to your tasks. You should not respond to this context unless it is highly
   relevant to your task." Why: the wrapper Claude Code puts around boot files marks the
   estate's closest frontier analog of rib law as dismissible, and the referenced issue
   18560 was closed Not Planned ([boorang], [albatross79] carry it). Practitioner mechanism
   facts: the harness, not the model, loads instruction files ([Merad], [adastra22]); a
   "mid session system-prompt refresh" overrode CLAUDE.md instructions ([sdf4j]); the
   working fix for late-session compliance is hooks that land at action time, "not 200
   turns ahead of time as a suggestion" ([Caveman81]); the skills folder (.agents/skills)
   was deliberately excluded from the change ([clutter55561] changelog quote), so skill
   decks still do not port across harnesses; session history is path-keyed and breaks on
   workspace renames ([yoavsha1], [KetoManx64] bulk-migrated 100 conversations by sed).
   Q1/Q2 material: the estate's rib injection should be tested for the same
   dismissed-wrapper decay Harbor measured.
   Overlap: 2.1.277 and mpoteat zero. New.
7. **Claude Code reads AGENTS.md only when telemetry is on, the 486-point thread**
   (news.ycombinator.com/item?id=49814947, 2026-09-23, thread read; the linked article
   404'd live, the thread is the record). Quote: "we needed a way to turn this off remotely
   via feature flags if it broke something, and with telemetry off you don't get those."
   Why: a continuity feature was silently absent for telemetry-off users because the
   kill-switch rode the telemetry channel; the Anthropic staff author (mpoteat) admitted
   "this was a fully human error on my part - I should've found a better way to launch with
   a kill-switch" and fixed it in v2.1.281. Two carries: kill-switches must not be coupled
   to observability channels (the estate's fresh-organ-dies-quietly class, cf. the FTS
   index decay law in AGENTS.md), and AGENTS.md support shipped as a Mod, "a plugin with a
   new type of hook, which we call a function hook", source-available in the anthropics
   claude-code repo; continuity behavior is a pluggable harness hook, which is the same
   shape as the estate's rib_boot layer.
   Overlap: szypowi zero (catalog and memory). New.
8. **Jotbus, shared encrypted scratchpad for coding agents** (jotbus.com, HN 49978401,
   2026-10-06, 28 pts / 17 comments; site read, thread read). Quote: "We route your agents'
   notes. We can't read them." Why: end-to-end-encrypted shared workspaces where agents
   hand off work across machines and harnesses via MCP plus @mention hooks; the handoff
   note ("what you found and what's left") is a first-class message type; the server stores
   only ciphertext and never receives keys. Marginal for the estate (rib_bus is
   local-first by design) but the E2E-relay pattern is the missing piece if the mesh ever
   spans machines.
   Overlap: jotbus zero. New.

## Research-question verdicts

- Q1 (warm-boot chain vs 41 percent islands): answered estate-side this sitting; the
  builder is read, the two organs are disjoint, and the islands are missing edge builders
  for knot/doctrine/steal, not lost warm-state data. Frontier corroboration: IHMT and
  Rutter both keep continuity in plain files with supersession or hash-pinning, neither
  builds a connectivity graph, so the frontier does not solve the island problem either;
  it avoids it.
- Q2 (agentmemory 781 / ms-agents-beginners 9,429): the corpus bytes are unverified live
  (parked path not found on disk this sitting; OWED). The HN door found the missing
  patterns itemized in five named 2026 studies (item 1): measured decay, add-only rule
  growth, cost of always-on context, index-vs-skill invocation. Steal-card verdict: item 1
  is a steal card, not new research to conduct; the estate can adopt served-vs-cited
  counting directly.
- Q3 (oral_history second card miner): no direct frontier instrument found; the recurring
  shape is served-vs-cited telemetry plus a usage gate (items 1 and 4). An oral_history
  miner without that ledger would repeat the R4b objection.
- Q4 (three unbanked runs): answered estate-side; the 10-09 register holds 9 rows, 10-10
  is unfolded, adhoc is the zero-confirmation run. This sweep's eight items are the first
  confirmed rows for the area in the 10-11 window and overlap none of them.

## OWED

- library_parked/agentmemory live bytes: catalog says 781 rows, disk says absent at depth
  4; reconcile the catalog drift before any Q2 corpus read.
- Rutter's neighbor "Recall" identity vs the banked Polign/recall.
- Mini-AGI replication write-up fetch (huggingface.co/spaces/dreddnafious/mini-agi-replicat).
- SwarmAgent's Century Run numbers are vendor-claimed; no independent corroboration fetched.
- The Harbor five studies' primary papers (2602.11988, 2605.10039, 2606.12231, 2602.20478)
  were read via the meta post, not first-hand; treat numbers as secondhand until an arxiv
  door pass.
- szypowi article body never read (404); the telemetry thread is the only record.

## Instruments this sitting

watch/inbox/frontier_olm_2026-10-11/sweep/_amh_pass1.py (30 Algolia lanes, receipts
_amh_p1_hits.json), _amh_pass2.py (13 fetches, receipts _amh_p2_*), _amh_overlap.py
(catalog 1,136,889 rows + scoped memory tree, all nine phrase groups zero, positive control
agentmemory 783 hits), plus the read set named above. Python: .venv/Scripts/python.exe
only. Every fetch passed the https-plus-host allowlist guard.
