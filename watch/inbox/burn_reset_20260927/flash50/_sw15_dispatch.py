"""sw-15 free-lane dispatch: information bottleneck in multi-agent
communication (optimal compression for inter-agent messages).

Reuses tools/stealth_fanout.py LANES + _check_base (allowlisted bases,
public-host check) and the sw-03 session lane repairs: llm7 gpt-4o-mini
retired for glm-5.3, muse-spark 403 on this key, stealth+ling need the
reasoning-key fallback. Low width per the fanout width law: 3 asks,
2 workers. Outputs banked as SENSING findings
(RIB_DRIVING_LADDER_20260928), never trusted work. No subprocess spawns
in this script (urllib only), so no CREATE_NO_WINDOW surface.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from tools.stealth_fanout import LANES, _check_base  # noqa: E402


def dispatch2(lane: dict, ask: str, max_tokens: int = 3000):
    """fanout dispatch + reasoning-key fallback (ling puts completion
    tokens in msg.reasoning, content empty at finish_reason length)."""
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


LANES[9]["model"] = "glm-5.3"  # llm7 repair measured by sibling sw-03

OUT_DIR = ROOT / "watch" / "inbox" / "burn_reset_20260927" / "flash50"
HEARTBEAT = OUT_DIR / "_sw15_heartbeat.jsonl"

ASKS = [
    ("sw-ib-1",
     "Information bottleneck theory applied to inter-agent communication "
     "in multi-agent systems: how is the Tishby-Pereira-Bialek 1999 "
     "information bottleneck formalized when the message M sent from one "
     "agent to another must minimize I(M; sender full state) while "
     "maximizing I(M; receiver task performance)? Cover the original "
     "paper, Tishby-Zaslavsky 2015 deep-learning IB view, Alemi et al "
     "2016 Deep Variational Information Bottleneck (arXiv 1612.00410), "
     "and any paper that states an agent-communication IB objective "
     "explicitly. Give exact titles, arXiv ids, years. OWED if you "
     "cannot verify a claim."),
    ("sw-ib-2",
     "Channel compression for emergent multi-agent reinforcement "
     "learning communication: CommNet (Foerster et al 2016), DIAL "
     "(Sukhbaatar et al 2016), message dropout and channel noise, "
     "discrete/Gumbel-softmax bottlenecked messages, variational "
     "message passing, and papers that measure bits-per-message vs task "
     "reward tradeoffs (2016-2026). Which papers explicitly constrain "
     "bandwidth or information content of inter-agent messages, and what "
     "did they measure? Exact titles, arXiv ids, venues. OWED if "
     "unverifiable."),
    ("sw-ib-3",
     "Compression of inter-agent messages in LLM-based multi-agent "
     "systems: LLMLingua prompt compression family (Jiang et al 2023), "
     "agent message summarization, multi-agent communication topology "
     "and cost optimization (GPTSwarm, AFlow, MaAS), token-budget "
     "control, measured token savings and quality tradeoffs. What is "
     "actually published with numbers, and what is only claimed? Exact "
     "titles, arXiv ids, venues, measured percentages where stated. OWED "
     "if unverifiable."),
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
    out = OUT_DIR / f"_sw15_out_{item_id}_{slug}.md"
    out.write_text(
        f"# SW15 {item_id}\n\nlane model: {lane['model']}\n"
        f"ts: {datetime.now(timezone.utc).isoformat()}\ndt: {dt}s\n\n"
        f"---\n\n{text}\n", encoding="utf-8")
    row = {"id": item_id, "model": lane["model"], "ok": ok, "dt_s": dt,
           "chars": len(text)}
    with HEARTBEAT.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


LANE_MAP = {0: 9, 1: 1, 2: 0}  # glm-5.3@llm7, ling:free@OR, stealth@OR


def main() -> int:
    print(f"sw15 dispatch: {len(ASKS)} asks over {len(LANES)} lanes",
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
