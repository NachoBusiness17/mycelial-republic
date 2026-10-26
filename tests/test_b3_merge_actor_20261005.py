"""B3 merge actor tests (build wave 2026-10-05).

Steal card: watch/inbox/frontier_olm_2026-10-04/steal/swarm-orchestration via x.md
FIND 1 (Google 180-config study, numbers live-verified on the card): centralized
coordination +80.9 pct on parallelizable work; independent swarms amplify errors
17.2x vs 4.4x contained by one centralized merge turn. consensus_merge is that
turn: consensus_quality over pooled answers + one shape-matched trail row.

CID law under test (the consensus-illusion guard): a unanimous pool is one
correlated opinion (quality penalty), genuine dissent is the healthier signal.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pytest

from mag import memweave

UNANIMOUS = ["alpha beta gamma delta"] * 4
DISSENTING = [
    "alpha beta gamma delta",
    "epsilon zeta eta theta",
    "iota kappa lambda mu",
    "nu xi omicron pi",
]


def _merge(answers: list[str], trail: Path, **kw) -> dict:
    return memweave.consensus_merge(answers, "research", trail=trail, **kw)


def test_unanimous_pool_takes_cid_quality_penalty(tmp_path: Path) -> None:
    res = _merge(UNANIMOUS, tmp_path / "trail.jsonl")
    v = res["verdict"]
    assert v["ok"] is True
    assert v["schema"] == "memweave.consensus.v1"
    assert v["n_answers"] == 4
    assert v["n_independent"] == 1          # 4 identical answers = 1 opinion
    assert v["n_effective"] == 1.0          # the CID quality penalty in full
    assert v["correlated"] is True
    assert v["verdict"] == "correlated_weak"


def test_dissenting_pool_is_healthier(tmp_path: Path) -> None:
    trail = tmp_path / "trail.jsonl"
    uni = _merge(UNANIMOUS, trail)["verdict"]
    dis = _merge(DISSENTING, trail)["verdict"]
    assert dis["n_answers"] == 4
    assert dis["n_independent"] == 4        # 4 disjoint-token answers
    assert dis["n_effective"] == 4.0
    assert dis["correlated"] is False
    assert dis["verdict"] == "strong"
    # healthier than the unanimous pool on every CID axis
    assert dis["n_independent"] > uni["n_independent"]
    assert dis["n_effective"] > uni["n_effective"]


def test_rho_pass_through_applies_cid_correction(tmp_path: Path) -> None:
    res = _merge(UNANIMOUS, tmp_path / "trail.jsonl", rho=0.9)
    v = res["verdict"]
    assert v["rho"] == 0.9
    assert v["n_effective"] == pytest.approx(4 / (1 + 3 * 0.9), abs=1e-4)
    assert v["verdict"] == "correlated_weak"  # 10-at-0.9 style collapse at n=4


def test_independent_pass_through_matches_len_guard(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        _merge(UNANIMOUS, tmp_path / "trail.jsonl", independent=[True, True])


def test_trail_row_shape_matches_live_rows(tmp_path: Path) -> None:
    trail = tmp_path / "trail.jsonl"
    seed = ('{"ts": "2026-10-05T00:00:00Z", "actor": "research", '
            '"event": "shift_start", "detail": "seed row", "artifacts": []}\n')
    trail.write_text(seed, encoding="utf-8")
    res = _merge(DISSENTING, trail)
    rows = [json.loads(ln) for ln in trail.read_text(encoding="utf-8").splitlines() if ln]
    assert len(rows) == 2                    # append-only: the seed row survives
    row = rows[-1]
    assert set(row) == {"ts", "actor", "event", "detail", "artifacts"}
    assert row["actor"] == "research-merge"
    assert row["event"] == "CONSENSUS_MERGE"
    assert row["detail"] == res["verdict"]
    assert row["artifacts"] == []
    assert row["ts"].endswith("Z")
    datetime.fromisoformat(row["ts"].replace("Z", "+00:00"))  # parseable UTC stamp


def test_default_trail_is_the_owning_lane_trail() -> None:
    p = memweave.lane_trail("research")
    assert p == memweave.ROOT / "queue" / "lanes" / "research" / "trail.jsonl"
    assert p.is_file()                       # the live research trail read for shape


def test_lane_name_rejects_paths(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        memweave.consensus_merge(DISSENTING, "../escape", trail=tmp_path / "t.jsonl")
