"""lane_salon — the frontier salon, made to work with the seats we ACTUALLY have.

Operator (2026-08-24): "look at all the seats you do have. look at what it was attempting and
make it work. i was just simply attempting what you are now capable of."

The ORIGINAL frontier_salon was a sacred cow that hung forever: it reached ChatGPT/SuperGrok via
the CDP browser seats (down), so it sat waiting instead of answering. The IDEA was right — many
seats witness the same question, then their answers are combined. This module makes it WORK by
using the seats that ARE reachable: the API lanes (models.providers.chat_provider — verified:
nvidia, openrouter, groq, together, deepseek), all with real timeouts, honest down-reporting.

  salon(question) -> every reachable API lane witnesses the SAME question, then the answers are
                     combined: roshomon-style shared invariant (token overlap = the consensus) +
                     each seat's distinct contribution. Honest: a down lane reports down, never
                     fabricates. FREE-FIRST: the paid lane (deepseek-pro) only joins off-peak
                     (mag.offpeak) unless MAG_ALLOW_PEAK=1.

Schema: lane_salon.v1 · deterministic + $0 coordinator · reuse: models.providers.chat_provider,
roshomon (consensus), offpeak (paid-lane gating)
CLI: python -m mag.lane_salon salon "<question>" [--lanes nvidia,openrouter,...]
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from typing import Any

try:
    from config import ROOT
except Exception:  # noqa: BLE001
    from pathlib import Path as _P
    ROOT = _P(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # noqa: BLE001
    pass

SCHEMA = "lane_salon.v1"
OUT = ROOT / "memory" / "runs" / "lane_salon"

# The witnesses — the API lanes that actually work (verified today):
# (label, provider_id, model or None=provider default, paid?).
WITNESSES: list[tuple[str, str, str | None, bool]] = [
    ("nvidia-flash", "nvidia", "deepseek-ai/deepseek-v4-flash-0731", False),
    ("openrouter", "openrouter", "openrouter/auto", False),
    ("groq", "groq", None, False),
    ("together", "together", None, False),
    ("deepseek-pro", "deepseek", None, True),  # paid — off-peak only
]

_TOKEN_RE = re.compile(r"[a-z0-9_]+")
_TRIVIAL = {"that", "this", "with", "from", "have", "will", "what", "would", "your",
            "there", "they", "should", "their", "about"}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _witness(label: str, provider: str, model: str | None, paid: bool, question: str) -> dict[str, Any]:
    """Ask ONE lane via the API surface (chat_provider). Honest down-reporting, never fabricates.
    Paid lanes defer off-peak unless MAG_ALLOW_PEAK=1 (free-first)."""
    if paid:
        try:
            from mag.offpeak import defer_if_peak
            if defer_if_peak().get("defer"):
                return {"ok": False, "surface": label, "provider": provider, "paid": True,
                        "error": "deferred_peak — paid lane off-peak only (MAG_ALLOW_PEAK=1 overrides)",
                        "answer": ""}
        except Exception:  # noqa: BLE001
            pass
    try:
        from models.providers import reload_providers, chat_provider
        reload_providers()
        kw = {"tier": "T2", "max_tokens": 900}
        if model:
            kw["model"] = model
        r = chat_provider(provider, system="You are one witness in a sovereign roundtable. "
                                           "Answer the question directly and concretely, your own view.",
                          user=question, **kw)
        text = (r.get("text") or "").strip()
        return {"ok": bool(r.get("ok")) and bool(text), "surface": label, "provider": provider,
                "paid": paid, "answer": text, "error": (r.get("error") or "")[:160]}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "surface": label, "provider": provider, "paid": paid,
                "answer": "", "error": f"unreachable: {str(e)[:120]}"}


def _consensus(witnesses: list[dict[str, Any]]) -> str:
    """roshomon-style: the tokens SHARED across the available witnesses (deterministic)."""
    ok = [w for w in witnesses if w.get("ok")]
    if not ok:
        return "no witnesses answered — the salon cannot consensus on nothing"
    sets = [set(_TOKEN_RE.findall((w.get("answer") or "").lower())) for w in ok]
    common = set.intersection(*sets) if sets else set()
    common = {t for t in common if len(t) > 3 and t not in _TRIVIAL}
    return " ".join(sorted(common))[:400] if common else \
        "the witnesses agree on no shared token (distinct expertise — each line kept)"


def salon(question: str, *, lanes: list[str] | None = None) -> dict[str, Any]:
    """Every reachable API lane witnesses the same question; answers combined into consensus +
    per-seat contributions. Honest: down lanes reported, never fabricated."""
    q = (question or "").strip()
    if not q:
        return {"ok": False, "schema": SCHEMA, "error": "empty question"}
    selected = WITNESSES
    if lanes:
        want = {str(x).strip().lower() for x in lanes}
        selected = [w for w in WITNESSES if w[0].lower() in want]
    results = []
    for label, provider, model, paid in selected:
        results.append(_witness(label, provider, model, paid, q))
    up = [w for w in results if w.get("ok")]
    consensus = _consensus(results)
    OUT.mkdir(parents=True, exist_ok=True)
    run = {"schema": SCHEMA, "ts": _now(), "question": q, "n_witnesses": len(selected),
           "n_up": len(up), "consensus": consensus, "witnesses": results}
    try:
        (OUT / f"salon_{_now()[:16].replace(':', '')}.json").write_text(
            json.dumps(run, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    return {"ok": bool(up), "schema": SCHEMA, "ts": _now(), "n_witnesses": len(selected),
            "n_up": len(up), "consensus": consensus,
            "witnesses": [{k: w[k] for k in ("surface", "ok", "paid", "answer", "error")} for w in results],
            "note": "the seats we actually have, in tandem — free lanes first, paid deepseek off-peak"}


def main(argv: list[str] | None = None) -> int:
    import argparse
    p = argparse.ArgumentParser(prog="lane_salon", description="salon over the working API seats")
    p.add_argument("cmd", nargs="?", default="salon", choices=["salon", "status"])
    p.add_argument("question", nargs="?")
    p.add_argument("--lanes", default="")
    a = p.parse_args(argv)
    if a.cmd == "status":
        print(json.dumps({"schema": SCHEMA, "witnesses": [w[0] for w in WITNESSES],
                          "note": "API lanes that work — free-first, paid deepseek off-peak"}, indent=2))
        return 0
    q = a.question or ""
    if not q:
        print("usage: python -m mag.lane_salon salon '<question>' [--lanes ...]")
        return 1
    lanes = [x for x in a.lanes.split(",") if x.strip()] if a.lanes else None
    print(json.dumps(salon(q, lanes=lanes), ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
