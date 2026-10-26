# Steal card: quantization-compression via arxiv (frontier_olm 2026-09-28)

- **Round:** 1 (first draft, no prior critique)
- **Seat:** steal gopher, area `quantization-compression via arxiv`
- **Banked:** 2026-09-29
- **Source find:** "Quantization Thresholds Replicate, Failure Modes Do Not: A Three-Model Study of Agentic Tool Use in Polish from 8-bit to 2-bit", arXiv:2609.32042, 2026-09-25, Jakub Prejzner. Author's repo: https://github.com/JakubPrejzner/polagentbench
- **Source URL:** https://arxiv.org/abs/2609.32042

## The find (as confirmed, then re-verified this ask)

The ask's quote: "All three models fall off a cliff between 3-bit and 2-bit (11B 0.716 to 0.045, 7B 0.463 to 0.149, PLLuM 0.224 to 0.015; paired McNemar p < 0.001 in each)". Verified live this ask via WebFetch of the abs page (title, author, date, and the quoted sentence all match) and against the estate's own in-repo full text at `watch/inbox/frontier_olm_20260928/sweep/_raw/full_2609.32042.txt:99` (same numbers, rendered with arrows in HTML).

This is the estate's own sweep question answered: `watch/inbox/frontier_olm_20260928/sweep/quantization-compression-arxiv.md:18` defines Q1 as "Do 2 to 4 bit weight quantizations preserve tool-call JSON reliability on 2B to 8B models, and which formats for Ollama-class serving?" The find's `why` field calls it "The Q1 anchor"; that anchor is real and cited at the path above.

## The steal (mechanism, not links)

Three portable mechanisms, strongest first:

1. **The collapse threshold replicates; the failure mode does not.** Across three models spanning a fourfold capability spread and two axes of variation (pruned child vs parent, foreign pretraining family), exactly one thing transfers: the cliff sits between 3-bit and 2-bit GGUF. Everything else is per-model: at 2-bit the 7B fails long (median 9.1k tokens over 4 steps) while the 11B answers at step 1 with a confabulated final answer (37 of 64 failures); PLLuM keeps parsing the protocol (71.8 to 92.0 percent of steps) while failing content (`full_2609.32042.txt:99`, `:370`, `:732`). Port shape: a **quant floor law keyed to role, not to a failure signature**. You cannot learn the dangerous regime from one model's telemetry; you can only fix the floor (Q3_K_M is the working edge, Q2_K is out for tool-serving roles) and measure each model's own signature.

2. **Below the cliff, failure looks like success to a tool harness.** The 11B's 2-bit failures "end at the first step with a well-formed final_answer, no tool call and no parse error, all but one asserting a temperature, a forecast or a sent alert that the empty tool log never produced" (`full_2609.32042.txt:370`); the conclusion restates it: "At 2-bit the same model often keeps the protocol well formed while confabulating the content" (`:732`). Eighteen of the 37 confabulations even reuse the system prompt's example sentence verbatim (`:370`). So parse-success telemetry is blind exactly where the model is most broken. Port shape: the estate's tool harnesses must score **protocol-shape and content separately** (the paper's own format-tag vs content-tag split, `:152`), never a blended pass rate.

3. **A free collapse detector: inverted token economics.** At every precision except 11B Q2_K, the median failing trajectory costs more tokens than the median passing one, by 1.18x to 7.65x; at 11B Q2_K the failures are the CHEAP ones (median 1,506.5 tokens vs 4,010 for passes) because the model answers before it looks (`:370`). Port shape: track steps-to-final-answer, tool-call count, and tokens per trajectory in the janitor harness; "final answer at step 1 with an empty tool log" plus "failure cheaper than success" is a zero-inference-cost alarm that fires without any extra model calls.

Secondary rider from the same read (same file, `:559`): explicit decomposition scaffolding lifts 8-bit models off the unscaffolded floor (11B 1/10 to 9/10, McNemar p=0.0078; 7B 0/10 to 7/10, p=0.016) but the lift does NOT survive to 4-bit (trap arm 0/6 both models, corrected L3N only 0.40 and 0.30), so scaffolding is a precision-coupled repair, not a free constant. And the paper's artifact audit (rounding-hostile gold values, strict answer typing, a no-tool rule stated to the oracle but not the model, `:557`, `:732`) is a template for the estate's own eval hygiene: report strict and corrected numbers side by side.

## Estate map (organ + concrete port move)

**Primary organ: the quantizer** (GGUF weights side of the local janitor fleet; AGENTS.md names gemma:2b scut and gemma4 short worker as the local-first rung). Concrete moves:

