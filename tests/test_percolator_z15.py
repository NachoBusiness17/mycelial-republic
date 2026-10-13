"""Z15 percolator count laws (2026-09-29) — decay, MAX-merge, self-emission cap.

S15 diagnosis (configs/mates.yaml: "the percolator's memorization is an exploit played
by the loop on itself", 232,214 self-reinforcements = 79.8% of all events) fixed in
mag/percolator.py. Receipt: watch/inbox/hydrology/Z15_PERCOLATOR_FIX.md.

Laws under test:
  1. half-life decay — count halves every half_life_days (default 30) without
     reinforcement, floor 1 (time alone never erases an observed invariant);
  2. heal-merge MAX — seal/live shared counts merge by max(), idempotent under
     repeated heals (the old SUM triple-counted, heal.log 2026-09-06..09-26);
  3. self-emission cap — same source reinforcing the same invariant within one
     cycle (UTC day) counts once per cycle, not once per repetition.

Every test runs against a tmp_path world (registry/seals/noise/explore/config all
redirected; fact_bus.publish_fact and destructive_receipt.record stubbed) — the live
memory/percolator/invariants.json is never touched, same discipline as
mag/percolator_heal_test.py make_world.
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from mag import percolator

SIGNAL_TEXT = "the training signal invariant: we built a procedure mechanism"


def _iso(dt: datetime) -> str:
    return dt.isoformat().replace("+00:00", "Z")


@pytest.fixture
def world(tmp_path, monkeypatch):
    """Isolated percolator world; restores every patched module path on teardown."""
    monkeypatch.setattr(percolator, "INVARIANT_REGISTRY", tmp_path / "invariants.json")
    monkeypatch.setattr(percolator, "SEALS_DIR", tmp_path / "seals")
    monkeypatch.setattr(percolator, "NOISE_DIR", tmp_path / "noise")
    monkeypatch.setattr(percolator, "EXPLORE_QUEUE", tmp_path / "explore.jsonl")
    # no config file in the tmp world -> in-code defaults (half_life 30d, cap on)
    monkeypatch.setattr(percolator, "PERCOLATOR_CFG", tmp_path / "percolator.json")
    monkeypatch.setattr(percolator, "_cfg_cache",
                        {"mtime": None, "data": dict(percolator._CFG_DEFAULTS)})
    # keep the live tree byte-still: no facts, no destructive-receipt ledger rows
    monkeypatch.setattr("mag.fact_bus.publish_fact",
                        lambda *a, **k: {"ok": True, "stub": True})
    monkeypatch.setattr("mag.destructive_receipt.record",
                        lambda *a, **k: {"ok": True, "stub": True})
    return tmp_path


def _write_registry(tmp_path: Path, invs: dict, false_positives: int = 0) -> None:
    (tmp_path / "invariants.json").write_text(
        json.dumps({"invariants": invs, "false_positives": false_positives}, ensure_ascii=False),
        encoding="utf-8")


def _read_registry(tmp_path: Path) -> dict:
    return json.loads((tmp_path / "invariants.json").read_text(encoding="utf-8"))


# ── law 1: half-life decay math (pure function) ──────────────────────────────

def test_decay_math_exact_halvings():
    assert percolator._decay_count(100, 0, half_life_days=30) == 100      # no time, no decay
    assert percolator._decay_count(100, 30, half_life_days=30) == 50      # one half-life
    assert percolator._decay_count(100, 60, half_life_days=30) == 25      # two half-lives
    assert percolator._decay_count(100, 15, half_life_days=30) == 70      # 70.71 floors to 70
    assert percolator._decay_count(64, 8, half_life_days=8) == 32         # generic half-life


def test_decay_math_cycle_quantization():
    # law 1's clock is the UTC-day cycle (law 3): sub-day remainders never decay
    assert percolator._decay_count(100, 0.999, half_life_days=30) == 100  # same-cycle repeat
    assert percolator._decay_count(100, 29.9, half_life_days=30) == 51    # 29 whole cycles
    assert percolator._decay_count(100, 30.9, half_life_days=30) == 50    # 30 whole cycles


def test_decay_math_floor_and_disable():
    assert percolator._decay_count(1, 10_000, half_life_days=30) == 1     # floor: never to 0
    assert percolator._decay_count(5, -3, half_life_days=30) == 5         # future timestamp
    assert percolator._decay_count(9, 45, half_life_days=0) == 9          # hl<=0 disables law


def test_decay_default_reads_config():
    # tmp world has no config file -> the default half-life of 30 days applies
    assert percolator._decay_count(64, 30) == 32


def test_runtime_decay_on_repeat(world):
    """A repeat after ~30 idle days: 30 whole cycles elapsed -> 100 halves to 50, +1 = 51."""
    now = datetime.now(timezone.utc)
    canonical = percolator._canonical_hex([SIGNAL_TEXT])
    _write_registry(world, {canonical: {
        "text": SIGNAL_TEXT, "count": 100,
        "first_seen": _iso(now - timedelta(days=31)),
        "last_seen": _iso(now - timedelta(days=30)),   # pre-Z15 row: no decay_as_of yet
        "domain": "test"}})
    res = percolator.percolate(SIGNAL_TEXT, source="unit-test", domain="test")
    assert res["verdict"] == "repeat"
    assert res["count"] == 51  # decay(100, 30 whole cycles) = 50, +1 for this observation
    inv = _read_registry(world)["invariants"][canonical]
    assert inv["decay_as_of"]  # baseline stamped so a rerun decays only the fresh interval


def test_runtime_no_decay_within_same_baseline(world):
    """Back-to-back observations (milliseconds apart) do not decay: 100 -> 101."""
    canonical = percolator._canonical_hex([SIGNAL_TEXT])
    _write_registry(world, {canonical: {
        "text": SIGNAL_TEXT, "count": 100,
        "last_seen": _iso(datetime.now(timezone.utc)), "domain": "test"}})
    res = percolator.percolate(SIGNAL_TEXT, source="unit-test", domain="test")
    assert res["count"] == 101  # sub-half-life elapsed floors to zero decay


# ── law 2: heal-merge takes MAX (idempotent), not SUM ────────────────────────

def _make_seal_world(world, seal_gens, live_gens):
    seal_dir = world / "seals" / "2026-09-26T09-03-57" / "memory" / "percolator"
    seal_dir.mkdir(parents=True)
    (seal_dir / "invariants.json").write_text(
        json.dumps({"invariants": seal_gens, "false_positives": 0}, ensure_ascii=False),
        encoding="utf-8")
    _write_registry(world, live_gens)
    return seal_dir / "invariants.json"


def test_heal_merge_takes_max_not_sum(world):
    """Heal fires via the missing-ID diff (S1 sealed, absent from live). Shared S2:
    MAX(10 seal, 12 live) = 12 — the old SUM said 22."""
    seal = {"S1": {"text": "gen 1", "count": 10, "first_seen": "2026-09-01T00:00:00Z",
                   "last_seen": "2026-09-26T00:00:00Z", "domain": "test"},
            "S2": {"text": "gen 2", "count": 10, "first_seen": "2026-09-01T00:00:00Z",
                   "last_seen": "2026-09-26T00:00:00Z", "domain": "test"}}
    live_s2 = dict(seal["S2"], count=12)  # live outgrew the seal between heals
    _make_seal_world(world, seal, {"S2": live_s2})
    got = percolator._load_registry()
    assert got["invariants"]["S1"]["count"] == 10  # restored from seal, no live to sum
    assert got["invariants"]["S2"]["count"] == 12  # MAX(10, 12); SUM said 10 + 12 = 22


def test_heal_merge_idempotent_across_repeated_heals(world):
    """The triple-counting falsifier, in the production shape: live already holds the
    sealed count (a prior heal was saved), then partial loss re-triggers the heal —
    N rounds of seal+live re-merge must NOT inflate the shared count. SUM said
    10 -> 20 -> 40 -> 80; MAX holds 10 forever."""
    seal = {"S1": {"text": "gen 1", "count": 10, "first_seen": "2026-09-01T00:00:00Z",
                   "last_seen": "2026-09-26T00:00:00Z", "domain": "test"},
            "S2": {"text": "gen 2", "count": 5, "first_seen": "2026-09-01T00:00:00Z",
                   "last_seen": "2026-09-26T00:00:00Z", "domain": "test"}}
    _make_seal_world(world, seal, {"S1": dict(seal["S1"])})  # S1 survived at sealed count
    for i in range(3):  # heal.log 2026-09-06..09-26: repeated heals riding one seal
        got = percolator._load_registry()  # S2 missing -> ID diff fires the heal
        assert got["invariants"]["S1"]["count"] == 10, f"heal #{i + 1} inflated the count"
        # the writer persists S1 between heals while S2 is lost again (the amnesia shape)
        _write_registry(world, {"S1": got["invariants"]["S1"]})


def test_heal_merge_keeps_cap_ledger_from_fresher_side(world):
    """Shared gen where live is fresher: the law-3 cycle ledger rides along with last_seen."""
    seal = {"S1": {"text": "gen 1", "count": 10, "first_seen": "2026-09-01T00:00:00Z",
                   "last_seen": "2026-09-26T00:00:00Z", "domain": "test"},
            "S2": {"text": "gen 2", "count": 10, "first_seen": "2026-09-01T00:00:00Z",
                   "last_seen": "2026-09-26T00:00:00Z", "domain": "test"}}
    live_s2 = {"S2": {"text": "gen 2 live", "count": 4, "first_seen": "2026-09-28T00:00:00Z",
                      "last_seen": "2026-09-29T00:00:00Z", "domain": "test",
                      "decay_as_of": "2026-09-29T00:00:00Z",
                      "cycle_hits": {"pro-fire": "2026-09-29"}}}
    _make_seal_world(world, seal, live_s2)  # S1 missing from live -> ID diff fires the heal
    got = percolator._load_registry()
    assert got["invariants"]["S2"]["count"] == 10  # MAX(10, 4)
    assert got["invariants"]["S2"]["last_seen"] == "2026-09-29T00:00:00Z"
    assert got["invariants"]["S2"]["cycle_hits"] == {"pro-fire": "2026-09-29"}


# ── law 3: self-emission cap (once per source per cycle) ─────────────────────

def test_self_emission_cap_same_source_same_cycle(world):
    percolator.percolate(SIGNAL_TEXT, source="pro-fire", domain="test")
    for _ in range(5):  # the exploit shape: the same steer fired 5x in one day
        res = percolator.percolate(SIGNAL_TEXT, source="pro-fire", domain="test")
        assert res["capped"] is True
        assert res["count"] == 1  # once per cycle, not once per repetition
    canonical = percolator._canonical_hex([SIGNAL_TEXT])
    assert _read_registry(world)["invariants"][canonical]["count"] == 1


def test_self_emission_cap_different_source_counts(world):
    percolator.percolate(SIGNAL_TEXT, source="pro-fire", domain="test")
    res = percolator.percolate(SIGNAL_TEXT, source="chord", domain="test")
    assert res["capped"] is False and res["count"] == 2
    res = percolator.percolate(SIGNAL_TEXT, source="pro-fire", domain="test")
    assert res["capped"] is True and res["count"] == 2  # A,B,A in one day: each source once


def test_self_emission_cap_new_cycle_counts_again(world, monkeypatch):
    percolator.percolate(SIGNAL_TEXT, source="pro-fire", domain="test")
    tomorrow = datetime.now(timezone.utc) + timedelta(days=1)
    monkeypatch.setattr(percolator, "_cycle_key",
                        lambda now=None: tomorrow.date().isoformat())
    res = percolator.percolate(SIGNAL_TEXT, source="pro-fire", domain="test")
    assert res["capped"] is False and res["count"] == 2  # next cycle: counts again


def test_self_emission_cap_off_via_config(world):
    percolator.PERCOLATOR_CFG.write_text(
        json.dumps({"self_emission_cap": False}), encoding="utf-8")
    percolator._cfg_cache.update(mtime=None)  # force reload
    percolator.percolate(SIGNAL_TEXT, source="pro-fire", domain="test")
    res = percolator.percolate(SIGNAL_TEXT, source="pro-fire", domain="test")
    assert res["capped"] is False and res["count"] == 2  # opt-out honored


# ── maintenance backfill (dry/apply) ─────────────────────────────────────────

def test_maintenance_dry_then_apply(world):
    """The 232,214 shape: cap to observed days, then decay from last_seen; dry never writes."""
    now = datetime.now(timezone.utc)
    canonical = percolator._canonical_hex([SIGNAL_TEXT])
    invs = {canonical: {"text": SIGNAL_TEXT, "count": 232_214,
                        "first_seen": _iso(now - timedelta(days=28)),
                        "last_seen": _iso(now - timedelta(days=2)), "domain": "test"}}
    _write_registry(world, invs)
    dry = percolator.maintenance(dry=True)
    assert dry["ok"] and dry["dry"] is True
    # cap: min(232214, 27 observed days) = 27; decay: 27 * 0.5**(2/30) = 25.78 -> 25
    assert dry["top_after"][0]["count"] == 25
    assert _read_registry(world)["invariants"][canonical]["count"] == 232_214  # dry: no write
    applied = percolator.maintenance(dry=False)
    assert applied["backup"] and Path(applied["backup"]).is_file()
    reg = _read_registry(world)
    assert reg["invariants"][canonical]["count"] == 25
    backup_reg = json.loads(Path(applied["backup"]).read_text(encoding="utf-8"))
    assert backup_reg["invariants"][canonical]["count"] == 232_214  # pre-edit bytes preserved


def test_maintenance_rerun_does_not_compound(world):
    """decay_as_of is stamped on apply: an immediate rerun decays ~zero fresh interval."""
    now = datetime.now(timezone.utc)
    canonical = percolator._canonical_hex([SIGNAL_TEXT])
    _write_registry(world, {canonical: {"text": SIGNAL_TEXT, "count": 1_000,
                                        "first_seen": _iso(now - timedelta(days=90)),
                                        "last_seen": _iso(now - timedelta(days=90)),
                                        "domain": "test"}})
    first = percolator.maintenance(dry=False)
    second = percolator.maintenance(dry=False)  # milliseconds later, baseline already stamped
    assert second["top_after"][0]["count"] == first["top_after"][0]["count"] == 1
    # 1000 capped to 1 observed day -> 1; decay 90d floors at 1; rerun decays nothing new
