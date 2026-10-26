# Sweep: inference-efficiency via hn - source-fetched: 2026-10-06

Seat: sweep gopher (inference-efficiency, Hacker News door). Two passes per ask.

## Pass 1 (broad census)

HN Algolia API over the window 2026-09-06..2026-10-06 (`numericFilters=created_at_i>1788652800`,
`tags=story`), 8 queries, both `search_by_date` and relevance `search`: "inference",
"model routing llm", "reasoning tokens", "quantization", "smaller model offload agent",
"tokens per second throughput" (relevance mode; **nbHits: 0**, reported as-is, no fallback
fabricated), "KV cache", "inference cost cheap model", "distillation". Roughly 70 distinct
candidate stories considered; the 30-candidate bar is cleared with margin. Candidate pool
(highlights): 49980715 openTPU, 49973521 VeloGB10, 49971028 Ototo, 49968241
engineering-behind-LLM-inference, 49966715 inference-market essay, 49964551 Gartner-96
economics, 49961971 Gutsy, 49960535 Recursant, 49951356 Ask-HN solo moat, 49911500
weave-os/router, 49800187 Relay gateway, 49689250 Swobu, 49979498 codex-reasoning-token-
experiment, 49815972 Reasoning Yield, 49727511 Swift-Qwen3.8-27B, 49833102 UkisAI Swift
series dup, 49840698 control-token CoT suppression, 49861047 Codex $78k runaway, 49888619
reasoning budget API-vs-Codex, 49823211 quant stress-test, 49822130 Lifeboat, 49804932
vla-edge, 49778955 QLoRA explainer, 49743523 4-bit rotational quantization, 49703818
Flash-Next GSQ, 49676635 per-tensor GGUF layout, 49644045 glq vLLM plugin, 49611128
Qwen3.8-27B quant benchmark, 49813610 trained KV cache bank Jev, 49796779 what-are-KV-
caches, 49838474/49632252 KV-CREAM essay, 49619645 zero-copy KV migration, 49945575 KV
memory wall, 49893944 Fathom, 49783040 Ask-HN KV for swarms, 49699918 kv-cache-truth-
auditor, 49735358/49879775 FastRecall, 49699267 Nari Qwen3 TTS, 49807276 Shrewd, 49802789
InstinctFlash, plus the distillation-policy news cluster (CISA/OpenAI/CNBC, off-area).

## Estate-side grounding (what I ran here)

- Prior-sweep dedupe: read this session,
  `watch/inbox/frontier_olm_2026-10-05/sweep/inference-efficiency-hn.md` (196 lines). Its 8
  banked items (agentic-kv-cache 49643543, Magnitude 49911995, Decision Models 49934323,
  getunblocked AIMD routing 49897322, doug.sh prefix cache 49758259, j9s.io agentic KV
  49701675, Yandex KV runtime 49578969, token-compression CLI 49911910) and its 2 rejects
  (justine.lol 49938916, DeepSeek KV blog 49735410) plus the 09-30 bank of 8 (vLLM AMD
  49596054, prompt-lookup 49859982, Mozilla benchmark 49742415, Mercury 2.5 49823348,
  slotstream 49524447, JevBench 49800574, Ollaya 49848269, DeepSeek beta 49607094) are ALL
  excluded from re-banking this window. Every item below is new against both lists.
- Overlap greps run this session: `grep -ic "weave-os\|quesma\|Swift-Qwen\|Lifeboat\|
  kv-cache-truth-auditor\|Recursant\|Ototo\|rotational quantization\|per-tensor layout\|
  gutsy" catalog/catalog.jsonl` over 1,096,848+ rows returned **0**; per-term loop hits only
  Shrewd (excluded, see below). `grep -rin` over `memory/` for the same terms plus
  "thinking.*x1.95" and "reasoning-token-experiment" returned only nautical "lifeboat" lines
  in `memory/corpus/ractors/esoterica/texts/pg41971.txt` (irrelevant).
- EXCLUDED: Shrewd (49807276) - the 10-05 sibling sweep already fetched its README
  (`catalog/catalog.jsonl:1073391`, `_shrewd_readme.md` 41,004 bytes, mtime 2026-10-05).
  Re-banking known work is waste.
