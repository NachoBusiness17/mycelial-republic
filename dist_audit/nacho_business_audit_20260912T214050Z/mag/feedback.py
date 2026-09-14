"""feedback — OUR feedback pipe (replaces the vendor thumbs-up). A 👍/👎 becomes a training
signal in the SOVEREIGN mem weave, not Microsoft telemetry.

Operator (2026-08-11): "delete theirs and put our common tools there" — the feedback gesture feeds
OUR system: attention_ranker.record_feedback (ranking) + training_row.v1 (training) + verkle knot
(durable, content-addressed record). Same gesture, signal lands in OUR memory.

Contract: feedback.v1 · deterministic · $0.
CLI: python -m mag.feedback good|bad [item_id] [--context "..."]   (also via ghost chat / REST)
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

SCHEMA = "feedback.v1"
TRAINING = ROOT / "memory" / "pile" / "training_rows.jsonl"
FEEDBACK_LEDGER = ROOT / "memory" / "runs" / "feedback" / "feedback.jsonl"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _append_jsonl(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False, default=str) + "\n")


def capture(signal: str, *, item_id: str = "", context: str = "", source: str = "ghost-chat") -> dict[str, Any]:
    """Turn a positive/negative signal into a sovereign training + ranking + verkle record."""
    signal = (signal or "").strip().lower()
    if signal not in ("good", "bad", "up", "down", "positive", "negative", "thumbs-up", "thumbs-down"):
        return {"ok": False, "schema": SCHEMA, "error": f"unknown signal: {signal}"}
    # normalize
    good = signal in ("good", "up", "positive", "thumbs-up")
    norm = "good" if good else "bad"
    out: dict[str, Any] = {"ok": True, "schema": SCHEMA, "ts": _now(),
                           "signal": norm, "source": source, "item_id": item_id}

    # 1) ranking feedback (existing attention_ranker pipe)
    try:
        from mag.attention_ranker import record_feedback
        r = record_feedback(item_id or f"feedback-{datetime.now(timezone.utc).strftime('%H%M%S')}",
                            norm, source=source)
        out["ranking"] = bool(r.get("ok", True))
    except Exception as e:
        out["ranking_error"] = str(e)[:80]

    # 2) training_row.v1 (our training data)
    _append_jsonl(TRAINING, {"schema": "training_row.v1", "ts": _now(),
                             "source": "feedback", "signal": norm,
                             "input": context or item_id, "output": norm})
    out["training_written"] = True

    # 3) feedback ledger
    _append_jsonl(FEEDBACK_LEDGER, {"ts": _now(), "signal": norm, "item_id": item_id,
                                    "context": context, "source": source})

    # 4) verkle knot (durable content-addressed record)
    try:
        from mag.verkle_knot import append_verkle_knot
        append_verkle_knot({"session_id": f"feedback:{datetime.now(timezone.utc).strftime('%H%M%S')}",
                            "theme": "behavior",
                            "summary": f"[feedback] {norm} signal from {source} on {item_id or context[:60]}"})
        out["verkle"] = True
    except Exception as e:
        out["verkle_error"] = str(e)[:80]
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="feedback",
                                 description="Our feedback pipe: 👍/👎 -> training + ranking + verkle (not Microsoft).")
    ap.add_argument("signal", nargs="?", default="good")
    ap.add_argument("item_id", nargs="?", default="")
    ap.add_argument("--context", default="")
    ap.add_argument("--source", default="ghost-chat")
    a = ap.parse_args(argv)
    print(json.dumps(capture(a.signal, item_id=a.item_id, context=a.context, source=a.source),
                     indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

__all__ = ["capture", "main"]
