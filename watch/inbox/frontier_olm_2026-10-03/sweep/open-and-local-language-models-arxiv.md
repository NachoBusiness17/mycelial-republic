# SWEEP: open-and-local-language-models via arxiv (2026-10-03, second seat)

source-fetched: 2026-10-03
seat: sweep gopher, area open-and-local-language-models via arxiv (frontier_olm_2026-10-03)
provenance note: this file REPLACES an 11:05 same-day version of the same lane written by an
earlier seat of this run (the run died on the quota wall before its result was consumed).
That version's items were treated as LEADS only: nothing in this file is banked on the prior
seat's say-so. Every quote below was byte-verified this sitting against a page fetched this
sitting (arXiv abs-page og:description meta, or the raw HF model card markdown), unless the
item text says otherwise.

## Doors run, with incidents (nothing papered over)

- WebFetch on export.arxiv.org 429'd three times this sitting (two parallel calls first, then
  one spaced retry; bodies were "Rate exceeded." / "HTTP 429"). Fallback used: the SAME arXiv
  API door via `curl -A "mag-frontier-sweep/1.0"` with 4-8 s spacing between calls. That door
  then returned 200 for every query except two transient errors noted below. The mcp
  web_reader tool was also tried on the API URL and rejected the format outright
  ("Please Enter the Correct URL Format") - not used.
- One API call returned an HTML 503 body (query E, first attempt); a spaced retry returned 30
  entries. Query G/H (submittedDate:[202610020000 TO 202610040000] on cat:cs.CL and cat:cs.LG)
  returned 0 entries BOTH times: at fetch time the API's newest visible submissions are
  2026-10-01 (2610.02206v1 at 2026-10-01T17:59:55Z is the newest in query A). So the literal
  "after 2026-10-02" sub-window of Q1 read EMPTY at this door this sitting; read as
  announcement lag, and stated as measured, not assumed.
