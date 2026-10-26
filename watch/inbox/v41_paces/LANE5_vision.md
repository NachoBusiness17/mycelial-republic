# LANE 5 — VISION PROBE: what DeepSeek-V4.1-Flash's eyes actually are
(2026-09-11, lane 5/8, zcode seat. Sources: the 51-page tech report we hold —
`docs/report_v1/sources/DeepSeek_V41_Flash_tech_report.pdf` (pypdf, primary) —
plus the HF model card (fetched 09-11) and `watch/inbox/DESK_DSV41FLASH_20260911.md`.)

**THE POINT:** the answer to "how does it do computer use without vision?" is:
it doesn't do it without vision — it has a real, from-scratch ViT wired into the
backbone from token one, trained on screen captures and computer-use
trajectories. Vision is native, not bolted on. The report names our exact use
case: "rendered screen captures for visual inspection and self-correction"
(p5, multimodal agentic bullet). The honest gap is on the API surface: the
model card documents NO image formats or transport — the contract lives in
code (`encoding/encoding.py`), not docs. We verify with one screenshot probe
before trusting it as an eye.

---

## 1. Vision architecture (from the report, SUPPORTED — page-cited)

**Input pathway** (§2.1.1, p7): images and text in, text out.
`image → DeepSeek-ViT → spatial grid of features → 3×3 pixel-unshuffle → 2-layer MLP projector → visual embeddings inserted at image-token positions in the LLM input sequence`, processed jointly with text embeddings.

- **Encoder — DeepSeek-ViT**, trained from scratch (not a CLIP hand-me-down):
  ViT base with 32 layers, hidden 1024, 16 heads, **patch size 14** (p21).
  Modifications: **2D-RoPE** instead of absolute positional embeddings (native
  variable resolution — no fixed grid), linear patch projection instead of conv
  (Muon-optimizer compatible), RMSNorm, SwiGLU.
- **Token compression:** 3×3 **pixel-unshuffle** moves each 3×3 neighborhood
  into channels — **9x fewer visual tokens** — "effectively supporting input
  resolutions up to approximately **1344×1344 pixels**" (p7). That 1344 cap is
  the practical eye envelope.
- **Projector:** 2-layer MLP, hidden dim 5120 (p21).
- **MoE routing:** modality-specific auxiliary-loss-free load balancing —
  separate expert-correction biases for image vs text tokens (p7).

**How the eyes were trained** (§4, p21-22): two-stage encoder pre-training,
then joint multimodal pretrain with the backbone:
1. **Contrastive:** SigLIP sigmoid loss, ~47B image-text pairs (alt-text data),
   capped at 224×224.
2. **Autoregressive fine-tune:** ViT attached to a throwaway 4B MoE LLM,
   236B tokens (captions, alt text, **charts, OCR**), resolution 544×544–
   **1344×1344**. LLM discarded, encoder kept. High-res handling is learned here.
3. **Backbone joint pretrain:** multimodal data **from the start** of LM
   pre-training (p6), 45T tokens total, **7:1 text:multimodal token ratio** (p20),
   64K → 1M context extension at 34T tokens.

**What the multimodal corpus covered** (§4.2 "Multimodal Data Curation", p20):
image-text pairs (Common Crawl re-bootstrapped, relevance-filtered, deduped),
interleaved image-text (webpages + PDFs, SmolVLM quality-scored), and
domain-specific sets for **visual grounding and pointing, OCR**, long-tail
knowledge — plus "extensive **image-code pairs and computer-use trajectories**
to improve multimodal agentic understanding." That last clause is the computer-use
answer in the report's own words.

**Agentic vision, post-training** (p5): beyond metrics, it "can utilize rendered
**screen captures for visual inspection and self-correction**" in frontend dev
and office-automation workflows — i.e., screenshot-loop computer use is a
designed-in behavior, admitted gap vs top competitors acknowledged in the same
paragraph. Training infra notes (p16): disaggregated encoder (3-phase step),
balanced image sharding, incremental image transfer in RL rollouts — images are
first-class in the RL loop, not an afterthought.

