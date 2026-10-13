"""x_churn_cli — the SD-seat batch driver: 20 Grok-CLI queries, one fresh headless
invocation each (no cumulative seat context bleed), status IDs extracted from raw
output, deduped against the estate inventory, vxtwitter-pulled, anchor-graded.
Rides the SD seat per operator GO (2026-09-23 night). Deterministic wrapper; no LLM
on our side — Grok's own live X search does the finding.
SSRF law: the vxtwitter door passes lite_guard._safe_https_url + no-redirect opener.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from mag import lite_guard  # noqa: E402  (SSRF validator + no-redirect opener)

GROK_EXE = r"C:\Users\foste\.grok\bin\grok.exe"
SD_HOME = r"C:\Users\foste\.grok-sd"
OUT_MD = ROOT / "watch" / "inbox" / "X_ANCHOR_MAP_SD_SEAT_20260923.md"
OUT_JSONL = ROOT / "state" / "fuel" / "x_churn_hits_sd.jsonl"
RAW_IDS = ROOT / "state" / "fuel" / "x_churn_sd_raw.txt"
ID_RE = re.compile(r"x\.com/NachoQuixotic/status/(\d{18,20})")
HANDLE = "NachoQuixotic"

INVENTORY_FILES = [
    ROOT / "watch" / "inbox" / "ACCOUNT_VS_AUDIT_20260923.md",
    ROOT / "corpus" / "canon" / "founding_curriculum" / "FOUNDING_CURRICULUM.md",
    ROOT / "corpus" / "canon" / "x_canon_2025_pass3.md",
    ROOT / "corpus" / "canon" / "x_canon_2025_pass6.md",
    ROOT / "corpus" / "canon" / "receipts_dec2025_mar2026.md",
]

QUERIES = [
    ("smith-mundt", "from:NachoQuixotic Smith-Mundt OR HR 5736 OR propaganda"),
    ("church-surveillance", "from:NachoQuixotic Church Committee OR COINTELPRO OR SHAMROCK OR surveillance"),
    ("cic-echoic", "from:NachoQuixotic censorship industrial complex OR echoic drift OR Rashomon"),
    ("bernays-ellul", "from:NachoQuixotic Bernays OR Ellul OR manufacturing consent"),
    ("gilens-page", "from:NachoQuixotic oligarchy OR elites policy OR Gilens"),
    ("money-fed", "from:NachoQuixotic federal reserve OR Jekyll Island OR fiat OR debt slavery"),
    ("epstein-network", "from:NachoQuixotic Epstein OR Maxwell OR Brunel OR island"),
    ("dutroux-belgium", "from:NachoQuixotic Dutroux OR Belgium OR X-dossiers"),
    ("franklin-coverup", "from:NachoQuixotic Franklin OR Nebraska cover-up"),
    ("mkultra", "from:NachoQuixotic MKULTRA OR Helms OR Gottlieb"),
    ("mystery-schools", "from:NachoQuixotic mystery schools OR mystery cults OR Eleusis"),
    ("templars-pike", "from:NachoQuixotic Templars OR Albert Pike OR Palladium"),
    ("tartaria", "from:NachoQuixotic Tartaria OR mudflood OR old world"),
    ("dead-sea-scrolls", "from:NachoQuixotic Dead Sea Scrolls OR Enoch"),
    ("adrenochrome", "from:NachoQuixotic adrenochrome OR Huxley"),
    ("loosh-entities", "from:NachoQuixotic loosh OR McKenna OR machine elves"),
    ("black-nobility", "from:NachoQuixotic Black Nobility OR bloodlines OR dynasties"),
    ("bohemian-grove", "from:NachoQuixotic Bohemian Grove OR Cremation of Care"),
    ("apathy-consent", "from:NachoQuixotic apathy as consent OR attention is valuable"),
    ("vision-consciousness", "from:NachoQuixotic vision OR awakening OR consciousness force"),
]

ANCHOR_SIGNALS = re.compile(
    r"(19\d\d|20\d\d)|("
    r"Smith-Mundt|Church|COINTELPRO|MKULTRA|Bernays|Ellul|Jung|Wasson|Hofmann|Ruck|Eleusis|"
    r"Epstein|Maxwell|Brunel|Dutroux|Franklin|Pike|Taxil|Margiotta|Illuminati|Bavarian|"
    r"Tartaria|Enoch|Dead Sea|adrenochrome|Huxley|loosh|Bohemian|Grove|Jekyll|Rothschild|Rockefeller|"
    r"Federal Reserve|Torture Report|Pentagon Papers|Family Jewels|Operation |CTIL|GEC|USAID)", re.I)


def known_ids() -> set:
    ids = set()
    for p in INVENTORY_FILES:
        if p.is_file():
            ids |= set(ID_RE.findall(p.read_text(encoding="utf-8", errors="replace")))
    return ids


def run_cli_query(query: str) -> str:
    env = dict(os.environ)
    env["GROK_HOME"] = SD_HOME
    prompt = (f"Search X for posts by @{HANDLE} matching: {query}\n"
              f"List EVERY matching post you can find. For each give the full status URL "
              f"(https://x.com/{HANDLE}/status/<id>), the post date, like count if visible, "
              f"and a one-sentence gist. Only real posts by this handle. No commentary.")
    r = subprocess.run([GROK_EXE, "--output-format", "plain", prompt],
                       capture_output=True, text=True, timeout=420,
                       env=env, errors="replace")
    return (r.stdout or "") + "\n" + (r.stderr or "")


def pull_post(pid: str) -> dict | None:
    if not re.fullmatch(r"\d{18,20}", pid):
        return None
    from mag import lite_guard
    url = f"https://api.vxtwitter.com/{HANDLE}/status/{pid}"
    if not lite_guard._safe_https_url(url):
        return None
    try:
        req = urllib.request.Request(url)
        with lite_guard._OPENER.open(req, timeout=20) as r:
            d = json.loads(r.read().decode())
        return {"id": pid, "date": d.get("date"), "text": (d.get("text") or "")[:600],
                "likes": d.get("likes"), "rts": d.get("retweets")}
    except Exception:
        return None


def cialdini_summary(text: str) -> dict:
    """Persuasion-payload scan at the intake read path (DOUBLE_DROP_20261001.md).

    Every filed hit row is untrusted content entering an agentic loop; the scan
    rides the row so the reading lane sees the payload class, not just the gist.
    Deterministic: tools/cialdini_scanner.py, the 7 Cialdini influence patterns.
    """
    from tools.cialdini_scanner import scan  # lazy: stdlib-only module, no cycle
    s = scan(text or "")
    return {"n_findings": s["n_findings"],
            "worst_confidence": s["worst_confidence"],
            "patterns": sorted(pid for pid, st in s["pattern_hits"].items() if st["hits"]),
            "verdict": s["verdict"]}


def main() -> dict:
    known = known_ids()
    raw_ids: dict[str, str] = {}
    for family, q in QUERIES:
        t0 = time.time()
        try:
            out = run_cli_query(q)
        except Exception as e:
            out = "QUERY_FAIL " + type(e).__name__ + ": " + str(e)[:80]
        for pid in set(ID_RE.findall(out)):
            raw_ids.setdefault(pid, family)
        log = {"family": family, "ts": datetime.now(timezone.utc).isoformat(),
               "ids_found": len(set(ID_RE.findall(out))), "secs": round(time.time() - t0)}
        print(json.dumps(log), flush=True)
        RAW_IDS.parent.mkdir(parents=True, exist_ok=True)
        with RAW_IDS.open("a", encoding="utf-8") as f:
            f.write(json.dumps(log) + "\n")

    new_ids = [pid for pid in raw_ids if pid not in known]
    hits = []
    misses = 0
    for pid in new_ids:
        post = pull_post(pid)
        if not post or not (post.get("text") or "").strip():
            misses += 1
            continue
        if ANCHOR_SIGNALS.search(post["text"]):
            hits.append({"family": raw_ids[pid], **post,
                         "cialdini": cialdini_summary(post["text"])})
        else:
            misses += 1
    for h in sorted(hits, key=lambda h: -(h.get("likes") or 0)):
        OUT_JSONL.parent.mkdir(parents=True, exist_ok=True)
        with OUT_JSONL.open("a", encoding="utf-8") as f:
            f.write(json.dumps(h) + "\n")

    md = [
        "# X ANCHOR MAP — SD-seat churn, missing @NachoQuixotic posts",
        "",
        f"2026-09-23 · seat: SD (second Grok account) · queries: {len(QUERIES)} · "
        f"known inventory IDs: {len(known)} · new posts: {len(new_ids)} · hits: {len(hits)} · misses: {misses}",
        "",
        "A HIT = a post missing from the estate inventory carrying receipts language, "
        "checkable dates/numbers, named documents, or ties to a ledger family.",
        "",
        "## Hits, by engagement",
        "",
    ]
    for h in sorted(hits, key=lambda h: -(h.get("likes") or 0)):
        md.append(f"- **{h['date']}** · {h['likes']} likes · RTs {h.get('rts')} · family: {h['family']}")
        md.append(f"  - https://x.com/{HANDLE}/status/{h['id']}")
        md.append(f"  - > {(h['text'] or '')[:220].replace(chr(10), ' ')}")
        if h.get("cialdini", {}).get("n_findings"):
            md.append(f"  - PERSUASION-FLAG: {h['cialdini']['verdict']} "
                      f"[{', '.join(h['cialdini']['patterns'])}]")
    md += ["", "*Append-only. Anchors feed the conversion plan's re-ladder.*"]
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    return {"new_posts": len(new_ids), "hits": len(hits), "misses": misses,
            "queries": len(QUERIES), "file": str(OUT_MD)}


if __name__ == "__main__":
    print(json.dumps(main(), indent=1))
