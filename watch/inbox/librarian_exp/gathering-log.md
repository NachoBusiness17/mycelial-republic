# GATHERING LOG - gala librarian-expedition / expedition lane - 2026-10-01

The owed waltz executed. Priority order: (1) founding texts of the estate's own laws, (2) top-cited papers whose bytes evaporated, (3) fetched-today scratch sources. Every acquisition: magic-bytes checked, ledger row written, receipt written, catalog row written through the sanctioned writer (`mag.catalog scan`), FTS index healed fresh, estate holdings audit re-run CLEAN absorbing all rows.

**The "foundational-gaps table":** no file by that name exists anywhere in the estate (repo-wide grep; only hit was this lane's own echo in the trajectory tape). The referent used: `docs/ref/BIBLIOGRAPHY_MAP.md` section "THE UNNAMED DEBT" (founding citations of the two load-bearing laws) plus the holdings-doctrine lane's named founding texts (Turing 1936, Shannon 1948, EDVAC 1945, Watson 1928 - all four already hold bytes in `corpus/library/`, receipts `docs/report_v1/sources/receipts/`, verified this session).

## P1: founding texts of the estate's laws

| primary | source URL | bytes | corpus path | catalog id | magic | register |
|---|---|---:|---|---|---|---|
| Dynamo (SOSP 2007), append-only-record law | https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf | 900,468 | corpus/papers_reference_nonredistributable/law_dynamo-2007-sosp.pdf | f6c36903f936 | %PDF- | GATHERING_LANDING.json + receipt law_dynamo-2007-sosp.md |
| The Part-Time Parliament (Lamport 1998), governance law | https://lamport.azurewebsites.net/pubs/lamport-paxos.pdf | 568,998 | corpus/papers_reference_nonredistributable/law_lamport-1998-part-time-parliament.pdf | 44d56a7362ab | %PDF- | GATHERING_LANDING.json + receipt law_lamport-1998-part-time-parliament.md |
| Dolstra 2006 Nix thesis, behavior-follows-bytes law | https://nixos.org/~eelco/pubs/phd-thesis.pdf | 1,694,654 | corpus/papers_reference_nonredistributable/law_dolstra-2006-nix-thesis.pdf | a6354e57fe2a | %PDF- | GATHERING_LANDING.json + receipt law_dolstra-2006-nix-thesis.md |

## P2: top-cited research papers whose bytes evaporated

Feed: sibling division-B lane cited-missing (`unique_citations.json`: 91 unique citations in last-48h receipts, 80 not held durably, 66 distinct arXiv ids). Fetched the 37 ids cited 2+ times plus 2509.05276 (13 cites, top of the list). All 38: HTTP 200 from arxiv.org/pdf, serial with 3 s pauses, magic `%PDF-`, titles resolved via export.arxiv.org batch API (arxiv_titles.xml in memory/runs/gathering_expedition/).

| arxiv id | title (export API) | bytes | corpus path | catalog id | register |
|---|---|---:|---|---|---|
| 2310.03003 | From Words to Watts: Benchmarking the Energy Costs of Larg | 1,229,976 | corpus/papers_reference_nonredistributable/paper_2310.03003.pdf | e120eac6b96b | PAPERS_LANDING.json + receipt |
| 2310.06694 | Sheared LLaMA: Accelerating Language Model Pre-training vi | 1,270,497 | corpus/papers_reference_nonredistributable/paper_2310.06694.pdf | 1eb76cf9f141 | PAPERS_LANDING.json + receipt |
| 2311.16863 | Power Hungry Processing: Watts Driving the Cost of AI Depl | 936,671 | corpus/papers_reference_nonredistributable/paper_2311.16863.pdf | 0b5271e20b4d | PAPERS_LANDING.json + receipt |
| 2312.00752 | Mamba: Linear-Time Sequence Modeling with Selective State  | 1,168,615 | corpus/papers_reference_nonredistributable/paper_2312.00752.pdf | b7f1d82c5792 | PAPERS_LANDING.json + receipt |
| 2312.09084 | Language Modeling on a SpiNNaker 2 Neuromorphic Chip | 342,275 | corpus/papers_reference_nonredistributable/paper_2312.09084.pdf | 79304cabc75a | PAPERS_LANDING.json + receipt |
| 2402.00070 | EvoMerge: Neuroevolution for Large Language Models | 157,223 | corpus/papers_reference_nonredistributable/paper_2402.00070.pdf | 9563ff4ea7be | PAPERS_LANDING.json + receipt |
| 2402.19427 | Griffin: Mixing Gated Linear Recurrences with Local Attent | 951,680 | corpus/papers_reference_nonredistributable/paper_2402.19427.pdf | 24ca9963f332 | PAPERS_LANDING.json + receipt |
| 2403.13187 | Evolutionary Optimization of Model Merging Recipes | 2,048,456 | corpus/papers_reference_nonredistributable/paper_2403.13187.pdf | 89ee13cd786d | PAPERS_LANDING.json + receipt |
| 2403.17887 | The Unreasonable Ineffectiveness of the Deeper Layers | 2,268,238 | corpus/papers_reference_nonredistributable/paper_2403.17887.pdf | 5ac6ea79a94e | PAPERS_LANDING.json + receipt |
| 2403.20306 | Towards Greener LLMs: Bringing Energy-Efficiency to the Fo | 363,052 | corpus/papers_reference_nonredistributable/paper_2403.20306.pdf | f3df9c136eec | PAPERS_LANDING.json + receipt |
| 2407.12345 | VisionTrap: Vision-Augmented Trajectory Prediction Guided  | 31,107,874 | corpus/papers_reference_nonredistributable/paper_2407.12345.pdf | bac6be09c082 | PAPERS_LANDING.json + receipt |
| 2408.11796 | LLM Pruning and Distillation in Practice: The Minitron App | 1,712,898 | corpus/papers_reference_nonredistributable/paper_2408.11796.pdf | df2b99e1d96c | PAPERS_LANDING.json + receipt |
| 2408.15237 | The Mamba in the Llama: Distilling and Accelerating Hybrid | 2,658,177 | corpus/papers_reference_nonredistributable/paper_2408.15237.pdf | fc4c967874cd | PAPERS_LANDING.json + receipt |
| 2410.10254 | LoLCATs: On Low-Rank Linearizing of Large Language Models | 5,495,805 | corpus/papers_reference_nonredistributable/paper_2410.10254.pdf | de7582c90d59 | PAPERS_LANDING.json + receipt |
| 2502.14458 | Llamba: Scaling Distilled Recurrent Models for Efficient L | 875,844 | corpus/papers_reference_nonredistributable/paper_2502.14458.pdf | 7fc15e1173ad | PAPERS_LANDING.json + receipt |
| 2503.01155 | Nature-Inspired Population-Based Evolution of Large Langua | 1,550,354 | corpus/papers_reference_nonredistributable/paper_2503.01155.pdf | 3f43a205c8ed | PAPERS_LANDING.json + receipt |
| 2503.18002 | Neuromorphic Principles for Efficient Large Language Model | 1,801,000 | corpus/papers_reference_nonredistributable/paper_2503.18002.pdf | 1438f3095977 | PAPERS_LANDING.json + receipt |
| 2507.10059 | GeLaCo: An Evolutionary Approach to Layer Compression | 1,544,320 | corpus/papers_reference_nonredistributable/paper_2507.10059.pdf | 89f796cdefdc | PAPERS_LANDING.json + receipt |
| 2508.14444 | NVIDIA Nemotron Nano 2: An Accurate and Efficient Hybrid M | 1,828,212 | corpus/papers_reference_nonredistributable/paper_2508.14444.pdf | d4da333d06d2 | PAPERS_LANDING.json + receipt |
| 2508.16204 | Competition and Attraction Improve Model Fusion | 7,562,845 | corpus/papers_reference_nonredistributable/paper_2508.16204.pdf | 1a5c24bf1a21 | PAPERS_LANDING.json + receipt |
| 2509.05276 | SpikingBrain: Spiking Brain-inspired Large Models | 3,976,973 | corpus/papers_reference_nonredistributable/paper_2509.05276.pdf | 44461cc45f7a | PAPERS_LANDING.json + receipt |
| 2512.03024 | TokenPowerBench: Benchmarking the Power Consumption of LLM | 461,490 | corpus/papers_reference_nonredistributable/paper_2512.03024.pdf | 39bcd24177d3 | PAPERS_LANDING.json + receipt |
| 2601.22076 | Where Do the Joules Go? Diagnosing Inference Energy Consum | 669,899 | corpus/papers_reference_nonredistributable/paper_2601.22076.pdf | 11cbeecebd78 | PAPERS_LANDING.json + receipt |
| 2603.15569 | Mamba-3: Improved Sequence Modeling using State Space Prin | 1,090,013 | corpus/papers_reference_nonredistributable/paper_2603.15569.pdf | c29e09adc733 | PAPERS_LANDING.json + receipt |
| 2605.14386 | Darwin Family: MRI-Trust-Weighted Evolutionary Merging for | 743,322 | corpus/papers_reference_nonredistributable/paper_2605.14386.pdf | 08271f23a2ed | PAPERS_LANDING.json + receipt |
| 2605.16727 | PopuLoRA: Co-Evolving LLM Populations for Reasoning Self-P | 1,918,594 | corpus/papers_reference_nonredistributable/paper_2605.16727.pdf | 8ad18279eee9 | PAPERS_LANDING.json + receipt |
| 2606.03458 | KVarN: Variance-Normalized KV-Cache Quantization Mitigates | 874,189 | corpus/papers_reference_nonredistributable/paper_2606.03458.pdf | 42a2dd1727b3 | PAPERS_LANDING.json + receipt |
| 2608.10644 | Curate Before You Connect: Identity and Ontology Tagging i | 355,844 | corpus/papers_reference_nonredistributable/paper_2608.10644.pdf | db67d1e3bc69 | PAPERS_LANDING.json + receipt |
| 2608.30439 | Event-Driven Language Models with Sparse Neural Activity f | 575,379 | corpus/papers_reference_nonredistributable/paper_2608.30439.pdf | b90eb8091f6a | PAPERS_LANDING.json + receipt |
| 2609.07901 | Quantization Amplifies Determinism, Not Bias: Scale-Depend | 414,567 | corpus/papers_reference_nonredistributable/paper_2609.07901.pdf | 446f471589f3 | PAPERS_LANDING.json + receipt |
| 2609.16338 | Breaking the 1.58-bit Barrier for Ternary LLMs | 551,640 | corpus/papers_reference_nonredistributable/paper_2609.16338.pdf | b470da397f34 | PAPERS_LANDING.json + receipt |
| 2609.18526 | The Illusion of Local Privacy: Confidentiality Boundary Fa | 768,220 | corpus/papers_reference_nonredistributable/paper_2609.18526.pdf | d313d1f20bc4 | PAPERS_LANDING.json + receipt |
| 2609.23125 | Perplexity Cost Understates What Activation Quantisation B | 619,216 | corpus/papers_reference_nonredistributable/paper_2609.23125.pdf | c603f326817c | PAPERS_LANDING.json + receipt |
| 2609.29144 | Scope Before You Persist: Preventing Cross-Family Interfer | 245,390 | corpus/papers_reference_nonredistributable/paper_2609.29144.pdf | 1007d58a61df | PAPERS_LANDING.json + receipt |
| 2609.31678 | When Keywords Drop but Classifiers Hold: Soft Refusals und | 614,174 | corpus/papers_reference_nonredistributable/paper_2609.31678.pdf | ca7dfbe84b18 | PAPERS_LANDING.json + receipt |
| 2609.32049 | EngramRAG: Dynamic Usage-Weighted Topology and Synaptic Co | 767,807 | corpus/papers_reference_nonredistributable/paper_2609.32049.pdf | a6c2d46821a2 | PAPERS_LANDING.json + receipt |
| 2609.34160 | RoutePrism: Tracing Construction Order Effects in Agent Me | 1,754,462 | corpus/papers_reference_nonredistributable/paper_2609.34160.pdf | 8c7903bd3c5c | PAPERS_LANDING.json + receipt |
| 2609.36805 | UpliftMem: Learning Set-Level Uplift for Agent Memory Retr | 2,576,146 | corpus/papers_reference_nonredistributable/paper_2609.36805.pdf | d85f70b1191c | PAPERS_LANDING.json + receipt |

## P3: fetched-today sources loose in scratch, landed into corpus

Classification of the repo-root scratch (git status adds): 17 real-data files (arctic-shift `as_*` and pullpush Reddit archive pulls with `data` rows, plus `selftext_full.txt`), 3 real web sources riding mangled temp-path filenames, and 13 NOT-SOURCES (8 pullpush rate-limit error bodies, 4 arctic-shift timeout bodies, `as_kg_mem.json`/`pp_aimemory_all.json` empty-data, `kvarn_redlib.html` Anubis challenge page, `sweep_llama_m.json` 0 bytes). Only real sources landed; error bodies named, never landed as if sources.

| source | bytes | corpus path | catalog id | magic/content | register |
|---|---:|---|---|---|---|
| as_aiagents_graph.json | 20,842 | corpus/social_archive/reddit_20261001/as_aiagents_graph.json | 1eda31eb696f | { | GATHERING_LANDING.json + receipt |
| as_aimemory_all.json | 97,787 | corpus/social_archive/reddit_20261001/as_aimemory_all.json | b02be552e685 | { | GATHERING_LANDING.json + receipt |
| as_claudecode_mem.json | 157,922 | corpus/social_archive/reddit_20261001/as_claudecode_mem.json | 672cab56c30a | { | GATHERING_LANDING.json + receipt |
| as_llama_graph.json | 20,207 | corpus/social_archive/reddit_20261001/as_llama_graph.json | a8561672851f | { | GATHERING_LANDING.json + receipt |
| as_llama_mem.json | 130,074 | corpus/social_archive/reddit_20261001/as_llama_mem.json | 6b9214e62386 | { | GATHERING_LANDING.json + receipt |
| as_llmdevs_mem.json | 141,974 | corpus/social_archive/reddit_20261001/as_llmdevs_mem.json | 28831f8bee93 | { | GATHERING_LANDING.json + receipt |
| as_ollama_mem.json | 101,547 | corpus/social_archive/reddit_20261001/as_ollama_mem.json | 49a971140633 | { | GATHERING_LANDING.json + receipt |
| as_rag_graph.json | 39,484 | corpus/social_archive/reddit_20261001/as_rag_graph.json | 22cbdbd7207c | { | GATHERING_LANDING.json + receipt |
| as_rag_mem.json | 53,305 | corpus/social_archive/reddit_20261001/as_rag_mem.json | d48729e2c7a9 | { | GATHERING_LANDING.json + receipt |
| as_test.json | 17,936 | corpus/social_archive/reddit_20261001/as_test.json | edbd990afd63 | { | GATHERING_LANDING.json + receipt |
| pullpush_sub.json | 26,859 | corpus/social_archive/reddit_20261001/pullpush_sub.json | 18c1f49acf7a | { | GATHERING_LANDING.json + receipt |
| pullpush_comments.json | 69,568 | corpus/social_archive/reddit_20261001/pullpush_comments.json | a138cce1735b | { | GATHERING_LANDING.json + receipt |
| pullpush_test.json | 3,923 | corpus/social_archive/reddit_20261001/pullpush_test.json | 19b2cb413029 | { | GATHERING_LANDING.json + receipt |
| pp_ids.json | 191,879 | corpus/social_archive/reddit_20261001/pp_ids.json | 4b373c38e0ea | { | GATHERING_LANDING.json + receipt |
| kvarn_pullpush.json | 5,377 | corpus/social_archive/reddit_20261001/kvarn_pullpush.json | bf674d2fa45a | { | GATHERING_LANDING.json + receipt |
| kvarn_comments.json | 23,784 | corpus/social_archive/reddit_20261001/kvarn_comments.json | 977d820c092b | { | GATHERING_LANDING.json + receipt |
| selftext_full.txt | 9,066 | corpus/social_archive/reddit_20261001/selftext_full.txt | ebdd504bf224 | I | GATHERING_LANDING.json + receipt |
| UsersfosteAppDataLocalTempbudget.html | 38,336 | corpus/library/web_sources_20261001/UsersfosteAppDataLocalTempbudget.html | 58642dba3477 | <!DOC | GATHERING_LANDING.json + receipt |
| UsersfosteAppDataLocalTempdeepswe.html | 402,564 | corpus/library/web_sources_20261001/UsersfosteAppDataLocalTempdeepswe.html | cc4321201bb7 | <!DOC | GATHERING_LANDING.json + receipt |
| UsersfosteAppDataLocalTempjevals_readme.md | 26,663 | corpus/library/web_sources_20261001/UsersfosteAppDataLocalTempjevals_readme.md | c7572e1cd06b | # jev | GATHERING_LANDING.json + receipt |

## Failures named (permanently missing or blocked - never faked)

- **GDPR Art 17 (EUR-Lex primary): ROBOT-BLOCKED.** eur-lex.europa.eu returned HTTP 202 with 0 bytes on 2 attempts (TXT/HTML and TXT forms); not faked
- **Merkle 1987 (A Digital Signature Based on a Conventional Encryption Function): PAYWALLED/GONE.** merkle.com/papers/signCon.pdf 404; Springer CRYPTO87 paywall; not fetched
- **Simmons-Nelson-Simonsohn 2011 (False-Positive Psychology): GONE-AT-TRIED-URLS.** people.fas.harvard.edu 404, wayback availability empty; journal paywall
- **Dietterich 2000 (Ensemble Methods in ML): GONE-AT-TRIED-URLS.** web.engr.oregonstate.edu 404, archive.org 404, wayback availability empty; Elsevier paywall
- **Hurlbert 1984 (pseudoreplication): NOT-FETCHED-JOURNAL-PAYWALLED.** Ecology/ESAJ paywalled; classical-print class named in LIBRARIAN_RETIRED_20260927 (pulled if ever cited live)
- **scratch error bodies (pp_* rate-limit x8, as_* timeout x4, pp_aimemory_all empty, as_kg_mem 0 rows): NOT SOURCES - named, not landed.** bodies are API error JSON; kvarn_redlib.html is an Anubis browser-verification challenge page; sweep_llama_m.json is 0 bytes

## Register events (byte-checked)

- `mag.catalog scan --roots corpus/papers_reference_nonredistributable,corpus/social_archive,corpus/library/web_sources_20261001 --max 200` -> `{"scanned": 100}`, catalog.jsonl 821,776 lines; 38 `paper_*` + 3 `law_*` + 17 `social_archive/` + 3 `web_sources_20261001/` rows verified present.
- B2-465 FTS heal: `tools/corpus_fts_rebuild.py --check --deep` reported STALE (catalog moved), rebuilt through the sanctioned writer (821,776 rows, 0 malformed), recheck `index_state: fresh`.
- `mag.holdings_audit` re-run after landing: ledger->disk 262 ok / 0 missing / 0 mismatch (842,965,168 B), disk->ledger 263 files / 0 unreceipted / 0 dup groups, content 0 unreadable, **verdict CLEAN** (was 201 claims / 752,370,614 B before this expedition; delta = exactly the 61 rows landed here).
- Full-chain verifier: 61/61 PASS (file exists + sha256 matches ledger + catalog row present + receipt present). Raw output: `watch/inbox/gala_20260925/librarian-expedition/lanes/expedition.check.txt`.

Ledgers: `memory/runs/gathering_expedition/GATHERING_LANDING.json` (23 rows + 6 named failures), `memory/runs/gathering_expedition/PAPERS_LANDING.json` (38 rows). Total new durable bytes: 90,594,721 B across 61 primaries.