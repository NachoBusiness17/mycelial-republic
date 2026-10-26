# CITED-BUT-MISSING sweep (librarian-expedition, division B)

Date: 2026-10-01. Lane: cited-missing. Ask: extract every primary-source citation from the
last-48h receipts and check whether the actual primary is held in the estate (catalog + corpus +
loose bytes) or only fetched-at-runtime with bytes never retained.

## Method

- Surfaces swept (all banked in the last 48h): watch/inbox/48h_synth (6 chapters),
  frontier_olm_2026-09-30/steal (6 cards), frontier_olm_2026-10-01/steal (5 cards + DIGEST + RECEIPT),
  spiking_wide (7 cards), localfirst (7 cards + LOCALFIRST_MEMORY_LANDSCAPE_20261001.md), drop
  receipts (SPIKINGBRAIN, STRATA, DOUBLE_DROP, x_intel_drop, model_mating_paper_dig, ABLITERATUS_DROP),
  ractor50 (8 chapters).
- Extraction: regex for arxiv.org URLs, bare arXiv ids (YYMM.NNNNN month-validated), and github.com
  owner/repo pairs, per receipt line. Scripts: watch/inbox/gala_20260925/librarian-expedition/
  extract_citations.py + holdings_check.py + render_receipt.py; raw data lanes/citations_raw.json
  (205 rows) and lanes/unique_citations.json.
- Holdings test: (a) id substring in any catalog/catalog.jsonl path or title (691,789 rows);
  (b) id substring in any FILENAME under corpus/, watch/, memory/, docs/, mag/, tools/, state/
  (state/arxiv/ holds 4,010 dated fetched-text files). Catalog-only hits whose sole path is a
  %TEMP%/tmpdir file are classed WEAK (bytes outside the durable estate), not held-durable.
- Fetchability: HTTP HEAD probes (curl -I -L): 3 arXiv ids + 13 github repos + the placeholder id,
  all returned HTTP 200 (raw probe log in lanes/cited-missing.check.txt).

## Counts

- Unique citations extracted: 90 (40 arXiv ids, 12 GitHub repos)
- Cite locations (file:line): 205
- HELD (durable estate): 49
- HELD (weak, temp-path only): 1
- NOT HELD (cited-but-missing): 40
- Priority split of the missing: P1-HIGH 15, P2-MED 1, P3-LOW 24, placeholder n/a 1

## Verdict

The estate's memory is leaking: 40 of 90 primaries (44 pct) cited by banked receipts are NOT held anywhere in
catalog/corpus/loose bytes AT THE MOMENT OF THIS SWEEP (2026-10-01 ~19:37Z). The pattern is
systematic, not random: receipts that fetched a primary kept only their own prose about it; the
only citations held are ones a holding pass (state/arxiv ingest, training_pdfs, olm0928 sweep _raw)
happened to catch.

MOVING ESTATE WARNING: the holdings numbers above are a snapshot of a live tree. Mid-sweep the
holdings grew twice: (a) the spiking-wide gala lane banked ev_arxiv_2509_05276_abstract.md
(1,461 bytes, mtime 18:33Z), and (b) a sibling gathering_expedition lane has been landing fetched
primaries into memory/runs/gathering_expedition/ DURING this check: at final render the dir holds
48 files (27 arXiv PDFs were already there by 19:36Z, more may have landed since), healing
a large slice of the gap in flight. The counts in the table are honest for the named moment; a
re-run of this lane's scripts after the healer finishes will read a smaller missing set.

## HELD (durable) - 49

