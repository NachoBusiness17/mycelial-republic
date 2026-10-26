# SPIKING-WIDE RUN RECEIPT (gala_20260925)

Written 2026-10-01 by herald from the run script's authoritative sections (gate output, lane metadata, fold, review, filing). Script numbers only; nothing re-derived. Checks this writer executed fresh during receipt writing are marked [herald check]; everything else is reported as the script/review/filing agents returned it. Gate verdict: **GATE PASS** (script output line; this writer did not re-execute the fold gate).

## Header

- Slug: spiking-wide (gala_20260925)
- Lane count: 8 (expected 8)
- Lanes parsed OK: 7/8 (energy-frontier.json carries status complete but no ok key; the gate banks it rather than dances it, see Scoreboard)
- Divisions: B: 7, A: 1 (synthesis is the division A lane)
- Gate: GATE PASS
- [herald check] `ls watch/inbox/gala_20260925/spiking-wide/lanes/` lists exactly the 8 lane JSONs (energy-frontier, event-driven-resonance, linear-family, neuromorphic-hardware, nonnvidia-stacks, spikingbrain-deep, synthesis, upcycle-economics) plus per-lane .check.txt evidence and _qc/ fetch artifacts.

## Scoreboard

- Ballroom: danced 8 / refired 0 / buried 0
- Byte checks cited: 28; mined rows: 21
- Decisions changed: 8 of 8
- Banked (not danced): energy-frontier.json (ok absent/false, evidence-banked: 4 checks, 0 rows)
- Division B: 7/7 danced, 7/7 changed a decision (gate ballroom 8/0/0; by_division B:7)
- Division A: 1/1 danced (synthesis), decision changed; read all 7 siblings, 5 rows with byte-verified quotes (RUN 3: 5x byte_match=YES), 8/8 lane-JSON parse on its corrected rerun

### Standouts (from the fold scoreboard)

- spikingbrain-deep: 10 findings, 8 byte checks; refuted the drop's "runnable TODAY" verdict (HF BICLab org returns [] HTTP 200, weights ModelScope-only, GLAswa/gla_swa = 0 hits in the llama.cpp conversion registry and upstream transformers with positive controls hitting)
- neuromorphic-hardware: richest mine, 7 rows; spiking silicon closed NO for 2026; published LLM SOTA on any spiking chip is a 370M-param model on Loihi 2
- nonnvidia-stacks: 7 checks, 5 rows; export-control bound ruled non-binding at estate scale; first sovereignty-compute ladder R0/R1/R2 created
- upcycle-economics: 4 rows; convert-don't-train priced at 150B tokens = ~579 consumer-GPU-days; GO 1/GO 2 named; cluster recipes no-go'd
- energy-frontier: the gate's one banked lane (ok absent, 4 checks, 0 rows); measured gemma:2b at 84.65 tok/s; verdict quantization-first
- linear-family and event-driven-resonance mined 0 rows but both changed decisions (5 verified open 7B-14B linear-family models; one named port: homeostatic bands for mag/attention_ranker.py:146)

### Top laws (from the fold)

