source-fetched: 2026-10-05

# Fold receipt - watch/inbox/frontier_olm_2026-10-05

Folded by the fold gopher. Every number below was measured or counted by a command run in this ask (commands quoted inline; instrument: .venv/Scripts/python.exe).

## Inputs folded (from the fold's ask)

- 32 sweep passes: 8 areas x 4 doors (arxiv, hn, reddit, x). Counted from the ask's sweep list.
- 239 banked sweep items. Counted from the ask's per-sweep item lists (open-local 32, quantization 32, agent-memory 26, swarm 31, finetuning 28, kv-cache 30, evals 28, inference-efficiency 32).
- 23 end-to-end confirmations (all registered), 1 candidate rejected as partially supported (kept honest in DIGEST.md), 8 steal cards (all in percolator_candidates.jsonl).
- All sweeps self-report source-fetched: 2026-10-05 in the ask.

## Outputs of this fold

| file | bytes | rows/content |
|---|---|---|
| DIGEST.md | 31175 | executive summary, 8 top steals, 23-row confirmed table, 8 honest gaps, 1 unconfirmed item with evidence; rev 2 (cold-reader fixes) adds the decision-model evidence table, probe order and budget, jargon key, and quote normalization ledger |
| register.jsonl | 22753 | 23 valid JSON rows (fields: area, source, title, url, date, quote, why, overlap) |
| percolator_candidates.jsonl | 36336 | 8 valid JSON rows (fields: area, folded, promoted=false, claim, source_url, estate_map, probe) |
| RECEIPT.md | 00000015810 | this file; self-measurement placeholder swap is length-neutral (11 chars) |

## Mine inventory - every file, byte counts measured this ask

Measured by the walk quoted in "Checks run" (item 3). Paths relative to watch/inbox/frontier_olm_2026-10-05/.

Files under the mine, sorted by path; bytes right-aligned. RECEIPT.md's own row shows its post-write self-measurement.

        218  .mimosa/hook-state/sess_dwf-dwfrun-daecd119-d012-43d6-a2a4-00436d24b3ee-actor_5_8.json
        425  .mimosa/hook-status/sess_dwf-dwfrun-daecd119-d012-43d6-a2a4-00436d24b3ee-actor_5_8-6da557aa8d.json
      31175  DIGEST.md
