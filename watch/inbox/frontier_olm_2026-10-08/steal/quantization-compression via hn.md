# STEAL CARD: quantization-compression via hn (frontier_olm 2026-10-08, round 1)

Seat: steal-quantization-compression via hn gopher. Source find: arXiv 2610.04403,
"Saying, Not Knowing: Aggressively GGUF-Quantized Small Language Models Still Write Rare
Words They Can No Longer Define" (https://arxiv.org/abs/2610.04403), found by the round's
HN sweep via the newly proven arXiv submittedDate-range door (sweep:18-22). Banked quote
(find + sweep:225): "Validation must be per artifact."

## Overlap, stated first (delta discipline)

- Day-6 fold already holds the paper at sweep level: quote and mechanism refetched live
  there, one estate extrapolation STRUCK (the paper never evaluated Gemma 1 / the
  gemma:2b tag; its robust Regime III datum is Gemma-2-2B, 2.6B params, -2.3/-9.4 at Q2;
  the "gemma:2b sits inside the dissociation regime" component was ruled confirmed=false),
  sweep-level disposition kept (watch/inbox/frontier_olm_2026-10-06/DIGEST.md:92).
- This round's sweep seat already banked the full-abstract regime numbers as its item 3
  and carried them into RQ3/RQ5 (watch/inbox/frontier_olm_2026-10-08/sweep/
  quantization-compression-hn.md:223-230, :130-151, :180-189), ending "Stays sweep-level."
- This card does NOT re-bank those numbers as new. Its delta is threefold, all verified
  against bytes this sitting: (1) estate-state update - the four-lane-re-owed qwen2.5:7b
  A/B RAN mid-round and discharged (receipt sweep/quant_ab/RECEIPT.md, "RUN COMPLETE
  2026-10-08", seat sweep-quantization-compression-x; the round's own lens recorded it
  un-run at watch/inbox/frontier_olm_2026-10-08/lens/burns.md:205-208 before the run
  landed); (2) the on-box sub-2B census below; (3) the port moves + probe that convert
  the sweep-level find into estate mechanisms. Honesty: this seat did NOT fetch arXiv;
  the paper's numbers are carried from two independent in-repo live fetches (day-6
  DIGEST.md:92 refetch; this round's sweep full fetch), not re-verified here.

## The mechanisms (what the paper adds beyond the four-pinned-choices rule)

All numbers below are the paper's abstract-level regime facts as banked at day-6
DIGEST.md:92 and sweep:130-151/:223-230 (carried, not re-fetched):

1. PER-ARTIFACT REGIMES, SIZE-DRIVEN. At Q2 the damage splits three ways: total collapse
   into unusable builds, "severe semantic dissociation in sub-2B models" (definitions
   fall 20-67% below each artifact's OWN baseline; roster: Granite-4.0-H-350M -47.3%,
   Qwen2.5-0.5B -20.3%, LFM2-700M -41.8%, Granite-4.0-H-1B -43.6%, LFM2-1.2B -29.8%,
   LFM2.5-1.2B -49.0%, Llama-3.2-1B -61.1%, Qwen2.5-1.5B -66.6%), and mostly robust
   preservation above ~3B. Damage correlates with parameter count (rho=0.72), not
   tokenizer size (rho=0.12). "Q4_K_M remains lexically clean at >=1B."
2. PERPLEXITY CANNOT SET PINS. Across nine artifact-matched ladders, near-identical Q2
   WikiText-2 PPL penalties (+47.6% and +44.7%) separate an artifact keeping its
   definitions (3.6% loss) from one losing them (43.6%). Any PPL/KLD-ranked ladder
   selecting per-role pins is measuring the wrong channel; diagnostics only.
3. BUILD PROVENANCE IS TASK-VISIBLE. Same model, same quant, different GGUF build
   (section 4.9, day-6 DIGEST.md:92): Ollama's Llama-3.2-1B at Q2 loses -34.3%/-61.1%
   inclusion/definitions vs the independent Unsloth build's -11.1%/-43.6%. The digest pin
   has a task-level consequence, not just repo hygiene.
4. THE INSTRUMENT ITSELF: rare-word surface inclusion vs one-sentence definition, tiered
   multi-synonym matcher, blind-judge census - a cheap channel that detects damage a
   100%-pass task mix cannot see. This is exactly the property the estate's fresh A/B
   receipt names as its own blind spot: "CEILING-BOUND INSTRUMENT: 100% on both arms
   means the task set sits above both quants' competence floor and cannot discriminate
   near it" (sweep/quant_ab/RECEIPT.md limitation 1).

