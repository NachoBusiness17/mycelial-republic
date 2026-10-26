"""riddler_veil tests - the code-as-law organ must itself be truthful.

Covers: party-term detection, copy-through 8-grams, stands declaration,
certified-grade truth requirement, and the init path. Uses tmp_path registries
written directly (the tool reads fixed state/riddler paths, so tests monkeypatch
the module's path constants - never the real state/ files).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import riddler_veil as rv  # noqa: E402


def _mk(tmp_path: Path, parties: list, stands: list):
    parties_path = tmp_path / "parties.json"
    stands_path = tmp_path / "stands.json"
    parties_path.write_text(json.dumps({"parties": parties}), encoding="utf-8")
    stands_path.write_text(json.dumps({"stands": stands}), encoding="utf-8")
    return parties_path, stands_path


PARTY = [{"id": "p1", "names": ["Harbor King"], "handles": ["harbor_king"], "orgs": ["Toll Co"]}]
STAND = [{"id": "trust-salted-fish", "text": "trust is the fish you salted yourself"}]


def test_party_name_hit_is_violation(tmp_path):
    p, s = _mk(tmp_path, PARTY, STAND)
    parable = tmp_path / "parable.md"
    parable.write_text("stands: trust-salted-fish\n\nThe Harbor King ruled the port.\n", encoding="utf-8")
    parties = json.loads(p.read_text())
    stands = json.loads(s.read_text())
    violations, _ = rv.check_parable(parable, [], parties, stands)
    assert any("NO-DOX" in v and "Harbor King" in v for v in violations)


def test_clean_parable_passes(tmp_path):
    p, s = _mk(tmp_path, PARTY, STAND)
    parable = tmp_path / "parable.md"
    parable.write_text("stands: trust-salted-fish\n\nThe council weighed dead fish and starved false weighers.\n",
                       encoding="utf-8")
    violations, _ = rv.check_parable(parable, [], json.loads(p.read_text()), json.loads(s.read_text()))
    assert violations == []


def test_copy_through_8gram_caught(tmp_path):
    p, s = _mk(tmp_path, PARTY, STAND)
    source = tmp_path / "thread.md"
    parable = tmp_path / "parable.md"
    raw = "we should absolutely ship the payment leg before the harbor audit next tuesday morning"
    source.write_text(raw, encoding="utf-8")
    parable.write_text("stands: trust-salted-fish\n\nPlan: " + raw + "\n", encoding="utf-8")
    violations, _ = rv.check_parable(parable, [source], json.loads(p.read_text()), json.loads(s.read_text()))
    assert any("COPY-THROUGH" in v for v in violations)


def test_missing_stands_header_fails(tmp_path):
    p, s = _mk(tmp_path, PARTY, STAND)
    parable = tmp_path / "parable.md"
    parable.write_text("A tale of the sea with no declaration.\n", encoding="utf-8")
    violations, _ = rv.check_parable(parable, [], json.loads(p.read_text()), json.loads(s.read_text()))
    assert any("SAME-STANDS" in v and "no 'stands:'" in v for v in violations)


def test_unknown_stand_fails(tmp_path):
    p, s = _mk(tmp_path, PARTY, STAND)
    parable = tmp_path / "parable.md"
    parable.write_text("stands: invented-stand\n\nTale.\n", encoding="utf-8")
    violations, _ = rv.check_parable(parable, [], json.loads(p.read_text()), json.loads(s.read_text()))
    assert any("not in stands registry" in v for v in violations)


def test_certified_grade_without_consensus_fails_loud(tmp_path, monkeypatch, capsys):
    """Truth law: certified cannot be claimed from nothing (exit 2 even when mechanical checks pass)."""
    p, s = _mk(tmp_path, PARTY, STAND)
    parable = tmp_path / "parable.md"
    parable.write_text("stands: trust-salted-fish\n\nClean tale.\n", encoding="utf-8")
    monkeypatch.setattr(rv, "PARTIES", p)
    monkeypatch.setattr(rv, "STANDS", s)
    rc = rv.main(["check", "--parable", str(parable), "--grade", "certified"])
    out = capsys.readouterr().out
    assert rc == 2
    assert "TRUTH" in out
    assert "VEIL-FAIL" in out


def test_sensing_grade_pass_reports_its_own_grade(tmp_path, monkeypatch, capsys):
    """Truth law: a sensing verdict must never print as certified."""
    p, s = _mk(tmp_path, PARTY, STAND)
    parable = tmp_path / "parable.md"
    parable.write_text("stands: trust-salted-fish\n\nClean tale.\n", encoding="utf-8")
    monkeypatch.setattr(rv, "PARTIES", p)
    monkeypatch.setattr(rv, "STANDS", s)
    rc = rv.main(["check", "--parable", str(parable), "--grade", "sensing"])
    out = capsys.readouterr().out
    assert rc == 0
    verdict = [l for l in out.splitlines() if l.startswith("VERDICT")][0]
    assert "VEIL-PASS" in verdict
    assert "sensing grade: mechanical checks only" in verdict  # grade rides inline, never hides


def test_init_creates_registries(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(rv, "RIDDLER_DIR", tmp_path)
    monkeypatch.setattr(rv, "PARTIES", tmp_path / "parties.json")
    monkeypatch.setattr(rv, "STANDS", tmp_path / "stands.json")
    rc = rv.main(["init"])
    assert rc == 0
    assert (tmp_path / "parties.json").is_file()
    assert (tmp_path / "stands.json").is_file()
