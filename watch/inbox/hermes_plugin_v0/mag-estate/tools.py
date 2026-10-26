"""Thin, read-only wrappers over existing Mag organs. No new engine, no secrets, no network.

Each handler: (args: dict, **kwargs) -> JSON str, never raises.
The Mag repo is located from plugin setting mag_root, else env MAG_ROOT.
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import sys
from pathlib import Path

_ROOT: Path | None = None


def configure(root: str | None) -> None:
    global _ROOT
    r = (root or os.environ.get("MAG_ROOT") or "").strip()
    _ROOT = Path(r).expanduser().resolve() if r else None


def _ready() -> str | None:
    if _ROOT is None:
        return "not_configured: set plugins.entries.mag-estate.settings.mag_root or env MAG_ROOT"
    if not (_ROOT / "mag" / "__init__.py").exists() and not (_ROOT / "mag").is_dir():
        return f"not_a_mag_root: {_ROOT}"
    if str(_ROOT) not in sys.path:
        sys.path.insert(0, str(_ROOT))
    return None


def _out(obj) -> str:
    return json.dumps(obj, default=str, ensure_ascii=False)


def _quiet(fn, *a, **k):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        return fn(*a, **k)


def mag_chain_verify(args: dict, **kwargs) -> str:
    try:
        if (e := _ready()):
            return _out({"ok": False, "error": e})
        from mag import verkle_knot
        ok, why = _quiet(verkle_knot._verify_chain_consistent)
        return _out({"ok": bool(ok), "reason": why, "tier": "verified-internal-consistency",
                     "caveat": "no external witness consulted"})
    except Exception as exc:  # never raise into the agent
        return _out({"ok": False, "error": f"{type(exc).__name__}: {exc}"[:400]})


def mag_receipt_validate(args: dict, **kwargs) -> str:
    try:
        if (e := _ready()):
            return _out({"ok": False, "error": e})
        from mag import fleet_report
        raw = args.get("report", "")
        try:
            obj = json.loads(raw) if isinstance(raw, str) else raw
        except ValueError as exc:
            return _out({"ok": False, "errors": [f"not JSON: {exc}"]})
        errs = fleet_report.validate(obj)
        return _out({"ok": not errs, "errors": errs})
    except Exception as exc:
        return _out({"ok": False, "error": f"{type(exc).__name__}: {exc}"[:400]})


def mag_notices(args: dict, **kwargs) -> str:
    try:
        if (e := _ready()):
            return _out({"ok": False, "error": e})
        from mag import fleet_report
        n = fleet_report.notices()
        rows = [{"notice_id": x.get("notice_id"), "acks": len(x.get("acks") or []),
                 "receipt": x.get("receipt")} for x in n.get("in_force", [])]
        return _out({"ok": True, "in_force": rows, "closed": len(n.get("closed", []))})
    except Exception as exc:
        return _out({"ok": False, "error": f"{type(exc).__name__}: {exc}"[:400]})


def mag_leases(args: dict, **kwargs) -> str:
    try:
        if (e := _ready()):
            return _out({"ok": False, "error": e})
        from mag import leases
        return _out(leases.list_leases(include_free=False))
    except Exception as exc:
        return _out({"ok": False, "error": f"{type(exc).__name__}: {exc}"[:400]})
