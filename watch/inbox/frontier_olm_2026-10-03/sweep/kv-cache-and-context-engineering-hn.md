# SWEEP: kv-cache-and-context-engineering via HN (frontier_olm 2026-10-03)

source-fetched: 2026-10-03

RECONCILIATION HEADER (pass B, appended same day). This path already held a completed
sweep written by this seat name earlier today (pass A below, preserved verbatim; its 4
banks and 13 deep reads stand as filed). A second invocation of the same ask re-ran the
door independently. Per the anti-rebank laws (lens/burns.md section 5), pass B did NOT
re-bank pass A's items and did NOT re-bank work the greps showed already held. Pass B's
byte-checked dedupe verdicts, its own deep reads, and its 4 genuinely new banks are in
the PASS B section at the bottom. Nothing in pass A was edited.

---

## PASS A (found at this path on arrival; preserved verbatim; written earlier today)

source-fetched: 2026-10-03

Seat: sweep-kv-cache-and-context-engineering-hn. Doors: hn.algolia.com `search_by_date` + `search` (both answered JSON first try, every call), then news.ycombinator.com item threads, then the underlying articles/repos/abs pages. Zero 403s, zero degraded doors this run; no fallback used and none claimed.

### Pass 1 (broad sweep)

Eleven Algolia queries fired: search_by_date for "KV cache", "prefix caching", "context compression LLM", `"lost in the middle"` (empty result, stated), `"long context"`, `"context engineering"`, "vLLM", `"agent memory"`, `"context rot" OR "context degradation"` (empty result, stated); search (relevance) for "KV cache" points>10 and "context rot". Roughly 60 unique in-window (2026-09-03..10-03) candidates considered, including: token compression CLI 49911910, Fathom 49893944, Internet-for-the-KV-Cache 49883064, KV-Cache-Rules-Everything 49838474/49632252, InstinctFlash 49802789, What-are-KV-caches-really 49796779, Ask-HN-provider-KV-swarms 49783040, doug.sh prefix cache 49758259, DeepSeek-V4.1-Flash 49735410, token-CDN 49714867, j9s.io 49701675, cache-hit-not-proof 49699918, LRU-is-harder 49643543, Zero-Copy-KV 49619645, Yandex-KV-agent-runtime 49598646/49578969, Magnitude 49911995, Replay 49691257, Prompt-Trees 49637425, LensVLM 49820496, Learning-How-to-Forget 49896983, MOBA 49687552, context-engineering-kit 49571131, When-Fancy-Eviction-Fails 49927418, OKF-Agent-Memory 49581240, Skillsync 49743049, dwarfstar 49936575, Red-Hat-Jev-benchmark 49933476, System-One-serving-blog 49936590, D-Engine 49925593, agent-cost-bench 49927585, plus the boolean.ai context-rot 49734038 and the agent-memory cluster (18 hits).

### Pass 2 (deep reads, fetched and actually read this ask)

Thirteen pages fetched end to end: github.com/gauravapiscean/agentic-kv-cache README + HN thread 49643543; zartbot.github.io DeepSeek-V4.1-Flash arch post; github.com/magnitudedev/magnitude README; siddhantkhare.com/writing/kv-cache-truth-auditor; j9s.io/posts/agentic_inference/; boolean.ai context-rot post; arXiv abs 2609.28870 (Fancy Eviction); research.yandex.com KV-as-agent-runtime; arXiv abs 2609.17652 (Fathom); arXiv abs 2608.01526 (Internet for the KV Cache); developers.redhat.com decision-models benchmark; supercomputing-system-ai-lab.github.io System-One serving post. Of these, nine were already-held corroboration reads and four were new-item deep reads (Fathom, Internet-KV, Red-Hat benchmark, System-One blog). Every item banked below was read by this seat this ask.

### Overlap findings (greps run this ask, ripgrep over catalog/catalog.jsonl, memory/, and all five prior sweep dirs)

