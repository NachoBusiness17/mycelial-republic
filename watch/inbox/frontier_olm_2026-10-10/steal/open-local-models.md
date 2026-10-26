# STEAL CARD: open-local-models (frontier OLM 2026-10-10) - REV 2

Round 2 per the REJECT critique. Repairs landed this revision: (1) the overlap receipt is
rewritten because round 1's "genuinely new to the estate" was FALSE: the estate has held
this exact find since 2026-09-13 and the full prior chain is now cited below; round 1's
own grep output listed the prior carrier and mischaracterized it as sweep-tree. (2) The
JSON twin is banked next to this file (open-local-models.json, same {area, steal,
source_url, estate_map, probe, chars} shape as the sibling inference-efficiency.json,
verified this session). (3) The primary port is DEMOTED TO CONDITIONAL: the decode-bias
capability it assumed was empirically probed on the live local host this session and
does not exist there (probe + result below). (4) The falsifier is DECOUPLED into two
independent probes, one per claim (hosted-model displacement vs method-port). (5) The
headline now leads with the cross-benchmark xhigh MEAN 41%, with 58% flagged as the
single-benchmark best case, and the three citation drifts are fixed (raw :10, :16;
gopher_lite :225).

## Find

UkisAI Swift-Qwen3.8-27B: a post-train of Qwen 3.8 27B cutting thinking tokens by a
MEAN 41% at xhigh effort across its 9-benchmark table (best case 58% fewer on
GPQA-Diamond; worst 19% on C-Eval), <1% accuracy loss, 1.95x speedup
(watch/inbox/frontier_olm_2026-10-10/sweep/raw/swift_qwen3827b.txt:2,:18). Reddit post
1wg7dd5, independently held as JSON since 2026-10-06
(watch/inbox/frontier_olm_2026-10-06/sweep/doors/ff_deep/1wg7dd5.post.json: 7,206
bytes, id 1wg7dd5, score 891, 364 comments, author Secure_Recording_472, all re-read
this session).

## Verification run this session (commands, not vibes)

- Direct Reddit fetch twice blocked (www + old.reddit); all quotes byte-verified in the
  estate's banked raw capture swift_qwen3827b.txt (76,404 bytes, catalog row
  0ae3576508d2, mtime 2026-10-10T14:47:59Z, zone intake; the ONLY case-insensitive
  ukisai row in catalog/catalog.jsonl).
- Headline at :2 (mechanism quote + -58% best case + 1.95x + <1%); complementarity to
  effort settings, chat templates and token caps and "anxiety-like" loops at :6; method
  chain at :10-:14 (8xH100 trace generation at :10, common-denominator token mining,
  inference-time penalizer, LoRA SFT, accuracy restored via On-Policy Distillation /
  RL(GSPO) / ThinkingCap 3.6 chunks at :14); full benchmark table at :18 (GPQA-D 88.4
  -> 88.3 at 58% fewer, Terminal-Bench 2.1 66.7 -> 65.8 at 39%, MMLU-Pro 85.5 -> 85.0,
  C-Eval 90.0 -> 90.6, IFBench 73.5 -> 71.8, AIME26 98.7 -> 94.0 author-linked to a
  penalized math token, HMMT 99.3 -> 96.0, ERQA 67.5 -> 66.3; xhigh mean 41%, medium
  23%, low 26% with admitted 1-4% medium-effort loss); evals repo link at :16; Flash
  3.8 follow-up -30% at :23, -38.1% not-ready at :217; free 5RPM API at :4.
- API liveness re-verified: curl https://ukisai.com/api/swift/v1/models -> HTTP 200,
  {"object":"list","data":[{"id":"swift","object":"model","owned_by":"ukisai"}]}.
- All benchmark numbers are the author's SELF-REPORT from the post; the estate has not
  re-run them. The 10-01 sweep independently re-read the HF page end-to-end
  (frontier_olm_2026-10-01/sweep/inference-efficiency-hn.md:7) and confirmed only
  "58.3% fewer, <1% loss, GPQA 88.38->88.28, 1.95x" (:55).