- EXCLUDED: distillation-campaign policy news (CISA aa26-251a, OpenAI/Kimi, CNBC Huang,
  ~10 items) - security-policy news, not inference-efficiency engineering.
- EXCLUDED: arXiv abstracts the arxiv door already holds (49880342 on-policy distillation
  confirmed via `_abs_onpolicy.html` in the 10-05 sweep dir; 49840698, 49893944, 49883064
  same class). The estate holds the PAPER layer; HN banking must add measured threads and
  engineering claims.
- Envelope note: no external source this window publishes a numeric rolling-throughput cap;
  the estate's width-10/109.4M tok/h number remains estate-original (unchanged from the
  10-05 sweep's finding, re-confirmed by absence in today's census).

## Pass 2 (deep reads, 7 items read end to end)

Three HN threads read end to end (49911500, 49611128, 49727511). Three threads were EMPTY
shells (0 comments: 49822130, 49961971, 49699918) - per the recipe the thread was supposed
to be the signal and was not, so I fetched the linked source pages directly instead
(2 GitHub READMEs + 1 article). Plus one repo fetch for a fresh 2026-10-06 story
(codex-reasoning-token-experiment). All 7 banked items below were read by me this session;
quotes are verbatim from the fetched pages.

## Banked items (8, strongest first)

