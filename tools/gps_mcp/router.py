"""The gps-mcp router: ask() and cascade() over measured capability.

Routing rules, in priority order (from the spec):
  (a) hard constraints filter (max_cost_usd, max_latency_ms)
  (b) measured pass-rate from the ledger (default threshold 0.85,
      caller-overridable via constraints.pass_rate_threshold)
  (c) cost (cheapest qualifying candidate wins; ties broken by tier
      rank then model_id for determinism)
  (d) calibrated confidence of the candidate's own output, when the
      endpoint provides probabilities: recorded on every ask receipt,
      and the escalation trigger inside cascade()

Exploration rule: a task shape with NO ledger history routes to the
designated mid-tier exploration model with exploration: true.

Every routing decision (including no-route outcomes and every cascade
attempt) emits one append-only JSONL receipt row:
  {ts, task_shape, chosen, considered, reasons, cost_usd, confidence,
   exploration}
Cascade rows add trace_id and cascade_step so attempts group cleanly.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from .ledger import CapabilityLedger
from .providers import (
    ProviderConfig,
    ProviderRegistry,
    ProviderResponse,
    call_provider,
)

DEFAULT_PASS_RATE_THRESHOLD = 0.85
DEFAULT_CASCADE_MIN_CONFIDENCE = 0.8
MAX_CASCADE_TIERS = 3

# Positive-arm tiebreaker (LM7, operator positive-steering law 2026-09-30):
# at similar measured pass_rate (both qualify, cost tied) RISING outranks
# STEADY/no-data, which outranks DECLINING. The AC10 lane-chooser law
# inverted toward momentum. No verdict history is neutral (rank 1), so the
# v0 cost-first behavior is byte-stable wherever the positive arm has no
# evidence to weigh in with.
MOMENTUM_RANK = {"RISING": 0, "STEADY": 1, "DECLINING": 2}

RECEIPT_REQUIRED_KEYS = (
    "ts",
    "task_shape",
    "chosen",
    "considered",
    "reasons",
    "cost_usd",
    "confidence",
    "exploration",
)


@dataclass
class Constraints:
    max_cost_usd: Optional[float] = None
    max_latency_ms: Optional[int] = None
    min_confidence: Optional[float] = None
    pass_rate_threshold: float = DEFAULT_PASS_RATE_THRESHOLD

    @classmethod
    def from_dict(cls, raw: Optional[dict[str, Any]]) -> "Constraints":
        raw = raw or {}
        known = {k: v for k, v in raw.items() if v is not None}
        return cls(
            max_cost_usd=known.get("max_cost_usd"),
            max_latency_ms=known.get("max_latency_ms"),
            min_confidence=known.get("min_confidence"),
            pass_rate_threshold=float(
                known.get("pass_rate_threshold", DEFAULT_PASS_RATE_THRESHOLD)
            ),
        )


@dataclass
class Candidate:
    """One provider evaluated against one ask: the 'considered' row."""

    model_id: str
    tier: str
    cost_usd_per_call: float
    latency_ms: int
    pass_rate: Optional[float]
    sample_size: int
    passes_constraints: bool
    passes_threshold: bool
    momentum_badge: Optional[str] = None  # RISING/STEADY/DECLINING or None

    def as_dict(self) -> dict[str, Any]:
        return {
            "model_id": self.model_id,
            "tier": self.tier,
            "cost_usd_per_call": self.cost_usd_per_call,
            "latency_ms": self.latency_ms,
            "pass_rate": self.pass_rate,
            "sample_size": self.sample_size,
            "passes_constraints": self.passes_constraints,
            "passes_threshold": self.passes_threshold,
            "momentum_badge": self.momentum_badge,
        }


@dataclass
class Decision:
    task_shape: str
    chosen: Optional[str]
    response: Optional[ProviderResponse]
    considered: list[dict[str, Any]]
    reasons: list[str]
    exploration: bool
    receipt: dict[str, Any]

    @property
    def answer(self) -> Optional[str]:
        return None if self.response is None else self.response.answer

    @property
    def confidence(self) -> Optional[float]:
        return None if self.response is None else self.response.confidence

    @property
    def cost_usd(self) -> float:
        return 0.0 if self.response is None else self.response.cost_usd

    def as_dict(self) -> dict[str, Any]:
        return {
            "task_shape": self.task_shape,
            "chosen": self.chosen,
            "answer": self.answer,
            "confidence": self.confidence,
            "cost_usd": self.cost_usd,
            "considered": self.considered,
            "reasons": self.reasons,
            "exploration": self.exploration,
            "receipt": self.receipt,
        }


@dataclass
class CascadeAttempt:
    step: int
    tier: str
    model_id: str
    confidence: Optional[float]
    cost_usd: float
    reason: str
    answer: str
    escalated: bool

    def as_dict(self) -> dict[str, Any]:
        return {
            "step": self.step,
            "tier": self.tier,
            "model_id": self.model_id,
            "confidence": self.confidence,
            "cost_usd": self.cost_usd,
            "reason": self.reason,
            "answer": self.answer,
            "escalated": self.escalated,
        }


@dataclass
class CascadeResult:
    task_shape: str
    attempts: list[CascadeAttempt] = field(default_factory=list)
    stopped_because: str = ""
    exploration: bool = False

    @property
    def total_cost_usd(self) -> float:
        return round(sum(a.cost_usd for a in self.attempts), 10)

    @property
    def final(self) -> Optional[CascadeAttempt]:
        return self.attempts[-1] if self.attempts else None

    def as_dict(self) -> dict[str, Any]:
        return {
            "task_shape": self.task_shape,
            "attempts": [a.as_dict() for a in self.attempts],
            "tiers_tried": [a.tier for a in self.attempts],
            "total_cost_usd": self.total_cost_usd,
            "final_answer": None if self.final is None else self.final.answer,
            "final_confidence": None if self.final is None else self.final.confidence,
            "stopped_because": self.stopped_because,
            "exploration": self.exploration,
        }


class ReceiptLog:
    """Append-only JSONL receipts. A decision we cannot audit did not happen."""

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def emit(self, row: dict[str, Any]) -> dict[str, Any]:
        ordered = {key: row.get(key) for key in RECEIPT_REQUIRED_KEYS}
        for key, value in row.items():
            if key not in ordered:
                ordered[key] = value
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(ordered, sort_keys=False) + "\n")
        return ordered

    def rows(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        out = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                out.append(json.loads(line))
        return out


class Router:
    def __init__(self, registry: ProviderRegistry, ledger: CapabilityLedger,
                 receipts_path: str | Path):
        self.registry = registry
        self.ledger = ledger
        self.receipts = ReceiptLog(receipts_path)

    # -- selection (rules a, b, c) ------------------------------------------

    def _evaluate(self, task_shape: str, constraints: Constraints) -> list[Candidate]:
        candidates: list[Candidate] = []
        for p in self.registry.all():
            passes_constraints = True
            if constraints.max_cost_usd is not None:
                if p.cost_usd_per_call > constraints.max_cost_usd:
                    passes_constraints = False
            if constraints.max_latency_ms is not None:
                if p.latency_ms > constraints.max_latency_ms:
                    passes_constraints = False
            rate = self.ledger.get_rate(p.model_id, task_shape)
            momentum_badge: Optional[str] = None
            if rate is None:
                pass_rate: Optional[float] = None
                sample_size = 0
                passes_threshold = False
            else:
                pass_rate, sample_size = rate
                passes_threshold = pass_rate >= constraints.pass_rate_threshold
                mom = self.ledger.momentum(p.model_id, task_shape)
                momentum_badge = None if mom is None else mom.badge
            candidates.append(
                Candidate(
                    model_id=p.model_id,
                    tier=p.tier,
                    cost_usd_per_call=p.cost_usd_per_call,
                    latency_ms=p.latency_ms,
                    pass_rate=pass_rate,
                    sample_size=sample_size,
                    passes_constraints=passes_constraints,
                    passes_threshold=passes_threshold,
                    momentum_badge=momentum_badge,
                )
            )
        return candidates

    def _select(
        self, task_shape: str, constraints: Constraints
    ) -> tuple[Optional[ProviderConfig], list[dict[str, Any]], list[str], bool]:
        """Return (chosen_provider, considered, reasons, exploration)."""
        candidates = self._evaluate(task_shape, constraints)
        considered = [c.as_dict() for c in candidates]
        reasons: list[str] = []
        by_id = {c.model_id: c for c in candidates}
        eligible = [c for c in candidates if c.passes_constraints]

        def mrank(c: Candidate) -> int:
            if c.momentum_badge is None:
                return MOMENTUM_RANK["STEADY"]  # no verdict history is neutral
            return MOMENTUM_RANK[c.momentum_badge]

        def cheapest(cs: list[Candidate]) -> Candidate:
            return min(
                cs,
                key=lambda c: (
                    c.cost_usd_per_call,
                    mrank(c),
                    self.registry.tier_rank(c.tier),
                    c.model_id,
                ),
            )

        def momentum_reasons(pick: Candidate, pool: list[Candidate]) -> list[str]:
            # The tiebreak is only narrated when it actually outranked a
            # cost-tied peer: silent reordering is unauditable reordering.
            outranked = sorted(
                c.model_id
                for c in pool
                if c.model_id != pick.model_id
                and c.cost_usd_per_call == pick.cost_usd_per_call
                and mrank(c) > mrank(pick)
            )
            if not outranked:
                return []
            return [
                f"momentum tiebreak at equal cost: {pick.model_id}"
                f" ({pick.momentum_badge}) outranks {', '.join(outranked)}"
                f" on verdict-window momentum"
            ]

        if not self.ledger.task_shape_has_history(task_shape):
            exploration_pick = by_id.get(self.registry.exploration_model)
            if exploration_pick is not None and exploration_pick.passes_constraints:
                reasons.append(
                    f"no ledger history for task shape; exploration route to"
                    f" designated mid tier {self.registry.exploration_model}"
                )
                return self.registry.get(exploration_pick.model_id), considered, reasons, True
            if eligible:
                pick = cheapest(eligible)
                reasons.append(
                    "no ledger history and exploration model blocked by constraints;"
                    " cheapest constraint-passing fallback"
                )
                return self.registry.get(pick.model_id), considered, reasons, True
            reasons.append(
                "no ledger history, exploration model blocked by constraints,"
                " and no provider passes constraints"
            )
            return None, considered, reasons, True

        qualifying = [c for c in eligible if c.passes_threshold]
        if qualifying:
            pick = cheapest(qualifying)
            reasons.append(
                f"{len(qualifying)} candidate(s) pass constraints and pass-rate"
                f" threshold {constraints.pass_rate_threshold}; cheapest wins"
            )
            reasons.extend(momentum_reasons(pick, qualifying))
            return self.registry.get(pick.model_id), considered, reasons, False
        if eligible:
            pick = cheapest(eligible)
            reasons.append(
                f"no candidate meets pass-rate threshold"
                f" {constraints.pass_rate_threshold}; cheapest constraint-passing"
                f" fallback ({pick.model_id} at {pick.pass_rate})"
            )
            reasons.extend(momentum_reasons(pick, eligible))
            return self.registry.get(pick.model_id), considered, reasons, False
        reasons.append("no provider passes the hard constraints")
        return None, considered, reasons, False

    # -- ask ------------------------------------------------------------------

    def ask(
        self, task_shape: str, payload: Any,
        constraints: Constraints | dict[str, Any] | None = None,
    ) -> Decision:
        constraints = _coerce_constraints(constraints)
        chosen, considered, reasons, exploration = self._select(task_shape, constraints)
        ts = _utc_now_iso()
        if chosen is None:
            receipt = self.receipts.emit(
                {
                    "ts": ts,
                    "task_shape": task_shape,
                    "chosen": None,
                    "considered": considered,
                    "reasons": reasons,
                    "cost_usd": 0.0,
                    "confidence": None,
                    "exploration": exploration,
                }
            )
            return Decision(task_shape, None, None, considered, reasons, exploration, receipt)
        response = call_provider(chosen, task_shape, payload)
        reasons = list(reasons)
        if constraints.min_confidence is not None and response.confidence is not None:
            if response.confidence < constraints.min_confidence:
                reasons.append(
                    f"returned confidence {response.confidence} below min_confidence"
                    f" {constraints.min_confidence}; single-shot ask does not"
                    f" escalate, use cascade"
                )
        receipt = self.receipts.emit(
            {
                "ts": ts,
                "task_shape": task_shape,
                "chosen": chosen.model_id,
                "considered": considered,
                "reasons": reasons,
                "cost_usd": response.cost_usd,
                "confidence": response.confidence,
                "exploration": exploration,
            }
        )
        return Decision(
            task_shape, chosen.model_id, response, considered, reasons, exploration, receipt
        )

    # -- cascade ---------------------------------------------------------------

    def cascade(
        self, task_shape: str, payload: Any,
        constraints: Constraints | dict[str, Any] | None = None,
    ) -> CascadeResult:
        """Cheapest qualifying tier first; escalate one tier when the
        endpoint's returned confidence is below the caller threshold.
        Max three tiers. Prior answers attach as context. One receipt
        per attempt, all sharing a trace_id.
        """
        constraints = _coerce_constraints(constraints)
        min_conf = constraints.min_confidence
        if min_conf is None:
            min_conf = DEFAULT_CASCADE_MIN_CONFIDENCE
        result = CascadeResult(task_shape)
        chosen, considered, reasons, exploration = self._select(task_shape, constraints)
        result.exploration = exploration
        if chosen is None:
            ts = _utc_now_iso()
            trace_id = _trace_id(ts, task_shape)
            self.receipts.emit(
                {
                    "ts": ts,
                    "task_shape": task_shape,
                    "chosen": None,
                    "considered": considered,
                    "reasons": list(reasons) + ["cascade aborted: no starting candidate"],
                    "cost_usd": 0.0,
                    "confidence": None,
                    "exploration": exploration,
                    "trace_id": trace_id,
                    "cascade_step": 0,
                }
            )
            result.stopped_because = "no_starting_candidate"
            return result

        ts = _utc_now_iso()
        trace_id = _trace_id(ts, task_shape)
        current = chosen
        prior_answers: list[str] = []
        tried_models: set[str] = set()

        for step in range(MAX_CASCADE_TIERS):
            tried_models.add(current.model_id)
            response = call_provider(current, task_shape, payload, prior_answers)
            step_reasons = list(reasons) if step == 0 else [
                f"escalated from {result.attempts[-1].model_id}: confidence"
                f" {result.attempts[-1].confidence} below threshold {min_conf}"
            ]
            confident = response.confidence is not None and response.confidence >= min_conf
            if response.confidence is None:
                stop_reason = "endpoint provided no confidence signal; rule (d) not applicable"
            elif confident:
                stop_reason = f"confidence {response.confidence} meets threshold {min_conf}"
            else:
                stop_reason = ""
            self.receipts.emit(
                {
                    "ts": _utc_now_iso(),
                    "task_shape": task_shape,
                    "chosen": current.model_id,
                    "considered": considered,
                    "reasons": step_reasons,
                    "cost_usd": response.cost_usd,
                    "confidence": response.confidence,
                    "exploration": exploration and step == 0,
                    "trace_id": trace_id,
                    "cascade_step": step,
                }
            )
            result.attempts.append(
                CascadeAttempt(
                    step=step,
                    tier=current.tier,
                    model_id=current.model_id,
                    confidence=response.confidence,
                    cost_usd=response.cost_usd,
                    reason=stop_reason or "escalating",
                    answer=response.answer,
                    escalated=step > 0,
                )
            )
            if stop_reason:
                result.stopped_because = stop_reason
                return result
            if step + 1 >= MAX_CASCADE_TIERS:
                result.stopped_because = (
                    f"max {MAX_CASCADE_TIERS} tiers reached with confidence still"
                    f" below {min_conf}"
                )
                return result
            nxt = self._next_tier_candidate(
                current, task_shape, constraints, tried_models
            )
            if nxt is None:
                result.stopped_because = (
                    f"confidence below {min_conf} and no higher tier passes"
                    f" constraints/threshold"
                )
                return result
            prior_answers.append(response.answer)
            current = nxt
        return result

    def _next_tier_candidate(
        self,
        current: ProviderConfig,
        task_shape: str,
        constraints: Constraints,
        tried_models: set[str],
    ) -> Optional[ProviderConfig]:
        """Cheapest constraint-passing, threshold-qualifying provider in the
        next tier up. None when escalation is blocked (cost cap, tier
        exhausted, threshold miss)."""
        current_rank = self.registry.tier_rank(current.tier)
        for tier in self.registry.tier_order[current_rank + 1:]:
            tier_members = [
                p for p in self.registry.all()
                if p.tier == tier and p.model_id not in tried_models
            ]
            viable = []
            for p in tier_members:
                if constraints.max_cost_usd is not None:
                    if p.cost_usd_per_call > constraints.max_cost_usd:
                        continue
                if constraints.max_latency_ms is not None:
                    if p.latency_ms > constraints.max_latency_ms:
                        continue
                rate = self.ledger.get_rate(p.model_id, task_shape)
                if rate is None:
                    continue
                if rate[0] < constraints.pass_rate_threshold:
                    continue
                viable.append(p)
            if viable:
                return min(
                    viable,
                    key=lambda p: (p.cost_usd_per_call, p.model_id),
                )
        return None


# -- duel-bank wiring (D2 GPS_ROUTES, 2026-09-30) ---------------------------
#
# The duel harness (tools/duel_harness.py) banks one row per duel to
# logs/duel/duels.jsonl and its docstring promises those rows "feed the
# future gps router". This is that wire, landed from the router side so
# the fleet's own bank becomes the meter's fleet-wide table:
#
#   import_duel_bank()  duel rows -> record_verdict() per contender, one
#                       verdict per (duel, contender), evidence_hash =
#                       sha256 of the canonical banked row -- recomputed
#                       at append from the same canonical bytes (Q28
#                       evidence-resolution gate: the bytes ride the
#                       verdict_log row so audit_evidence re-verifies
#                       them). Idempotent: a row whose evidence_hash
#                       already sits in verdict_log is skipped whole
#                       (README growth item 1, verification-gate
#                       direction, cheap slice).
#   pick_duel_contenders()  the momentum-badged capability table picks
#                       the NEXT duel's anchor + challenger + judge.
#                       Model selection goes through the meter, not vibes.
#
# Semantics disclosure: a duel verdict measures RELATIVE quality (this
# answer beat that answer under a blind judge), so a duel-fed pass_rate
# reads "judged win-rate on this shape", while verdicts from e.g. the
# legality fixtures are absolute pass/fail. Both are honest capability
# signals; they are not the same unit, and the receipt names the source.

# Rubric -> task shape, keyed by the frozen criteria sets the duel series
# actually used. Evidence: W8_MULTIFAMILY.md (3 shapes: adversarial-review,
# schema-design, planning), LW9_DUEL_N30.md (5 shapes: adds grading and
# code-analysis), AH10_GLM_VS_DS.md ("the W8 adv rubric, kept for
# cross-receipt comparability"), V1_MULTIFAMILY_DUEL.md + the retro G1-vs-G3
# rows (adversarial-review). The rubric, not the series, is the stable key:
# LW9 planning and W8 planning used different criteria sets for the same
# named shape, and both map to planning.
DUEL_RUBRIC_TO_SHAPE: dict[frozenset[str], str] = {
    frozenset({"section coverage", "defect severity", "evidence citations", "actionability"}):
        "adversarial-review",
    frozenset({"root cause accuracy", "evidence citations", "falsifying predicates", "actionability"}):
        "adversarial-review",
    frozenset({"root cause accuracy", "evidence citations", "severity ranking", "actionability"}):
        "code-analysis",
    frozenset({"failure mode coverage", "sequencing correctness", "evidence citations", "actionability"}):
        "planning",
    frozenset({"dependency ordering", "gate metric soundness", "risk identification", "actionability"}):
        "planning",
    frozenset({"normality and edge coverage", "type correctness", "migration safety", "evidence citations"}):
        "schema-design",
    frozenset({"calibration to the artifact", "evidence citations", "verdict consistency", "actionability"}):
        "grading",
}

# altjudge rows re-judge answers already counted by their primary row (AJ1
# pairs rows by rejudge_of); feeding both would double-count one answer.
# TIE rows measure neither contender. Both are skipped, never silently.
DUEL_SKIP_MODES = {"altjudge"}
DUEL_SKIP_WINNERS = {"TIE"}

# The judge must be blind AND third-family (LW9 judge-bias finding, AJ1
# single-family contamination caveat). ember-1 stays the standing judge
# wherever it does not share a family with a contender; the altjudge
# replay path (run_rejudge) remains the second-judge owed on verdicts
# that route dollars (THE_LENSING kill-3, RIB_MODEL_GATES EMBER-1 row).
PREFERRED_JUDGES = ("fireworks/ember-1", "z-ai/glm-5.3-prime")

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DUEL_BANK = REPO_ROOT / "logs" / "duel" / "duels.jsonl"


def family_of(model_id: str) -> str:
    """Family = the provider prefix before the slash (z-ai, qwen, x-ai...)."""
    return model_id.split("/", 1)[0]


def duel_bank_rows(path: str | Path = DEFAULT_DUEL_BANK) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    # Chronological feed order so momentum windows read time honestly.
    return sorted(rows, key=lambda r: str(r.get("ts", "")))


def import_duel_bank(
    ledger: CapabilityLedger,
    rows: list[dict[str, Any]] | None = None,
    source_path: str | Path = DEFAULT_DUEL_BANK,
) -> dict[str, Any]:
    """Feed the duel bank into the capability ledger. Returns the census.

    Skips (named, counted): altjudge mode, TIE winners, rows whose rubric
    is not in the frozen shape map (unknown shape refuses loudly rather
    than filing under a guess). Idempotent on the row's evidence hash.
    """
    if rows is None:
        rows = duel_bank_rows(source_path)
    stats: dict[str, Any] = {
        "source": str(source_path),
        "banked_rows": len(rows),
        "fed": 0,
        "skipped_altjudge": 0,
        "skipped_tie": 0,
        "skipped_unknown_shape": [],
        "skipped_duplicate": 0,
        "verdicts": 0,
        "shapes": {},
    }
    seen_hashes = {
        r["evidence_hash"]
        for r in ledger.connection().execute(
            "SELECT evidence_hash FROM verdict_log WHERE evidence_hash != ''"
        )
    }
    for row in rows:
        if row.get("mode") in DUEL_SKIP_MODES:
            stats["skipped_altjudge"] += 1
            continue
        if row.get("winner") in DUEL_SKIP_WINNERS:
            stats["skipped_tie"] += 1
            continue
        shape = DUEL_RUBRIC_TO_SHAPE.get(frozenset(row.get("rubric") or []))
        if shape is None:
            stats["skipped_unknown_shape"].append(row.get("ask_id"))
            continue
        # One canonical byte form feeds both the claimed hash and the
        # resolution gate, so the digest and the verified bytes can never
        # drift apart (Q28: the hash is recomputed by record_verdict from
        # these exact bytes, not trusted from this line).
        evidence_bytes = json.dumps(
            row, sort_keys=True, ensure_ascii=True
        ).encode("utf-8")
        digest = hashlib.sha256(evidence_bytes).hexdigest()
        evidence = f"duel:{digest}"
        # Dedup compares the STORED form (duel:<sha256>): the first version
        # of this check compared the bare digest against the prefixed rows
        # and never matched, so a re-run double-fed every verdict (caught on
        # the D2 idempotency re-run; ledger repaired from the pre-feed
        # backup before re-import. Fixed by comparing like forms).
        if evidence in seen_hashes:
            stats["skipped_duplicate"] += 1
            continue
        seen_hashes.add(evidence)
        for model, won in (
            (row["a_model"], row["winner"] == "A"),
            (row["b_model"], row["winner"] == "B"),
        ):
            ledger.record_verdict(
                model, shape, won, evidence_hash=evidence,
                evidence_bytes=evidence_bytes,
                evidence_source=f"duel-bank:{source_path}",
            )
            stats["verdicts"] += 1
        stats["fed"] += 1
        stats["shapes"][shape] = stats["shapes"].get(shape, 0) + 1
    return stats


@dataclass
class DuelRoute:
    """The meter's answer for one duel: who fights, who judges, why."""

    task_shape: str
    ranked: list[dict[str, Any]]   # momentum-badged table, best first
    anchor: Optional[str]
    challenger: Optional[str]
    judge: Optional[str]
    reasons: list[str]
    receipt: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return {
            "task_shape": self.task_shape,
            "ranked": self.ranked,
            "anchor": self.anchor,
            "challenger": self.challenger,
            "judge": self.judge,
            "reasons": self.reasons,
            "receipt": self.receipt,
        }