## The steal (mechanism, not the download)

NOT "pull a 27B finetune onto the janitor box" (our local tier is 2B-class; a 27B xhigh
model is the wrong shape). The steal is the METHOD, which is a percolator pattern
wearing a training costume: (1) harvest traces from your own workload; (2) group the
ones showing overthinking loops; (3) mine the COMMON DENOMINATOR tokens across them
(repeatables); (4) penalize exactly those tokens at inference, never attacking
reasoning length itself; (5) restore lost accuracy via on-policy distillation. That is
the estate's percolator law one level down: raw signal in, noise stripped, REPEATables
compiled to invariants (mag/percolator.py:13-14), applied to TOKENS instead of
sentences. Key honesty marker matching our theater-stripping: loop tokens "do not
contribute to answer quality when properly targeted" (raw :6) - reasoning length should
be optimized, never shortened by force. This is COMPLEMENTARY to the effort-knob
framing the ribs already hold (RIB_INFERENCE_BUDGET_20261001.md:106,111;
RIB_MODEL_GARDEN_ROUTING.md:227, grep this session), exactly as raw :6 positions it,
so no rib duplication.

## Estate map

- PRIMARY ORGAN, percolator (mag/percolator.py:13-14), port now TWO-STAGE and
  CONDITIONAL on stage 2:
  - Stage 1 (unconditional, $0): point the deterministic percolate() pipeline at a new
    input class - the estate's own janitor reasoning traces (dashboard/static/trails/
    *.jsonl lanes, session logs). Classify repeated loop-signature tokens as REPEAT
    signal; compile to an invariant penalty list. UkisAI saw the effect from the
    penalizer BEFORE any SFT (raw :12-:13), so the list is the deliverable, not a
    training run.
  - Stage 2 (CONDITIONAL, host absent today): apply the list at decode time. Empirical
    probe this session on the LIVE local host (Ollama 0.34.3): POST /api/chat with
    options.logit_bias {"the":-100,"The":-100} returned HTTP 200 with output
    BYTE-IDENTICAL to the unbiased control (temperature 0, seed 7, gemma:2b), and the
    OpenAI-compat /v1/chat/completions logit_bias behaved identically - silently
    accepted and ignored at BOTH layers. The estate drivers also carry no bias field
    (mag/afk_loop.py:104-112, mag/cache_identity.py:202-213) and rg -in "logit" over
    mag/ + tools/ hits only numpy internals (tools/concept_predictor.py:292-294,
    tools/ldt_lattice.py:38,59,67, tools/ldt_train.py:169-206). So: no decode-bias
    path exists on the current local lane; stage 2 waits on a verified host (OWED).
- SECONDARY, gopher fleet (mag/gopher_lite.py:14-15, CHORES dict at :225): the live 5RPM
  free API is a new free-lane sensing surface in the KEY_2 idle-pool shape; a
  tiny-prompt chore can fingerprint it at $0.
- TERTIARY, water graph (mag/water_graph.py): a held-accuracy 40-58% thinking-token cut
  is a flow fact; if a probe below passes, the projected token savings belong in the
  burn ledger the way smith projection() already lands rows.
- NOT mapped to the quantizer organs: mag/auto_quantize.py, mag/tool_quant.py,
  mag/state_quantizer.py quantize analytics, tool essence and Verkle state - not model
  weights; the GGUF/NVFP4 angle feeds the local lane directly, not the quantizer.

## Probes (two, DECOUPLED - one per claim; either can fail without killing the other)

- PROBE A (hosted-model displacement claim): send 20 estate-canary janitor prompts
  (label-farm tiny-prompt class, mag/gopher_lite.py:15) to the live 5RPM API twice,
  xhigh + medium effort = 40 calls, ~10 minutes inside the rate limit, $0. FALSIFIER:
  if median completion tokens at xhigh are not at least 25% below our local gemma
  short-worker baseline on the same canaries, OR more than 1 of 20 canary tasks fails
  vs baseline, the displacement claim is dead for OUR workload and the model-side lane
  closes SENSING-ONLY. Probe A failure does NOT close probe B.
