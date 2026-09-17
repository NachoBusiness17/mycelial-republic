"""librarian -- the fleet's own database expert, cold-loaded on the free Lite lane.

Operator order (2026-09-17): "dedicate one 5.3 agent to be an expert in our database that
we can load cold on max so we can ask it questions about ourselves when you forget."

Rides models.providers.chat_provider (the canonical door: quota, tiers, keys, timeout) --
dogfood law. The imprint (watch/inbox/FLEET_IMPRINT_20260917.md) is byte-stable, so the
provider's prompt cache pays for it once; every question after the first is crumbs.

RUN: .venv\\Scripts\\python.exe scripts\\librarian.py "do we have a mechanism that X?"
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

IMPRINT = ROOT / "watch" / "inbox" / "FLEET_IMPRINT_20260917.md"


def main(argv: list[str] | None = None) -> int:
    args = [a for a in (argv or sys.argv[1:])]
    coldload = "--coldload" in args
    q = " ".join(a for a in args if not a.startswith("-")).strip()
    if not q:
        print(json.dumps({"ok": False, "error": "usage: librarian.py [--coldload] \"question\""}))
        return 1
    from models.providers import chat_provider

    system = IMPRINT.read_text(encoding="utf-8", errors="replace")
    # --coldload (salon enhancement 1): union-alpha's 256K window takes the imprint PLUS
    # raw estate-index slices matching the query keywords — the inward battery engine.
    provider, model, extra = "z_ai3", "glm-5.3-flash", ""
    if coldload:
        import re as _re
        idx = ROOT / "watch" / "ESTATE_INDEX" / "ESTATE_INDEX.jsonl"
        terms = [t for t in _re.findall(r"[a-zA-Z_0-9]{4,}", q.lower())][:6]
        hits = []
        if idx.is_file():
            for ln in idx.read_text(encoding="utf-8", errors="replace").splitlines():
                low = ln.lower()
                if any(t in low for t in terms):
                    hits.append(ln[:300])
                    if len(hits) >= 120:
                        break
        extra = "\n\nESTATE INDEX SLICES (matching rows, path | size | mtime):\n" + "\n".join(hits)
        provider, model = "openrouter", "stealth/union-alpha"
        system = system[:200000] + extra  # U8: 256K window, imprint + slices fit
    r = chat_provider(
        provider, system=system, user=q,
        model=model, tier="T2", timeout=420 if coldload else 300,
    )
    out = {"ok": r.get("ok"), "provider": "z_ai3 (Lite, glm-5.3-flash)",
           "imprint_bytes": len(system)}
    if r.get("ok"):
        out["answer"] = r.get("text", "")[:4000]
        out["usage"] = r.get("usage")
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 0
    out["error"] = r.get("error")
    print(json.dumps(out, ensure_ascii=False))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
