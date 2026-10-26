"""Confirmation pass, part 3: 6 reddit items via the RSS door (pacing, browser UA)."""
import re
import time
import html as htmlmod
import urllib.request
import urllib.error
import urllib.parse

ALLOWED = {"www.reddit.com", "old.reddit.com"}
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


class G(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if urllib.parse.urlsplit(newurl).hostname.lower() not in ALLOWED:
            raise urllib.error.URLError(f"redirect blocked: {newurl}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


OP = urllib.request.build_opener(G)


def fetch(url, timeout=45):
    scheme, host = urllib.parse.urlsplit(url)[:2]
    if scheme != "https" or host.lower() not in ALLOWED:
        raise urllib.error.URLError(f"blocked: {url}")
    req = urllib.request.Request(url, headers=UA)
    return OP.open(req, timeout=timeout).read().decode("utf-8", errors="replace")


def norm(s):
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    return re.sub(r"\s+", " ", s).lower()


THREADS = [
    ("unswallow", "https://www.reddit.com/r/ollama/comments/1wc6tka/.rss",
     ["tool_calls", "think"]),
    ("CodeFinetuner", "https://www.reddit.com/r/LocalLLaMA/comments/1wdp9qc/.rss",
     ["sweet spot", "codebleu"]),
    ("FunctionGemma", "https://www.reddit.com/r/LocalLLaMA/comments/1r6gx75/.rss",
     ["270m", "90.9"]),
    ("RustVulkan", "https://www.reddit.com/r/LocalLLaMA/comments/1wu6cbl/.rss",
     ["2e-7", "lora"]),
    ("Spanda", "https://www.reddit.com/r/ollama/comments/1wdasar/.rss",
     ["entropy", "0.89"]),
    ("hemmingway-1", "https://www.reddit.com/r/LocalLLM/comments/1wlhh08/.rss",
     ["1330", "eq-bench"]),
]

for label, url, needles in THREADS:
    try:
        raw = fetch(url)
        # RSS <content:encoded> or <content> entries carry post+comments
        entries = re.findall(r"<(?:content:encoded|content)>(.*?)</(?:content:encoded|content)>", raw, re.S)
        blob = norm(htmlmod.unescape(" ".join(entries)))
        if not blob:
            blob = norm(htmlmod.unescape(raw))
        hits = [n for n in needles if norm(n) in blob]
        verdict = "CONFIRMED" if len(hits) == len(needles) else ("PARTIAL" if hits else "QUOTE_ABSENT")
        print(f"{label} | {verdict} | hits {len(hits)}/{len(needles)} | entries {len(entries)} | {len(raw)} bytes")
    except Exception as e:
        print(f"{label} | DEAD | {type(e).__name__}: {e}")
    time.sleep(9)
