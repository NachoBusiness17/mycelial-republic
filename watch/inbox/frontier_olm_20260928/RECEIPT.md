source-fetched: 2026-09-28

Receipt for the frontier_olm_20260928 fold (second pass), rewritten 2026-09-29 per operator
instruction after a missing-file report. Write-time state, measured before this rewrite:
os.path.exists on this path returned True and the on-disk file measured 26347 B (the version
written earlier on 2026-09-29), so the operator's surface and this seat disagreed; both facts are
recorded and this rewrite supersedes that file with fresh measurements. Every byte count below
was measured in this session with .venv/Scripts/python.exe os.walk + os.path.getsize over
watch/inbox/frontier_olm_20260928/ (never bare python, per AGENTS.md). A count is a snapshot of
one tree at one moment, not a constant (B2-216 discipline).

## Supersession

This pass overwrote the same-path predecessor fold earlier on 2026-09-29, measured before that
overwrite: DIGEST.md 28472 B (mtime 2026-09-29T17:53:25Z), RECEIPT.md 12380 B (17:55:43Z),
register.jsonl 34871 B and percolator_candidates.jsonl 37317 B (both 22:30:28Z). The predecessor
folded an 18-lane / 23-find / 9-card confirmation state; the current fold holds the 32-return
mine (21 confirmed finds, 3 unconfirmed items, 5 steal cards). The four fold outputs are
untracked in git with no committed history, so the predecessor text is not recoverable; its
headline counts survive here and in DIGEST.md's pass-over delta note. One predecessor
verification is carried forward inside register row 18's overlap field: the PolAgentBench CC0
attribution is FALSE (repo README says MIT code, CC BY 4.0 release data; the arXiv page's CC0 is
the paper-text license).

## Fold files (bytes measured this session, after the cold-read fixes to DIGEST.md and before this receipt's own rewrite)

| file | bytes (measured) |
|---|---|
| DIGEST.md | 41801 |
| register.jsonl | 24903 |
| percolator_candidates.jsonl | 20144 |
| RECEIPT.md (this file) | final size measured after this write and reported in the run result (a file cannot contain its own final byte count) |

register.jsonl: 21 rows, one per confirmed find, fields area, source, title, url, date, quote,
why, overlap, confidence; re-parsed line by line with json.loads this pass (21/21 clean). Rows 1
and 18 carry post-confirmation corrections inside overlap (Vals #1-open leg refuted at probe
2026-09-29; PolAgentBench license correction above). Rows 18 and 19 are the same paper (arXiv
2609.32042) independently confirmed from two lanes; both kept per one-row-per-confirmation; the
url-duplicate check run this pass over the parsed rows found exactly that one duplicate.

