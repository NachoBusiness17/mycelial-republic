"""break-accuracy byte-checks (hostile pass, 2026-10-07). Read-only against the
estate; the only network touch is localhost ollama /api/tags. No paid keys."""
from __future__ import annotations

import json
import re
import time
import urllib.request
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
DIR = ROOT / "watch" / "inbox" / "ractor_engine" / "2026-10-07-stupidmodel-comics"

print("=== 1. snapshot_openrouter.json: gemma + google entries ===")
snap = json.loads((ROOT / "watch/inbox/endpoint_news/snapshot_openrouter.json").read_text(encoding="utf-8"))
print("top-level type:", type(snap).__name__)
models = snap.get("data") if isinstance(snap, dict) else snap
if not isinstance(models, list):
    print("keys:", list(snap)[:10] if isinstance(snap, dict) else "n/a")
    models = []
hits = [m for m in models if "gemma" in json.dumps(m).lower()]
print(f"gemma entries: {len(hits)} of {len(models)}")
for m in hits:
    print(json.dumps({k: v for k, v in m.items() if k in ("id", "name", "pricing", "free")}, ensure_ascii=False)[:400])
g26 = [m for m in models if m.get("id") == "google/gemma-4-26b-a4b-it"]
if g26:
    print("FULL google/gemma-4-26b-a4b-it entry keys:", list(g26[0]))
    print(json.dumps(g26[0], ensure_ascii=False)[:1200])
other_google = [m.get("id") for m in models if str(m.get("id", "")).startswith("google/")]
print("all google/ ids:", other_google)

print()
print("=== 2. probe_panel_spec_results.json: summary vs rows re-derivation ===")
res = json.loads((DIR / "probe_panel_spec_results.json").read_text(encoding="utf-8"))
rows = res["rows"]
print("row count:", len(rows), "| ts:", res["ts"])
rederived = {}
for key in {(r["model"], r["arm"]) for r in rows}:
    sub = [r for r in rows if (r["model"], r["arm"]) == key]
    rederived[f"{key[0]}:{key[1]}"] = {
        "n": len(sub),
        "parses": sum(r["parses"] for r in sub),
        "spec_valid": sum(r["spec_valid"] for r in sub),
        "errors": sum(1 for r in sub if r["error"]),
        "mean_secs": round(sum(r["secs"] for r in sub) / len(sub), 1),
    }
ok = True
for k, v in rederived.items():
    claimed = res["summary"].get(k)
    match = claimed and all(
        claimed.get(f) == v[f] for f in ("n", "parses", "spec_valid", "errors", "mean_secs")
    )
    ok = ok and bool(match)
    print(f"{k}: rederived {v} | claimed {claimed} | MATCH={match}")
print("SUMMARY==ROWS:", ok)
fenced = [r["prompt_i"] for r in rows if r["arm"] == "unconstrained" and r["raw_head"].startswith("```")]
print("unconstrained fenced-output rows:", fenced, f"(count={len(fenced)})")

print()
print("=== 3. scorer-defect unit test on the PERSISTED probe script ===")
src = (DIR / "probe_panel_spec.py").read_text(encoding="utf-8")
ns: dict = {"__file__": str(DIR / "probe_panel_spec.py"), "__name__": "probe_mod"}
exec(compile(src, str(DIR / "probe_panel_spec.py"), "exec"), ns)
score = ns["score"]
boom = 0
try:
    out = score('{"title":"T","panels":[{"caption":"c","characters":["a"],"bubbles":null}]}')
    print("bubbles:null scored:", out)
except TypeError as e:
    boom = 1
    print("bubbles:null RAISES TypeError:", e)
guard_ok = score('{"title":"T","panels":[{"caption":"c","characters":["a"],"bubbles":[{"who":"a","text":"hi"}]}]}')
print("well-formed spec scores spec_valid:", guard_ok["spec_valid"])
print("DEFECT MECHANISM CONFIRMED" if boom else "no defect reproduced")

print()
print("=== 4. venv rasterizer census ===")
import importlib.util
for mod in ("cairosvg", "svglib", "PIL"):
    print(f"{mod}: {importlib.util.find_spec(mod) is not None}")
import shutil
print("resvg on PATH:", shutil.which("resvg"))
try:
    from PIL import Image, ImageDraw  # noqa: F401
    print("PIL ImageDraw importable: True")
except Exception as e:
    print("PIL ImageDraw importable: False", e)

print()
print("=== 5. ollama local tags (localhost only) ===")
try:
    with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=10) as r:
        tags = json.loads(r.read().decode())
    for m in tags.get("models", []):
        print(m.get("name"), m.get("size"))
except Exception as e:
    print("ollama unreachable:", type(e).__name__, e)

print()
print("=== 6. econ arm B seats (typed-schema door provenance) ===")
for name in ("econ_probe_results_arm_b.json", "econ_probe_results_arm_a.json"):
    p = DIR / name
    if p.is_file():
        d = json.loads(p.read_text(encoding="utf-8"))
        s = d.get("summary", d if isinstance(d, dict) else {})
        seats = sorted({r.get("model", r.get("provider", "?")) for r in d.get("rows", [])})
        print(name, "| seats:", seats, "| summary keys:", list(s)[:8])
