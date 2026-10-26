# STEAL CARD: inference-efficiency (frontier_olm_adhoc) - rev 2

source-fetched: adhoc - seat: steal-inference-efficiency - moment: 2026-10-11 - rev 2
(round 1 drew a six-fix critique; the core passed byte-verification, the defects were
wording/citation class, all fixed below and re-verified this session)

## Revision ledger (round-2 critique -> this rev)

The critique byte-verified every load-bearing claim (all quotes, numbers, dates, view
counts match the raw captures; all sweep-bank and estate line cites check; the
overlap conclusion holds) and named six fixes. Each applied and re-verified this
session:

1. BLOCKING lint fail fixed: the wired EMPTY_REASONING carrier is
   tools/model_garden.py (:296 the INFERENCE-BUDGET entry comment, :363-364 the
   guard_terminal + raise); mag/model_garden.py does not exist (ls confirmed) -
   round 1 transcribed its own rg output's tools\ prefix as mag\. Round-1 run of
   .venv/Scripts/python.exe tools/citation_lint.py check --files on this card:
   FAIL exit 1, PATH-MISSING x2. This rev: exit 0 (command and output in Receipt).
2. Saluki catalog truth corrected: 1 row, not 2. grep -i -c saluki
   catalog/catalog.jsonl = 1; the row (cdcc328361fd) carries 2 string occurrences
   (path + title). The sweep's grep -o | uniq -c counted occurrences as rows and
   round 1 inherited a nonexistent trajectory-log row and said it was inspected -
   the hand-copied-count class the census law strikes. Overlap conclusion unchanged.
3. corpus/ ngram hits are TWO unrelated classes, not one: game_estate 'engram'
   strings (4+4+1 across three files) AND corpus/library/ai-engineering-from-scratch
   course content (ngram + ngramBackoff tokens in site/figures-nlp2.js, plus the
   phases/19-capstone-projects/14-speculative-decoding-server phase dir). Neither
   is the swept finding; conclusion unchanged, wording now names both classes.
4. Handle-overlap claim scoped to byte truth: catalog holds zero rows for every
   author handle and for PREFIX_AWARE; memory/'s only hits are this run's own
   memory/trajectory/steps.jsonl (19 matching lines; the file is gitignored, which
   is why directory-level rg misses it - instrument note) plus 'janmm' substring
   collisions in memory/corpus/ai_canon DL-book HTML. No rows predate this run.
5. "The estate's own prior plan (a 2B-class draft model)" reworded: '2B-class
   draft' is the lens question's own phrasing
   (watch/inbox/frontier_olm_adhoc/lens/questions.md:305), not a banked estate
   plan (no memory/rib/ hit for it).
6. "this IS that post" -> "presumably cures": the burns-lens OWED item is
   carried-unchanged and names no specific post (lens/burns.md:235).
Plus the critique's non-blocking completeness add, taken: steal 2 now names the
estate's own family-conditional negative case (glm-5.3-flash emptied at ANY cap,
memory/rib/RIB_INFERENCE_BUDGET_20261001.md:21-22) and its probe stratifies by
family from the start. Bare lens/sweep anchors expanded to full repo-relative
paths (the 10 round-1 lint WARNs were shorthand-anchor misses, legal under the
a05-r2 default but cheap to cure).

## Provenance (nothing fabricated)

Five confirmed finds arrived in the round-1 ask. Every quote and number in this card
was re-verified THIS session against the raw fxtwitter JSON captures the sweep seat
banked (the byte truth; x.com itself was not fetched - auth wall, and the estate's X
surface is an OWED carry per commit e8eedd8eb):

- find 1 ngram: sweep/raw/x_grok/_sweff_fx_ngram_sebastavar_2107803719815291333.json
- find 2 empty-cap: sweep/raw/x_grok/_sweff_fx_empty-cap_cozybearlog_2102052987334209707.json
  + _sweff_fx_empty-gw_cozybearlog_2101006279510827440.json (both loaded via
  .venv/Scripts/python.exe json this session; full texts printed and matched)
- find 3 blind-cost: _sweff_fx_blind-cost_janmm_va_2108656759523168641.json +
  _sweff_fx_blind-empty_janmm_va_2108656761968414975.json
- find 4 saluki-mtp: _sweff_fx_saluki-mtp_ghulamurtaza__2108674475344462013.json
- find 5 prefix-aware: _sweff_fx_prefix-aware_SupersocksIntel_2098310560253165822.json

