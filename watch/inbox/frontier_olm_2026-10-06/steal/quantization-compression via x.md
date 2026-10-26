# STEAL CARD: BreadthKV port to the quantizer organ (arXiv 2610.05685)

- Area: quantization-compression via x
- Round 2 draft, 2026-10-06. Amended from round 1 per critique: freshness claim corrected (M1), fold-law caveat retracted and replaced with the banked PAIR anchor (M2), inherited constraints cited (M3), confidence figure marked unattributed (M4), probe reshaped so the cap actually bites and the readouts cannot lie (B1-B3).

## Provenance and freshness (corrected per M1 and M4)

This card banks the PORT, not the find. The paper is already banked end to end, same day, by three registers in this same inbox:

- KV lane: watch/inbox/frontier_olm_2026-10-06/sweep/kv-context-engineering-arxiv.md:24-25 marks 2610.05685 as a catalog digest-row only ("No sweep has deep-read any of the three; banking here adds the end-to-end read, ... from the KV side"), with the read receipt at :15-16 (one of six arxiv.org/html full reads, cross-checked against an export.arxiv.org API pull) and the bank at :40.
- X lane: watch/inbox/frontier_olm_2026-10-06/sweep/quantization-compression-x.md:103-114 holds it as find 4 ("read end to end") with the same headline numbers.
- Quant lane: watch/inbox/frontier_olm_2026-10-06/sweep/quantization-compression-arxiv.md:31 already lists "BreadthKV (2610.05685, 0)" in its not-re-banked exclusion list.

Round 1's freshness line ("0 mining hits in memory/ and the prior sweep registers, so this is a fresh mechanism for the estate") is RETRACTED. The find's own overlap note scoped its grep to catalog, memory, and five PRIOR-day sweep dirs (x-sweep :279-285); the bank is same-day, same inbox. Corrected claim: the paper is banked; the mechanism (breadth-before-fidelity at constant KV bytes, end-to-end calibration over offline error proxies) is new to the QUANTIZER organ, and no sibling steal card owns the port: grep -rln "BreadthKV\|2610.05685" over watch/inbox/frontier_olm_2026-10-06/steal/ matched only this card (re-run this ask).

