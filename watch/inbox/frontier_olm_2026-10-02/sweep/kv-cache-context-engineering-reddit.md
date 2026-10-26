# Sweep: kv-cache-context-engineering via reddit (2026-10-02)

Seat: sweep-kv-cache-context-engineering-reddit (frontier_olm_2026-10-02). House laws held:
ascii only, no em or en dashes, every claim cites the page fetched or the file read this
sitting, anything not verified is marked OWED. Overlap checked against
`catalog/catalog.jsonl` (byte scan, 8 rows for 2606.03458) and `memory/` (recursive byte
scan) with `./.venv/Scripts/python.exe` this sitting.

## Door record (all doors tried this sitting, in order)

1. `old.reddit.com/r/LocalLLaMA/top.json?t=month&limit=50` -> Reddit welcome shell, zero
   posts (WebFetch, this sitting). Matches the mapped degradation at
   `watch/inbox/frontier_olm_2026-10-02/lens/burns.md:108-112`.
2. `old.reddit.com` thread HTML for 1w8rnyi -> welcome shell again (WebFetch).
3. `arctic-shift.photon-reddit.com/api/posts/subreddit?...` -> HTTP 404 (my guessed
   endpoint; correct endpoint never determined this sitting).
4. `api.pullpush.io/reddit/search/submission/?subreddit=LocalLLaMA...` -> HTTP 429.
5. WORKING DEEP-READ DOOR: `safereddit.com` redlib mirror. Served 5 full threads end to
   end this sitting. (The 10-01 fold hit a Cloudflare challenge on safereddit;
   `frontier_olm_2026-10-01/DIGEST.md:114`. It served me clean today. Door status is
   per-day, not permanent.)
6. WORKING DISCOVERY DOOR: WebSearch `site:reddit.com` (7 queries; one query returned
   transient MCP 1302 rate-limit noise inside the search backend and answered on a
   dropped-terms retry).

So: primary subreddit JSON doors all degraded this sitting; discovery ran on WebSearch
site:reddit.com fallback and deep reads on the safereddit redlib mirror. No fallback
success is fabricated: arctic-shift 404 and PullPush 429 are recorded as failures.

## Pass 1: candidates considered (30+ from discovery searches; date shown only where a
fetched page or search snippet stated it)

1w8rnyi (cache-pressure validate advertised KV, 2026-09-06), 1twnj5r (KVarN r/ML,
2026-06-04), 1wuty3r (Pi BetterCompaction, 2026-10-01), 1t3vlrx (FastDM 6.4x), 1v5k08a
(CachyLLama persistent KV, 2026-07-24), 1vqqqcs (sparse-attn eval critique, 2026-08-17),
1rrp5l8 (sustaining long sessions), 1olouiw (KV swap to RAM), 1s1iiw6 (KVCache memory),
1s6eozp (KV architecture evolution), 1l75fc8 + 1ldmlj4 (KVzip), 1mhlj69 (quantized KV
verdict), 1v5wviz (DKV DifferentialKV), 1q9syiz (KV bandwidth in production), 1s7v30u
(TurboQuant), 1ig0z7h (KV compression via LCM), 1p4pold, 1qxb34b, 1v4f6cw, 1lypm28
(ClaudeAI compaction quartet), 1w5fz5m (ChatGPT conversation-length limit), 1rxv8i1
(openclaw full-window confusion), 1w7gu6f (Halogen Flash server), 186phti (macOS VRAM),
arXiv 2606.03458 (KVarN paper), github.com/ggml-org/llama.cpp discussions/20572
(per-session KV restore), upguard.com llama-cpp-prompt-leak, gmicloud KV blog, AMD KV
reuse article, modular handbook KV offloading, spheron context-engineering blog. That is
33 considered; the 9 strongest were fetched and read. Dates unknown = the fetched page or
snippet did not show one; not asserted.

## Pass 2: deep reads actually executed this sitting (8 pages + 1 abstract)

1. arxiv.org/abs/2606.03458 (live fetch, abstract page).
2. r/MachineLearning 1twnj5r (safereddit, post + 13 comments).
3. r/PiCodingAgent 1wuty3r (safereddit, post + comments).
4. r/LocalLLaMA 1w8rnyi (safereddit, post + comments).
5. r/LocalLLaMA 1t3vlrx (safereddit, post + comments).
6. r/LocalLLaMA 1v5k08a (safereddit, post + comments).
7. r/LocalLLaMA 1rrp5l8 (safereddit, post + comments).
8. r/MachineLearning 1vqqqcs (safereddit, post + 4 comments).
9. github.com/ggml-org/llama.cpp/discussions/20572 (live fetch, full discussion).
Plus upguard.com/blog/llama-cpp-prompt-leak (live fetch, full article).

## RQ1: KVarN (arXiv 2606.03458) - CONFIRMED from two live primaries; llama.cpp clause stays UNSOURCED