All under watch/inbox/frontier_olm_adhoc/. Dash law: quotes normalize en-dashes and
arrows to ASCII hyphens / -> (marked per item, the sweep seat's own convention at
watch/inbox/frontier_olm_adhoc/sweep/inference-efficiency-x.md:6); the byte-true
unicode forms live in those JSONs.

## Overlap (the standing-law check, run this session)

The sibling card's standing law (watch/inbox/frontier_olm_adhoc/steal/
kv-cache-context-engineering.md:36-40) says overlap checks must grep the
frontier_olm run dirs, not catalog + memory alone. Run (rg over
watch/inbox/frontier_olm_adhoc, catalog/, memory/, corpus/; terms: ngram,
sebastavar, cozybearlog, janmm, ghulamurtaza, SupersocksIntel, PREFIX_AWARE): ALL
FIVE finds are already banked at SWEEP layer by
watch/inbox/frontier_olm_adhoc/sweep/inference-efficiency-x.md (find 1 at :21-24,
find 2 at :26-29, find 3 at :31-34, find 4 at :41-44, find 5 at :46-49; the raw JSON
captures above are that bank's). Catalog + memory hold no rows for these subjects
predating this run: catalog has zero rows for every author handle and for
PREFIX_AWARE; saluki's catalog truth is 1 row (cdcc328361fd, the UnderdogAI model
page) carrying 2 string occurrences, path + title (fix 2 above); memory/'s only
hits are this run's own trajectory steps (memory/trajectory/steps.jsonl, 19 lines,
gitignored) plus 'janmm' substring collisions in the DL-book HTML under
memory/corpus/ai_canon. The 'ngram' hits in corpus/ are two unrelated classes:
game_estate 'engram' strings and ai-engineering-from-scratch course content
('ngram'/'ngramBackoff' in site/figures-nlp2.js; a 14-speculative-decoding-server
capstone phase dir in the same library - course docs, the class the sweep's own
overlap section already covered at :78). So THIS CARD IS THE STEAL-LAYER
DISTILLATION, not a first bank: what it adds over the sweep bank is the per-organ
port map, the estate-side gap each steal exposes, and one falsifiable probe per
steal. The sweep named RQ verdicts and rib actions (:83-97); it did not map organs
or design probes.

## The five steals, organs, and probes

### 1. n-gram speculative decoding with NO draft model (gopher fleet)

Mechanism (verified in the raw capture): llama.cpp 0.6.0, --spec-type ngram-map-k
with all defaults (size-n 12, size-m 48, min-hits 1; spec-draft-n-max is irrelevant
without a draft model), full serving line -ub 2048 -c 196608 -ngl 99 --jinja.
Measured: acceptance on code edits 90 to 96% at ~44-token drafts, so edit-shaped
decode runs ~170 tok/s while new text stays ~50 (~3.4x on the edit class, zero new
weights loaded). The same post rules OUT the fancier variants: ngram-map-k4v,
ngram-mod, ngram-cache did not beat plain ngram-map-k on edits, and none speed up
new text. Post: https://x.com/sebastavar/status/2107803719815291333 (2026-10-07,
37 views - low engagement, banked on substance).

Organ: the GOPHER FLEET's local janitor decode lane. The estate's edit-shaped work
(re-render, patch, re-fire with a standing prefix) is exactly the acceptance class
measured here. Port move: serve one janitor lane from llama-server with the flag
flipped, batch-1 only - the ds_workhorse batch lane is excluded by the banked
high-batch caveat (specdec at high batch collapses 3x -> ~1.1x, the sweep's
near-miss at :63). Where a draft model is nonetheless on the table, note the
framing's provenance: '2B-class draft' is the lens question's own phrasing
(watch/inbox/frontier_olm_adhoc/lens/questions.md:305), not a banked estate plan,
and for the edit class ngram-map-k dominates any draft model where it applies: no
second model, no tokenizer-match risk.

Probe (headline, this week, an afternoon, $0 API): on the local llama.cpp box,
A/B llama-server with and without --spec-type ngram-map-k over a 20-item
edit-shaped job (re-render 20 known files with a standing prefix), recording tok/s
and accepted-draft stats per item. Falsifier: if edit-class acceptance lands under
60% or the speedup under 1.5x on OUR workload shapes, the steal closes for the
estate's class of work and the specdec shelf entry drops to "tried, not ours".

### 2. The cap must sit ABOVE the reasoning draw range (percolator + inference budget)

