# STEAL CARD: open-local-models via arxiv (frontier OLM 2026-10-10) - ROUND 2

Seat: steal gopher "steal-open-local-models via arxiv". Two confirmed finds handed by the
scout (both confidence 0.95), digested at
watch/inbox/frontier_olm_2026-10-10/sweep/open-local-models-arxiv.md:21-22 (banked items
5 and 6). Round 1 banked; round 2 lands the four blocking fixes from the critique, each
verified on this seat's own instruments before the edit.

## Round 2 revision log (blocking fixes, where each landed)

1. FIND-1 PROBE RESTATED AT n=19. Verdict census run this seat (round 2): python Counter
   over memory/frontier/scout_findings.jsonl returns {'STEALTH': 5, 'WATCH': 7, 'PASS':
   2, 'STEAL_NOW': 5} total: 19. The round-1 "freeze 20 rows" failed its own contract;
   the probe now freezes ALL 19 rows and sets its falsifier against the majority-class
   baseline (always-WATCH = 7/19).
2. FIND-2 PROBE NOW RIDES THE HELD A/B HARNESS. The estate already built and ran the
   paired-arm instrument: watch/inbox/frontier_olm_2026-10-08/sweep/quant_ab/ (RECEIPT.md:1
   "RUN COMPLETE (2026-10-08)", :12 "deterministic tool-failure-recovery tasks x 5 prompt
   phrasings = 50 runs per arm", :13 temperature 0.0 + paired per-item seeds, :27 arm B
   qwen2.5:7b-instruct-q8_0; run_ab.py 24,544 bytes in the same dir; spec commit
   6685db6bc at :5). Probe-2 laws inherited verbatim from the 10-08 kv-cache card:
   frontier_olm_2026-10-08/steal/kv-cache-context-engineering.md:199 "No arm ever mixes
   paths." and :203 "task-level completion, never perplexity, plus decode t/s per arm."
   Poolability declared below. The dual-correctness gate is also NOT paper-borne for this
   estate: its twin is STANDING_RAILS law 2, ok_api + ok_material
   (tools/ds_workhorse.py:19,:46,:151-153) - the paper's numerical + downstream gate is
   external validation of a gate shape the estate already enforces on batch lanes.
3. JSON TWIN BANKED: this card now has its own {area, steal, source_url, estate_map,
   probe, chars} twin at steal/open-local-models via arxiv.json, same convention as the
   sibling REV-2 twin (open-local-models.json), validated by json.load this session.
4. SHARED-SURFACE HYGIENE: watch/inbox/seis_arxiv_2610.04646.xml (this run's own export
   fetch, 2,856 bytes) moved out of the inbox root into
   frontier_olm_2026-10-10/sweep/raw/seis_arxiv_2610.04646.xml (mv run this seat; mtime
   preserved Oct 10 12:51; ls of the inbox root now returns zero seis* files; INDEX.json
   grep for the old path returned 0 both before and after, so nothing dangles).

Non-blocking folds: water_graph fracture-law cite widened to :25-33 (round 1 cited :1-24
only); steps.jsonl telemetry count moment-stamped at three moments (below); find-1's
review instrument distinguished from mag/rel_mem_eval.py:1-10 (memory-discrimination
harness, a different instrument - the nested-strictness review scorer is NOT a re-bank);
held-work named plainly in its own section.

## Overlap truth (checked BEFORE the steal, per the REV-2 lesson)

The sibling card steal/open-local-models.md:3-5 was REJECTED in its round 1 for a false
"genuinely new" claim, so this card leads with its own overlap receipt.

- Full-tree scan run this seat (round 1; python walk over catalog/, memory/, corpus/,
  configs/, docs/, queue/ plus watch/inbox/ minus today's dir; 756,244 text files; scan
  script kept in %TEMP% and removed after): paper ID 2610.10827 appears in
  watch/inbox/frontier_olm_2026-10-09/sweep/open-local-language-models-arxiv.md:16,:36,:64,:128
  and frontier_olm_2026-10-09/DIGEST.md:41. FIND 1 IS NOT NEW TO THE ESTATE: yesterday's
  sibling sweep deep-read it, banked it, and folded it into the DIGEST decision "Janitor
  tier: no base swap; compound the current tier" with the Grammar 0.8B fine-tune named as
  the lever. The scout's "absent everywhere" was false as stated because its grep surface
  list omitted prior frontier_olm digests. This card's legitimate delta over the 10-09
  bank row: the three mechanism shapes, the organ wiring, and the two falsifiable probes.
