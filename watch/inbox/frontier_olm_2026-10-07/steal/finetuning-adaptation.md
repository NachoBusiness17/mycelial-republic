# STEAL CARD: finetuning-adaptation (frontier OLM 2026-10-07) - REV 2

Round 2 per the steer critique. Four fixes landed this revision: (1) the overlap ledger is
extended to the prior-day watch/inbox frontier trees and NAMES the 2026-09-30 raw holding,
which is then mined (RL mechanism detail, practitioner Aider and llm-bench numbers); (2)
the headline probe no longer re-derives an owed probe with a broken instrument, it FIRES
the owed fold probe 5 with deepseek-r1:1.5b as the thinking-capable primary arm; (3) the
"reproducible on other model families" quote is re-attributed from the HF card to the HN
thread author; (4) a machine-readable card section identical to the returned StealCard
JSON is embedded (steer contract reads both, .zcode/workflows/olm-mine.dwf.ts:406; the
10-06 precedent shape is kv-context-engineering.md:58). Repair class is the same R5 the
10-06 finetuning-adaptation card took
(watch/inbox/frontier_olm_2026-10-06/steal/finetuning-adaptation.md:57). What survived
from round 1 untouched: all primary-URL quote verifications, every code pin, and the organ
maps and probes of finds 2 and 3. Reddit/arXiv quotes below are ASCII-normalized
(typographic apostrophes flattened); wording is otherwise verbatim.

## Find 1 (headline): Swift-Qwen3.8-27B, reasoning-marker penalization at weight level

- URL: https://huggingface.co/ukisai/Swift-Qwen3.8-27b (HN thread 49727511, source: hn)
- Verified at the model card (round 1, re-verified by the steer): "using 58.3% fewer
  thinking tokens while maintaining near-identical performance (<1% loss) and as a result
  getting a x1.95 speed-up on several tasks"; "fine-tuned Qwen by penalizing usage of
  those tokens while it reasons"; bench deltas AIME 2026 98.67 -> 94.00, LiveCodeBench
  v6 76.76 -> 81.55 (gain, tokens down 24.3%), Terminal-Bench 2.1 66.74 -> 65.84,
  GPQA-Diamond 88.38 -> 88.28 (58.3% is the MEDIAN token cut there, mean ~41%); transfer
  component credited to BottleCap AI's ThinkingCap-Qwen3.6-27B.

### The estate already holds the raw primary (named and mined this session)

The estate has held this find's raw practitioner bytes since 2026-09-30 in
watch/inbox/frontier_olm_2026-09-30/sweep/_raw/ (extracted this session by a python walk
over the JSON; commands in the receipt section below):

- p30_LocalLLaMA_win_rate.json, thread 1wh5elt, "Cut Qwen3.8-27B Reasoning Tokens by 40%
  -- 3.8 'ThinkingCap' benchmarked!" (86 comments, outbound link to the ukisai HF card).
  Selftext carries the mechanism detail the HF card omits, the RL framing: "They
  identified 'reasoning-marker tokens that ... trigger overthinking in Qwen's reasoning
  rollouts' and penalized them using RL, resulting in fewer overthinking errors. They also
  employed 'a transfer component derived from BottleCap AI's
  ThinkingCap-Qwen3.6-27B'". Same thread carries the Aider eval table: Pass1 30.8 vs 27.1,
  Pass2 75.7 vs 77.6, well-formed diff 98.1 vs 99.1, completion tokens 7,301 vs 12,547,
  seconds/case 750 vs 1,481, total tokens/solve 12.1k vs 19.3k, with the author's summary
  "equivalent success rate in approximately half the time, using 63% of the tokens".
  ATTRIBUTION CORRECTION AGAINST THE CRITIQUE (byte-true): this Aider table lives in
  1wh5elt, not 1wq56pf; the critique swapped them. 1wq56pf is the Flash-Next successor
  thread ("Swift1.5-Qwen3.8-Flash-Next is phenomenal vs. base 3.8-Flash!", re-held in
  watch/inbox/frontier_olm_2026-10-03/sweep/arctic_LocalLLaMA.json) and carries its own
  paired stats: n=107 paired cases, 99 agree / 2 gains / 6 losses, "McNemar exact p = 0.29
  (not significant)" so "statistically indistinguishable in quality"; mechanism color:
  "base frequently goes on long reasoning binges, looping back several times on itself.
  Swift almost never does"; on base's 20 most token-hungry runs Swift used 29% of the
  tokens and solved 16/20 vs base's 17/20.