- Hugging Face: WebFetch on the MiniCPM5-2B card timed out at 60 s. Fallback: curl of the raw
  card markdown (huggingface.co/OpenBMB/MiniCPM5-2B/raw/main/README.md, 112,204 bytes, 200)
  plus the HF API JSON (followed the API's 307 to the lowercase org name openbmb).

## Pass 1 instruments (exact queries, all via curl on export.arxiv.org)

Six productive queries, sortBy=submittedDate descending, max_results 30-40 each, 200 entries
fetched total:

1. abs:"open weights" OR abs:"open-weight" -> 40 entries (newest 2026-10-01T17:59Z)
2. ti:"small language model" OR abs:"on-device" -> 40 entries
3. ti:"tool calling" OR ti:"function calling" -> 30 entries (back to 2026-08-25)
4. cat:cs.CL AND abs:quantization AND (abs:"coding" OR abs:"code generation") -> 30 entries
5. ti:Qwen OR ti:Gemma OR ti:SmolLM OR ti:Nemotron OR ti:Ministral -> 30 entries
6. abs:"llama.cpp" OR abs:GGUF OR abs:"local LLM" OR abs:"consumer GPU" OR abs:"edge device"
   AND abs:"language model" -> 30 entries
7+8. cat:cs.CL and cat:cs.LG AND submittedDate:[202610020000 TO 202610040000] -> 0 + 0.

In-window candidates considered (2026-09-03 .. 2026-10-03; well over the 30 floor): Mingbird
2610.02001, KaliBench 2610.02206, MoE-CORE 2610.01950, Cross-Benchmark RL Coding 2610.00890,
cua-speedrun 2609.40284, Staying on Task 2609.38712, ActionGuard 2609.39450, Market-Aware
Routing 2609.37902, Measuring the Serving Stack 2609.26693, SFT-or-RL 2609.17848, Tetra
2609.35465, Gemma-4 behavioral eval 2609.30716, Quantization Thresholds 2609.32042, MILO
2609.38349, radiology open-weight FT 2609.40236, Galahad 2609.39358, PCIe consumer-GPU expert
parallel 2609.40093, Denial-of-Wallet 2609.28585, EDGEGEN 2609.24115, SilentCall 2609.32021,
NemotronLabs VoiceChat 2609.21967, Ask-the-Tool serving 2609.18849, workflow-boundary
anomalies 2609.15397, carbon-aware routing 2609.13559, vehicle-agent schemas 2609.09476,
sub-2B MCP CPU bench 2609.07370, KOPA 2609.05395, Scale-QLoRA 2609.04526, evidence-preserving
PTQ 2609.24799, PastForward 2609.32166, LUMO 2609.30692, PTC-Decoder 2609.30836, AIR-LLM
2610.00465, EdgeVLN 2609.35570, FunctionGemma 2609.25373, Keyword Harnesses 2610.02142,
OverAct 2610.01508, ContractRL 2610.00328, Learning-to-Ask 2610.01236, Qwen-Audio-3.1
2609.25176 (off-area), Qwen-CUA 2608.02352 (out of window).

## Pass 2 deep reads (8 items read this sitting, all verified)

WebFetch read + byte-verified: 2610.02001, 2609.37902, 2609.32042, 2609.26693, 2609.17848,
2609.35465, 2609.30716 (abs pages, og:description greps). curl-read end to end of the visible
page abstract: 2610.02206, 2610.01950, 2610.00890, 2609.40284, 2609.38712, 2609.39450, plus
the MiniCPM5-2B raw card + HF API JSON. Fourteen sources read; nothing banked unread; five
of the fourteen were read and then DROPPED as held (below) - the reads still happened, and
their verification work is what proves the held files' numbers.

### Instrument incident worth keeping: Atom flat-extraction misaligns id-title pairs

The flat `grep -o '<id>...|<title>...'` listing paired MoE-CORE with the WRONG id (showed
2610.01956, whose abs page is actually EndoLive, a surgical-video paper). The raw XML shows
the true id is 2610.01950. Cause: some `<id>` lines are https and the grep pattern only
matched http, shifting every later pair. Every id banked below was confirmed against its own
abs page `<title>`, not against the API listing. (Six of six post-incident fetches confirmed.)

## Overlap instrument (what was grepped, and the sanity check)

Ran (this sitting, forward-slash paths, grep not findstr): single-pass
`grep -n -i -e <33 names/ids> catalog/catalog.jsonl` (917,885 lines); targeted
`grep -rn <name> watch/inbox/frontier_olm_20260928/sweep/ watch/inbox/frontier_olm_2026-09-30/
sweep/ watch/inbox/frontier_olm_2026-10-01/sweep/ watch/inbox/frontier_olm_2026-10-02/sweep/`;
same patterns against memory/; `grep -io <names> register.jsonl DIGEST.md` of today's fold.
SANITY POSITIVE: "driving ladder" greps returned memory/rib/RIB_MODEL_GARDEN_ROUTING.md and
memory/runs/ds_batches/cow2_items.jsonl (the known-positive), so the instrument reads. (The
09-30 olm sweep's own file records the same findstr-under-bash void lesson; this seat
repeated the sanity check anyway.) One instrument caveat discovered and documented: a
combined grep over memory/ hits memory/trajectory/steps.jsonl for EVERY name this session
touches - that file is the live per-session trajectory journal (its rows carry this
session_id and current timestamps), so it is SELF-ECHO, not a holding; overlap claims against
memory/ must discount it.

Reading of the catalog hits: the estate's daily arxiv pull auto-archives abstract stubs under
state/arxiv/<date>/<id>v1.txt, so a catalog stub is NOT a holding - it is an unread abstract.
Stub-only ids this sitting (stub AND nothing else): 2609.17848 (2026-09-17), 2610.02206
(2026-10-02), 2610.02001, 2609.37902, 2609.26693, 2609.30716, 2609.35465 and others. Stub
PLUS held elsewhere: 2609.40284 (10-02 inference sweep), 2610.02001 (10-02 olm sweep item 1),
2609.32042 (09-28 sweeps), 2609.37902 (09-30/10-01), 2609.26693 (09-28), 2609.30716 (09-30),
2609.35465 (09-28/10-01). No stub at all: 2609.38712, 2609.39450, 2610.01950, 2610.00890.

### DROPPED as already-held (with receipts; re-banking would be waste)

- Mingbird 2610.02001 - banked as item 1 of the 10-02 olm sweep
  (watch/inbox/frontier_olm_2026-10-02/sweep/open-and-local-language-models-arxiv.md:114-116),
  full-text read, models gemma4:e2b/12b + qwen3.5:4b + ornith-1.5:35b via Ollama Q4_K_M,
  Mingbird 0.886 vs goose 0.631. I re-verified its abs page this sitting (same 0.886/0.791/
  0.737 numbers byte-present); held is held.
- Quantization Thresholds Replicate 2609.32042 - item 5 of the 09-28 olm sweep
  (watch/inbox/frontier_olm_20260928/sweep/open-and-local-language-models-arxiv.md:94) AND
  item 1 of the 09-28 quantization sweep (:53), full-text reads both; raw full text cached at
  frontier_olm_20260928/sweep/_raw/full_2609.32042.txt.
- Market-Aware Routing / FACET 2609.37902 - item 2 of the 09-30 olm sweep
  (watch/inbox/frontier_olm_2026-09-30/sweep/open-and-local-language-models-arxiv.md:20, DEEP)
  and the 10-01 inference-efficiency sweep (:19).
- Measuring the Serving Stack 2609.26693 - held by the 09-28 inference-efficiency-arxiv sweep
  (:22, :42), which already drew the "replication on our hosts is the move" conclusion.
- Tetra 2609.35465 - full-HTML read by the 09-28 inference sweep (:163); the 10-01 olm sweep
  explicitly logs it "drop-as-rebank"
  (watch/inbox/frontier_olm_2026-10-01/sweep/open-local-language-models-arxiv.md:49).
- Gemma-4 behavioral eval 2609.30716 - item 6 of the 09-30 olm sweep (:24, DEEP abs).
- cua-speedrun 2609.40284 - substantively held by the 10-02 inference-efficiency sweep
  (watch/inbox/frontier_olm_2026-10-02/sweep/inference-efficiency-arxiv.md:118-121): its
  per-task cost/time accounting is folded into the estate's per-deliverable-meter discussion.
  I re-read its abs page this sitting; the "reproducibility crisis" quote and uniform-rig
  claim match. Dropped from items.
- Today's 11:05 superseded lane file held MiniCPM5-2B, Kolibri, KOPA promotion, 2610.01236,
  2610.01508, 2610.00328, Groq/Gemini rate-limit docs. Of those, ONLY MiniCPM5-2B is re-banked
  here, and only because this seat re-verified the card byte-for-byte AND the fold register +
  DIGEST carry neither it nor Kolibri (zero hits in register.jsonl and DIGEST.md this
  sitting) - without a re-bank it evaporates with the replaced file. The rest stay dropped:
  2610.01236/2610.01508/2610.00328 are in-window siblings of items the 10-01/10-02 sweeps
  already hold, and the two provider-doc pages were the 11:05 seat's own fetches (their
  quotes rest on that seat's fetch, not mine, so they are not re-asserted here).

## Items banked (7, strongest first; every quote verified on a page fetched this sitting)

1. SFT or RL for Tool-Calling Agents? A Controlled Study Across Data, Method, and Scale -
   arxiv.org/abs/2609.17848 (2026-09-15, REALM @ EMNLP 2026). Six Qwen3 models 0.6B-32B,
   SFT+LoRA vs GRPO vs SFT->GRPO. Quote: "SFT with LoRA is the strongest in-distribution
   method throughout the 0.6B-32B range and best in 15 out of 18 experimental settings."
   Also verified on-page: GRPO wins transfer "29 out of 54 settings ... but its margin over
   SFT averages under one point"; "LoRA outperforms full-parameter fine-tuning ...
   demonstrating that LoRA better preserves pretrained agentic behavior." Estate: the garden's
   finetune lanes should default LoRA-SFT for janitor tool-calling; RL is a transfer tool, not
   an in-distribution win. Overlap: catalog stub only (catalog/catalog.jsonl:444218,
   state/arxiv/2026-09-17/2609.17848v1.txt); zero hits in the four sibling olm sweep dirs and
   memory/. NEW.
2. KaliBench: Fine-Grained Benchmark for Cybersecurity Tool Use on Kali Linux with
   Runtime-Free Verifiable Rewards - arxiv.org/abs/2610.02206 (2026-10-01). 8,504
   query-command pairs, 1,642 Kali tools, 23 capability dimensions, deterministic
   canonicalization + alias-aware eval, sandboxed verification, rewards usable for RLVR.
   Quote: "no open-weight model exceeds 42% exact-command accuracy in the unrestricted
   setting"; also on-page: SFT+RLVR on an 8B reaches "performance comparable to a 685B MoE
   model." Estate: this is the Q1 measurement instrument in the wild - agentic CLI claims at
   small size are mostly assertion until verified, and verifiable rewards close an
   implausible-looking 8B-vs-685B gap. Overlap: catalog stub only
   (catalog/catalog.jsonl:870471); zero in sibling sweeps and memory/. NEW.
3. ActionGuard: Tool Call Authorization under Poisoned Skills - arxiv.org/abs/2609.39450
   (2026-09-30). Skill-poisoning defense, evaluated on 139 contextual + 180 obvious
   injections, ASR/TSR, 3 open-source + 2 commercial Reviewer models, 3 repetitions each.
   Quote: "ActionGuard intercepts each Tool Call at OpenClaw's before-tool-call stage and
   enforces the Reviewer's ALLOW or DENY decision under a fail-closed policy." The strangers
   are dogfooding OUR surface: authorization split from generation context, fail-closed
   default - the model-proposes/switchboard-authorizes law, measured. Overlap: no catalog
   stub, zero sibling-sweep and memory hits. NEW.
4. MiniCPM5-2B model card - huggingface.co/OpenBMB/MiniCPM5-2B (HF API: createdAt
   2026-09-06T11:12:19Z, lastModified 2026-09-29T06:12:33Z, safetensors total
   2,516,756,480; card license apache-2.0; tags include tool-calling, on-device, edge-ai).
   Quote (tag-stripped card text): "built for on-device, local deployment, and
   resource-constrained scenarios, reaching 2B-class open-source SOTA." Card table header
   claim verified on-page: "MiniCPM5-2B reaches 2B-class open-source SOTA with an average
   score of 53.9, and also exceeds all of the larger models included here (the highest is
   51.1)"; SGLang named the recommended tool-calling backend. Caveats banked: scores are
   self-reported on the card; no summarization/janitor-task bench on the card; Q1's answer is
   therefore "claims with a measuring table, third-party reproduction still OWED." Overlap:
   zero in catalog, memory/, fold register and DIGEST; present only in today's superseded
   11:05 lane file (item 1 there); substring noise in 09-28 _raw reddit JSON. NEW post-purge.
5. Staying on Task: Testing the Foundations of Long-Horizon Agent Reliability -
   arxiv.org/abs/2609.38712 (2026-09-30). Long-Transduction diagnostic, seven open-weight
   models, axes varied independently. Quote: "Together, these failures represent critical
   liabilities in long-horizon agentic workflows"; measured on-page: "a 62.8\% decrease when
   scaling context length from 4-128K, a 36.5\% decrease when varying input format, and a
   39.9\% decrease by increasing local task complexity" (backslash-percent as the page
   prints it). Estate: the janitors' long ledgers are exactly this diagnostic; context
   length alone cuts open-weight transduction by ~63 percent. Overlap: no catalog stub,
   zero sibling-sweep and memory hits. NEW.