1. **Weave Router 2.0: open-source model routing for coding agents** (HN item 49911500,
   2026-09-30, 122 pts/42 comments, github.com/weave-os/router). The founder argues AGAINST
   the estate's Q4 prior in public: Copilot-style routing "only route once per session (or
   subagent)" is "basically impossible to do correctly" - his router re-decides PER TURN via
   an HMM session-state trace + a capability-bucket classifier ("the single biggest
   performance unlock" against "10^100 possible paths" over a 100-turn session), and the
   cost win is CACHE-AWARE NON-SWITCHING: a subsystem computes the expected value of
   switching models to avoid paying cache-fill costs, and "This is where most of our
   improvement on cost has come from." Claims: Terminal Bench 4.0 / SWE Atlas parity with
   GPT-6 Astra at ~52-54% cost, 2.2-2.5x faster. Commenters pushed back: svnt (can a
   frontier-labeled router exceed the frontier? answer: "We're training a frontier
   router"), capocasa (switching generates "a lot of non-cache input tokens"), devmor
   (multi-model failure modes: models hallucinating "control instructions"). Why it
   matters: Q4+Q5 in one thread - external engineering says route-per-turn with
   switch-EV gating, NOT pin-forever; and its biggest cost win is exactly the estate's Q5
   census result (zero in-session switches) read as a FEATURE: the switch machinery's value
   is not in switching but in pricing the switch and mostly declining it. The trained
   router itself is closed-weight; no local-model support yet.
   Overlap: catalog grep "weave" 0 relevant rows (only darkweaver .cpp + pytest-tmp);
   memory 0; both prior sweep banks 0. Genuinely new.

2. **Benchmarking Qwen3.8 27B quantizations: 4-bit holds up, 1-bit collapses** (quesma.com
   blog, HN item 49611128, 2026-09-08, 286 pts/139 comments). End-to-end Terminal Bench 2.1
   task-success benchmark across quant tiers with Wilson 95% CIs; author (stared):
   "there is little difference down to 4-bit; only the 2-bit scores a bit lower", 1-bit
   collapses to near random-guessing; ~"$500 per a single combination". Two transferable
   finds beyond the headline: (a) kmike84 - KL-divergence quality numbers "are dramatically
   different, depending on which dataset you use"; KLD on agentic traces reads far worse
   than on wikitext, and stared agreed KLD "does not measure what any e2e test does" - the
   estate's quant register (tests/test_inference_budget.py rows) should never fill from
   KLD/proxy metrics; (b) the QUANT x THINKING interaction (sharmajai + anyfoo): quants
   shift the token distribution and the model "offsets that by just thinking more";
   anyfoo: even Q5 "seems to be enough to kill the model's ability to solve a particular
   problem in reasonable time", thinking mode drove it into "thinking itself into an
   extremely expensive and error-prone approach without backing out", and REASONING-OFF
   fixed it - direct external evidence for Q2's contamination suspicion (thinking-ON
   economics are quant-dependent; an explicit-off re-measure can flip verdicts). Side
   numbers: skolos NVFP4 on RTX 5090 "10k tok/s prompt processing, 200 tok/s generation"
   at 200k context; KV-cache quant "has almost no impact on this model all the way to
   q4"; zrail's full llama.cpp config (IQ3_S + q4_0 KV + spec decode) at 30-50 tok/s on a
   5060 Ti.
   Overlap: catalog grep "quesma" 0; memory 0. The estate's pending "scoped qwen2.5:7b
   Q4_K_M vs q8_0 A/B" (10-05 lens/burns.md next-actions list, read this session) is a
   different model and tier - this is the 27B external complement, not a duplicate.

3. **Codex reasoning-token experiment: same model, byte-identical input, 32x reported
   reasoning-token difference by auth surface** (github.com/johnmu/codex-reasoning-token-
   experiment, HN item 49979498, posted 2026-10-06; repo fetched). 960 responses, fresh
   sessions, "the same Codex client, requested model and thinking level, with byte-identical
   model input for each matched pair"; a local proxy enforced byte-equality; API key vs
   ChatGPT Pro sign-in. Bookstore task, Luna 6 Medium: 96.3 vs 3.0 avg reasoning tokens -
   "about 32x more across 40 completed responses per sign-in"; all four model/level
   differences survived multiple-comparison correction in study + follow-up. Accuracy was
   EQUAL ("All 480 bookstore decision sets were correct") - "More tokens did not
   automatically mean a better answer." Caveats the author states honestly: counts are
   "reported usage" only, cause unknown, one credential + one account + two prompts,
   reproduction invited. Why it matters (Q2): the estate's whole spend ledger
   (memory/burns/LEDGER.jsonl, usage.jsonl banking) meters REPORTED usage; this is measured
   proof that reported reasoning tokens vary ~32x by surface at equal accuracy, i.e. a
   thinking-ON economics comparison across surfaces can be an artifact of the surface's
   hidden budget, not of the work. The explicit-off re-measure (laws.md:109) is the control
   this study lacks.
   Overlap: catalog grep 0; memory grep 0. Genuinely new (posted today).

4. **Swift-Qwen3.8-27B: -58.3% thinking tokens at flat accuracy** (huggingface.co/
   ukisai/Swift-Qwen3.8-27b, HN item 49727511, 2026-09-16, 33 pts/17 comments). Post-trained
   thinking reduction, not a prompt trick: overthinking-loop traces mined for "common
   denominator" tokens, an inference-time token penalizer, LoRA SFT, then GSPO RL + on-policy
   distillation to restore accuracy. Measured (vs base at xhigh, 5 runs): GPQA-Diamond 88.4%
   -> 88.3% at 58% fewer median thinking tokens (2,771 vs 6,642); MMLU-Pro 85.5 -> 85.0 at
   -28%; Terminal-Bench 2.1 66.7 -> 65.8 at -39%; honest regression: AIME 98.7 -> 94.0 from
   a training bug penalizing a math-relevant token. Thesis: "reasoning length IS extremely
   important and should NOT be shortened by force, but rather optimized." Thread gold for
   Q2: zionsati cites "research showing lower quants suffer from low confidence in its own
   reasoning and tend to overthinking because of that" - the same quant-x-thinking axis as
   item 2, from the model side; author admits loops still occur, "very rarely (as opposed to
   the Base Qwen 3.8 27B)"; pu_pe voices the accuracy-skeptic prior; billziss offers a light
   oMLX Q8 replication ("certainly seems to cut down on thinking compared to stock").
   Why it matters: an alternative axis to EMPTY_REASONING skip-on-sight - a FAMILY_TABLE
   entry that spends fewer thinking tokens by training rather than by off-switch; also a
   template for the estate's own anti-overthinking penalizer on the janitor fleet.
   Overlap: catalog grep "Swift-Qwen" 0; memory 0; the smaller dup post 49833102 was never
   banked either. Genuinely new.

