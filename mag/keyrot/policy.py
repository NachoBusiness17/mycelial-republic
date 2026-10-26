"""Policy: leaked (git history / public remote), old (age > per-provider max), unused."""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "configs" / "keyrot_policy.json"
PUBLIC_REMOTES = {"github", "origin"}


def load() -> dict:
    return json.loads(POLICY.read_text(encoding="utf-8"))


def evaluate(row: dict, first_seen: str, pol: dict, today: dt.date | None = None) -> dict:
    today = today or dt.date.today()
    flags: list[str] = []
    lk = row.get("leak", {})
    if lk.get("head_files"):
        flags.append("leaked_head")
    if lk.get("commits"):
        flags.append("leaked_public_remote" if set(lk.get("remotes", [])) & PUBLIC_REMOTES else "leaked_git_history")
    if lk.get("history") in ("timeout", "partial"):
        flags.append("history_unverified")
    max_age = pol["max_age_days"].get(row["type"], pol["default_max_age_days"])
    age = (today - dt.date.fromisoformat(first_seen)).days if first_seen else None
    if age is not None and age > max_age:
        flags.append("old")
    if pol.get("unused_flag") and row.get("usage", {}).get("code_refs", 0) == 0 and not row.get("live"):
        flags.append("unused")
    if not row.get("live"):
        flags.append("stale_copy_only")
    rotate = any(f.startswith("leaked") for f in flags) or "old" in flags
    action = "rotate" if rotate else ("cleanup" if "unused" in flags else "keep")
    return {"flags": flags, "age_days": age, "max_age_days": max_age, "action": action,
            "severity": "P0" if any(f.startswith("leaked") for f in flags) else ("P1" if rotate else "P3")}
