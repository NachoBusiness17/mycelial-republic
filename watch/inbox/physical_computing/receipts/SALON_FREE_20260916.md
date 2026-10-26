# SALON FREE LANE — 2026-09-16 — physical-computing substrate pass

Lane: background wave-lane (fleet repo). Budget law: $0 only, free providers/lanes.
Status: RECEIPT OPENED. No tool run yet.

Witness question (verbatim, for lanes):
"The fleet is weighing physical computing substrates (thermodynamic/water/analog computers, laser-etched local manufacture, mycelium bioreactors) as the sovereign hardware layer — the answer to 'they can't buy us' when memory prices double. Round 1 of a multi-AI cohort established: (a) only full-system accounting is honest (DAD round-trip test: encode/decode/verify overhead swamps the physical core above ~10k variables); (b) effective-sample-size-per-Joule is the load-bearing uncertainty for thermodynamic samplers; (c) embedding penalties decide Ising machines; (d) vocabulary dispute: 'substrate-native' vs 'Dynamics-Engineered Computing'; (e) claim: a $0 software fleet's free-lane salons ARE a thermodynamic sampler of judgment space (correlated lanes = slow mixing = waste). Witness task: attack or extend ONE of these in your own voice, ≤200 words, and name ONE falsifiable next measurement a $0-budget fleet could actually run this week."

## Plan
1. Read mag/research_fanout.py + mag/scale_salon.py (argparse/main).
2. Fire ONE bounded run: free providers only, ≤20 lanes. Abort any paid path, record why.
3. Collect tool receipts/logs, distill per-lane one-liners (max 10 best) + novel mechanisms/falsifiers not in round-1 cohort.
4. Budget ledger at end.