6. Cross-Benchmark Transfer from RL on Agentic Coding Tasks - arxiv.org/abs/2610.00890
   (2026-10-01). Kimi K2.7 Code (1T total / 32B active MoE), RL alone, 1,700 tasks, reward =
   fraction of target checks, zeroed on any pass-to-pass failure. Quote: "One epoch of GSPO
   on a rank-32 LoRA adapter improves pass@1 on each of the six external benchmarks we
   evaluated"; verified numbers: SWE-Bench Pro 60.1 -> 64.8, Terminal-Bench 2.1 67.4 -> 82.0;
   transfers to both never-trained harnesses. Estate: Q2-adjacent measurement culture for
   agentic coding (hidden fail-to-pass + pass-to-pass grading is the shape the estate's
   local-27B replication should copy), at 1T scale, not local class. Overlap: no catalog
   stub, zero sibling-sweep and memory hits. NEW.
7. MoE-CORE: Coordinated Expert Offloading and Residency for Memory-Constrained MoE
   Inference - arxiv.org/abs/2610.01950 (2026-10-01). Quote: "MoE-CORE records a mean time
   per output token (TPOT) of 38.0-44.8 ms versus 1268.9-1269.1 ms for the evaluated vLLM
   Prefetch configuration on DeepSeek-V4-Flash-W4A8"; also on-page: under an 84-GB NPU-memory
   cap, best GSM8K config 21.5 ms TPOT. Estate: the memory-constrained-MoE-serving genre the
   garden will need if MoE janitors ever land on small VRAM; measured, but NPU-appliance
   class, not RX 5600 XT class - banked as genre intel, not a fit. Overlap: no catalog stub,
   zero sibling-sweep and memory hits. NEW.

