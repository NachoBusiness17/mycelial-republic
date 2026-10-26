# LENS: corpus (frontier_olm 2026-10-09)

What the estate's corpus already covers, with counts counted in-session. Lens seat: lens-corpus. No em-dashes per law. Every number below was counted by me this session unless explicitly attributed.

## Instruments run (this session)

- Read `catalog/catalog_manifest.json` (44 lines). Manifest states snapshot_ts 2026-10-09T07:35:41Z (line 28), tags_rows 1,343,390 (line 38), base_rows 1,266,929 (line 33), mode incremental (line 26).
- Read `CORPUS_CATALOG.md` (33 lines). Line 5 flags the canon manifest as DRIFT (checked 205, missing 0, drifted 4) and says to resolve before trusting the shelves. Its shelf table (lines 9-21) is the Librarian's 2026-10-09T13:21:27Z run (line 3), roughly 5h46m newer than the catalog snapshot; the two are not same-moment instruments.
- `wc -l catalog/catalog.jsonl` returned 1,343,390 lines (384,088,978 bytes; byte size matches manifest map_bytes line 22 exactly).
- Streaming JSON counts over all 1,343,390 rows of `catalog/catalog.jsonl` (repo venv python, heredoc): rows by zone, top-level dir, second/third-level segments, per-shelf rows and bytes.
- Streaming counts over all 1,343,390 rows of `catalog/tags.jsonl` by kind: config 828,166; other 178,246; prose 121,428; code 86,495; ledger 50,017; image 41,164; receipt 14,976; test 10,792; brief 6,205; card 2,552; corpus 1,785; state 1,564. This matches `catalog_manifest.json` kind_counts (lines 8-21) exactly, key for key.
- Path-substring probe over all 1,343,390 paths for 19 frontier-topic keywords (counts below).

## Corpus scale (counted)

1,343,390 catalog rows total. Zone split (counted): memory 793,480; lsa 351,683; runs 56,948; ext:lsa_reboot_staging 56,343; intake 21,077; watch 4,764; queue 986; code 935; doctrine 802; research 95; vault 135; remainder external roots and singletons. Rows are files, not words; most of `memory` is the biography knot machinery (knots 78,834 rows plus knots_attic 204,327 plus dated biography_backup snapshots, largest 20261004 at 42,910), not research holdings.

## Research domains the corpus already covers (my counts: rows / MB)