| citation | kind | cited-where | holding evidence |
|---|---|---|---|
| 2310.03003 | arxiv-bare | watch/inbox/spiking_wide/energy-frontier.md:114; watch/inbox/spiking_wide/energy-frontier.md:153; watch/inbox/spiking_wide/energy-frontier.md:39 (+1 more) | memory/runs/gathering_expedition/p2_2310.03003.pdf; corpus/papers_reference_nonredistributable/paper_2310.03003.pdf; docs/report_v1/sources/receipts/paper_2310.03003.md |
| 2310.06694 | arxiv | watch/inbox/spiking_wide/upcycle-economics.md:115; watch/inbox/spiking_wide/upcycle-economics.md:26 | memory/runs/gathering_expedition/p2_2310.06694.pdf; corpus/papers_reference_nonredistributable/paper_2310.06694.pdf; docs/report_v1/sources/receipts/paper_2310.06694.md |
| 2311.16863 | arxiv-bare | watch/inbox/spiking_wide/energy-frontier.md:157; watch/inbox/spiking_wide/energy-frontier.md:47 | memory/runs/gathering_expedition/p2_2311.16863.pdf; corpus/papers_reference_nonredistributable/paper_2311.16863.pdf; docs/report_v1/sources/receipts/paper_2311.16863.md |
| 2312.00752 | arxiv-bare | watch/inbox/spiking_wide/energy-frontier.md:159; watch/inbox/spiking_wide/energy-frontier.md:46; watch/inbox/spiking_wide/linear-family.md:35 | memory/runs/gathering_expedition/p2_2312.00752.pdf; corpus/papers_reference_nonredistributable/paper_2312.00752.pdf; docs/report_v1/sources/receipts/paper_2312.00752.md |
| 2312.09084 | arxiv | watch/inbox/spiking_wide/neuromorphic-hardware.md:33; watch/inbox/spiking_wide/neuromorphic-hardware.md:46; watch/inbox/spiking_wide/neuromorphic-hardware.md:77 | memory/runs/gathering_expedition/p2_2312.09084.pdf; corpus/papers_reference_nonredistributable/paper_2312.09084.pdf; docs/report_v1/sources/receipts/paper_2312.09084.md |
| 2402.00070 | arxiv | watch/inbox/model_mating_paper_dig_20261001.md:128; watch/inbox/model_mating_paper_dig_20261001.md:129 | memory/runs/gathering_expedition/p2_2402.00070.pdf; corpus/papers_reference_nonredistributable/paper_2402.00070.pdf; docs/report_v1/sources/receipts/paper_2402.00070.md |
| 2402.19427 | arxiv-bare | watch/inbox/spiking_wide/linear-family.md:26; watch/inbox/spiking_wide/linear-family.md:42 | memory/runs/gathering_expedition/p2_2402.19427.pdf; corpus/papers_reference_nonredistributable/paper_2402.19427.pdf; docs/report_v1/sources/receipts/paper_2402.19427.md |
| 2403.13187 | arxiv | watch/inbox/model_mating_paper_dig_20261001.md:127; watch/inbox/model_mating_paper_dig_20261001.md:128 | memory/runs/gathering_expedition/p2_2403.13187.pdf; corpus/papers_reference_nonredistributable/paper_2403.13187.pdf; docs/report_v1/sources/receipts/paper_2403.13187.md |
| 2403.17887 | arxiv | watch/inbox/spiking_wide/upcycle-economics.md:110; watch/inbox/spiking_wide/upcycle-economics.md:22 | memory/runs/gathering_expedition/p2_2403.17887.pdf; corpus/papers_reference_nonredistributable/paper_2403.17887.pdf; docs/report_v1/sources/receipts/paper_2403.17887.md |
| 2403.20306 | arxiv-bare | watch/inbox/spiking_wide/energy-frontier.md:113; watch/inbox/spiking_wide/energy-frontier.md:156; watch/inbox/spiking_wide/energy-frontier.md:50 | memory/runs/gathering_expedition/p2_2403.20306.pdf; corpus/papers_reference_nonredistributable/paper_2403.20306.pdf; docs/report_v1/sources/receipts/paper_2403.20306.md |
| 2407.12345 | arxiv-bare | watch/inbox/ractor50/accuracy.md:31; watch/inbox/ractor50/accuracy.md:33 | memory/runs/gathering_expedition/p2_2407.12345.pdf; corpus/papers_reference_nonredistributable/paper_2407.12345.pdf; docs/report_v1/sources/receipts/paper_2407.12345.md |
| 2408.11796 | arxiv | watch/inbox/spiking_wide/upcycle-economics.md:109; watch/inbox/spiking_wide/upcycle-economics.md:23 | memory/runs/gathering_expedition/p2_2408.11796.pdf; corpus/papers_reference_nonredistributable/paper_2408.11796.pdf; docs/report_v1/sources/receipts/paper_2408.11796.md |
| 2408.15237 | arxiv | watch/inbox/spiking_wide/upcycle-economics.md:113; watch/inbox/spiking_wide/upcycle-economics.md:24 | memory/runs/gathering_expedition/p2_2408.15237.pdf; corpus/papers_reference_nonredistributable/paper_2408.15237.pdf; docs/report_v1/sources/receipts/paper_2408.15237.md |
| 2410.10254 | arxiv | watch/inbox/spiking_wide/upcycle-economics.md:112; watch/inbox/spiking_wide/upcycle-economics.md:122; watch/inbox/spiking_wide/upcycle-economics.md:21 | memory/runs/gathering_expedition/p2_2410.10254.pdf; corpus/papers_reference_nonredistributable/paper_2410.10254.pdf; docs/report_v1/sources/receipts/paper_2410.10254.md |
| 2502.14458 | arxiv | watch/inbox/spiking_wide/upcycle-economics.md:114; watch/inbox/spiking_wide/upcycle-economics.md:123; watch/inbox/spiking_wide/upcycle-economics.md:25 | memory/runs/gathering_expedition/p2_2502.14458.pdf; corpus/papers_reference_nonredistributable/paper_2502.14458.pdf; docs/report_v1/sources/receipts/paper_2502.14458.md |
| 2503.01155 | arxiv | watch/inbox/model_mating_paper_dig_20261001.md:122; watch/inbox/model_mating_paper_dig_20261001.md:123 | memory/runs/gathering_expedition/p2_2503.01155.pdf; corpus/papers_reference_nonredistributable/paper_2503.01155.pdf; docs/report_v1/sources/receipts/paper_2503.01155.md |
| 2503.18002 | arxiv | watch/inbox/spiking_wide/neuromorphic-hardware.md:32; watch/inbox/spiking_wide/neuromorphic-hardware.md:78 | memory/runs/gathering_expedition/p2_2503.18002.pdf; corpus/papers_reference_nonredistributable/paper_2503.18002.pdf; docs/report_v1/sources/receipts/paper_2503.18002.md |
| 2507.10059 | arxiv | watch/inbox/model_mating_paper_dig_20261001.md:130; watch/inbox/model_mating_paper_dig_20261001.md:131 | memory/runs/gathering_expedition/p2_2507.10059.pdf; corpus/papers_reference_nonredistributable/paper_2507.10059.pdf; docs/report_v1/sources/receipts/paper_2507.10059.md |
| 2508.14444 | arxiv | watch/inbox/spiking_wide/linear-family.md:16; watch/inbox/spiking_wide/linear-family.md:61 | memory/runs/gathering_expedition/p2_2508.14444.pdf; corpus/papers_reference_nonredistributable/paper_2508.14444.pdf; docs/report_v1/sources/receipts/paper_2508.14444.md |
| 2508.16204 | arxiv | watch/inbox/model_mating_paper_dig_20261001.md:103; watch/inbox/model_mating_paper_dig_20261001.md:108; watch/inbox/model_mating_paper_dig_20261001.md:113 (+7 more) | memory/runs/gathering_expedition/p2_2508.16204.pdf; corpus/papers_reference_nonredistributable/paper_2508.16204.pdf; docs/report_v1/sources/receipts/paper_2508.16204.md |
| 2509.05276 | arxiv | watch/inbox/SPIKINGBRAIN_DROP_20261001.md:4; watch/inbox/SPIKINGBRAIN_DROP_20261001.md:9; watch/inbox/spiking_wide/energy-frontier.md:152 (+10 more) | memory/runs/gathering_expedition/p2_2509.05276.pdf; watch/inbox/gala_20260925/spiking-wide/lanes/ev_arxiv_2509_05276_abstract.md; corpus/papers_reference_nonredistributable/paper_2509.05276.pdf |
| 2510.26692 | arxiv | watch/inbox/spiking_wide/linear-family.md:13; watch/inbox/spiking_wide/linear-family.md:60 | memory/corpus/training_pdfs/20260916/b10_kimi_linear_2510.26692.pdf; memory/corpus/training_pdfs/20260916/b10_kimi_linear_2510.26692.pdf |
| 2512.03024 | arxiv-bare | watch/inbox/spiking_wide/energy-frontier.md:107; watch/inbox/spiking_wide/energy-frontier.md:116; watch/inbox/spiking_wide/energy-frontier.md:155 (+4 more) | memory/runs/gathering_expedition/p2_2512.03024.pdf; corpus/papers_reference_nonredistributable/paper_2512.03024.pdf; docs/report_v1/sources/receipts/paper_2512.03024.md |
| 2601.22076 | arxiv-bare | watch/inbox/spiking_wide/energy-frontier.md:114; watch/inbox/spiking_wide/energy-frontier.md:126; watch/inbox/spiking_wide/energy-frontier.md:154 (+4 more) | memory/runs/gathering_expedition/p2_2601.22076.pdf; corpus/papers_reference_nonredistributable/paper_2601.22076.pdf; docs/report_v1/sources/receipts/paper_2601.22076.md |
| 2603.15569 | arxiv | watch/inbox/spiking_wide/linear-family.md:14; watch/inbox/spiking_wide/linear-family.md:60 | memory/runs/gathering_expedition/p2_2603.15569.pdf; corpus/papers_reference_nonredistributable/paper_2603.15569.pdf; docs/report_v1/sources/receipts/paper_2603.15569.md |
| 2605.14386 | arxiv | watch/inbox/model_mating_paper_dig_20261001.md:117; watch/inbox/model_mating_paper_dig_20261001.md:118 | memory/runs/gathering_expedition/p2_2605.14386.pdf; corpus/papers_reference_nonredistributable/paper_2605.14386.pdf; docs/report_v1/sources/receipts/paper_2605.14386.md |
| 2605.16727 | arxiv | watch/inbox/model_mating_paper_dig_20261001.md:129; watch/inbox/model_mating_paper_dig_20261001.md:130 | memory/runs/gathering_expedition/p2_2605.16727.pdf; corpus/papers_reference_nonredistributable/paper_2605.16727.pdf; docs/report_v1/sources/receipts/paper_2605.16727.md |
| 2606.03458 | arxiv | watch/inbox/frontier_olm_2026-10-01/DIGEST.md:113; watch/inbox/frontier_olm_2026-10-01/DIGEST.md:115; watch/inbox/frontier_olm_2026-10-01/DIGEST.md:119 | memory/runs/gathering_expedition/p2_2606.03458.pdf; corpus/papers_reference_nonredistributable/paper_2606.03458.pdf; docs/report_v1/sources/receipts/paper_2606.03458.md |
| 2608.10644 | arxiv | watch/inbox/frontier_olm_2026-09-30/steal/agent-memory-continuity.md:51; watch/inbox/frontier_olm_2026-09-30/steal/agent-memory-continuity.md:60; watch/inbox/frontier_olm_2026-09-30/steal/agent-memory-continuity.md:7 (+1 more) | memory/runs/gathering_expedition/p2_2608.10644.pdf; corpus/papers_reference_nonredistributable/paper_2608.10644.pdf; docs/report_v1/sources/receipts/paper_2608.10644.md |
| 2608.28444 | arxiv-bare | watch/inbox/spiking_wide/upcycle-economics.md:20 | memory/corpus/training_pdfs/20260916/b11_sliding_window_sinks_2608.28444.pdf; watch/inbox/wave_20260916/receipts/N4_GOAT_VS_SINKS.md; memory/corpus/training_pdfs/20260916/b11_sliding_window_sinks_2608.28444.pdf |
| 2608.30439 | arxiv-bare | watch/inbox/spiking_wide/event-driven-resonance.md:203; watch/inbox/spiking_wide/event-driven-resonance.md:204; watch/inbox/spiking_wide/event-driven-resonance.md:67 | memory/runs/gathering_expedition/p2_2608.30439.pdf; corpus/papers_reference_nonredistributable/paper_2608.30439.pdf; docs/report_v1/sources/receipts/paper_2608.30439.md |
| 2609.07370 | arxiv | watch/inbox/48h_synth/steals.md:145 | watch/inbox/frontier_olm_20260928/sweep/_raw/abs_2609.07370.html; watch/inbox/frontier_olm_20260928/sweep/_raw/full_2609.07370.html; watch/inbox/frontier_olm_20260928/sweep/_raw/full_2609.07370.txt |
| 2609.07901 | arxiv-bare | watch/inbox/frontier_olm_2026-09-30/steal/quantization-compression.md:32; watch/inbox/frontier_olm_2026-09-30/steal/quantization-compression.md:7; watch/inbox/frontier_olm_2026-09-30/steal/quantization-compression.md:8 | memory/runs/gathering_expedition/p2_2609.07901.pdf; corpus/papers_reference_nonredistributable/paper_2609.07901.pdf; docs/report_v1/sources/receipts/paper_2609.07901.md |
| 2609.16338 | arxiv-bare | watch/inbox/frontier_olm_2026-09-30/steal/quantization-compression.md:42; watch/inbox/frontier_olm_2026-09-30/steal/quantization-compression.md:7; watch/inbox/frontier_olm_2026-09-30/steal/quantization-compression.md:8 | memory/runs/gathering_expedition/p2_2609.16338.pdf; corpus/papers_reference_nonredistributable/paper_2609.16338.pdf; docs/report_v1/sources/receipts/paper_2609.16338.md |
| 2609.18526 | arxiv | watch/inbox/frontier_olm_2026-10-01/DIGEST.md:105; watch/inbox/frontier_olm_2026-10-01/DIGEST.md:11; watch/inbox/frontier_olm_2026-10-01/DIGEST.md:83 (+1 more) | memory/runs/gathering_expedition/p2_2609.18526.pdf; corpus/papers_reference_nonredistributable/paper_2609.18526.pdf; docs/report_v1/sources/receipts/paper_2609.18526.md |
| 2609.23125 | arxiv-bare | watch/inbox/frontier_olm_2026-09-30/steal/quantization-compression.md:22; watch/inbox/frontier_olm_2026-09-30/steal/quantization-compression.md:7; watch/inbox/frontier_olm_2026-09-30/steal/quantization-compression.md:8 | memory/runs/gathering_expedition/p2_2609.23125.pdf; corpus/papers_reference_nonredistributable/paper_2609.23125.pdf; docs/report_v1/sources/receipts/paper_2609.23125.md |
| 2609.23742 | arxiv | watch/inbox/48h_synth/steals.md:31 | state/arxiv/2026-09-22/2609.23742v1.txt; watch/inbox/frontier_olm_20260928/sweep/_raw/abs_2609.23742.html; watch/inbox/frontier_olm_20260928/sweep/_raw/full_2609.23742.html |
| 2609.24799 | arxiv-bare | watch/inbox/frontier_olm_2026-09-30/steal/quantization-compression.md:52; watch/inbox/frontier_olm_2026-09-30/steal/quantization-compression.md:7; watch/inbox/frontier_olm_2026-09-30/steal/quantization-compression.md:8 | state/arxiv/2026-09-22/2609.24799v1.txt; state/arxiv/2026-09-22/2609.24799v1.txt |
| 2609.25447 | arxiv | watch/inbox/frontier_olm_2026-10-01/DIGEST.md:11; watch/inbox/frontier_olm_2026-10-01/DIGEST.md:82; watch/inbox/frontier_olm_2026-10-01/steal/open-local-language-models.md:174 (+1 more) | state/arxiv/2026-09-23/2609.25447v1.txt; state/arxiv/2026-09-23/2609.25447v1.txt |
| 2609.26693 | arxiv | watch/inbox/frontier_olm_2026-10-01/DIGEST.md:47; watch/inbox/frontier_olm_2026-10-01/DIGEST.md:80; watch/inbox/frontier_olm_2026-10-01/steal/open-local-language-models via x.md:103 (+1 more) | state/arxiv/2026-09-23/2609.26693v1.txt; state/arxiv/2026-09-23/2609.26693v1.txt |
| 2609.29144 | arxiv | watch/inbox/frontier_olm_2026-09-30/steal/agent-memory-continuity.md:39; watch/inbox/frontier_olm_2026-09-30/steal/agent-memory-continuity.md:41; watch/inbox/frontier_olm_2026-09-30/steal/agent-memory-continuity.md:64 | memory/runs/gathering_expedition/p2_2609.29144.pdf; corpus/papers_reference_nonredistributable/paper_2609.29144.pdf; docs/report_v1/sources/receipts/paper_2609.29144.md |
| 2609.31540 | arxiv-bare | watch/inbox/frontier_olm_2026-09-30/steal/open-and-local-language-models via reddit.md:151; watch/inbox/frontier_olm_2026-09-30/steal/open-and-local-language-models.md:13; watch/inbox/frontier_olm_2026-09-30/steal/open-and-local-language-models.md:19 (+5 more) | state/arxiv/2026-09-28/2609.31540v1.txt; state/arxiv/2026-09-28/2609.31540v1.txt |
| 2609.31678 | arxiv | watch/inbox/frontier_olm_2026-10-01/DIGEST.md:11; watch/inbox/frontier_olm_2026-10-01/DIGEST.md:81; watch/inbox/frontier_olm_2026-10-01/steal/open-local-language-models.md:150 | memory/runs/gathering_expedition/p2_2609.31678.pdf; corpus/papers_reference_nonredistributable/paper_2609.31678.pdf; docs/report_v1/sources/receipts/paper_2609.31678.md |
| 2609.32042 | arxiv | watch/inbox/48h_synth/steals.md:77; watch/inbox/48h_synth/steals.md:94 | watch/inbox/frontier_olm_20260928/sweep/_raw/abs_2609.32042.html; watch/inbox/frontier_olm_20260928/sweep/_raw/full_2609.32042.html; watch/inbox/frontier_olm_20260928/sweep/_raw/full_2609.32042.txt |
| 2609.32049 | arxiv | watch/inbox/frontier_olm_2026-09-30/steal/agent-memory-continuity.md:15; watch/inbox/frontier_olm_2026-09-30/steal/agent-memory-continuity.md:17; watch/inbox/frontier_olm_2026-09-30/steal/agent-memory-continuity.md:61 | memory/runs/gathering_expedition/p2_2609.32049.pdf; corpus/papers_reference_nonredistributable/paper_2609.32049.pdf; docs/report_v1/sources/receipts/paper_2609.32049.md |
| 2609.34160 | arxiv | watch/inbox/frontier_olm_2026-09-30/steal/agent-memory-continuity.md:23; watch/inbox/frontier_olm_2026-09-30/steal/agent-memory-continuity.md:25; watch/inbox/frontier_olm_2026-09-30/steal/agent-memory-continuity.md:62 | memory/runs/gathering_expedition/p2_2609.34160.pdf; corpus/papers_reference_nonredistributable/paper_2609.34160.pdf; docs/report_v1/sources/receipts/paper_2609.34160.md |
| 2609.36805 | arxiv | watch/inbox/frontier_olm_2026-09-30/steal/agent-memory-continuity.md:31; watch/inbox/frontier_olm_2026-09-30/steal/agent-memory-continuity.md:33; watch/inbox/frontier_olm_2026-09-30/steal/agent-memory-continuity.md:63 | memory/runs/gathering_expedition/p2_2609.36805.pdf; corpus/papers_reference_nonredistributable/paper_2609.36805.pdf; docs/report_v1/sources/receipts/paper_2609.36805.md |
| 2609.37902 | arxiv-bare | watch/inbox/frontier_olm_2026-09-30/steal/open-and-local-language-models via reddit.md:151; watch/inbox/frontier_olm_2026-09-30/steal/open-and-local-language-models.md:13; watch/inbox/frontier_olm_2026-09-30/steal/open-and-local-language-models.md:20 (+5 more) | state/arxiv/2026-09-30/2609.37902v1.txt; state/arxiv/2026-09-30/2609.37902v1.txt |
| 2609.39765 | arxiv-bare | watch/inbox/frontier_olm_2026-10-01/DIGEST.md:19 | state/arxiv/2026-10-01/2609.39765v1.txt; state/arxiv/2026-10-01/2609.39765v1.txt |

