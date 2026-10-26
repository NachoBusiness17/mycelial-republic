# STEAL CARD: finetuning-adaptation-arxiv (frontier OLM 2026-10-09) - REV 2 (AMENDED; ROUND-3 RE-VERIFIED)

Round 3: the same critique was re-fed unchanged; no new defects were named and the four
required amendments below were already landed in REV 2. This round re-ran the load-bearing
checks fresh (receipt block at the bottom, "Round 3 re-verification") and confirmed the
banked bytes still carry every cure: amendment markers present (21 rg hits), stale
round-1 claims absent (rg for "seed_percolator.py:5-7", ":8-9 for", and the round-1
"mirror-distilled janitor rows (Gate 2 output)" probe input: zero hits, exit 1). The
card stands as amended; nothing below was rewritten this round except this header and
the receipt block.

Round 2 per the critique (AMEND, DO NOT BANK AS-IS). Repairs landed this revision:
(a) the overlap receipt is rewritten to the scoped truth with the catalog rows listed
and the sweep's zero-hit claim struck; (b) an ASTRA v4 + Rocinante + code-agent-data
organ is added with this card's delta against them; (c) the probe is re-based on an
input that exists and a substrate that exists, with the adapter A/B explicitly gated;
(d) the two mag/seed_percolator.py citations are fixed to the byte-true lines. One
NEW scoping fact the critique did not name is also landed: find 7 (2610.09772) was
already banked 2026-10-08 by the sibling open-local-models lane, and is demoted here.
Every critique claim was re-verified against bytes this session before amending; two
of my round-1 reads were confirmed wrong and are struck below.

## Provenance, rewritten to the scoped truth