Mechanism (verified in both raw captures): same one-line prompt, temperature 0. At
cap 2000 the draws were 1945/2000/2000 thinking tokens and "Two of three runs came
back empty, billed in full, finish stop"; at cap 8000 the same prompt drew
2030/3158/2421, "Natural stops. Real answers. None got near the cap." Author's
law: the 2000 cap sat INSIDE the natural draw range, "slicing runs mid-thought and
looking exactly like a model failure"; raising it above the distribution made the
empties disappear. Tagline-class draws 2k to 3.2k. Gateway sibling (2026-09-18):
"400 tokens on the usage line, 0 in the answer... content field came back empty
and reasoning is not even a key in the response." Posts:
https://x.com/cozybearlog/status/2102052987334209707 and :2101006279510827440.

Organ: the PERCOLATOR (invariant mint, memory/percolator/invariants.json shape:
text + count + first_seen/last_seen) feeding the inference-budget enforcement organ
mag/inference_budget.py. The estate law already matches the terminal half: the
ONE-BUG census (memory/rib/RIB_INFERENCE_BUDGET_20261001.md:16-44, worst case
$20.53 of $29.91 re-fire theater; digest at
watch/inbox/frontier_olm_adhoc/lens/laws.md:45), the EMPTY_REASONING marker
(mag/inference_budget.py:36, terminal return :310, same-params refire terminal at
:151), wired into exactly two carriers (tools/hermes_burn.py:459-460,
tools/model_garden.py:363-364) with seven unwired jackets named at
watch/inbox/frontier_olm_adhoc/lens/laws.md:100. The OUTSIDE autopsy adds the
causal half the estate's law lacks as an invariant: a cap inside the family's draw
range is the failure's CAUSE, and cap-above-range is a third, preventive recovery
upstream of the terminal marker (the rib's two recoveries are re-stage with
FAMILY_TABLE recipe or switch family). FAMILY-CONDITIONAL CAVEAT (estate's own
census, named so the law never over-generalizes): glm-5.3-flash emptied at ANY
max_tokens cap (2600/4200/9000/16000, finish=length) per
memory/rib/RIB_INFERENCE_BUDGET_20261001.md:21-22 - for that family the
cap-inside-range mechanism does not apply and the terminal marker carries the load
alone. The cap-law is per-family, not universal.

Probe ($0, records mining, no API, stratified by family from the start):
histogram reasoning-draw vs max_tokens cap for every EMPTY_REASONING-class
incident already on disk (the rib census at
memory/rib/RIB_INFERENCE_BUDGET_20261001.md:16-44; usage records under
memory/runs/hermes_burn/), one stratum per model family. Prediction: outside the
glm-5.3-flash stratum, every empty-with-stop incident had its cap at or below that
family's observed draw ceiling. Falsifier: empties in non-glm strata that occurred
with caps ABOVE the family's draw range would break the cap-inside-range law, and
the third recovery closes as not-our-failure-mode (the marker law stands either
way - it is already estate-measured).

### 3. Cents-per-blind-point tie at ~8x price (model-garden economics)

Mechanism (verified in both raw captures): same blind-scored job, "Blind scores
out of 5, and the billed cost per intro: DeepSeek V4.1 Flash: 3.93, $0.00175;
Claude Sonnet 5.5: 3.93, $0.01412" (also Haiku 5.5 3.80 at $0.00103, Gemini 3.8
Flash 3.30 at $0.01775; Gemini's score covers 2 of 3 intros because one call
failed twice). Sibling post on the same lane: "at max_tokens 1,500, all four
models spent most of it reasoning. Two DeepSeek outputs came back empty... the
rerun gave every model 6,000" and "Reasoning bills as output." Posts:
https://x.com/janmm_va/status/2108656759523168641 + :2108656761968414975.

Organ (honest mapping): the MODEL-GARDEN ECONOMICS RIB, not one of the six charter
organ names. Cost-per-blind-point is already the estate's champion metric
(watch/inbox/frontier_olm_adhoc/lens/laws.md:41) and the instruments-only law
(watch/inbox/frontier_olm_adhoc/lens/laws.md:43) governs how this lands: an
outside practitioner measurement is a PRIOR to beat, never a cell fill. It feeds
the standing off-state re-measure (open question 5 at
watch/inbox/frontier_olm_adhoc/lens/laws.md:99) as both the economics shape
(cents per completed task, not per token) and a second independent empty-at-cap
autopsy on the exact flash lane that re-measure targets.

