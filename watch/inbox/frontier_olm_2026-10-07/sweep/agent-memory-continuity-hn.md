# Frontier sweep: agent-memory-continuity via Hacker News

source-fetched: 2026-10-07 · door: hn.algolia.com search_by_date + relevance search (no 403s on HN doors) · pass 1: 112 candidate story rows considered across 7 date-bounded doors ("agent memory" 30, "knowledge graph" 18, "LLM memory" 27, "context engineering" 3, "Mem0" 2, "Letta" 1, "Zep" 1) plus the relevance door, all in-window except where noted · pass 2: 11 full end-to-end reads (liao.gg + its 304-comment HN thread, gethrbr.com, arxiv 2609.23986, arxiv 2602.11243, astraobscura.net, past.dev blog, redreamality.com CTWM, github.com/chetto1983/Aura, cognition.com/agent-memory-repo, calpaterson.com/memoryfields.html).

## Ranked items (8 banked)

### 1. Do coding agents need memory or documentation? (gethrbr.com)
- URL: https://gethrbr.com/blog/do-agents-need-memory · HN id 49976848 (2026-10-06) · date 2026-10-06
- The strongest measured answer to our write-vs-read question. Synthesizes five 2026 studies:
  - VibeMemBench (arXiv:2609.23570): "eleven of twelve solver and system pairings failed to beat the same agent with memory off"; direct injection of verified experience lifted 4 of 5 solvers 1.1-4.5 pts.
  - arXiv:2609.30813: uncontested false beliefs in shared memory repeated in 97-99% of probes; source-type gating held false adoption at 6-9% vs 22-47% without.
  - arXiv:2609.08258: none of five memory systems enforced a revoked policy by default ("A retired fact keeps winning").
  - arXiv:2608.20195: 557 sessions, instruction files 60.5% of doc interactions, consultation followed by edit with probability 0.002.
  - arXiv:2608.23550: only ~4-16% of CLAUDE.md security rules map to an enforcing control.
- Position: gate facts at write time (human/policy approval; contradictions wait), enforce retirement at read time (a retrievable revoked fact still outranks its replacement), deliver rules with the task and count them when served/cited.
- Quote: "memory systems which choose what to remember rarely beat no memory at all"
- Overlap: the estate already holds the two strongest underlying papers as catalog stubs (2609.23570 VibeMemBench, catalog.jsonl id e639cfcda539; 2609.08258 Revoked but Still Authoritative, id ef3c7e98fa15) but NOT this synthesis, nor 2609.30813 / 2608.20195 / 2608.23550 (rg-verified absent from catalog/ and memory/).

### 2. Agents don't need memory, they need documentation (liao.gg)
- URL: https://liao.gg/blog/agents-dont-need-memory · HN id 49945933 (2026-10-03), 380 pts, 304 comments · date 2026-10-03
- Kevin Liao's Operator Memory plugin: write-time = the working agent updates Markdown mid-task while context is fresh ("Facts should be rewritten when truth changes. No appending."); use-time = session start reads a lean catalog + codebase indexes instead of exploratory ls/grep loops (~80k tokens/session claim, illustrative not measured).
- The HN thread is itself evidence: JohnBooty's "If you're burning 5000 tokens to rediscover the same thing in every session... it's an easy decision" vs kaydub's "the code itself is the documentation" and his MR-review skill losing to plain Claude + gitlab MCP; panarky flags Operator's file-injection as a prompt-injection surface.
- Quote: "Because agents don't need memory. They need documentation."
- Overlap: zero hits for liao.gg / "Operator Memory" / "agents don't need memory" in catalog/catalog.jsonl and memory/ (rg, 2026-10-07).

### 3. Jev-Mem: System-One-Controlled Agentic Memory for Efficient AI Agents
- URL: https://arxiv.org/abs/2609.23986 · HN id 49850669 (2026-09-25) · date 2026-09-21 (submission)
- Dual-process memory architecture: a non-LLM System-One controller does memory typing + relational organization at WRITE time and query routing / retrieval-budget allocation / graph traversal / candidate scoring / adaptive stopping at READ time; the LLM (System Two) is reserved for synthesis. Directly relevant to both the write-vs-read question and to stitching the star forest: relation organization happens in the cheap plane.
- Measured: LoCoMo 0.777 LLM-as-Judge (+11.0% over strongest baseline), memory construction 158 s (6.6x faster than quickest competitor), average query latency 0.93 s (-36.7%).
- Quote: "System Two is invoked only for complex reasoning and answer synthesis."
- Overlap: zero hits for "Jev-Mem" in catalog/ + memory/.