- **Floor law:** any model serving a tool/JSON-emitting role floors at Q3_K_M-equivalent; Q2_K is banned for those roles regardless of VRAM pressure. The evidence base is exactly the estate's size class (7B/8B/11B GGUF k-quants on tool-call JSON). `mag/gguf_cartography.py:48-80` already carries the full GGUF dtype table (Q2_K at `mag/gguf_cartography.py:59`, Q3_K at `:60`) and parses the container with zero deps, so the cartographer is the natural host for a per-model quant census that enforces the floor on whatever GGUFs land on disk.
- **Upgrade the one-liner:** `mag/vast_launcher.py:436` currently carries "24GB only fits Q4 (~18GB, quality drop)" as a VRAM comment; this find upgrades that folklore into a measured law with a cliff and a falsifiable threshold.
- **Detector into the harness:** wire the three free signals (tool calls before final answer, steps-to-final, tokens per trajectory) into the janitor run loop, and alert on the 2-bit signature (final answer, zero tool calls on tool-required tasks; failing median below passing median). The estate's own law "Anomalies are NEVER quantized" (`mag/auto_quantize.py:22`) gets a corollary: below the quant cliff, quantization itself manufactures anomalies shaped like successes.

**Secondary organ: gopher fleet.** The janitors' receipts feed the fleet's done-work ledgers; a confabulating quant produces well-formed "done" receipts with an empty tool log, which is exactly what the detector flags. The paper's negative-transfer result (a taxonomy fitted to the 11B did not predict the 7B, its own pruned child, `:370`) says the detector thresholds must be fit per janitor model, never shared.

## Probe (falsifiable, cheap, this week)

Pin a 15 to 20 task deterministic tool-call suite in the janitor's own idiom (every task requires at least one tool call before a final answer; oracle = JSON-schema-valid envelope plus correct content, scored separately as protocol-shape and content, per mechanism 2). Run gemma:2b and gemma4 twice each: current ollama quant vs one Q2_K_M rebuild from the same base (ollama create from a requantized GGUF; the paper's own requant path was llama-quantize from the official Q8_0, `full_2609.32042.txt:734`). Temperature 0, fixed seed, ~40 short local calls per model, one afternoon, no GPU rental.

Predictions from the find (any one failing does NOT kill the floor law; the detector leg is what dies):
1. Pass rate collapses at Q2_K_M relative to current quant (paper: 0.716 to 0.045 at 11B).
2. The dominant Q2_K_M failure mode is protocol-well-formed/content-wrong (final answers with an empty tool log), not parse failures.
3. Sharpest, most quantitative: median failing-trajectory tokens drop BELOW median passing-trajectory tokens at Q2_K_M only.

Falsification condition for the transfer claim: if our stack fails by parse errors (visible failures) and failures cost more tokens than successes at Q2_K_M, the signature does not transfer to gemma:2b; keep only the pass-rate collapse leg of the law and drop the detector. Running both janitors also tests the negative-transfer law on the estate's own sibling pair (does the 2b signature match the gemma4 signature).

## Verification ledger (what ran this ask)

- `grep -c "Quantization Thresholds Replicate" catalog/catalog.jsonl` returned **1**, not the 0 the find claimed. Drift attributed: the one row (catalog id `1f7bc87da923`) is the OLM sweep's own raw full-text of the paper, `watch/inbox/frontier_olm_20260928/sweep/_raw/full_2609.32042.txt`, 123,339 bytes, mtime 2026-09-29T02:59:44Z, banked AFTER the find's 2026-09-28 grep. It is a raw sweep artifact, not a prior steal; the steal target filename was absent from `watch/inbox/frontier_olm_20260928/steal/` (checked by `ls`), so the steal itself remains new to the estate.
- `ls state/arxiv/2026-09-25/ state/arxiv/2026-09-26/ state/arxiv/2026-09-27/ state/arxiv/2026-09-28/ | grep -c 32042` returned **0**: the paper is absent from the arxiv pull dirs through 09-28, matching the find's absence claim.
- WebFetch of https://arxiv.org/abs/2609.32042 (this ask): title, author (Jakub Prejzner), date 2026-09-25, and the cliff quote verified against the live abstract.
- Paper claims re-verified against in-repo bytes via grep on `watch/inbox/frontier_olm_20260928/sweep/_raw/full_2609.32042.txt` (lines 99, 152, 226, 370, 557, 559, 699, 732, 734, 1784, 1792, 1798, 1802, 1804): the confabulation signature, the inverted token economics, the scaffold numbers, and the artifact audit are all byte-present.
- Estate grounding read this ask: `mag/gguf_cartography.py` (lines 1-80), `mag/auto_quantize.py` (lines 1-80), `mag/tool_quant.py` (lines 1-60), `watch/inbox/frontier_olm_20260928/sweep/quantization-compression-arxiv.md` (full), plus grep hits at `mag/vast_launcher.py:415` and `:436`. AGENTS.md janitor names (gemma:2b, gemma4) come from the loaded workspace instructions, not from a file read this ask.
- Not run this ask: the probe itself (it is the proposal), any test suite, any estate gate. No numbers in this card come from runs I did not execute or files I did not read.