- Paper ID 2610.04646 (SEIS) appears ONLY in memory/trajectory/steps.jsonl, which is
  live sweep-session telemetry, not a knowledge surface. Census-denominator law applied:
  16 occurrences at the round-1 scan moment; 24 occurrences / 14 lines at the critique's
  moment; 31 occurrences / 18 lines at this seat's round-2 recount (moment
  2026-10-10T21:21:25Z). The count grows with the run's own footsteps and is never
  differenceable across moments. The bare "SEIS" tokens found elsewhere are substring
  noise (e.g. the SEISMIC watch app description in
  frontier_olm_2026-10-03/sweep/tmp/candidates_full.jsonl). FIND 2 IS GENUINELY NEW:
  zero hits across every knowledge surface (catalog, all curated memory dirs, corpus,
  docs, queue, configs, watch/inbox minus today).
- Catalog counts run this seat (round 1; io.open read of catalog/catalog.jsonl,
  323,798,504 bytes): Qwen3.5=32, 2610.10827=0, 2610.04646=0, SEIS=0, mini-sglang=0,
  "Grammar Concept Annotation"=0. Both papers are new to the CATALOG even though find 1
  is not new to the inbox. (The critique reproduced these counts on a catalog since moved
  to 324,004,975 bytes - same zeros, denominator named.)

## Find 1: Grammar Concept Annotation at Scale (arxiv 2610.10827, published 2026-10-07)

URL: https://export.arxiv.org/api/query?id_list=2610.10827
Authors verified this seat (round 2 re-fetch of the feed): Marjan Celikik, Ana Peleteiro
Ramallo, Javier Morales. Round-1 OWED discharged.

Verified (round 1 re-fetch, reviewer independently confirmed): scout quote verbatim -
"the deployed 0.8B model and a 4B reference comparator outperform prompted GPT-5.4 and
GPT-5.6 Sol in precision and recall" (sentence continues "under nested matching criteria
of increasing strictness: concept, evidence span, and correctness"). Numbers confirmed
present in the abstract: serving cost down approximately 16x; online experiment +15.8%
engagement, +2.1% scheduled hours, +13.2% GMV from new lessons. Mechanism phrases
"filtered and rebalanced teacher-generated supervision" and "compact matched prompt" are
abstract-verbatim.

### The steal (mechanism, not the model)

Three shapes, none of them "small models are good":
1. Contract internalization. Fine-tuning on filtered and rebalanced teacher-generated
   supervision moves the annotation contract out of the prompt and into adapter weights,
   so the 0.8B deploys with a compact matched prompt instead of verbose frontier
   instructions. Prompt verbosity was the frontier tax and they deleted it from the
   serving path.
2. Nested-strictness scoring. The benchmark reports precision AND recall at three rising
   strictness levels (concept, evidence span, correctness) against human-curated gold.
   One accuracy number hides exactly the failures a scoring lane cares about; the ladder
   does not.
3. Deployment gate online. The offline win only banked after a feature-level online
   experiment moved engagement and business metrics. Offline precision stays provisional
   until the online delta lands.

### Estate organ + port move

Feeds the PERCOLATOR scoring lane with the GOPHER FLEET as supervision supply:
- mag/percolator.py:23-27: --candidates ingests frontier digests into
  memory/percolator/candidates.jsonl as promoted=False, and promotion happens only
  through the reviewed-signal path. Port: rebuild the review instrument in the paper's
  shape - a frozen gold file of already-adjudicated estate rows, scored at two strictness
  levels with precision + recall reported, never a single accuracy number. Instrument
  boundary: this is NOT a re-bank of mag/rel_mem_eval.py:1-10, whose harness measures
  memory discrimination (telling related-but-distinct memories apart); the nested
  strictness here scores annotation verdicts against adjudicated gold.
- mag/gopher_lite.py:15-16: the label-farm chore (receipts dossier to Fleet-Bench rows)
  is exactly the "filtered teacher-generated supervision" supply line the paper
  fine-tuned on. Port: route label-farm output as the adapter's training rows.
- corpus/library/kev/PLAN_Qwen35.md:3,:14: the estate already ships Kev on Qwen3.5
  0.8B/4B/9B bases (executed 2026-09-20, pins recorded). The paper externally validates
  that exact family-and-scale choice, so the port is an adapter through the estate's own
  kev pipeline, not a new dependency. This aligns with the standing 10-09 DIGEST decision
  (frontier_olm_2026-10-09/DIGEST.md:41: no base swap, fine-tuning is the lever).

### Probe (falsifiable, cheap, this week) - RESTATED AT n=19

