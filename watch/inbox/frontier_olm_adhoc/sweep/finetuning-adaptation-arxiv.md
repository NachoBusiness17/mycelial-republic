# SWEEP: finetuning-adaptation via arxiv (frontier_olm_adhoc)

source-fetched: adhoc · seat: sweep-finetuning-adaptation-arxiv · moment: 2026-10-10
Doors: export.arxiv.org API returned HTTP 429 twice on this egress IP (same hard limit
the quantization sweep hit earlier today; sequential curl not attempted after the
WebFetch pair failed). Fallback per recipe: /list/cs.CL/recent + /list/cs.LG/recent via
WebFetch (worked, 50 titles each read), site-scoped WebSearch (two long-form queries
timed out at 60s; short id-anchored queries worked), GitHub /releases pages via
WebFetch for TRL and verl, and curl of arxiv abs + full-HTML pages (all succeeded;
raw pages banked as `_ft_*.html` / `_ftfull_*.html`, extracted text `_ftread_*.txt` in
this directory). Every banked item below was fetched and read by this seat; six papers
were read in full HTML end to end.

Estate hooks this feeds: corpus/CURRICULUM.md:85-89 (un-started clone queue: trl,
verl, deep-rl-class, vllm, sglang...), the `mag improve` promote lane,
memory/rib/RIB_TEN_MINUTE_SELF_20261010.md (the JIT fine-tuning law + two falsifiers),
memory/rib/RIB_LIVING_WEIGHTS_BY_NATURE.md (ASTRA-class context-to-weight door),
watch/inbox/frontier_olm_adhoc/lens/burns.md:103 (the fine_tuning_jit_law_20261010 card).

## Pass 1 coverage

Considered 100+ candidates: 50 cs.CL recent-listing titles (Oct 9), 50 cs.LG
recent-listing titles (Oct 9), plus search-surfaced items (Agentic-TTT related work:
RoboTTT, TTT-Discover, qTTT, In-Place TTT, ETT, SEAL, TTRL, TLM, TTT-FS, CURE, AMC-TSI).
Full abs pages fetched and read for eleven: 2610.12002, 2607.03441, 2510.07841,
2610.11959 (MiMo-V2.6), 2610.12367, 2610.11659, 2610.11776, 2610.11854 (GRPODropout),
2610.11519 (Residual Advantage/CoRA), 2610.12274 (HarnessSQL), 2610.12161 (ZCPO).
Pass 2 deep reads in full HTML: 2607.03441, 2610.12002, 2510.07841, 2610.12367,
2610.11776, 2610.11659 - six end to end.

## RQ verdicts

### RQ1: JIT/test-time/LoRA-swap adaptation under ten minutes - the law is now PUBLISHED, with its bound

aTTT (2607.03441, "No Time Like the Present: Agentic Test-Time Training for LLM
Agents") is the estate's JIT law built by someone else, down to the serving layer:
per-episode private LoRA adapters hot-swapped through vLLM's runtime LoRA API in
under 100 ms, training decoupled on separate GPUs, 16 concurrent episodes, wall-clock
1.9x the no-TTT run, update cadence K=5 agent steps, adapter persists within an
episode and resets between episodes. The estate's ten-minute budget is ~4 orders of
magnitude looser than what a published system already achieves; latency is not the
binding constraint - corpus quality and gating are.

The bound, stated by the authors: gains concentrate where the model already has task
competence and drifts on long trajectories; aTTT "mainly preserves existing competence
rather than teaching new abilities." And the smallest model gains least (Qwen3.5-4B:
1.9 to 3.6 ALFWorld vs 9B: 50.7 to 55.7). For the estate: the pitfall-bypass corpus
can rescue an agent that KNOWS better but drifts; it cannot inject missing skill into
a 2B janitor. Feed the workers, not the scut.

