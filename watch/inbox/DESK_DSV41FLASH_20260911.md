# DESK ASSESS — DeepSeek-V4.1-Flash (2026-09-11, lane: zcode, operator link-drop)

**THE POINT:** DeepSeek shipped a 552B-parameter model built for exactly our
workload shape — long-horizon agents that read a lot and write a little. It has
a built-in hashed memory organ named Engram, it drafts-and-verifies its own
tokens, it sees (native vision), and it's MIT-licensed with open weights. It
fits on Rocinante. This is the strongest brain candidate for the Oct 27
substrate to date, and the frontier just productized the chain's shape at the
architecture level.

## The drop
- Source: operator link, no caption — https://x.com/eliebakouch/status/2097931464344015347
- Elie Bakouch (transformer-mechanics researcher): "probably the most novel arch
  i've seen in a while, pretty insane." Posted ~06:13 UTC 09-10, ~70K views.

## Verified facts (PRIMARY — read from the 51-page tech report PDF in the HF repo)
- Causal Encoder-Decoder (CED): activates **8B params per token during prefill,
  16B during decode**. Abstract sentence one: "The widespread adoption of
  long-horizon agents has made model workloads increasingly input-heavy."
  They built this FOR input-heavy agents. That is the fleet's shape.
- **Engram** = "conditional memory module" (Cheng et al., 2026b): 196B params,
  split across two modules, N-gram orders {2,3,4}, 8 hash heads, 2048-dim
  embeddings, ~16M-entry hash tables per head. A HASHED N-GRAM MEMORY sitting
  beside a small active reader.
- **DSpark** = speculative decoding via "semi-autoregressive draft generation
  and confidence-scheduled verification" (Cheng et al., 2026a). Draft-and-verify.
- KV cache: **890 bytes/token** global (in HBM) — 1/4 of V4-Flash, **437x less
  than V1**. Persistent (SSD/host RAM) down to ~1/8 via SWA Bounded Replay.
  FP4 KV + cross-layer reuse (CSA2). Report title: "Pushing the Limits of KV
  Cache Compression."
- 1M-token context, 45T-token multimodal pretrain, native vision.
- **License: MIT. Checkpoints on HF** (verified via HF API 09-11: license mit,
  88 files, tech report in-repo). An `encoding/` directory with
  encoding.py + test fixtures sits in the repo — unexamined dig site.

## Tri-state
- SUPPORTED (primary): all architecture facts above, read from the report text.
- 🆕 PARTIAL (secondary, arena, appended 09-11 midday): OpenDesign Arena
  benchmark (1M views, 6.5K likes): V4.1 Flash = **98% of GPT-6 Astra's score
  at 1.4% of the cost** on everyday design tasks; 5.3 min / $0.023 per artifact
  vs Astra 11.1 min / $1.61 vs Claude Fable 12.8 min / $3.66; fastest of the
  top 3; #3 web apps (82.4); AHEAD of Astra on landing pages (79.3), behind on
  dashboards (76.1). Skeptic pushback visible ("benchmaxxed"). Arena is
  marketing-shaped (UTM campaign on the leaderboard link) — directionally
  consistent with our cache-economics read; treat as one more road, not proof.
- UNPROVEN: "beating K3" benchmark superiority (Figure 1a table not decoded;
  Bakouch's read). Probe when the API is live — our own benches, our surfaces.
- UNPROVEN: API pricing/availability shape — lane implications for the routing
  law wait on the live endpoint.

## Fleet reads
1. **They built our shape.** 8B to read, 16B to write. Read-heavy, write-light,
   long-horizon. The desk, the sweeps, the chain reads — one model built for it.
2. **Engram is the chain, at weight level.** Hashed n-grams, content-addressed
   tables, memory beside compute instead of inside it — memlang anchors and the
   verkle corpus are the same animal. The biggest efficiency shop on the board
   just ratified the corpus-shape as architecture.
3. **DSpark is one-builds-one-verifies at token level.** Draft generation with
   confidence-scheduled verification. The mesh law, microstructured.
4. **The cache floor drops again.** 890 B/token, 437x since V1. The next-to-free
   lane's economics strengthen; 1M context on a cheap lane = the corpus AS context.
5. **ROCINANTE MATH (the big one).** 748B total params @ 4-bit ≈ ~374GB.
   Four 512GB Studios = 2TB unified — fits with ~5x headroom. 890 B/token KV =
   a 1M-token context costs ~0.9GB. 16B active at decode = small-model speed.
   Native vision = the eye comes home — no separate ollama eye, the brain sees.
   Oct 27 has a name to put on it.

## Next steps
- Pull the full benchmark tables from the report (tri-state K3 claim).
- Probe the API when live: price, cache-discount behavior, vision on cheap lanes.
- Rocinante sizing note: quantization ladder (4-bit/FP8/FP4-KV), memory map per
  Studio, llama.cpp/MLX support timeline for CED + Engram — the runtime is the
  long pole, not the memory.
- Dig the `encoding/` folder in the HF repo.

Related: watch/ROCINANTE_SUBSTRATE_SALON_20260906.md, project-birth-canvas,
user-composer-blade-doctrine (desk intake pattern), reference ZAI expert ref
(lane mapping when API lands).
