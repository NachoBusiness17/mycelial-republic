"""tests for tools/quote_hitrate.py - standing quote hit-rate sampler.

Offline only, $0, stdlib only: tmp fixtures exercise the three contract paths
(sample verdict with hits and misses filed into the JSONL record, NO-SAMPLE
fail-open exit 0, and multi-source extraction across judge verdict rows,
quote-audit units and local-source lane rows). No network, no estate writes
under test: every fixture lives in tmp_path.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOL = ROOT / "tools" / "quote_hitrate.py"

# HEADLESS law: explicit creationflags (ratchet tests/test_headless_law.py; bare-spawn-descent 2026-09-29)
HEADLESS = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if sys.platform == "win32" else 0

SOURCE_TEXT = (
    "The estate files receipts, not claims.\n"
    "Verbatim quotes must match the cited source byte for byte.\n"
)

HIT_QUOTE = "Verbatim quotes must match the cited source byte for byte."


def run_tool(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(TOOL), *args],
        capture_output=True,
        text=True,
        creationflags=HEADLESS,
    )


def make_estate(tmp_path: Path, verdicts: list[dict], extra_units: list[dict] | None = None) -> tuple[Path, Path]:
    """Write one source file plus verdict jsons into tmp_path; return (root, jsonl)."""
    root = tmp_path / "inbox"
    root.mkdir(parents=True, exist_ok=True)
    (root / "hit_source.md").write_text(SOURCE_TEXT, encoding="utf-8")
    (root / "verdicts.json").write_text(json.dumps(verdicts), encoding="utf-8")
    if extra_units:
        (root / "audit.results.json").write_text(json.dumps({"units": extra_units}), encoding="utf-8")
    return root, tmp_path / "out" / "quote_hitrate.jsonl"


def test_sample_hit_and_miss_files_row(tmp_path: Path) -> None:
    verdicts = [
        {"evidence_quote": HIT_QUOTE, "cited_file": "hit_source.md"},
        {"evidence_quote": HIT_QUOTE, "cited_file": "hit_source.md"},
        {"evidence_quote": HIT_QUOTE, "cited_file": "hit_source.md"},
        {"evidence_quote": "this sentence is nowhere in the source", "cited_file": "hit_source.md"},
        {"evidence_quote": "also a paraphrase, gate must catch it", "cited_file": "hit_source.md"},
    ]
    root, jsonl = make_estate(tmp_path, verdicts)
    proc = run_tool(str(root), "--jsonl", str(jsonl))
    assert proc.returncode == 0, proc.stderr
    assert "NO-SAMPLE" not in proc.stdout
    assert "QUOTE-HITRATE: 3/5 = 60.0%" in proc.stdout
    assert proc.stdout.count("MISS: ") == 2
    assert "row filed" in proc.stdout
    rows = [json.loads(line) for line in jsonl.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 1
    row = rows[0]
    assert set(row) == {"ts", "sample", "hits", "misses", "miss_paths"}
    assert row["sample"] == 5 and row["hits"] == 3 and row["misses"] == 2
    assert len(row["miss_paths"]) == 2
    assert all(p.endswith("hit_source.md") for p in row["miss_paths"])


def test_multi_source_extraction(tmp_path: Path) -> None:
    sub = tmp_path / "inbox" / "corpus"
    sub.mkdir(parents=True)
    (sub / "doc.md").write_text("quote B lives here\n", encoding="utf-8")
    (tmp_path / "inbox" / "lane_src.txt").write_text("quote C lives here\n", encoding="utf-8")
    verdicts = [{"evidence_quote": HIT_QUOTE, "cited_file": "hit_source.md"}]
    extra = [
        {"text": "quote B lives here", "dir": "corpus", "file": "doc.md", "verdict": "HIT"},
        {"quote": "quote C lives here", "source": "lane_src.txt"},
    ]
    root, jsonl = make_estate(tmp_path, verdicts, extra_units=extra)
    # 3 units is still below min-sample; drop the floor to exercise the audit
    # and lane-row extractors, all three must gate as hits
    proc = run_tool(str(root), "--jsonl", str(jsonl), "--min-sample", "3")
    assert proc.returncode == 0, proc.stderr
    assert "QUOTE-HITRATE: 3/3 = 100.0%" in proc.stdout
    assert "gateable=3" in proc.stdout


def test_no_sample_fails_open(tmp_path: Path) -> None:
    root, jsonl = make_estate(tmp_path, [{"evidence_quote": HIT_QUOTE, "cited_file": "hit_source.md"}])
    proc = run_tool(str(root), "--jsonl", str(jsonl))
    assert proc.returncode == 0, proc.stderr
    assert "NO-SAMPLE" in proc.stdout
    assert "gateable=1" in proc.stdout
    assert not jsonl.exists(), "NO-SAMPLE must not file an empty row"


def test_no_sample_empty_root(tmp_path: Path) -> None:
    root = tmp_path / "empty"
    root.mkdir()
    jsonl = tmp_path / "out.jsonl"
    proc = run_tool(str(root), "--jsonl", str(jsonl))
    assert proc.returncode == 0, proc.stderr
    assert "gateable=0" in proc.stdout
    assert "NO-SAMPLE" in proc.stdout
    assert not jsonl.exists()