- The paper exists. Live abstract page fetched this sitting: "KVarN: Variance-Normalized
  KV-Cache Quantization Mitigates Error Accumulation in Reasoning Tasks", Muller, Bich,
  Boretti, Chang, Zhuang, Cavigelli, submitted Tue, 2 Jun 2026 10:34:56 UTC. Method:
  Hadamard rotation plus dual-scaling variance normalization across both axes of K and V;
  error accumulation across decode timesteps driven by incorrect token scales; SOTA on
  MATH500 / AIME24 / HumanEval at 2-bit.
- Second primary, the live r/MachineLearning thread 1twnj5r fetched this sitting via
  safereddit (2026-06-04, u/intentionallyBlue, 28 points, 13 comments), confirms the
  same: Hadamard + variance normalization + round-to-nearest, links to
  arxiv.org/abs/2606.03458 and github.com/huawei-csl/KVarN, vLLM implementation.
- The llama.cpp kv-rotation clause: REFUTED AS ATTRIBUTION, AGAIN, from a second
  independent surface. The abstract names ONLY a vLLM implementation. In the live thread,
  the only llama.cpp mentions are a commenter's unrelated personal project (Sea-Speaker1700
  porting to RDNA4 with their own "RFA 4.5bpw" method packing against "the NL code book
  used in llama.cpp") and "avoiding resorting to llama.cpp". This independently reproduces
  the 10-01 ruling that the clause is UNSOURCED-OWED
  (`frontier_olm_2026-10-01/DIGEST.md:114-115`). Search-level claim of a "llama.cpp PR
  merged 2026-04-01 applying normalized Hadamard rotation" (Particula Tech blog, via
  search snippet only, never fetched; note it predates KVarN's June 2026 submission) stays
  OWED as the only possible surviving source of that clause.
- Estate state moved since the 10-01 fold: the paper PDF is now bytes-held
  (catalog rows 821415 / 821729 / 829875, 874,189 bytes, sha256
  c437782e9352790102fde8561aaf2f74c930fed1b6cf44414c7d42ab57571739, landed 2026-10-01,
  receipt `docs/report_v1/sources/receipts/paper_2606.03458.md:1-13`), and the queued
  ARXIV_REGISTER append (DIGEST:119) was NOT executed by this seat (no write authority
  claimed for that register this sitting; it remains queued for the corpus_gap_research
  owner).

## RQ2: KV eviction/compression with degradation curves over long agentic sessions - essentially nobody publishes them

- FastDM (1t3vlrx), the strongest new compression candidate found: all evaluation is
  perplexity, KLD, token-match and throughput on synthetic short prompts (WikiText-2,
  ctx 1024-8192). The author's own caveat: "none of this matters if the compression tanks
  output quality", with quality checked only by KLD/PPL, and a commenter asking for
  "32k context with retrieval-style needle-in-haystack". Direct confirmation the surface
  the estate's specced KV degradation ladder targets is unoccupied. Bonus defect for
  multi-turn reuse: "shared prefix blocks need per-sequence eviction overlays or must be
  disabled".
- 1rrp5l8 (sustaining long sessions): qualitative only - "You use KV cache quantization on
  coding tasks and everything starts to break almost immediately", codegen and physics
  worst. No curves, no thresholds, despite the OP asking for exactly that.
- 1w8rnyi (cache-pressure tool, 2026-09-06, in-window) is the closest real instrument:
  calibrated probe, hydrate N contexts, validate hits in reverse order until first miss,
  reporting the oldest surviving context and cumulative retained tokens. Advertised vs
  measured: 2,023,924 advertised vs 1.05M retained (misconfig) up to 2,047,043 advertised
  vs 3,000,048 retained (146.56 percent). Commenters flag the confound the estate should
  steal: "The 149.69% retention tells you the probe is catching CPU offload, not just GPU
  KV cache" (feng_sg) - any reach/eviction instrument must disable or detect offload
  before reading an eviction boundary. This feeds the reach-ratio meter steal card
  directly.
- Nothing hour-scale or tool-loop-scale surfaced anywhere in the sweep. The KV degradation
  ladder (burns.md:98) has no external competitor to compare against; its novelty claim
  survives this sweep.

## RQ3: isolation/sandboxing responses for the cross-tenant state-restore flaw class - none found; only operational compartmentalization

Two targeted searches (llama.cpp plaintext prompts allocator memory; multi-user KV leak
between users) found NO reddit thread discussing sandboxing or isolation for the banked
flaw class (arXiv 2609.18526, cross-tenant state-restore 200/200, plaintext prompts in
allocator memory, banked 10-01 row 21). What exists instead is adjacent and weaker:

- UpGuard (2025-07-25, fetched): a DIFFERENT sub-class - unauthenticated /slots endpoint
  serves "the actual text of the prompts"; about one-third of exposed llama.cpp servers
  exposed prompt data. Mitigations are config-level only (disable /slots, do not expose).
  No process-per-tenant, no scrubbing, no allocator discussion. Useful as evidence the
  flaw class is real and unhandled in the wild, not as an isolation response.
