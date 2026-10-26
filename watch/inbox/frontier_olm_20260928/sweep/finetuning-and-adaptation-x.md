# sweep: finetuning-and-adaptation via X door (2026-09-28 stamp)

Sweeper: sweep-finetuning-and-adaptation-x (subagent, GLM). Area: tape-to-model fine-tuning,
corpus cleaning gates, 2B-vs-frontier on narrow chores, distill cost vs the $180-220 credit
budget, continual adaptation from own filed workdays.

## Door status (honest)

- fxtwitter JSON door: WORKED. 9 of 10 resolve attempts returned code 200 with full text,
  dates, engagement. 1 hard 404: X **article** endpoints are NOT served by fxtwitter
  (api.fxtwitter.com/jvr0x/article/2102364361998188575 -> 404). Workaround used: resolve the
  author's sharing status post instead, take article content from the fetch's article summary,
  and quote the article from its search-result snippet (marked below).
- WebSearch site:x.com: WEAK and rate-limited. Several lanes returned MCP error 429 / code 1302
  and had to be re-issued in narrower batches (2-3 per round). site:x.com is honored loosely;
  X is poorly indexed. No fabricated fallbacks; every unresolved lead is listed OWED.
- Search door note: the backend surfaced strong Feb 2026 and Oct 2025 items for the fine-tuning
  lanes; only 3 of the banked 8 sit inside the strict 30-day window (2026-08-30..09-29). Each
  item's date is stated; the older ones are banked because they are the strongest published
  evidence found for their question, not because they are fresh.

## Pass 1 census (30+ candidates considered)

Resolved and read via fxtwitter (9): tobi/status/2094808564355191249; MRRydon/status/2095200078327890136;
jvr0x/status/2102835768138076280; coderabbitai/status/2087175469963858146; NVIDIAAI/status/2087662769512571010;
togethercompute/status/2026738061376368879; ZainHasan6/status/2026898606838657252;
QingyangWu1/status/2026771941462606275; yueqi_song/status/1983539504385253684; gneubig/status/1983548125135655228.
Read off-X (4): arxiv.org/abs/2510.24702 (ADP paper); fastino.ai Nemotron learnings blog;
coderabbit.ai routing blog; ycombinator.com Moda launch page.
Candidates considered but not banked (snippets only, listed so the next sweeper does not re-mine):
cyi12 "1.5B on 200-500 good examples" post (status id never surfaced; OWED);
"Continual Learning for AI Agents: How to Actually Build It" x.com article Jun 2 2026 (author/id unresolved; OWED);
karpathy/status/1938626382248149433 "cognitive core" (Jun 2025, estate canon already);
ianchanning/status/2080594505942610160; eranshir/status/2047344052916380116 (~1,800x params claim);
fastinoAI/status/2087191704965410910; akshay_pachaar article 2029212227438518406 "How to Fine-Tune LLMs in 2026";
ADP announcement x.com/i/status/1983573211087565101 (no user handle, fxtwitter cannot resolve);
mikecarbone + heathercmiller repost pages (dups of tobi); daily.dev + Reddit mirrors of Shopify;
siguy.github.io data-flywheel blog; AlphaXiv "When Does Bigger Help?"; udit.co Qwen 3.5 small-model piece;
RedPajama-Data minhash dedup; ROOTS dedup docs; rensa PyPI; kensink.com / eqourse.com / ravikant.dev
data-pipeline writeups; TensorFlow-dying thread (junk); MichaelGannotti reshare (dup of jvr0x).

## Pass 2 deep reads and findings per research question