- The seven finds came from the ask's confirmed payloads; the sweep payload is
  watch/inbox/frontier_olm_2026-10-09/sweep/finetuning-adaptation-arxiv.md (header read
  this session; its overlap section claims "All other candidate titles: zero hits,
  genuinely new" over catalog plus memory). That claim is CONTRADICTED by bytes for
  catalog and corrected below; memory/ alone it got right.
- memory/ is clean for all 7: rg -l over the seven title phrases ("Harness Evolution
  Hits a Ceiling", "Decoupling Logic from Persona", "Fine-Grained Analysis of the
  LoRA", "Second Descent Extends", "Really Different", "LoRA-RIP", "NADI 2026") over
  memory/ returned zero files (exit 1), run this session.
- catalog/catalog.jsonl already held 5 of the 7 as auto-harvested abstracts BEFORE the
  sweep (rows re-read this session): 2610.11655 = row 1342837
  (state/arxiv/2026-10-09/2610.11655v1.txt, mtime 2026-10-09T06:30:55Z); 2609.40236 =
  row 806575 (state/arxiv/2026-10-01/); 2610.06542 = row 1071234
  (state/arxiv/2026-10-06/) PLUS row 1195665, a 1,089,547-byte deep HTML
  (frontier_olm_2026-10-06/sweep/raw/deep_2610.06542.html) a prior sweep fetched;
  2610.09934 = row 1265680 (state/arxiv/2026-10-08/) plus row 445354, the shared-task
  proposal paper 2609.27086 (adjacent harvest, not the Itgan paper); 2610.09772 =
  row 1265656 (state/arxiv/2026-10-08/). NOT in catalog at all: 2610.04507 and
  2610.09122 (rg by arXiv ID and by the distinctive phrases "Second Descent" and
  "Really Different": zero, run this session).
- Why the sweep's receipt failed is NOT determinable from the persisted payload: the
  payload records its instrument ("ripgrep 14.1.1, patterns = distinctive title
  phrases of all candidates, over catalog/catalog.jsonl and memory/") but not the
  per-pattern output, and 2610.11655's harvest predates the sweep window, so a
  snapshot-timing explanation does not cover it. The receipt is struck as false as
  stated; the true scoping is "abstracts auto-harvested for 5 of 7, unread by any
  estate lane" (next bullet), not "zero hits, new to the estate".
- Lane-level scoping, new this revision: rg -l for all seven arXiv IDs over the 10-06,
  10-07 and 10-08 frontier_olm trees hit exactly one banking: 2610.09772 is ALREADY
  BANKED in watch/inbox/frontier_olm_2026-10-08/steal/open-local-models.md:44-52 (read
  in full this session: 480 runs, INT4, 40/40 byte-identical decoupled outputs,
  242 -> 1,203 token growth, 0.669 -> 0.150 collapse, 8B-scoped cure, a NEGATIVE
  placement law at the 2B rung, and its own 20-row pollution-ladder probe). Find 7 is
  therefore demoted: no new steal is claimed on it; this card's round-1 context-pack
  read of the same numbers rides the sibling's bank. 2610.06542's raw bytes were
  fetched 10-06 (watch/inbox/frontier_olm_2026-10-06/RECEIPT.md:432, a byte-count
  line) but no card banked the paper (rg over that day's steal/*.md: zero ID hits),
  so 06542 stays bankable here.
- Flagship provenance upgraded beyond the ask: both flagship abstracts were read on
  disk this session from the estate's own harvests (state/arxiv/2026-10-09/
  2610.11655v1.txt:6 and state/arxiv/2026-10-01/2609.40236v1.txt:6), so Gates 1-3
  below cite local bytes, and the critique's two WebFetch verifications stand as the
  external check. Finds 2, 4, 5, 6 stand on the sweep payload's verbatim claims; not
  re-fetched this session.

## The steal, as one mechanism: DISTILL-DIAGNOSE-BANK

Three gates deciding what graduates from the harness/skill ledger into weights.

- Gate 1 DIAGNOSE (arXiv 2610.11655, local bytes :6): read failure composition first;
  process failures (blocked calls, loops, exhausted step budgets) belong to harness
  evolution, content failures (a delivered plan that is poor) are what weight training
  is for. The estate's harness/skill ledger is exactly the first lever: a self-evolving
  harness lifted Qwen3.5-4B 0.16 -> 0.30 and 9B 0.32 -> 0.44, and 4B held-out delivery
  rose 55% -> 90% "while content failures are left for the weights". Weights are the
  SECOND move: adapters trained on evolved-harness trajectories add +0.13 under the
  original harness, on 9B the adapter alone matches the full evolution line (content
  failures a quarter of trajectories -> one in twenty). Boundary condition banked with
  it: on WebArena-Lite (+0.09) "the gain lives in what the model sees and adapters do
  not add to it", so seeing-gains are not adapter food.
- Gate 2 DISTILL REAL, NEVER SYNTHETIC (arXiv 2609.40236, local bytes :6): in the 2x2
  design (classification head vs instruction fine-tuning, distilled-real vs synthetic
  data) "The decisive factor was the training-data source, not the fine-tuning
  method": the distilled instruction-tuned Gemma-3-12B matched GPT-4o (macro-F1 0.845
  vs 0.850, p = 1.000, +0.178 over base) while "both synthetic-data models failed to
  exceed the un-tuned open-weight base at any training size". Envelope: "Fine-tuning
  and inference fit within the memory envelope of a single 24 GB consumer GPU" (NVIDIA
  class; see the substrate gate below for this box).
- Gate 3 BANK WITH A PLACEBO FALSIFIER (arXiv 2610.11655, local bytes :6): "A placebo
  adapter trained on answer-shuffled trajectories falls below the base model"; an
  adapter promotes only if it beats base while its shuffled twin does not. The estate
  already runs the null-arm shape on prompts: "guard = null-variant canary: baseline
  copy must NOT exceed 50% wins, else judge is biased -> loop HALTS (auto), flag
  raised" (mag/seed_percolator.py:10-11, byte-corrected per the critique, read this
  session). The port adds an adapter arm to an existing instrument.

## Recipe constants (finds 2, 4, 5, 6; quotes from the ask payloads)

- Flavor: plain LoRA is the retention pick, DoRA the score pick, PiSSA costs retention;
  explicit spectral preservation proved unnecessary (arXiv 2610.09122). Fleet default:
  plain LoRA; DoRA only against a named score target.
- Rank: small, treated as regularization; rank-1 LoRA beat dense fine-tuning on 3 of 4
  backbones, but matching dense risk costs the parameter savings (arXiv 2610.04507).
- Rank is data-coupled: "the appropriate adapter rank should depend on the quality of
  the data-induced optimization geometry, rather than on the model alone" (arXiv
  2610.06542); screen corpus rows for conditioning before any run; bad bytes poison the
  rank budget.
- Field recipe: pooled adapter first, per-domain specialists continued from it;
  base-model choice beat adapter capacity; the final 0.60 WER "came free from
  weight-space averaging of independent runs" (arXiv 2610.09934). Soup of independent
  runs is a free pre-promotion gain.

## Estate map, organ by organ

- PERCOLATOR (memory/percolator/; docs/BOOT_DOC.md:85; falls-as-curriculum at
  docs/GAIT_PLAN.md:18 and :69): Gate 1 lands as a fall-classification extension; Gate
  3 lands on the existing promotion grammar ("fitness = paired blind win-rate vs
  frozen baseline", "threshold = >=55% win-rate, min 30 judged pairs PER EPOCH",
  "promotion = >=55% in 3 CONSECUTIVE epochs on fresh task sets (total >=90 pairs)",
  mag/seed_percolator.py:7-9, byte-corrected) with the placebo adapter as the null arm
  (:10-11).