### 4. The Memory That Wasn't Yours (astraobscura.net)
- URL: https://www.astraobscura.net/2026/09/28/the-memory-that-wasnt-yours/ · HN id 49887024 · date 2026-09-28
- Poisoned-memory falsifiers for the keyed-belief-retirement question. Torres et al. "GhostWriter" (July 2026): ~98% insertion success, ~60% average delayed activation across email/calendar scenarios. Dash et al. (June 2026): permissive write/retrieval increases vulnerability; injection defenses incomplete. Defense: MemSentry (Sept 2026) routes memory writes to accept / review / quarantine (1,000 GPT-4-generated scenarios).
- Core falsifier shape for us: can the system distinguish what its owner authorized from what it merely encountered.
- Quote: "A system may accurately execute a transaction while being wrong about why that transaction is authorized."
- Overlap: zero hits for "GhostWriter" in catalog/ + memory/.

### 5. Evaluating Memory Structure in LLM Agents (StructMemEval)
- URL: https://arxiv.org/abs/2602.11243 · HN id 49968612 (2026-10-05) · date 2026-10-01 (v4; first 2026-02-11)
- Benchmark for ORGANIZING memory (transaction ledgers, to-do lists, trees), not recalling facts. Findings: simple RAG-LLMs fail; memory agents succeed when prompted how to organize; models often fail to infer needed structure unprompted. Implication for the 1,066-orphan star forest: edge induction must be scaffolded/prompted, not expected to emerge, and structure itself is a measurable axis.
- Quote: "a benchmark that tests the agent's ability to organize its long-term memory, not just factual recall"
- Overlap: zero hits for "StructMemEval" in catalog/ + memory/.

### 6. Past.dev: memory layer for agents, 85% on BEAM 10M
- URL: https://past.dev/blog/introducing-past-dev · HN ids 49923182 (2026-10-01) + 49967073 (2026-10-04) · date 2026-09-30
- The clearest measured temporal-order architecture: ingestion carries occurrence time; recall returns dated sources + verbatim excerpts; queryTimestamp reads memory AS OF a past date; when a fact changes, old values are kept as history rather than overwritten (retire-by-supersede). Anti-flattening pitch: similarity ranks by wording, not time.
- Measured: 85.03% answer accuracy at 10M-token history (next published system 68.0%), LoCoMo 93.12%. Caveats: hosted service (SOC2), Enterprise self-host only; deletion cascades to derived memory; audience-based reader permissions.
- Quote: "past.dev returns $40k, cites the email of 28 July, and keeps the call note of 3 February as the value it replaced."
- Overlap: zero hits for "past.dev" / "BEAM 10M" in catalog/ + memory/.

### 7. CTWM: Heavy-Tailed Memory Traces in Long-Horizon Agents
- URL: https://redreamality.com/blog/ctwm-heavy-tailed-memory-traces-long-horizon-agents/ · HN id 49955466 · date 2026-10-04
- Read-time allocation knob, complementary to write-time curation (its own JitMem crosslink "asks when curation happens - write time versus read time"). Memory access in long-horizon agents is heavy-tailed and POLICY-DEPENDENT (random-walk tails are retrieval artifacts, 0% power-law pass; semantic-policy tails are truncated-power-law-compatible). Budget by rank b(r;tau) ~ r^-tau; "summarize the tail, do not drop it."
- Measured: LongMemEval -24.48% tokens at accuracy parity; Graph World -5.9% tokens, tail error 0.932 -> 0.805; ALFWorld 3.9-6.6% savings. Guidance: relax tau for recall-critical queries (multi-session recall blind spot).
- Quote: "Once the window is finite, memory is no longer a neutral ledger; it is a resource-allocation mechanism."
- Overlap: zero (the "CTwm" hits in memory/corpus/ai_canon HTML are case-insensitive substring noise, verified with rg -o).

