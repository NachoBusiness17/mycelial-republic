# STEAL CARD: inference-efficiency via arxiv (round 1, 2026-10-04)

Find: arXiv:2610.00694, "How Divergence Becomes Decision Flips in Compressed Language Models"
(title ask-carried; abs page https://arxiv.org/abs/2610.00694). NEW to estate: dedupe re-run
by this ask's own greps (checks section below). Sole prior mention anywhere on the box is the
10-03 pass-1 feed listing (watch/inbox/frontier_olm_2026-10-03/sweep/inference-efficiency-arxiv.md:41),
never in any bank list. Source sweep: watch/inbox/frontier_olm_2026-10-04/sweep/inference-efficiency-arxiv.md
(banked item 1 at :162-163, instrument note :110-113, dedupe ledger :130-131).

## The mechanism (verified this ask, not just ask-carried)

Total variation measured under teacher forcing between a compressed copy and its root predicts
greedy decision flips AND vLLM greedy draft acceptance at 1.1-2.4 percent mean relative error,
with NO task-specific calibration (the thing KL needs). Empirical spine: flip-rate/TV ratio,
median 1.05, constant-free, across 802 compressed copies of 19 open models. Verified against
the live abs page 2026-10-04 via WebFetch: the abstract reads back 1.1-2.4 percent, median 1.05,
802 copies, 19 open models, five corpora, nine perturbation families. The ask's verbatim quote
is the abstract's own claim.

Why this is a steal and not genre: every quant gate the estate runs today burns generation
passes (bench tokens_per_sec, the 15-task smoke, needle banks). TV is measurable WITHOUT
generation: teacher-forced logits over one fixed chunk, a few thousand forward passes. If the
constant-free 1.05 ratio holds at janitor scale, TV becomes a PRE-GATE: measure first, burn
eval passes only on candidates that survive.

## Estate map (organ -> concrete port move)

1. QUANT LANE ACCEPTANCE GATE (primary organ). Contract in force: Q4_K_M floor plus a 15-task
   smoke scored against the same-family high-precision baseline
   (watch/inbox/frontier_olm_2026-09-30/sweep/quantization-compression-arxiv.md:58-60),
   recall-shaped per the 10-02 card
   (watch/inbox/frontier_olm_2026-10-02/steal/quantization-compression-arxiv.md:27-29).
   Port move: TV-flip pre-screen IN FRONT of the smoke. Teacher-force a fixed probe chunk
   through the candidate quant and the f16 root, compute TV, predict flip count at the
   constant-free ratio ~1.05; candidates whose predicted flips exceed the gate's flip budget
   never reach the 15-task smoke. The smoke stays the final acceptance: instruments-only law
   (cited by the sibling sweep at :151-152), paper numbers are prioritization evidence until
   estate-measured.
2. GOPHER FLEET / desk A/B probe. mag/desk_model_probe.py:189-199 picks the desk winner on raw
   tokens_per_sec, then elapsed_ms, then gpu_pct; quality is invisible to the ranking. Port
   move: emit tv_vs_root and predicted_flips per candidate into the route_decision join (the
   join already tags hardware RX5600XT_6GB at mag/desk_model_probe.py:219), so a fast quant
   that silently moved the most decisions can no longer win on speed alone.
3. GPU LADDER RIB. memory/rib/RIB_GPU_LADDER_20261001.md:17-18 keeps the quant lane (GGUF on
   current box) "winning per dollar"; :30-31 records the standing correction "gemma:2b was
   Q4_0, pulls ordered 2026-10-01". Port move: TV gives that lane a dollar-free quality meter
   for exactly those pending corrections; each re-pull scores TV-vs-root before any bench.
4. ANALOGY ONLY, labeled per the estate convention
   (watch/inbox/frontier_olm_2026-09-30/steal/quantization-compression.md:46, applied again in
   the 10-01 percolator row, watch/inbox/frontier_olm_2026-10-01/percolator_candidates.jsonl
   fifth row): mag/auto_quantize.py:21-24 (L0-L5 analytics ladder, "Anomalies are NEVER
   quantized") and mag/state_quantizer.py are state quantizers, not model quants. No port
   claimed there.
5. SOVEREIGN MIRROR / spec-dec half: the paper's 1.1-2.4 percent draft-acceptance number is a
   vLLM result; estate janitors are Ollama/llama.cpp with no surfaced draft-acceptance
   plumbing. Recorded as genre, no port, until a llama.cpp speculative draft pairing exists.
   This is assessment, not measurement: I did not verify vLLM/llama.cpp parity in depth.
6. Percolator: bank the instrument as a candidate row only after the probe below lands an
   estate number; not banked as truth now.

## Falsifiable probe (cheap, this week, on-box; not executed this ask)

Arms: the served gemma:2b Q4_0 blob (identity per memory/rib/RIB_GPU_LADDER_20261001.md:30;
manifest present on box, ollama manifests read this ask, model-layer digest re-check OWED)
against the same weights' f16 root (one pull if no f16 root is already on disk: OWED, not
verified), plus an on-disk llama-quantize.exe Q8_0 arm built from that root as the second
point. Instruments verified on disk this ask: tools/llamacpp/llama-perplexity.exe and
llama-quantize.exe (ls output in checks). Method: dump per-token logits for both arms over one
fixed ~20K-token wiki chunk, compute TV = 0.5*sum|p_root - p_quant| per position in a small
python diff script, count greedy-argmax flips on the same positions. Prediction (constant-free
transfer): flip_rate/TV lands near the paper's median ratio 1.05 on BOTH arms; pre-registered
accept band 0.7-1.4. Falsifier: either arm's ratio lands outside the band (a fitted constant
would be needed and the pre-gate dies), or TV reads small while the existing 20-prompt needle
bank instrument (memory/percolator/candidates.jsonl:11 lineage) still flips 2+/20 on the Q4_0
janitor, meaning TV misses decision damage at 2B/Q4_0 and the 15-task smoke stays the only
gate. Cost: at most one 4-5 GB f16 pull, two llama.cpp logit passes, one python script; CPU
offpeak, zero paid tokens.