Probe (this is the re-measure design constraint set, the paid arm the estate
already owes): one 20-item job on the flash lane with explicit thinking-off on the
wire, caps set above the measured draw range (steal 2), finish_reason recorded
per item, cents-per-completed-task as the headline number, and off-ness VERIFIED
per ask class (the banked Thinking Inertia caveat at sweep :56-59: on open-ended
asks off is not off). Falsifier: if estate-measured cents-per-task at blind parity
does not undercut the premium lane by a wide margin, the 8x anchor does not
transfer to our task mix and the ladder keeps judgment on the primes.

### 4. Copy the base family's MTP head into the finetune (model shelf; presumptive OWED cure)

Mechanism (verified in the raw capture): Saluki 27B ships without an MTP draft
head; it is a Qwen3.8-27B finetune, so the author "copied the base model's MTP
layer (~350 MB) into the IQ2 GGUF." On 2x RTX 3060, 128k context, llama.cpp:
prose/code 23 -> 36-37 tok/s (en-dash normalized in quote), and exact copy/edits
with MTP + ngram lookup ~159 tok/s (~7x on the exact-copy class). Post:
https://x.com/ghulamurtaza_/status/2108674475344462013 (2026-10-09, 2,227 views).

Organ (honest mapping): the JANITOR MODEL SHELF. The charter organ name
"quantizer" resolves to mag/auto_quantize.py:1-27, which is analytics-resolution
quantization (L0-L5 buckets for telemetry), NOT model-file quantization - the true
port target is which GGUFs the local fleet runs and what gets grafted into them.
This is the cheapest-draft recipe on consumer GPUs: no second model loaded, one
~350MB layer copy from the base family. Banking it PRESUMABLY cures a carried OWED:
the burns lens lists "Saluki secondary X post" as owed
(watch/inbox/frontier_olm_adhoc/lens/burns.md:235) - the lens item is
carried-unchanged and names no specific post, so the cure is presumptive until the
burns seat confirms.

Probe ($0 existence gate first): does the estate's janitor family have a
base-family MTP head available to copy, and does the local llama.cpp build support
MTP for that architecture? (filesystem + model-dir + llama.cpp docs check; the
sweep bank flagged the same gate at :85 "OWED: check"). Only if yes: graft per the
recipe and A/B tok/s on the prose/code lane. Falsifier: no family MTP head exists
for our janitor family => the steal closes as not-applicable to the fleet (the
ngram path of steal 1 needs no head and remains the default).

### 5. Prefix-sticky routing across instances (water graph + context pack)

Mechanism (verified in the raw capture): "Random routing on a multi-instance LLM
endpoint wastes your prefix cache." SageMaker PREFIX_AWARE routes the same prompt
beginning to the same instance so the KV cache actually warms; on Llama 3.1 70B,
7x ml.p5.48xlarge, long 8k shared prefixes: P50 TTFT down up to 77%, KV hit rate
~25% -> >80%, throughput +15-16%, routing overhead 1.3-1.9ms. Overload protection
still spills to a quieter instance; knobs are PrefixLength + ConcurrencyThreshold
on the variant, no container rewrite. Post:
https://x.com/SupersocksIntel/status/2098310560253165822 (2026-09-11; links the
AWS ML blog, not fetched - numbers carried by the post text and raw capture).