def shape_table(ledger: CapabilityLedger, task_shape: str) -> list[dict[str, Any]]:
    """The momentum-badged capability table for one shape, best first.

    Rank: pass_rate desc, then momentum (RISING > STEADY/no-data >
    DECLINING), then sample size, then model_id for determinism.
    """
    rows = ledger.connection().execute(
        "SELECT model_id, pass_rate, sample_size FROM capability"
        " WHERE task_shape = ?",
        (task_shape,),
    ).fetchall()
    table = []
    for row in rows:
        mom = ledger.momentum(row["model_id"], task_shape)
        table.append(
            {
                "model_id": row["model_id"],
                "family": family_of(row["model_id"]),
                "pass_rate": round(float(row["pass_rate"]), 4),
                "sample_size": int(row["sample_size"]),
                "momentum_badge": None if mom is None else mom.badge,
                "streak_badge": None if mom is None else mom.streak_badge,
            }
        )
    def rank_key(entry: dict[str, Any]) -> tuple:
        badge = entry["momentum_badge"]
        mrank = MOMENTUM_RANK["STEADY"] if badge is None else MOMENTUM_RANK[badge]
        return (
            -entry["pass_rate"],
            mrank,
            -entry["sample_size"],
            entry["model_id"],
        )
    return sorted(table, key=rank_key)


