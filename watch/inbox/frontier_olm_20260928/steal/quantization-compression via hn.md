# Steal card draft 1: quantization-compression via hn

Area: quantization-compression via hn. Round 1, first draft, no prior critique. Both finds were source-fetched by the finder on 2026-09-28 via Hacker News (Algolia search_by_date + relevance search) and the news.ycombinator.com item threads. This seat re-verified every load-bearing claim on 2026-09-29: both source pages via WebFetch, both HN threads via the Algolia search/items API, and every estate-side code citation by grep in this session (commands and outputs under Checks). Provenance note: a prior draft of this card sat at this exact path from 12:49 today (an earlier seat's session); it was preserved as "quantization-compression via hn_prior-cycle-20260929T1249.md" in this directory before this overwrite, per the directory's existing prior-cycle naming convention. Nothing from it is reused here without re-verification this session, and the two thread-carried claims it marked OWED are now verified at the source and cited (Find 1). Anything still unverifiable is marked OWED, never asserted.

## Find 1: the Qwen3.8 27B quant ladder (quesma, 2026-09-08; HN item 49611128, 286 points, 139 comments)

Source: https://quesma.com/blog/qwen38-27b-quantizations-benchmarked/
Thread: https://news.ycombinator.com/item?id=49611128

Re-verified on-page this session via WebFetch; the headline claims are verbatim hits:

- "Yet the 17 GB Q4_K_M matches the full model on a popular agentic coding benchmark, Terminal-Bench 2.1."
- Instruction-following is flat down the ladder: "no change between models, down to a decent 2-bit one, weighing less than 11 GB" (the page names UD-Q2_K_XL at 10.7 GB).
- "At 1 bit, the model performs around random chance on GPQA Diamond, and longer reasoning makes it worse" (at the highest reasoning setting scores drop below low: the model reasons until the token budget runs out and returns an empty answer).
- The suite is exactly three benchmarks: GPQA Diamond, IFBench, Terminal-Bench 2.1 (89 tasks). Confirmed on-page: there is NO dedicated tool-calling benchmark and NO JSON or structured-output benchmark. The suite gap is real (the finder tied it to RQ1 of the context-tax brief; that mapping is finder-carried, this seat verified only the page-side absence).
- KL-divergence appears on the page once, only to be dismissed as a proxy: "Measuring token prediction differences (KL-divergence, top-1 predictions) is easy, but it does not tell us whether the model gets worse at solving tasks."

The two thread adds the find carried are now verified at the source (Algolia items API, item 49611128, fetched this session), so they graduate from OWED to cited:

- Quants are not uniform: kouteiheika: "Note that these quants are not quantized uniformly, so 4-bit isn't actually a 'true' 4-bit here"; wgd adds that the tested Q4_K_M is a standard K-quant while the smaller ones are dynamic.
- KL is dataset-dependent: kmike84: "A common issue is that it's rarely mentioned on which dataset KL-divergence is computed", with KL on agentic traces much higher than on chats or wiki text and top-1 divergence on agentic and coding data around 10 percent rather than around 1 percent; the post author (stared) agrees KL "does not measure what any e2e test does".

Mechanism to steal: a measured quant floor law for agentic work. Q4_K_M is the safe default that holds agentic coding at 4 bits; 2-bit is the instruction-following floor (flat from full precision down to 2-bit); 1-bit is collapse (random chance, and longer reasoning makes it worse). Quant selection must be judged on agentic task benchmarks, never on perplexity or KL proxies: the proxies do not predict task loss, and on agentic traces the proxy gap is at its widest (the kmike84 point above).

Estate map, organ fed: the quantizer organ, plus the gopher fleet's local tier. The estate runs local janitors (gemma:2b scut, gemma4 short worker, per AGENTS.md) and owns three quantizer organs that compress everything EXCEPT model weights, all verified this session: mag/state_quantizer.py:27 ("Schema: state_quantizer.v1", Verkle lattice into dense memory states; schema field written at :476), mag/auto_quantize.py:110 (class AutoQuantizer, adaptive resolution for analytics storage, docstring at :1), and tools/thought_quantizer.py, which compiles fleet law into packs: memory/corpus/quantized_thought/compile_report.json read this session (v0.4, compiled 2026-09-29T15:18:39Z, 401 laws in, 374 kept, packs frontier 24 / flash 12 / local 338, input memory/percolator/invariants.json). memory/research_polished/kv_cache_compaction.md:23 still lists "bare-metal steal (own quantized runtime / kernel layer)" as unexecuted, so the estate's first weight-quant decision is still ahead of it, and it should inherit this ladder instead of guessing.

Concrete port move: (1) file the floor law (Q4_K_M default for agentic scut, 2-bit floor for instruction-following, 1-bit never) into the thought quantizer's input stream so it compiles into the flash and local packs delivered at mag/context_pack.py:1142 (the "### L0b Compiled laws (thought quantizer, flash tier" section; the source line carries an em-dash, replaced with a hyphen here per house law); (2) add a quant-level axis (same local worker at current quant vs Q4_K_M vs 2-bit) to the next tools/tier_probe.py run (file verified present this session), scored on a fixed slice of real seat tasks (catalog tagging, lint summaries) so the ladder becomes the estate's own measurement; (3) the suite gap (no tool-calling or JSON benchmark) is exactly what that estate slice covers, since seat work is JSON-shaped.

## Find 2: LRU is the champion, capacity is the real enemy (agentic-kv-cache, 2026-09-10; HN item 49643543, 108 points, 58 comments)

Source: https://github.com/gauravapiscean/agentic-kv-cache
Thread: https://news.ycombinator.com/item?id=49643543

Re-verified on-page this session via WebFetch of the repo README; all five headline claims are verbatim hits:

- "I replayed 68,266 requests from 393 real Claude Code sessions and 23,608 Mooncake requests through a prefix-cache simulator" (68,266 + 23,608 = 91,874 requests total).
- The 8,000-block ablation row reads LRU-leaf at 83.48 percent, computed on 40 AgentX sessions / 4,751 requests (a subset of the replay corpus, not all 91,874; precision carried exactly).
- "Monotone negative. Every component made it worse, and the one I was most confident in - coherent eviction - was the worst." (em-dashes in source replaced with hyphens here per house law.) LFU and the +H/+HC/+HCG variants all underperform LRU-leaf.
- "The dominant source of cache misses here is tight two-second tool loops whose 88k-token working sets exceed cache capacity", framed as a capacity problem, not a liveness-prediction problem.
- Thesis verbatim: "LRU is harder to beat than the KV-cache papers suggest."

Mechanism to steal: the METHOD, not the number. Trace replay through a prefix-cache simulator, with radix-leaf LRU at the real budget as the free null arm, and ground-truth curve validation before any eviction candidate is believed. This is independent external confirmation of the estate's own gap law, gap-fold G1 at memory/research_polished/kv_cache_compaction.md:13: "any eviction/compaction claim must beat LRU/ARC/PBKV/Belady-MIN arms or it is decoration." A team with 91,874 real requests arrived at the same verdict from the outside. The diagnosis half ports as cheaply as the policy half: when the working set exceeds capacity, no eviction policy helps; the lever is budget and assembly, not a cleverer liveness predictor.

Estate map, organ fed: the context pack. Concrete port move: replay the estate's own traces (dashboard/static/trails/*.jsonl plus the db.sqlite transcripts named at memory/research_polished/kv_cache_compaction.md:28) through a block-level prefix-cache simulator at the context pack's real token budget. The resulting LRU hit curve becomes the null arm the governor eval bar already demands (kv_cache_compaction.md:28: "recency null first, threshold ablation, repeated-cycle decay, cache economics first-class, downstream task truth"). The frozen-prefix machinery to validate against already exists: mag/context_pack.py:489 has "def freeze_system_prompt(" and :548 carries the "## Auto-repack" tail marker. Doc-drift note for the percolator: kv_cache_compaction.md:27 still lists freeze_system_prompt() as never built ("The last live cache killer"); the function is present at :489 today, so that owed item has landed since the doc's 2026-09-20 code check and the doc line is stale on this point.

## Probes

Primary probe (this week, byte-cheap: pure local compute over files already on disk, no GPU, no API spend): compute radix-leaf LRU hit rate over the most recent 5,000 estate tape rows (trails jsonl plus db.sqlite transcripts) at the context pack's actual token budget. Falsifiable claim: LRU at the estate's real budget already achieves 80 percent-plus radix-leaf hit on estate traces (external reference: 83.48 percent at 8k blocks on the AgentX subset). If it holds, the measured number becomes the G1 null every future eviction or compaction proposal must beat or be rejected as decoration. If it does not hold, and per-session working sets blow past the budget the way the external 88k tool loops did, the correct fix is pack budget and assembly (freeze plus tail, mag/context_pack.py:489), not eviction policy. Either branch converts doctrine into a measured fact.

Secondary probe (needs Ollama, still cheap): serve the currently used local worker at Q4_K_M and at 2-bit, run 30 fixed prompts drawn from memory/corpus/quantized_thought/instructions_flash.jsonl, grade JSON-valid rate and exact match. Falsifies the port if 2-bit does NOT hold instruction-following on estate prompts, i.e. the flat-to-2-bit result fails to transfer off Qwen.

## Checks run this session (2026-09-29, exact commands and outputs)

1. grep -ci quesma catalog/catalog.jsonl -> 0. Finder's overlap claim confirmed.
2. grep -ci "agentic-kv-cache" catalog/catalog.jsonl -> 0. Confirmed.
3. wc -l catalog/catalog.jsonl -> 674,146 rows today. The find's "581,477-row catalog" was the finder's 2026-09-28 fetch-time figure; the catalog has moved since. Both named with their moments, never differenced across instruments.
4. WebFetch https://quesma.com/blog/qwen38-27b-quantizations-benchmarked/ -> all four headline claims verbatim-confirmed; suite = GPQA Diamond, IFBench, Terminal-Bench 2.1 (89 tasks); no tool-calling or JSON benchmark anywhere on the page; KL appears once, dismissed as a task-loss proxy.
5. WebFetch https://github.com/gauravapiscean/agentic-kv-cache -> 68,266 requests / 393 Claude Code sessions / 23,608 Mooncake requests; LRU-leaf 83.48 percent at 8,000 blocks on 40 AgentX sessions / 4,751 requests; monotone negative with coherent eviction worst; 88k tool-loop working-set capacity diagnosis; title verbatim.
6. WebFetch https://hn.algolia.com/api/v1/search (queries: "qwen3.8 27b quantizations" and "agentic-kv-cache", tags=story) -> quesma story objectID 49611128 (286 points, 139 comments, created 2026-09-08T14:49:19Z, matching the find's 2026-09-08 date; three earlier dupes at lower scores); agentic-kv-cache story objectID 49643543 (108 points, 58 comments, created 2026-09-10T13:39:11Z, matching the find's 2026-09-10 date).
7. WebFetch https://hn.algolia.com/api/v1/items/49611128 -> kouteiheika non-uniform-quant quote and kmike84 KL dataset-dependence quote verified verbatim in the comment tree; stared (post author) confirms KL does not measure e2e task performance; no comment in the tree discusses a missing tool-calling or JSON benchmark (that gap lives on the page itself, confirmed in check 4).
8. grep -n "def freeze_system_prompt" mag/context_pack.py -> :489 present; "L0b Compiled laws" -> :1142; "Auto-repack" -> :548.
9. grep -n on mag/state_quantizer.py -> schema header at :27, schema field at :476; grep on mag/auto_quantize.py -> class AutoQuantizer at :110, docstring at :1; ls tools/tier_probe.py -> present.
10. wc -l dashboard/static/trails/day_work.jsonl -> 1,894 rows; builder.jsonl -> 1,324 rows. Live files: the earlier seat's 12:49 draft recorded 1,748 / 1,206 at its moment; both moments named, not differenced.
11. Read memory/corpus/quantized_thought/compile_report.json -> v0.4, compiled 2026-09-29T15:18:39Z, 401 in / 374 kept / 374 packed, packs frontier 24 / flash 12 / local 338, input memory/percolator/invariants.json.

## OWED (not verified by this seat, marked, never asserted)

- The finder's exact discovery trail (which Algolia query surfaced each find): the item IDs, dates, and thread content now verify via the Algolia API (checks 6 and 7), but the finder's original query sequence is not reconstructible here.
- RQ1 mapping: the find ties the missing tool-calling or JSON benchmark to "RQ1"; this seat verified the page-side absence (check 4) but did not re-trace which brief's RQ1 the finder meant.
- The secondary probe's concrete Ollama quant tags for the estate's pinned gemma pulls (which Q4_K_M and 2-bit tags actually exist locally) were not checked against the local Ollama registry this session; the probe names that check as its first step.
- No pytest run for this card: it changes no code, so no test gate applies; the probes above are the runnables it proposes.
