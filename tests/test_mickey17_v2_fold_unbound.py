"""A14 unbound-aggregate gate in tools/mickey17_v2_fold.py (the 191.8M ERRATA class).

Founding phantom: STORY.md:240 claimed 191.8M tokens spent citing
watch/inbox/frontier_olm_20260928/DIGEST.md, a file carrying no such number
(watch/inbox/48h_synth/ERRATA.md, ERRATA 001). The fixture rebuilds that
shape in miniature and proves the gate trips on it, and that a bound control
line does not trip.
"""
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools"))
import mickey17_v2_fold as fold  # noqa: E402


def test_unbound_aggregate_trips_and_bound_control_passes(tmp_path):
    digest = tmp_path / "dig" / "DIGEST.md"
    digest.parent.mkdir()
    digest.write_text(
        "The sweep returned 32 of 32 ok and 21 confirmed finds.\n", encoding="utf-8"
    )
    master = tmp_path / "MASTER.md"
    master.write_text(
        "The mine spent 191.8M tokens (source: dig/DIGEST.md).\n"
        "The sweep returned 32 of 32 ok (dig/DIGEST.md).\n",
        encoding="utf-8",
    )

    fails = fold.unbound_aggregates(master, tmp_path)

    assert len(fails) == 1, f"expected exactly the phantom flagged, got {fails}"
    f = fails[0]
    assert f["line"] == 1
    assert f["number"] == "191.8M"
    assert "dig/DIGEST.md" in f["sources"]
    # R3 move 5: resolvable lines are labeled unbound, never weakened
    assert f["kind"] == "unbound"


# --- R3 move 5 (ouroboros 2026-10-05, SYNTHESIS row 5): the banked
# NO_SUCH_FILE fixture. The 900M probe line (a notable aggregate citing only
# a path that resolves nowhere) passed check-master exit 0 before the fix,
# so the founding 191.8M class survived one dead-path citation. The named
# path does not exist in the repo and must never be created.
DEAD_CITE_LINE = "The sweep burned 900M tokens (see watch/inbox/NO_SUCH_FILE_20261005.md).\n"


def test_unresolved_source_is_a_finding(tmp_path):
    master = tmp_path / "MASTER.md"
    master.write_text(DEAD_CITE_LINE, encoding="utf-8")

    fails = fold.unbound_aggregates(master, tmp_path)

    assert len(fails) == 1, f"the dead-path aggregate must not be silent: {fails}"
    f = fails[0]
    assert f["kind"] == "unresolved-source"
    assert f["number"] == "900M"
    assert "watch/inbox/NO_SUCH_FILE_20261005.md" in f["sources"]


def test_unresolved_source_gate_exits_2(tmp_path):
    master = tmp_path / "MASTER.md"
    master.write_text(DEAD_CITE_LINE, encoding="utf-8")

    proc = subprocess.run(
        [sys.executable, str(REPO / "tools" / "mickey17_v2_fold.py"),
         "--check-master", str(master)],
        capture_output=True, text=True, timeout=120,
    )

    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert "UNRESOLVED-SOURCE" in proc.stdout
    assert "900M" in proc.stdout


def test_unbound_aggregate_gate_exits_2(tmp_path):
    digest = tmp_path / "dig" / "DIGEST.md"
    digest.parent.mkdir()
    digest.write_text("no aggregate here\n", encoding="utf-8")
    master = tmp_path / "MASTER.md"
    master.write_text(
        "The mine spent 191.8M tokens (source: dig/DIGEST.md).\n", encoding="utf-8"
    )

    proc = subprocess.run(
        [sys.executable, str(REPO / "tools" / "mickey17_v2_fold.py"),
         "--check-master", str(master)],
        capture_output=True, text=True, timeout=120,
    )

    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert "UNBOUND AGGREGATES" in proc.stdout
    assert "191.8M" in proc.stdout