def pick_duel_contenders(
    ledger: CapabilityLedger,
    receipts: ReceiptLog,
    task_shape: str,
) -> DuelRoute:
    """Route one duel through the momentum-badged table.

    anchor = the strongest measured contender on the shape. challenger =
    the highest-ranked contender from a DIFFERENT family (a same-family
    rematch measures the family against itself and violates the
    cross-family purpose of a duel). judge = first preferred judge from
    a family neither contender belongs to. When the meter has no rows
    (or only one family) for the shape, the gap is named, not papered
    over: that shape is census material, and the duel itself is the
    instrument that would close the gap.
    """
    table = shape_table(ledger, task_shape)
    reasons: list[str] = []
    anchor = challenger = judge = None
    if not table:
        reasons.append(
            f"no measured contenders for task shape {task_shape}:"
            " coverage gap, route refuses to pick from vibes"
        )
    else:
        anchor_row = table[0]
        anchor = anchor_row["model_id"]
        reasons.append(
            f"anchor {anchor}: top of the momentum-badged table"
            f" (pass_rate {anchor_row['pass_rate']}, n={anchor_row['sample_size']},"
            f" momentum {anchor_row['momentum_badge']},"
            f" streak {anchor_row['streak_badge']})"
        )
        for entry in table[1:]:
            if entry["family"] != anchor_row["family"]:
                challenger = entry["model_id"]
                reasons.append(
                    f"challenger {challenger}: highest-ranked different-family"
                    f" contender (pass_rate {entry['pass_rate']},"
                    f" n={entry['sample_size']}, momentum {entry['momentum_badge']})"
                )
                break
        if challenger is None:
            reasons.append(
                "only one family measured on this shape: no cross-family"
                " challenger available, gap named"
            )
        for candidate in PREFERRED_JUDGES:
            fam = family_of(candidate)
            if challenger is not None and fam in (
                family_of(anchor), family_of(challenger)
            ):
                continue
            judge = candidate
            reasons.append(
                f"judge {judge}: first preferred judge outside both contender"
                " families (blind, third-family); altjudge replay stays the"
                " second judge owed on dollar-routing verdicts"
            )
            break
    receipt = receipts.emit(
        {
            "ts": _utc_now_iso(),
            "task_shape": task_shape,
            "chosen": anchor,
            "considered": table,
            "reasons": reasons,
            "cost_usd": 0.0,
            "confidence": None,
            "exploration": challenger is None,
            "decision": "duel-route",
            "challenger": challenger,
            "judge": judge,
        }
    )
    return DuelRoute(task_shape, table, anchor, challenger, judge, reasons, receipt)