## Append log
- Receipt opened 2026-09-16.
- Read CLIs: `research_fanout.py` (cmds: lanes/battery/run/retry/status; LANES = 12 free-tier lanes, paid keys excluded by design; battery is a hardcoded WoW corpus — wrong content for this witness). `scale_salon.py` (no CLI args; hardcoded parable; exposes `call(lane, prompt, key, temperature, timeout, max_tokens)` with https allowlist + resolved-IP SSRF guard; failures preserved as rows).
- Decision: no code edited, no scripts created. ONE bounded run reuses the tools' own `LANES` + `call()` unmodified from the repo venv, witness question verbatim, ≤12 lanes (list max), max_tokens at tool default, receipts captured to this directory. Any paid path = abort (none exists: allowlist is free tiers only).
- Next: check env key names (names only), probe lanes live, fire run.
- Probe (`research_fanout lanes`, 12 free READY calls): 10 LIVE — groq-oss, groq-oss20, cerebras-oss, cerebras-qwen, mistral-min8, zai-air, zai-47, or-glm52, or-nemotron, or-ling3. DEAD: groq-qwen (HTTP 429), mistral-small (HTTP 429). No paid lane exists in the list.
- Fire decision: `research_fanout.call_lane` (generic primitive; built-in contract = concrete/bullets/200-word limit — matches witness task) not `scale_salon.call` (hardcodes parable-writer system prompt). No code edited; call params at tool defaults (temp 0.2, max_tokens 2600), timeout 240s.
- FIRED (pass 1, 10 lanes parallel, ~4 min wall): 7 OK — groq-oss, groq-oss20, cerebras-oss, mistral-min8, zai-air, or-nemotron, or-ling3. 3 FAILED (preserved rows) — cerebras-qwen `empty_content`, zai-47 `TimeoutError` @240s, or-glm52 `HTTP 429`. Raw: `SALON_FREE_20260916_raw.jsonl`.
- PASS 2 (single retry, 3 calls): cerebras-qwen OK (had hit the 2600-token reasoning cap; raised max_tokens within the function's own params). zai-47 **ABORTED — HTTP 429 "Insufficient balance or no resource package. Please recharge" = PAID WALL. Do not retry this lane (budget law).** or-glm52 HTTP 502 (upstream, free tier, transient — not retried again, one-pass bound held).
- FINAL: 8/12 lanes answered. groq-qwen + mistral-small died in probe (429), zai-47 paid-walled, or-glm52 upstream 502.

---

## Distilled salon (witness question verbatim; 8 lanes; LEADS, NOT FACTS — no number below is byte-checked)

### Per-lane one-liners (all 8, best first)
1. **cerebras-qwen** (attack e): salons are biased MCMC — unknown proposal, no energy function, no detailed balance; correlation is *systematic bias*, not just waste. Falsifier: 6 Ollama temp lanes (0.2→1.6) × 20 judgment prompts × 5 repeats on one laptop; ESS = 6/(1+5·r̄); **median ESS < 2.0 ⇒ salon is an echo chamber, claim (e) false.**
2. **or-ling3** (attack e, hardest): salons are engagement-ranked graphs — no Hamiltonian, no heat bath, no temperature; "temperature" would only be recommendation-noise variance. Falsifier: 48h of public cross-post timestamps, autocorrelation C(Δt) of lane-identity switches; τ_int < 5× median inter-switch interval ⇒ fast mixing ⇒ (e) falsified; τ_int > 50× ⇒ holds.
3. **groq-oss** (attack c): embedding is an *energy* claim, not just a topology claim — minorminer CPU embedding (~5 J/instance claimed) vs ~0.02 W anneal ⇒ >250× overhead. Falsifier: perf-stat RAPL on embedding vs anneal Joule/variable for Gset #14 with free D-Wave community access; if embedding < 90% of total Joules, (c)'s premise dies.
4. **or-nemotron** (extend a): the ~10k-variable DAD break-even is **not protocol-invariant** — reported crossovers range ~7k–14k depending on codec, code rate, silicon, sparsity. Falsifier: DAD round-trip sweep n = 1k…20k on Qiskit free tier, per-stage timing + pyRAPL energy + Hamming verify; the measured crossover n* is the result; publish the CSV. (Lane leaked its own chain-of-thought into `answer`; extract the final bullets.)
5. **cerebras-oss** (extend b): ESS/J has a hard physical ceiling — Landauer k·ln2 ⇒ max ≈ 1.05×10¹³ samples/J. Falsifier: 2-resistor + Arduino Metropolis Ising toy, 10⁶ steps, USB power meter; measured ESS/J vs ceiling.
6. **groq-oss20** (extend b): ESS/J must be time-aware — ESS ≈ T_total/τ_mix. Falsifier: $0 dye-in-water cell, 10 thermistors + Arduino + smartphone OpenCV; autocorrelation lag where C < 0.1 defines τ_mix.
7. **zai-air** (extend b): measure samples/Joule scaling of plain numpy simulated annealing on 10×10→30×30 Ising grids — establishes the software baseline any physical substrate must beat.
8. **mistral-min8** (attack a): proposes DAD overhead at 5k vs 10k variables. **LOW TRUST: its citations (IBM/dad-benchmark repo, Rigetti Forest 1.1, exact version numbers) look confabulated — protocol shape is reusable, numbers are not.**

### Novel mechanisms/falsifiers round-1 did NOT produce
- **Bias ≠ waste.** Round 1 said correlated lanes = slow mixing = waste. Two independent lanes (cerebras-qwen, or-ling3) went further: correlation in a curated lane pool is *systematic bias* — no detailed balance, no energy function, so the salon converges on an attractor rather than sampling slowly. This upgrades (e) from an efficiency dispute to a validity dispute, and both give concrete ESS/autocorrelation falsifiers.
- **Landauer normalization (cerebras-oss):** a hard physical ceiling turns "ESS/J is load-bearing" into a bounded, comparable ratio across substrates.
- **Time-aware ESS (groq-oss20, zai-air):** divide by τ_mix, not raw samples — welds claim (b) to (e)'s mixing critique.
- **Break-even is stack-relative (or-nemotron):** (a)'s "~10k" is an aggregate; the honest form is "crossover n* given codec+node+sparsity," measurable by sweep.
- **Embedding Joules, not embedding penalties (groq-oss):** converts (c) into a laptop-measurable energy ratio.
- **The fleet can synthesize its own temperature axis (cerebras-qwen):** an Ollama temperature ladder on a local model is a real, $0 thermodynamic-style knob for salon mixing — makes (e) testable in-house this week.
- **Meta-datum:** witness-choice distribution was 4×(b), 3×(e), 2×(a), 1×(c), 0×(d) — nobody defended the vocabulary dispute. The round itself is a correlated sample (a small-salon mixing measurement in its own right).

## Budget ledger
| Item | Count | Cost |
|---|---|---|
| Probe calls (READY) | 12 | $0 (free tiers) |
| Pass 1 witness calls | 10 | $0 |
| Pass 2 retry calls | 3 | $0 |
| **Total external calls** | **25** | **$0.00** |
| Lanes answered | 8 of 12 configured | — |
| Lanes dead | groq-qwen (429), mistral-small (429), zai-47 (**paid wall — do not retry**), or-glm52 (502 upstream) | — |

- No paid API touched; no Hermes cash; no keys used outside the tool's free-lane allowlist (groq, cerebras, mistral, z.ai free tier, OpenRouter :free).
- Raw tape (13 rows, append-only): `watch\inbox\physical_computing\receipts\SALON_FREE_20260916_raw.jsonl`
- This receipt: `watch\inbox\physical_computing\receipts\SALON_FREE_20260916.md`
- Tool logs untouched elsewhere (research_fanout `run`/`retry` not executed; `memory/runs/research_50_wow` unmodified).
- Doctrine note: all answers are LEADS; every number needs a byte-check before promotion (mistral-min8's citations are almost certainly invented; or-nemotron/groq-oss figures unverified). The falsifier *protocols* are the durable output.