1. **headline-multipliers-deflate-on-primary-reading** (synthesis.json, row 2, leverage high) - every SpikingBrain headline shrank when the lanes read the paper's own tables: 100x TTFT is 26.5x measured at 1M tokens on 32 H100s and 2.4-3.7x at estate-scale 128k (spikingbrain-deep F3/F4, Table 4/5), and the 97% energy is per-MAC arithmetic (0.034 pJ) contingent on silicon whose LLM SOTA is 370M params - adoption math must come from the paper's measured rows at estate scale, never the tweet; all 8 lanes validated this law with bytes in one dig.
2. **loihi2-llm-sota-370m** (neuromorphic-hardware.json, row 3, leverage high) - the proved negative: the largest LLM-architecture model published on any spiking silicon is a 370M-parameter MatMul-free model on Loihi 2 (ICLR 2025, "preliminary"), three orders of magnitude below frontier; single-handedly closes the buy-silicon question for 2026 and defuses the paper's energy claim at its hardware premise; ships with a standing falsifier (a 10B+ LLM end-to-end on spiking silicon with per-token energy).
3. **upcycle-is-cluster-class-even-at-2-percent** (upcycle-economics.json, row 1, leverage high) - the real sovereignty steal (convert-don't-train on ~2% of the data) still prices at cluster class (150B tokens, ~579 derived consumer-GPU-days); the estate prices every future upcycle ask against this datum and no-gos cluster recipes, converting a hype drop into two named probes (GO 1 on the 4GB box, GO 2 on the 12GB GPU) instead of a research project.

## Decision ledger (fold says parade=false; standard ledger, not PARADE)

All 8 lanes changed a decision (gate: decisions_changed: 8; each lane JSON carries its own decision_changed field):

1. **spikingbrain-deep.json:32** - SPIKINGBRAIN_DROP_20261001 verdict corrected: "runnable on the ladder TODAY" refuted (no NVIDIA GPU, no llama.cpp GLAswa support, weights ModelScope-only with the HF BICLab org empty); WATCH + upcycle-pricing steal survive at the paper's own exchange rate (+150B tokens buys the architecture swap at -8 to -12 knowledge pts and -30 IFEval pts vs Qwen2.5).
2. **neuromorphic-hardware.json:7** - neuromorphic/spiking-silicon spend closed to NO for 2026 (research-grade only; Loihi 2 = free INRC membership, SpiNNcloud = contact sales, Akida $289 but edge-class with no estate organ under an edge-watts constraint), three named revisit triggers.
3. **energy-frontier.json:37** - the SpikingBrain energy-bet question closed: the tweet's 97% is a 45nm per-MAC analytic estimate, not a measurement; estate-scale energy moves via quantization + power capping (1.3-5x measured levers), the architecture bet rides only the measured 26.5x TTFT @1M door.
4. **linear-family.json:19** - local-backbone candidate set changed: Granite 4.0 H-Tiny/H-Micro, Nemotron-Nano-9B-v2, Qwen3.5-4B, RWKV-7 G1 7.2B, Falcon-H1 7B verified open and locally-servable; no migration made in the lane.
5. **upcycle-economics.json:51** - the drop's falsifiable probe closed PRICED: 12GB GPU read as the estate training tier, GO 1 (one-sitting layer probe, 4GB box) and GO 2 (one-weekend depth-prune+QLoRA-heal) named, all cluster-class recipes no-go'd.
6. **event-driven-resonance.json:20** - drop receipt's open question (SPIKINGBRAIN_DROP_20261001.md:54-56) closed: event-driven resonance confirmed as byte-backed system-level structure (sharpest C1), one named port candidate (homeostatic bands for mag/attention_ranker.py, measure-first, falsifier stated); port decision stays with the operator.
7. **nonnvidia-stacks.json:47** - sovereignty question closed: non-NVIDIA path is a ladder (R0 own-box Vulkan $0 / R2 TPU v5e chip-hours / R1 7900 XTX as the only vendor-supported owned train card), export-control bound ruled non-binding at estate scale; binding constraint is VRAM economics, not law; first move = price the upcycle probe as a v5e Flex-start job.
8. **synthesis.json:70** - next-rung spec changed: the ~$300 DDR3 body is a three-in-one falsifiable probe (serving duel + GO 2 heal + linear-family eval cards vs the SWA+4-sinks R0 incumbent), and the backbone candidate set is the five verified linear-family models behind the $0 Vulkan probe - not SpikingBrain-7B alone and nothing on spiking silicon (NO for 2026).

## Refired

None (script: ballroom_count refired 0).

## Buried

None (script: ballroom_count buried 0).

## Review verdict: ACCEPT

Reviewer's verified basis, as returned:

1. **Quotes byte-match.** Byte-substring checks (open(rb), q.encode('utf-8') in raw) on 8 cited quotes (3 asked, 5 extra), all True: synthesis row1 in lanes/ev_search_summaries.md, rows 2-3 in watch/inbox/SPIKINGBRAIN_DROP_20261001.md, row4 in watch/inbox/spiking_wide/energy-frontier.md, nonnvidia row1 in ev_unsloth_amd.md, upcycle row3 verbatim in STRATA_DROP_20261001.md, upcycle row2 in wave_20260916/receipts/B10_MLP_KV_CACHE_PRIORART.md, neuromorphic row0 in its receipt.
2. **Every claimed byte-check is backed on disk.** All 8 lanes' evidence files exist and contain what the JSONs claim: nonnvidia's CHECK 1-7 sit at the cited line ranges (check.txt lines 3-42, 7/7 PASS), spikingbrain's CHECK 1-9 present. synthesis.check.txt honestly labels its two defective harness runs (RUN 1 wrong depth/exit, RUN 2 QUOTE_FAIL=1 quoting bug) before the RUN 3 verdict.
3. **Decision ledger honest.** All 8 decision_changed entries name real anchors the reviewer verified: SPIKINGBRAIN_DROP line 43 "runnable on the ladder TODAY" (spikingbrain-deep's refutation target) and line 54 "Event-driven resonance (concept, not port)" (event-driven's closure), STRATA DDR3 line verbatim, mag/attention_ranker.py:146 carries bands 72/52/32, nonnvidia's no-prior-table CHECK 1, upcycle's GO 1/GO 2 in its receipt. None names nothing. Reviewer reran the fold gate: `bash watch/inbox/gala_20260925/fold_gate.sh watch/inbox/gala_20260925/spiking-wide/lanes 8` -> GATE PASS exit 0 (8 JSONs, B:7/A:1, 28 checks, 21 rows, 8 decisions).
4. **B-division finish lines met.** All 7 receipts exist at watch/inbox/spiking_wide/ with byte sizes exactly matching their own check claims (11246/13775/13343/11482/10335/8123/11588); content probes confirm each finish line (energy 84.65 x3 + verdict, event-driven 4 CONVERGENCE headings + SHARPEST + PORT VERDICT, linear-family 10 register rows vs min-3 gate, nonnvidia R0 + bound rows + 8-row signals.jsonl, upcycle GO1/GO2/NO-GO, spikingbrain run-path verdict, neuromorphic BRIDGE VERDICT "**NO.**" at receipt line 58-60). No lane claims another's work: synthesis attributes every mined row to its sibling source path; nonnvidia explicitly disclaims overlap ("spikingbrain-deep owns the paper deep-dig").
5. **Nits, none rising to REVISE:** (a) energy-frontier.json has status complete but no ok key, so the gate banks it rather than dances it (visible in gate output, substance real); (b) synthesis prose says linear_attention "2 hits" in memory/corpus while its own check file and the reviewer's rerun count 3 files (third is a training_pdfs manifest.jsonl bookkeeping row naming the same two PDFs); (c) neuromorphic-hardware quotes verify only against the lane's own receipt (check.py docstring says so; no raw web captures archived, unlike spikingbrain-deep's sb_* artifacts); (d) the gala-level FOLD_SECTIONS.txt covers w1/w2/w3 only, so the spiking-wide fold verdict on disk is the reviewer's executed run.

## Filing verdict: FILED

As returned by the filing agent:

1. **memory/corpus/LINKS.jsonl 235 -> 243:** 8 GALA rows appended (kind gala, slug spiking-wide, src watch/inbox/gala_20260925/spiking-wide/lanes/<id>.json for spikingbrain-deep, neuromorphic-hardware, energy-frontier, linear-family, upcycle-economics, event-driven-resonance, synthesis, nonnvidia-stacks), titles = each lane's top law where one exists (intel-hala-point-specs; THE 97 PERCENT IS PER-MAC NOT PER-TOKEN per the ask's lane summary; upcycle-is-cluster-class-even-at-2-percent; export-bound-does-not-bind-at-estate-scale; RDNA2+-training-line/RDNA1-inference-line) or its changed decision for the top-null lanes; dedupe by src executed first (grep spiking-wide/lanes over the ledger: 0 prior rows), whole-ledger re-parse 243/243 OK, each appended src exactly once, em/en-dash scan on the appended block 0.
2. **ONE STATE entry appended at memories/session/next-window-handoff.md:480** after the vonnegut-final close, gala-close format: slug spiking-wide, danced count 8 (7 division B + synthesis division A, all finished per lane JSON ok/status flags), decisions changed 8, B-division finish 7/7 + division A ok:true, graves filed 0. The entry notes no fold receipt existed at watch/inbox/gala_20260925/spiking-wide/ and no spiking-wide_RECEIPT.md at watch/inbox/gala_20260925/ "verified absent at filing" - this file is that receipt, written after the filing moment, so the absence note is superseded by this document; the entry's count basis (lane JSON ok/status flags) still matches the script's 8/0/0 ballroom.
3. All 8 lane JSONs were read in full before writing. Not run by the filing agent: pytest/ratchet (no code touched) and the fold gate (not requested; its absence is why the count basis is lane JSON flags).

### [herald check] fresh bytes at receipt-writing time

- `wc -l memory/corpus/LINKS.jsonl` -> 243 (matches the filing claim 235 -> 243).
- `grep -n "spiking-wide" memories/session/next-window-handoff.md` -> the GALA SPIKING-WIDE CLOSE 2026-10-01T19:30:51Z entry sits at line 480 (matches the filing claim :480).
- `grep -ril GALA_GRAVE watch/inbox/gala_20260925/spiking-wide/ watch/inbox/spiking_wide/` -> no matches (exit 1), matching graves filed 0.
- Not run by this writer: the fold gate, pytest, ratchet (the ask names none of these for the receipt writer; gate PASS is carried as script output and reviewer-rerun, both reported above as such).