### 8. Agent Memory Repo: an open standard (Cognition)
- URL: https://cognition.com/agent-memory-repo + https://github.com/AgentMemoryRepo/agentmemoryrepo · HN ids 49971101 + 49968066 · date 2026-10-05
- Git-native memory: clone latest, search/follow [[wikilinks]], update entries with no human in the loop, push after every edit; MEMORY.md entry point; a periodic "Dreaming" agent adds pattern-based memories and cleans duplicates, outdated entries, and contradictions (a keyed-belief-retirement mechanism keyed to contradiction, not deletion). Multi-repo composition keeps separate ownership; git merges most edits and flags conflicting lines.
- Measured: illustrative only (checkout fix 2.4 s -> 310 ms on the slowest 1% via bench.sh).
- Quote: "Memories link to each other, so your agent navigates them like a wiki."
- Overlap: zero for "AgentMemoryRepo" / "Dreaming agent" ("Cognition" alone is word-noise: 321 catalog hits are the common noun, none the company's spec).

## Answers mapped to the research questions

- Q1 write vs re-read / zero-memory-call sessions: 2026 evidence says the failure mode is not missing memory but auto-selecting memory: 11/12 VibeMemBench pairings failed to beat memory-off, while directly injected VERIFIED experience helped (gethrbr, item 1). Policies that demonstrably work: write-time gating by source type (false adoption 6-9% vs 22-47%), delivery-with-task + citation counting, rewrite-not-append documentation read at session start (item 2), and cheap-controller retrieval with adaptive stopping (item 3). CTWM (item 7) separates the axes: allocation at read time, curation at write time.
- Q2 temporal flattening: retire-by-supersede with as-of reads is the measured winner (past.dev, item 6: 85.03% at 10M tokens); validity windows per fact are the local-first version (Aura below; Graphiti already estate-held); CTWM's recency rungs are the budgeted version.
- Q3 Mem0/Letta/Zep 2026 lines: the HN brand doors are nearly EMPTY in-window (Mem0 -> one migration blogpost; Zep -> an unrelated JS event library; Letta -> nothing), and the estate already byte-swept these lines on 2026-10-01 (memory/corpus/LINKS.jsonl:220: Letta -> letta-ai/letta-code + MemFS git-tracking; Mem0 April 2026 single-pass ADD-only; Zep CE deprecated, Graphiti survives). The conversation moved to git-native / file-format / read-time designs: Cognition AMR (item 8) is the best local-first no-throne fit (plain files, per-owner repos, git merge semantics); Aura (below) is the temporal-graph local-first fit.
- Q4 star-forest stitching: no in-window method measured specifically for 1,000+ orphan nodes (gap stands, OWED). Closest measured primitives: Jev-Mem's cheap-plane relation organization (item 3); StructMemEval's finding that structure must be prompted (item 5); and the Cal Paterson counterpoint (near-window, 2026-08-31, 191 pts: "in a memoryfield, at most 2 tool calls are required") arguing semantic jump beats graph walking - stitching orphans into deep graphs may BUY latency rather than recall.
- Q5 keyed belief retirement: revocation enforcement fails by default in all five systems tested (2609.08258, estate-held); working shapes: source-type gating at write (2609.30813 via item 1), Dreaming-style contradiction-keyed cleanup (item 8), supersede-not-delete history (item 6), write-quarantine gates (MemSentry, item 4). Falsifier shapes: revocation probes (97-99% false-belief repetition when uncontested) and delayed-activation probes (GhostWriter ~60% activation).

## Held back / OWED

- OWED: "Five failure modes around fact retirement in agent memory, with measurements" (Medium, HN id 49877124, 2026-09-28) - Medium returned 403 to WebFetch and 500 to the web_reader MCP on three attempts (2026-10-07). NOT banked; the door stayed dark. This was the single most on-target item for Q5.
- Held back (9th, item cap): Aura, self-hosted Go agent with temporal knowledge graph "facts with sources and validity windows, one ArcadeDB database per identity" (github.com/chetto1983/Aura, HN id 49951895, 2026-10-04; read in full; MIT; ~7 GB stack on a 16 GB mini PC; restore drill recovered 93 entities / 75 facts / 40 mentions).
- Out of window (2026-08-31, 37 days): Cal Paterson "Agent memory as a file format" (HN id 49508317, 191 pts, 96 comments; read in full): "Memory is data! The less fixed machinery we put between the agent and that data, the better the agent can be."
- Environment note: lens/burns.md, lens/graph.md, lens/laws.md were not found at any repo path I checked (repo root, memory/lenses = JSON only); the ask's own citations were used as estate context.
- Overlap instrument: ripgrep + grep over catalog/catalog.jsonl, catalog/tags.jsonl and memory/ (2026-10-07), per-pattern counts recorded above.
