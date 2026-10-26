# SWEEP: open-and-local-language-models via arxiv (2026-10-02)

source-fetched: 2026-10-02
seat: sweep gopher, area 6 of the frontier_olm_2026-10-02 lens of lenses
inputs honored: lens/questions.md area 6 (5 questions), lens/burns.md anti-rebank rules,
lens/laws.md instruments-only law, lens/doors.md arXiv recipe (cat:-constrained queries) and
the pair-instruments-before-dead rule (doors.md:74).

## Instruments run this sitting (exact commands, verbatim outputs kept in session log)

- arXiv export API door, 8 queries, all 200 via WebFetch (door proven today in doors.md:16-26):
  ti:"Gemma" (totalResults 41), (ti:"Ling" AND cat:cs.CL) (totalResults 4),
  (all:"Qwen" AND cat:cs.CL) (1243), (all:"small language models" AND cat:cs.CL) (735),
  all:"OLMo" (832), (all:"on-device" AND cat:cs.CL) (1479),
  ((all:"open weights" OR all:"open-weight") AND cat:cs.CL) (1134), plus
  https://arxiv.org/list/cs.CL/recent (50 of 184 new submissions for 10-02 listed).
  In-window candidates surfaced and considered: roughly 140 distinct entries dated
  2026-09-02..2026-10-02 (2 from the Gemma query, 20 Qwen-list, 50 cs.CL-recent, 15 OLMo-list,
  20 small-LM, 15 on-device, 20 open-weights, minus overlaps). Floor was 30; cleared.
