"""B2-357: pinned counting contract for the seat crash scout (mag/improve.py).

The scout's crash row once computed real = count("Traceback (most recent
call last):") - count("INJECTED-") over the whole log text, so one
chained-exception real crash quoting the marker reported real=0 and one
unquoted chained real crash reported real=2. crash_log_census now counts
ENTRIES (guard stanzas) and classifies a stanza as test only when a body
line STARTS with the INJECTED- marker; the B2-86 annotation suffix rides
inside marker lines after the message and still classifies, while a
mid-message quote never does. Falsifier and receipt:
watch/inbox/burn_wave_20260926/B2_357_scout_pin_20260926.md; probe artifact
watch/inbox/burn_wave_20260926/B2_357_falsifier_probe.py imports these
constants so probe and pins cannot drift.

B2-372: the census must also SAY when a crash was chained. chains counts
the two exception-chain-marker sentences ("During handling of the above
exception" and "The above exception was the direct cause") over the same
bodies blocks and entries count, so an operator reading real=1 can tell a
wrap-and-reraise class from a plain crash without opening the log. The
scout row detail names chains=. Falsifier: a log with one chained stanza
reports entries=1 with no chain count on any surface. Receipt:
watch/inbox/burn_wave_20260926/B2_372_chain_census_20260926.md.

B2-383: chains must not count a QUOTED chain-marker sentence. The B2-372
count is a plain substring count, the same disease class B2-357 closed for
the INJECTED- marker, so an operator crash whose message quotes "During
handling of the above exception" mid-line inflated chains without changing
entries or real. The hardened contract counts a chain-marker sentence only
when a line STARTS with it at column 0 (the shape CPython prints between
chained sections) AND the stanza body holds at least two Traceback headers
(a chain link needs two sections). Falsifier: a single-entry log whose
exception message quotes a chain-marker sentence mid-message reports
chains=1 with entries=1. Receipt:
watch/inbox/burn_wave_20260926/B2_383_chain_quote_pin_20260926.md.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

MARK = "INJECTED-ONESHOT-CRASH"
HEADER = "Traceback (most recent call last):"

PLAIN_REAL = (
    "\n[2026-09-26T12:00:01+00:00] stage=do_turn\n"
    "Traceback (most recent call last):\n"
    '  File "m.py", line 1, in run\n'
    "    step()\n"
    "ValueError: provider socket died\n"
)

CHAINED_REAL_UNQUOTED = (
    "\n[2026-09-26T12:00:04+00:00] stage=one_shot\n"
    "Traceback (most recent call last):\n"
    '  File "m.py", line 5, in persist\n'
    "    save()\n"
    "OSError: disk full\n"
    "\n"
    "During handling of the above exception, another exception occurred:\n"
    "\n"
    "Traceback (most recent call last):\n"
    '  File "m.py", line 9, in run\n'
    "    run_agent()\n"
    "RuntimeError: persist failed after disk full\n"
)

CHAINED_REAL_DIRECT_CAUSE = (
    "\n[2026-09-26T12:00:08+00:00] stage=do_turn\n"
    "Traceback (most recent call last):\n"
    '  File "m.py", line 12, in persist\n'
    "    save()\n"
    "OSError: lock held\n"
    "\n"
    "The above exception was the direct cause of the following exception:\n"
    "\n"
    "Traceback (most recent call last):\n"
    '  File "m.py", line 20, in run\n'
    "    run_agent()\n"
    "RuntimeError: persist failed under lock\n"
)

PLAIN_QUOTED_REAL = (
    "\n[2026-09-26T12:00:03+00:00] stage=do_turn\n"
    "Traceback (most recent call last):\n"
    '  File "audit.py", line 7, in audit\n'
    "    scan(text)\n"
    "ValueError: pollution marker INJECTED- found in operator log line\n"
)

QUOTED_CHAINED_REAL = (
    "\n[2026-09-26T12:00:02+00:00] stage=do_turn\n"
    "Traceback (most recent call last):\n"
    '  File "scrub.py", line 3, in scrub\n'
    "    check(line)\n"
    "ValueError: marker INJECTED- seen in line 12\n"
    "\n"
    "During handling of the above exception, another exception occurred:\n"
    "\n"
    "Traceback (most recent call last):\n"
    '  File "seat.py", line 9, in do_turn\n'
    "    scrub(line)\n"
    "RuntimeError: marker INJECTED- escaped scrub\n"
)

TEST_ANNOTATED = (
    "\n[2026-09-26T12:00:05+00:00] stage=do_turn\n"
    "Traceback (most recent call last):\n"
    '  File "tests/test_seat_crash_guard.py", line 32, in boom_run_turn\n'
    '    raise RuntimeError(f"{MARK}-MIDTURN")\n'
    f"RuntimeError: {MARK}-MIDTURN  [pollution-annotated 2026-09-26 B2-86: "
    "test-injected block from tests/test_seat_crash_guard.py, pre-seam era; "
    "receipt watch/inbox/burn_wave_20260926/B2_86_writer_isolation_20260926.md]\n"
)

TEST_PLAIN = (
    "\n[2026-09-26T12:00:06+00:00] stage=one_shot\n"
    "Traceback (most recent call last):\n"
    '  File "tests/test_seat_crash_guard.py", line 35, in boom_save\n'
    '    raise RuntimeError(f"{MARK}-PERSIST")\n'
    f"RuntimeError: {MARK}-PERSIST\n"
)

REAL_WITH_NEUTRAL_ANNOTATION = (
    "\n[2026-09-26T12:00:07+00:00] stage=do_turn\n"
    "Traceback (most recent call last):\n"
    '  File "m.py", line 2, in run\n'
    "    step()\n"
    "ConnectionError: socket died  [note 2026-09-26: operator annotated]\n"
)

TRACELESS_STANZA = "\n[2026-08-03T06:21:24.554530+00:00]\n"

PREAMBLE = "log opened\nno stanza yet\n"


def old_scout_math(text: str) -> int:
    """The pre-B2-357 arithmetic, kept here only to pin the disease it had."""
    return text.count(HEADER) - text.count("INJECTED-")


def test_plain_real_block():
    from mag.improve import crash_log_census

    assert crash_log_census(PLAIN_REAL) == {
        "blocks": 1,
        "entries": 1,
        "test": 0,
        "real": 1,
        "chains": 0,
    }


def test_chained_real_block_is_one_crash_not_two():
    from mag.improve import crash_log_census

    assert old_scout_math(CHAINED_REAL_UNQUOTED) == 2
    assert crash_log_census(CHAINED_REAL_UNQUOTED) == {
        "blocks": 2,
        "entries": 1,
        "test": 0,
        "real": 1,
        "chains": 1,
    }


def test_direct_cause_marker_counts_chain():
    from mag.improve import crash_log_census

    assert crash_log_census(CHAINED_REAL_DIRECT_CAUSE) == {
        "blocks": 2,
        "entries": 1,
        "test": 0,
        "real": 1,
        "chains": 1,
    }


def test_quoted_marker_never_reclassifies_real_crash():
    from mag.improve import crash_log_census

    assert old_scout_math(PLAIN_QUOTED_REAL) == 0
    assert crash_log_census(PLAIN_QUOTED_REAL)["real"] == 1
    assert crash_log_census(PLAIN_QUOTED_REAL)["test"] == 0


def test_brief_falsifier_chained_quoted_reports_real_one():
    from mag.improve import crash_log_census

    assert old_scout_math(QUOTED_CHAINED_REAL) == 0
    assert crash_log_census(QUOTED_CHAINED_REAL) == {
        "blocks": 2,
        "entries": 1,
        "test": 0,
        "real": 1,
        "chains": 1,
    }


def test_annotated_marker_line_still_classifies_test():
    from mag.improve import crash_log_census

    assert crash_log_census(TEST_ANNOTATED) == {
        "blocks": 1,
        "entries": 1,
        "test": 1,
        "real": 0,
        "chains": 0,
    }
    assert crash_log_census(TEST_PLAIN)["test"] == 1


def test_annotation_suffix_on_real_line_does_not_classify():
    from mag.improve import crash_log_census

    assert crash_log_census(REAL_WITH_NEUTRAL_ANNOTATION) == {
        "blocks": 1,
        "entries": 1,
        "test": 0,
        "real": 1,
        "chains": 0,
    }


def test_mixed_log_census():
    from mag.improve import crash_log_census

    mixed = (
        PREAMBLE
        + TRACELESS_STANZA
        + PLAIN_REAL
        + CHAINED_REAL_UNQUOTED
        + PLAIN_QUOTED_REAL
        + QUOTED_CHAINED_REAL
        + TEST_ANNOTATED
        + TEST_PLAIN
        + REAL_WITH_NEUTRAL_ANNOTATION
    )
    assert crash_log_census(mixed) == {
        "blocks": 9,
        "entries": 7,
        "test": 2,
        "real": 5,
        "chains": 2,
    }


def test_empty_and_headerless_text():
    from mag.improve import crash_log_census

    assert crash_log_census("") == {
        "blocks": 0,
        "entries": 0,
        "test": 0,
        "real": 0,
        "chains": 0,
    }
    assert crash_log_census("no crashes here\n") == {
        "blocks": 0,
        "entries": 0,
        "test": 0,
        "real": 0,
        "chains": 0,
    }
    assert crash_log_census(TRACELESS_STANZA)["entries"] == 0


def test_scout_row_names_census(tmp_path, monkeypatch):
    import mag.improve as improve_mod

    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    mixed = PLAIN_REAL + CHAINED_REAL_UNQUOTED + TEST_ANNOTATED + TEST_PLAIN
    (log_dir / "seat_crashes.log").write_text(mixed, encoding="utf-8")
    monkeypatch.setattr(improve_mod, "ROOT", tmp_path)

    rows = [
        r
        for r in improve_mod._behavioral_candidates("2026-09-26")
        if r.get("claim", "").startswith("Seat crash log:")
    ]
    assert len(rows) == 1
    row = rows[0]
    for token in ("blocks=5", "test=2", "real=2"):
        assert token in row["claim"], row["claim"]
        assert token in row["detail"], row["detail"]
    assert "chains=1" in row["detail"], row["detail"]
    assert row["status"] == "new"


def test_scout_row_holds_when_only_test_blocks(tmp_path, monkeypatch):
    import mag.improve as improve_mod

    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    (log_dir / "seat_crashes.log").write_text(TEST_PLAIN, encoding="utf-8")
    monkeypatch.setattr(improve_mod, "ROOT", tmp_path)

    rows = [
        r
        for r in improve_mod._behavioral_candidates("2026-09-26")
        if r.get("claim", "").startswith("Seat crash log:")
    ]
    assert len(rows) == 1
    row = rows[0]
    assert "blocks=1" in row["claim"] and "test=1" in row["claim"] and "real=0" in row["claim"]
    assert row["status"] == "hold"


def test_scout_row_detail_names_chain_count(tmp_path, monkeypatch):
    """B2-372 falsifier: one chained stanza must not surface as a bare
    entries=1 with no chain count anywhere; the detail names chains=."""
    import mag.improve as improve_mod

    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    (log_dir / "seat_crashes.log").write_text(CHAINED_REAL_DIRECT_CAUSE, encoding="utf-8")
    monkeypatch.setattr(improve_mod, "ROOT", tmp_path)

    rows = [
        r
        for r in improve_mod._behavioral_candidates("2026-09-26")
        if r.get("claim", "").startswith("Seat crash log:")
    ]
    assert len(rows) == 1
    row = rows[0]
    assert "entries=1" in row["detail"], row["detail"]
    assert "chains=1" in row["detail"], row["detail"]
    assert "real=1" in row["claim"], row["claim"]
    assert row["status"] == "new"


# B2-383 fixtures: every shape an operator traceback can carry a QUOTED
# chain-marker sentence in, none of which is a real chained exception.
CHAIN_QUOTED_MID_MESSAGE = (
    "\n[2026-09-26T12:10:01+00:00] stage=do_turn\n"
    "Traceback (most recent call last):\n"
    '  File "config.py", line 14, in load\n'
    "    parse(raw)\n"
    "ValueError: config parser said 'During handling of the above exception' "
    "and stopped\n"
)

CHAIN_QUOTED_SOURCE_ECHO = (
    "\n[2026-09-26T12:10:02+00:00] stage=one_shot\n"
    "Traceback (most recent call last):\n"
    '  File "wrap.py", line 21, in wrap\n'
    '    raise WrapError("The above exception was the direct cause of the '
    'following exception:")\n'
    "WrapError: wrap failed\n"
)

CHAIN_QUOTED_TYPE_PREFIX = (
    "\n[2026-09-26T12:10:03+00:00] stage=do_turn\n"
    "Traceback (most recent call last):\n"
    '  File "relay.py", line 9, in relay\n'
    "    push(event)\n"
    "TypeError: relay log said: During handling of the above exception was "
    "reported upstream\n"
)

CHAIN_QUOTED_MULTILINE_MESSAGE = (
    "\n[2026-09-26T12:10:04+00:00] stage=do_turn\n"
    "Traceback (most recent call last):\n"
    '  File "m.py", line 3, in run\n'
    "    step()\n"
    "RuntimeError: config context follows\n"
    "During handling of the above exception\n"
    "and stopped\n"
)


def test_brief_falsifier_quoted_chain_marker_reports_chains_zero():
    """B2-383 falsifier: a single-entry log whose exception message quotes a
    chain-marker sentence mid-message must not report a chain."""
    from mag.improve import crash_log_census

    assert crash_log_census(CHAIN_QUOTED_MID_MESSAGE) == {
        "blocks": 1,
        "entries": 1,
        "test": 0,
        "real": 1,
        "chains": 0,
    }


def test_quoted_chain_marker_in_source_echo_never_counts():
    from mag.improve import crash_log_census

    census = crash_log_census(CHAIN_QUOTED_SOURCE_ECHO)
    assert census["chains"] == 0, census
    assert census["real"] == 1


def test_quoted_chain_marker_after_type_prefix_never_counts():
    from mag.improve import crash_log_census

    census = crash_log_census(CHAIN_QUOTED_TYPE_PREFIX)
    assert census["chains"] == 0, census
    assert census["real"] == 1


CHAIN_QUOTED_AT_END_OF_TWO_HEADER_STANZA = (
    "\n[2026-09-26T12:10:05+00:00] stage=do_turn\n"
    "Traceback (most recent call last):\n"
    "  File \"m.py\", line 3, in run\n"
    "    step()\n"
    "ValueError: inner failed\n"
    "\n"
    "During handling of the above exception, another exception occurred:\n"
    "Traceback (most recent call last):\n"
    "  File \"m.py\", line 9, in top\n"
    "    run()\n"
    "RuntimeError: outer failed and the operator log quoted verbatim:\n"
    "During handling of the above exception, another exception occurred:\n"
    "(end of operator note)\n"
)


def test_quoted_marker_at_end_of_two_header_stanza_counts_one_join():
    # B2-418 falsifier: a genuine chained stanza (2 headers, one real
    # column-0 join between them) whose FINAL exception message embeds a
    # newline plus the exact marker sentence at column 0 must report the
    # one real join, not a phantom second link. Between-headers placement:
    # a marker line strictly between the first and last header line index
    # counts; a marker line after the last header is quoted message text.
    from mag.improve import crash_log_census

    census = crash_log_census(CHAIN_QUOTED_AT_END_OF_TWO_HEADER_STANZA)
    assert census["blocks"] == 2, census
    assert census["entries"] == 1, census
    assert census["real"] == 1, census
    assert census["chains"] == 1, census

def test_quoted_marker_on_its_own_line_without_second_header_never_counts():
    """A column-0 quote riding a multi-line exception message is still not a
    chain: a chain link needs two Traceback headers in the stanza."""
    from mag.improve import crash_log_census

    assert crash_log_census(CHAIN_QUOTED_MULTILINE_MESSAGE) == {
        "blocks": 1,
        "entries": 1,
        "test": 0,
        "real": 1,
        "chains": 0,
    }


def test_quoted_marker_stanza_does_not_inflate_chained_log():
    from mag.improve import crash_log_census

    mixed = CHAINED_REAL_UNQUOTED + CHAIN_QUOTED_MID_MESSAGE
    assert crash_log_census(mixed) == {
        "blocks": 3,
        "entries": 2,
        "test": 0,
        "real": 2,
        "chains": 1,
    }
