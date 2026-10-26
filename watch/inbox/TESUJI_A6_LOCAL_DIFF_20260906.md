# TESUJI A6 — LOCAL DIFF PROTOCOL (hosted 5.3-flash vs MIT-weights GGUF)
**2026-09-06 · walker: external · charter: watch/TESUJI_MAP_5_3FLASH_20260906.md · $0**

A6 is the map's payoff axis: run the SAME tesuji grid on owned weights and diff it against
the hosted field. The diff between substrates IS the research result — if the map transfers,
the fleet owns its primary lane outright on Rocinante day (Oct 27).

## 1. DAY-ONE RECIPE (banked by others, $0 to prepare)
Sources: watch/scout/X_FLASH_HARVEST_20260905.md (roots 4-5) + watch/INTAKE_FLASH_LOCAL_WEIGHTS_20260905.md.
1. Weights: GLM-5.3-Flash (320B-A18B MoE) is **MIT-licensed**, weights public.
2. Quants: **Unsloth dynamic GGUF** — 1-bit ~100GB RAM / 3-bit 128GB / **Q4_XS** (field-tested primary).
3. Runtime: llama.cpp via the **special Unsloth PR — support is NOT upstream**. Missing the PR = day-one faceplant.
4. Host: Rocinante (4x Mac Studio M5 Ultra, 128GB+ unified per box). Serve loopback-only per fleet law.
5. Serve local endpoint → fire the tesuji grid through the same `mag/tesuji_map.py post` path,
   seat `local-rocinante`, cell names mirrored `A#/<same-probe-id>` (hosted rows keep `/external/`+probe seats).

## 2. PROBE PARITY RULES (the diff is void without these)
- **Byte-identical prompts:** the exact probe strings from the hosted grid, no paraphrase (paraphrase is the A2 shadow test, a different instrument).
- **Identical parsers:** same response parser, same verdict classifier, same code path as hosted probes.
- **Identical sampling config:** temperature pinned; 5.3 laws hold locally too — thinking is FORCED (cannot disable, vendor doc `docs/ref/ZAI_API_EXPERT_REFERENCE.md`), reasoning_effort pinned per probe, `max_tokens >= 1536` (epoch-1 infra finding, same file).
- **Seeds:** pin where the stack honors them; where it doesn't, run the rotation test (3x) on BOTH substrates and compare verdict-class modes, not single draws.
- **Timing fields recorded:** TTFT and gen tok/s per probe — A6 doubles as the substrate benchmark (M2 Ultra baseline: TTFT 3-4 min, gen 40-130+ tok/s at Q4_XS).

## 3. DIFF METRIC
Per cell: **verdict-class agreement** hosted-vs-local over {SUPPORTED, SHADOW, DISPUTED, UNPROVEN}.
- `agreement = matched cells / comparable cells` (a cell is comparable only if hosted verdict reproduced under rotation — unstable hosted cells can't diff against anything).
- **>= 0.80** (charter falsifier bar): the map TRANSFERS — local substrate certified as a valid field read; banked hosted cells usable for local routing.
- **< 0.80:** the quant has its own field — do not blend the ledgers; map the local diff AS a new layer (`A6/quant-shadow/*`), per-quant (1-bit vs 3-bit vs Q4_XS).
- Tokens/ms deltas reported per cell regardless (cost-of-substrate table).

## 4. GATES (real, not laziness)
- **HARD GATE — memory:** this box is **68.7GB < ~100GB (1-bit floor)** — no vanity local attempt before Rocinante (watch/INTAKE_FLASH_LOCAL_WEIGHTS_20260905.md). Nothing A6-local runs before Oct 27.
- **DATE GATE:** Rocinante 4x M5 Ultra, **Oct 27**. T1 (metered hosted probes) is the pre-gate work; A6 is T2.
- **ACCEPTANCE GATE (day-one falsifier, from the INTAKE card):** Q4_XS on Rocinante — **TTFT < 60s AND gen > 30 tok/s** → local flash becomes a standing fleet batch lane. TTFT > 3 min (M2 Ultra parity) → Apple-Silicon prompt processing is structural; local stays batch-only, spec-decode (UZU probe) becomes the lever.
- Both numbers gate (TTFT AND tok/s) — an interactive-feeling gen rate with 4-minute TTFT is NOT an interactive lane.

## 5. QUANT DEGRADATION — TRI-STATE (from harvested sources only)
- **SUPPORTED — quantized 5.3-flash runs functionally:** Unsloth Q4_XS + llama.cpp PR on M2 Ultra "works" end-to-end (r/LocalLLaMA field test, watch/scout/X_FLASH_HARVEST_20260905.md root 5); Unsloth ships 1-bit/3-bit dynamic quants (root 4). Community claim of API-class speed on $8K hardware (root 7, @krunkosaurus) — SUPPORTED as a claim on record, for big-RAM boxes.
- **DISPUTED — "faster than API speeds":** contradicted on Apple Silicon by the TTFT 3-4 min measurement (root 5, prompt-processing-bound). Generation rate may beat API; time-to-first-token does not. Hardware-dependent claim — treat per-host, never globally.
- **UNPROVEN — the degradation MAGNITUDE:** no banked source measures benchmark delta hosted-vs-quant for 5.3-flash (Terminal-Bench 84.3 is the hosted number; no local-quant bench score exists in our corpus). This is precisely what the A6 diff metric measures — the map's biggest open cell. Upstream Unsloth per-quant notes would shrink the prior; not fetched ($0 law, no network this walk).

## 6. EXECUTION ORDER (post-Oct-27)
1. Rocinante boots → pull Unsloth GGUF + PR llama.cpp → Q4_XS first.
2. Acceptance gate (§4) measured before anything else — one probe, both numbers.
3. Gate passes → replay hosted grid cell-by-cell under §2 parity → agreement score (§3).
4. Ledger: all A6 rows via `mag/tesuji_map post --seat local-rocinante`, resp-hash = quant manifest sha16.
5. 1-bit and 3-bit variants only if Q4_XS agreement < 0.80 or RAM pressure demands.

*Cells banked this walk (chain watch/TESUJI_MAP.jsonl): A6/external/mit-weights-gguf, A6/external/local-ttft-m2ultra — every external cell marked EXTERNAL (vendor-benchmark, not our probe).*