- llama.cpp discussion 20572 (2026-03-15, fetched): the state-restore path itself, as a
  tutorial. `--slot-save-path` + `/slots/<id>/save|restore`, session-ID-keyed slot files
  "~hundreds of MB for long contexts", `--swa-full` required for SWA models "otherwise the
  restored cache may cover tokens the model can't attend to". Security content: zero.
  Multi-user guidance is one line: "-np 1 means one concurrent user. For multi-user
  setups, use -np N and map session IDs to slot indices." No auth, no cleanup, no tenant
  boundary. This is the estate's isolation-hardening target in its own authors' words.
- CachyLLama (1v5k08a, fetched): persistent SSD-backed KV checkpoints plus per-agent
  slots via --parallel to stop cross-agent cache thrashing ("whoever's request lands last
  evicts the state the other agent needed"). Compartmentalization for PERFORMANCE, not
  security - and it EXTENDS the at-rest attack surface: plaintext session state written
  to disk, "GBs of data for every session". Repo since deleted entirely, per the thread.
- Verdict for the steal queue: the isolation hardening line in the 10-01 register row 21
  has no public prior art in this sweep. The estate's own design (per-tenant slot
  namespacing + prompt-lifetime guarantee + encrypted or zeroed restore files) would be
  novel work, not a re-derivation.

## RQ4: compaction preserving law-critical context at 96.6 pct removal; worst-event reach elsewhere

- BetterCompaction (1wuty3r, 2026-10-01, in-window): the cache-law answer - "appends the
  compaction instruction to the already-cached conversation"; "The existing prefix stays
  byte-identical, so the backend can reuse its KV/prompt cache and only prefill the small
  new suffix." 13-15 min -> 6.5 min, 2 min with thinking off, one request "94.4k tokens
  served from cache". Counter-evidence worth stealing: commenters demand summary-quality
  evals ("I feel like I am going blue in the face asking folk for some proof of so many
  bold claims") and flag the buffer-room assumption. Note this thread is about compaction
  COST, not compaction FIDELITY: its default-implementation complaint is "the normal
  approach can throw away the prompt cache", while information loss is only a commenter
  worry. Adjacent policies in-thread: async continuous compaction (pi-observational-
  memory), chunk + small-model summarization (pi-refine-compact, arXiv 2308.15022),
  externalize durable knowledge to an llm-wiki and start fresh sessions.
- Nobody in this sweep measures preservation at anything like the estate's 96.6 pct
  removal scale (61-day instrumentation, r/LLMDevs 1wu24sc, banked 10-01 row 13 - not
  re-banked). Closest to "worst-event reach" as a discipline: 1vqqqcs (2026-08-17), the
  eval-critique thread: report aggregates to hide failure cases - "your method degrades on
  the NIAH-MK3, which actually stress-tests lossless compression"; AIME statistics
  ("AIME has 30 samples. You did 4 seeds"); the aggregate-metrics trick "everyone does it
  and reviewers just let it slide". So the estate's worst-event-reach framing has no
  external standard to conform to; if anything the field's practice is the opposite
  (aggregate and hide). The reach-ratio meter remains uncopied territory.

## Bank list (strongest first, all fetched and read this sitting)

1. KVarN live abstract (arXiv 2606.03458) - Q1 confirmation primary.
2. KVarN r/MachineLearning 1twnj5r live thread - Q1 second primary; llama.cpp clause
   absent (again, independently).
3. BetterCompaction 1wuty3r - Q4 cache-preserving compaction, in-window.
4. cache-pressure 1w8rnyi - Q2 eviction-boundary instrument + offload confound.
5. llama.cpp discussion 20572 - Q3 the state-restore path, security-zero.
6. CachyLLama 1v5k08a - Q3/Q2 persistent KV + per-agent slots, repo now deleted.
7. FastDM 1t3vlrx - Q2 negative result (PPL-only evaluation).
8. Eval-critique 1vqqqcs - Q4 worst-event culture absent in the field.

Not banked (older or thinner, listed only): 1rrp5l8 (qualitative, no numbers beyond one
60k-token figure), UpGuard (2025, different sub-class, kept as RQ3 evidence), the rest of
the pass-1 list.

## OWED carried forward

- ARXIV_REGISTER.json append for 2606.03458 still not executed (owner: corpus_gap_research
  seat; DIGEST:119).
- Particula Tech llama.cpp Hadamard-rotation PR claim: unfetched blog, predates KVarN;
  fetch it or drop the clause forever.
- No in-window thread publishes hour-scale agentic KV degradation curves; the ladder probe
  has no external baseline to calibrate against - if the operator wants one, building the
  estate's own is the only path this sweep found.
