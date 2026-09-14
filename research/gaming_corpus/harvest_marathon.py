"""termlink harvest: marathon.bungie.org/story terminal text -> plain .txt per chapter.
Domain-locked to marathon.bungie.org (NETWORK LAW 09-06). ~1 req/sec politeness."""
import re, sys, time, html as htmlmod
import urllib.request
from urllib.parse import urljoin

BASE = "https://marathon.bungie.org/story/"
ALLOWED_HOST = "marathon.bungie.org"
UA = "termlink-harvester/1 (fan-archive research; credit marathon.bungie.org)"
OUT = "research/gaming_corpus/marathon_terminals"

CHAPTERS = {
    "m1": [
        ("arrival", "Arrival"),
        ("counterattack", "Counterattack"),
        ("reprisal", "Reprisal"),
        ("durandal", "Durandal"),
        ("pfhor", "The Pfhor"),
        ("rebellion", "Rebellion"),
    ],
    "m2": [
        ("lhowon", "Lh'owon"),
        ("volunteers", "Volunteers"),
        ("garrison", "Garrison"),
        ("citadel", "Citadel"),
        ("durandal2", "Durandal"),
        ("captured", "Captured"),
        ("blake", "Blake"),
        ("simulacrums", "Simulacrums"),
        ("sphtkr", "S'pht'Kr"),
        ("necedemalis", "Ne Cede Malis"),
    ],
}

def fetch(path):
    assert ALLOWED_HOST in BASE, "domain lock"
    url = urljoin(BASE, path)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read().decode("utf-8", "replace")
    time.sleep(1.0)  # politeness
    return url, data

TAG_BREAK = re.compile(r"(?i)</?(br|p|div|tr|td|table|h[1-6]|hr|li)[^>]*>")
SCRIPT = re.compile(r"(?is)<script.*?</script>")
STYLE = re.compile(r"(?is)<style.*?</style>")
COMMENT = re.compile(r"<!--.*?-->", re.S)
ANYTAG = re.compile(r"<[^>]+>")
H4 = re.compile(r"(?is)<h4[^>]*>(.*?)</h4>")

def html_to_text(chunk):
    chunk = SCRIPT.sub("", chunk)
    chunk = STYLE.sub("", chunk)
    chunk = COMMENT.sub("", chunk)
    chunk = TAG_BREAK.sub("\n", chunk)
    chunk = ANYTAG.sub("", chunk)
    chunk = htmlmod.unescape(chunk)
    lines = [ln.strip() for ln in chunk.split("\n")]
    out, blank = [], 0
    for ln in lines:
        if not ln:
            blank += 1
            if blank > 1:
                continue
        else:
            blank = 0
        out.append(ln)
    return "\n".join(out).strip()

def parse_chapter(html):
    """Return list of (terminal_title, text) sections split on <h4> headings."""
    sections = []
    matches = list(H4.finditer(html))
    if not matches:
        return [("chapter-header", html_to_text(html))]
    pre = html_to_text(html[: matches[0].start()])
    for i, m in enumerate(matches):
        title = html_to_text(m.group(1))
        end = matches[i + 1].start() if i + 1 < len(matches) else len(html)
        body = html_to_text(html[m.end(): end])
        sections.append((title, body))
    return sections

def main():
    fetched = 1  # contents.html already fetched
    report = {}
    for game, chapters in CHAPTERS.items():
        for slug, label in chapters:
            url, doc = fetch(slug + ".html")
            fetched += 1
            sections = parse_chapter(doc)
            parts = [f"SOURCE: {url}\nCHAPTER: {label}\nARCHIVE: marathon.bungie.org (fan-maintained; cite on any use)"]
            nterm = 0
            for title, body in sections:
                if "(Terminal" in title:
                    nterm += 1
                parts.append(f"\n\n{'='*70}\n### {title}\n{'='*70}\n\n{body}")
            text = "\n".join(parts)
            path = f"{OUT}/{game}/{slug}.txt"
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            report[f"{game}/{slug}"] = (label, nterm, len(text))
            print(f"{game}/{slug}: {label:14s} terminals={nterm:3d} chars={len(text)}")
    print("TOTAL_PAGES_FETCHED", fetched)
    with open(f"{OUT}/_harvest_log.txt", "w", encoding="utf-8") as f:
        for k, (label, nterm, chars) in report.items():
            f.write(f"{k}\t{label}\tterminals={nterm}\tchars={chars}\n")

if __name__ == "__main__":
    sys.exit(main())
