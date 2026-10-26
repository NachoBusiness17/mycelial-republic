# SEATS INVENTORY - every primary source seats added, 48h window

Lane: seats-inventory (division B), gala_20260925 librarian-expedition. Run moment: 2026-10-01T22:56Z start, receipt generated ~2026-10-02T00:1xZ. Window: 2026-09-29T22:56Z .. 2026-10-01T22:56Z (mtime-based, machine local EDT).

## Method (byte-checked)

- Enumerated in-window files under the named fetch trails (flash50, burn_reset work, localfirst, gala localfirst-steal, music-ractor, watch/inbox/music) via `find -newermt "2026-09-29 22:56"`, plus every staged/untracked add from `git status --porcelain -uall` (adds_all.txt, 573 rows), plus the 10 corpus additions; window-filtered by mtime. Listing: watch/inbox/librarian_exp/trail_listing_raw.txt (438 rows) + adds_all.txt. Dedup by exact path. Raw instrument: watch/inbox/librarian_exp/build_inventory.py + reconcile_print_only.py; intermediate rows: inventory_rows.json + rows2.jsonl.
- Catalog match: exact normalized repo-relative path against a full stream of catalog/catalog.jsonl; prefix convention 'local_sovereign_agent/' stripped (770,616 of 821,776 rows carried it in the pass-2 stream). A catalog hit counts 'yes' only if the row's recorded bytes equal the on-disk bytes; a bytes mismatch counts 'stale'.
- INDEX match: watch/inbox/INDEX.json (2,420 items) by path relative to watch/inbox/; where an item carries sha256 and the artifact is <20MB, the sha was recomputed from disk and compared.
- Format: first-bytes sniffing (PDF/PAR1/gzip/tar/zip/sqlite/MZ/pyc/JSON/HTML/text), cross-checked against extension. No extension was trusted.
- FTS: catalog_fts.sqlite crows table streamed read-only; registered artifacts checked for FTS presence by normalized path.

## SURFACE MOMENTS (the census law: name instrument and moment; the catalog moved during this run)

- catalog/catalog.jsonl: 193,942,047 bytes, 691,789 lines at 18:57 EDT (2026-10-01T22:57Z); pass-1 stream read 821,408 rows ~19:05 EDT; pass-2 stream read 821,776 rows ~23:45-59Z; file measured 230,735,284 bytes at Oct 1 19:45 EDT after the run. A rebuild swept through mid-run; all registration verdicts below are against the pass-2 stream moment.
- catalog/catalog_fts.sqlite: Sep 30 09:00 EDT mtime when first read; measured Oct 1 19:45 EDT (234,754,048 bytes) after pass-2, with crows = 821,776 = the pass-2 catalog row count exactly. So the FTS surface is FRESH as of that moment. logs/fts_index.log still ends at [2026-09-30 09:00:02] END with no Oct 1 START: whatever rebuilt the surfaces at 19:45 EDT did not write the MagFtsIndexDaily log path. Stated as observed, not attributed.
- watch/inbox/INDEX.json: 717,823 bytes, 2,420 items, read once (single moment).

## HEADLINE

- Artifacts inventoried: **975** files, **72,591,499** bytes.
- Cataloged (exact path + bytes match): **891** (91 pct). Stale catalog rows (recorded bytes != disk): **4**. Unregistered: **80** (8 pct) - and every one of the 80 is clone plumbing, Mimosa hook-state, or pyc; ZERO fetched sources or lane outputs of value are unregistered.
- INDEX-registered: **84** (sha verified on recompute where recorded); INDEX sha-STALE: **6** (registered receipt edited after registration).
- Location: scratch-inbox 641, scratch-root 94, durable-holdings 10, durable-repo 230. The shared-surface rule (watch/inbox is cache, not holdings) is respected in only one direction: the fetched SOURCES live as scratch, and the only durable copies of most of them are the catalog rows themselves.
- Real magic-vs-extension corruptions: **0** of 975 (pass-1's 105 'mismatches' were this lane's own classifier false-positives on dotfiles and git internals; corrected in pass 2 - owned here per no-fabrication). Minor container mislabels: 11 .jsonl files whose whole body is a single JSON document.

## By class of artifact

- fetched-source: 420 files, 48,707,782 bytes
- instrument-output: 339 files, 23,176,994 bytes
- fetch-receipt: 192 files, 311,450 bytes
- code-land: 17 files, 213,221 bytes
- estate-bookkeeping: 6 files, 118,659 bytes
- fetched-source-mangled-copy: 1 files, 63,393 bytes

## By fetcher (fetched-by)

- localfirst-steal gala lanes (herald seat; clones/tarball/readmes): 359
- report_v1 desk (per-source retrieval receipts): 192
- model garden local lane (2026-10-01): 105
- frontier olm mine day sweep (2026-09-30 dig): 55
- pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin): 43
- music-ractor gala lanes: 32
- burn_reset work lanes (hermes/openrouter/impfeed/verify by filename): 28
- animal tape collector (seat session tapes): 24
- flock parity instrument: 24
- secret gate scanner outputs (2026-10-01): 18
- estate code lands (builders): 17
- top-level inbox drops (seat/cron receipts): 14
- descent burn carrier outputs: 13
- report_v1 desk prior-art pull (arxiv export; receipts docs/report_v1/sources/receipts/persona_priorart_*.md): 9
- localfirst dig (stealth lane digests): 8
- mimo_v26 dataset download: 7
- estate bookkeeping (ribs/burns/renders): 6
- day ledger / radar outputs: 5
- gala_20260925 sibling lanes (receipts/digests): 5
- mangled-path temp copy (path separators eaten): 3
- seats-inventory lane (this inventory): 3
- flash50 stealth burn lane (2026-09-27 reset, f-seats): 1
- mangled-env scratch copy (literal %TMPDIR% dir): 1
- descent day1 carrier (hermes_burn receipt mining): 1
- console render instrument: 1
- mangled-path root copy (path separators eaten): 1

## Librarian diseases, checked for and found/not found

