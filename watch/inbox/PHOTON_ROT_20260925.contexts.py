# PHOTON_ROT_20260925.contexts.py - print live-post text around key phrases
# so the current (post-revision) wording can be quoted beside the stranded quotes.
import html
import re
import sys
import unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LIVE = Path(r"C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/PHOTON_ROT_20260925.live.html")


def to_text(raw: bytes) -> str:
    s = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)),
               raw.decode("utf-8", errors="replace"))
    s = html.unescape(s)
    return re.sub(r"<[^>]+>", " ", s)


def canon(s: str) -> str:
    s = unicodedata.normalize("NFC", s)
    s = re.sub(r"[\u2010\u2011\u2012\u2013\u2014\u2015\u2212]", "-", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


text = canon(to_text(LIVE.read_bytes()))
keys = ["20% fewer", "month", "controller", "interrupt", "resumable", "checkpoint",
        "statistically", "mirroring", "incumbent", "all production traffic", "five"]
for key in keys:
    for m in list(re.finditer(re.escape(key), text, re.I))[:4]:
        a, b = max(0, m.start() - 200), min(len(text), m.end() + 260)
        print(f"=== {key!r} @ {m.start()} ===")
        print(text[a:b])
        print()