def _cli(argv: Optional[list[str]] = None) -> int:
    """CLI: duel-import and duel-route (the D2 wiring).

    Examples (repo venv, from the repo root):
      .venv/Scripts/python.exe -m tools.gps_mcp.router duel-import
      .venv/Scripts/python.exe -m tools.gps_mcp.router duel-route -s adversarial-review
    """
    import argparse

    parser = argparse.ArgumentParser(prog="tools.gps_mcp.router")
    parser.add_argument("--db", default=str(Path(__file__).parent / "gps_ledger.db3"))
    parser.add_argument(
        "--receipts", default=str(Path(__file__).parent / "receipts.jsonl")
    )
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_import = sub.add_parser(
        "duel-import", help="feed logs/duel/duels.jsonl into the ledger"
    )
    p_import.add_argument("--duels", default=str(DEFAULT_DUEL_BANK))
    p_route = sub.add_parser(
        "duel-route", help="pick the next duel's contenders from the meter"
    )
    p_route.add_argument("-s", "--task-shape", required=True)
    args = parser.parse_args(argv)

    ledger = CapabilityLedger(args.db)
    receipts = ReceiptLog(args.receipts)
    if args.cmd == "duel-import":
        stats = import_duel_bank(ledger, source_path=args.duels)
        print(json.dumps(stats, indent=2, sort_keys=True))
        return 0
    route = pick_duel_contenders(ledger, receipts, args.task_shape)
    print(json.dumps(route.as_dict(), indent=2, sort_keys=True))
    return 0


def _coerce_constraints(
    constraints: Constraints | dict[str, Any] | None,
) -> Constraints:
    if constraints is None:
        return Constraints()
    if isinstance(constraints, Constraints):
        return constraints
    return Constraints.from_dict(constraints)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def _trace_id(ts: str, task_shape: str) -> str:
    digest = hashlib.sha256(f"{ts}|{task_shape}".encode("utf-8")).hexdigest()[:12]
    return f"csc_{digest}"


if __name__ == "__main__":  # pragma: no cover - CLI shell entry
    raise SystemExit(_cli())