5. **Gutsy: subsecond-ish decision-model inference on CPU, Jev-format, no API**
   (github.com/kouhxp/gutsy, HN item 49961971, 2026-10-05, 3 pts/0 comments; README
   fetched because the thread was empty). Full fine-tune of Qwen3.5-0.8B on ~105,000
   questions (one epoch, ONE 80 GB GPU, roughly an hour) with "cross-entropy plus Brier
   loss on soft labels", teacher Qwen3.8-27B with two-pass agreement filtering; serves
   calibrated probabilities via llama.cpp on CPU: "Send a state (text or JSON) and typed
   questions (yes/no, choice, score); get a probability for every option back." Q8_0
   775 MB, Q4_K_M 505 MB "25-30% faster". The claims-vs-receipt catch the estate runs on
   itself: "subsecond" holds only for typical inputs - "median 4.3 s, 95th percentile
   27 s on JevBench's hard tier (Q8_0)" - and Jev-via-API still wins quality on 3/3
   benchmarks (BoolQ 0.906 vs 0.837; CommonsenseQA 0.863 vs 0.577); calibration 0.022
   in-distribution but 0.137 on hard unfamiliar items.
   Why it matters (Q1): external replication of the estate's day-5 dominant find (decision
   models create a rung UNDER gemma:2b) with a concrete trainable recipe at 1-GPU-hour
   cost - the estate's typed-verdict lattice (tri-state, lane gates) is exactly this
   shape, and the p95 caveat says the rung's SLA must be quoted per question class, not
   as one "subsecond" number.
   Overlap: catalog grep "gutsy" 0. Adjacent-but-held: JevBench banked 09-30, Jev arXiv
   abstracts held, Decision Models llama.cpp post banked 10-05 (item 3 there). The new
   delta is the training recipe + honest CPU latency tail, not the Jev concept.

