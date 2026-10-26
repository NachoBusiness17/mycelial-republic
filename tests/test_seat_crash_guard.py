"""Seat crash-guard LIVE test (Run 1 refine): one-shot crash -> nonzero exit + log.

Exercises the REAL run_agent one-shot path with injected failures:
  - run_turn raises mid-turn (provider-style crash) -> do_turn inner guard
    recovers and logs stage=do_turn.
  - save_session raises during persist (post-turn persistence crash) ->
    propagates out of do_turn -> one_shot outer guard -> _log_seat_crash
    stage=one_shot + return 1 (nonzero exit).

Exit-code propagation: run_agent returns 1; main_argv sys.exit(main_argv()) -> 1.

B2-86 (2026-09-26): the crash-log sink is injected per test via the
MAG_SEAT_CRASH_LOG seam in _log_seat_crash; the production
logs/seat_crashes.log must stay byte-identical across each test. Pre-fix
runs appended INJECTED-* traceback blocks to the production log (372 of the
424 "guard caught N total" blocks on bytes at fix time, 52 real; receipt
watch/inbox/burn_wave_20260926/B2_86_writer_isolation_20260926.md).

B2-373 (2026-09-26): the writer's stanza shape is pinned HERE, not only by
the census reader. Every injected run asserts _assert_stanza_shape: the
stanza first line matches mag.improve._CRASH_STANZA_RE (imported from the
reader so the two cannot drift) and carries the documented stage= field,
the reader sees exactly the 2 stanza boundaries this flow writes, and its
first boundary lands on the writer's first line (preamble bytes silently
drop out of every census entry). Falsifier that motivated the pin: with the
stanza prefix mutated on real bytes ([<iso>] -> "<ts <iso>>"), this suite
and the census fixture suite stayed 14 green while the census on the
writer's own bytes collapsed a 2-crash log (1 test, 1 real) to entries=1
real=0; probe watch/inbox/burn_wave_20260926/B2_373_falsifier_probe.py,
receipt watch/inbox/burn_wave_20260926/B2_373_stanza_pin_20260926.md.
"""
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mag.agent_cli as ac
from mag.improve import _CRASH_STANZA_RE  # B2-373: reader regex, single source

MARK = "INJECTED-ONESHOT-CRASH"


def _prod_log():
    return ac.ROOT / "logs" / "seat_crashes.log"


def _redirect_crash_log():
    """Point MAG_SEAT_CRASH_LOG at a temp file; return (temp log, old env)."""
    old = os.environ.get("MAG_SEAT_CRASH_LOG")
    tmp_dir = tempfile.mkdtemp(prefix="b2_86_seat_crash_")
    tmp = Path(tmp_dir) / "seat_crashes.log"
    os.environ["MAG_SEAT_CRASH_LOG"] = str(tmp)
    return tmp, old


def _restore_crash_log(old):
    if old is None:
        os.environ.pop("MAG_SEAT_CRASH_LOG", None)
    else:
        os.environ["MAG_SEAT_CRASH_LOG"] = old


def _read(path):
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def _prod_bytes():
    prod = _prod_log()
    return prod.read_bytes() if prod.exists() else b""


def _install_boom():
    real_run_turn = ac.run_turn
    real_save = ac.save_session

    def boom_run_turn(*a, **k):
        raise RuntimeError(f"{MARK}-MIDTURN")

    def boom_save(*a, **k):
        raise RuntimeError(f"{MARK}-PERSIST")

    ac.run_turn = boom_run_turn
    ac.save_session = boom_save
    return real_run_turn, real_save


def _restore(real_run_turn, real_save):
    ac.run_turn = real_run_turn
    ac.save_session = real_save


# B2-373: the one-shot boom flow writes exactly 2 crashes (the do_turn inner
# guard recovers from the run_turn raise, the one_shot outer guard logs the
# save_session raise), so the census reader must see exactly 2 stanzas.
FLOW_STANZA_COUNT = 2


