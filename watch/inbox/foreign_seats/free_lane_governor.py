#!/usr/bin/env python3
"""tools/sovereign/free_lane_governor.py — Sovereign Free Lane Governor & Hoeffding Circuit Breaker.

Self-steals and synthesizes the estate's complete free-compute reliability primitives:
1. The Three Laws of Free Compute (public_seed/FREE_COMPUTE.md)
2. Mathematical Hoeffding Calibration Gate (lane_hoeffding.py: Hoeffding 1963)
3. Multi-Armed Bandit Cascade (tools/contextual_bandit_router.py: LinUCB)
4. Tri-State Whaler Cadence (free_whaler.py: ALIVE, FLAKY, DEAD)
5. Syntactic Normalization Gate (strips chat fluff, enforces schema, extracts JSON)

Zero third-party dependencies (Python 3.10+ stdlib only).
"""

from __future__ import annotations

import json
import math
import os
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
TELEMETRY_PATH = REPO_ROOT / "lane_stats_bob.json"
VERIFIED_PATH = REPO_ROOT / "free_lanes_verified.json"
STATE_PATH = REPO_ROOT / "free_governor_state.json"


@dataclass
class LaneRecord:
    id: str
    provider: str
    n_calls: int = 0
    n_success: int = 0
    latency_sum: float = 0.0
    consecutive_fails: int = 0
    circuit_open_until: float = 0.0
    status: str = "PROBATION"  # SEALED, SPECULATIVE, QUARANTINED, DEAD

    @property
    def fail_rate(self) -> float:
        if self.n_calls == 0:
            return 0.0
        return (self.n_calls - self.n_success) / self.n_calls

    @property
    def avg_latency(self) -> float:
        if self.n_success == 0:
            return 999.0
        return round(self.latency_sum / self.n_success, 2)

    def is_available(self, now: float) -> bool:
        return now >= self.circuit_open_until and self.status != "DEAD"


class HoeffdingGate:
    """Calculates rigorous statistical confidence on whether a free lane's failure rate
    exceeds observed failure rate f + tolerance t (Hoeffding 1963)."""

    @staticmethod
    def bound(k: int, failures: int, tolerance: float = 0.15) -> float:
        """P(true_rate > (failures/k) + tolerance) <= exp(-2 * k * t^2)."""
        if k <= 0:
            return 1.0
        return math.exp(-2.0 * k * (tolerance ** 2))

    @staticmethod
    def evaluate(k: int, failures: int, tolerance: float = 0.15, alpha: float = 0.05) -> Tuple[bool, float]:
        """Returns (is_sealed, bound_probability). Sealed means P <= alpha (e.g. 5% tail)."""
        if k < 10:
            return False, 1.0  # Insufficient sample count
        p = HoeffdingGate.bound(k, failures, tolerance)
        return p <= alpha, p


