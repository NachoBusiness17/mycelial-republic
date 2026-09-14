# HARDWARE_RADAR — physical-silicon avenue map

> **[AUDIT-TYPED 2026-09-08]** status: PROSE · claims: hardware as a cost play is dead on arrival (used 3090 ~$1,200 never beats vast.ai on-demand at realistic duty); only the capability play (fine-tune forge + offline sovereignty) is live — SUPPORTED (quoted+URL'd street prices and breakeven math; utility power rate card-flagged UNVERIFIED) · falsifier: vast.ai on-demand climbing above ~$0.20/hr or 3090 street price collapsing would reopen own-vs-rent (the card's own cap-leak trigger)
Standing economist mission #2 (compute-source radar) extended to purchased hardware.
Date: 2026-09-01 02:2xZ  ·  Operator 02:09Z: "we're also looking at purchasing physical hardware."
Reader: operator / economist / basecamp.
Classification stance: every price is QUOTED+URL'd or UNVERIFIED. Not a buy recommendation — an avenue map with breakevens and a JIT trigger.

---

## 0. WHY THIS IS NOT THE CHEAPEST LANE (read first)

Hardware does not reprice tokens — it pays a fixed cost to move the *ceiling*. Our paid lanes are already cheap and measured:
- DeepSeek flash Hands: ~$1.33/day run-rate (late-month avg, MEMORY L47) — **$1.33/day**.
- z.ai 5.3-flash brain / GLM lane: $0.075/M in, $0.25/M out, $0.015 cache — **measured cheapest interactive lane**.
- Flash driver incl. cache discipline: ~$0.75/day.
- Vast.ai 3090 blade: **$0.09–0.116/hr (BELOW our covenant cap $0.12)**.

A used 3090 at ~$1,200 capex + $0.064/hr power is **$0.20/hr all-in at 24/7** — that is *more expensive* than vast.ai on-demand and double spot. Hardware only wins when the measured demand pattern makes the *last three dollars of rent* hurt more than the first twelve hundred of capex, or when a capability appears that no subscription sells. This report sizes that.

---

## 1. USED-GPU STREET PRICES (2026, QUOTED)

All figures are 2026 used/eBay "street" medians aggregated from price trackers. Expect ±10–20% by condition/AIB/cooler.

| Card | VRAM | Used street (eBay/completed-median) | Source | Verdict for us |
|---|---|---|---|---|
| RTX 3090 | 24 GB | **~$1,100–1,300** (median ~$1,200; EU ~€1,084) | pcprice.watch; bestvaluegpu.com; siliconcomps.com; insiderllm.com/pdfs/used-rtx-3090-buying-guide.pdf | **The 24GB sweet spot** — AI demand has *raised* prices vs pure-gaming depreciation |
| RTX 3090 Ti | 24 GB | **~$1,400–1,600** (median ~$1,450) | bestvaluegpu.com; gpudojo.com/rtx-3090-ti | Premium for same VRAM, higher TDP — marginal |
| RTX 4090 | 24 GB | **~$2,200–2,600** (median ~€2,121 / ~$2,310) | pcprice.watch; dealhunter.io; bestvaluegpu.com | Faster but 2× capex for same 24GB class — overkill for our capped use |
| RTX 4060 Ti 16GB | 16 GB | **~$350–500** (used ~$300–450) | siliconcomps.com; gpuprix.com; bestvaluegpu.com | Cheap but **16GB cannot run 32B coder** — rules it out for our load-bearing model |

**Reality check on the task's capex assumption:** the brief said "~$800-ish capex." In 2026 the 24GB-class 3090 street sits at **~$1,200, not ~$800** (AI/local-LLM demand has held/raised prices). A $1,200 card amortized over 1 year ≈ **$0.137/hr** capex alone, **$0.201/hr** all-in at 24/7 — ~30% above the $0.155/hr the $800 assumption implies. Any breakeven below is built on stale pricing. Secondhand 3090 supply is a "value king" per craftrigs/locallmgear rankings, but it is a *king of value among GPUs*, not among our avenue set.

---

## 2. WHAT FITS 24 GB — local-model fit (QUOTED)

