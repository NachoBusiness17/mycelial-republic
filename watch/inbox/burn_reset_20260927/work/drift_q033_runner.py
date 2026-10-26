"""Q-033 comparative drift audit: SAME prompt to 3 free-tier lanes.

Dispatch pattern copied from tools/stealth_fanout.py (dispatch() body shape,
_check_base SSRF boundary, LAWS suffix, per-lane raw banking + heartbeat row).
Lanes: stealth/space-bunny-alpha (OPENROUTER_API_KEY),
inclusionai/ling-3.0-flash-vl (OPENROUTER_API_KEY_2),
meta/muse-glimmer-30b (OPENROUTER_API_KEY_2).
Sequential dispatch, 5s spacing (patience law), no threads.
"""
from __future__ import annotations

import difflib
import hashlib
import importlib.util
import json
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
spec = importlib.util.spec_from_file_location(
    "stealth_fanout", ROOT / "tools" / "stealth_fanout.py")
sf = importlib.util.module_from_spec(spec)
sys.modules["stealth_fanout"] = sf
spec.loader.exec_module(sf)  # loads LANES, LAWS, _check_base

MODELS = [
    "stealth/space-bunny-alpha",
    "inclusionai/ling-3.0-flash-vl",
    "meta/muse-glimmer-30b",
]

PROMPT = ("Answer in under 250 words, numbered 1-3. "
          "(1) Give the exact citation (authors, title, venue, volume, "
          "issue, pages, year, DOI) for the 1966 study of the Belady "
          "anomaly in FIFO page replacement. "
          "(2) Name the four Galilean moons of Jupiter in order of "
          "DECREASING radius and give each radius in km. "
          "(3) In one sentence: why does FIFO page replacement show the "
          "anomaly while LRU does not? "
          "State a source for each answer or say OWED.")

WORK = ROOT / "watch" / "inbox" / "burn_reset_20260927" / "work"
QUEUE = ROOT / "watch" / "inbox" / "burn_reset_20260927" / "queue"
HEARTBEAT = sf.HEARTBEAT


def call_lane(lane: dict) -> dict:
    sf._check_base(lane["base"])
    body = json.dumps({
        "model": lane["model"],
        "messages": [{"role": "user",
                      "content": PROMPT + "\n\n" + sf.LAWS}],
        "max_tokens": 3000,  # pattern default, tools/stealth_fanout.py:105
    }).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if lane["key"]:
        headers["Authorization"] = f"Bearer {lane['key']}"
    req = urllib.request.Request(lane["base"], data=body, headers=headers)
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.loads(r.read().decode("utf-8", "replace"))
    dt = round(time.time() - t0, 1)
    choice = (d.get("choices") or [{}])[0]
    msg = choice.get("message") or {}
    text = (msg.get("content") or msg.get("reasoning_content")
            or msg.get("reasoning") or "").strip()
    if not text:
        print(f"  warn {lane['model']}: empty content, finish="
              f"{choice.get('finish_reason')} keys={sorted(msg)}", flush=True)
    usage = d.get("usage") or {}
    return {"text": text, "dt_s": dt, "ok": bool(text),
            "finish": choice.get("finish_reason"),
            "echoed_model": d.get("model"),
            "usage": usage}


def main() -> int:
    WORK.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    lanes = {l["model"]: l for l in sf.LANES}
    results = {}
    for i, model in enumerate(MODELS):
        if i:
            time.sleep(5)
        lane = lanes[model]
        row = {"lane_keyvar": "OPENROUTER_API_KEY"
               if model == MODELS[0] else "OPENROUTER_API_KEY_2",
               "base": lane["base"], "model": model}
        try:
            r = call_lane(lane)
            row.update(r)
        except Exception as e:
            row.update({"text": f"DISPATCH-ERR {type(e).__name__}: "
                                f"{str(e)[:160]}",
                        "ok": False, "dt_s": None, "finish": None,
                        "echoed_model": None, "usage": {}})
        slug = model.replace("/", "_")
        raw = WORK / f"drift_q033_{slug}.md"
        raw.write_text(
            f"# DRIFT Q-033\n\nlane model: {model}\n"
            f"key var: {row['lane_keyvar']}\n"
            f"ts: {datetime.now(timezone.utc).isoformat()}\n"
            f"dt: {row['dt_s']}s\nfinish: {row['finish']}\n"
            f"echoed_model: {row['echoed_model']}\n"
            f"usage: {json.dumps(row['usage'])}\n\n---\n\n{row['text']}\n",
            encoding="utf-8")
        hb = {"id": f"Q-033-drift-{slug}", "model": model, "ok": row["ok"],
              "dt_s": row["dt_s"], "chars": len(row["text"]),
              "finish": row["finish"],
              "cached": (row["usage"].get("prompt_tokens_details")
                         or {}).get("cached_tokens")}
        with HEARTBEAT.open("a", encoding="utf-8") as f:
            f.write(json.dumps(hb, ensure_ascii=False) + "\n")
        results[model] = row
        print(f"{model}: ok={row['ok']} chars={len(row['text'])} "
              f"dt={row['dt_s']}s finish={row['finish']}", flush=True)

    # pairwise unified diffs
    diffs = {}
    for a, b in [(0, 1), (0, 2), (1, 2)]:
        ma, mb = MODELS[a], MODELS[b]
        ta = results[ma]["text"].splitlines(keepends=True)
        tb = results[mb]["text"].splitlines(keepends=True)
        diff = "".join(difflib.unified_diff(
            ta, tb, fromfile=ma, tofile=mb, lineterm="\n"))
        diffs[f"{ma} vs {mb}"] = diff
    (WORK / "drift_q033_diffs.txt").write_text(
        "\n\n".join(f"===== {k} =====\n{v}"
                    for k, v in diffs.items()), encoding="utf-8")

    summary = {}
    for model, r in results.items():
        summary[model] = {
            "ok": r["ok"], "dt_s": r["dt_s"], "chars": len(r["text"]),
            "words": len(r["text"].split()), "finish": r["finish"],
            "echoed_model": r["echoed_model"],
            "completion_tokens": (r["usage"] or {}).get("completion_tokens"),
            "cached_tokens": ((r["usage"] or {}).get("prompt_tokens_details")
                              or {}).get("cached_tokens"),
            "sha256": hashlib.sha256(
                r["text"].encode("utf-8")).hexdigest(),
            "em_dash_count": r["text"].count("\u2014"),
            "says_OWED": "OWED" in r["text"],
        }
    (WORK / "drift_q033_summary.json").write_text(
        json.dumps({"prompt": PROMPT, "laws": sf.LAWS,
                    "lanes": summary, "diffs_chars":
                    {k: len(v) for k, v in diffs.items()}},
                   indent=2, ensure_ascii=False), encoding="utf-8")
    print("BANKED diffs + summary to", WORK.relative_to(ROOT), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