- This area was swept five prior times (20260928, 09-30, 10-01, 10-02 x multi-lane). Already HELD, read this ask as corroboration only, NOT re-banked: LRU-is-harder repo+thread (banked 09-30 + 10-01 item 2, 17.5/33.1 decomposition), DeepSeek-V4.1-Flash (banked 10-01 item 4), j9s.io (banked 10-01 item 5), boolean.ai context-rot (banked 10-01), Yandex KV-as-agent-runtime (banked), When-Fancy-Eviction-Fails 2609.28870 (triple-banked: 0928 arxiv sweep lines 103-112, 10-01 kv-arxiv corroboration :41, mickey17 kv-agents-week.json claim row idempotency-keyed), truth-auditor/LLMTraceFX (banked 09-30 by the reddit sibling item 6, promoted to memory/percolator/candidates.jsonl row 2 canonical 6c6f025ce875fa28), Magnitude (judged "off-questions per 10-01" by prior lanes; my README read found it on-question but self-reported-thin, left unbanked with that disposition stated), Ask-HN-swarms, doug.sh, Prompt-Trees, Replay (banked as leads 09-30).
- Fathom 2609.17652: catalog row 050b090834b5 = 1,353-byte abstract pull (state/arxiv/2026-09-17/2609.17652v1.txt, mtime 09-17), listed but never read or banked (10-01 quant-arxiv "Unbanked near hits ... NOT read at abstract level" list; 10-02 kv-hn OWED named it an open lead). Closed this ask.
- Internet-for-the-KV-Cache 2608.01526: catalog 0, memory 0, prior-sweep listings only (pass-1 volume tables), never read or banked. Closed this ask.
- Red Hat Jev benchmark 49933476: the 10-02 evals-self-improvement sibling saw it and passed (evals-self-improvement-hn.md:80 "lower marginal value" for their questions); never banked; my area has the stronger claim (decision-model rows). Banked here with that disposition disclosed.
- System-One serving blog 49936590 / supercomputing-system-ai-lab: zero hits in catalog, memory, and all prior sweeps. Clean new primary.
- `2609.28870`/`Fancy Eviction` catalog greps: 0 rows; `magnitudedev`: 0 catalog rows; `LLMTraceFX`: 0 catalog rows.

### Research question verdicts

