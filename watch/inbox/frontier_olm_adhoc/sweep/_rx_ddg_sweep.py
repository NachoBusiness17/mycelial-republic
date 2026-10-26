"""DDG-html site:x.com candidate harvester for the open-local-models-x sweep.
Auth-free discovery of x.com status URLs (with IDs) + snippets, deduped.
Run with the repo venv python. Output: _rx_ddg_candidates.json
"""
import json
import re
import time
import urllib.parse
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")

QUERIES = [
    "site:x.com qwen tool calling local model",
    "site:x.com small model agentic tool calling 8B",
    "site:x.com ollama release windows",
    "site:x.com UnslothAI gemma",
    "site:x.com llama.cpp vulkan AMD RDNA",
    "site:x.com LocalLLaMA tool calling benchmark",
    "site:x.com Qwen3.8 GGUF quantized",
    "site:x.com gemma4 tool calling",
    "site:x.com cloudflare clef decision model ollama",
    "site:x.com tokens per second 5600 XT",
    "site:x.com phi small model agent",
    "site:x.com mistral 8B local agent",
]

LINK_RE = re.compile(r'href="//duckduckgo\.com/l/\?uddg=([^&"]+)&amp;rut=')
SNIP_RE = re.compile(r'<a[^>]*class="result__snippet"[^>]*>(.*?)</a>', re.S)
TITLE_RE = re.compile(r'<a[^>]*class="result__a"[^>]*>(.*?)</a>', re.S)
TAG_RE = re.compile(r'<[^>]+>')


def strip(h):
    return TAG_RE.sub('', h).replace('&amp;', '&').replace('&#x27;', "'").replace(
        '&quot;', '"').replace('&lt;', '<').replace('&gt;', '>').strip()


def fetch(q):
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001
            print(f"  fetch error attempt {attempt}: {e}")
            time.sleep(3 + attempt * 3)
    return ""


def main():
    seen = {}
    for q in QUERIES:
        print(f"QUERY: {q}")
        html = fetch(q)
        time.sleep(2.5)
        if not html:
            continue
        # pair up result blocks: split on result__a anchors
        blocks = re.split(r'(?=<a[^>]*class="result__a")', html)
        titles = TITLE_RE.findall(html)
        for b in blocks[1:]:
            m = re.search(r'href="//duckduckgo\.com/l/\?uddg=([^&"]+)&amp;', b)
            if not m:
                continue
            real = urllib.parse.unquote(m.group(1))
            tm = re.search(r'<a[^>]*class="result__a"[^>]*>(.*?)</a>', b, re.S)
            sm = re.search(r'<a[^>]*class="result__snippet"[^>]*>(.*?)</a>', b, re.S)
            title = strip(tm.group(1)) if tm else ""
            snip = strip(sm.group(1)) if sm else ""
            if "x.com/" not in real:
                continue
            if real not in seen:
                seen[real] = {"url": real, "title": title, "snippet": snip,
                              "query": q}
        print(f"  cumulative unique x.com urls: {len(seen)}")
    out = list(seen.values())
    with open("watch/inbox/frontier_olm_adhoc/sweep/_rx_ddg_candidates.json",
              "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    print(f"TOTAL unique x.com candidate urls: {len(out)}")
    for c in out:
        sid = re.search(r"x\.com/([A-Za-z0-9_]+)/status/(\d+)", c["url"])
        print(("STATUS " if sid else "OTHER  ") + c["url"][:90] + " | " +
              c["title"][:60])


if __name__ == "__main__":
    main()
