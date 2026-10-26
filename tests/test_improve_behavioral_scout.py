"""B2-374: pinned counting contract for the behavioral-events scout (mag/improve.py).

The scout's behavioral row once counted kinds with a JSON-field rule but
EMITTED the census tokens and the free-form samples into one string, so a
row whose detail quoted a counted kind literal (a digest row reading
"tool_fail=12 collapse=3") printed a phantom census token for a kind the
census never counted, and no test could tell census from prose inside the
emitted line. behavioral_events_census now pins the row-level contract:
window = the LAST 80 raw lines (blank and unparseable lines consume slots
exactly as the pre-B2-374 scout did); events = window lines that parse to
JSON objects, ONE line is ONE row; kinds count the "kind" FIELD only, a
detail never counts even when it quotes a counted literal; samples = the
first 5 counted rows as "kind:detail[:80]". The scout row detail now
separates census from prose on a " samples: " marker, so the census
section carries exactly the counted kinds. Delta on old math: one
non-dict JSON row used to abort the whole block via the outer except
(emitting no row at all); the census skips that row and keeps the rest.
Falsifier and receipt:
watch/inbox/burn_wave_20260926/B2_374_behavioral_pin_20260926.md; probe
artifact watch/inbox/burn_wave_20260926/B2_374_falsifier_probe.py imports
these constants so probe and pins cannot drift. Pattern and neighboring
pin: tests/test_improve_crash_scout.py (B2-357).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

TOOL_FAIL_ROW = (
    '{"ts": "2026-09-26T12:00:01+00:00", "kind": "tool_fail", '
    '"detail": "provider socket died on run_turn", "tool": "run_turn"}\n'
)
COLLAPSE_ROW = (
    '{"ts": "2026-09-26T12:00:02+00:00", "kind": "collapse", '
    '"detail": "seat loop stalled 3 cycles", "tool": null}\n'
)
# The brief falsifier's row: a digest row whose DETAIL quotes counted
# kind literals. Under the old emission this printed phantom census
# tokens tool_fail=12 and collapse=3 for kinds the census never counted.
QUOTED_DIGEST_ROW = (
    '{"ts": "2026-09-26T12:00:03+00:00", "kind": "digest", '
    '"detail": "earlier tail read tool_fail=12 collapse=3", "tool": null}\n'
)
KINDLESS_ROW = (
    '{"ts": "2026-09-26T12:00:04+00:00", "detail": "row with no kind field"}\n'
)
PRO_FIRE_ROW = (
    '{"ts": "2026-09-26T12:00:05+00:00", "kind": "pro_fire", '
    '"detail": "[steer] deliberate ask", "tool": "steer"}\n'
)
NONDICT_ROW = "12345\n"
JUNK_LINE = "not json at all\n"
BLANK_LINE = "\n"


def old_scout_emission(kinds: dict[str, int], samples: list[str]) -> str:
    """The pre-B2-374 detail line, kept here only to pin the disease it
    had: census kind tokens and free-form samples share one string, so a
    quoted literal inside a sample detail reads as a census token."""
    return (
        "; ".join(f"{k}={v}" for k, v in sorted(kinds.items()))
        + " · "
        + "; ".join(samples)
    )


def test_census_counts_rows_by_kind_field_only():
    from mag.improve import behavioral_events_census

    text = TOOL_FAIL_ROW + COLLAPSE_ROW + QUOTED_DIGEST_ROW + KINDLESS_ROW
    census = behavioral_events_census(text)
    assert census["events"] == 4
    # tool_fail stays at 1: the digest row's quoted "tool_fail=12" never
    # counts; the kindless row counts under the historical "event" label.
    assert census["kinds"] == {
        "collapse": 1,
        "digest": 1,
        "event": 1,
        "tool_fail": 1,
    }
    assert len(census["samples"]) == 4
    assert census["samples"][0] == "tool_fail:provider socket died on run_turn"


def test_brief_falsifier_quoted_literal_never_counts_or_emits():
    from mag.improve import behavioral_events_census

    census = behavioral_events_census(QUOTED_DIGEST_ROW)
    assert census["kinds"] == {"digest": 1}
    assert "tool_fail" not in census["kinds"]
    assert "collapse" not in census["kinds"]
    # Disease demo on the old emission: the quoted literals surface as
    # census-shaped tokens for kinds the census never counted.
    old_detail = old_scout_emission(census["kinds"], census["samples"])
    assert "tool_fail=12" in old_detail
    assert "collapse=3" in old_detail


def test_window_is_last_80_raw_lines():
    from mag.improve import behavioral_events_census

    outside = "".join(
        '{"ts": "t", "kind": "tool_fail", "detail": "old %d"}\n' % i
        for i in range(5)
    )
    inside = "".join(
        '{"ts": "t", "kind": "collapse", "detail": "new %d"}\n' % i
        for i in range(80)
    )
    census = behavioral_events_census(outside + inside)
    assert census["events"] == 80
    assert census["kinds"] == {"collapse": 80}
    # The reverse cut: the 5 OLDEST collapse rows fall outside while the
    # newest tool_fail rows stay inside (75 + 5 = the 80-line window).
    census_rev = behavioral_events_census(inside + outside)
    assert census_rev["events"] == 80
    assert census_rev["kinds"] == {"collapse": 75, "tool_fail": 5}


def test_blank_and_unparseable_lines_consume_window_slots():
    from mag.improve import behavioral_events_census

    events_then_junk = TOOL_FAIL_ROW * 5 + JUNK_LINE * 80
    assert behavioral_events_census(events_then_junk)["events"] == 0
    junk_then_events = (JUNK_LINE + BLANK_LINE) * 40 + TOOL_FAIL_ROW * 80
    assert behavioral_events_census(junk_then_events)["events"] == 80


def test_nondict_json_row_skipped_not_fatal():
    """Delta on old math: one non-dict JSON row used to raise inside the
    scout block and the outer except silently dropped the WHOLE row."""
    from mag.improve import behavioral_events_census

    text = TOOL_FAIL_ROW + NONDICT_ROW + COLLAPSE_ROW
    census = behavioral_events_census(text)
    assert census["events"] == 2
    assert census["kinds"] == {"collapse": 1, "tool_fail": 1}


def test_samples_cap_at_five():
    from mag.improve import behavioral_events_census

    text = "".join(
        '{"ts": "t", "kind": "k%d", "detail": "%s"}\n' % (i, "x" * 100)
        for i in range(6)
    )
    census = behavioral_events_census(text)
    assert census["events"] == 6
    assert len(census["samples"]) == 5
    assert census["samples"][0] == "k0:" + "x" * 80


def test_empty_and_windowless_text():
    from mag.improve import behavioral_events_census

    assert behavioral_events_census("") == {"events": 0, "kinds": {}, "samples": []}
    assert behavioral_events_census(JUNK_LINE * 80) == {
        "events": 0,
        "kinds": {},
        "samples": [],
    }


def test_scout_row_names_census_and_segregates_samples(tmp_path, monkeypatch):
    import mag.improve as improve_mod

    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    text = TOOL_FAIL_ROW + COLLAPSE_ROW + QUOTED_DIGEST_ROW + KINDLESS_ROW
    (log_dir / "behavioral_events.jsonl").write_text(text, encoding="utf-8")
    monkeypatch.setattr(improve_mod, "ROOT", tmp_path)

    rows = [
        r
        for r in improve_mod._behavioral_candidates("2026-09-26")
        if r.get("claim", "").startswith("Behavioral events log:")
    ]
    assert len(rows) == 1
    row = rows[0]
    assert "census events=4" in row["claim"], row["claim"]
    assert "kinds=4" in row["claim"], row["claim"]
    assert "census events=4" in row["detail"], row["detail"]
    # B2-420 relabel (2026-09-26): the "seat errors" number is the error-kind
    # count (tool_fail counts), the census naming stays in claim and detail,
    # and the detail census section carries events, error_kind_events,
    # error_kinds, kinds, and the 4 kind counts.
    assert "error_kind_events=1" in row["claim"], row["claim"]
    census_section = row["detail"].split(" samples: ")[0]
    eq_tokens = [t for t in census_section.split() if "=" in t]
    assert sorted(eq_tokens) == sorted(
        ["events=4", "error_kind_events=1", "error_kinds=['tool_fail']",
         "kinds=4", "collapse=1", "digest=1", "event=1", "tool_fail=1"]
    ), census_section
    # The quoted literals live only in the samples section, never census.
    assert "tool_fail=12" not in census_section, census_section
    samples_section = row["detail"].split(" samples: ", 1)[1]
    assert "digest:earlier tail read tool_fail=12 collapse=3" in samples_section
    assert row["kind"] == "risk"
    assert row["status"] == "new"


def test_scout_row_absent_when_window_holds_no_events(tmp_path, monkeypatch):
    import mag.improve as improve_mod

    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    (log_dir / "behavioral_events.jsonl").write_text(
        JUNK_LINE * 80, encoding="utf-8"
    )
    monkeypatch.setattr(improve_mod, "ROOT", tmp_path)

    rows = [
        r
        for r in improve_mod._behavioral_candidates("2026-09-26")
        if r.get("claim", "").startswith("Behavioral events log:")
    ]
    assert rows == []


def test_scout_row_survives_nondict_row(tmp_path, monkeypatch):
    """Old math: the non-dict row aborted the block and the scout emitted
    no behavioral row at all; the census skips the row and keeps 2."""
    import mag.improve as improve_mod

    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    (log_dir / "behavioral_events.jsonl").write_text(
        TOOL_FAIL_ROW + NONDICT_ROW + COLLAPSE_ROW, encoding="utf-8"
    )
    monkeypatch.setattr(improve_mod, "ROOT", tmp_path)

    rows = [
        r
        for r in improve_mod._behavioral_candidates("2026-09-26")
        if r.get("claim", "").startswith("Behavioral events log:")
    ]
    assert len(rows) == 1
    assert "census events=2 error_kind_events=1 kinds=2" in rows[0]["claim"], rows[0]["claim"]  # B2-420 relabel: seat-errors number is the error-kind count
