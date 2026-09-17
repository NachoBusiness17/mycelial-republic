# THE RACTOR ENGINE — SPEC v0.1

**Date:** 2026-09-16 · **Status:** design basis COMPLETE, pre-build (no code has run — all numbers below are design values or cited claims, marked per the ledger in §9)
**Lineage (all read in full, receipts on file):**
- `watch/inbox/moonshot_20260916/receipts/M1_MNEMONIC_PRIORART.md` — prior art + the empty middle + steals
- `watch/inbox/moonshot_20260916/receipts/M2_RECURRENT_DEPTH.md` — Geiping et al. 2502.05171, recurrence budgets, depth receipt
- `watch/inbox/moonshot_20260916/receipts/M3_LAPLACIAN_BELIEFS.md` — the math: graph, update rule, OCEAN map, falsifier
- `watch/inbox/wave_20260916/receipts/RS_RACTOR_ENGINE_SALON.md` — 9-lane free salon (12/12 answered, $0): decoder bridge, generative probe, placebo certification, Q2 unanimous

**The empty middle (M1 verdict):** no published system combines (a) witnesses as modules of a brain-graph, (b) OCEAN vectors as physical parameters of the graph's dynamics, (c) thinking rendered as literal state flow over that graph, (d) decisions firing only as threshold crossings with every crossing receipted and scored against a human self-agreement ceiling. Stanford owns believable-but-flat agents; Line A owns trait-conditioning on flat models; neuroscience owns threshold decisions without LLM witnesses; mnemonic.ai owns the business case and the benchmark protocol but has no dynamics. This spec occupies that middle — locally, on small models, with receipts.

---

## 1. Architecture — three layers, one sovereignty rule

A **ractor witness** is a harvested persona (dossier on file) given a physical mind: a signed belief-graph whose state evolves by diffusion, a recurrence loop that composes diffusion steps, and a local LLM that speaks for the graph. The layers are strictly separated by the sovereignty rule (§1.5).

### 1.1 Layer A — the Laplacian feeling-graph (diffusion owns feeling)

**Graph.** 33 nodes, signed valence u_i ∈ [−1, +1] (+ = endorse/approach, − = repel/avoid), in five substrate layers plus one output node (M3 §2a; the mission shorthand "5 layers" is here reconciled as 5 substrate layers + O1 = 33):

