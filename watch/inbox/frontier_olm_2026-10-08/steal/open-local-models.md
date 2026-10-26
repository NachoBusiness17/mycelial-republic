# STEAL CARD: open-local-models (frontier OLM 2026-10-08) - REV 1

Round 1 draft, no prior critique. Eight confirmed finds, all banked by this sitting's own
sweep (watch/inbox/frontier_olm_2026-10-08/sweep/open-local-models-arxiv.md; overlap
census at :210-229 shows zero memory/ + watch/inbox/ hits outside the sweep dir, all
catalog hits are state/arxiv mirror snapshots). Per the BreadthKV precedent ("this card
banks the PORT, not the find", watch/inbox/frontier_olm_2026-10-06/steal/quantization-
compression via x.md:8), this card banks estate ports and probes.

Two ground facts moved UNDER the finds while this card was drafted, both re-verified
against current bytes this sitting, and both honored below:

- (a) The P6 four-pinned-choices quant A/B instrument ALREADY FIRED today:
  watch/inbox/frontier_olm_2026-10-08/sweep/quant_ab/RECEIPT.md records the qwen2.5:7b
  Q4_K_M vs q8_0 run (tie at ceiling, both falsifiers fired as pre-agreed, ~$0). So
  find 1's "add serving context to the spec" port lands on a RUN instrument's
  seven-pin minimal contract (RECEIPT.md:91-96), not a paper spec, and the natural
  trigger is the receipt's own OWED row (difficulty-hardened re-run, RECEIPT.md:100-104).
- (b) The ollama toolchain pin on this box is 0.34.3 (RECEIPT.md:31, `ollama --version`
  during the A/B), so every typed-decision port (finds 6-8) carries a version step 0
  (0.34.3 -> 0.35, /v1/systemone door), exactly as the held percolator row's own probe
  already specified (memory/percolator/candidates.jsonl, ts 2026-10-02T04:17:43Z,
  grep -i tev1 run this sitting).

## Find 1: serving-context nondeterminism (arXiv 2610.09111) -> QUANTIZER + the P2 contamination tripwire

The paper (sweep :73-78, live abs page fetched by the sweep): 180 classifiers, checkpoint
and text fixed, fp32 batch-shape changes flip ZERO labels, bf16 batch-shape changes move
up to 56.7 percentage points of predicted probability mass with flips concentrated at
small margins. Organ: the quantizer's A/B instrument. Port move, concrete: add an
eighth pin, the SERVING-CONTEXT FINGERPRINT, to the run instrument's minimal pin
contract at quant_ab/RECEIPT.md:91-96 (which today pins weight-blob sha256, temp 0 +
paired seeds, num_ctx/num_predict, pooled verdict, strict rider, ps snapshot as a
logged rider only, and ollama version - batch shape and dtype appear NOWHERE in
QUANT_AB_SPEC_AMEND.md; grep over that file this sitting returned zero batch/dtype
lines). Concretely: promote the per-run `ollama ps` snapshot from logged rider (pin 6)
to a verdict-affecting pin, add OLLAMA_NUM_PARALLEL and flash-attention state to the
pinned-and-logged set, and require any two arms compared for promotion to have matched
serving fingerprints. Secondary landing: the P2 contamination tripwire (duty_fuzz mints
twins, delta >= 0.15 lands B2-106 risk rows; first pair gemma:2b 0.9167/0.8333, commit
6685db6bc) gains a mechanism candidate: the banked twin delta could be serving-context
drift, not prompt-twin drift. The primary probe below tests exactly this.

## Find 2: pollution collapse at the small rung (arXiv 2610.09772) -> GOPHER FLEET