- Reddit fallback probes (curl on this network, UA mag-frontier-probe/1.0):
  - old.reddit.com/r/LocalLLaMA/top.json: status 302, redirect to /login/?reason=lor2 (same
    wall doors.md:48 recorded; still walled 2026-10-02).
  - api.pullpush.io submission search: HTTP 429 with body "Rate limit exceeded. This website
    does not provide free scraping resources for agents. Please contact the administrator on
    Discord if you're interested in a paid scraping service." PullPush is agent-walled today;
    the 09-30 sweep's PullPush door (register rows 16-19) no longer answers free.
  - arctic-shift.photon-reddit.com: probe 1 (limit=1) HTTP 200 full post JSON (id 1wvxjwk,
    created_utc 1790956782 = today, r/LocalLLaMA). Probe 2 fired back-to-back: HTTP 422
    "Timeout. Maybe slow down a bit". Probe 3 after `sleep 45` with query=Qwen after=1790812800:
    HTTP 200, 3 hits, first id 1wvvjsq. VERDICT: arctic-shift ALIVE and is the restored
    r/LocalLLaMA surface; recipe: `curl --tlsv1.2
    "https://arctic-shift.photon-reddit.com/api/posts/search?subreddit=LocalLLaMA&query=<q>&after=<epoch>&limit=<n>"`
    with ~45s pacing; WebFetch reads it too (plain, no TLS flag needed). curl without
    --tlsv1.2 intermittently dies with schannel SEC_E_UNSUPPORTED_FUNCTION on this box; the
    TLS flag is part of the recipe.
  - redlib mirrors: safereddit.com 200 but body is an Anubis JS challenge ("<title>Verifying
    your browser...</title>", /.within.website/x/xess) - no clean recipe; perennialte 403
    (5747-byte block page); redlib.catsarch.com curl TLS-fail 000 and WebFetch 429 (mixed,
    unresolved); redlib.privacyredirect.com and red.artemislena.eu TLS-fail 000 from this
    network. No redlib mirror yielded a working unauthenticated recipe today.
- Local instrument (RQ4): `ollama --version` -> "ollama version is 0.34.3"; `ollama list` ->
  17 models, NO nimble, NO tev1, includes gemma:2b (b50d6c999e59), gemma4:latest (c6eb396dbd59),
  frob/ling-3.0-flash:latest (77 GB, 2 weeks old). Ollama 0.35 is NOT installed here; the
  DIGEST:48 upgrade-and-systemone probe has not run.
- olm-x probe (RQ3): `curl https://api.fxtwitter.com/nahid_pro09/status/2102229686378213649`
  -> 200, full tweet text fetched today: "GLM-5.3-Flash is 100% FREE with UNLIMITED usage right
  now on ZCode (Extended) ... ZCode: unlimited GLM-5.3-Flash during promotional hours ...
  originally ending Sep 20 now extra 2+ weeks unlocked ... claim your unlimited runs before
  October 7". Matches register row 15 (watch/inbox/frontier_olm_2026-09-30/register.jsonl:15).
  It stays a promotional tweet, not an official z.ai page (09-30 DIGEST:75 honesty label).

## Answers to the 5 questions

1. Open-weight releases / license changes post-10-01 touching gemma:2b, gemma4, Ling radar:
   NO new Gemma release or license change post-10-01 found on arXiv (ti:"Gemma" newest is
   2609.30716, 09-25, already banked twice - see anti-rebank below) or on the model card
   (ai.google.dev/gemma/docs/core/model_card_4, "Last updated 2026-07-30 UTC"). The model card
   fills the 10-01 OWED "Gemma 4 license terms": License named "Apache 2.0"; variants E2B
   (2.3B effective, 5.1B with embeddings), E4B (4.5B effective, 8B with embeddings), 12B
   (11.95B), 26B A4B MoE (25.2B total, 3.8B active), 31B dense (30.7B); small models 128K
   context, medium 256K. Janitor slot read: the estate's gemma4:latest (9.6 GB GGUF) is the
   12B class; the card's local-execution claim covers E2B/E4B. Ling-3.1-flash radar CONFIRMED
   by a new dated primary (aiweekly, pub 09-30, upd 10-01): 560B total / ~25B active verbatim;
   three-stage rollout (free 256K trial -> paid 1M after Oct 13 -> open weights "after the
   trial"); caveat banked: "All 8 publicly visible benchmark scores for Ling-3.1-flash are
   vendor-reported from Ant's own launch screenshots; no third-party evaluation has occurred."
   Locally the box already holds the predecessor frob/ling-3.0-flash (77 GB).
2. Qwen small-model supply drying, post-10-01 confirmation: NOT obtained today. The arctic-shift
   Qwen search (after=2026-10-01) returned 3 posts, none read as supply-drying evidence at the
   depth fetched; the latest banked evidence stays r/LocalLLaMA 1wrez7j (09-30 register row 16).
   Academic side reads the opposite way: Qwen3.5-4B / Qwen3-4B are the default small backbones
   of the week's small-model papers (LLM2Jev 2610.02076, CallScreenBench 2609.23959, on-device
   routing 2609.18672). Substitutes that hold in the narrow small-model-with-tools regimes,
   from full-text reads: (a) the HARNESS, not the model, is the bottleneck - Mingbird 0.886 vs
   goose 0.631 on the same small models, 2B tier 0.821 vs 0.017-0.271 under cloud harnesses
   (2610.02001); (b) tool selection is lexical (BM25 resolves 162/164 exact and 85/166
   paraphrase), abstention is where the neural component is required (2609.18672); (c) small
   models are already Jev-style decision models out of the box - Qwen3.5-4B 81.4 pct JevBench
   training-free, fine-tuning pays only in narrow high-cardinality regimes like Banking77
   (2610.02076); (d) keyword harnesses fail OPEN on SLM tool-use claims - 600M vs 1B pair
   scored 0.660 vs 0.650 lenient but separated 6/6 vs 0/4-6 on verbatim reproduction
   (2610.02142).
3. olm-x free rung before Oct 7 close: it serves unlimited GLM-5.3-Flash on ZCode during
   promotional hours through October 7 (tweet re-fetched today, full text above). Worth a probe
   slot: yes, and cheaper than priced - the estate's own session account is this rung
   (account:zai-individual-coding-plan, GLM-5.3-Flash), so the 09-30 DIGEST:83 salon-fold ask is
   a $0 time-stamp of the credential before Oct 7, not a new spend. OWED stays: the official
   z.ai page confirming the extension (the tweet alone is promotional, OWED-1..4 of the 09-30
   fold remain open).
4. Ollama 0.35 91 ms/decision claim, verification status: still VENDOR-ONLY, now pinned
   tighter. Vendor primary fetched verbatim today: "Nimble 9B averaged 91ms per decision in the
   Pac-Man example below when running locally on an M5 Max" (blog post dated September 29,
   2026; the blog does NOT state what Tev1 is fine-tuned from). Second primary: NONE exists.
   The only independent Jev benchmark (2609.37647, full text read) benchmarks TypeSafe AI's
   HOSTED Jev (jev-1.13.0 API, 0.36 s client-side mean at 32 concurrency, 346,009 requests for
   US$9.15) and states Ollama and /v1/systemone do not appear - a different serving path, so it
   cannot confirm the local 91 ms number. The closest independent local latency datum is
   2609.23959: Qwen3-4B LoRA at 64.5 ms per decision (p95 110.5 ms) on one RTX 3090, i.e. the
   91 ms class is plausible on desktop GPUs but unmeasured on this estate's hardware. Local
   instrument run: ollama 0.34.3, nimble/tev1 absent (see Instruments). The DIGEST:48 $0
   three-arm probe (rule floor vs gemma:2b vs tev1:0.8b) remains the only instrument that may
   fill the routing-grid cell under the instruments-only law (laws.md:15).
