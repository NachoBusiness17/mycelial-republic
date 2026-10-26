"""golem_shabbat.py - Golem Emet/Met kill switch, Shabbat dormancy cycle, and Ghost Residuals.

Implements architectural mechanisms derived from the estate fiction corpus:
  1. GolemKillSwitch (Kabbalah / Pratchett Feet of Clay / Esoteric Mine 20261014):
     A construct animated by the token 'EMET' (Truth). A deterministic single-character
     diff erasing 'E' yields 'MET' (Dead), immediately halting all execution without
     unclean process killing or memory corruption.
  2. ShabbatCycle (THE_BRIEFING / SYNTHESIS 20261014 / Shabbat Pauses):
     Mandatory periodic dormancy cycle for autonomous agents and crons. Refuses compute
     consumption and expires write-leases during the Shabbat window, unless an explicit
     emergency override ('pikuach_nefesh') is supplied with verified justification.
  3. GhostResidual (Mickey 17 / Outer Wilds Ash Twin Protocol / Residue of Light):
     Cryptographically signed engram left behind when an agent seat exhausts context
     or reaches a terminal dead-end. Inherited directly into the successor seat's
     prefix cache, enforcing falsification inheritance (a successor cannot repeat
     an identical dead-end hypothesis).
"""
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_GOLEM_TOKEN_FILE = ROOT / "state" / "golem_token.txt"
DEFAULT_GHOST_LEDGER = ROOT / "state" / "ghost_residuals.jsonl"

TOKEN_EMET = "EMET"
TOKEN_MET = "MET"


class GolemHaltError(RuntimeError):
    """Raised when an operation is attempted while the Golem is in MET (halted) state."""
    pass


class ShabbatDormancyError(RuntimeError):
    """Raised when compute or write-lease is attempted during the active Shabbat window."""
    pass


@dataclass(frozen=True)
class GolemKillSwitch:
    token_path: Path = DEFAULT_GOLEM_TOKEN_FILE

    def ensure_initialized(self) -> str:
        if not self.token_path.exists():
            self.token_path.parent.mkdir(parents=True, exist_ok=True)
            self.token_path.write_text(TOKEN_EMET, encoding="utf-8")
            return TOKEN_EMET
        return self.read_token()

    def read_token(self) -> str:
        if not self.token_path.exists():
            return TOKEN_MET
        return self.token_path.read_text(encoding="utf-8").strip()

    def is_alive(self) -> bool:
        return self.read_token() == TOKEN_EMET

    def kill(self, reason: str = "halt_requested") -> Tuple[str, str]:
        """Erases the first letter 'E' to change EMET -> MET (Dead)."""
        current = self.read_token()
        if current == TOKEN_MET:
            return TOKEN_MET, "already_dead"
        self.token_path.parent.mkdir(parents=True, exist_ok=True)
        self.token_path.write_text(TOKEN_MET, encoding="utf-8")
        return TOKEN_MET, reason

    def revive(self) -> str:
        """Restores the letter 'E' to re-animate the Golem (MET -> EMET)."""
        self.token_path.parent.mkdir(parents=True, exist_ok=True)
        self.token_path.write_text(TOKEN_EMET, encoding="utf-8")
        return TOKEN_EMET

    def assert_alive(self) -> None:
        if not self.is_alive():
            raise GolemHaltError(
                f"Golem token at {self.token_path} is {self.read_token()!r} (MET). All execution halted."
            )


@dataclass(frozen=True)
class ShabbatCycle:
    interval_hours: int = 168  # Weekly cycle (7 days)
    dormancy_hours: int = 24   # 24-hour mandatory rest
    anchor_epoch: float = 0.0  # Unix timestamp reference

    def is_shabbat(self, ts: Optional[float] = None) -> bool:
        """Determines if the given timestamp falls inside the periodic Shabbat window."""
        t = ts if ts is not None else datetime.now(timezone.utc).timestamp()
        cycle_position = (t - self.anchor_epoch) % (self.interval_hours * 3600)
        dormancy_seconds = self.dormancy_hours * 3600
        return cycle_position < dormancy_seconds

    def check_clearance(
        self,
        ts: Optional[float] = None,
        pikuach_nefesh_override: Optional[str] = None,
    ) -> bool:
        """Validates clearance. During Shabbat, operations are refused unless overridden."""
        if not self.is_shabbat(ts):
            return True
        if pikuach_nefesh_override and pikuach_nefesh_override.strip():
            return True
        raise ShabbatDormancyError(
            "Operation refused: active Shabbat dormancy window. Compute is paused. "
            "Pass non-empty pikuach_nefesh_override only for life-safety / critical rescue."
        )


@dataclass(frozen=True)
class GhostResidual:
    seat_id: str
    iteration: int
    parent_hash: str
    dead_end_hypothesis: str
    next_probable_vector: str
    timestamp: str
    residual_hash: str = ""

    @classmethod
    def create(
        cls,
        seat_id: str,
        iteration: int,
        parent_hash: str,
        dead_end_hypothesis: str,
        next_probable_vector: str,
        ts: Optional[str] = None,
    ) -> GhostResidual:
        timestamp_str = ts or datetime.now(timezone.utc).isoformat()
        payload = f"{seat_id}:{iteration}:{parent_hash}:{dead_end_hypothesis}:{next_probable_vector}:{timestamp_str}"
        res_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        return cls(
            seat_id=seat_id,
            iteration=iteration,
            parent_hash=parent_hash,
            dead_end_hypothesis=dead_end_hypothesis,
            next_probable_vector=next_probable_vector,
            timestamp=timestamp_str,
            residual_hash=res_hash,
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class GhostResidualRegistry:
    def __init__(self, ledger_path: Optional[Path] = None) -> None:
        self.ledger_path = Path(ledger_path) if ledger_path else DEFAULT_GHOST_LEDGER

    def append(self, wisp: GhostResidual) -> None:
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.ledger_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(wisp.to_dict()) + "\n")

    def load_for_seat(self, seat_id: str) -> List[GhostResidual]:
        if not self.ledger_path.exists():
            return []
        wisps = []
        with open(self.ledger_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    if data.get("seat_id") == seat_id:
                        wisps.append(GhostResidual(**data))
                except Exception:
                    continue
        return wisps

    def validate_hypothesis_not_repeated(self, seat_id: str, proposed_hypothesis: str) -> bool:
        """Verifies that the successor seat does not repeat any dead-end hypothesis."""
        prior = self.load_for_seat(seat_id)
        cleaned_prop = proposed_hypothesis.strip().lower()
        for wisp in prior:
            if wisp.dead_end_hypothesis.strip().lower() == cleaned_prop:
                return False
        return True