Organs: the WATER GRAPH's routing law and the CONTEXT PACK's frozen prefix
together. The estate's deliberate-ask law already freezes a shared prefix (the
percolated invariant "[steer] Elevate with a deliberate ask: frozen prefix
(cache-shared) + tight ask" in memory/percolator/invariants.json; the freeze
machinery at mag/context_pack.py:948 freeze_system_prompt and :988 evolving_tail)
- that frozen front is exactly the "long shared prefix" the measurement keys on.
The routing decision belongs to the routing-as-physics engine (mag/water_graph.py
docstring :1-15: valves, gravity tick, one-way check valves generalized from
mag/water_computer.py), but NOTHING routes janitor traffic through it today: the
port is a NEW thin router in front of the multi-ollama janitor fleet that hashes
the frozen prefix and routes to the warm instance, spilling on overload (Ollama
itself has no cross-instance prefix-sticky router; the sweep's RQ4 verdict at :88).

Probe ($0, minutes, deterministic): extend tools/prefix_cache_sim.py (on disk,
15,083 bytes; its sibling instrument tools/lru_null_arm.py:1-12 already replays
the estate trail tapes) with a routing-arms race over 2- and 4-instance fleets:
random routing vs frozen-prefix-hash sticky, measuring the KV-hit proxy at the
estate's real prefix-sharing rate. Falsifier: if sticky routing gains under 10pp
of KV hit at our actual sharing rate, the win does not transfer (our prefixes may
already share so uniformly that instance-level warming has no headroom) and the
router port closes until the fleet grows.

## OWED (never asserted)

- gemma/gemma4-family MTP head existence + local llama.cpp MTP support (steal 4's
  gate; also flagged by the sweep bank at :85).
- The AWS blog behind steal 5 was not fetched this session (post text + raw
  capture carry the numbers; the sweep bank flagged the same at :104).
- Estate-side hardware truth: I did NOT verify the local GPU box or any llama.cpp
  0.6.0 install this session (no bench was run here; the sweep's "RX 5600 XT box"
  at :85 is the sweep seat's claim, not mine). Steal 1's probe includes
  install/verify as step 0.
- Whether any estate carrier today sets max_tokens inside a family's draw range
  (steal 2's probe measures this from records; not yet measured; the glm-5.3-flash
  stratum is expected to fail the cap-law by its own census entry).
- No pytest was run this session (nothing in this card changes code; the probes
  name the instruments their future runs will use).

## Receipt (what this session actually ran)

- Citation lint (the critique's blocking check, rerun after the fixes):
  .venv/Scripts/python.exe tools/citation_lint.py check --files
  watch/inbox/frontier_olm_adhoc/steal/inference-efficiency.md -> exit 0,
  "ok records=1 anchors=29 numbers-checked=6 blocking=0 warns=15" (round-1 state,
  per the critique's run: exit 1, PATH-MISSING x2). The 15 remaining WARNs are
  all TOKEN-MISS heuristic class on multi-cite sentences, WARN-only and legal
  under the a05-r2 default (enforce-tokens=False in the output).
- Fix verifications: ls mag/model_garden.py (No such file) vs ls tools/model_garden.py
  + sed :294-297/:362-365 (comment at :296, guard_terminal + raise at :363-364);
  grep -i -c saluki catalog/catalog.jsonl = 1 and grep -o -i saluki | wc -l = 2;
  rg -i -l ngram corpus/library/ai-engineering-from-scratch (site/figures.js,
  site/figures-nlp2.js, the 14-speculative-decoding-server phase) + token sample
  (ngram x2, ngramBackoff x2 in figures-nlp2.js) + rg -i -c ngram corpus/game_estate
  (4/4/1, all 'engram'); rg -i -c over memory/trajectory/steps.jsonl for the six
  subject terms = 19 lines + git check-ignore confirms the file gitignored (why
  directory rg misses it); sed lens/questions.md:303-307 ('2B-class draft model'
  at :305); rg glm-5.3-flash in the rib -> :21-22 (any-cap empties) and :52 (uncap
  note); sed tools/hermes_burn.py:459-460 (guard_terminal + raise).
- Round-1 verifications still standing (unchanged this rev): overlap greps (rg -i
  per term over watch/inbox/frontier_olm_adhoc, catalog/, memory/, corpus/);
  .venv/Scripts/python.exe json-load + print of both cozybearlog captures; rg text
  extraction displaying the full sebastavar, janmm_va x2, ghulamurtaza_, and
  SupersocksIntel capture texts; sed lens/laws.md 40-48 and 96-102;
  corpus/CURRICULUM.md 36-44 (INFERENCE-OPT shelf at :38-43); sed
  memory/rib/RIB_INFERENCE_BUDGET_20261001.md (ONE-BUG census region); rg for
  EMPTY_REASONING (mag/inference_budget.py:19,36,40,151,310;
  tools/hermes_burn.py:237,459-460; tools/model_garden.py:296,363-364;
  tools/code_swarm.py:9), reasoning_content (tools/ds_workhorse.py:89),
  freeze_system_prompt/evolving_tail (mag/context_pack.py:948,988); ls
  tools/prefix_cache_sim.py (15,083 bytes) + tools/lru_null_arm.py (12,421 bytes);
  head mag/auto_quantize.py, configs/mates.yaml, mag/water_graph.py; read in full:
  sweep/inference-efficiency-x.md and steal/kv-cache-context-engineering.md/.json.
- Not run: any pytest, any local bench, any x.com or AWS blog fetch (provenance
  went through the banked raw captures instead).
