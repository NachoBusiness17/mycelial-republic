"""Tests for tools.cite_allowlist (port wave P1, 2026-10-07).

Founding steal: both existing gates verify cites against the whole repo, so a
seat citing a sibling file it never read passes (watch/inbox/
frontier_olm_2026-10-07/steal/evals-self-improvement via reddit.md, find 2).
The three founding scenarios, per the lane spec:
  1. a doc citing only allowlisted paths passes (exit 0)
  2. a doc citing a sibling file outside the allowlist trips
     CITE-OUTSIDE-ALLOWLIST
  3. a doc citing a nonexistent path trips PATH-MISSING

Fixture world is hermetic: ESTATE_ROOT is monkeypatched to tmp_path, so
fixture "repo paths" resolve inside the throwaway tree and never touch the
live repo.

Receipt: watch/inbox/port_wave_20261007/p1_cite_allowlist.md
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools import cite_allowlist as ca


@pytest.fixture
def world(tmp_path: Path, monkeypatch) -> Path:
    """Hermetic estate root: resolution lands in tmp_path only."""
    monkeypatch.setattr(ca, "ESTATE_ROOT", tmp_path)
    return tmp_path


def _write(root: Path, rel: str, text: str = "source bytes for the claim\n") -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def _allow(root: Path, entries: list) -> Path:
    p = root / "ask_inputs.allowlist.txt"
    body = "# input set the seat was given\n" + "\n".join(entries) + "\n"
    p.write_text(body, encoding="utf-8")
    return p


def _doc(root: Path, body: str) -> Path:
    p = root / "out" / "card.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def test_allowlisted_cites_pass(world: Path):
    """Founding scenario 1: cites inside the allowlist are clean, exit 0."""
    _write(world, "watch/inbox/given_source.md")
    _write(world, "tools/given_tool.py")
    al = _allow(world, ["watch/inbox/given_source.md", "tools/given_tool.py"])
    doc = _doc(world, "The claim holds. Evidence: watch/inbox/given_source.md and "
                     "tools/given_tool.py\n")
    row = ca.check_doc(doc, al)
    assert row["ok"] is True
    assert row["findings"] == []
    assert row["cites_checked"] == 2
    assert ca.main(["check", "--doc", str(doc), "--allowlist", str(al)]) == 0


def test_sibling_outside_allowlist_trips(world: Path):
    """Founding scenario 2: the file exists on disk (so PATH-MISSING would
    pass, the whole point of the steal) but the seat was never given it."""
    _write(world, "watch/inbox/given_source.md")
    _write(world, "watch/inbox/sibling_lane_draft.md")
    al = _allow(world, ["watch/inbox/given_source.md"])
    doc = _doc(world, "The claim stands. Evidence: watch/inbox/sibling_lane_draft.md\n")
    row = ca.check_doc(doc, al)
    assert row["ok"] is False
    assert len(row["findings"]) == 1
    f = row["findings"][0]
    assert f["verdict"] == "CITE-OUTSIDE-ALLOWLIST"
    assert f["cited"] == "watch/inbox/sibling_lane_draft.md"
    assert f["doc_line"] == 1
    assert ca.main(["check", "--doc", str(doc), "--allowlist", str(al)]) == 1


def test_nonexistent_path_trips_path_missing(world: Path):
    """Founding scenario 3: a cite that resolves nowhere is PATH-MISSING even
    when an allowlist is present."""
    _write(world, "watch/inbox/given_source.md")
    al = _allow(world, ["watch/inbox/given_source.md"])
    doc = _doc(world, "Basis: docs/never_written.md\n")
    row = ca.check_doc(doc, al)
    assert row["ok"] is False
    f = row["findings"][0]
    assert f["verdict"] == "PATH-MISSING"
    assert f["nearest"] is None


def test_directory_entry_covers_children(world: Path):
    """An allowlist entry that is a directory prefix covers every file under
    it (an ask that hands over a whole pack directory)."""
    _write(world, "watch/inbox/pack/file_a.md")
    _write(world, "watch/inbox/pack/sub/file_b.md")
    _write(world, "watch/inbox/outside.md")
    al = _allow(world, ["watch/inbox/pack/"])
    doc = _doc(world, "A: watch/inbox/pack/file_a.md\nB: watch/inbox/pack/sub/file_b.md\n"
                      "C: watch/inbox/outside.md\n")
    row = ca.check_doc(doc, al)
    assert [f["cited"] for f in row["findings"]] == ["watch/inbox/outside.md"]
    assert row["findings"][0]["verdict"] == "CITE-OUTSIDE-ALLOWLIST"


def test_on_disk_directory_entry_expands(world: Path):
    """An entry without a trailing slash that is a real directory on disk
    becomes a prefix too."""
    _write(world, "corpus/steal/real_card.md")
    al = _allow(world, ["corpus/steal"])
    doc = _doc(world, "Evidence: corpus/steal/real_card.md\n")
    assert ca.check_doc(doc, al)["ok"] is True


def test_line_anchors_and_prose_tail_clean(world: Path):
    """path:line and path:N-M cites and prose tails (parens, periods) parse to
    the same bare path."""
    _write(world, "mag/improve.py", text="def scout():\n    return 1\n")
    al = _allow(world, ["mag/improve.py"])
    doc = _doc(world, "Per mag/improve.py:1-2 the scout exists (tools form).\n")
    row = ca.check_doc(doc, al)
    assert row["ok"] is True
    assert row["cites_checked"] == 1


def test_bare_filename_is_a_mention_not_a_cite(world: Path):
    """cite_gate's standing stance: a bare filename with no separator is a
    mention and never trips the gate."""
    _write(world, "watch/inbox/given_source.md")
    al = _allow(world, ["watch/inbox/given_source.md"])
    doc = _doc(world, "This mirrors README.md conventions. Evidence: "
                      "watch/inbox/given_source.md\n")
    row = ca.check_doc(doc, al)
    assert row["ok"] is True
    assert row["cites_checked"] == 1


def test_win32_and_case_forms_match_one_allowlist(world: Path):
    """Backslash and case variants of a given path are the same cite."""
    _write(world, "watch/inbox/Given_Source.md")
    al = _allow(world, ["watch/inbox/given_source.md"])
    doc = _doc(world, "Evidence: watch\\inbox\\Given_Source.md\n")
    assert ca.check_doc(doc, al)["ok"] is True


def test_root_prefix_form_matches(world: Path):
    """ROOT/-prefixed cites (cite_gate's display form) normalize the same."""
    _write(world, "memory/attention.md")
    al = _allow(world, ["memory/attention.md"])
    doc = _doc(world, "Evidence: ROOT/memory/attention.md\n")
    assert ca.check_doc(doc, al)["ok"] is True


def test_nearest_neighbor_names_closest_given(world: Path):
    """A near-miss cite gets the closest allowlist entry named for remediation."""
    _write(world, "watch/inbox/alpha_report.md")
    _write(world, "watch/inbox/alpha_reprt.md")  # typo'd sibling, on disk
    al = _allow(world, ["watch/inbox/alpha_report.md"])
    doc = _doc(world, "Evidence: watch/inbox/alpha_reprt.md\n")
    row = ca.check_doc(doc, al)
    assert row["findings"][0]["verdict"] == "CITE-OUTSIDE-ALLOWLIST"
    assert row["findings"][0]["nearest"] == "watch/inbox/alpha_report.md"


def test_mixed_doc_reports_each_class(world: Path):
    """One doc, three cites: allowed, sibling outside, nonexistent. Exactly
    the two non-allowed classes fire, deduped, first line reported."""
    _write(world, "watch/inbox/given.md")
    _write(world, "watch/inbox/sibling.md")
    al = _allow(world, ["watch/inbox/given.md"])
    doc = _doc(world,
               "Line one: watch/inbox/given.md\n"
               "Line two: watch/inbox/sibling.md\n"
               "Line three: docs/ghost.md\n"
               "Repeat of line two: watch/inbox/sibling.md\n")
    row = ca.check_doc(doc, al)
    assert row["cites_checked"] == 3
    got = [(f["cited"], f["verdict"]) for f in row["findings"]]
    assert got == [
        ("watch/inbox/sibling.md", "CITE-OUTSIDE-ALLOWLIST"),
        ("docs/ghost.md", "PATH-MISSING"),
    ]
    assert row["findings"][0]["doc_line"] == 2


def test_cli_json_output_contract(world: Path, capsys):
    """--json emits the verdict row; exit codes are 0 clean / 1 findings /
    2 cannot-verify (unreadable doc)."""
    _write(world, "watch/inbox/given.md")
    al = _allow(world, ["watch/inbox/given.md"])
    good = _doc(world, "Evidence: watch/inbox/given.md\n")
    assert ca.main(["check", "--doc", str(good), "--allowlist", str(al),
                    "--json"]) == 0
    row = json.loads(capsys.readouterr().out)
    assert row["tool"] == "CITE-ALLOWLIST"
    assert row["ok"] is True

    _write(world, "watch/inbox/sibling.md")  # on disk, so it is outside, not missing
    bad = _doc(world, "Evidence: watch/inbox/sibling.md\n")
    assert ca.main(["check", "--doc", str(bad), "--allowlist", str(al)]) == 1
    out = capsys.readouterr().out.splitlines()
    assert out[0].startswith("CITE-ALLOWLIST: FAIL")
    assert "CITE-OUTSIDE-ALLOWLIST" in out[1]

    assert ca.main(["check", "--doc", str(world / "no_such_doc.md"),
                    "--allowlist", str(al)]) == 2
    assert capsys.readouterr().out.startswith("CITE-ALLOWLIST: ERROR")


def test_empty_allowlist_flags_every_cite(world: Path):
    """A seat given nothing owns nothing: every cite is outside."""
    _write(world, "watch/inbox/given.md")
    al = _allow(world, [])
    doc = _doc(world, "Evidence: watch/inbox/given.md\n")
    row = ca.check_doc(doc, al)
    assert row["ok"] is False
    assert row["findings"][0]["verdict"] == "CITE-OUTSIDE-ALLOWLIST"
