source-fetched: 2026-10-03

Fold receipt for watch/inbox/frontier_olm_2026-10-03/, written 2026-10-03 by the fold seat. Every byte count below was measured this session by a .venv/Scripts/python.exe os.path.getsize walk over this folder (script kept at %TEMP%/gen_receipt.py and %TEMP%/fold_inventory.py); nothing is hand-copied.

## Fold files

```text
| file | bytes |
|---|---|
| DIGEST.md | 30695 | (sweep/tmp/fold2_inventory_current.txt)
| register.jsonl | 24640 | (sweep/tmp/fold2_inventory_current.txt)
| percolator_candidates.jsonl | 15161 | (sweep/tmp/fold2_inventory_current.txt)
| RECEIPT.md | 15190 | (sweep/tmp/fold2_inventory_current.txt)
```

The RECEIPT.md figure is self-measured: the file is written with a fixed-width placeholder, the final size is computed to a fixed point, the number is substituted at the same width, and the result is re-measured to confirm equality (see Checks).

## Counts

- Inputs carried from the run: 32 sweep results (8 areas x 4 sources: arxiv, hn, reddit, x), 238 lane-banked items counted from those results, 24 confirmation candidates (23 confirmed, 1 struck), 5 steal cards.
- register.jsonl rows: 23 (one per confirmed find).
- percolator_candidates.jsonl rows: 5 (one per steal: claim, source_url, estate_map, probe, plus area and steal_card provenance).
- Unconfirmed and held out of the register: 1 (arxiv.org/abs/2610.00905: quote verbatim-confirmed and counts supported, central assertion contradicted by the page; evidence and disposition in DIGEST.md).

### Finds by area (23 total)

- swarm-orchestration via arxiv: 5
- swarm-orchestration: 4
- evals-and-self-improvement via reddit: 6
- open-and-local-language-models: 5
- quantization-and-compression: 3

### Finds by source (primary URL surface of each find)

- arxiv.org (export API / abs / html): 8
- reddit via Arctic Shift archive: 6
- news.ycombinator.com: 4
- provider docs direct: 2
- x.com via fxtwitter: 1
- tomshardware.com: 1
- quesma.com: 1

## Steal cards (full text under steal/)

- steal/evals-and-self-improvement via reddit.md (18100 bytes)
- steal/open-and-local-language-models.md (16240 bytes)
- steal/quantization-and-compression.md (20931 bytes) + steal/quantization-and-compression.json (3729 bytes, steering-gate card JSON)
- steal/swarm-orchestration.md (7416 bytes)
- steal/swarm-orchestration via arxiv.md (7314 bytes)

## Workflow gate row pointer

NOT FOUND for this run, reported not guessed:

- `grep -c -i "frontier_olm" memory/workflows/REGISTRY.jsonl` returned 0 over 63 lines (re-run at receipt time).
- Distinct-name census of the same file shows 7 rows named frontier-olm-mine / frontier-olm-mine.dwf.ts, all timestamped 2026-09-29 or 2026-09-30 (lines 31-40); none carries a 2026-10-02 or 2026-10-03 timestamp.
- The registry's 2026-10-03 rows are lines 61-63: `Wide-dig-the-Grok-bot-ecosystem.dwf.ts` (20:18:03Z), `gap-analysis.dwf.ts` (21:17:54Z), `music-cut.dwf.ts` (21:56:30Z), all different workflows.

OWED: the 2026-10-03 olm mine run has no workflow-gate row in memory/workflows/REGISTRY.jsonl. Either the run was gated under a name both greps missed, or the gate check never registered; the gate owner should resolve this.

## Cross-checks: measured bytes vs the lanes' own claimed byte counts

Every file whose lane note named a byte or char count was re-measured; all 10 match:

```text
- `steal/evals-and-self-improvement via reddit.md`: claimed 18100, measured 18100, match True (sweep/tmp/fold2_inventory_current.txt)
- `steal/open-and-local-language-models.md`: claimed 16240, measured 16240, match True (sweep/tmp/fold2_inventory_current.txt)
- `steal/quantization-and-compression.md`: claimed 20931, measured 20931, match True (sweep/tmp/fold2_inventory_current.txt)
- `steal/swarm-orchestration via arxiv.md`: claimed 7314, measured 7314, match True (sweep/tmp/fold2_inventory_current.txt)
- `steal/swarm-orchestration.md`: claimed 7416, measured 7416, match True (sweep/tmp/fold2_inventory_current.txt)
- `sweep/agent-memory-and-continuity-x.md`: claimed 12374, measured 12374, match True (sweep/tmp/fold2_inventory_current.txt)
- `sweep/evals-and-self-improvement-x.md`: claimed 16905, measured 16905, match True (sweep/tmp/fold2_inventory_current.txt)
- `sweep/kv-cache-and-context-engineering-reddit.md`: claimed 14506, measured 14506, match True (sweep/tmp/fold2_inventory_current.txt)
- `sweep/kv-cache-and-context-engineering-x.md`: claimed 16674, measured 16674, match True (sweep/tmp/fold2_inventory_current.txt)
- `sweep/quantization-and-compression-hn.md`: claimed 19205, measured 19205, match True (sweep/tmp/fold2_inventory_current.txt)
```

## Checks run this fold (commands and outcomes)

1. Folder walk + byte measurement: `.venv/Scripts/python.exe C:/Users/foste/AppData/Local/Temp/fold_inventory.py` (os.path.getsize over every file, run before and after the fold files landed).
2. Gate registry grep: `grep -n -i "frontier_olm" memory/workflows/REGISTRY.jsonl` (0 matches, 61 lines) and `grep -o '"name": "[^"]*"' ... | sort | uniq -c` (name census above).
3. Confirmation-evidence file (cold-reader round 2): the unconfirmed item's full-text HTML was copied into the run folder so it survives Temp cleanup; sweep/_evidence_2610.00905_fulltext.html: 584526 bytes, sha256 c16ffcfd5518015e080b7b729ea4d5668786f35c92b20f0f43c78064da585f98 (temp fetch c16ffcfd5518015e080b7b729ea4d5668786f35c92b20f0f43c78064da585f98, identical=True). DIGEST.md cites this copy.
4. JSONL validation: json.loads per line over register.jsonl (23 rows) and percolator_candidates.jsonl (5 rows), required-field presence checked, zero parse errors, zero missing fields.
5. Em/en-dash scan over DIGEST.md, register.jsonl, percolator_candidates.jsonl and this receipt: DIGEST.md em=0 en=0, percolator_candidates.jsonl em=0 en=0, register.jsonl em=0 en=0.
6. Area/source counts computed from register.jsonl rows by script (Counter over area and URL-host buckets), not hand-tallied; area counts sum to the row count (asserted in script).

Provenance boundary: all sweep, confirmation, and steal-card claims in DIGEST.md / register.jsonl / percolator_candidates.jsonl are carried from the run's own outputs and cite their bank files; this seat re-verified only on-disk facts (items 1-6 above) and did not re-fetch remote URLs.

