"""Eviction-order test: bottom-appended patrol alerts structurally survive the
session-record flood in memory/attention.md.

Guards the inverted eviction (w4-09 section 1): biography.py prepended newest-
first and beheaded prev[:40000] while the census patrol (scripts/
census_patrol_daily.ps1 Add-Content :79/:109/:150/:170) and improve.py (:535,
mode "a") appended at the bottom, so the bottom was the eviction zone and the
2026-09-26 COLLECT-DRIFT plus 2026-09-28 fleet-task-doctor alerts were beheaded
within hours of their append. Since this file exists, an eviction that touches
the preserved alert tail is a red test, not a lost incident.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone

import mag.act as act
import mag.biography as biography

SENTINEL = act.ATTENTION_ALERT_SENTINEL
PATROL_ALERT = (
    "\n---\n\n### Census collect patrol fired (2026-09-30T08:30:30)\n\n"
    "- verdict: COLLECT-DRIFT (exit 1)\n"
    "- log: `logs/census_patrol.log`\n"
    "- response (exit 1): rerun pytest --collect-only -q, refresh the claim.\n"
)
DOCTOR_ALERT = (
    "\n---\n\n### Fleet task doctor fired (2026-09-30T08:31:00)\n\n"
    "- MagSomeTask: last result 1 at 2026-09-30 08:30:00\n"
)


def _tmp_estate(tmp_path, monkeypatch):
    """Redirect every attention-surface writer the flood touches to tmp."""
    monkeypatch.setattr(biography, "ROOT", tmp_path)
    monkeypatch.setattr(act, "ROOT", tmp_path)
    return tmp_path


def _seed_repaired_file(tmp_path) -> None:
    """The 2026-09-29 live repair shape: header + compacted note + sentinel."""
    (tmp_path / "memory").mkdir(parents=True, exist_ok=True)
    (tmp_path / "memory" / "attention.md").write_text(
        "# Mag attention\n\nCompacted 2026-09-29.\n\n" + SENTINEL + "\n",
        encoding="utf-8",
    )


def _flood(tmp_path, n: int) -> None:
    for i in range(n):
        out = biography.ping_session_record(
            sid=f"mag-agent-flood-{i:04d}",
            seat="mag_agent",
            narrative=f"/app/memory/biography/derived/mag-agent-flood-{i:04d}.md",
            pack={},
            exists=False,
            force=False,
            incomplete=True,
        )
        assert out["pinged"] is True


def _body(tmp_path) -> str:
    return (tmp_path / "memory" / "attention.md").read_text(encoding="utf-8")


def _assert_no_partial_record(body: str) -> None:
    """Every record chunk in the evictable region is a whole block.

    The old prev[:cap] behead sliced mid-identifier (w4-09: the file's last
    line ended inside 'mag-agent-orc-t0'), feeding consumers that split on
    separator lines a headless half-record. Under flood even the '# Mag
    attention' title line is evictable (oldest content first), so chunk 0 may
    be empty: the invariant is that NO chunk is a headless fragment.
    """
    evictable = body.split(SENTINEL, 1)[0]
    chunks = evictable.split("\n---\n")
    for chunk in chunks:
        if not chunk.strip():
            continue
        assert "### Session record ready" in chunk, f"headless chunk: {chunk[:80]!r}"
        assert chunk.rstrip().endswith("brief under `memory/briefs/`"), (
            f"partial record at eviction boundary: ...{chunk[-80:]!r}"
        )


def test_patrol_alert_survives_a_full_record_flood(tmp_path, monkeypatch):
    _tmp_estate(tmp_path, monkeypatch)
    _seed_repaired_file(tmp_path)
    att = tmp_path / "memory" / "attention.md"
    with att.open("a", encoding="utf-8") as f:  # the patrol's Add-Content shape
        f.write(PATROL_ALERT)

    _flood(tmp_path, 200)  # ~66KB of session records through a 40KB cap

    body = _body(tmp_path)
    assert SENTINEL in body
    assert "### Census collect patrol fired" in body, "patrol alert was evicted"
    assert "COLLECT-DRIFT (exit 1)" in body
    _assert_no_partial_record(body)
    # bounded: cap applies to records, preserved tail rides on top
    assert len(body) <= 40000 + len(PATROL_ALERT) + 1000


def test_second_patrol_alert_joins_the_first_and_both_survive(tmp_path, monkeypatch):
    _tmp_estate(tmp_path, monkeypatch)
    _seed_repaired_file(tmp_path)
    att = tmp_path / "memory" / "attention.md"
    with att.open("a", encoding="utf-8") as f:
        f.write(PATROL_ALERT)
    _flood(tmp_path, 200)
    with att.open("a", encoding="utf-8") as f:
        f.write(DOCTOR_ALERT)
    _flood(tmp_path, 200)

    body = _body(tmp_path)
    assert "### Census collect patrol fired" in body
    assert "### Fleet task doctor fired" in body
    _assert_no_partial_record(body)


def test_improve_style_bottom_append_survives_too(tmp_path, monkeypatch):
    _tmp_estate(tmp_path, monkeypatch)
    _seed_repaired_file(tmp_path)
    att = tmp_path / "memory" / "attention.md"
    line = "- [priority][probe-alarm] provider_probe degraded (run 2026-09-30) -> x\n"
    with att.open("a", encoding="utf-8") as f:  # mag/improve.py:535 mode "a" shape
        f.write(line)
    _flood(tmp_path, 200)
    assert "[priority][probe-alarm]" in _body(tmp_path)


def test_eviction_keeps_whole_blocks_and_never_drops_the_new_note(tmp_path, monkeypatch):
    prev = (
        "# Mag attention\n"
        + "\n---\n\n### Session record ready (first)\n\n- session: `old-1`\n- also: `x`\n\n"
        + "\n---\n\n### Session record ready (first)\n\n- session: `old-2`\n- also: `x`\n\n"
    )
    note = "\n---\n\n### Session record ready (first)\n\n- session: `new`\n- also: `x`\n\n"
    body = act.evict_for_prepend(prev, note, cap=90)
    assert body.startswith(note), "the newest note is never evicted"
    assert SENTINEL in body, "sentinel seeded on first contract write"


def test_preserved_tail_is_never_sliced_even_past_cap(tmp_path, monkeypatch):
    alert = "\n" + SENTINEL + "\n\n### Patrol fired\n\n- verdict: HARD\n" * 3
    prev = "# Mag attention\n\n---\n\n### old record\n- also: x\n" + alert
    note = "\n---\n\n### new ping\n- session: `n`\n"
    body = act.evict_for_prepend(prev, note, cap=40)  # cap smaller than the tail
    assert body.count("### Patrol fired") == 3
    assert body.startswith(note)


def test_ping_dedup_unchanged_amend_does_not_ping(tmp_path, monkeypatch):
    _tmp_estate(tmp_path, monkeypatch)
    _seed_repaired_file(tmp_path)
    before = _body(tmp_path)
    out = biography.ping_session_record(
        sid="s", seat="mag_agent", narrative="n", pack={},
        exists=True, force=False, incomplete=False,
    )
    assert out == {"pinged": False}
    assert _body(tmp_path) == before


def test_ping_stamps_a_ts_and_meters_the_flood(tmp_path, monkeypatch):
    _tmp_estate(tmp_path, monkeypatch)
    _seed_repaired_file(tmp_path)
    _flood(tmp_path, 3)
    body = _body(tmp_path)
    assert body.count("- ts: 20") == 3, "every ping carries a timestamp"
    counter = tmp_path / "watch" / "attention_count_day.txt"
    text = counter.read_text(encoding="utf-8").strip()
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2} 3", text), (
        f"counter must stay in the daemon-readable 'YYYY-MM-DD N' shape, got {text!r}"
    )


def test_counter_rotates_on_stale_day_and_garbage(tmp_path, monkeypatch):
    _tmp_estate(tmp_path, monkeypatch)
    stale = tmp_path / "watch"
    stale.mkdir(parents=True, exist_ok=True)
    (stale / "attention_count_day.txt").write_text("2026-08-07 48\n", encoding="utf-8")
    day, count = act.bump_attention_count()
    assert count == 1, "a 52-day-stale counter restarts at 0, it does not freeze"
    (stale / "attention_count_day.txt").write_text("garbage bytes", encoding="utf-8")
    _day, count = act.bump_attention_count()
    assert count == 1, "an unparsable counter restarts, it does not stay dead"


def test_over_cap_attention_is_filed_but_push_suppressed(tmp_path, monkeypatch):
    _tmp_estate(tmp_path, monkeypatch)
    att = tmp_path / "memory" / "attention.md"
    att.parent.mkdir(parents=True, exist_ok=True)
    att.write_text("# Mag attention\n\n" + SENTINEL + "\n", encoding="utf-8")
    counter = tmp_path / "watch" / "attention_count_day.txt"
    counter.parent.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    counter.write_text(f"{today} 2\n", encoding="utf-8")  # cap 2 already spent
    pol = {"attention_path": str(att), "max_attention_per_day": 2}
    res = act._do_attention({"attention_text": "ping over cap"}, pol)
    assert res["suppressed"] is True
    assert res["count_today"] == 3
    body = att.read_text(encoding="utf-8")
    assert "ping over cap" in body, "over-cap alerts are still FILED, only the push is capped"
    assert not (tmp_path / "watch" / "attention_flag.txt").exists(), "no push over cap"