## Estate state this sitting (commands run here)

- `curl -s http://localhost:11434/api/tags` (this sitting): 15 models returned. Arm B of
  the A/B is NOW ON BOX: qwen2.5:7b-instruct-q8_0, Q8_0, 7.6B, 8,098,538,978 bytes,
  manifest digest 2d9500c948416525... (pulled 2026-10-08T13:35 local), arm A qwen2.5:7b
  Q4_K_M digest 845dbda0ea48... - both match RECEIPT.md's recomputed blob hashes.
- Sub-2B census from the same call: deepseek-r1:1.5b is the ONLY sub-2B generative
  artifact (parameter_size "1.8B", Q4_K_M, digest e0979632db5a88d1..., 1,117,322,768
  bytes). Janitor tier: gemma:2b (parameter_size "3B", Q4_0, digest b50d6c999e59...)
  holds the clerk/router/orchestrator/voice pins (configs/lanes.yaml:31-33, :36);
  gemma2:2b-instruct-q5_K_M is the 2.6B artifact. Correction to sweep:136-137's
  "2.6B params per the box tag list" lumping: that number belongs to gemma2:2b-instruct;
  the API reads gemma:2b as "3B" (coarse field; Gemma-1-2B is ~2.51B true params; exact
  count OWED to a gguf_cartography blob read, mag/gguf_cartography.py:1-8).
- Service-path exposure: `grep -rn "deepseek-r1" configs/ mag/` hits only
  mag/ollama_policy.py:186 (a docstring example of the capability thinking shape, not a
  pin) and configs/providers.yaml:209 (a comment about the REMOTE deepseek API being
  gone). No lanes.yaml or code path pins the 1.5B model. The estate's sub-2B exposure is
  preventive-only today.
- Registry check (this sitting): `curl -s -o /dev/null -w "%{http_code}"
  https://registry.ollama.ai/v2/library/qwen2.5/manifests/{0.5b-instruct-q8_0,
  0.5b-instruct-q2_K,0.5b-instruct-q4_K_M}` all returned HTTP 200 - the probe arms exist.

## Estate map: what each mechanism feeds, and the port move

QUANTIZER organ (weights side; mag/auto_quantize.py:1-24 is the DATA-side quantizer, its
"LAW: Anomalies are NEVER quantized" philosophy at :20-22, so the weights gate lives in
the paper trail) and through it the GOPHER FLEET local tier (configs/lanes.yaml:31-37).

1. A/B instrument, post-run: the owed debt is DISCHARGED (RECEIPT.md: tie at ceiling,
   50/50 both arms, byte-identical responses, per-task spread 0.0 pp, strict-parse 98% =
   98% so falsifier 2 fired and the parse channel demoted to rider, multi-prompt
   falsifier 1 fired as a task-mix-scoped stability datum, Q4_K_M 2.30x decode speed).
   The paper's estate-relevant prior ("Q4_K_M lexically clean at >=1B") is CONSISTENT
   with that tie. PORT MOVE: the paper's definitional channel becomes the discriminator
   the ceiling-bound receipt says is missing - add it as the lexical leg on any
   floor-near quant claim (sweep:117 already reserved "the lexical rider below if
   cheap"; this card makes it concrete), reusing run_ab.py's paired-seed temperature-0
   pattern (sweep/quant_ab/run_ab.py, proven this round) and the receipt's 7-element pin
   contract (RECEIPT.md, "Minimal pin contract").
2. Regime tripwire on the pin gate: extend the promotion gate (QUANT_AB_SPEC_AMEND.md,
   watch/inbox/port_wave_20261007, "Promotion gate" section, :92-100) with one clause:
   no lanes.yaml pin below 2B parameters at Q3-or-lower without a per-artifact
   definitional-grade receipt, and no PPL/KLD channel ever sets a pin (paper's
   non-calibration law, mechanism 2; matches the VeriLoop structure already banked,
   sweep:98-104). Today's pins are safe under it (gemma:2b Q4_0, worker Q4_K_M 7.6B);
   the tripwire guards the 6GB-envelope emergency path (configs/lanes.yaml:28) where
   someone reaches for a 0.5B-1.5B rung under VRAM pressure.
3. Digest/build pinning: the paper's build-variance datum (mechanism 3) is the
   task-level argument for extending MAG_PIN_DIGESTS coverage (mag/ollama_policy.py:26,
   :54-55, which logs unpinned tags at :126) to the whole janitor tier - today the pins
   ride floating library tags. Concretely: pin tag=digest for gemma:2b, qwen2.5-coder:7b,
   qwen-desk, deepseek-r1:1.5b before any further quant work rides them.

## Falsifiable probe (cheap, this week; specced, NOT run)

THE probe: same-artifact two-rung definitional A/B at sub-2B - the paper's central
Regime II claim tested on estate instruments. Pull qwen2.5:0.5b-instruct-q8_0 and
qwen2.5:0.5b-instruct-q2_K (registry-verified HTTP 200 this sitting; ~0.5 GB + ~0.4 GB).
Run 20 rare low-frequency words through the stolen channel: surface-inclusion check,
then one-sentence definition, tiered multi-synonym matcher, blind-judge census judged by
an on-box NON-arm model (qwen2.5:32b, on box per the tag call), temperature 0, paired
seeds, per run_ab.py's pattern. PREDICTION (paper roster, Qwen2.5-0.5B at Q2: -20.3%
definitional): the q2_K arm loses >=15 percentage points of definitional hit-rate vs its
q8_0 twin on the same word list. FALSIFIER: delta <5 pp - the cliff is absent on this
artifact/rung on-box, a first counter-datum that demotes the regime tripwire from law to
"Q4_K_M-and-above guidance" and, either way, decides whether the estate's 6GB envelope
has a safe sub-2B emergency rung (the only decision the tripwire actually gates). Cost:
under 1 GB of pulls, ~15 minutes, $0, hardware on box.