## Full folder inventory (162 files, 24546995 bytes)

```text
     177  .mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_7_1.continue.json
    1581  .mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_7_1.json
    1241  .mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_7_1.mut1t5nl-49612-9e46c4d5e6.baseline/06ae5fba3b84a9d1961ad518056c10ad6b2d4d13a61a390f486fcc1c84edc64b.source
    2450  .mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_7_1.mut1t5nl-49612-9e46c4d5e6.baseline/3d2d241ea322b8470004cb85423ae252a3ada17319627573ba6dd1aeefde5ba4.source
    2434  .mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_7_1.mut1t5nl-49612-9e46c4d5e6.baseline/4cfe44fc8963ff7d904aeac09939b1ff2d3f3c2a91767fcdd4816e675c5cc81d.source
    2015  .mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_7_1.mut1t5nl-49612-9e46c4d5e6.baseline/70b4e155eb220096b9fbec8f0ff1ba0e8af34a3fd953a3bf70b117ddd6bcffea.source
    1985  .mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_7_1.mut1t5nl-49612-9e46c4d5e6.baseline/84e442b7300e63be720f636919741be5151ce9d7d2b69ad2179d6f24a8652720.source
    1972  .mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_7_1.mut1t5nl-49612-9e46c4d5e6.baseline/8abc47736210550f5e3ce73249c7aefef9ce9fee9639cc1b3c1af8e64b8cb045.source
    1291  .mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_7_1.mut1t5nl-49612-9e46c4d5e6.baseline/9887707520e9d08b81ccc25ba3027b250772824d82284191ca77b176187c14a0.source
    1282  .mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_7_1.mut1t5nl-49612-9e46c4d5e6.baseline/d6fa7ae538ad70c87782422e1792bbc67c123d3e32df4f8c4617e5c11e62f9a9.source
    1459  .mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_7_1.mut1t5nl-49612-9e46c4d5e6.baseline/d89ac0d82828ec0584136c1ddf2a8a90e1d53c65a3c126ba7b8bf97a94b1b544.source
     418  .mimosa/hook-status/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_7_1-148d7e425a.json
   30695  DIGEST.md
   15190  RECEIPT.md
    2434  lens/_count_corpus.py
    1459  lens/_count_corpus2.py
    2450  lens/_count_corpus3.py
    1291  lens/_count_corpus4.py
    2015  lens/_count_corpus5.py
   16648  lens/burns.md
    7689  lens/corpus.md
    6020  lens/doors.md
    5602  lens/graph.md
   27522  lens/laws.md
   21578  lens/questions.md
   15161  percolator_candidates.jsonl
   24640  register.jsonl
   18100  steal/evals-and-self-improvement via reddit.md
   16240  steal/open-and-local-language-models.md
    3729  steal/quantization-and-compression.json
   20931  steal/quantization-and-compression.md
    7314  steal/swarm-orchestration via arxiv.md
    7416  steal/swarm-orchestration.md
     218  sweep/.mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_3_27.json
     729  sweep/.mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_3_28.json
     177  sweep/.mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_6_1.continue.json
     923  sweep/.mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_6_1.json
    1972  sweep/.mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_6_1.muspgis1-48464-8570242da5.baseline/27b1afef71f470bfd9060201f87bcff44aa55f4e47532ae58e5b4cbf0436687a.source
    1985  sweep/.mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_6_1.muspgis1-48464-8570242da5.baseline/c74aa2ab897e45f4dca4ed742ca9b2dfe161c0dc16f1d62fdd457921627f5a85.source
    1241  sweep/.mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_6_1.muspgis1-48464-8570242da5.baseline/c769d5764422161d4f179fa6f53fa05fbad600cb10b332fb39d7e48aaa3bb80b.source
    1282  sweep/.mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_6_1.muspgis1-48464-8570242da5.baseline/df7158de303a6a8ddf3aabab3f8ee1f2d9434317db31cc9886b3e60a473471db.source
     411  sweep/.mimosa/hook-status/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_3_27-392cbc3656.json
     407  sweep/.mimosa/hook-status/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_3_28-6e6129f6de.json
    1282  sweep/_arxiv_deep.py
       0  sweep/_arxiv_judge.xml
    1972  sweep/_arxiv_sweep.py
  129620  sweep/_bing1.html
  584526  sweep/_evidence_2610.00905_fulltext.html
    7901  sweep/_frozen_judges.html
    1241  sweep/_grep_kv.py
   91467  sweep/_hn49611128.json
     218  sweep/_raw/.mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_3_21.json
     542  sweep/_raw/.mimosa/hook-status/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_3_21-99bfb4de3d.json
  443078  sweep/_raw/2609.32852v1.html
   82493  sweep/_raw/2609.32852v1.txt
  303306  sweep/_raw/2609.32961v1.html
   84770  sweep/_raw/2609.32961v1.txt
  537754  sweep/_raw/2609.39068v1.html
  103921  sweep/_raw/2609.39068v1.txt
  330010  sweep/_raw/2609.39329v1.html
   72846  sweep/_raw/2609.39329v1.txt
  436288  sweep/_raw/2610.00412v1.html
   69644  sweep/_raw/2610.00412v1.txt
   53377  sweep/_raw/idlist_shortlist.xml
    2207  sweep/_syn.html
   13427  sweep/agent-memory-and-continuity-arxiv.md
   12078  sweep/agent-memory-and-continuity-hn.md
   20707  sweep/agent-memory-and-continuity-reddit.md
   12374  sweep/agent-memory-and-continuity-x.md
 1623827  sweep/arctic_LocalLLM.json
 1848115  sweep/arctic_LocalLLaMA.json
  669169  sweep/arctic_MachineLearning.json
    1334  sweep/arctic_grep.ps1
    1046  sweep/arctic_grep2.ps1
  619006  sweep/arctic_ollama.json
    2455  sweep/arctic_sweep.ps1
    2828  sweep/ddg_sweep.ps1
    2361  sweep/deep_read.ps1
    2041  sweep/deep_read_evals.ps1
   11147  sweep/evals-and-self-improvement-arxiv.md
   12911  sweep/evals-and-self-improvement-hn.md
   12559  sweep/evals-and-self-improvement-reddit.md
   16905  sweep/evals-and-self-improvement-x.md
    1767  sweep/fetch_extra.ps1
    1354  sweep/fetch_reddit.ps1
     628  sweep/find_kvarn.ps1
     330  sweep/find_phantom.ps1
   24309  sweep/finetuning-and-adaptation-arxiv.md
   10148  sweep/finetuning-and-adaptation-hn.md
   11174  sweep/finetuning-and-adaptation-reddit.md
    9971  sweep/finetuning-and-adaptation-x.md
     314  sweep/grep_laws.ps1
    7041  sweep/inference-efficiency-arxiv.md
   11784  sweep/inference-efficiency-hn.md
   14644  sweep/inference-efficiency-reddit.md
    8953  sweep/inference-efficiency-x.md
   19713  sweep/kv-cache-and-context-engineering-arxiv.md
   12118  sweep/kv-cache-and-context-engineering-hn.md
   14506  sweep/kv-cache-and-context-engineering-reddit.md
   16674  sweep/kv-cache-and-context-engineering-x.md
       0  sweep/llama_top.json
   15474  sweep/open-and-local-language-models-arxiv.md
   13293  sweep/open-and-local-language-models-hn.md
   20487  sweep/open-and-local-language-models-reddit.md
   16815  sweep/open-and-local-language-models-x.md
    2621  sweep/overlap_grep.ps1
    1699  sweep/print_threads.ps1
    1261  sweep/probe_doors.ps1
    1379  sweep/probe_doors2.ps1
   11035  sweep/quantization-and-compression-arxiv.md
   19205  sweep/quantization-and-compression-hn.md
   10809  sweep/quantization-and-compression-reddit.md
   10652  sweep/quantization-and-compression-x.md
  324208  sweep/rss_LocalLLM.xml
  324401  sweep/rss_LocalLLaMA.xml
  324729  sweep/rss_MachineLearning.xml
  324734  sweep/rss_ollama.xml
   15734  sweep/swarm-orchestration-arxiv.md
    8124  sweep/swarm-orchestration-hn.md
   15844  sweep/swarm-orchestration-reddit.md
   15604  sweep/swarm-orchestration-x.md
    8518  sweep/thread_1w9llr4.json
   19667  sweep/thread_1w9myqc.json
  112274  sweep/thread_1wc6tka.json
   75849  sweep/thread_1wdasar.json
    5524  sweep/thread_1wdc1jj.json
   40919  sweep/thread_1wloz92.json
  267902  sweep/thread_1wms904.json
   86583  sweep/thread_1wnedrc.json
  157618  sweep/thread_1wp5668.json
     605  sweep/thread_1wpodl1.json
  491293  sweep/thread_1wr5ylm.json
  448133  sweep/thread_1wsq0pa.json
  466380  sweep/thread_1wsuag0.json
  140775  sweep/thread_1wt03zh.json
    5198  sweep/thread_1wu1ugy.json
   11746  sweep/thread_1wu6reb.json
  171070  sweep/thread_1wv05u1.json
   84124  sweep/thread_1wv09ja.json
     588  sweep/thread_1wv0b24.json
  502073  sweep/thread_1wv1u54.json
     640  sweep/thread_1wvwdn1.json
    1381  sweep/tmp/.mimosa/finding-ledger/v1/events/batch-pretooluse-a37136a9fa4c5726c4471e64708c91d7.json
    1160  sweep/tmp/.mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_3_15.json
     970  sweep/tmp/.mimosa/hook-status/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_3_15-638ae0bd8b.json
    1985  sweep/tmp/as_sweep.py
    6456  sweep/tmp/as_test.json
   35127  sweep/tmp/batch1.json
 1102933  sweep/tmp/candidates.jsonl
 9996693  sweep/tmp/candidates_full.jsonl
   20950  sweep/tmp/comments_1w67g8k.json
    6273  sweep/tmp/comments_1w6gg8v.json
   17692  sweep/tmp/comments_1w950fw.json
   13220  sweep/tmp/comments_1wb35xo.json
   32537  sweep/tmp/comments_1wbc03f.json
   25554  sweep/tmp/comments_1wbifl0.json
    6034  sweep/tmp/comments_1wg442g.json
    8300  sweep/tmp/comments_1wmafge.json
    4577  sweep/tmp/comments_test.json
     263  sweep/tmp/post_1w950fw.json
   19294  sweep/tmp/ranked_ids.json
      54  sweep/tmp/search_cc_agent.json
```