5. Reddit fallbacks alive from this network (r/LocalLLaMA surface restored): arctic-shift
   ALIVE (curl --tlsv1.2 + WebFetch, query/after params work, pace ~45 s). Everything else
   mapped on 10-01 is now degraded or walled: PullPush 429 agent-walled (new degradation vs the
   09-30 recipe), old.reddit JSON still 302 lor2, safereddit behind an Anubis JS challenge,
   perennialte 403, catsarch unresolved (curl TLS-fail + WebFetch 429), privacyredirect and
   artemislena TLS-fail. Working recipe of record: arctic-shift, paced; pair curl and WebFetch
   before declaring any door dead (doors.md:74 held - the 422 was pacing, not death, proven by
   the sleep-45 retry).

## Items banked (8, strongest first; every quote from a page fetched this sitting)

1. Mingbird: A Local-First Agent Harness Enabling Small Open Models to Complete Real Tasks -
   arxiv.org/html/2610.02001v1 (10-01). Harness-not-model verdict on exactly our janitor
   family: gemma4:e2b, gemma4:12b, qwen3.5:4b, ornith-1.5:35b via Ollama Q4_K_M; Mingbird
   0.886 vs goose 0.631 / opencode 0.479 / agent-mini 0.405; silent-abandonment and
   156-call-zero-artifact loop classes named; byte-level net-zero prefill budget (797 static
   tokens) and finish gate are the two mechanisms that move the number.
2. LLM2Jev: LLMs Are Already Jev-Style Decision Models - arxiv.org/html/2610.02076v1 (10-01).
   Qwen3.5-4B training-free 81.4 pct on 231 JevBench items, ECE 0.057; fine-tuning pays only
   narrow high-cardinality regimes (0.6B Banking77 +35.0-42.6 pts); intent-only FT DEGRADES
   81.4 -> 76.2 while loss falls - the shortcut-learning signature the estate's own grader laws
   warn about.
3. Evaluating and Benchmarking the System One Model Jev - arxiv.org/html/2609.37647v1 (09-29).
   Independent Jev numbers: 96.5 IMDB / 91.8 MMLU / 73.9 ANLI; beats Qwen3.8-27B on 27/37
   datasets and Gemma-4-E4B on all 37; 0.36 s mean latency hosted; MMLU-withheld-question drop
   to 31.5 pct (memorization probe); Ollama/systemone absent - the 91 ms local claim keeps no
   second primary.
4. Keyword Harnesses Fail Open - arxiv.org/html/2610.02142v1 (10-01). SLM tool-use claims
   audited by a 4-rung cheap ladder; lenient keyword harness 0.660 vs 0.650 while verbatim
   reproduction separates 6/6 vs 0/4-6; over-trigger on near-miss prompts 0.087/0.174 pass.
   Directly sharpens the estate's gate-canary and citation-lint instincts: keyword gates fail
   open, exactly the class AGENTS.md already ratchets.