## Checks run this ask

1. Dedupe re-run (my own commands, not inherited):
   `git grep --no-index -n "2610.00694" catalog memory docs state watch` -> hits ONLY at
   watch/inbox/frontier_olm_2026-10-03/sweep/inference-efficiency-arxiv.md:41 (the 10-03
   pass-1 feed listing, unbanked), the 10-04 sibling sweep's own analysis lines (:19, :43,
   :55, :110, :130, :162), and memory/trajectory/steps.jsonl echoes of the sweep session's
   own commands (session log, not bank content). catalog/ and every other memory/ dir: zero
   hits. `git grep --no-index -n -i "Divergence Becomes Decision Flips" catalog memory docs
   state watch` -> zero hits. NEW confirmed.
2. Abstract verification: WebFetch of https://arxiv.org/abs/2610.00694 (2026-10-04) read back
   1.1-2.4 percent MRE, median ratio 1.05, 802 compressed copies, 19 open models. Ask quote
   matches the abstract's claim.
3. Organ reads: mag/desk_model_probe.py:170-237 (ranking at :189-199, hardware tag :219);
   memory/rib/RIB_GPU_LADDER_20261001.md:1-31; watch/inbox/frontier_olm_2026-09-30/sweep/
   quantization-compression-arxiv.md:50-67; mag/auto_quantize.py:14-25; 10-02 steal card
   :27-29; 10-04 sibling sweep :100-174; 09-30 steal card :40-50 (analogy convention).
4. Tool presence: `ls tools/llamacpp | grep -iE "perplexity|quantize|bench|llama-"` ->
   llama-perplexity.exe and llama-quantize.exe present (plus llama-bench.exe, llama-cli.exe,
   llama-server.exe).
5. On-box root: ollama manifests listing read this ask shows gemma, gemma2, gemma4,
   gemma4-desk present under ~/.ollama/models/manifests/registry.ollama.ai/library/.

## OWED / not run

- The probe above: NOT fired; zero models were run this ask.
- f16 root of gemma:2b already on disk: not verified.
- Exact logit-dump flags the on-disk llama.cpp build supports: not verified.
- gemma:2b model-layer digest re-check (the b50d6c999e59 identity): not run; only manifest
  presence confirmed (config digest sha256:887433b8...).
- lens/laws.md:31 (instruments-only law) is cited secondhand from the sibling sweep
  (watch/inbox/frontier_olm_2026-10-04/sweep/inference-efficiency-arxiv.md:151-152);
  lens/laws.md is not in the tracked tree this ask (`git ls-files | grep -i lens` returns no
  such path), so the law is cited via the sibling, not the file.
- vLLM draft-acceptance transfer to llama.cpp: unassessed in depth; genre until measured.