**Q1 (KV techniques shipping in open serving stacks; extend, do not re-open, KVarN).** Nothing re-opens KVarN: the closure stands (parity-not-win 59.3 vs 59.4 AIME25, arXiv 2606.03458, PR #21038 sourced, per frontier_olm_2026-10-03/lens/burns.md:71-76). Extensions found, all composable with the closure: (a) Fathom 2609.17652 moves quantized-offloaded KV from static read cost to per-query adaptive read depth (4-bit K stored channel-major as bit planes; reading t planes = t-bit quantization; reverse-water-filling bit budget) - 1.67x decode GPU-time at 1M tokens on Qwen3-8B vs 136-bit scans of Double Sparsity/Loki/SparQ r=32, matches the 136-bit scan at 92 bits on real coding-agent sessions, exact top-k on RULER-style tasks, and no speedup when the index sits in GPU memory; (b) the held DeepSeek-V4.1-Flash post re-read this ask confirms FP4-class KV (MXFP4/NVFP4-style, E2M1 + E4M3 per-16-channel scale, QAT) shipping in an open-weights frontier stack at ~890 bytes/token global KV - a data point below the estate's banked 3-bit floor, which the floor law should absorb as "QAT-only, closed-loop"; (c) System-One serving blog (clean new primary) ships a decision-model serving runtime on vLLM 0.30 whose scheduler uses predicted output length for queue reordering and predicted session return for KV keep/evict, with measured SLO/goodput numbers (below). Magnitude claims cross-session prefix-cache sharing in an open engine but self-reported numbers only (2x vs llama.cpp, 92% faster Metal decode, 27% less memory/agent); prior lanes judged it off-questions; left unbanked.

**Q2 (context degradation at 100k+ for agentic workloads). No new unbanked primary on this door this window; the held set stands.** The 30-day candidates were all previously banked: boolean.ai context-rot (250k/500k prefill arms on terminal-bench v4; GPT-5.6 Sol 31%->24% regardless of context relatedness, Opus 5 flat on unrelated but 50%->40% on task-relevant context, "momentum-induced collapse" at 250k+), How-Fast-Do-Agents-Rot 2609.01660 (banked 09-30), j9s.io traffic shape (banked 10-01: median agent prefill 15,146 tokens/turn, agent median gap 0.18s vs chat 96.24s, ~2x chat context by turn 10). Both quoted-phrase Algolia queries ("lost in the middle", "context rot OR context degradation") returned empty by-date result sets - stated, not papered over. The estate's specced KV degradation ladder still has no new public competitor instrument.

**Q3 (compression compatible with the byte-identical-asks cache-hit law).** The load-bearing instrument is already held and I re-verified it byte-true this ask: the truth-auditor's five-check attestation (token oracle expected-reuse, observed prompt work, output-token identity vs no-cache control, evaluator correctness, hash-bound evidence bundle; verdict enum verified_hit/partial_reuse/verified_miss/evicted; synthetic ten-case control: exact dup 8/9 reused, same-length-different-token-IDs 0 reused) - banked 09-30 by the reddit sibling and sitting as percolator candidate row 2. Its mechanism is exactly the estate's law made falsifiable: byte-identical prefix is necessary but not sufficient (namespace isolation and eviction are named zero-reuse causes), so the estate's cache-hit instrumentation should carry the verdict enum, not a hit boolean. New this ask: nothing banked; the token-compression CLI (49911910) remains the one unbanked Q3 lead, considered and not read (prompt compression that rewrites bytes is presumptively incompatible with prefix identity - unverified, flagged as such).

**Q4 (KV eviction policies for agentic long-tool-loop vs chat).** Settled law re-confirmed from held items: recency/LRU is the production answer; fancy eviction adds little because agentic prefix reuse is paced by active sessions (Fancy Eviction triple-banked: 14 policies, two production traces, "Despite a large gap to Belady, sophisticated policies designed for traditional caches provide little benefit over LRU"; LRU repo: 33.1% of recompute after <10s gaps, capacity-bound, Belady-oracle loss was a harness bug). NEW datum this ask (System-One blog): a learned keep/evict signal (Jev return-prediction, AUROC 0.60) LOSES to a simple turn-count heuristic (0.68) on conversation-KV retention - the third independent simple-heuristic-wins result after LRU-leaf and Fancy Eviction, now at the admission/retention layer. The strongest agentic-specific published policy remains the held j9s.io state-driven reordering (dontneed/pageout/default-LRU/willneed hints from per-tool EWMA gaps; GPU-local hit-rate 1.06-1.44x). Agentic-vs-chat shape: held j9s.io numbers carry it.

### Items banked (strongest first)

1. **Rethinking LLM Serving with System One Models** (supercomputing-system-ai-lab.github.io, HN 49936590, 10-02). Clean new primary; likely the serving-side source behind the fold's banked two-runtime rows; second source for the ~92ms hosted decision-model latency family (fold's 91ms Nimble/Tev1 was flagged single-source); measured vLLM 0.30 replay of 2,000 ShareGPT requests: SLO attainment 75%->99%, P90 TTFT 8.3s->0.17s, goodput +15-21%, open models 51-284ms on one H200; and the Q4 retention finding (learned return-prediction AUROC 0.60 loses to turn-count 0.68). Quote: "It writes nothing. An answer is one forward pass over the request, with no output tokens to generate or pay for".
2. **Fathom: Per-Query Read Depth for Sparse Decoding over Offloaded KV Caches** (arXiv 2609.17652, HN 49893944, 09-29). Open lead closed with numbers; extends the quant law toward read-time adaptivity; caveat named (no win with GPU-resident index). Quote: "At one million tokens on Qwen3-8B a decode step is 1.67x faster in GPU time than with the 136-bit scans of Double Sparsity, Loki and SparQ r=32".
3. **An Internet for the KV Cache** (arXiv 2608.01526, HN 49883064, 09-28). Open lead closed; vision paper, zero measurements (stated); frames cross-session/cross-cloud KV reuse as a content-distribution system - the infra-level version of the prefix-reuse question. Quote: "We propose a vision for an Internet for the KV Cache, with KV Cache management working as a content-distribution system."
4. **Red Hat: Benchmarking AI decision models against traditional guardrails** (developers.redhat.com, HN 49933476, 10-02). Seen and deprioritized by the 10-02 evals sibling (their :80), never banked; my area banks it: quality-side counterweight to the fold's banked decision-model rows - 9 guardrails, 4 paradigms; Jev-style decision models did not win speed/accuracy/quality; small pretrained classifiers stay competitive (deberta 89.01% at 54ms vs Qwen3.6-35B 89.31% at 312ms vs Jev 86.35% at 348ms on prompt injection). Quote: "we did not find that decision models produced faster, cheaper, or higher-quality answers compared with LLM-as-a-judge."