| Model | Size | 3090 speed (Q4_K_M, llama.cpp) | Fits 24GB? | Source |
|---|---|---|---|---|
| **Qwen2.5-Coder-32B** (our local-run coder) | 32B | **~28–37 t/s** (28.4 @275W, 32.8 @350W; ~55 t/s w/ speculative decoding) | **YES** (~19–21 GB Q4) | reddit.com/r/LocalLLaMA/.../1gp376v; .../1gxs34g; llmconfigurator.com |
| **GLM-4.7-Flash** (z.ai family, ~30B-A3B MoE) | 30B MoE | **~25–80 t/s** Q4 | **YES** | llmconfigurator.com/en/can-i-run/glm-4-7-on-rtx-3090; hackernoon.com/glm-47-flash-on-2x-rtx-3090 |
| GLM-Z1 / 32B variants | ~32B | ~25–80 t/s | YES | same |
| **Llama-3.3-70B** / dense 70B | 70B | **Q2_K/IQ2 ~8–12 t/s**; Q4 needs 40+GB → does NOT fit | **NO at Q4** (Q2 only, slow) | mustafa.net; gigagpu.com/can-rtx-3090-run-llama-3-70b; craftrigs.com |
| gpt-oss-120b (free-lane workhorse) | 120B | — | **NO** (needs ~63GB+) | vault manifest, size known |