---

## Round 2 fold receipt (2026-10-04 night seat)

Round-2 fold of the same run: DIGEST.md gained the Round 2 fold section (and its header counts were updated), register.jsonl grew from 23 to 42 rows (rows 24-42; row 38 deep-reads the paper of round-1 row 23, overlap stated in-row), percolator_candidates.jsonl grew from 5 to 9 rows (rows 6-9). Line 1 of this receipt is unchanged. Amended the same sitting after a cold-reader review: 14 fixes applied to DIGEST.md (probe-status ledger for round-1 probe 1, census reconciliation with the round-1 marker counts, banking-shape correction with the round-2 item count, OUI-1 wiring clarification, reap-phrasing moved to hypothesis, 42-rows-over-41-distinct restatement, knowledge-graph reconciliation by parse, bypass-import status and scope, contradiction-headline softening, pullpush door annotation, referent expansions for the Jev dossier and Gevva0, 6 GB headline scoped to the fetched window, quant-probe ordering, confirmed-table count restatement). Every byte count below was measured this sitting by .venv/Scripts/python.exe os.walk/getsize (scripts kept at sweep/tmp/fold2_inventory.py, sweep/tmp/fold2_build.py, sweep/tmp/fold2_receipt.py); nothing is hand-copied.

### Fold files (current bytes, measured after the round-2 append)

```text
| file | bytes |
|---|---|
| DIGEST.md | 66471 | (sweep/tmp/fold2_inventory_current.txt)
| register.jsonl | 45274 | (sweep/tmp/fold2_inventory_current.txt)
| percolator_candidates.jsonl | 29091 | (sweep/tmp/fold2_inventory_current.txt)
| RECEIPT.md | 47271 | (sweep/tmp/fold2_inventory_current.txt)
```

The RECEIPT.md figure is self-measured at a fixed point: the file is written with a 5-digit placeholder, the final size is computed, the placeholder is substituted at equal width, and the result is re-measured to confirm equality (asserted in fold2_receipt.py).

### Counts

- Round-2 inputs carried: 32 second-pass lane sections (appended to the same 32 sweep/ bank files, round-1 sections preserved), 227 round-2 lane-banked items counted by the fold seat from the round-2 sweep results handed to the fold (open-and-local-language-models 31, quantization-and-compression 28, agent-memory-and-continuity 29, swarm-orchestration 27, finetuning-and-adaptation 31, kv-cache-and-context-engineering 28, evals-and-self-improvement 28, inference-efficiency 25), 24 round-2 confirmation candidates resolved to 19 confirmed plus 5 held with evidence, 4 round-2 steal cards.
- register.jsonl rows: 42 (23 round-1 + 19 appended), json.loads-validated line by line this sitting.
- percolator_candidates.jsonl rows: 9 (5 + 4), json.loads-validated line by line this sitting.
- Unconfirmed and held out of the register (round 2): 5, each with confirmation evidence and disposition in DIGEST.md's round-2 unconfirmed section (Ollama 0.35.1 regression claim, Featherless roster-halving claim, LLM7 churn claim, TTPO archive-confirmed-but-page-unseen, OUI-1 license-flip quote).

### Finds by area (round-2 register rows, 19 total)

- agent-memory-and-continuity: 1
- finetuning-and-adaptation via reddit: 6
- open-and-local-language-models: 9
- quantization-and-compression: 3

### Finds by source (round-2 register rows, bucketed by each row's source field)

