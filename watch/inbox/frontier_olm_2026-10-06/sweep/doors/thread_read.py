"""Thread deep-reader for the agent-memory-continuity reddit sweep (2026-10-06).

Door: per-thread comments RSS, https://www.reddit.com/r/{sub}/comments/{id}/{slug}/.rss
(verified 200 this sitting while .json doors 403/404/login-wall).

Fetches each thread's RSS, extracts post + comment entries (author, score-ish meta when
present, content HTML stripped to text), writes one text file per thread for deep reading.

Security posture: thread URLs are copied verbatim from memsearch_candidates.json entries
(same www.reddit.com host, no user input); output paths resolved inside the sweep evidence
dir; XML parse rejects DOCTYPE/ENTITY and caps size (Mimosa finding); win32 subprocess
carries CREATE_NO_WINDOW per law.
"""
import html
import json
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
OUT_DIR = (REPO_ROOT / "watch/inbox/frontier_olm_2026-10-06/sweep/raw").resolve()
if not str(OUT_DIR).startswith(str(REPO_ROOT)):
    print("refusing: output dir escaped repo root", file=sys.stderr)
    sys.exit(2)
OUT_DIR.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0"
ALLOWED_HOST = "www.reddit.com"
A = "{http://www.w3.org/2005/Atom}"
MAX_XML_BYTES = 8_000_000

THREADS = [
    ("1wl3828", "https://www.reddit.com/r/LocalLLaMA/comments/1wl3828/what_are_you_all_using_for_long_term/.rss"),
    ("1wd4tcw", "https://www.reddit.com/r/ollama/comments/1wd4tcw/what_should_be_the_source_of_truth_when_several/.rss"),
    ("1wqa5da", "https://www.reddit.com/r/LocalLLaMA/comments/1wqa5da/forget_compact_we_need_offload_to_memorymd_and/.rss"),
    ("1wz3xnf", "https://www.reddit.com/r/LocalLLaMA/comments/1wz3xnf/only_13_of_context_is_used_but_model_starts_to/.rss"),
    ("1wai0iv", "https://www.reddit.com/r/ollama/comments/1wai0iv/which_local_models_handle_structured_extraction/.rss"),
    ("1wqqott", "https://www.reddit.com/r/ollama/comments/1wqqott/built_a_local_sqlite_memory_layer_for_ai_coding/.rss"),
    ("1wlbqnl", "https://www.reddit.com/r/LocalLLaMA/comments/1wlbqnl/building_better_memory_for_your_agents_you_dont/.rss"),
]


def fetch(url):
    if url.split("/")[2] != ALLOWED_HOST:
        raise ValueError("blocked non-allowlist host")
    body = ""
    for attempt in range(4):
        cp = subprocess.run(
            ["curl", "-s", "-L", "-m", "60", "-A", UA, "-w", "%{http_code}", url],
            capture_output=True, text=True, timeout=90,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        body, code = cp.stdout[:-3], cp.stdout[-3:]
        if code == "200":
            return 200, body
        time.sleep(20 * (attempt + 1))
    return int(code or 0), body


def strip_tags(s):
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"[ \t]+", " ", s).strip()


def parse(xml_text):
    if len(xml_text) > MAX_XML_BYTES:
        return []
    head = xml_text[:4096].lower()
    if "<!doctype" in head or "<!entity" in head:
        return []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []
    entries = []
    for e in root.findall(A + "entry"):
        title = (e.find(A + "title").text or "").strip()
        author_el = e.find(f"{A}author/{A}name")
        author = author_el.text if author_el is not None else "?"
        content_el = e.find(A + "content")
        raw = content_el.text or "" if content_el is not None else ""
        entries.append({
            "title": title,
            "author": author,
            "text": strip_tags(raw),
            "link": e.find(A + "link").attrib.get("href", ""),
        })
    return entries


def main():
    summary = []
    for tid, url in THREADS:
        code, body = fetch(url)
        entries = parse(body) if code == 200 else []
        dest = (OUT_DIR / f"thread_{tid}.txt").resolve()
        if not str(dest).startswith(str(OUT_DIR)):
            print("refusing path escape", file=sys.stderr)
            sys.exit(2)
        with dest.open("w", encoding="utf-8") as f:
            f.write(f"THREAD {tid} HTTP {code} entries={len(entries)}\nURL {url}\n\n")
            for i, en in enumerate(entries):
                f.write(f"--- entry {i} [{en['author']}] {en['title'][:100]}\n")
                f.write(en["text"][:4000] + "\n\n")
        print(f"== {tid}: HTTP {code}, {len(entries)} entries -> {dest.name}")
        summary.append({"id": tid, "http": code, "entries": len(entries)})
        time.sleep(10)
    print(json.dumps(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