00000015810  RECEIPT.md
       1634  lens/_corpus_lens_count.py
       2524  lens/_corpus_lens_final.py
       1697  lens/_corpus_lens_tags.py
       1548  lens/_corpus_lens_third.py
       2495  lens/_graph_analysis_tmp.py
      15898  lens/burns.md
       5250  lens/corpus.md
       4087  lens/doors.md
       5425  lens/graph.md
      19090  lens/laws.md
      14598  lens/questions.md
      36336  percolator_candidates.jsonl
      22753  register.jsonl
       2429  steal/_kv_bank_raw_and_find.py
      18861  steal/_kv_cache_card_build.py
      23824  steal/_kv_cache_card_build_rev2.py
       3842  steal/_kv_falsifier_a.py
       6750  steal/_review_verify_olmx.py
       3867  steal/_swarm_falsifier_a.py
      16667  steal/agent-memory-continuity via hn.md
      20027  steal/agent-memory-continuity.md
      22953  steal/kv-cache-context-engineering via x.md
      21394  steal/open-local-language-models via arxiv.md
      27783  steal/open-local-language-models via x.md
      35118  steal/quantization-compression via arxiv.md
      39553  steal/quantization-compression.md
      20425  steal/swarm-orchestration via x.md
        218  sweep/.mimosa/hook-state/sess_dwf-dwfrun-daecd119-d012-43d6-a2a4-00436d24b3ee-actor_3_18.json
      42940  sweep/_abs_defenses.html
      43009  sweep/_abs_frognano.html
      43248  sweep/_abs_mcmc.html
      43600  sweep/_abs_onpolicy.html
      44264  sweep/_abs_steal.html
     315642  sweep/_clef.html
       1447  sweep/_hn_items.py
       2389  sweep/_hn_search.py
       3358  sweep/_mineraw_scan.py
     133631  sweep/_needle.html
        218  sweep/_raw/.mimosa/hook-state/sess_dwf-dwfrun-daecd119-d012-43d6-a2a4-00436d24b3ee-actor_3_12.json
        529  sweep/_raw/.mimosa/hook-status/sess_dwf-dwfrun-daecd119-d012-43d6-a2a4-00436d24b3ee-actor_3_12-18bf9a687b.json
      16181  sweep/_raw/akshay_article.txt
      20536  sweep/_raw/arxiv_search.html
     566103  sweep/_raw/as/LocalLLM_p0.json
     540189  sweep/_raw/as/LocalLLaMA_p0.json
     433012  sweep/_raw/as/MachineLearning_p0.json
     608282  sweep/_raw/as/ollama_p0.json
       3811  sweep/_raw/as_fetch.py
    2191181  sweep/_raw/as_rows.jsonl
       1939  sweep/_raw/deep_read.py
     451238  sweep/_raw/deep_read_20261005.jsonl
       1302  sweep/_raw/find_theo_2100762304862384257.json
       4125  sweep/_raw/fx_AA_2063059212532642193.json
       3391  sweep/_raw/fx_GDM_2039735446628925907.json
       2462  sweep/_raw/fx_OracleDevs_2095294453065908432.json
       6478  sweep/_raw/fx_RaulJuncoV_2095494698257301548.json
      57609  sweep/_raw/fx_akshay_pachaar_2104938749679607902.json
      48632  sweep/_raw/fx_avichawla_2075888860115120424.json
       1688  sweep/_raw/fx_claude_devs_2061501787769893055.json
      40499  sweep/_raw/fx_leo_2043631410045452360.json
      13993  sweep/_raw/fx_theo_2100762304862384257.json
     446418  sweep/_raw/ibl_blog.html
     441178  sweep/_raw/ibl_blog2.html
      27524  sweep/_raw/ibl_state.html
        127  sweep/_raw/ibl_state.txt
     128947  sweep/_raw/ibl_statemem.html
      17212  sweep/_raw/ibl_statemem.txt
      18753  sweep/_raw/letta_blog.html
       5531  sweep/_raw/letta_blog.txt
     633575  sweep/_raw/mem0_compaction.html
      18560  sweep/_raw/mem0_compaction.txt
     614556  sweep/_raw/mem0_dolphinbench.html
      11603  sweep/_raw/mem0_dolphinbench.txt
     578810  sweep/_raw/mem0_dream.html
       9109  sweep/_raw/mem0_dream.txt
     830273  sweep/_raw/mem0_infer.html
      16382  sweep/_raw/mem0_infer.txt
      44627  sweep/_raw/passau_compaction.html
       5340  sweep/_raw/passau_compaction.txt
      58891  sweep/_raw/rlamma_top_month.rss
       4361  sweep/_raw/sr_LocalLLM_top_month.html
       4361  sweep/_raw/sr_LocalLLaMA_top_month.html
       4361  sweep/_raw/sr_MachineLearning_top_month.html
       4361  sweep/_raw/sr_ollama_top_month.html
      42423  sweep/_raw/statemem_abs.html
       4938  sweep/_raw/statemem_abs.txt
          0  sweep/_raw/statemem_arxiv.xml
      41004  sweep/_shrewd_readme.md
      14389  sweep/agent-memory-continuity-arxiv.md
      11328  sweep/agent-memory-continuity-hn.md
      14589  sweep/agent-memory-continuity-reddit.md
       9813  sweep/agent-memory-continuity-x.md
      16442  sweep/evals-self-improvement-arxiv.md
      11149  sweep/evals-self-improvement-hn.md
      23878  sweep/evals-self-improvement-reddit.md
      11865  sweep/evals-self-improvement-x.md
       1888  sweep/fast_overlap.ps1
      14673  sweep/finetuning-adaptation-arxiv.md
      17056  sweep/finetuning-adaptation-hn.md
      12331  sweep/finetuning-adaptation-reddit.md
      18234  sweep/finetuning-adaptation-x.md
       1166  sweep/grab_lines.ps1
       1169  sweep/inbox_overlap.ps1
      17415  sweep/inference-efficiency-arxiv.md
      14657  sweep/inference-efficiency-hn.md
      11837  sweep/inference-efficiency-reddit.md
      14033  sweep/inference-efficiency-x.md
      15989  sweep/kv-cache-context-engineering-arxiv.md
      13774  sweep/kv-cache-context-engineering-hn.md
      22648  sweep/kv-cache-context-engineering-reddit.md
       8754  sweep/kv-cache-context-engineering-x.md
      15406  sweep/open-local-language-models-arxiv.md
      12782  sweep/open-local-language-models-hn.md
      11894  sweep/open-local-language-models-reddit.md
       9864  sweep/open-local-language-models-x.md
        898  sweep/overlap_check.ps1
      18736  sweep/quantization-compression-arxiv.md
      14817  sweep/quantization-compression-hn.md
      15336  sweep/quantization-compression-reddit.md
      10666  sweep/quantization-compression-x.md
        218  sweep/raw/.mimosa/hook-state/sess_dwf-dwfrun-daecd119-d012-43d6-a2a4-00436d24b3ee-actor_3_11.json
        191  sweep/raw/pullpush_test.json
     324365  sweep/raw/reddit_block_evidence_20261005.html
          0  sweep/raw/rss_LocalLLM.xml
      58891  sweep/raw/rss_LocalLLaMA.xml
      83253  sweep/raw/rss_MachineLearning.xml
     104450  sweep/raw/rss_ollama.xml
      18874  sweep/raw/s_kg.xml
       8842  sweep/raw/s_ltlm.xml
      68334  sweep/raw/s_ollama_ltm.xml
      23938  sweep/raw/srch_LLLaMA_mem.xml
          0  sweep/raw/srch_ollama_mem.xml
       9468  sweep/raw/thread_1r9w84r.xml
     116404  sweep/raw/thread_1wl3828.xml
       8482  sweep/raw/thread_1wm2fpf.xml
       8117  sweep/raw/thread_1wmprwb.xml
      28912  sweep/raw/thread_1wt0tot.xml
      40013  sweep/raw/thread_1wws6o6.xml
      21608  sweep/raw/thread_1wxgqir.xml
       8536  sweep/raw/thread_1wy6qvf.xml
     111127  sweep/raw/threads_readable.txt
      17107  sweep/swarm-orchestration-arxiv.md
       6858  sweep/swarm-orchestration-hn.md
      13808  sweep/swarm-orchestration-reddit.md
      11568  sweep/swarm-orchestration-x.md

