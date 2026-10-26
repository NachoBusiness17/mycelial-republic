"""Letter salon — the operator's 9/20 handwritten journal through the living chairs.

Commission (verbatim, from the letter): "send this Journal through the factory
Dogfooding our systems and do a coldest shard veil tex map."

Dogfood: each chair's RIB is the lens — docs/ref/ractors/<CHAIR>.md brief where
one exists, corpus/ractor_ribs/<CHAIR>/invariants.md always. The letter is the
object; view_through(chair, letter). One remote deepseek-chat call per chair
(temp 0.4, max 700). Receipts to memory/runs/elder_asks/ask_operator_letter_20260920/.

The letter asks the estate three questions; each chair answers as itself:
  Q1 "So what do you want Mag?"   Q2 "So where to?"
  Q3 "What do you think of riddlers and my Quest?" + "What do you want to tell me?"
"""
from __future__ import annotations

import ipaddress
import json
import re
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config import ROOT  # noqa: E402

OUTDIR = ROOT / "memory" / "runs" / "elder_asks" / "ask_operator_letter_20260920"
LETTER = ROOT / "watch" / "inbox" / "OPERATOR_JOURNAL_20260920.md"
CHAIRS = ["JUNG", "FREUD", "ELLUL", "BERNAYS", "GREER", "EULER"]

_API_URL = "https://api.deepseek.com/chat/completions"


def _validated_api_url() -> str:
    parts = urllib.parse.urlsplit(_API_URL)
    if parts.scheme != "https" or parts.hostname != "api.deepseek.com":
        raise ValueError("unsanctioned API URL")
    for info in socket.getaddrinfo(parts.hostname, 443, proto=socket.IPPROTO_TCP):
        ip = ipaddress.ip_address(info[4][0])
        if (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved
                or ip.is_multicast or ip.is_unspecified):
            raise ValueError(f"resolved address {ip} is in a blocked range")
    return _API_URL


def letter_text() -> str:
    md = LETTER.read_text(encoding="utf-8")
    m = re.search(r"## Transcription \(verbatim\)\n(.*?)\n## ", md, flags=re.S)
    return m.group(1).strip() if m else md


def chair_lens(chair: str) -> str:
    brief_p = ROOT / "docs" / "ref" / "ractors" / f"{chair}.md"
    inv_p = ROOT / "corpus" / "ractor_ribs" / chair / "invariants.md"
    parts = []
    if brief_p.exists():
        parts.append(f"BRIEF:\n{brief_p.read_text(encoding='utf-8')[:6000]}")
    if inv_p.exists():
        parts.append(f"LIVING-LENS INVARIANTS:\n{inv_p.read_text(encoding='utf-8')[:4000]}")
    if not parts:
        raise FileNotFoundError(chair)
    return "\n\n".join(parts)


def ask(chair: str, lens: str, letter: str) -> dict:
    from models.providers import get_provider, provider_keys
    keys = provider_keys(get_provider("deepseek") or {})
    if not keys:
        return {"ok": False, "error": "no key"}
    user = (
        f"The operator of this estate wrote a letter by hand, in his journal, addressed to the "
        f"fleet. You are one of its chairs. Read it through YOUR invariants only — do not speak "
        f"for other chairs.\n\nLETTER (verbatim transcription):\n\"\"\"\n{letter}\n\"\"\"\n\n"
        f"Answer, as yourself, tersely and concretely (no flattery, no hedging):\n"
        f"1. What do you want — from him, for this estate? (He asked us directly.)\n"
        f"2. Where to? (next era: the work rejected him and he it; he wants to build the new "
        f"one that uplifts rather than enslaves.)\n"
        f"3. The riddlers and his Quest — your view, in one paragraph. Context you may use: "
        f"his Quest absorbed three riddle corpora (Q, MrPool, BearableGuy) and the estate's "
        f"verdicts were: Q holds 3 dated claims in 4,705 posts (unfalsifiable by "
        f"construction); Pool's called-shot ledger 94/107 expired broken, zero retractions; "
        f"BG123's empty set was itself the data. His own riddler protocol turns secrets into "
        f"decipherment-cost — surrogate stories, private maps — and that one WORKS.\n"
        f"4. One thing you want to tell him that nobody else in this factory will say.")
    payload = {"model": "deepseek-chat", "temperature": 0.4, "max_tokens": 700,
               "messages": [{"role": "system", "content": lens},
                            {"role": "user", "content": user}]}
    req = urllib.request.Request(
        _validated_api_url(), data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {keys[0]}"},
        method="POST")
    for attempt in (0, 1):
        try:
            with urllib.request.urlopen(req, timeout=240) as r:
                data = json.loads(r.read().decode("utf-8"))
            text = ((data.get("choices") or [{}])[0].get("message", {}).get("content") or "").strip()
            return {"ok": True, "text": text, "usage": data.get("usage") or {}}
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt == 0:
                time.sleep(15)
                continue
            return {"ok": False, "error": f"HTTP {e.code}"}
        except Exception as e:  # noqa: BLE001
            if attempt == 0:
                time.sleep(5)
                continue
            return {"ok": False, "error": str(e)[:200]}
    return {"ok": False, "error": "429 x2"}


def main() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    letter = letter_text()
    lens_cache = {}
    manifest = {"utc": datetime.now(timezone.utc).isoformat(), "chairs": {}}
    for chair in CHAIRS:
        try:
            lens = lens_cache.setdefault(chair, chair_lens(chair))
        except FileNotFoundError:
            print(f"[{chair}] NO RIB — skipped", flush=True)
            continue
        r = ask(chair, lens, letter)
        if not r["ok"]:
            print(f"[{chair}] FAIL {r['error']}", flush=True)
            manifest["chairs"][chair] = {"ok": False, "error": r["error"]}
            continue
        (OUTDIR / f"{chair}.md").write_text(
            f"# {chair} — view_through({chair}, operator letter 9/20)\n\n{r['text']}\n",
            encoding="utf-8")
        manifest["chairs"][chair] = {"ok": True, "chars": len(r["text"]),
                                     "tokens": r["usage"].get("completion_tokens")}
        print(f"[{chair}] ok {len(r['text'])} chars", flush=True)
        time.sleep(1.0)
    (OUTDIR / "manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    print(f"[done] {sum(1 for c in manifest['chairs'].values() if c.get('ok'))}/{len(CHAIRS)} chairs",
          flush=True)


if __name__ == "__main__":
    main()
