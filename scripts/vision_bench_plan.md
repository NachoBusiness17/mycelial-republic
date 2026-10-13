# Vision benchmark plan — local vision model on scanned pages

Salon: `memory/runs/salons/salon_infinite_library_20260905/SALON_ARTIFACT.md` BUILD
ORDER item 1. Purpose: measure the real cost of the vision branch of the
deterministic triage (`scripts/pdf_triage.py`), and test the 12-18 pages/hour
claim against the "2-3 s/page" collision.

## Sample source (known-scanned, already in corpus custody)

- `corpus/training_materials/tesla/colorado_springs_notes_1899_1900_scan.pdf`
  (431 pages, 48 MB, archive.org full scan, intake 2026-09-05).
- Original IA URL:
  `https://archive.org/download/nikola-tesla-colorado-springs-notes-with-bookmarks/Nikola_Tesla_Colorado_Springs_Notes_%20with%20bookmarks.pdf`
- Property that makes it the right test bed: it is a genuine scan (431
  DCTDecode JPEG page images) that ALSO carries an archive.org OCR text layer
  — so `pdftotext` per page gives free ground truth for the accuracy
  spot-check, while the images exercise the vision path.
- Fallback if a no-text-layer sample is wanted (SAMPLE-NEEDED): any IA scan
  without OCR layer, e.g. `https://archive.org/download/<identifier>/` — mark
  SAMPLE-NEEDED until one is fetched.

## Renderer situation (measured on this box 2026-09-05)

No pdftoppm, no ImageMagick, no ghostscript, no pymupdf/pypdf/pdfminer in the
system Python. Pages are obtained by CARVING the embedded DCTDecode JPEG
XObjects out of the PDF with stdlib zlib/regex (`scripts/vision_bench.py::
carve_jpegs`) — archive.org scans store one JPEG per page. This is the
stdlib-only render path; if a future box has pdftoppm:
`pdftoppm -png -r 150 -f N -l N in.pdf out` is the drop-in replacement.

## Exact commands

```bash
# 0. confirm a vision model is served
curl -s http://127.0.0.1:11434/api/tags | grep -o '"name":"[^"]*"'
#    -> qwen2.5vl:3b present (families ["qwen25vl"]) as of 2026-09-05

# 1. triage first — vision only fires on pdftotext-fail / <50% tokens
python scripts/pdf_triage.py corpus/training_materials

# 2. 5-page real benchmark (carve 5 JPEG pages at 25% depth, fire 5 calls)
python scripts/vision_bench.py \
  corpus/training_materials/tesla/colorado_springs_notes_1899_1900_scan.pdf 5 0.25

# 3. scale: 20 pages for a tighter CI once 5-page smoke passes
python scripts/vision_bench.py \
  corpus/training_materials/tesla/colorado_springs_notes_1899_1900_scan.pdf 20 0.1
```

## Metrics recorded (per page and aggregate)

- `sec/page` — wall clock per vision call, model load amortized over 5 calls.
- `tok/page` — ollama `eval_count` (generated tokens) per page.
- `recall` — accuracy spot-check: fraction of ground-truth OCR words (len>=4,
  lowercased, punctuation-stripped) from `pdftotext -f P -l P` present in the
  vision transcription; maximized over a +-3 page window to absorb the
  image-index/page-number offset. 1.0 = perfect vs the OCR layer (note: the
  OCR layer itself is noisy — "ColoradD Springs" — so recall ~0.8 is already
  strong; vision can beat its ground truth).
- `pages/hour` — 3600 / mean(sec/page), plus tok/s from eval_count.

## Pass/fail bar (the 12-18 pg/hr claim)

- PASS (claim SUPPORTED): mean sec/page in [200, 300] s -> 12-18 pg/hr, with
  median recall >= 0.60 on this sample.
- FAIL-FAST (claim DISPUTED, better): sec/page < 60 s -> >60 pg/hr, vision is
  cheap; triage can loosen the vision gate.
- FAIL-SLOW (claim DISPUTED, worse): sec/page > 300 s or recall < 0.40 -> the
  vision branch is a last resort only; corpus policy stays pdftotext-first and
  scanned-no-OCR items get human-flagged, not auto-visioned.
- 100-page salon target: run step 3 and require the same bars to hold at n=20
  before spending a night on n=100.

## Receipt

2026-09-05: RAN, 5 real pages through qwen2.5vl:3b on ollama 127.0.0.1:11434.
Numbers in `memory/runs/vision_bench_20260905/bench_results.json` and the room
receipt row in `watch/room.jsonl`.
