# SWEEP: open-and-local-models via X (frontier_olm 2026-10-06)

source-fetched: 2026-10-06
seat: sweep-open-and-local-models-x (workflow subagent)
instrument: WebSearch (site:x.com queries, partially honored by the engine), WebFetch on
api.fxtwitter.com, export.arxiv.org/api/query, hn.algolia.com/api/v1/search_by_date,
huggingface.co model cards, blog.cloudflare.com, typesafe.ai; curl with a browser UA against
the r/LocalLLaMA Atom RSS; local grep over catalog/catalog.jsonl, memory/, state/arxiv/, and
the sibling sweeps in this directory; one PowerShell CIM read for the host GPU. Every web
claim below was fetched this sitting; overlap claims cite the exact grep or file read.

## Door scoreboard this sitting

| Door | Verdict | Evidence |
|---|---|---|
| X search (site:x.com) | DEGRADED | repeated MCP 1302 rate-limit errors mid-sweep (4 observed); site: operator only partially honored; results arrived as engine summaries, sometimes without permalinks |
| fxtwitter (api.fxtwitter.com) | ANSWERED x2 | OmNawale45831/status/2104490537889996980 returned full JSON (code 200, created Mon Sep 28 08:36:58 +0000 2026, 7 likes / 496 views); StepFun_ai/status/2101510462685003786 was already resolved by the estate Oct 2 (memory/trajectory/steps.jsonl:45486) |
| arXiv export API + submittedDate window (doors.md:28-29 OWED) | EXECUTED, ANSWERED | query all:"open weights" AND submittedDate:[202609060000 TO 202610070000], sortBy=submittedDate desc: 325 results, 15 listed; standouts 2610.06782 (T-Search), 2610.06625 (JEV vs LLMs), 2610.05367 (AIProver) |
| HN Algolia search_by_date + numericFilters (doors.md:42-44 OWED) | EXECUTED, ANSWERED | query "open weights", tags=story, created_at_i>1788652800: 17 hits; standouts: Cloudflare Clef on HF (Oct 5), Mistral Large 4 Le Chonk 1T (Oct 6), StepFun Step 5 Preview open weights Oct 15 (Sep 22) |
| r/LocalLLaMA Atom RSS + browser UA (burns.md:73-74, 100-102 recipe) | ANSWERED | curl -A "Mozilla/5.0 ..." on https://www.reddit.com/r/LocalLLaMA/new/.rss?limit=25 returned 66,583 bytes of Atom XML (file: sweep/_localllama_rss.xml, 11:47 local); first attempt exited 23 on a %TEMP% write path, second attempt to the repo path succeeded - the door works, the first failure was the sink |

## Two passes, honestly labeled

Pass 1 (broad, 40 candidates, 2026-09-06 to 2026-10-06): 7 routing/cascade X posts from the
first search (6 of them snowflake-dated Jul-Aug 2026, out of window; OmNawale45831 Sep 28 in
window), Kolibri coverage cluster (already banked day-5), Qwen3.8-27B "It's Opus 4.6" engine
summary (no permalink surfaced), latent.space Jev AINews Sep 16, 9 arXiv entries from the
executed recipe, 17 HN hits, 8+ r/LocalLLaMA RSS entries, plus awesome-jev and nishbhana.com
from the Jev search. Pass 2 (deep, 6 read end to end): HF Cloudflare/clef card, the Cloudflare
Clef blog, typesafe.ai, HF google/embeddinggemma-2 card, arXiv 2610.06625 abstract (read twice:
fetched through the API door and re-read verbatim from the estate's own ingest
state/arxiv/2026-10-06/2610.06625v1.txt), arXiv 2610.05367 abstract via id_list, plus the
fxtwitter JSON body of the Om Nawale post.

## Overlap verdicts (do not re-bank these)

- The decision-model wave core is HEAVILY banked: corpus/library/jev_steal_library/ (catalog
  rows 27772-27774), the kev prototype "Kev - prototype of a Jev-style decision model" +
  kev/jev.py (catalog rows 27777, 27981), Kev-4B rows (catalog 27798-27799), six decision-model
  abstracts ingested state/arxiv/ (2609.23886 this-that-model-1.0, 2609.24574, 2609.30243
  JevOut, 2609.37832, 2610.01601, 2610.02076 LLM2Jev), and the day-5 sweep-level headline
  (frontier_olm_2026-10-06/lens/burns.md:92-95: five sweep rows, none confirmation-passed).
- Kolibri (78.1B total / 3.46B active) is day-5 banked (burns.md:82-83); the download-gated
  pull stays OWED lane work; this sitting adds nothing measured on it.
- StepFun Step 5 Preview is estate-resolved via fxtwitter Oct 2
  (memory/trajectory/steps.jsonl:45486) and banked as "open weights Oct 15"
  (frontier_olm_2026-10-03/lens/burns.md, r18); skipped as an item here.
- The sibling lane's open-and-local-models-arxiv.md already executed the same two OWED recipes
  (independent corroboration: both ANSWERED twice this sitting by different seats) and already
  names 2610.06625 once; its deep-read list does not include 2610.06782 or 2610.05367.
- The daily arXiv ingest already cataloged 2610.06625 and 2610.06782 (9 catalog line hits for
  the two ids; state/arxiv/2026-10-06/2610.06625v1.txt + 2610.06782v1.txt read in full). The
  deep-read verdicts below are what the abstract rows do not carry. 2610.05367 is NOT ingested
  (grep over state/arxiv/2026-10-05 and -10-06 matched only the two above) and has zero
  catalog hits for AIProver/Leanstral.

## Answers to the five research questions

