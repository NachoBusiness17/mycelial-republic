"""Tests for tools/surface_orphan_walk.py (G1 lane i07-orphan-walk).

Parent gene G0 g04-contract-widening. The regression at the heart of this
module is mag/shared_surface.py:275-280: basename-keyed, top-level-only
orphan matching that (a) never sees subdir files and (b) false-clears a
top-level file when an indexed subdir item shares its basename. Every test
here runs against a synthetic tmp inbox built through the same helpers the
walk itself reads.
"""

from __future__ import annotations

import json

import pytest

import tools.surface_orphan_walk as sow


def make_inbox(tmp_path, files, index_items, index_extra=None):
    """Build a synthetic inbox tree + INDEX.json; returns (inbox, index)."""
    inbox = tmp_path / "inbox"
    for rel in files:
        path = inbox / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"payload: {rel}\n", encoding="utf-8")
    payload = {
        "schema": "index.v1",
        "root": "/board/inbox",
        "items": [{"path": p} for p in index_items],
    }
    if index_extra:
        payload.update(index_extra)
    index = inbox / "INDEX.json"
    index.write_text(json.dumps(payload), encoding="utf-8")
    return inbox, index


def run_main(capsys, argv):
    code = sow.main(argv)
    out = capsys.readouterr().out
    return code, out


class TestStripInboxPrefix:
    """Pin the ladder to mag/shared_surface.py:298-303 semantics."""

    @pytest.mark.parametrize("raw,expected", [
        ("note.md", "note.md"),
        ("sub/dir/note.md", "sub/dir/note.md"),
        ("/board/inbox/note.md", "note.md"),
        ("/board/inbox/sub/note.md", "sub/note.md"),
        ("/app/inbox/sub/note.md", "sub/note.md"),
        ("inbox/sub/note.md", "sub/note.md"),
        ("inbox\\win\\seps.md", "win/seps.md"),
        # First match only, exactly like the source (break after strip).
        ("inbox/inbox/note.md", "inbox/note.md"),
        ("/board/inbox/inbox/note.md", "inbox/note.md"),
    ])
    def test_vectors(self, raw, expected):
        assert sow.strip_inbox_prefix(raw) == expected


class TestMixedTree:
    def test_all_depths_and_controls(self, tmp_path, capsys):
        files = [
            "indexed_top.md",          # indexed, top level
            "indexed/nested.md",       # indexed, subdir
            "orphan_top.md",           # unindexed, top level
            "unindexed/deep/orphan.md",  # unindexed, subdir (invisible pre-fix)
            "INDEX.md",                # control file, unindexed -> never orphan
            "SHARED_SURFACE_CONTRACT.json",  # control file
        ]
        inbox, index = make_inbox(
            tmp_path, files,
            ["indexed_top.md", "indexed/nested.md"],
        )
        code, out = run_main(capsys, ["--inbox", str(inbox), "--index", str(index)])
        assert code == 0
        first = out.splitlines()[0]
        assert first == "surface_orphan_walk: ok (2 orphans)"
        # The subdir orphan is named WITH its subdir (the old gate could not
        # even express one).
        assert "unindexed/deep/orphan.md" in out
        assert "orphan_top.md" in out
        assert "indexed/nested.md" not in out.split("orphan sample")[1]
        assert "INDEX.md" not in out.split("orphan sample")[1]

    def test_index_prefix_spellings_all_join(self, tmp_path, capsys):
        files = ["a.md", "d/b.md"]
        inbox, index = make_inbox(
            tmp_path, files,
            ["/board/inbox/a.md", "/app/inbox/d/b.md"],
        )
        code, out = run_main(capsys, ["--json", "--inbox", str(inbox),
                                      "--index", str(index)])
        assert code == 0
        doc = json.loads(out)
        assert doc["orphans_total"] == 0


class TestBasenameCollisionRegression:
    """The shared_surface.py:275-280 false-clear defect, pinned red-proof.

    Old behavior: indexed set == {"note.md"} (basename of the indexed
    subdir item), so the UNINDEXED top-level note.md was false-cleared.
    Correct behavior: relative path is the identity, so exactly the
    top-level file is the orphan.
    """

    def test_top_level_not_cleared_by_subdir_basename(self, tmp_path, capsys):
        files = ["note.md", "sub/note.md"]
        inbox, index = make_inbox(tmp_path, files, ["sub/note.md"])
        code, out = run_main(capsys, ["--json", "--inbox", str(inbox),
                                      "--index", str(index)])
        assert code == 0
        doc = json.loads(out)
        assert doc["orphans_total"] == 1
        assert doc["orphans_sample"] == ["note.md"]
        assert "sub/note.md" not in doc["orphans_sample"]

    def test_unindexed_subdir_file_reported(self, tmp_path, capsys):
        files = ["sub/ghost.md"]
        inbox, index = make_inbox(tmp_path, files, [])
        code, out = run_main(capsys, ["--json", "--inbox", str(inbox),
                                      "--index", str(index)])
        assert code == 0
        doc = json.loads(out)
        assert doc["orphans_sample"] == ["sub/ghost.md"]


