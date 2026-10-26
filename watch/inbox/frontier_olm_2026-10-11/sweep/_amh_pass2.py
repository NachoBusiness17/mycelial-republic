"""amh pass2: deep reads for agent-memory-continuity HN sweep (2026-10-11).

Fetches (a) HN comment trees via the Algolia items API and (b) primary article
HTML, saving byte receipts to _amh_p2_<name>.txt. SSRF guard: https only,
host must be in _ALLOWED_HOSTS. Text extraction: stdlib html.parser.
"""
import json
import re
import time
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent

_ALLOWED_HOSTS = {
    "hn.algolia.com", "raw.githubusercontent.com", "blog.szypowi.cz",
    "swarmagent.dev", "gethrbr.com", "ruttermemory.com", "github.com",
    "code.claude.com", "jotbus.com",
}

# (receipt name, url)
FETCHES = [
    # HN threads (Algolia items API = full comment tree)
    ("hn_49760187", "https://hn.algolia.com/api/v1/items/49760187"),
    ("hn_49783133", "https://hn.algolia.com/api/v1/items/49783133"),
    ("hn_49867329", "https://hn.algolia.com/api/v1/items/49867329"),
    ("hn_50038733", "https://hn.algolia.com/api/v1/items/50038733"),
    ("hn_49828496", "https://hn.algolia.com/api/v1/items/49828496"),
    ("hn_50029798", "https://hn.algolia.com/api/v1/items/50029798"),
    ("hn_49978401", "https://hn.algolia.com/api/v1/items/49978401"),
    # primary pages
    ("ihmt_readme", "https://raw.githubusercontent.com/gonzaroman/IHMT-MEMORY/main/README.md"),
    ("szypowi_agentsmd", "https://blog.szypowi.cz/p/claude-code-reads-agents-md-only-when-telemetry-is-on/"),
    ("swarmagent_plans", "https://swarmagent.dev/resources/engineering/plans-harnesses-and-final-handoffs/"),
    ("hrbr_agentsmd_research", "https://gethrbr.com/blog/is-agents-md-useful"),
    ("rutter", "https://ruttermemory.com/"),
    ("jotbus", "https://jotbus.com/"),
]


def guard(url: str) -> None:
    p = urllib.parse.urlparse(url)
    if p.scheme != "https" or p.hostname not in _ALLOWED_HOSTS:
        raise ValueError(f"blocked non-allowlisted fetch target: {p.scheme} {p.hostname}")


def fetch(url: str, tries: int = 2) -> bytes:
    guard(url)
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) mag-frontier-sweep/1.0"})
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 * (i + 1))
    raise RuntimeError(f"fetch failed {url}: {last}")


class _Text(HTMLParser):
    SKIP = {"script", "style", "noscript", "svg", "head"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self._skip += 1
        if tag in ("p", "div", "li", "h1", "h2", "h3", "h4", "br", "tr"):
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if not self._skip and data.strip():
            self.out.append(data)


def html_to_text(raw: bytes) -> str:
    p = _Text()
    p.feed(raw.decode("utf-8", errors="replace"))
    text = "".join(p.out)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return re.sub(r"[ \t]{2,}", " ", text)


def flatten_comments(node: dict, depth: int = 0, out: list | None = None) -> list:
    if out is None:
        out = []
    author = node.get("author") or "?"
    text = re.sub(r"<[^>]+>", " ", node.get("text") or "")
    text = re.sub(r"\s+", " ", text).strip()
    if text:
        out.append(("  " * depth) + f"[{author}] {text}")
    for ch in node.get("children", []):
        flatten_comments(ch, depth + 1, out)
    return out


def main() -> None:
    report = []
    for name, url in FETCHES:
        try:
            raw = fetch(url)
            (HERE / f"_amh_p2_{name}.raw").write_bytes(raw)
            if url.startswith("https://hn.algolia.com"):
                tree = json.loads(raw.decode("utf-8"))
                lines = flatten_comments(tree)
                body = (f"TITLE: {tree.get('title')}\nAUTHOR: {tree.get('author')}\n"
                        f"POINTS: {tree.get('points')}\n\n" + "\n".join(lines))
            elif url.endswith(".md") or "raw.githubusercontent" in url:
                body = raw.decode("utf-8", errors="replace")
            else:
                body = html_to_text(raw)
            (HERE / f"_amh_p2_{name}.txt").write_text(body, encoding="utf-8")
            report.append((name, url, len(raw), len(body), "OK"))
        except Exception as e:  # noqa: BLE001
            report.append((name, url, 0, 0, f"FAIL {e}"))
        time.sleep(0.3)
    for name, url, nbytes, nchars, status in report:
        print(f"{name:24s} {status:8s} bytes={nbytes:7d} chars={nchars:7d} {url}")


if __name__ == "__main__":
    main()