- HN door: Algolia + primaries (GitHub releases API, Featherless API): 2
- arXiv export API / abs (quant lane, field reads as arxiv): 3
- arXiv export API via curl + abs pages + HF card/API (olm arxiv+hf lane): 7
- hn (quesma primary): 1
- reddit via the Arctic Shift archive door (finetuning lane): 6

### Workflow gate row pointer

FOUND; this resolves round 1's NOT FOUND above (that row landed after the 17:09 receipt was written):

- memory/workflows/REGISTRY.jsonl:64 = ts 2026-10-04T02:33:47Z, name olm-mine.dwf.ts, digest 70571fea3957, script .zcode/workflows/olm-mine.dwf.ts, verdict PASS, checks G1-multiplicity ok=true, G2-passoff ok=true, G3-steering ok=true, G4-salvage ok=true, G5-deliverable ok=true, G6-receipts ok=true, G7-laws ok=true

Re-located this sitting by scanning memory/workflows/REGISTRY.jsonl line by line for olm-mine inside fold2_receipt.py.

### Cross-checks: lane-claimed counts vs measured bytes (round 2)

All 10 named claims match. Files claimed in characters are pure ASCII, so chars equal bytes there.

```text
| file | claimed unit | claimed | measured | match |
|---|---|---|---|---|
| steal/agent-memory-and-continuity.md | chars | 16124 | 16124 | true | (sweep/tmp/fold2_inventory_current.txt)
| steal/open-and-local-language-models-arxiv-hf.md | bytes | 24852 | 24852 | true | (sweep/tmp/fold2_inventory_current.txt)
| steal/quantization-and-compression.md | chars | 22856 | 22856 | true | (sweep/tmp/fold2_inventory_current.txt)
| sweep/agent-memory-and-continuity-hn.md | bytes | 15259 | 15259 | true | (sweep/tmp/fold2_inventory_current.txt)
| sweep/evals-and-self-improvement-x.md | bytes | 21603 | 21603 | true | (sweep/tmp/fold2_inventory_current.txt)
| sweep/open-and-local-language-models-arxiv.md | bytes | 18525 | 18525 | true | (sweep/tmp/fold2_inventory_current.txt)
| sweep/quantization-and-compression-hn.md | bytes | 34342 | 34342 | true | (sweep/tmp/fold2_inventory_current.txt)
| sweep/swarm-orchestration-hn.md | bytes | 16729 | 16729 | true | (sweep/tmp/fold2_inventory_current.txt)
| sweep/swarm-orchestration-reddit.md | bytes | 35621 | 35621 | true | (sweep/tmp/fold2_inventory_current.txt)
| sweep/swarm-orchestration-x.md | bytes | 31487 | 31487 | true | (sweep/tmp/fold2_inventory_current.txt)
```

### Round-1 anchor repairs forced by the citation gate

Three blocking findings on the amended DIGEST.md were repaired before landing, all disclosed:

1. The round-1 digest's design-detail anchor pointed into sweep/swarm-orchestration-arxiv.md at line 41, which went blank when the round-2 swarm lane REPLACED that bank file (the lane's own note declares the replacement); the design detail now lives at sweep/agent-memory-and-continuity-x.md:44 and the anchor was moved there.
2. A round-1 evidence bullet named RECEIPT.md inside the same sentence block as the struck paper's counts (phantom-number); the RECEIPT.md mention moved to its own bullet.
3. The round-2 unconfirmed item 2 named memory/burns/LEDGER.jsonl inside the sentence carrying the re-run counts; the sentence was split so the ledger sentence carries only ledger numbers, anchored as memory/burns/LEDGER.jsonl:683 and memory/burns/LEDGER.jsonl:692 (both lines verified this sitting: they bank 22,054 and 22,059 served rows on 09-28).
4. The citation gate parses byte-count rows as sentences naming their measured files and asks which named source carries each number, so every byte-bearing row in this receipt (round-1 and round-2 alike) now also cites sweep/tmp/fold2_inventory_current.txt, the on-disk measurement receipt this fold regenerates at close. That file carries the full current walk, the total, the ten claimed-versus-measured pairs, the four historical round-1 fold-file sizes, and the six round-1 cross-check values for files the round-2 lanes since grew; all values are unchanged.

### Checks run this round-2 fold (commands and outcomes)