class TestMalformedInput:
    """Malformed input is exit 2; orphans are WARN and never are."""

    def _case(self, tmp_path, index_bytes):
        inbox = tmp_path / "inbox"
        inbox.mkdir(exist_ok=True)
        (inbox / "x.md").write_text("payload\n", encoding="utf-8")
        index = inbox / "INDEX.json"
        index.write_bytes(index_bytes)
        return inbox, index

    @pytest.mark.parametrize("label,index_bytes", [
        ("bad-json", b"{not json"),
        ("root-not-object", b"[]"),
        ("items-not-list", b'{"items": {}}'),
        ("items-missing", b"{}"),
        ("item-not-object", b'{"items": ["a.md"]}'),
        ("path-not-string", b'{"items": [{"path": 7}]}'),
        ("path-empty", b'{"items": [{"path": "   "}]}'),
    ])
    def test_exit_2(self, tmp_path, capsys, label, index_bytes):
        inbox, index = self._case(tmp_path, index_bytes)
        code, out = run_main(capsys, ["--inbox", str(inbox), "--index", str(index)])
        assert code == 2, label
        assert out.splitlines()[0].startswith(
            "surface_orphan_walk: malformed input"), label

    def test_missing_index_exit_2(self, tmp_path, capsys):
        inbox = tmp_path / "inbox"
        inbox.mkdir()
        code, out = run_main(capsys, ["--inbox", str(inbox),
                                      "--index", str(inbox / "INDEX.json")])
        assert code == 2
        assert "INDEX missing" in out

    def test_missing_inbox_dir_exit_2(self, tmp_path, capsys):
        code, out = run_main(capsys, [
            "--inbox", str(tmp_path / "nope"),
            "--index", str(tmp_path / "nope" / "INDEX.json"),
        ])
        assert code == 2
        assert "inbox directory missing" in out

    def test_malformed_json_mode_is_pure_json_exit_2(self, tmp_path, capsys):
        inbox, index = self._case(tmp_path, b"{not json")
        code, out = run_main(capsys, ["--json", "--inbox", str(inbox),
                                      "--index", str(index)])
        assert code == 2
        doc = json.loads(out)
        assert doc["ok"] is False
        assert "not valid JSON" in doc["error"]

    def test_negative_limit_exit_2(self, capsys):
        code, out = run_main(capsys, ["--limit", "-1"])
        assert code == 2
        assert "--limit must be >= 0" in out


class TestSampling:
    def test_limit_bounds_sample_not_count(self, tmp_path, capsys):
        files = ["o1.md", "d/o2.md", "d/e/o3.md"]
        inbox, index = make_inbox(tmp_path, files, [])
        code, out = run_main(capsys, ["--inbox", str(inbox),
                                      "--index", str(index), "--limit", "1"])
        assert code == 0
        lines = out.splitlines()
        assert lines[0] == "surface_orphan_walk: ok (3 orphans)"
        assert "orphan sample (1 of 3, sorted):" in out
        assert "and 2 more" in out

    def test_json_mode_sample_bounded_count_full(self, tmp_path, capsys):
        files = ["o1.md", "d/o2.md"]
        inbox, index = make_inbox(tmp_path, files, [])
        code, out = run_main(capsys, ["--json", "--inbox", str(inbox),
                                      "--index", str(index), "--limit", "1"])
        assert code == 0
        doc = json.loads(out)
        assert doc["orphans_total"] == 2
        assert len(doc["orphans_sample"]) == 1
        assert doc["limit"] == 1
        assert doc["headline"] == "surface_orphan_walk: ok (2 orphans)"

    def test_zero_orphans_clean_headline(self, tmp_path, capsys):
        files = ["only.md"]
        inbox, index = make_inbox(tmp_path, files, ["only.md"])
        code, out = run_main(capsys, ["--inbox", str(inbox), "--index", str(index)])
        assert code == 0
        assert out.splitlines()[0] == "surface_orphan_walk: ok (0 orphans)"
        assert "orphan sample" not in out
