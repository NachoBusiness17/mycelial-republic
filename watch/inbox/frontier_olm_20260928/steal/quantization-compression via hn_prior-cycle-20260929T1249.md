# Steal card draft 1: quantization-compression via hn

Area: quantization-compression via hn. Round 1, first draft, no prior critique. Both finds were source-fetched by the finder on 2026-09-28 via Hacker News (Algolia search_by_date + relevance) and the HN item threads; this seat re-verified the sources on-page and re-ran the estate-side overlap checks on 2026-09-29 (commands and outputs listed under Checks). Anything this seat could not verify is marked OWED, never asserted.

## Find 1: the Qwen3.8 27B quant ladder (quesma, 2026-09-08)

URL: https://quesma.com/blog/qwen38-27b-quantizations-benchmarked/

Re-verified on-page by this seat 2026-09-29 via WebFetch (two fetches, second answered from the 15-minute cache):

- Verbatim hit: "Yet the 17 GB Q4_K_M matches the full model on a popular agentic coding benchmark, Terminal-Bench 2.1."
- Verbatim hit: instruction-following shows "no change between models, down to a decent 2-bit one, weighing less than 11 GB."
- Verbatim hit: "At 1 bit, the model performs around random chance on GPQA Diamond, and longer reasoning makes it worse."
- Benchmark suite named on-page: GPQA Diamond, IFBench, Terminal-Bench 2.1 ("Terminal-Bench 2.1 is a standard agentic benchmark, with 89 tasks"). Confirmed: there is NO dedicated tool-calling benchmark and NO JSON/structured-output benchmark in the suite. The finder's RQ1 gap claim is verified, and it names the exact hole an estate-side quant eval would fill.
- The page cites KL-divergence only to dismiss it as a proxy: "Measuring token prediction differences (KL-divergence, top-1 predictions) is easy, but it does not tell us whether the model gets worse at solving tasks." The finder's add that KL-divergence is dataset-dependent with agentic traces diverging far worse than wikitext is attributed to the HN thread comments, NOT the page: OWED (thread not fetched by this seat).

Mechanism to steal: a measured quant floor law for agentic work. Q4_K_M (4-bit GGUF) is the safe default that holds agentic coding; 2-bit is the instruction-following floor (flat from full precision down to 2-bit); 1-bit is collapse (random chance, and longer reasoning makes it worse). Quant selection must be judged on agentic task benchmarks, never on perplexity or KL proxies, because the proxies do not predict task loss.

Why it lands here: the estate runs local janitors (gemma:2b scut, gemma4 short worker per AGENTS.md) and its quantizer organ family compresses everything EXCEPT model weights. Confirmed organs: mag/state_quantizer.py:1 (State Quantizer, compresses Verkle lattice into dense memory states, schema state_quantizer.v1 at :27), mag/auto_quantize.py:1 and :110 (AutoQuantizer, adaptive resolution for analytics data, storage-savings report at :353), and tools/thought_quantizer.py, which compiles fleet law into packs (memory/corpus/quantized_thought/compile_report.json, read this session: v0.4, compiled 2026-09-29T15:18:39Z, 401 laws in, 374 kept, packs frontier 24 / flash 12 / local 338). memory/research_polished/kv_cache_compaction.md:23 lists "bare-metal steal (own quantized runtime / kernel layer) unexecuted". So the estate's FIRST weight-quant decision is still ahead of it, and it should inherit this ladder instead of guessing.

Organ fed: quantizer organ (thought quantizer law stream) plus the gopher fleet's local tier. Concrete port move: (1) file the floor law (Q4_K_M default for agentic scut, 2-bit floor for instruction-following, 1-bit never) into the thought quantizer's input stream so it compiles into the flash/local packs delivered at mag/context_pack.py:1142 ("### L0b Compiled laws (thought quantizer, flash tier - obey)"); (2) add a quant-level axis (same model at current quant vs Q4_K_M vs 2-bit) to the next tools/tier_probe.py run, scored on a fixed slice of real seat tasks (catalog tagging, lint summaries), so the ladder becomes the estate's own measurement. Bonus target: the suite gap (no tool-calling/JSON benchmark) is exactly what the estate's own eval slice would cover, since seat work is JSON-shaped.

Secondary probe (needs Ollama, still cheap): serve the currently used local worker at Q4_K_M and at 2-bit, run 30 fixed prompts drawn from memory/corpus/quantized_thought/instructions_flash.jsonl, grade JSON-valid rate and exact match. Falsifies the port if 2-bit does NOT hold instruction-following on estate prompts, i.e. the flat-to-2-bit result fails to transfer off Qwen.

## Find 2: LRU is the champion, tool loops are the waste (agentic-kv-cache, 2026-09-10)

URL: https://github.com/gauravapiscean/agentic-kv-cache

Re-verified on-page by this seat 2026-09-29 via WebFetch of the repo README. All four headline numbers are verbatim hits:

