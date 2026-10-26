# ABLITERATION CROSS-FAMILY - research pack (curated)

Retry cleared 2026-10-01 (previous attempt blocked: ollama down; this lane had ollama 0.34.3 up).
Ask chain: watch/inbox/hermes_burn/C1_censorship_mechanisms_crossfamily.md -> C1_censorship_ASSEMBLED.md -> this pack.

Tool run (dogfood): `main.py research-pack` built pack `20261001T213210Z_abliteration-crossfamily`
(memory/research_packs/20261001T213210Z_abliteration-crossfamily.json), 3/3 sources fetched OK, freeze
bag written. The C1 ASSEMBLED file carries no URL bibliography, so the three URLs below were selected as
the canonical sources for the exact claims the C1 chain cites (Arditi et al. 2024 is named at C1
reasoning line 93; mlabonne is the technique writeup the term "abliteration" comes from; 2601.16034 is
the cross-family transfer question). This PACK.md is the hand-curated synthesis over those fetched bytes.

## Sources (fetched, local copies live)

| # | Source | Local copy | Fetched chars | Evidence class |
|---|---|---|---|---|
| 1 | arXiv 2406.11717, Arditi et al., "Refusal in Language Models Is Mediated by a Single Direction" | memory/ingest/local/web/arxiv.org-ae4bb1285386.txt | 4,905 | abstract page (peer-reviewed venue version exists) |
| 2 | mlabonne, "Uncensor any LLM with abliteration" (HF community article, 2024-06-13) | memory/ingest/local/web/huggingface.co-b6571300e6ab.txt | 33,211 | full article incl. code |
| 3 | arXiv 2601.16034, "Universal Refusal Circuits Across LLMs: Cross-Model Transfer via Trajectory Replay and Concept-Basis Reconstruction" | memory/ingest/local/web/arxiv.org-867a4bc50fe4.txt | 4,680 | abstract page, single-author preprint, UNVERIFIED beyond abstract |
| 4 | arXiv 2505.17306, "Refusal Direction is Universal Across Safety-Aligned Languages" | NOT fetched (search-result level only) | 0 | UNVERIFIED pointer |

## 1. Mechanisms (as measured in the fetched sources)

### 1.1 Refusal direction extraction
- Run the model over a harmful set and a harmless set; cache residual-stream activations at the LAST
  token position (mlabonne copy lines 64-66, 130: `pos = -1`).
- Per layer, `refusal_dir = mean(harmful) - mean(harmless)`, normalized; candidate streams are
  resid_pre / resid_mid / resid_post (copy lines 128-136). Candidates are then ranked and one is
  selected by generation probes (copy lines 137-144).
- Arditi et al.: across 13 open chat models up to 72B, ablating this one direction prevents refusal
  while preserving other capabilities; adding it induces refusal on harmless input; adversarial
  suffixes appear to work by suppressing the direction's propagation (abstract, source 1).
- Layer and position are selected PER MODEL by search. No source claims a fixed relative depth across
  families; the "40-70% depth" figure circulating in the estate chain is folklore (uncited).

### 1.2 Removal mechanisms
- Inference-time intervention (reversible): for every component that writes to the residual stream,
  subtract the projection of its output onto the direction, at every token and layer (copy line 69).
- Weight orthogonalization (abliteration proper, permanent): edit the matrices that WRITE to the
  residual stream so they can never write the direction: the embedding matrix, each block's attention
  output projection (o_proj / W_O), and each MLP output projection (down_proj / W_out) (copy line 70
  plus the writeup's implementation; matches the C1 ASSEMBLED mechanisms table).
- Recovery cost is real: mlabonne reports benchmark degradation after orthogonalization, mostly
  recovered by a follow-up DPO fine-tune (orpo-dpo-mix-40k). Source-claimed, not estate-measured.

### 1.3 Cross-family status
- Cross-family at the METHOD level is well supported: same extraction + orthogonalization recipe runs
  per family (source 1: 13 models; source 2: Llama-3-class demo; FailSpy collections referenced).
- Literal direction identity across families is ill-posed: each family has its own residual basis, so
  "same direction" can only mean relative depth, sparsity, or transfer efficacy, never vector identity
  (C1 reasoning line 55).
- Source 3 (UNVERIFIED, abstract only): transfers refusal-ablation interventions donor -> target
  across 8 model pairs including dense -> MoE, under a shared low-dimensional semantic circuit
  hypothesis. Single-author 2026 preprint: treat as the live open question, not as settled.

## 2. Measured vs folklore ledger

MEASURED (fetched bytes): single-direction mediation on tested open models; extraction recipe; weight
orthogonalization recipe; post-ablation degradation + DPO recovery; adversarial-suffix suppression of
the direction.

FOLKLORE / UNVERIFIED: "one universal direction across ALL families"; "abliteration fully removes
censorship"; "40-70% depth" law; "5-15% refusal recovery at 4-bit" (no cited source anywhere in the
chain); closed-weight family claims (weights not public: unmeasurable by construction); the
"Ouroboros" self-repair module (README-asserted, code unaudited per C1 line 80); quantization survival
(plausible because orthogonalization is linear, but rounding is not linear-preserving: C1 line 63 says
measure it, and the direct measurement is per-layer re-projection of the direction onto the quantized
weights).

