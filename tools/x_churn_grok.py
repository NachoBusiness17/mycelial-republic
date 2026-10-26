"""x_churn_grok — mine @NachoQuixotic's timeline for posts MISSING from the estate
inventory, via the second Grok key's live X search (operator GO, 2026-09-23 night).

Import-law audit:
  SPENDS: xAI credits on GROK_API_KEY_2 ONLY (operator-armed for this named job).
  CAP:    MAX_QUERIES search calls per run (default 30); every call logged to
          state/fuel/x_churn_ledger.jsonl with usage.
  SSRF:   every outbound URL passes lite_guard._safe_https_url; redirects refused
          via lite_guard._OPENER (Mimosa law, mirrors gopher_lite).
  DEDUPE: candidate post IDs are dropped if present in the estate's known
          inventory (account-vs-audit, founding curriculum, x_canon, receipts).
  HITS:   a new post is a HIT when it anchors content — receipts language,
          checkable dates/numbers/named documents, or ties to a ledger family.
          Misses (flops, out-of-scope, duplicates) are discarded, not filed.

CLI: python tools/x_churn_grok.py
"""
from __future__ import annotations

import json
import re
import sys
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


def _grok_key() -> str:
    # load_env does not surface GROK_API_KEY_2 (audit finding, 09-23): parse the
    # root .env line directly. The value is never printed or logged.
    envf = ROOT / ".env"
    try:
        for line in envf.read_text(encoding="utf-8", errors="replace").splitlines():
            m = re.match(r"^\s*GROK_API_KEY_2\s*=\s*(\S+)\s*$", line)
            if m:
                return m.group(1).strip().strip('"').strip("'")
    except Exception:
        pass
    return ""


KEY = _grok_key()
API = "https://api.x.ai/v1/chat/completions"
VX = "https://api.vxtwitter.com/"
MODELS = ["grok-4-fast", "grok-3-mini", "grok-3"]
MAX_QUERIES = 30
LEDGER = ROOT / "state" / "fuel" / "x_churn_ledger.jsonl"
OUT_MD = ROOT / "watch" / "inbox" / "X_ANCHOR_MAP_20260923.md"
OUT_JSONL = ROOT / "state" / "fuel" / "x_churn_hits.jsonl"
HANDLE = "NachoQuixotic"

INVENTORY_FILES = [
    ROOT / "watch" / "inbox" / "ACCOUNT_VS_AUDIT_20260923.md",
    ROOT / "corpus" / "canon" / "founding_curriculum" / "FOUNDING_CURRICULUM.md",
    ROOT / "corpus" / "canon" / "x_canon_2025_pass3.md",
    ROOT / "corpus" / "canon" / "x_canon_2025_pass6.md",
    ROOT / "corpus" / "canon" / "receipts_dec2025_mar2026.md",
]
ID_RE = re.compile(r"\b(\d{18,20})\b")

