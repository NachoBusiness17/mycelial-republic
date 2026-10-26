# SWEEP: inference-efficiency via arXiv (frontier_olm 2026-10-04, third round of this area)

stamp: source-fetched: 2026-10-04

Third pass over this area. Rounds one and two are on file and own their finds:
frontier_olm_2026-10-01/sweep/inference-efficiency-arxiv.md, frontier_olm_2026-10-02/sweep/
inference-efficiency-hn.md, and frontier_olm_2026-10-03/sweep/inference-efficiency-arxiv.md
(read in full this sitting; the 10-03 file itself folds an even-earlier 10-03 seat). Today's
sibling lanes in this same carrier also hold claims: the ID walk over sweep/*.md shows kv-cache
holding FACET 2609.37902 and PatchKV 2609.39329, quantization holding RATIO 2609.39801 and
STEPQuant 2609.38169 (register rows 37/42). All of those are excluded from my bank.

## Doors used, degradations honest

- export.arxiv.org/api/query Atom feeds: 7 queries this sitting (language-model-routing;
  cascade+language-model; inference-cost x cs.LG; speculative decoding; cost+routing+LLM;
  token+accounting; rate-limit+API), sortBy submittedDate desc, 15-25 results each. All seven
  returned full feeds, zero 403s, zero rate-limit contact.
- arxiv.org/abs pages: 13 fetched this sitting (2609.37402, 2609.32917, 2609.34712, 2610.00694,
  2609.38386, 2609.33141, 2610.01108 twice, 2610.00499, 2609.38697, 2609.40093, 2609.37362,
  2610.01955, 2609.38585). All answered. The parallel-abs timeout the 10-03 seat hit did not
  recur; no fallback was fabricated because none was needed.
- One WebSearch (free-tier quota measurement) returned results; it is a blog-tier door and its
  quota numbers are NOT banked (see RQ4).
- state/arxiv auto-digest stubs read directly: state/arxiv/2026-10-02/2610.01955v1.txt (full
  abstract, read this sitting) and the presence of state/arxiv/2026-10-01/2609.40093v1.txt.
- The recipe's arxiv.org/list/cs.CL/recent and /list/cs.LG/recent doors: NOT run (API coverage
  sufficed). Reported as not run, not as success.
- No HTML full texts were fetched this sitting; every banked item below is read at abstract-page
  depth with verbatim abstracts captured, one notch below the 10-03 seat's full-HTML standard,
  and marked so.

## Pass 1 (broad)

7 feeds, roughly 140 entries, of which the in-window named consideration set is about 60 items
(window 2026-09-06..2026-10-04 as the feeds date them). Routing feed standouts not already held:
FlexRouter 2609.38585, SaveRouter 2609.37402 (10-01 banked, excluded), RouteFM 2609.37362,
SeLMRoute 2609.34736, LLMRouter 2608.06867 (outside window), WISERouter 2607.23765 (outside).
Cascade feed: HARISSA 2609.38006 (held), Planner-as-Router 2609.32917 (held), RSI-Router
2609.34712 (held), Protocol-Preserving Context Trimming 2609.16461, Cascade unlearning 2609.16890.
Inference-cost feed: DWS 2610.00499, Fork-dLLM 2609.39859, Schur-Replay NVFP4 2609.36654,
ThunderEP 2609.40093, DLFP 2609.38386 (10-02 HN-held, excluded), PatchKV 2609.39329 (sibling).
Spec-dec feed: Divergence-Flips 2610.00694, AgSpec 2610.01108 (held), DRelay 2610.01439, HAWK
2610.00623, UBTree 2609.39972 (held), Cascadia 2609.38697, CAST 2610.00321, DScale 2609.37532.
Cost-routing feed: OpCaches 2609.33141, RSI-Router (dup), SLM-LLM Learning-to-Ask 2610.01236
(today's open-local sibling holds it), MoSE 2609.39138, SparLeak 2609.38830. Token-accounting
feed: nothing on-point (token-level training papers; DYOR 2610.01955 surfaced via the
tokenomics-adjacent hit and confirmed fresh). Rate-limit feed: nothing in-window on provider
rate-limit shapes; nearest are FailureAtlas 2607.17525, ContinuityBench 2607.15899, KeyPooling
2608.17485, HiveMind 2604.17111 - all outside the 30-day window, listed not banked, same verdict
the 10-03 seat reached on the same feed.

## Pass 2 (deep)

Nine abs pages read end to end this sitting: 2609.37402, 2609.32917, 2609.34712, 2610.00694,
2609.38386, 2609.33141, 2610.01108, 2610.00499, 2609.38697, 2609.40093, 2609.37362, 2610.01955,
2609.38585 (thirteen fetches; several were dedupe reads of already-held items and are excluded
from the bank). Eight items banked below, all read by me this sitting, none full-HTML.

## Answers to the five research questions (evidence read this sitting; no estate instrument run)

**RQ1 tank accounting.** No in-window arXiv paper publishes a per-lane token/spend ledger schema
for harnesses; the published near-neighbors are per-REQUEST cost prediction (DWS 2610.00499:
two-dimensional block-step cost surface, predictor runs on one CPU core, transfers across
hardware without retraining) and DLFP's "exact token accounting" evaluation methodology (10-02
held). The estate ledger memory/runs/hermes_burn/usage.jsonl was read this sitting (lines 1-6):
flat rows {ts, id, model, turn, prompt_tokens, completion_tokens, cost_usd, ok}. Verdict: no
schema migration is needed to adopt the published practice, because public designs are a subset
of what the estate already records per dispatch; the only field class public designs add is
predicted-vs-realized cost, which appends as a new column with zero breaking change (append-only
law, memory/rib/RIB_MD_RECORD_20260921.md via lens/laws.md:17). Public practice lags the estate
here, it does not lead it.

**RQ2 UNMEASURED routing cells.** The window's economics papers converge on the probe-budget
question the instruments-only law (lens/laws.md:31) already forces: RouteFM 2609.37362 measures
that EIGHT observations per candidate suffice for a capability estimate that beats the strongest
baseline by 2.23 points on a held-out benchmark, and SaveRouter (10-01 banked) measures the
break-even volume of supervision itself (1.9-9.5x reduction, and the supervision level that
minimizes serving cost differs from the one that achieves earliest payback). Public
cost/latency data can therefore only PRIORITIZE which cells to probe (PaR's held 25x
frontier:small per-token gap says probe the expensive columns first); the cell values themselves
still require the estate's own instruments. Minimal funded probe set implied: ~8 funded
observations per (family, capability) cell for readable-class asks. This is a proposal read off
papers, not a measurement; no cell was filled.

**RQ3 cascade/router savings curves.** The held banks (PaR 44 percent cost for minus 2.9 points;
RSI-Router 48.3 percent) already carry the curve shape. This sitting adds the two objectives the
estate's tier ladder lacks names for: FlexRouter 2609.38585 optimizes ANSWER COVERAGE
(probability at least one sampled model is right) via DPPs that penalize shared failure modes -
the fan-out width law's objective function, formalized - and adapts subset size per ask instead
of fixing a budget. RouteFM shows a frozen router adapting to a new pool via context alone. DYOR
2610.01955 marks the boundary: a 3B-active RL policy matches Claude Opus 4.5 on soft-Brier
(0.254 vs 0.256, n=265) at about 5 percent of inference cost on a BOUNDED evidence task class -
a third datapoint for the question-class law (readable routes cheap, lens/laws.md:30), and a
warning that the class boundary is task-specific. None of the window validates a premium-to-
small route for the simulation class; the estate's 0/5 there stands unchallenged.

**RQ4 free-tier ceilings and rate-window decay.** Negative result, honestly: 2 targeted arXiv
feeds (token+accounting, rate-limit+API) plus one WebSearch surfaced NO in-window measurement
study of free-tier token ceilings or rate-window decay. The nearest items are all outside the
window (HiveMind 2604.17111: OS-style proxy cut concurrent-agent failures on rate-limited
endpoints from up to 100 percent to 0-18 percent - genre intel, April 2026, not banked;
FailureAtlas 2607.17525; KeyPooling 2608.17485). WebSearch surfaced only commercial blog quota
numbers (a Google AI Studio free-tier 250K TPM / 5-15 RPM claim, snippet-only, NOT read at
primary, NOT banked). The grid's CONTRADICTION at RIB_MODEL_GARDEN_ROUTING.md:186-192 therefore
stays exactly where the 10-03 seat left it: resolvable only by the owed limit-kill census and
funded live probes; arXiv is the wrong door for provider limit shapes.

**RQ5 local janitor serving on consumer hardware.** Three measurable levers this window, none
needing new hardware: (a) MEASUREMENT INSTRUMENT - Divergence-Flips 2610.00694: total variation
(not KL) predicts decision flips at flip-rate/TV ratio median 1.05 across 802 compressed copies
of 19 models, and predicts vLLM greedy draft acceptance at 1.1-2.4 percent mean relative error
without per-task calibration; this is the missing cheap instrument for the janitor quant lane
(measure TV, know how many decisions the quant moved). (b) CONTROL - DLFP (10-02 held) cut P99
inter-token latency 27.7 percent on a 0.6B model but failed to generalize to 8B/32B/two-GPU;
per-model tuning is the law, matching the per-animal harness profiles (lens/laws.md:34).
(c) FLEET SHAPE - Cascadia 2609.38697 serves LLMs on commodity AI-PC fleets over a libp2p QUIC
mesh with CA-issued ed25519 admission certs, signed response receipts, hash-chained logs, KV
prefix mobility, 3.10x throughput at three nodes - the estate's murmur party line and receipt
laws arriving independently in serving form; its sharded-chain mode assumes NPUs the RX 5600 XT
does not have. ThunderEP 2609.40093 (2.00x/1.53x dispatch/combine over NCCL, 1.66x e2e on RTX
4090/5090 PCIe systems) is MoE-only genre intel: the dense gemma janitors ride none of it; it
prices the future multi-card MoE janitor option. The 10-03 verdict stands: self-speculation and
early-exit remain the classes that fit a 6 GB card; this window added no AMD-portable kernel.

## Overlap greps (commands run this sitting)

git grep --no-index over catalog/, memory/, docs/, state/, and all four frontier_olm sweep dirs,
per-ID and per-title-token:
- 2610.00694: one hit, the 10-03 file's pass-1 feed listing (spec-dec feed line), never in any
  bank list. NEW.
- 2610.00499: zero hits anywhere. NEW.
- 2609.37362: zero hits anywhere, including the 10-03 pass-1 lists. NEW.
- 2609.38585: zero catalog/memory; named in the 10-03 pass-1 routing feed, not banked there
  (their bank list is items 1-7 and excludes it). NEW.
- 2609.33141: zero catalog; one auto-digest register row at
  memory/runs/corpus_gap_research/ARXIV_REGISTER.json:5564; no prose bank. NEW.
- 2609.38697: zero catalog/memory; named in the 10-03 pass-1 spec-dec feed listing only. NEW.
- 2609.40093: state/arxiv auto-digest stub only (state/arxiv/2026-10-01/2609.40093v1.txt +
  digest.jsonl); zero prose bank; zero sibling overlap. NEW with stub noted.
- 2610.01955: state/arxiv stub (state/arxiv/2026-10-02/2610.01955v1.txt, full abstract read this
  sitting) plus one catalog pointer row ("Learning to Forecast" token, single hit); no prose
  bank. NEW with stub noted.
- Title-token noise resolved: "Cascadia" hits in memory/corpus are the Cascadia Sugar Snap Pea
  cultivar in mycology prose (pmc9673936.xml), not the paper.

## OWED / not run

- Probe 3 (per-dispatch tank accounting counting requests) and the limit-kill census: both stay
  owed and were not fired; this sweep ran zero models.
- No estate grid cell was filled and no A/B was fired; paper numbers above are PRIORITIZATION
  evidence, never cell values (instruments-only law, lens/laws.md:31).
- No HTML full texts fetched; every bank below is abstract-page depth (the 10-03 seat's deeper
  standard was full-HTML for its top five).
- /list/cs.CL and /list/cs.LG recent listings not run.
- DYOR's 5-percent-cost and 0.254-vs-0.256 numbers are double-sourced this sitting (abs-page
  fetch + the estate's own state/arxiv stub), but remain the authors' numbers, not estate
  measurements.

## Banked items (strongest first; receipts in the submitted result)

1. Divergence-Flips 2610.00694 - TV predicts quant decision flips and draft acceptance without
   calibration; the janitor quant lane's missing cheap instrument.
2. DWS 2610.00499 - per-request cost prediction as a two-dimensional surface; the published
   nearest-neighbor to the tank-accounting probe; ledger needs no migration.
3. RouteFM 2609.37362 - frozen router, context-only adaptation, 8 observations per candidate;
   the minimal-funded-probe-set math.
4. FlexRouter 2609.38585 - coverage-maximizing DPP routing with adaptive subset size; the
   fan-out width law's objective function, formalized.
5. OpCaches 2609.33141 - classifier-centric operation caches: minus 56 percent inference cost,
   5x hit latency; the frozen-prefix efficiency law in product form.
6. Cascadia 2609.38697 - control-plane-free commodity-fleet serving with ed25519 admission,
   signed receipts, KV prefix mobility, 3.10x at three nodes.
7. ThunderEP 2609.40093 - consumer-PCIe MoE expert-parallel speedups; MoE-only genre intel for
   the dense janitor fleet.
8. DYOR 2610.01955 - bounded-class frontier parity at 5 percent of cost; the question-class
   boundary law's newest datapoint.