## HELD (weak: temp-path only) - 1

| citation | kind | cited-where | holding evidence |
|---|---|---|---|
| 2609.27612 | arxiv | watch/inbox/48h_synth/steals.md:204 | %TEMP%/arxiv_2609.27612v1.html |

## CITED-BUT-MISSING table

| citation | kind | cited-where | held | fetchable | priority |
|---|---|---|---|---|---|
| Abrar051/sml_mcp_benchmark | github | watch/inbox/48h_synth/steals.md:145; watch/inbox/48h_synth/steals.md:31 | no | yes (public GitHub; HTTP 200 probe) | P1-HIGH |
| SakanaAI/natural_niches | github | watch/inbox/model_mating_paper_dig_20261001.md:14; watch/inbox/model_mating_paper_dig_20261001.md:141 | no | yes (public GitHub; HTTP 200 probe) | P1-HIGH |
| 2502.10436 | arxiv | watch/inbox/model_mating_paper_dig_20261001.md:72 | no | yes (arXiv public; registry verified by probes) | P1-HIGH |
| 2505.11427 | arxiv | watch/inbox/model_mating_paper_dig_20261001.md:126 | no | yes (arXiv public; registry verified by probes) | P1-HIGH |
| 2601.07054 | arxiv-bare | watch/inbox/frontier_olm_2026-10-01/DIGEST.md:100 | no | yes (arXiv public; registry verified by probes) | P1-HIGH |
| 2604.17111 | arxiv-bare | watch/inbox/frontier_olm_2026-10-01/DIGEST.md:17 | no | yes (arXiv public; registry verified by probes) | P1-HIGH |
| 2609.12002 | arxiv-bare | watch/inbox/frontier_olm_2026-10-01/DIGEST.md:15 | no | yes (arXiv public; registry verified by probes) | P1-HIGH |
| 2609.29757 | arxiv-bare | watch/inbox/frontier_olm_2026-10-01/DIGEST.md:105 | no | yes (arXiv public; registry verified by probes) | P1-HIGH |
| 2609.32584 | arxiv-bare | watch/inbox/frontier_olm_2026-10-01/DIGEST.md:19 | no | yes (arXiv public; registry verified by probes) | P1-HIGH |
| 2609.33180 | arxiv | watch/inbox/48h_synth/steals.md:124 | no | yes (arXiv public; registry verified by probes) | P1-HIGH |
| 2609.35875 | arxiv-bare | watch/inbox/frontier_olm_2026-10-01/DIGEST.md:17 | no | yes (arXiv public; registry verified by probes) | P1-HIGH |
| 2609.36457 | arxiv-bare | watch/inbox/frontier_olm_2026-10-01/DIGEST.md:19 | no | yes (arXiv public; registry verified by probes) | P1-HIGH |
| Niko1221/Strata | github | watch/inbox/STRATA_DROP_20261001.md:4 | no | yes (public GitHub; HTTP 200 probe) | P1-HIGH |
| gauravapiscean/agentic-kv-cache | github | watch/inbox/48h_synth/steals.md:61 | no | yes (public GitHub; HTTP 200 probe) | P1-HIGH |
| huawei-csl/KVarN | github | watch/inbox/frontier_olm_2026-10-01/DIGEST.md:113 | no | yes (public GitHub; HTTP 200 probe) | P1-HIGH |
| StewAlexander-com/continuous-ai | github | watch/inbox/localfirst/aida.md:8; watch/inbox/localfirst/aida.md:82 | no | yes (public GitHub; HTTP 200 probe) | P2-MED |
| 2006.16236 | arxiv-bare | watch/inbox/spiking_wide/linear-family.md:32 | no | yes (arXiv public; registry verified by probes) | P3-LOW |
| 2310.08560 | arxiv | watch/inbox/localfirst/adjacent.md:32 | no | yes (arXiv public; registry verified by probes) | P3-LOW |
| 2312.04927 | arxiv-bare | watch/inbox/spiking_wide/linear-family.md:39 | no | yes (arXiv public; registry verified by probes) | P3-LOW |
| 2312.06635 | arxiv-bare | watch/inbox/spiking_wide/linear-family.md:33 | no | yes (arXiv public; registry verified by probes) | P3-LOW |
| 2402.01032 | arxiv-bare | watch/inbox/spiking_wide/linear-family.md:40 | no | yes (arXiv public; registry verified by probes) | P3-LOW |
| 2402.18668 | arxiv-bare | watch/inbox/spiking_wide/linear-family.md:41 | no | yes (arXiv public; registry verified by probes) | P3-LOW |
| 2403.19887 | arxiv-bare | watch/inbox/spiking_wide/linear-family.md:43 | no | yes (arXiv public; registry verified by probes) | P3-LOW |
| 2404.05892 | arxiv-bare | watch/inbox/spiking_wide/linear-family.md:37 | no | yes (arXiv public; registry verified by probes) | P3-LOW |
| 2405.21060 | arxiv-bare | watch/inbox/spiking_wide/linear-family.md:36 | no | yes (arXiv public; registry verified by probes) | P3-LOW |
| 2406.06484 | arxiv-bare | watch/inbox/spiking_wide/linear-family.md:34 | no | yes (arXiv public; registry verified by probes) | P3-LOW |
| 2410.05355 | arxiv | watch/inbox/spiking_wide/linear-family.md:17 | no | yes (arXiv public; registry verified by probes) | P3-LOW |
| 2410.12032 | arxiv-bare | watch/inbox/spiking_wide/energy-frontier.md:158 | no | yes (arXiv public; registry verified by probes) | P3-LOW |
| 2501.00663 | arxiv-bare | watch/inbox/spiking_wide/linear-family.md:44 | no | yes (arXiv public; registry verified by probes) | P3-LOW |
| 2503.14456 | arxiv-bare | watch/inbox/spiking_wide/linear-family.md:38 | no | yes (arXiv public; registry verified by probes) | P3-LOW |
| 2507.06457 | arxiv-bare | watch/inbox/spiking_wide/linear-family.md:46 | no | yes (arXiv public; registry verified by probes) | P3-LOW |
| 2507.22448 | arxiv | watch/inbox/spiking_wide/linear-family.md:17 | no | yes (arXiv public; registry verified by probes) | P3-LOW |
| 2511.23404 | arxiv | watch/inbox/spiking_wide/linear-family.md:18 | no | yes (arXiv public; registry verified by probes) | P3-LOW |
| 2609.34422 | arxiv-bare | watch/inbox/frontier_olm_2026-09-30/steal/agent-memory-continuity.md:49 | no | yes (arXiv public; registry verified by probes) | P3-LOW |
| KJP-Git/myAgentMemory | github | watch/inbox/localfirst/pam.md:11 | no | yes (public GitHub; HTTP 200 probe) | P3-LOW |
| MoonshotAI/Kimi-Linear | github | watch/inbox/spiking_wide/linear-family.md:13 | no | yes (public GitHub; HTTP 200 probe) | P3-LOW |
| RichSchefren/atlas | github | watch/inbox/localfirst/atlas.md:7 | no | yes (public GitHub; HTTP 200 probe) | P3-LOW |
| csnyder256/RAG-OS | github | watch/inbox/localfirst/ragos.md:5 | no | yes (public GitHub; HTTP 200 probe) | P3-LOW |
| santhoshravindran7/portable-agent-memory | github | watch/inbox/localfirst/pam.md:9 | no | yes (public GitHub; HTTP 200 probe) | P3-LOW |
| state-spaces/mamba | github | watch/inbox/spiking_wide/linear-family.md:14 | no | yes (public GitHub; HTTP 200 probe) | P3-LOW |

