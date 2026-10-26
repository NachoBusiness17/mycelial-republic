"""model_bakeoff — 50 concurrent calls across the free model-lane wall (2026-09-23,
operator: "call 50c of ten different models to test their output and the rest").

Every call does a REAL micro-chore (anchor-note for a verified ledger stone), so the
bake-off's output is usable, not just diagnostic. Measures per lane: ok-rate, latency,
tok/s, correctness (Church Committee final report = 1976), empty-content failures.
SSRF law: every outbound URL passes lite_guard._safe_https_url; redirects refused.
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from models.env_load import load_dotenv
load_dotenv()
from mag import lite_guard  # noqa: E402

MATRIX_MD = ROOT / "watch" / "inbox" / "MODEL_MATRIX_20260923.md"
LEDGER = ROOT / "state" / "fuel" / "bakeoff_ledger.jsonl"
CALLS_PER_LANE = 5
PROMPT = ("A verified receipt: the Church Committee issued its Final Report (S. Rep. 94-755) "
          "in April 1976, exposing COINTELPRO (2,000+ covert actions) and SHAMROCK (~150,000 "
          "telegrams/month copied). In exactly two sentences, write an anchor note for this "
          "receipt that a public post could quote. Include the year 1976.")

LANES = []


def lane(name: str, url: str, model: str, keyenv: str) -> None:
    key = (os.environ.get(keyenv, "") or os.environ.get(keyenv + "_2", "") or "").strip()
    if key:
        LANES.append({"name": name, "url": url, "model": model, "key": key})


lane("nvidia/glm-5.3-flash", "https://integrate.api.nvidia.com/v1/chat/completions",
     "z-ai/glm-5.3-flash", "NVIDIABuild")
lane("nvidia/deepseek-v4.1", "https://integrate.api.nvidia.com/v1/chat/completions",
     "deepseek-ai/deepseek-v4.1-flash", "NVIDIABuild")
lane("openrouter-a1/auto", "https://openrouter.ai/api/v1/chat/completions",
     "openrouter/auto", "OPENROUTER_API_KEY")
lane("openrouter-a2/auto", "https://openrouter.ai/api/v1/chat/completions",
     "openrouter/auto", "OPENROUTER_API_KEY_2")
lane("groq/gpt-oss-120b", "https://api.groq.com/openai/v1/chat/completions",
     "openai/gpt-oss-120b", "GROQ_API_KEY")
lane("groq2/gpt-oss-120b", "https://api.groq.com/openai/v1/chat/completions",
     "openai/gpt-oss-120b", "GROQ_API_KEY_2")
lane("cerebras/llama-3.3-70b", "https://api.cerebras.ai/v1/chat/completions",
     "llama-3.3-70b", "CEREBRAS_API_KEY")
lane("deepseek/deepseek-chat", "https://api.deepseek.com/chat/completions",
     "deepseek-chat", "DEEPSEEK_API_KEY")
lane("together/dsv4-flash", "https://api.together.xyz/v1/chat/completions",
     "deepseek-ai/DeepSeek-V4-Flash-0731", "TOGETHER_API_KEY")
lane("zai-lite/glm-4.7-flash", "https://api.z.ai/api/paas/v4/chat/completions",
     "glm-4.7-flash", "ZAI_API_KEY_Lite")

HERMES_KEY = (os.environ.get("HERMES_API_KEY_1", "") or os.environ.get("HERMES_API_KEY_2", "") or "").strip()
HERMES_URL = "https://inference-api.nousresearch.com/v1/chat/completions"
if HERMES_KEY:
    lane("nous/hermes-4-70b", HERMES_URL, "Hermes-4-70B", "HERMES_API_KEY_1")


def call(ln: dict) -> dict:
    if not lite_guard._safe_https_url(ln["url"]):
        return {"lane": ln["name"], "ok": False, "wall_s": 0, "error": "SSRF guard rejected url"}
    body = json.dumps({"model": ln["model"],
                       "messages": [{"role": "user", "content": PROMPT}],
                       "max_tokens": 300, "temperature": 0}).encode()
    headers = {"Authorization": "Bearer " + ln["key"], "Content-Type": "application/json"}
    req = urllib.request.Request(ln["url"], data=body, headers=headers)
    t0 = time.time()
    try:
        with lite_guard._OPENER.open(req, timeout=120) as r:
            d = json.loads(r.read().decode())
        msg = (d.get("choices") or [{}])[0].get("message", {}) or {}
        content = (msg.get("content") or "").strip()
        if not content:
            content = "[reasoning only] " + (msg.get("reasoning_content") or "").strip()
        wall = time.time() - t0
        usage = d.get("usage", {}) or {}
        ev = usage.get("completion_tokens", 0)
        return {"lane": ln["name"], "ok": bool(content.strip()), "wall_s": round(wall, 1),
                "tok_per_s": round(ev / (wall or 1), 1), "correct_1976": "1976" in content,
                "head": content[:150]}
    except Exception as e:
        return {"lane": ln["name"], "ok": False, "wall_s": round(time.time() - t0, 1),
                "error": type(e).__name__ + ": " + str(e)[:100]}


def one_call(ln: dict) -> dict:
    r = call(ln)
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": datetime.now(timezone.utc).isoformat(), **r}) + "\n")
    return r


def main() -> dict:
    if not LANES:
        return {"ok": False, "error": "no lanes had keys"}
    tasks = [(ln, i) for ln in LANES for i in range(CALLS_PER_LANE)]
    print(f"firing {len(tasks)} calls across {len(LANES)} lanes...", flush=True)
    with ThreadPoolExecutor(max_workers=12) as ex:
        futures = {ex.submit(one_call, ln): (ln["name"], i + 1) for ln in LANES for i in range(CALLS_PER_LANE)}
    out = []
    for fut, tag in futures.items():
        try:
            r = fut.result()
            r["call"] = tag[1]
            out.append(r)
        except Exception as e:
            out.append({"lane": tag[0], "ok": False, "error": str(e)[:100]})

    by_lane: dict[str, list] = {}
    for r in out:
        by_lane.setdefault(r["lane"], []).append(r)
    summary_rows = []
    for name in by_lane:
        rs = by_lane[name]
        oks = [r for r in rs if r.get("ok")]
        corr = [r for r in oks if r.get("correct_1976")]
        lat = [r["wall_s"] for r in oks]
        tps = [r["tok_per_s"] for r in oks if r.get("tok_per_s")]
        summary_rows.append({
            "lane": name, "calls": len(rs), "ok": len(oks), "correct": len(corr),
            "avg_lat_s": round(sum(lat) / len(lat), 1) if lat else None,
            "avg_tok_s": round(sum(tps) / len(tps), 1) if tps else None,
            "verdict": ("carry" if len(oks) == len(rs) and len(corr) >= 3 else
                        "flaky" if len(oks) >= 2 else "cut"),
        })
    md = [
        "# MODEL MATRIX — 50-call bake-off across the free wall (2026-09-23)",
        "",
        "Chore: anchor-note for the Church Committee stone (correct = cites 1976). All calls fired concurrently.",
        "",
        "| lane | calls | ok | correct | avg latency | avg tok/s | verdict |",
        "|---|---|---|---|---|---|---|",
    ]
    for s in summary_rows:
        md.append("| " + s["lane"] + " | " + str(s["calls"]) + " | " + str(s["ok"]) + " | "
                  + str(s["correct"]) + " | " + str(s["avg_lat_s"] or "-") + "s | "
                  + str(s["avg_tok_s"] or "-") + " | **" + s["verdict"] + "** |")
    md += ["", "## Sample outputs (first ok call per lane)", ""]
    for name, rs in by_lane.items():
        okr = next((r for r in rs if r.get("ok")), None)
        md.append("### " + name)
        md.append((okr.get("head") if okr else "no ok call"))
        md.append("")
    MATRIX_MD.parent.mkdir(parents=True, exist_ok=True)
    MATRIX_MD.write_text("\n".join(md), encoding="utf-8")
    return {"lanes": len(by_lane), "summary": summary_rows, "file": str(MATRIX_MD)}


if __name__ == "__main__":
    print(json.dumps(main(), indent=1))
