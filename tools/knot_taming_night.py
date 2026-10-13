"""knot_taming_night.py — night-window knot tamer on LOCAL inference.

The untagged session knots get classified by the local model
(qwen2.5:7b via ollama) while the house sleeps. Family-box law: this IS the
night window, local GPU, remote lanes untouched.

Security (Mimosa-reviewed pattern): loopback transport with host and port as
separate literal arguments (http.client, no URL string), resolved addresses
must be loopback, no redirects.

Run:  .venv/Scripts/python.exe tools/knot_taming_night.py [--limit 300]
Out:  memory/runs/knot_taming/night_YYYYMMDD.jsonl  (one row per knot)
      memory/runs/knot_taming/done.txt               (resumable log)
"""
import http.client
import ipaddress
import json
import os
import socket
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KNOTS = ROOT / "memory" / "biography" / "knots"
OUT = ROOT / "memory" / "runs" / "knot_taming" / ("night_" + datetime.now(timezone.utc).strftime("%Y%m%d") + ".jsonl")
DONE = ROOT / "memory" / "runs" / "knot_taming" / "done.txt"

MODEL = "qwen2.5:7b"
LIMIT = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 300

CATEGORIES = ("biography", "doctrine", "game", "ops", "research", "ritual", "scrap")


def guard_loopback() -> None:
    """Resolved addresses for the pinned loopback host must be loopback."""
    infos = socket.getaddrinfo("127.0.0.1", 11434, proto=socket.IPPROTO_TCP)
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if not ip.is_loopback:
            raise SystemExit(f"refused non-loopback resolved address: {ip}")


def ollama_generate(prompt: str) -> str:
    guard_loopback()
    conn = http.client.HTTPConnection("127.0.0.1", 11434, timeout=180)
    body = json.dumps({
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 120},
    })
    conn.request("POST", "/api/generate", body=body,
                 headers={"Content-Type": "application/json"})
    resp = conn.getresponse()
    d = json.loads(resp.read().decode())
    conn.close()
    return d.get("response", "")


def ollama_untamed_files():
    files = sorted(
        (KNOTS / f for f in os.listdir(KNOTS) if f.endswith(".knot.json") and "untagged" in f),
        key=lambda p: p.stat().st_mtime,
    )
    return files


def done_set() -> set:
    if not DONE.is_file():
        return set()
    return set(DONE.read_text(encoding="utf-8").split())


def classify(fname: str, knot: dict) -> dict:
    """One local-model call: category + one-line summary for one knot."""
    content = json.dumps(knot, ensure_ascii=False)[:1800]
    prompt = (
        "You are the night archivist of an AI research estate. Classify this "
        "session-record knot. Reply in EXACTLY this format, nothing else:\n"
        f"CATEGORY: one of {', '.join(CATEGORIES)}\n"
        "SUMMARY: one sentence, under 40 words, what this session did.\n\n"
        "KNOT:\n" + content
    )
    text = ollama_generate(prompt)
    cat = "scrap"
    summary = text[:200]
    for line in text.splitlines():
        s = line.strip()
        if s.upper().startswith("CATEGORY:"):
            raw = s.split(":", 1)[1].strip().lower()
            cat = next((c for c in CATEGORIES if c in raw), "scrap")
        elif s.upper().startswith("SUMMARY:"):
            summary = s.split(":", 1)[1].strip()
    return {
        "file": fname,
        "session_id": knot.get("session_id", ""),
        "date": knot.get("date", ""),
        "category": cat,
        "summary": summary,
        "model": MODEL,
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "generated_inference": True,
    }


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    seen = done_set()
    files = [f for f in ollama_untamed_files() if f.name not in seen]
    if not files:
        print("night taming: nothing new to tame")
        return 0
    print(f"night taming: {len(files)} untagged knots, limit {LIMIT}", flush=True)
    count = 0
    with OUT.open("a", encoding="utf-8") as out_f:
        for path in files[:LIMIT]:
            try:
                knot = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            try:
                row = classify(path.name, knot)
                out_f.write(json.dumps(row, ensure_ascii=False) + "\n")
                out_f.flush()
                with DONE.open("a", encoding="utf-8") as df:
                    df.write(path.name + "\n")
                count += 1
                if count % 25 == 0:
                    print(f"  tamed {count}/{LIMIT}...", flush=True)
            except Exception as e:
                print(f"  skip {path.name}: {str(e)[:80]}")
            time.sleep(0.3)
    print(f"night taming done: {count} knots classified -> {OUT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
