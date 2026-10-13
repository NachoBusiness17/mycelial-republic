"""B2-358 pins: the env-redirect tripwire surfaces name the leaked target.

Falsifier under repair: MAG_SEAT_CRASH_LOG set in a plain shell, one real seat
crash, and no surface naming where the trace went. After B2-358 both surfaces
(mag.doctor.check_env_sanity and python -m mag.shared_surface validate) warn
with the redirect target whenever MAG_SEAT_CRASH_LOG or MAG_GAPS_LOG is set.
The warning fires unconditionally on a set variable: the surfaces are operator
commands, so a variable set at invocation time is a leak to name even inside a
test runner process (the PYTEST_CURRENT_TEST marker flips per phase and cannot
serve as a suppression key; pinned by test_warning_fires_even_inside_test_runner).
"""

from __future__ import annotations

import pytest

from mag.env_redirect import (
    OPERATOR_RESPONSE,
    env_redirect_status,
    env_redirect_warnings,
)


@pytest.fixture()
def plain_shell(monkeypatch):
    """Clear the isolation variables so ambient state cannot leak into pins."""
    for var in ("MAG_SEAT_CRASH_LOG", "MAG_GAPS_LOG"):
        monkeypatch.delenv(var, raising=False)
    return monkeypatch


def test_warning_names_var_and_target_when_set(plain_shell, tmp_path):
    target = tmp_path / "stray_crash.log"
    plain_shell.setenv("MAG_SEAT_CRASH_LOG", str(target))
    lines = env_redirect_warnings()
    assert len(lines) == 1
    assert "MAG_SEAT_CRASH_LOG" in lines[0]
    assert str(target) in lines[0]
    assert "Operator response" in lines[0]
    assert OPERATOR_RESPONSE in lines[0]


def test_gaps_log_var_named_with_displaced_production_default(plain_shell, tmp_path):
    target = tmp_path / "stray_gaps.jsonl"
    plain_shell.setenv("MAG_GAPS_LOG", str(target))
    lines = env_redirect_warnings()
    assert len(lines) == 1
    assert "MAG_GAPS_LOG" in lines[0]
    assert str(target) in lines[0]
    # the warning must name the production log the var displaced
    assert "loop_gaps.jsonl" in lines[0]


def test_warning_fires_even_inside_test_runner(plain_shell, tmp_path, monkeypatch):
    # The suppression trap that shaped the design: PYTEST_CURRENT_TEST is
    # re-set by pytest at every phase transition, so it can never be the key
    # that silences the tripwire. The warning fires regardless, and the
    # status record flags the context for the operator instead.
    plain_shell.setenv("MAG_SEAT_CRASH_LOG", str(tmp_path / "x.log"))
    monkeypatch.setenv("PYTEST_CURRENT_TEST", "tests/test_x.py::test_y (call)")
    assert len(env_redirect_warnings()) == 1
    status = env_redirect_status()
    assert status[0]["in_test_run"] is True


def test_in_test_run_flag_false_without_marker(plain_shell, tmp_path, monkeypatch):
    # body-level delenv: the marker is re-set at each pytest phase, so only a
    # call-phase delete models the plain shell
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
    plain_shell.setenv("MAG_GAPS_LOG", str(tmp_path / "g.jsonl"))
    status = env_redirect_status()
    assert status[0]["in_test_run"] is False


def test_no_vars_no_warnings(plain_shell):
    assert env_redirect_warnings() == []
    assert env_redirect_status() == []


def test_both_vars_two_records_with_target_exists(plain_shell, tmp_path):
    crash = tmp_path / "crash.log"
    crash.write_text("seed", encoding="utf-8")
    plain_shell.setenv("MAG_SEAT_CRASH_LOG", str(crash))
    plain_shell.setenv("MAG_GAPS_LOG", str(tmp_path / "missing.jsonl"))
    status = env_redirect_status()
    by_var = {rec["var"]: rec for rec in status}
    assert by_var["MAG_SEAT_CRASH_LOG"]["target_exists"] is True
    assert by_var["MAG_GAPS_LOG"]["target_exists"] is False
    assert "seat_crashes.log" in by_var["MAG_SEAT_CRASH_LOG"]["moves"]


def test_doctor_env_sanity_carries_redirect_warning(plain_shell, tmp_path):
    from mag.doctor import check_env_sanity

    target = tmp_path / "stray_crash.log"
    plain_shell.setenv("MAG_SEAT_CRASH_LOG", str(target))
    result = check_env_sanity()
    # warning, not a hard env failure: ok stays driven by missing required vars
    assert any(
        "MAG_SEAT_CRASH_LOG" in w and str(target) in w
        for w in result["redirect_warnings"]
    )


def test_doctor_examine_aggregates_redirect_warnings(plain_shell, tmp_path, monkeypatch):
    import mag.doctor as doctor_mod

    target = tmp_path / "stray_crash.log"
    plain_shell.setenv("MAG_SEAT_CRASH_LOG", str(target))
    green = {"check": "stub", "ok": True, "issues": [], "missing_optional": []}
    for name in (
        "check_provider_sanity",
        "check_provider_endpoints",
        "check_model_sanity",
        "check_inbox_sanity",
        "check_chain_discipline",
        "check_memlance_discipline",
        "check_scheduled_tasks",
        "check_self_steal",
        "check_system_tracking",
    ):
        monkeypatch.setattr(doctor_mod, name, lambda: dict(green))
    report = doctor_mod.examine()
    assert report.ok is True
    assert any("ENV-REDIRECT" in w and "MAG_SEAT_CRASH_LOG" in w for w in report.warnings)


def test_shared_surface_validate_warns(plain_shell, tmp_path):
    from mag.shared_surface import inspect_surface

    target = tmp_path / "stray_crash.log"
    plain_shell.setenv("MAG_SEAT_CRASH_LOG", str(target))
    result = inspect_surface()
    assert any(
        "ENV-REDIRECT" in w and "MAG_SEAT_CRASH_LOG" in w and str(target) in w
        for w in result["warnings"]
    )


def test_shared_surface_validate_clean_when_unset(plain_shell):
    from mag.shared_surface import inspect_surface

    result = inspect_surface()
    assert not any("ENV-REDIRECT" in w for w in result["warnings"])