## Research questions, answered with what this door can answer

1. Open-weight agentic releases after 2026-10-02 at RX 5600 XT-class VRAM: the arXiv API
   showed ZERO cs.CL and cs.LG submissions dated 2026-10-02..10-04 at fetch time (queries 7+8,
   0 entries each), so nothing new after the ask's cutoff was visible; newest in-window items
   are 2026-10-01. The in-window measured-claim release remains MiniCPM5-2B (item 4), whose
   card MEASURES a benchmark table but self-reports it; KaliBench (item 2) is the field's own
   evidence that open-weight CLI agentic claims sit under 42 percent exact-command accuracy
   without tool hints.
2. local-27B-on-real-code (1wv1u54) replication at Q4_K_M: NOT RUN by this seat - it is an
   estate-instrument job (GPU bench), not an arXiv-door job, and nothing in this sweep ran a
   model. What the door adds: the grading shape worth copying (2610.00890's hidden
   fail-to-pass + pass-to-pass, item 7) and the held 09-28 GGUF threshold result (Q8->Q2
   collapse between 3- and 2-bit, failure modes non-replicating) as the quantization prior.
3. Free-tier replacement / Featherless roster diff: nothing arXiv-side this sitting; the
   provider-economics instrument (FACET, 2609.37902) is already held (09-30 sweep item 2).
   The roster diff itself remains an estate instrument run, not attempted here.
