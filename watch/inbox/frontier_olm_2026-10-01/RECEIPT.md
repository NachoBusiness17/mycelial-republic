source-fetched: 2026-10-01

Receipt for the fold of the frontier mine (the-gala run) into DIGEST.md, register.jsonl, and percolator_candidates.jsonl. All byte counts below were measured by this fold with `find <folder> -type f -printf '%s %p\n'` (measured repeatedly across the fold and its cold-reader fix pass; the numbers here are from the final measure).

## Files and byte counts (measured)

Root (5 files):

| File | Bytes |
|---|---|
| DIGEST.md | 34,328 (grown from 26,581 in the cold-reader fix pass) |
| RECEIPT.md | 0008084 (self-measure: value substituted from the measurement of this exact file state, same digit width as this placeholder so the count stays true) |
| arxiv_deepread.xml | 21,034 |
| register.jsonl | 24,955 |
| percolator_candidates.jsonl | 23,260 |

Root `.mimosa/` (7 files at the final measure, all written by the harness during the fold and its cold-reader fix pass, not by the fold; harness-live, sizes drift): finding-ledger/v1/events/batch-stop-20261001T193630258Z-22840-148652c94742.json 1,690 | history/run-20261001T193630258Z-22840-148652c94742.json 1,232 | hook-state/sess_dwf-dwfrun-22ad421a-8ea0-4e1a-9045-e7956ed55914-actor_7_1.json 448 | hook-state/sess_dwf-dwfrun-22ad421a-8ea0-4e1a-9045-e7956ed55914-actor_7_1.continue.json 177 | hook-status/sess_dwf-dwfrun-22ad421a-8ea0-4e1a-9045-e7956ed55914-actor_7_1-9123fa9a71.json 400 | reports/task-review-sess_dwf-dwfrun-22ad421a-8ea0-4e1a-9045-e7956ed55914-actor_7_1.json 4,398 | reports/task-review-sess_dwf-dwfrun-22ad421a-8ea0-4e1a-9045-e7956ed55914-actor_7_1-20261001T193630258Z-22840-148652c94742.json 4,398

lens/ (6 files): burns.md 6,869 | corpus.md 3,315 | doors.md 3,774 | graph.md 6,548 | laws.md 18,061 | questions.md 15,689

steal/ (5 files): kv-cache-context-engineering.md 18,645 | "open-local-language-models via reddit.md" 15,186 | "open-local-language-models via x.md" 21,841 | open-local-language-models.md 16,632 | quantization-compression.md 15,590

sweep/ (55 files):

- .mimosa/ (2 harness hook files): hook-state/sess_dwf-dwfrun-22ad421a-8ea0-4e1a-9045-e7956ed55914-actor_3_32.json 218 | hook-status/sess_dwf-dwfrun-22ad421a-8ea0-4e1a-9045-e7956ed55914-actor_3_32-dd16dc462c.json 470
- _fx/ (18 fxtwitter fetch receipts): 0x0SojalSec_status_2090922730376069244.json 3,081 | BrandonMusicKy_2102950326487703652.json 34 | BrandonMusicKy_status_2102950326487703652.json 19,895 | Mayhem4Markets_2098094324437184575.json 34 | Mayhem4Markets_status_2082487427138994230.json 26,355 | Mayhem4Markets_status_2098094324437184575.json 2,376 | Oluwaphilemon1_status_2092421623118709048.json 12,558 | TeksEdge_status_2096657401919557887.json 8,147 | TeksEdge_status_2097005540115386703.json 4,264 | TeksEdge_status_2100630867097899078.json 4,525 | _avichawla_article_2096491130489872479.json 34 | _avichawla_status.json 96,038 | _iosg_modelfusion_raw.json 39,270 | _jev_article_raw.json 27,000 | outsource__status_2088743329760469374.json 16,023 | superalesha_2096976602127044995.json 34 | superalesha_status_2090318708283502972.json 2,998 | superalesha_status_2096976602127044995.json 43,771
- Lane write-ups and arXiv XML (35 files): agent-memory-continuity-arxiv.md 15,247 | agent-memory-continuity-hn.md 15,109 | agent-memory-continuity-reddit.md 13,355 | agent-memory-continuity-x.md 18,031 | arxiv_deepread.xml 21,034 | arxiv_deepread2.xml 5,427 | arxiv_deepread3.xml 8,416 | evals-self-improvement-arxiv.md 17,553 | evals-self-improvement-hn.md 13,137 | evals-self-improvement-reddit.md 30,788 | evals-self-improvement-x.md 12,855 | finetuning-adaptation-arxiv.md 9,236 | finetuning-adaptation-hn.md 9,433 | finetuning-adaptation-reddit.md 18,438 | finetuning-adaptation-x.md 13,002 | inference-efficiency-arxiv.md 9,606 | inference-efficiency-hn.md 14,484 | inference-efficiency-reddit.md 9,961 | inference-efficiency-x.md 13,877 | kv-cache-context-engineering-arxiv.md 26,295 | kv-cache-context-engineering-hn.md 16,822 | kv-cache-context-engineering-reddit.md 20,114 | kv-cache-context-engineering-x.md 12,035 | open-local-language-models-arxiv.md 23,668 | open-local-language-models-hn.md 10,685 | open-local-language-models-reddit.md 13,052 | open-local-language-models-x.md 18,983 | quantization-compression-arxiv.md 18,582 | quantization-compression-hn.md 14,299 | quantization-compression-reddit.md 14,318 | quantization-compression-x.md 8,392 | swarm-orchestration-arxiv.md 16,663 | swarm-orchestration-hn.md 9,854 | swarm-orchestration-reddit.md 19,797 | swarm-orchestration-x.md 16,309

