#!/usr/bin/env python3
"""vision_bench.py — real throughput + accuracy benchmark for the local vision
model on scanned pages (salon_infinite_library BUILD ORDER item 1).

No page renderer exists on this box (no pdftoppm/magick/gs/pymupdf), so pages
are obtained by CARVING the DCTDecode JPEG XObjects out of the scanned PDF —
archive.org scans store one JPEG per page. Ground truth for the accuracy
spot-check is the PDF's own OCR text layer (pdftotext per page, window +-3 to
absorb image/page off-by-few).

Usage: python vision_bench.py <scanned.pdf> [n_pages] [start_frac]
"""
import base64
import json
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

MODEL = "qwen2.5vl:3b"
OLLAMA = "http://127.0.0.1:11434/api/generate"
PROMPT = "Transcribe all text on this page. Output only the transcription."
NUM_PREDICT = 512
OUT_DIR = Path("memory/runs/vision_bench_20260905")


def carve_jpegs(pdf: Path, n: int, start_frac: float = 0.25):
    """Carve n DCTDecode JPEG page images spread from start_frac of the file."""
    raw = pdf.read_bytes()
    found = []
    for m in re.finditer(rb"stream\r?\n", raw):
        dict_start = max(0, m.start() - 900)
        header = raw[dict_start:m.start()]
        if b"/Image" not in header or b"/DCTDecode" not in header:
            continue
        end = raw.find(b"endstream", m.end())
        if end < 0:
            continue
        jpg = raw[m.end():end].rstrip(b"\r\n")
        if jpg[:2] == b"\xff\xd8" and jpg[-2:] == b"\xff\xd9" and len(jpg) > 20000:
            found.append((m.start(), jpg))
    if not found:
        return []
    lo = int(len(found) * start_frac)
    idxs = [lo + int(i * (len(found) - lo) / max(1, n)) for i in range(n)]
    return [(i, found[i][1]) for i in idxs]


def page_text(pdf: Path, page: int) -> str:
    r = subprocess.run(
        ["pdftotext", "-q", "-f", str(page), "-l", str(page), str(pdf), "-"],
        capture_output=True, encoding="utf-8", errors="replace", timeout=60,
    )
    return r.stdout if r.returncode == 0 else ""


def best_recall(vision_out: str, pdf: Path, page_guess: int, window: int = 3):
    """Recall of ground-truth OCR words (len>=4) present in vision output,
    maximized over a page window to absorb image->page offset."""
    vtoks = {w.lower().strip(".,;:()[]'\"") for w in vision_out.split()}
    best = (0.0, 0, 0)
    for p in range(max(1, page_guess - window), page_guess + window + 1):
        gt = page_text(pdf, p)
        gtw = {w.lower().strip(".,;:()[]'\"") for w in gt.split() if len(w) >= 4}
        if not gtw:
            continue
        hit = len(gtw & vtoks) / len(gtw)
        if hit > best[0]:
            best = (hit, p, len(gtw))
    return best


def main(argv):
    pdf = Path(argv[0])
    n = int(argv[1]) if len(argv) > 1 else 5
    start_frac = float(argv[2]) if len(argv) > 2 else 0.25
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pages = carve_jpegs(pdf, n, start_frac)
    print(f"carved {len(pages)} JPEG pages from {pdf.name} ({n} requested)")
    rows = []
    for k, (idx, jpg) in enumerate(pages, 1):
        img_path = OUT_DIR / f"page_{k:02d}_img{idx:05d}.jpg"
        img_path.write_bytes(jpg)
        b64 = base64.b64encode(jpg).decode()
        t0 = time.time()
        body = json.dumps({
            "model": MODEL, "prompt": PROMPT, "stream": False,
            "images": [b64], "options": {"num_predict": NUM_PREDICT},
        }).encode()
        try:
            req = urllib.request.Request(
                OLLAMA, data=body, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=300) as resp:
                out = json.loads(resp.read())
            dt = time.time() - t0
            text = out.get("response", "")
            recall, gt_page, gt_words = best_recall(text, pdf, idx + 1)
            rows.append({"page": k, "img_idx": idx, "sec": round(dt, 1),
                         "out_words": len(text.split()),
                         "eval_tokens": out.get("eval_count", 0),
                         "recall": round(recall, 3), "gt_page": gt_page,
                         "jpg_kb": len(jpg) // 1024})
            print(f"page {k}: {dt:6.1f}s  out_words={len(text.split()):>4}  "
                  f"recall_vs_ocr={recall:.2f} (gt p.{gt_page})")
        except Exception as e:
            dt = time.time() - t0
            rows.append({"page": k, "img_idx": idx, "sec": round(dt, 1),
                         "error": str(e)[:200]})
            print(f"page {k}: ERROR after {dt:.1f}s: {e}")
    ok = [r for r in rows if "error" not in r and r.get("eval_tokens")]
    if ok:
        tot_sec = sum(r["sec"] for r in ok)
        pph = 3600.0 * len(ok) / tot_sec
        recalls = [r["recall"] for r in ok]
        print(f"\nBENCH: {len(ok)}/{len(rows)} pages | {tot_sec/len(ok):.1f} s/page "
              f"| {pph:.1f} pages/hour | recall median={sorted(recalls)[len(recalls)//2]:.2f} "
              f"min={min(recalls):.2f} max={max(recalls):.2f} | model={MODEL} "
              f"num_predict={NUM_PREDICT}")
    (OUT_DIR / "bench_results.json").write_text(json.dumps(rows, indent=1))
    print(f"results -> {OUT_DIR / 'bench_results.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