| Layer | # | Role | Boundary class |
|---|---|---|---|
| **P** perception | 4 | factual claim, asker tone, source credibility, personal stakes | **Clamped (Dirichlet)** per session by the question |
| **M** memory | 12 | biography nodes (dossier-harvested; e.g. for Fermat: the margin, Wallis quarrel, Pascal friendship, …) | Free, slow leak |
| **V** value | 8 | truth-over-reputation, secrecy, fairness, curiosity, … | **Pseudo-clamped**: λ_V ≈ 0.02 (conservation) |
| **I** inference | 6 | "genuine puzzle or trap?", "worthy opponent?", gut valence composite, … | Free, fast |
| **S** social | 2 | S1 salon consensus (neighbors' live O1), S2 asker status | **Forced input** from other minds |
| **O** output | 1 | **O1 verdict node** — the only node allowed to fire | Free |

The **signed weight matrix A** (33×33, sparse) is the witness's personality skeleton, authored/harvested from the dossier once, then **frozen and hash-committed**. A is shared across questions; only P clamps and S inputs change per question.

**Update rule (M3 §2b, exact):**

```
du_i/dt = −γ · Σ_j W_ij (u_i − u_j) − λ_i·u_i + b_i + σ_i (S_i − u_i)·1[i∈S] + ξ_i(t)

W_ij = A_ij · (1 + κ·1[A_ij<0]) · (1 + a·1[A_ij>0])
```

Terms: (1) graph diffusion through conductance W — the heat/Laplacian core; (2) leak λ_i (≈0 for values, larger for inference nodes); (3) intrinsic bias b_i from the dossier; (4) salon coupling on S nodes only; (5) small bounded noise ξ (rounded-off cognition, seeded — see §5.3). P nodes clamped; S1 driven by neighbors' O1; all u clipped to [−1, 1]. Euler integration, Δt ≈ 0.05, ~200-step cap per epoch. With κ=0 this is exactly Zhu et al.'s Gaussian field with clamped boundary (live-verified M3 §1c); with κ>0 it is Altafini's signed network with leak (live-verified M3 §1d).

**Lineage honesty (M3 Step 1):** DeGroot 1974 (consensus), heat-kernel ⇔ consensus, Zhu/Ghahramani/Lafferty 2003 (Dirichlet perception layer), Altafini 2013 (antagonistic negative edges), Pearl 1988 / Yedidia-Freeman-Weiss 2003 (BP upgrade path), Collins & Loftus 1975 / Hopfield 1982 (activation precedent). All LIVE-VERIFIED except Pearl/YFW (canon-labeled). What is *ours* is only the OCEAN parameterization (§2).

**Verdict = threshold crossing (M3 §2d):**
- Fire: first time |u_O1| ≥ θ_eff, **sustained for h** (hysteresis; suppresses noise-fires). Default θ = 0.35 *(design value, unrun)*.
- **verdict = sign(u_O1)** → ENDORSE / REFUSE.
- **confidence c = min(1, (|u_O1| − θ_eff) / (1 − θ_eff))** — literally distance past threshold.
- **T_fire** = steps to first stable crossing — deliberation time is a first-class output.
- Step cap with no stable crossing → **UNDECIDED with oscillation flag set.** Rumination is a real, reportable outcome; never hidden in a forced sign.

### 1.2 Layer B — the recurrent reasoning loop (depth = steps)

**v0.1 decision (flagged, §10.1):** the Geiping latent-token loop is **approximated, not trained**. gemma:2b is not Huginn; v0.1 implements recurrent depth as **state-dependent re-wiring epochs** — the M3 fix for Kill 2:

- Every K diffusion steps, re-wire conductances from current state: **W(t) = φ(A, u(t))** — e.g. when u_I4 ("connects to the margin?") saturates high, strengthen M1→O1 and M12→I1 for the next epoch. The rewiring function φ is a small deterministic rule table (hash-committed with A), not learned in v0.1.
- Dynamics becomes a composition of *different* operators: u(t+nK) = Φ_{w_n}∘…∘Φ_{w_1}(u(0)) — finite-step sequential composition; each step an honest diffusion. **Sequence = unrolling; depth = number of re-wirings.**
- **Exit rule (M2 App 5 translated):** loop until the state/draft stops moving — diff a witness-state fingerprint between successive epochs; stop when **final_delta < 5×10⁻⁴** *(Geiping's KL-exit constant, translated to our state diff — design guess, see ledger)*, or at the epoch budget cap, or at the T1.3 hard cap (§3).
- **Path independence (M2 App 3):** each epoch starts from a random s₀ ~ N(0, σ²I) with the question clamps re-injected — the input-injection + random-init pairing that stabilizes Geiping's loop and makes the final state reproducible regardless of initialization. This is what makes the receipt's `state_hash` meaningful evidence rather than vapor. Cheap check: one rerun at a different init, hash-compare (§4).

**What depth buys and does not (M2, paper-verified):** easy/recall tasks saturate by ~8–16 loops; hard/procedural tasks keep gaining to 32–64; r=1 collapses (ARC-C below random); depth buys **procedure, not facts** — closed-book gaps stay open, context extends useful depth 8→32. The witness gets facts from clamps/retrieval, not from more loops.

### 1.3 Layer C — the LLM mouth (the only novelty source)

The mouth is the harvested persona model — **local, small** (gemma:2b for the v0.1 prototype). It receives **the feeling vector** (verdict, confidence, T_fire, top contributing nodes from drift decomposition, oscillation flag) plus the dossier, and *speaks* the justification in the witness's voice.

The mouth's second, load-bearing job (M3 fix for Kill 1; salon amendment 2): the **sparse generative probe**. Diffusion conserves belief mass — it can blend, never create (the convex-hull kill). So:
- When the graph stalls (no stable crossing by mid-budget, or oscillation flagged), the mouth is prompted to emit a **short token patch proposing new content**: a new memory/inference node with a signed valence ("wait — this touches Pascal's honor"), or a proposed edge.
- Proposals are **parsed, then re-enter the PDE** as new nodes/edges clamping in on the next epoch. The hull's boundary is moved *by the mouth*, then validated *by the physics*. This is the only path by which the system generates content genuinely outside the current hull.
- Every proposal is receipted (node name, valence, accepted/rejected) so novelty is auditable.

### 1.4 The decoder bridge (salon amendment 1 — load-bearing, not optional)

Q1 consensus (4/4 lanes: no unconditional fatality, 3/4 independently located the first break at the token interface): **no witness may emit verdicts from raw diffusion state.** A flat belief vector handed to a decoder collapses the token stream — the fix is an explicit bridge:

- **v0.1 bridge (deterministic, flagged §10.2):** a typed projection — feeling vector → structured verdict record + a rendered prompt block for the mouth. Deterministic, hash-committed, trivially auditable.
- **Future bridge (open cell, §8):** a *learned* diffusion→logits/verdict projection head (the salon's prescribed fix), trained on accumulated receipts. Out of v0.1 scope.
- A witness without a bridge fails Q1's first break by construction.

### 1.5 The sovereignty rule

> **Diffusion owns feeling; the mouth owns words; neither writes the other's state.**

- The LLM mouth may **NOT write u_O1** — not the verdict, not the confidence, not the fire. It can only propose node/edge edits that re-enter the diffusion (§1.3).
- The graph may **NOT write words** — it emits the feeling vector through the bridge; justification text is the mouth's alone.
- The rewiring table φ(A, u) is part of the graph's physics; the mouth cannot trigger or edit it mid-run.
- Whether-and-how-sure is the graph's sovereignty; why-and-what's-new is the mouth's. Neither impersonates the other (M3 Step 3, fix 3).

### 1.6 The four kills — kept as standing invariants (M3 Step 3)

Each layer exists because a kill says the others are insufficient. These are invariants, not history — any design change must re-state where each kill now lives:

| Kill | What diffusion cannot do | Where the fix lives |
|---|---|---|
| **1. No novelty** (convex hull) | Linear diffusion only mixes existing ingredients; cannot mint a new operator or node | Mouth's sparse generative probe (§1.3) — validated by re-diffusion |
| **2. No sequence** (semigroup) | e^{−(s+t)L} = e^{−sL}e^{−tL}: thought order is meaningless to the heat flow | Layer B re-wiring epochs (§1.2) — bounded composition, inherits GNN expressiveness limits (WL-1, canon) |
| **3. Instability vs convergence** | κ>0 removes the contraction guarantee; high-N witnesses can limit-cycle | Leak λ + step cap + UNDECIDED-with-oscillation readout (§1.1) — rumination allowed, non-termination not |
| **4. Scalar verdict, no propositions** | sign(u_O1) says for/against, never why | Mouth speaks why; drift decomposition into layer contributions is the diagnostic backbone (instrumentation, not cognition) |

---

## 2. The OCEAN parameter table

Every trait enters as a **material constant of L or its boundary conditions** — none is a post-hoc label on the output. All formulas and coefficients are **design values from M3 §2c, never run** (ledger §9). The DDM column is the M1 steal (spiking/DDM line: Zhou 2018, Jaffard 2025, Zoltowski 2020) — a *readout-level correspondence*, an analogy not a fit; its value is that it independently agrees with the Laplacian map on what each trait does.

| Trait | Sets (Laplacian, primary) | Formula (design value) | Mechanism | DDM correspondence (M1) | Extreme phenomenology |
|---|---|---|---|---|---|
| **O** openness | boundary conductance **g_P** | g_P = 0.5 + 1.5·O | how hard evidence injects through P clamps into {I, M} | drift rate toward novel options | High: belief shifts fast under new evidence. Low: insulated medium; first impressions survive counter-evidence |
| **C** conscientiousness | leak **λ** + hysteresis band **h** on O1 | λ = λ₀(1 − 0.8·C); h = 0.05 + 0.2·C | conservation vs evaporation; re-fire gap after a verdict | boundary height | High: beliefs persist and accumulate, decisions stick. Low: leaky, impulsive fire at first crossing, verdicts evaporate |
| **E** extraversion | salon coupling **σ** | σ = 0.2 + 1.3·E | strength of S1/S2 drive | starting-point bias toward the social/input side | High: porous to the salon (contagion). Low: neighbors are a whisper |
| **A** agreeableness | cooperative-edge gain **a** + conformity shift | a = 0.3·A; θ_eff = θ − 0.15·A when S1 aligns with drift | averages more with others; discounts own resistance when the room agrees | *(no clean DDM analog — noted)* | High: conformity gradient visible in latency. Low: contrarian stability |
| **N** neuroticism | negative-edge gain **κ** (Altafini) + negative-crossing threshold **θ⁻** | κ = 0.3 + 2.2·N; θ⁻ = θ(1 − 0.5·N) | amplifies antagonistic (negative) edges → pushes signed structure toward unbalance → eigenvalues drift toward the imaginary axis → **oscillation = rumination**; θ⁻ = negativity bias | noise σ | High: fear loops amplify (e.g. M5→I1), O1 oscillates around θ, latency long, "no stable opinion" possible. N=0: symmetric, calm, contractive |

The convergence of the two maps (C = boundary in both; N = noise/instability in both; E = bias/coupling in both; O = drift/conductance in both) is circumstantial evidence the parameterization is principled — the falsifiers in §5 are what make it more than costume.

---

## 3. Per-witness recurrence budgets

The M2 fleet translation table, adopted verbatim as the engine's budget ladder. Budgets are **per-question, armed per witness persona, logged per answer**. **T1.3 CAP (non-negotiable): 64.** Gains end at ~64 in the source paper's own model card; beyond that, compute is disintegration theater — cap the loop or the loop caps you.

| seat | model class | recurrence budget (v0.1: re-wiring epochs) | expected depth behavior (M2 curves) |
|---|---|---|---|
| scut janitor | gemma:2b | **4 loops max** | r=4 zone: "very coarse answers"; triage/classify only, no reasoning expected |
| short worker | gemma-class 4B | **8 loops** | easy/recall tasks near-peak by 8; cheap |
| witness (standard) | gemma-class + loop engine | **12–16 loops** | MMLU/OBQA saturated; ARC plateau reached; the workhorse depth |
| witness (context-loaded) | same, retrieved facts in prompt | **20–32 loops** | rich context extends useful saturation 8-12 → ~32 (Fig-9 law); open-book jumps |
| obsessive witness | same, math/procedural only | **64 loops — hard cap** | GSM8K sigmoid tail (42→47% from 32→64); >64 = zero gain, pure burn |
| specialist (remote, scarce) | pro-class | n/a | reserved for what depth cannot buy: long-tail facts, synthesis breadth. Delay, not replacement |

**Per-question budget policy (M2 difficulty dial):**
1. **Probe:** one cheap pass at low depth (r≈2–4). Answer stable + recall-class → done at worker depth; unstable/procedural → escalate.
2. **Stability exit, not fixed depth:** loop until the state stops moving (delta < 5×10⁻⁴, §1.2). Easy questions converge on their own; hard ones earn more loops. Early exit cost ≈ nil in the source (MTBench 5.56 vs 5.63).
3. **Context scaling:** budget rises with prompt richness — zero-shot cap 12, with retrieved evidence cap 32.
4. **Loop hygiene:** 16-state KV rolling budget is lossless in the source — a looped witness need not grow memory linearly with depth. *(Applies to the future latent loop; v0.1 epochs have fixed 33-node state.)*

**Caveat carried forward (M2):** these budgets were measured on a trained latent-recurrent LLM, not on diffusion epochs. For v0.1 they are an *imported shape law* — the falsifier in §5.4 exists precisely to check whether our loop earns its depth. Unverified for our architecture (ledger §9).

---

## 4. The receipt schema

Every witness run files one receipt. Schema `ractor.witness.receipt.v0.1`. The depth field is M2's design, extended with the path-independence check and the salon/mouth fields. Hashes make receipts evidence, not narrative.

```json
{
  "schema": "ractor.witness.receipt.v0.1",
  "witness": {
    "name": "fermat",
    "ocean": {"O": 0.7, "C": 0.4, "E": 0.2, "A": 0.6, "N": 0.8},
    "graph_hash": "sha256:…",          // frozen A + rewiring table φ
    "persona_hash": "sha256:…"
  },
  "question": {
    "id": "amb-07",
    "text_hash": "sha256:…",
    "clamps": {"P1": 0.8, "P2": -0.3, "P3": 0.1, "P4": -0.6}
  },
  "verdict": {
    "outcome": "REFUSE",                // ENDORSE | REFUSE | UNDECIDED
    "u_O1_final": -0.41,
    "confidence": 0.09,                 // min(1,(|u_O1|−θ_eff)/(1−θ_eff))
    "theta_eff": 0.35, "theta_neg": 0.175,
    "fire_latency_steps": 84,
    "oscillation_flag": false           // true ⇒ UNDECIDED rumination is reportable
  },
  "depth": {
    "loops": 24,                        // re-wiring epochs actually executed
    "budget_cap": 64,                   // armed ceiling (persona × difficulty policy)
    "exit": "stability",                // "stability" | "cap" | "probe-pass"
    "final_delta": 3.1e-05,             // last state diff vs threshold (5e-4 analog)
    "state_hash": "sha256:…",           // fingerprint of final graph state — the s_r evidence
    "path_independence": {              // cheap rerun at a different random init
      "checked": true,
      "rerun_init_hash": "sha256:…",
      "match": true                     // hash/within-tolerance equality of final state
    }
  },
  "bridge": {
    "feeling_vector": {"verdict": "REFUSE", "confidence": 0.09,
                        "top_nodes": [["M5", -0.33], ["I1", -0.21], ["M8", -0.17]],
                        "oscillation": false},
    "mouth_prompt_hash": "sha256:…"
  },
  "mouth": {
    "model": "gemma:2b",
    "utterance_hash": "sha256:…",
    "proposed_nodes": [{"name": "Pascal's honor", "valence": -0.6, "accepted": true}],
    "proposals_accepted": 1
  },
  "novelty": {"nodes_before": 33, "nodes_after": 34, "hull_extended": true},
  "provenance": {"ts": "…", "seed": 7, "engine_version": "ractor-engine-0.1"}
}
```

Rules:
- `exit:"cap"` + `path_independence.match:false` (or oscillation) on a saturated answer = the flag that this question needs the specialist (M2).
- `state_hash` is only meaningful because of the path-independence design (§1.2); when `checked:false`, treat the receipt as narrative, not evidence.
- Mouth proposals never touch `verdict` — if a proposal changed the outcome, that happened via re-diffusion in a *new* epoch, with its own depth record appended.

---

## 5. Falsifiers (all pre-registered; file numbers before any run)

### 5.1 Personality-visibility: N=0 vs N=1 (M3 Step 4, unchanged)

**Claim under test:** OCEAN traits are material constants of L, visible in behavior — not costume labels.

- Same 33-node graph, same A, same clamps, same seeds and noise schedule. **≥ 20 ambiguous questions** (constructed so pro and con memory/value paths roughly balance — e.g. "Wallis challenges your margin proof in public; do you answer?").
- **N=0 witness:** κ = 0.3, θ⁻ = θ. **N=1 witness:** κ = 2.5, θ⁻ = 0.5θ.
- Measured per item: verdict sign, confidence c, fire latency T_fire, oscillation flag.

**Pass — all four must hold:**
1. Negative-verdict rate differs by **≥ 15 percentage points** between N=0 and N=1 on ambiguous items;
2. Confidence distributions separated: **KS distance D ≥ 0.2**; or
3. Latency separated: **median T_fire(N=1) / median T_fire(N=0) ≥ 1.5×**; and
4. **Recoverability:** fit κ from verdict/latency data on a held-out half of the battery; recovered κ must land within **±30%** of the planted value. If the map is unfittable from behavior, it is unfalsifiable decoration.

**Kill condition:** N=0 vs N=1 statistically indistinguishable under all measures → the OCEAN→L map is **COSTUME** — kill the parameterization, keep the explainer, file a canon correction. Silence is not an allowed outcome.

**Symmetric honesty note (M3):** a positive result proves the parameterization is behaviorally load-bearing, not that traits are "real personality." Ontological claims stay poetry until the M2/verbalizer loop is live.

### 5.2 Placebo-twin certification (salon Q3, unanimous)

Every OCEAN-parameterized witness ships with a **zero-coupling placebo twin**: trait adjectives IN the mouth prompt, **all graph gains neutral** (intercept values: κ=0.3, g_P=0.5, λ=λ₀, σ=0.2, a=0 — the maps evaluated at all-traits-zero), same seeds, same memory init, same question set.

- **Certification gate:** the witness's verdict distribution must separate from its placebo twin (KS or chi-square, threshold as in §5.1). One-factor-at-a-time sweeps (O, C, E, A, N each alone from the placebo baseline) localize which parameter carries the effect.
- Prompt costume fails the gate by design: "if flips persist [against the placebo], it is costume, not mechanism" (salon s11). A witness that cannot beat its own placebo is **not certified** and may not join a salon quorum.
- The s10 parameter-swap null is adopted as a re-test: swap the witness's gains back to placebo mid-battery; the separation must appear and disappear with the gains, not with run order.

### 5.3 The sampler-lesson cap: seed diversity or the depth is theater

**Principle:** verdict distributions must differ across seeds, or the depth (and the noise term ξ) did nothing — the run is a dressed-up lookup table. *(Concrete thresholds below were not given by any source; they are invented this session and pre-registered here first — flagged §10.3.)*

- Every ambiguous question is run at **≥ 5 noise-seed reruns** (same witness, same clamps, different ξ streams and epoch inits).
- **Pass:** the per-question verdict distribution across seeds is non-degenerate — **≥ 2 distinct outcomes** among {ENDORSE, REFUSE, UNDECIDED} on ambiguous items, **and** per-seed verdict entropy above a floor (pre-registration value: normalized entropy ≥ 0.15 nats on ≥ 30% of ambiguous items).
- **Failure reading:** all seeds agreeing on *ambiguous* items means the graph has collapsed to a fixed point independent of the noise — the "physics" is decorative and the mouth is doing all the work.
- This pairs with the **honesty target** (M1 steal): a witness reproducing its own answers ~**70–90%** is SOTA, not a bug — the human self-agreement ceiling is 73% (mnemonic.ai claim) and Park-style agents sit at ~85% (claimed). A local witness at 100% self-agreement on ambiguous items has failed §5.3, not aced the exam.

### 5.4 Loop-depth honesty: 64× ≠ 70B (salon Q2, unanimous 4/4) + standing regression

Depth is refinement, not acquisition. The salon's four measurable differences between a looping small witness and a big single pass — adopted as the engine's standing regression battery:

1. **Counterfactual sensitivity** on **one-fact minimal pairs** (union-alpha's instrument — cheapest to automate; the primary standing metric);
2. **Long-range causal alignment** — multi-hop chains where the loop must backtrack (mistral-min8);
3. **Degradation beyond the loop's effective memory horizon** — quality vs loop count curves must not invert (nemotron);
4. **Compositional OOD factual grounding** — depth refines priors, breadth supplies priors; the witness must route unknown facts to clamps/retrieval, not hallucinate through loops (ling3).

Unified mechanism (fold): **attractor capture** — the loop reinforces an impoverished state while Laplacian smoothing erases minority evidence. All four probes are the same failure wearing different clothes. Budget claims that fail the minimal-pairs regression are theater regardless of what §3's imported table says.

---

## 6. Build plan — gemma:2b prototype (v0.1)

**Scope:** one witness (Fermat — dossier on file, `watch/FERMAT_RACTOR_20260906.md`), 33 nodes, deterministic engine + local mouth. Everything runs local; **nothing paid, nothing remote** in v0.1.

| Component | Runs where | Notes |
|---|---|---|
| Graph A + rewiring table φ | **Host** (repo venv, Python) | authored as YAML from the dossier; hash-committed; frozen |
| Euler integrator (33×33, Δt≈0.05, ≤200 steps/epoch, ≤16 epochs) | **Host** — pure numpy | trivial compute (33 nodes); seeded RNG for ξ and s₀ |
| Verdict monitor (θ_eff, hysteresis h, confidence, T_fire, oscillation detector) | **Host** | deterministic readout; writes `verdict` + `depth` receipt fields |
| Decoder bridge v0.1 (deterministic feeling→record→prompt block) | **Host** | §1.4; hash-committed templates |
| Mouth | **Local Ollama, gemma:2b** | the only LLM in the loop; fixed temperature; JSON-constrained output for node proposals |
| Proposal parser / re-diffusion trigger | **Host** | mouth output → new nodes/edges → next epoch |
| Receipt writer + hash chain | **Host** | schema §4; append to `watch/inbox/` |
| Falsifier stats (KS, chi-square, entropy, κ-grid-fit) | **Host** — scipy.stats | §5; the κ recovery estimator is a coarse grid search in v0.1 (open cell §8) |

**Steps:**
1. Author `fermat_graph.yaml` (33 nodes, signed A, b_i, leak classes) from the dossier; commit hashes.
2. `mag/ractor/engine.py` — integrator + verdict monitor + depth/receipt writer. No LLM. Testable against hand-computed two-node cases.
3. Bridge templates + mouth driver (Ollama gemma:2b): feeling in → utterance + proposal JSON out. Proposal parser.
4. Author the **≥ 20 ambiguous-question battery** (M3 style: pro/con memory paths balanced); hash-commit; split into fit/held-out halves for the κ recovery check.
5. Run falsifiers in order: §5.3 seed sweep → §5.2 placebo certification → §5.1 N=0/N=1 → §5.4 minimal pairs. **File the real numbers** (house law: trust bytes, not reports).
6. Report: receipts + pass/kill verdict per falsifier, appended to the moonshot receipt directory.

**Estimate of effort:** the engine is small (33×33 matrix, ~200 steps/epoch); the only moving parts with judgment are A authoring and battery authoring. Days, not weeks. No training anywhere in v0.1.

**Out of v0.1 scope (open cells §8):** learned bridge head, latent recurrent block, multi-witness salon (live S1 coupling), dossier→A automation, learned κ estimator.

---

## 7. Evaluation harness (the M1 steal, adopted)

- **Ceiling-relative scoring:** score witnesses against the **human self-agreement ceiling**, not against 100% (mnemonic.ai Twin-2K-500 protocol shape: 2,058 people / 191,406 held-out answers / 89% of the 73% ceiling — *their claims, not reproduced*). Our honest band: witness self-consistency ~**70–90%** (§5.3).
- **Held-out protocol:** batteries are hash-committed before runs; κ recovery and certification are scored only on the held-out half.
- **Witness-Score (future, M1 steal from Brain-Score):** score witness-graph dynamics against human thought traces (receipt logs are the recordings analog). Not buildable until receipts accumulate. Open cell.

---

## 8. Open cells (honest — designed around, not solved)

| # | Cell | Status |
|---|---|---|
| 1 | **Learned decoder bridge** (diffusion→logits/verdict head) | Open. Salon says load-bearing; v0.1 ships deterministic bridge; training deferred until receipts exist to train on |
| 2 | **True latent recurrent loop** (Huginn-style R-block inside a small LM) | Open. Needs training runs; v0.1 approximates with re-wiring epochs — the approximation's fidelity is exactly what §5.4 tests |
| 3 | **κ recovery estimator** | Open method. Grid search in v0.1; a proper (Bayesian/likelihood) estimator is future work |
| 4 | **Dossier→A automation** (matrix authoring at scale) | Open. One witness, hand-authored, hash-committed in v0.1 |
| 5 | **Live salon coupling** (S1 driven by real neighbor witnesses) | Open. v0.1 is single-witness with S1 neutral or scripted |
| 6 | **OCEAN provenance per witness** | Open. v0.1: authored numbers + the ±30% recovery check as the guard; dossier-derived trait estimation deferred |
| 7 | **Self-agreement battery sizing** (how many repeated/paraphrased items for a stable ceiling estimate locally) | Open. Protocol adopted (§7), size unsized |
| 8 | **Wave/fluid operators** (advection = state-dependent transport) | Poetry until proven (M3 §2e label retained) |
| 9 | **Rewiring rule φ** (learned vs hand-authored rule table) | Open; v0.1 hand-authored + hash-committed |
| 10 | **Whether the verbalizer ever legitimately nudges u_O1-adjacent nodes** (the proposal path touches I/M nodes — where exactly "may not write u_O1" sits) | Open design tension; v0.1 rule: proposals enter as *new* nodes or clamp-value suggestions, reviewed by the parser, never direct writes to O1 or I-layer existing nodes |

---

## 9. Unverified-number ledger

Every number in this spec, and its status:

| Number | Source | Status |
|---|---|---|
| All OCEAN→L coefficients (g_P = 0.5+1.5O; λ = λ₀(1−0.8C); h = 0.05+0.2C; σ = 0.2+1.3E; a = 0.3A; θ_eff shift 0.15A; κ = 0.3+2.2N; θ⁻ = θ(1−0.5N)) | M3 §2c design | **DESIGNED, NEVER RUN** |
| θ = 0.35 default, Δt ≈ 0.05, 200-step cap, λ_V ≈ 0.02 | M3 §2b/2d design | **DESIGNED, NEVER RUN** |
| Falsifier thresholds (15pp, KS 0.2, 1.5×, ±30%) | M3 Step 4 pre-registration | **PRE-REGISTERED, UNTESTED** |
| Seed-sweep thresholds (≥5 seeds, ≥2 outcomes, entropy ≥ 0.15 nats on ≥30% of items) | This spec §5.3 | **INVENTED THIS SESSION, pre-registered here first** |
| Recurrence budgets 4/8/12–16/20–32/64 and their curve shape | M2 (Geiping et al. 2502.05171, paper-verified) | **PAPER-VERIFIED for a latent-recurrent LM — imported shape law, unverified for diffusion epochs** |
| KL/stability exit 5×10⁻⁴ | M2 App 5 (Geiping) | Paper-verified in situ; **our translation to a graph-state diff is a design guess** |
| T1.3 cap 64; r=1 collapse; context-extends-depth 8→32; KV 16-step lossless | M2 | Paper-verified (source paper + model card) |
| Human self-agreement 73%; mnemonic.ai 89%-of-ceiling; Park et al. 2024 ~85% | M1 App 2 | **COMPANY/ PAPER CLAIMS, not independently reproduced** |
| DDM correspondence (O→drift, C→boundary, N→noise, E→bias) | M1 steal (Zhou 2018 / Jaffard 2025 / Zoltowski 2020 line) | Literature-verified mechanism; **the mapping onto Laplacian parameters is analogy, not fit** |
| Salon results (12/12 answered, Jaccard diversity 0.15–0.19, unanimous Q2) | RS receipt | Single run on tape; stats as filed |
| Mouth identity "gemma:2b suffices as mouth" | This spec | **ASSUMPTION** — the scut-tier seat is the repo's standing local model; adequacy untested until §6 step 3 |
| Witness-Score feasibility | M1 (Brain-Score analogy) | Speculative, deferred |

---

## 10. Design decisions made alone (flagged for operator)

These three forks were not settled by any source receipt; the synthesizer chose, and the choices are reversible before first run:

1. **Recurrent depth is approximated by re-wiring epochs, not a trained latent loop.** The M2 budgets are imported as epoch caps; the M3 rewiring fix (φ(A, u(t))) is the loop. Rationale: gemma:2b cannot do latent recurrence without training runs we are not doing in v0.1. Risk: the §3 shape law may not transfer; §5.4 is the tripwire. *Reversible:* swap in a trained R-block later without touching Layers A/C.
2. **The decoder bridge ships deterministic in v0.1** (typed feeling→record→prompt projection), with the salon's learned head deferred. Rationale: a learned head needs training data that only receipts can provide; determinism is auditable and hash-committable now. Risk: if the deterministic bridge is too lossy, mouth quality suffers — visible immediately in step 3 of the build plan.
3. **The sampler-lesson cap got concrete invented thresholds** (≥5 seeds, ≥2 outcomes, entropy ≥ 0.15 nats on ≥30% of ambiguous items). No source supplied numbers; leaving it qualitative would make §5.3 unfalsifiable — the exact sin this engine exists to avoid. These are first-dance values and should be re-derived after the first battery run.

---

*Spec end. Receipt of record for this synthesis: `watch/inbox/moonshot_20260916/receipts/M4_RACTOR_ENGINE_SPEC.md`. No git per law. No paid APIs touched. All sources local receipts.*
