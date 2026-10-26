"""GROK 4.7 CLI OVERFLOW BURN - one real fan-out-suitable chore through the estate's
grok CLI harness seat (2026-09-25 window task, grok-overflow seat).

Chore: BOOT_LANE_INTERFERENCE_BURN_20260925.md Stone 5.1 - adversarial pass on the
frozen interference-replication pre-registration (+ Amendment 1) BEFORE Arms A/C run.
Fan-out-suitable shape: same review chore fans out across prereg docs/items.

Path taken: grok CLI headless (harness.grok_cli.escalate_via_harness), session auth
via auth.x.ai OIDC -> cli-chat-proxy.grok.com. This is NOT the Nous Portal 50%-off
lane (that rides portal.nousresearch.com / Hermes keys) and NOT the estate
XAI_API_KEY cash lane (operator-gated by grok_route.v1). Proxy self-reports
total_cost_usd; receipt appended to logs/provider_usage.jsonl.

Run: .venv/Scripts/python.exe _grok47_chore_run.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from harness.grok_cli import escalate_via_harness  # noqa: E402

PREREG = ROOT / "watch/inbox/INTERFERENCE_REPLICATION_PREREG_20260925.md"
AMEND = ROOT / "watch/inbox/INTERFERENCE_REPLICATION_PREREG_AMENDMENT1_20260925.md"
LEDGER = ROOT / "logs/provider_usage.jsonl"
HANDOFF = "20260925-grok47-prereg-adversarial"

goal = (
    "Adversarial pass on a frozen experiment pre-registration BEFORE its arms run. "
    "Work ONLY from the text pasted below: do NOT read files, do NOT use any tools, "
    "do NOT explore the repository. Output the review directly in this reply. "
    "Find the strongest real objections: bars that are miscalibrated or gameable, "
    "missing controls, ambiguities a result could exploit (reroll/bar-shopping/"
    "rescue-interpretation risks), claims the design cannot support. For each: quote "
    "the pasted line, state the risk, give the cheapest fix that does NOT move a "
    "frozen bar. Judge the design as-is; do not redesign it. Keep the review under "
    "800 words. End with VERDICT: SOUND, SOUND-WITH-FIXES, or UNSOUND, and one "
    "sentence why."
)
context = (
    f"### PRE-REGISTRATION (frozen)\n{PREREG.read_text(encoding='utf-8')}\n\n"
    f"### AMENDMENT 1 (frozen)\n{AMEND.read_text(encoding='utf-8')}"
)

res = escalate_via_harness(
    goal=goal,
    context=context,
    warm=False,  # one-shot review; the CLI session prefix is already cache-warm
    cwd=ROOT,
    max_turns=1,  # single-turn review, no tool use wanted
    yolo=False,
    output_format="json",
    handoff_id=HANDOFF,
    timeout=420,
    model="grok-4.7",
    reasoning_effort="low",
)

out_path = ROOT / "watch/inbox/INTERFERENCE_PREREG_ADVERSARIAL_GROK47_20260925.md"
res["chore"] = "BOOT_LANE Stone 5.1 adversarial pass on interference prereg"
res["asked_model"] = "grok-4.7"
if res.get("ok") and (res.get("deliverable") or "").strip():
    body = res["deliverable"]
    header = (
        "# GROK 4.7 ADVERSARIAL PASS - interference prereg (filed 2026-09-25)\n\n"
        "Chore: BOOT_LANE_INTERFERENCE_BURN_20260925.md Stone 5.1, adversarial pass on the\n"
        "frozen prereg + Amendment 1 BEFORE Arms A/C run. Fan-out-suitable shape (same\n"
        "review chore fans across prereg docs).\n\n"
        "Path: grok CLI harness (harness/grok_cli.py, headless) -> cli-chat-proxy.grok.com,\n"
        "auth.x.ai session. NOT the Nous Portal 50% lane; NOT the estate XAI cash lane.\n"
        f"Model: {(res.get('model_used') or ['?'])[0]} | cost ${res.get('cost_usd')} "
        f"(proxy self-reported) | latency {res.get('latency_ms')}ms | "
        f"usage {json.dumps(res.get('usage') or {})}\n"
        "Verbatim model output below; review-of-review is the driver seat's job, not this file's.\n\n"
        "---\n\n"
    )
    out_path.write_text(header + body + "\n", encoding="utf-8")
else:
    out_path.write_text(
        json.dumps(res, indent=2)[:200000], encoding="utf-8"
    )

# Ledger row: same schema as logs/provider_usage.jsonl rows (cost + latency receipt).
usage = res.get("usage") or {}
row = {
    "ts": datetime.now(timezone.utc).isoformat(),
    "provider": "xai",
    "model": (res.get("model_used") or ["grok-4.7?"])[0],
    "calls": 1,
    "prompt_tokens": usage.get("input_tokens", 0),
    "completion_tokens": usage.get("output_tokens", 0),
    "cache_hit_tokens": usage.get("cache_read_input_tokens", 0),
    "cache_miss_tokens": usage.get("cache_creation_input_tokens", 0),
    "session_id": HANDOFF,
    "latency_ms": res.get("latency_ms"),
    "tokens": usage.get("total_tokens", 0),
    "ok": bool(res.get("ok")),
    "cost_usd": res.get("cost_usd"),
    "meta": {
        "surface": "grok CLI harness (harness/grok_cli.py) -> cli-chat-proxy.grok.com, auth.x.ai session",
        "pricing_path": "xAI account session on Grok Build proxy; cost self-reported by proxy "
                        "total_cost_usd. NOT the Nous Portal 50%-off week lane; NOT the estate "
                        "XAI_API_KEY cash lane (grok_route.v1 operator-gated).",
        "chore": res["chore"],
        "result_path": str(out_path),
    },
}
with LEDGER.open("a", encoding="utf-8") as f:
    f.write(json.dumps(row) + "\n")

print(json.dumps({
    "ok": res.get("ok"),
    "exit_code": res.get("exit_code"),
    "latency_ms": res.get("latency_ms"),
    "cost_usd": res.get("cost_usd"),
    "usage": res.get("usage"),
    "model_used": res.get("model_used"),
    "stop_reason": res.get("stop_reason"),
    "result_path": str(out_path),
    "deliverable_head": (res.get("deliverable") or "")[:400],
}, indent=2))
