#!/usr/bin/env python3
"""tests/test_gate_canary.py - tests for tools/gate_canary.py (Mickey17 W2).

Three laws under test, from the W2 brief:
  1. the canary detects a deliberately broken gate stub (fixture family
     whose gate stays silent on its own known-bad) and files the attention
     alert naming it;
  2. a canary run completes without touching the real tree (tracked mtime
     snapshot over the real repo is byte-identical before and after a full
     fixture run whose attention path is redirected to tmp);
  3. the known-bad fixture set triggers each detection path: every family's
     fired predicate on the gate's documented detection output, the plant
     functions editing exactly their targets, the fake provider token
     actually blocking in the secret scanner core, and live subprocess runs
     of the cheap pure gates (ratchet, config_seal, description_pin,
     freshness, checkbox, census) on fixture trees.

No real secret ever appears in this file: the fake token is imported from
tools/gate_canary.py, which builds it by concatenation.

Run: .venv/Scripts/python.exe -m pytest tests/test_gate_canary.py -q
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from tools import gate_canary as gc  # noqa: E402

GIT_ID = ["-c", "user.email=canary@example", "-c", "user.name=canary"]


def _git(repo: Path, *args: str, env_extra: dict | None = None) -> None:
    import os
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                       text=True, env=env)
    assert r.returncode == 0, "git %s failed: %s" % (args[:2], r.stderr)


# ------------------------------------------------------------ stub gates --
ALIVE_STUB = (
    "import sys\n"
    "from pathlib import Path\n"
    "if Path('canary_bad.txt').is_file():\n"
    "    print('STUB-GATE: FIRED known-bad present')\n"
    "    sys.exit(1)\n"
    "print('STUB-GATE: ok')\n"
)
DEAD_STUB = "print('STUB-GATE: ok')\n"  # never fires, the broken gate


def make_fixture_repo(base: Path) -> Path:
    repo = base / "repo"
    repo.mkdir(parents=True)
    (repo / "AGENTS.md").write_text("# fixture repo\n", encoding="utf-8")
    (repo / "gate_alive.py").write_text(ALIVE_STUB, encoding="utf-8")
    (repo / "gate_dead.py").write_text(DEAD_STUB, encoding="utf-8")
    _git(repo, "init", "-q")
    _git(repo, "add", "-A")
    _git(repo, *GIT_ID, "commit", "-q", "-m", "fixture base")
    return repo


def stub_family(name: str, script: str) -> gc.Family:
    def plant(wt: Path) -> list[str]:
        return gc._write(wt, "canary_bad.txt", "planted known-bad\n")

    return gc.Family(name, "stub family for tests", plant,
                     [gc.Step([script],
                              lambda ro: gc._has(ro, "STUB-GATE: FIRED", rc=1))])


def run_stub_family(base: Path, fam: gc.Family) -> tuple[dict, dict]:
    repo = make_fixture_repo(base)
    workroot = base / "work"
    wt, interp, _notes = gc.setup_worktree(repo, workroot, sparse=[], venv_link=False)
    try:
        control = gc.run_family(fam, wt, interp, plant=False)
        result = gc.run_family(fam, wt, interp, plant=True)
        isolation = not (wt / "canary_bad.txt").exists()
    finally:
        gc.teardown_worktree(repo, wt)
    assert isolation, "planted known-bad survived the family restore"
    listed = subprocess.run(["git", "-C", str(repo), "worktree", "list"],
                            capture_output=True, text=True).stdout
    assert str(wt) not in listed, "worktree registration survived teardown"
    assert not wt.exists(), "worktree dir survived teardown"
    return control, result


# ----------------------------------------------------------------- laws 1-2
def test_dead_gate_stub_detected_and_attention_filed(tmp_path):
    _c, result = run_stub_family(tmp_path, stub_family("stub_dead", "gate_dead.py"))
    assert result["state"] == "DEAD"
    assert result["steps"][0]["fired"] is None
    att = tmp_path / "attention.md"
    gc.append_attention(att, [result])
    text = att.read_text(encoding="utf-8")
    assert "[gate-canary] DEAD stub_dead" in text
    assert "stayed silent on its own known-bad" in text


def test_alive_gate_stub_fires_and_no_attention(tmp_path):
    _c, result = run_stub_family(tmp_path, stub_family("stub_alive", "gate_alive.py"))
    assert result["state"] == "ALIVE"
    assert "STUB-GATE: FIRED" in result["steps"][0]["fired"]
    att = tmp_path / "attention.md"
    gc.append_attention(att, [r for r in [result] if r["state"] != "ALIVE"])
    assert not att.exists() or "stub_alive" not in att.read_text(encoding="utf-8")


def test_control_run_on_pristine_tree_stays_quiet(tmp_path):
    control, result = run_stub_family(tmp_path, stub_family("stub_alive", "gate_alive.py"))
    assert control["state"] == "DEAD"  # nothing planted: expected quiet
    assert result["state"] == "ALIVE"


def test_crashed_step_is_blind_not_dead(tmp_path):
    fam = stub_family("stub_crash", "gate_missing.py")
    repo = make_fixture_repo(tmp_path)
    wt, interp, _n = gc.setup_worktree(repo, tmp_path / "w", sparse=[], venv_link=False)
    try:
        result = gc.run_family(fam, wt, interp, plant=True)
    finally:
        gc.teardown_worktree(repo, wt)
    assert result["state"] == "BLIND"


def test_canary_run_leaves_real_tree_untouched(tmp_path):
    # Scoped to the canary's own plant targets: sibling lanes share this tree
    # and may legitimately write elsewhere mid-test. One retry absorbs a
    # sibling burst inside the window; a real canary write reproduces on both
    # attempts (it happens inside the family run itself).
    scopes = ["AGENTS.md", "configs", "tools", "scripts", "tests",
              "watch/inbox/burn_wave_20260926", "watch/inbox/qdrop_export"]
    drift: set = set()
    for _attempt in (1, 2):
        before = gc.snapshot(REPO)
        _c, result = run_stub_family(tmp_path / "iso", stub_family("stub_a", "gate_alive.py"))
        after = gc.snapshot(REPO)
        drift = {k for k in before if k in after and before[k] != after[k]
                 and any(k == s or k.startswith(s + "/") for s in scopes)}
        if not drift:
            break
    assert result["state"] == "ALIVE"
    assert not drift, "real tree changed under a canary plant scope: %s" % sorted(drift)[:8]


# ------------------------------------------------------- law 3: predicates --
FIRED_CASES = {
    "violation_ratchet": (1, "RATCHET check: scope=1 changed files; hits=1; NEW=1\n"
                          "  NEW 1c86242d11e4a61d except-pass: tools/x.py:3\n"
                          "RATCHET: FAIL"),
    "config_seal": (1, "CONFIG-SEAL verify: sealed=9 live=9 modified=1\n"
                    "  MODIFIED  lanes.yaml\nCONFIG-SEAL: FAIL"),
    "secret_gate": (1, "blocking=1 (threshold=high, provider shapes only)\n"
                    "  tools/x.py:1:GITHUB-TOKEN:high masked=ghp_...(len=40)\n"
                    "exit=1 BLOCKING findings present"),
    "census_drift_patrol": (1, "CENSUS-PATROL: STALE - census 28d old (bar 7d)"),
    "freshness_gate": (2, "FRESHNESS-GATE: FAIL r.md (stamp 2026-01-01 is 241d old; bar is 14d)"),
    "checkbox_receipt_gate": (1, "CHECKBOX-RECEIPT-GATE: 3 checked Open rows, 0 baseline, 1 offenders\n"
                              "  NEW DEBT: B2-9999\nCHECKBOX-RECEIPT-GATE: FAIL"),
    "description_pin": (2, "configs/tools/c.json: canary_tool: description unpinned and unmarked"),
    "caption_ledger_verify": (1, "RESULT: FAIL - 191 rows, check7 mismatch"),
    "refold_gate": (1, "REFOLD-GATE: FAIL, fold pins red\n  FAILED tests/test_index_fold_host.py::x"),
    "workflow_gate_scenarios": (2, "SCENARIOS FAIL G1_multiplicity.card.json: verdict FAIL != expected PASS"),
}


@pytest.mark.parametrize("name", sorted(FIRED_CASES))
def test_known_bad_fixture_fires_each_detection_path(name):
    fam = next(f for f in gc.FAMILIES if f.name == name)
    rc, out = FIRED_CASES[name]
    step = fam.steps[-1]  # the detector step (arming helper first when present)
    assert step.fired((rc, out)) is not None, "%s stayed silent on its known-bad" % name


@pytest.mark.parametrize("name", sorted(FIRED_CASES))
def test_silent_gate_does_not_count_as_fired(name):
    fam = next(f for f in gc.FAMILIES if f.name == name)
    detector = fam.steps[-1]  # the detector step; the arming helper is rc-only
    assert detector.fired((0, "all quiet\n")) is None
    assert detector.fired((1, "some unrelated output\n")) is None


def test_armed_helper_step_requires_exit_one():
    fam = next(f for f in gc.FAMILIES if f.name == "caption_ledger_verify")
    arm = fam.steps[0]
    assert arm.fired((1, "changed")) is not None
    assert arm.fired((0, "unchanged")) is None


# --------------------------------------------------- law 3: plants + token --
MINI_QUEUE = "## Dispensed\n\nrow\n\n## Open\n\n- [ ] open row\n"
MINI_CARRIER = "- **Tests:** 2,303 tests collected / 352 files (2026-09-27 census, rest)\n"
MINI_HOST = (
    "function seqOrderKey(ev) {\n"
    "  const s = ev.seq;\n"
    "  if (typeof s === 'number') {\n"
    "    if (Number.isSafeInteger(s)) return { tier: 2, seq: BigInt(s) };\n"
    "    if (Number.isInteger(s)) return { tier: 1, seq: BigInt(s) };\n"
    "    return { tier: 0, seq: null };\n"
    "  }\n"
    "  if (typeof s === 'string' && /^\\d+$/.test(s)) return { tier: 2, seq: BigInt(s) };\n"
    "  return { tier: 0, seq: null };\n"
    "}\n"
)


def mini_tree(tmp: Path) -> Path:
    wt = tmp / "wt"
    (wt / "watch/inbox/burn_wave_20260926").mkdir(parents=True)
    (wt / "watch/inbox/burn_wave_20260926/QUEUE.md").write_text(MINI_QUEUE)
    (wt / "configs/workflow_gate_scenarios").mkdir(parents=True)
    (wt / "tools").mkdir()
    (wt / "tools/workflow_gate.py").write_text("# stub gate\n")
    (wt / "AGENTS.md").write_text("preamble\n" + MINI_CARRIER)
    (wt / "scripts").mkdir()
    (wt / "scripts/index_fold_host.mjs").write_text(MINI_HOST)
    (wt / "configs/workflow_gate_scenarios/G1_multiplicity.card.json").write_text(
        '{"expected_verdict": {"overall": "FAIL"}}')
    return wt


def fam(name: str) -> gc.Family:
    return next(f for f in gc.FAMILIES if f.name == name)


def test_plants_edit_exactly_their_targets(tmp_path):
    wt = mini_tree(tmp_path)
    fam("census_drift_patrol").plant(wt)
    assert "(2026-09-01 census" in (wt / "AGENTS.md").read_text()
    fam("checkbox_receipt_gate").plant(wt)
    q = (wt / "watch/inbox/burn_wave_20260926/QUEUE.md").read_text()
    assert "- [x] B2-9999 gate canary row, no receipt anywhere\n" in q
    fam("refold_gate").plant(wt)
    h = (wt / "scripts/index_fold_host.mjs").read_text()
    assert "SafeInteger(s)) return { tier: 1," in h and "isInteger(s)) return { tier: 2," in h
    fam("workflow_gate_scenarios").plant(wt)
    assert '"overall": "PASS"' in (wt / "configs/workflow_gate_scenarios/"
                                   "G1_multiplicity.card.json").read_text()


def test_plant_raises_when_shape_missing(tmp_path):
    wt = tmp_path / "wt"
    wt.mkdir()
    (wt / "AGENTS.md").write_text("no carrier here\n")
    with pytest.raises(gc.PlantError):
        fam("census_drift_patrol").plant(wt)


def test_fake_token_blocks_in_secret_scan_core(tmp_path):
    from tools import secret_gate_scan as sgs
    planted = tmp_path / "planted_bad.py"
    planted.write_text("PLANTED = %r\n" % gc.FAKE_GH_TOKEN, encoding="utf-8")
    res = sgs.scan([str(planted)], {}, [], "high")
    kinds = {b["kind"] for b in res["blocking"]}
    assert "GITHUB-TOKEN" in kinds and res["blocking_count"] >= 1
    # the canary's own source (token built by concatenation) stays clean
    own = sgs.scan([str(REPO / "tools" / "gate_canary.py")], {}, [], "high")
    assert own["blocking_count"] == 0


# ---------------------------------------------------- law 3: live gate runs --
def run_py(args: list[str], cwd: Path | None = None) -> tuple[int, str]:
    p = subprocess.run([sys.executable, *args], cwd=str(cwd) if cwd else None,
                       capture_output=True, text=True, errors="replace")
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def test_live_description_pin_fires_on_unpinned_manifest(tmp_path):
    d = tmp_path / "manifests"
    d.mkdir()
    (d / "m.json").write_text('{"tools": [{"name": "canary_tool",'
                              ' "description": "no version"}]}')
    rc, out = run_py([str(REPO / "tools/description_pin.py"), str(d)])
    assert rc == 2 and "canary_tool" in out and "unpinned" in out


def test_live_freshness_gate_fires_on_stale_stamp(tmp_path):
    r = tmp_path / "stale.md"
    r.write_text("source-fetched: 2026-01-01\n")
    rc, out = run_py([str(REPO / "tools/freshness_gate.py"), str(r)])
    assert rc == 2 and "FRESHNESS-GATE: FAIL" in out


def test_live_checkbox_gate_fires_on_receiptless_row(tmp_path):
    q = tmp_path / "QUEUE.md"
    q.write_text("## Open\n\n- [x] B2-9999 no receipt at all\n")
    rc, out = run_py([str(REPO / "tools/checkbox_receipt_gate.py"), "--queue", str(q)])
    assert rc == 1 and "B2-9999" in out and "FAIL" in out


def test_live_config_seal_fires_on_modified_config(tmp_path):
    root = tmp_path / "cs"
    (root / "tools").mkdir(parents=True)
    (root / "configs").mkdir()
    shutil.copy(REPO / "tools/config_seal.py", root / "tools/config_seal.py")
    (root / "configs/app.json").write_text('{"a": 1}\n')
    script = str(root / "tools/config_seal.py")
    rc, out = run_py([script, "update", "--by", "t", "--note", "fixture"])
    assert rc == 0, out
    (root / "configs/app.json").write_text('{"a": 2}\n')
    rc, out = run_py([script, "verify"])
    assert rc == 1 and "MODIFIED" in out and "FAIL" in out


def test_live_ratchet_fires_on_new_violation(tmp_path):
    root = tmp_path / "rr"
    (root / "tools").mkdir(parents=True)
    (root / "configs").mkdir()
    shutil.copy(REPO / "tools/violation_ratchet.py", root / "tools/violation_ratchet.py")
    (root / "configs/violation_baseline.json").write_text('{"version": 1, "accepted": {}}')
    _git(root, "init", "-q")
    _git(root, "add", "-A")
    _git(root, *GIT_ID, "commit", "-q", "-m", "base")
    (root / "tools/bad.py").write_text("try:\n    x = 1\nexcept Exception:\n    pass\n")
    rc, out = run_py([str(root / "tools/violation_ratchet.py"), "check", "--changed"],
                     cwd=root)
    assert rc == 1 and "NEW" in out and "except-pass" in out and "RATCHET: FAIL" in out


def test_live_census_patrol_fires_on_stale_carrier(tmp_path):
    root = tmp_path / "cp"
    (root / "tools").mkdir(parents=True)
    (root / "tests").mkdir()
    shutil.copy(REPO / "tools/census_drift_patrol.py", root / "tools/census_drift_patrol.py")
    (root / "AGENTS.md").write_text("- **Tests:** 10 tests collected / 5 files"
                                    " (2026-09-01 census, fixture)\n")
    (root / "tests/test_a.py").write_text("def test_a():\n    pass\n")
    _git(root, "init", "-q")
    _git(root, "add", "-A")
    when = {"GIT_AUTHOR_DATE": "2026-09-20T12:00:00", "GIT_COMMITTER_DATE": "2026-09-20T12:00:00"}
    _git(root, *GIT_ID, "commit", "-q", "-m", "grow tests", env_extra=when)
    rc, out = run_py([str(root / "tools/census_drift_patrol.py"), "--root", str(root)])
    assert rc == 1 and "CENSUS-PATROL: STALE" in out