Secondary (minutes, $0): run mag/gguf_cartography.py (pure-stdlib GGUF parser, :1-8) over
the on-box deepseek-r1:1.5b and gemma:2b blobs to settle exact parameter counts (the
regime boundary is param-count-sensitive at rho=0.72; the API's "1.8B"/"3B" fields are
coarse; dtype 2+ stats are PROXY-labeled per the tool's honesty law, tensor census still
yields param arithmetic). Falsifier for the card's census claim: if the blob reads the
1.5B distill above 2.0B true params, the "only sub-2B generative artifact on box" line
is struck.

## OWED / not verified

- Paper numbers carried from day-6 DIGEST.md:92 and this round's sweep (:130-151,
  :180-189, :223-230); this seat fetched neither arXiv nor any HN page.
- Probe not run: no pulls made, no definitional run executed. Registry tag existence
  (HTTP 200 x 3) is the only network check this seat ran.
- Exact param counts for gemma:2b and deepseek-r1:1.5b (API fields coarse) - owed to
  gguf_cartography; nothing downstream asserts the coarse numbers as truth.
- The A/B receipt's difficulty-hardened follow-up set and the deepseek-r1:1.5b
  thinking-channel sibling probe (spec leg 7, QUANT_AB_SPEC_AMEND.md, the leg citing
  watch/inbox/frontier_olm_2026-10-07/steal/finetuning-adaptation.md) remain un-run and
  are NOT this card's ask - the definitional channel claimed here is a different,
  unclaimed lane on the same artifact class.

## Receipts (commands this seat ran this sitting)

- `curl -s http://localhost:11434/api/tags` (full JSON read: 15 models; arm B digest
  2d9500c948... present; deepseek-r1:1.5b 1.8B/Q4_K_M; gemma:2b 3B/Q4_0; gemma2:2b 2.6B/
  Q5_K_M).
- `curl -s -o /dev/null -w "%{http_code}"` x 3 against registry.ollama.ai qwen2.5
  manifests 0.5b-instruct-{q8_0,q2_K,q4_K_M} - all 200.
- `grep -rn "deepseek-r1" configs/ mag/` (2 hits + 1 pycache; no service-path pin).
- Reads: sweep/quant_ab/SUMMARY.json + RECEIPT.md in full; QUANT_AB_SPEC_AMEND.md
  :40-115; sweep/quantization-compression-hn.md in full; frontier_olm_2026-10-06/
  DIGEST.md grep+read of the 2610.04403 entry (:92); configs/lanes.yaml :25-40 with
  grep -n line numbers (:28,:31-33,:36,:37); mag/ollama_policy.py :180-192 + MAG_PIN_
  DIGESTS grep (:26,:54-55,:126); mag/auto_quantize.py :1-24; mag/gguf_cartography.py
  :1-10; watch/inbox/frontier_olm_2026-10-08/lens/burns.md :200-215; lens/doors.md
  :35-45; frontier_olm_2026-10-07/steal/quantization-compression.{json,md} (format +
  lineage convention).
- JSON card banked beside this md in the 10-03/10-07 field shape
  (area/steal/source_url/estate_map/probe/chars).