Agentic-TTT (2610.12002) supplies the missing organ - the GATE. A learned policy
decides per query: direct answer, reuse a stored skill-LoRA, or run one of 5 TTT
methods (PoT, TTT-FS, TTRL, SEAL, TLM) as a callable tool. Headline: overall utility
0.256 to 0.510 on Qwen2.5-7B-Instruct (2x), vs prompted 0.271 and embedding-router
0.347. The falsifier-relevant finding: without an explicit compute penalty the policy
OVERUSES TTT; a moderate penalty cuts compute ~30% while utility RISES (direct-answer
rate 11.8% to 39.8% at lambda 0 to 0.4). Fixed methods flip sign across domains
(Always-SEAL helps passage QA, hurts math/code). Estate law confirmed from outside:
adaptation without gating is a drain, exactly the 03:00Z drain bug in weight-space.

### RQ2: has anyone cleared the ten-minute-self falsifiers? Not the week-over-week one; the prompt-vs-weights one, YES (twice)

Falsifier 1 (week-over-week pitfall-rate decline): NOT CLEARED anywhere I read.
Nearest neighbors: aTTT shows within-episode repetition-rate decline in rescued pairs
(no-TTT trajectories' self-text repetition rises above 80%; aTTT stays low and the run
finishes in 26.3 steps vs the 50-step budget) - episode-scale, not week-scale.
Agentic-TTT evaluates on a 176-query held-out sequential stream with a persistent,
warm-started skill library ("accumulation-before-reuse order", adapter re-adaptation
refused until N new samples accumulate) - compounding-over-deployment-time, but scored
as final utility, not as a pitfall-rate time series. SGUID shows two-round model-skill
co-evolution where unfiltered skill feeding DEGRADES the model on round 2 (Qwen3-4B
HMMT25 -0.3 with naive update vs +1.1 selected) - the estate's dead-salmon curation
rider has a published twin. Verdict: the estate's specific falsifier (week-over-week
recurring-pitfall rate from commit diffs) remains unclaimed territory; nobody is
measuring self-improvement on a pitfall-rate clock.

Falsifier 2 (controlled-corpus fold beats prompt-only on held-out pitfalls): CLEARED
by aTTT 4.5 and by TT-SI. aTTT, matched update text, Qwen3.5-9B ALFWorld: in-context
injection of the Summary signal scores 49.3%, BELOW the no-TTT baseline 50.7%, while
the same text as adapter update scores 54.3%. Stated reason: injected text consumes
prompt budget competing with the growing trajectory; adapter updates persist at zero
prompt cost. TT-SI on SealTool: fine-tune variant 72.43% vs ICL-with-same-generated-
examples 68.36% vs standard ICL 67.74%. Two independent 2025-2026 results say: under
matched food, weights beat prompt. The JIT framing is NOT "distillation wearing a
clock" - it is the serving-time choice that wins precisely because context is the
scarce resource on long horizons.

TT-SI (2510.07841, ACL 2026 Findings) is the closest published self-improvement loop
to the ten-minute-self shape: uncertainty estimator H flags hard cases, then
synthesizes ONE similar training instance per case, then a single-LoRA test-time
update on one A40. +5.48% absolute across 4 tool-calling benchmarks (ToolAlpaca
+5.84, NexusRaven +6.05, SealTool +5.76, API-Bank +4.26); beats 13k-sample SFT 70.20%
with 190 cases (72.43%, 68x fewer samples); SMALLER models gain MORE (Qwen2.5-1.5B
+5.76 vs 7B +3.02); teacher variant (gpt-5-mini) adds only +0.94 to +2.65. Bound:
bounded by base capacity - absent knowledge needs retrieval, confirming the estate's
tier design (sensing/free + retrieval stays; the fold adds pitfall-bypass, not world
knowledge).

### RQ3: where the clone budget should land (TRL first, verl second, deep-rl-class deprioritized)

TRL 2026 arc (github.com/huggingface/trl/releases, read this session):
- v1.15.0 (Oct 8, 2026): fused Triton LM-head for SFT/DPO/KTO/GRPO/RLOO/Distillation,
  up to 6.9x longer sequences, 52-82% peak memory cut - the single biggest lever for a
  1-8B local lane on consumer VRAM.