The find's confidence figure 0.95 comes from the ask's find JSON. It is not located on disk (the round-2 critique's deep grep of deep_reads.json, doors candidates files, and finding-ledger JSONs found no banked find JSON; not re-run this ask). Treat 0.95 as unattributed until the find JSON is banked.

## The find (verified this sitting: live abs page fetched round 1; snapshot state/arxiv/2026-10-06/2610.05685v1.txt read in full)

Single-author paper (Runguo Li, cs.CL, 2026-10-05). Decode-time KV compression splits one fixed byte budget two ways: fewer cached tokens at higher precision (eviction-first) versus more tokens at lower precision (breadth-first). Claims, every quote cross-checked verbatim against the abstract:

- BreadthKV scores above eviction alone in 17 of 18 settings (3 reasoning models, 4 math and science benchmarks) and produces shorter outputs.
- Bit-width is picked per model and budget by a 60-problem end-to-end calibration, "since offline attention error does not predict it reliably".
- Reliability is where eviction dies: "eviction sends 91% of AIME samples to the cap and BreadthKV 40%" (Qwen3-8B, tightest budget). Derailed runs keep reasoning until the length cap without reaching an answer.
- Under the same protocol BreadthKV is statistically indistinguishable from RDKV, a joint rate-distortion allocator that uses 27% more KV memory-time, and it outperforms the authors' ThinKV re-implementation.

The KV lane's fuller end-to-end read (kv-context-engineering-arxiv.md:40) adds the mechanism detail this card's abstract-only basis lacked: pooled +17.4 pp over eviction-only; Qwen3-8B AIME25 at B=512: SnapKV-D 5.8% vs FullKV 65.4%, BreadthKV 62.9% at B=1024 on 0.10x FullKV memory-time; the bit optimum is model- and budget-dependent (Qwen3 2 bits everywhere, R1-Qwen 3@B512 / 4@B1024, R1-Llama 3/2) and calibration beats always-4-bit by 4.5 pp; 1.25-bit collapses to 0-12% calibration accuracy; an oracle evictor still loses about 13% of future attention mass at 10% retention, yet quantize-plus-evict beats oracle eviction end to end at every byte ratio; the derailment diagnostic is stall-token frequency ("wait" 6.4 vs 3.7 per 1000 tokens: eviction deletes the evidence that a result was verified, so the model re-derives endlessly); Triton int4 decode kernel 1.70 ms vs 1.63 ms fp16 FlashAttention at 32K on H200.

## The mechanism (what we steal, stated as a rule)

At a fixed KV byte budget, buy token COUNT at reduced per-token precision before buying per-token FIDELITY. The cost of eviction-first compression is run death, not marginal quality on finished runs: generations derail past the cap without terminating. And the safe bit-width is workload-specific, chosen by end-to-end task calibration, never by offline attention-error proxies.

## Estate anchor: the gate is banked doctrine (M2, retraction of round 1's caveat)

Round 1 called the "run-reliability-before-solvability" linkage "the finder's gloss, unverified here" after grepping only docs/ and memory/. That was too narrow a scope and the conclusion was false. The gate is banked estate doctrine: PAIR (arXiv 2609.36526), law "compression degrades reliability before solvability", banked at watch/inbox/frontier_olm_2026-10-05/steal/quantization-compression via arxiv.md:9 (find provenance) and :35 ("FIND 1, THE GATE (PAIR, 2609.36526)"), with the StealCard row at frontier_olm_2026-10-05/register.jsonl:13. The x-sweep find text this card inherited even carried the pointer ("banked 2609.36526", quantization-compression-x.md:113-114); round 1 failed to chase it. BreadthKV is the KV-bytes measurement of the PAIR gate: derailed-until-cap (91% vs 40%) is what reliability-before-solvability looks like when the compressed surface is the decode-time KV cache. Organ separation: the 10-05 card feeds tools/thought_quantizer.py compile gates; this card feeds mag/state_quantizer.py and mag/llama_cpp_bridge.py, which that card never touched.

## Estate map (organ it feeds and the concrete port moves)

- Quantizer organ: mag/state_quantizer.py:249-273 quantize_state() folds verkle_tail=50 knots into ONE QuantizedMemory summary knot (the N:1 aggregation), injected via QuantizedMemory.to_agent_context (mag/state_quantizer.py:400-432). That is eviction-first state compression: high fidelity per retained knot, massive count loss. Port move: a breadth mode at constant injected-context bytes: the recent 50 knots keep full summary fidelity, an older tail (roughly 150) rides as one-line digests, and the mode is scored by a consumer-side task probe (does an agent answering from the breadth render act identically on a held task set), never by summary-pretty metrics. This inherits the Q5 instrument law below.
- KV surface: mag/llama_cpp_bridge.py:90-102 spawns llama-cpp-python 0.3.36 with a hard-coded --n_ctx 2048, and :171-174 builds Llama(n_ctx=2048) hard-coded per call. Port move: expose n_ctx and KV type as bridge config so lanes can run breadth KV. Today the bridge cannot express an equal-byte tradeoff at all (both knobs hard-coded, B3), which is itself a finding.
- Doctrine anchors: "full fidelity only at load-bearing (the quantization-architecture law)" (mag/vram_hologram.py:127, right-sizing at :125-128 and :86-93); auto_quantize's LAWS "Anomalies are NEVER quantized" and "Variance determines resolution" (mag/auto_quantize.py:22-23) are the in-repo adaptive-resolution and reliability-first carve-outs; the PAIR gate above is the reliability-before-solvability law this paper measures for KV bytes.
- Inherited constraints this card rides (M3): lens/burns.md:59 banks B4's measured KV rung (q8_0 decode 100.8 vs f16 55.9 t/s: low-bit KV carried no speed tax on this estate's hardware, measured, not assumed); the Q5 instrument law (kv-context-engineering-arxiv.md:57) requires the owed KV A/Bs to score task-level probes end to end, never offline PPL, the same law the quant lane set for the weight-side qwen2.5:7b A/B ("stays OWED locally", sweep/quantization-compression-arxiv.md:62-63).
- Path note: the find's overlap note and the x-sweep (:106) name the snapshot as state/arxiv/2026-10-05/2610.05685v1.txt; that path does not exist on disk (ls this ask: "No such file or directory"). The snapshot lives at state/arxiv/2026-10-06/2610.05685v1.txt (catalog/catalog.jsonl:1071100, id 41f4600481f5, 1325 bytes, mtime 2026-10-06T06:30:05Z; file read in full this sitting).

## Falsifiable probe (reshaped per B1-B3: make the cap bite, read from returns, one load per arm)

What round 1 got wrong: generate_move defaults max_tokens=256 (mag/llama_cpp_bridge.py:153) and both arms held n_ctx (1024/2048) far above prompt+256, so neither arm ever hit the cap or evicted; as designed it degenerated into a q8_0 quality check that could not test the breadth mechanism. Reshaped:

