"""Self-play orchestrator — actor-reward loop with bottleneck measurement.

Splits the self-play loop into two legs:
  1. LOCAL ACTOR — generates self-play moves via llama.cpp bridge
     (Q4 quantized model fitting RX 5600 XT 6 GB VRAM).
  2. REMOTE REWARD SCORER — scores positions via free-tier API lanes
     (lane_runner.flash_call → L1 free_remote).

Bottleneck measurement hooks on every leg isolate which component
dominates wall time.  Produces Elo-vs-baseline evidence on a
built-in math benchmark (GSM8K-style questions).

Integrates with existing mag/lanes.py and mag/lane_runner.py for the
API scoring leg; the local actor leg is mag/llama_cpp_bridge.py.
"""
from __future__ import annotations

import json
import logging
import time
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from mag import llama_cpp_bridge as bridge
from mag.selfplay_evidence import write_session_evidence

_LOG = logging.getLogger("mag.selfplay_orchestrator")

# ── math benchmark (GSM8K-style, operator-named) ──────────────────────

MATH_PROBLEMS: list[dict[str, Any]] = [
    {"id": "m001", "question": "What is 17 × 23?", "answer": 391},
    {"id": "m002", "question": "What is 128 ÷ 4?", "answer": 32},
    {"id": "m003", "question": "What is 7² + 24²?", "answer": 625},
    {"id": "m004", "question": "What is 3 × (14 + 6) − 10?", "answer": 50},
    {"id": "m005", "question": "What is 99 − 47 + 15?", "answer": 67},
    {"id": "m006", "question": "What is 5! ?", "answer": 120},
    {"id": "m007", "question": "What is 0.6 × 0.5?", "answer": 0.3},
    {"id": "m008", "question": "What is 2³ × 3²?", "answer": 72},
]


@dataclass
class BottleneckSample:
    """One measurement of a single leg's wall time."""
    leg: str  # "actor" | "scorer" | "total"
    ms: float
    ok: bool = True
    detail: str = ""


@dataclass
class SelfPlayResult:
    """One self-play game result."""
    problem_id: str
    actor_move: str
    actor_ms: float
    scorer_ms: float
    total_ms: float
    reward: float  # 0.0–1.0
    correct: bool
    bottleneck: str  # which leg dominated


@dataclass
class SessionReport:
    """Full session evidence."""
    n_games: int
    n_correct: int
    accuracy: float
    elo: float
    elo_vs_baseline: float
    avg_actor_ms: float
    avg_scorer_ms: float
    bottleneck: str
    samples: list[BottleneckSample] = field(default_factory=list)
    per_problem: list[dict[str, Any]] = field(default_factory=list)
    # Move 3 cure (stockfish-door-20261007): scorer health is evidence, not
    # an implementation detail.  scorer_fallbacks counts games whose scorer
    # leg raised and fell back to neutral 0.5; scorer_ok_ratio is the live
    # share of scored games.  main() asserts ratio == 1.0 before any
    # evidence write.
    scorer_fallbacks: int = 0
    scorer_ok_ratio: float = 1.0


# ── Elo engine ─────────────────────────────────────────────────────────

class EloEngine:
    """Standard Elo with configurable K-factor and baseline rating."""

    BASELINE_RATING = 1000.0
    DEFAULT_K = 32.0

    def __init__(self, k: float = DEFAULT_K, baseline: float = BASELINE_RATING) -> None:
        self.k = k
        self.rating = baseline
        self.n_games = 0
        self.n_wins = 0

    def update(self, reward: float) -> float:
        """Apply one game result (0/0.5/1 reward). Returns new rating."""
        expected = 1.0 / (1.0 + 10 ** ((self.BASELINE_RATING - self.rating) / 400.0))
        self.rating += self.k * (reward - expected)
        self.n_games += 1
        if reward >= 1.0:
            self.n_wins += 1
        return round(self.rating, 1)

    @property
    def elo_vs_baseline(self) -> float:
        return round(self.rating - self.BASELINE_RATING, 1)


# ── bottleneck hooks ───────────────────────────────────────────────────

def _measure(
    leg: str, fn, *args: Any, **kwargs: Any
) -> tuple[Any, BottleneckSample]:
    """Time a callable, return (result, BottleneckSample)."""
    t0 = time.monotonic()
    try:
        result = fn(*args, **kwargs)
        ok = True
        detail = ""
    except Exception as e:
        result = None
        ok = False
        detail = str(e)
    elapsed = (time.monotonic() - t0) * 1000
    return result, BottleneckSample(leg=leg, ms=round(elapsed, 1), ok=ok, detail=detail)


# ── orchestrator ───────────────────────────────────────────────────────