class FreeLaneGovernor:
    """Governs free lane routing, exponential backoffs, circuit breaking, and telemetry updates."""

    # Default baseline providers and models known to offer zero-cost tiers
    DEFAULT_FREE_LANES = [
        ("nvidia/nemotron-3-super-120b-a12b:free", "openrouter"),
        ("nvidia/nemotron-3-ultra-550b-a55b:free", "openrouter"),
        ("nvidia/nemotron-3.5-lightning:free", "openrouter"),
        ("liquid/lfm-2.5-2.6b:free", "openrouter"),
        ("dots-studio/dots-3-note-preview:free", "openrouter"),
        ("cohere/north-mini-code:free", "openrouter"),
        ("groq/gpt-oss-120b", "groq"),
        ("groq/qwen3.8-27b", "groq"),
        ("gemini-2.0-flash-exp", "google"),
        ("ollama/qwen3:1.7b", "local"),
    ]

    def __init__(self, state_file: Optional[Path] = None):
        self.state_file = state_file or STATE_PATH
        self.lanes: Dict[str, LaneRecord] = {}
        self.load_state()

    def _infer_provider(self, lane_id: str) -> str:
        if lane_id.startswith("ollama/"):
            return "local"
        if lane_id.startswith("groq/"):
            return "groq"
        if "gemini" in lane_id:
            return "google"
        return "openrouter"

    def load_state(self):
        """Seed initial state from legacy telemetry files (lane_stats_bob.json, free_lanes_verified.json)."""
        # 1. Initialize defaults
        for lane_id, provider in self.DEFAULT_FREE_LANES:
            self.lanes[lane_id] = LaneRecord(id=lane_id, provider=provider)

        # 2. Fold historical lane stats from bob if present
        if TELEMETRY_PATH.is_file():
            try:
                with open(TELEMETRY_PATH, "r", encoding="utf-8") as f:
                    tele = json.load(f)
                for lid, stats in tele.items():
                    prov = self._infer_provider(lid)
                    rec = self.lanes.get(lid) or LaneRecord(id=lid, provider=prov)
                    rec.n_calls = int(stats.get("n", 0))
                    rec.n_success = int(stats.get("ok", 0))
                    rec.latency_sum = float(stats.get("latSum", 0.0))
                    self.lanes[lid] = rec
            except Exception:
                pass

        # 3. Fold verified status from whaler if present
        if VERIFIED_PATH.is_file():
            try:
                with open(VERIFIED_PATH, "r", encoding="utf-8") as f:
                    vdata = json.load(f)
                dead_set = {d["id"] for d in vdata.get("detail", []) if d.get("status") == "DEAD"}
                for lid in dead_set:
                    if lid in self.lanes:
                        self.lanes[lid].status = "DEAD"
            except Exception:
                pass

        # 4. Load persisted governor state if available
        if self.state_file.is_file():
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                for lid, d in saved.get("lanes", {}).items():
                    if lid in self.lanes:
                        rec = self.lanes[lid]
                        rec.consecutive_fails = d.get("consecutive_fails", 0)
                        rec.circuit_open_until = d.get("circuit_open_until", 0.0)
                        rec.status = d.get("status", rec.status)
            except Exception:
                pass

        self._calibrate_all()

    def save_state(self):
        data = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "lanes": {
                lid: {
                    "provider": rec.provider,
                    "n_calls": rec.n_calls,
                    "n_success": rec.n_success,
                    "avg_latency": rec.avg_latency,
                    "fail_rate": round(rec.fail_rate, 3),
                    "consecutive_fails": rec.consecutive_fails,
                    "circuit_open_until": rec.circuit_open_until,
                    "status": rec.status,
                }
                for lid, rec in self.lanes.items()
            },
        }
        try:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def _calibrate_all(self):
        """Run the Hoeffding gate on each lane to determine status."""
        now = time.time()
        for lid, rec in self.lanes.items():
            if rec.status == "DEAD":
                continue
            if rec.circuit_open_until > now or rec.consecutive_fails >= 3:
                rec.status = "QUARANTINED"
                continue
            fails = rec.n_calls - rec.n_success
            is_sealed, bound_prob = HoeffdingGate.evaluate(rec.n_calls, fails, tolerance=0.15, alpha=0.05)
            if is_sealed and rec.fail_rate <= 0.15:
                rec.status = "SEALED"
            else:
                rec.status = "SPECULATIVE"

    def record_feedback(self, lane_id: str, success: bool, latency: float, error_code: Optional[int] = None):
        """Record execution outcome, apply circuit breaker rules, and calibrate Hoeffding gate."""
        now = time.time()
        rec = self.lanes.get(lane_id)
        if not rec:
            prov = self._infer_provider(lane_id)
            rec = LaneRecord(id=lane_id, provider=prov)
            self.lanes[lane_id] = rec

        rec.n_calls += 1
        if success:
            rec.n_success += 1
            rec.latency_sum += latency
            rec.consecutive_fails = 0
            if rec.status == "QUARANTINED":
                rec.status = "SPECULATIVE"
        else:
            rec.consecutive_fails += 1
            # Circuit breaker trigger: 429 or 3 consecutive failures
            if error_code in (429, 503) or rec.consecutive_fails >= 3:
                # Exponential cooldown: 30s * 2^(fails - 1)
                backoff_s = min(3600.0, 30.0 * (2 ** max(0, rec.consecutive_fails - 1)))
                rec.circuit_open_until = now + backoff_s
                rec.status = "QUARANTINED"
            elif error_code in (403, 404, 410):
                # Permanent failure -> DEAD
                rec.status = "DEAD"

        self._calibrate_all()
        self.save_state()

    def route(self, task_intent: str = "general", max_latency: float = 10.0) -> Tuple[str, List[str]]:
        """Compute Upper Confidence Bound (LinUCB) ranking over available free lanes.
        Returns (best_lane, ranked_cascade_ladder)."""
        now = time.time()
        candidates = [rec for rec in self.lanes.values() if rec.is_available(now)]

        if not candidates:
            # All remote free lanes quarantined or dead -> Fall back to local edge
            return "ollama/qwen3:1.7b", ["ollama/qwen3:1.7b"]

        scored: List[Tuple[float, str]] = []
        for rec in candidates:
            # Exploitation: empirical success rate (0.0 to 1.0)
            p_success = 1.0 - rec.fail_rate
            # Exploration bonus: Hoeffding/LinUCB UCB radius
            n = max(1, rec.n_calls)
            exploration_bonus = math.sqrt(2.0 * math.log(max(10, sum(c.n_calls for c in candidates) + 1)) / n)
            # Latency penalty: penalize slow lanes (> 2.0s)
            lat = rec.avg_latency if rec.avg_latency < 900.0 else 2.0
            lat_penalty = min(0.5, (lat / max_latency) * 0.5)

            # Intent modifier
            intent_bonus = 0.0
            if "fast" in task_intent and "groq" in rec.id:
                intent_bonus += 0.3
            elif "strong" in task_intent and ("550b" in rec.id or "120b" in rec.id):
                intent_bonus += 0.4
            elif "code" in task_intent and "code" in rec.id:
                intent_bonus += 0.3

            score = p_success + (0.5 * exploration_bonus) - lat_penalty + intent_bonus
            scored.append((score, rec.id))

        scored.sort(key=lambda x: x[0], reverse=True)
        ladder = [item[1] for item in scored]
        # Always guarantee local edge is the absolute terminal backstop
        if "ollama/qwen3:1.7b" not in ladder:
            ladder.append("ollama/qwen3:1.7b")

        return ladder[0], ladder

    def scrub_for_dispatch(self, prompt: str) -> Tuple[str, Any]:
        """Scrubs internal IPs, paths, and secrets before dispatching to external free lane."""
        try:
            from tools.sovereign.standin_scrubber import BidirectionalScrubber
            return BidirectionalScrubber().scrub_outbound(prompt)
        except Exception:
            return prompt, None

    def restore_from_dispatch(self, reply: str, session: Any) -> str:
        """Restores original real IPs and paths from model completion."""
        if not session:
            return reply
        try:
            from tools.sovereign.standin_scrubber import BidirectionalScrubber
            return BidirectionalScrubber().restore_inbound(reply, session)
        except Exception:
            return reply