- RQ1 (decision model vs gemma:2b per dollar, L15 instruments): the battery fill was NOT run
  this sitting and cannot be from a sweep seat: law 1 of RIB_MODEL_GARDEN_ROUTING.md:47-53
  fills cells only from estate instruments, and the fill procedure (same rib:202-209) is lane
  work. The headline stays a LEAD (burns.md:95). What the sweep adds: the wave's cost claim now
  has an independent counter-row - arXiv 2610.06625 finds "no cost advantage over GPT-6 Luna at
  OpenAI's batch prices" and calibration "not consistently better than Qwen3.8-27B's" - against
  typesafe.ai's own "193.6x Faster, 444.6x Cheaper." vendor page. That is the L15 disease
  (vendor numbers) meeting its cure (instruments) in the wild; it strengthens the case that
  only the estate's own gemma:2b-vs-decision-model instrument rows can fill the cell.
- RQ2 (UNMEASURED local-lane battery cells, laws.md:88): not fillable by this seat; reported as
  not run. Candidate rungs captured for whoever fills the cells: Clef-flash (Qwen3.5-9B base,
  rank-256 LoRA + routing head, median 38.8 ms on Cloudflare iron) and Clef (Qwen3.8-27B base,
  54.7 GB BF16, "Tested ... on a single H200" per the HF card) - a 9B Q4-ish local rung is
  plausible on the 6 GB RX 5600 XT ONLY IF llama.cpp ever supports the joint schema head; that
  support is UNVERIFIED, do not assert it.
- RQ3 (open weights after 2026-09-06 vs the five gates): NONE pass on this host, on my own
  instrument: PowerShell CIM read this sitting returns "AMD Radeon RX 5600 XT", driver
  32.0.21045.5002, AdapterRAM 4.29 GB (the 32-bit cap; the sibling arXiv sweep's CIM read adds
  63.95 GB system RAM, Ryzen 7 3800XT, nominal 6 GB card). Gate 1 (SM90/SM100) fails on RDNA1
  and gate 2 (24 GB minimum) fails at 6 GB, so every candidate release fails the five gates
  regardless of quality (RIB_GPU_LADDER_20261001.md gates list). Releases captured for the
  ladder's price-trigger surveillance instead: Mistral Large 4 "Le Chonk" LeChonk-1T-A49B
  (weights "by the end of the month" per the RSS entry), StepFun Step 5 Preview 600B/27B-active
  (weights Oct 15, banked), Leanstral-1.5 119B (2610.05367), T-Search on Qwen3.6-35B-A3B
  (2610.06782), EmbeddingGemma 2 740M (sub-1B; fits THIS box on the CPU/quant lane, which never
  enters the GPU ladder at all).
- RQ4 (Kolibri fit/serve): NOT MEASURED this sitting. The pull remains download-gated lane work;
  the only new third-party detail surfaced is the search-snippet cluster repeating that
  Qwen3-27B beat Kolibri on German (79.9 vs 70.8) inside Kolibri's own benchmark harness - a
  vendor-harness number, planning input only under RIB_MODEL_GARDEN_ROUTING.md:50-53, never a
  verdict cell.
- RQ5 (HAD harness-vs-model replication, burns.md:84): NOT REPLICATED this sitting (requires
  swapping harness halves on the estate harness; lane work). Sweep evidence in HAD's favor:
  2610.05367 (AIProver) moves pass@4 semantic correctness 15.7 pct to 36.7 pct on a FIXED
  119B base purely via "HarnessEvolve, a certificate-driven evolutionary search over the whole
  harness control flow" - independent support that harness control flow moves capability; and
  Clef's whole design ("no free-form text generation and no output parsing", HF card) is a
  harness-shaped readout choice, not a scale choice.

## Items banked (7, strongest first; full rows in the submitted result)

1. JEV versus LLMs (2610.06625) - the independent audit that deflates the wave's cost claim.
2. Cloudflare Clef + Clef-flash open decision models - the wave's second mover, weights on HF,
   Apache-2.0, full architecture recipe in the blog.
3. TypeSafe Jev vendor page - the primary source of "193.6x Faster, 444.6x Cheaper." that
   item 1 contradicts at batch prices.
4. EmbeddingGemma 2 - 740M multimodal embedder, Apache-2.0, fits this host; v1 already serves
   estate memory search (memory/thinking/app_reasoning.jsonl:3811).
5. T-Search (2610.06782) - open-weight retriever/generator split, +14.4 Recall@10 over base.
6. Mistral Large 4 "Le Chonk" LeChonk-1T-A49B - ladder surveillance; X relay unresolved,
   banked from the RSS/HN snippets as declared.
7. AIProver / Leanstral-1.5 (2610.05367) - 119B open-weight + the HarnessEvolve result that
   feeds RQ5.

## X-door honesty notes

- The fxtwitter door itself never failed this sitting; the degradation is upstream in the
  search backend (1302 storms) and in site:x.com indexing. Per the recipe, unresolved threads
  are banked as search-result snippets with URLs and are labeled as such: the Cloudflare Clef
  X post ("our open-source decision models, and new RL fine-tuning", ~4 days old, surfaced in a
  translated engine summary without a permalink) and the @qtnx_ Mistral Large 4 post ("still
  doing RL runs ... Release at the end of the month", relayed through the
  r/LocalLLaMA/comments/1wz2y2v RSS entry). Neither was resolved to a fxtwitter JSON body;
  neither is quoted as if it were.
- The one NEW X permalink resolved end to end this sitting (OmNawale45831 routing/cascades,
  Sep 28) is a generic explainer; the estate's routing doctrine is already deeper
  (RIB_MODEL_GARDEN_ROUTING.md, avichawla banked day-5), so it is NOT banked as an item.