The paper (sweep :79-87): 480 runs, INT4, Llama-3.1-8B + Gemma-3-4B on one M2. The
decoupled logic path is pollution-invariant (40/40 byte-identical outputs) while the
mixed single pass grows 242 -> 1,203 tokens and collapses (0.669 -> 0.150 Llama); the
8B decoupled arm beats single-pass (Holm p <= 0.03) but BOTH arms collapse on the 4B,
failure mode = failure to emit required structured output. Organ: the gopher fleet's
janitor rung (mag/ollama_policy.py:16, JANITOR = gemma:2b default, read this sitting).
Port move: a NEGATIVE placement law, one row in the gate's placement-law set (the G2
blind-sweep placement WARN from commit 6685db6bc is the precedent shape): decoupled-
logic / persona-separation cures are BARRED at the 2B rung without an on-box pollution
ladder; if the fleet ever needs pollution immunity, the mechanism is 8B-scoped
(qwen3:8B class) first, 2B only after its own curve exists. This is the paper's own
warning restated as estate law: a cure validated at 8B must not be assumed at 2B.
Per-find probe: a 20-row pollution ladder on gemma:2b (prompt-injected escalating
in-band pollution, score structured-output emission), minutes of box time, banks the
band's own curve the sweep's steal queue row 4 already asked for (sweep :206-208).

## Find 3: HEAR harness-engine protocol (arXiv 2610.06597) -> WATER GRAPH serving telemetry + lane runners

The paper (sweep :88-93): bidirectional harness-engine intent/state protocol buys 1.61x
batch speedup and 2.23x median TTFT reduction on SCBench under memory-constrained
concurrent serving, no task-quality loss. Organ: the water graph's serving-flow side and
the lane runners. Honest port shape: the intent/state channel itself is NOT portable to
ollama 0.34.3 (no protocol surface; the box toolchain pin is RECEIPT.md:31), so this
lands as a CONDITIONAL grammar row exactly like the sibling card's PatchKV conditional:
the port the estate CAN take today is the measurement half - per-run ttft_ms and
concurrency-state columns in the lane runner's row schema, so the estate owns its own
serving-state distribution (n=0 today) and any future engine change (0.35 upgrade,
llama.cpp bridge) has a before/after denominator. The 1.61x/2.23x numbers become the
pinned prediction that a future protocol port would have to beat on-box. Per-find
probe: instrument 50 real lane runs with ttft_ms + resident-model snapshot; prediction
from the paper's memory-constrained regime: two concurrent lanes on the 6 GB RX 5600 XT
push median TTFT >= 1.5x solo (Ollama serializes on one GPU); falsifier: concurrency
costs < 1.2x, meaning the estate envelope already captures the headroom and no protocol
port is worth buying.

## Find 4: same-family contamination + LR artifact (arXiv 2610.06204) -> PERCOLATOR + garden cell schema

The paper (sweep :99-104): Gemma-4 GRPO sellers, 1,152 negotiations/arm; small-model
failure was a learning-rate artifact (tripled LR wins at every size, +0.032 to +0.081);
the 4.5B arm fits one 48 GB GPU with no detectable gap to frontier sellers; and the
2.3B ten-x-LR arm's gain CONCENTRATES on the evaluation buyer sharing the training
pool's model family. Organ: the percolator and the garden's cell schema. Port moves:
(1) the champion-cell contamination suspicion (grok-4.7 row, "SWEEP CONTAMINATION-
SUSPECT (r1 answered a self-invented task)", RIB_MODEL_GARDEN_ROUTING.md, champion
table read this sitting) now has a small-model replicate in the literature - any
fine-tuned rung row in the garden gains an EVAL-FAMILY flag (was the scoring
distribution authored by the training family?) and defaults to contamination-suspect
when family matches; (2) the training half is hardware-dead on this box: 4.5B/48 GB
fails gate 2 of the five-gate tripwire (VRAM 24 GB minimum, RIB_GPU_LADDER_20261001.md
:15-16; box is RX 5600 XT RDNA1, :5-7, both read this sitting), which is exactly the
door find 8's $17 vendor fact walks through. Per-find probe: same-family shape, zero
spend - take 20 scored lane items, 10 authored by the mag stack (gemma-adjacent text)
and 10 imported verbatim from external corpora, score all with gemma:2b janitor;
prediction: same-family pass-rate exceeds cross-family; falsifier: gap <= 2 points,
meaning the tripwire's prompt-twin axis is the only contamination axis this fleet needs.

## Find 5: benchmarks must match task flows (arXiv 2610.09633) -> GOPHER FLEET battery + the decision meter

