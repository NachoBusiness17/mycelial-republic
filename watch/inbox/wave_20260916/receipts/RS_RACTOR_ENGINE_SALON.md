# RS RACTOR ENGINE SALON — receipt (wave 20260916, lane RS)

**Mission (operator, verbatim):** "burn our free lanes — we have prior art for all of this, self steal" — run the free-lane salon on THE RACTOR ENGINE (fleet's newest design) using prior art as context. Driver pattern: `watch/inbox/wave_20260916/d23_salon50_night_20260916.py` (imports `mag.research_fanout` LANES/_env/_now UNMODIFIED; probe first; or-union-alpha only if the probe says alive).
**Laws honored:** receipt FIRST (this file, appended as work proceeds) · no git · $0 live free lanes only · z.ai paid walls never called (Lite seat is burst-only, never a default carrier — mag/lite_guard law 15) · SSRF allowlist + resolved-IP guard · rows append to raw.jsonl as they land · failures preserved as rows · 2 seeds/question minimum across distinct lanes.
**Driver:** `watch/inbox/wave_20260916/rs_ractor_salon_20260916.py` · **Raw tape:** `memory/runs/rs_ractor_salon_20260916/raw.jsonl` · **Schema:** `rs_ractor_salon.v1`
**Interpreter:** `.venv\Scripts\python.exe` only.

## Registered BEFORE firing (frozen question set + context)

CONTEXT block embedded verbatim in every segment prompt (≤250 tokens):

> A fleet is building ractor witnesses for multi-model deliberation: each witness is a small local model (2B-class) whose 'mind' is a graph of belief nodes (memory/values/perception/verdict) evolving by Laplacian diffusion, parameterized by an OCEAN personality vector (openness = boundary conductance, neuroticism = negative feedback gain, etc.); decisions fire on threshold crossings; reasoning depth = a recurrent latent loop (a 3.6B model looping its state 64x matched a 103B model — Geiping et al. 2502.05171); prior art: OCEAN-conditioned LLM agents, DeGroot consensus, generative agents.

Questions (verbatim, word limits enforced by prompt):

1. **Q1-diffusion-break** — "What breaks first when a witness's 'thinking' is graph diffusion on beliefs instead of token generation — and is that break fatal or fixable? Take a side, 120 words."
2. **Q2-recursion-vs-breadth** — "Does recurrence depth substitute for parameter breadth in judgment tasks — can a 2B model looping 64x produce verdicts indistinguishable from a 70B single pass? What is the first measurable difference? 120 words."
3. **Q3-ocean-falsifier** — "Design the cheapest falsifier: how do you prove a witness's OCEAN parameters actually change its verdicts, beyond prompt costume? Name the control. 100 words."

## Probe (one READY ping per candidate lane; zai-lite excluded BEFORE any call)

Fired 20260916, `.venv\Scripts\python.exe watch/inbox/wave_20260916/rs_ractor_salon_20260916.py --probe`. Rows also on the raw tape.

| lane | verdict | ms | note |
|---|---|---|---|
| groq-qwen | DEAD | 287 | HTTP 429 — "Request too large for model qwen/qwen3.8-27b" (org-level limit; not a paid wall) |
| groq-oss | LIVE | 531 | READY |
| groq-oss20 | LIVE | 526 | READY |
| cerebras-oss | LIVE | 316 | READY |
| cerebras-qwen | LIVE | 206 | READY |
| mistral-min8 | LIVE | 2705 | ok, but anomaly: probe sample answered about "The Ractor Engine's actor model…" instead of "READY" — full run answers are on the tape, contamination checkable |
| mistral-small | DEAD | 463 | HTTP 429 rate_limited code 1300 (not a paid wall) |
| or-union-alpha | LIVE | 5008 | probe says ALIVE → cleared per mission law (time-boxed stealth lane) |
| or-glm52 | LIVE | 3170 | READY |
| or-nemotron | LIVE | 18323 | READY (slow — 18s ping; run rows may be slow) |
| or-ling3 | LIVE | 1041 | READY |

- skipped BEFORE any call: `zai-lite` (mission order: never the zai paid walls; Lite seat burst-only, never a default carrier)
- **LIVE (9):** groq-oss, groq-oss20, cerebras-oss, cerebras-qwen, mistral-min8, or-union-alpha, or-glm52, or-nemotron, or-ling3
- question_digest `c1d24f3ea1a55666`-class digest recorded on tape; context_digest also on tape
- Seed map (frozen, 4 seeds/question = 12 total, 2 minimum exceeded): Q1 → groq-oss, groq-oss20, cerebras-oss, cerebras-qwen · Q2 → mistral-min8, or-union-alpha, or-glm52, or-nemotron · Q3 → or-ling3, groq-oss, groq-oss20, cerebras-oss; temps cycle {0.2, 0.7, 1.2}

## Run (12 seeds, append-as-land)

CORRECTION (recorded, not silently edited): `--run` re-probes when `--live=` is not passed; the re-probe caught `or-glm52` transiently rate-limited (HTTP 429, "temporarily rate-limited") while groq-qwen / mistral-small stayed dead. The run therefore executed on **8 live lanes**, and the executed seed map is the tape's `kind=run` row (question_digest `270067c51345d21a`, context_digest `cd0dd1ddffc64613`):

- **Q1-diffusion-break** (s0–s3): groq-oss t0.2 · groq-oss20 t0.7 · cerebras-oss t1.2 · cerebras-qwen t0.2
- **Q2-recursion-vs-breadth** (s4–s7): mistral-min8 t0.7 · or-union-alpha t1.2 · or-nemotron t0.2 · or-ling3 t0.7
- **Q3-ocean-falsifier** (s8–s11): groq-oss t1.2 · groq-oss20 t0.2 · cerebras-oss t0.7 · cerebras-qwen t1.2

Pass 1: 10/12 answered. Failures preserved as rows (d23 law): s7 or-ling3 `empty_content`, s11 cerebras-qwen `empty_content`. Pass 2 (retry, same seed→lane map, append-only, extra headroom): **both recovered — 12/12 answered.**

Diversity (pairwise token-Jaccard, mean): Q1 0.167 · Q2 0.151 · Q3 0.186 — low overlap, no echo chamber. Word-limit discipline imperfect (a few answers run ~130–150 words vs the 120/100 ask); content intact, counts on the tape.

### Answer digest (sides taken)

**Q1 — what breaks first, fatal or fixable?**
- s0 groq-oss: **token-generation interface** collapses (decoder gets a flat belief vector, not a token stream). Fatal for explicit output; **fixable** — learned diffusion→logits projection head.
- s1 groq-oss20: **sequential compositionality** — Laplacian smoothing erases ordered structure, contexts bleed, drift to equilibrium, catastrophic forgetting. **Fatal for deliberation unless hybrid** (gating + lightweight autoregressive decoder).
- s2 cerebras-oss: **chain-of-thought trace** destroyed — global smoothing overwrites token autocorrelation. Fatal for pure generation, **mitigable** — decoder projecting belief→logits.
- s3 cerebras-qwen: **novelty** — diffusion only redistributes mass, cannot invent a node/category/counterfactual that has no edge; OOD-brittle, echoes consensus. **Not fatal** — threshold-triggered sparse generative probe (short token patch → new nodes/edges → re-diffuse).

**Q2 — does 64x recurrence substitute for 70B breadth?** — **unanimous NO (4/4).**
- s4 mistral-min8: first measurable difference = **long-range causal alignment** (fails to backtrack on multi-hop chains; loop collapses into DeGroot-like consensus).
- s5 or-union-alpha: first measurable difference = **counterfactual sensitivity** on one-fact minimal pairs; mechanism = attractor capture; Laplacian smoothing wipes minority evidence.
- s6 or-nemotron: first measurable difference = **degradation beyond the loop's effective memory horizon** (quality decays with loop count).
- s7 or-ling3: first measurable difference = **compositional OOD factual grounding** ("depth refines priors; breadth supplies the priors"; loop hallucinates confidently).

**Q3 — cheapest OCEAN falsifier + control**
- s8 groq-oss: blind A/B "Parameter-Ablation Control" — twin with gains neutralized, identical prompt/seed/memory init, **KS test** on verdict distributions.
- s9 groq-oss20: **factorial OCEAN sweep**, 200 identical prompts, neutral-OCEAN baseline, **chi-square** vs baseline.
- s10 cerebras-oss: **double-blind one-factor A/B** (alter openness only), evaluator blinded, KL divergence; control = **parameter-swap null** (swap back to original).
- s11 cerebras-qwen: fix weights/prompt/seed/budget; **never render OCEAN into the prompt**; alter only numeric gains; control = **zero-coupling placebo** (trait adjectives in prompt WITH all gains neutral) — "if flips persist, it is costume, not mechanism."

## Fold

**Per-question fold:**
- **Q1** — Sides: 4/4 say the first break is real and NONE call it unconditionally fatal; 3/4 locate it at the token interface (compositional chain lost to smoothing) and 3/4 independently prescribe the same fix: a **decoder bridge** (learned diffusion→logits/verdict projection). 1/4 (qwen) dissents on location: the deeper break is **novelty/mass conservation** — diffusion cannot mint new belief nodes, so fluency is recoverable but invention is not. Sharpest mechanism: **Laplacian smoothing destroys sequential compositionality and conserves belief mass — it can blend but never create.**
- **Q2** — Sides: **unanimous no**; the Geiping-style depth loop is refinement of existing representations, not acquisition. Sharpest mechanism: **attractor capture** (union-alpha's name) — the loop reinforces an impoverished state while Laplacian smoothing erases minority evidence, which predicts ALL four proposed first-measurable-differences at once (backtracking failure, counterfactual insensitivity, OOD hallucination, loop-horizon decay are the same failure wearing different probes). Best single instrument: **one-fact minimal pairs** (counterfactual sensitivity) — cheapest to automate in a ractor.
- **Q3** — Sides: unanimous that OCEAN must be tested at the **parameter level with the prompt frozen**, and all four name the same control family: a **neutral-gain twin**. Sharpest mechanism/control: **qwen's zero-coupling placebo** — trait adjectives IN the prompt while ALL graph gains are neutral — because it measures costume and mechanism in the same run; verdict-flip significance (KS/chi-square/KL all converge) against the placebo is the falsifier.

**Consensus/divergence line:** Consensus is unusually strong — a unanimous Q2 "no," a shared Q1 fix (decoder bridge), a shared Q3 control (neutral-gain twin) — the fleet's design intuitions are convergent. The one live divergence is *where the first break lives*: interface vs novelty (3–1). That split is not noise; it ranks which amendment is load-bearing: the bridge restores fluency, the node-creation path restores judgment.

**3 best design amendments for the ractor engine spec:**
1. **Decoder bridge is load-bearing, not optional.** No witness may emit verdicts from raw diffusion state: spec a learned diffusion→verdict/logits projection (or a short token patch) as a required component. A witness without it fails Q1's first break by construction (3/4 lanes converged on this independently).
2. **Add a sparse generative probe (node-creation path).** Diffusion conserves mass, so cap novelty by construction; give each witness a threshold-triggered escape hatch — emit a short token patch, parse it into NEW belief nodes/edges, re-diffuse. This fixes qwen's novelty break and directly counters the consensus-echo failure mode; pair it with counterfactual one-fact minimal pairs as the standing regression metric for loop depth (Q2's cheapest first-measurable-difference).
3. **Certify witnesses against the zero-coupling placebo.** Every OCEAN-parameterized witness ships with a neutral-gain twin (same prompt adjectives, same seeds, same memory init, one-factor-at-a-time sweeps). A witness is only certified if its verdict distribution separates from the placebo twin (KS/chi-square) — prompt costume fails the gate by design (Q3, unanimous).

## Receipts

- Driver: `watch/inbox/wave_20260916/rs_ractor_salon_20260916.py` (pattern: d23_salon50_night_20260916.py; `mag.research_fanout` LANES/_env/_now unmodified; SSRF allowlist + resolved-IP guard; 1.2 s/lane pacing; Mistral no-`seed` exception)
- Raw tape: `memory/runs/rs_ractor_salon_20260916/raw.jsonl` (probe ×2 passes + run row + 14 seed rows incl. 2 pass-2 recoveries; append-only, failures preserved)
- Summary: `memory/runs/rs_ractor_salon_20260916/summary.json` — 12 seeds / 12 answered / 0 failed
- Cost: **$0.** Lanes fired: groq-oss, groq-oss20, cerebras-oss, cerebras-qwen, mistral-min8, or-union-alpha (probe-alive, as ordered), or-nemotron, or-ling3. Never called: zai-lite (paid-wall seat, excluded before any call). Dead at probe: groq-qwen, mistral-small (429s, not paid walls); or-glm52 dropped by the run-time re-probe (transient 429).

