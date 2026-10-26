"""Memory-topic search RSS fetcher for the agent-memory-continuity reddit sweep (2026-10-06).

Door: https://www.reddit.com/r/{sub}/search/.rss?q=...&restrict_sr=1&sort=relevance&t=month
(the .rss door answers 200 where the .json doors 403/404/login-wall; verified this sitting).

Security posture: literal https URLs against host allowlist www.reddit.com; subreddit and
query strings are whitelist constants below (no user input); output paths resolved and
asserted inside the sweep evidence dir; win32 subprocess carries CREATE_NO_WINDOW per law;
XML parse rejects DOCTYPE/ENTITY (entity-expansion guard, Mimosa finding 2026-10-06) and
caps input size.
"""
import json
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import quote

REPO_ROOT = Path(__file__).resolve().parents[5]
OUT_DIR = (REPO_ROOT / "watch/inbox/frontier_olm_2026-10-06/sweep/doors").resolve()
if not str(OUT_DIR).startswith(str(REPO_ROOT)):
    print("refusing: output dir escaped repo root", file=sys.stderr)
    sys.exit(2)
OUT_DIR.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0"
ALLOWED_HOST = "www.reddit.com"
A = "{http://www.w3.org/2005/Atom}"
MAX_XML_BYTES = 4_000_000

QUERIES = [
    ("LocalLLaMA", "long term memory"),
    ("LocalLLaMA", "persistent memory"),
    ("LocalLLaMA", "summarization"),
    ("LocalLLaMA", "knowledge graph"),
    ("LocalLLaMA", "forget"),
    ("LocalLLM", "agent memory"),
    ("ollama", "memory"),
    ("MachineLearning", "agent memory"),
]


def fetch(url):
    if url.split("/")[2] != ALLOWED_HOST:
        raise ValueError("blocked non-allowlist host")
    body = ""
    for attempt in range(4):
        cp = subprocess.run(
            ["curl", "-s", "-L", "-m", "40", "-A", UA, "-w", "%{http_code}", url],
            capture_output=True, text=True, timeout=60,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        body, code = cp.stdout[:-3], cp.stdout[-3:]
        if code == "200":
            return 200, body
        time.sleep(15 * (attempt + 1))
    return int(code or 0), body


def parse(xml_text):
    rows = []
    if len(xml_text) > MAX_XML_BYTES:
        return rows
    head = xml_text[:4096].lower()
    if "<!doctype" in head or "<!entity" in head:
        return rows
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return rows
    for e in root.findall(A + "entry"):
        title = (e.find(A + "title").text or "").strip()
        link = e.find(A + "link").attrib.get("href", "")
        upd = (e.find(A + "updated").text or "")[:10]
        content = e.find(A + "content")
        snippet = re.sub(r"<[^>]+>", " ", content.text or "")[:300].strip() if content is not None else ""
        rows.append({"title": title, "link": link, "date": upd, "snippet": snippet})
    return rows


def main():
    all_rows = []
    for sub, q in QUERIES:
        url = f"https://{ALLOWED_HOST}/r/{sub}/search/.rss?q={quote(q)}&restrict_sr=1&sort=relevance&t=month"
        code, body = fetch(url)
        rows = parse(body) if code == 200 else []
        safe_q = q.replace(" ", "_")
        dest = (OUT_DIR / f"memsearch_{sub}_{safe_q}.rss").resolve()
        if not str(dest).startswith(str(OUT_DIR)):
            print("refusing path escape", file=sys.stderr)
            sys.exit(2)
        dest.write_text(body, encoding="utf-8", errors="replace")
        print(f"== r/{sub} [{q}]: HTTP {code}, {len(rows)} entries")
        all_rows.extend(rows)
        time.sleep(8)
    (OUT_DIR / "memsearch_candidates.json").write_text(
        json.dumps(all_rows, indent=1), encoding="utf-8")
    print(f"TOTAL: {len(all_rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
