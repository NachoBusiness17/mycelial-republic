"""DDG HTML search door for quantization-specific reddit threads (pass 1).

Queries html.duckduckgo.com/html/ with site:reddit.com queries, extracts the
real target URLs from uddg redirects plus titles and snippets. Saves evidence.

Security posture: single fixed search host; queries are literal strings from
the module constant; output paths resolved inside the sweep evidence dir.
"""
import html as H
import json
import re
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = (REPO_ROOT / "watch/inbox/frontier_olm_2026-10-06/sweep/doors").resolve()
OUT_DIR.mkdir(parents=True, exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0"

QUERIES = [
    "site:reddit.com/r/LocalLLaMA Q4_K_M vs Q8_0 quality",
    "site:reddit.com/r/LocalLLaMA KV cache quantization q4",
    "site:reddit.com/r/LocalLLaMA IQ2 quantization",
    "site:reddit.com/r/LocalLLaMA quantization small model collapse",
    "site:reddit.com/r/LocalLLM quantized model accuracy loss",
    "site:reddit.com/r/ollama quantization q4 quality",
    "site:reddit.com AQLM quantization 2-bit",
    "site:reddit.com/r/LocalLLaMA bitnet ternary quantization",
    "site:reddit.com/r/LocalLLaMA long context KV cache f16 quality",
    "site:reddit.com/r/LocalLLaMA new quantization method paper",
    "site:reddit.com/r/LocalLLaMA dynamic quantization imatrix unsloth",
    "site:reddit.com/r/LocalLLaMA 2b model quantization degradation",
]

RESULT_RE = re.compile(
    r'<a rel="nofollow" class="result__a" href="([^"]+)">(.*?)</a>', re.S)
SNIP_RE = re.compile(
    r'<a class="result__snippet"[^>]*>([\s\S]*?)</a>')


def ddg(query):
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
    cp = subprocess.run(
        ["curl", "-s", "-m", "30", "-A", UA, url],
        capture_output=True, text=True,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    return cp.stdout


def clean(s):
    return re.sub(r"\s+", " ", TAG_SUB(s)).strip()


def TAG_SUB(s):
    return re.sub(r"<[^>]+>", "", H.unescape(s))


def main():
    all_rows = []
    for q in QUERIES:
        raw = ddg(q)
        stamp = re.sub(r"[^A-Za-z0-9]+", "_", q)[:60]
        (OUT_DIR / f"ddg_{stamp}.html").write_text(raw, encoding="utf-8")
        res = RESULT_RE.findall(raw)
        snips = [clean(s) for s in SNIP_RE.findall(raw)]
        n = 0
        for i, (href, title) in enumerate(res):
            if "uddg=" in href:
                target = urllib.parse.unquote(
                    href.split("uddg=")[1].split("&rut=")[0])
            else:
                target = href
            all_rows.append({
                "query": q,
                "title": clean(title),
                "url": target,
                "snippet": snips[i] if i < len(snips) else "",
            })
            n += 1
        print(f"{n:2d} results | {q}")
        time.sleep(2.5)
    (OUT_DIR / "ddg_candidates.json").write_text(
        json.dumps(all_rows, indent=1), encoding="utf-8")
    print(f"\nTOTAL ddg candidates: {len(all_rows)}")
    for i, r in enumerate(all_rows, 1):
        print(f"{i:2d}. {r['url'][:110]}")
        print(f"      {r['title'][:100]} | {r['snippet'][:120]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
