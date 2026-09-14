# INTAKE CARD — THENEWSTACK: GLM-5.3-FLASH, CHEAP AND ON CHINESE CHIPS (Grok batch 12/10, 2026-09-04)

## ITEM (verbatim root, fxtwitter 200 OK)
@thenewstack, Sep 04 2026 00:00Z: "https://Z.ai's GLM-5.3-Flash is cheap, good, and served
on Chinese chips" + article link thenewstack.io/glm-5-3-flash-chinese-chips/.
Stats: 110 views / 0 replies. (Fetch integrity note: scout file's copy of this URL was
fine; the batch's fxtwitter mirror 404'd fleet-wide on round 1 and cleared on round 2 —
transient mirror failure, logged in the batch report.)

## INGEST (article fetched on WebFetch retry — strike 2 succeeded)
- Model: 320B params, 18B active; hybrid linear + sparse attention; 1M-token context;
  30T-token multimodal training corpus; MIT-licensed weights on HF.
- Serving: entirely on Chinese AI chips, on a Z.ai engine built on SGLang; Z.ai claims 3x
  end-to-end serving gain on identical hardware, per-token cost "comparable to mainstream
  NVIDIA GPUs"; a GLM-5.3-driven infra agent tuned the serving stack ("self-optimizing").
- Benchmarks: 57 on Artificial Analysis Intelligence Index — in line with GPT-5.6 Terra,
  Gemini 3.7 Flash, Muse Spark 1.2, Qwen 3.8; keeps pace with Claude Opus 4.8 / GPT-5.6
  Terra at max-effort; "performs even better relative to rivals on agentic tasks."
- Pricing: OpenRouter $0.075/M input, $0.25/M output (50% discount); "reportedly served
  100 trillion free tokens daily" per OpenCode.
- Caveats (article's own): "very chatty", token-hungry — low prices offset; performance
  claims rest on Z.ai's own reporting; early "Claude Fable 5 level" hype NOT supported by
  benchmarks. Previously circulated as the stealth model "ox-alpha."

## THREAD (Amendment 2)
0 replies. No community note. The article is the primary source; the tweet is a pointer.

## MAP
- LANE CONFIRMATION: the fleet's workhorse lane (glm-5.3-flash, 3x quota, cache-mining
  doctrine) is third-party-confirmed cheap+good — CACHE_YIELD_MATH_20260901 economics
  stand on the right reservoir.
- CORPUS MYSTERY RESOLVED: "ox-alpha" = GLM-5.3-Flash. UNTOUCHED_SURFACE_20260831.md and
  the uzu card's "Ox Alpha = SGLang/vLLM server-class" line now have their referent
  (Supported by this article; the corpus had the name, not the identity).
- CHATTINESS CONVERGENCE: "very chatty / token-hungry" independently corroborates
  SWARM_SCALE_PLAN_20260904 divergence S2 (output-token discipline per worker; noisy
  worker burns 14x share) and the Economist's output-envelope guard. Two external lanes,
  same finding.
- Fireworks + OpenRouter pricing rows belong in docs/ref/ZAI_API_EXPERT_REFERENCE.md.

## [SOCRATIC] assumption attacked: "vendor PR echoed by a trade press = new information" —
attacked by reading the article's own caveat paragraphs (it carries its skepticism inline:
hype unsupported, claims self-reported). What survives: confirmation value + the ox-alpha
resolution, not new performance truth.

## ASSERT
GLM-5.3-Flash is a frontier-class cheap workhorse (AA 57, $0.075/$0.25 per M on
OpenRouter) servable at scale on non-NVIDIA Chinese chips — vendor-lane risk for NVIDIA
pricing is real, and the fleet's lane choice is externally validated.

## ATTACK
1. Every performance number traces to Z.ai's own reporting (the article says so) — the
   3x serving gain and AA-57 placement are single-source (evidence: article's caveat
   section).
2. "100T free tokens daily" is an OpenCode relay of a vendor claim, unfalsifiable from
   here — worse than Unproven, it's the citation cascade the corpus law names.
3. Chatty/token-hungry cuts both ways: low price/token with high tokens/task can net out
   worse than a pricier terse model — the article doesn't do the net-cost math our
   output-envelope guard exists for.

## MEASURE ($0, already run by the fleet)
The fleet's own lane is the standing falsifier: cache receipts + flight-recorder output
envelopes measure chatty-ness weekly (NIGHT_CACHE_RECEIPTS, meter_readings). OpenRouter
price row is checkable in one $0 page load when the router table next re-prices. Kill
condition for the "cheap in practice" reading: our own measured $/task on 5.3-flash
exceeds the DS-off-peak reservoir's $0.03/1M-cached economics — then the lane is cheap
per token, not per task.

## SCORE — F:5 P:3 C:5 W:3 N:3 = **19/25 → BUILD, WINDOWED** band; verb below is REMEMBER
(corroboration filing — the score tracks confirmation value, nothing to run tonight).

## TRI-STATE
- GLM-5.3-Flash exists as described (320B/18B A, MIT, 1M ctx) — **Supported** (article +
  fleet's own daily use; specs from vendor via article).
- Served at scale on Chinese chips via SGLang-based engine — **Supported-single-source**
  (Z.ai's announcement via the article; no independent verification exists in-corpus).
- AA index 57, peer-class with Terra/3.7-Flash — **Unproven** (vendor-reported placement).
- Ox-alpha = GLM-5.3-Flash — **Supported** (article states it; corpus name now resolved).
- "Very chatty, token-hungry" — **Supported** (article + our own output-envelope findings).
- 100T free tokens/day — **Unproven** (relay of vendor claim; unfalsifiable as posted).

## VERDICT — **REMEMBER** (file the law: cheap-per-token is not cheap-per-task; the
chattiness finding is the third independent vote for output-envelope discipline).
Route: one small $0 BUILD offered to the driver — add to docs/ref/ZAI_API_EXPERT_REFERENCE.md:
OpenRouter price row, Fireworks-US serving note (see augmentcode card), ox-alpha alias.
TWO COUNTERS: FORBIDS citing "on par with Opus 4.8" anywhere in fleet docs (single-source
vendor placement). PAID RENT: resolves the ox-alpha referent; corroborates the envelope
guard with an external vote.

## THE CROP
Training hardware undisclosed (article's own gap); no independent serving benchmark
exists; the "self-optimizing infra agent" claim unexamined (could be its own intake).
Different-mind contest: the Economist chair should do the net-cost-per-task math the
article skipped, using our own ledger data.

## FILED — watch/INTAKE_NEWSTACK_GLM_CHIPS_20260904.md + room thread "intake"
