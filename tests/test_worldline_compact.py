"""worldline_compact tests (night shift 2026-10-04, free-lane draft).

Fixture law: everything runs on tmp_path - a couple of fake dwf- actor seeds
sharing identical genome+invariants slabs (one newer than the rest, the keeper),
a divergent dwf seed (its own minute), and one seat seed that must never be
compacted. The three contracts under test:

  --check    counts prefixes, bytes, ages, and the newest-of-minute dedupe
             potential; JSON rides between the marker lines.
  --plan     writes ONE markdown plan grouping identical-slab seeds into
             lineage rows (keeper = newest, members with sha256s) and touches
             no seed file.
  --execute  fail-closed: refuses without BOTH WORLDLINE_COMPACT_GO=1 and
             --plan <file>; under GO it MOVES members to _compact_archive
             (never unlink) and leaves keeper + seat seeds in place; a stale
             plan aborts before the first move.

The estate law this battery pins (operator brief 2026-10-04): NEVER delete
sibling data without operator GO. Receipt: watch/inbox/night_shift_20261004/
worldline_compact_tool.md.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import tools.worldline_compact as wc  # noqa: E402
from tools.worldline_compact_io import JSON_BEGIN, JSON_END, parse_plan_file  # noqa: E402

MIN = "2026-10-03T21:00"


def _mk_seed(root: Path, name: str, created: str, skill_count: int = 2, tape_n: int = 1) -> Path:
    """One fake seed dir: identical genome/invariants when skill_count matches."""
    d = root / name
    d.mkdir(parents=True)
    doc = {
        "schema_version": 1,
        "kind": "worldline_seed",
        "created_utc": created,
        "session_id": name,
        "consent": {"replication": "operator-gated", "egress": "none"},
        "seed_hash": hashlib.sha256(name.encode()).hexdigest()[:16],
        "slabs": {
            "genome": {"agents_md": {"path": "AGENTS.md", "sha256": "aa" * 8},
                        "skills": ["chan", "memlance", "salon"], "skill_count": skill_count},
            "invariants": {"memory_md": {"path": "MEMORY.md", "sha256": "bb" * 8},
                            "curator_rule": "one rule", "curator_list": [], "curator_stats": {}},
            "organs": {"mcp_config": {}, "secrets": "redacted"},
            "record": {"tape_ref": {"row": tape_n}, "knot_ref": {}, "selector": {}},
            "position": {"chain_tip": {"tip": f"{tape_n:064x}"}, "minute_span": {}, "prev_seed": None},
        },
    }
    (d / "SEED.json").write_text(json.dumps(doc, indent=1), encoding="utf-8")
    return d


@pytest.fixture()
def grove(tmp_path: Path) -> Path:
    wl = tmp_path / "worldline"
    wl.mkdir()
    _mk_seed(wl, "dwf-dwfrun-11111111-1111-1111-1111-111111111111-actor_1_1", f"{MIN}:05Z", tape_n=1)
    _mk_seed(wl, "dwf-dwfrun-11111111-1111-1111-1111-111111111111-actor_1_2", f"{MIN}:40Z", tape_n=2)  # newest -> keeper
    _mk_seed(wl, "dwf-dwfrun-11111111-1111-1111-1111-111111111111-actor_1_3", f"{MIN}:12Z", tape_n=3)
    _mk_seed(wl, "dwf-dwfrun-22222222-2222-2222-2222-222222222222-actor_2_1", "2026-10-03T21:05:00Z",
             skill_count=3, tape_n=4)  # divergent genome, own minute: stays
    _mk_seed(wl, "sess_20261003_night", "2026-10-03T22:00:00Z", tape_n=5)  # seat: never compacted
    (wl / "REGISTRY.jsonl").write_text('{"kind": "seed_registry_row"}\n', encoding="utf-8")
    return wl


def _seed_bytes(wl: Path) -> dict[str, bytes]:
    return {p.parent.name: p.read_bytes()
            for p in sorted(wl.rglob("SEED.json"))}


def _json_of(out: str) -> dict:
    body = out[out.index(JSON_BEGIN) + len(JSON_BEGIN):out.index(JSON_END)].strip()
    return json.loads(body)


def test_check_counts_prefixes_and_dedupe(grove: Path, capsys: pytest.CaptureFixture):
    rc = wc.main(["--check", "--root", str(grove)])
    out = capsys.readouterr().out
    assert rc == 0
    r = _json_of(out)
    assert r["prefixes"]["dwf"]["count"] == 4
    assert r["prefixes"]["seat"]["count"] == 1
    assert r["totals"]["seed_dirs"] == 5
    assert r["prefixes"]["dwf"]["runs"] == 2
    d = r["dedupe"]
    assert d["compactable_seeds"] == 2  # actor_1_1 + actor_1_3 vs newest-of-minute actor_1_2
    assert d["keepers"] == 2  # the 21:00 minute + the singleton 21:05 minute
    assert d["multi_variant_minutes"] == 0
    assert d["unkeyed_dwf_seeds"] == 0
    assert d["compactable_bytes"] == sum(
        (grove / n / "SEED.json").stat().st_size
        for n in ("dwf-dwfrun-11111111-1111-1111-1111-111111111111-actor_1_1",
                  "dwf-dwfrun-11111111-1111-1111-1111-111111111111-actor_1_3"))
    assert r["other_files"] == [{"name": "REGISTRY.jsonl", "bytes": 31}]
    assert "<1d" in r["prefixes"]["dwf"]["age_buckets"]


def test_check_missing_root_exits_2(tmp_path: Path, capsys: pytest.CaptureFixture):
    rc = wc.main(["--check", "--root", str(tmp_path / "nope")])
    assert rc == 2
    assert "cannot verify" in capsys.readouterr().out


def test_plan_groups_keeper_newest_and_touches_no_seed(grove: Path, tmp_path: Path,
                                                       capsys: pytest.CaptureFixture):
    before = _seed_bytes(grove)
    plan_path = tmp_path / "plan.md"
    rc = wc.main(["--plan", str(plan_path), "--root", str(grove)])
    out = capsys.readouterr().out
    assert rc == 0 and plan_path.is_file() and "seeds touched: 0" in out
    assert _seed_bytes(grove) == before  # read-only over the seeds
    plan = parse_plan_file(plan_path)
    assert plan is not None and plan["worldline_dir"] == grove.resolve().as_posix()
    (groups := plan["groups"])
    assert len(groups) == 1  # the divergent 21:05 seed is a singleton, not a group
    g = groups[0]
    assert g["minute"] == MIN
    assert g["keeper"]["dir_name"] == "dwf-dwfrun-11111111-1111-1111-1111-111111111111-actor_1_2"
    assert sorted(m["dir_name"] for m in g["members"]) == [
        "dwf-dwfrun-11111111-1111-1111-1111-111111111111-actor_1_1",
        "dwf-dwfrun-11111111-1111-1111-1111-111111111111-actor_1_3"]
    for m in g["members"]:
        assert m["seed_sha256"] == hashlib.sha256((grove / m["dir_name"] / "SEED.json").read_bytes()).hexdigest()
    assert all(not m["dir_name"].startswith("sess_") for gg in groups for m in gg["members"])
    md = plan_path.read_text(encoding="utf-8")
    assert "WORLDLINE_COMPACT_GO=1" in md and "never deletes" in md  # the law block rides the plan


def test_plan_refuses_to_overwrite_existing_artifact(grove: Path, tmp_path: Path,
                                                     capsys: pytest.CaptureFixture):
    plan_path = tmp_path / "plan.md"
    assert wc.main(["--plan", str(plan_path), "--root", str(grove)]) == 0
    rc = wc.main(["--plan", str(plan_path), "--root", str(grove)])
    assert rc == 2 and "already exists" in capsys.readouterr().out


def _plan_for(grove: Path, tmp_path: Path) -> Path:
    plan_path = tmp_path / "plan.md"
    assert wc.main(["--plan", str(plan_path), "--root", str(grove)]) == 0
    return plan_path


def test_execute_refuses_without_go(grove: Path, tmp_path: Path, monkeypatch, capsys):
    monkeypatch.delenv(wc.GO_ENV, raising=False)
    plan_path = _plan_for(grove, tmp_path)
    rc = wc.main(["--execute", "--plan", str(plan_path), "--root", str(grove)])
    out = capsys.readouterr().out
    assert rc == 2 and "REFUSED" in out and wc.GO_ENV in out and "THE ASK (operator)" in out
    assert (grove / "dwf-dwfrun-11111111-1111-1111-1111-111111111111-actor_1_1").is_dir()  # nothing moved


def test_execute_refuses_with_go_but_no_plan_file(grove: Path, monkeypatch, capsys):
    monkeypatch.setenv(wc.GO_ENV, "1")
    rc = wc.main(["--execute", "--root", str(grove)])
    out = capsys.readouterr().out
    assert rc == 2 and "--plan" in out and "REFUSED" in out
    assert _seed_bytes(grove)  # tree untouched


def test_execute_under_go_moves_members_never_deletes(grove: Path, tmp_path: Path,
                                                      monkeypatch, capsys):
    monkeypatch.setenv(wc.GO_ENV, "1")
    before = _seed_bytes(grove)
    plan_path = _plan_for(grove, tmp_path)
    plan = parse_plan_file(plan_path)
    rc = wc.main(["--execute", "--plan", str(plan_path), "--root", str(grove)])
    out = capsys.readouterr().out
    assert rc == 0 and "EXECUTE ok" in out
    m1 = "dwf-dwfrun-11111111-1111-1111-1111-111111111111-actor_1_1"
    m3 = "dwf-dwfrun-11111111-1111-1111-1111-111111111111-actor_1_3"
    keeper = "dwf-dwfrun-11111111-1111-1111-1111-111111111111-actor_1_2"
    divergent = "dwf-dwfrun-22222222-2222-2222-2222-222222222222-actor_2_1"
    assert not (grove / m1).exists() and not (grove / m3).exists()  # moved out
    archive = grove / "_compact_archive" / plan["stamp"]
    for name in (m1, m3):
        moved = archive / name / "SEED.json"
        assert moved.is_file() and moved.read_bytes() == before[name]  # byte-identical, never deleted
    assert (grove / keeper / "SEED.json").read_bytes() == before[keeper]  # keeper stays
    assert (grove / divergent / "SEED.json").read_bytes() == before[divergent]  # singleton stays
    assert (grove / "sess_20261003_night" / "SEED.json").read_bytes() == before["sess_20261003_night"]
    rows = [json.loads(ln) for ln in (grove / "_compact_archive" / "MANIFEST.jsonl").read_text(encoding="utf-8").splitlines()]
    assert {r["session_id"] for r in rows} == {m1, m3}
    assert all(r["op"] == "worldline-compact-move" and r["plan_sha256"] for r in rows)


def test_execute_stale_plan_fails_closed_before_any_move(grove: Path, tmp_path: Path,
                                                        monkeypatch, capsys):
    monkeypatch.setenv(wc.GO_ENV, "1")
    plan_path = _plan_for(grove, tmp_path)
    m1 = "dwf-dwfrun-11111111-1111-1111-1111-111111111111-actor_1_1"
    doc = json.loads((grove / m1 / "SEED.json").read_text(encoding="utf-8"))
    doc["slabs"]["genome"]["skill_count"] = 99  # mutate AFTER the plan: slab no longer matches
    (grove / m1 / "SEED.json").write_text(json.dumps(doc, indent=1), encoding="utf-8")
    rc = wc.main(["--execute", "--plan", str(plan_path), "--root", str(grove)])
    out = capsys.readouterr().out
    assert rc == 2 and "stale tree" in out
    assert (grove / m1).is_dir() and (grove / "dwf-dwfrun-11111111-1111-1111-1111-111111111111-actor_1_3").is_dir()
    assert not (grove / "_compact_archive").exists()  # verify-then-move: nothing moved at all


def test_execute_refuses_plan_root_mismatch(grove: Path, tmp_path: Path, monkeypatch, capsys):
    monkeypatch.setenv(wc.GO_ENV, "1")
    plan_path = _plan_for(grove, tmp_path)
    other_root = tmp_path / "other_worldline"
    other_root.mkdir()
    rc = wc.main(["--execute", "--plan", str(plan_path), "--root", str(other_root)])
    out = capsys.readouterr().out
    assert rc == 2 and "does not match live root" in out
