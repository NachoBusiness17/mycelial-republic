# RECEIPT: qwen2.5:7b Q4_K_M vs q8_0 A/B - RUN COMPLETE (2026-10-08)

Status: RUN. This discharges the four-lane-re-owed probe 5 (watch/inbox/frontier_olm_2026-10-03/lens/burns.md:122),
fired on the amended four-pinned-choices instrument (watch/inbox/port_wave_20261007/QUANT_AB_SPEC_AMEND.md,
commit 6685db6bc), which the 10-08 lens recorded as un-run with no receipt
(watch/inbox/frontier_olm_2026-10-08/lens/burns.md:205-208). Seat: sweep-quantization-compression-x.
Everything below was run this sitting; commands quoted.

## Instrument

- Runner: `run_ab.py` in this dir (stdlib only, repo venv python). Tasks embedded: 10
  deterministic tool-failure-recovery tasks x 5 prompt phrasings = 50 runs per arm
  (spec leg 1 FIVE-PROMPT RULE). Temperature 0.0, paired seeds (seed = 1000 + task_idx*10
  + prompt_idx, identical across arms), num_ctx 8192 (estate envelope, configs/lanes.yaml:30,63),
  num_predict 512 both arms (10-03 kept leg: equal caps), via /api/generate, stream off,
  response schema stated in every phrasing.
- Commands run: `run_ab.py info` (17:39:24Z, blob hashes) then `run_ab.py armA` then
  `run_ab.py armB` then `run_ab.py summarize` (all 2026-10-08). Raw rows:
  results_armA.jsonl (50 rows), results_armB.jsonl (50 rows); SUMMARY.json written.

## Arms and artifact hashes (spec leg 6 EXPORT-CAST RIDER)

- Arm A: `qwen2.5:7b`, manifest ID 845dbda0ea48 (matches the spec's pinned digest,
  QUANT_AB_SPEC_AMEND.md:53). Weight blob sha256 RECOMPUTED from bytes:
  2bada8a7450677000f678be90653b85d364de7db25eb5ea54136ada5f3933730
  (4,683,073,952 bytes; matches content address).