### Q1 tape-to-model recipes and data scale for first gains
- jvr0x "How fine-tuning actually works, explained by a 4B pirate" (2026-09-22, article;
  shared via jvr0x/status/2102835768138076280, 2026-09-23): Qwen3-4B-Instruct-2507 on DGX Spark,
  QLoRA 4-bit load, LoRA r=16 alpha=16 on all seven target modules across 36 layers (~33M trainable,
  <1%, 126 MB adapter), 2 epochs, LR 2e-4, batch 2 x grad-accum 4 (186 steps), max seq 2048,
  train_on_completions true. Food: 743 JSONL Q&A rows from a local 35B teacher in a ~120-line script
  (~10-15 min), 20 held out, 10% of rows given a generic system prompt to kill a
  "no system prompt = persona" leak. 7 min 20 s train, 678,785 tokens at ~1,540 tok/s, loss 2.14 -> 0.81,
  exported 4.3 GB Q8_0 GGUF. Lessons the estate should bank verbatim: fine-tuning teaches behavior not
  facts; generic Q&A teaches nothing new; chat-template mismatch silently breaks the model; loss drop
  is not answer quality; teacher errors propagate into the student.
- Together AI CoderForge-Preview (2026-02-25): 258,134 test-verified coding-agent trajectories,
  155,144 passing / 103K failing; plain SFT of Qwen3-32B on the PASSING SUBSET lifts SWE-bench
  Verified pass@1 23.0 -> 59.4, #1 open-data <=32B. Scale for first gains at 32B: ~155k passing tapes.
  The pass/fail split is itself a cleaning gate: train on verified wins, hold out fails.
- ADP paper (arxiv 2510.24702, v1 2025-10-28, v2 2026-03-04) + yueqi_song/gneubig threads:
  13 heterogeneous agent datasets unified into one "interlingua" format, 1.27M trajectories (~36B tokens);
  standardization ALONE (no new data) yields ~20% average gain over base models at 7-32B. Direct
  answer to the estate's tape-format question: a typed row schema is worth real points before any
  weights move.

### Q2 corpus cleaning gates the estate lacks
The estate's corpus-grade doctrine (code-agent-data SKILL.md) gates on: >=600 bytes, one
##Result-class section, contrast (wrong move vs corrected), tri-state labels, dated falsifiers.
Published pipelines run gates the estate does not have yet:
- Exact + near-duplicate removal with recorded counts: Fastino "Exact and near-duplicate removal
  brought the final mixture to 11,776 rows" (recipe A) - dedup is counted and reported, not assumed.
- Executability verification: "Every arithmetic program was executed, and 13,180 of 13,215 rows
  passed verification" (recipe C) - the tape's tool calls are re-RUN as the quality gate. This is
  stronger than the estate's "byte receipts" bar: replay the commands, keep only rows that pass.
- Teacher-free sourcing where possible: "All 6,251 targets were already executable, so no teacher
  model was needed" (recipe B) - spend credits only where execution cannot grade the output.
- The negative gate, verbatim: "Do not trust valid-but-easy synthetic data. Synthetic examples can
  pass every automated check and still be too easy, teaching the model nothing it did not already do."
  The estate's >=600-byte floor checks substance shape; it does not check DIFFICULTY. A holdout-difficulty
  gate (does the base janitor fail this row?) is the missing gate.
- PII scrub / provenance tags: not surfaced as X-native posts in this window; the standard published
  kit (minhash/LSH dedup, PII masking) lives in RedPajama-Data and ROOTS docs (candidates above,
  not deep-read). OWED if the estate wants pinned receipts for those two.
- Provenance at the format level IS published: ADP's typed rows carry source dataset identity across
  13 sources; that is the provenance-tag layer to copy for room.jsonl -> corpus packs.

### Q3 fine-tuned 2B-class vs prompted frontier on narrow chores
- Tobi Lutke (2026-09-01, 8,539 likes / 1.66M views): "finetuned 0.8b model beats GPT 5.6-sol xhigh
  in this very specialized task", attributed to the Shopify ML team's "self improving recursive flywheel".
  The strongest public claim that the janitor workload shape (narrow, repetitive, house-style chores)
  is winnable by a sub-1B model. Caveat banked from MRRydon (2026-09-02): one narrow task is not
  general competence; route cheap chores to specialists, keep frontier "for work where being wrong is
  costly" - which is exactly the estate's janitor-vs-specialist split.