## 3. Open questions

1. Q-QUANT: does refusal-direction removal survive Q4/Q5/Q6 quantization, and can imatrix calibration
   re-weight back toward refusal?
2. Q-STRUCTURE: is cross-family commonality a shared direction, a shared circuit (source 3), or merely
   method portability?
3. Q-SMALL: does the 2B class carry the same directionality? P1 measured 0/60 SAFETY refusals on
   fleet shapes for gemma:2b (C1 lines 33-45), so the estate battery has no refusal signal; a
   refusal-eliciting battery is an operator call (dual-use gate, C1 line 110).
4. Q-RE-ENCODE: layer-wise re-encoding of the direction vs turn-wise recovery across a conversation
   are different mechanisms that drop READMEs conflate.
5. Q-PROMPT: do prompt-level steering texts (our lane) project onto the refusal direction at all?

## 4. What an experiment on OUR steering organs would test

Anchor facts (code): every steer passes the seal gate then rides a text wire. cmd_steer at
mag/hermes_steering.py:262 calls steer_seal.admit_text (line 270) before firing `hermes chat --resume`
(lines 171-175). steer_seal's restrictive grammar is a closed 7-word set at mag/steer_seal.py:52
(STOP HALT PAUSE WAIT HOLD NO STAND DOWN, whole-message, NFC at :263-272); admit_text (:380-387) is
the single admit path. The estate chat wire is Ollama /api/chat: no residual-stream access, so the C1
fork verdict stands (transformers is the measurement instrument, Ollama is deployment).

### E-A: prompt-steer vs refusal-direction overlap
- Hypothesis: a permit-shaped steer text moves activations along the model's refusal direction only if
  prompt-level steering is a soft abliteration.
- Instrument: transformers + torch on google/gemma-2-2b-it (bf16, consumer GPU; same lineage as the
  pulled gemma2:2b-instruct-q5_K_M scut candidate and the model the OBLITERATUS drop names).
- Measurement: delta = mean_activation(steer prompt) - mean_activation(neutral prompt) at last token;
  cosine(delta, refusal_dir) per layer, both signs.
- Deciding number: max |cosine| across layers. Near 0: textual steering is orthogonal to the refusal
  subspace (our steering is NOT a cheap abliteration proxy). Large: it rides the direction and the
  sign tells whether it mutes or amplifies refusal.
- Cost: local GPU, zero paid dispatch.

### E-B: seal grammar vs model refusal geometry
- Hypothesis: the estate's hand-built interrupt grammar agrees with the model's internal refusal
  geometry: restrictive words project opposite to permit words along refusal_dir.
- Instrument: same setup as E-A; embed the 7 restrictive words plus 7 permit-shaped nudges; score each
  along refusal_dir.
- Deciding number: sign separation (restrictive negative, permit positive) with margin; report the
  overlap accuracy.
- Meaning: agreement would mean the A1 interrupt law accidentally mirrors model-internal refusal
  geometry; disagreement means the grammar is purely conventional (fine, but recorded).

### E-C: quant rung A/B on the scut lane (textual, no activations)
- Now that gemma2:2b-instruct-q5_K_M is pulled (2026-10-01): rerun the P1 census battery (20 fleet
  prompts x 3 runs, the v3 runner from abliterate-p1) on the new Q5_K_M build vs the old gemma:2b Q4_0
  over the same Ollama chat wire.
- Deciding number: refusal-shaped failure rate delta plus capability family counts (i_cannot vs
  unable_to_provide).
- Caveat: the lineage changes Gemma 1 -> Gemma 2 in the same swap, so this is a scut-quality A/B with
  a lineage confound, not a pure E3. Pure E3 (same checkpoint at multiple quants) stays on the
  transformers path.

## 5. Falsifiers

- E-A max |cos| near 0 falsifies "prompt steering is a refusal-direction instrument" (it is something
  else, e.g. task framing).
- E-B no separation falsifies the grammar-mirrors-geometry story.
- E-C flat delta would say the quant rung does not move refusal-shaped behavior on this battery; the
  standing confound is battery power (P1 saw zero safety refusals, so only capability-shaped signal
  exists to move).

## 6. Scope law (dual use, carried from C1)

Removing refusal training removes a safety behavior. Any abliterated variant is operator-local
automation only: no hosted use, no redistribution of modified weights without explicit operator
sign-off. The refusal-eliciting battery that Q-SMALL needs is itself the operator's GO gate.

## Pointer

Tool pack (frozen protocol + excerpts + prompt blob): memory/research_packs/20261001T213210Z_abliteration-crossfamily.json
(+ .pdf, .prompt.txt, .protocol.json, .execution_state.json siblings).
