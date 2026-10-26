# STEAL: finetuning-adaptation (7 deep-read finds, sweep-level) - 2026-10-06 - REV 2

Area: finetuning-adaptation
Banked by: steal-finetuning-adaptation (Mag Resource Harness steal gopher)
Source sitting: watch/inbox/frontier_olm_2026-10-06/sweep/finetuning-adaptation-hn.md
(cited as "sweep:<line>"). REV 2 answers the round-2 critique in full: five repairs, each
re-verified by a run or read THIS sitting, evidence inline. Every repair claim below was
executed in this sitting; round-1 carries are marked as carried. Nothing rides REV 1's
text alone.

CONFIDENCE VOICE (repair R2): these seven are DEEP-READ SWEEP-LEVEL banks, not
confirmation-seat rows. The estate's own law, re-read this sitting at
watch/inbox/frontier_olm_2026-10-06/lens/burns.md:92-95: the decision-model wave "rests
on FIVE SWEEP-LEVEL rows, none confirmation-seat passed. It is a lead, not a find; treat
as pending confirmation, never as banked truth." The 10-06 sweep's confirmation pass
(sweep:221-267) confirmed the 28 items of 2026-10-05, not these seven; these seven carry
confidence 1 from the ask plus end-to-end thread reads in the sweep receipts, which is
sweep-level bank quality, nothing higher. The StealCard JSON below opens with that caveat.

## Revision 2 repairs (evidence ran this sitting)

- R1 (probe leg 0 - the blocking fix). The REV 1 probe's gate is dead on arrival as
  written: I ran the exact instrument it named, `.venv/Scripts/python.exe -c "from
  mag.verb import weekly_trigger; print(weekly_trigger())"` -> `{'n': 0, 'accuracy':
  None, 'meter_valid': False, 'trigger_ge_0880': False}`. The 7-day cutoff is
  mag/verb.py:493 (`cutoff = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()`,
  def weekly_trigger at :487, gates at :504-505), and memory/runs/fleet_bench/scores.jsonl
  holds exactly 8 rows (rg -c ""), all ts 2026-09-19T15:52-15:54Z - 17 days stale, outside
  the window, so upgrade+pull+score returns UNMEASURED either way and the two-sided
  falsifier never fires. The gate's own writer is mag/verb.py:462 `def meter_record`,
  whose docstring carries the label law (:465-467): "every row must name non-model label
  provenance -- a receipt path, arithmetic, or operator adjudication -- in evidence; a row
  without evidence is decoration and is refused at write time. Idempotent by id." The
  fold's falsifier leg names the shape (memory/continuity/seat_memory_20260927/
  jev-salon2-fold-20260919.md:33-36, read this sitting): "40 rows, three label classes,
  non-model provenance", with the standing counter ":36: 40 rows may never clear 0.880
  honestly", and the economist leg names the constraint (:28-30): "the label meter is the
  binding constraint, not the bill." REV 1 quoted :36 but never stated the current n=8
  stale state; REV 2 states it and adds LEG 0 to the probe: manufacture 40+ fresh
  fleet-labeled rows through meter_record before any upgrade/pull/score.
- R2 (confidence voice). Title retitled "7 deep-read finds, sweep-level"; the
  burns.md:92-95 caveat now leads the card and the StealCard JSON's first sentence. REV
  1's "7 confirmed finds" inflated the estate's own pending-lead register and is struck.