- "I replayed 68,266 requests from 393 real Claude Code sessions and 23,608 Mooncake requests through a prefix-cache simulator"
- Policy ablation table: LRU-leaf 83.48% at 8,000 blocks. Precision note carried exactly: that ablation row is computed on 40 AgentX sessions, 4,751 requests, a subset of the replay corpus, not the full 91,874 requests.
- "Monotone negative. Every component made it worse, and the one I was most confident in, coherent eviction, was the worst." LFU and the +H/+HC/+HCG variants all underperform LRU-leaf. The title is the thesis: "LRU is harder to beat than the papers suggest."
- "The dominant source of cache misses here is tight two-second tool loops whose 88k-token working sets exceed cache capacity - a capacity problem, not a liveness-prediction problem." (em-dash in source replaced with hyphen here per house law; wording otherwise verbatim)

Mechanism to steal: the METHOD, not the number. Trace replay through a prefix-cache simulator, with radix-leaf LRU at the real budget as the free null arm, and ground-truth curve validation before any eviction candidate is believed. This is the independent external confirmation of the estate's own gap law, gap-fold G1 at memory/research_polished/kv_cache_compaction.md:13: "any eviction/compaction claim must beat LRU/ARC/PBKV/Belady-MIN arms or it is decoration." A team with 91,874 real requests arrived at the same verdict. The diagnosis half is as portable as the policy half: when the working set exceeds capacity, no eviction policy helps, the lever is capacity/budget/assembly, not a cleverer liveness predictor.

Organ fed: context pack. Concrete port move: replay the estate's own traces (dashboard/static/trails/*.jsonl, measured this session: day_work.jsonl 1,748 rows, builder.jsonl 1,206 rows, plus the db.sqlite transcripts named at kv_cache_compaction.md:28) through a block-level prefix-cache simulator at the context pack's real token budget. The resulting LRU hit curve becomes the null arm the governor eval bar already demands (kv_cache_compaction.md:28: "recency null first, threshold ablation, repeated-cycle decay, cache economics first-class, downstream task truth"). The frozen-prefix machinery to validate against already exists: mag/context_pack.py:489 has def freeze_system_prompt(, and :534-548 shows the repacked flag with the "## Auto-repack" tail marker. Doc-drift note: kv_cache_compaction.md:23 still lists freeze_system_prompt() as never built; the function is present at :489 today (grep run this session), so that owed item has landed since the doc's 2026-09-20 code check and the doc line is stale on this point.

Primary probe (this week, byte-cheap: pure local compute over existing files, no GPU, no API spend): compute radix-leaf LRU hit rate over the most recent 5,000 estate tape rows (trails jsonl + db.sqlite transcripts) at the context pack's actual token budget. Falsifiable claim: LRU at the estate's real budget already achieves 80%+ hit on estate traces (external reference: 83.48% at 8k blocks on the AgentX subset). If it holds, that measured number becomes the G1 null every future eviction/compaction proposal must beat or be rejected as decoration. If it does not hold, and per-session working sets blow past the budget the way the external 88k tool loops did, the correct fix is pack budget and assembly (freeze plus tail), not eviction policy. Either branch converts doctrine into a measured fact.

## Checks run this session (2026-09-29, exact commands and outputs)

1. grep -ci "quesma" catalog/catalog.jsonl -> 0. Finder's overlap claim confirmed.
2. grep -ci "agentic-kv-cache" catalog/catalog.jsonl -> 0. Confirmed. (First attempt at these greps misfired: this Bash tool runs Git Bash, so a cmd.exe-style backslash command was mangled into a whole-drive find scan; it was stopped within seconds via TaskStop and re-run with forward-slash paths. No repo state was touched, read-only greps only.)
3. wc -l < catalog/catalog.jsonl -> 674,146 rows today. The find's "581,477-row catalog" was the finder's 2026-09-28 fetch-time figure. Both named with their moments; never differenced across instruments.
4. WebFetch https://quesma.com/blog/qwen38-27b-quantizations-benchmarked/ -> claims 1-3 verbatim-confirmed; benchmark suite = GPQA Diamond, IFBench, Terminal-Bench 2.1; no tool-calling or JSON benchmark; KL thread-add NOT on page.
5. WebFetch https://github.com/gauravapiscean/agentic-kv-cache -> 68,266 / 393 sessions / 23,608 / LRU-leaf 83.48% at 8,000 blocks (40 AgentX sessions, 4,751 requests) / every component worse than LRU / 88k tool-loop working-set quote, all verbatim-confirmed.
6. grep -n "def freeze_system_prompt" mag/context_pack.py -> :489 present.
7. wc -l dashboard/static/trails/day_work.jsonl -> 1,748; builder.jsonl -> 1,206.
8. python os.listdir: mag/ holds auto_quantize.py, state_quantizer.py, tool_quant.py; watch/inbox/frontier_olm_20260928/steal/ exists and did not contain this card's filename before this write.

## OWED (not verified by this seat, marked, never asserted)

- KL-divergence dataset-dependence (agentic traces diverge far worse than wikitext): finder's HN-thread attribution; not present on the quesma page; thread not fetched this session.
- HN provenance chain (Algolia search_by_date + relevance, item threads): finder's method statement from the ask; item IDs not re-pulled here.
- This seat did not run the pytest suite for this card: nothing in the card changes code, so no test gate applies; the probes above are the runnables it proposes.