### OWED / not done

- Magnitude README re-read found on-question content (cross-session prefix-cache sharing) against the prior "off-questions" verdict; left unbanked pending measured numbers from its benchmark charts (referenced, not shown on the README). One page fetch would close it if a later seat wants it.
- Token compression CLI (49911910): unbanked Q3 lead, not read this ask.
- 16+ pass-1 candidates not deep-read; the five-prior-sweep saturation of this area is the documented reason, not door failure.
- The KVarN ARXIV_REGISTER append debt belongs to its named owner (per 10-02 kv-hn OWED); untouched here.

---

## PASS B (this invocation, same day; independent re-run of the same ask)

source-fetched: 2026-10-03. Instruments this pass: the recipe's WebFetch on
hn.algolia.com `search_by_date`/`search` with `numericFilters=created_at_i>1788393600`
(epoch verified this sitting with `./.venv/Scripts/python.exe -c "import datetime; ..."`
-> 1788393600 for 2026-09-03T00:00:00Z); estate instruments read:
tools/prefix_cache_sim.py (full), tools/lru_null_arm.py:1-80,
watch/inbox/buildall/lru-null-arm.md (full),
memory/research_polished/kv_cache_compaction.md (full), mag/inference_budget.py (full),
lens/laws.md, lens/burns.md, lens/corpus.md, the 09-30 kv-cache steal card (full).

Door health this pass, honest: the web-reader tool rejected every Algolia query URL with
"MCP error -400: Please Enter the Correct URL Format" on three encodings, so WebFetch on
the identical URLs is the door of record (all listing queries answered JSON first try).
One WebFetch call (vLLM by-date) timed out at 60s and succeeded on retry.
venturebeat.com returned HTTP 429 on the Stanford/Nvidia Jev-like piece and its HN thread
(item 49890520) has zero comments, so that candidate is LEFT UNBANKED on title-slug
evidence alone. Four queries returned real empties (single instrument, not cross-checked):
"context caching", "cache hit LLM", "structured context", "prompt structure" (the last
two are the Q3 negative below).

Pass-1 census: over 60 distinct in-window story rows observed across 10 listing queries;
33+ distinct stories actively considered after dedup and triage. Held items surfaced and
excluded from banking: 49643543, 49735410, 49783040, 49758259, 49699918, 49691257 (all
banked 09-30/10-01), 49814007/49807383 (page already fetched verbatim by the estate,
kv_cache_compaction.md:15), KVarN 48399974 (anti-rebank, burns.md section 5).

### Pass B dedupe verdicts (byte-checked this sitting)

- 2609.30854 "The KV Cache Is the New Memory Wall": REGISTERED find of the 10-02 run
  (watch/inbox/frontier_olm_2026-10-02/register.jsonl row: title + arxiv.org/abs/2609.30854
  + quote "for llama-3-70b in bf16, the 140 gb ..."; 10-02 DIGEST confirmed-finds table;
  10-02 percolator_candidates.jsonl carries the corrected closed-form per-token KV bytes).
  The 09-28 arxiv lane had already deduped it. NOT re-banked even though its HN surface
  (49945575, jaehun.me review, 10-03) postdates those. Pass B's added value, byte-verified:
  the on-disk abstract state/arxiv/2026-09-28/2609.30854v1.txt (2,002 bytes) confirms the
  title, author Tejinder Singh, "the binding resource shifts from model weights to the
  Key-Value (KV) cache as sequence length grows", and the five-domain taxonomy
  "quantization, token eviction, KV paging, prefix caching, and heterogeneous tiering";
  the review post's body-level numbers (0.33 MB/token, conformal-bounded eviction,
  "Tiering is for reuse between steps, not for reads within a step") are review-attested
  only, absent from the 2KB abstract.
