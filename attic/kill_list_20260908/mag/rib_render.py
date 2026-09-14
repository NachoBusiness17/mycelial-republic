"""rib_render — render the invariant stack as real infographics (the constitutional percolation, seen).

STEAL (2026-08-13, agentswarm): structured state is rendered as a ```chart block -> self-contained
inline HTML/SVG in house style, 'wherever a trend, split, or headline metric tells the story better
than prose'. The report/synthesis prompt demands: use real tables for tabular findings + ```chart
blocks wherever a metric tells the story better than prose. BuildPlanGraph renders the plan as a
live graph.

ADAPTED: the invariant stack (the ~160 RIBs across 40 domains) is STRUCTURED STATE — render it as:
  1. a MERMAID diagram (the invariant graph by domain) — inline, in-editor.
  2. a ```chart-style HTML artifact (invariants-per-domain bar chart) — the real infographic.
  3. DELIVERED to the operator's desktop via clawbot (pictures/) so it's seen, not just inline.

Deterministic + $0, pure stdlib. Honest — every number is a real count from the rib_bus files.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from config import ROOT
except Exception:
    ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

SCHEMA = "rib_render.v1"
RIB_DIR = ROOT / "memory" / "rib_bus"
ARTIFACT_DIR = ROOT / "memory" / "artifacts" / "rib_render"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _invariant_counts() -> dict[str, int]:
    counts: dict[str, int] = {}
    if RIB_DIR.is_dir():
        for f in sorted(RIB_DIR.glob("*.json")):
            try:
                data = json.loads(f.read_text(encoding="utf-8", errors="replace"))
                ribs = data.get("ribs") or {}
                counts[f.stem] = len(ribs)
            except Exception:
                continue
    return counts


def _total(counts: dict[str, int]) -> int:
    return sum(counts.values())


def render_stack() -> dict[str, Any]:
    """RENDER the invariant stack: invariants-per-domain counts + a mermaid graph + the numbers.
    Deterministic + $0. HONEST — every count is real from the rib_bus files, never invented."""
    counts = _invariant_counts()
    total = _total(counts)
    # mermaid: the invariant graph (top domains by count, as a hierarchy)
    top = sorted(counts.items(), key=lambda kv: -kv[1])[:8]
    mermaid_lines = ["flowchart LR"]
    for name, n in top:
        mermaid_lines.append(f"    {name}[{name}: {n} invariants]")
    if top:
        mermaid_lines.append("    " + " --> ".join(dict(top).keys()))
    return {"ok": True, "schema": SCHEMA, "tool": "rib_render",
            "n_domains": len(counts), "n_invariants": total,
            "per_domain": counts,
            "top_domains": dict(top),
            "mermaid": "\n".join(mermaid_lines),
            "note": "the invariant stack rendered — the constitutional percolation's output, seen"}


def render_chart_artifact(*, deliver: bool = True) -> dict[str, Any]:
    """Render a ```chart-STYLE HTML artifact (bar chart: invariants per domain) — the real infographic,
    and (optionally) deliver it to the operator's desktop via clawbot. Deterministic + $0. Honest."""
    counts = _invariant_counts()
    total = _total(counts)
    top = sorted(counts.items(), key=lambda kv: -kv[1])[:20]
    rows = "\n".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in top)
    html = f"""<!doctype html><html><head><meta charset="utf-8"><title>Invariant Stack</title>
<style>body{{font:14px ui-monospace,Menlo,monospace;background:#0f1117;color:#e6e6e6;padding:24px}}
h1{{font-size:16px}} table{{border-collapse:collapse;margin-top:12px}}
td,th{{border:1px solid #333;padding:4px 10px;text-align:left}} .bar{{background:#5a7cff;height:12px;display:inline-block}}</style></head>
<body><h1>Invariant Stack — the constitutional percolation, seen</h1>
<p>{total} invariants across {len(counts)} domains</p><table><tr><th>domain</th><th>invariants</th><th></th></tr>
{''.join(f'<tr><td>{k}</td><td>{v}</td><td><span class="bar" style="width:{max(2,int(120*v/max(1,max(counts.values()))))}px"></span></td></tr>' for k,v in top)}
</table></body></html>"""
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    out = ARTIFACT_DIR / "invariant_stack.html"
    out.write_text(html, encoding="utf-8")
    result = {"ok": True, "schema": SCHEMA, "tool": "rib_render",
              "n_domains": len(counts), "n_invariants": total,
              "artifact": str(out), "deliverable": False}
    if deliver:
        try:
            from mag import clawbot
            d = clawbot.deliver(out)
            result["deliverable"] = bool(d.get("ok"))
            result["delivered_to"] = d.get("delivered")
        except Exception as e:
            result["deliver_error"] = str(e)[:80]
    return result


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="rib-render")
    ap.add_argument("cmd", nargs="?", default="render", choices=["render", "chart"])
    a = ap.parse_args(argv)
    if a.cmd == "chart":
        print(json.dumps(render_chart_artifact(), ensure_ascii=False, indent=2, default=str))
    else:
        print(json.dumps(render_stack(), ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