1. **AI/LLM and agent engineering curriculum** (`local_sovereign_agent/corpus/library`, 52,313 rows / 4,646.3 MB): ms-genai-beginners 12,142; ms-agents-beginners 9,429; zcode-zai-org 6,810; ai-engineering-from-scratch 5,401; openai-cookbook 3,120; lmcache-src 2,331; kev 934. Adjacent: the estate's own frontier mining tree `mine/raw/` totals 97,867 rows: agent_platform 72,329; agent_bleeding_edge 14,468; mesh_comm 5,297; steal_protocol 4,118; narrative_corpus 1,653.
2. **Game-server emulation and MMO internals**: external roots azerothcore-wow 10,356 / 857.3 MB; vmangos-core 4,397 / 166.1 MB; tortoise-wow 3,767 / 365.4 MB; plus in-corpus mod-playerbots 5,019 (inside corpus/library); DFHack (Dwarf Fortress) corpus/dfhack_full 2,123 / 17.8 MB; evennia MUD framework 1,579; world-games-corpus root 81 / 2.7 MB; memory/corpus/game_design_docs 38 / 39.2 MB.
3. **Shaders / GPU visuals**: memory/corpus/shadertoy21k 21,806 rows / 136.6 MB (single largest named research holding after the curriculum shelves).
4. **Oral history / social archaeology**: corpus/oral_history 14,860 rows / 1,347.9 MB (seat_pools 11,871; nacho_archaeology 2,981); sibling top-level root `corpus/` adds social_archive 17 and papers_reference_nonredistributable 82 / 132.5 MB; nacho-business root 43 / 8.4 MB.
5. **Reverse engineering / binary tooling**: corpus/tools 6,029 rows / 2,121.9 MB (ghidra_12.1.4_PUBLIC 5,219; jdk-21 490).
6. **Small canon shelves** (memory/corpus/*): ai_canon 33 / 187.1 MB; mycology_canon 52 / 100.8 MB; electronics_canon 30 / 61.2 MB; training_pdfs 36 / 54.3 MB; ractors 310 / 122.6 MB; game_design_docs 38 / 39.2 MB; moonshot_canon 21 / 9.8 MB; augmentation_canon 9 / 13.9 MB; quantized_thought 33 / 2.0 MB; esoteric_canon 23 / 3.3 MB; ml 17 / 3.5 MB; founding_law 14 / 1.5 MB.
7. **Adjacent-domain repo scans** (external roots, small): the_margin_lean 9,164 / 100.0 MB; teach 366 / 34.1 MB; mycelial-republic 312 / 13.7 MB; mag-sovereign-kit 310 / 4.3 MB; research 767 / 28.8 MB; ai-job-search 96 / 2.3 MB; the-mountain 74 / 1.2 MB; field-strike-the-chord 68 / 1.6 MB; ractor-salon 30 / 0.2 MB; embassy-sandbox 37 / 0.1 MB.
8. **Estate operations record** (not research, but the sweep's reverse-GPS): watch 27,069 rows / 14,278.4 MB; canon dirs lsa/corpus/canon 210 / 19.7 MB and lsa/canon 107 / 338.9 MB; logs 10,894 / 27,069.6 MB; state 7,347 / 591.7 MB; attic 147 / 5,299.1 MB.

## Frontier-topic path probe (substring over 1,343,390 paths; weak signal where the word is generic)

token 2,315; defi 389; crypto 249; genome 235; hardware 68; robot 65; quantum 45; energy 21; satellite 10; blockchain 9; climate 7; rocket 7; verilog 3; semiconductor 2; fpga 2. ZERO matches in the entire catalog for: biology, biotech, drug, web3. Note: token/defi/genome hits ride game-economy and code paths, so they are not domain coverage; the zero rows are the trustworthy signal.

## Coverage gaps the frontier sweep can treat as open

Per the probe, the corpus has no rows at all in bio/health (biology, biotech, drug: 0 paths) and no web3-native domain corpus (web3: 0; blockchain: 9 incidental). Physics/hardware (quantum 45, semiconductor 2, fpga 2, verilog 3) is incidental naming, not a shelf: no canon or library shelf for them exists in my bucketed tree.

## Cross-checks and unreconciled drift (stated, not smoothed over)

- My kind census equals the manifest exactly (verified this session); tags rows equal catalog rows equal `wc -l` (1,343,390).
- My buckets are whole top-level directories and do NOT match the Librarian's shelf definitions one-to-one, so I do not equate them. Where they nearly align they disagree: canon (mine 210 rows vs Librarian 209 files, CORPUS_CATALOG.md line 11) and oral_history (mine 14,860 rows / 1,347.9 MB vs Librarian 15,749 files / 1,423.9 MB, line 15; the Librarian ran later the same day, catalog 07:35Z vs Librarian 13:21Z). The library shelf at 66,715 files / 7,235.1 MB (line 18) vs my corpus/library 52,313 / 4,646.3 MB: unexplained by me, likely differing shelf definitions; not reconciled in this lens.
- OWED (not done here): reconcile the canon manifest drift; sample inside large shelves for topical depth (row counts are file counts, not evidence of content quality).

## Source lines

catalog/catalog_manifest.json:8-21 (kind_counts), :22 (map_bytes), :26 (mode), :28 (snapshot_ts), :33 (base_rows), :38 (tags_rows). CORPUS_CATALOG.md:3 (run moment), :5 (DRIFT flag), :9-21 (shelf table), :23-31 (bulk layers). All counts otherwise: my in-session streaming counts over catalog/catalog.jsonl and catalog/tags.jsonl as described in Instruments.