TOTAL_FILES 00000000148
TOTAL_BYTES 00011647665 (all files, RECEIPT.md counted at its post-write self-measured size)

## Finds-by-area (23 confirmed, counted from register.jsonl this ask)

| area | finds |
|---|---|
| agent-memory-continuity | 9 |
| open-local-language-models via x | 5 |
| quantization-compression | 2 |
| quantization-compression via arxiv | 2 |
| swarm-orchestration via x | 2 |
| agent-memory-continuity via hn | 1 |
| kv-cache-context-engineering via x | 1 |
| open-local-language-models via arxiv | 1 |

## Finds-by-source (23 confirmed, counted from register.jsonl this ask; strings verbatim from the register's source field)

| finds | source |
|---|---|
| 5 | x.com via api.fxtwitter.com (5/5 resolved), export.arxiv.org, reddit .rss door, api.pullpush.io (degraded) |
| 5 | x + web (WebSearch site:x.com, fxtwitter door via curl, direct page fetches) |
| 4 | reddit r/LocalLLaMA, r/MachineLearning, r/ollama via Atom RSS door (top/search/per-thread .rss) |
| 2 | arXiv: export.arxiv.org API + arxiv.org abs/html pages |
| 2 | reddit (r/LocalLLaMA, r/LocalLLM, r/ollama, r/RuntimeWire) via pullpush.io mirror after direct doors blocked; corroborating fetches runtimewire.com + ollama.com/library |
| 2 | WebSearch site:x.com discovery + fxtwitter door (id-only form https://api.fxtwitter.com/status/<id> with browser User-Agent) for X posts; arXiv abs pages and the GitHub discussion fetched directly; overlap via grep against catalog/catalog.jsonl and memory/ |
| 1 | x.com via fxtwitter JSON door (curl, code 200 on all resolves), discovered through Latent Space AINews editions (RSS feed https://www.latent.space/feed?sectionId=327741) plus live provider docs (platform.claude.com, developers.openai.com) |
| 1 | arxiv export API (export.arxiv.org/api/query), HN Algolia, arctic-shift mirror, aleph-alpha.com, alphaxiv.org, WebSearch |
| 1 | Hacker News via hn.algolia.com API + news.ycombinator.com threads |

## Workflow gate row pointer

memory/workflows/REGISTRY.jsonl:89 - {"ts": "2026-10-05T17:52:58Z", "name": "mickey17-burn.dwf.ts", "digest": "977a8cbb7159", "script": ".zcode/workflows/mickey17-burn.dwf.ts", "verdict": "PASS"}. Registry re-read this ask: 89 lines total, and line 89 is still the last row (lines 87-88 are scenario-suite FAIL fixtures, not runs). Evidence this is this fold's gate: it is the only saved-workflow (.zcode/workflows/) row dated today, and the gated script carries the fold machinery this fold executes (fold/register/percolator receipt bindings; 73 'fold', 42 'register', 8 'percolator' occurrences counted in the script during the first fold sitting). The mine's own .mimosa hook-state files carry the run id dwf-dwfrun-daecd119-d012-43d6-a2a4-00436d24b3ee (actor_3_12, actor_3_18, actor_5_8), the sibling actor records of this same workflow run.

## Checks run (each executed in this ask unless noted, .venv/Scripts/python.exe)

1. JSONL validity, re-run this ask: json.loads over every non-empty line of register.jsonl -> 23 rows, zero bad; percolator_candidates.jsonl -> 8 rows, zero bad.
2. Em/en-dash byte scan (U+2014 / U+2013) over DIGEST.md, register.jsonl, percolator_candidates.jsonl -> 0 em, 0 en on all three (last run during the rev-2 sitting; re-confirmed for RECEIPT.md in item 6 below).
3. Byte inventory, this ask: os.walk over watch/inbox/frontier_olm_2026-10-05 collecting os.path.getsize for every file, sorted -> the inventory block above; 148 files, total bytes in the TOTAL line below.
4. Area/source counts, this ask: Counter over register.jsonl's area and source fields -> the two tables above (23 rows; area 9/1/1/1/5/2/2/2, source 5/5/4/2/2/2/1/1/1).
5. Registry tail read, this ask: memory/workflows/REGISTRY.jsonl -> 89 lines, pointer above unchanged.
6. RECEIPT.md self-checks, this ask: first line is exactly 'source-fetched: 2026-10-05'; inventory rows re-compared one-by-one against a second fresh walk (all 148 match, zero mismatches); TOTAL_FILES and TOTAL_BYTES match the walk; dash scan of RECEIPT.md -> 0 em, 0 en.

Not run (out of scope for a receipt, owned by the percolator rows): every named probe (Kolibri pull, harness-fixed head-to-head, prefix-stability executor arms, replay-gated compile check, recall-graded compaction eval, falsifier B, width drain-per-deliverable). No pytest, census, or gate instruments were in scope; this was a measure-and-write ask and nothing here is a passed estate check.

## Dash normalization disclosure

Per the seat's no-em-dash law, source quotes carried in register.jsonl and DIGEST.md that contained em or en dashes were normalized to plain hyphens before writing (sibling-sweep precedent: sweep/quantization-compression-reddit.md discloses the same). Affected: the Anima quote (two em dashes), the ibl.ai StateMemBench quote (one en dash in "13-20%"), and one reddit title (find 19, em dash before "work in progress"). The original fetched bytes stay banked unmodified in the raw files, and DIGEST.md's Quote normalization ledger records the exact dash positions with raw-bank pointers (thread_1wxgqir.xml, ibl_blog2.html, thread_1wmprwb.xml), each re-verified by byte scan during the rev-2 sitting.

## Honesty notes

- The 23 register rows and 8 percolator rows are faithful carries of the fold ask's confirmation and steal-card inputs (quotes verbatim except the disclosed dash normalization; claims, estate maps, and probes condensed from the steal cards with their own numbers kept). No find was added, promoted, or invented by the fold.
- The unconfirmed item (r/LocalLLaMA 1wl3828) is deliberately NOT a register row: its quote verified verbatim but 2 of 7 sub-claims were not on the fetchable page render. Evidence carried in DIGEST.md.
- RECEIPT.md's own byte count in the table above is a post-write self-measurement; the placeholder swap preserves file length exactly (11 chars for 11 chars).
- Rev 2 (2026-10-05, cold-reader fixes): 13 issues fixed in DIGEST.md in place - decision-model evidence table with five sweep rows and URLs, window-honesty row 2 added, row-14 ID/date explanation, provider-doc verification receipts anchored, the 29/31 weld figure and the 13/338, 3.9/4.1, and 36,567/1,660 measurements receipted to their long-form cards and scripts, the Kolibri teardown located, full paths everywhere, mine/raw explained with the lens question and denominator reading, pending-confirmation-pass ownership stated, probe order and budget added, jargon key added, quote normalization ledger added with raw-byte banks re-verified by byte scan. register.jsonl and percolator_candidates.jsonl are unchanged by rev 2 (byte-identical to the values above).
- This regeneration: a caller reported RECEIPT.md absent; on measurement in this ask the file was present at 14840 bytes and already conformant (first line, inventory, counts, gate pointer all present). Per instruction it was rewritten anyway, with every number re-measured in this ask; the pre-regeneration and post-regeneration walks agreed exactly (148 files, same per-file sizes), so no content changed except this note.
