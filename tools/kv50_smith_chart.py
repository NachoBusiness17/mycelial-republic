"""KV50 SMITH CHART — the 50-wide lift mapped onto the smith chart.

Law (operator prose -> teeth, 2026-09-22): every lane of the lift is an organ.
Its CLAIM is the lane ask; its DELIVERY is measured in bytes, not vibes.

Named unfolding (report it when citing a number):
  delivered = 0.4 * has_verifiable_source   (>=1 http URL, or an absolute file
                                             path that exists on disk)
            + 0.3 * has_hard_evidence       (evidence field >= 20 chars: a
                                             verbatim quote, number, or path)
            + 0.3 * action_carries_a_bar    (steal_action contains a number or
                                             an explicit cost/time token)
  Gamma    = 1 - delivered
Bar: 0.5 — lanes above the bar go on the no-prose list: re-ask or die.
Lane self-reported confidence is NOT an input: that is the lane grading its
own homework. Bytes only.

Usage: .venv/Scripts/python.exe tools/kv50_smith_chart.py <findings.json>
Out:   watch/inbox/KV50_SMITH_CHART_<date>.{json,png}
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

NOW = datetime.now(timezone.utc)
STAMP = NOW.strftime("%Y%m%d")
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "watch" / "inbox"
BAR = 0.5
BAR_RE = re.compile(r"\d|\$|bar\b|hour|minute|day|week", re.I)


def delivered(f: dict) -> tuple[float, dict]:
    parts = {}
    sources = f.get("sources") or []
    ok_src = False
    for s in sources:
        s = str(s)
        if s.startswith("http"):
            ok_src = True
            break
        p = Path(s)
        if p.is_absolute() and p.exists():
            ok_src = True
            break
    parts["source"] = 0.4 if ok_src else 0.0
    parts["evidence"] = 0.3 if len(str(f.get("evidence") or "")) >= 20 else 0.0
    parts["bar"] = 0.3 if BAR_RE.search(str(f.get("steal_action") or "")) else 0.0
    return round(1.0 - sum(parts.values()), 2), parts


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: kv50_smith_chart.py <findings.json>")
        return 2
    findings = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    rows = []
    for f in findings:
        g, parts = delivered(f)
        rows.append(
            {
                "lane": f.get("lane") or "?",
                "gamma": g,
                "status": "DELIVERING" if g <= 0.0 else ("PARTIAL" if g <= BAR else "REFLECTING"),
                "credits": parts,
                "converges_with": f.get("converges_with") or "",
            }
        )
    rows.sort(key=lambda r: r["gamma"])
    no_prose = [r["lane"] for r in rows if r["gamma"] > BAR]
    out = {
        "schema": "kv50_smith_chart.v1",
        "ts": NOW.isoformat(),
        "bar": BAR,
        "unfolding": "delivered = 0.4*source + 0.3*evidence + 0.3*action_bar; Gamma = 1 - delivered",
        "organs": rows,
        "no_prose_list": no_prose,
        "summary": {
            "lanes": len(rows),
            "delivering": sum(1 for r in rows if r["status"] == "DELIVERING"),
            "partial": sum(1 for r in rows if r["status"] == "PARTIAL"),
            "reflecting": len(no_prose),
            "mean_gamma": round(sum(r["gamma"] for r in rows) / max(len(rows), 1), 3),
        },
    }
    OUT.mkdir(parents=True, exist_ok=True)
    jp = OUT / f"KV50_SMITH_CHART_{STAMP}.json"
    jp.write_text(json.dumps(out, indent=2), encoding="utf-8")

    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        names = [r["lane"] for r in rows][::-1]
        gammas = [r["gamma"] for r in rows][::-1]
        colors = ["#2a9d8f" if r["status"] == "DELIVERING" else ("#e9c46a" if r["status"] == "PARTIAL" else "#e76f51") for r in rows][::-1]
        fig, ax = plt.subplots(figsize=(10, max(6, len(rows) * 0.28)))
        ax.barh(names, gammas, color=colors)
        ax.axvline(BAR, color="k", ls="--", lw=1)
        ax.text(BAR + 0.01, len(rows) - 0.5, "bar 0.5 — no prose beyond this line", fontsize=8)
        ax.set_xlabel("Gamma = 1 - delivered/claimed (lower is better)")
        ax.set_title(f"KV50 LIFT — SMITH CHART {NOW.date()} · delivering/partial/reflecting = {out['summary']['delivering']}/{out['summary']['partial']}/{out['summary']['reflecting']}")
        ax.margins(y=0.01)
        fig.tight_layout()
        fig.savefig(OUT / f"KV50_SMITH_CHART_{STAMP}.png", dpi=110)
        plt.close(fig)
    except Exception as e:  # chart is optional; the JSON is the record
        print(f"[kv50-smith] chart skipped: {e}")

    print(f"KV50 SMITH CHART {NOW.isoformat()}  bar={BAR}")
    for r in rows:
        print(f"  {r['lane']:24s} Gamma={r['gamma']:.2f}  {r['status']}")
    print(f"  no-prose list ({len(no_prose)}): {', '.join(no_prose) if no_prose else 'none'}")
    print(f"  wrote {jp.name} (+png)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