Priority legend (claim-weight): P1-HIGH = cited by a drop receipt, 48h_synth steals chapter, olm
DIGEST headline, or 3+ cite locations (a banked claim rests on it in the widest-read surfaces);
P2-MED = 2 cite locations in steal cards; P3-LOW = 1 cite location in a steal card.

## Named examples of the leak (highest claim-weight)

1. arXiv 2509.05276 (SpikingBrain) - 13 cite locations across spiking_wide (7 cards) +
   SPIKINGBRAIN_DROP_20261001. At sweep start not one byte was held: the entire wide dig rested
   on prose quotes only. TWO MID-SWEEP HEALS: the spiking-wide gala lane banked abstract bytes
   (watch/inbox/gala_20260925/spiking-wide/lanes/ev_arxiv_2509_05276_abstract.md, 1,461 bytes,
   18:33Z) and the gathering_expedition lane landed the full paper (memory/runs/gathering_expedition/
   p2_2509.05276.pdf, 3.9MB, 19:34Z). The estate healed its biggest leak while this lane measured it.
2. arXiv 2508.16204 (Sakana natural niches) - 10 cite locations in model_mating_paper_dig_20261001
   (MATE_MOE GO-ready verdict). Held at final re-check ONLY via the healer's p2_2508.16204.pdf
   (7.5MB, 19:35Z); no holding existed at sweep start. Repo github.com/SakanaAI/natural_niches
   still not cloned anywhere in the estate.