- PROBE B (method-port claim, $0, local): mine dashboard/static/trails/*.jsonl for a
  repeatable loop-signature token class via the percolator lexicon scan (stage 1).
  FALSIFIER: falsified if no repeatable loop-token class emerges from the traces (the
  penalizer has nothing to save), or if no local decode-bias host is verified (today's
  probe shows the current host ignores bias; candidate host to verify: llama.cpp
  llama-server logit_bias against the estate's GGUF stack - NOT verified this
  session). Probe B failure does not close probe A.

## OWED

- HF page: estate read it end-to-end 2026-10-01 (inference-efficiency-hn.md:7); the
  10-07 sweep re-attempted and timed out twice (inference-efficiency-hn.md:12); not
  retried this session. GGUF bytes never pulled.
- Evals repo (github.com/UkisAI/Swift-Qwen3.8-27B-evals, raw :16) not pulled;
  benchmarks remain author self-report.
- The AIME26 math-token bugfix release does not exist yet; AIME-class work must not
  ride this model until it lands.
- A verified decode-bias host for stage 2 (llama.cpp llama-server or a sampler fork);
  today's Ollama 0.34.3 probe result stands until then.

## Overlap receipt (CORRECTED; round 1's "genuinely new" was false)

Prior carriers, all re-read this session:
- 2026-09-13: watch/inbox/RESONANCE_INTAKE_20260913.md:15 holds the exact find as a
  resonance row: "Swift-Qwen3.8 anti-overthinking fine-tune: -58.3% thinking tokens,
  accuracy flat (creator-reported) | UNPROVEN numbers, SUPPORTED shape | pumping at the
  WRONG frequency = thinking loops". Round 1's own rg -il "swift-?qwen" output listed
  this file and round 1 wrongly folded it into "the sweep tree" - struck.
- 2026-09-28: quantization sweep lists HN 49833102 "UkisAI Swift Series (09-24)" and
  49727511 "Swift-Qwen3.8-27B (09-16, 33 pts)"
  (frontier_olm_20260928/sweep/quantization-compression-hn.md:16).
- 2026-10-01: deep hold - HF page fetched end-to-end
  (frontier_olm_2026-10-01/sweep/inference-efficiency-hn.md:7), numbers re-confirmed
  (:55), "Swift-Qwen IS partially held" with a full section
  (frontier_olm_2026-10-01/sweep/quantization-compression-hn.md:31,:65,:100-101), and
  section-heading carriers in memory/runs/gapwave/hn_x_fanout/local_serving.md:34
  ("-58.3% thinking tokens, x1.95 speed [24GB-CLASS]") and skill_quantization.md:56.
- 2026-10-02: reddit sweep listing-read names 1wg7dd5
  (frontier_olm_2026-10-02/sweep/open-and-local-language-models-reddit.md:47).
- 2026-10-07: inference sweep names it held-known with the HF re-fetch timed out twice
  (frontier_olm_2026-10-07/sweep/inference-efficiency-hn.md:12,:71).
Net novelty, honestly stated: the NUMBER and the shape resonated 2026-09-13 and are
held with headings since 10-01. What is genuinely new in this card: the full 9-benchmark
table with per-benchmark token medians and the AIME bug attribution (raw :18), the
complete method chain as a portable recipe (raw :10-:14), the live-verified 5RPM
fingerprint endpoint, and the empirical local-host finding that Ollama 0.34.3 ignores
logit_bias at both API layers. Mechanism-name novelty: rg -in "overthink" over corpus/
+ memory/rib/ exits 1 (zero hits); GAP_REGISTER has no ukisai/overthink row (rg exit 1
this session). The find's own overlap claim ("ZERO hits in catalog.jsonl") was true
only of the catalog at scan time and false of the estate's watch/inbox + gapwave
holdings.
