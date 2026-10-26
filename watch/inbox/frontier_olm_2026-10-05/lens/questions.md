# LENS OF LENSES: 8 research areas for the frontier sweep (frontier_olm 2026-10-05)

Written by the lens-questions seat after reading the five banked lens files in this
directory: `corpus.md`, `laws.md`, `graph.md`, `burns.md`, `doors.md`. Each area below
states what the estate already holds (so the sweep adds, never re-derives), the
questions the sweep should answer, and the estate map naming the organs it feeds.
The verification section at the bottom lists every command run this sitting.

Laws honored: no fabrication (unverified items are marked OWED), no em-dashes, every
quantity is sourced to a named file in its own sentence.

## 1. open-local-language-models

**Held.** The corpus's deep shelf is agent/LLM engineering: `corpus/library` holds
ms-genai-beginners 12,142 rows, ms-agents-beginners 9,429, zcode-zai-org 6,810,
openai-cookbook 3,120, and hf-agents-course 435 (`corpus.md` section 1), plus scraped
`mine/raw` 97,865 rows with title hits agent 2,323, llm 1,007, mcp 875 (`corpus.md`
section 1). The sensing doors are proven: arXiv export API answers in Atom XML with
`opensearch:totalResults` 170 for "local llm" (`doors.md` door 1), HN Algolia answers
JSON with `nbHits` 35091 (`doors.md` door 2), fxtwitter answers JSON with HTTP code 200
(`doors.md` door 4), while Reddit `top.json` is BLOCKED and its named oauth/www/mirror
alternates are unprobed (`doors.md` door 3, OWED). The tiering law is the driving
ladder: only Hermes primes and grok-4.7 are funded, free lanes are sensing-only
(`memory/rib/RIB_DRIVING_LADDER_20260928.md`; `laws.md` Part 1).

**Questions.**
1. Which open-weight releases of the last 90 days (7B to 70B class) change the
   ladder's "local janitors first, remote specialist scarce" shape, and at what VRAM?
2. Which currently downloadable models beat the `gemma:2b` scut and `gemma4`
   short-worker janitors (AGENTS.md line 7) on tool-call-shaped tasks at the same
   local footprint?
3. What do the freshest arXiv results (the proven door) say about small local models
   as agent executors versus hosted-API agents?
4. Which Reddit r/LocalLLaMA access recipe actually returns JSON (oauth, www, or a
   mirror), closing the `doors.md` OWED?
5. Do the `mine/raw` scraped rows already answer current "best local model" questions,
   and where exactly is their staleness boundary?

**Estate map.** Feeds the driving ladder (`memory/rib/RIB_DRIVING_LADDER_20260928.md`)
and the model-gate laws in
`memory/corpus/quantized_thought/instructions_frontier.jsonl`: this sweep decides
which models the janitor, sensing, and judgment tiers run next.

## 2. quantization-compression

**Held.** The lenses surfaced no dedicated weight-quantization shelf; the nearest
holdings are the inference-systems shelf lmcache-src 2,331 rows (`corpus.md` section 2)
and the estate's own law-compilation practice: the 24 compiled laws in
`memory/corpus/quantized_thought/instructions_frontier.jsonl` are all compiled-v0.4
(`laws.md` Part 1 intro). That gap is the point: weight quantization for the local
tier is un-inventoried in the corpus, so this sweep is a first pass, not a re-derivation.

**Questions.**
1. What do current papers measure for quality-versus-bits on 2B-8B janitor-class
   models at 4-bit versus 8-bit, specifically on tool-calling and repo-editing tasks?
2. Does sub-8-bit quantization degrade structured tool-call syntax and JSON adherence,
   which the estate's tool-call shape laws depend on (`laws.md` Part 1)?
3. Which quantized variants (GGUF, AWQ) of the newest open models are actually
   downloadable and runnable on a local Ollama host today?
4. What compression techniques for long-lived agent context (rule compilation,
   summary distillation) map onto the quantized_thought practice, and what recall do
   they cost?

**Estate map.** Feeds the deliberate-ask quantize-target law and the local janitor
tier's model cards (AGENTS.md deliberate-ask bullet): it sets the byte budget the
2B-4B workers can carry on this host.

## 3. agent-memory-continuity

**Held.** The self-knowledge shelf is the biggest zone: memory/biography_backup
258,840 + biography 65,934 rows and watch/inbox 17,831 (`corpus.md` section 4). The
knowledge graph is thin and partially broken: `memory/knowledge_graph.json` holds
2,919 nodes / 1,143 edges (`graph.md` findings), 1,204 nodes (41.3%) are isolated
(`graph.md` finding 1), 29 of 31 `already_inside` edges dangle to nonexistent ids
because `mag/knowledge_graph.py:236-239` builds ids from free-text `we_have` names
(`graph.md` finding 2), and 447 modules carry no documented invariant (`graph.md`
finding 5). The day-4 olm carrier already banked an agentmemory pin wave (commit
de0f6a870, git log this sitting).