def _assert_stanza_shape(log_text: str, tag: str) -> None:
    """B2-373 first-line shape pin: the writer's stanza line must match the
    census reader's regex (imported from mag.improve so writer and reader
    cannot drift) and keep the documented "[<iso-utc>] stage=<stage>" field;
    the reader must see exactly the stanza boundaries this flow writes, the
    first one at the writer's first line (bytes before the first stanza
    boundary are census preamble and silently drop from every entry)."""
    lines = [ln for ln in log_text.splitlines() if ln.strip()]
    assert lines, f"{tag}: injected crash log empty"
    first = lines[0]
    assert _CRASH_STANZA_RE.match(first), (
        f"{tag}: writer stanza first line {first!r} does not match the census "
        "stanza regex imported from mag.improve (B2-373 writer/reader drift: "
        "the census would silently stop counting the writer's crashes)"
    )
    assert "stage=" in first, (
        f"{tag}: writer stanza first line {first!r} lost the documented "
        "'[<iso-utc>] stage=<stage>' field (B2-373 stanza contract)"
    )
    found = _CRASH_STANZA_RE.findall(log_text)
    assert len(found) == FLOW_STANZA_COUNT, (
        f"{tag}: census regex sees {len(found)} stanza lines in a flow that "
        f"writes exactly {FLOW_STANZA_COUNT} crashes (stage=do_turn + "
        "stage=one_shot); writer/reader drift (B2-373)"
    )
    first_idx = log_text.find(first)
    assert _CRASH_STANZA_RE.search(log_text).start() == first_idx, (
        f"{tag}: the census reader's first stanza boundary lands before the "
        "writer's first line; the bytes in between become census preamble "
        "and silently drop out of every entry (B2-373)"
    )


def test_one_shot_crash_nonzero_exit_and_logged():
    prod_before = _prod_bytes()
    tmp, old_env = _redirect_crash_log()
    real_run_turn, real_save = _install_boom()
    try:
        rc = ac.run_agent(provider="fake", model=None, one_shot="say hi")
    finally:
        _restore(real_run_turn, real_save)
    try:
        new = _read(tmp)
        assert rc == 1, f"expected nonzero exit for one-shot crash, got {rc}"
        assert "stage=do_turn" in new, f"inner guard (do_turn) not logged: {new[-400:]}"
        assert "stage=one_shot" in new, f"outer guard (one_shot) not logged: {new[-400:]}"
        assert MARK in new, f"crash marker missing from log: {new[-400:]}"
        _assert_stanza_shape(new, "one_shot crash flow (B2-373)")
    finally:
        _restore_crash_log(old_env)
    assert _prod_bytes() == prod_before, (
        "production logs/seat_crashes.log changed during the test (B2-86 sink not injected)"
    )
    print("PASS test_one_shot_crash_nonzero_exit_and_logged rc=", rc)


def test_main_argv_propagates_nonzero_exit():
    """CLI entry: sys.exit(main_argv()) -> run_agent's return 1 becomes exit 1."""
    prod_before = _prod_bytes()
    tmp, old_env = _redirect_crash_log()
    real_run_turn, real_save = _install_boom()
    try:
        rc = ac.main_argv(["-q", "say hi", "--provider", "fake"])
    finally:
        _restore(real_run_turn, real_save)
    try:
        new = _read(tmp)
        assert rc == 1, f"main_argv should return 1, got {rc}"
        assert "stage=one_shot" in new, f"one_shot crash not logged in injected sink: {new[-400:]}"
        _assert_stanza_shape(new, "main_argv crash flow (B2-373)")
    finally:
        _restore_crash_log(old_env)
    assert _prod_bytes() == prod_before, (
        "production logs/seat_crashes.log changed during the test (B2-86 sink not injected)"
    )
    print("PASS test_main_argv_propagates_nonzero_exit rc=", rc)


def test_writer_stanza_line_matches_census_reader_regex():
    """B2-373: dedicated first-line shape pin on an injected run.

    The crash census (mag.improve.crash_log_census) splits
    logs/seat_crashes.log on the "[<iso-utc>] stage=<stage>" stanza line, but
    before this pin the writer's shape was asserted by no writer test: a
    _log_seat_crash format change broke the census silently. This pin runs a
    real injected crash flow and holds the writer to the reader's regex
    (mag.improve._CRASH_STANZA_RE, imported so the two cannot drift), the
    stage= field, the exact stanza count of this flow, and the first
    boundary at the writer's first line."""
    prod_before = _prod_bytes()
    tmp, old_env = _redirect_crash_log()
    real_run_turn, real_save = _install_boom()
    try:
        rc = ac.run_agent(provider="fake", model=None, one_shot="say hi")
    finally:
        _restore(real_run_turn, real_save)
    try:
        new = _read(tmp)
        assert rc == 1, f"expected nonzero exit for one-shot crash, got {rc}"
        _assert_stanza_shape(new, "dedicated stanza-shape pin (B2-373)")
    finally:
        _restore_crash_log(old_env)
    assert _prod_bytes() == prod_before, (
        "production logs/seat_crashes.log changed during the test (B2-86 sink not injected)"
    )
    print("PASS test_writer_stanza_line_matches_census_reader_regex rc=", rc)