3. arXiv 2608.10644 - 4 cites in frontier_olm_2026-09-30/steal/agent-memory-continuity.md (the
   agent-memory headline card). Not held at sweep start, while sibling ids from the same sweep
   window (2609.31540, 2609.37902) WERE held in state/arxiv: the old holding pass was partial, not
   principled. The healer's p2_2608.10644.pdf (355KB, 19:34Z) closed this one mid-sweep.
4. github.com/RichSchefren/atlas - localfirst/atlas.md:7 says the card was written from a shallow
   clone at pinned HEAD 229df544944ffb1dadf4d155bcb41334e850da0c, 339 files, read first-hand. The
   clone survives nowhere in the estate: the first-hand-verification claim is unverifiable by bytes.
5. arXiv 2609.27612 (48h_synth/steals.md:204) - catalog hit is a %TEMP% file only
   (%TEMP%/arxiv_2609.27612v1.html). Temp-dir bytes are not a durable estate holding. Classed WEAK.
6. ractor50/accuracy.md:31,33 cites arXiv 2407.12345 as the UF-124/125/126 fabricated-citation
   artifact (the poison canary, accuracy.md:33 falsifier). The id itself resolves (HTTP 200 probe)
   but no banked claim rests on its content; recorded n/a, not counted missing.

## Instrument proposal (decision ledger)

ractor50/accuracy.md:35 already specs a citation resolver at the ledger append path (each id must
resolve to fetched bytes in the same session, else the row lands UNVERIFIED, never LANDED). This
sweep extends it to holdings: every LANDED row citing an external primary should leave the primary
bytes in state/arxiv/<date>/<id>v1.txt (the existing 4,010-file archive) or a corpus dir, and cite
that path. A nightly sweep (this lane's three scripts) diffs fresh receipts against holdings and
flags new leaks before the session that held the bytes dies.

Not run / limits: book-class and non-id primaries (e.g. Wilkes/Wheeler/Gill 1951, already held in
corpus/papers_reference_nonredistributable/) out of scope beyond the extracted id/repo set; unprobed
arXiv ids inherit fetchability from the 3-probe registry verification (same host, same id shape);
content-level checks (does the held text contain the quoted claim) NOT run: held means bytes exist,
not that the quote was re-verified against them.

