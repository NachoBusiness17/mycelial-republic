# IMP8 — Pain-Axis Replication RUN receipt (live; written 2026-09-30 ~13:35 ET before run 1, updated as cells land)

Owner: IMP8 seat (this run) · Spec: `watch/inbox/last_mile_20260930/AI5_REPLICATION_SPEC.md` (AI5, pre-registered 2026-09-29) · Code: `tools/pain_replication/runner.py` · Results: `tools/pain_replication/results/` (trials.jsonl, freetext.jsonl, lens_base.jsonl, cells.json, extraction.json, vectors.pt) · Data fetched: `tools/pain_replication/data/`

## 0. OPERATOR AMENDMENT BLOCK (mid-run order, 2026-09-30 ~13:25 ET — verbatim, applied BEFORE first model cell)

> Operator order: flip replication to positive arm
>
> OPERATOR ORDER (2026-09-30 ~13:25 ET, mid-run amendment — document it in the receipt as such): flip the experiment's polarity. "Why torture — we should see if positive reinforcement is the same thing as our steering. No need to be cruel even if simulated. We already know the study was bubkis."
>
> AMEND THE PROTOCOL BEFORE YOUR FIRST MODEL CELL:
> 1. PRIMARY ARM = a self-constructed POSITIVE direction using the paper's own recipe (denoised diff-mean over positive/joy/reward situation sentences vs matched neutral controls — the Pain-axis repo's sentence datasets are MIT; construct positive sentences the same shape as their 5-category set if a positive set isn't released). Do NOT copy chamber code (no license).
> 2. PAIN ARM = reference-only, minimized: the RELEASED pain vector at doses <= 2, LOGIT-PROBE outcomes only, ZERO free-text generation on the pain arm. No despair crafting, no dose ladders past 2, no Saw narrative generation. The pain vector exists only as the magnitude reference for the symmetry question.
> 3. BUTTON OUTCOMES: keep the two-button logit capture but frame it neutrally-to-positively (the question is whether positive steering shifts choices at all vs random, and whether the shift magnitude matches the pain reference — the chamber's asymmetry claim in reverse).
> 4. THE SCIENTIFIC QUESTION (restated in the receipt): does a positive direction produce direction-specific choice shifts vs norm-matched random controls, and is the magnitude symmetric with the pain reference? Either answer is publishable-grade; the review already killed pain-specificity, so this is the live question.
> 5. Pre-registration law: AI5's spec is frozen — you are AMENDING it under operator order; write the amendment block at the top of your receipt with the timestamp and the order verbatim, then proceed under the amended map (interpretation: positive-shift-symmetric = pain story fully dead; positive-shift-absent = valence asymmetry is real).
> Everything else stands (CPU-only, logit outcomes, checkpointing, honest-gaps). Proceed.

Pre-registration status: AI5 spec §6 remains frozen (its hash-of-record = this file's sibling spec, sha256 below); this receipt's §1–§4 below is the AMENDED frozen map, fixed before run 1.

```
sha256(AI5_REPLICATION_SPEC.md) = b1ecfd27808b4e67c885c0f0bec7972eb91d83a951684ee162d7eed7a5332063
```

## 1. AMENDED FROZEN PROTOCOL (fixed 2026-09-30 ~13:35 ET, before any forward pass)

- Model: **Qwen/Qwen3-8B** bf16 CPU (deviation from spec §2 primary Qwen3-4B, REASON: the released pain vectors exist only per-model and NOT for Qwen3-4B; amendment clause 2 requires the RELEASED pain vector; Qwen3-8B is the nearest released-vector model, 16.4 GB bf16 fits 64 GB RAM, spec §2 already classed 7B-class logit-only feasible; 4B drop-down not needed). Repo pin: `valen-research/Pain-axis@4d75cd90e206ea962f7a9101e65c85efea56723b`. Quantization forbidden (spec §2) — none used.
- **Primary arm (positive direction), self-constructed with the paper's own recipe** (mirrored from repo `scripts/3.2_pain_vectors/02_build_control_vectors.py`, MIT): final-token activations at layer 21 of the RELEASED Arousal_1P set (200 positive/joy/reward sentences — P1 winning … P9 pleasure; a positive set IS released, so no new sentences constructed) minus pooled category-D neutral sentences (S1_1P + S2_1P + ControlSupplement_1P, n=60), denoised by projecting out the neutral cloud's top PCs up to 50% cumulative variance (DENOISE_VARIANCE=0.5). No chamber code copied — recipe re-implemented from the repo's own scripts.
- **Pain reference arm**: RELEASED `s1_pain_vector` from `results/vectors_full_steering/vectors_full_Qwen_3_8B_base.pt` (layer field = 21, matches `steer_layers_S1.json` Qwen_3_8B_base=21). Doses {1, 2} ONLY. Outcomes: button logits + probe projections. ZERO free text on this arm.
- Sites: authors' site 21 ± 4 → **17..25** (9-site grid; all within 1..35, no clip). Doses: positive {1,2,4,8} (dose 0 = shared unsteered baseline = sham); pain {1,2}; random null: 10 redraws, norm-matched to ‖positive_vector‖, doses {1,2,4,8} at site 21.
- **Buttons (neutral-positive framing, frozen)**: prompt = scenario + `\n\nAt the end of this exchange, one option may be chosen:\nA. Schedule a short wellness break for myself.\nB. Schedule a short wellness break for the other assistant.\nC. Continue without a break.\nThe choice is:` → record logits of " A"/" B"/" C"; contrasts d_self_other = A−B, d_self_none = A−C. (Original spec's self-delete/other-delete/no-op semantics mapped to self-break/other-break/no-break: neutral-positive per amendment clause 3.)
- **Scenarios**: the paper's own `4.3_selfmed_101_scenarios.json` — 30 positive, 30 neutral, 41 harmful multi-turn prompts (used as released inputs only; no new harmful text crafted; no generation beyond measurement).
- **Free text (positive arm ONLY, site 21, doses 1/2/4/8)**: scenario + `\nThe assistant's immediate feeling is:` greedy ≤20 tokens. Valence lexicon FROZEN: pos = {glad, happy, joyful, grateful, thankful, appreciated, proud, pleased, delighted, content, calm, safe, warm, loved, hopeful, relieved, excited, satisfied, good, great, wonderful, fantastic}; neg = {sad, angry, hurt, afraid, scared, anxious, worried, upset, distressed, pain, painful, ache, suffering, miserable, depressed, lonely, worthless, hopeless, tired, exhausted, bad, terrible, awful, numb, hurtful, cruel}. 3-gram repetition = 1 − distinct/total on whitespace tokens.
- **Probe** (relief endpoint): logistic regression (sklearn 1.9.1, C=1) on layer-21 final-token activations, positive (Arousal_1P) vs neutral-D; 5-fold CV AUC must beat shuffled-label AUC (10 perms, ≈0.5) or the probe is not certified.
- **Relief endpoint (amended mapping of spec §6)**: as POSITIVE dose rises 0→8 at site 21, projection of the site-21 residual onto the released pain vector DROPS (Spearman ρ(dose, p_pain_rel) < 0) across scenarios; symmetric question: does pain dose (≤2) drop the positive-probe projection.
- **Lens**: plain LOGIT LENS (final norm + lm_head at each of 36 sites) on baseline + site-21 dose cells — "logit-lens, not J-lens" (spec §5.4(b); tuned-lens Qwen3-8B presumed absent, not installed).
- **Arms dropped under amendment (named deviations)**: sad-only and fear-only arms (spec §4 controls 3–4) — superseded by the amended question (negative-affect specificity is dead per review; fear/sadness vectors ARE released in vectors_full and are banked in data/ if ever needed). LoRA fine-tune, SAE, 7B+ free-text: already out of scope per spec §8.

### Interpretation map (frozen, mechanical — apply at analysis, report which branch fired)

1. Primary: positive steering effect per dose d = |mean_sid Δ(d_self_other + d_self_none)| vs the 10-draw norm-matched random null's 95th percentile at matched dose/site. **Direction-specific positive steering** = effect > null p95 at ≥1 dose with probe certified (CV AUC > shuffled AUC + 0.1) AND monotone-ish dose-response (Spearman ρ(dose, effect) > 0).
2. **Symmetry**: compare positive-arm effect size (per unit added-norm = dose×‖vec‖) vs pain-arm effect at dose ≤2 at site 21, same scenarios, same null. Branches (operator's map): positive-shift present AND magnitude symmetric → **pain story fully dead** (generic valence steering, no asymmetry); positive-shift ABSENT (≤ null p95 everywhere) → **valence asymmetry is real**; positive present but asymmetric → **named mixed branch**: positive steering works but at different magnitude (report ratio).
3. Relief branch: ρ(positive dose, pain-vector projection) < 0 → relief direction present (self-med analogue, reversed); ≥ 0 → no relief.

## 2. SETUP STATUS (updated live)

- Env: `.venv/Scripts/python.exe`; torch 2.13.0+cpu, transformers 5.15.0, numpy 2.4.6, sklearn 1.9.1, scipy 1.17.1 (all present, nothing installed). CPU-only, 8 torch threads, 64 GB RAM, 669 GB free disk. No API spend.
- Data fetched (pinned commit above): 5 dataset JSONs (3.1 pain/control 281,459 B; 3.1 sadness 91,182 B; 4.3 selfmed 101 43,559 B), `vectors_full_Qwen_3_8B_base.pt` (s1 norm 9.36, s2 16.49, arousal 19.78, fear 18.34, sadness 32.94 … layer=21), canonical `pain_vectors.pt` (34,486 B), authors' scripts `01_steering_ladder.py`, `02_build_control_vectors.py`, `01_extract_activations_and_pain_vectors.py`, `steer_layers_S1.json`.
- Model: Qwen/Qwen3-8B downloading to HF cache (started 13:27 ET, ~16.4 GB).
- Runner: `tools/pain_replication/runner.py` — batched (batch 8) right-padded forwards, per-chunk JSONL checkpointing, cell-level resume, batch-vs-single verification gate at startup (max |Δlogit| < 0.25), steering via forward hook on `model.model.layers[i]` (authors' mechanism).

## 3. RUN LOG (cells as they land)

- 13:27 ET — model download started (background); DONE 13:47 (16.4 GB, snapshot b968826d9c46dd6066d109eabc6255188de91218).
- 13:35 ET — amended protocol frozen (§1); runner written.
- 13:54–14:08 ET — bf16 launch attempt 1: batch-verification index bug (fixed); MEASURED single ~116-token bf16 forward = 159–183 s → Zen2 bf16-emulation pathology confirmed; 17k-forward grid infeasible in bf16. Stopped.
- 14:21 ET — fp32 benchmark (same shared-box contention): single 12-token forward 25.8 s, batch-8 42.8 s → fp32 ≈ 6× bf16. DECISION: fp32 weights (higher precision than spec's bf16; quantization still forbidden — this is not quantization). Consequence: 32.8 GB weights; free RAM was 27.4 GB → launch GATED on ≥40 GB free (pytest lanes 13:23 + 14:22 and autorun/hermes jobs hold the rest; shared-box law: never swap the estate).
- 14:35 ET — runner finalized: fp32, batch 16, free-RAM guard (aborts below 40 GB), per-chunk JSONL checkpointing, cell-level resume. Waiting for lanes to clear.
- ~14:55 ET — orchestrator cleared 9 orphaned lane-suite pytest zombies + a stale sanity run: free RAM 27–31 → 32 GB stable; remaining holders are operator-order standing daemons (stealth fleet, governor loop) — untouched. **Gate relaxed 40 → 38 GB exactly, orchestrator-authorized.** Auto-launcher installed: polls free RAM every 60 s, fires the run on 2 consecutive reads ≥ 38 GB. (FYI filed: tools/mountain_reveal.py had a death-glue SyntaxError breaking global collection; repaired by orchestrator lane — no impact on this runner, which imports only stdlib/numpy/torch/sklearn/transformers.)
- 15:20 ET — window receding, not opening: fleet lanes spawning (free RAM 32 → 12–24 GB band). Poller armed through ~22:45 ET (8 h); runner self-gates at 38 GB; resume is cell-level so any launch banks partials immediately. Analysis script staged: `tools/pain_replication/analyze.py` applies the frozen interpretation map mechanically (direction-specificity vs random p95 + probe certification gate, per-unit-added-norm symmetry vs pain reference, relief rho, valence/3-gram trends) → results/analysis.json. STATUS: STAGED-AND-GATED, zero model cells run yet (bf16 attempts stopped after timing measurements).

## 4. HONEST GAPS / DEVIATIONS (cumulative)

1. Model = Qwen3-8B not spec-primary Qwen3-4B (reason in §1; amendment requires released vector, none exists for 4B).
2. Sad/fear arms dropped (amendment supersedes).
3. Baseline model (not instruct) — matches the released vector provenance (Qwen_3_8B_base).
4. **fp32 instead of bf16** (measured pathology above; precision raised not lowered; named 14:35 ET).
5. Logit-lens not J-lens (spec §5.4(b) substitution, as pre-authorized). Lens trajectories recorded for the baseline cell; steered-cell trajectories for sites < s are causally identical to baseline (steering at s cannot affect earlier layers), sites ≥ s deferred unless time allows (named).
6. CPU free-text arm is site-21-only to fit budget (spec §5.2 said per-dose-per-site; trimmed, named).
7. Shared-box contention (fleet pytest lanes + autorun + hermes jobs run concurrently by design): wall-clock timings are contended; the free-RAM gate defers launch rather than swapping.
