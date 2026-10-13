#!/usr/bin/env python3
"""lane_budget.py - pre-bound metered budgets that HALT a running lane.

Mechanism 1 of the two the estate lacks (S22 orb-lane spec, wave ledger
watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md S22, agent c254b1ce):
"(a) pre-bound metered budgets that HALT a running lane (we only have
post-hoc billing receipts)". mag/lane_effort.py still only DECIDES which
budget shape a width deserves; nothing at runtime ever stops a lane that
outspends it. This module is that missing runtime half: lanes wrap their
work in a Budget and every .spend() is checked against caps bound BEFORE
the work starts (pre-bound = the lane cannot raise its own ceiling).

Contract (W3 lane ask, 2026-09-29):
  Budget(name, max_actions, max_seconds, max_usd_estimate)
  .spend(n=1, seconds=, usd=)  -> raises BudgetExhausted; BEFORE raising it
      appends a death receipt row {lane, reason, spent, ts} to
      logs/lane_budget/deaths.jsonl (one row per death, not per raise:
      one corpse, one epitaph - the Mickey17 law, deaths teach).
  context manager               -> on exit writes a checkpoint so a resumed
      lane inherits the REMAINING budget, not a fresh one.
  no budget = UNMETERED (explicit). The lane that wants no ceiling says so
      in code by wrapping UNMETERED; the choice is auditable, never an
      accident of a missing argument.

Time is metered on the wall clock (auto-stop, the S22 "auto-stop" clause):
elapsed since budget start counts toward max_seconds with no caller action;
the seconds= argument exists for work time NOT already on the lane's own
wall clock (e.g. a child lane's reported time) - passing your own elapsed
wall time would double-count and is a misuse.

Cap semantics: reaching a cap exactly on a legal spend is allowed; the
spend that pushes a dimension strictly past its cap is the fatal one.
Checked in order actions -> seconds -> usd; the first tripped dimension is
the death reason. None caps that dimension (a Budget of all-None caps is
an explicit meter-that-never-halts; UNMETERED is no meter at all).

Fail shape: the halt is the enforcement and always happens; if the death
receipt cannot be written the OSError chains into the BudgetExhausted so
the loss is visible, never swallowed.

Usage:
    from tools.lane_budget import Budget, BudgetExhausted, UNMETERED

    with Budget("steal-mine-7", max_actions=200, max_seconds=3600,
                max_usd_estimate=0.80) as budget:
        for item in work:
            budget.spend(n=1, usd=0.004)
            ...  # BudgetExhausted halts the lane; receipt already on disk

    # next window: the resumed lane inherits what was left
    with Budget.resume(checkpoint_path) as budget:
        ...

Schema: lane_budget.v1
"""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

SCHEMA = "lane_budget.v1"

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DEATHS_PATH = REPO_ROOT / "logs" / "lane_budget" / "deaths.jsonl"
DEFAULT_CHECKPOINT_DIR = REPO_ROOT / "logs" / "lane_budget" / "checkpoints"

# Order is the death-reason priority; first tripped dimension names the death.
_DIMENSIONS = ("actions", "seconds", "usd_estimate")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class BudgetExhausted(RuntimeError):
    """A pre-bound cap was overspent; the lane must halt, not trim.

    Carries .budget_name, .reason (the tripped dimension) and .spent (the
    fatal totals, identical to the death-receipt row's spent dict) so a
    supervisor can log the halt without re-reading deaths.jsonl.
    """

    def __init__(self, budget_name: str, reason: str, spent: dict[str, float]):
        super().__init__(
            f"lane {budget_name!r} exhausted its pre-bound {reason} budget "
            f"(spent {spent})"
        )
        self.budget_name = budget_name
        self.reason = reason
        self.spent = spent