1. Schema + pre-append walk: .venv/Scripts/python.exe watch/inbox/frontier_olm_2026-10-03/sweep/tmp/fold2_inventory.py (register 23 rows with keys area, confidence, date, overlap, quote, source, title, url, why; percolator 5 rows with keys area, claim, estate_map, probe, source_url, steal_card; 385 files, 67186686 bytes).
2. Appends: .venv/Scripts/python.exe watch/inbox/frontier_olm_2026-10-03/sweep/tmp/fold2_build.py (register rows 24-42, percolator rows 6-9, four DIGEST header edits, round-2 section appended; post-append assertions: 42 and 9 rows parse with all required fields, appended area counts sum to 19).
3. Citation lint on the amended DIGEST.md: .venv/Scripts/python.exe tools/citation_lint.py check --files watch/inbox/frontier_olm_2026-10-03/DIGEST.md returned CITATION-LINT: ok records=1 anchors=41 numbers-checked=27 blocking=0 warns=8 enforce-tokens=False (the 8 warns are round-1 warn-only heuristics: token-miss and bare-basename shorthand; accepted, warn-only by the a05-r2 default). RECEIPT.md was linted after this section landed and any blocking finding was fixed before the fold finished.
4. Dash scan (raw bytes): results below; non-ASCII quote characters inside register.jsonl and percolator_candidates.jsonl are JSON-escaped by ensure_ascii, so the raw files stay ASCII while the decoded values preserve the verbatim quotes (one en-dash and one minus sign ride inside the verbatim Minima quote, one multiplication sign inside the Bonsai A/B quote, all as escapes).
- DIGEST.md: em-dash 0, en-dash 0 (raw file scan)
- RECEIPT.md: em-dash 0, en-dash 0 (raw file scan)
- percolator_candidates.jsonl: em-dash 0, en-dash 0 (raw file scan)
- register.jsonl: em-dash 0, en-dash 0 (raw file scan)
5. Gate registry scan: olm-mine row found at memory/workflows/REGISTRY.jsonl line 64 (see pointer above).
6. Self-size fixed point: placeholder substituted at equal width, re-measured equal (assertion in script).
7. Cold-reader fix 8 bypass-import check: grep -c inference_budget tools/stealth_driver.py tools/duel_harness.py mag/tesuji_fire.py mag/lane_runner.py mag/lite_scale.py mag/wave_fire.py tools/ds_workhorse.py returned 0 in all seven files (the four mag/ paths located by a filename walk this sitting; the card's bare names tesuji_fire, lane_runner, lite_scale and wave_fire live under mag, not tools). tools/stealth_driver.py:275 and :245 verified as the _work_lanes and work_payload definitions by sed.
8. Cold-reader fix 7 knowledge-graph reconciliation: two .venv/Scripts/python.exe parses of memory/knowledge_graph.json this sitting, output kept at sweep/tmp/kg_reconcile.json. With source/target keys: 0 nodes with degree 1 or more, 1,650 of 1,650 endpoints dangling, reproducing the 2,086/2,086 zero-degree read as a field-name bug (the schema keys edges from/to). With from/to: 602 nodes with degree 1 or more, 823 of 1,650 endpoints dangling (has_invariant 794 plus already_inside 29), 827 resolving endpoints, matching lens/graph.md's 1,484 edge-orphans (2,086 minus 602). Repair planning uses the lens numbers.
9. Receipt refresh (same sitting, cold-reader follow-up): the full folder inventory fence below was regenerated because the fix pass landed four scratch and artifact files (sweep/tmp/coldread_fix.py, sweep/tmp/fold2_receipt_fix.py, sweep/tmp/fold2_receipt_fix2.py, sweep/tmp/kg_reconcile.json) and changed DIGEST.md, RECEIPT.md and sweep/tmp/fold2_inventory_current.txt after the previous fence moment; the fold-files table values were re-verified against measured truth.

### Full folder inventory (393 files, 67438916 bytes, measured 2026-10-04 after the cold-reader fix pass)

```text
      177  .mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_7_1.continue.json
     1581  .mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_7_1.json
     1241  .mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_7_1.mut1t5nl-49612-9e46c4d5e6.baseline/06ae5fba3b84a9d1961ad518056c10ad6b2d4d13a61a390f486fcc1c84edc64b.source
     2450  .mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_7_1.mut1t5nl-49612-9e46c4d5e6.baseline/3d2d241ea322b8470004cb85423ae252a3ada17319627573ba6dd1aeefde5ba4.source
     2434  .mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_7_1.mut1t5nl-49612-9e46c4d5e6.baseline/4cfe44fc8963ff7d904aeac09939b1ff2d3f3c2a91767fcdd4816e675c5cc81d.source
     2015  .mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_7_1.mut1t5nl-49612-9e46c4d5e6.baseline/70b4e155eb220096b9fbec8f0ff1ba0e8af34a3fd953a3bf70b117ddd6bcffea.source
     1985  .mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_7_1.mut1t5nl-49612-9e46c4d5e6.baseline/84e442b7300e63be720f636919741be5151ce9d7d2b69ad2179d6f24a8652720.source
     1972  .mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_7_1.mut1t5nl-49612-9e46c4d5e6.baseline/8abc47736210550f5e3ce73249c7aefef9ce9fee9639cc1b3c1af8e64b8cb045.source
     1291  .mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_7_1.mut1t5nl-49612-9e46c4d5e6.baseline/9887707520e9d08b81ccc25ba3027b250772824d82284191ca77b176187c14a0.source
     1282  .mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_7_1.mut1t5nl-49612-9e46c4d5e6.baseline/d6fa7ae538ad70c87782422e1792bbc67c123d3e32df4f8c4617e5c11e62f9a9.source
     1459  .mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_7_1.mut1t5nl-49612-9e46c4d5e6.baseline/d89ac0d82828ec0584136c1ddf2a8a90e1d53c65a3c126ba7b8bf97a94b1b544.source
      742  .mimosa/hook-state/sess_dwf-dwfrun-3cec1e3a-3251-49cc-ac56-f0901c195b4a-actor_3_19.json
      418  .mimosa/hook-status/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_7_1-148d7e425a.json
      434  .mimosa/hook-status/sess_dwf-dwfrun-3cec1e3a-3251-49cc-ac56-f0901c195b4a-actor_3_19-2a140ca4b7.json
      437  .mimosa/hook-status/sess_dwf-dwfrun-3cec1e3a-3251-49cc-ac56-f0901c195b4a-actor_3_3-7d9f47237b.json
    66471  DIGEST.md
    47271  RECEIPT.md
     2434  lens/_count_corpus.py
     1459  lens/_count_corpus2.py
     2450  lens/_count_corpus3.py
     1291  lens/_count_corpus4.py
     2015  lens/_count_corpus5.py
    16648  lens/burns.md
     7689  lens/corpus.md
     6020  lens/doors.md
     5602  lens/graph.md
    27522  lens/laws.md
    21578  lens/questions.md
    29091  percolator_candidates.jsonl
    45274  register.jsonl
      218  steal/.mimosa/hook-state/sess_dwf-dwfrun-3cec1e3a-3251-49cc-ac56-f0901c195b4a-actor_5_4.json
     4115  steal/agent-memory-and-continuity.json
    16124  steal/agent-memory-and-continuity.md
    18100  steal/evals-and-self-improvement via reddit.md
    14468  steal/finetuning-and-adaptation via reddit.md
     5081  steal/open-and-local-language-models-arxiv-hf.json
    24852  steal/open-and-local-language-models-arxiv-hf.md
    16240  steal/open-and-local-language-models.md
     5407  steal/quantization-and-compression.json
    22856  steal/quantization-and-compression.md
     7314  steal/swarm-orchestration via arxiv.md
     7416  steal/swarm-orchestration.md
      218  sweep/.mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_3_27.json
      729  sweep/.mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_3_28.json
      177  sweep/.mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_6_1.continue.json
      923  sweep/.mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_6_1.json
     1972  sweep/.mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_6_1.muspgis1-48464-8570242da5.baseline/27b1afef71f470bfd9060201f87bcff44aa55f4e47532ae58e5b4cbf0436687a.source
     1985  sweep/.mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_6_1.muspgis1-48464-8570242da5.baseline/c74aa2ab897e45f4dca4ed742ca9b2dfe161c0dc16f1d62fdd457921627f5a85.source
     1241  sweep/.mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_6_1.muspgis1-48464-8570242da5.baseline/c769d5764422161d4f179fa6f53fa05fbad600cb10b332fb39d7e48aaa3bb80b.source
     1282  sweep/.mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_6_1.muspgis1-48464-8570242da5.baseline/df7158de303a6a8ddf3aabab3f8ee1f2d9434317db31cc9886b3e60a473471db.source
      218  sweep/.mimosa/hook-state/sess_dwf-dwfrun-3cec1e3a-3251-49cc-ac56-f0901c195b4a-actor_3_16.json
      218  sweep/.mimosa/hook-state/sess_dwf-dwfrun-3cec1e3a-3251-49cc-ac56-f0901c195b4a-actor_3_24.json
      880  sweep/.mimosa/hook-state/sess_dwf-dwfrun-3cec1e3a-3251-49cc-ac56-f0901c195b4a-actor_3_5.json
      218  sweep/.mimosa/hook-state/sess_dwf-dwfrun-3cec1e3a-3251-49cc-ac56-f0901c195b4a-actor_3_7.json
      411  sweep/.mimosa/hook-status/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_3_27-392cbc3656.json
      407  sweep/.mimosa/hook-status/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_3_28-6e6129f6de.json
      428  sweep/.mimosa/hook-status/sess_dwf-dwfrun-3cec1e3a-3251-49cc-ac56-f0901c195b4a-actor_3_17-683faca7db.json
      404  sweep/.mimosa/hook-status/sess_dwf-dwfrun-3cec1e3a-3251-49cc-ac56-f0901c195b4a-actor_3_5-d28176af18.json
      430  sweep/.mimosa/hook-status/sess_dwf-dwfrun-3cec1e3a-3251-49cc-ac56-f0901c195b4a-actor_3_7-a1952e1965.json
     1282  sweep/_arxiv_deep.py
     1406  sweep/_arxiv_deep_swarm_r2.py
        0  sweep/_arxiv_judge.xml
     1972  sweep/_arxiv_sweep.py
     3459  sweep/_arxiv_sweep_swarm_r2.py
   129620  sweep/_bing1.html
   584526  sweep/_evidence_2610.00905_fulltext.html
     7901  sweep/_frozen_judges.html
     4733  sweep/_fx_2102897972484686221.json
     5148  sweep/_fx_2104478985614704756.json
     4812  sweep/_fx_2104602215440666826.json
     2688  sweep/_fx_cognition.json
     2978  sweep/_fx_markk.json
    23677  sweep/_fx_nateherk.json
    34217  sweep/_fx_waselnuk.json
       47  sweep/_fx_waselnuk_article.json
     1241  sweep/_grep_kv.py
    91467  sweep/_hn49611128.json
     2386  sweep/_q1_sweep.py
     2081  sweep/_q2_sweep.py
     1343  sweep/_q3_fetch.py
      218  sweep/_raw/.mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_3_21.json
      218  sweep/_raw/.mimosa/hook-state/sess_dwf-dwfrun-3cec1e3a-3251-49cc-ac56-f0901c195b4a-actor_3_31.json
      542  sweep/_raw/.mimosa/hook-status/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_3_21-99bfb4de3d.json
      529  sweep/_raw/.mimosa/hook-status/sess_dwf-dwfrun-3cec1e3a-3251-49cc-ac56-f0901c195b4a-actor_3_13-9724a41d15.json
      532  sweep/_raw/.mimosa/hook-status/sess_dwf-dwfrun-3cec1e3a-3251-49cc-ac56-f0901c195b4a-actor_3_31-20293aee78.json
   109002  sweep/_raw/2609.04749_fulltext.txt
    48746  sweep/_raw/2609.10964_fulltext.txt
    78864  sweep/_raw/2609.25959_fulltext.txt
   443078  sweep/_raw/2609.32852v1.html
    82493  sweep/_raw/2609.32852v1.txt
   303306  sweep/_raw/2609.32961v1.html
    84770  sweep/_raw/2609.32961v1.txt
    60521  sweep/_raw/2609.33768_fulltext_r2.txt
   204678  sweep/_raw/2609.34215_fulltext.txt
    49214  sweep/_raw/2609.34701_fulltext.txt
    96260  sweep/_raw/2609.35875_fulltext.txt
    80841  sweep/_raw/2609.38482_fulltext_r2.txt
   537754  sweep/_raw/2609.39068v1.html
   103921  sweep/_raw/2609.39068v1.txt
   330010  sweep/_raw/2609.39329v1.html
    72846  sweep/_raw/2609.39329v1.txt
   290204  sweep/_raw/2610.00349_fulltext.txt
   436288  sweep/_raw/2610.00412v1.html
    69644  sweep/_raw/2610.00412v1.txt
     9353  sweep/_raw/as_1wv05u1.json
       11  sweep/_raw/as_comments_1wkwy6g.json
    28389  sweep/_raw/as_comments_1wmkr01.json
    24557  sweep/_raw/as_comments_1wshwqz.json
    19384  sweep/_raw/as_comments_1wsp4bp.json
    16893  sweep/_raw/as_comments_1wtygav.json
     9773  sweep/_raw/as_comments_1wtzwwn.json
    80301  sweep/_raw/as_comments_1wv05u1.json
       11  sweep/_raw/as_comments_1wv5lbj.json
    25759  sweep/_raw/as_comments_1wvqk0f.json
    49226  sweep/_raw/as_deep_ids.json
   150972  sweep/_raw/as_kw_gemma.json
       54  sweep/_raw/as_kw_groq.json
       54  sweep/_raw/as_kw_ollama_limit.json
    88877  sweep/_raw/as_kw_ratelimit.json
   684361  sweep/_raw/as_list_LocalLLM.json
   509762  sweep/_raw/as_list_LocalLLaMA.json
   418414  sweep/_raw/as_list_MachineLearning.json
   597964  sweep/_raw/as_list_ollama.json
    53377  sweep/_raw/idlist_shortlist.xml
     1194  sweep/_raw/jina_1wk0st3.txt
        9  sweep/_raw/llama_top.json
   189908  sweep/_raw/llama_top_www.json
       38  sweep/_raw/pp1wk0st3.json
      191  sweep/_raw/pp_search.json
       38  sweep/_raw/pp_t3.json
    14644  sweep/_raw/prior_pass_inference-efficiency-reddit.md
    22360  sweep/_raw/q1_candidates.json
    12330  sweep/_raw/q2_candidates.json
   297874  sweep/_raw/q_2609.04098.html
    47298  sweep/_raw/q_2609.04098.txt
   206495  sweep/_raw/q_2609.19441.html
    52640  sweep/_raw/q_2609.19441.txt
   242065  sweep/_raw/q_2609.23587.html
    67877  sweep/_raw/q_2609.23587.txt
    80528  sweep/_raw/q_2609.28007.html
    30858  sweep/_raw/q_2609.28007.txt
   943685  sweep/_raw/q_2609.37887.html
   207060  sweep/_raw/q_2609.37887.txt
   380689  sweep/_raw/q_2609.38166.html
    67981  sweep/_raw/q_2609.38166.txt
   572761  sweep/_raw/q_2609.38169.html
   109638  sweep/_raw/q_2609.38169.txt
   415848  sweep/_raw/q_2609.39801.html
    86412  sweep/_raw/q_2609.39801.txt
    37908  sweep/_raw/swarm_r2_pass1.txt
        0  sweep/_raw/t1wk0st3.json
     4674  sweep/_raw/wb_1wk0st3.html
      218  sweep/_raw2/.mimosa/hook-state/sess_dwf-dwfrun-3cec1e3a-3251-49cc-ac56-f0901c195b4a-actor_3_21.json
   211750  sweep/_raw2/ft_2609.19657.html
    61819  sweep/_raw2/ft_2609.19657.txt
     7899  sweep/_raw2/ft_2609.24991.html
      730  sweep/_raw2/ft_2609.24991.txt
   202060  sweep/_raw2/ft_2609.27354.html
    79885  sweep/_raw2/ft_2609.27354.txt
   280536  sweep/_raw2/ft_2609.27981.html
    58252  sweep/_raw2/ft_2609.27981.txt
   391239  sweep/_raw2/ft_2609.32259.html
    71004  sweep/_raw2/ft_2609.32259.txt
   167576  sweep/_raw2/ft_2609.32283.html
    53561  sweep/_raw2/ft_2609.32283.txt
  1059871  sweep/_raw2/ft_2609.33334.html
   131065  sweep/_raw2/ft_2609.33334.txt
     7899  sweep/_raw2/ft_2609.36289.html
      730  sweep/_raw2/ft_2609.36289.txt
    25686  sweep/_raw2/hn_kv.json
    21369  sweep/_raw2/idlist_2.xml
    90499  sweep/_raw2/list_csCL.html
    88100  sweep/_raw2/list_csLG.html
   104283  sweep/_raw2/q1_kvcache.xml
    74594  sweep/_raw2/q2_prefix.xml
    61719  sweep/_raw2/q3_evict.xml
    17998  sweep/_raw2/q4_ctxeng.xml
    44066  sweep/_raw2/q5_compress.xml
    50194  sweep/_raw2/q6_struct.xml
    54093  sweep/_raw2/q7_agent.xml
     2207  sweep/_syn.html
     1854  sweep/_x2_deep.py
     1623  sweep/_x2_deep2.py
     2126  sweep/_x2_sweep.py
     7894  sweep/_x_abs_batch.xml
     4427  sweep/_x_abs_batch2.xml
     5879  sweep/_x_abs_batch3.xml
     2660  sweep/_x_abs_cachewise.xml
     2731  sweep/_x_abs_govdecay.xml
    14014  sweep/_x_ace.xml
    63447  sweep/_x_owed_arxiv_q1.xml
    62394  sweep/_x_owed_hn_q1.json
    54261  sweep/_x_q3_recent.xml
    21940  sweep/agent-memory-and-continuity-arxiv.md
    15259  sweep/agent-memory-and-continuity-hn.md
    32114  sweep/agent-memory-and-continuity-reddit.md
    18196  sweep/agent-memory-and-continuity-x.md
  1623827  sweep/arctic_LocalLLM.json
  1848115  sweep/arctic_LocalLLaMA.json
   669169  sweep/arctic_MachineLearning.json
      601  sweep/arctic_comment.py
     1334  sweep/arctic_grep.ps1
     1046  sweep/arctic_grep2.ps1
   619006  sweep/arctic_ollama.json
     1294  sweep/arctic_read.py
     2455  sweep/arctic_sweep.ps1
     1569  sweep/arctic_sweep.py
     2219  sweep/arctic_sweep2.py
     2828  sweep/ddg_sweep.ps1
     2361  sweep/deep_read.ps1
     2041  sweep/deep_read_evals.ps1
    18291  sweep/evals-and-self-improvement-arxiv.md
    24931  sweep/evals-and-self-improvement-hn.md
    25069  sweep/evals-and-self-improvement-reddit.md
    21603  sweep/evals-and-self-improvement-x.md
     1767  sweep/fetch_extra.ps1
     1354  sweep/fetch_reddit.ps1
      628  sweep/find_kvarn.ps1
      330  sweep/find_phantom.ps1
    52555  sweep/finetuning-and-adaptation-arxiv.md
    23561  sweep/finetuning-and-adaptation-hn.md
    24235  sweep/finetuning-and-adaptation-reddit.md
    28586  sweep/finetuning-and-adaptation-x.md
      314  sweep/grep_laws.ps1
    13530  sweep/inference-efficiency-arxiv.md
    25371  sweep/inference-efficiency-hn.md
    20268  sweep/inference-efficiency-reddit.md
    12943  sweep/inference-efficiency-x.md
    20012  sweep/kv-cache-and-context-engineering-arxiv.md
    29014  sweep/kv-cache-and-context-engineering-hn.md
    30634  sweep/kv-cache-and-context-engineering-reddit.md
    19384  sweep/kv-cache-and-context-engineering-x.md
        0  sweep/llama_top.json
    18525  sweep/open-and-local-language-models-arxiv.md
    24174  sweep/open-and-local-language-models-hn.md
    39282  sweep/open-and-local-language-models-reddit.md
    16815  sweep/open-and-local-language-models-x.md
    21172  sweep/open-and-local-language-models-x.round2.md
     2621  sweep/overlap_grep.ps1
     1699  sweep/print_threads.ps1
     1261  sweep/probe_doors.ps1
     1379  sweep/probe_doors2.ps1
    12794  sweep/quantization-and-compression-arxiv.md
    34342  sweep/quantization-and-compression-hn.md
    33184  sweep/quantization-and-compression-reddit.md
    15338  sweep/quantization-and-compression-x.md
    10652  sweep/quantization-and-compression-x.pass0.md
   324208  sweep/rss_LocalLLM.xml
   324401  sweep/rss_LocalLLaMA.xml
   324729  sweep/rss_MachineLearning.xml
   324734  sweep/rss_ollama.xml
    20074  sweep/swarm-orchestration-arxiv.md
    16729  sweep/swarm-orchestration-hn.md
    35621  sweep/swarm-orchestration-reddit.md
    31487  sweep/swarm-orchestration-x.md
     8518  sweep/thread_1w9llr4.json
    19667  sweep/thread_1w9myqc.json
   112274  sweep/thread_1wc6tka.json
    75849  sweep/thread_1wdasar.json
     5524  sweep/thread_1wdc1jj.json
    40919  sweep/thread_1wloz92.json
   267902  sweep/thread_1wms904.json
    86583  sweep/thread_1wnedrc.json
   157618  sweep/thread_1wp5668.json
      605  sweep/thread_1wpodl1.json
   491293  sweep/thread_1wr5ylm.json
   448133  sweep/thread_1wsq0pa.json
   466380  sweep/thread_1wsuag0.json
   140775  sweep/thread_1wt03zh.json
     5198  sweep/thread_1wu1ugy.json
    11746  sweep/thread_1wu6reb.json
   171070  sweep/thread_1wv05u1.json
    84124  sweep/thread_1wv09ja.json
      588  sweep/thread_1wv0b24.json
   502073  sweep/thread_1wv1u54.json
      640  sweep/thread_1wvwdn1.json
     1381  sweep/tmp/.mimosa/finding-ledger/v1/events/batch-pretooluse-a37136a9fa4c5726c4471e64708c91d7.json
     1160  sweep/tmp/.mimosa/hook-state/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_3_15.json
      218  sweep/tmp/.mimosa/hook-state/sess_dwf-dwfrun-3cec1e3a-3251-49cc-ac56-f0901c195b4a-actor_3_15.json
      733  sweep/tmp/.mimosa/hook-state/sess_dwf-dwfrun-3cec1e3a-3251-49cc-ac56-f0901c195b4a-actor_3_19.json
      218  sweep/tmp/.mimosa/hook-state/sess_dwf-dwfrun-3cec1e3a-3251-49cc-ac56-f0901c195b4a-actor_6_2.json
      970  sweep/tmp/.mimosa/hook-status/sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_3_15-638ae0bd8b.json
      530  sweep/tmp/.mimosa/hook-status/sess_dwf-dwfrun-3cec1e3a-3251-49cc-ac56-f0901c195b4a-actor_3_15-fcf6dae2fd.json
      408  sweep/tmp/.mimosa/hook-status/sess_dwf-dwfrun-3cec1e3a-3251-49cc-ac56-f0901c195b4a-actor_3_19-2a140ca4b7.json
     1985  sweep/tmp/as_sweep.py
     6456  sweep/tmp/as_test.json
    35127  sweep/tmp/batch1.json
  1102933  sweep/tmp/candidates.jsonl
  9996693  sweep/tmp/candidates_full.jsonl
    25028  sweep/tmp/coldread_fix.py
    20950  sweep/tmp/comments_1w67g8k.json
     6273  sweep/tmp/comments_1w6gg8v.json
    17692  sweep/tmp/comments_1w950fw.json
    13220  sweep/tmp/comments_1wb35xo.json
    32537  sweep/tmp/comments_1wbc03f.json
    25554  sweep/tmp/comments_1wbifl0.json
     6034  sweep/tmp/comments_1wg442g.json
     8300  sweep/tmp/comments_1wmafge.json
     4577  sweep/tmp/comments_test.json
    15697  sweep/tmp/evening_appendix.md
    70377  sweep/tmp/fold2_build.py
     2548  sweep/tmp/fold2_inventory.py
    22009  sweep/tmp/fold2_inventory_current.txt
    11656  sweep/tmp/fold2_receipt.py
     5351  sweep/tmp/fold2_receipt_fix.py
     9267  sweep/tmp/fold2_receipt_fix2.py
   188829  sweep/tmp/ft_deepread.json
     3095  sweep/tmp/ft_deepread.py
   779951  sweep/tmp/ft_hits.jsonl
     1491  sweep/tmp/ft_overlap.py
     3516  sweep/tmp/ft_rank.py
      813  sweep/tmp/hnolm/featherless_headers.txt
    34891  sweep/tmp/hnolm/featherless_roster_100.json
    25253  sweep/tmp/hnolm/featherless_roster_page1.json
    25280  sweep/tmp/hnolm/p1_27b.json
    53540  sweep/tmp/hnolm/p1_agentic.json
    26264  sweep/tmp/hnolm/p1_cerebras.json
     1229  sweep/tmp/hnolm/p1_chutes.json
    33951  sweep/tmp/hnolm/p1_deepseek.json
     1997  sweep/tmp/hnolm/p1_featherless.json
   117285  sweep/tmp/hnolm/p1_freellmapi.json
    78814  sweep/tmp/hnolm/p1_freetier.json
    46659  sweep/tmp/hnolm/p1_gemma.json
    40176  sweep/tmp/hnolm/p1_gguf.json
    60103  sweep/tmp/hnolm/p1_glm.json
    35591  sweep/tmp/hnolm/p1_kimi.json
    34831  sweep/tmp/hnolm/p1_llamacpp.json
    54353  sweep/tmp/hnolm/p1_localllm.json
    29012  sweep/tmp/hnolm/p1_minimax.json
    41440  sweep/tmp/hnolm/p1_mistral.json
    41755  sweep/tmp/hnolm/p1_ollama.json
    48424  sweep/tmp/hnolm/p1_openw.json
    93377  sweep/tmp/hnolm/p1_osllm.json
    26974  sweep/tmp/hnolm/p1_quant.json
    36907  sweep/tmp/hnolm/p1_qwen.json
    54453  sweep/tmp/hnolm/p1_ratelimit.json
      460  sweep/tmp/hnolm/p1_siliconflow.json
    78480  sweep/tmp/hnolm/p1_slm.json
   106311  sweep/tmp/hnolm/p1_toolcall.json
    19365  sweep/tmp/hnolm/p1_vllm.json
    13293  sweep/tmp/hnolm/prior_pass_hn_backup.md
    11124  sweep/tmp/hnolm/stealr1_arxiv4.xml
     8979  sweep/tmp/hnolm/stealr1_minicpm5.json
    37264  sweep/tmp/hnolm/stealr1_ollama351.json
      932  sweep/tmp/kg_reconcile.json
        0  sweep/tmp/llama_top.json
     6855  sweep/tmp/ollama_adapter_comments.json
      263  sweep/tmp/post_1w950fw.json
    19294  sweep/tmp/ranked_ids.json
     5189  sweep/tmp/receipt_refresh.py
       54  sweep/tmp/search_cc_agent.json
     4404  sweep/tmp/sw2_crawl.py
 22738168  sweep/tmp/sw2_full.jsonl
    27388  sweep/tmp/sw2_item_1woj7dv.json
    31182  sweep/tmp/sw2_item_1wpxh2g.json
    30341  sweep/tmp/sw2_item_1wqnjkp.json
    10268  sweep/tmp/sw2_item_1wt0tot.json
    17439  sweep/tmp/sw2_item_1wtmhgw.json
    49162  sweep/tmp/sw2_item_1wui0hj.json
     3278  sweep/tmp/sw2_item_1wv66mt.json
    59232  sweep/tmp/sw2_item_1wvpffv.json
     2519  sweep/tmp/sw2_read.py
     5802  sweep/tmp/x_evening/alex.json
    41872  sweep/tmp/x_evening/arxiv_2509.05396.html
     6909  sweep/tmp/x_evening/avichawla.json
     2425  sweep/tmp/x_evening/emollick.json
    19277  sweep/tmp/x_evening/file_air.html
    15689  sweep/tmp/x_evening/file_feed.xml
    10159  sweep/tmp/x_evening/file_hn.html
     5327  sweep/tmp/x_evening/file_links.html
     9182  sweep/tmp/x_evening/file_root.html
    10569  sweep/tmp/x_evening/file_safety.html
     7893  sweep/tmp/x_evening/harper.json
   881419  sweep/tmp/x_evening/kg_blog.html
   111867  sweep/tmp/x_evening/kg_root.html
   429709  sweep/tmp/x_evening/kg_swarm.html
   231473  sweep/tmp/x_evening/kilo.html
   230828  sweep/tmp/x_evening/kilo_archive.html
   155983  sweep/tmp/x_evening/kilo_swarm.html
   153663  sweep/tmp/x_evening/kilo_swarm_orig.html
    14031  sweep/tmp/x_evening/lenny.json
    10251  sweep/tmp/x_evening/levie.json
   147115  sweep/tmp/x_evening/lw_swarm.html
    42370  sweep/tmp/x_evening/mweinbach.json
    54746  sweep/tmp/x_evening/parallelcode.html
    34578  sweep/tmp/x_evening/pc_429.html
    70670  sweep/tmp/x_evening/pc_blog.html
     4218  sweep/tmp/x_evening/rohan.json
     3531  sweep/tmp/x_evening/thezvi.json
   151935  sweep/tmp/x_evening/tianpan.html
   246893  sweep/tmp/x_evening/tianpan_consensus.html
  2204929  sweep/tmp/x_evening/tianpan_sitemap.xml
    30534  sweep/tmp/x_evening/walden.json
TOTAL files=393 bytes=67438916
```