Totals: content files (all listed above except RECEIPT.md and the root `.mimosa/` hook tree): 70 files, 1,081,709 bytes measured; the only content file that ever changed between passes was DIGEST.md, rewritten in the cold-reader fix pass (26,581 -> 34,328). Adding the 7 root hook files (12,743 bytes at the final measure) and RECEIPT.md (self-entry above): the folder held 78 files, 1102536 bytes at the final measure. The `.mimosa/` tree is harness-live, so hook-file sizes and presence drift after each measure; the 70 content files are stable. The root arxiv_deepread.xml and sweep/arxiv_deepread.xml are both 21,034 bytes (size match observed; contents not diffed by this fold).

## Finds by area (banked items across the 32 sweep lanes, counted by this fold from the run's sweep payloads; each lane's write-up file is on disk above)

| Area | arxiv | hn | reddit | x | Total |
|---|---|---|---|---|---|
| open-local-language-models | 8 | 8 | 7 | 8 | 31 |
| quantization-compression | 8 | 7 | 8 | 8 | 31 |
| agent-memory-continuity | 8 | 8 | 5 | 8 | 29 |
| swarm-orchestration | 8 | 8 | 8 | 6 | 30 |
| finetuning-adaptation | 8 | 8 | 8 | 8 | 32 |
| kv-cache-context-engineering | 7 | 8 | 8 | 7 | 30 |
| evals-self-improvement | 8 | 7 | 6 | 8 | 29 |
| inference-efficiency | 8 | 8 | 8 | 8 | 32 |
| **Total** | **63** | **62** | **58** | **61** | **244** |

## Finds by source (door)

| Door | Banked items |
|---|---|
| arXiv (export API + abs/html deep reads) | 63 |
| Hacker News (Algolia + threads + linked pages) | 62 |
| Reddit (doors walled; pullpush / arctic-shift / redlib / WebSearch fallbacks) | 58 |
| X (WebSearch discovery + fxtwitter resolution) | 61 |
| **Total** | **244** |

## Adjudication outcome

- Confirmed finds: 23 rows in register.jsonl (22 unique URLs; the transformers-GGUF blog confirmed twice, via the reddit and x lanes). Table in DIGEST.md.
- Unconfirmed: 1 (KVarN, r/MachineLearning 1twnj5r). Full confirmation evidence in DIGEST.md; deliberately excluded from register.jsonl.
- Steal cards: 5, mirrored one-to-one into percolator_candidates.jsonl.

## Checks run in this fold (commands and outcomes)

1. Byte listing: `find . -type f -printf '%s %p\n'` over this folder, run twice (pre-write and post-fix). All counts above come from it.
2. Workflow gate registry: `wc -l < memory/workflows/REGISTRY.jsonl` = 45 rows; `grep -n "frontier_olm"` = zero matches by that string; name census via sed over the registry shows `the-gala.dwf.ts` rows dated 2026-10-01 and PASS.
3. JSONL validation (.venv\Scripts\python.exe, this session): register.jsonl parses to 23 rows with exactly the keys area, source, title, url, date, quote, why, overlap; percolator_candidates.jsonl parses to 5 rows with exactly the keys claim, source_url, estate_map, probe.
4. Seat-law scan (.venv\Scripts\python.exe, this session): em/en dashes (U+2013/U+2014) = 0 in DIGEST.md, register.jsonl, percolator_candidates.jsonl. Non-ASCII = exactly one codepoint, U+2192 RIGHTWARDS ARROW, inside the verbatim quote of register row 13 (r/LLMDevs 1wu24sc), carried as quoted material.

## Workflow gate row pointer

`memory/workflows/REGISTRY.jsonl`, line 45 of 45 (last line): name `the-gala.dwf.ts`, ts 2026-10-01T01:16:55Z, digest 2285b0104993, script `.zcode/workflows/the-gala.dwf.ts`, verdict PASS, checks G1-multiplicity through G7-laws all ok. The four prior rows for this run (01:13:49Z, 01:15:09Z, 01:15:25Z, 01:16:18Z) are also the-gala PASS rows. This fold step itself wrote no new registry row (the fold is a downstream step of the gated run, not a workflow spawn).