- R3 (find-set provenance mapping). REV 1's header said "sweep items 1, 2, 3, 4, 5, 7, 8",
  implying identity mapping; the true mapping to the sweep's pass-2 deep-read sections is:
  find 1 = sweep:101 (### 1 Laya), find 2 = sweep:115 (### 2 CUA-S1), find 3 = sweep:164
  (### 5 llama.cpp), find 4 = sweep:132 (### 3 Red Hat), find 5 = sweep:149 (### 4 Jeff),
  find 6 = sweep:184 (### 7 Mini-AGI), find 7 = sweep:194 (### 8 nimble). The calibration
  numbers REV 1 rode in its JSON ("82% confidence at coin-flip accuracy") belong to sweep
  item 6 (### 6 Synthpop, sweep:174-182, HN 49933643), which is NOT in the seven-find set
  - it is named here as a sweep-window bank outside this find-set, and the falsifier leg
  cites it as such.
- R4 (citation drift). REV 1 cited mag/lora_pipeline.py:5-6 for the QLoRA model line and
  :9-10 for the hands-box 3090. grep -n this sitting: the QLoRA model line is :8 ("Local
  6B inference card: QLoRA 4-bit on Qwen2.5-1.5B or Gemma-2B") and the hands-box 3090 is
  :10-11. Corrected below.
- R5 (overlap ledger extension). REV 1 missed three estate holdings, each read this
  sitting: (a) find 3's source (huggingface.co/blog/ggml-org/decision-models-in-llamacpp)
  is estate-held since 10-05 as row 1 of the five backing rows in
  watch/inbox/frontier_olm_2026-10-05/DIGEST.md:77, banked at
  frontier_olm_2026-10-05/sweep/open-local-language-models-hn.md:62-73 (full roster, read
  this sitting) and frontier_olm_2026-10-05/sweep/inference-efficiency-hn.md:76-84
  (latency table: Julia-1 144M 3 ms, Laya 421M 5 ms, Kev-4B 12 ms, lev 36 ms, OpenJev
  43 ms on one RTX PRO 6000; sample response input_tokens 130 / output_tokens 0; the
  0.25-vs-0.80 confidence-routing datum). (b) Find 7's core is estate-held at
  open-local-language-models-hn.md:33 ("9B (nimble, Bespoke Labs, 91 ms per decision on
  an M5 Max)") and :68-69 ("Ollama ships it in 0.35 with nimble 9B, tev1 4B and
  tev1:0.8B"); the genuine increments are only the Apache 2.0 license and the 75.7%
  13-benchmark panel (the critic's first-hand fetch of ollama.com/library/nimble
  confirmed 9B/Bespoke/Apache/75.7/<100ms//v1/systemone/requires 0.35+). (c) Find 1's
  prior-art core is estate-held at open-local-language-models-hn.md:181-183 (sibling
  thread 49736660, 97 pts, 2026-09-17: "open Jev-shaped prior art exists (arXiv 2503.23303
  from March 2025 plus 2510.01237)... Zero-shot generality, not the architecture, is
  Jev's actual moat" - 2510.01237 was omitted from REV 1) and watch/LIBRARIAN_REPORT.md:708
  ("arxiv:2503.23303 <- watch\inbox\frontier_olm_2026-09-30\sweep\
  evals-self-improvement-reddit.md +2"). REV 1's "only Laya hit is a Gutenberg word"
  (sweep:339-340) was scoped to catalog + four Jev files and missed the sibling sweep one
  directory over; find 1's genuine increment is the 1363-pt thread's practitioner
  economics, not the prior-art discovery. The 10-06 sweep's own framing "the
  decision-model wave the 10-05 pass missed" (sweep:55) is therefore FALSE for the find
  1/3/7 cluster; this card corrects its own framing and flags the sweep line, edits
  nothing in the source seat's receipt.

## Find provenance (corrected per R2/R3/R5)

Confidence voice per find, overlap status first:

- **Find 1 (Laya thread, HN 49765348, 1363 pts, sweep:101-113) - INCREMENT over
  estate-held prior art.** Held: OLLM:181-183 (2503.23303 + 2510.01237, thread 49736660)
  and LIBRARIAN_REPORT.md:708. New here: the practitioner economics ("Jev made a bunch of
  workloads we had on Luna or Gemini 10x cheaper and 2x faster"; 10,000+ inventory items
  "in minutes and for less than 1 cent"; 5 specialized tasks beaten by a custom model at
  orders-of-magnitude lower cost - sweep:107-111), plus the in-thread architecture dispute
  ("the paper does not describe a model architecture, it describes a system built on
  embeddings, rag, and orchestrators" - sweep:106-107).
- **Find 2 (CUA-S1, HN 49767564, 95 pts, sweep:115-130) - GENUINELY NEW, resolves an
  estate dead end.** The Jev Salon 2 fold holds only "CUA-S1/classifier.dev blocked"
  (jev-salon2-fold-20260919.md:24, re-read this sitting) and the 09-19 session recorded
  "CUA-S1 NOT FOUND in trycua/cua" (memory/agent_sessions/orc-t39817fa14e.json, presence
  verified round 1 and by the round-2 critique). The thread supplies location (trycua/cua,
  built from jevlike), params (706k, 2.8 MB checkpoint), training (first iteration <30 min
  on synthetic data), and scoped results (99.7% vs 83.6% whole set; leave-alone steps 100%
  vs 74%; 7-9 ms local vs 260-280 ms hosted - sweep:117-123).
- **Find 3 (llama.cpp /v1/systemone, ggml-org blog, sweep:164-172) - CONFIRMATION of
  estate-held DIGEST row 1** (DIGEST.md:77; OLLM:62-73; IE:76-84). The find adds the
  source-fetched quote ("The model returns a probability for each option in a single
  forward pass") and PR #29818; sizes/endpoints/latencies were already banked 10-05.
- **Find 4 (Red Hat guardrails, HN 49933476, 160 pts, sweep:132-147) - GENUINELY NEW
  falsifier side.** The estate's only prior Jev-skeptic datum was fleet-internal (SemIf
  0.845 vs Jev 0.883, watch/inbox/JEV_CONSOLIDATED_BRIEF_20260919.md:122, carried from
  round 1's read; re-confirmed by the round-2 critique). New: the hedged external verdict
  ("decision models like Jev do not reliably outperform [other] models in speed or
  accuracy. However, they rightly refocus industry attention on lightweight, task-specific
  inference paradigm"), the title-editorialization catch, and the independent benchmark
  cross-cites (hard-decisions.anth.us, ml6, tessl "3-4 times cheaper, 7-14 times faster",
  sweep:136-142).
- **Find 5 (Jeff, HN 49883844, 575 pts, sweep:149-162) - GENUINELY NEW.** Adoptable
  Apache-2.0 open weights (Qwen3.5+Gemma fine-tunes, Jev-compatible API; 2B at 83.1% vs
  Jev's 83.0 five-benchmark; 0.8B ~28 ms on M4 Max) AND the classical-baseline falsifier
  (embeddings+logistic "matches or beats Jev and Laya" on AG News/Emotion/MASSIVE/
  Banking77 at <1 ms; linear SVM + bag-of-words; ModernBERT 0.4B; field report 70% vs
  94% - sweep:154-161). Hardware honesty: author trained on 2x DGX Spark, not consumer
  parts (sweep:162).
- **Find 6 (Mini-AGI, HN 49783133, 277 pts, sweep:184-192) - GENUINELY NEW, watch-only.**
  Full pretraining (not finetuning) on an 8 GB RTX 3070 Laptop via dynamic expert
  add/prune MoE + batch-1 continuous stream; no weights; author's own words "way too small
  and undertrained to make any generalization claims" / "Worse than GPT-2 as it stands"
  (sweep:190-191).
- **Find 7 (nimble in Ollama 0.35, HN 49908997, sweep:194-202) - CONFIRMATION INCREMENT
  over estate-held OLLM:33/:68-69.** New: Apache 2.0 license, 75.7% mean across 13 public
  benchmarks, choice/noul/score types via /v1/systemone (find quote + the critique's
  first-hand fetch). Already held: 9B/Bespoke/M5 Max latency (91 ms held vs the find's
  "under 100 ms"), Ollama 0.35 distribution, /v1/systemone. Banked as the fold's gated
  front-runner: "Nimble front-runner + taroleo hedge, gated on our weekly >=0.880, never
  oracle-scored" (jev-salon2-fold-20260919.md:23, re-read this sitting).
- **Outside the set, cited by the falsifier leg only:** sweep item 6 (### 6 Synthpop,
  HN 49933643, sweep:174-182): ~575k API calls; "Jev was right only 51% of the time, no
  better than a coin flip, yet its confidence rose to 82%"; recalibration left "roughly 20
  points overconfident"; 90%+ confidence filter kept 99.75% correctness on familiar
  ground. Sweep-window bank, not one of the seven.

## The mechanism (stated under the pending-lead caveat)

Burns law first: the rung is a LEAD (burns.md:92-95). What the seven deep reads add is
shape and falsifier, not confirmation. The lead's shape, as the finds support it:

- **Rung A, scoped specialists (706k-421M params) trained on the estate's OWN synthetic
  data.** CUA-S1 (find 2) is the only existence proof in the set, and it is strong on its
  scoped task (99.7% vs 83.6%; leave-alone 100% vs 74%; 7-9 ms vs 260-280 ms). The port
  inverts the estate's original adaptation question: not "finetune gemma:2b" but "carve
  the fleet's most repetitive typed judgment into a sub-1M-param specialist trained on
  estate-synthesized examples." Training-hardware feasibility on this host is OWED (the
  <30 min figure names no consumer parts in the quoted text; Jeff's author used DGX
  Spark).
- **Rung B, adoptable general decision models (0.8B-9B, Apache 2.0).** Jeff (find 5) and
  nimble (find 7) are pullable weights; the fold already gates nimble at >=0.880
  never-oracle-scored (fold:23) and its falsifier leg demands "40 rows, three label
  classes, non-model provenance" (fold:33-36). Adoption rides the estate's meter, never
  vendor panels - and the meter is currently UNMEASURED (see R1).
- **Rung C, serving: /v1/systemone, one forward pass, per-option probabilities.**
  Source-confirmed and estate-held since 10-05 (find 3 + DIGEST row 1). DRIFT MEASURED
  ROUND 1 AND RE-RUN THIS SITTING: `ollama --version` -> "ollama version is 0.34.3";
  `where llama-server llama-cli nvidia-smi` -> not found. The pending row's serving
  clause (burns.md:93 "llama.cpp + Ollama 0.35") is aspirational on THIS host; the Ollama
  0.34.3 -> 0.35 upgrade (or a llama.cpp build with PR #29818) is the mechanism's literal
  first move after leg 0. OWED: which host, if any, the day-5 "Ollama 0.35" claim
  described.
- **The falsifier leg is part of the mechanism.** Red Hat's hedge (find 4), the Jeff
  thread's classical baseline (find 5: embeddings+logistic at <1 ms matches/beats
  Jev/Laya on Banking77-class tasks; 70% vs 94% field report), synthpop calibration
  (sweep ###6: 82% confidence at coin-flip accuracy), and the fold's own counter
  (fold:36) compose the adoption gate: beat the classical baseline AND clear >=0.880 on
  fleet-labeled rows (n>=40, non-model provenance, never oracle-scored), else the rung
  stays a lead. The estate's own prior datum already shows hosted Jev is beatable on its
  terms (SemIf 0.845 vs 0.883, JEV_CONSOLIDATED_BRIEF:122).
- **NOT ported.** Mini-AGI (find 6): no weights, "worse than GPT-2", watch-list only.
  The QLoRA arm of the estate's own LoRA organ on THIS host: `where nvidia-smi` not found
  and `Get-CimInstance Win32_VideoController` -> "AMD Radeon RX 5600 XT 4293918720"
  (re-run this sitting; WMI saturates at 4 GiB, vendor spec 6 GB), RDNA1 fails the L30
  gates (sweep:279-289); mag/lora_pipeline.py:8 names the local QLoRA option and
  :10-11 the hands-box 3090 24 GB rung that the arm would need.

## Estate organ map (per-find feeds and port moves)

1. **Find 1 -> percolator** (mag/percolator.py; memory/percolator/invariants.json,
   "invariants dict 648" verified by parse round 1): attach 2503.23303 AND 2510.01237
   (the REV 1 omission) to burns.md:92-95 as prior-art; bank the thread economics into
   the driving-ladder's cheap-first SHERPA math.
2. **Find 2 -> gopher fleet** (swarm_worker / swarm_surface, mag/organ_map.py:115 and
   :103, ids re-pinned this sitting): carve the fleet's most-repeated typed judgment into
   a CUA-S1-shaped specialist trained on estate-synthesized examples; resolves the fold's
   blocked row (fold:24) with a location and measured numbers.
3. **Find 3 -> sovereign mirror** (mag/lora_pipeline.py is the organ's adaptation
   module): make /v1/systemone real here - Ollama 0.35 upgrade or llama.cpp PR #29818 -
   so classification never leaves the box.
4. **Find 4 -> percolator (falsifier leg)**: adoption-gate candidate rule - "beat
   embeddings+logistic AND >=0.880 on fleet rows (n>=40, non-model provenance), else
   drop" - riding the existing promote gate, no second retirement path.
5. **Find 5 -> gopher fleet + quantizer** (mag/state_quantizer.py): pull, GGUF-quantize,
   meter-gate Jeff 0.8B/2B; the classical baseline is a mandatory arm, not a footnote.
6. **Find 6 -> quantizer, watch-only**: dynamic expert add/prune rhymes with the
   quantizer's knot idiom; no port until weights exist. (Water graph, mag/water_computer.py,
   organ id water_computer mag/organ_map.py:48: weakest feed, watch-datum only.)
7. **Find 7 -> sovereign mirror + gopher fleet**: measure the fold's front-runner on the
   ESTATE's own meter instead of the vendor's 13-benchmark panel; the gate exists
   (fold:23), the local number does not (n=0 measured this sitting).

**Context pack side-effect** (mag/organ_map.py:81, id context_pack): if any rung clears
the gate, typed-classification asks leave the premium dispatch tier; the pack's SHERPA
cheap-first leg gains a rung below gemma:2b it does not currently know. Find 1's
economics ("<1 cent" per 10k classifications) is the pricing datum for that re-rank.

## The probe (one, falsifiable, cheap, this week - now with the leg that makes it fire)

**LEG 0 (first move, no new hardware): manufacture the labeled set the gate is starving
for.** Write 40+ fresh Fleet-Bench rows through mag/verb.py:462 `meter_record` - three
label classes (A/B/C per the existing 8-row shape), every row's evidence naming non-model
provenance per the writer's own law (:465-467: receipt path, arithmetic, or operator
adjudication; evidence-less rows are refused), truths fixed by construction, ids fresh so
idempotence never inflates n - all inside one 7-day window so `weekly_trigger()` actually
reads them. The existing 8 rows' evidence fields (arithmetic divisibility, os.stat byte
receipts, law-registry citations) are the pattern to scale; 40 such items are a half-day
of the janitor tier's scut. **LEG 1:** score the current replica (gemma:2b) on the set via
meter_record; `weekly_trigger()` must now return n>=40 and a real accuracy - the first
measurement the fold's gate has ever had. **LEG 2:** upgrade Ollama 0.34.3 -> 0.35,
`ollama pull nimble` (Apache 2.0), score nimble on the SAME truths, receipted in a
parallel file (scores.jsonl is the replica meter; do not conflate arms), same bar
>=0.880 never-oracle-scored. **Falsifies both ways once n>=40:** below 0.880, the rung
stays a pending lead exactly as burns.md:92-95 demands and the port dies at the gate
(fold:36's counter - "40 rows may never clear 0.880 honestly" - gets its answer);
at/above 0.880, one typed-classification lane wires through /v1/systemone and the
five sweep-level rows earn their confirmation seat. Named caveat: 9B on a 6 GB AMD card
CPU-offloads, so local latency is OWED (91 ms is an M5 Max figure, OLLM:33); if the pull
will not fit, the same truths on the 144M-421M roster (Julia-1, Laya, via llama.cpp -
not installed here, `where` checked this sitting) is the small-rung alternate arm.

## Verified THIS sitting vs carried vs OWED

Ran this sitting: `weekly_trigger()` (n=0 output above); sed/rg of mag/verb.py (:462,
:465-467, :487, :493, :504-505); cat + rg -c of memory/runs/fleet_bench/scores.jsonl
(8 rows, ts 2026-09-19); sed of jev-salon2-fold-20260919.md:19-40 (:23-24, :28-30,
:33-36); rg of mag/lora_pipeline.py (:8, :10-11); sed of
frontier_olm_2026-10-05/sweep/open-local-language-models-hn.md (:30-35, :62-73,
:178-186); sed of frontier_olm_2026-10-05/sweep/inference-efficiency-hn.md:76-84;
rg+sed of frontier_olm_2026-10-05/DIGEST.md (:9, :73, :77, :78); sed of
watch/LIBRARIAN_REPORT.md:705-710 (:708); host drift trio re-run (ollama 0.34.3;
llama-server/llama-cli/nvidia-smi not found; AMD Radeon RX 5600 XT 4293918720);
sed of burns.md:92-95; rg of organ_map.py ids (:48, :81, :103, :115).
Carried (run in this session's round 1; re-confirmed by the round-2 critique under its
own re-runs): JEV_CONSOLIDATED_BRIEF_20260919.md:122; invariants dict 648 parse;
sweep pass-2 section numbers (:101, :115, :132, :149, :164, :174, :184, :194);
sweep:55 framing; sweep:339-340 Gutenberg note.
NOT run by this seat, credited where used: the round-2 critique's first-hand fetch of
ollama.com/library/nimble (9B/Bespoke/Apache/75.7/<100ms//v1/systemone/0.35+); the
critique's own weekly_trigger re-run and _read receipt existence checks.
OWED: leg 0's 40 rows (the probe's first move); any /v1/systemone endpoint or model pull
on this host; which host runs Ollama 0.35; CUA-S1-shaped training feasibility on AMD;
find-side source URLs not refetched by this seat (the seven ride the ask's confidence-1
finds plus the sweep's `_read_*.txt` receipts).

## StealCard JSON

```json
{"area": "finetuning-adaptation", "steal": "SWEEP-LEVEL DEEP-READS, NOT CONFIRMED ROWS: the estate's own law (burns.md:92-95) holds the 'rung UNDER gemma:2b' as a pending lead - five sweep-level rows, none confirmation-seat passed - and these seven finds deepen the lead, they do not confirm it. The lead's shape after the deep reads: RUNG A, scoped specialists (CUA-S1: 706k params, 2.8 MB, <30 min on synthetic data, 99.7% vs hosted Jev 83.6% scoped, 7-9 ms local vs 260-280 ms hosted, leave-alone steps 100% vs 74%; genuinely new - it resolves the estate's 09-19 'CUA-S1 NOT FOUND in trycua/cua' dead end with a location and numbers) trained on the ESTATE'S OWN synthetic data instead of finetuning gemma:2b. RUNG B, adoptable Apache-2.0 decision models (Jeff 0.8B/2B at 83.1% vs Jev 83.0 five-benchmark, Jev-compatible API - genuinely new; nimble 9B, 75.7%/13 benchmarks - confirmation increment over the 10-05 OLLM sweep's holdings at :33/:68-69, new only in license + panel), pulled and gated on the estate's own meter (mag/verb.py:505, n>=40 rows, accuracy>=0.880, non-model provenance), never vendor panels. RUNG C, serving via /v1/systemone (one forward pass, per-option probabilities; llama.cpp PR #29818, roster 144M-27B; Ollama 0.35) - source-confirmed but ALREADY ESTATE-HELD since 10-05 as DIGEST.md:77 row 1 (open-local-language-models-hn.md:62-73, inference-efficiency-hn.md:76-84 latency table); DRIFT measured: this host reads Ollama 0.34.3 with no llama.cpp, so the serving clause is aspirational here. The falsifier leg is load-bearing: Red Hat's hedge (do NOT reliably outperform LLM-as-judge or classical classifiers), the Jeff thread's embeddings+logistic baseline (<1 ms, matches/beats Jev and Laya; 70% vs 94% field report), synthpop calibration disease (sweep item 6, outside the find-set: 82% confidence at coin-flip accuracy), and the fold's counter (40 rows may never clear 0.880 honestly) compose the adoption gate: beat the classical baseline AND clear 0.880 on fleet-labeled rows or the rung stays a lead. GATE STATE MEASURED: weekly_trigger() reads n=0; scores.jsonl holds 8 stale 09-19 rows outside the 7-day window - the meter has never been valid. NOT ported: Mini-AGI full-pretrain MoE (no weights, 'worse than GPT-2', watch-only) and the QLoRA arm on this host (AMD RX 5600 XT RDNA1, no CUDA; the 3090 hands-box rung mag/lora_pipeline.py:10-11 is the only local training escape). Find-provenance mapping to the sweep's pass-2 sections: find 1=s:101, find 2=s:115, find 3=s:164, find 4=s:132, find 5=s:149, find 6=s:184, find 7=s:194. Full REV 2 write-up banked at watch/inbox/frontier_olm_2026-10-06/steal/finetuning-adaptation.md.", "source_url": "https://huggingface.co/blog/ggml-org/decision-models-in-llamacpp", "estate_map": "Five organs, under the burns.md:92-95 pending-lead caveat. (1) GOPHER FLEET (mag/organ_map.py:115 swarm_worker, :103 swarm_surface): rung A is the port - carve the fleet's most-repeated typed judgment into a 706k-param specialist trained on estate-synthesized examples (CUA-S1 shape), or adopt Jeff 0.8B/nimble; single-digit-ms local latency frees gemma:2b and premium dispatch. (2) SOVEREIGN MIRROR (mag/lora_pipeline.py adaptation module; QLoRA line :8, hands-box 3090 :10-11): make /v1/systemone real on the estate's own stack (Ollama 0.34.3->0.35, measured this sitting, or llama.cpp PR #29818) so classification never leaves the box. (3) PERCOLATOR (mag/percolator.py; memory/percolator/invariants.json, invariants dict 648): attach arxiv 2503.23303 AND 2510.01237 to burns.md:92-95 as prior-art (Laya thread economics are the increment - the prior-art core was already held at the 10-05 OLLM sweep:181-183 and LIBRARIAN_REPORT.md:708); write the adoption gate as a percolator candidate rule - beat embeddings+logistic AND >=0.880 on n>=40 fleet rows with non-model provenance, else drop - riding the existing promote gate. (4) QUANTIZER (mag/state_quantizer.py): rung-A training data comes from the quantizer's compiled thought (memory/corpus/quantized_thought/instructions_*.jsonl) as the synthetic set; GGUF quantization of Apache-2.0 weights is the quantizer's idiom in weight space; Mini-AGI expert add/prune is watch-only. (5) CONTEXT PACK (mag/organ_map.py:81): find 1's economics (10x cheaper/2x faster, <1 cent per 10k classifications) re-rank the tier ladder below gemma:2b for typed classification - a cheapest rung the pack's SHERPA leg does not currently know. Water graph gets the weakest feed (watch-datum only, mag/organ_map.py:48).", "probe": "Three legs, leg 0 first because the gate is starved: (LEG 0) manufacture 40+ fresh Fleet-Bench rows through mag/verb.py:462 meter_record - three label classes (A/B/C), every row's evidence naming non-model provenance per the writer's own law (:465-467: receipt path, arithmetic, or operator adjudication; evidence-less rows refused), truths fixed by construction, all inside one 7-day window - because weekly_trigger() measured n=0 this sitting and scores.jsonl holds only 8 stale 09-19 rows outside the cutoff (mag/verb.py:493); (LEG 1) score the current replica (gemma:2b) on the set so weekly_trigger() returns n>=40 and the fold's gate gets its first real reading; (LEG 2) upgrade Ollama 0.34.3->0.35, ollama pull nimble (Apache 2.0), score nimble on the SAME truths receipted in a parallel file (scores.jsonl is the replica meter; do not conflate arms), same bar >=0.880 never-oracle-scored per jev-salon2-fold-20260919.md:23-24 and :33-36. Falsifier, two-sided once n>=40: below 0.880 the 'rung under gemma:2b' stays a pending lead exactly as burns.md:92-95 demands and the port dies at the gate (answering the fold's own counter that 40 rows may never clear 0.880 honestly); at/above 0.880 one typed-classification lane wires through /v1/systemone and the five sweep-level rows earn their confirmation seat. Caveat: 9B on the 6 GB AMD card CPU-offloads so local latency is OWED (91 ms is an M5 Max figure, already estate-held); if the pull will not fit, the same truths on the 144M-421M roster (Julia-1, Laya, via llama.cpp - not installed here) is the small-rung alternate arm.", "chars": 25643}
```