class SyntacticNormalizer:
    """Extracts valid JSON payloads and cleans chat flaked output from free models."""

    @staticmethod
    def extract_json(raw_text: str) -> Optional[Any]:
        if not raw_text:
            return None
        raw = raw_text.strip()
        # 1. Direct parse attempt
        try:
            return json.loads(raw)
        except Exception:
            pass

        # 2. Markdown fenced block extraction: ```json ... ```
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", raw, re.IGNORECASE)
        if match:
            candidate = match.group(1).strip()
            try:
                return json.loads(candidate)
            except Exception:
                pass

        # 3. Outer bracket search { ... } or [ ... ]
        first_curly = raw.find("{")
        last_curly = raw.rfind("}")
        if first_curly != -1 and last_curly > first_curly:
            slice_obj = raw[first_curly : last_curly + 1]
            try:
                return json.loads(slice_obj)
            except Exception:
                pass

        first_sq = raw.find("[")
        last_sq = raw.rfind("]")
        if first_sq != -1 and last_sq > first_sq:
            slice_arr = raw[first_sq : last_sq + 1]
            try:
                return json.loads(slice_arr)
            except Exception:
                pass

        return None


def run_selftest() -> bool:
    """Verify governor mathematical properties, LinUCB routing, and JSON normalizer."""
    print("=== [TEST 1] Hoeffding Calibration Gate ===")
    # 40 trials, 9 failures, 15% tolerance
    b = HoeffdingGate.bound(40, 9, 0.15)
    is_sealed, p = HoeffdingGate.evaluate(40, 9, 0.15, alpha=0.05)
    print(f"  Hoeffding bound (K=40, fail=9, t=0.15): P <= {p:.4f} (Sealed: {is_sealed})")
    assert p < 0.20, "Hoeffding bound calculation divergence"

    # High sample, low failure -> Must SEAL
    is_sealed_high, p_high = HoeffdingGate.evaluate(100, 5, 0.15, alpha=0.05)
    print(f"  Hoeffding bound (K=100, fail=5, t=0.15): P <= {p_high:.4f} (Sealed: {is_sealed_high})")
    assert is_sealed_high, "High confidence lane failed to seal"

    print("=== [TEST 2] Governor LinUCB Routing & Cascade ===")
    test_state_file = REPO_ROOT / "scratch" / "test_governor_state.json"
    test_state_file.parent.mkdir(parents=True, exist_ok=True)
    if test_state_file.exists():
        test_state_file.unlink()

    gov = FreeLaneGovernor(state_file=test_state_file)
    best, ladder = gov.route("fast")
    print(f"  Initial Route (intent=fast) -> Best: {best}")
    print(f"  Cascade Ladder: {ladder[:3]} ... (total {len(ladder)})")
    assert len(ladder) >= 3, "Cascade ladder too short"

    # Simulate 429 rate limit tripping circuit breaker
    print("=== [TEST 3] Circuit Breaker & 429 Quarantine ===")
    gov.record_feedback(best, success=False, latency=0.2, error_code=429)
    assert gov.lanes[best].status == "QUARANTINED"
    new_best, new_ladder = gov.route("fast")
    print(f"  Post-429 Route -> Quarantined: {best} | New Best: {new_best}")
    assert new_best != best, "Circuit breaker failed to route away from quarantined lane"

    print("=== [TEST 4] Syntactic Normalizer Chaff Removal ===")
    chaff_payload = 'Here is the JSON output you requested:\n```json\n{"status": "ok", "items": [1, 2, 3]}\n```\nHope that helps!'
    parsed = SyntacticNormalizer.extract_json(chaff_payload)
    print(f"  Extracted from conversational markdown: {parsed}")
    assert parsed is not None and parsed.get("status") == "ok", "JSON normalizer failed on fenced block"

    naked_chaff = 'Certainly! The dictionary is: {"verdict": "RATIFIED", "votes": 5} without backticks.'
    parsed2 = SyntacticNormalizer.extract_json(naked_chaff)
    print(f"  Extracted from naked conversational text: {parsed2}")
    assert parsed2 is not None and parsed2.get("verdict") == "RATIFIED", "JSON normalizer failed on curly search"

    print("[free_lane_governor] ALL 4 TESTS PASSED CLEANLY.")
    return True


if __name__ == "__main__":
    if "--test" in sys.argv:
        success = run_selftest()
        sys.exit(0 if success else 1)

    gov = FreeLaneGovernor()
    if "--status" in sys.argv:
        print(f"=== SOVEREIGN FREE LANE GOVERNOR (Active Lanes: {len(gov.lanes)}) ===")
        print(f"{'LANE ID':<50} {'STATUS':<13} {'CALLS':<7} {'FAIL%':<7} {'LAT(s)':<7}")
        print("-" * 88)
        for lid, rec in sorted(gov.lanes.items(), key=lambda x: (x[1].status != 'SEALED', x[1].fail_rate)):
            print(f"{lid:<50} {rec.status:<13} {rec.n_calls:<7} {rec.fail_rate*100:<6.1f}% {rec.avg_latency:<7.2f}")
    elif "--route" in sys.argv:
        idx = sys.argv.index("--route")
        intent = sys.argv[idx + 1] if len(sys.argv) > idx + 1 else "general"
        best, ladder = gov.route(intent)
        print(json.dumps({"intent": intent, "best": best, "cascade": ladder}, indent=2))
    else:
        print("Usage: python -m tools.sovereign.free_lane_governor [--status | --route <intent> | --test]")
