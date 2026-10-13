"""garden_battery_local_refire - amendment for series local-20261001-a.

WHY: the battery staging moved under the lane-local run (a sibling lane
staged B6/B8 with ASK_TEXT.md evidence at 18:11:05, then reverted to the
evidence-less spec shape at 18:20:31, WHILE the run was firing). gemma2's
B6/B8 fired on the with-evidence bytes; gemma4 B6/B8 and gemma:2b B6 failed
preflight when the files vanished. Per-item byte-identity across models
broke for B6/B8, so this amendment re-fires B6/B8 for ALL THREE models on
the pinned post-revert staging (contracts byte-verified identical to the
run snapshot; B1-B5/B7 rows stand, their contracts byte-identical and
surface shas frozen-ok). Also fixes two run artifacts: error rows graded
vacuously are replaced by real rows, and the raw reply dumps that landed in
NTFS alternate data streams (colon in the model tag) are recovered to
properly-named files. Grid rows carry attempt lineage in notes.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import garden_battery_local as G  # noqa: E402

SERIES = G.SERIES
GRID_PATH = G.OUT_DIR / f"GRID_{SERIES}.json"
SNAP = G.REPLY_DIR / "ask_snapshot"

REFIRE = [
    ("gemma2:2b-instruct-q5_K_M", ["B6", "B8"]),
    ("gemma4:latest", ["B6", "B8"]),
    ("gemma:2b", ["B6"]),
]


def pinned_meta(item: str) -> dict:
    """Load the CURRENT ask.json, byte-assert its contract matches the
    snapshot the run fired, and pin this copy for the re-fire."""
    raw = (G.BATTERY_DIR / item / "ask.json").read_bytes()
    meta = json.loads(raw.decode("utf-8"))
    old = json.loads((SNAP / f"{item}_ask.json").read_text(encoding="utf-8"))
    if meta["contract"] != old["contract"]:
        raise RuntimeError(f"{item}: contract drifted from run snapshot; abort")
    (SNAP / f"{item}_ask.json.refire2").write_bytes(raw)
    return meta


def recover_ads() -> int:
    """Colon-tagged reply dumps landed as NTFS streams off 0-byte base
    files; a colon path in Python stats and reads the STREAM itself, so
    read each one back out to a sanitized filename and drop the stream."""
    recovered = 0
    for model, items in G.RUNS:
        for item in items:
            bad = G.REPLY_DIR / f"{model.replace('/', '_')}__{item}.md"
            if bad.exists():
                text = bad.read_text(encoding="utf-8", errors="replace")
                if text.strip():
                    good = G.REPLY_DIR / f"{model.replace(':', '_').replace('/', '_')}__{item}.md"
                    if not good.exists():
                        good.write_text(text, encoding="utf-8")
                        recovered += 1
                bad.unlink()
    for base in ("gemma", "gemma2", "gemma4"):
        p = G.REPLY_DIR / base
        if p.exists() and p.stat().st_size == 0:
            p.unlink()
    return recovered


def main() -> int:
    grid_doc = json.loads(GRID_PATH.read_text(encoding="utf-8"))
    grid = grid_doc["grid"]
    n_recovered = recover_ads()
    print(f"[ads] recovered {n_recovered} colon-tagged reply dumps")
    for model, items in REFIRE:
        for item in items:
            meta = pinned_meta(item)
            old_row = grid[model][item]
            lineage = (f"attempt1: {old_row['finish']}, {old_row['notes']}"
                       .replace("instrument=lane-local-script; ", ""))
            try:
                res = G.fire(model, meta)
            except Exception as exc:
                res = {"reply": "", "finish": "error", "prompt_tokens": 0,
                       "completion_tokens": 0, "wall_s": 0.0, "tok_s": 0.0,
                       "body_sha": "", "error": repr(exc)[:300]}
            g = (G.GRADERS[G.ITEM_KIND[item]](res["reply"])
                 if res["finish"] != "error"
                 else {"checks": {"ERROR": 0}, "total": 1, "passed": 0})
            notes = (f"instrument=lane-local-script; family=ollama-local; "
                     f"prompt_tokens={res['prompt_tokens']}; "
                     f"finish={res['finish']}; refire2 on pinned post-revert "
                     f"staging (contract byte-identical); {lineage}")
            if res.get("error"):
                notes += f"; error={res['error']}"
            if model == "gemma:2b":
                notes += "; quant probe (old Q4_0 self), B6/B7 only"
            grid[model][item] = {
                "score_norm": round(g["passed"] / g["total"], 3),
                "checks_passed": g["passed"],
                "checks_total": g["total"],
                "checks": g["checks"],
                "cost_usd": 0.0,
                "latency_s": res["wall_s"],
                "tok_s": res["tok_s"],
                "finish": res["finish"],
                "contamination_flags": meta.get("contamination_flags_at_staging", []),
                "notes": notes,
            }
            bs = grid_doc["ask_body_shas"].setdefault(item, {})
            bs[model] = res.get("body_sha", "")
            G.bank({"ts": G._now(), "id": meta["id"], "model": model,
                    "model_family": "ollama-local", "base_url": G.BASE_URL,
                    "turn": 1, "prompt_tokens": res["prompt_tokens"],
                    "completion_tokens": res["completion_tokens"],
                    "channel": "lane-local-script", "cost_usd": 0.0,
                    "ok": res["finish"] not in ("error",),
                    "series": SERIES, "tok_s": res["tok_s"],
                    "finish": res["finish"], "refire": 2})
            slug = model.replace(":", "_").replace("/", "_")
            keep = G.REPLY_DIR / f"{slug}__{item}.md"
            if keep.exists():
                keep.rename(G.REPLY_DIR / f"{slug}__{item}.attempt1.md")
            keep.write_text(
                f"# {meta['id']} | {model} | series {SERIES} | instrument=lane-local-script | refire2\n"
                f"# finish={res['finish']} prompt_tokens={res['prompt_tokens']} "
                f"completion_tokens={res['completion_tokens']} wall_s={res['wall_s']} "
                f"tok_s={res['tok_s']} checks={g['passed']}/{g['total']} {g['checks']}\n\n"
                f"{G.sanitize(res['reply'])}\n", encoding="utf-8")
            print(f"[refire2] {model} {item}: {g['passed']}/{g['total']} "
                  f"finish={res['finish']} ctok={res['completion_tokens']} "
                  f"tok/s={res['tok_s']}")
    grid_doc["amendments"] = grid_doc.get("amendments", []) + [{
        "ts": G._now(),
        "what": ("B6/B8 re-fired for all three models on pinned post-revert "
                 "staging; attempt-1 lineage preserved in row notes; error "
                 "rows no longer graded vacuously; colon-tagged ADS reply "
                 "dumps recovered"),
        "recovered_ads_files": n_recovered,
    }]
    GRID_PATH.write_text(json.dumps(grid_doc, indent=2, ensure_ascii=False) + "\n",
                         encoding="utf-8")
    print(f"[land] {GRID_PATH} (amended)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
