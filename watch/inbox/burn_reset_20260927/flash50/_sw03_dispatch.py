"""sw-03 free-lane dispatch: economics of AI agent swarms.

Reuses tools/stealth_fanout.py lanes + dispatch (allowlisted bases,
public-host check). Low width per the fanout width law: 3 asks, 2 workers.
Outputs banked as SENSING findings (RIB_DRIVING_LADDER_20260928), never
trusted work. No subprocess spawns in this script (urllib only), so no
CREATE_NO_WINDOW surface.
"""
from __future__ import annotations

import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from tools.stealth_fanout import LANES, _check_base  # noqa: E402

import json  # noqa: E402
import urllib.request  # noqa: E402


def dispatch2(lane: dict, ask: str, max_tokens: int = 3000):
    """fanout dispatch + reasoning-key fallback (ling 2026-09-29 puts all
    completion tokens in msg.reasoning, content empty at finish_reason
    length)."""
    _check_base(lane["base"])
    body = json.dumps({
        "model": lane["model"],
        "messages": [{"role": "user", "content": ask}],
        "max_tokens": max_tokens,
    }).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if lane["key"]:
        headers["Authorization"] = f"Bearer {lane['key']}"
    req = urllib.request.Request(lane["base"], data=body, headers=headers)
    with urllib.request.urlopen(req, timeout=240) as r:
        d = json.loads(r.read().decode("utf-8", "replace"))
    msg = (d.get("choices") or [{}])[0].get("message") or {}
    text = (msg.get("content") or msg.get("reasoning")
            or msg.get("reasoning_content") or "").strip()
    return text, d.get("usage") or {}


# lane repairs measured this session: llm7 gpt-4o-mini retired (400
# model_unavailable, live /v1/models lists glm-5.3); muse-spark 403 on this
# key; stealth+ling need the reasoning fallback.
LANES[9]["model"] = "glm-5.3"

OUT_DIR = ROOT / "watch" / "inbox" / "burn_reset_20260927" / "flash50"
HEARTBEAT = OUT_DIR / "_sw03_heartbeat.jsonl"

ASKS = [
    ("sw-econ-1",
     "Economics of AI agent swarms: cost per useful output. What published "
     "numbers or credible industry writeups exist for token cost per "
     "completed agent task? Include Anthropic's statement that agentic "
     "interactions use roughly 4x the tokens of a chat interaction, any "
     "OpenAI/Google agent-economics posts, and per-task dollar figures from "
     "production deployments. Name each source. OWED if unverifiable."),
    ("sw-econ-2",
     "Free-tier API models vs paid models for production agent work: rate "
     "limits, reliability, silent model routing/downgrades on free tiers, "
     "data-usage and licensing restrictions (Gemini free tier training use, "
     "OpenRouter :free models, Groq free tier). What is the practical "
     "boundary where free tiers stop being safe for production? Cite docs or "
     "writeups by name. OWED if unverifiable."),
    ("sw-econ-3",
     "The quality-price frontier for LLMs: benchmark-per-dollar evidence "
     "(Artificial Analysis intelligence index per dollar, LMArena vs price, "
     "downscaled-model value), and the route-cheap-models-for-simple-steps "
     "pattern in multi-agent systems (FrugalGPT and successors). What does "
     "the evidence say about small models matching frontier models at a "
     "fraction of cost? Cite names. OWED if unverifiable."),
]


def run_item(i: int, item_id: str, ask: str, lane_idx: int) -> dict:
    lane = LANES[lane_idx]
    t0 = time.time()
    try:
        text, usage = dispatch2(lane, ask, max_tokens=3000)
        ok = bool(text.strip())
    except Exception as e:
        text = f"DISPATCH-ERR {type(e).__name__}: {str(e)[:140]}"
        ok, usage = False, {}
    dt = round(time.time() - t0, 1)
    slug = lane["model"].replace("/", "_")
    out = OUT_DIR / f"_sw03_out_{item_id}_{slug}.md"
    out.write_text(
        f"# SW03 {item_id}\n\nlane model: {lane['model']}\n"
        f"ts: {datetime.now(timezone.utc).isoformat()}\ndt: {dt}s\n\n"
        f"---\n\n{text}\n", encoding="utf-8")
    row = {"id": item_id, "model": lane["model"], "ok": ok, "dt_s": dt,
           "chars": len(text)}
    with HEARTBEAT.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


LANE_MAP = {0: 9, 1: 1, 2: 0}  # glm-5.3@llm7, ling:free@OR, stealth@OR


def main() -> int:
    print(f"sw03 dispatch: {len(ASKS)} asks over {len(LANES)} lanes",
          flush=True)
    for idx, lane in [(k, LANES[v]) for k, v in LANE_MAP.items()]:
        print(f"  ask[{idx}] -> {lane['model']}", flush=True)
    results = []
    with ThreadPoolExecutor(max_workers=2) as ex:
        futs = {ex.submit(run_item, i, item_id, ask, LANE_MAP[i]): item_id
                for i, (item_id, ask) in enumerate(ASKS)}
        for fut in as_completed(futs):
            results.append(fut.result())
    ok_n = sum(1 for r in results if r["ok"])
    print(f"DONE {ok_n}/{len(results)} banked to "
          f"{OUT_DIR.relative_to(ROOT)}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