1. **Match beyond arXiv-id** - CONFIRMED as a trap, resisted: matching by the id string '2310.10158' hits **3** catalog rows while the actual pdf is one file (persona_priorart_2310.10158.pdf, 786,216 bytes on disk, matching its retrieval receipt docs/report_v1/sources/receipts/persona_priorart_2310.10158.md). Two of the three rows ARE the pdf path - see disease 4. Matching was done by exact normalized path + bytes equality only.
2. **Dedupe-detector-excludes-itself** - CONFIRMED as a trap, resisted: **54** of the 80 unregistered files share a basename stem with some OTHER catalog path (e.g. the lbrain clones' .git/hooks/*.sample vs unrelated catalog files). A stem-keyed dedupe would have wrongly marked clone plumbing 'already registered'. Exact-path matching kept them honestly unregistered.
3. **Magic-bytes-before-trust** - CLEAN: 0 real content-vs-extension corruptions among 975 files; 7 PDFs open %PDF, 5 parquets open PAR1, the tarball is gzip. The one content-class quirk class: 11 .jsonl seat-tape files hold a single JSON object each (container mislabel, content intact): claude_fable_5_1.jsonl, deepseek.jsonl, gemini_flash.jsonl, glm_5_3_flash.jsonl, grok_4_3.jsonl, kimi.jsonl...
4. **Path-convention double registration** - FOUND: the catalog rebuild mixed conventions, and 18 artifacts are registered under BOTH 'watch/inbox/...' and 'local_sovereign_agent/watch/inbox/...' (normalized key count 2). The pdf persona_priorart_2310.10158.pdf is one of them (2 rows, 1 file).
5. **Mangled-path scratch copies** - FOUND: 5 root-level files whose names are paths with separators eaten ('%TMPDIR%/pp_localllama.json' under a literal %TMPDIR% directory, 'UsersfosteAppDataLocalTempbudget.html' etc., 'watchinboxgala_20260925localfirst-steallanes_gh_search_lbrain.json') - a fetcher lost its path separators; these are copies, not holdings.
6. **Catalog stale-bytes rows** - FOUND: 4 rows record bytes that no longer match disk (file edited after registration):
   - watch/inbox/burn_reset_20260927/work/w-belt-cube-mechanism_hermes.md: catalog 1 row(s), recorded bytes [2600] vs disk 2939
   - watch/inbox/burn_reset_20260927/work/w-belt-cube-mechanism_openrouter1.md: catalog 1 row(s), recorded bytes [10060] vs disk 8751
   - watch/inbox/burn_reset_20260927/work/w-belt-cube-mechanism_openrouter2.md: catalog 1 row(s), recorded bytes [1596] vs disk 1127
   - watch/inbox/burn_reset_20260927/work/w-belt-cube-mechanism_openrouter3.md: catalog 1 row(s), recorded bytes [1372] vs disk 1486
7. **INDEX sha staleness** - FOUND: 6 INDEX-registered receipts fail sha256 recompute (edited after INDEX registration):
   - watch/inbox/CYCLE_BRIEF_NEXT.md
   - watch/inbox/ESTATE_CENSUS_20261001.md
   - watch/inbox/OFFSITE_BACKUP_PLAN_20260930.md
   - watch/inbox/STRATA_DROP_20261001.md
   - watch/inbox/VERKLE_V2_DECISION.md
   - watch/inbox/model_garden/KIMI_DOSSIER.md

## The unregistered count, named

**80 unregistered** (all 80 also scratch): 67 are the two lbrain clones' .git internals and .github config (clone support, correctly out of the corpus map), 11 are Mimosa hook-state/hook-status session jsons, 2 are __pycache__ .pyc. Verdict: no fetched primary source of value is sitting unregistered; the catalog swept the seats' fetch trail cleanly. The 54 stem-shadowed among them are the proof the dedupe-detector trap was live and avoided.

## Per-artifact inventory table

| bytes | fmt | cataloged | INDEX | location | class | fetched-by | path |
|---:|---|---|---|---|---|---|---|
| 534,980 | text | yes | no | durable-holdings | fetched-source | report_v1 desk prior-art pull (arxiv export; receipts docs/report_v1/sources/receipts/persona_priorart_*.md) | corpus/papers_reference_nonredistributable/computing_1951_m_v_wilkes_w_wheeler_s_gill_the_preparation_of_programs_for_an_electronic_digital_c.txt |
| 5,166 | text | yes | no | durable-holdings | fetched-source | report_v1 desk prior-art pull (arxiv export; receipts docs/report_v1/sources/receipts/persona_priorart_*.md) | corpus/papers_reference_nonredistributable/computing_2010_michael_d_godfrey_intro_to_edvac_first_draft.txt |
| 786,216 | pdf | yes | no | durable-holdings | fetched-source | report_v1 desk prior-art pull (arxiv export; receipts docs/report_v1/sources/receipts/persona_priorart_*.md) | corpus/papers_reference_nonredistributable/persona_priorart_2310.10158.pdf |
| 3,855,898 | pdf | yes | no | durable-holdings | fetched-source | report_v1 desk prior-art pull (arxiv export; receipts docs/report_v1/sources/receipts/persona_priorart_*.md) | corpus/papers_reference_nonredistributable/persona_priorart_2405.07248.pdf |
| 1,138,554 | pdf | yes | no | durable-holdings | fetched-source | report_v1 desk prior-art pull (arxiv export; receipts docs/report_v1/sources/receipts/persona_priorart_*.md) | corpus/papers_reference_nonredistributable/persona_priorart_2506.11798.pdf |
| 2,505,762 | pdf | yes | no | durable-holdings | fetched-source | report_v1 desk prior-art pull (arxiv export; receipts docs/report_v1/sources/receipts/persona_priorart_*.md) | corpus/papers_reference_nonredistributable/persona_priorart_2506.12657.pdf |
| 4,177,596 | pdf | yes | no | durable-holdings | fetched-source | report_v1 desk prior-art pull (arxiv export; receipts docs/report_v1/sources/receipts/persona_priorart_*.md) | corpus/papers_reference_nonredistributable/persona_priorart_2508.06149.pdf |
| 514,445 | pdf | yes | no | durable-holdings | fetched-source | report_v1 desk prior-art pull (arxiv export; receipts docs/report_v1/sources/receipts/persona_priorart_*.md) | corpus/papers_reference_nonredistributable/persona_priorart_2508.06950.pdf |
| 4,855,666 | pdf | yes | no | durable-holdings | fetched-source | report_v1 desk prior-art pull (arxiv export; receipts docs/report_v1/sources/receipts/persona_priorart_*.md) | corpus/papers_reference_nonredistributable/persona_priorart_2511.17813.pdf |
| 30,760 | text | yes | no | durable-holdings | fetched-source | descent day1 carrier (hermes_burn receipt mining) | corpus/steal/DESCENT_DAY1_STEAL_20261001.md |
| 790 | text | yes | no | durable-repo | fetched-source | mimo_v26 dataset download | data/mimo_v26/README.md |
| 13,314,620 | parquet | yes | no | durable-repo | fetched-source | mimo_v26 dataset download | data/mimo_v26/code.parquet |
| 227,632 | parquet | yes | no | durable-repo | fetched-source | mimo_v26 dataset download | data/mimo_v26/cyber.parquet |
| 3,122,244 | parquet | yes | no | durable-repo | fetched-source | mimo_v26 dataset download | data/mimo_v26/general/train.parquet |
| 495,593 | jsonl? | yes | no | durable-repo | fetched-source | mimo_v26 dataset download | data/mimo_v26/image-mapping.jsonl |
| 135,467 | parquet | yes | no | durable-repo | fetched-source | mimo_v26 dataset download | data/mimo_v26/music.parquet |
| 4,120,378 | parquet | yes | no | durable-repo | fetched-source | mimo_v26 dataset download | data/mimo_v26/webdev.parquet |
| 1,374 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/anc_frontinus-two-books-water-supply-rome-1899.md |
| 908 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/anc_vitruvius-architecture-1826.md |
| 980 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/anc_vitruvius-elements-civil-architecture-1824.md |
| 1,146 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/anchor_edison_1910_frank_lewis_dyer.md |
| 1,167 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/anchor_tesla_1919_nikola_tesla.md |
| 947 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/child_1907_wbdrummond_an_introduction_to_study.md |
| 876 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/child_1915_williambyr_study_and_training.md |
| 1,094 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/child_1928_johnbwatso_psychological_care_of_infant_and_child.md |
| 933 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/child_1929_jeanpiaget_representation_du_monde_chez_l_enfant.md |
| 851 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/child_1930_ruthmaystr_an_introduction_to_study.md |
| 967 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/child_1943_arnoldgese_infant_and_in_the_culture_of_today.md |
| 1,000 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/child_1947_viktorlowe_creative_and_mental_growth.md |
| 835 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/child_an_introduction_to_study.md |
| 984 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/child_creative_and_mental_growth.md |
| 951 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/child_infant_and_in_the_culture_of_today.md |
| 1,078 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/child_psychological_care_of_infant_and_child.md |
| 917 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/child_representation_du_monde_chez_l_enfant.md |
| 860 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/child_study_and_training.md |
| 1,204 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/computing_1936_a_m_turing_on_computable_numbers_with_an_application_to_the_entscheidungsproblem.md |
| 1,338 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/computing_1945_john_von_neumann_edvac_first_draft_document_only.md |
| 1,203 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/computing_1945_john_von_neumann_first_draft_of_a_report_on_the_edvac.md |
| 1,180 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/computing_1948_c_e_shannon_a_mathematical_theory_of_communication_part_i.md |
| 1,141 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/computing_1948_c_e_shannon_a_mathematical_theory_of_communication_part_iii.md |
| 1,337 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/computing_1951_m_v_wilkes_w_wheeler_s_gill_the_preparation_of_programs_for_an_electronic_digital_c.md |
| 1,257 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/computing_2010_michael_d_godfrey_intro_to_edvac_first_draft.md |
| 1,547 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19630012013_pdf.md |
| 1,544 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19630012013_txt.md |
| 1,454 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19660002894_pdf.md |
| 1,451 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19660002894_txt.md |
| 1,587 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19660017409_pdf.md |
| 1,584 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19660017409_txt.md |
| 1,576 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19660019469_pdf.md |
| 1,573 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19660019469_txt.md |
| 1,634 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19660020339_pdf.md |
| 1,633 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19660020339_txt.md |
| 1,555 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19660023139_pdf.md |
| 1,553 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19660023139_txt.md |
| 1,479 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19670009708_pdf.md |
| 1,476 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19670009708_txt.md |
| 1,660 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19670017082_pdf.md |
| 1,658 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19670017082_txt.md |
| 1,453 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19670026463_pdf.md |
| 1,451 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19670026463_txt.md |
| 1,463 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19670028612_pdf.md |
| 1,460 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19670028612_txt.md |
| 1,902 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19670077025_pdf.md |
| 1,904 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19670077025_txt.md |
| 1,605 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19680009847_pdf.md |
| 1,603 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19680009847_txt.md |
| 1,439 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19680014253_pdf.md |
| 1,436 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19680014253_txt.md |
| 1,510 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19680014302_pdf.md |
| 1,508 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19680014302_txt.md |
| 1,535 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19700015154_pdf.md |
| 1,532 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19700015154_txt.md |
| 1,409 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19700023966_pdf.md |
| 1,406 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19700023966_txt.md |
| 2,016 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19740021004_pdf.md |
| 2,013 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19740021004_txt.md |
| 1,924 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19750004273_pdf.md |
| 1,921 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19750004273_txt.md |
| 1,884 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19750004937_pdf.md |
| 1,881 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19750004937_txt.md |
| 1,594 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19750017915_pdf.md |
| 1,591 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19750017915_txt.md |
| 1,964 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19750021220_pdf.md |
| 1,961 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19750021220_txt.md |
| 1,592 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19760006056_pdf.md |
| 1,588 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19760006056_txt.md |
| 1,896 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19760023154_pdf.md |
| 1,893 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19760023154_txt.md |
| 1,466 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19770026109_pdf.md |
| 1,463 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19770026109_txt.md |
| 1,863 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19780004990_pdf.md |
| 1,859 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19780004990_txt.md |
| 2,065 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19780008664_pdf.md |
| 2,062 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19780008664_txt.md |
| 1,482 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19790007854_pdf.md |
| 1,479 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19790007854_txt.md |
| 1,669 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19820007835_pdf.md |
| 1,667 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19820007835_txt.md |
| 1,669 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19820008468_pdf.md |
| 1,666 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19820008468_txt.md |
| 1,742 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19860012092_pdf.md |
| 1,740 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19860012092_txt.md |
| 1,943 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19880003133_pdf.md |
| 1,941 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19880003133_txt.md |
| 1,918 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19910014756_pdf.md |
| 1,917 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19910014756_txt.md |
| 1,634 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19910018906_pdf.md |
| 1,631 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19910018906_txt.md |
| 2,051 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19930001814_pdf.md |
| 2,048 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19930001814_txt.md |
| 1,894 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19930008981_pdf.md |
| 1,893 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19930008981_txt.md |
| 1,966 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19930012218_pdf.md |
| 1,964 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19930012218_txt.md |
| 2,000 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19930013037_pdf.md |
| 1,997 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19930013037_txt.md |
| 1,703 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19930013417_pdf.md |
| 1,700 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19930013417_txt.md |
| 1,976 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19930013431_pdf.md |
| 1,975 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19930013431_txt.md |
| 1,881 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19930018610_pdf.md |
| 1,875 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19930018610_txt.md |
| 1,867 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19940012599_pdf.md |
| 1,864 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19940012599_txt.md |
| 1,924 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19940020707_pdf.md |
| 1,923 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19940020707_txt.md |
| 1,933 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19950006118_pdf.md |
| 1,930 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19950006118_txt.md |
| 2,001 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19950016829_pdf.md |
| 1,998 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19950016829_txt.md |
| 2,079 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19950017495_pdf.md |
| 2,076 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19950017495_txt.md |
| 1,608 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19980003950_pdf.md |
| 1,605 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19980003950_txt.md |
| 1,949 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19980228123_pdf.md |
| 1,948 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_19980228123_txt.md |
| 1,993 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20030016689_pdf.md |
| 1,992 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20030016689_txt.md |
| 1,995 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20040001034_pdf.md |
| 1,994 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20040001034_txt.md |
| 2,005 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20040161455_pdf.md |
| 2,001 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20040161455_txt.md |
| 2,074 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20050188505_pdf.md |
| 2,073 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20050188505_txt.md |
| 2,046 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20050205646_pdf.md |
| 2,045 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20050205646_txt.md |
| 1,906 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20060024010_pdf.md |
| 1,901 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20060024010_txt.md |
| 1,502 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20080018572_pdf.md |
| 1,501 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20080018572_txt.md |
| 1,863 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20090005159_pdf.md |
| 1,860 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20090005159_txt.md |
| 1,935 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20100014848_pdf.md |
| 1,934 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20100014848_txt.md |
| 1,939 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20100031530_pdf.md |
| 1,936 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20100031530_txt.md |
| 2,046 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20110007936_pdf.md |
| 2,045 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20110007936_txt.md |
| 1,860 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20110016777_pdf.md |
| 1,858 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20110016777_txt.md |
| 2,057 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20120013578_pdf.md |
| 2,053 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20120013578_txt.md |
| 1,862 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20140001441_pdf.md |
| 1,861 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20140001441_txt.md |
| 2,266 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20150011087_pdf.md |
| 2,265 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20150011087_txt.md |
| 1,808 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20190011733_pdf.md |
| 1,806 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20190011733_txt.md |
| 2,063 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20200001376_pdf.md |
| 2,062 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20200001376_txt.md |
| 2,060 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20200001394_pdf.md |
| 2,056 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20200001394_txt.md |
| 2,142 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20210024113_pdf.md |
| 2,143 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20210024113_txt.md |
| 2,059 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20220014634_pdf.md |
| 2,060 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20220014634_txt.md |
| 2,125 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20230012701_txt.md |
| 1,409 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20240008039_pdf.md |
| 1,411 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20240008039_txt.md |
| 1,846 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20240013198_pdf.md |
| 1,847 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20240013198_txt.md |
| 1,976 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20250000547_txt.md |
| 1,832 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20260005386_pdf.md |
| 1,835 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/nasa_20260005386_txt.md |
| 884 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/pd_siege_castle_fiction_pg14048.md |
| 843 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/pd_siege_castle_fiction_pg14851.md |
| 948 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/pd_siege_castle_fiction_pg16170.md |
| 920 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/pd_siege_castle_fiction_pg19856.md |
| 860 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/pd_siege_castle_fiction_pg20288.md |
| 874 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/pd_siege_castle_fiction_pg30172.md |
| 844 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/pd_siege_castle_fiction_pg40630.md |
| 915 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/pd_siege_castle_fiction_pg41168.md |
| 928 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/pd_siege_castle_fiction_pg46678.md |
| 949 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/pd_siege_castle_fiction_pg47197.md |
| 983 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/pd_siege_castle_fiction_pg48602.md |
| 950 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/pd_siege_castle_fiction_pg51664.md |
| 890 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/pd_siege_castle_fiction_pg54560.md |
| 996 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/pd_siege_castle_fiction_pg59253.md |
| 999 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/pd_siege_castle_fiction_pg60518.md |
| 896 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/pd_siege_castle_fiction_pg63088.md |
| 940 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/pd_siege_castle_fiction_pg73751.md |
| 917 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/pd_siege_castle_fiction_pg74739.md |
| 1,616 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/persona_priorart_2310.10158.md |
| 1,691 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/persona_priorart_2405.07248.md |
| 1,665 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/persona_priorart_2506.11798.md |
| 1,734 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/persona_priorart_2506.12657.md |
| 1,406 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/persona_priorart_2508.06149.md |
| 1,648 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/persona_priorart_2508.06950.md |
| 1,616 | text | yes | no | durable-repo | fetch-receipt | report_v1 desk (per-source retrieval receipts) | docs/report_v1/sources/receipts/persona_priorart_2511.17813.md |
| 7,348 | json | yes | no | durable-repo | instrument-output | console render instrument | memory/artifacts/console_render/show-2026-10-01T15.json |
| 4,383 | jsonl? | yes | no | durable-repo | instrument-output | animal tape collector (seat session tapes) | memory/behavioral/animals/anthropic_claude_fable_5_1.jsonl |
| 2,491 | jsonl? | yes | no | durable-repo | instrument-output | animal tape collector (seat session tapes) | memory/behavioral/animals/anthropic_claude_haiku_4_5.jsonl |
| 2,608 | jsonl? | yes | no | durable-repo | instrument-output | animal tape collector (seat session tapes) | memory/behavioral/animals/anthropic_claude_sonnet_5_5.jsonl |
| 275 | json | yes | no | durable-repo | instrument-output | animal tape collector (seat session tapes) | memory/behavioral/animals/claude_fable_5_1.jsonl |
| 374 | json | yes | no | durable-repo | instrument-output | animal tape collector (seat session tapes) | memory/behavioral/animals/deepseek.jsonl |
| 1,556 | jsonl? | yes | no | durable-repo | instrument-output | animal tape collector (seat session tapes) | memory/behavioral/animals/fireworks_ember_1.jsonl |
| 1,771 | jsonl? | yes | no | durable-repo | instrument-output | animal tape collector (seat session tapes) | memory/behavioral/animals/garden_v1_a1.jsonl |
| 327 | json | yes | no | durable-repo | instrument-output | animal tape collector (seat session tapes) | memory/behavioral/animals/gemini_flash.jsonl |
| 2,871 | jsonl? | yes | no | durable-repo | instrument-output | animal tape collector (seat session tapes) | memory/behavioral/animals/gemma2_2b_instruct_q5_k_m.jsonl |
| 5,389 | jsonl? | yes | no | durable-repo | instrument-output | animal tape collector (seat session tapes) | memory/behavioral/animals/gemma4_latest.jsonl |
| 939 | jsonl? | yes | no | durable-repo | instrument-output | animal tape collector (seat session tapes) | memory/behavioral/animals/gemma_2b.jsonl |
| 406 | json | yes | no | durable-repo | instrument-output | animal tape collector (seat session tapes) | memory/behavioral/animals/glm_5_3_flash.jsonl |
| 1,440 | jsonl? | yes | no | durable-repo | instrument-output | animal tape collector (seat session tapes) | memory/behavioral/animals/google_gemini_3_8_flash.jsonl |
| 310 | json | yes | no | durable-repo | instrument-output | animal tape collector (seat session tapes) | memory/behavioral/animals/grok_4_3.jsonl |
| 254 | json | yes | no | durable-repo | instrument-output | animal tape collector (seat session tapes) | memory/behavioral/animals/kimi.jsonl |
| 282 | json | yes | no | durable-repo | instrument-output | animal tape collector (seat session tapes) | memory/behavioral/animals/meta_muse_glimmer_30b.jsonl |
| 4,819 | jsonl? | yes | no | durable-repo | instrument-output | animal tape collector (seat session tapes) | memory/behavioral/animals/moonshotai_kimi_k2.jsonl |
| 359 | json | yes | no | durable-repo | instrument-output | animal tape collector (seat session tapes) | memory/behavioral/animals/nous_primes.jsonl |
| 396 | json | yes | no | durable-repo | instrument-output | animal tape collector (seat session tapes) | memory/behavioral/animals/qwen_flash.jsonl |
| 1,787 | jsonl? | yes | no | durable-repo | instrument-output | animal tape collector (seat session tapes) | memory/behavioral/animals/qwen_qwen3_8_max_prime.jsonl |
| 385 | json | yes | no | durable-repo | instrument-output | animal tape collector (seat session tapes) | memory/behavioral/animals/stealth_free_lanes.jsonl |
| 943 | jsonl? | yes | no | durable-repo | instrument-output | animal tape collector (seat session tapes) | memory/behavioral/animals/stealth_space_bunny_alpha.jsonl |
| 824 | jsonl? | yes | no | durable-repo | instrument-output | animal tape collector (seat session tapes) | memory/behavioral/animals/x_ai_grok_4_3.jsonl |
| 2,187 | jsonl? | yes | no | durable-repo | instrument-output | animal tape collector (seat session tapes) | memory/behavioral/animals/z_ai_glm_5_3_prime.jsonl |
| 73,998 | json | yes | no | durable-repo | estate-bookkeeping | estate bookkeeping (ribs/burns/renders) | memory/burns/verdict_enum_map.json |
| 3,567 | text | yes | no | durable-repo | estate-bookkeeping | estate bookkeeping (ribs/burns/renders) | memory/rib/RIB_DEEPSEEK_SHOULDERS_20261001.md |
| 1,714 | text | yes | no | durable-repo | estate-bookkeeping | estate bookkeeping (ribs/burns/renders) | memory/rib/RIB_GPU_LADDER_20261001.md |
| 6,519 | text | yes | no | durable-repo | estate-bookkeeping | estate bookkeeping (ribs/burns/renders) | memory/rib/RIB_INFERENCE_BUDGET_20261001.md |
| 14,802 | text | yes | no | durable-repo | estate-bookkeeping | estate bookkeeping (ribs/burns/renders) | memory/rib/RIB_MODEL_GARDEN_ROUTING.md |
| 18,059 | json | yes | no | durable-repo | estate-bookkeeping | estate bookkeeping (ribs/burns/renders) | memory/rib_boot.json |
| 2,717 | text | yes | yes:sha match | scratch-inbox | instrument-output | top-level inbox drops (seat/cron receipts) | watch/inbox/CONDUCTOR_PLAN.md |
| 4,120 | text | yes | sha-stale:SHA MISMATCH | scratch-inbox | instrument-output | top-level inbox drops (seat/cron receipts) | watch/inbox/CYCLE_BRIEF_NEXT.md |
| 3,308 | text | yes | no | scratch-inbox | instrument-output | top-level inbox drops (seat/cron receipts) | watch/inbox/DOUBLE_DROP_20261001.md |
| 46,823 | text | yes | sha-stale:SHA MISMATCH | scratch-inbox | instrument-output | top-level inbox drops (seat/cron receipts) | watch/inbox/ESTATE_CENSUS_20261001.md |
| 10,264 | text | yes | sha-stale:SHA MISMATCH | scratch-inbox | instrument-output | top-level inbox drops (seat/cron receipts) | watch/inbox/OFFSITE_BACKUP_PLAN_20260930.md |
| 2,746 | text | yes | yes:sha match | scratch-inbox | instrument-output | top-level inbox drops (seat/cron receipts) | watch/inbox/RIB_BOOT_DECISION.md |
| 3,126 | text | yes | yes:sha match | scratch-inbox | instrument-output | top-level inbox drops (seat/cron receipts) | watch/inbox/SPIKINGBRAIN_DROP_20261001.md |
| 4,236 | text | yes | sha-stale:SHA MISMATCH | scratch-inbox | instrument-output | top-level inbox drops (seat/cron receipts) | watch/inbox/STRATA_DROP_20261001.md |
| 3,460 | text | yes | yes:sha match | scratch-inbox | instrument-output | top-level inbox drops (seat/cron receipts) | watch/inbox/THE_MOUNTAIN_CLIMB_PLAN.md |
| 8,608 | text | yes | sha-stale:SHA MISMATCH | scratch-inbox | instrument-output | top-level inbox drops (seat/cron receipts) | watch/inbox/VERKLE_V2_DECISION.md |
| 287,453 | text | yes | no | scratch-inbox | instrument-output | flash50 stealth burn lane (2026-09-27 reset, f-seats) | watch/inbox/burn_reset_20260927/flash50/_w425_commits.txt |
| 2,939 | text | stale | no | scratch-inbox | instrument-output | burn_reset work lanes (hermes/openrouter/impfeed/verify by filename) | watch/inbox/burn_reset_20260927/work/w-belt-cube-mechanism_hermes.md |
| 8,751 | text | stale | no | scratch-inbox | instrument-output | burn_reset work lanes (hermes/openrouter/impfeed/verify by filename) | watch/inbox/burn_reset_20260927/work/w-belt-cube-mechanism_openrouter1.md |
| 1,127 | text | stale | no | scratch-inbox | instrument-output | burn_reset work lanes (hermes/openrouter/impfeed/verify by filename) | watch/inbox/burn_reset_20260927/work/w-belt-cube-mechanism_openrouter2.md |
| 1,486 | text | stale | no | scratch-inbox | instrument-output | burn_reset work lanes (hermes/openrouter/impfeed/verify by filename) | watch/inbox/burn_reset_20260927/work/w-belt-cube-mechanism_openrouter3.md |
| 1,010 | json | yes | no | scratch-inbox | instrument-output | burn_reset work lanes (hermes/openrouter/impfeed/verify by filename) | watch/inbox/burn_reset_20260927/work/w-belt-cube-mechanism_proposal.json |
| 3,362 | text | yes | no | scratch-inbox | instrument-output | burn_reset work lanes (hermes/openrouter/impfeed/verify by filename) | watch/inbox/burn_reset_20260927/work/w-belt-cube-mechanism_verify.md |
| 4,137 | text | yes | no | scratch-inbox | instrument-output | burn_reset work lanes (hermes/openrouter/impfeed/verify by filename) | watch/inbox/burn_reset_20260927/work/w-kabbalah-epistemics_hermes.md |
| 5,558 | text | yes | no | scratch-inbox | instrument-output | burn_reset work lanes (hermes/openrouter/impfeed/verify by filename) | watch/inbox/burn_reset_20260927/work/w-kabbalah-epistemics_openrouter1.md |
| 1,595 | text | yes | no | scratch-inbox | instrument-output | burn_reset work lanes (hermes/openrouter/impfeed/verify by filename) | watch/inbox/burn_reset_20260927/work/w-kabbalah-epistemics_openrouter2.md |
| 1,923 | text | yes | no | scratch-inbox | instrument-output | burn_reset work lanes (hermes/openrouter/impfeed/verify by filename) | watch/inbox/burn_reset_20260927/work/w-kabbalah-epistemics_openrouter3.md |
| 2,010 | text | yes | no | scratch-inbox | instrument-output | burn_reset work lanes (hermes/openrouter/impfeed/verify by filename) | watch/inbox/burn_reset_20260927/work/w-kabbalah-epistemics_verify.md |
| 2,675 | text | yes | no | scratch-inbox | instrument-output | burn_reset work lanes (hermes/openrouter/impfeed/verify by filename) | watch/inbox/burn_reset_20260927/work/w-muse-spark-access_hermes.md |
| 983 | text | yes | no | scratch-inbox | instrument-output | burn_reset work lanes (hermes/openrouter/impfeed/verify by filename) | watch/inbox/burn_reset_20260927/work/w-muse-spark-access_impfeed.md |
| 1,975 | text | yes | no | scratch-inbox | instrument-output | burn_reset work lanes (hermes/openrouter/impfeed/verify by filename) | watch/inbox/burn_reset_20260927/work/w-muse-spark-access_openrouter1.md |
| 1,049 | text | yes | no | scratch-inbox | instrument-output | burn_reset work lanes (hermes/openrouter/impfeed/verify by filename) | watch/inbox/burn_reset_20260927/work/w-muse-spark-access_openrouter2.md |
| 1,259 | text | yes | no | scratch-inbox | instrument-output | burn_reset work lanes (hermes/openrouter/impfeed/verify by filename) | watch/inbox/burn_reset_20260927/work/w-muse-spark-access_openrouter3.md |
| 2,777 | text | yes | no | scratch-inbox | instrument-output | burn_reset work lanes (hermes/openrouter/impfeed/verify by filename) | watch/inbox/burn_reset_20260927/work/w-muse-spark-access_verify.md |
| 2,710 | text | yes | no | scratch-inbox | instrument-output | burn_reset work lanes (hermes/openrouter/impfeed/verify by filename) | watch/inbox/burn_reset_20260927/work/w-nelson-shuffle_hermes.md |
| 3,067 | text | yes | no | scratch-inbox | instrument-output | burn_reset work lanes (hermes/openrouter/impfeed/verify by filename) | watch/inbox/burn_reset_20260927/work/w-nelson-shuffle_hermes_verify.md |
| 2,179 | text | yes | no | scratch-inbox | instrument-output | burn_reset work lanes (hermes/openrouter/impfeed/verify by filename) | watch/inbox/burn_reset_20260927/work/w-nelson-shuffle_openrouter1.md |
| 978 | text | yes | no | scratch-inbox | instrument-output | burn_reset work lanes (hermes/openrouter/impfeed/verify by filename) | watch/inbox/burn_reset_20260927/work/w-nelson-shuffle_openrouter2.md |
| 1,580 | text | yes | no | scratch-inbox | instrument-output | burn_reset work lanes (hermes/openrouter/impfeed/verify by filename) | watch/inbox/burn_reset_20260927/work/w-nelson-shuffle_openrouter3.md |
| 1,956 | text | yes | no | scratch-inbox | instrument-output | burn_reset work lanes (hermes/openrouter/impfeed/verify by filename) | watch/inbox/burn_reset_20260927/work/w-nelson-shuffle_verify.md |
| 3,055 | text | yes | no | scratch-inbox | instrument-output | burn_reset work lanes (hermes/openrouter/impfeed/verify by filename) | watch/inbox/burn_reset_20260927/work/w-water-display_hermes.md |
| 7,990 | text | yes | no | scratch-inbox | instrument-output | burn_reset work lanes (hermes/openrouter/impfeed/verify by filename) | watch/inbox/burn_reset_20260927/work/w-water-display_openrouter1.md |
| 1,472 | text | yes | no | scratch-inbox | instrument-output | burn_reset work lanes (hermes/openrouter/impfeed/verify by filename) | watch/inbox/burn_reset_20260927/work/w-water-display_openrouter2.md |
| 2,248 | text | yes | no | scratch-inbox | instrument-output | burn_reset work lanes (hermes/openrouter/impfeed/verify by filename) | watch/inbox/burn_reset_20260927/work/w-water-display_openrouter3.md |
| 1,726 | text | yes | no | scratch-inbox | instrument-output | burn_reset work lanes (hermes/openrouter/impfeed/verify by filename) | watch/inbox/burn_reset_20260927/work/w-water-display_verify.md |
| 11,526 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/lens/burns.md |
| 3,949 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/lens/corpus.md |
| 5,992 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/lens/doors.md |
| 4,223 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/lens/graph.md |
| 23,107 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/lens/laws.md |
| 20,610 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/lens/questions.md |
| 13,960 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/steal/agent-memory-continuity.md |
| 16,278 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/steal/kv-cache-context-engineering.md |
| 9,362 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/steal/open-and-local-language-models-x.md |
| 15,747 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/steal/open-and-local-language-models.md |
| 14,593 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/steal/quantization-compression.md |
| 892 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/_html2txt.py |
| 189,908 | text | yes | no | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/_ll_top.json |
| 323,662 | html | yes | no | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/_localllama_top.json |
| 1,311 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/_parse_arxiv.py |
| 191 | json | yes | no | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/_pp_quant_month.json |
| 3,143 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/_pullpush_fetch.py |
| 156,269 | text | yes | no | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/_rss_localllm.xml |
| 0 | text | yes | no | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/_rss_ml.xml |
| 0 | text | yes | no | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/_rss_ollama.xml |
| 137,683 | text | yes | no | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/_rss_quant_month.xml |
| 56,509 | text | yes | no | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/_rss_tak_comments.xml |
| 0 | text | yes | no | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/_rss_taskaware_comments.xml |
| 17,734 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/agent-memory-continuity-arxiv.md |
| 12,112 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/agent-memory-continuity-hn.md |
| 10,369 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/agent-memory-continuity-reddit.md |
| 16,542 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/agent-memory-continuity-x.md |
| 17,623 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/evals-self-improvement-arxiv.md |
| 19,867 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/evals-self-improvement-hn.md |
| 30,982 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/evals-self-improvement-reddit.md |
| 21,776 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/evals-self-improvement-x.md |
| 12,687 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/finetuning-adaptation-arxiv.md |
| 17,173 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/finetuning-adaptation-hn.md |
| 16,028 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/finetuning-adaptation-reddit.md |
| 15,008 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/finetuning-adaptation-x.md |
| 13,131 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/inference-efficiency-arxiv.md |
| 12,433 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/inference-efficiency-hn.md |
| 13,089 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/inference-efficiency-reddit.md |
| 18,437 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/inference-efficiency-x.md |
| 18,774 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/kv-cache-context-engineering-arxiv.md |
| 10,809 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/kv-cache-context-engineering-hn.md |
| 17,488 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/kv-cache-context-engineering-reddit.md |
| 16,606 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/kv-cache-context-engineering-x.md |
| 19,121 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/open-and-local-language-models-arxiv.md |
| 14,454 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/open-and-local-language-models-hn.md |
| 15,387 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/open-and-local-language-models-reddit.md |
| 19,431 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/open-and-local-language-models-x.md |
| 20,718 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/quantization-compression-arxiv.md |
| 16,148 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/quantization-compression-hn.md |
| 15,216 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/quantization-compression-reddit.md |
| 18,360 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/quantization-compression-x.md |
| 12,907 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/swarm-orchestration-arxiv.md |
| 11,180 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/swarm-orchestration-hn.md |
| 25,576 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/swarm-orchestration-reddit.md |
| 16,295 | text | yes | yes:sha match | scratch-inbox | instrument-output | frontier olm mine day sweep (2026-09-30 dig) | watch/inbox/frontier_olm_2026-09-30/sweep/swarm-orchestration-x.md |
| 6,414 | text | yes | no | scratch-inbox | instrument-output | gala_20260925 sibling lanes (receipts/digests) | watch/inbox/gala_20260925/librarian-expedition/extract_citations.py |
| 46,381 | json | yes | no | scratch-inbox | instrument-output | gala_20260925 sibling lanes (receipts/digests) | watch/inbox/gala_20260925/librarian-expedition/lanes/citations_raw.json |
| 1,045 | json | yes | no | scratch-inbox | instrument-output | gala_20260925 sibling lanes (receipts/digests) | watch/inbox/gala_20260925/librarian-expedition/lanes/cited-missing.json |
| 588 | text | yes | no | scratch-inbox | instrument-output | gala_20260925 sibling lanes (receipts/digests) | watch/inbox/gala_20260925/librarian-expedition/lanes/holdings-doctrine.check.txt |
| 9,118 | json | yes | no | scratch-inbox | instrument-output | gala_20260925 sibling lanes (receipts/digests) | watch/inbox/gala_20260925/librarian-expedition/lanes/instrument-audit.json |
| 407 | json | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/.mimosa/hook-status/sess_dwf-dwfrun-c0bb7c4b-86da-4d0c-97b3-fbacab475b1d-actor_1_4-b3dc09fdd9.json |
| 2,191,864 | gzip | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/continuous-ai-main.tar.gz |
| 11,220 | binary-unknown | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/continuous-ai-main/__pycache__/eval_battery.cpython-311.pyc |
| 58 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/fetched/ownmem/.gitignore |
| 218 | json | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/fetched/ownmem/.mimosa/hook-state/sess_dwf-dwfrun-c0bb7c4b-86da-4d0c-97b3-fbacab475b1d-actor_1_1.json |
| 508 | json | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/fetched/ownmem/.mimosa/hook-status/sess_dwf-dwfrun-c0bb7c4b-86da-4d0c-97b3-fbacab475b1d-actor_1_1-2e5bc77f7e.json |
| 611 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/fetched/ownmem/.ownmem_MEMORY-general.md |
| 41 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/fetched/ownmem/.ownmem_MEMORY.md |
| 2,176 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/fetched/ownmem/.ownmem_ci_latency_lock_needs_machine_scaling.md |
| 209 | json | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/fetched/ownmem/.ownmem_config.json |
| 74 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/fetched/ownmem/.ownmem_index_previous-v1 |
| 3,324 | json | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/fetched/ownmem/.ownmem_index_snapshots_f03c1cb532c12a145a109fd420868f5919a04d53ea5b914b597436e25cc9ac2e_manifest.json |
| 74 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/fetched/ownmem/.ownmem_index_v1 |
| 14,769 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/fetched/ownmem/README.md |
| 5,969 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/fetched/ownmem/docs_ARCHITECTURE.md |
| 871 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/fetched/ownmem/docs_MEMORY_INSTRUCTIONS.md |
| 3,892 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/fetched/ownmem/docs_PRIVACY.md |
| 16,025 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/fetched/ownmem/docs_TECHNICAL.md |
| 2,508 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/fetched/ownmem/lib_features_compiler.mjs |
| 40,033 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/fetched/ownmem/lib_features_recall.mjs |
| 16,009 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/fetched/ownmem/lib_memory-index-store.mjs |
| 29,216 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/fetched/ownmem/lib_memory-query-planner.mjs |
| 43,675 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/fetched/ownmem/lib_memory-ranker.mjs |
| 25,131 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/fetched/ownmem/lib_memory-trust-store.mjs |
| 6,002 | json | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/fetched/ownmem/repo_meta.json |
| 5,501 | json | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/fetched/ownmem/schemas_index_manifest.schema.json |
| 67,554 | json | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/fetched/ownmem/tree.json |
| 218 | json | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/.mimosa/hook-state/sess_dwf-dwfrun-c0bb7c4b-86da-4d0c-97b3-fbacab475b1d-actor_1_2.json |
| 477 | json | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/.mimosa/hook-status/sess_dwf-dwfrun-c0bb7c4b-86da-4d0c-97b3-fbacab475b1d-actor_1_2-1e5e22704b.json |
| 14,655 | text | yes | yes:sha match | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/_adjacent_append.py |
| 5,522 | text | yes | yes:sha match | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/_adjacent_check.py |
| 2,283 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/adjacent.check.txt |
| 3,804 | json | yes | yes:sha match | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/adjacent.json |
| 25,599 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/aida.check.txt |
| 11,978 | json | yes | yes:sha match | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/aida.json |
| 9,632 | text | yes | yes:sha match | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/aida_register_row.py |
| 1,135 | text | yes | yes:sha match | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/aida_row_verify.py |
| 5,628 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/atlas.check.txt |
| 10,797 | json | yes | yes:sha match | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/atlas.json |
| 8,436 | text | yes | yes:sha match | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/evidence/atlas_excerpts.md |
| 669 | json | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/.mimosa/hook-state/sess_dwf-dwfrun-c0bb7c4b-86da-4d0c-97b3-fbacab475b1d-actor_1_7.json |
| 533 | json | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/.mimosa/hook-status/sess_dwf-dwfrun-c0bb7c4b-86da-4d0c-97b3-fbacab475b1d-actor_1_7-fb5b0a79ee.json |
| 934 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/SHA256SUMS.txt |
| 26,484 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/anythingllm.readme.md |
| 18,223 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/cognee.readme.md |
| 28,280 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/graphiti.readme.md |
| 15,935 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/groundmemory.readme.md |
| 6,182 | json | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/groundmemory.repo.json |
| 4,701 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/khoj.readme.md |
| 88,685 | json | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/gh_search_lbrain.json |
| 21 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/HEAD |
| 319 | jsonl? | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/config |
| 73 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/description |
| 478 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/hooks/applypatch-msg.sample |
| 1,972 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/hooks/commit-msg.sample |
| 4,611 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/hooks/fsmonitor-watchman.sample |
| 189 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/hooks/post-update.sample |
| 424 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/hooks/pre-applypatch.sample |
| 1,649 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/hooks/pre-commit.sample |
| 416 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/hooks/pre-merge-commit.sample |
| 1,374 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/hooks/pre-push.sample |
| 4,898 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/hooks/pre-rebase.sample |
| 544 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/hooks/pre-receive.sample |
| 1,492 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/hooks/prepare-commit-msg.sample |
| 2,783 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/hooks/push-to-checkout.sample |
| 2,308 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/hooks/sendemail-validate.sample |
| 3,650 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/hooks/update.sample |
| 3,630 | binary-unknown | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/index |
| 240 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/info/exclude |
| 209 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/logs/HEAD |
| 209 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/logs/refs/heads/main |
| 209 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/logs/refs/remotes/origin/HEAD |
| 2,416 | binary-unknown | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/objects/pack/pack-7357d2be2463c3d87cf7b7ae897ccfaeff49fe09.idx |
| 22,215 | binary-unknown | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/objects/pack/pack-7357d2be2463c3d87cf7b7ae897ccfaeff49fe09.pack |
| 244 | binary-unknown | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/objects/pack/pack-7357d2be2463c3d87cf7b7ae897ccfaeff49fe09.rev |
| 112 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/packed-refs |
| 41 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/refs/heads/main |
| 30 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/refs/remotes/origin/HEAD |
| 41 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/refs/tags/v0.1.3 |
| 41 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.git/shallow |
| 148 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/.gitignore |
| 1,535 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/LICENSE |
| 696 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/PASTE-TO-YOUR-AGENT.md |
| 3,509 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/README.md |
| 365 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/bin/cli.js |
| 191 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/lbrain_agents/__init__.py |
| 96 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/lbrain_agents/__main__.py |
| 5,545 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/lbrain_agents/cli.py |
| 16,690 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/lbrain_agents/installer.py |
| 820 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/lbrain_agents/mcp_entry.py |
| 129 | json | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/lbrain_agents/share/agent-plugin/mcp.json |
| 498 | json | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/lbrain_agents/share/agent-plugin/plugin.json |
| 1,004 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/lbrain_agents/share/agent-plugin/skills/lbrain-memory/SKILL.md |
| 1,660 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/lbrain_agents/share/cookbooks/01-abstain.md |
| 888 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/lbrain_agents/share/cookbooks/02-superseded.md |
| 1,112 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/lbrain_agents/share/cookbooks/03-model-swap.md |
| 181 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/lbrain_agents/share/cookbooks/toy-lair/deploy-runbook-2025-09-14.md |
| 309 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/lbrain_agents/share/cookbooks/toy-lair/deploy-runbook-2026-03-02.md |
| 267 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/lbrain_agents/share/cookbooks/toy-lair/metrics-exporter-2026-01-10.md |
| 923 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/lbrain_agents/share/docs/openclaw.md |
| 479 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/lbrain_agents/share/hooks/session-start.sh |
| 2,517 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/lbrain_agents/share/skills/lbrain-memory/SKILL.md |
| 3,698 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/lbrain_agents/wrap.py |
| 442 | json | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/package.json |
| 1,206 | jsonl? | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/pyproject.toml |
| 669 | json | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/server.json |
| 0 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/tests/__init__.py |
| 4,685 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/tests/test_installer.py |
| 18 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/vscode/.vscodeignore |
| 526 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/vscode/README.md |
| 879 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/vscode/extension.js |
| 806 | json | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain-coding-agents/vscode/package.json |
| 157 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.dockerignore |
| 775 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.env.example |
| 21 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.git/HEAD |
| 305 | jsonl? | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.git/config |
| 73 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.git/description |
| 478 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.git/hooks/applypatch-msg.sample |
| 1,972 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.git/hooks/commit-msg.sample |
| 4,611 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.git/hooks/fsmonitor-watchman.sample |
| 189 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.git/hooks/post-update.sample |
| 424 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.git/hooks/pre-applypatch.sample |
| 1,649 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.git/hooks/pre-commit.sample |
| 416 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.git/hooks/pre-merge-commit.sample |
| 1,374 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.git/hooks/pre-push.sample |
| 4,898 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.git/hooks/pre-rebase.sample |
| 544 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.git/hooks/pre-receive.sample |
| 1,492 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.git/hooks/prepare-commit-msg.sample |
| 2,783 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.git/hooks/push-to-checkout.sample |
| 2,308 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.git/hooks/sendemail-validate.sample |
| 3,650 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.git/hooks/update.sample |
| 19,834 | binary-unknown | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.git/index |
| 240 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.git/info/exclude |
| 195 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.git/logs/HEAD |
| 195 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.git/logs/refs/heads/main |
| 195 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.git/logs/refs/remotes/origin/HEAD |
| 7,372 | binary-unknown | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.git/objects/pack/pack-b381782219dc4015cafb01ce540f445c16598ea7.idx |
| 1,368,221 | binary-unknown | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.git/objects/pack/pack-b381782219dc4015cafb01ce540f445c16598ea7.pack |
| 952 | binary-unknown | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.git/objects/pack/pack-b381782219dc4015cafb01ce540f445c16598ea7.rev |
| 112 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.git/packed-refs |
| 41 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.git/refs/heads/main |
| 30 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.git/refs/remotes/origin/HEAD |
| 41 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.git/shallow |
| 2,867 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.github/ISSUE_TEMPLATE/bug_report.yml |
| 425 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.github/ISSUE_TEMPLATE/config.yml |
| 1,559 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.github/ISSUE_TEMPLATE/install_problem.yml |
| 205,487 | binary-unknown | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.github/assets/fable-avatar.png |
| 1,425 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.github/workflows/ci.yml |
| 9,516 | text | no | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.github/workflows/release.yml |
| 357 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/.gitignore |
| 9,945 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/AGENTS.md |
| 35,806 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/CHANGELOG.md |
| 5,569 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/CONTRIBUTING.md |
| 2,974 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/CONTRIBUTORS.md |
| 1,670 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/Dockerfile |
| 1,535 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/LICENSE |
| 9,033 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/README-DRAFT-v2.md |
| 20,994 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/README.md |
| 1,055 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/RELEASE-REQUIRES |
| 4,265 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/RELEASING.md |
| 2,674 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/bench/ab_search.py |
| 2,951 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/contrib/hooks/README.md |
| 718 | json | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/contrib/hooks/hooks.snippet.json |
| 7,111 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/contrib/hooks/lbrain-capture.sh |
| 8,869 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/contrib/hooks/lbrain-heartbeat.sh |
| 4,018 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/contrib/hooks/nc-14-capture-extracts-text.py |
| 2,597 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/contrib/lbrain-proxy/README.md |
| 3,614 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/contrib/lbrain-proxy/main.py |
| 63 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/contrib/lbrain-proxy/requirements.txt |
| 3,315 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/docker-compose.kite.yml |
| 11,335 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/docs/BACKUP-AND-RESTORE.md |
| 12,240 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/docs/DESIGN-binding-aware-serving.md |
| 11,567 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/docs/DESIGN-evidence-grading.md |
| 8,563 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/docs/DESIGN-gcx-authority-verification.md |
| 7,607 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/docs/DESIGN-manifest-scoped-views.md |
| 6,580 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/docs/DESIGN-modules.md |
| 13,621 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/docs/DEVELOPER-NOTES.md |
| 4,957 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/docs/KEYS.md |
| 4,450 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/docs/SCAFFOLDING.md |
| 3,731 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/docs/UPGRADING.md |
| 308,572 | binary-unknown | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/docs/assets/lbrain-emblem.jpg |
| 229,063 | binary-unknown | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/docs/assets/lbrain-lockup.jpg |
| 2,507 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/docs/lair-framework/README.md |
| 820 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/examples/README-demo-corpus.md |
| 171 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/examples/demo-abstention.tape |
| 136 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/examples/demo-corpus/caching-notes.md |
| 206 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/examples/demo-corpus/deploy-flag-update.md |
| 124 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/examples/demo-corpus/deploy-flag.md |
| 214 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/examples/demo-corpus/postgres-choice.md |
| 218 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/examples/demo-corpus/redis-evaluation.md |
| 54 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/examples/demo-corpus/team-lunch.md |
| 286 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/examples/demo.tape |
| 1,610 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/A506-DO-NOT-PUBLISH-BEFORE-FILING.md |
| 158 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/__init__.py |
| 8,454 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/admissibility.py |
| 12,720 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/amp.py |
| 1,415 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/archive/__init__.py |
| 28,756 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/archive/archiver.py |
| 24,857 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/archive/cli.py |
| 1,624 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/archive/config.py |
| 8,363 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/archive/crypto.py |
| 2,812 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/archive/mcp.py |
| 8,297 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/archive/storage.py |
| 27,775 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/beliefs.py |
| 128,911 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/cli.py |
| 24,357 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/config.py |
| 15,210 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/consolidate.py |
| 12,858 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/dialin.py |
| 25,434 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/disclosure.py |
| 10,458 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/embed.py |
| 26,779 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/epoch.py |
| 38,736 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/epoch_build.py |
| 10,399 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/framework/AUTHORING_DISCIPLINE.md |
| 13,270 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/framework/FAST_START_PROTOCOL.md |
| 4,244 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/framework/LAIR_RULES.md |
| 1,893 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/framework/LAIR_TEMPLATE.md |
| 15,438 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/framework/SELF_FILLING_PROTOCOL.md |
| 1,335 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/framework/__init__.py |
| 17,033 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/gcx.py |
| 7,368 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/grading.py |
| 11,781 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/identity.py |
| 35,237 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/index.py |
| 9,505 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/index_currency.py |
| 14,718 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/lair_from_repo.py |
| 13,065 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/lair_protocol.py |
| 26,138 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/mcp_server.py |
| 12,933 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/modules/__init__.py |
| 1,105 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/modules/role-continuity/README.md |
| 371 | jsonl? | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/modules/role-continuity/module.toml |
| 1,252 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/modules/role-continuity/questions/001-standing-state.md |
| 1,185 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/modules/role-continuity/questions/002-decisions-and-reasons.md |
| 1,297 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/modules/role-continuity/questions/003-commitments-and-relationships.md |
| 2,037 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/modules/role-continuity/questions/004-the-boundary.md |
| 5,297 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/onboard.py |
| 3,303 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/plugins.py |
| 1,843 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/presentation.py |
| 2,806 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/rerank.py |
| 51,401 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/search.py |
| 9,232 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/selftest.py |
| 35,685 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/serve.py |
| 10,102 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/spool.py |
| 11,300 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/staleness.py |
| 54,449 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/store.py |
| 3,973 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/telemetry.py |
| 5,702 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/lbrain/write_gates.py |
| 3,769 | jsonl? | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/pyproject.toml |
| 163 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/release-consumers.txt |
| 3,554 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/scripts/check-ip-boundary.sh |
| 230 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/scripts/git-hooks/pre-commit |
| 4,840 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/scripts/lbrain-backup.sh |
| 1,067 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/scripts/lbrain-mcp |
| 3,920 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/scripts/lbrain-restore.sh |
| 7,153 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/scripts/release-preflight.sh |
| 3,102 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/scripts/release.sh |
| 5,432 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/scripts/release_gate.sh |
| 2,710 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/_coldembed.py |
| 8,704 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/conftest.py |
| 1,884 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_a3_b4_case_fold_when_unique.py |
| 7,541 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_a3_dual_declaration_renders_corroborated.py |
| 6,268 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_a3_retired_names_its_correction.py |
| 3,872 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_a3_serve_layer_location_axis.py |
| 4,109 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_a592_epoch_home_recognition.py |
| 1,645 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_admissibility.py |
| 9,575 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_anti_pattern_detection.py |
| 10,797 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_archive.py |
| 3,859 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_backup_script_both_home_shapes.py |
| 30,903 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_beliefs.py |
| 18,274 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_capture_spool.py |
| 1,710 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_chunker_special_tokens.py |
| 11,339 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_chunker_version.py |
| 3,149 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_chunking_tables.py |
| 17,685 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_claim_date_reaches_serve.py |
| 3,175 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_claim_span_dual_view.py |
| 7,550 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_config_roundtrip.py |
| 2,935 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_core_session_serve.py |
| 1,713 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_current_only_reachable.py |
| 4,270 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_dedupe_identity.py |
| 5,609 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_dialin.py |
| 40,617 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_disclosure.py |
| 2,349 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_dual_view_current_only.py |
| 3,521 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_embed_reuse.py |
| 1,820 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_engine_stamp_bound_at_import.py |
| 787 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_engine_stamp_in_footer.py |
| 11,776 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_epoch_2d_gap_closures.py |
| 10,688 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_epoch_build.py |
| 8,385 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_epoch_cso_red.py |
| 8,160 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_epoch_protocol.py |
| 8,687 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_epoch_reader.py |
| 10,811 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_evidence_grading.py |
| 2,268 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_exclude_path_markers.py |
| 4,138 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_framework_ships.py |
| 13,728 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_gcx_authority.py |
| 4,748 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_gcx_refusal.py |
| 7,221 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_gcx_resolve.py |
| 4,859 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_heading_ancestry.py |
| 5,400 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_human_facing_register.py |
| 5,686 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_identity_register.py |
| 3,102 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_identity_verification.py |
| 9,327 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_import_reconcile_a591.py |
| 10,927 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_index_currency.py |
| 2,237 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_init_provider_notes.py |
| 3,220 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_integrator_enclave.py |
| 1,981 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_lair_from_repo_graph.py |
| 2,338 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_lair_protocol.py |
| 5,380 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_mcp_disclosure_seam.py |
| 14,480 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_modules.py |
| 4,544 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_multisource_relpath_collision.py |
| 5,790 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_plugins.py |
| 1,528 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_presentation.py |
| 4,404 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_provider_fail_closed.py |
| 2,709 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_prune_scope.py |
| 6,700 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_prune_unreachable.py |
| 1,539 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_prune_unreachable_case_live.py |
| 15,123 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_ranking.py |
| 10,347 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_reconcile_5b_gap_closures.py |
| 4,559 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_record_date_utc_frame.py |
| 1,284 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_renaming_is_not_retiring.py |
| 4,080 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_restore_script_config_db_pair.py |
| 1,306 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_rsi_build_provenance.py |
| 3,344 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_rsi_confusables.py |
| 906 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_rsi_currency_unreachable.py |
| 3,399 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_rsi_doctrine_heading.py |
| 4,920 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_rsi_supersede_collision.py |
| 7,404 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_rsi_supersession.py |
| 1,545 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_rsi_tiktoken_lazy.py |
| 4,863 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_runtime_vintage_in_identity.py |
| 28,874 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_security_redteam_2026_07_28.py |
| 2,461 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_selftest.py |
| 21,767 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_serve.py |
| 19,234 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_spool_sweep.py |
| 9,596 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_spool_sweep_e2e.py |
| 2,447 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_sqlite_extension_guard.py |
| 5,787 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_staleness.py |
| 6,690 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_status_retired_at_serve_time.py |
| 4,361 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_supersession.py |
| 4,054 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_telemetry.py |
| 3,342 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_transcript_snapshot.py |
| 2,718 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_unprovisioned_mcp.py |
| 2,059 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_version_is_single_sourced.py |
| 1,240 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_version_single_truth.py |
| 7,962 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_write_gates_unit.py |
| 11,571 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/lbrain/lbrain/tests/test_write_path_gates.py |
| 9,696 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/letta-code.readme.md |
| 75,901 | html | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/letta-docs-memory.html |
| 1,574 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/letta.readme.md |
| 11,914 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/mem0.readme.md |
| 42,540 | html | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/memgpt-abstract.html |
| 1,261 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/memgpt-abstract.txt |
| 8,052 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/memmachine.readme.md |
| 16,018 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/people-context.readme.md |
| 3,362 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/fetched/zep.readme.md |
| 13,132 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/lbrain.check.txt |
| 8,763 | json | yes | yes:sha match | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/lbrain.json |
| 3,211 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/ownmem.check.txt |
| 5,762 | json | yes | yes:sha match | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/ownmem.json |
| 3,226 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/pam.check.txt |
| 8,345 | json | yes | yes:sha match | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/pam.json |
| 3,156 | text | yes | no | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/ragos.check.txt |
| 9,383 | json | yes | yes:sha match | scratch-inbox | fetched-source | localfirst-steal gala lanes (herald seat; clones/tarball/readmes) | watch/inbox/gala_20260925/localfirst-steal/lanes/ragos.json |
| 821 | json | no | no | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/.mimosa/hook-state/sess_dwf-dwfrun-c8c03b09-0b74-46de-b4e5-7add111b079c-actor_1_1.json |
| 8,670 | text | no | no | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/.mimosa/hook-state/sess_dwf-dwfrun-c8c03b09-0b74-46de-b4e5-7add111b079c-actor_1_1.mupf5ivz-29448-a72f23c46e.baseline/f3556de320683793ba43f124d86656719ed590c7023d28c4763f2fe8d9b35f56.source |
| 218 | json | no | no | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/.mimosa/hook-state/sess_dwf-dwfrun-c8c03b09-0b74-46de-b4e5-7add111b079c-actor_1_3.json |
| 218 | json | no | no | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/.mimosa/hook-state/sess_dwf-dwfrun-c8c03b09-0b74-46de-b4e5-7add111b079c-actor_3_1.json |
| 1,034 | json | no | no | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/.mimosa/hook-status/sess_dwf-dwfrun-c8c03b09-0b74-46de-b4e5-7add111b079c-actor_1_1-cfba7c28d3.json |
| 411 | json | no | no | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/.mimosa/hook-status/sess_dwf-dwfrun-c8c03b09-0b74-46de-b4e5-7add111b079c-actor_1_3-530dd80443.json |
| 23,526 | binary-unknown | no | no | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/__pycache__/audio_dna_scan.cpython-311.pyc |
| 36,103 | json | yes | no | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/artifacts/style-synthesis.profile.json |
| 4,236 | text | yes | no | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/audio-dna.check.txt |
| 1,640 | json | yes | yes:sha match | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/audio-dna.json |
| 13,838 | text | yes | yes:sha match | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/audio_dna_scan.py |
| 1,863 | jsonl? | yes | no | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/cutter-disco.check.txt |
| 6,933 | json | yes | yes:sha match | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/cutter-disco.json |
| 2,921 | text | yes | no | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/cutter-electro.check.txt |
| 7,962 | json | yes | yes:sha match | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/cutter-electro.json |
| 4,476 | text | yes | yes:sha match | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/cutter_disco_check.py |
| 7,814 | text | yes | yes:sha match | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/cutter_electro_check.py |
| 1,367 | text | yes | no | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/electro_subset_calc.txt |
| 13,565 | text | yes | yes:sha match | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/filer_links_append.py |
| 16,821 | text | yes | no | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/remix-mechanics.check.txt |
| 11,270 | json | yes | yes:sha match | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/remix-mechanics.json |
| 1,945 | text | yes | no | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/remix-mechanics.quotes.txt |
| 1,424 | text | yes | no | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/remix-mechanics.verify.txt |
| 18,807 | text | yes | yes:sha match | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/remix_scan.py |
| 4,759 | text | yes | yes:sha match | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/style-synthesis.check.py |
| 1,337 | text | yes | no | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/style-synthesis.check.txt |
| 22,409 | text | yes | no | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/style-synthesis.gitstatus.txt |
| 5,490 | json | yes | yes:sha match | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/style-synthesis.json |
| 7,424 | text | yes | yes:sha match | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/style-synthesis.profile.py |
| 30,010 | text | yes | no | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/taxonomy.check.txt |
| 5,993 | json | yes | yes:sha match | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/taxonomy.json |
| 10,111 | text | yes | yes:sha match | scratch-inbox | instrument-output | music-ractor gala lanes | watch/inbox/gala_20260925/music-ractor/lanes/taxonomy_scan.py |
| 16,660 | text | yes | no | scratch-inbox | instrument-output | top-level inbox drops (seat/cron receipts) | watch/inbox/gap_analysis_20261001/GAP_REGISTER.md |
| 4,675 | text | yes | no | scratch-inbox | instrument-output | descent burn carrier outputs | watch/inbox/hermes_burn/DUEL2_train_04_r2.md |
| 1,222 | text | yes | no | scratch-inbox | instrument-output | descent burn carrier outputs | watch/inbox/hermes_burn/DUEL2_train_05_r2.md |
| 818 | text | yes | no | scratch-inbox | instrument-output | descent burn carrier outputs | watch/inbox/hermes_burn/DUEL2_train_06_r2.md |
| 8,062 | text | yes | no | scratch-inbox | instrument-output | descent burn carrier outputs | watch/inbox/hermes_burn/DUEL2_train_07_r2.md |
| 6,750 | text | yes | no | scratch-inbox | instrument-output | descent burn carrier outputs | watch/inbox/hermes_burn/DUEL2_train_08_r2.md |
| 11,302 | text | yes | no | scratch-inbox | instrument-output | descent burn carrier outputs | watch/inbox/hermes_burn/DUEL2_train_09_r2.md |
| 2,712 | text | yes | no | scratch-inbox | instrument-output | descent burn carrier outputs | watch/inbox/hermes_burn/DUEL2_train_10_r2.md |
| 7,944 | text | yes | no | scratch-inbox | instrument-output | descent burn carrier outputs | watch/inbox/hermes_burn/DUEL2_train_11_r2.md |
| 12,698 | text | yes | no | scratch-inbox | instrument-output | descent burn carrier outputs | watch/inbox/hermes_burn/DUEL2_train_12_r2.md |
| 8,835 | text | yes | no | scratch-inbox | instrument-output | descent burn carrier outputs | watch/inbox/hermes_burn/DUEL2_train_13_r2.md |
| 6,573 | text | yes | no | scratch-inbox | instrument-output | descent burn carrier outputs | watch/inbox/hermes_burn/DUEL2_train_14_r2.md |
| 6,129 | text | yes | no | scratch-inbox | instrument-output | descent burn carrier outputs | watch/inbox/hermes_burn/DUEL_JUDGE2.md |
| 5,709 | text | yes | no | scratch-inbox | instrument-output | descent burn carrier outputs | watch/inbox/hermes_burn/N1R_parables_songmap.md |
| 31,295 | text | yes | no | scratch-inbox | instrument-output | seats-inventory lane (this inventory) | watch/inbox/librarian_exp/adds_all.txt |
| 17,724 | text | yes | no | scratch-inbox | instrument-output | seats-inventory lane (this inventory) | watch/inbox/librarian_exp/root_adds.txt |
| 57,789 | text | yes | no | scratch-inbox | instrument-output | seats-inventory lane (this inventory) | watch/inbox/librarian_exp/trail_listing_raw.txt |
| 7,969 | text | yes | yes:sha match | scratch-inbox | instrument-output | localfirst dig (stealth lane digests) | watch/inbox/localfirst/adjacent.md |
| 16,185 | text | yes | yes:sha match | scratch-inbox | instrument-output | localfirst dig (stealth lane digests) | watch/inbox/localfirst/aida.md |
| 15,776 | text | yes | yes:sha match | scratch-inbox | instrument-output | localfirst dig (stealth lane digests) | watch/inbox/localfirst/atlas.md |
| 14,444 | text | yes | yes:sha match | scratch-inbox | instrument-output | localfirst dig (stealth lane digests) | watch/inbox/localfirst/lbrain.md |
| 16,046 | text | yes | yes:sha match | scratch-inbox | instrument-output | localfirst dig (stealth lane digests) | watch/inbox/localfirst/ownmem.md |
| 7,880 | text | yes | yes:sha match | scratch-inbox | instrument-output | localfirst dig (stealth lane digests) | watch/inbox/localfirst/pam.md |
| 2,893 | text | yes | yes:sha match | scratch-inbox | instrument-output | localfirst dig (stealth lane digests) | watch/inbox/localfirst/probe_ragos_fingerprint.py |
| 9,191 | text | yes | yes:sha match | scratch-inbox | instrument-output | localfirst dig (stealth lane digests) | watch/inbox/localfirst/ragos.md |
| 170 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/A1_B6_ask_frozen.md |
| 576 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/A1_B8_ask_frozen.md |
| 43,296 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/B7_material_queue_tail_frozen.md |
| 22,555 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/BATTERY.md |
| 11,664 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/CENSUS.md |
| 6,325 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/ECON.md |
| 7,009 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/FABLE1.md |
| 3,384 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/GARDEN_RACTOR.md |
| 11,971 | json | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/GRID_ANTHROPIC1.json |
| 23,185 | json | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/GRID_cheapgrid1.json |
| 7,028 | json | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/GRID_fable1.json |
| 5,097 | json | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/GRID_kimi1.json |
| 19,902 | json | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/GRID_local-20261001-a.json |
| 7,506 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/GRID_local-20261001-a_RECEIPT.md |
| 5,682 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/KIMI1_RUN.md |
| 9,345 | text | yes | sha-stale:SHA MISMATCH | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/KIMI_DOSSIER.md |
| 18,555 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/PRIORS.md |
| 7,459 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/RUN_ANTHROPIC1.md |
| 1,415 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-A1-haiku45-B1.md |
| 1,355 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-A1-haiku45-B2.md |
| 1,472 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-A1-haiku45-B3.md |
| 1,865 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-A1-haiku45-B4.md |
| 1,506 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-A1-haiku45-B5.md |
| 144 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-A1-haiku45-B6.md |
| 422 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-A1-haiku45-B7.md |
| 1,810 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-A1-haiku45-B8.md |
| 2,676 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-A1-sonnet55-B1.md |
| 2,856 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-A1-sonnet55-B2.md |
| 1,946 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-A1-sonnet55-B3.md |
| 2,271 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-A1-sonnet55-B4.md |
| 1,970 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-A1-sonnet55-B5.md |
| 146 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-A1-sonnet55-B6.md |
| 388 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-A1-sonnet55-B7.md |
| 2,634 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-A1-sonnet55-B8.md |
| 2,796 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-B1-ds41flash.md |
| 1,650 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-B1-glm53flash.md |
| 39,948 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-B1-qwen38max.md |
| 2,717 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-B2-ds41flash.md |
| 1,679 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-B2-glm53flash.md |
| 1,779 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-B2-qwen38max.md |
| 1,819 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-B3-ds41flash.md |
| 1,866 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-B3-glm53flash.md |
| 1,618 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-B3-qwen38max.md |
| 1,648 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-B4-ds41flash.md |
| 1,985 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-B4-glm53flash.md |
| 2,124 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-B4-qwen38max.md |
| 2,645 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-B5-ds41flash.md |
| 2,063 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-B5-glm53flash.md |
| 727 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-B5-qwen38max.md |
| 134 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-B6-ds41flash.md |
| 130 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-B6-glm53flash.md |
| 139 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-B6-qwen38max.md |
| 401 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-B7-ds41flash.md |
| 377 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-B7-glm53flash.md |
| 333 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-B7-qwen38max.md |
| 688 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-B8-ds41flash.md |
| 616 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-B8-glm53flash.md |
| 1,151 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-B8-qwen38max.md |
| 10,497 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-fable1-B1.md |
| 2,038 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-fable1-B3.md |
| 1,902 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-fable1-B4.md |
| 13,919 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-fable1-B5.md |
| 133 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-fable1-B6.md |
| 3,189 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-fable1-B8.md |
| 1,437 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-kimi1-B1.md |
| 1,054 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-kimi1-B2.md |
| 1,134 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-kimi1-B3.md |
| 1,037 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-kimi1-B4.md |
| 1,097 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-kimi1-B5.md |
| 131 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-kimi1-B6.md |
| 346 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-kimi1-B7.md |
| 322 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/garden-v1-kimi1-B8.md |
| 2,574 | json | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/ask_snapshot/B1_ask.json |
| 2,488 | json | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/ask_snapshot/B2_ask.json |
| 2,871 | json | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/ask_snapshot/B3_ask.json |
| 2,690 | json | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/ask_snapshot/B4_ask.json |
| 2,469 | json | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/ask_snapshot/B5_ask.json |
| 1,497 | json | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/ask_snapshot/B6_ask.json |
| 1,323 | json | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/ask_snapshot/B6_ask.json.refire2 |
| 2,370 | json | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/ask_snapshot/B7_ask.json |
| 2,477 | json | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/ask_snapshot/B8_ask.json |
| 2,303 | json | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/ask_snapshot/B8_ask.json.refire2 |
| 1,704 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/gemma2_2b-instruct-q5_K_M__B1.md |
| 2,559 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/gemma2_2b-instruct-q5_K_M__B2.md |
| 1,047 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/gemma2_2b-instruct-q5_K_M__B3.md |
| 782 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/gemma2_2b-instruct-q5_K_M__B4.md |
| 1,446 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/gemma2_2b-instruct-q5_K_M__B5.md |
| 350 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/gemma2_2b-instruct-q5_K_M__B6.attempt1.md |
| 334 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/gemma2_2b-instruct-q5_K_M__B6.md |
| 2,721 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/gemma2_2b-instruct-q5_K_M__B7.md |
| 888 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/gemma2_2b-instruct-q5_K_M__B8.attempt1.md |
| 505 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/gemma2_2b-instruct-q5_K_M__B8.md |
| 1,849 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/gemma4_latest__B1.md |
| 5,045 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/gemma4_latest__B2.md |
| 1,576 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/gemma4_latest__B3.md |
| 1,644 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/gemma4_latest__B4.md |
| 785 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/gemma4_latest__B5.md |
| 270 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/gemma4_latest__B6.attempt1.md |
| 337 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/gemma4_latest__B6.md |
| 6,909 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/gemma4_latest__B7.md |
| 196 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/gemma4_latest__B8.attempt1.md |
| 2,043 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/gemma4_latest__B8.md |
| 265 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/gemma_2b__B6.attempt1.md |
| 306 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/gemma_2b__B6.md |
| 3,015 | text | yes | no | scratch-inbox | instrument-output | model garden local lane (2026-10-01) | watch/inbox/model_garden/lanelocal/local-20261001-a/gemma_2b__B7.md |
| 5,902 | text | yes | no | scratch-inbox | instrument-output | top-level inbox drops (seat/cron receipts) | watch/inbox/mountain_selfplay_20260929/SELFPLAY_RECEIPT.md |
| 9,214 | text | yes | no | scratch-inbox | instrument-output | top-level inbox drops (seat/cron receipts) | watch/inbox/operator_model/OPERATOR_MODEL_V2_BASE.md |
| 888,565 | json | yes | no | scratch-inbox | instrument-output | secret gate scanner outputs (2026-10-01) | watch/inbox/secret_gate_results/changed_20260930T162304Z.json |
| 972,459 | json | yes | no | scratch-inbox | instrument-output | secret gate scanner outputs (2026-10-01) | watch/inbox/secret_gate_results/changed_20260930T162801Z.json |
| 1,139,053 | json | yes | no | scratch-inbox | instrument-output | secret gate scanner outputs (2026-10-01) | watch/inbox/secret_gate_results/changed_20260930T163050Z.json |
| 1,639,625 | json | yes | no | scratch-inbox | instrument-output | secret gate scanner outputs (2026-10-01) | watch/inbox/secret_gate_results/changed_20261001T120844Z.json |
| 2,389,866 | json | yes | no | scratch-inbox | instrument-output | secret gate scanner outputs (2026-10-01) | watch/inbox/secret_gate_results/changed_20261001T120941Z.json |
| 3,392,434 | jsonl? | yes | no | scratch-inbox | instrument-output | secret gate scanner outputs (2026-10-01) | watch/inbox/secret_gate_results/changed_20261001T121329Z.json |
| 1,167 | json | yes | no | scratch-inbox | instrument-output | secret gate scanner outputs (2026-10-01) | watch/inbox/secret_gate_results/full_20260930T111951Z.json |
| 1,150 | json | yes | no | scratch-inbox | instrument-output | secret gate scanner outputs (2026-10-01) | watch/inbox/secret_gate_results/full_20260930T111952Z.json |
| 1,167 | json | yes | no | scratch-inbox | instrument-output | secret gate scanner outputs (2026-10-01) | watch/inbox/secret_gate_results/full_20260930T113445Z.json |
| 1,150 | json | yes | no | scratch-inbox | instrument-output | secret gate scanner outputs (2026-10-01) | watch/inbox/secret_gate_results/full_20260930T113446Z.json |
| 1,167 | json | yes | no | scratch-inbox | instrument-output | secret gate scanner outputs (2026-10-01) | watch/inbox/secret_gate_results/full_20260930T123911Z.json |
| 1,150 | json | yes | no | scratch-inbox | instrument-output | secret gate scanner outputs (2026-10-01) | watch/inbox/secret_gate_results/full_20260930T123912Z.json |
| 1,167 | json | yes | no | scratch-inbox | instrument-output | secret gate scanner outputs (2026-10-01) | watch/inbox/secret_gate_results/full_20260930T213919Z.json |
| 1,150 | json | yes | no | scratch-inbox | instrument-output | secret gate scanner outputs (2026-10-01) | watch/inbox/secret_gate_results/full_20260930T213921Z.json |
| 1,167 | json | yes | no | scratch-inbox | instrument-output | secret gate scanner outputs (2026-10-01) | watch/inbox/secret_gate_results/full_20260930T220703Z.json |
| 1,150 | json | yes | no | scratch-inbox | instrument-output | secret gate scanner outputs (2026-10-01) | watch/inbox/secret_gate_results/full_20260930T220704Z.json |
| 1,165 | json | yes | no | scratch-inbox | instrument-output | secret gate scanner outputs (2026-10-01) | watch/inbox/secret_gate_results/full_20261001T023644Z.json |
| 1,148 | json | yes | no | scratch-inbox | instrument-output | secret gate scanner outputs (2026-10-01) | watch/inbox/secret_gate_results/full_20261001T023645Z.json |
| 15,723 | text | yes | no | scratch-inbox | instrument-output | top-level inbox drops (seat/cron receipts) | watch/inbox/x_intel_deepgemm_20261001.md |
| 191 | json | yes | no | scratch-root | fetched-source | mangled-env scratch copy (literal %TMPDIR% dir) | %TMPDIR%/pp_localllama.json |
| 38,336 | html | yes | no | scratch-root | instrument-output | mangled-path temp copy (path separators eaten) | UsersfosteAppDataLocalTempbudget.html |
| 402,564 | html | yes | no | scratch-root | instrument-output | mangled-path temp copy (path separators eaten) | UsersfosteAppDataLocalTempdeepswe.html |
| 26,663 | text | yes | no | scratch-root | instrument-output | mangled-path temp copy (path separators eaten) | UsersfosteAppDataLocalTempjevals_readme.md |
| 2,280 | text | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | _sweep_pp_memory.py |
| 3,953 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | _sweep_pp_memory_pool.json |
| 20,842 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | as_aiagents_graph.json |
| 54 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | as_aiagents_mem.json |
| 97,787 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | as_aimemory_all.json |
| 157,922 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | as_claudecode_mem.json |
| 11 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | as_kg_mem.json |
| 20,207 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | as_llama_graph.json |
| 130,074 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | as_llama_mem.json |
| 54 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | as_llama_session.json |
| 141,974 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | as_llmdevs_mem.json |
| 54 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | as_localllm_mem.json |
| 54 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | as_ml_mem.json |
| 101,547 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | as_ollama_mem.json |
| 39,484 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | as_rag_graph.json |
| 53,305 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | as_rag_mem.json |
| 17,936 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | as_test.json |
| 23,784 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | kvarn_comments.json |
| 5,377 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | kvarn_pullpush.json |
| 4,295 | html | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | kvarn_redlib.html |
| 17,791 | text | yes | no | scratch-root | code-land | estate code lands (builders) | mag/inference_budget.py |
| 6,559 | text | yes | no | scratch-root | code-land | estate code lands (builders) | mag/rib_boot.py |
| 50,513 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | pc_1s1jlnd.json |
| 28,112 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | pc_1sc5zpf.json |
| 53,259 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | pc_1tod2hv.json |
| 34,676 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | pc_1ujp3pq.json |
| 212,035 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | pc_1veeix3.json |
| 99,747 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | pc_1w9sklm.json |
| 257,130 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | pc_1wl3828.json |
| 68,277 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | pc_1wo6qew.json |
| 191 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | pp_aiagents_mem.json |
| 38 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | pp_aimemory_all.json |
| 191 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | pp_claudecode_mem.json |
| 191,879 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | pp_ids.json |
| 191 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | pp_llama_mem.json |
| 191 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | pp_llmdevs_mem.json |
| 191 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | pp_localllm_mem.json |
| 191 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | pp_ml_mem.json |
| 191 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | pp_ollama_mem.json |
| 191 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | pp_rag_mem.json |
| 69,568 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | pullpush_comments.json |
| 26,859 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | pullpush_sub.json |
| 3,923 | json | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | pullpush_test.json |
| 24,785 | text | yes | no | scratch-root | code-land | estate code lands (builders) | queue/PITCHES_NEXT.md |
| 21,433 | text | yes | no | scratch-root | code-land | estate code lands (builders) | scripts/garden_battery_local.py |
| 11,192 | text | yes | no | scratch-root | code-land | estate code lands (builders) | scripts/garden_battery_local_amend1.py |
| 7,869 | text | yes | no | scratch-root | code-land | estate code lands (builders) | scripts/garden_battery_local_profiles.py |
| 7,124 | text | yes | no | scratch-root | code-land | estate code lands (builders) | scripts/garden_battery_local_refire.py |
| 1,842 | text | yes | no | scratch-root | code-land | estate code lands (builders) | scripts/register_tip_witness_task.ps1 |
| 9,066 | text | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | selftext_full.txt |
| 21 | json | yes | no | scratch-root | code-land | estate code lands (builders) | server/srp_users.json |
| 0 | text | yes | no | scratch-root | fetched-source | pp-sweep reddit/pullpush instrument (_sweep_pp_memory.py + kin) | sweep_llama_m.json |
| 8,915 | text | yes | no | scratch-root | code-land | estate code lands (builders) | tests/test_carrier_patch_t1w1.py |
| 14,941 | text | yes | no | scratch-root | code-land | estate code lands (builders) | tests/test_inference_budget.py |
| 9,814 | text | yes | no | scratch-root | code-land | estate code lands (builders) | tests/test_model_garden.py |
| 10,223 | text | yes | no | scratch-root | code-land | estate code lands (builders) | tests/test_mountain_selfplay.py |
| 12,837 | text | yes | no | scratch-root | code-land | estate code lands (builders) | tests/test_t1w1_ractor_fixes.py |
| 647 | json | yes | no | scratch-root | instrument-output | flock parity instrument | tools/flock_parity_out/codec_doc.json |
| 503 | json | yes | no | scratch-root | instrument-output | flock parity instrument | tools/flock_parity_out/codec_echo.jsonl |
| 1,974 | json | yes | no | scratch-root | instrument-output | flock parity instrument | tools/flock_parity_out/free_doc.json |
| 30,591 | jsonl? | yes | no | scratch-root | instrument-output | flock parity instrument | tools/flock_parity_out/free_godot.jsonl |
| 184 | json | yes | no | scratch-root | instrument-output | flock parity instrument | tools/flock_parity_out/free_report.json |
| 1,492,752 | jsonl? | yes | no | scratch-root | instrument-output | flock parity instrument | tools/flock_parity_out/full_frames.jsonl |
| 2,556,303 | json | yes | no | scratch-root | instrument-output | flock parity instrument | tools/flock_parity_out/full_gd_doc.json |
| 1,669,651 | jsonl? | yes | no | scratch-root | instrument-output | flock parity instrument | tools/flock_parity_out/full_godot.jsonl |
| 32,604 | json | yes | no | scratch-root | instrument-output | flock parity instrument | tools/flock_parity_out/full_inputs.json |
| 1,852,733 | jsonl? | yes | no | scratch-root | instrument-output | flock parity instrument | tools/flock_parity_out/full_python.jsonl |
| 2,426 | json | yes | no | scratch-root | instrument-output | flock parity instrument | tools/flock_parity_out/full_report.json |
| 2,531 | json | yes | no | scratch-root | instrument-output | flock parity instrument | tools/flock_parity_out/latest.json |
| 270,735 | jsonl? | yes | no | scratch-root | instrument-output | flock parity instrument | tools/flock_parity_out/quick_frames.jsonl |
| 464,345 | json | yes | no | scratch-root | instrument-output | flock parity instrument | tools/flock_parity_out/quick_gd_doc.json |
| 303,020 | jsonl? | yes | no | scratch-root | instrument-output | flock parity instrument | tools/flock_parity_out/quick_godot.jsonl |
| 11,552 | json | yes | no | scratch-root | instrument-output | flock parity instrument | tools/flock_parity_out/quick_inputs.json |
| 336,217 | jsonl? | yes | no | scratch-root | instrument-output | flock parity instrument | tools/flock_parity_out/quick_python.jsonl |
| 2,326 | json | yes | no | scratch-root | instrument-output | flock parity instrument | tools/flock_parity_out/quick_report.json |
| 21,827 | jsonl? | yes | no | scratch-root | instrument-output | flock parity instrument | tools/flock_parity_out/smoke_frames.jsonl |
| 37,405 | json | yes | no | scratch-root | instrument-output | flock parity instrument | tools/flock_parity_out/smoke_gd_doc.json |
| 23,845 | jsonl? | yes | no | scratch-root | instrument-output | flock parity instrument | tools/flock_parity_out/smoke_godot.jsonl |
| 5,658 | json | yes | no | scratch-root | instrument-output | flock parity instrument | tools/flock_parity_out/smoke_inputs.json |
| 26,491 | jsonl? | yes | no | scratch-root | instrument-output | flock parity instrument | tools/flock_parity_out/smoke_python.jsonl |
| 2,226 | json | yes | no | scratch-root | instrument-output | flock parity instrument | tools/flock_parity_out/smoke_report.json |
| 15,293 | text | yes | no | scratch-root | code-land | estate code lands (builders) | tools/garden_grade.py |
| 21,641 | text | yes | no | scratch-root | code-land | estate code lands (builders) | tools/model_garden.py |
| 20,941 | text | yes | no | scratch-root | code-land | estate code lands (builders) | tools/reverse_map.py |
| 156 | text | yes | no | scratch-root | instrument-output | day ledger / radar outputs | watch/DAY_LEDGER_2026-09-30.md |
| 129 | text | yes | no | scratch-root | instrument-output | day ledger / radar outputs | watch/DAY_LEDGER_2026-10-01.md |
| 9,276 | text | yes | no | scratch-root | instrument-output | day ledger / radar outputs | watch/PROSE_CENSUS_20261001.md |
| 5,404 | text | yes | no | scratch-root | instrument-output | day ledger / radar outputs | watch/X_REPLY_RADAR_20260930.md |
| 908 | text | yes | no | scratch-root | instrument-output | day ledger / radar outputs | watch/scout/MONITOR_LANE_2026-10-01.md |
| 63,393 | json | yes | no | scratch-root | fetched-source-mangled-copy | mangled-path root copy (path separators eaten) | watchinboxgala_20260925localfirst-steallanes_gh_search_lbrain.json |

## Receipt chain

- Raw check output: watch/inbox/gala_20260925/librarian-expedition/lanes/seats-inventory.check.txt (pass 1 + pass 2).
- Row data: watch/inbox/librarian_exp/inventory_rows.json (pass 1) and rows2.jsonl (pass 2, authoritative).
- Instruments: watch/inbox/librarian_exp/build_inventory.py, reconcile_print_only.py, gen_receipt.py (this generator, print-only).
- Trail listing: watch/inbox/librarian_exp/trail_listing_raw.txt; adds list: watch/inbox/librarian_exp/adds_all.txt.

## Not run / limits (honest)

- mag/ or tools/ code was NOT touched by this lane, so the violation-ratchet leg does not apply (nothing to check).
- The catalog and FTS surfaces moved mid-run (see SURFACE MOMENTS); counts are pinned to the pass-2 stream moment and would drift on a re-run by design (census law B2-216).
- INDEX sha recompute skipped for artifacts >20MB (none of the INDEX-registered set exceeded it).
