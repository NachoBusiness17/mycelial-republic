"""research_mine.py — run estate research through DeepSeek for grounded
literature briefings. Speculative research analyst pipeline.

Usage:
  python tools/research_mine.py [--limit 25]
"""
import ipaddress
import json
import http.client
import socket
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "watch" / "inbox" / "deepseek_research"
ENV = ROOT / ".env"
API_HOST = "api.deepseek.com"
API_PORT = 443
MODEL = "deepseek-flash"
SYSTEM = (
    "You are a speculative research analyst. For the document below:\n"
    "1. Identify the core scientific/technical claims\n"
    "2. Find related arXiv papers and GitHub repositories "
    "(cite real papers only — if unsure, say uncertain)\n"
    "3. Rank scientific importance (High/Medium-High/Foundational/Low/Pedagogical)\n"
    "4. Assess journal/venue quality for the cited works\n"
    "5. Socratic expansion: 3 open questions the field should answer\n\n"
    "Format: markdown with sections. Under 1500 words. "
    "Honesty: if you cannot verify a paper exists, say uncertain. "
    "Never invent citations."
)


def get_key() -> str:
    for line in ENV.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("DEEPSEEK_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"')
    raise SystemExit("DEEPSEEK_API_KEY not found")


def guard() -> None:
    for info in socket.getaddrinfo(API_HOST, API_PORT, proto=socket.IPPROTO_TCP):
        ip = ipaddress.ip_address(info[4][0])
        if not ip.is_global:
            raise SystemExit(f"refused non-public address: {ip}")


def call(content: str, title: str, keyv: str) -> str:
    guard()
    conn = http.client.HTTPSConnection(API_HOST, API_PORT, timeout=120)
    body = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"Document: {title}\n\n{content[:12000]}"}
        ],
        "max_tokens": 3000,
        "temperature": 0.3,
    })
    conn.request("POST", "/chat/completions", body=body, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {keyv}",
    })
    resp = conn.getresponse()
    d = json.loads(resp.read().decode())
    conn.close()
    return d["choices"][0]["message"]["content"]


def main() -> int:
    keyv = get_key()
    outdir = ROOT / "watch" / "inbox" / "deepseek_research" / "mined"
    outdir.mkdir(parents=True, exist_ok=True)
    src_dir = ROOT / "memory" / "research_packs"
    donefile = outdir / ".mined_done"
    doneset = set(donefile.read_text().split()) if donefile.is_file() else set()
    files = sorted(src_dir.rglob("*.md")) if src_dir.is_dir() else []
    count = 0
    for f in files:
        if count >= 25:
            break
        rel = str(f.relative_to(ROOT))
        if rel in doneset or f.stat().st_size < 500:
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="replace")[:12000]
            if len(content.strip()) < 100:
                continue
            title = f.stem.replace("_", " ").replace("-", " ")
            print(f"mining: {title[:60]}...", flush=True)
            result = call(content, title, keyv)
            out = outdir / (f.stem + "_analysis.md")
            out.write_text(
                f"# Research Analysis — {title}\n\n"
                f"Source: `{rel}`\nModel: {MODEL}\n"
                f"Date: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n\n"
                + result, encoding="utf-8")
            count += 1
            with donefile.open("a") as df:
                df.write(rel + "\n")
            time.sleep(1.5)
        except Exception as e:
            print(f"  err {f.name}: {str(e)[:100]}")
            time.sleep(3)
    print(f"session: {count} mined")
    return 0


if __name__ == "__main__":
    sys.exit(main())