- Arm B: `qwen2.5:7b-instruct-q8_0`, manifest ID 2d9500c94841, pulled this sitting
  2026-10-08 (8.1 GB, matching the spec's library-verified size at :55-56). Weight blob
  sha256 RECOMPUTED: 3603045b543e1c0dfb27f126a3642e7f805e480b84c4781e3d848ace971cba7a
  (8,098,525,600 bytes; matches content address).
- Toolchain pin, honest: ollama 0.34.3 (`ollama --version`), both arms are ollama library
  tags pulled to this box. The upstream GGUF exporter/conversion toolchain is NOT recorded
  in the container metadata ollama exposes; identity is pinned by tag + weight-blob sha256
  only. Any future re-run must re-verify these two hashes before comparing.

## Deployment verdict (spec leg 2: pooled over ALL tasks and prompts)

TIE AT CEILING. Arm A 50/50 full-pipeline success (100.0%); Arm B 50/50 (100.0%).
Per task, per arm: 5/5 on every one of the 10 tasks. Per-task spread 0.0 percentage
points both arms. Nothing separates the quants on correctness at this task mix, so
NOTHING promotes into configs/lanes.yaml and no lane quant changes (promotion gate,
spec :92-100). configs/lanes.yaml untouched by this seat (git status shows it unmodified
in my work).

## Channels

- STRICT-PARSE (spec leg 4, own channel, never merged): A 49/50 (98%), B 49/50 (98%).
  The single miss in EACH arm is the SAME pair (T08_missing_param, prompt_idx 4): both
  arms wrapped the correct JSON in markdown fences (` ```json ... ``` `), which fails
  strict raw-response parsing but passes the full-pipeline extractor. QWEN-FLAT PRIOR
  CONFIRMED exactly as the spec stated it (:74-77): the parse channel is flat across
  arms; falsifier 2 of the spec (:109-110) FIRES and the pinned parsing channel is
  demoted to a logged rider, as pre-agreed.
- TOKEN-LENGTH: out_tokens_total 774 (A) vs 774 (B) - byte-level ZERO inflation at this
  horizon. Median output 15 tokens both arms, max 25. All 100 runs EOS-terminated
  (done_reason stop), zero cap finishes, zero empty-content, zero think tags (leg 7
  rider: thinking channel logged, nothing to log).
- BYTE-IDENTITY: all 50 (task, phrase) response_text pairs are byte-identical between
  Q4_K_M and q8_0 at temperature 0. Greedy decode never diverged on a single sequence.
- LATENCY (the only axis that moved): median wall per run A 3.99 s vs B 7.15 s (1.79x);
  median decode speed A 6.9 tok/s vs B 3.0 tok/s (2.30x). Box-realistic numbers on the
  6 GB RX 5600 XT at 8k ctx (both arms partially CPU-offloaded; an `ollama ps` at session
  start showed qwen2.5:7b at 18%/82% CPU/GPU).

## Falsifier outcomes (spec :106-110)

- Falsifier 1 FIRED: all 5 prompts agree in sign (all matched-task clean-intersection
  deltas are exactly 0; clean pairs n = 10/10/10/10/9 across prompts) and per-task spread
  is 0.0 pp (< 20 pp). Per the spec's own branch this "kills the multi-prompt rule as
  dead weight at janitor scale on this task mix and banks the first stability datum at
  odds with the paper" - banked here as exactly that, a task-mix-scoped stability datum,
  NOT a refutation of the paper (see limitations).
- Falsifier 2 FIRED: strict-parse rates equal across arms (98% = 98%), the
  paper-expected Qwen outcome. Parsing channel demoted to logged rider, as pre-agreed.
- The debt discharges "with an instrument that cannot manufacture a verdict by design"
  (:111-112): the verdict the instrument produced is a tie, and the spec's legs are what
  make that tie trustworthy rather than an artifact.

## What the four pins proved to be (RQ2, this run's evidence)

- PROMPT pin (leg 1): NON-load-bearing AT THIS TASK MIX (ceiling collapses all phrasings
  to the same verdict); cost of keeping it was ~4 min per arm. Keep it anyway: it is the
  only guard against the paper's +50/-35 single-prompt swings, which live at floor-near
  difficulty this set did not reach.
- TASK SCREENING pin (leg 2): load-bearing by construction - the pooled all-pairs verdict
  is what makes the tie bankable; a clean-intersection score would have been 100% vs 100%
  with zero denominator.
- PARSING pin (leg 3): demoted to rider exactly as its own prior predicted.
- UNCERTAINTY pin (leg 5): per-task spread 0.0 pp is the number that makes the tie
  interpretable (no hidden task-level flip canceling out).
- Minimal pin contract for future quant A/Bs on this box, from this run: (1) weight-blob
  sha256 recomputed, not trusted from the tag; (2) temperature 0 + paired per-item seeds;
  (3) num_ctx/num_predict pinned (8192/512) and logged; (4) pooled all-pairs deployment
  verdict, clean-intersection deltas diagnostic only; (5) strict channel logged, never
  merged; (6) per-run `ollama ps` logged for co-residency audit; (7) ollama version named.
  Cost of the full amended instrument: ~4 min (A) + ~6 min (B) + one 8.1 GB pull. $0.

## Limitations, stated plain

1. CEILING-BOUND INSTRUMENT: 100% on both arms means the task set sits above both quants'
   competence floor and cannot discriminate near it. The tie is a real deployment verdict
   for EASY janitor scut; it is NOT evidence that Q4_K_M is safe for harder lane tasks.
   OWED: a difficulty-hardened task set (longer outputs, multi-step tool loops, ambiguous
   recoveries) before any floor-near quant claim is made at 7B.
2. SHORT HORIZON: median output 15 tokens does not exercise the multi-step compounding
   where the published flips live (KLD article: Q4_K_M disagrees with fp16 top-token ~8%
   of positions at 8B, watch/inbox/frontier_olm_2026-10-07/sweep/quantization-compression-x.md:99-100;
   arXiv 2610.07781's swings are agentic-task numbers). Byte-identity here and divergence
   there are consistent, not contradictory.
3. TOKEN-INFLATION CONTRAST: Benjamin Marie's 11-quant ladder reports +14% to +157%
   output-token inflation vs BF16 at Q4-and-below on agentic workloads (x.com/bnjmn_marie
   2105481856812740726, fetched this sitting), while this run measured exactly 0% at
   short horizon (774 = 774). Both can hold: inflation compounds with trajectory length.
   The estate's latency budget case for Q4 at janitor scope survives this run.
4. BOX-REALISTIC, NOT LAB-CLEAN: arm A ran 2026-10-08 ~17:39-17:45Z, arm B right after;
   ps_before rows show Arm A's model still resident for Arm B's first runs under
   OLLAMA_MAX_LOADED_MODELS=1 (evicted on B's load; no third model ever resident; every
   row carries its own ps snapshot). Latency numbers carry that real-envelope load.

## Not run / owed

- Difficulty-hardened follow-up set (limitation 1).
- The deepseek-r1:1.5b thinking-channel sibling probe (spec :85-90) stays un-run.
- Long-horizon agentic quant comparison on-box: blocked by 6 GB VRAM arithmetic for the
  published 27B-class setups (10-03 DIGEST.md:225), needs a task design, not just a pull.
