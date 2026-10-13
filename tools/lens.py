"""lens.py — the lens socket (LENS RIB v3, step 2.5).

view_through(chair, object): summon any chair on any object through its living
lens — kernel brief + invariants (L0/L0.5) + case law (L4) loaded, voice/shadow
layers by pointer (travel-kit law: over-cap sources ride pointer+hash), refusal
path open, L5 dossier rebuilt per summon.

Output = testimony + citations (INV-n / CASE-n) + precedent-touch register +
manifest stamped with the lens's uniqueness (corpus hashes + case-law chain
range): a lens rebuilt from the same texts elsewhere is NOT this lens.

Citation law (spec): every claim cites its invariant or case row; conflict with
own precedent must cite both and mark OVERRULE-CANDIDATE — silent contradiction
is illegal. REFUSED is a legal output and a fidelity signal.

Usage:
  python -u tools/lens.py --chair BERNAYS --object-file <path> [--ask "extra instruction"]
  python -u tools/lens.py --chair GREER --assemble-only --out <dir>   # bundle without summon

Remote deepseek-chat by default (VRAM law: no local inference while family on box).
"""
from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import os
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
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import ROOT  # noqa: E402

RIBS = ROOT / "corpus" / "ractor_ribs"
BRIEFS = ROOT / "docs" / "ref" / "ractors"
STARTERS = ROOT / "corpus" / "library" / "ractor_starter"

_API_URL = "https://api.deepseek.com/chat/completions"
_CITE_RE = re.compile(r"\b(INV-\d+|CASE-\d+|OVERRULE-CANDIDATE|REFUSED)\b")


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


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def assemble_lens(chair: str) -> dict:
    """Bundle the living lens for a chair. Raises FileNotFoundError if no lens exists."""
    inv_p = RIBS / chair / "invariants.md"
    cl_p = RIBS / chair / "case_law.jsonl"
    if not inv_p.exists() and not cl_p.exists():
        raise FileNotFoundError(f"no lens for {chair} (need invariants.md or case_law.jsonl)")
    brief_p = BRIEFS / f"{chair}.md"
    starter = STARTERS / chair.lower()

    invariants = inv_p.read_text(encoding="utf-8") if inv_p.exists() else ""
    case_rows = []
    if cl_p.exists():
        for line in cl_p.read_text(encoding="utf-8").splitlines():
            try:
                case_rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    prov = {"invariants_sha": sha256_file(inv_p) if inv_p.exists() else None,
            "case_law_rows": len(case_rows),
            "brief_sha": sha256_file(brief_p) if brief_p.exists() else None}
    if starter.exists():
        prov["starter_files"] = sum(1 for _ in starter.rglob("*") if _.is_file())
        man = starter / "MANIFEST.sha256"
        prov["starter_manifest"] = sha256_file(man) if man.exists() else "no-manifest"

    parts = []
    if brief_p.exists():
        parts.append("L0 KERNEL BRIEF (verbatim):\n" + brief_p.read_text(encoding="utf-8")[:6000])
    if invariants:
        parts.append("L0.5 LIVING INVARIANTS (cite as INV-n by their numbered order):\n" + invariants[:5000])
    if case_rows:
        cl = "\n".join(
            f"CASE-{i+1} [{r.get('date','?')}] ({r.get('stance','?')}) {r.get('topic','')[:110]}"
            for i, r in enumerate(case_rows[:40]))
        parts.append(("L4 CASE LAW — your own prior rulings. Cite as CASE-n. To contradict one, "
                      "cite it and mark OVERRULE-CANDIDATE; silent contradiction is illegal.\n" + cl))
    if starter.exists():
        parts.append(f"L1/L2 WORKS+VOICE: held at corpus/library/ractor_starter/{chair.lower()}/ "
                     f"({prov['starter_files']} files, manifest {prov.get('starter_manifest')}) — "
                     f"pointer only; cite from memory of the lens, do not fabricate quotes.")
    parts.append(
        "LENS LAW: testify THROUGH these invariants. Every load-bearing claim cites INV-n or "
        "CASE-n. If the object contradicts your precedent, cite both rows and mark "
        "OVERRULE-CANDIDATE with one line of why. You may REFUSED (one word + <=2 lines why) — "
        "refusal is a fidelity signal, not a failure. No flattery, no hedging, no speaking for "
        "other chairs.")
    return {"system": "\n\n===\n".join(parts), "provenance": prov, "case_rows": case_rows}