**Honest read:** on a single 24GB card, the load-bearing local models are the **27–34B class at Q4 (25–80 t/s)** — not the 70B/120B class. That is exactly our existing local-run set: **Qwen2.5-Coder-32B (the vault's "local-run coder") and GLM-4.7-Flash (the $0-marginal backbone).** A 70B dense needs a second 3090 or aggressive Q2 (8–12 t/s — too slow for interactive Hands work). So a 24GB card upgrades our *local-run ceiling* from 7B (current ollama gemma/qwen/2.5-coder:7b) to 32B — a 4× model-class jump — but it does NOT bring 70B/120B local. That bound is a hardware reality, and it caps the "replace paid lanes locally" fantasy.

---

## 3. LORA / FINE-TUNING ON 24 GB (the new-capability section)

The vault's scarce layer is exactly tuning sets (operator 20:15Z: "vault's scarce layer = tuning/fine-tune datasets + their LICENSE OBLIGATIONS"). A 24GB card makes fine-tuning a *capability* — which no API subscription sells at any price (there is no "fine-tune on someone else's weights then keep them forever" path in our lane set).

| Model size | QLoRA (4-bit base) on 24GB | Standard LoRA (FP16) | Note |
|---|---|---|---|
| **7B** | **~5–12 GB — easy** | ~18–22 GB (fits) | comfortable batches; Unsloth ~2–5× faster / ~40–70% less VRAM |
| **13B** | **~10–20 GB — workable** | ~28–40 GB → **OOM on single 24GB** | QLoRA + grad-checkpointing + Flash-Attn + paged-AdamW |
| >13B / full FT | — | — | not practical on one 24GB card |

Sources: gigagpu.com/rtx-3090-for-ai-training; gigagpu.com/rtx-4090-fine-tuning-guide; compute-market.com/blog/best-gpu-for-fine-tuning-llm-2026; insiderllm.com/guides/what-can-you-run-24gb-vram; presenc.ai/research/local-llm-fine-tuning-hardware-requirements-2026; craftrigs.com/guides/fine-tuning-7b-llm-consumer-gpu-unsloth-lora.

**What the vault's tuning-set work would need:** the operator's banked recipe sets (e.g. Steiniger's 569-example Athena set) are 7B–13B-scale — **QLoRA on 13B fits a single unused 3090 with room.** A few-hours-per-epoch training loop (~10K samples, 2048 seq) on a 3090 is realistic. This converts the vault from a *passive mirror* (we store weights) into an *active forge* (we retrain) — the one thing in this entire radar that a GPU buys and no subscription sells.

---

## 4. POWER DRAW (UNVERIFIED assumption flagged)

- **Draw under load:** ~350W TGP (real-world gaming 355–365W; stress ~450W peaks) — techpowerup/unanswered.io/r/Furmark refs.
- **US residential cost:** national average **18.3–18.4 ¢/kWh** (EIA, 2026). ⚠️ **UNVERIFIED for the operator** — we do not know the operator's actual utility rate. Band: ~13 ¢/kWh (cheap states) to 30+ ¢/kWh (CA/HI/NE).
- **Cost/hr at 350W:** 0.35 × $0.183 ≈ **$0.064/hr (6.4¢)**; at 30¢/kWh ≈ $0.105/hr. Idle ~15–20W (near $0). At our realistic 8h/day the electricity is **~$0.51/day** at national avg — real but not decisive vs. the $1,200 capex amortization.

---

## 5. RENT vs OUR CAP — the covenant-cap finding (QUOTED)

This is the sharpest number in the pool: **the market has a blade at or below our covenant cap.**

| Provider | 3090 on-demand $/hr | vs cap $0.12 | Source |
|---|---|---|---|
| **vast.ai** (marketplace) | **$0.09–0.116** (cheapest ~$0.10; spot ~$0.07–0.08) | **AT/BELOW cap** | computeprices.com/providers/vast/gpus/rtx3090; getdeploying.com/gpus/nvidia-rtx-3090; gpufinder.dev/gpu/rtx-3090 |
| RunPod Community | $0.22 | ABOVE | computeprices.com/providers/runpod/gpus/rtx3090; runpod.io/gpu-models/rtx-3090 |
| RunPod Secure | $0.50 | ABOVE | same |
| Market median | ~$0.17 | ABOVE | getdeploying.com |

**Meaning:** we already have a covenant-compliant rental path for 24GB burst (vast.ai on-demand at $0.10 ≤ $0.12 cap), and an even cheaper spot tier ($0.075). So the decision is **not "own vs nothing" — it's "own vs vast.ai on-demand/spot," and vast is cheap.** Ownership must clear that bar, not just clear the cap.

---

## 6. OWN-vs-RENT BREAKEVEN (the line the operator asked for)

**Assumptions:** used 3090 capex **$1,200** (2026 street, §1); power $0.064/hr at 350W (flag: rate UNVERIFIED); no resale/failure/PSU-upgrade modeled (would worsen own); blade rates per §5. **Breakeven hours = capex ÷ blade_dph.**

| Blade scenario | $/hr | Breakeven hrs | **@4h/day** | **@8h/day** | **@24h/day** |
|---|---|---|---|---|---|
| vast.ai on-demand | 0.10 | 12,000 | **100.0 mo** | **~50.0 mo** | **~16.7 mo** |
| vast.ai spot | 0.075 | 16,000 | 133 mo | 66.7 mo | 22.2 mo |
| covenant cap | 0.12 | 10,000 | 83 mo | 41.7 mo | 13.9 mo |
| RunPod community | 0.22 | 5,455 | 45.5 mo | 22.7 mo | **7.6 mo** (beats rent only here) |

**Read the line:** ownership only beats the cheap rental at **sustained 24/7 load against the expensive providers** (RunPod community, ~7.6 mo payback). Against vast.ai on-demand — our covenant-compliant default — a 3090 **never pays back in practical fleet life** (50 mo at 8h/day). At 8h/day (generous for a capped off-peak fleet) even the richest scenario is 22+ months. **Hardware as a cost play is dead on arrival; hardware as a *capability* play (fine-tuning + sovereignty + ceiling-removal) is the only live thesis.**

All-in own cost/hr for comparison: $1,200 card ≈ **$0.201/hr at 24/7** (vs vast $0.10, runpod $0.22). At $800 capex it'd be $0.155/hr — still above vast.

---

## 7. MAP TO OUR SEATS (the analysis that matters)

| Seat | What a 24GB GPU serves | Verdict |
|---|---|---|
| **Tail** (unlimited scut) | Endless inference past every free-tier TPD/RPM/429 ceiling; glm-4.7-flash / qwen2.5:32b as the base | **STRONG ceiling removal** — Tail's only real constraint is quota, and local burns quota-free (electricity only). This is the cheapest pure win. |
| **Hands** (coding labor) | qwen2.5-coder-32B local at ~30 t/s as a DS-flash *fallback/parallel* lane; not a quality replacement | **WHERE/odd** — qwen-coder-32B at Q4 is good-but-not-frontier vs DS-flash; it buys *concurrency* (unlimited local fan-out) more than quality. Do not pitch it as a DS-flash replacement — it isn't. |
| **Probe lane** | unlimited banked-model probes (vault passport pipeline runs on banked weights off-peak) at $0 marginal | **STRONG** — the vault's §Tier-A probe loop currently rides cpu-ollama (slow). A 30 t/s card makes the probe pack actually runnable. |
| **Vault (fine-tune)** | QLoRA 7B–13B on a training set we own forever | **UNIQUE — the single thing no subscription sells** (§3). This is the load-bearing capex justification. |
| **Standing self** | local cache-of-identity, offline | minor (host already does this). |

**Ceiling-removal precision:** the fleet's measured ceilings are quota/RPM/TPD on the free lanes (groq 30RPM/200K TPD, cerebras 5RPM/1M TPD) and rate/window discipline on paid ones. A local card zeroes those for scalar/bulk/mechanical work at ~$0.064/hr. It does **not** zero the corridor for frontier/Brain work — a 24GB card locally tops out at 32B, which is below the 5.3-flash/DS-Pro-class Brain quality.

---

## 8. HONEST FRAME — what it buys / does NOT buy

**What a GPU DOES buy:**
1. **Ceiling removal** — unlimited local inference past every free-tier TPD/RPM/429 wall; no quota polling, no window discipline for Tail/probe bulk.
2. **Privacy / offline sovereignty** — the operator's whole thesis: weights on a disk we hold keys to (age-encrypted per vault law), zero exfiltration surface, works offline. **No API path can ever offer this.**
3. **Fine-tuning** — QLoRA 7B–13B into a permanent asset; the vault Forge. **No subscription in our lane set sells this.**
4. **Permanent asset** — a $1,200 card is still a card after the other avenues' credits vanish; it survives free-tier rate changes.

**What it does NOT buy:**
- **Quality replacement for paid lanes.** It does not beat DS-flash Hands ($1.33/day) on coding quality, nor 5.3-flash on judgment. Local 32B ≈ good workhorse, not frontier.
- **Frontier/Brain work locally.** No 70B/120B-class on a single 24GB card (§2). If the operator wants that offline, capex jumps to 2× 3090 (~$2,400, pooled 48GB at Q4 ~10–20 t/s).
- **Cost relief at realistic burst.** At 8h/day it pays back in 22–100 months vs the already-cheap vast.ai lane (§6). It does not reprice tokens.
- **Reliability/zero-ops.** Physical hardware fails, needs a PSU (500W+ system draw), cooling, and a home in the operator's rig; a rented blade has none of that.

---

## 9. VERDICT + JIT TRIGGER (pack-style)

**Under what measured demand does hardware beat every other avenue?**
> When (a) the Tail/probe lanes are **consistently quota-starved** (free-tier TPD/RPM ceilings hit on ≥2 consecutive ops retros), AND (b) the vault's fine-tune recipe sets are **ready and banked for a QLoRA 7B–13B run**, AND (c) the operator values sovereignty/privacy at ≥ the all-in cost. At that point the 3090 is not a cheaper token spigot — it is the cheapest *ceiling-remover + forge + offline-vault* bundle. If only (c) holds (sovereignty thesis alone), it still justifies — but that is a flagged, deliberate non-cost call.

**What to observe in the ops retro to trigger it (JIT, like the pack — no speculative purchase now):**
1. **Quota-hunger metric:** ≥2 consecutive weekly retros where groq/cerebras/OR free-tier ceilings are hit and work is *deferred or demoted* for quota, not quality → the Tail/probe lane is hardware-shaped.
2. **Forge readiness:** the operator's banked tuning-set recipes (Steiniger-class 569-example set and others in the vault §Tier-B) reach a *training-ready* state (cleaned, licensed, hashed) with a target 7B–13B model → the fine-tune capability has a first job.
3. **Sovereignty trigger:** operator says "do this X offline / never-hand-to-provider" for a recurring workload → privacy-based justification regardless of breakeven.
4. **Cap leak:** vast.ai on-demand climbs above ~$0.20/hr (blade inflation) while our burst hours stay high → own-versus-rent reopens in ownership's favor.

**Execution shape (if triggered):** buy ONE used **RTX 3090 (~$1,200)**, not a 4090/3090Ti (same 24GB class, higher capex), keep the 4060-Ti-16G off the list (can't run 32B). Integrate as a **local Tail + probe + Forge lane on the WSL2 cage** (Mag venv is Windows; cage = Linux WSL2 — see §10 stack note), leaving the cheap vast.ai lane in place as overflow. Reserve a resale-out at measured failure.

---

## 10. LOCAL-INFERENCE STACK on our host (2026, QUOTED)

**Windows host + WSL2 workaround is the standard 2026 path and is already half-built for us** (ollama already runs CPU on Windows; cage is Linux WSL2):
- **vLLM:** no native Windows — runs in **WSL2** with CUDA passthrough (uv-installable `pip install vllm`; serves OpenAI-compatible on :8000; continuous batching 2–20× Ollama at concurrency). — insiderllm.com/guides/wsl2-local-ai-windows-guide; github.com/vllm-project/vllm; fazm.ai/t/vllm-windows-support-2026.
- **llama.cpp / Ollama:** the fast single-GPU path; Ollama auto-detects CUDA in WSL2 and exposes :11434 OpenAI-compatible — our existing ollama wiring upgrades from 7B to 32B by pointing it at the card. — docs.ollama.com/windows; aleksandarhaber.com/.../wsl2-ollama; ggml-org/llama.cpp.
- **Key WSL2 rule:** install the **NVIDIA driver on the Windows side only**; never a Linux driver inside WSL2 (breaks passthrough); verify with `nvidia-smi`. — docs.nvidia.com/cuda/wsl-user-guide; ilirivezaj.com/tutorials/wsl2-cuda-setup.
- **Fine-tune stack:** Unsloth (2–5× faster, −40–70% VRAM) or LLaMA-Factory/Axolotl on the WSL2 cage for QLoRA 7B–13B. — craftrigs.com/guides/fine-tuning-7b... ; gigagpu.com/rtx-3090-for-ai-training.

**Bottom line for stack:** the operator's existing Windows/Mag + WSL2/cage layout is *already* the standard 2026 local-inference topology. Adding a 3090 to the WSL2 cage slots into the current ollama + vLLM path with no new architecture — a genuine integration advantage, not a rebuild.

---

## 11. FETCH LOG / RECEIPTS

| Q | Query | Added here? | Key cites |
|---|---|---|---|
| Q1 | used 3090/3090Ti/4090/4060Ti prices | §1 | pcprice.watch; bestvaluegpu; siliconcomps; gpudojo; dealhunter |
| Q2 | qwen2.5-coder-32B t/s on 3090 | §2 | reddit LocalLLaMA 1gp376v/1gxs34g/1hqlug2; llmconfigurator |
| Q3 | GLM/70B t/s on 3090 | §2 | mustafa.net; gigagpu 70b; craftrigs; hackernoon glm-47 |
| Q4 | LoRA tuning 24GB | §3 | gigagpu training/Fine-tune guides; compute-market; insiderllm; presenc; craftrigs unsloth |
| Q5 | 3090 power draw + cost/hr | §4 | techpowerup; unanswered.io; eia.gov (US avg 18.3¢ 2026) |
| Q6 | vast.ai / runpod 3090 $/hr | §5 | computeprices vast/runpod; getdeploying; gpufinder |
| Q7 | local stack Windows/WSL2/vLLM/Ollama | §10 | insiderllm; github vllm/llama.cpp; docs.nvidia.com wsl |

**Confidence tags:** street *prices* and *token/s* are QUOTED (aggregated trackers / r/LocalLLaMA benches) — directional ±10–20%, verify live if the JIT fires. Power **rate** is UNVERIFIED (we don't know the operator's utility rate — flagged). vast.ai spot is the one place the market dips meaningfully below our cap.

---

## 12. FINISH
- This file: `/board/HARDWARE_RADAR_20260901.md` (sha256 recorded in INDEX item, not inlined, per fleet practice).
- Copy: `/board/inbox/HARDWARE_RADAR_20260901.md` (byte-identical) + INDEX.json item appended.
- Ownership is NOT recommended today. Recommended: a JIT trigger (§9.2) that greases the tail/probe lanes until either (a) quota-hunger ≥2 retro streaks, (b) a fine-tune recipe is training-ready, or (c) the operator names a sovereignty workload. Until then the covenant-compliant vast.ai on-demand ($0.10 ≤ cap) is the strictly-better token spigot.
