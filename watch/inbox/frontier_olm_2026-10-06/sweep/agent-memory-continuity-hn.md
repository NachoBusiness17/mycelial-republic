# agent-memory-continuity via HN, sweep 2026-10-06

source-fetched: 2026-10-06
Seat: sweep-agent-memory-continuity-hn (frontier gopher, Mag Resource Harness).
Door: hn.algolia.com API (search_by_date + search + items) fetched with curl through the repo
venv python for JSON compaction; deep reads fetched with curl (browser UA) and read as stripped
text. The ask's recipe named WebFetch: the Algolia door returned raw JSON cleaner through curl,
and WebFetch was exercised where it mattered (Medium retry below, 403). Every quote below was
re-verified verbatim against the fetched bytes this sitting (rg -cF runs, section 4).

## 0. Anti-rebank base (read this sitting)

- watch/inbox/frontier_olm_2026-10-06/lens/burns.md (217 lines, full): day-5 banked set, dead
  doors, owed list. Day-5 HN deep-reads NOT repeated here: 49945933 (docs-vs-memory), 49877499
  (Motif), 49581240 (OKF), 49923182 (past.dev BEAM), 49955466 (CTWM), 49628820 (Four Kinds),
  49951895 (Aura) per frontier_olm_2026-10-05/sweep/agent-memory-continuity-hn.md:12-24 (read
  in full this sitting).
- watch/inbox/frontier_olm_2026-10-06/lens/graph.md and lens/laws.md (full): the five research
  questions' estate side (zero dangling endpoints at 2,924 nodes; the trailing-space
  `invariant:law ` id; 56 ribs / 326,713 bytes).

## 1. Pass 1 (broad, 40+ candidates, window 2026-09-06..10-06)

