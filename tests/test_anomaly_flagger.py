"""Anomaly flagger tests (IMP6, 2026-09-30; Q36 integrity arm 2026-10-01).

Fixture contract for tools/anomaly_flagger.py: malformed JSONL lines
(blanks included) are named per row; step_hash must fullmatch 16
lowercase hex; strict ts descents are named as rows and grouped into
runs, with comparison surviving malformed gaps and mixed Z/+00:00
offsets and equal ts never counting as a descent; ORAL thread_id
duplicates name every row they occupy; the burns join counts OTHER and
REVIEW informationally (not anomalies) while fallback_unknown verdicts
and missing landing paths are anomalies; evidence sampling is
deterministic and even; the CLI exits 0 clean / 1 anomalies with rows
named / 2 on a missing stream.

Q36 integrity arm (watch/inbox/mountain_climb/FIFTY_QUESTIONS_ANSWERED.md,
FAIL: "clean" meant well-formed, not intact): a row whose bytes allow
recomputation of the step_hash basis (owned by mag.trajectory_step
make_row/verify) is TAMPERED when its shape-valid hash mismatches the
recomputed basis - writer-produced bytes must read clean, mutated text
under the writer's own hash must read tampered, and rows that cannot be
compared (step_hash=None, basis gaps) land in hash_unverifiable, never
silently clean and never guessed tampered. Writer-backed fixtures come
from mag.trajectory_step.make_row itself (env_path pinned to a
nonexistent file so redaction is identity) so the clean path is proven
against the writer, not against the flagger's own recompute.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

# Module import, not from-imports: keeps tool helpers out of this
# module's test-prefixed collection namespace (house rule from
# tests/test_census_drift_patrol.py).
import tools.anomaly_flagger as af

# Writer import for the integrity fixtures: mag.trajectory_step is the
# basis OWNER (read-only here - this test file never modifies it), and
# mag is a lazy package so the import stays light.
import mag.trajectory_step as traj


def write_jsonl(path: Path, lines: list) -> Path:
    with path.open("w", encoding="utf-8") as handle:
        for line in lines:
            if line is None:
                handle.write("\n")  # blank physical line
            else:
                handle.write(line if isinstance(line, str) else json.dumps(line))
                handle.write("\n")
    return path


def step(ts: str, step_hash="auto") -> dict:
    """Synthetic step row. step_hash='auto' (default) computes the honest
    basis hash so shape/ts fixtures stay out of the integrity arm's
    findings; any other literal (None, uppercase) is a deliberate
    violation fixture and is stored verbatim."""
    row = {"schema_version": "trajectory_step.v1",
           "ts": ts, "session_id": "s", "face": "bash", "command": "c",
           "result": {"exit": 0, "output_excerpt": "", "truncated": False}}
    if step_hash == "auto":
        step_hash = af.integrity_of(row)[0]
    row["step_hash"] = step_hash
    return row


def writer_row(tmp_path: Path, command: str = "echo hi", output: str = "hello") -> dict:
    """A row produced by the WRITER itself (identity redaction via a
    nonexistent env file) - intact by construction, not by the flagger's
    own say-so."""
    return traj.make_row("sess-test", command, output, 0,
                         env_path=tmp_path / "no.env")


def checks(findings) -> dict:
    return {f.check: f for f in findings}


class TestSteps:
    def test_all_classes_named_and_grouped(self, tmp_path):
        path = write_jsonl(tmp_path / "steps.jsonl", [
            step("2026-09-01T00:00:00.000+00:00"),
            None,                                   # blank -> malformed
            "not json at all",                      # garbage -> malformed
            step("2026-09-01T00:00:01.000+00:00", step_hash=None),
            step("2026-09-01T00:00:02.000+00:00", step_hash="ABCDEF0123456789"),
            step("2026-09-01T00:00:01.500+00:00"),  # descent row 6
            step("2026-09-01T00:00:01.000+00:00"),  # adjacent descent row 7
            step("2026-09-01T00:00:02.000+00:00"),
        ])
        findings, total = af.scan_steps(path)
        by_check = checks(findings)
        assert total == 8
        assert [r.split(" ")[0] for r in by_check["malformed_json"].rows] == ["2", "3"]
        assert [r.split(" ")[0] for r in by_check["hash_shape"].rows] == ["4", "5"]
        desc = by_check["ts_non_monotonic"]
        assert [r.split(" ")[0] for r in desc.rows] == ["6", "7"]
        assert "2 descent(s) in 1 run(s)" in desc.summary  # adjacent = one run
        # Q36 arm: rows 4/5 cannot be compared -> unverifiable (AND they
        # stay shape findings); honest-hash rows 1/6/7/8 verify clean.
        unv = by_check["hash_unverifiable"]
        assert [r.split(" ")[0] for r in unv.rows] == ["4", "5"]
        assert unv.anomaly
        assert "hash_integrity" not in by_check
        assert "verified=4 tampered=0 unverifiable=2" in \
            by_check["hash_integrity_census"].summary

    def test_descent_survives_gap_and_mixed_offsets(self, tmp_path):
        path = write_jsonl(tmp_path / "steps.jsonl", [
            step("2026-09-01T00:00:01+00:00"),
            "}{ broken",
            step("2026-09-01T00:00:00Z"),            # Z vs +00:00, across gap
        ])
        findings, _ = af.scan_steps(path)
        desc = checks(findings)["ts_non_monotonic"]
        assert desc.rows and desc.rows[0].startswith("3 ")

    def test_equal_ts_is_not_a_descent(self, tmp_path):
        path = write_jsonl(tmp_path / "steps.jsonl", [
            step("2026-09-01T00:00:00Z"),
            step("2026-09-01T00:00:00Z"),
        ])
        findings, _ = af.scan_steps(path)
        assert "ts_non_monotonic" not in checks(findings)


class TestIntegrityArm:
    """Q36: clean must mean intact, not just well-formed. Fixtures in
    this class are produced (or mutated) from mag.trajectory_step's own
    writer so the verdicts are proven against the basis owner."""

    def test_q36_falsifier_mutated_text_is_tampered(self, tmp_path):
        # The Q36 falsifier verbatim: writer row, mutate the text, keep
        # the shape-valid 16-hex stored hash.
        row = writer_row(tmp_path)
        row["result"]["output_excerpt"] += " TAMPERED"
        path = write_jsonl(tmp_path / "steps.jsonl", [row])
        findings, _ = af.scan_steps(path)
        by_check = checks(findings)
        tampered = by_check["hash_integrity"]
        assert tampered.anomaly
        assert tampered.rows[0].startswith("1 ")
        assert "!=" in tampered.rows[0]          # stored vs recomputed named
        assert "1 row(s) TAMPERED" in tampered.summary
        assert "hash_unverifiable" not in by_check
        assert "hash_shape" not in by_check      # shape arm stays quiet...
        assert "verified=0 tampered=1 unverifiable=0" in \
            by_check["hash_integrity_census"].summary

    def test_writer_bytes_are_clean(self, tmp_path):
        path = write_jsonl(tmp_path / "steps.jsonl",
                           [writer_row(tmp_path), writer_row(tmp_path, "ls", "a.py")])
        findings, _ = af.scan_steps(path)
        by_check = checks(findings)
        assert "hash_integrity" not in by_check
        assert "hash_unverifiable" not in by_check
        census = by_check["hash_integrity_census"]
        assert not census.anomaly
        assert "verified=2 tampered=0 unverifiable=0" in census.summary

    def test_step_hash_none_is_unverifiable_not_clean_not_tampered(self, tmp_path):
        row = writer_row(tmp_path)
        row["step_hash"] = None
        path = write_jsonl(tmp_path / "steps.jsonl", [row])
        findings, _ = af.scan_steps(path)
        by_check = checks(findings)
        unv = by_check["hash_unverifiable"]
        assert unv.anomaly
        assert unv.rows[0].startswith("1 (")
        assert "step_hash not comparable" in unv.rows[0]
        assert "hash_integrity" not in by_check      # not guessed tampered
        # ...and it stays a shape finding too, honestly counted in both.
        assert by_check["hash_shape"].rows[0].startswith("1 ")
        assert "verified=0 tampered=0 unverifiable=1" in \
            by_check["hash_integrity_census"].summary

    def test_basis_gap_is_unverifiable_even_with_valid_hash(self, tmp_path):
        row = writer_row(tmp_path)
        del row["command"]  # basis incomplete: recompute impossible
        path = write_jsonl(tmp_path / "steps.jsonl", [row])
        findings, _ = af.scan_steps(path)
        by_check = checks(findings)
        assert "hash_shape" not in by_check          # hash itself is fine
        unv = by_check["hash_unverifiable"]
        assert "command" in unv.rows[0]              # the gap is named
        assert "hash_integrity" not in by_check

    def test_cli_counts_tampered_and_exits_one(self, tmp_path, capsys):
        # One writer row, two copies at the same ts (equal ts is legal):
        # the intact copy verifies, the mutated copy is tampered - no
        # wall-clock dependence in the fixture.
        row = writer_row(tmp_path)
        clean = dict(row, result=dict(row["result"]))
        bad = dict(row, result=dict(row["result"]))
        bad["result"]["output_excerpt"] += " EDITED BY HAND"
        write_jsonl(tmp_path / "steps.jsonl", [clean, bad])
        write_jsonl(tmp_path / "oral.jsonl",
                    [{"thread_id": "t1", "ts": "2026-09-01T00:00:00Z"}])
        landing = tmp_path / "receipt.md"
        landing.write_text("ok", encoding="utf-8")
        write_jsonl(tmp_path / "ledger.jsonl",
                    [{"ts": "t", "slug": "a", "verdict": "steal",
                      "landing": str(landing)}])
        (tmp_path / "map.json").write_text(json.dumps(tiny_map()), encoding="utf-8")
        rc = af.main(["--steps", str(tmp_path / "steps.jsonl"),
                      "--oral", str(tmp_path / "oral.jsonl"),
                      "--ledger", str(tmp_path / "ledger.jsonl"),
                      "--enum-map", str(tmp_path / "map.json")])
        out = capsys.readouterr().out
        assert rc == af.EXIT_ANOMALIES
        assert "hash_integrity" in out
        assert "TAMPERED" in out
        assert "verified=1 tampered=1 unverifiable=0" in out


class TestOral:
    def test_sort_violation_and_duplicate_thread_ids(self, tmp_path):
        path = write_jsonl(tmp_path / "oral.jsonl", [
            {"thread_id": "t1", "ts": "2026-09-02T00:00:00Z"},
            {"thread_id": "t2", "ts": "2026-09-03T00:00:00Z"},
            {"thread_id": "t1", "ts": "2026-09-01T00:00:00Z"},  # dup + descent
        ])
        findings, total = af.scan_oral(path)
        by_check = checks(findings)
        assert total == 3
        assert by_check["ts_sort"].rows[0].startswith("3 ")
        dup = by_check["dup_thread_id"]
        assert dup.rows == ["t1 at 1,3"]

    def test_unique_ids_clean(self, tmp_path):
        path = write_jsonl(tmp_path / "oral.jsonl", [
            {"thread_id": "t1", "ts": "2026-09-01T00:00:00Z"},
            {"thread_id": "t2", "ts": "2026-09-01T00:00:01Z"},
        ])
        findings, _ = af.scan_oral(path)
        assert not any(f.anomaly for f in findings)


def tiny_map() -> dict:
    return {"census": {
        "steal": {"enum": "LANDED", "review": False},
        "roam": {"enum": "OTHER", "review": True},
    }}


class TestBurns:
    def make(self, tmp_path, rows, sample=50):
        ledger = write_jsonl(tmp_path / "ledger.jsonl", rows)
        map_path = tmp_path / "map.json"
        map_path.write_text(json.dumps(tiny_map()), encoding="utf-8")
        findings, total = af.scan_burns(ledger, map_path, sample=sample)
        return checks(findings), total

    def test_counts_informational_anomalies_flagged(self, tmp_path):
        landing = tmp_path / "receipt.md"
        landing.write_text("ok", encoding="utf-8")
        by_check, total = self.make(tmp_path, [
            {"ts": "t", "slug": "a", "verdict": "steal", "landing": str(landing)},
            {"ts": "t", "slug": "b", "verdict": "roam", "landing": str(landing)},
            {"ts": "t", "slug": "c", "verdict": "zzz-unknown-verdict",
             "landing": str(landing)},
            {"ts": "t", "slug": "d", "verdict": "steal", "landing": "no/such/file.md"},
            {"ts": "t", "slug": "e", "verdict": "steal"},
        ])
        assert total == 5
        census = by_check["verdict_enum"]
        assert not census.anomaly
        # roam is census-OTHER+review; the fallback verdict is OTHER+review too
        # (the map's fallback: {enum: OTHER, review: true}).
        assert "OTHER=2" in census.summary and "REVIEW=2" in census.summary
        assert "fallback_unknown=1" in census.summary
        assert by_check["fallback_unknown"].rows[0].startswith("3 ")
        assert by_check["evidence_missing"].rows[0].startswith("4 ")
        assert by_check["evidence_no_field"].rows[0].startswith("5 ")

    def test_sample_is_deterministic_and_bounded(self, tmp_path):
        rows = [{"ts": "t", "slug": f"s{i}", "verdict": "steal",
                 "landing": f"missing/{i}.md"} for i in range(1, 11)]
        by_check, _ = self.make(tmp_path, rows, sample=3)
        assert [r.split(" ")[0] for r in by_check["evidence_missing"].rows] == ["1", "4", "7"]

    def test_sample_zero_covers_all(self, tmp_path):
        rows = [{"ts": "t", "slug": f"s{i}", "verdict": "steal",
                 "landing": f"missing/{i}.md"} for i in range(1, 5)]
        by_check, _ = self.make(tmp_path, rows, sample=0)
        assert len(by_check["evidence_missing"].rows) == 4


class TestCli:
    def cli_args(self, tmp_path):
        return ["--steps", str(tmp_path / "steps.jsonl"),
                "--oral", str(tmp_path / "oral.jsonl"),
                "--ledger", str(tmp_path / "ledger.jsonl"),
                "--enum-map", str(tmp_path / "map.json")]

    def clean_tree(self, tmp_path):
        write_jsonl(tmp_path / "steps.jsonl", [step("2026-09-01T00:00:00Z")])
        write_jsonl(tmp_path / "oral.jsonl", [{"thread_id": "t1", "ts": "2026-09-01T00:00:00Z"}])
        landing = tmp_path / "receipt.md"
        landing.write_text("ok", encoding="utf-8")
        write_jsonl(tmp_path / "ledger.jsonl",
                    [{"ts": "t", "slug": "a", "verdict": "steal", "landing": str(landing)}])
        (tmp_path / "map.json").write_text(json.dumps(tiny_map()), encoding="utf-8")

    def test_clean_exits_zero(self, tmp_path, capsys):
        self.clean_tree(tmp_path)
        assert af.main(self.cli_args(tmp_path)) == af.EXIT_CLEAN
        assert "CLEAN" in capsys.readouterr().out

    def test_anomalies_exit_one_rows_named(self, tmp_path, capsys):
        self.clean_tree(tmp_path)
        write_jsonl(tmp_path / "steps.jsonl", [
            step("2026-09-01T00:00:00Z"),
            "garbage {",
            step("2026-09-01T00:00:00Z"),
        ])
        assert af.main(self.cli_args(tmp_path)) == af.EXIT_ANOMALIES
        out = capsys.readouterr().out
        assert "2 (Expecting" in out          # row named on stdout
        assert "exit 1" in out

    def test_missing_stream_exits_two(self, tmp_path, capsys):
        self.clean_tree(tmp_path)
        args = self.cli_args(tmp_path)
        args[args.index("--steps") + 1] = str(tmp_path / "nope.jsonl")
        assert af.main(args) == af.EXIT_USAGE
        assert "IO-ERROR" in capsys.readouterr().err
