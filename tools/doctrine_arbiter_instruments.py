"""Instrument adapters for the doctrine arbiter (R10, 2026-09-30).

One read-only measurer per estate instrument the arbiter can query; the
metric tables and selector contracts live in tools/doctrine_arbiter_core.py
(the arbiter's spec). Laws that live here:

  - InstrumentError means the SURFACE is dark (missing stream, unreadable
    file): an incident, exit 2. It is distinct from returning None/None-
    valued metric, which means no data yet: the prediction has merely not
    materialized (stays PENDING, or EXPIRES at its deadline).
  - Every measurer is read-only against the estate.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Optional

ROOT = Path(__file__).resolve().parents[1]

GPS_DB_PATH = ROOT / "tools" / "gps_mcp" / "gps_ledger.db3"
DUELS_PATH = ROOT / "logs" / "duel" / "duels.jsonl"
PARITY_LATEST_PATH = ROOT / "tools" / "rule_parity_out" / "latest.json"


class InstrumentError(Exception):
    """The instrument surface itself is dark (missing stream, unreadable)."""


@dataclass
class InstrumentPaths:
    """Every instrument surface, injectable for tests/frozen fixtures."""

    gps_db: Path = GPS_DB_PATH
    duels: Path = DUELS_PATH
    parity_latest: Path = PARITY_LATEST_PATH
    anomaly_steps: Optional[Path] = None   # None = anomaly_flagger defaults
    anomaly_oral: Optional[Path] = None
    anomaly_ledger: Optional[Path] = None
    anomaly_enum_map: Optional[Path] = None


def measure_gps_ledger(selector: dict[str, Any], paths: InstrumentPaths
                       ) -> Optional[dict[str, Any]]:
    if not paths.gps_db.exists():
        raise InstrumentError(f"gps ledger db missing: {paths.gps_db}")
    from tools.gps_mcp.ledger import CapabilityLedger  # lazy: sqlite only here
    ledger = CapabilityLedger(paths.gps_db)
    try:
        rate = ledger.get_rate(selector["model_id"], selector["task_shape"])
    finally:
        ledger.close()
    if rate is None:
        return None  # pair never measured: no data, not an error
    return {"pass_rate": rate[0], "sample_size": rate[1]}


def measure_duel_table(selector: dict[str, Any], paths: InstrumentPaths
                       ) -> Optional[dict[str, Any]]:
    if not paths.duels.exists():
        raise InstrumentError(f"duel ledger missing: {paths.duels}")
    model = selector["model"]
    wins = decided = ties = 0
    seen_any = False
    with paths.duels.open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped:
                continue
            try:
                row = json.loads(stripped)
            except json.JSONDecodeError:
                continue
            seen_any = True
            winner = row.get("winner")
            a_model, b_model = row.get("a_model"), row.get("b_model")
            if winner == "TIE" and model in (a_model, b_model):
                ties += 1
                continue
            if winner not in ("A", "B"):
                continue  # UNPARSED etc: not evidence about either side
            if a_model == model:
                decided += 1
                wins += 1 if winner == "A" else 0
            elif b_model == model:
                decided += 1
                wins += 1 if winner == "B" else 0
    # no decided duels -> win_rate undefined (no data), but the raw counts
    # are real and checkable (decided == 0 is a claim a prediction may
    # legitimately make). v0 counts every ledger row incl. altjudge rows.
    return {"decided": decided, "ties": ties,
            "win_rate": None if not seen_any or decided == 0 else wins / decided}


def measure_parity_gate(selector: dict[str, Any], paths: InstrumentPaths
                        ) -> Optional[dict[str, Any]]:
    if not paths.parity_latest.exists():
        raise InstrumentError(f"parity latest.json missing: {paths.parity_latest}")
    doc = json.loads(paths.parity_latest.read_text(encoding="utf-8"))
    if "mode" in selector and doc.get("mode") != selector["mode"]:
        return None  # wrong profile for the claim: no data, not an error
    per_family = doc.get("per_family") or {}
    diverged = sum(int(f.get("diverged_seqs") or 0) for f in per_family.values())
    return {"parity_ok": bool(doc.get("parity")), "diverged_seqs": diverged}


def measure_anomaly_counts(selector: dict[str, Any], paths: InstrumentPaths
                           ) -> Optional[dict[str, Any]]:
    import tools.anomaly_flagger as af  # lazy: sibling tool, own imports

    steps = Path(paths.anomaly_steps or af.STEPS_PATH)
    oral = Path(paths.anomaly_oral or af.ORAL_PATH)
    ledger = Path(paths.anomaly_ledger or af.LEDGER_PATH)
    enum_map = Path(paths.anomaly_enum_map or af.ENUM_MAP_PATH)
    for name, path in (("steps", steps), ("oral_law_index", oral),
                       ("burns_ledger", ledger), ("burns_enum_map", enum_map)):
        if not path.exists():
            raise InstrumentError(f"anomaly surface missing: {name} at {path}")
    findings: list["af.Finding"] = []
    findings.extend(af.scan_steps(steps)[0])
    findings.extend(af.scan_oral(oral)[0])
    findings.extend(af.scan_burns(ledger, enum_map)[0])
    surface = selector.get("surface")
    if surface:
        findings = [f for f in findings if f.surface == surface]
    # The unit is the anomalous ROW (named rows are the flagger's own
    # contract), not the anomaly class: two bad rows in one class is a
    # worse world than one row in two classes.
    return {"anomaly_count": sum(len(f.rows) for f in findings if f.anomaly)}


MEASURERS: dict[str, Callable[[dict[str, Any], InstrumentPaths],
                              Optional[dict[str, Any]]]] = {
    "gps_ledger": measure_gps_ledger,
    "duel_table": measure_duel_table,
    "parity_gate": measure_parity_gate,
    "anomaly_counts": measure_anomaly_counts,
}
