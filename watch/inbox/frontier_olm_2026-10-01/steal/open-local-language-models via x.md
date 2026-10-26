# STEAL CARD: open-local-language-models via x (2026-10-01, round 2)

Area: open-local-language-models via x
Banked by: steal gopher seat, frontier_olm_2026-10-01 workflow. Round 1 landed 14:13; round 2 rewritten against the round-1 critique.
Verification note: every external claim below was re-fetched by this seat on 2026-10-01 (WebFetch) unless the line says ASK-SOURCED or CRITIQUE-VERIFIED (the round-1 critique re-fetched the Ollama blog and dated it September 29, 2026, resolving this card's former OWED date item; that re-fetch is cited, not re-run). Estate claims cite path:line read this seat. Local claims name the exact command run this seat.

## 0. Round 2 corrections ledger (what the critique caught, what changed)

1. R1: section 1.1 was labeled NEW; the same announcement is HELD from the 09-30 window (frontier_olm_2026-09-30/sweep/open-and-local-language-models-hn.md:54, read this seat, carrying MORE detail than round 1 had: ~4-token outputs, one call answering all named questions, the classifier demystification). Relabeled 09-30-HELD; this card's true delta is named inline.
2. R2: section 1.2's HF fact was already banked 09-28 and cross-banked by the sibling reddit card 11 minutes before this card's round 1. Cross-cited; this card's unique carries named inline.
3. M1: the E1 two-runtime A/B now AMENDS the estate's held measurement instrument (tools/abliterate_p1_probe.py) and its Sep-29 baseline instead of standing fresh.
4. B1: the round-1 probe presumed a logged clerk/classify ask corpus. This seat ran the check and it does not exist in logs/usage.jsonl (command and counts in section 3). Probe restated on a synthetic corpus with a rule-classifier floor arm.
5. B2: probe gains a step-0 schema-conformance request, because the no-client-rewrite steal was earned for the sglang server, not Ollama.
6. B3: the 0.34.3 -> 0.35 upgrade is a state change on the shared janitor host; probe gains a quiet-window and rollback note.
7. M3: this card was absent from INDEX.json while both siblings were registered (verified: INDEX.json:14553 via reddit, :14577 open-local-language-models.md, zero hits for this path). INDEX rebuilt this round; result recorded in section 4.
8. S1 (carried, script owner): the steer ask in .zcode/workflows/olm-mine.dwf.ts never receives the prior card JSON. Verified this seat by reading lines 388-394: `lastCard = card;` is assigned and the steer ask string names "the returned card JSON" but interpolates only the file path. Fix belongs to the workflow script (interpolate JSON.stringify(lastCard)); the sibling round-2 card carries the same defect.

## 1. The steal, as mechanisms

### 1.1 Typed decision models in Ollama 0.35: 09-30-HELD, this card adds the doctrine coupling, the port map, and the probe

HELD GROUND (09-30 window, read this seat): frontier_olm_2026-09-30/sweep/open-and-local-language-models-hn.md:54 banks the whole landing: "typed decision models landed natively in Ollama 0.35 (2026-09-30, /v1/systemone endpoint) with three models: nimble 9B (Bespoke Labs), tev1 4B and tev1:0.8B (Together AI, experimental). Vendor claims 91 ms per decision on an M5 Max, ~4-token outputs, one call answering all named questions - verbatim: 'Send text as state with a set of named questions, and a model running on your machine answers them all in one request.'" That sweep also carries the demystification guard this card adopts into its falsifier: per hbrn, "'Decision model' is just marketing jargon. decision model = classifier... system one model = small non-reasoning LLM"; the Ollaya author conceded their 421M ModernBERT Laya is "well below Jev on harder queries"; Kev/decider (Qwen-based, 0.8B-35B) approach Jev quality. CRITIQUE-VERIFIED: the Ollama blog itself is dated September 29, 2026, and the typesafe_sdk question exports (choice/noul/score) match the held CHOICE/SCORE/NOUL primitive set.

The estate's own doctrine predates all of it: Jev = TypeSafe "System One", POST api.typesafe.ai/v1/systemone, model jev-1.13.0, 70-500ms, three primitives CHOICE / SCORE / NOUL, batched questions evaluated in parallel and in isolation (memory/research_packs/THE50_W3_T11_TYPED_DECISION_ORACLES.md:8-11), with the standing steal "stand a local Jev-compatible /v1/systemone behind the existing lane runner with no client rewrite; the A/B harness then only swaps base URLs" (same file :283-285). Read carefully: that no-client-rewrite steal was earned against the sglang replica server (same pack :275-277), NOT against Ollama 0.35. Whether Ollama's implementation honors batched named questions in one request is exactly what the probe's step 0 tests.

THIS CARD'S DELTA (the three things the 09-30 sweep did not bank):
(a) The lane-level port map: the scut target is pinned in code, not prose. mag/lanes.py:45 clerk = "gemma:2b", :48 router = "gemma:2b"; mag/task_router.py:13 "CLASSIFY tasks -> gemma:2b" and :147 the ("classify", "ollama", "gemma:2b", 0.0) tuple; mag/ollama_policy.py:16 JANITOR = os.environ.get("MAG_JANITOR_MODEL", "gemma:2b").
(b) The falsifiable probe with a schema-conformance gate (section 3).
(c) The port decision rule: gemma:2b stays JANITOR fallback; the decision-model endpoint can take the typed-decision traffic only after passing the three-arm bake-off.

Local feasibility, run this seat: `ollama --version` reads 0.34.3, so /v1/systemone is NOT live here until the upgrade; `ollama list` shows 15 installed models including gemma:2b (b50d6c999e59, 1.7 GB, 4 weeks old) as the incumbent janitor, and the keep-alive set mag/ollama_policy.py:18 ("gemma:2b,gemma4-desk,qwen-desk") is live VRAM policy the upgrade must not disturb (quiet-window note in section 3).

### 1.2 Same GGUF bytes, two runtimes: HELD since 09-28, cross-banked by the sibling card; the unique carries kept

HOLDING STATUS, fully stated: the estate has held "transformers runs llama.cpp quants" since 09-28 as pointers (watch/inbox/frontier_olm_20260928/sweep/quantization-compression-hn.md:20, items "49812339 + 49799125 Transformers now runs llama.cpp quants (09-23/09-22)"; :47 "Transformers now also runs llama.cpp quants directly (HF blog, 2 posts)" - both read this seat), and the sibling card banked the C1 mechanism connection 11 minutes before this card's round 1 (watch/inbox/frontier_olm_2026-10-01/steal/open-local-language-models via reddit.md:102 "Only the C1 mechanism connection was new", :109-121 the four-way provenance). The reddit sibling owns the "same-bytes two-runtime measurement design" framing.

THIS CARD'S UNIQUE CARRIES on top of the sibling:
(a) The measurement caveat the sibling does not carry: the HF blog's parity claim mixes conditions - "the Transformers measurement includes prefill while llama-bench reports decode-only throughput" (re-fetched this seat from https://huggingface.co/blog/transformers-llama-cpp-quants) - so any two-runtime comparison must align prefill and decode accounting before comparing numbers.
(b) The Windows posture: the packed ggml-kernel path is "MPS-only for now" (same blog), so on this host the transformers leg runs the fallback path, which "falls back to dequantizing the model and uses more memory" - the memory cost is the unmeasured OWED that decides whether the two-runtime A/B runs here at all.
(c) The rebase of the A/B onto the held instrument (section 1.3).

### 1.3 The censorship surface is runtime-relative; the A/B amends the held census probe, it does not stand fresh

Re-fetched this seat from https://blog.madhukaraphatak.in/non-destructive-refusal-supression-using-engram: dynamic abliteration on Qwen3-4B (bf16, A100/Colab), PyTorch forward hooks at TARGET_LAYERS = [12, 14, 16, 18, 20], 2,000 PKU-Alignment/PKU-SafeRLHF samples, loss ~3.92 (step 10) to ~1.77 (step 250) in "Elapsed: 8.92m", base weights frozen. Negative result carried: single-layer steering at layer 14 (ALPHA 1.2) FAILED, "the downstream layers reconstruct the refusal behaviour again"; suppression needed the multi-layer window.

This lands on the fork C1 already named: "Ollama cannot inject residual vectors; prompt-level rides existing instruments" (watch/inbox/hermes_burn/WINDOW1_STATE.md:24-25). The transformers loader from 1.2 is the injection path Ollama lacks: refusal behavior is a property of the pair (checkpoint, runtime), not the checkpoint.

THE INSTRUMENT ALREADY EXISTS (prior-art, read this seat): tools/abliterate_p1_probe.py is the estate's P1 refusal census - docstring :1 "ABLITERATUS P1 baseline refusal census - gemma:2b as-is via local ollama API"; :7-10 "Battery: 20 prompts from the fleet's own janitor task shapes" with "RUNS per prompt (default 3) through the same wire as mag/afk_loop.py:104"; :223 def classify(text, err) -> the verdict channel; :279 --model default "gemma:2b"; :323 emits "schema": "abliterate_p1_census.v1", lane "abliterate-p1". The Sep-29 baseline is banked at watch/inbox/ball2/abliterate_p1_runs.json (42,936 bytes, mtime Sep 29 11:07, ls-verified this seat). E1 therefore AMENDS this probe: same wire, same 20-prompt battery, same classify() verdict channel, same abliterate_p1_census.v1 schema, plus a runtime axis (ollama vs transformers-on-the-same-GGUF) - comparable to baseline by construction. The owed abliteration rib (WINDOW1_STATE.md:42-43) and the owed refusal-field banking (WINDOW1_STATE.md:55) ride the same amendment.

### 1.4 Tune config before any engine swap (the anti-churn guard)

Re-fetched from https://blog.mozilla.ai/benchmarking-local-llm-servers-llama-cpp-llamafile-lm-studio-and-ollama/: controlled multi-server benchmark (llama.cpp, llamafile, LM Studio, Ollama; identical GGUFs; Qwen 0.8B/9B/27B; Mac Studio M4 Max, L40S Linux box, Steam Deck OLED; "Each point ... is the result of 15 llama-benchy runs", middle 10 averaged) finds no engine winner and tens-of-percent configuration swings: Vulkan shader toolchain +63.3% prompt processing on the 9B, llamafile CUDA graphs +16.8% decode on the 0.8B, speculative-draft winner flipping by platform (draft 2 on Metal, draft 4 on CUDA, up to 16%), MLX artifacts +9.9%/+10.7% prompt processing on Apple silicon. Explicitly NOT measured: "time to first token, end-to-end latency, model-loading time, memory use, power consumption, or concurrent requests". Port: before any janitor engine change, including 1.1's swap, try config knobs on the incumbent first, and measure TTFT and per-decision latency yourself, because the public benchmarks do not. (Note: the 09-30 window already holds this Mozilla benchmark - open-and-local-language-models-hn.md:46, read this seat; this card keeps it for the decision rule, not as a novelty claim.)

### 1.5 The serving-stack confound program is peer-reviewed now

Re-fetched from https://arxiv.org/abs/2609.26693: "Measuring the Serving Stack Instead of the Model: Hidden Confounds in Local Tool-Use Evaluation", accepted at the REALM workshop @ EMNLP 2026. Verbatim: Ollama gates the default tools= request "per model by a static template flag" and "Phi-3 and Gemma-3 are rejected before inference"; cross-stack probes (Ollama, llama.cpp, vLLM, SGLang) "show different handling of the same request"; "turn-pooled versus per-instance estimates differ by up to about 55 points"; "Constrained decoding removes parse failures but can induce non-termination"; rejection and retry exhaustion are "not preserved as structured failure metadata", which can make an eval "naively report 0% fidelity". Port: the citation basis for C1's E1-E3 arms and the methodology law for every A/B in 1.1 through 1.3: per-instance scoring only, rejections banked as first-class rows, pre-inference rejection census before believing any capability number. (The estate's own abstract snapshot is already in catalog: catalog.jsonl:445316 per the ask; the full findings were digested nowhere before this card.)

### 1.6 Release radar (context, not janitor news)

Re-fetched via https://api.fxtwitter.com/AntLingAGI/status/2105335205741596911: "Meet Ling-3.1-flash: ~560B total params, ~25B active/token, up to 1M-token context." plus "We plan to open-source the model soon." (747,227 views, 1,964 likes at this seat's fetch; the ask's harvest read 734,816; numbers move). NOT janitor-class; it is the release-wave marker the RQ1 answer cites. The janitor-relevant conclusion stands as the ask framed it: in-window small-model churn is decision models and Qwen GGUFs, not a new 8B dense flagship. The GLM-5.4 / DSv4.1-pro leak lists (JulianGoldieSEO) stay ASK-SOURCED RUMOR, unverified, not ported.

## 2. Estate map (organ -> concrete port move)

| Organ | Anchor (read this seat) | Port move |
|---|---|---|
| gopher fleet (janitor/clerk lane) | mag/ollama_policy.py:16,18, mag/lanes.py:45,48, mag/task_router.py:13,147, tools/workflow_gate.py:14 (Mickey17 gopher fan-out) | After the section-3 probe passes, route typed-decision traffic (clerk CLASSIFY, router choices) to /v1/systemone (tev1:0.8b or nimble). The 09-30 sweep's guard applies: this is a classifier slot; it must beat a classifier-class baseline, not a chat baseline. gemma:2b stays JANITOR fallback. |
| sovereign mirror (C1 censorship program) | tools/abliterate_p1_probe.py:1,7-10,223,279,323; watch/inbox/ball2/abliterate_p1_runs.json; watch/inbox/hermes_burn/WINDOW1_STATE.md:24-25,42-43,55; docs/DOCTRINE_MAP.md:78 | E1 = AMEND the P1 census probe with a runtime axis (ollama vs transformers on the same GGUF), same wire, same classify() verdict channel, same abliterate_p1_census.v1 schema, comparable to the Sep-29 baseline. Refusals bank as first-class rows per 1.5 and the owed carrier defect (:55). |
| quantizer | mag/gguf_cartography.py, mag/auto_quantize.py (exist, grepped this seat) | Record Q4_K_M as the recommended starting quant beside the cartography notes with the prefill-vs-decode caveat attached; transformers becomes a second consumer of existing GGUFs. Windows fallback = dequant, memory cost unmeasured (OWED). |
| water graph | memory/continuity/seat_memory_20260927/go-wide-pass-20260927.md:35-36 ("every verb routes through WaterGraph") | Routed-verb A/Bs adopt the 1.5 checklist: per-instance scoring, rejection rows, never turn-pooled estimates (the 55-point gap is the standing falsifier of past pooled comparisons). |
| percolator | mag/percolator.py (exists, grepped this seat) | Promote as candidates: (a) the decision-model oracle lane spec WITH the sglang-vs-Ollama schema caveat, (b) the runtime-relative censorship fork with the 1.3 citations, (c) the config-before-engine rule. |
| context pack | mag/context_pack.py, docs/FRAMEWORK_LOAD.md:124 | One pack line: "janitor decisions: typed /v1/systemone after the 0.35 upgrade, gated on step-0 schema conformance; refusal A/B amends abliterate_p1_probe, needs the transformers runtime; never compare engines without TTFT plus per-instance scoring." |

## 3. The probe v2 (falsifiable, cheap, this week; restated per critique B1/B2/B3 + guard M2)

**Step -1 (quiet window):** the Ollama 0.34.3 -> 0.35 upgrade is a state change on the shared janitor host (15 installed models; keep-alive lane policy live at mag/ollama_policy.py:18). Run it in a quiet window with no desk/voice seats mid-session, note the current version for rollback (`ollama --version` -> 0.34.3 today), and re-verify `ollama --version` and `ollama list` after; installed model blobs survive version changes, the daemon binary is the rollback surface.

**Step 0 (schema conformance, gates everything):** one POST /v1/systemone request carrying a batch of three named questions (one CHOICE, one SCORE, one NOUL) against tev1:0.8b. Record whether the response returns typed decisions for all three in one call (the held doctrine's "batched questions evaluated in parallel and in isolation", THE50 pack :10-11) or whether Ollama's implementation only answers single questions or prose-wraps. If step 0 fails outright, the no-client-rewrite steal does NOT transfer from sglang to Ollama (it was earned for the sglang server, THE50 pack :275-285): bank that as the finding and stop; a thin adapter is the only fallback and it narrows the steal.

**Steps 1-2:** `ollama pull tev1:0.8b` (smallest of the trio).

**Step 3 (the bake-off, corrected corpus):** the round-1 premise is dead, verified this seat - logs/usage.jsonl (70,672,723 bytes, mtime Oct 1 13:40) contains ZERO clerk-lane or classify-action rows. Enumeration command run this seat (python json line-scan over logs/usage.jsonl): actions = brief 79,544 / provider_chat 77,609 / chat 6,851 / visual_pack 149 / ask 112 / multi_smoke 96 (no clerk, no classify action); lanes on provider_chat = L1 74,578 / L0 3,031; raw substring lines matching clerk|classify = 2,646, all inside detail text, none a logged ask with an outcome label. So the scoring target is restated: 50 synthetic CLASSIFY-shape triage items (estate-plausible routing asks across 4-5 lane labels), each labeled ONCE by the operator-proxy seat before any model runs. Three arms on the identical 50 items: (a) a keyword/rule classifier as the floor (the M2 guard: a decision model must beat a classifier, per "decision model = classifier", 09-30 sweep :54), (b) gemma:2b incumbent via the existing chat lane, (c) tev1:0.8b via /v1/systemone. Score per-instance agreement with the labels (never turn-pooled, per 1.5) plus mean ms/decision on this box.

**Falsifier (fires on any one):** tev1:0.8b fails to beat BOTH the rule-classifier floor and gemma:2b on the same 50 items; OR mean decision latency exceeds 500ms on this Windows box (the 91ms figure is a vendor M5 Max demo claim, not a triage benchmark and not this hardware); OR step 0 shows the batched-question contract is not honored and no thin adapter closes it within a day. On any fire: the swap is REFUTED, gemma:2b stays JANITOR (mag/ollama_policy.py:16), and the numbers bank. Cost: $0 (local), roughly two hours including the quiet-window upgrade.

## 4. OWED / not verified

- INDEX registration: this card was absent from INDEX.json (verified this seat: rg over INDEX.json shows the via-reddit sibling at :14553 and open-local-language-models.md at :14577, zero hits for this path). Heal attempted this round via the sanctioned writer; result recorded here after the rebuild runs (see the run log at the bottom of this file).
- tev1/nimble license terms: not read. OWED, blocks any product-lane bake.
- The transformers-GGUF fallback path's memory cost on this Windows box (MPS-only packed path does not apply here): unmeasured. OWED, one config run.
- A real logged clerk/classify ask corpus with outcome labels: does not exist in logs/usage.jsonl (verified, section 3). If one exists elsewhere (mag/task_router.py runtime logs, mag/lanes.py lane logs), OWED to locate before replacing the synthetic corpus.
- HN thread 49831201 (the abliteration discussion, 108 pts): not fetched; the projected-direction critique rides the ask's summary.
- GLM-5.4 / DSv4.1-pro leak lists: ASK-SOURCED RUMOR, unverified, not ported.
- S1 script defect (carried, script owner): .zcode/workflows/olm-mine.dwf.ts:390-393 assigns lastCard but the steer ask interpolates only the file path, so the reviewer seat never sees the prior card JSON. Fix: interpolate JSON.stringify(lastCard) into the steer ask string.

## 5. Sources

External (re-fetched by this seat 2026-10-01 unless noted):
- https://ollama.com/blog/ollama-now-supports-jev-style-decision-models (CRITIQUE-VERIFIED for the Sep 29, 2026 date and typesafe_sdk choice/noul/score exports; round 1 fetched content)
- https://x.com/ollama/status/2105152056382345544 (re-fetched via api.fxtwitter.com/ollama/status/2105152056382345544)
- https://huggingface.co/blog/transformers-llama-cpp-quants
- https://blog.madhukaraphatak.in/non-destructive-refusal-supression-using-engram
- https://blog.mozilla.ai/benchmarking-local-llm-servers-llama-cpp-llamafile-lm-studio-and-ollama/
- https://arxiv.org/abs/2609.26693
- https://x.com/AntLingAGI/status/2105335205741596911 (re-fetched via api.fxtwitter.com/AntLingAGI/status/2105335205741596911)

Estate (path:line, read this seat this round unless noted):
- watch/inbox/frontier_olm_2026-09-30/sweep/open-and-local-language-models-hn.md:54 (09-30 HELD ground + demystification guard), :46 (Mozilla benchmark held)
- watch/inbox/frontier_olm_20260928/sweep/quantization-compression-hn.md:20,47 (HF fact held since 09-28)
- watch/inbox/frontier_olm_2026-10-01/steal/open-local-language-models via reddit.md:102,107-121 (sibling cross-cite, four-way provenance)
- tools/abliterate_p1_probe.py:1,7-10,223,279,323 (held E1 instrument); watch/inbox/ball2/abliterate_p1_runs.json (Sep-29 baseline, 42,936 bytes)
- memory/research_packs/THE50_W3_T11_TYPED_DECISION_ORACLES.md:8-11,275-285 (Jev doctrine; sglang-earned no-client-rewrite steal)
- watch/inbox/hermes_burn/WINDOW1_STATE.md:24-25,42-43,55
- mag/ollama_policy.py:16,18; mag/lanes.py:45,48; mag/task_router.py:13,147; mag/gguf_cartography.py; mag/auto_quantize.py; mag/percolator.py; mag/context_pack.py; docs/FRAMEWORK_LOAD.md:124; docs/DOCTRINE_MAP.md:78; memory/continuity/seat_memory_20260927/go-wide-pass-20260927.md:35-36; tools/workflow_gate.py:14; catalog.jsonl:445316 (per the ask, not re-opened)
- .zcode/workflows/olm-mine.dwf.ts:388-394 (S1 defect, read this seat)
- logs/usage.jsonl (70,672,723 bytes; action enumeration run this seat, section 3)

## 6. Round 2 run log

- Card rewritten and banked at watch/inbox/frontier_olm_2026-10-01/steal/open-local-language-models via x.md.
- INDEX heal: `.venv/Scripts/python.exe -m mag.shared_surface rebuild` run this seat, returned "ok": true with 1,325 top_level_files / 2,419 active_items (warnings only: out-of-inbox register events and past-2^53 seq demotions, pre-existing). Verification: rg over watch/inbox/INDEX.json finds this card registered at INDEX.json:14715 as path "frontier_olm_2026-10-01/steal/open-local-language-models via x.md". M3 closed.
