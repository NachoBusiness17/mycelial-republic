#!/usr/bin/env python3
"""tests/test_attention_dam.py - tests for tools/attention_dam.py (Mickey17 W3).

The dam laws under test, from the W3 brief:
  1. fixture flood -> signal preserved (probe-alarm / patrol / gate-canary /
     DRIFT blocks and the preserved-alert sentinel survive in attention.md),
     noise archived (session-record blocks moved verbatim to the dated
     archive, absent from attention.md), pointer note left in the header;
  2. the signal:noise ratio is reported before and after the pass;
  3. idempotent: a second pass writes nothing -- attention.md and the
     archive stay byte-identical, zero blocks re-archived;
  4. conservative classification: a session block carrying an embedded
     [priority] alert line stays; --stats is read-only.

No real memory/ file is touched: every case redirects --attention/--archive
into tmp_path (the same redirection discipline as tests/test_gate_canary.py).

Run: .venv/Scripts/python.exe -m pytest tests/test_attention_dam.py -q
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.attention_dam import SENTINEL, dam_pass, main, stats_of  # noqa: E402


def _session_block(n: int, extra: str = "") -> str:
    return (
        f"### Session record ready (first)\n\n"
        f"- ts: 2026-09-30T02:1{n}:26.460833+00:00\n"
        f"- session: `mag-agent-orc-t15e4b0c9{n}`\n"
        f"- seat: `mag_agent`\n"
        f"- narrative: `/app/memory/biography/derived/mag-agent-orc-{n}.md`\n"
        f"- dossier: `/app/memory/biography/residual/mag-agent-orc-{n}.json`\n"
        f"- also: `memory/biography/latest.md` · brief under `memory/briefs/`\n"
        f"{extra}"
    )


PROBE = (
    "- [priority][probe-alarm] provider_probe DOWN mistral; "
    "QUOTA-DEAD cerebras (run 2026-09-26) -> tmp/improve/provider_health/2026-09-26.json"
)
PATROL_BLOCK = (
    "### Census collect patrol fired (2026-09-29 08:30:02)\n\n"
    "- verdict: CENSUS-PATROL: COLLECT-DRIFT - collected drift: pytest holds "
    "2478 vs carrier claim 2436 (delta +42, bar 20) (exit 1)\n"
    "- log: logs/census_patrol.log\n"
    "- response (exit 1): rerun pytest --collect-only -q, refresh the AGENTS.md bullet"
)
GATE = (
    "- [priority][gate-canary] DEAD caption_ledger_verify: stayed silent on its own "
    "known-bad canary run 2026-09-29 20:45; githooks/pre-push liveness receipt owed"
)


def _flood(n_noise: int = 40, *, embed_signal: bool = True) -> str:
    """A flooded attention.md shaped like the real one (2026-09-30)."""
    sep = "\n\n---\n\n"
    noise = sep.join(_session_block(i) for i in range(n_noise))
    if not embed_signal:
        return f"---\n\n{noise}\n\n"
    tail = f"{SENTINEL}\n{PROBE}\n{GATE}"
    return f"---\n\n{noise}\n\n{tail}\n\n---\n\n{PATROL_BLOCK}\n"


def test_flood_signal_preserved_noise_archived_pointer_left(tmp_path: Path) -> None:
    att = tmp_path / "attention.md"
    arc = tmp_path / "attention_archive_20260930.md"
    att.write_text(_flood(40), encoding="utf-8")

    report = dam_pass(att, arc)

    kept = att.read_text(encoding="utf-8")
    archived = arc.read_text(encoding="utf-8")
    # law 1a: every signal line survives in attention.md
    assert PROBE in kept
    assert GATE in kept
    for line in PATROL_BLOCK.splitlines():
        assert line in kept
    assert SENTINEL in kept  # region contract for mag/act.py stays intact
    # law 1b: noise moved, not deleted -- verbatim in the archive, gone from attention
    assert "### Session record ready" not in kept
    assert archived.count("### Session record ready (first)") == 40
    assert _session_block(7) in archived  # verbatim block content
    assert report["archived_blocks"] == 40
    # law 1c: pointer note in the header names the archive
    assert kept.startswith("# Mag attention")
    assert "<!-- attention-dam:" in kept.splitlines()[1]  # header pointer
    assert arc.name in kept


def test_ratio_reported_before_and_after(tmp_path: Path) -> None:
    att = tmp_path / "attention.md"
    arc = tmp_path / "attention_archive_20260930.md"
    att.write_text(_flood(40), encoding="utf-8")

    report = dam_pass(att, arc)

    before, after = report["before"], report["after"]
    # ratio reported in both directions
    assert "signal_noise_ratio" in before and "signal_noise_ratio" in after
    # 40 noise blocks x 8 lines archived; signal lines fully preserved
    assert before["noise_blocks"] == 40
    assert after["noise_blocks"] == 0
    assert after["noise_lines"] == 0
    assert after["signal_lines"] == before["signal_lines"]
    assert after["signal_blocks"] == before["signal_blocks"]
    # before-ratio was heavy noise (40 blocks of 8 lines vs ~13 signal lines)
    bn, sn = before["noise_lines"], before["signal_lines"]
    assert bn > sn
    assert after["signal_noise_ratio"] == f"{after['signal_lines']}:0"


def test_idempotent_second_pass_writes_nothing(tmp_path: Path) -> None:
    att = tmp_path / "attention.md"
    arc = tmp_path / "attention_archive_20260930.md"
    att.write_text(_flood(5), encoding="utf-8")

    dam_pass(att, arc)
    snap_att = att.read_text(encoding="utf-8")
    snap_arc = arc.read_text(encoding="utf-8")

    report2 = dam_pass(att, arc)

    assert report2["archived_blocks"] == 0
    assert report2["wrote"] is False
    assert att.read_text(encoding="utf-8") == snap_att  # byte-identical
    assert arc.read_text(encoding="utf-8") == snap_arc  # byte-identical


def test_new_noise_after_dam_gets_archived_once(tmp_path: Path) -> None:
    """Dam is reusable: a later flood pass archives only the new blocks."""
    att = tmp_path / "attention.md"
    arc = tmp_path / "attention_archive_20260930.md"
    att.write_text(_flood(2), encoding="utf-8")
    dam_pass(att, arc)
    dammed = att.read_text(encoding="utf-8")

    # biography floods again on top of the dammed file (newest-first prepend)
    head = "---\n\n" + "\n\n---\n\n".join(_session_block(i) for i in range(3)) + "\n\n"
    att.write_text(head + dammed, encoding="utf-8")
    report = dam_pass(att, arc)

    assert report["archived_blocks"] == 3
    kept = att.read_text(encoding="utf-8")
    assert "### Session record ready" not in kept
    assert PROBE in kept and SENTINEL in kept
    assert arc.read_text(encoding="utf-8").count("### Session record ready (first)") == 5


def test_conservative_session_block_with_embedded_alert_stays(tmp_path: Path) -> None:
    att = tmp_path / "attention.md"
    arc = tmp_path / "attention_archive_20260930.md"
    # a bottom-appender dropped a probe-alarm INSIDE a session block's chunk
    flood = _flood(2) + "\n\n---\n\n" + _session_block(9, extra=f"{PROBE}\n")
    att.write_text(flood, encoding="utf-8")

    dam_pass(att, arc)

    kept = att.read_text(encoding="utf-8")
    # the mixed block is kept whole (never split, never archived)
    assert "### Session record ready" in kept
    assert PROBE in kept
    assert arc.read_text(encoding="utf-8").count("### Session record ready (first)") == 2


def test_stats_mode_is_read_only(tmp_path: Path, capsys) -> None:
    att = tmp_path / "attention.md"
    att.write_text(_flood(6), encoding="utf-8")
    before_bytes = att.read_bytes()

    rc = main(["--stats", "--attention", str(att)])

    out = capsys.readouterr().out
    assert rc == 0
    assert "ratio signal:noise" in out
    assert "noise=48 lines/6 blocks" in out
    assert att.read_bytes() == before_bytes  # untouched


def test_stats_counts_on_synthetic_states(tmp_path: Path) -> None:
    st = stats_of(_flood(4))
    assert st.noise_blocks == 4
    assert st.noise_lines == 4 * 8
    assert st.signal_blocks == 2  # sentinel/alert tail + patrol block
    # signal tail = sentinel + PROBE + GATE = 3 lines; patrol block = 5 lines
    assert st.signal_lines == 8
    assert st.ratio == "1:4"