- p30_LocalLLaMA_judge.json, thread 1wte7n0, "Swift-1.5-Qwen3.8-27b-oQ8e-mtp on Apple M5
  Max - 34.8 tok/s - llm-bench.io": per full run "Swift averages 51k generated tokens and
  Qwen3.8 averages 77k" (code 28.6k vs 40.1k, research 11.1k vs 21.2k, agent workflow
  7.5k vs 11.9k, role play 4.0k vs 3.8k), run duration 24 vs 38 min, llm-judge quality
  85.8 vs 85.0 (four runs 84.3 to 87.2).
- watch/inbox/frontier_olm_2026-10-04/sweep/_amc_harvest_LocalLLaMA.jsonl carries 43
  ukisai/Swift rows, including a benchmark row "Swift-Qwen3.8-27B (this run) 68.4 84.4%".

So the estate held the phenomenon (09-30) and the sweep found the primary (10-07); no
prior steal card banks the mechanism (first carding, receipt below). This card is the
first to lift the mechanism into a port.

### Estate prior art (read round 1, re-pinned; plus one convergence added this round)

- The estate's overthinking disease is named and param-cured: mag/inference_budget.py:13
  "THE ONE BUG (months of jackets, one law): the model spends the whole output budget on
  hidden reasoning and the content channel returns empty"; EMPTY_REASONING is TERMINAL at
  mag/inference_budget.py:19.
- The LoRA organ and its arming pattern: mag/lora_pipeline.py:27 (TARGET
  Qwen2.5-1.5B-Instruct, QLoRA 4-bit) and mag/lora_pipeline.py:15-17 (the ReFlux
  watch-trigger precedent: a published finetune method arms the pipeline door at a new
  target on the hands-box 3090 rung).
- NEW CONVERGENCE (this round): the 10-03 quantization steal card already banked the
  SAMPLER-level twin of this mechanism
  (watch/inbox/frontier_olm_2026-10-03/steal/quantization-and-compression.md:31): on a
  reasoning model, W3 PTQ inflates CoT length 2.94x (GPTQ) to 3.77x (AWQ) while accuracy
  falls 60.13 to 33.82, and "training-free token-specific penalties recover up to 9.8
  accuracy points while cutting CoT length up to 51.3 percent". Same marker class, two
  independent intervention points: decode-side bias (banked) and weight-side penalty
  (this find). The mechanism is convergent, not single-source.

### The delta (what is actually new to port)

