# QUANT A/B SPEC AMEND: qwen2.5:7b Q4_K_M vs q8_0 (port wave 2026-10-07, lane P6 port 1)

Status: SPEC AMEND ONLY. The owed A/B stays UN-RUN; this file amends its instrument
before firing so the run cannot manufacture a verdict by design. Nothing here executes
the probe; the burns ledger owns firing.

## The debt being amended

- Owed probe: fold probe 5, "local qwen2.5:7b Q4_K_M vs q8_0 A/B"
  (watch/inbox/frontier_olm_2026-10-03/lens/burns.md:118-123, probe 5 named at :122).
  Re-owed unrun in the 10-03 DIGEST honest gap 1
  ("still unrun after four lanes re-owed it this pass",
  watch/inbox/frontier_olm_2026-10-03/DIGEST.md:224) and
  again in the round-2 probe-status ledger ("probe 5 ... re-owed unrun",
  watch/inbox/frontier_olm_2026-10-03/DIGEST.md:274).
- Pointer drift note: the day-7 steal card cites the debt at burns lines 97 and 218
  (watch/inbox/frontier_olm_2026-10-07/steal/quantization-compression.md, steal 1).
  On this tree :97 is the agent-limit-retry confirmed-find row and :216-218 is the
  counts-law bullet; the verified debt pins are the probe list at
  watch/inbox/frontier_olm_2026-10-03/lens/burns.md:118-123 (probe 5 at :122).
  Instrument spec: watch/inbox/frontier_olm_2026-10-03/DIGEST.md:224.

## Why amend, not fire: the four-pinned-choices rule

Source: watch/inbox/frontier_olm_2026-10-07/steal/quantization-compression.md, steal 1
(arXiv 2610.07781, NeurIPS 2026 SLM-Agents workshop). "The
8-bit-4-bit recovery comparison changes direction across prompts and evaluation
targets" is byte-present at state/arxiv/2026-10-07/2610.07781v1.txt:6. The
paper's own conclusion, carried by the card: "one prompt, one screened
task set, and one scoring policy do not establish a stable conclusion about
quantized-agent robustness."

The four choices, each able to flip the verdict alone. Full-text numbers are carried
from the sweep seat's end-to-end HTML read
(watch/inbox/frontier_olm_2026-10-07/sweep/quantization-compression-arxiv.md:26-37,
honesty note at :85); they are not re-fetched by this seat.

1. PROMPT: matched-task deltas across 5 prompts ran +8.3 / -3.3 / -10.0 / -50.0 /
   +35.0 points at the estate's exact pair (Qwen2.5-7B-Instruct served via llama.cpp
   at GGUF Q8_0 vs Q4_K_M, naming per the card), and the only two CIs excluding zero
   favor OPPOSITE precisions.
2. TASK SCREENING (Llama, one prompt): scoring each variant only on its own
   clean-passing tasks favored 4-bit by 17.5 points; scoring the same tasks for both
   variants gave no difference; scoring the full pipeline favored 8-bit by 28.3 points.
3. PARSING POLICY (Llama, one prompt): strict output parsing flipped that +28.3 to
   -15.0, while the paper's own Qwen datum is FLAT ("essentially unchanged").
4. UNCERTAINTY UNIT: tasks, not injected fault sites (paper closing sentence).

## Amended instrument

Arms (unchanged from the 10-03 spec):

- Arm A: on-box qwen2.5:7b Q4_K_M, digest 845dbda0ea48
  (watch/inbox/frontier_olm_2026-10-03/steal/quantization-and-compression.md:11).
- Arm B: qwen2.5:7b-instruct-q8_0, library-verified 8.1 GB pull
  (watch/inbox/frontier_olm_2026-10-03/percolator_candidates.jsonl:3).
- Shape: 10 deterministic tool-failure-recovery tasks via /api/generate, temperature 0,
  identical caps, paired seeds.
- KEPT from watch/inbox/frontier_olm_2026-10-03/DIGEST.md:224: pin-or-reset
  serving-cache state between arms, token counts
  compared only on EOS-terminated responses or equal caps.

Amended legs, each traced to the choice it pins:

1. FIVE-PROMPT RULE (pins choice 1): at least 5 prompt phrasings per task, 50 runs per
   arm minimum. A single-prompt score is a screening artifact, never a result.
2. DEPLOYMENT VERDICT (pins choice 2): full-pipeline success pooled over ALL tasks and
   prompts. This is the only number that promotes or kills a quant. Nothing scored on
   a pre-screened clean-intersection task set enters the verdict.
3. MATCHED-TASK DELTAS ARE DIAGNOSTIC (pins choices 1 and 2): per-prompt
   clean-intersection deltas are reported with their sign flips across prompts, never
   as the headline.
4. STRICT-PARSE CHANNEL WITH PRIOR (pins choice 3): strict-parse success is banked as
   its own channel, never merged into the verdict. THE QWEN-FLAT PRIOR IS STATED UP
   FRONT: the paper's parse-channel verdict flip is Llama-side (+28.3 to -15.0); at
   Qwen the paper read "essentially unchanged", so the expected case is a flat
   channel, and a firing there is a surprise to be explained, not a designed finding.
5. PER-TASK SPREAD REPORTED (pins choice 4): the pooled verdict carries per-task
   spread; the paper's own +8.3 to +35.0 range datum makes a point estimate without
   spread meaningless.
6. EXPORT-CAST RIDER: hash the exact GGUF artifact (sha256 of the blob) and pin the
   conversion toolchain in the result receipt, or the ladder measures the exporter
   instead of the quant (day-7 card steal 1, port move rider, from arXiv 2610.07853
   via the sweep receipt).
7. THINKING CHANNEL stays a logged rider, never the verdict
   (watch/inbox/frontier_olm_2026-10-03/steal/quantization-and-compression.md:31
   extended the A/B with the thinking-token
   channel; the 10-07 finetuning card
   watch/inbox/frontier_olm_2026-10-07/steal/finetuning-adaptation.md fires the
   sibling deepseek-r1:1.5b probe for that channel).

## Promotion gate (new, binding)

No single-prompt quant score promotes into configs/lanes.yaml model pins (janitor
pins :31-33, worker pin :37). Promotion requires the amended instrument's
full-pipeline verdict over all tasks times at least 5 prompts, with per-task spread
reported, on hashed artifacts. This extends the 10-03 Q4_K_M floor gate
(watch/inbox/frontier_olm_2026-10-03/percolator_candidates.jsonl:3) to any future
quant drop into the lanes.yaml pins. Scope note carried from the day-7 card round-2
fix: the probe substrate qwen2.5:7b-instruct is not pinned in lanes.yaml at all today.

## Cost and falsifiers

- Cost: $0 plus one 8.1 GB pull, one afternoon, 50 runs per arm, hardware already on
  box (RX 5600 XT 6GB envelope, configs/lanes.yaml:28).
- Falsifier 1: all 5 prompts agree in sign with per-task spread under 20 points. That
  kills the multi-prompt rule as dead weight at janitor scale on this task mix and
  banks the first stability datum at odds with the paper.
- Falsifier 2: strict-parse rates equal across arms (the paper-expected Qwen outcome),
  demoting the pinned parsing channel to a logged rider.
- Either way the four-lane-re-owed debt discharges with an instrument that cannot
  manufacture a verdict by design.