**Questions.**
1. How do current agent-memory systems ground entity identity so cross-session links
   cannot dangle (the estate's 29-of-31 phantom-weld failure mode)?
2. What published designs weld narrative memory to code (linking session records to
   the modules that implemented them), attacking the isolated-node gap?
3. What recall and continuity evals could score a biography shelf of 258,840 + 65,934
   rows, turning the estate's biggest corpus into a measured memory asset?
4. What memory-tier architectures (working, episodic, semantic) do frontier agents
   ship, and do they beat the zknot recap plus rib stack for boot freshness
   (`memory/zknot/LATEST.md`)?

**Estate map.** Feeds `mag/knowledge_graph.py` (the dangling-id repair), the zknot
boot recap, and the rib vault: this area converts the graph lens's isolation findings
into a fix design instead of more unlinked nodes.

## 4. swarm-orchestration

**Held.** The dispatch envelope is measured law, not folklore: workflow children get
`maxAttempts 0` and stay at `max_concurrency` 3 or less, Task agents measured clean at
widths 3, 6, 10 and 12 with width 10 banking 109.4M tok/h (AGENTS.md fan-out width
bullet). The fresh R062 instrument made the free-usage verdict conditions-bound: 429s
appear only at forced width 13 (`burns.md` section 4), and a 24/7 fleet is armed
(`burns.md` section 4). Game-world testbeds sit catalogued as AI-society substrates:
azerothcore-wow 10,356, mod-playerbots 5,019, evennia 1,579 (`corpus.md` section 3).

**Questions.**
1. What retry, backoff, and admission-control strategies do current multi-agent
   frameworks use against rolling-throughput caps (429/1302-class), beyond the
   measured Task-agent envelope?
2. What heterogeneous-tier dispatch designs (cheap workers plus scarce premium
   judgment) exist in the literature, and how do they compare to the driving ladder?
3. Can the game-world repos serve as long-horizon multi-agent coordination
   benchmarks, and has anyone published results on them as such?
4. What consensus mechanisms let N lanes merge outputs without a coordinator throne
   (the no-throne invariants, `laws.md` Part 1) while staying honest under the
   consensus-illusion law?

**Estate map.** Feeds the width and concurrency laws in AGENTS.md and the lane
runners under `queue/lanes`: the sweep either validates the measured envelope
(R062's width 13 boundary) or finds a cheaper dispatch shape.

## 5. finetuning-adaptation

**Held.** The lenses surfaced no dedicated finetuning corpus; the nearest holdings
are hf-agents-course 435 rows (`corpus.md` section 1) and the honestly-gated
Gero-4B calibrator: "no published evals + GB-class download = operator sitting to
define the battery target first" (commit de0f6a870, git log this sitting; the same
commit family f94adae8d lists "Gero-4B sitting" among operator-gated doors). The
X-intel card 993a5977b names the Gero-4B thesis: proper-scoring-rule calibrated
probabilities instead of text (git log this sitting).

**Questions.**
1. What do 2026 LoRA/QLoRA recipes achieve on small models for tool-calling and repo
   navigation with under 10k training examples?
2. What minimum viable eval batteries do papers use to show a finetune did not
   regress general capability, the exact blocker that parked Gero-4B?
3. What synthetic-data pipelines for agentic finetuning are reproducible at zero
   cost, fitting the free-lane sensing doctrine?
4. What licensing governs distilling frontier reasoning traces into local weights,
   and does any of it permit commercial internal use?

**Estate map.** Feeds the operator-gated Gero-4B calibrator door (commits
de0f6a870 and f94adae8d) and the hf-agents-course shelf: it defines the eval battery
that un-parks the download decision.

## 6. kv-cache-context-engineering

**Held.** The estate's only dedicated inference-systems shelf is lmcache-src 2,331
rows (`corpus.md` section 2), and a fresh B4 KV sweep instrument landed this week
(`burns.md` section 4). The prompt-cache doctrine assumes byte-identical asks for
cache hits (AGENTS.md running-workflows bullet, pointing at
`corpus/steal/ZCODE_OPERATING_PLAYBOOK_20260925.md`). The descent protocol already
fixes prompt shape: the animal's claritas face via `mag/claritas.py` plus the
deterministic estate-law block (AGENTS.md descent protocol bullet).

**Questions.**
1. What KV-cache reuse and prefix-caching designs (LMCache lineage and successors in
   the vLLM/SGLang stacks) are current best practice for multi-turn agent sessions?
2. What does 2026 evidence say about how context ordering and section structure
   measurably change long-context agent accuracy?
3. What compaction patterns preserve tool-call fidelity when a long agent transcript
   is summarized back into context?
4. Do provider prompt caches actually key on byte-identity the way the estate
   playbook assumes, per current documented provider behavior?

**Estate map.** Feeds the lmcache shelf, the B4 KV sweep instrument, and the descent
protocol's prompt-shape leg (`mag/claritas.py` + estate-law block): better cache and
context shape cuts paid-turn cost directly.

## 7. evals-and-self-improvement

**Held.** The estate's self-steal organs are the ratchet, citation lint, and workflow
gate at pre-push (AGENTS.md build discipline), with census tripwires in
`tools/census_drift_patrol.py` (AGENTS.md clippy bullet). The burns ledger is silent
day seven: 693 rows, last ts 2026-09-28T13:45Z (`burns.md` section 1). The graph's
447 modules without documented invariants (`graph.md` finding 5) are eval-shaped
debt. `laws.md` Part 2 lists open research questions as numbered items running to 17
(`laws.md` item 17 is the last). The descent protocol's own falsifier names the
failure mode: a week where the ledger grows but no rib carries a frontier
contribution is spend theater (AGENTS.md descent protocol bullet).

**Questions.**
1. What public agent evals (SWE-bench-likes, tool-use suites) grade 2B-8B local
   models cheaply, and which run on CPU-only hosts?
2. Which self-improvement loops in the literature verify improvement with gates and
   ledgers the way the ratchet does, versus merely claiming it, and what falsifiers
   do they publish?
3. What health-check designs keep burn and usage ledgers from going dark (the
   estate's day-7 silence), and which revive automatically?
4. What minimum viable battery proves a new small model that has no published evals
   before it is admitted to a tier (the Gero-4B gate, made repeatable)?

**Estate map.** Feeds the pre-push gates (`githooks/pre-push`: ratchet, citation
lint, workflow gate), `tools/census_drift_patrol.py`, and the burns ledger carrier
`tools/hermes_burn.py`: this area improves the estate's own instrumentation.

## 8. inference-efficiency

**Held.** The measured envelope is the anchor: Task agents at width 10 banking
109.4M tok/h (AGENTS.md fan-out width bullet), the lmcache-src 2,331-row shelf
(`corpus.md` section 2), and the inference-budget law in the ribs (`laws.md` Part 1).
The janitor tier runs `gemma:2b` scut and `gemma4` short worker on local Ollama
(AGENTS.md line 7).

**Questions.**
1. What 2026 serving wins (paged attention, continuous batching, speculative decoding
   with small drafters) apply to 2B-4B janitor models on consumer hardware?
2. What does current evidence say about speculative decoding for agentic workloads
   where outputs are structured tool calls rather than prose?
3. What per-tier inference-budget accounting methods are reproducible, making the
   ribs' inference-budget law operational?
4. Is the measured 109.4M tok/h Task-agent envelope account-specific, or consistent
   with published multi-tenant throughput findings?

**Estate map.** Feeds the inference-budget law and the local Ollama janitor fleet:
the sweep decides where a faster local serving stack changes what the cheap tier can
absorb.

## Verification (commands run this sitting)

1. `ls -la watch/inbox/frontier_olm_2026-10-05/lens/`: all five lens files present
   (corpus.md 5,250 bytes, laws.md 19,090, graph.md 5,425, burns.md 15,898,
   doors.md 4,087) plus the banked analysis scripts.
2. Greps confirming every quantity cited above appears in its named source
   (corpus.md: 871,790 x3, 12,142, 9,429, 6,810, 3,120, 435, 97,865, 2,323, 1,007,
   875, 2,331, 1,579, 5,019, 10,356 x2, 2,123, 17,831 x2, 21,806, 14,860, 829;
   graph.md: 2,919 x2, 1,143, 273 x2, 1,204, 41.3, 300 x3, 447 x2, 236-239 x2;
   laws.md: 24, 56, v0.4 x2, item-17 at line 234; burns.md: 693 x9,
   2026-09-28T13:45 x2, R062 x4, "width 13" x1, 24/7 x1, B4 x2; doors.md: 170,
   35091, 1122, fxtwitter x4, HTTP 200 at line 62). The 324,774 biography sum and
   the 21-dir carrier count from the ask's lens summaries are NOT greppable in the
   banked files, so this document cites the split 258,840 + 65,934 instead of the
   sum and omits the 21-dir count entirely.
3. Path-existence loop over 14 cited paths (memory/rib/RIB_DRIVING_LADDER_20260928.md,
   memory/corpus/quantized_thought/instructions_frontier.jsonl, mag/knowledge_graph.py,
   mag/ai_landscape.py, memory/knowledge_graph.json, queue/lanes,
   memory/zknot/LATEST.md, corpus/library, memory/research_packs, tools/hermes_burn.py,
   githooks/pre-push, tools/census_drift_patrol.py, tools/citation_lint.py, this lens
   dir): 14 OK, 0 missing.
4. `git log --oneline -8` and `git log --format="%h %s" -3 --grep="Gero"`: confirms
   commits f94adae8d, de0f6a870, and 993a5977b as cited in areas 3, 5, and 7.
5. Citation lint on this file:
   `.venv\Scripts\python.exe tools\citation_lint.py check --files
   watch/inbox/frontier_olm_2026-10-05/lens/questions.md`: `ok records=1
   anchors=1 numbers-checked=35 blocking=0 warns=0 enforce-tokens=False`, exit 0.
6. Em-dash and non-ASCII scan on this file (python byte scan): non-ascii count 0,
   dash count (u2010 through u2015) 0, 246 lines.