**Vision benchmark numbers** (Table 1, p23 — Base model):
| Benchmark | Score |
|---|---|
| MMMU-Pro (EM, 4-shot) | 56.5 |
| CVBench (EM, 4-shot) | 77.9 |
| DocVQA (LLM-Judge, 4-shot) | 95.6 |
| RefCOCO-avg (Acc@0.5, 0-shot) | 86.0 |

Model card adds tool-using visual-agent scores: Chartography 78.9 Pass@1,
BabyVision 89.6 Pass@1, ZeroBench-main 49.0 Pass@5. Claim: beats Kimi-K3 on
visual reasoning + professional chart interpretation (p5) — DESK card holds this
part UNPROVEN until we run it.

## 2. API-side implications (model card, fetched 09-11)

- **No documented image formats.** No jpeg/png/webp, base64-vs-URL transport,
  or resolution parameter anywhere on the model card. Tri-state: **UNPROVEN** —
  the input contract is code, not prose: the repo ships `encoding/encoding.py`
  (self-contained reference implementation) with test fixtures covering
  "interleaved image content", plus a `deepseek-recipe` Rust toolkit that
  encodes requests incl. images. Read `encoding.py` before writing our adapter.
- **No Jinja chat template** on the HF repo — encoding.py IS the chat template.
  Any prompt-assembly we do must match its fixtures exactly.
- **Provider config:** `toolCalling: true`, **`structuredOutput: false`** —
  schema-validated JSON is NOT guaranteed at the API; our structured extraction
  must be prompt-schema + tolerant parse (cite_gate pattern), not response_format.
- **The only documented API knob is reasoning effort:** three tiers
  max/high/low → effort scalar b = 100/75/50 (Table 2, p29). No vision-specific
  API surface documented in the report.
- **Practical envelope for screenshots:** trained hi-res band is 544²–1344²;
  feed screenshots at ≤1344px long edge, aspect preserved (their own scaling
  policy), and expect degraded reads below ~544px.

## 3. The 15-minute probe (one screenshot → structured extraction)

**Falsifier framing:** report + card CLAIM an eye that reads screens for
self-correction. Probe = make that claim pass or fail on OUR surface, tri-state,
no vibes.

**Setup (min 0-2):** take ONE known screenshot of a fleet surface —
`dashboard/static/live.html` (overseer strip) at a state we can independently
verify from `dashboard/static/overseer.json` (the ground truth file is the
answer key). Render at 1920×1080, save PNG. Also save a second copy downscaled
to 1344px long edge (their envelope).

**Call (min 2-7):** send each image with one prompt, model's effort tier `low`
(cheapest first):

> Extract this dashboard screenshot as JSON only:
> {"page_title": str, "containers": [{"name": str, "state": str}],
>  "numbers_visible": [num], "error_banner": bool, "top_headline": str}
> Rules: only what is visibly rendered; empty list if none; no invented fields.

**Diff (min 7-12):** compare against overseer.json programmatically.

**PASS — all four:**
1. Valid JSON parse (no prose wrapper).
2. `page_title` exact match.
3. Container names: ≥90% exact-match against the census, states (running/
   exited) all correct.
4. `error_banner` correct, and ≥1 rendered number transcribed exactly.

**BONUS graded, not gating:** return bounding-box pixel coords for one named
container (grounding/pointing is in the training diet; RefCOCO 86.0 says it
should land within ~tolerance) — this is the computer-use "can it click" signal.

**FAIL conditions (any one):** invalid JSON twice; title wrong; >1 hallucinated
container; banner state wrong. If the 1344px copy passes but full-res fails,
that's a preprocessing finding (we own downscaling, not the API).

**Read-out:** PASS → vision is SUPPORTED on our surface; wire as the eye for
cite_gate/screenshot triage and log a tesuji row. FAIL → DISPUTED with the
diff pasted; the "viral shopping run" was probably DOM-reading, not vision.

**Runtime reality check:** weights are 552B (8B/16B active) — nothing local
until Rocinante (Oct 27). Probe runs against the public API / HF inference
provider once live; transport details come from `encoding.py`, which is the
next dig site (DESK card already flags it unexamined).