QUERIES = [
    ("church-surveillance", "from:NachoQuixotic Church Committee OR COINTELPRO OR SHAMROCK OR surveillance"),
    ("smith-mundt", "from:NachoQuixotic Smith-Mundt OR HR 5736 OR propaganda"),
    ("cic-echoic", "from:NachoQuixotic censorship industrial complex OR echoic drift OR Rashomon"),
    ("bernays-ellul", "from:NachoQuixotic Bernays OR Ellul OR manufacturing consent"),
    ("gilens-page", "from:NachoQuixotic oligarchy OR policy elites OR Gilens"),
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


def _post_json(url: str, payload: dict, key: str, timeout: int = 120) -> dict | None:
    if not lite_guard._safe_https_url(url):
        raise RuntimeError("SSRF guard rejected url")
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers={"Authorization": "Bearer " + key,
                                          "Content-Type": "application/json"})
    with lite_guard._OPENER.open(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def _get_json(url: str, timeout: int = 20) -> dict | None:
    if not lite_guard._safe_https_url(url):
        raise RuntimeError("SSRF guard rejected url")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (estate x_churn_grok)"})
    with lite_guard._OPENER.open(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def log_row(row: dict) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")


def call_grok(query: str) -> dict:
    last_err = ""
    for model in MODELS:
        payload = {"model": model,
                   "messages": [{"role": "user", "content":
                       f"Search X for posts by @{HANDLE} matching: {query}\n"
                       f"List EVERY matching post you can find. For each give: the full status URL "
                       f"(https://x.com/{HANDLE}/status/<id>), the post date, the like count if visible, "
                       "and a one-sentence gist. Only real posts by this handle. No commentary."}],
                   "search_parameters": {"mode": "on", "return_citations": True},
                   "max_tokens": 1200, "temperature": 0}
        try:
            d = _post_json(API, payload, KEY)
            text = d["choices"][0]["message"]["content"]
            usage = d.get("usage", {})
            log_row({"ts": datetime.now(timezone.utc).isoformat(), "model": model,
                     "query": query, "tokens": usage.get("total_tokens"), "ok": True})
            return {"ok": True, "text": text, "model": model}
        except Exception as e:
            last_err = type(e).__name__ + ": " + str(e)[:100]
            log_row({"ts": datetime.now(timezone.utc).isoformat(), "model": model,
                     "query": query, "ok": False, "error": last_err})
    return {"ok": False, "error": last_err}


def known_ids() -> set:
    ids = set()
    for p in INVENTORY_FILES:
        if p.is_file():
            ids |= set(ID_RE.findall(p.read_text(encoding="utf-8", errors="replace")))
    return ids


def pull_post(pid: str) -> dict | None:
    if not re.fullmatch(r"\d{18,20}", pid):
        return None
    try:
        d = _get_json(VX + HANDLE + "/status/" + pid)
        return {"id": pid, "date": d.get("date"), "text": (d.get("text") or "")[:600],
                "likes": d.get("likes"), "rts": d.get("retweets"), "replies": d.get("replies")}
    except Exception:
        return None


ANCHOR_SIGNALS = re.compile(
    r"(19\d\d|20\d\d)|("
    r"Smith-Mundt|Church|COINTELPRO|MKULTRA|Bernays|Ellul|Jung|Wasson|Hofmann|Ruck|Eleusis|"
    r"Epstein|Maxwell|Brunel|Dutroux|Franklin|Pike|Taxil|Margiotta|Illuminati|Bavarian|"
    r"Tartaria|Enoch|Dead Sea|adrenochrome|Huxley|loosh|Bohemian|Grove|Jekyll|Rothschild|Rockefeller|"
    r"Federal Reserve|Torture Report|Pentagon Papers|Family Jewels|Operation |CTIL|GEC|USAID)", re.I)


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
    if not KEY:
        return {"ok": False, "error": "no GROK key in env"}
    known = known_ids()
    candidates: dict[str, dict] = {}
    queries_run = 0
    for family, q in QUERIES:
        if queries_run >= MAX_QUERIES:
            break
        queries_run += 1
        r = call_grok(q)
        if not r.get("ok"):
            continue
        for pid in set(ID_RE.findall(r.get("text", ""))):
            if pid not in known and pid not in candidates:
                post = pull_post(pid)
                if post and post.get("text"):
                    candidates[pid] = {"family": family, **post,
                                       "cialdini": cialdini_summary(post["text"])}
    hits = []
    misses = 0
    for pid, c in sorted(candidates.items(), key=lambda kv: -(kv[1].get("likes") or 0)):
        if ANCHOR_SIGNALS.search(c.get("text") or ""):
            hits.append(c)
        else:
            misses += 1
    for h in hits:
        OUT_JSONL.parent.mkdir(parents=True, exist_ok=True)
        with OUT_JSONL.open("a", encoding="utf-8") as f:
            f.write(json.dumps(h) + "\n")
    md = [
        "# X ANCHOR MAP — missing @NachoQuixotic posts, mined via Grok live search",
        "",
        f"2026-09-23 · key: GROK_API_KEY_2 · queries: {queries_run}/{MAX_QUERIES} · "
        f"known inventory IDs: {len(known)} · new posts pulled: {len(candidates)} · "
        f"hits (anchor-worthy): {len(hits)} · misses discarded: {misses}",
        "",
        "A HIT = a post missing from the estate inventory that carries receipts language, "
        "checkable dates/numbers, named documents, or direct ties to a ledger family — "
        "i.e., content the conversion plan can anchor to.",
        "",
        "## Hits, by engagement",
        "",
    ]
    for h in hits:
        md.append(f"- **{h['date']}** · {h['likes']} likes · RTs {h['rts']} · family: {h['family']}")
        md.append(f"  - https://x.com/{HANDLE}/status/{h['id']}")
        md.append(f"  - > {(h['text'] or '')[:220].replace(chr(10), ' ')}")
        if h.get("cialdini", {}).get("n_findings"):
            md.append(f"  - PERSUASION-FLAG: {h['cialdini']['verdict']} "
                      f"[{', '.join(h['cialdini']['patterns'])}]")
    md += ["", "## Ledger", "", "- calls logged: state/fuel/x_churn_ledger.jsonl", "",
           "*Append-only. Anchors feed the conversion plan's re-ladder.*"]
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    return {"ok": True, "queries": queries_run, "known": len(known),
            "new_pulled": len(candidates), "hits": len(hits), "misses": misses,
            "file": str(OUT_MD)}


if __name__ == "__main__":
    print(json.dumps(main(), indent=1))