5. Selection Is Retrieval, Abstention Is Not - arxiv.org/html/2609.18672v1 (09-16). On-device
   routing over 70 actions: BM25 0.140 ms / e5-base int8 13.7 ms CPU; separate gate cuts
   delegate-to-skill errors 134/150 -> 12/150; "Abstention, not selection, is where a neural
   component is required"; Gemma 4 E4B-it and Granite 4.0 H-Small FAILED to deploy under vLLM
   0.27.1 - a stack warning for any estate vLLM move.
6. Open-Jev Judgments on CallScreenBench - arxiv.org/html/2609.23959v1 (09-21). Qwen3-4B LoRA,
   64.5 ms per decision (p95 110.5) on one RTX 3090, AUROC 97.4, ECE 5.2, 100 pct on legit
   calls, ~30x cheaper than the judge API. The closest independent measured analog to the 91 ms
   claim, and a template for the estate's typed-decision-oracle line.
7. Gemma 4 model card - ai.google.dev/gemma/docs/core/model_card_4 (last updated 2026-07-30).
   Fills the 10-01 OWED "Gemma 4 license terms": Apache 2.0; five variants E2B/E4B/12B/26B
   A4B/31B; 128K/256K context; no post-10-01 change evidenced. License TEXT page itself still
   unfetched - residual OWED, narrowed.
8. Ling-3.1-flash release alert - aiweekly.co/alerts/ants-inclusionai-ships-ling-31-flash-
   with-560b-parameters (pub 09-30, upd 10-01). Confirms the radar line with dates and the
   vendor-scores caveat; three-stage rollout; 1M paid tier after Oct 13.

## Anti-rebank statement (burns.md:174-184 honored)

- 2609.30716 (Gemma 4 behavioral eval) was fetched full-text this sitting, then DROPPED from the
  bank: already item #6 of the 09-30 sweep
  (watch/inbox/frontier_olm_2026-09-30/sweep/open-and-local-language-models-arxiv.md:24) and
  explicitly marked "drop: banked by 09-30 olm sweep (#6)" in the 10-01 sweep line 67.
- The Ollama blog was banked in the 10-01 sweep line 156; today's fetch adds only the verbatim
  pin and the no-second-primary verdict, banked in Q4 above, not as an item.
- All six arXiv items hold ~2 KB abstract stubs in catalog/catalog.jsonl
  (state/arxiv/<date>/<id>v1.txt, e.g. 2610.02076v1.txt mtime 2026-10-02T06:30:25Z, 1,621
  bytes); rg confirms none of the six appears in the 09-30 or 10-01 olm sweep files except the
  two dropped above. This sweep's contribution is the full-text depth and the numbers, not the
  discovery of the ids.

## OWED (carried, not asserted)

- The 91 ms/decision local number: no second primary exists; local instrument reads Ollama
  0.34.3 with nimble/tev1 absent. Fill only via the DIGEST:48 probe on upgraded 0.35.
- Official z.ai confirmation of the GLM-5.3-Flash promo extension (olm-x OWED-1..4, 09-30
  DIGEST:75) - tweet-only evidence as of today.
- Qwen supply-drying post-10-01 community confirmation - not re-established today; 1wrez7j
  remains the latest banked row.
- Gemma 4 full license text page - card names Apache 2.0; terms doc not fetched.
- arctic-shift rate-limit envelope (how many queries per window before 422) - one data point
  (back-to-back fails, 45 s spacing passes), not a curve.

## Honesty notes

- arXiv full texts were read through WebFetch's extract-and-answer instrument with verbatim
  instructions; ids and titles cross-checked against catalog stubs. Quote marks in the JSON are
  as returned; en-dashes normalized to hyphens per house ASCII law.
- The Ling-3.1 WebSearch snippet claimed CyberGym 87.90; the fetched aiweekly page contains NO
  benchmark numbers and says all visible scores are vendor-reported. The snippet number is NOT
  banked.
- PullPush's 429 text and arctic-shift's 422 text are quoted verbatim from the curl bodies
  above; no fallback success is claimed beyond what a command returned.