4. Free-lane throttling contradiction: not arXiv-addressable; no new evidence this door.
5. Ollama 0.34.3-to-0.35 upgrade effects: the measured serving-stack instrument
   (2609.26693, Ollama template-flag gating of tools requests, Gemma-3 rejected
   pre-inference in its studied version) is HELD by the 09-28 sweep; the delta for 0.35
   specifically remains OWED an estate probe on our own hosts.

## OWED (carried, not asserted)

- MiniCPM5-2B third-party benchmark reproduction and a janitor-task (summarization/classification)
  bench; card scores are self-reported.
- The after-2026-10-02 release window: re-query the API in ~48 h; 0 entries today is
  announcement lag, not absence.
- Estate-side probes this door cannot run: Q2 Q4_K_M replication, Featherless roster diff,
  per-dispatch tank accounting, Ollama 0.35 serving delta.
- ActionGuard full-text read (this sitting read and verified the abs page only; the
  OpenClaw-stage interception claim deserves the paper's numbers pulled into the estate's
  policy-engine design notes).

## Honesty notes

- Quotes are byte-grepped substrings of fetched pages (og:description meta, blockquote, or
  raw card markdown), not paraphrases; markup entities decoded (&#39; -> ', -- kept as the
  page prints it); the 62.8\% backslash form is the page's own escaping.
- WebFetch's extract-and-answer was used for 7 abs pages; every load-bearing quote from those
  reads was then re-verified by curl + grep on the raw page this sitting. The one number I
  could not re-verify beyond WebFetch's read is Mingbird's LRAB cell values (0.886 vs 0.631/
  0.479/0.405) - but Mingbird is dropped as held anyway, and the held file's numbers match
  the abs page's tau2 numbers I did verify.
- No em-dashes were introduced by this seat; page-internal double hyphens are quoted as-is.