Gold-reproduction probe, all local, zero paid dispatch, one evening: freeze ALL 19 rows
of memory/frontier/scout_findings.jsonl (census run this seat: STEAL_NOW 5 / STEALTH 5 /
WATCH 7 / PASS 2, total 19; benefit fields all int). Blind the verdict and benefit
fields, hand each row's name + description to qwen2.5:3b-instruct and gemma:2b (both
installed per `ollama list` run this seat, round 1) under one compact contract at
temperature 0 with per-row paired seeds (the run_ab.py discipline,
quant_ab/RECEIPT.md:13). Readouts: exact-verdict accuracy against the recorded gold, plus
per-class precision and recall at two strictness levels (loose: verdict class only;
strict: verdict class + benefit within 2). FALSIFIER: if neither local model beats the
majority-class baseline (always-WATCH = 7/19 = 36.8% exact-verdict accuracy) by 10 or
more points, a small local model cannot hold the annotation contract at janitor scale
and the port must budget kev-pipeline adapter training before any percolator wiring.
Honest bounds: the gold is estate-adjudicated, not crowd-human (the probe measures
reproduction of estate judgment, the same gold class the percolator would gate on), and
19 rows make per-class recall coarse - the probe decides direction, not fine rates.

## Find 2: SEIS: Self-Evolving Inference Systems (arxiv 2610.04646, published 2026-10-03)

URL: https://export.arxiv.org/api/query?id_list=2610.04646
Authors verified this seat (round 2 re-fetch): Zhen Xu, Jingyu Liu, Zongze Li, Tahseen
Rabbani, Ce Zhang. Round-1 OWED discharged.

Verified (round 1 re-fetch, reviewer independently confirmed): scout quote verbatim -
"reaches 3.27X the throughput of the original mini-sglang implementation and beats SOTA
engines like vLLM, TensorRT-LLM, and SGLang in the single-request workload" (Qwen3-0.6B
on H100). Also confirmed present: correctness "tested in terms of numerical difference
and downstream accuracy on math and long-context retrieval tasks"; "the speedup comes
from redesigning the whole engine"; "building on earlier sessions beats independent
attempts".

### The steal (mechanism)

Honest framing first: this is the estate's own percolator/ratchet doctrine arriving in
serving systems, so the steal is external validation plus one instrument, not a new
philosophy. Two portable laws, now with outside proof:
1. Evolve the WHOLE serving path, not isolated knobs - the 3.27x came from whole-engine
   redesign, and sessions that inherited earlier findings beat independent attempts.
2. No throughput claim banks without a dual correctness gate (numerical difference AND
   downstream task accuracy). The estate already holds this gate shape as STANDING_RAILS
   law 2, ok_api + ok_material (tools/ds_workhorse.py:19,:46,:151-153: the wire answered
   AND the material is real, empty text is not success); SEIS is the same law proven out
   in engine-evolution form.

### Estate organ + port move

