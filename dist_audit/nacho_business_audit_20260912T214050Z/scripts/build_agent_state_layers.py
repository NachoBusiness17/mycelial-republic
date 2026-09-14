"""Map existing agent-state evidence into its recovery strata.

This is a read-only projection, not ``chain.v2`` and not a repair.  It makes
the already-existing levels explicit for cold boot and elder review:

L0 viewport   = LATEST (what a seat loads first)
L1 continuity = recent chain rows (what can be followed without full history)
L2 history    = the append-only parsed chain + version files
L3 evidence   = malformed physical rows and unreferenced version files

No row is reparented, deleted, renamed, or redirected.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mag import agent_state as ast  # noqa: E402

SCHEMA = "agent_state_layers.v1"
DEFAULT_OUT = ROOT / "memory/runs/verkle_recovery/agent_state_layers_20260902.json"


def _load_rows() -> tuple[list[dict], int]:
    rows: list[dict] = []
    malformed = 0
    if not ast.CHAIN.is_file():
        return rows, malformed
    for line in ast.CHAIN.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            malformed += 1
            continue
        if isinstance(value, dict):
            rows.append(value)
        else:
            malformed += 1
    return rows, malformed


def _commit_hex(row: dict, key: str) -> str:
    value = row.get(key)
    if isinstance(value, dict):
        return str(value.get("hex") or "")
    return str(value or "")


def build(*, recent: int = 256) -> dict:
    rows, malformed = _load_rows()
    recent_rows = rows[-max(1, int(recent)):]
    continuity_breaks = 0
    for left, right in zip(recent_rows, recent_rows[1:]):
        if _commit_hex(right, "parent_commit") != _commit_hex(left, "content_commit"):
            continuity_breaks += 1
    chain_names = {str(row.get("filename") or "") for row in rows if row.get("filename")}
    version_names = {p.name for p in ast.VERSIONS.glob("*.json")} if ast.VERSIONS.is_dir() else set()
    return {
        "ok": True,
        "schema": SCHEMA,
        "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_of_truth": "existing agent_state viewport/history/evidence; projection only",
        "layers": {
            "L0_viewport": {
                "path": "memory/agent_state/LATEST.json",
                "exists": ast.LATEST_JSON.is_file(),
                "content_commit": ((ast.load_latest() or {}).get("content_commit") or {}).get("hex"),
            },
            "L1_continuity": {
                "path": "memory/agent_state/chain.jsonl",
                "window_rows": len(recent_rows),
                "window_parent_breaks": continuity_breaks,
                "note": "recent navigation aid; does not assert the whole chain is linear",
            },
            "L2_history": {
                "chain_rows": len(rows),
                "version_files": len(version_names),
                "chain_filenames": len(chain_names),
                "missing_version_files": len(chain_names - version_names),
            },
            "L3_evidence": {
                "malformed_physical_rows": malformed,
                "unreferenced_version_files": len(version_names - chain_names),
                "policy": "preserve for review; never silently fold into L0",
            },
        },
        "repair_policy": "derive and review; preserve the legacy chain and existing commitments",
    }


def main() -> int:
    result = build()
    DEFAULT_OUT.parent.mkdir(parents=True, exist_ok=True)
    tmp = DEFAULT_OUT.with_suffix(".tmp")
    tmp.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    tmp.replace(DEFAULT_OUT)
    result["output"] = str(DEFAULT_OUT)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
