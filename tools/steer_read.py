"""steer_read — read the operator STEER channel (watch/inbox/STEER.md).

Spec: watch/inbox/operator_model/STEER.md (2026-09-30). The file is JSONL,
append-only, one row per operator interrupt. This reader resolves the
operative row for a mate so the leave protocol can inject it between cycles.

Contract (spec THE READ PATH + VALIDATION AND GATES):
- Applicable rows for a mate: `mate` == the mate id OR "all" (no other wildcards).
- LATEST WINS: operative row = newest `ts` among applicable VALID rows; file
  order breaks exact ts ties (later line wins).
- Schema per row: strings `mate`, `steer`, `ts` (ts must parse as ISO-8601).
  Malformed/unparseable rows are skipped, reported, and logged to stderr —
  a corrupt steer never silently widens scope; the mate proceeds with the
  last VALID row.
- ANTI-FORGERY: only `via` in {"hand-edit", "hermes-dm", "phone-relay"} is an
  operator-sourced order. Any other/missing `via` marks the row a PROPOSAL
  in the output (`proposal: true`); consumers treat proposals as asks, not orders.

Exit code (CLI): 0 when the file read cleanly, 1 when malformed rows were seen.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_PATH = Path(__file__).resolve().parent.parent / "watch" / "inbox" / "STEER.md"

OPERATOR_VIA = {"hand-edit", "hermes-dm", "phone-relay"}  # spec ANTI-FORGERY: no-provenance = proposal
REQUIRED_FIELDS = ("mate", "steer", "ts")


def _parse_ts(raw: str) -> datetime | None:
    """Parse an ISO-8601 ts; tolerate the trailing Z the spec examples use."""
    if not isinstance(raw, str) or not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None


def _classify(row: dict[str, Any]) -> dict[str, Any]:
    """Annotate a valid row with proposal status (anti-forgery teeth)."""
    out = dict(row)
    out["proposal"] = row.get("via") not in OPERATOR_VIA
    return out


def read(target_mate: str, path: Path | str | None = None) -> dict[str, Any]:
    """Resolve the operative steer row(s) for target_mate.

    Returns {"ok", "mate", "operative", "rows", "malformed", "n_seen"}:
      operative — latest applicable valid row (or None), already proposal-annotated;
      rows      — all applicable valid rows, oldest first, annotated;
      malformed — [{"line": n, "reason": str}, ...] for skipped lines;
      ok        — False when the file is missing.
    """
    p = Path(path) if path is not None else DEFAULT_PATH
    if not p.exists():
        return {"ok": False, "mate": target_mate, "operative": None, "rows": [],
                "malformed": [{"line": 0, "reason": f"steer channel not found: {p}"}], "n_seen": 0}

    applicable: list[tuple[datetime, int, dict[str, Any]]] = []
    malformed: list[dict[str, Any]] = []
    n_seen = 0

    for lineno, line in enumerate(p.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue  # header comment rows are part of the file contract (spec: Activation)
        try:
            row = json.loads(stripped)
        except json.JSONDecodeError as exc:
            malformed.append({"line": lineno, "reason": f"unparseable JSON: {exc.msg}"})
            continue
        if not isinstance(row, dict):
            malformed.append({"line": lineno, "reason": "row is not a JSON object"})
            continue
        missing = [f for f in REQUIRED_FIELDS if not isinstance(row.get(f), str) or not row.get(f)]
        if missing:
            malformed.append({"line": lineno, "reason": f"missing/empty required field(s): {', '.join(missing)}"})
            continue
        ts = _parse_ts(row["ts"])
        if ts is None:
            malformed.append({"line": lineno, "reason": f"ts is not ISO-8601: {row['ts']!r}"})
            continue
        if row["mate"] == "all" or row["mate"] == target_mate:
            applicable.append((ts, lineno, _classify(row)))
        n_seen += 1

    if malformed:  # fail loud: the leave protocol log consumes stderr (spec: VALIDATION)
        for bad in malformed:
            print(f"[steer_read] WARN malformed row line {bad['line']}: {bad['reason']}", file=sys.stderr)

    applicable.sort(key=lambda t: (t[0], t[1]))  # latest wins; file order breaks ts ties
    rows = [r for _, _, r in applicable]
    return {
        "ok": True,
        "mate": target_mate,
        "operative": rows[-1] if rows else None,
        "rows": rows,
        "malformed": malformed,
        "n_seen": n_seen,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: python tools/steer_read.py <mate-id>", file=sys.stderr)
        return 2
    result = read(argv[1])
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] and not result["malformed"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
