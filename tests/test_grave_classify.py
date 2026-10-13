"""tests for tools/grave_classify.py (gopher t27, gala afterparty 2026-09-25).

Covers: the canonical five labels (explicit, marker-adopted, successor
default), unknown-label rejection at both the function and CLI level, the
successor-on-disk law, and the no-em-dash law for emitted text.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.grave_classify import (  # noqa: E402
    CANONICAL_LABELS,
    GraveClassifyError,
    UnknownLabelError,
    classify,
    main,
    require_label,
)


def _write(tmp_path: Path, name: str, text: str) -> Path:
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return p


def test_canonical_label_set_is_exactly_five():
    assert CANONICAL_LABELS == (
        "FOSSIL",
        "ABSORBED-BY",
        "SUPERSEDED-BY",
        "DONE-ELSEWHERE",
        "STILL-RELEVANT",
    )


@pytest.mark.parametrize("label", list(CANONICAL_LABELS))
def test_require_label_accepts_each_canonical_label(label):
    assert require_label(label) == label
    assert require_label(label.lower()) == label  # normalization


@pytest.mark.parametrize(
    "bad", ["MERGED", "STILL-OWED", "ABSORBED", "superseded", "", "fossil-by-date"]
)
def test_require_label_rejects_unknown_labels(bad):
    with pytest.raises(UnknownLabelError) as err:
        require_label(bad)
    assert err.value.exit_code == 2


@pytest.mark.parametrize("label", list(CANONICAL_LABELS))
def test_explicit_label_classifies_with_justification(tmp_path, label):
    p = _write(tmp_path, "h.md", "# handoff\nsome ask\n")
    kwargs = {"label": label}
    if label in ("ABSORBED-BY", "SUPERSEDED-BY"):
        kwargs["successor"] = str(_write(tmp_path, "succ.md", "# successor\n"))
    row = classify(p, **kwargs)
    assert row["label"] == label
    assert row["source"] == "explicit"
    assert row["justification"].startswith(str(p))
    assert label in row["justification"]


def test_marker_adoption_fossil_from_c1_style_verdict(tmp_path):
    p = _write(tmp_path, "h.md", "Verdict: **FOSSIL as of 2026-09-25.**\n")
    row = classify(p)
    assert row["label"] == "FOSSIL"
    assert row["source"] == "marker"


def test_marker_adoption_done_elsewhere_from_json_field(tmp_path):
    p = _write(tmp_path, "h.json", '{"classification": "DONE-ELSEWHERE"}\n')
    row = classify(p)
    assert row["label"] == "DONE-ELSEWHERE"
    assert row["source"] == "marker"


def test_marker_unknown_label_is_exit2_drift_enforcement(tmp_path):
    p = _write(tmp_path, "h.md", "Verdict: STILL-OWED, moved where\n")
    with pytest.raises(GraveClassifyError) as err:
        classify(p)
    assert err.value.exit_code == 2
    assert "STILL-OWED" in str(err.value)


def test_marker_ambiguous_canonical_labels_exit3(tmp_path):
    p = _write(
        tmp_path,
        "h.md",
        "classification: ABSORBED-BY\nverdict: STILL-RELEVANT\n",
    )
    with pytest.raises(GraveClassifyError) as err:
        classify(p)
    assert err.value.exit_code == 3


def test_successor_on_disk_defaults_superseded_by(tmp_path):
    succ = _write(tmp_path, "succ.md", "# successor\n")
    p = _write(tmp_path, "h.md", "no markers here\n")
    row = classify(p, successor=str(succ))
    assert row["label"] == "SUPERSEDED-BY"
    assert row["successor"] == str(succ)
    assert row["successor_exists"] is True


def test_successor_hint_missing_on_disk_is_exit1(tmp_path):
    p = _write(tmp_path, "h.md", "no markers here\n")
    with pytest.raises(GraveClassifyError) as err:
        classify(p, successor=str(tmp_path / "ghost.md"))
    assert err.value.exit_code == 1
    assert "never fabricate" in str(err.value)


def test_absorbed_by_requires_successor(tmp_path):
    p = _write(tmp_path, "h.md", "no markers here\n")
    with pytest.raises(GraveClassifyError) as err:
        classify(p, label="ABSORBED-BY")
    assert err.value.exit_code == 1


def test_missing_handoff_file_is_exit1(tmp_path):
    with pytest.raises(GraveClassifyError) as err:
        classify(tmp_path / "absent.md")
    assert err.value.exit_code == 1


@pytest.mark.parametrize("label", list(CANONICAL_LABELS))
def test_no_em_or_en_dash_in_justifications(tmp_path, label):
    p = _write(tmp_path, "h.md", "body\n")
    kwargs = {"label": label}
    if label in ("ABSORBED-BY", "SUPERSEDED-BY"):
        kwargs["successor"] = str(_write(tmp_path, "succ.md", "s\n"))
    row = classify(p, **kwargs)
    assert "\u2014" not in row["justification"]  # em dash
    assert "\u2013" not in row["justification"]  # en dash


def test_cli_unknown_label_exits_2(tmp_path):
    p = _write(tmp_path, "h.md", "body\n")
    assert main([str(p), "--label", "STILL-OWED"]) == 2


def test_cli_json_row_for_still_relevant_default(tmp_path, capsys):
    p = _write(tmp_path, "h.md", "plain handoff, no markers\n")
    code = main([str(p), "--json"])
    out = json.loads(capsys.readouterr().out)
    assert code == 0
    assert out["label"] == "STILL-RELEVANT"
    assert out["source"] == "default"
    assert out["successor"] is None


# --- batch mode (gopher t48, 2026-09-25) -----------------------------------


def test_batch_classifies_every_file_in_one_run_exits_zero(tmp_path, capsys):
    _write(tmp_path, "a.json", '{"classification": "DONE-ELSEWHERE"}\n')
    _write(tmp_path, "b.md", "Verdict: **FOSSIL as of 2026-09-25.**\n")
    _write(tmp_path, "c.md", "plain handoff, no markers\n")
    assert main(["--batch", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "batch: 3 files, 3 classified, 0 failed" in out
    for label in ("DONE-ELSEWHERE", "FOSSIL", "STILL-RELEVANT"):
        assert label in out


def test_batch_table_rows_are_sorted_by_filename(tmp_path, capsys):
    _write(tmp_path, "zz.md", "plain\n")
    _write(tmp_path, "aa.md", "plain\n")
    assert main(["--batch", str(tmp_path)]) == 0
    table = capsys.readouterr().out
    assert table.index("aa.md") < table.index("zz.md")


def test_batch_pattern_filters_file_names(tmp_path, capsys):
    _write(tmp_path, "a.json", '{"classification": "DONE-ELSEWHERE"}\n')
    _write(tmp_path, "b.md", "plain\n")
    _write(tmp_path, "c.md", "plain\n")
    assert main(["--batch", str(tmp_path), "--pattern", "*.json"]) == 0
    out = capsys.readouterr().out
    assert "batch: 1 files, 1 classified, 0 failed" in out
    body_rows = [line for line in out.splitlines() if line.startswith(str(tmp_path))]
    assert len(body_rows) == 1 and "a.json" in body_rows[0]


def test_batch_json_emits_one_machine_row_per_file(tmp_path, capsys):
    _write(tmp_path, "a.json", '{"classification": "DONE-ELSEWHERE"}\n')
    _write(tmp_path, "b.md", "plain\n")
    assert main(["--batch", str(tmp_path), "--json"]) == 0
    rows = json.loads(capsys.readouterr().out)
    assert isinstance(rows, list) and len(rows) == 2
    assert [r["label"] for r in rows] == ["DONE-ELSEWHERE", "STILL-RELEVANT"]


def test_batch_failed_file_stays_a_row_and_exit_is_2(tmp_path, capsys):
    _write(tmp_path, "good.md", "plain handoff\n")
    _write(tmp_path, "drift.md", "Verdict: STILL-OWED, moved where\n")
    assert main(["--batch", str(tmp_path)]) == 2
    out = capsys.readouterr().out
    assert "ERROR(2)" in out
    assert "STILL-OWED" in out  # the drift is named, not swallowed
    assert "batch: 2 files, 1 classified, 1 failed" in out


def test_batch_worst_code_wins_ambiguous_beats_unknown(tmp_path):
    _write(tmp_path, "amb.md", "classification: ABSORBED-BY\nverdict: STILL-RELEVANT\n")
    _write(tmp_path, "drift.md", "Verdict: STILL-OWED\n")
    assert main(["--batch", str(tmp_path)]) == 3


def test_batch_missing_directory_is_exit1(tmp_path, capsys):
    assert main(["--batch", str(tmp_path / "absent")]) == 1
    assert "batch directory not found" in capsys.readouterr().err


def test_batch_skips_subdirectories(tmp_path, capsys):
    _write(tmp_path, "a.md", "plain\n")
    (tmp_path / "sub").mkdir()
    _write(tmp_path / "sub", "nested.md", "plain\n")
    assert main(["--batch", str(tmp_path)]) == 0
    assert "batch: 1 files, 1 classified, 0 failed" in capsys.readouterr().out


def test_batch_rejects_handoff_and_batch_together(tmp_path):
    p = _write(tmp_path, "h.md", "plain\n")
    with pytest.raises(SystemExit) as err:
        main([str(p), "--batch", str(tmp_path)])
    assert err.value.code == 2


def test_batch_rejects_label_and_successor_alongside_batch(tmp_path):
    _write(tmp_path, "h.md", "plain\n")
    with pytest.raises(SystemExit) as err:
        main(["--batch", str(tmp_path), "--label", "FOSSIL"])
    assert err.value.code == 2
    with pytest.raises(SystemExit) as err:
        main(["--batch", str(tmp_path), "--successor", "succ.md"])
    assert err.value.code == 2


def test_batch_classifies_only_never_writes_handoff_files(tmp_path):
    import hashlib

    names = ["a.json", "b.md", "drift.md"]
    before = {}
    for name in names:
        text = (
            "body + Verdict: STILL-OWED\n" if name == "drift.md" else f"body of {name}\n"
        )
        p = _write(tmp_path, name, text)
        before[name] = hashlib.sha256(p.read_bytes()).hexdigest()
    main(["--batch", str(tmp_path)])
    for name in names:
        p = tmp_path / name
        assert hashlib.sha256(p.read_bytes()).hexdigest() == before[name]


def test_batch_justification_lines_have_no_em_or_en_dash(tmp_path, capsys):
    _write(tmp_path, "a.md", "plain\n")
    _write(tmp_path, "drift.md", "Verdict: STILL-OWED\n")
    assert main(["--batch", str(tmp_path), "--json"]) == 2
    rows = json.loads(capsys.readouterr().out)
    assert len(rows) == 2
    for row in rows:
        assert "\u2014" not in row["justification"]
        assert "\u2013" not in row["justification"]