def summon(lens: dict, chair: str, object_text: str, object_ref: str, extra_ask: str) -> dict:
    from models.providers import get_provider, provider_keys
    keys = provider_keys(get_provider("deepseek") or {})
    if not keys:
        return {"ok": False, "error": "no DEEPSEEK_API_KEY in env"}
    user = (f"OBJECT ({object_ref}):\n\"\"\"\n{object_text[:14000]}\n\"\"\"\n\n"
            f"view_through({chair}, object). Testify.\n"
            + (f"Additional instruction from the summoner: {extra_ask}\n" if extra_ask else ""))
    payload = {"model": "deepseek-chat", "temperature": 0.4, "max_tokens": 900,
               "messages": [{"role": "system", "content": lens["system"]},
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
    ap = argparse.ArgumentParser()
    ap.add_argument("--chair", required=True)
    ap.add_argument("--object-file")
    ap.add_argument("--object-text")
    ap.add_argument("--ask", default="")
    ap.add_argument("--assemble-only", action="store_true")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    chair = args.chair.upper()
    lens = assemble_lens(chair)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = Path(args.out) if args.out else ROOT / "memory" / "runs" / "lens_sockets" / f"{stamp}_{chair}"
    out.mkdir(parents=True, exist_ok=True)

    if args.assemble_only:
        (out / "lens_bundle.md").write_text(lens["system"], encoding="utf-8")
        (out / "manifest.json").write_text(json.dumps(
            {"chair": chair, "utc": stamp, "provenance": lens["provenance"],
             "uniqueness": f"{chair} lens = corpus hashes + case-law rows 1..{lens['provenance']['case_law_rows']} + this fleet's salons"},
            indent=1), encoding="utf-8")
        print(f"[assembled] {out}/lens_bundle.md (+manifest.json)")
        return

    if args.object_file:
        src = ROOT / args.object_file if not os.path.isabs(args.object_file) else Path(args.object_file)
        object_text = src.read_text(encoding="utf-8", errors="replace")
        object_ref = str(src)
    elif args.object_text:
        object_text, object_ref = args.object_text, "inline text"
    else:
        raise SystemExit("need --object-file or --object-text")

    r = summon(lens, chair, object_text, object_ref, args.ask)
    if not r["ok"]:
        raise SystemExit(f"[summon failed] {r['error']}")
    text = r["text"]
    cites = sorted(set(_CITE_RE.findall(text)))
    touched = [f"CASE-{i+1}" for i, row in enumerate(lens["case_rows"][:40])
               if any(w.lower() in text.lower() for w in re.findall(r"[a-z]{6,}", row.get("topic", "")))]

    (out / "testimony.md").write_text(
        f"# view_through({chair}) — {object_ref}\n\n{text}\n", encoding="utf-8")
    (out / "manifest.json").write_text(json.dumps({
        "chair": chair, "utc": stamp, "object": object_ref,
        "provenance": lens["provenance"],
        "citations": cites, "precedent_touched": touched,
        "refused": "REFUSED" in cites,
        "overrule_candidates": text.count("OVERRULE-CANDIDATE"),
        "tokens": r["usage"].get("completion_tokens"),
        "uniqueness": f"{chair} lens = corpus hashes + case-law rows 1..{lens['provenance']['case_law_rows']} + this fleet's salons",
    }, indent=1), encoding="utf-8")
    print(f"[socket] {out}/testimony.md")
    print(f"[citations] {', '.join(cites) if cites else 'NONE — uncited testimony, flag'}")
    print(f"[precedent touched] {', '.join(touched) if touched else 'none'}")
    print(f"[refused] {'YES' if 'REFUSED' in cites else 'no'}")


if __name__ == "__main__":
    main()