Feeds the WATER GRAPH serving lane and the gopher fleet's serving surface. The estate
already runs three local serving surfaces (mag/ollama_policy.py, mag/lm_studio.py,
mag/llama_cpp_bridge.py), and mag/water_graph.py:1-33 is the routing-as-physics engine
(nodes, check-valve pipes, xor/sill junctions; fracture law at :25-33: sustained
full-bore pipes accumulate stress and burst closed) whose flows this loop would tune
under. Port: a bounded SEIS loop over the janitor serving lane - sweep {surface x num_ctx
x batch x keep_alive x quant variant} for the incumbent janitor, every mutation gated by
the dual check (numerical: bounded-diff outputs on a frozen task set; downstream: the
chore's own ok_api + ok_material scorecard), each session starting from the last winner
via the receipt/rib memory. That is the standing ratchet shape (registered winners pass
forward, unverified speedups block) applied to serving config instead of code.

### Probe (falsifiable, cheap, this week) - RIDES THE HELD HARNESS

Single-request bake-off on the run_ab.py shape (watch/inbox/frontier_olm_2026-10-08/
sweep/quant_ab/run_ab.py; its receipt at :1,:12,:13,:39 shows the discipline: 10
deterministic tasks x 5 prompt phrasings = 50 runs per arm, temperature 0.0, paired
per-item seeds, task-level readouts): arms = ollama vs llama_cpp_bridge vs lm_studio
serving the SAME installed model on the SAME frozen 50-run chore set, plus a num_ctx /
keep_alive sweep on the winning surface. Readouts per arm: single-request p50/p95 latency
and decode t/s; quality gate is task-level completion, never perplexity
(kv-cache-context-engineering.md:203), plus the ok_api + ok_material rails. POOLABILITY,
declared up front per "No arm ever mixes paths" (kv-cache-context-engineering.md:199):
cross-surface arms are NOT poolable with the 10-08 quant baseline (different serving
paths, different kernels, different overheads); only within-ollama knob arms share a
path family with the 10-08 Q4_K_M/q8_0 numbers and may be read against them. FALSIFIER:
if no surface or knob beats the ollama baseline p50 by 15% or more while passing the dual
gate, SEIS single-request headroom does NOT transfer to this host at the
config/engine-choice level and only whole-engine surgery (the paper's actual mechanism)
remains. Honest-outcome note kept from round 1: the abstract's own cause says the 3.27x
came from engine redesign, so the likely result is "config headroom small, surgery is the
real lever" - which would itself redirect the port away from knob-twiddling.

## Held, named plainly (re-banked work this card does not claim)

- Find 1 AS A FIND is the 10-09 bank row (frontier_olm_2026-10-09 sweep :64,:128 +
  DIGEST :41). This card claims only the delta: three mechanism shapes, organ wiring,
  two probes.
- The 50-run paired Ollama A/B harness shape: held and run 2026-10-08
  (sweep/quant_ab/, spec commit 6685db6bc). Probe 2 extends its arms; it does not
  re-invent the instrument.
- The dual correctness gate: held as STANDING_RAILS ok_api + ok_material
  (tools/ds_workhorse.py), predating this paper.

## Verification receipts (this seat, this session)

Round 1:
1. Abstract verification: fetched
   https://export.arxiv.org/api/query?id_list=2610.10827,2610.04646 - both entries
   returned; both scout quotes verbatim; 16x / +15.8% / +2.1% / +13.2% and 3.27X / vLLM
   / TensorRT-LLM / SGLang / dual-correctness wording / inherited-sessions wording all
   present. Published 2026-10-07T19:31:24Z and 2026-10-03T16:36:48Z match the find dates.
2. Catalog counts: python io.count over catalog/catalog.jsonl (323,798,504 bytes):
   Qwen3.5=32, both paper IDs=0, titles=0.
3. Full-tree overlap scan: 756,244 files; findings as stated in Overlap truth.
4. Local inventory: `ollama list` - 15 models, no Qwen3.5 present; qwen2.5:3b-instruct
   and gemma:2b installed (probe stand-ins).
5. Gold schema: memory/frontier/scout_findings.jsonl:1 read; verdict + numeric-score
   fields confirmed.

Round 2 (this revision):
6. Verdict census: python Counter over scout_findings.jsonl -> {'STEALTH': 5, 'WATCH':
   7, 'PASS': 2, 'STEAL_NOW': 5} total: 19.
7. Harness verification: quant_ab dir listed (run_ab.py 24,544 bytes, results_armA/B
   .jsonl present); RECEIPT.md greps at :1,:5,:12,:13,:27,:39 confirm RUN COMPLETE
   2026-10-08, spec commit 6685db6bc, 50 runs per arm, temperature 0.0 + paired seeds,
   5/5 on every one of the 10 tasks.
8. Rails twin: grep tools/ds_workhorse.py -> STANDING_RAILS law 2 at :19, ok_api +
   ok_material schema at :46, split implementation at :151-153.
9. Probe laws: kv-cache-context-engineering.md:199 ("No arm ever mixes paths.") and :203
   (task-level, never perplexity) located and quoted.
10. Hygiene fix executed: mv of seis_arxiv_2610.04646.xml into
    frontier_olm_2026-10-10/sweep/raw/ verified (2,856 bytes, mtime Oct 10 12:51
    preserved; inbox root now has zero seis* files; INDEX.json grep 0 before and after).
11. Bylines: round-2 re-fetch of the same feed returned 2610.10827 = Celikik, Peleteiro
    Ramallo, Morales; 2610.04646 = Xu, Liu, Li, Rabbani, Zhang.
12. Telemetry recount: 2610.04646 in steps.jsonl = 31 occurrences / 18 lines at moment
    2026-10-10T21:21:25Z (16 at the round-1 scan moment; 24/14 at the critique moment).

## OWED

- The 2610.10827 "compact matched prompt" artifact itself: abstract-level read only; the
  exact prompt pair lives in the paper body - OWED a full-text pull if the percolator
  port starts.
- The +15.8% / +2.1% / +13.2% online deltas are from a language-learning product; their
  transfer to estate surfaces is a hypothesis to probe, not a claim.