The paper (sweep :110-114): 4,782 real JetBrains sessions; no single interaction
distribution is universally realistic; sequential multi-step solving roughly doubles
cost at flat resolve rate in the pilot. Organ: the gopher fleet's bench and the
sovereignty meter. The meter demands "accuracy >= 0.880 on the fleet's own labeled
distribution" (mag/verb.py:490-491) with validity at n >= 40 (mag/verb.py:504, read
this sitting) - but the DISTRIBUTION is unspecified, which makes the meter's denominator
undefined and the beat-gemma:2b question formally unanswerable (the sweep says the same
at :141-148). Port move: the fleet bench's sampling weights are derived from the lanes'
real trails (dashboard/static/trails/*.jsonl) BEFORE any challenger rung is scored;
bench task mix becomes a named, versioned spec, not a default. Per-find probe: zero GPU
- classify 100 recent trail rows by task type and interaction shape (single-shot vs
sequential multi-step), emit the empirical mix; pinned prediction: lanes are > 70
percent single-shot, so single-step benches are distribution-valid and find 5's cost
warning does not bind; falsifier: < 40 percent single-shot, meaning the current 10-task
single-step quant_ab task set (RECEIPT.md:11-12) is mis-specified for the lanes it
claims to speak for.

## Find 6: Kev 1.0 decision family (x.com/jaredpalmer 2105803379587068011) -> PERCOLATOR

Kev-27B + Kev-9B, open-weight decision models with their own fine-tuning path (find
quote). Organ: the percolator. Port move: a candidate row carrying the new-animal gate
- Kev is a NEW animal under the per-animal harness law ("Every animal below gets its
OWN harness", RIB_MODEL_GATES_20261001.md:8-11, read this sitting), so it inherits no
gemma/qwen harness profile; Kev-9B sits at the band edge (estate band 0.5B-8B per the
sweep header :4-5) and needs an operator ruling to enter; Kev-27B fails five-gate gate
2 outright on this box (24 GB minimum, RIB_GPU_LADDER_20261001.md:15-16). Per-find
probe: zero spend - check HF + the Ollama library for a Kev-9B GGUF and its Q4_K_M
bytes against the 6 GB envelope; no GGUF or over-envelope -> files UNMEASURED + GATED
with the gate named; sub-envelope -> enters the garden queue behind tev1:0.8b and
d1-3B (the sweep's steal queue row 3, sweep :203-205).

## Find 7: Tev1 0.8B weights (x.com/nutlope 2103548354022305802) -> PERCOLATOR held row + GOPHER FLEET bench

The delta banked this sitting (percolator row verified: memory/percolator/
candidates.jsonl, "tev1 4B and tev1:0.8b Together AI" held since the 09-30 window, ts
2026-10-02): primary post + HF weights URL (huggingface.co/togethercomputer/
Tev1-0.8B-experimental) + the vendor's own scope caveat ("very simple classification")
which matches janitor scut scope exactly. 0.8B is inside the band. Organ: percolator ->
gopher fleet bench. Port move: tev1:0.8b is the cheapest concrete candidate for the
band's first UNMEASURED-cell measurement, through the typed-decision door the estate
already specced: CHOICE / SCORE / NOUL primitives (memory/research_packs/
THE50_W3_T11_TYPED_DECISION_ORACLES.md:8-11, read this sitting), reachable only after
the ollama 0.34.3 -> 0.35 upgrade step 0 (RECEIPT.md:31 toolchain pin; the held row's
own probe names the same step with rollback surface = daemon binary, model blobs
persist). Rows would land through the fleet-bench record function, which by
construction refuses evidence-free rows (mag/verb.py:471 "meter row without evidence
is decoration: refused", read this sitting). Per-find probe: the held row's own
three-question POST (one CHOICE, one SCORE, one NOUL) against tev1:0.8b on 0.35 -
either the typed contract parses on-box or it does not; both outcomes bank a row.

## Find 8: tev1-4B $17 training cost (x.com/togethercompute 2102882216950763814) -> PERCOLATOR economics + five-gate gate 3

The fact: a Jev-like 4B classifier fine-tuned on Qwen3.5 4B, $0.042/M input and $0
output on Together serverless, $17 total training cost, data recipe released (find
quote). Organ: percolator economics, as the standing counterweight to any local-LoRA
instinct. Port move: one ECON.md planning-input row (vendor numbers live as PLANNING
inputs, never verdicts - garden Law 1 "INSTRUMENTS ONLY ... Hand-copying a vendor
number into an empty cell is fabrication", RIB_MODEL_GARDEN_ROUTING.md, read this
sitting): before ANY on-box fine-tune attempt is scoped, the vendor path is priced
first, because the box cannot host the training run at all (gate 2: 24 GB minimum vs
6 GB VRAM, RIB_GPU_LADDER_20261001.md:15-16) and $17 is the measured price of the
whole alternative. This converts the five-gate law's hardware gate from a block into
an economic comparison with a number in it. No standalone probe: this find's falsifier
rides find 7's probe (if tev1:0.8b/4B fill the decision rung through the vendor or
library path, the on-box LoRA branch is dead on arrival, which is the prediction).

## PRIMARY PROBE (the card's one falsifiable probe; cheap, instruments already live)

Serving-context variation on the banked P2 twin pair. Step 0: enumerate which serving
knobs ollama 0.34.3 actually exposes on this box (OLLAMA_NUM_PARALLEL, flash-attention
toggle, keep_alive cold/warm) via `ollama serve --help` + env docs, minutes. Then
re-score the SAME duty_fuzz-minted cases through gemma:2b (JANITOR default,
mag/ollama_policy.py:16) under three deliberately varied serving shapes with prompts
byte-identical and temperature 0, and recompute the twin deltas (P2 threshold: delta
>= 0.15 lands a risk row, commit 6685db6bc). Pinned prediction from 2610.09111's
mechanism: at least one serving-shape pair moves the gemma:2b twin delta by >= 0.15,
proving serving drift is a live confounder on this stack and earning the
serving-fingerprint column in both the P2 tripwire schema and the quant A/B pin
contract (find 1's port). Falsifier: all deltas stable within +/-0.05 across shapes -
the bf16 batch-shape mechanism does not port to this box's GGUF-Q4 accumulation path
at 2B, the banked 0.9167/0.8333 pair stands as genuine prompt-twin drift, and the
eighth pin is demoted to a logged rider like the strict-parse channel was (RECEIPT.md
:46-53 precedent). Cost: roughly a dozen 2B generations x 3 shapes, minutes, $0.

## Verification census (this sitting, for this card)

- Read: sweep/open-local-models-arxiv.md in full (the finds' source); sweep/quant_ab/
  RECEIPT.md in full; port_wave_20261007/QUANT_AB_SPEC_AMEND.md pin legs (grep + read,
  zero batch/dtype lines confirmed); mag/verb.py:328 and :470-505; mag/ollama_policy.py
  :10-25; memory/rib/RIB_MODEL_GATES_20261001.md in full; memory/rib/
  RIB_MODEL_GARDEN_ROUTING.md Law 1 + champion-cell table section; memory/rib/
  RIB_GPU_LADDER_20261001.md:1-23; memory/research_packs/THE50_W3_T11_TYPED_DECISION_
  ORACLES.md:8-11; memory/percolator/candidates.jsonl tev1 row (grep -i tev1);
  tools/duty_fuzz.py structure (grep def/delta/score); the 10-02 five-gate steal card
  :35-45; sibling steal card + JSON (kv-cache-context-engineering) for format.
- NOT run this sitting (stated, not guessed): the catalog/memory overlap greps are the
  sweep seat's own runs, cited from sweep :210-229, not re-run here; no ollama calls,
  no duty_fuzz scoring, no trail classification, no Kev-9B GGUF lookup were executed;
  every probe above is a proposal, none is a result. All paper numbers are the
  papers'/vendors' own claims at abs-page level (sweep OWED section :231-248 carries
  the full not-read list: no PDFs, vendor pages unverified beyond their own text).
- Em-dash law: ASCII only, by construction.
