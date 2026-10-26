# ARCHIVE PROPOSAL: watch/inbox cold heavyweights → watch/archive/2026-09/ (PROPOSAL ONLY)

Written 2026-10-17 by the inbox librarian pass. **Nothing was moved.** Sizes come from the 2026-10-17 inventory (`watch_inbox_inventory.csv`). Code references come from a read-only `git grep` over tracked `*.py *.ps1 *.sh *.ts *.js *.yaml *.yml *.toml *.json`, excluding `watch/inbox` and `watch/LIBRARY`.

## Candidates and bytes

| candidate | files | bytes | newest activity | code references (git grep) | verdict |
|---|---|---|---|---|---|
| `mrpool_export/` | 2,861 | 3.66 GB (3,656,410,466) | **2026-10-17 02:30** (`vision_nightly_receipts.jsonl`) | **LIVE.** `scripts/vision_nightly.py:43` and `scripts/vision_triage_pool.py:41` (`MRP = ROOT/"watch"/"inbox"/"mrpool_export"`), `scripts/register_vision_nightly.ps1:38` (nightly receipts land here), `mag/verb.py:156-157` (reads `called_shot_ledger.jsonl`, `SOUND_READING_FULL.json`), `tools/drift_dashboard.py:57` (`ledger.jsonl`), plus 5 `the50_*` scripts and `tools/caption_ledger_sha_check.py`, `tools/drift_pairs_stamp.py`, and `configs/secret_gate_baseline.json` | **Do not move yet.** Even the media is live: `scripts/vision_nightly.py:140` and `scripts/vision_triage_pool.py:43` glob `mrpool_export/media_full/msg_*.jpg` (3.64 GB of the 3.66 GB) for the nightly vision triage. Retire or repoint that job first, then move `media_full/` (it is 99% of the bytes). |
| `ESSENTIALS_PACK_20260926.tar.gz.enc` (root) | 1 | 1.71 GB (1,706,469,664) | 2026-09-26 | No runtime code. Named only in `memory/audit_20260926/*.json` (audit evidence) and old in-inbox burn scripts (`burn_wave_20260926/B2_146_regcheck.py`, `burn_reset_20260927/flash50/s2-07_characterize.py`) | Safe to move. It is an encrypted backup, so better still, send it to the 10TB cold tier (see THE_10TB_TIER_20261016.md). The 22 MB `ESSENTIALS_PACK_VAULT_20260926.tar.gz.enc` sibling should travel with it. |
| `qdrop_export/` | 4,979 | 607 MB (607,055,594) | 2026-09-26 | **LIVE.** `scripts/qcaption_verify_daily.py:28` (`q_caption_ledger.jsonl`), `tools/gate_canary.py:42,51,104`, `tests/test_qdrop_canonical.py:21` (imports `qdrop_export/qdrop_canonical.py`), `tools/corpus.py`, `mag/catalog_freshness.py`/`catalog_rescan.py` (docstrings), plus 6 `the50_*` scripts | Move only the bulk `qaggdrop_*.png` media. Keep `q_caption_ledger.jsonl` and `qdrop_canonical.py` in place, or repoint the daily verifier, gate canary and test first. |
| `frontier_olm_<date>/` × 13 day folders (2026-09-28 .. 2026-10-11; not `_adhoc`) | 2,397 | 236 MB (236,118,336) | 2026-10-11 | 32 tracked files cite them, nearly all as **provenance comments** in `mag/` (knowledge_graph, memweave, marker_penalty, context_checkpoint, improve, llama_cpp_bridge, contamination_tripwire...) and tests, plus `configs/citation_lint_baseline.json`, `configs/marker_penalty_profile.json`, `configs/improve.yaml` (comment). No runtime path construction found. | Movable, but it breaks the citation trail: citation lint / marker-penalty baselines point at these paths. Either leave a `MOVED_TO.txt` stub per folder and update the two config baselines in the same commit, or keep them. `frontier_olm_adhoc` (newest 10-12, also cited) stays. |
| 23 cold folders (nothing newer than 30 days) | 318 | 66 MB (65,896,354) | ≤ 2026-09-17 | 22 of 23: **zero** references. `steal_research_pipeline/` is cited in `mag/invariant_surface.py:7,195` (comment and provenance string). | Safe to move. Leave a stub or update the one citation for `steal_research_pipeline`. |

The 23 cold folders: hypersigils_202603 (23.0 MB), bad_apple (18.4 MB), journal_mark_202609 (14.2 MB), desktop_bundle_20260901 (3.2 MB), ore_20260916 (2.4 MB), fleet_research_lens, physical_computing, matthews_zenodo_17811909, mickey, KG_SOURCES_20260901_src, media, moonshot_20260916, FLT_20260906, v41_paces, hive_operating_floor, static_rebuild, astra_ask_package, outbound, kvos_steal, steal_research_pipeline, astra_review_sep16, astra_corpus, the_margin.

## Bytes saved from the live inbox

- All five candidate groups as listed: **≈ 6.29 GB** (3.66 + 1.73 incl. vault pack + 0.61 + 0.24 + 0.07) of 7.31 GB, about 86% of the inbox.
- Safe-now subset (no runtime code depends on it): `.enc` packs + 23 cold folders = **≈ 1.79 GB**.
- qdrop media-only split (`qaggdrop_*.png`, 601 MB) after repointing nothing (the .png files are not referenced by code; only the ledger and `qdrop_canonical.py` are): +0.60 GB.
- mrpool `media_full/` (3.64 GB) only after the nightly vision triage is retired or repointed.
- The frontier_olm day folders add 0.24 GB once the citation stubs are handled.

## Suggested order (when the operator approves)

1. Move the `.enc` packs + 22 unreferenced cold folders. Stub `steal_research_pipeline`.
2. qdrop: move only the `qaggdrop_*.png` media and keep the ledger + `qdrop_canonical.py`. mrpool: first decide on the nightly vision job (registered by `scripts/register_vision_nightly.ps1`).
3. frontier_olm day folders: move along with `MOVED_TO.txt` stubs and a baseline-config update in the same commit, after the v2 bintree build is marked DONE.
4. Re-run `python scripts\inbox_librarian.py --full` so the catalog reflects the new paths.

The `memory/trajectory/steps.jsonl` reference inside `B2_sw08_reapply_board.py` was seen only as a grep match line. The file itself was not opened.