The estate cures overthinking at the JACKET level (caps, terminal reactions, recipe
gates) and, since 10-03, knows the sampler-level penalty. This find adds the weight-level
cure with published deltas and RL as the training signal, so every future call of the
animal is cheaper with no jacket and no sampler change. The thread's zionsati claim
("lower quants suffer from low confidence in its own reasoning and tend to overthink
because of that", sweep/finetuning-adaptation-hn.md:16) makes the quantizer coupling the
testable local hinge. Reproducibility across families is the THREAD AUTHOR's claim
(sweep/finetuning-adaptation-hn.md:16, "author claims"), not a HF-card claim (fix 3;
the card carries no such sentence).

### Organ map

Feeds the LORA PIPELINE organ (mag/lora_pipeline.py) and lands its resulting animal in
the inference-budget recipe table (mag/inference_budget.py, the per-animal recipe single
source). Port move, staged: (1) mine marker-token candidates from the estate's own
EMPTY_REASONING receipts and local rollout traces (the wait/however/alternatively hedge
class inside thinking blocks); (2) cheap leg first, the sampler-level token-specific
penalty on the SAME marker set (the banked 10-03 mechanism, deployable without training);
(3) durable leg second, the marker-usage penalty objective (RL-shaped per the held thread
bytes) beside the identity-vector objective in the QLoRA pipeline at the 1.5B/2B rung,
armed via the existing ReFlux-style watch-then-fire discipline.

### Falsifiable probe (REVISED, fix 2: fires the owed probe instead of re-deriving it)

The estate already owes this probe: 10-03 lens fold probe 5, "local qwen2.5:7b Q4_K_M vs
q8_0 A/B" (watch/inbox/frontier_olm_2026-10-03/lens/burns.md:122), which the 10-03
quantization steal card extended to "gain the thinking-token channel" with
deepseek-r1:1.5b named as the reasoning-capable arm on box
(quantization-and-compression.md:31), its q8_0 twin verified at tag level as
deepseek-r1:1.5b-qwen-distill-q8_0 at 1.9 GB (quantization-and-compression.md:12;
byte-digest check at pull time still OWED there). This card fires that owed probe with
the zionsati hypothesis attached. Primary arm: deepseek-r1:1.5b (thinking-capable,
<think> blocks) at its held default quant vs the q8_0 twin; same deterministic 12-task
set, fixed temperature; count thinking tokens inside think blocks plus hedge-marker
frequency per CORRECT answer only. Prediction: the lower-quant arm emits more thinking
tokens and hedge markers at equal accuracy. Confirmed -> the marker-penalty LoRA target
is armed for mag/lora_pipeline.py, a quant-aware line enters the per-animal recipe table,
and owed probe 5 retires with a result. Falsified -> the coupling claim dies locally and
the port scopes to EMPTY_REASONING-family animals only. Round 1's qwen2.5:3b-instruct arm
is RETIRED as an instrument error: it is a non-reasoning model with no thinking blocks,
so a thinking-channel counter cannot fire on it at all (critique fix 2, conceded; ollama
list stamped 17 rows at 2026-10-07T22:19Z this session, all three animals on box).

## Find 2: ActFirst-OPD, reference-conditioned inverse dynamics (act first, reason later)

- URL: https://arxiv.org/abs/2609.36608 (2026-09-29). Verified at the abstract (round 1,
  re-verified by the steer): final sentence "These results demonstrate that reasoning
  need not block acting during multi-turn agent distillation."; students Qwen3
  0.6B/1.7B/4B; wall-clock speedups over Vanilla OPD: 2.3x ALFWorld, 1.8x WebShop, 4.9x
  ScienceWorld; sweep adds matches-or-beats all OPD baselines on 8 of 9 settings
  (sweep/finetuning-adaptation-x.md:15).
- Estate prior art: mag/max_distill.py:3-5 asks the estate's experiment question (pin
  corrected from :1 this round: "what fraction of a frontier model's verified advantage
  can be recovered as an automatically-extracted, mechanically-applicable policy executed
  by a cheap model on held-out states?"); the SkillCandidate schema is already act-shaped
  (action_policy at mag/max_distill.py:40, no rationale field required). But
  distill-to-bus is an ORPHAN doctrine
  (watch/inbox/frontier_olm_2026-10-07/lens/graph.md:30, bare label, zero edges).
- Delta and organ map (stands as drafted): the missing measured recipe at exactly the
  sub-8B tier; condition the student on the eventual SUCCESS REFERENCE via inverse
  dynamics, never on teacher rationales. Port: outcome-conditioned SkillCandidate minting
  from banked gopher runs, (antecedent state, action sequence, landed outcome) triples,
  rationale excluded from conditioning and kept as human-facing provenance; the admission
  firewall and near-miss suite untouched.