- ASTRA v4 + Rocinante + code-agent-data (NEW organ row per critique (b)): the estate
  already holds a CONVERGED adapter-training spec in this exact territory:
  "The spec for turning fleet receipts into a local gemma-class adapter that emits
  gate-passing design directions" (memory/continuity/seat_memory_20260927/
  astra-v4-converged-training-brief.md:13) with the fixed spine at :16: harness_audit
  -> curator (sealed-first, diagnose->repair->GraphFilter select) -> validate -> QLoRA
  SFT -> RS-DPO+HyPO -> GRPO -> budget-matched eval vs champion -> canary promotion
  with rollback (arrows rendered ASCII from the yaml source). This card's DELTA against
  ASTRA v4, three rows: (1) Gate 1 supplies the evidence-backed WHEN-TO-TRAIN trigger
  (failure composition, weights-second) that the audit-driven harness_audit stage does
  not name; (2) Gate 3's answer-shuffled placebo is an adapter-arm falsifier; the
  visible spine names "canary promotion with rollback" but no null-data training arm
  (stated at the brief's visible level of detail only); (3) the recipe constants are
  absent from the visible spine and land as its SFT-stage defaults. Row source already
  named by the estate: "room.jsonl rows, seat session tapes, and intake cards ARE the
  training corpus for the fleet's successors ... when the QLoRA campaign's Stage 2/3
  asks for food" (docs/SKILLS_CATALOG.md:10, read this session), and the box-burn law
  names "the training spine (QLoRA/Rocinante)" as the GPU sink
  (memory/continuity/seat_memory_20260927/box-burn-90-percent-law.md:17).
- SOVEREIGN MIRROR (mag/grok_mirror.py, configs/mirrors.json): CORRECTION of round 1
  per the critique, verified this session: the mirror does NOT emit janitor task rows.
  It writes one report JSON per run keyed by vision slug (mag/grok_mirror.py:52-53
  SCHEMA/OUT_DIR, :305-308), and memory/runs/grok_mirror/ holds exactly 4 reports
  (listed this session), research-plan class, oldest-class content per the critique's
  open of the 2026-08-09 report. So Gate 2's law binds the ASTRA/code-agent-data
  corpus (real seat tapes = real specialist outputs), and a mirror row-logger is
  BUILD-FIRST if mirror sessions are ever to feed adapters. DISTILL-EPOCH2 ("1.7B/8B
  students learn the 320B brain's verdicts at >=55% paired win-rate (seed_percolator
  rails)", docs/experiments/EXP_BRAIN_00_MASTER.md:17) inherits the real-not-synthetic
  data law as its upgrade.
- GOPHER FLEET (AGENTS.md janitors gemma:2b scut, gemma4 short worker): the recipe
  constants become fleet adapter defaults. On 2610.09772 this card claims nothing new:
  the sibling 10-08 placement law (2B rung barred from decoupled-logic cures without an
  on-box pollution ladder; 8B-scoped first) is the operative bank.
- CONTEXT PACK (mag/context_pack.py): the 180/167-vs-242 -> 1,203 token-growth numbers
  are now cited to the sibling card's read (open-local-models.md:46-47) as adjacency;
  the pack's minimal-logic-prompt discipline is the same pollution-invariant shape.
- QUANTIZER: state-side, not weight-side (mag/state_quantizer.py:1-4 "compress Verkle
  lattice into dense summary representations"; mag/auto_quantize.py:6 RenderMan
  adaptive sampling); no port claimed.
- WATER GRAPH: water_computer graph mode (memory/continuity/seat_memory_20260927/
  go-wide-pass-20260927.md:35); no steal mapped. OWED: a precise owner read before the
  2610.06542 conditioning screen is wired there.

## Falsifiable probe, re-based on inputs and substrate that exist

- PROBE FOR THIS WEEK (CPU-only, zero new deps, one seat-hour): FALL-COMPOSITION
  CENSUS. Inputs exist today, sizes measured this session: memory/percolator/
  explore.jsonl (1,976 rows) + candidates.jsonl (31 rows) + lane trails
  (queue/lanes/day_work/trail.jsonl 2,725 lines; builder 1,924). Hand-classify a
  100-row sample by 2610.11655's binary: process failure (blocked call, loop, exhausted
  budget) vs content failure (delivered but poor). FALSIFIED IF: content-class falls
  are rare in the sample (<~10%), because then the estate's trainable residue is thin,
  Gate 1 says keep compounding the ledger, and the weights port has no food (the
  paper's own WebArena boundary). If content-class is fat, the census banks the
  row-class tag schema for ASTRA's curator stage and hands the adapter A/B its row
  source. This tests the card's central claim with zero GPU.
- STAGE-2 (named, NOT scheduled; all three critique gates attached): the round-1
  placebo-adapter A/B is retained only as gated follow-up. Input gate: corpus-grade
  seat tapes per docs/SKILLS_CATALOG.md:10, never the 4 mirror reports. Substrate
  gate: the training spine does not exist on this box (rg -i
  "torch|peft|transformers|bitsandbytes|unsloth" over requirements.txt: zero hits,
  exit 1; GPU is an AMD Radeon RX 5600 XT per Get-CimInstance Win32_VideoController,
  run this session; box-burn law :17: gfx1010, ROCm will never support it, GPU access
  is llama.cpp Vulkan inference-only). Any A/B therefore runs spine-build-first, night
  window only (box-burn law :15: heavy local runs NIGHT only, hard stop 07:00,
  amd_window_guard ENFORCED), with a CPU-feasibility check before any GPU claim. The
  paper's "24 GB consumer GPU" is NVIDIA-class and is not this box.

## Session receipt (round 2, what was actually run)

- rg catalog: seven-title-phrase counts, arXiv-ID greps, row reads at 1342837, 806575,
  1071234, 1195665, 1265680, 1265656, 445354 (head -c 400 on the last).
- rg memory/ over the seven phrases: zero files (exit 1).
- Read tool: mag/seed_percolator.py:1-16 (citation fix verified), mag/grok_mirror.py
  :48-57 and :300-311, state/arxiv/2026-10-09/2610.11655v1.txt (full),
  state/arxiv/2026-10-01/2609.40236v1.txt (full).
- sed reads: astra-v4-converged-training-brief.md:1-20 (lines 13 and 16 confirmed),
  docs/SKILLS_CATALOG.md:8-14 (code-agent-data at :10), box-burn-90-percent-law.md
  :14-18 (:15 night window, :17 Vulkan + QLoRA/Rocinante confirmed).
- ls memory/runs/grok_mirror/ (4 JSONs); rg -l for the 7 IDs over the 10-06/07/08
  frontier_olm trees (one banking found: open-local-models, find 2 section read);
  wc -l on the probe inputs; rg requirements.txt (exit 1); Get-CimInstance GPU.
- Not run this session: pytest, any arXiv fetch (flagship bytes are the estate's own
  harvests; the critique's WebFetch checks stand), any training or evaluation, and the
  probe itself (this card names it, it does not claim it). The round-1 returned StealCard
  JSON lives in the workflow result channel, not on disk; this file and the JSON below
  are the round-2 deliverables.

## Round 3 re-verification (fresh runs, this ask)

The critique text returned with round 3 is byte-identical to round 2's, and its line
references (card lines 3-6, 99-103, 33-35/65,103) match the round-1 file, not the
banked REV 2; the amendments were verified landed, then the load-bearing checks were
re-run so this ask's receipt is its own:

- Banked bytes: rg -c over the amendment markers (REV 2, ASTRA, FALL-COMPOSITION,
  catalog rows 1265656/1265680/1342837, ":10-11", ":7-9", SKILLS_CATALOG.md:10,
  box-burn) = 21 hits; rg for the three stale round-1 claims = zero (exit 1).
- Catalog scoping re-run: rg -o over the five harvested IDs returned 2610.11655 x1,
  2609.40236 x1, 2610.06542 x3 (harvest + deep HTML + third row), 2610.09934 x1,
  2610.09772 x1, and NO rows for 2610.04507 or 2610.09122. 5 of 7 harvested, 2 absent,
  as REV 2 states.
- memory/ clean re-run: rg -l over the seven title phrases = zero files (exit 1).
- Substrate re-run: rg -i "torch|peft|transformers|bitsandbytes|unsloth" over
  requirements.txt = zero (exit 1); Get-CimInstance Win32_VideoController = AMD Radeon
  RX 5600 XT; ls memory/runs/grok_mirror/ | wc -l = 4.
- Critique's own line cites verified by my read this round: judge() at
  mag/seed_percolator.py:64 and paired_run() at :78 (Read :60-81); ASTRA brief :13 and
  :16 re-read via sed, verbatim.
- Not run this round: pytest, arXiv fetches, training, the probe.
