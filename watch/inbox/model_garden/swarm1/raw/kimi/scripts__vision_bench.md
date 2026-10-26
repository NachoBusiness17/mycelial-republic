# swarm1-kimi-scripts__vision_bench (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

DEFECT 1: `page_guess` passed to `best_recall` uses JPEG stream byte offset (`idx`) instead of actual PDF page number, causing OCR lookup to search wrong page range | EVIDENCE: scripts/vision_bench.py:93 | FIX: pass actual PDF page number from `carve_jpegs` return value or remove `best_recall` until page mapping is implemented

DEFECT 2: `urllib.request` lacks User-Agent header, causing potential 403/ blocking by Ollama or proxies | EVIDENCE: scripts/vision_bench.py:89 | FIX: add `headers={"Content-Type": "application/json", "User-Agent": "mag-vision-bench/0.1"}` to Request

DEFECT 3: `OUT_DIR` is global mutable path with hardcoded date suffix, causing collisions on re-runs and preventing parallel execution | EVIDENCE: scripts/vision_bench.py:19 | FIX: accept output directory via CLI arg with `OUT_DIR = Path(argv[3]) if len(argv) > 3 else Path(f"memory/runs/vision_bench_{datetime.now().strftime('%Y%m%d_%H%M%S')}")`

DEAD-CODE: `ok` filter checks `r.get("eval_tokens")` which is always truthy (0 or positive int) but never falsey in success case; condition adds no value | EVIDENCE: scripts/vision_bench.py:101

ONE-SITTING FIX: replace `idx + 1` with proper page number or remove `best_recall` entirely; the current `page_guess` logic is fundamentally broken for accuracy measurement | EVIDENCE: scripts/vision_bench.py:93