- v1.14.2 (Oct 6): fixes SILENTLY WRONG GRPO/RLOO/Distillation on models with extra
  end-of-turn ids - Gemma 3/4 named. The estate's janitors are gemma: any RL
  experiment on gemma must be on >=1.14.2 or its numbers are suspect.
- v1.14.0 (Sep 25): chunked logprob streaming + fused Triton logprob/entropy kernel
  (~14x faster); six experimental trainers removed (BCO, XPO, NashMD, PRM,
  replay-buffer GRPO, GSPO-token).
- v1.13.0 (Sep 10): PPO removed entirely; 1M-token long-context training recipe
  (Qwen3-8B, 8xH100); tensor-core chunked lm_head (1.2-1.7x, "big win for small
  models with large vocabs").
- v1.11/v1.10 (Aug): `trl vllm-serve` (1.4-1.6x GRPO step), DistillationTrainer
  stable (VLMs + tool calling), AsyncGRPO agent training via OpenEnv, experimental
  AsyncDistillationTrainer (multi-teacher MOPD).
Verdict: TRL is the estate's post-training spine - the whole 2026 arc is
small-model-and-memory efficiency plus agent-loop training. Clone trl first.

verl 2026 arc (github.com/volcengine/verl/releases, read this session): v0.9.1 (Sep
20) unified V1 trainer + idle-GPU lending + Liger fused PPO head (13.5% faster actor
updates); v0.9.0 (Aug 14) delta-sharded checkpoint weight sync (1.9-3.1x on 7B-72B -
directly the LoRA-hot-swap class aTTT relies on), uni-agent reference stack for
long-horizon agent RL; v0.8.0 (Jun 1) on-policy distillation e2e + SGLang LoRA rollout
support; v0.7.0 (Jan 5) Megatron-Bridge LoRA/PEFT "trillion-param RL with 10% GPUs".
Verdict: verl is the reference for the multi-node agent-RL shape the estate does NOT
have hardware for, but its uni-agent stack + async rollout design is the map to steal
for a single-box async loop. Clone second, read not run.

deep-rl-class (huggingface, read this session): repo self-describes as "now in a
low-maintenance state", Unit 7 AI-vs-AI broken, leaderboard dead, 93 open issues.
Still fine as free theory reading (classic RL, not LLM post-training), but it is NOT
a 2026-relevant shelf; do not spend clone budget ahead of trl/verl/vllm.

### RQ4: cost points for the ASTRA-class context-to-weight door

DPPM (2610.11776) is the strongest published instance of the door the living-weights
rib names: a frozen hypernetwork (Doc-to-LoRA compiler + decoder) turns cross-session
interaction history into history-conditioned LoRA adapters in a forward pass, no
per-segment optimization, backbone frozen, only lightweight memory modules trained.
Cost points on Qwen3-4B, single A800, batch 1: answer-stage latency 46.14 ms (+2.43
ms over RPMem), 3.1x faster than RAG and 62.7x faster than Full Context; peak memory
7,762 MiB flat vs Full Context 10,204 to 18,246 MiB as history grows 33k to 139k
tokens (57.46% less at the long end). Accuracy: 54.22% PersonaMem-v2 (+21.26 over the
best textual baseline, Full Context), 86.79% PrefEval (+11.30 over Mem0). So YES - at
personalization-session scale, compiled-to-weights now beats both prompt-stuffing and
retrieval-based memory on accuracy AND latency AND memory. The family has names worth
grepping later: Doc-to-LoRA, PLUME, RPMem, delta-mem, Metis.

DIAL-OPD (2610.11659) sets the distillation cost point: in on-policy distillation,
supervising FEWER tokens wins - retaining 40% of tokens beats full-token OPD by up to
5.25 points mean accuracy and doubles AIME25 Pass@16 (13.33% to 26.67%); at matched
retention +18% over the best selection baseline; a 4B teacher with selection beats an
8B teacher without, by up to 1.76 points - "effective supervision allocation can
outweigh teacher scaling." Random 80% retention already beats 100% on a 0.6B student
(+8.2 MATH-500). Mechanism: low-low tokens (both models assign ~1e-3) soak up 49.8% of
absolute reward at 10% retention while hindering learning. Estate translation: when
distilling session lessons, select the supervision (pitfall-adjacent tokens), don't
just compress the corpus; a small local teacher with good selection beats a big dumb
one.

SGUID (2610.12367) prices the curation step: fewer than 25% of retrieved skills give
useful distillation signal; 6 selected skills match or beat full-bank (up to 11x
larger) distillation across Olmo-3-7B / Qwen3-1.7B/4B/8B; a second co-evolution round
with 3 newly selected skills takes Qwen3-8B from 64.3 to 66.3; robust across K=4-12.
All on 4x H200 with LoRA. Estate translation: the dead-salmon curation rider is not
just an honesty guard, it is the difference between a co-evolution loop that improves
round over round and one that degrades.

### Adjacent finds (abs-read, not banked as items)

- MiMo-V2.6 (2610.11959, Xiaomi): RL scaled explicitly "towards self-improvement",
  1,568 samples/step at up to 1M context, groupwise agentic grading, frozen MoE
  router, multi-layer reward-hacking defense. Frontier-scale mirror of the estate's
  verdict-driven fold; useful as the "they take reward hacking seriously at scale"
  citation.
- HarnessSQL (2610.12274): harness-native post-training (teachers roll out inside the
  target harness, verified-trajectory SFT + execution-reward RL) lifts Qwen3-8B from
  15.5 to 45.2 on Spider 2.0-SQLite. The estate analogy - train inside your own
  execution harness, not on static pairs - is direct support for fine-tuning on own
  filed traces (the MASS mechanism the rib names).
- GRPODropout (2610.11854): drop high-probability positive-advantage rollouts before
  the update to fight entropy collapse, negligible overhead. Shelf item for the
  improve lane's future GRPO use.
- Residual Advantage/CoRA (2610.11519): teacher-student probability residual as
  bounded one-step reward; teacher LoRA updated on the same scored batch - the
  "teacher that adapts to the student" pattern, Qwen3-1.7B/4B students with an 8B
  teacher.
- ZCPO (2610.12161): seven failure modes of KL regularization in group policy
  optimization - read before tuning any GRPO/KL knobs.

## What is OWED

- Agentic-TTT's cross-model-size section (3.4) was mapped by section headers but not
  line-read; its Qwen2.5-7B numbers are from the main table read in full.
- MiMo-V2.6 full text not read (abs only); its reward-hacking defense details are
  second-hand from the abstract.
- The 429 on export.arxiv.org means this sweep's query surface was listing+search
  shaped, not exhaustive API shaped; a 30-day API window query for LoRA-swap serving
  papers specifically did not run (both attempts to reach the API 429'd). The serving
  side is covered by aTTT's own system section instead.

## Overlap verdict (grep run this session against catalog/catalog.jsonl + memory/)

- 2607.03441 (aTTT) and 2510.07841 (TT-SI): zero catalog rows; the only memory/
  hits are THIS session's own trajectory steps (memory/trajectory/steps.jsonl,
  session_id sess_dwf-...actor_3_17). Genuinely new to the estate.
- 2610.12002, 2610.12367, 2610.11659, 2610.11776: one catalog row each - the
  automated daily ingest stubs at state/arxiv/2026-10-09/<id>v1.txt (title +
  authors + abstract, 1.3-2.0 KB, no analysis, no full read, no estate mapping).
  This sweep adds the full-HTML read and the law mapping; the stubs are sensing
  surface, not prior analysis.
- TRL / verl / deep-rl-class: zero catalog rows (grep "huggingface/trl",
  "volcengine/verl", "deep-rl-class"); the repos are named only in the
  corpus/CURRICULUM.md:85-89 clone queue, which is the ask's own pointer.

## Verbatim quotes banked per item (source: arxiv abs page fetched this session)

See items in the submitted SweepResult; quotes verified against `_ft_*.html` /
`_ftread_*.txt` in this directory.

---

## AMENDMENT 2026-10-11 (verification pass, same seat lineage, session sess_dwf-...actor_3_17)

source-fetched: adhoc. This block is a claim-by-claim re-verification of the 2026-10-10
sweep above by the resubmitted seat, run before the SweepResult landed. The original
bytes above are untouched; everything below was re-read from the banked `_ftread_*.txt`
/ `_ft_*.html` / `_ft_trl_releases.json` / `_ft_verl_releases.json` / `_ft_drl_readme.md`
artifacts in this directory this sitting, plus live door checks.

### Door state today (2026-10-11)

- Live WebFetch of arxiv.org/abs/2607.03441: title "No Time Like the Present: Agentic
  Test-Time Training for LLM Agents", submitted Fri 3 Jul 2026, abstract fragments
  ("revisit explored states, repeat failed actions") byte-match `_ftread_2607.03441.txt:109`.
- Live WebFetch of arxiv.org/abs/2610.12002: title "Agentic-TTT: Training test-time
  policy for test-time training", submitted 8 Oct 2026, abstract sentence "Agentic-TTT
  turns TTT procedures into callable tools" byte-matches `_ftread_2610.12002.txt:145`.
- The export.arxiv.org API 429 named at the top of this file has CLEARED: one Atom
  query (test-time training + LoRA, 15 results, sorted by submittedDate desc) returned
  14 entries. The 10-10 OWED item "30-day API window query for LoRA-swap serving
  papers" is therefore partially discharged; fresh find from that probe below.

### Claim-by-claim verification (all line cites are into this directory's files)

- aTTT 2607.03441: VERIFIED. vLLM runtime LoRA API + 16 concurrent episodes + 1.9x
  wall-clock (`_ftread_2607.03441.txt:312`); hot-swap under 100 ms, dedicated training
  GPUs, non-blocking (`:802`); K=5 cadence, adapter persists within episode, resets
  between episodes (`:308`, `:834`); "mainly preserves existing competence" (`:109`);
  in-context 49.3% < no-TTT 50.7% < adapter 54.3% with matched Summary text (`:510`);
  repetition >80% and 26.3 steps vs 50-step budget (`:419`); Qwen3.5-4B 1.9 -> 3.6
  (Self block) vs 9B 50.7 -> 55.7 (Table 1, `:324-348`).
- Agentic-TTT 2610.12002: VERIFIED. 0.256 -> 0.510, prompted 0.271, embedding-router
  0.347 (`_ftread_2610.12002.txt:680-688`); compute penalty lambda 0 -> 0.4 raises
  direct-answer rate 11.8% -> 39.8%, compute 1375.5 -> 886.9 (-35.5%) (`:752-757`);
  moderate penalties cut ~30% compute with HIGHER utility, "the policy may overuse
  TTT" (`:759-763`); 176 held-out scored queries (`:464`); Qwen2.5-7B-Instruct
  (`:478`); 5 TTT methods PoT/TTT-FS/TTRL/SEAL/TLM as callable tools (`:480-484`);
  re-adapt refused until N NEW samples accumulate, warm-started (`:2427`, `:2431`);
  help-to-harm 20:1 and 100 skill-reuse answers (`:703-713`).
- TT-SI 2510.07841: VERIFIED. +5.48% avg with per-benchmark deltas (`_ftread_
  2510.07841.txt:106`); 190 uncertain cases + 1 synthetic each beat 13k-sample SFT
  72.43% vs 70.20%, ~68x fewer samples (`:475`); ICL variant 66.37 -> 68.36 vs
  standard ICL 67.74 (`:478`); Qwen2.5-1.5B +5.76 (66.67 -> 72.43) vs 7B +3.02
  (80.95 -> 83.97) (`:539`); gpt-5-mini TT-D adds +0.94/+1.68/+2.65 (`:472`); single
  A40, LoRA/PEFT (`:376`, `:571`); bounded by base capacity, absent knowledge needs
  retrieval (`:563`). CORRECTION: the 10-10 body's "(ACL 2026 Findings)" venue tag is
  NOT in the fetched bytes (grep ACL/Findings: no venue string) - venue withdrawn, id
  2510.07841v1 cs.LG 09 Oct 2025 (`:77`) stands on its own.
- DPPM 2610.11776: VERIFIED. 46.14 ms answer latency (+2.43 over RPMem), 3.1x faster
  than RAG, 62.7x faster than Full Context (`_ftread_2610.11776.txt:680`); peak
  memory 7,762.32 MiB flat vs Full Context 10,203.91 -> 18,245.97 MiB as history
  grows 33,143 -> 139,319 tokens, 57.46% less (`:682`); Qwen3-4B, one A800, batch 1
  (`:686`); 54.22% PersonaMem-v2 (+21.26 over Full Context) and 86.79% PrefEval
  (+11.30 over Mem0) (`:144`, `:636`); frozen Doc-to-LoRA compiler + decoder, only
  lightweight memory modules trained (`:161`); family names D2L/PLUME/RPMem/
  delta-mem/Metis (`:325`).
- DIAL-OPD 2610.11659: VERIFIED. 40% retention beats Vanilla OPD and full-token
  variants by up to 5.25 pts, doubles AIME25 Pass@16 13.33% -> 26.67% (`_ftread_
  2610.11659.txt:134`, `:153`); up to 18% relative over strongest token-selection
  baseline at matched retention (`:134`); 4B teacher with selection beats 8B-teacher
  full-token by up to 1.76 ("effective supervision allocation can outweigh teacher
  scaling", `:72`, `:135`, `:153`); random 80% retention beats 100% on the 0.6B
  student 38.4% vs 30.2% MATH-500 (+8.2, `:183`); low-low tokens are 20.6% of
  selected tokens at 10% retention but 49.8% of total absolute reward (`:149`,
  `:213`).
- SGUID 2610.12367: VERIFIED. Fewer than 25% of retrieved skills produce active
  verifier-aligned distillation signal (`_ftread_2610.12367.txt:656`); 6 selected
  skills match/exceed full banks up to 11x larger on 3 of 4 models, all 4 after a
  second 3-skill round (`:108`, `:125`); round 2 takes Qwen3-8B 64.3 -> 66.3
  (`:109`, `:135`); naive unfiltered update on Qwen3-4B drops HMMT25 0.3 below base
  while SGUID adds +0.5 then +1.1 (`:109`); full-bank co-evolution decays +2.1 ->
  +1.6 while selected holds +3.0 -> +3.1 (`:536`, `:656`); K=4/6/12 robust, K=2
  fails (`:596`); 4x H200, LoRA (`:471`).
- TRL releases (`_ft_trl_releases.json`, 5 releases read): VERIFIED. v1.15.0
  (2026-10-08) fused Triton LM head "up to 6.9x longer sequences on the same GPU",
  peak memory drops 52% to 82% at 8,192 tokens, SFT/DPO/KTO/GRPO/RLOO/Distillation,
  gain largest for small models with large vocabularies; v1.14.2 (2026-10-06) "Patch
  release fixing two cases of silently wrong training", #7505: "Models that end a
  turn with an id only their generation config declares (Gemma 3/4, Phi-3.5, ...)
  did not stop at the end of the turn, and everything generated after it was trained
  on" - the gemma-janitor tripwire; v1.14.0 (2026-09-25) chunked logprobs + fused
  Triton logprob/entropy kernel, six experimental trainers removed; v1.13.0
  (2026-09-10) PPO removed, Qwen3-8B 1,048,576-token recipe 380 s/step 56.2 GB/GPU,
  tensor-core chunked lm_head (gemma-3-270m vocab 262k 1.32x). The "big win for
  small models with large vocabs" phrasing is the release's own.
- verl releases (`_ft_verl_releases.json`, 4 releases read: v0.9.1 2026-09-20,
  v0.9.0 2026-08-14, v0.8.0 2026-06-01, v0.7.1 2026-03-16): v0.9.1 idle-GPU lending
  + Liger fused PPO head "13.5% faster actor" VERIFIED; v0.9.0 delta_sharded
  "2.4x at Qwen2.5-7B, 1.9x at 32B, 3.1x at 72B" + uni-agent reference stack for
  long-horizon agent RL ("bring any harness") VERIFIED; v0.8.0 on-policy
  distillation e2e + SGLang LoRA rollout work VERIFIED. CORRECTION: the 10-10 body's
  "v0.7.0 (Jan 5) Megatron-Bridge LoRA/PEFT 'trillion-param RL with 10% GPUs'" is
  NOT byte-backed in the banked artifact (banked v0.7.1 is dated 2026-03-16 and no
  "10% GPUs" string exists in any banked release body). Verified instead: v0.7.1
  body carries the Megatron-Bridge LoRA enhancements (actor/ref share, LoRA-adapter-
  only refit, LoRA FP16 with Megatron-Bridge). The Jan-5 claim is struck; not owed,
  it changes no verdict.
- deep-rl-class (`_ft_drl_readme.md`, read in full): "low-maintenance state", "Unit
  7 (AI vs AI): This feature is currently non-functional", "The leaderboard is no
  longer operational" - all verbatim. The 10-10 body's "93 open issues" is NOT in
  the banked readme bytes (it would have been a repo-page count) - struck.

### Overlap greps re-run this sitting (2026-10-11, burns-law 5.3 shape)

Instrument: grep -c / python jsonl scan over catalog/catalog.jsonl (1.1M rows),
recursive grep over memory/, and grep over watch/inbox/frontier_olm_adhoc/register.jsonl.

- 2607.03441: catalog 3 rows = this sweep's own `_ft*` artifacts only; memory/ hit =
  memory/trajectory/steps.jsonl (this session lineage's steps); register.jsonl 2
  mentions (the 10-11 adhoc-fold sensing rows, title-grade). No prior analysis
  anywhere. Genuinely new as a read.
- 2610.12002 / 2610.11776 / 2610.11659 / 2610.12367: same shape plus one
  state/arxiv/2026-10-09/<id>v1.txt ingest stub each (1,279-1,456 bytes, title +
  authors + abstract, no analysis). The sweep's full-HTML reads are the estate's
  first. Register sensing rows: 2 mentions each.
- 2510.07841 (TT-SI): ZERO prior rows - no catalog row, no register mention, no
  state/arxiv stub, memory/ only this lineage's trajectory steps. The one item that
  is new even at sensing grade.
- huggingface/trl, volcengine/verl, verl-project/verl, deep-rl-class: ZERO catalog
  rows each (grep of all four strings). Named only in corpus/CURRICULUM.md:85-89
  (the clone queue, the ask's own pointer) and, for deep-rl-class, nothing in
  memory/rib/.

### Fresh find from the recovered API door (abs-read only, NOT deep-read; candidate for the next sweep)

- ASCENT 2610.05303, "Online Test-Time Training of Long-Horizon Agents via
  Self-Distillation of Verified Experience", submitted 4 Oct 2026 (live fetch this
  sitting). Abs quote: "We introduce ASCENT (Agentic Self-distillation for
  Cross-task EvolutioN at Test-time), which instead self-distills verified"
  [experience rather than imitating or reinforcing the single attempt's tokens];
  "ASCENT improves task success and interaction efficiency as experience
  accumulates, outperforms online adaptation methods" on ALFWorld, WebShop,
  AppWorld. This is the estate's verdict-driven-fold shape (verified experience,
  not raw rollouts) published as online TTT - the strongest RQ1/RQ4 candidate the
  10-10 pass missed. OWED to the next sweep: full-HTML read.

### What remains OWED after this amendment

- The OWED list of the 10-10 body stands except: the API 429 item is discharged
  (door verified working today; one 30-day query run), and the TT-SI venue +
  verl v0.7.0 + deep-rl "93 issues" items are resolved as corrections above.
- Agentic-TTT section 3.4 (cross-model-size) still not line-read (unchanged OWED).
- ASCENT 2610.05303 full read (new OWED above).
- RDNA1-specific check: NONE of the six deep-read papers ran on AMD hardware or
  sub-4B models through a local serving stack; the RQ1 "what can gemma:2b absorb on
  THIS box" question stays an estate-measured question. Published evidence bounds it
  (aTTT smallest model gains least; TT-SI 1.5B gains most of anyone tested) but
  cannot answer it. Not fabrication: named as unmeasured.