- j9s.io (49701675): banked 10-01 (10-02 kv-cache-hn sweep line: "j9s.io agentic
  inference (49701675, 09-14, banked 10-01)"; 10-01 sweep deep-read list). Pass B read it
  in full as corroboration; NOT re-banked.
- Yandex KV cache as an agent runtime (49578969/49598646): banked (10-02 kv-cache-hn
  sweep line: "yandex kv-as-agent-runtime dups (49598646/49578969, 09-05/07, banked)").
  Corroboration only.
- An Internet for the KV Cache (2608.01526): banked by pass A today (its item 3). Pass B's
  independent read of the same abs page corroborates the same quote. NOT re-banked.
- SCR / wai-org (49939893): ZERO hits in catalog.jsonl and all five olm run dirs. NEW.
- Forge / mohitranka (49909945): only prior touch is a 09-30 reddit-lane candidate line
  ("token compression/prompt cache reuse clis"); never fetched or banked. NEW.
- Revefi (49848678): fetched by the 10-01 inference-efficiency lane (its sweep file lists
  the URL in the fetch list) but NEVER banked: 0 hits in 10-01/10-02/10-03 DIGEST,
  register.jsonl, and percolator_candidates.jsonl (greps run this sitting). NEW bank,
  prior-lane disposition disclosed.
- completeskeptic (49838474): the 10-02 X lane read only the tweet TLDR via fxtwitter
  (its sweep file: "resolved both article attempts ... as http 200 json carrying tweet
  text, article title, tldr"); never banked in any register/DIGEST. Pass B read the FULL
  blog post. NEW bank, disposition disclosed.

### Pass B banked items (strongest first; every one read whole by this seat this sitting)

1. **Suffix Cache Reuse Explained** (wai-org.com, HN 49939893; blog 2026-09-28, HN post
   2026-10-02). Rulin Shao and Oscar Yin (CLM team). Mechanism: after a mid-context edit,
   keep the cached KV of the unchanged suffix, diff the prompts, shift surviving spans'
   rotary positions (exact, position-only), splice them in, re-prefill only the edited
   middle; at most six spans per edit, longest first; linear-attention layers resume from
   a pre-edit recurrent-state snapshot. Quotes from the fetched page: "Accuracy is
   identical, 60.2% both ways, while compute drops from 10.98 to 7.14 PFLOPs per
   question."; "SCR serves an extra 28.2% of the prompt from relocated cache that
   standard serving would have recomputed."; on an agentic trace "standard SGLang serves
   72.9% of all prompt tokens from its prefix cache, but only 24.2% on the turns right
   after a" mid-context edit, and SCR brings serving cost to 65% of that; and "most of
   SCR's extra reuse comes from stripped reasoning rather than CLM edits."
   WHY: the estate's measured stack is prefix-only (lru-null-arm.md arms frozen_append
   0.93876 / frozen_window 0.376234 / volatile 0.001283; kv_cache_compaction.md:9 "any
   mutation re-pays the miss"). SCR is the missing arm for the two mutations the estate
   actually commits: repack mid-relation and the daily rib-chain-tip advance (body
   persists, tip moves = an edit with a surviving suffix). The 72.9-to-24.2 post-edit
   collapse is the external quantification of doug.sh's "compaction invalidates the whole
   prefix" pain (context_economics_1m.md:46 via the 09-30 card).
   OVERLAP: catalog.jsonl "suffix cache"/"wai-org" = 0 rows; zero hits in all five olm
   run dirs incl. today's register/DIGEST. Genuinely new. Quote risk: WebFetch
   small-model transcription of the fetched page.
2. **How Forge Structures Requests for Prompt Cache Reuse** (mohitranka.com, HN 49909945;
   blog 2026-09-24, Mohit Ranka). Quotes from the fetched page: "Forge builds a canonical
   request; provider adapters serialize it and add their cache markers or routing
   hints."; "Tool names and Skills are sorted to prevent incidental map or filesystem
   order from changing the prompt."; "In order to keep the prefix stable, Forge keeps the
   static content at the beginning and dynamic content at the end of the request.";
   measured: "Appending messages or changing only the last message resulted in improved
   cache-hit ratios, as reflected by 99.60% and 99.48% mean cache-hit ratios"; journal
   replay on session resumption; "Forge hashes the workspace path into prompt_cache_key".
   WHY: the field's existence proof for RQ4 (one tool across the seven bypass surfaces,
   lens/laws.md:83): a single canonical-request builder feeding thin provider adapters is
   a shipped architecture at 99.6% hit, the same centralization move
   mag/inference_budget.py:9-11 already made for the budget guard. Spec details the
   estate's canonicalizer should absorb: pin serializer order, model identity (model
   switches destroy caches, completeskeptic item 4 below), and the provider cache key;
   acceptance metric should be provider-reported cached-input share, not internal hashes
   alone (the 09-30 card's Find 6: a hit is not proof of skipped work).
   OVERLAP: catalog "mohitranka"/"forge structures" = 0; candidate-line only in the 09-30
   reddit lane; never fetched or banked. Related-but-distinct holding: OpenAI
   prompt_cache_key docs in mine/raw/agent_platform/openai/openai-agents-python (the
   provider key Forge hashes into).
3. **How Revefi Reduced Its Data Agent's Spend by 90%** (revefi.com, HN 49848678; blog
   2026-09-23, Mishra and Kalipatnapu). The bug: fresh timestamp + user context near the
   TOP of the system prompt invalidated prefix caching, re-billing history full price
   every call. Fix: "changes to our prompt generation layer where the least volatile
   content comes first, and the most volatile last", timestamp into a trailing system
   reminder. Quotes from the fetched page: "Cache reads climbed to 99% of input
   tokens."; "Not every agent needs the 1 hour TTL at 2x write cost. The 5-minute option
   at 1.25x is often enough."; "Generally, cached input tokens cost ~0.1x the price of
   regular input tokens (0.025x on Claude Fable 5.1)."; "We identified ~$300K in annual
   savings on a single internal agent for one of our customers."
   WHY: RQ2's per-tier dollar rule in practitioner form. On paid tiers the budget is TTL
   x price ratio, not chars: the 4,800-char rule survives only as the SIZE of the
   byte-identical unit; whether a warm prefix survives a boot gap is the provider
   retention window; what a reset costs is the hit/miss ratio (theirs ~0.1x/0.025x; the
   estate's flash 50x / pro 30x, kv_cache_compaction.md:9). The TTL-tier table is exactly
   the tier_probe cache-economics cell the estate owes (kv_cache_compaction.md:23/30).
   Their silent-burn finding ("agents lower down the pecking order had cache read ratios
   near zero, burning money as silently as we had been") is the bypass-surface risk in
   practitioner form.
   OVERLAP: catalog "revefi" = 0; never banked in any register/DIGEST/percolator (greps
   this sitting); 10-01 inference-efficiency fetched the URL without banking. The
   adjacent OpenAI GPT-6 numbers are already held (kv_cache_compaction.md:15) - this post
   adds the TTL tier table and the $300K case.
4. **(KV) Cache Rules Everything Around Me** (completeskeptic.com, HN 49838474; blog
   2026-09-09, Diogo). Quotes from the fetched page: "At Claude Code's reported 89% hit
   rate, the same workload costs $1.97M instead of $1.07M: 84% more!!" and "If you build
   agents, measure your cache hit rate and the number of tool calls." Central argument:
   agents re-read full context every turn so cache reads dominate the bill (output 9-18%
   of cost in the author's simulation); cache reads cost providers almost nothing (KV
   held during a tool call uses no compute or HBM bandwidth), which is where subscription
   margin comes from; routing and subagents often backfire because switching models
   destroys the cache.
   WHY: the sensitivity curve that bounds the estate's headline (6.5% to 98% cache hit,
   ~$161 to ~$3.60, lens/laws.md:23) from independent ground: small hit-rate deltas move
   the bill double-digit percent, which prices the seven-surface bypass (laws.md:83) as a
   money bug, and names the two counters the estate's provider_usage telemetry already
   captures (cache_hit_tokens/cache_miss_tokens, per the 09-30 card's schema scan).
   OVERLAP: catalog "completeskeptic"/"cache rules everything" = 0; never banked; 10-02
   X lane read the TLDR only (fxtwitter JSON), not the post.

### Pass B research-question verdicts (same five questions, pass-B evidence only; held items cited as held)

1. **Prefix-reuse gains vs the measured 98% ~$3.60 (lens/laws.md:23).** The field now
   reports hits ABOVE the estate's headline with discipline: Forge 99.60%/99.48% mean
   cache-hit (new, item 2), Revefi 99% of input tokens (new, item 3), and the held
   j9s.io "~100% prefix reuse across the sweep" on vLLM-local agentic traces. The
   binding result is sensitivity, not the ceiling: 89% vs target nearly doubles the bill
   (new item 4), which is the same curve shape as the estate's 6.5-to-98 swing. The
   estate's own 93.88% local null (lru-null-arm.md:72) sits below the field's
   provider-adjacent numbers; per the null arm's own arms result, the headroom is
   assembly and ordering, not eviction. Nothing found beats the estate number on the
   estate's own tapes; the G1 null stands.
2. **Does the 4,800-char budget transfer to paid tiers?** prefix_cache_sim predicts NO
   per-tier dollar rule: it is char-denominated end to end
   (tools/prefix_cache_sim.py:274-297, replay() returns hit_rate/evictions only) and its
   one budget is mag/context_pack.py:67 max_chars 4800. What transfers is the shape rule:
   hit rate is capacity-in-blocks vs working set (knee 64 blocks = 16,384 chars = ~3.4
   packs; one-pack cache 0.5045; plateau 0.9388 with zero evictions, lru-null-arm.md
   curve), so keep the byte-identical unit small enough that the session working set
   fits under the knee. What does NOT transfer: on paid tiers the reset rate is the
   provider TTL (Revefi: 5-minute at 1.25x write vs 1-hour at 2x; the estate-side
   retention window is still unmeasured, kv_cache_compaction.md RQ6) and the reset cost
   is the hit/miss ratio; j9s.io's 43,270-token reload-vs-wait crossover is the serving
   side of the same trade. The char-to-dollar per-tier mapping remains an owed estate
   measurement; no paper in either pass supplies it.
3. **Context shapes and tokens-per-correct-verdict.** NO post-10-02 paper found measuring
   structured-context-vs-prose verdict economics directly: "structured context" and
   "prompt structure" Algolia queries returned 0 in-window hits, and none of the nine
   pages this pass read scores verdicts per context shape. Nearest neighbors: the held
   Yandex multi-view KV framing (structure at the runtime layer), SCR's "most of SCR's
   extra reuse comes from stripped reasoning rather than CLM edits" (reasoning-channel
   structure dominates reuse gains, new item 1), Revefi's volatility ordering (new item
   3). The estate's memlang/frozen-RIB/claritas question remains externally unmeasured;
   its own frozen_append-vs-volatile arms remain the only measured structure comparison
   on its own traffic.