- CodeRabbit (2026-08-11): Nemotron 3.5 Lightning (30B MoE) SFT on their own routing decisions:
  under 3 hours, under $100, exact route agreement 75.8% (GPT-class baseline) -> 80.4%, ~50% lower
  inference cost, training examples built by knowledge distillation from the stronger model's choices.
  Note: the estate already runs nvidia/nemotron-3.5-lightning:free as the or-nemotron lane
  (memory/runs/corpus_gap_research/CORPUS_GAP_RESEARCH.md:199) - this recipe is directly portable to it.
- Delta answer: ~4-5 points accuracy on a routing/decision chore for <$100; a 0.8B beating a frontier
  flag on ONE task with a flywheel behind it. No published "2B beats frontier generally" claim found.

### Q4 distillation cost vs the $180-220 credit budget
- CodeRabbit: <$100, <3 h, one narrow decision chore, +4 pts. INSIDE budget.
- Fastino: ~10 h autonomous search + adapters; one recipe trained in 11.6 min on 4xH200 for
  9.52M tokens. Small-adapter regime is minutes-cheap; the cost lives in data generation.
- Zain Hasan (2026-02-26): a 6.7B-token agentic-trace dataset cost $130k to generate (51k tasks,
  1.6k repos) - corpus-scale distillation is ~600x the estate's budget. NOT inside budget.
- Cost curve verdict: per-task distillation (one chore, thousands-to-tens-of-thousands of rows,
  teacher labels the decisions) is published at <$100; whole-corpus distillation is published at
  $100k+. The estate's $220 buys 2-4 CodeRabbit-shaped chores, not a CoderForge.

### Q5 own-workdays-as-training-set (the DNA cycle)
- Tobi's flywheel line is the marquee confirmation: "self improving recursive flywheel" is credited
  as the precondition for the 0.8B win - the filed-workdays loop is the product, not a side effect.
- Moda (YC W26, $6.1M raised) productizes the loop one layer earlier: "Turn production agent traces
  into validated improvements for your agent harness" - traces feed prompts/tools/skills/evals FIRST,
  weight mutation is not even the default surface. This matches the estate's own gate instinct
  (judge tapes corpus-grade before feeding Stage 2/3) and suggests the DNA cycle's first turn should
  target harness objects, with QLoRA as the second turn.
- Learned lessons published: ADP shows format unification is worth ~20% before new data; Fastino
  shows unverified-easy rows are the failure mode of self-generated data; jvr0x shows teacher errors
  propagate, so the funded-tier teacher's own mistakes must be filtered before the 2B eats them
  (the estate's sibling evals-self-improvement sweep already banked the Shopify Sidekick HN thread,
  HN 49561583 - same company, adjacent lane, not a dupe of the tobi X post).

## OWED (could not resolve, not asserted)
- cyi12 "1.5B parameter model fine-tuned on 200-500 good examples" post status id (search never
  returned the permalink; claim unverified beyond snippet).
- "Continual Learning for AI Agents: How to Actually Build It" (x.com, 2026-06-02) author + id.
- RedPajama-Data / ROOTS dedup docs read end-to-end (banked as candidates only).
- The tobi post's attached screenshot contents (image not described by the door).

## Receipt
All fetches this session via WebFetch: 9 fxtwitter JSON resolves (1 x 404 on article endpoint),
4 web pages (arxiv, fastino.ai, coderabbit.ai, ycombinator.com), 12 WebSearch calls (4 lanes
hit 429/1302 and were re-issued narrower). Overlap greps run against catalog/catalog.jsonl
(674,146 lines) and memory/ with the item phrases (recursive flywheel, 0.8b, coderabbit, nemotron,
coderforge, 130k, 6.7B, agent data protocol, 1.27M, cognitive core, DGX Spark, Javi1,
valid-but-easy): only pre-existing nemotron LANE usage found; zero title/phrase dupes; sibling
sweep evals-self-improvement-hn.md holds the adjacent Shopify Sidekick HN item.