class SelfPlayOrchestrator:
    """Actor-reward self-play loop with bottleneck measurement."""

    def __init__(
        self,
        actor: bridge.LlamaCppBridge | None = None,
        k_factor: float = EloEngine.DEFAULT_K,
    ) -> None:
        self.actor = actor or bridge.LlamaCppBridge()
        self.elo = EloEngine(k=k_factor)
        self.samples: list[BottleneckSample] = []
        self.results: list[SelfPlayResult] = []

    # --- single game --------------------------------------------------

    def play_one(self, problem: dict[str, Any]) -> SelfPlayResult:
        """Run one actor-reward cycle on a math problem."""
        prompt = f"Solve: {problem['question']} Answer with just the number."

        # Leg 1: local actor
        actor_result, actor_sample = _measure(
            "actor", self.actor.generate_move, prompt
        )
        self.samples.append(actor_sample)
        move = actor_result.get("move", "") if isinstance(actor_result, dict) else str(actor_result)
        actor_ms = actor_sample.ms

        # Leg 2: remote reward scorer (via lane_runner.flash_call)
        scorer_prompt = (
            f"Problem: {problem['question']}\n"
            f"Answer: {move}\n"
            "Rate 0.0–1.0: is the answer correct and complete?"
        )
        t0 = time.monotonic()
        scorer_ok = True
        scorer_detail = ""
        try:
            from mag.lane_runner import flash_call
            score_text = flash_call(system="You are a math rater.", user=scorer_prompt)
        except Exception as e:
            # Move 3 cure (stockfish-door-20261007): a dead scorer must never
            # read neutral 0.5 with ok=True.  The exception is threaded into
            # ok=False on the scorer BottleneckSample and counted on the
            # SessionReport; main() refuses to write evidence off a degraded
            # reward leg.  Cause at cure time: the bare except swallowed the
            # flash_call RuntimeError (mag/lane_runner.py flash lane down) and
            # appended the sample hard-coded ok=True, so offline runs scored
            # every game 0.5 while the evidence read healthy.
            scorer_ok = False
            scorer_detail = str(e)
            score_text = SelfPlayOrchestrator._fallback_score(scorer_prompt)
        scorer_ms = round((time.monotonic() - t0) * 1000, 1)
        self.samples.append(
            BottleneckSample(leg="scorer", ms=scorer_ms, ok=scorer_ok, detail=scorer_detail)
        )

        # Parse reward
        reward = self._parse_reward(score_text)

        # Ground truth
        correct = self._check_answer(problem["question"], problem["answer"], move)

        # Elo update
        self.elo.update(reward if correct else 0.0)

        # Bottleneck
        bottleneck = "actor" if actor_ms >= scorer_ms else "scorer"

        result = SelfPlayResult(
            problem_id=problem["id"],
            actor_move=move,
            actor_ms=round(actor_ms, 1),
            scorer_ms=round(scorer_ms, 1),
            total_ms=round(actor_ms + scorer_ms, 1),
            reward=round(reward, 2),
            correct=correct,
            bottleneck=bottleneck,
        )
        self.results.append(result)
        return result

    def run_session(self, problems: list[dict[str, Any]] | None = None) -> SessionReport:
        """Run a full self-play session over problems. Returns SessionReport."""
        probs = problems or MATH_PROBLEMS
        for p in probs:
            self.play_one(p)
        return self.report()

    # --- report -------------------------------------------------------

    def report(self) -> SessionReport:
        """Produce the session evidence report."""
        n = len(self.results)
        if n == 0:
            return SessionReport(n_games=0, n_correct=0, accuracy=0.0, elo=1000.0, elo_vs_baseline=0.0, avg_actor_ms=0.0, avg_scorer_ms=0.0, bottleneck="none")
        correct = sum(1 for r in self.results if r.correct)
        actor_times = [r.actor_ms for r in self.results if r.actor_ms > 0]
        scorer_times = [r.scorer_ms for r in self.results if r.scorer_ms > 0]
        avg_actor = sum(actor_times) / len(actor_times) if actor_times else 0.0
        avg_scorer = sum(scorer_times) / len(scorer_times) if scorer_times else 0.0
        bottleneck = (
            "actor" if avg_actor >= avg_scorer else "scorer"
            if scorer_times else "actor"
            if actor_times else "none"
        )
        # Move 3 cure (stockfish-door-20261007): count dead-scorer legs from
        # the samples themselves so the ratio always matches the measured
        # evidence.  0 games scores vacuously healthy (nothing written claims
        # a reward leg).
        scorer_fallbacks = sum(
            1 for s in self.samples if s.leg == "scorer" and not s.ok
        )
        scorer_ok_ratio = round((n - scorer_fallbacks) / n, 3) if n else 1.0
        return SessionReport(
            n_games=n,
            n_correct=correct,
            accuracy=round(correct / n, 3),
            elo=round(self.elo.rating, 1),
            elo_vs_baseline=self.elo.elo_vs_baseline,
            avg_actor_ms=round(avg_actor, 1),
            avg_scorer_ms=round(avg_scorer, 1),
            bottleneck=bottleneck,
            scorer_fallbacks=scorer_fallbacks,
            scorer_ok_ratio=scorer_ok_ratio,
            samples=list(self.samples),
            per_problem=[
                {
                    "id": r.problem_id,
                    "move": r.actor_move,
                    "reward": r.reward,
                    "correct": r.correct,
                    "actor_ms": r.actor_ms,
                    "scorer_ms": r.scorer_ms,
                    "total_ms": r.total_ms,
                    "bottleneck": r.bottleneck,
                }
                for r in self.results
            ],
        )

    # --- helpers ------------------------------------------------------

    @staticmethod
    def _fallback_score(prompt: str) -> str:
        """Score without an API: return 0.5 (neutral)."""
        return "0.5"

    @staticmethod
    def _parse_reward(text: str) -> float:
        if not text:
            return 0.5
        t = text.strip().lower()
        # Look for a 0.0–1.0 number
        import re
        m = re.search(r"(\d+(?:\.\d+)?)", t)
        if m:
            val = float(m.group(1))
            return max(0.0, min(1.0, val))
        if "correct" in t or "yes" in t or "true" in t or "complete" in t:
            return 1.0
        if "incorrect" in t or "no" in t or "false" in t or "wrong" in t:
            return 0.0
        return 0.5

    @staticmethod
    def _check_answer(question: str, expected: Any, move: str) -> bool:
        """Crude ground-truth check: look for the answer number in the move."""
        move_str = str(move).strip().strip('"').strip("'")
        try:
            move_val = float(move_str)
            return abs(move_val - float(expected)) < 0.01
        except (ValueError, TypeError):
            return str(expected) in move_str