- Falsifiable probe (stands as drafted, deterministic, $0, one script): walk the banked
  run ledgers (dashboard/static/trails/*.jsonl, memory/runs/), count what fraction of
  SUCCESS rows carry enough (state, action, outcome) signal to mint an act-first
  SkillCandidate with zero rationale in the conditioning. High fraction -> telemetry-ready
  today; low fraction -> blocked on run-logging shape (conclusions logged, moves not) and
  that blockage is itself the finding.

## Find 3: recurrence boundary condition for looped LMs (reasoning gains, knowledge loss)

- URL: https://arxiv.org/abs/2609.36636 (2026-09-29). Verified at the abstract (round 1,
  re-verified by the steer): "We find that recurrence can improve reasoning beyond the
  training horizon while degrading knowledge performance"; proposed fix: "channel-wise
  history-state injection combined with timestep conditioning", "better preserving
  knowledge under extended unrolling while improving robustness across inference
  budgets". Boundary condition for the LiFT loop-flow claim (arXiv 2610.05538,
  link-dropped 10-07 at lens/burns.md:159; sweep x-file :21, :43).
- Estate prior art (stands): the loop-flow claim held with no boundary; loop surfaces at
  mag/distill.py:117 (cycle(raw, n)) and any second-pass/self-refine in batch lanes.
- Delta and organ map (stands as drafted): loop depth is NOT free capability; it trades
  against knowledge tasks; the mitigation is conditioning design (timestep visible to the
  model), not depth choice alone. Port: a per-task-class loop-depth gate in the
  inference-budget recipe table: reasoning-class asks may loop; knowledge-class asks
  (recitation from corpus/memory bytes) pin depth 1; every looped pass carries its
  timestep visibly.
- Falsifiable probe (stands as drafted): 10 knowledge questions answered verbatim in
  banked bytes (exact-substring graded) plus 10 deterministic reasoning micro-tasks,
  single-pass vs two-pass (output fed back), on qwen2.5:7b (on box, ollama list stamped
  this session). Prediction: two-pass helps the reasoning arm, hurts or flat-lines the
  knowledge arm. Honest scope note: a prompt-loop second pass is the cheap cousin of
  architectural recurrence; the probe tests the boundary's practical form, not the looped
  architecture itself.

## Overlap receipt (REV 2: extended to prior-day frontier trees, R5 repair class)

Scope-true round-1 greps (reproduced by the steer): rg -c -e "Swift-Qwen" -e "ukisai" -e
"ActFirst" -e "2609\.36608" -e "2609\.36636" catalog/catalog.jsonl -> 0, exit 1; rg -l
same terms over memory docs state (excluding this frontier dir and trajectory telemetry)
-> 0 hits. EXTENDED this round: (a) the 09-30 raw holding named above, extracted with a
.venv/Scripts/python.exe utf-8-sig JSON walk printing id/title/selftext for targets
{1wh5elt, 1w5atm, 1wte7n0, 1wq56pf} over the four files p30_LocalLLaMA_win_rate.json,
p30_LocalLLaMA_judge.json, 10-03 arctic_LocalLLaMA.json, 10-04
_amc_harvest_LocalLLaMA.jsonl; hits printed for 1wh5elt, 1wq56pf (win_rate + arctic),
1wte7n0 (judge); (b) rg -c "ukisai|Swift" on the 10-04 amc harvest -> 43; (c) FIRST
CARDING: rg -l -e "Swift-Qwen" -e "ukisai" -e "reasoning-marker" over corpus/steal and
the steal dirs of frontier_olm 2026-09-30, 10-03, 10-04, 10-05, 10-06 -> zero hits, exit
1 (the 10-06 finetuning-adaptation.md sibling exists but banks none of this mechanism;
it took repair R5 itself at its :57). UNVERIFIED: the critique's "sibling thread 1w5atm
same" - rg -l "1w5atm" over watch corpus memory -> ZERO hits repo-wide; that thread id
exists in no estate byte this seat can read, so it stands on the critique's say-so only.

## Verification ledger (REV 2)

Verified this session (round 2): the 09-30 holding existence and content (python walk,
quotes above); the 10-03 arctic re-hold of 1wq56pf; the 10-04 amc 43-row count; the
first-carding grep over all prior steal dirs; the owed-probe lineage
(frontier_olm_2026-10-03/lens/burns.md:122 read; quantization-and-compression.md:12 and
:31 read); the steer-contract line (.zcode/workflows/olm-mine.dwf.ts:406 "Read " + OUT +
"/steal/" + areaKey + ".md and the returned card JSON."); the R5 precedent
(10-06 finetuning-adaptation.md:57) and the machine-readable precedent
(kv-context-engineering.md:58); max_distill.py:3-5 pin; ollama list stamped 17 rows at
2026-10-07T22:19Z; em-dash byte check on this file (grep for U+2014: 0 hits). Carried
from round 1 (re-verified by the steer, not refetched by this seat): the three
primary-URL quote fetches (HF card, both arXiv abstracts). OWED / not run: all probes are
named, not run (card scope is draft-and-bank); the q8_0 twin is not yet pulled
(tag-level verification only, per the 10-03 card's own OWED); 1w5atm unverified (above);
both arXiv items read at abstract level only; the 09-30/10-03/10-04 holdings were read as
raw JSON rows this session, their source threads were not refetched from reddit; the
marker-mining corpus (EMPTY_REASONING receipts as marker source) is asserted from the
module header, not yet extracted.

## Machine-readable card (identical to the returned StealCard JSON)

Appended by the drafting seat; chars field counts this file's characters.

```json
{
 "area": "finetuning-adaptation",
 "steal": "Reasoning-marker penalization, doubly specified this round: the estate's own 09-30-held thread bytes (1wh5elt in frontier_olm_2026-09-30/sweep/_raw/p30_LocalLLaMA_win_rate.json) carry the mechanism detail the HF card omits - the markers are penalized USING RL ('They identified reasoning-marker tokens that ... trigger overthinking in Qwen's reasoning rollouts and penalized them using RL') with a BottleCap ThinkingCap transfer component; the card adds -58.3% thinking tokens (GPQA median, mean ~41%), <1% accuracy loss, x1.95 speed, AIME 98.67-94.00, LiveCodeBench 76.76-81.55, Terminal-Bench 66.74-65.84. Practitioner deltas held in-estate: Aider Pass1 30.8 vs 27.1 at 7,301 vs 12,547 completion tokens and 750 vs 1,481 sec/case (1wh5elt); llm-bench 51k vs 77k generated tokens, 24 vs 38 min, judge quality 85.8 vs 85.0 (1wte7n0); Flash-Next paired n=107 McNemar p=0.29, statistically indistinguishable (1wq56pf). The mechanism CONVERGES with the estate's banked sampler-level twin (10-03 quant card leg 1: training-free token-specific penalties recover up to 9.8 points, cut CoT 51.3%) - same marker class, weight-side vs decode-side. Supporting steals: ActFirst-OPD (arXiv 2609.36608, success-reference-conditioned inverse dynamics, acting never blocks behind reasoning, 1.8-4.9x wall-clock at Qwen3 0.6B/1.7B/4B) and the looped-LM recurrence boundary (arXiv 2609.36636: recurrence improves reasoning beyond the training horizon while degrading knowledge; channel-wise history-state injection + timestep conditioning is the mitigation).",
 "source_url": "https://huggingface.co/ukisai/Swift-Qwen3.8-27b",
 "estate_map": "Feeds the LORA PIPELINE organ (mag/lora_pipeline.py:27 Qwen2.5-1.5B QLoRA target, ReFlux arming precedent :15-17) plus the inference-budget recipe table (mag/inference_budget.py:13 and :19, the EMPTY_REASONING disease this cures at weight level instead of jacket level). Staged port: mine marker candidates from EMPTY_REASONING receipts and rollout traces; cheap leg first (sampler-level token-specific penalty on the same marker set, the banked 10-03 mechanism, no training needed); durable leg second (marker-usage penalty objective, RL-shaped per the held thread bytes, beside the identity-vector objective), armed via watch-then-fire. Supporting maps stand from round 1: GOPHER FLEET via max_distill (experiment question at mag/max_distill.py:3-5, act-shaped action_policy :40; outcome-conditioned SkillCandidate minting with rationale excluded from conditioning; distill-to-bus orphan per lens/graph.md:30) and the recipe-table loop-depth gate (reasoning asks may loop, knowledge asks pin depth 1, timestep visible, vs the LiFT claim at lens/burns.md:159). Full write-up: watch/inbox/frontier_olm_2026-10-07/steal/finetuning-adaptation.md.",
 "probe": "FIRES the estate's owed fold probe 5 instead of re-deriving it (10-03 lens/burns.md:122 '(5) local qwen2.5:7b Q4_K_M vs q8_0 A/B', extended by the 10-03 quant steal card :31 to the thinking channel with deepseek-r1:1.5b as the reasoning-capable arm; q8_0 twin verified at tag level as deepseek-r1:1.5b-qwen-distill-q8_0, 1.9 GB, card :12). Run one deterministic 12-task set on deepseek-r1:1.5b default quant vs the q8_0 twin, fixed temperature; count thinking tokens inside think blocks plus hedge-marker frequency per CORRECT answer. Zionsati hypothesis attached (sweep/finetuning-adaptation-hn.md:16): lower quants overthink from low confidence; prediction: the lower-quant arm emits more thinking tokens at equal accuracy. Confirmed arms the marker-penalty LoRA target and retires the owed probe with a result; falsified kills the coupling locally and scopes the port to EMPTY_REASONING-family animals. Round-1's qwen2.5:3b-instruct arm is retired (non-reasoning model, no thinking channel - instrument error, conceded). Companions in the write-up: the act-first SkillCandidate telemetry census over banked SUCCESS rows, and the single-vs-two-pass knowledge/reasoning A/B on qwen2.5:7b.",
 "chars": 19959
}
```