6. **A cache hit is not proof that you skipped the work (LLMTraceFX kv-cache-truth-auditor)**
   (siddhantkhare.com/writing/kv-cache-truth-auditor, HN item 49699918, 2026-09-14, 2 pts/0
   comments; article fetched because the thread was empty). "A cache hit can be true and
   still fail to prove that work was skipped" - the auditor validates an engine's cache-hit
   attestation against five independent checks (independent token oracle - "the engine
   cannot verify itself", observed prompt work, output token-identity, evaluator
   correctness, hash-bound verifier); failures "fail closed". Synthetic control shows the
   failure taxonomy: interior mutation = partial_reuse (3 reused / 6 processed), same-length-
   different-ids = zero reuse ("Equal length creates no identity"), namespace isolation =
   verified miss, eviction = its own verdict. Lessons: "Mutation position defines the
   reusable prefix"; eviction/isolation/cold misses are distinct causes a bare miss verdict
   cannot separate; and explicitly unproven: "Null is not zero."
   Why it matters (Q5 + the estate's cache-receipt lane): the switch-machinery retirement
   question and any "we saved N tokens by caching" row need exactly this five-check chain -
   a cache receipt that only counts hits proves skip only when prefix identity, output
   identity, and evaluator agree. Directly upgrades the build_wave b2 cache-receipt lane's
   verdict vocabulary (verified_hit / partial_reuse / evicted / isolated, not a boolean).
   Overlap: catalog grep "truth-auditor" 0; memory 0. Genuinely new.

7. **Weaviate 4-bit rotational quantization vs TurboQuant for embeddings** (weaviate.io/
   blog/4-bit-rotational-quantization, HN item 49743523, 2026-09-17, 5 pts). SCOPE NOTE
   first: this is vector-EMBEDDING quantization for ANN search, not LLM weights or KV -
   do not file it in the model-quant register. Random rotation via FWHT then 4-bit scalar
   quant plus outlier correction ("largest two magnitude coordinates exactly"); "4-bit RQ
   provides similar recall with a 45% heap reduction" vs 8-bit, and head-to-head vs
   4-bit TurboQuant variants "RQ4c wins on 7/8 datasets" (margins ~0.1-3.2 recall points;
   TurboQuant wins msmarco-arctic 95.9 vs 95.8; paper-faithful TurboQuant "loses on every
   dataset"). Speed: RQ8 encoding 3.8x faster, prefetching "+7-11% query throughput and
   12% faster imports"; recall "flat across a 1M-250M range" on Meta's Sphere corpus.
   Why it matters: the estate holds TurboQuant as kernels (catalog/catalog.jsonl:29813-29816,
   lmcache turboquant kernels, per the 10-05 sweep's overlap note read this session) - this
   is the first external head-to-head with a measured verdict against it, and the 45%-heap
   result prices the memory/lenses embedding tier (lens corpus index, concept predictor)
   where heap, not tok/s, is the budget line.
   Overlap: catalog grep "rotational quantization" 0; TurboQuant prior art HELD as code
   (row above) - the comparison is the new delta. Genuinely new.

8. **Lifeboat: the 2-6x headline the README does not contain** (github.com/IterateAI/
   lifeboat-releases, HN item 49822130, 2026-09-23, 6 pts/0 comments; README fetched because
   the thread was empty). The HN title claims "2-6x more concurrent agent sessions per GPU,
   no quantization"; the README contains NO such number - the only concurrency figure is
   "the 2x concurrency" reserved for the container image (with FP8 KV cache and speculative
   decoding), and the measured server-vs-server numbers are "1.94x llama.cpp on a 64-core
   server", "2.01x ollama on a Jetson", "1.48x on a Mac". One real engineering line:
   "Decode speed is limited by memory bandwidth, not by core count." Free tier caps at
   "Up to 2 concurrent inference servers, single node"; NPU sits idle.
   Why it matters (Q3): banked as a NEGATIVE result - a vendor headline that outruns its own
   receipt, caught by the same read-the-README move the estate applies to its own tok/s
   claims; and the bandwidth-bound reminder says the 12-16 width rung's limit will be
   rolling throughput/memory-bandwidth, not session count. No independent measurement of
   the 2-6x claim exists anywhere I fetched.
   Overlap: catalog grep 0; memory grep only nautical "lifeboat" in esoterica (pg41971).
   Genuinely new.

## Surveyed and REJECTED (pass-2 candidates that did not survive)

- Ototo (49971028), Recursant (49960535), Reasoning Yield (49815972), Relay gateway
  (49800187), Swobu (49689250), MoE microscope (49690947), openTPU (49980715), VeloGB10
  (49973521), Gartner-96 essay (49964551), inference-market essay (49966715): candidate
  threads carry 0-1 comments and were not deep-read; not banked under the
  bank-only-what-you-read rule. They remain unmined leads, listed in pass 1 above.
- Ask HN: Is provider KV caching sufficient for agent swarms (49783040): 0 comments,
  question unanswered - nothing to bank.
- Distillation policy cluster (CISA aa26-251a, OpenAI/Kimi disruption posts, CNBC Huang
  49879032, Garry Tan 49655978): off-area (adversarial distillation policy, not
  efficiency economics).
- Known/banked items re-surfaced by today's queries (16 IDs from the 09-30 + 10-05 banks,
  plus 49735410 and 49938916 rejects): all excluded per the dedupe block above.
- Shrewd (49807276): already fetched by the 10-05 sibling sweep (catalog:1073391).

## Door health

- hn.algolia.com API: clean (9 queries; one returned nbHits:0 - "tokens per second
  throughput" in relevance mode - reported as-is, not a degradation).
- news.ycombinator.com item pages: clean fetches, but 3 of 8 fetched threads (49822130,
  49961971, 49699918) were EMPTY (0 comments) - reported per-item; the signal was recovered
  from the linked sources, which is the recipe's own instruction ("the thread is OFTEN the
  real signal"), not a fabricated fallback.
- github.com (x3), siddhantkhare.com, weaviate.io, quesma/HN, huggingface.co/HN: all clean.
- No fallback success was fabricated anywhere.

## OWED / not done here

- Any width-12/16 measurement or tok/h run: not run here (sweep seat, no dispatch executed
  this session); Q3 stays estate-measurement work. External analog absent: no public source
  in this window publishes a rolling-throughput cap or a 12-16 width curve.
- The quant-x-thinking interaction (items 2 and 4 agree) is the strongest new external
  hypothesis the estate could falsify cheaply on its own A/B: does q4 janitor thinking-ON
  burn more thinking tokens than q8 at equal verdict quality? OWED to
  tests/test_inference_budget.py owners.
- Ototo/Recursant/Reasoning-Yield remain unread leads if a later window wants them.
- The codex-reasoning-token-experiment authors request independent reproduction across
  accounts/dates; the estate could contribute one replicated pair from its own dispatch log
  (byte-identical re-stage, API vs free-lane surface) - OWED, not done.
