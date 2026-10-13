"""Trajectory minimizer tests (D11, 2026-09-30).

Fixture contract for tools/trajectory_minimizer.py: citations are extracted
from receipt text only - ISO minute tokens honor their Z/+00:00/EDT/EST
marker and a bare token is UTC; local H:MM EDT/EST/UTC tokens anchor only to
a filename carrying exactly one date; day-only citations never make signal
(precision law). Signal = receipt_minute OR anomaly-named (live
tools/anomaly_flagger definition, imported) OR face=milestone. Signal rows
cluster by session + reason family + ts contiguity, a noise row breaks the
cluster, and cluster entries carry bounded gists and receipt pointers. The
differentiator reports share enrichment with a min-count floor and honest
negatives. CLI: exit 0 writes output+report, exit 2 on missing stream,
missing inbox, or an inbox with zero minute citations (fail-closed ground
truth).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import tools.trajectory_minimizer as tm
import tools.anomaly_flagger as af  # fixture hashes (Q36 note below)


def write_steps(path: Path, rows: list) -> Path:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            if row is None:
                handle.write("\n")            # blank physical line
            else:
                # raw strings stay raw (a malformed fixture must NOT become a
                # valid JSON string - that shape is outside the flagger's
                # contract and it crashes scan_monotonic_ts; cause verified
                # 2026-09-30 while landing these tests)
                handle.write(row if isinstance(row, str) else json.dumps(row))
                handle.write("\n")
    return path


def step(ts: str, command: str = "echo hi", session: str = "sess-a",
         face: str = "bash", exit_code: int = 0) -> dict:
    row = {"schema_version": "trajectory_step.v1",
           "ts": ts, "session_id": session, "face": face, "command": command,
           "result": {"exit": exit_code, "output_excerpt": "out", "truncated": False}}
    # Q36 fix (2026-10-01): the flagger's steps surface gained an integrity
    # arm, so the old fake-but-shape-valid "a"*16 fixture hash now reads
    # tampered and flipped this suite's P2 signal patterns (3 tests red,
    # evidence: pytest run right after the arm landed). Fixtures must
    # carry the honest recomputed basis hash to stay unnamed.
    row["step_hash"] = af.integrity_of(row)[0]
    return row


class TestCitations:
    def test_iso_marker_forms_convert_to_utc(self, tmp_path):
        receipt = tmp_path / "R_2026-09-01.md"
        receipt.write_text(
            "at 2026-09-01T10:00Z and 2026-09-01T10:01+00:00 "
            "and 2026-09-01T10:02 EDT (bare 2026-09-01T11:00)", encoding="utf-8")
        cites = tm.extract_citations(tmp_path)
        assert "2026-09-01T10:00" in cites["minutes"]
        assert "2026-09-01T10:01" in cites["minutes"]
        assert "2026-09-01T10:02 EDT" not in cites["minutes"]
        assert "2026-09-01T14:02" in cites["minutes"]   # EDT 10:02 -> UTC 14:02
        assert "2026-09-01T11:00" in cites["minutes"]   # bare token = UTC
        assert cites["receipts_read"] == 1

    def test_local_token_needs_unique_filename_date(self, tmp_path):
        (tmp_path / "ONE_2026-09-02.md").write_text(
            "kickoff at 09:30 EDT", encoding="utf-8")
        (tmp_path / "TWO_2026-09-02_2026-09-03.md").write_text(
            "recap at 08:00 EDT", encoding="utf-8")
        cites = tm.extract_citations(tmp_path)
        assert "2026-09-02T13:30" in cites["minutes"]   # 09:30 EDT -> 13:30 UTC
        assert "2026-09-02T12:00" not in cites["minutes"]  # ambiguous anchor skipped
        assert cites["tokens_local_ambiguous_skipped"] >= 1

    def test_day_only_citation_is_not_a_minute(self, tmp_path):
        (tmp_path / "D_2026-09-04.md").write_text(
            "on 2026-09-04 the lane burned", encoding="utf-8")
        cites = tm.extract_citations(tmp_path)
        assert cites["minutes"] == set()

    def test_cited_by_pointer_is_bounded(self, tmp_path):
        for i in range(5):
            (tmp_path / f"C{i}_2026-09-05.md").write_text(
                "ran at 2026-09-05T08:00Z", encoding="utf-8")
        cites = tm.extract_citations(tmp_path)
        assert len(cites["cited_by"]["2026-09-05T08:00"]) <= tm.CITED_BY_BOUND


class TestClassify:
    def make_tree(self, tmp_path):
        inbox = tmp_path / "inbox"
        inbox.mkdir()
        (inbox / "R_2026-09-01.md").write_text(
            "the step landed at 2026-09-01T00:05:00Z", encoding="utf-8")
        steps = write_steps(tmp_path / "steps.jsonl", [
            step("2026-09-01T00:05:10.000+00:00", command=".venv/Scripts/python.exe -m mag.run"),
            step("2026-09-01T00:05:40.000+00:00", command="grep -rn foo mag/"),
            step("2026-09-01T00:06:20.000+00:00", command="ls"),           # not cited
            step("2026-09-01T00:07:00.000+00:00", command="folded", face="milestone"),
            "}{ broken",                                                    # malformed
            step("2026-09-01T00:08:00.000+00:00", command="after"),
        ])
        return inbox, steps

    def test_three_prongs_and_precision_law(self, tmp_path):
        inbox, steps = self.make_tree(tmp_path)
        cites = tm.extract_citations(inbox)
        named = tm.anomaly_named_lines(steps)
        assert 5 in named and named[5] == "malformed_json"
        rows, totals = tm.classify_stream(steps, cites["minutes"], named)
        assert totals["lines"] == 6 and totals["malformed"] == 1
        assert [r["signal"] for r in rows] == [True, True, False, True, True, False]
        assert rows[0]["reasons"] == ["receipt_minute"]
        assert rows[3]["reasons"] == ["milestone"]  # its minute is uncited
        assert rows[4]["reasons"] == ["anomaly:malformed_json"]

    def test_day_only_receipt_keeps_everything_noise(self, tmp_path):
        inbox = tmp_path / "inbox"
        inbox.mkdir()
        (inbox / "D_2026-09-01.md").write_text("all day 2026-09-01", encoding="utf-8")
        steps = write_steps(tmp_path / "steps.jsonl", [step("2026-09-01T00:00:00Z")])
        rows, _ = tm.classify_stream(steps, set(), {})
        assert not any(r["signal"] for r in rows)


class TestCluster:
    def rows_for(self, tmp_path, rows_spec):
        inbox = tmp_path / "inbox"
        inbox.mkdir()
        (inbox / "R_2026-09-01.md").write_text(
            "cited 2026-09-01T00:00Z 2026-09-01T00:01Z", encoding="utf-8")
        steps = write_steps(tmp_path / "steps.jsonl", rows_spec)
        cites = tm.extract_citations(inbox)
        named = tm.anomaly_named_lines(steps)
        return tm.classify_stream(steps, cites["minutes"], named), cites

    def test_same_session_minutes_merge_noise_breaks(self, tmp_path):
        spec = [
            step("2026-09-01T00:00:10Z", command="git commit -m x"),
            step("2026-09-01T00:00:50Z", command="git push"),
            step("2026-09-01T00:03:00Z", command="ls"),               # noise break
            step("2026-09-01T00:01:30Z", command="pytest -q"),        # new cluster
        ]
        (rows, _), cites = self.rows_for(tmp_path, spec)
        entries = tm.cluster_signals(rows, cites["cited_by"])
        assert len(entries) == 2
        assert entries[0]["rows"] == 2 and entries[0]["reason"] == "receipt_minute"
        assert entries[0]["verbs"] == {"git commit": 1, "git push": 1}
        assert entries[0]["receipts"] == ["R_2026-09-01.md"]
        assert len(entries[0]["gists"]) == 2 and "exit=0" in entries[0]["gists"][0]

    def test_milestone_stands_alone_with_text_gist(self, tmp_path):
        spec = [
            step("2026-09-01T00:00:10Z", command="pytest -q"),
            # uncited minute + milestone face -> milestone prong only, so it
            # clusters alone instead of folding into the receipt-minute burst
            step("2026-09-01T00:05:30Z", command="NIGHT FOLD: doctrine v2", face="milestone"),
        ]
        (rows, _), cites = self.rows_for(tmp_path, spec)
        entries = tm.cluster_signals(rows, cites["cited_by"])
        reasons = sorted(e["reason"] for e in entries)
        assert reasons == ["milestone", "receipt_minute"]
        ms = next(e for e in entries if e["reason"] == "milestone")
        assert ms["gists"] == ["MILESTONE: NIGHT FOLD: doctrine v2"]

    def test_gists_bounded(self, tmp_path):
        spec = [step(f"2026-09-01T00:00:{i:02d}Z", command=f"cmd{i}") for i in range(9)]
        (rows, _), cites = self.rows_for(tmp_path, spec)
        entries = tm.cluster_signals(rows, cites["cited_by"])
        assert len(entries) == 1
        assert len(entries[0]["gists"]) == tm.GISTS_PER_ENTRY + 1  # +N more line
        assert entries[0]["gists"][-1] == f"+{9 - tm.GISTS_PER_ENTRY} more"


class TestCoverageAndDiff:
    def fixture_rows(self):
        # 20 rows: 6 signal (4 venv-instrument + 1 milestone + 1 pytest),
        # 14 noise (1 venv + 1 pytest + 12 echo in a pure-noise session)
        def row(lineno, coarse, signal, session="s1", reasons=("receipt_minute",),
                face="bash"):
            return {"lineno": lineno, "parsed": True, "ts": "2026-09-01T00:00:10Z",
                    "session_id": session, "face": face, "coarse": coarse,
                    "command": "x" * 10, "exit": 0, "truncated": False, "output": "y",
                    "signal": signal, "reasons": list(reasons) if signal else []}

        rows = [row(1 + i, ".venv Scripts python.exe", True) for i in range(4)]
        rows.append(row(5, ".venv Scripts python.exe", False))
        rows.append(row(6, "python -m mag", True, reasons=("milestone",),
                        face="milestone"))
        rows.append(row(7, "pytest", True))
        rows.append(row(8, "pytest", False))
        rows += [row(9 + i, "echo", False, session="s2") for i in range(12)]
        return rows

    def test_coverage_counts(self):
        rows = self.fixture_rows()
        cov = tm.coverage(rows, {"lines": 20, "parsed": 20, "malformed": 0},
                          [{"rows": 3}] * 2, {})
        assert cov["signal_rows"] == 6
        assert cov["signal_rows_pct"] == 30.0
        assert cov["substance"]["milestones"] == "1/1"
        assert cov["substance"]["distinct_coarse_shapes"] == "3/4"
        assert cov["sessions"] == {"total": 2, "with_signal": 1, "pure_noise": 1}
        assert cov["compression"]["cluster_entries"] == 2

    def test_differentiator_enrichment_and_floor(self):
        rows = self.fixture_rows()
        diff = tm.differentiate(rows, min_count=5)
        venv = next(v for v in diff["enriched_in_signal"]
                    if v["verb"] == ".venv Scripts python.exe")
        assert venv["signal_rows"] == 4 and venv["noise_rows"] == 1
        assert venv["signal_pct"] == round(100 * 4 / 6, 2)
        # echo: 12 noise rows vs 0 signal -> depleted (12 >= min_count 5)
        assert any(v["verb"] == "echo" for v in diff["depleted_in_signal"])
        # pytest has 2 total rows < 5 -> never ranked
        assert not any(v["verb"] == "pytest"
                       for v in diff["enriched_in_signal"] + diff["depleted_in_signal"])
        assert "exit_nonzero_pct" in diff["honest_negatives"]

    def test_differentiator_degenerate_split(self):
        rows = [r for r in self.fixture_rows() if r["signal"]]
        assert "error" in tm.differentiate(rows)


class TestCli:
    def cli_args(self, tmp_path):
        return ["--steps", str(tmp_path / "steps.jsonl"),
                "--inbox", str(tmp_path / "inbox"),
                "--output", str(tmp_path / "min.jsonl"),
                "--report", str(tmp_path / "report.json")]

    def clean_tree(self, tmp_path):
        inbox = tmp_path / "inbox"
        inbox.mkdir()
        (inbox / "R_2026-09-01.md").write_text(
            "landed 2026-09-01T00:05Z", encoding="utf-8")
        write_steps(tmp_path / "steps.jsonl", [
            step("2026-09-01T00:05:10Z"), step("2026-09-01T00:06:00Z")])

    def test_ok_exits_zero_and_writes_both(self, tmp_path, capsys):
        self.clean_tree(tmp_path)
        assert tm.main(self.cli_args(tmp_path)) == tm.EXIT_OK
        out = capsys.readouterr().out
        assert "MINIMAL TRAJECTORY" in out and "50.0%" in out
        lines = (tmp_path / "min.jsonl").read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 1 and json.loads(lines[0])["reason"] == "receipt_minute"
        report = json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))
        assert report["coverage"]["substance"]["milestones"] == "0/0"

    def test_missing_steps_exits_two(self, tmp_path, capsys):
        self.clean_tree(tmp_path)
        args = self.cli_args(tmp_path)
        args[args.index("--steps") + 1] = str(tmp_path / "nope.jsonl")
        assert tm.main(args) == tm.EXIT_USAGE
        assert "IO-ERROR" in capsys.readouterr().err

    def test_zero_citation_inbox_fails_closed(self, tmp_path, capsys):
        inbox = tmp_path / "inbox"
        inbox.mkdir()
        (inbox / "DAY.md").write_text("quiet day, no times cited", encoding="utf-8")
        write_steps(tmp_path / "steps.jsonl", [step("2026-09-01T00:00:00Z")])
        assert tm.main(self.cli_args(tmp_path)) == tm.EXIT_USAGE
        assert "ZERO minute citations" in capsys.readouterr().err
