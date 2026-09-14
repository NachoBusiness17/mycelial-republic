# INTAKE CARD — UZU SPECULATIVE DECODING ON APPLE M5 (item, 2026-09-03)

## ITEM
Operator pasted: https://x.com/trymirai/status/2095533045453337036
Mirai Labs (@trymirai) released speculative decoding in their inference engine
**uzu** — initially for **Qwen3.6 27B**, Qwen3.8 27B + Muse Glimmer coming soon.
Claims on Apple M5-series chips: ~2x over MTPLX (MLX + speculative decoding),
3x+ over llama.cpp at comparable quantization; strongest on math + coding;
co-designed around M5 GPU Neural Accelerators with aggressive spec budgets of
16-32 tokens vs model-native MTP's 3-4 token chains. "FreeBSD licensed, open to
PRs." Posted 3:23 PM Sep 3, 2026 — hours old at intake. 79.7K views / 13
replies / 31 RT / 120 likes / 107 bookmarks (bookmarks > likes = latent-demand
signal, same shape as the HF-incident receipt census).

## RECEIPTS (consult-first, this turn — thread + web sweep)
- Root post + replies fetched via web_reader (X wall did NOT block this time):
  - @pymike00 independent measurement, **M4 Pro**: TTFT 3.14s, prefill 117.43
    t/s, generation **16.06 t/s, 1.00 t/f** (tokens-per-forward = 1.0 means no
    spec-decode boost visible on M4), 14.03 GB memory. Single anonymous run,
    setup unknown — Unproven but directional: gains look M5-gated, which matches
    uzu's own "co-designed around M5 Neural Accelerators" framing.
  - @benlnyc fire; @MARUF positive one-liner. No community notes, no expert
    pushback found in the 13 replies — thread is too young for the wall to have
    sharpened it yet.
- Repo existence **Supported**: github.com/trymirai/uzu ("high-performance
  inference engine", Rust, Apple Silicon); HN Show HN launch thread (id
  44570048); r/rust thread; cited by name in arXiv 2607.00501 (BaseRT, native
  Metal inference) — third-party academic citation, engine is real and notable.
- The comparison baseline is community-measured: r/LocalLLaMA MTPLX post reports
  **2.24x via native MTP spec decoding, Qwen3.6 27B, M5 Max, ~28 → ~63 tok/s**
  (accept rate 71-73%). This makes uzu's "almost 2x over MTPLX" a FALSIFIABLE
  number: implied ~110-125 tok/s on M5 Max is the target for our own probe.
- Vendor speedup numbers (2x MTPLX / 3x llama.cpp) = **Unproven vendor claims**
  until measured on our silicon. License claim "FreeBSD" = Unproven (GitHub
  fetch 500'd; repo existence verified, license file not read).
- trymirai.com/metrics = vendor's own uzu-vs-MLX-vs-llama.cpp benchmark page
  exists (self-published; useful as the protocol to replicate, not as proof).

## SCORE — F:4 P:4 C:5 W:3 N:4 = **20/25 → BUILD NOW** (band floor)

## READ (the honest why)
This is a **Rocinante-docked item**. Every axis lands because of one fact: the
4x Mac Studio M5 Ultra arrives Oct 27, and this post is a vendor shipping
M5-specific inference speedups for exactly the model class the fleet already
runs locally (qwen2.5:32b maze-keeper, SAELIS-31B Q4_K_M, the bulk→local-Qwen
leg of the router decision table). It does not unblock THIS week's critical
path — the GLM 5.3-flash campaign Stages 2-5 run on cloud lanes — so PULL is 4
not 5, and WINDOW is 3: runtime is date-gated, but the Oct 27 prep lane
("one-button corpus package for Oct 27" is live in the campaign next-queue)
can consume it NOW as engine selection + a pinned falsifiable target. COST is a
clean 5: file today for $0, evaluate on arrival day for $0 (free OSS engine,
our own hardware). FIT 4 not 5: it rides committed substrate, but brings its
own model formats (oQ4/oQ8, not GGUF) and does NOT list GLM models — the
GLM-5.3 self-host arm stays SGLang/vLLM; uzu serves the Qwen lane only.
The sharpest single receipt is the @pymike00 M4 Pro number: 1.00 t/f on M4
says the magic is (claimed to be) in M5 silicon co-design — which is either
exactly our arrival-day windfall or exactly the claim Oct 27 falsifies.

## DOGFOOD
1. **INVARIANT PASS**: reinforces receipts-over-claims (vendor numbers stay
   Unproven until our probe — the vast-autopilot tok/s probe-card pattern is
   the exact verification instrument, second deployment); reinforces
   cheapest-lane routing (local inference is the terminal free lane;
   bulk→local Qwen already sits in the router table, this strengthens that
   leg 2-3x if it holds). Loopback-only trivially satisfied — on-device is
   the most loopback a lane can be. No contradictions. One tension filed:
   format lock-in (uzu quants vs the GGUF/ollama fleet standard) is a small
   anti-portability cost against model-swap flexibility.
2. **STOCKFISH PASS**: placement = **SUBSTRATE opcode** (of the four verbs).
   Consumers: compute-inventory/routing decision table (bulk→local leg), the
   Rocinante manifest, and the Oct 27 day-one probe card. Placement succeeds.

## TRI-STATE
- uzu exists, is Rust, Apple-Silicon-native, community-known since mid-2025 —
  **Supported** (GitHub + HN + r/rust + arXiv citation).
- MTPLX baseline ~63 tok/s on M5 Max — **Supported** (community-measured,
  r/LocalLLaMA, independent of the vendor).
- uzu beats MTPLX ~2x / llama.cpp 3x+ on M5 — **Unproven** (vendor claims; only
  community data point is M4 Pro at plain-decode speed, no boost visible).
- Gains are M5-gated (Neural Accelerator co-design) — **Unproven**, directional
  support from the M4 reply; falsifiable Oct 27.
- FreeBSD license + PR openness — **Unproven** (repo verified, license not read).
- Qwen3.8 27B + Muse Glimmer support "coming soon" — **Unproven** (roadmap talk).

## VERDICT
**BUILD** — small, now: pin uzu into the Rocinante manifest as the Qwen-lane
engine candidate and write the Oct 27 day-one probe card TODAY with the target
number baked in: on our M5 Ultra, qwen3.6-27B quant, uzu must beat ~63 tok/s
(community MTPLX baseline) and ideally approach ~110-125 tok/s (vendor-implied);
protocol = the vast-autopilot take-C probe format (tok/s, TTFT, memory, same
quant, three prompt classes incl. one math/coding where claims are strongest).
Zero code before hardware. This is not a re-find: the corpus has no
Apple-Silicon-native engine or spec-decoding entry (desk GPU history = ROCm
gap; Ox Alpha = SGLang/vLLM/TokenSpeed server-class; vast boxes = NVIDIA).

## ROUTE
Wire: yes, one pointer — Oct 27 package builder / GLM-5.3-flash campaign
next-queue ("one-button corpus package for Oct 27") gets this card + the probe
target. No driver interrupt; nothing runs until the Studios land. Typed
room.jsonl row left to the main thread per Amendment 1 (path not handed to
this spawn).