class Budget:
    """Pre-bound, metered, halting budget for one lane run.

    max_actions / max_seconds / max_usd_estimate are bound at construction
    (pre-bound); None leaves that dimension uncapped. deaths_path and
    checkpoint_path are injectable for tests; production lanes use the
    repo defaults so every death lands in one auditable file.
    """

    def __init__(
        self,
        name: str,
        max_actions: Optional[int] = None,
        max_seconds: Optional[float] = None,
        max_usd_estimate: Optional[float] = None,
        *,
        deaths_path: Optional[Path] = None,
        checkpoint_path: Optional[Path] = None,
    ) -> None:
        self.name = name
        self.max_actions = max_actions
        self.max_seconds = max_seconds
        self.max_usd_estimate = max_usd_estimate
        self.deaths_path = Path(deaths_path) if deaths_path else DEFAULT_DEATHS_PATH
        self.checkpoint_path = (
            Path(checkpoint_path)
            if checkpoint_path
            else DEFAULT_CHECKPOINT_DIR / f"{_safe_name(name)}.json"
        )
        self._actions = 0
        self._seconds = 0.0  # caller-reported work time (not our wall clock)
        self._usd = 0.0
        self._t0 = time.monotonic()
        self._dead = False  # one corpse, one epitaph: receipt written once

    # -- metering ------------------------------------------------------------

    def spent(self) -> dict[str, float]:
        """Totals including wall-clock elapsed (the honest current spend)."""
        return {
            "actions": self._actions,
            "seconds": round(self._seconds + self._wall_elapsed(), 6),
            "usd_estimate": round(self._usd, 6),
        }

    def remaining(self) -> dict[str, Optional[float]]:
        """Remaining headroom per dimension; None = uncapped."""
        s = self.spent()
        return {
            "actions": (
                self.max_actions - s["actions"]
                if self.max_actions is not None
                else None
            ),
            "seconds": (
                round(self.max_seconds - s["seconds"], 6)
                if self.max_seconds is not None
                else None
            ),
            "usd_estimate": (
                round(self.max_usd_estimate - s["usd_estimate"], 6)
                if self.max_usd_estimate is not None
                else None
            ),
        }

    def _wall_elapsed(self) -> float:
        return time.monotonic() - self._t0

    def spend(
        self,
        n: int = 1,
        seconds: float = 0.0,
        usd: float = 0.0,
    ) -> dict[str, float]:
        """Meter work against the pre-bound caps; halt (raise) on overdraft.

        The spend is applied first (the fatal action IS spent), then each
        capped dimension is checked in _DIMENSIONS order. On the first
        tripped dimension the death receipt is written to deaths.jsonl
        BEFORE BudgetExhausted raises. Re-spending a dead budget re-raises
        without a second receipt row.
        """
        self._actions += n
        self._seconds += seconds
        self._usd += usd
        totals = self.spent()
        caps = {
            "actions": self.max_actions,
            "seconds": self.max_seconds,
            "usd_estimate": self.max_usd_estimate,
        }
        for dim in _DIMENSIONS:
            cap = caps[dim]
            if cap is not None and totals[dim] > cap:
                if not self._dead:
                    self._write_death_receipt(dim, totals)
                    self._dead = True
                raise BudgetExhausted(self.name, dim, totals)
        return totals

    # -- death receipt + checkpoint -------------------------------------------

    def _write_death_receipt(self, reason: str, spent: dict[str, float]) -> None:
        # Exactly the four contract keys: {lane, reason, spent, ts}.
        row = {
            "lane": self.name,
            "reason": reason,
            "spent": spent,
            "ts": _utc_now(),
        }
        self.deaths_path.parent.mkdir(parents=True, exist_ok=True)
        with self.deaths_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, sort_keys=True) + "\n")

    def checkpoint(self) -> Path:
        """Persist the budget state so a resumed lane inherits the remainder."""
        state = {
            "schema": SCHEMA,
            "name": self.name,
            "caps": {
                "max_actions": self.max_actions,
                "max_seconds": self.max_seconds,
                "max_usd_estimate": self.max_usd_estimate,
            },
            "spent": self.spent(),
            "dead": self._dead,
            "ts": _utc_now(),
        }
        self.checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
        self.checkpoint_path.write_text(
            json.dumps(state, indent=2, sort_keys=True), encoding="utf-8"
        )
        return self.checkpoint_path

    @classmethod
    def resume(cls, checkpoint_path: Path, **overrides: Any) -> "Budget":
        """Rebuild a Budget from a checkpoint; spent carries over verbatim.

        Caps come from the checkpoint (pre-bound law: the lane itself
        cannot re-raise them); keyword overrides exist for the paths and
        for an operator re-bind, which is a supervisor action, not a lane
        action. Wall-clock timing restarts at resume, so checkpointed
        elapsed seconds are folded into the carried spend exactly once.
        """
        state = json.loads(Path(checkpoint_path).read_text(encoding="utf-8"))
        if state.get("schema") != SCHEMA:
            raise ValueError(
                f"checkpoint {checkpoint_path} is schema {state.get('schema')!r}, "
                f"not {SCHEMA!r}"
            )
        budget = cls(
            state["name"],
            state["caps"]["max_actions"],
            state["caps"]["max_seconds"],
            state["caps"]["max_usd_estimate"],
            **overrides,
        )
        budget._actions = int(state["spent"]["actions"])
        budget._seconds = float(state["spent"]["seconds"])
        budget._usd = float(state["spent"]["usd_estimate"])
        budget._dead = bool(state.get("dead", False))
        return budget

    # -- context manager -------------------------------------------------------

    def __enter__(self) -> "Budget":
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> bool:
        # Always checkpoint (checkpointed sleep state, S22): a clean exit
        # banks the remainder for the next window; an exhausted exit banks
        # a dead state a resume will refuse to launder. Never swallow.
        self.checkpoint()
        return False


class _Unmetered:
    """The explicit no-budget: same surface, no ceiling, no writes.

    Lanes that opt out of metering must wrap UNMETERED so the choice is a
    visible token in code (and greppable in reviews), never an accident of
    a missing argument. spend() accepts and records nothing.
    """

    name = "UNMETERED"

    def spend(self, n: int = 1, seconds: float = 0.0, usd: float = 0.0) -> None:
        return None

    def spent(self) -> dict[str, None]:
        return {"actions": None, "seconds": None, "usd_estimate": None}

    def remaining(self) -> dict[str, None]:
        return {"actions": None, "seconds": None, "usd_estimate": None}

    def checkpoint(self) -> None:
        return None

    def __enter__(self) -> "_Unmetered":
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> bool:
        return False


UNMETERED = _Unmetered()


def _safe_name(name: str) -> str:
    return "".join(c if c.isalnum() or c in "-_." else "_" for c in name)


if __name__ == "__main__":  # smoke: python tools/lane_budget.py
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        demo = Budget(
            "smoke",
            max_actions=2,
            deaths_path=td_path / "deaths.jsonl",
            checkpoint_path=td_path / "ckpt.json",
        )
        with demo as b:
            b.spend()
            b.spend()
            try:
                b.spend()
            except BudgetExhausted as ex:
                print(f"halted: {ex}")
        print(f"receipt: {(td_path / 'deaths.jsonl').read_text().strip()}")
        revived = Budget.resume(td_path / "ckpt.json")
        print(f"resumed remaining: {revived.remaining()}")