4. **One tool across the seven fire surfaces.** Mechanically yes, and it ships in the
   field: Forge's canonical-request builder with sorted keys, journal replay, and
   provider cache key at 99.6% (new item 2); the estate already proved the centralization
   move with the budget guard import (mag/inference_budget.py:9-11). The spec detail this
   pass adds: pin serializer order, model identity (switching models destroys the cache,
   new item 4), and the provider cache key; acceptance on provider-reported cached-input
   share, not byte hashes alone (held Find 6). A sweep cannot build it; the pattern and
   acceptance bar are now cited.
5. **Eviction policy for the repeated-boot pattern.** The estate's measured answer stands
   and both passes corroborate it: zero evictions at 1,024 blocks and up (the working set
   fits, lru-null-arm.md:79-82), so eviction policy is not the lever, assembly is
   (0.93876 vs 0.001283); the held anchors (49643543 thread this sitting: "Everything in
   this realm is about recency bias. I think it is a feature in this context, not a
   problem"; G1 bar kv_cache_compaction.md:13) cover the steady state. The refinements
   for the two regimes where eviction could matter: (a) when capacity binds, reorder LRU
   by predicted per-tool-type gap (willneed/pageout/dontneed, held j9s.io); (b) when the
   tip advances, suffix relocation beats recompute (new item 1); (c) the quality-bounded
   learned eviction idea (held 2609.30854) is the next G1-legal candidate shape.

### Pass B unbanked / not done

- Stanford/Nvidia open Jev-like model caching reusable agent actions (HN 49890520):
  venturebeat.com HTTP 429, HN thread zero comments; unbanked, not fabricated.
- Prompt Trees (49637425): considered, never deep-read by this pass (pass A also listed
  it unbanked); training-time lane.
- 49813610 (trained KV cache bank Jev demo): tailnet demo URL, not read, unbanked.
- The four zero-hit queries are single-instrument empties, not cross-checked.
- Pass A's OWED list above (Magnitude benchmark charts, token-compression CLI, KVarN
  register append) remains owed; this pass did not pick those up.