# ── CLI entry point ────────────────────────────────────────────────────

def main(orch: SelfPlayOrchestrator | None = None) -> SessionReport:
    """Run a full self-play session, write evidence, print summary."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    orch = orch or SelfPlayOrchestrator()

    # Move 6 gate (stockfish-door-20261007): fail closed without a configured
    # model.  main() used to default-construct LlamaCppBridge() with
    # model_path=None, whose generate_move answers every prompt with a sha256
    # hash fallback move, and then still wrote the evidence file: an
    # unconfigured run would clobber the day's only real session evidence
    # with fallback-hash junk (register row, SYNTHESIS.md:36, ractor_engine
    # 2026-10-06-stockfish-coding).  No model file on disk, no session, no
    # write.  This removes the silent fallback path rather than adding one
    # (no-fallback-branch-creep law).
    model_path = getattr(orch.actor, "model_path", None)
    if model_path is None or not Path(model_path).is_file():
        raise SystemExit(
            "selfplay main() refused to run: no configured model_path "
            f"(actor.model_path={model_path!r}); an unconfigured actor answers "
            "every move with a hash fallback and would land junk evidence. "
            "Configure one, e.g. SelfPlayOrchestrator(actor=LlamaCppBridge(model_path=...))"
        )

    report = orch.run_session()

    # Move 3 gate (stockfish-door-20261007): the assert fires BEFORE the
    # evidence write so a dead scorer can never land evidence_latest.json
    # with every game reading neutral 0.5 as if healthy.  Evidence rule:
    # write only when every game was scored by a live scorer (ratio == 1.0).
    assert report.scorer_ok_ratio == 1.0, (
        f"dead scorer: {report.scorer_fallbacks}/{report.n_games} games fell back "
        f"to neutral 0.5 (scorer_ok_ratio={report.scorer_ok_ratio}); "
        "refusing to write evidence"
    )

    # Move 6 (stockfish-door-20261007): evidence is append-only with a
    # pointer file (mag/selfplay_evidence.py); the writer used to be
    # last-write-wins on one fixed name, so a rerun destroyed the previous
    # session's only record.
    evidence_path, pointer_path = write_session_evidence(
        report, Path("memory/runs/selfplay")
    )
    _LOG.info(
        "self-play session: %d games, %.0f%% correct, Elo %.1f (+%.1f vs baseline), bottleneck=%s",
        report.n_games,
        report.accuracy * 100,
        report.elo,
        report.elo_vs_baseline,
        report.bottleneck,
    )
    return report


if __name__ == "__main__":
    main()