- Harness: a standalone probe script that constructs llama_cpp.Llama directly per arm (not through generate_move, whose Llama construction at :171-174 is hard-coded and per-call, so riding it would reload the model every round and could not vary n_ctx without a code edit). One Llama instance per arm, N generations each.
- Task: 20 short math word problems (each with a known integer answer) with instructions to reason step by step and end with a parseable "ANSWER: <n>" line, tuned so correct reasoning needs roughly 350-600 generated tokens. 20 is the estate's cheap cut of the paper's 60-problem calibration; the scale-down is stated, not hidden.
- Arm A (eviction/depth proxy): n_ctx 384, type_k = type_v = GGML_TYPE_F16. With a ~60-token prompt, A has roughly 320 tokens of headroom, so a large share of runs hit the context cap mid-reasoning. Cap behavior of this wheel (exception vs silent truncation vs stop) is an owed byte-prove (probe step 1), logged per run, in the spawn-compat discipline of mag/llama_cpp_bridge.py:81-89.
- Arm B (breadth): n_ctx 768, type_k = type_v = GGML_TYPE_Q8_0. GGML q8_0 stores 32 int8 values plus 1 fp16 scale per 32 elements (34 bytes vs f16's 64 bytes per 32 elements), so B holds twice the tokens in approximately the same KV bytes. Byte parity is approximate (q8_0 is 34/64, not exactly 1/2); the probe logs the ratio it assumed and treats the residual as noise against a completion-rate margin, not as equality.
- Readouts, all computed in the probe's own loop from the raw generate returns: (1) end-to-end completion rate: share of runs producing the correct ANSWER line (task-level scoring per the Q5 law, never perplexity); (2) cap-hit/derail rate: share of runs ending without ANSWER (exception, truncation, or max_tokens exhausted mid-reasoning), the 91-vs-40 analog; (3) tokens/s per arm, against the banked burns.md:59 prior. Readouts deliberately avoid benchmark_bridge: its fallback field (mag/llama_cpp_bridge.py:273) is computed over the constant list [{"ok": False}] * rounds rather than over results, so it returns True regardless of what the runs did (read and confirmed this sitting); its latency fields are real but the probe computes its own anyway.
- Prediction (falsifiable, the paper's shape at toy scale): B's completion rate exceeds A's by a material margin at equal KV bytes, with no decode-time regression beyond noise (prior: q8_0 measured faster than f16 on this estate). Falsifier: A and B complete at indistinguishable rates, or B's answers degrade where both complete. Either outcome banks: one installs a breadth KV mode on the bridge and a breadth fold in state_quantizer, the other bounds the steal to long-CoT 8B-class lanes and leaves the estate's depth-first fold standing.
- Step 0, run this ask: .venv/Scripts/python.exe -c "import llama_cpp, inspect; print(llama_cpp.__version__); print('type_k' in inspect.signature(llama_cpp.Llama.__init__).parameters, 'type_v' in inspect.signature(llama_cpp.Llama.__init__).parameters)" returned 0.3.36, True True. And: .venv/Scripts/python.exe -c "import llama_cpp; print([c for c in dir(llama_cpp) if c.startswith('GGML_TYPE') and ('Q8_0' in c or 'F16' in c)])" returned ['GGML_TYPE_F16', 'GGML_TYPE_Q8_0']. Step 1, owed: a smoke spawn with type_k = GGML_TYPE_Q8_0 and one generation, to byte-prove the wheel compiles the KV-quant path (enum presence is not compile proof). No model has been run for this probe; that remains honest unknown.

## Citations

- https://arxiv.org/abs/2610.05685 (fetched round 1 of this ask set, 2026-10-06)
- state/arxiv/2026-10-06/2610.05685v1.txt (abstract snapshot, read in full this sitting)
- catalog/catalog.jsonl:1071100
- watch/inbox/frontier_olm_2026-10-06/sweep/kv-context-engineering-arxiv.md:15-16, :24-25, :40, :57
- watch/inbox/frontier_olm_2026-10-06/sweep/quantization-compression-x.md:103-114, :106, :279-285
- watch/inbox/frontier_olm_2026-10-06/sweep/quantization-compression-arxiv.md:31, :62-63
- watch/inbox/frontier_olm_2026-10-05/steal/quantization-compression via arxiv.md:9, :35
- watch/inbox/frontier_olm_2026-10-05/register.jsonl:13
- watch/inbox/frontier_olm_2026-10-06/lens/burns.md:59
- mag/llama_cpp_bridge.py:81-89, 90-102, 152-201, 171-174, 259-273 (fallback defect at :273)
- mag/state_quantizer.py:249-273, 400-432
- mag/auto_quantize.py:22-23
- mag/vram_hologram.py:86-93, 125-128
