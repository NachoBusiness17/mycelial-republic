"""PD3 — founding-law canon fetch.

Fixed URL manifest, stdlib urllib only (house style: see N6 / fetch_training_pdfs.py).
Output: memory/corpus/founding_law/ + manifest.json
Robots checked manually 2026-09-16 (see watch/inbox/wave_20260916/receipts/PD3_FOUNDING_LAW.md):
  - www.archives.gov: crawl-delay 10, targets allowed
  - www.congress.gov: crawl-delay 2, /search disallowed (not used here)
  - crsreports.congress.gov: no robots.txt rules
  - www.gutenberg.org: only /ebooks/search disallowed (not used)
  - avalon.law.yale.edu: no robots.txt (error page == no rules)
"""
from __future__ import annotations

import hashlib
import json
import re
import time
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "memory" / "corpus" / "founding_law"
UA = "MagResourceHarness/0.1 (public-domain corpus fetch; contact: local operator)"
DELAY = {"www.archives.gov": 10, "www.congress.gov": 2, "crsreports.congress.gov": 2}

MANIFEST = [
    {
        "id": "magna_carta_1215",
        "title": "Magna Carta (1215) — English translation, Yale Avalon (public-domain translation; BL preferred but bl.uk outside sanctioned fetch domains)",
        "url": "https://avalon.law.yale.edu/medieval/magna.asp",
        "kind": "html",
        "checks": ["John", "freemen", "law of the land"],
    },
    {
        "id": "constitution_nara_transcript",
        "title": "Constitution of the United States — original transcript, National Archives (7 articles, unaltered text intact)",
        "url": "https://www.archives.gov/founding-docs/constitution-transcript",
        "kind": "html",
        "checks": ["We the People", "Article. VII"],  # NARA keeps original period-punctuated headings
    },
    {
        "id": "bill_of_rights_nara_transcript",
        "title": "Bill of Rights (Amendments I-X) — National Archives transcript",
        "url": "https://www.archives.gov/founding-docs/bill-of-rights-transcript",
        "kind": "html",
        "checks": ["Amendment I", "Amendment X"],
    },
    {
        "id": "amendments_11_27_nara_transcript",
        "title": "Amendments XI-XXVII — National Archives transcript (includes XXI repealing XVIII: repeal by addition; XIX: retroactive fix)",
        "url": "https://www.archives.gov/founding-docs/amendments-11-27",
        "kind": "html",
        "checks": ["Amendment XI", "Amendment XXI", "Amendment XXVII"],
    },
    {
        "id": "amendment_19_nara",
        "title": "19th Amendment — National Archives milestone document (transcript + background): retroactive-fix amendment",
        "url": "https://www.archives.gov/milestone-documents/19th-amendment",
        "kind": "html",
        "checks": ["vote", "sex"],
    },
    {
        "id": "federalist_papers_gutenberg_1404",
        "title": "The Federalist Papers (Hamilton, Madison, Jay) — Project Gutenberg ebook #1404, plain text (includes No. 78 on judicial review)",
        "url": "https://www.gutenberg.org/cache/epub/1404/pg1404.txt",
        "kind": "text",
        "checks": ["FEDERALIST", "Hamilton"],
    },
    {
        "id": "crs_modes_of_constitutional_interpretation",
        "title": "CRS Report R45129, Modes of Constitutional Interpretation — neutral primer on originalism vs living constitution (US Gov work)",
        "url": "https://crsreports.congress.gov/product/pdf/R/R45129",
        "kind": "pdf",
        "checks": [],
    },
]


class TextExtractor(HTMLParser):
    """Strip tags, keep block-level structure. Skips script/style/noscript/head."""

    SKIP = {"script", "style", "noscript", "head", "svg", "iframe"}
    BLOCK = {
        "p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6",
        "section", "article", "table", "blockquote", "hr", "ul", "ol",
    }

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self._skip_depth += 1
        elif tag in self.BLOCK and self._skip_depth == 0:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self._skip_depth > 0:
            self._skip_depth -= 1
        elif tag in self.BLOCK and self._skip_depth == 0:
            self.parts.append("\n")

    def handle_data(self, data):
        if self._skip_depth == 0 and data.strip():
            self.parts.append(data)

    def text(self) -> str:
        raw = "".join(self.parts)
        raw = re.sub(r"[ \t]+", " ", raw)
        raw = re.sub(r" ?\n ?", "\n", raw)
        raw = re.sub(r"\n{3,}", "\n\n", raw)
        return raw.strip() + "\n"


def fetch(url: str) -> tuple[bytes, int]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read(), resp.status


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    entries: list[dict] = []
    last_host: str | None = None

    for item in MANIFEST:
        host = urllib.parse.urlsplit(item["url"]).netloc
        if last_host and last_host == host and host in DELAY:
            print(f"  (crawl-delay {DELAY[host]}s for {host})")
            time.sleep(DELAY[host])
        last_host = host

        entry = {
            "id": item["id"],
            "title": item["title"],
            "url": item["url"],
            "status": "fetched",
            "files": {},
        }
        try:
            body, status = fetch(item["url"])
            print(f"[{status}] {item['id']} <- {item['url']} ({len(body)} bytes)")
            entry["http_status"] = status

            if item["kind"] == "html":
                raw_path = OUT / f"{item['id']}.html"
                raw_path.write_bytes(body)
                entry["files"]["raw"] = raw_path.name
                txt = TextExtractor()
                txt.feed(body.decode("utf-8", errors="replace"))
                text = txt.text()
            elif item["kind"] == "text":
                text = body.decode("utf-8", errors="replace")
            else:  # pdf — save bytes; text extraction left to the reader
                raw_path = OUT / f"{item['id']}.pdf"
                raw_path.write_bytes(body)
                entry["files"]["raw"] = raw_path.name
                text = None

            if text is not None:
                out_path = OUT / f"{item['id']}.txt"
                out_path.write_text(text, encoding="utf-8")
                entry["files"]["text"] = out_path.name

                missing = [c for c in item["checks"] if c.lower() not in text.lower()]
                if item["checks"] and missing:
                    entry["status"] = "fetched_content_warning"
                    entry["missing_checks"] = missing
                    print(f"  WARNING: missing content checks: {missing}")
                else:
                    print(f"  content checks OK ({len(text)} chars)")
        except Exception as exc:  # noqa: BLE001 — record honestly
            entry["status"] = f"failed: {type(exc).__name__}: {exc}"
            print(f"  FAILED: {entry['status']}")

        entries.append(entry)

    manifest_path = OUT / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "lane": "PD3",
                "date": "2026-09-16",
                "description": "Founding-law canon: the append-only amendment lineage the VOID procedure inherits.",
                "receipt": "watch/inbox/wave_20260916/receipts/PD3_FOUNDING_LAW.md",
                "entries": entries,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"manifest -> {manifest_path}")


if __name__ == "__main__":
    import urllib.parse  # noqa: E402 (used in main via module namespace)

    main()