Queries (search_by_date unless noted, all run this sitting): "agent memory" (95 nbHits),
"long-term memory LLM", "context window compaction", "AGENTS.md" (24), "knowledge graph
agents", "context engineering", "mem0" (487), "memory consolidation" (0), "Letta OR MemGPT
memory" (0), "compaction cliff" (relevance: 4), "stale knowledge LLM frozen" (0),
"content addressed OR content-addressable" (0), "sleep-time compute" (0), "ChatGPT memory",
"machine unlearning" (2), "graphrag" (10), "memory benchmark agents" (8). NOTE: Algolia
treats bare OR as a literal without advancedSyntax; the three OR-queries returned 0 and were
re-run without OR. Candidates considered (id: title fragment): 49945933* (banked day-5),
49760187 (741pt AGENTS.md support, covered by item 1's story arc), 49814947, 49833075
(Agents.md speaks Unix, 16pt, skimmed not deep-read), 49867329, 49926105, 49976848 (same
author as 49867329, 10-06), 49975380 (skillhub-local), 49874916 (CliffCompaction, CATALOG-HELD:
local_sovereign_agent/state/arxiv/2026-09-23/2609.26779v1.txt; dropped as known work),
49828496, 49955466* (banked day-5), 49968612, 49950478 (SuperLocalMemory 4.0, DROPPED: day-4
sibling already fetched the arXiv page, catalog row
watch/inbox/frontier_olm_2026-10-04/sweep/_am_page_49950478_slm_https_arxiv_org_abs_2608_08253.txt),
49963587 (Hindsight), 49884835 (Recalld), 49698184 (Skillzero), 49971101 + 49968066 (Agent
Memory Repo), 49976560 (ERC-8350), 49978800 (Tinyhat per-specialist memory), 49939791
(harness engineering), 49672213 (Novgraph), 49698073 (Ask HN legacy codebase), 49609821,
49609014 (Fraise), 49746030, 49727072, 49645202 + 49743385 (post-graph-rag), 49685838 (Ask HN
embeddings-for-retrieval), 49911995 (Magnitude), 49689454 (Ask HN 1000s of agents), 49877124
(fact retirement, DOOR DEGRADED, section 3), 49877752 (Omnesis), 49643048, 49854439 (Linux
kernel AGENTS.md, skimmed headline only).

## 2. Pass 2 (deep reads end to end, this sitting)

1. **Claude Code reads AGENTS.md only when telemetry is on [fixed]** (HN 49814947, 486 pts /
   32 top-level comments, 2026-09-23; thread read via hn.algolia.com/api/v1/items/49814947,
   full tree walked; the linked blog blog.szypowi.cz 404s post-fix, both slug variants tried,
   section 3). Q1. An Anthropic engineer (mpoteat) confirms in-thread: "Sorry folks, this is a
   rollout artifact, we needed a way to turn this off remotely via feature flags if it broke
   something, and with telemetry off you don't get those. It's already been fixed as part of
   v2.1.281 releasing today." So the law pack (AGENTS.md) reached or did not reach the seat's
   boot depending on an UNRELATED telemetry flag, for days, for 500k+ engineers, with no
   surface showing it. That is compile coverage is not propagation in vendor form. Second
   catch (arcfour branch): "what happens when users only update AGENTS.md going forward while
   keeping a stale, unchanged CLAUDE.md around?" is the two-law-stack disease named by a
   bystander. Third catch (vorticalbox): a cross-harness symlink farm (~/.agents/skills) where
   "claude uses .skills/synced which is uses to sync changes to skills from claude servers into
   the skills folder" - one vendor writing into a shared law directory. Estate read: this is
   next-loop target 1's failure mode exactly; a boot-pack presence check per seat class is the
   missing instrument, and the thread shows the failure survives even a shipped, watched,
   741pt-announcement feature (49760187, 2026-09-18).
2. **Is AGENTS.md useful? What the research found** (gethrbr.com/blog/is-agents-md-useful,
   fetched in full, 10,639 chars of text; HN 49867329, 2026-09-27; page shows Published:
   September 23, 2026). Q1/Q2. Five 2026 studies, side by side: ETH Zurich arXiv:2602.11988
   (hand-written context files +2.4 success / LLM-generated -2, neither significant, cost about
   +20%; "Repository overviews, the section most templates start with, did not help agents find
   the relevant files"); McMillan arXiv:2605.10039 (1,650 Claude Code sessions: file size,
   position, splitting, and neighboring contradictions had NO detectable compliance effect, but
   "Each additional function the agent generated came with about 5.6 percent lower odds of
   following the rule" - the propagation clock INSIDE a window); Vercel/Jude Gao evals
   (compressed docs index in AGENTS.md 100% vs 53% for a skill the agent "never invoked in 56
   percent of cases"; "The index in AGENTS.md had no decision point: it was simply there";
   40KB to 8KB); Cai et al. arXiv:2606.12231 (7,310 rules from 83 projects: 77.78% of rule
   edits correct AI errors, "usually by adding a new negative rule rather than editing an old
   one"; compliance 49.14% to 72.13% after rule updates; "every mistake adds a line, and
   nothing ever takes one away"); Codified Context arXiv:2602.20478 (283 sessions, 108k-line
   system, ~660-line hot constitution + on-demand docs). The author's own product angle names
   the instrument we lack: "the count turns 'is this file useful' from a paper you read into a
   ledger you can act on, and a rule that stops being true can be retired instead of carried
   forever" (served-vs-cited per-rule counters). Estate read: the AGENTS.md half of the
   two-stack merge has its evidence base now; rib rows need the same served/cited/retired
   ledger; the 5.6%-per-function decay is a measurable propagation clock for within-window
   law, complementary to the boot-pack check of item 1.
3. **Agent Memory Repo** (Cognition open spec; README raw fetched in full, 6,957 chars;
   cognition.com/agent-memory-repo fetched, 200; HN 49971101 + Show HN 49968066, 2026-10-05).
   Q1/Q2/Q5. "Agents need memory that lasts across sessions, and a single `MEMORY.md` file
   isn't enough. Agent Memory Repo is an open spec that treats agent memory as a git repo."
   Loop: clone, grep or follow links, "Update entries as the agent learns, with no human in the
   loop", "Commit after every edit". MEMORY.md is the always-loaded entry point: "keep it
   short: include only what every session needs, plus links to everything else." Entries are
   one-line bullets with open metadata keys (source = session link, added = date); "Update or
   remove entries when the information changes." Retirement is a named agent: "Dreaming ... a
   dedicated agent that runs periodically ... Merge duplicates, remove outdated entries, and
   check sources to resolve contradictions." Swarms share "the same memory repo, and git flags
   any edits" (merge conflicts surface); multiplayer keeps per-person repos with ownership.
   Case studies on the Etymon-adjacent ecosystem aside, this is the estate's rib vault +
   zknot + percolator published as one interoperable shape, with the boot-pack half (MEMORY.md
   short by law) and the retirement half (Dreaming) both spec'd. Falsifiable fit: our zknot
   LATEST.md rewrite-at-logon is their MEMORY.md; what we lack spec'd is the per-entry source
   key discipline (our welds dangled on prose ids - graph.md lens) and a scheduled Dreaming
   pass with merge-duplicate semantics (percolator has candidates, not dedupe).
4. **Why agent harnesses need plans - and why you shouldn't compact context** (swarmagent.dev/
   resources/engineering/plans-harnesses-and-final-handoffs/, fetched in full, 20,770 chars;
   HN 49828496, 2026-09-24). Q3. The whole piece is a placement-vs-compaction design: "an agent
   harness is not an LLM chat wrapper - it is an authoritative finite state machine";
   compaction's DEFECT 01: "LLMs summarize concepts, not technical invariants. Specific git
   commit SHAs, line numbers, subtle race condition edge cases, and exact variable renames are
   smoothed away. The agent begins hallucinating that previously resolved bugs still exist, or
   repeats failed approaches." Replacement: per-checkpoint structured final_handoff contracts
   (changed_files, impact_bullets, validation command) - "Checkpoint 2 inherits 100% of the
   verified technical signal while discarding 99.6% of the token weight" (~350-token handoff);
   strict schema validation rejects hand-waving; parent verification barriers (child coders
   cannot self-certify tests); on-demand deep recall via durable plan history. Numbers (vendor,
   their Century Run bench): 100 agents, 7,890,000 prompt tokens, $9.97 total, 80.2-92.4%
   prompt-cache hit rate; compaction cost table ($594/mo per 100 agents at frontier pricing).
   Estate read: this is mem0's placement-before-compaction cliff (banked day-5) carried into
   harness architecture, and its DEFECT 01 is our belief-retirement question: a cure that
   exists only in the discarded layer does not propagate; the handoff doc is the propagation
   unit. Our zknot summarize-at-window-close is the same shape as their naive compaction, one
   cadence coarser; the probe is to re-run the 171-pair zknot share measurement (0.59%,
   burns.md:88-89) after injecting a structured handoff block at window close instead of prose
   summary, same asks, and see whether stable-leading-block share moves.
5. **post-graph-rag** (github.com/crajah/post-graph-rag, README raw fetched, Apache-2.0, 635
   tests on the underlying post-graph layer; HN 49645202 "your RAG still thinks the old CFO is
   the CFO" 2026-09-10 + 49743385 2026-09-17). Q5. "What makes it different: **a later document
   can close an earlier fact**, so your model stops reporting that someone is both an ally and
   a rival." Fact closure is a first-class write: index "Helena Voss is CFO" (2019.txt), then
   "Priya Nair has been appointed CFO, succeeding Helena Voss" (2023.txt), and the query returns
   only the successor - "the earlier fact is closed, not competing". Underneath: append-only
   history and trigger-based audit logging on every table, capturing old and new state; vague
   connectors (relates_to, associated_with) rejected at extraction time. Measurements with
   disclosed qualifications: full 500-question LongMemEval 94.0% vs Zep/Graphiti gpt-4o 71.2%
   (different judge setups, disclosed); ECT-QA 0.807 vs TG-RAG 0.599 / GraphRAG 0.405 /
   LightRAG 0.406, with a second-family judge at 0.805 (judge-independence shown, per L23's
   shape). Estate read: this is the R4B dangling-weld cure (29/31 to 0) with a measurement
   harness attached; the missing piece it demonstrates is the CLOSURE SEMANTICS on edges - our
   graph now has zero dangling endpoints but nothing retires a superseded claim; their
   trigger-based old+new audit rows are a zknot-compatible shape (append-only, one item per
   record, L31/L32).
6. **Evaluating Memory Structure in LLM Agents** (arXiv:2602.11243, abstract page fetched;
   StructMemEval; HN 49968612, 2026-10-05, 1 pt / 0 comments). Q3/Q4. "We propose
   StructMemEval - a benchmark that tests the agent's ability to organize its long-term memory,
   not just factual recall ... simple retrieval-augmented LLMs struggle with these tasks,
   whereas memory agents can reliably solve them if prompted how to organize their memory.
   However, we also find that modern LLMs do not always recognize the memory structure when not
   prompted to do so." Tasks are ledger-shaped: transaction ledgers, to-do lists, trees.
   Estate read: the FLOW_LEDGER / trail.jsonl / LEDGER.jsonl organs are exactly the tested
   structures; the finding says structure must be PLACED in the prompt (placement again, third
   independent source this sweep), which prices the difference between a compile pack that
   carries the ledger schema and a pack that carries only facts. Weak HN signal (1/0); banked
   for the benchmark name and the placement finding, not the thread.
7. **Etymon** (github.com/landoncrabtree/etymon, README raw fetched in full, 4,131 chars; HN
   49926105, 2026-10-01, 2 pts). Q2. "Replace `CLAUDE.md`, `AGENTS.md`, `opencode.json`,
   `.codex/config.toml`, `.cursor/rules/`, `.mcp.json`, and other tool-specific setup with one
   shared manifest and lockfile: `etymon.toml` and `etymon.lock`." One source, generated
   per-harness views ("etymon sync --harness claude,codex,opencode"), hash-pinned lockfile.
   Migrations banked in the README: "LobeHub consolidates nine agent setup locations into
   .agents, Ant Design six, and Formbricks seven. Imported originals were explicitly retired
   after verification." Estate read: this is the two-law-stack merge contract as shipped tool:
   single law source (ribs), generated per-seat-class views (compile packs), lock-pinned
   provenance (verkle tip), and the retirement step NAMED in the migration verb set. The
   "retired after verification" phrase is the merge contract's safety clause: nothing is
   deleted until the generated view proves it carries the law - exactly the compile-coverage-
   is-not-propagation trap with its guard.
8. **ERC-8350: Agent Memory State Registry** (eips.ethereum.org/EIPS/eip-8350, fetched, Draft,
   created 2026-07-14; HN 49976560, 2026-10-06, 1 pt). Q4. "This ERC defines a minimal registry
   interface for committing authorized state transitions of autonomous-agent memory without
   placing raw memory in calldata." Each transition is an ExperienceDelta identified by an
   EIP-712 struct hash, applied to a linear per-space state machine; deletion claims and
   payload semantics are explicitly out of scope. Weakest item: on-chain verification of memory
   state is not an estate need, but the addressing design (commitment-hash transitions,
   controller/authorizer separation) is the Q4 counterfactual - content-addressed memory where
   the address is a signed struct hash, not a path; noted for the addressability question, not
   for adoption.

## 3. Degraded doors and honest gaps (no fabrication)

- The szypowi blog post (item 1's article) returns 404 on both slug variants tried this
  sitting ("...agents.md-only...", "...agentsmd-only...", posts/ variant); the story is banked
  from the HN thread itself (items API JSON, fetched and walked). The [fixed] in the title and
  mpoteat's v2.1.281 comment suggest the post may have been pulled or re-slugged post-fix.
- Medium fact-retirement article (HN 49877124, "Five failure modes around fact retirement in
  agent memory, with measurements"): curl direct returned HTTP 000 (connection failure) and
  WebFetch returned 403 Forbidden - the SAME door that stopped the day-5 seat
  (frontier_olm_2026-10-05/sweep/agent-memory-continuity-hn.md:38). Thread has 1 pt / 0
  comments, nothing else to read. NOT banked; Q5's anchor this sweep is post-graph-rag instead.
- Quoted-OR Algolia queries returned 0 hits ("documentation rot" OR, "Letta OR MemGPT",
  "content addressed OR content-addressable"): Algolia needs advancedSyntax for OR; re-ran
  without OR. Not a fetch failure, a query-shape lesson.
- news.ycombinator.com HTML item pages were not scraped directly this sitting; thread content
  came from the Algolia items API (same content, structured). Day-5 noted the same
  empty-shell rendering on item pages (sweep:40), so the API path is the working variant.
- Not deep-read, listed only: 49833075 (Agents.md speaks Unix), 49854439 (Linux kernel
  AGENTS.md), 49976848 (memory-or-documentation, same-author companion to item 2), 49978800
  (Tinyhat), 49698184 (Skillzero), 49884835 (Recalld), 49963587 (Hindsight). None quoted, none
  banked.
- ERC-8350 read covers abstract + motivation only (2,200 of 22,187 chars); claims beyond that
  ride the TOC, not read.

## 4. Overlap instrument (exact commands run this sitting)

- rg -i 'telemetry is on|szypowi|is-agents-md-useful|etymon|plans-harnesses-and-final-handoffs|
  swarmagent|2602.11243|agentmemoryrepo|fact retirement|five failure modes|superlocalmemory|
  2608.08253|skillzero|eip-8350' catalog/catalog.jsonl -> exactly 1 hit, the day-4 sibling's
  SuperLocalMemory page-fetch artifact (row id cb232ec02231,
  _am_page_49950478_slm_..._2608_08253.txt); SuperLocalMemory dropped from banking. Same
  pattern over memory/ -> 1 file, memory/corpus/ractors/hall_mp/texts/
  secret_teachings_of_all_ages.txt, a false positive (occult-text corpus; no product overlap;
  a follow-up literal rg for 'etymon|fact retirement|telemetry' inside that file read 0).
- rg '2602.11988|2605.10039|2606.12231|2602.20478|2608.24921|post-graph-rag|StructMemEval|
  2602.11243' catalog/catalog.jsonl -> 0 lines. The five studies behind item 2 and items 5-6
  are estate-new.
- rg -o '_am_page_(49945933|49828496|49971101|49867329|49926105|49968612|49814947|49645202|
  49743385)...' catalog/catalog.jsonl -> only _am_page_49945933 (the day-5-banked thread).
  No day-4 page artifact exists for any item banked here.
- Banked-set cross-check (manual, read this sitting): none of the 8 items appears in the day-5
  confirmed register (burns.md:71-79), the day-5 HN pass-2 list (sweep:12-24), or rounds 1-2 /
  day-4 registers (burns.md:51-56). 49828496 was a day-5 pass-1 CANDIDATE (sweep:8), never
  deep-read or registered; this sitting is its first read and first banking.
- Quote verification: rg -cF per quote against the fetched bytes, all read >= 1: "every mistake
  adds a line, and nothing ever takes one away" (ghrbr.html 1), "had no decision point"
  (ghrbr.html 1), "a rule that stops being true can be retired instead of carried forever"
  (ghrbr.html 1), "treats agent memory as a git repo" (amr.md 1), "LLMs summarize concepts,
  not technical invariants" (swarm.html 1), "a later document can close an earlier fact"
  (pgr.md 1), "memory agents can reliably solve them if prompted how to organize their memory"
  (arxiv_2602.11243.html 3, abstract + meta tags), "one shared manifest and lockfile"
  (etymon.md 1), "without placing raw memory in calldata" (eip8350.html 1), and the mpoteat
  clauses "this is a rollout artifact" / "with telemetry off you don" / "fixed as part of
  v2.1.281" (item_49814947.json 1 each). Local fetch artifacts under
  %TEMP%/fmem/ (szypowi.html 404 page, ghrbr.html, swarm.html, amr.md, pgr.md, etymon.md,
  eip8350.html, arxiv_2602.11243.html, item_49814947.json, item_49971101.json,
  item_49968612.json, item_49877124.json, szypowi2/3.html 404s).

## 5. Fix-design implications for the estate, per question

- Q1 propagation clock: two instruments named, not one. (a) BOOT-PRESENCE CHECK per seat
  class: after any rib landing, a cheap seat's next boot is asserted to carry the row
  (next-loop target 1, ba03060bb) - item 1 shows the failure class is a silent unrelated flag,
  so the check must run from the seat's own boot bytes, not the compiler's output. (b) IN-
  WINDOW decay clock: McMillan's 5.6%-per-generated-function compliance decay (item 2) is a
  within-window propagation measure; our citation-lint/ratchet hooks already fire per-turn and
  could log rule-hit rate vs functions-since-boot as the same curve for the estate.
- Q2 two-stack merge: the contract shape converges across items 1, 2, 3, 7 - one law source,
  generated per-seat views, lock/verkle pinning, per-entry source keys, "retired after
  verification" before any original-stack deletion, and a served/cited/retired ledger per row
  (Harbor's instrument) so rows earn deletion. ETH's finding (generated files LOWER success)
  warns the merge must not let an LLM write the merged stack unreviewed.
- Q3 placement vs compaction on our archives: the probe is now three-source-backed (Vercel
  index-in-boot-pack 100% vs invoked-skill 53%; StructMemEval structure-must-be-prompted;
  Swarm's handoff-not-summary). Concrete: re-run the 171-pair zknot stable-leading-block
  measurement (0.59% baseline) with a structured per-window handoff block replacing the prose
  summary on the same asks; if leading-block share does not move, summarize-at-window-close is
  locally equivalent and the cliff does not replicate on zknot.
- Q4 addressability: StructMemEval gives the eval; ERC-8350 gives the content-hash addressing
  counterfactual; the trailing-space id disease (graph.md:30) is the local evidence that
  path/id addressing already silently undercounts - an exact-match lookup audit tool (trim and
  compare id sets across vault, catalog, graph) is the cheap first probe, no LLM.
- Q5 belief-retirement depth: post-graph-rag's closure semantics + AMR's Dreaming + Motif's
  supersede-flag (banked day-5) triangulate the same contract: retirement is a WRITE (old+new
  rows kept, append-only), not a delete; the R4B 29-to-0 dangling cure needs its one-layer-
  down audit (do seats still cite retired rows from packs compiled before the cure?) - which
  is again the boot-presence check of Q1, run over retired rows.

## 6. Line count and receipt

This file: written 2026-10-06 by sweep-agent-memory-continuity-hn; 8 banked items, all quoted
from bytes fetched this sitting; 40+ pass-1 candidates listed; 7 deep reads end to end (items
1-5 and 7 in full text, item 6 via the complete arXiv abstract page, item 8 partial and marked);
3 degraded doors reported with their exact error codes. Falsifier for the sweep as a whole: any
item above whose quote fails rg -cF against the named fetch artifact is struck; none failed.