percolator_candidates.jsonl: 5 rows, one per steal card, fields claim, source_url, estate_map,
probe, area, card_path; parsed line by line with json.loads this session (5/5 clean; file bytes
unchanged since that parse, 20144 B in both walks). All five card_path targets exist and their
byte sizes equal the chars figure each card carries: 12088, 24863, 15737, 9707, 13335 (5/5
match, sizes re-confirmed in this pass's walk).

Dash/non-ascii scans: DIGEST.md re-scanned after the cold-read fixes (em 0 / en 0 / non-ascii 0);
register.jsonl and percolator_candidates.jsonl scanned this session (0/0/0 each); this receipt is
scanned after write and the result reported in the run result. The one unicode math token in a
source quote (the REUSE paper's 1-minus-alpha) is normalized to "1-alpha" in DIGEST.md and
register.jsonl; the normalization is stated in the digest header.

## Finds by area and by source (recounted by script this pass from register.jsonl)

By area (21 rows): open-and-local-language-models via x 8; evals-self-improvement via arxiv 6;
open-and-local-language-models-arxiv 4; quantization-compression via arxiv 1;
quantization-compression via hn 2.

By source as carried in the rows: x.com door (WebSearch site:x.com degraded + smol.ai AINews
indexes + fxtwitter door + mcp web_reader) 8; arXiv export API + arxiv.org/html full texts
(evals lane) 6; arXiv API via export.arxiv.org serialized curl (open-and-local-arxiv lane) 4;
export.arxiv.org Atom API (quantization-arxiv lane) 1; Hacker News via Algolia API + item
threads 2. Normalized by door: arxiv 11, x.com 8, hn 2. Total 21.

## Workflow gate row pointer

memory/workflows/REGISTRY.jsonl holds 39 rows this session. Rows for this workflow
(frontier-olm-mine, script .zcode/workflow-drafts/frontier-olm-mine.dwf.ts), every one verdict
PASS with G1-multiplicity, G2-passoff, G3-steering, G4-salvage, G5-deliverable, G6-receipts,
G7-laws all true (rows json-parsed this pass; the all-checks-true flag printed per row):

- line 31: ts 2026-09-29T01:29:32Z, name frontier-olm-mine, digest c4e6ac3c747a, PASS
- line 32: ts 2026-09-29T01:34:51Z, name frontier-olm-mine, digest 556f206840ee, PASS
- line 33: ts 2026-09-29T01:37:17Z, name frontier-olm-mine, digest 9015e3ec978f, PASS
- line 34: ts 2026-09-29T09:39:53Z, name frontier-olm-mine, digest 198e42a73ef3, PASS
- line 35: ts 2026-09-29T22:52:47Z, name frontier-olm-mine.dwf.ts, digest dbb3f296e2a4, PASS
- line 38: ts 2026-09-29T23:36:36Z, name frontier-olm-mine.dwf.ts, digest dbb3f296e2a4, PASS (latest)

Lines 36, 37, 39 are seatlaw_* payload-test rows (FAIL / PASS / FAIL on temp .dwf.ts probes),
not this workflow. Search note: rows 31-33 surfaced only when the registry was grepped by the
hyphenated workflow name (frontier-olm); an earlier grep using the underscore form (frontier_olm)
matched none of the names, which is why the previous receipt's pointer listed only lines 34, 35,
38. The full row set for this workflow is the six lines above.

## Tree census and full inventory

Census at the measurement moment (this pass, before this receipt's rewrite): 250 files,
14214544 bytes, with DIGEST.md already at its post-cold-read-fix size (41801 B) and RECEIPT.md
still at its pre-rewrite size (26347 B). After this receipt lands, the only changed file is
RECEIPT.md itself. Aggregates: fold files 4 (113195 B at census moment); lens/ 6 files (58824 B);
steal/ .md 13 files (184441 B); sweep bank .md 32 files (539001 B); sweep top-level raw receipts
21 files (518265 B, includes two intentional 0-byte files); sweep/_raw 157 files (12790871 B);
.mimosa hook artifacts 17 files (9947 B, harness state, listed for completeness, not fold
content). Aggregates sum to the census total (14214544), checked this pass.

```
218 watch/inbox/frontier_olm_20260928/.mimosa/hook-state/sess_dwf-dwfrun-c41194a8-e725-4bd7-8ee8-5f46206f8fde-actor_5_2.json
418 watch/inbox/frontier_olm_20260928/.mimosa/hook-status/sess_dwf-dwfrun-c41194a8-e725-4bd7-8ee8-5f46206f8fde-actor_5_2-dca3efdfbe.json
41801 watch/inbox/frontier_olm_20260928/DIGEST.md
26347 watch/inbox/frontier_olm_20260928/RECEIPT.md
11161 watch/inbox/frontier_olm_20260928/lens/burns.md
5277 watch/inbox/frontier_olm_20260928/lens/corpus.md
4389 watch/inbox/frontier_olm_20260928/lens/doors.md
6675 watch/inbox/frontier_olm_20260928/lens/graph.md
15477 watch/inbox/frontier_olm_20260928/lens/laws.md
15845 watch/inbox/frontier_olm_20260928/lens/questions.md
20144 watch/inbox/frontier_olm_20260928/percolator_candidates.jsonl
24903 watch/inbox/frontier_olm_20260928/register.jsonl
177 watch/inbox/frontier_olm_20260928/steal/.mimosa/hook-state/sess_dwf-dwfrun-c41194a8-e725-4bd7-8ee8-5f46206f8fde-actor_5_2.continue.json
449 watch/inbox/frontier_olm_20260928/steal/.mimosa/hook-state/sess_dwf-dwfrun-c41194a8-e725-4bd7-8ee8-5f46206f8fde-actor_5_2.json
19821 watch/inbox/frontier_olm_20260928/steal/agent-memory-continuity.md
12088 watch/inbox/frontier_olm_20260928/steal/evals-self-improvement via arxiv.md
14682 watch/inbox/frontier_olm_20260928/steal/inference-efficiency via reddit.md
12485 watch/inbox/frontier_olm_20260928/steal/inference-efficiency.md
8673 watch/inbox/frontier_olm_20260928/steal/open-and-local-language-models via reddit.md
24863 watch/inbox/frontier_olm_20260928/steal/open-and-local-language-models via x.md
15737 watch/inbox/frontier_olm_20260928/steal/open-and-local-language-models-arxiv.md
20553 watch/inbox/frontier_olm_20260928/steal/open-and-local-language-models-arxiv_prior-cycle-6finds.md
9056 watch/inbox/frontier_olm_20260928/steal/open-and-local-language-models.md
9707 watch/inbox/frontier_olm_20260928/steal/quantization-compression via arxiv.md
13335 watch/inbox/frontier_olm_20260928/steal/quantization-compression via hn.md
10239 watch/inbox/frontier_olm_20260928/steal/quantization-compression via hn_prior-cycle-20260929T1249.md
13202 watch/inbox/frontier_olm_20260928/steal/quantization-compression.md
218 watch/inbox/frontier_olm_20260928/sweep/.mimosa/hook-state/sess_dwf-dwfrun-c41194a8-e725-4bd7-8ee8-5f46206f8fde-actor_3_7.json
422 watch/inbox/frontier_olm_20260928/sweep/.mimosa/hook-status/sess_dwf-dwfrun-aa9969b0-38ab-415b-a2fe-6193ea0510d0-actor_3_29-989fcc1d39.json
895 watch/inbox/frontier_olm_20260928/sweep/_raw/.mimosa/hook-state/sess_dwf-dwfrun-279d66b4-d212-4d02-8869-7e35a5e423f7-actor_3_1.json
177 watch/inbox/frontier_olm_20260928/sweep/_raw/.mimosa/hook-state/sess_dwf-dwfrun-aa9969b0-38ab-415b-a2fe-6193ea0510d0-actor_6_6.continue.json
807 watch/inbox/frontier_olm_20260928/sweep/_raw/.mimosa/hook-state/sess_dwf-dwfrun-aa9969b0-38ab-415b-a2fe-6193ea0510d0-actor_6_6.json
1576 watch/inbox/frontier_olm_20260928/sweep/_raw/.mimosa/hook-state/sess_dwf-dwfrun-aa9969b0-38ab-415b-a2fe-6193ea0510d0-actor_6_6.mumu872j-47816-25be8793ae.baseline/645d78611874fbd197253b0164a70ba765be44d5bd5450785c7a39129754fa02.source
1027 watch/inbox/frontier_olm_20260928/sweep/_raw/.mimosa/hook-state/sess_dwf-dwfrun-aa9969b0-38ab-415b-a2fe-6193ea0510d0-actor_6_6.mumu872j-47816-25be8793ae.baseline/7ad3f2a62b9191c5f04fa3336876b628184811d800bd61bf172095090afef22b.source
1967 watch/inbox/frontier_olm_20260928/sweep/_raw/.mimosa/hook-state/sess_dwf-dwfrun-aa9969b0-38ab-415b-a2fe-6193ea0510d0-actor_6_6.mumu872j-47816-25be8793ae.baseline/ab53734f5776fa9efc3a2d674442e9d8f398b1e9ddea78d1c239328fdafde955.source
218 watch/inbox/frontier_olm_20260928/sweep/_raw/.mimosa/hook-state/sess_dwf-dwfrun-c41194a8-e725-4bd7-8ee8-5f46206f8fde-actor_3_4.json
218 watch/inbox/frontier_olm_20260928/sweep/_raw/.mimosa/hook-state/sess_dwf-dwfrun-c41194a8-e725-4bd7-8ee8-5f46206f8fde-actor_5_2.json
218 watch/inbox/frontier_olm_20260928/sweep/_raw/.mimosa/hook-state/sess_dwf-dwfrun-c41194a8-e725-4bd7-8ee8-5f46206f8fde-actor_6_2.json
405 watch/inbox/frontier_olm_20260928/sweep/_raw/.mimosa/hook-status/sess_dwf-dwfrun-279d66b4-d212-4d02-8869-7e35a5e423f7-actor_3_1-94b86b3985.json
537 watch/inbox/frontier_olm_20260928/sweep/_raw/.mimosa/hook-status/sess_dwf-dwfrun-c41194a8-e725-4bd7-8ee8-5f46206f8fde-actor_5_2-dca3efdfbe.json
41788 watch/inbox/frontier_olm_20260928/sweep/_raw/abs_2608.30005.html
43576 watch/inbox/frontier_olm_20260928/sweep/_raw/abs_2609.05881.html
43082 watch/inbox/frontier_olm_20260928/sweep/_raw/abs_2609.07370.html
69746 watch/inbox/frontier_olm_20260928/sweep/_raw/abs_2609.21341.html
40889 watch/inbox/frontier_olm_20260928/sweep/_raw/abs_2609.23742.html
42708 watch/inbox/frontier_olm_20260928/sweep/_raw/abs_2609.25373.html
43996 watch/inbox/frontier_olm_20260928/sweep/_raw/abs_2609.32042.html
42923 watch/inbox/frontier_olm_20260928/sweep/_raw/abs_2609.33467.html
2138 watch/inbox/frontier_olm_20260928/sweep/_raw/cookies.txt
5660 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1w39y4n.txt
14748 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1w39y4n_comments.json
6160 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1w39y4n_post.json
11665 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1w4rhsw.txt
74578 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1w4rhsw_comments.json
3468 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1w4rhsw_post.json
7308 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1w60b3s.txt
37617 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1w60b3s_comments.json
4374 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1w60b3s_post.json
13801 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1w65ise.txt
116066 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1w65ise_comments.json
7228 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1w65ise_post.json
2239 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wa5t43.txt
2175 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wa5t43_comments.json
7465 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wa5t43_post.json
7504 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1waa3yw.txt
44455 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1waa3yw_comments.json
3764 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1waa3yw_post.json
3168 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wau3a0.txt
8249 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wau3a0_comments.json
8460 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wau3a0_post.json
22616 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wb35xo.txt
55906 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wb35xo_comments.json
19101 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wb35xo_post.json
882 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wct2r3.txt
2410 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wct2r3_comments.json
3018 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wct2r3_post.json
17007 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wdrgz0.txt
78690 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wdrgz0_comments.json
7914 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wdrgz0_post.json
369 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1we3y13.txt
2 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1we3y13_comments.json
4517 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1we3y13_post.json
6429 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wi0803.txt
10430 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wi0803_comments.json
8012 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wi0803_post.json
17029 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wkpm2i.txt
84219 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wkpm2i_comments.json
7770 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wkpm2i_post.json
8178 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wm8j45.txt
33307 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wm8j45_comments.json
6050 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wm8j45_post.json
2856 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wn91x5.txt
13080 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wn91x5_comments.json
4193 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wn91x5_post.json
10415 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wpv1gz.txt
126430 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wpv1gz_comments.json
3818 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wpv1gz_post.json
24317 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wpxh2g.txt
157676 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wpxh2g_comments.json
3316 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wpxh2g_post.json
2060 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wqpswd.txt
5363 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wqpswd_comments.json
4614 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wqpswd_post.json
900 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wte7cv.txt
2373 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wte7cv_comments.json
4514 watch/inbox/frontier_olm_20260928/sweep/_raw/deep_1wte7cv_post.json
1967 watch/inbox/frontier_olm_20260928/sweep/_raw/dump_shortlist.py
534 watch/inbox/frontier_olm_20260928/sweep/_raw/extract_hit_36033.ps1
582459 watch/inbox/frontier_olm_20260928/sweep/_raw/full_2608.30005.html
120236 watch/inbox/frontier_olm_20260928/sweep/_raw/full_2608.30005.txt
98153 watch/inbox/frontier_olm_20260928/sweep/_raw/full_2609.05881.html
43967 watch/inbox/frontier_olm_20260928/sweep/_raw/full_2609.05881.txt
169792 watch/inbox/frontier_olm_20260928/sweep/_raw/full_2609.07370.html
48765 watch/inbox/frontier_olm_20260928/sweep/_raw/full_2609.07370.txt
207225 watch/inbox/frontier_olm_20260928/sweep/_raw/full_2609.21341.html
52444 watch/inbox/frontier_olm_20260928/sweep/_raw/full_2609.21341.txt
94953 watch/inbox/frontier_olm_20260928/sweep/_raw/full_2609.23742.html
21680 watch/inbox/frontier_olm_20260928/sweep/_raw/full_2609.23742.txt
517984 watch/inbox/frontier_olm_20260928/sweep/_raw/full_2609.25373.html
76442 watch/inbox/frontier_olm_20260928/sweep/_raw/full_2609.25373.txt
574760 watch/inbox/frontier_olm_20260928/sweep/_raw/full_2609.32042.html
123339 watch/inbox/frontier_olm_20260928/sweep/_raw/full_2609.32042.txt
656213 watch/inbox/frontier_olm_20260928/sweep/_raw/full_2609.33467.html
102455 watch/inbox/frontier_olm_20260928/sweep/_raw/full_2609.33467.txt
3743 watch/inbox/frontier_olm_20260928/sweep/_raw/fx_Alibaba_Qwen_status_2094968708288680276.json
9067 watch/inbox/frontier_olm_20260928/sweep/_raw/fx_ArtificialAnlys_status_2098148674203488422.json
6587 watch/inbox/frontier_olm_20260928/sweep/_raw/fx_BlinkDL_AI_status_2094785763129151677.json
3778 watch/inbox/frontier_olm_20260928/sweep/_raw/fx_NVIDIARobotics_status_2094480283135316182.json
2446 watch/inbox/frontier_olm_20260928/sweep/_raw/fx_ValsAI_status_2098125164072554545.json
6249 watch/inbox/frontier_olm_20260928/sweep/_raw/fx_aayush_small.json
4181 watch/inbox/frontier_olm_20260928/sweep/_raw/fx_aayush_small2.json
9588 watch/inbox/frontier_olm_20260928/sweep/_raw/fx_arena_status_2094566204488962483.json
9728 watch/inbox/frontier_olm_20260928/sweep/_raw/fx_ashcsx_nemotron.json
4150 watch/inbox/frontier_olm_20260928/sweep/_raw/fx_ggerganov_status_2095897173376618881.json
3341 watch/inbox/frontier_olm_20260928/sweep/_raw/fx_kimmonismus_status_2097286327909675477.json
24688 watch/inbox/frontier_olm_20260928/sweep/_raw/fx_minimax_m21.json
3300 watch/inbox/frontier_olm_20260928/sweep/_raw/fx_ollama_status_2094622506720391454.json
4277 watch/inbox/frontier_olm_20260928/sweep/_raw/fx_ollama_status_2098188014119985406.json
5222 watch/inbox/frontier_olm_20260928/sweep/_raw/fx_rasbt_status_2098142625819672603.json
59866 watch/inbox/frontier_olm_20260928/sweep/_raw/fx_thevalueist.json
7878 watch/inbox/frontier_olm_20260928/sweep/_raw/fx_zaibatsu_article.json
5047 watch/inbox/frontier_olm_20260928/sweep/_raw/fx_zizhpan_status_2094386230675062836.json
2508 watch/inbox/frontier_olm_20260928/sweep/_raw/hf_rwkv7g1.json
5883 watch/inbox/frontier_olm_20260928/sweep/_raw/hf_v4flashvision.json
35797 watch/inbox/frontier_olm_20260928/sweep/_raw/jetson_home.html
35797 watch/inbox/frontier_olm_20260928/sweep/_raw/jetson_root.html
108336 watch/inbox/frontier_olm_20260928/sweep/_raw/jetson_tutorials.html
3197 watch/inbox/frontier_olm_20260928/sweep/_raw/jetson_unsloth.html
92055 watch/inbox/frontier_olm_20260928/sweep/_raw/jetson_unsloth_on_jetson.html
1143 watch/inbox/frontier_olm_20260928/sweep/_raw/jina_top.md
91929 watch/inbox/frontier_olm_20260928/sweep/_raw/list_csCL.html
87893 watch/inbox/frontier_olm_20260928/sweep/_raw/list_csLG.html
322843 watch/inbox/frontier_olm_20260928/sweep/_raw/llama_top.rss
0 watch/inbox/frontier_olm_20260928/sweep/_raw/llama_top2.json
322940 watch/inbox/frontier_olm_20260928/sweep/_raw/llama_top3.json
8603 watch/inbox/frontier_olm_20260928/sweep/_raw/nemotron35_fastino_article.md
89522 watch/inbox/frontier_olm_20260928/sweep/_raw/ollama_lib_v41flash.html
69 watch/inbox/frontier_olm_20260928/sweep/_raw/ollama_registry_v41flash.txt
1165 watch/inbox/frontier_olm_20260928/sweep/_raw/overlap_grep_20260929.ps1
928 watch/inbox/frontier_olm_20260928/sweep/_raw/overlap_grep_final.ps1
1207 watch/inbox/frontier_olm_20260928/sweep/_raw/overlap_grep_ids.ps1
1576 watch/inbox/frontier_olm_20260928/sweep/_raw/parse_arxiv.py
277264 watch/inbox/frontier_olm_20260928/sweep/_raw/pull2_AI_Agents_handoff.json
160641 watch/inbox/frontier_olm_20260928/sweep/_raw/pull2_ClaudeAI_rate_limit.json
297727 watch/inbox/frontier_olm_20260928/sweep/_raw/pull2_ClaudeAI_subagent.json
208124 watch/inbox/frontier_olm_20260928/sweep/_raw/pull2_ClaudeCode_agent_teams.json
132169 watch/inbox/frontier_olm_20260928/sweep/_raw/pull2_ClaudeCode_rate_limit.json
543912 watch/inbox/frontier_olm_20260928/sweep/_raw/pull2_ClaudeCode_subagent.json
511895 watch/inbox/frontier_olm_20260928/sweep/_raw/pull2_LocalLLaMA_mcp.json
425665 watch/inbox/frontier_olm_20260928/sweep/_raw/pull2_LocalLLaMA_multi-agent.json
104141 watch/inbox/frontier_olm_20260928/sweep/_raw/pull2_LocalLLaMA_rate_limit.json
26786 watch/inbox/frontier_olm_20260928/sweep/_raw/pull2_mcp_orchestration.json
78334 watch/inbox/frontier_olm_20260928/sweep/_raw/pull2_ollama_multi-agent.json
191 watch/inbox/frontier_olm_20260928/sweep/_raw/pullpush_test.json
128754 watch/inbox/frontier_olm_20260928/sweep/_raw/q_a_toolcall.xml
126930 watch/inbox/frontier_olm_20260928/sweep/_raw/q_b_small.xml
60457 watch/inbox/frontier_olm_20260928/sweep/_raw/q_c_json.xml
129291 watch/inbox/frontier_olm_20260928/sweep/_raw/q_d_openweight.xml
98753 watch/inbox/frontier_olm_20260928/sweep/_raw/q_e_verify.xml
53560 watch/inbox/frontier_olm_20260928/sweep/_raw/q_f_bfcl.xml
81939 watch/inbox/frontier_olm_20260928/sweep/_raw/q_g_quant.xml
47174 watch/inbox/frontier_olm_20260928/sweep/_raw/q_h_smallslm.xml
122326 watch/inbox/frontier_olm_20260928/sweep/_raw/smol_26-08-31-not-much.html
193875 watch/inbox/frontier_olm_20260928/sweep/_raw/smol_26-09-01-claude-mythos-51.html
120285 watch/inbox/frontier_olm_20260928/sweep/_raw/smol_26-09-04-collusionwiki.html
134570 watch/inbox/frontier_olm_20260928/sweep/_raw/smol_26-09-08-navier-stokes.html
144771 watch/inbox/frontier_olm_20260928/sweep/_raw/smol_26-09-10.html
1027 watch/inbox/frontier_olm_20260928/sweep/_raw/strip_html.py
3144 watch/inbox/frontier_olm_20260928/sweep/_raw/sweep_swarm_deepread.py
54 watch/inbox/frontier_olm_20260928/sweep/_raw/sweep_swarm_llama_mcp.json
3156 watch/inbox/frontier_olm_20260928/sweep/_raw/sweep_swarm_pull.py
2927 watch/inbox/frontier_olm_20260928/sweep/_raw/sweep_swarm_pull2.py
322796 watch/inbox/frontier_olm_20260928/sweep/_raw/thread_test.html
1297267 watch/inbox/frontier_olm_20260928/sweep/_raw/vals_home_20260929.html
305311 watch/inbox/frontier_olm_20260928/sweep/_raw/vals_model_v41flash.html
55073 watch/inbox/frontier_olm_20260928/sweep/_raw/vals_try.html
189908 watch/inbox/frontier_olm_20260928/sweep/_raw/www_top.json
20616 watch/inbox/frontier_olm_20260928/sweep/agent-memory-continuity-arxiv.md
14432 watch/inbox/frontier_olm_20260928/sweep/agent-memory-continuity-hn.md
12554 watch/inbox/frontier_olm_20260928/sweep/agent-memory-continuity-reddit.md
13312 watch/inbox/frontier_olm_20260928/sweep/agent-memory-continuity-x.md
19922 watch/inbox/frontier_olm_20260928/sweep/evals-self-improvement-arxiv.md
16230 watch/inbox/frontier_olm_20260928/sweep/evals-self-improvement-hn.md
18042 watch/inbox/frontier_olm_20260928/sweep/evals-self-improvement-reddit.md
17424 watch/inbox/frontier_olm_20260928/sweep/evals-self-improvement-x.md
14922 watch/inbox/frontier_olm_20260928/sweep/finetuning-and-adaptation-arxiv.md
10857 watch/inbox/frontier_olm_20260928/sweep/finetuning-and-adaptation-hn.md
10175 watch/inbox/frontier_olm_20260928/sweep/finetuning-and-adaptation-reddit.md
11161 watch/inbox/frontier_olm_20260928/sweep/finetuning-and-adaptation-x.md
15487 watch/inbox/frontier_olm_20260928/sweep/inference-efficiency-arxiv.md
15913 watch/inbox/frontier_olm_20260928/sweep/inference-efficiency-hn.md
19989 watch/inbox/frontier_olm_20260928/sweep/inference-efficiency-reddit.md
19848 watch/inbox/frontier_olm_20260928/sweep/inference-efficiency-x.md
24608 watch/inbox/frontier_olm_20260928/sweep/kv-cache-context-engineering-arxiv.md
24060 watch/inbox/frontier_olm_20260928/sweep/kv-cache-context-engineering-hn.md
14268 watch/inbox/frontier_olm_20260928/sweep/kv-cache-context-engineering-reddit.md
14643 watch/inbox/frontier_olm_20260928/sweep/kv-cache-context-engineering-x.md
18307 watch/inbox/frontier_olm_20260928/sweep/open-and-local-language-models-arxiv.md
13139 watch/inbox/frontier_olm_20260928/sweep/open-and-local-language-models-hn.md
20882 watch/inbox/frontier_olm_20260928/sweep/open-and-local-language-models-reddit.md
21532 watch/inbox/frontier_olm_20260928/sweep/open-and-local-language-models-x.md
191 watch/inbox/frontier_olm_20260928/sweep/pp_LocalLLM.json
191 watch/inbox/frontier_olm_20260928/sweep/pp_LocalLLaMA.json
191 watch/inbox/frontier_olm_20260928/sweep/pp_MachineLearning.json
11904 watch/inbox/frontier_olm_20260928/sweep/pp_c_1q9o6n9.json
27649 watch/inbox/frontier_olm_20260928/sweep/pp_c_1qbei13.json
91864 watch/inbox/frontier_olm_20260928/sweep/pp_c_1thjsnx.json
23288 watch/inbox/frontier_olm_20260928/sweep/pp_c_1v2stwu.json
89557 watch/inbox/frontier_olm_20260928/sweep/pp_c_1vlm9ai.json
47832 watch/inbox/frontier_olm_20260928/sweep/pp_ids_b1.json
88190 watch/inbox/frontier_olm_20260928/sweep/pp_ids_b2.json
66718 watch/inbox/frontier_olm_20260928/sweep/pp_ids_b3.json
40437 watch/inbox/frontier_olm_20260928/sweep/pp_ids_b4.json
22255 watch/inbox/frontier_olm_20260928/sweep/pp_ids_b5.json
54 watch/inbox/frontier_olm_20260928/sweep/pp_ids_batch1.json
191 watch/inbox/frontier_olm_20260928/sweep/pp_new_page1.json
191 watch/inbox/frontier_olm_20260928/sweep/pp_ollama.json
5363 watch/inbox/frontier_olm_20260928/sweep/pp_probe2.json
191 watch/inbox/frontier_olm_20260928/sweep/pp_q_toolcalling.json
0 watch/inbox/frontier_olm_20260928/sweep/pullpush_pass1.err
2008 watch/inbox/frontier_olm_20260928/sweep/pullpush_pass1.py
16227 watch/inbox/frontier_olm_20260928/sweep/quantization-compression-arxiv.md
20244 watch/inbox/frontier_olm_20260928/sweep/quantization-compression-hn.md
16243 watch/inbox/frontier_olm_20260928/sweep/quantization-compression-reddit.md
17739 watch/inbox/frontier_olm_20260928/sweep/quantization-compression-x.md
0 watch/inbox/frontier_olm_20260928/sweep/reddit_llama_top.json
12830 watch/inbox/frontier_olm_20260928/sweep/swarm-orchestration-arxiv.md
16338 watch/inbox/frontier_olm_20260928/sweep/swarm-orchestration-hn.md
26276 watch/inbox/frontier_olm_20260928/sweep/swarm-orchestration-reddit.md
10781 watch/inbox/frontier_olm_20260928/sweep/swarm-orchestration-x.md
```

## Checks run this session (exact commands and outcomes)

1. Tree walk with sizes over watch/inbox/frontier_olm_20260928 (.venv/Scripts/python.exe,
   os.walk + os.path.getsize), run this pass before this rewrite: 250 files, 14214544 bytes;
   per-file table above. Also confirmed RECEIPT.md existed at 26347 B at check time (recorded in
   the header, against the operator's missing-file report).
2. register.jsonl re-parsed this pass: json.loads per line, 21/21 clean; finds-by-area and
   url-duplicate counts computed from the parsed rows (numbers above).
   percolator_candidates.jsonl parsed 5/5 this session; bytes unchanged (20144 B in both walks)
   since that parse; the five card_path sizes re-confirmed in this pass's walk (5/5 equal to the
   cards' chars figures).
3. Registry: memory/workflows/REGISTRY.jsonl grepped this pass by the hyphenated name
   (frontier-olm), 6 matching rows at lines 31, 32, 33, 34, 35, 38 out of 39 total; each row
   json-parsed with per-check ok flags printed (all true); noted that an earlier underscore-form
   grep (frontier_olm) had missed lines 31-33.
4. Dash scans: DIGEST.md re-scanned after the cold-read fixes (0/0/0); register.jsonl and
   percolator_candidates.jsonl scanned this session (0/0/0); this receipt post-write scan
   reported in the run result.

Not run by this fold: any of the five steal-card probes (proposals), any estate test suite (none
named by the ask), and any re-fetch of source URLs (content is lane-reported from the
2026-09-28 sweeps; the confirmation-pass evidence is carried from the ask's material).
