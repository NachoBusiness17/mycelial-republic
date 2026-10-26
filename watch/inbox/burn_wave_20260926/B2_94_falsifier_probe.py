#!/usr/bin/env python3
"""B2-94 falsifier probe: wandr_selfeval.fetch_url vs a loopback HTTP listener.

The brief's disease class: fetch_url re-fetches submission-cited URLs, and a
submission is model-authored input, so fetch_url("http://127.0.0.1:<port>/...")
lets untrusted input point the harness at internal services and embeds the
response in the graded report.

Phase PRE (against pre-fix bytes, sha256 dbb8803ce973268f...):
  the loopback listener is actually hit (handler count 1, payload returned),
  proving the internal fetch leaves the process today.

Phase POST (against the B2-94 guard):
  the same URL is refused before any socket connects (listener count 0),
  file:// estate evidence still fetches, and a nonexistent host returns an
  error row instead of crashing.

Writes JSON results beside this file. Never disables the guard to re-open the
hole; PRE must be run before the fix lands.
"""
import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tools.wandr_selfeval import fetch_url  # noqa: E402

PAYLOAD = b"B2-94-LOOPBACK-CANARY-internal-service-response"
OUT = Path(__file__).resolve().parent / "B2_94_falsifier_probe_results.json"
HITS = {"count": 0}


class Canary(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        HITS["count"] += 1
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(PAYLOAD)

    def log_message(self, *a):  # silence
        pass


def main() -> int:
    phase = sys.argv[1] if len(sys.argv) > 1 else "pre"
    srv = HTTPServer(("127.0.0.1", 0), Canary)
    port = srv.server_address[1]
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()

    results = {"phase": phase, "port": port}

    loop = fetch_url(f"http://127.0.0.1:{port}/b2_94_payload")
    results["loopback_fetch"] = loop
    results["loopback_text_matches_canary"] = PAYLOAD.decode() in (loop.get("text") or "")
    results["listener_hits_after_loopback"] = HITS["count"]

    if phase == "post":
        gold = fetch_url(
            (ROOT / "tools" / "wandr_selfeval_task.json").as_uri())
        results["file_scheme_gold"] = {
            "ok": gold.get("ok"), "status": gold.get("status"),
            "bytes_read": len(gold.get("text") or "")}
        dead = fetch_url("http://b2-94-nonexistent-host.invalid/x")
        results["dead_host_row"] = {"ok": dead.get("ok"), "error": dead.get("error", "")[:120]}
        results["verdict"] = (
            "HOLDS" if (loop.get("ok") is False and HITS["count"] == 0
                        and gold.get("ok") is True and dead.get("ok") is False)
            else "FAILS")

    srv.shutdown()
    OUT.write_text(json.dumps(results, indent=1), encoding="utf-8")
    print(json.dumps(results, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
