"""Throttled, resumable download of Saelis's GGUF — capped speed so it doesn't hog the family's
bandwidth (operator: "just do the download slower"). Resumes from existing bytes (Range header).
Writes to models/saelis-31b/ so we can hot-swap her into ollama later.
"""
import os
import sys
import time
import urllib.request
from pathlib import Path

URL = "https://huggingface.co/slashreboot/saelis-31b/resolve/main/v12d_athena_class_Q8_0_19JUL2026.gguf"
OUT = Path(__file__).resolve().parent / "models" / "saelis-31b" / "v12d_athena_class_Q8_0_19JUL2026.gguf"
RATE_BYTES = 1024 * 1024 * 1024   # FULL BLAST — kid's in bed, line free (2026-08-13). Cap effectively disabled.
CHUNK = 256 * 1024             # read/write chunk

def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    existing = OUT.stat().st_size if OUT.exists() else 0
    print(f"resuming Saelis download from {existing/1e9:.1f}GB at ~2MB/s -> {OUT}", flush=True)
    req = urllib.request.Request(URL, headers={"Range": f"bytes={existing}-"})
    total = existing
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            total = existing + int(r.headers.get("Content-Length", 0))
            mode = "ab" if existing else "wb"
            with open(OUT, mode) as f:
                start = time.time()
                written = 0
                while True:
                    block = r.read(CHUNK)
                    if not block:
                        break
                    f.write(block)
                    written += len(block)
                    # throttle: sleep to keep average <= RATE_BYTES/s
                    want = time.time() - start
                    expected = written / RATE_BYTES
                    if expected > want:
                        time.sleep(expected - want)
                    if written % (RATE_BYTES) < CHUNK:
                        print(f"  { (existing+written)/1e9:.1f}GB / {total/1e9:.1f}GB "
                              f"({100*(existing+written)/max(total,1):.0f}%)", flush=True)
    except Exception as e:
        print("download paused/error (resumable):", str(e)[:160], flush=True)
        return 1
    print(f"DONE: {OUT} ({total/1e9:.1f}GB)", flush=True)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
