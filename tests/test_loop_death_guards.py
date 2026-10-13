"""Raise-into-wrapper tests for LOOP-DEATH GUARD prints (a14 species: silent loop death).

SPEC (3 lines, files touched by t19):
1. mag/daemon.py: the silent `except Exception: pass` around write_heartbeat in the
   main daemon cycle becomes a traced HEARTBEAT LOOP DEATH GUARD print (non-fatal).
2. mag/work_loop.py: `_anchor`'s bare swallow of the verkle chain append becomes a
   traced VERKLE-ANCHOR LOOP DEATH GUARD print (non-fatal).
3. mag/afk_loop.py: squeeze_free_test_data's silent ollama producer swallow becomes a
   traced SQUEEZE LOOP DEATH GUARD print (non-fatal).

Raise into each wrapper, assert no exception escapes and the guard print fires.
Also covers the two pre-existing ghost.py wrappers (2026-09-25), which had no test.

SPEC (3 lines, files touched by t43):
1. mag/work_loop.py: the fuel_feed swallow discarded the captured error and fell through
   to a FALSE halt note ("nothing real left to do"); now traced (FUEL LOOP DEATH GUARD)
   and the halt carries fuel_error + a note that admits it is NOT a verified halt.
2. mag/afk_loop.py: squeeze_free_test_data's silent deepseek routing producer swallow
   becomes a traced SQUEEZE LOOP DEATH GUARD print (deepseek routing producer).
3. mag/afk_cadence.py: the operator pause gate FAILED OPEN (an errored pause_reason let
   the loop work through a pause); now fails CLOSED: error = honor the pause, skip the
   tick, name the error. This is a DIFFERENT species (deny-gate) than the death guards,
   so it gets its own test below, not a guard-print case.

SPEC (3 lines, files touched by t52):
1. mag/afk_cadence.py: _operator_afk FAILED OPEN (an errored operator_status read as
   "operator AFK" and the cadence kept spending); now fails CLOSED: error = operator
   presumed ACTIVE, deny honored, cause named in AFK_GATE_ERROR.
2. mag/afk_cadence.py: _right_size FAILED OPEN (an errored rightsizer returned full
   blast budget 4); now fails CLOSED: error = level none / budget 0, error named in
   right_size_error.
3. mag/work_loop.py: _ceiling_gate FAILED OPEN (an errored headroom check returned
   throttled=False "assume safe" and the loop claimed work with the ceiling unknown);
   now fails CLOSED: error = throttled deny honored, error named in ceiling_gate_error.

SPEC (1 line, file touched by t61):
1. mag/afk_loop.py: _operator_afk had the t52 species fail-open (errored operator_status
   read as "operator AFK" so occupy() kept spending) plus the t43 species pause swallow
   (errored pause_reason fell through); now fails CLOSED per the afk_cadence convention:
   error = operator presumed ACTIVE / pause honored, cause named in AFK_GATE_ERROR and
   surfaced as afk_gate_error by occupy().

SPEC (2 lines, files touched by t65):
1. mag/afk_orchestrator.py: _operator_offline had the t52 species fail-open (an errored
   operator_status read as "operator offline" so the AFK cadence kept spending; every
   call site treats offline=True as GO: run_afk runs, _right_size grants full budget),
   now fails CLOSED per the afk_cadence/t61 convention: error = operator presumed ACTIVE
   (return False), cause named in AFK_GATE_ERROR, surfaced as afk_gate_error by run_afk
   and the status output.
2. mag/capability_steal.py: the byte-identical twin gate had the same fail-open (an
   errored operator_status read as "operator offline" so expand() kept steal-searching;
   expand/_right_size treat offline=True as GO), now fails CLOSED identically: error =
   operator presumed ACTIVE (return False), cause named in AFK_GATE_ERROR, surfaced as
   afk_gate_error by expand().

SPEC (3 lines, files touched by t75, the remaining fail-open cluster t65 flagged):
1. mag/afk_orchestrator.py run_afk: the pause gate had the t43 species swallow
   ('except Exception: pass'), so an ERRORED pause_reason let the AFK cadence work
   through an operator pause; now fails CLOSED per the afk_cadence t43 convention:
   error = pause honored (skip), cause named in reason + pause_gate_error.
2. mag/afk_orchestrator.py _right_size: the t52 species rightsizer fail-open
   ('except Exception: return "full"') handed run_afk the FULL blast (budget 4) on an
   errored sizing; now fails CLOSED: error = SMALLEST budget (level "none", run_afk
   skips the pass), cause named in RIGHT_SIZE_ERROR and surfaced as right_size_error
   by run_afk's skip and the status output.
3. mag/capability_steal.py _right_size: the twin rightsizer fail-open
   ('except Exception: return {"level": "full", "budget": 4}') handed expand() the FULL
   blast on an errored sizing; now fails CLOSED identically: error = smallest budget
   (level none / budget 0), cause named in RIGHT_SIZE_ERROR and surfaced as
   right_size_error by expand()'s skip.

SPEC (4 lines, files touched by t78, t75's next_steal: fold telemetry + peak defer):
1. mag/afk_orchestrator.py _fold: the training_events.emit swallow ('except Exception:
   pass') is the t19 species (observability-side; its error direction cannot grant GO):
   a silently dead fold voids the cadence's telemetry while run_afk still reports
   success. Converted to a traced FOLD LOOP DEATH GUARD print (non-fatal, names cause).
2. mag/capability_steal.py _fold: the byte-identical emit swallow; same conversion,
   traced FOLD LOOP DEATH GUARD print.
3. mag/afk_cadence.py _fold: the third twin emit swallow; same conversion.
4. mag/lane_salon.py _witness (part-2 sweep conversion): the paid-lane off-peak defer
   gate FAILED OPEN (the t52 species: 'except Exception: pass' let an errored
   defer_if_peak read fall through to a PAID call at peak pricing); now fails CLOSED
   per the t43/t52/t61/t75 convention: an errored peak check defers the paid witness,
   cause named in error.
Cap note: the t78 sweep found two more same-family sites beyond the LAWS cap of 4
fixes (mag/afk_loop.py _fold emit swallow, mag/capability_steal.py expand() add_move
swallow); both are filed remaining-open with file:line in lanes/t78.check.txt.

SPEC (4 lines, files touched by t84, t78's remaining-open quartet):
1. mag/afk_loop.py _fold: the FOURTH training_events.emit swallow (t19 species,
   byte-identical to the three t78 converted); traced FOLD LOOP DEATH GUARD print
   (non-fatal, names cause).
2. mag/capability_steal.py expand(): the add_move promotion swallow ('except Exception:
   promoted = None') left the row recording promoted=None with no trace of WHY; now a
   traced PROMOTION LOOP DEATH GUARD print (non-fatal, promotion still honestly None,
   cause named).
3. mag/lane_cadence.py cooldown(): a FAILED row with an unparseable ts hit 'except
   Exception: return 0' and read as READY (pacing GO). Call sites confirm the safe
   direction is the cooled/slower path: queue_gate.preflight denies dispatch while
   cd>0 (mag/queue_gate.py:206), fuel_feed._lane_order probes cooled lanes last
   (mag/fuel_feed.py:201), pick_free_glm rides the calmer clerk pool while cd>0.
   FAIL CLOSED: return MAX_RETRY, cause named in COOLDOWN_GATE_ERROR (cleared on a
   clean read, surfaced by status()).
4. mag/lane_cadence.py brake_after(): an unparseable ts row hit 'except Exception:
   continue' and read as NOT a failure, undercounting recent free fails and delaying
   the paid brake (the pacing GO: the free rotation keeps pounding unpaced). No
   production callers today (repo grep: status() + the dist_audit copy); the contract
   is the docstring: the return is the count of free fails still needed before the
   brake may fire. FAIL CLOSED: the unverifiable row counts as a recent failure,
   cause named in BRAKE_GATE_ERROR (cleared on a clean pass, surfaced by status()).

SPEC (1 line, files touched by t85, t84's next_steal):
1. mag/queue_gate.py preflight: the lane-cadence wrapper ('except Exception: pass')
   is the LAST GO path on the queue gate (cooldown() itself is t84 fail-closed;
   provider_spawn_allowed is internally fail-closed via its budget_unreadable deny).
   Safe direction confirmed at the deny semantics: cd>0 denies dispatch (leave
   queued), and the sole production caller mag/swarm_worker.py:400 leaves a not-ok
   gate result queued (visible, not consumed). FAIL CLOSED: an errored cadence read
   denies with reason cadence_gate_error, cause named in CADENCE_GATE_ERROR
   (module-level, cleared on a clean read, surfaced by status()).
"""
from __future__ import annotations

import asyncio
import sys
import types

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))

import mag.afk_loop
import mag.work_loop
from mag.ghost import _bard_loop_wrapper, _cost_enforcer_loop_wrapper

import pytest


def _boom(msg: str = "injected death"):
    raise RuntimeError(msg)


@pytest.mark.parametrize(
    "kind",
    ["ghost_cost", "ghost_bard", "work_anchor", "afk_squeeze", "work_fuel", "afk_routing"],
)
def test_loop_death_guard_fires_on_raise(kind, capsys, monkeypatch):
    """A raise inside the wrapped body must not escape and must leave a guard trace."""
    if kind == "ghost_cost":
        async def _dead_loop(interval_s=15.0):
            _boom()
        monkeypatch.setitem(
            sys.modules, "mag.cost_enforcer",
            types.SimpleNamespace(cost_enforcer_loop=_dead_loop),
        )
        asyncio.run(_cost_enforcer_loop_wrapper())
        needle = "COST-ENFORCER LOOP DEATH GUARD"
    elif kind == "ghost_bard":
        async def _dead_bard(interval=30.0):
            _boom()
        monkeypatch.setitem(
            sys.modules, "mag.bard",
            types.SimpleNamespace(bard_subscriber_loop=_dead_bard),
        )
        asyncio.run(_bard_loop_wrapper())
        needle = "BARD LOOP DEATH GUARD"
    elif kind == "work_anchor":
        monkeypatch.setattr(
            "mag.verkle_knot.append_verkle_knot",
            lambda *_a, **_k: _boom(),
        )
        mag.work_loop._anchor("drilled", {"queued": 0, "running": 0, "cold_pending": 1})
        needle = "VERKLE-ANCHOR LOOP DEATH GUARD"
    elif kind == "work_fuel":
        # force run_once down to the fuel branch: ceiling open, nothing queued/running,
        # nothing cold, discovery empty, then the fake fuel_feed.run raises
        fake_fuel = types.SimpleNamespace(run=lambda batch=1: _boom())
        # B2-288 fix (2026-09-26): sys.modules alone is not enough. work_loop's
        # fuel branch does `from mag import fuel_feed`, which reads the PARENT
        # PACKAGE ATTRIBUTE first. Once any earlier test imports mag.fuel_feed
        # (test_zai_burst does, transitively), that attribute pins the real
        # module and the sys.modules fake is silently bypassed, so this test
        # fired a REAL openrouter lane call instead of the guard. Patch both
        # surfaces so the fake wins regardless of import order.
        monkeypatch.setitem(sys.modules, "mag.fuel_feed", fake_fuel)
        monkeypatch.setattr(mag, "fuel_feed", fake_fuel, raising=False)
        monkeypatch.setattr(mag.work_loop, "_ceiling_gate",
                            lambda: {"ok": True, "throttled": False, "drill_width": 1})
        monkeypatch.setattr(mag.work_loop, "sense",
                            lambda: {"ok": True, "queued": 0, "running": 0, "cold_pending": 0})
        monkeypatch.setattr(mag.work_loop, "_discover",
                            lambda: {"ok": True, "pending": 0, "fired": 0})
        monkeypatch.setattr(mag.work_loop, "_anchor", lambda *a, **k: None)
        out = mag.work_loop.run_once()
        assert out["action"] == "halt", f"expected the halt branch, got: {out!r}"
        assert out.get("fuel_error"), f"halt must carry fuel_error: {out!r}"
        assert "NOT a verified" in out["note"], f"halt note must tell the truth: {out!r}"
        needle = "FUEL LOOP DEATH GUARD"
    elif kind == "afk_routing":
        monkeypatch.setattr(mag.afk_loop, "_ollama_up", lambda: False)
        fake_routing = types.SimpleNamespace(match=lambda *_a, **_k: _boom())
        # B2-288 twin (wave5 suite-burn, 2026-09-29): sys.modules alone is not
        # enough. squeeze_free_test_data's routing branch does `from mag import
        # skill_pipeline` (mag/afk_loop.py:260), which reads the PARENT PACKAGE
        # ATTRIBUTE first. Once any earlier test imports mag.skill_pipeline for
        # real, that attribute pins the real module and the sys.modules fake is
        # silently bypassed (the f-15 full run produced=1; solo runs pass).
        # Patch both surfaces so the fake wins regardless of import order.
        monkeypatch.setitem(sys.modules, "mag.skill_pipeline", fake_routing)
        monkeypatch.setattr(mag, "skill_pipeline", fake_routing, raising=False)
        out = mag.afk_loop.squeeze_free_test_data(budget=4)
        assert out["ok"] is True and out["produced"] == 0
        needle = "deepseek routing producer exited"
    else:
        monkeypatch.setattr(mag.afk_loop, "_ollama_up", lambda: True)
        monkeypatch.setattr(mag.afk_loop, "_ollama_ask", lambda *_a, **_k: _boom())
        out = mag.afk_loop.squeeze_free_test_data(budget=1)
        assert out["ok"] is True and out["produced"] == 0
        needle = "SQUEEZE LOOP DEATH GUARD"

    captured = capsys.readouterr()
    assert needle in captured.out, f"guard print missing for {kind}: {captured.out!r}"
    assert "injected death" in captured.out, f"guard must name WHY it died: {captured.out!r}"


def test_operator_pause_gate_fails_closed(monkeypatch):
    """t43 species (deny-gate, not a death guard): an ERRORED pause check must HONOR
    the pause. The gate fails closed: the tick is skipped and the error is named,
    instead of the old fail-open fall-through that worked through the pause."""
    import mag.afk_cadence

    def _dead_gate():
        _boom()

    monkeypatch.setattr("mag.operator_mode.pause_reason", _dead_gate)
    out = mag.afk_cadence.run_once()
    assert out["action"] == "skip", f"errored gate must skip the tick: {out!r}"
    assert "CLOSED" in out["reason"], f"reason must say it failed closed: {out!r}"
    assert "injected death" in out["reason"], f"reason must name the error: {out!r}"
    assert "pause_gate_error" in out, f"errored gate must record the error: {out!r}"


def test_afk_gate_fails_closed(monkeypatch):
    """t52 species (deny-gate): an ERRORED operator_status must read as operator ACTIVE,
    not AFK. The old fail-open `except: return True` kept the cadence spending while the
    operator was invisible."""
    import mag.afk_cadence
    import mag.preferences

    monkeypatch.setattr(mag.preferences, "operator_status", lambda: _boom())
    assert mag.afk_cadence._operator_afk() is False, "errored gate must deny (operator presumed active)"
    err = mag.afk_cadence.AFK_GATE_ERROR or ""
    assert "CLOSED" in err, f"error must say it failed closed: {err!r}"
    assert "injected death" in err, f"error must name the cause: {err!r}"


def test_right_size_gate_fails_closed(monkeypatch):
    """t52 species (deny-gate): an ERRORED rightsizer must deny work (level none,
    budget 0), not hand the cadence full blast."""
    import mag.afk_cadence
    import mag.afk_loop

    monkeypatch.setattr(mag.afk_loop, "system_resources", lambda: _boom())
    rs = mag.afk_cadence._right_size()
    assert rs.get("level") == "none", f"errored rightsizer must deny work: {rs!r}"
    assert int(rs.get("budget") or 0) == 0, f"errored rightsizer must give zero budget: {rs!r}"
    assert "right_size_error" in rs, f"errored rightsizer must name the error: {rs!r}"
    assert "injected death" in rs["right_size_error"], f"error must name the cause: {rs!r}"
    # and run_once must skip the tick on the denied sizing
    monkeypatch.setattr(mag.afk_cadence, "_right_size", lambda: rs)
    out = mag.afk_cadence.run_once()
    assert out["action"] == "skip", f"denied sizing must skip the tick: {out!r}"


def test_ceiling_gate_fails_closed(monkeypatch):
    """t52 species (deny-gate): an ERRORED ceiling check must refuse work (throttled),
    not claim "assume safe (no throttle)" and let the loop claim work with the ceiling
    unknown."""
    import mag.cadence_learn
    import mag.work_loop

    monkeypatch.setattr(mag.cadence_learn, "headroom", lambda *a, **k: _boom())
    g = mag.work_loop._ceiling_gate()
    assert g.get("throttled") is True, f"errored gate must honor the deny: {g!r}"
    assert "ceiling_gate_error" in g, f"errored gate must name the error: {g!r}"
    assert "injected death" in g["ceiling_gate_error"], f"error must name the cause: {g!r}"
    # and run_once must refuse work on the errored gate
    out = mag.work_loop.run_once()
    assert out.get("throttled") is True, f"run_once must refuse work on an errored gate: {out!r}"
    assert "ceiling_gate_error" in out, f"run_once output must carry the error: {out!r}"


def test_afk_loop_operator_afk_fails_closed(monkeypatch):
    """t61 species (deny-gate): mag/afk_loop._operator_afk had the same fail-open as
    t52's afk_cadence gate (an ERRORED operator_status read as "operator AFK" so the
    legacy occupy() loop kept spending) plus t43's pause swallow (an ERRORED pause_reason
    silently fell through). Both error paths must now deny: operator presumed ACTIVE,
    pause honored, cause named in AFK_GATE_ERROR."""
    import mag.afk_loop
    import mag.preferences

    # path 1: the pause gate errors -> the pause must be honored, not swallowed
    monkeypatch.setattr("mag.operator_mode.pause_reason", lambda: _boom())
    monkeypatch.setattr(mag.preferences, "operator_status",
                        lambda: {"operator_active": False})
    assert mag.afk_loop._operator_afk() is False, "errored pause gate must honor the pause"
    err = mag.afk_loop.AFK_GATE_ERROR or ""
    assert "CLOSED" in err, f"pause error must say it failed closed: {err!r}"
    assert "injected death" in err, f"pause error must name the cause: {err!r}"

    # path 2: the status read errors -> operator presumed ACTIVE, not AFK
    monkeypatch.setattr("mag.operator_mode.pause_reason", lambda: None)
    monkeypatch.setattr(mag.preferences, "operator_status", lambda: _boom())
    assert mag.afk_loop._operator_afk() is False, "errored status read must deny (operator presumed active)"
    err = mag.afk_loop.AFK_GATE_ERROR or ""
    assert "CLOSED" in err, f"status error must say it failed closed: {err!r}"
    assert "injected death" in err, f"status error must name the cause: {err!r}"

    # a clean read clears the named error
    monkeypatch.setattr(mag.preferences, "operator_status",
                        lambda: {"operator_active": False})
    assert mag.afk_loop._operator_afk() is True, "healthy AFK read must still report AFK"
    assert mag.afk_loop.AFK_GATE_ERROR is None, "a clean read must clear AFK_GATE_ERROR"


def test_afk_orchestrator_operator_offline_fails_closed(monkeypatch):
    """t65 species (deny-gate, t52/t61 twin): mag/afk_orchestrator._operator_offline had
    the fail-open 'except: return True' (an ERRORED operator_status read as "operator
    offline" so run_afk kept spending the AFK cadence). Every call site treats
    offline=True as GO, so the fix denies: operator presumed ACTIVE (False), cause named
    in AFK_GATE_ERROR and surfaced by run_afk."""
    import mag.afk_orchestrator
    import mag.preferences

    monkeypatch.setattr(mag.afk_orchestrator, "AFK_GATE_ERROR", None)
    monkeypatch.setattr("mag.operator_mode.pause_reason", lambda: None)
    monkeypatch.setattr(mag.preferences, "operator_status", lambda: _boom())
    assert mag.afk_orchestrator._operator_offline() is False, "errored gate must deny (operator presumed active)"
    err = mag.afk_orchestrator.AFK_GATE_ERROR or ""
    assert "CLOSED" in err, f"error must say it failed closed: {err!r}"
    assert "injected death" in err, f"error must name the cause: {err!r}"
    out = mag.afk_orchestrator.run_afk()
    assert out["action"] == "skip", f"errored gate must skip the cadence: {out!r}"
    assert "afk_gate_error" in out, f"skip must surface the gate error: {out!r}"
    assert "injected death" in out["afk_gate_error"], f"surfaced error must name the cause: {out!r}"
    # a clean read clears the named error and still reports offline honestly
    monkeypatch.setattr(mag.preferences, "operator_status",
                        lambda: {"operator_active": False})
    assert mag.afk_orchestrator._operator_offline() is True, "healthy read must still report offline"
    assert mag.afk_orchestrator.AFK_GATE_ERROR is None, "a clean read must clear AFK_GATE_ERROR"


def test_capability_steal_operator_offline_fails_closed(monkeypatch):
    """t65 species (deny-gate, t52/t61 twin): mag/capability_steal._operator_offline had
    the byte-identical fail-open 'except: return True' (an ERRORED operator_status read
    as "operator offline" so expand() kept steal-searching). Call sites treat
    offline=True as GO, so the fix denies: operator presumed ACTIVE (False), cause named
    in AFK_GATE_ERROR and surfaced by expand()."""
    import mag.capability_steal
    import mag.preferences

    monkeypatch.setattr(mag.capability_steal, "AFK_GATE_ERROR", None)
    monkeypatch.setattr(mag.preferences, "operator_status", lambda: _boom())
    assert mag.capability_steal._operator_offline() is False, "errored gate must deny (operator presumed active)"
    err = mag.capability_steal.AFK_GATE_ERROR or ""
    assert "CLOSED" in err, f"error must say it failed closed: {err!r}"
    assert "injected death" in err, f"error must name the cause: {err!r}"
    out = mag.capability_steal.expand()
    assert out["action"] == "skip", f"errored gate must skip the expand pass: {out!r}"
    assert "afk_gate_error" in out, f"skip must surface the gate error: {out!r}"
    assert "injected death" in out["afk_gate_error"], f"surfaced error must name the cause: {out!r}"
    # a clean read clears the named error and still reports offline honestly
    monkeypatch.setattr(mag.preferences, "operator_status",
                        lambda: {"operator_active": False})
    assert mag.capability_steal._operator_offline() is True, "healthy read must still report offline"
    assert mag.capability_steal.AFK_GATE_ERROR is None, "a clean read must clear AFK_GATE_ERROR"


def test_afk_orchestrator_pause_gate_fails_closed(monkeypatch):
    """t75 species (t43 twin in run_afk): mag/afk_orchestrator.run_afk swallowed the
    pause gate's exceptions ('except Exception: pass'), so an ERRORED pause_reason let
    the AFK cadence work through an operator pause. Fix honors the pause: skip with the
    cause named in reason + pause_gate_error."""
    import mag.afk_orchestrator

    monkeypatch.setattr("mag.operator_mode.pause_reason", lambda: _boom())
    out = mag.afk_orchestrator.run_afk()
    assert out["action"] == "skip", f"errored pause gate must skip the cadence: {out!r}"
    assert "CLOSED" in out["reason"], f"reason must say it failed closed: {out!r}"
    assert "injected death" in out["reason"], f"reason must name the error: {out!r}"
    assert "pause_gate_error" in out, f"errored gate must record the error: {out!r}"
    assert "injected death" in out["pause_gate_error"], f"error field must name the cause: {out!r}"


def test_afk_orchestrator_right_size_fails_closed(monkeypatch):
    """t75 species (t52 twin): mag/afk_orchestrator._right_size returned "full" on any
    exception, handing run_afk the FULL blast (budget 4) on a broken rightsizer. Fix:
    the SMALLEST budget (level "none"), cause named in RIGHT_SIZE_ERROR and surfaced as
    right_size_error by run_afk's skip."""
    import mag.afk_loop
    import mag.afk_orchestrator

    monkeypatch.setattr(mag.afk_orchestrator, "RIGHT_SIZE_ERROR", None)
    monkeypatch.setattr("mag.operator_mode.pause_reason", lambda: None)
    monkeypatch.setattr(mag.afk_loop, "system_resources", lambda: _boom())
    assert mag.afk_orchestrator._right_size() == "none", "errored rightsizer must deny (smallest budget)"
    err = mag.afk_orchestrator.RIGHT_SIZE_ERROR or ""
    assert "CLOSED" in err, f"error must say it failed closed: {err!r}"
    assert "injected death" in err, f"error must name the cause: {err!r}"
    out = mag.afk_orchestrator.run_afk(force=True)
    assert out["action"] == "skip", f"denied sizing must skip the cadence: {out!r}"
    assert "right_size_error" in out, f"skip must surface the rightsizer error: {out!r}"
    assert "injected death" in out["right_size_error"], f"surfaced error must name the cause: {out!r}"
    # a clean read clears the named error and still sizes honestly
    monkeypatch.setattr(mag.afk_loop, "system_resources", lambda: {"cpu": 1})
    monkeypatch.setattr(mag.afk_loop, "right_size", lambda *a, **k: {"level": "light"})
    assert mag.afk_orchestrator._right_size() == "light", "healthy rightsizer must still size"
    assert mag.afk_orchestrator.RIGHT_SIZE_ERROR is None, "a clean read must clear RIGHT_SIZE_ERROR"


def test_capability_steal_right_size_fails_closed(monkeypatch):
    """t75 species (t52 twin): mag/capability_steal._right_size returned
    {"level": "full", "budget": 4} on any exception, handing expand() the FULL blast on
    a broken rightsizer. Fix: the SMALLEST budget (level none / budget 0), cause named
    in RIGHT_SIZE_ERROR and surfaced as right_size_error by expand()'s skip."""
    import mag.afk_loop
    import mag.capability_steal
    import mag.preferences

    monkeypatch.setattr(mag.capability_steal, "RIGHT_SIZE_ERROR", None)
    monkeypatch.setattr(mag.preferences, "operator_status",
                        lambda: {"operator_active": False})
    monkeypatch.setattr(mag.afk_loop, "system_resources", lambda: _boom())
    rs = mag.capability_steal._right_size()
    assert rs.get("level") == "none", f"errored rightsizer must deny work: {rs!r}"
    assert int(rs.get("budget") or 0) == 0, f"errored rightsizer must give zero budget: {rs!r}"
    assert "right_size_error" in rs, f"errored rightsizer must name the error: {rs!r}"
    assert "injected death" in rs["right_size_error"], f"error must name the cause: {rs!r}"
    out = mag.capability_steal.expand()
    assert out["action"] == "skip", f"denied sizing must skip the expand pass: {out!r}"
    assert "right_size_error" in out, f"skip must surface the rightsizer error: {out!r}"
    assert "injected death" in out["right_size_error"], f"surfaced error must name the cause: {out!r}"
    # a clean read clears the named error and still sizes honestly
    monkeypatch.setattr(mag.afk_loop, "system_resources", lambda: {"cpu": 1})
    monkeypatch.setattr(mag.afk_loop, "right_size", lambda *a, **k: {"level": "light", "budget": 1})
    rs2 = mag.capability_steal._right_size()
    assert rs2.get("level") == "light", "healthy rightsizer must still size"
    assert mag.capability_steal.RIGHT_SIZE_ERROR is None, "a clean read must clear RIGHT_SIZE_ERROR"


def test_afk_orchestrator_fold_guard_prints(capsys, monkeypatch):
    """t78 species (death-guard print, not a deny-gate): mag/afk_orchestrator._fold
    swallowed a dead training_events.emit with 'except Exception: pass', voiding the
    cadence's telemetry while run_afk still reported success. The swallow must now be a
    traced FOLD LOOP DEATH GUARD print that names WHY it died, without breaking the pass."""
    import mag.afk_orchestrator
    import mag.training_events

    monkeypatch.setattr(mag.training_events, "emit", lambda *a, **k: _boom())
    mag.afk_orchestrator._fold("full", 3)  # must not raise
    captured = capsys.readouterr()
    assert "FOLD LOOP DEATH GUARD" in captured.out, f"guard print missing: {captured.out!r}"
    assert "injected death" in captured.out, f"guard must name WHY it died: {captured.out!r}"


def test_capability_steal_fold_guard_prints(capsys, monkeypatch):
    """t78 species (t19 twin): mag/capability_steal._fold swallowed a dead
    training_events.emit the same way while expand() still reported n_expanded. Same
    traced FOLD LOOP DEATH GUARD conversion."""
    import mag.capability_steal
    import mag.training_events

    monkeypatch.setattr(mag.training_events, "emit", lambda *a, **k: _boom())
    mag.capability_steal._fold(2)  # must not raise
    captured = capsys.readouterr()
    assert "FOLD LOOP DEATH GUARD" in captured.out, f"guard print missing: {captured.out!r}"
    assert "injected death" in captured.out, f"guard must name WHY it died: {captured.out!r}"


def test_afk_cadence_fold_guard_prints(capsys, monkeypatch):
    """t78 species (t19 twin #3): mag/afk_cadence._fold swallowed a dead
    training_events.emit the same way while run_once still reported ok_steps. Same
    traced FOLD LOOP DEATH GUARD conversion."""
    import mag.afk_cadence
    import mag.training_events

    monkeypatch.setattr(mag.training_events, "emit", lambda *a, **k: _boom())
    mag.afk_cadence._fold({"ok_steps": 2, "total_steps": 3, "right_size": {"level": "none"}})
    captured = capsys.readouterr()
    assert "FOLD LOOP DEATH GUARD" in captured.out, f"guard print missing: {captured.out!r}"
    assert "injected death" in captured.out, f"guard must name WHY it died: {captured.out!r}"


def test_lane_salon_defer_gate_fails_closed(monkeypatch):
    """t78 species (deny-gate, the part-2 sweep conversion): mag/lane_salon._witness's
    paid-lane off-peak defer gate FAILED OPEN ('except Exception: pass' around
    defer_if_peak), so an ERRORED peak check sent a PAID call out at peak pricing. Fix:
    fail CLOSED per the t43/t52/t61/t75 convention: the paid witness is deferred, the
    provider is never reached, the cause is named in error."""
    import mag.lane_salon
    import mag.offpeak

    monkeypatch.setattr(mag.offpeak, "defer_if_peak", lambda *a, **k: _boom())
    w = mag.lane_salon._witness("t78-test", "deepseek", None, True, "does the gate hold?")
    assert w["ok"] is False, f"errored defer gate must defer the paid witness: {w!r}"
    assert w["answer"] == "", f"no answer may be produced on an errored defer gate: {w!r}"
    assert "CLOSED" in w["error"], f"error must say it failed closed: {w!r}"
    assert "injected death" in w["error"], f"error must name the cause: {w!r}"
    assert "unreachable" not in w["error"], "gate error must fail at the gate, never reach the provider"


def test_afk_loop_fold_guard_prints(capsys, monkeypatch):
    """t84 species (t19 twin #4, t78's filed remaining-open): mag/afk_loop._fold swallowed
    a dead training_events.emit with 'except Exception: pass' while occupy() still
    reported success. Same traced FOLD LOOP DEATH GUARD conversion as t78's three."""
    import mag.training_events

    monkeypatch.setattr(mag.training_events, "emit", lambda *a, **k: _boom())
    mag.afk_loop._fold({"action": "tesuji", "socratic": {}, "tool_test": {}, "freebies": {}})  # must not raise
    captured = capsys.readouterr()
    assert "FOLD LOOP DEATH GUARD" in captured.out, f"guard print missing: {captured.out!r}"
    assert "injected death" in captured.out, f"guard must name WHY it died: {captured.out!r}"


def test_capability_steal_promotion_guard_prints(capsys, monkeypatch):
    """t84 species (t78's filed remaining-open): mag/capability_steal.expand() swallowed a
    dead pro_library.add_move with 'except Exception: promoted = None', leaving the row
    to record promoted=None with no trace of WHY. Promotion stays honestly None and the
    pass non-fatal; the cause is now a traced PROMOTION LOOP DEATH GUARD print."""
    import mag.capability_steal

    monkeypatch.setattr(mag.capability_steal, "_operator_offline", lambda: True)
    monkeypatch.setattr(mag.capability_steal, "_right_size",
                        lambda: {"level": "light", "budget": 1})
    monkeypatch.setattr(mag.capability_steal, "_default_steal_sources", lambda: ["t84-src"])
    monkeypatch.setattr(mag.capability_steal, "steal_search",
                        lambda *a, **k: {"source": "t84-src",
                                         "invariants": [{"family": "t84_family"}]})
    monkeypatch.setattr(mag.capability_steal, "test_local",
                        lambda inv: {"applies": True, "local_test": "ok"})
    monkeypatch.setattr(mag.capability_steal, "_append", lambda row: None)
    monkeypatch.setattr(mag.capability_steal, "_fold", lambda n: None)
    monkeypatch.setattr("mag.pro_library.add_move", lambda *a, **k: _boom())
    out = mag.capability_steal.expand()  # must not raise
    assert out["n_expanded"] == 1, f"the steal pass must still complete: {out!r}"
    assert out["expanded"][0]["promoted"] is None, f"promotion must stay honestly None: {out!r}"
    captured = capsys.readouterr()
    assert "PROMOTION LOOP DEATH GUARD" in captured.out, f"guard print missing: {captured.out!r}"
    assert "injected death" in captured.out, f"guard must name WHY it died: {captured.out!r}"


def test_lane_cadence_cooldown_fails_closed(monkeypatch):
    """t84 species (pacing deny-gate, t52 convention): mag/lane_cadence.cooldown read a
    FAILED row with an unparseable ts as READY (the old 'except Exception: return 0'),
    a pacing GO. Call sites confirm the safe direction is the cooled/slower path:
    queue_gate.preflight denies dispatch while cd>0, fuel_feed._lane_order probes cooled
    lanes last, pick_free_glm rides the calmer clerk pool. FAIL CLOSED: a full-cap
    breather, cause named in COOLDOWN_GATE_ERROR, cleared on a clean read."""
    from datetime import datetime, timezone

    from mag import lane_cadence as lc

    monkeypatch.setattr(lc, "_ledger_rows",
                        lambda: [{"ts": "not-a-timestamp", "lane": "z_ai3", "ok": False,
                                  "error": "HTTP 1305"}])
    cd = lc.cooldown("z_ai3")
    assert cd == lc.MAX_RETRY, f"unverifiable lane state must honor the slower path: {cd!r}"
    err = lc.COOLDOWN_GATE_ERROR or ""
    assert "FAIL-CLOSED" in err, f"error must say it failed closed: {err!r}"
    assert "ts parse exited" in err, f"error must name the failing parse: {err!r}"
    # a clean read clears the named error and still reads honestly
    fresh = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    monkeypatch.setattr(lc, "_ledger_rows",
                        lambda: [{"ts": fresh, "lane": "z_ai3", "ok": True, "error": ""}])
    assert lc.cooldown("z_ai3") == 0, "a fresh success must still read as ready"
    assert lc.COOLDOWN_GATE_ERROR is None, "a clean read must clear COOLDOWN_GATE_ERROR"


def test_lane_cadence_brake_fails_closed(monkeypatch):
    """t84 species (pacing deny-gate, t52 convention): mag/lane_cadence.brake_after let an
    unparseable ts row read as NOT a failure (the old 'except Exception: continue'),
    undercounting recent free fails and delaying the paid brake. FAIL CLOSED: the
    unverifiable row counts as a recent failure, cause named in BRAKE_GATE_ERROR,
    cleared on a clean pass."""
    from datetime import datetime, timezone

    from mag import lane_cadence as lc

    bad = [{"ts": "garbage", "lane": "z_ai3", "ok": False, "error": "boom"}] * 3
    monkeypatch.setattr(lc, "_ledger_rows", lambda: bad)
    assert lc.brake_after() == 0, (
        "unverifiable rows must count toward the brake, not read as healthy "
        f"({lc.BRAKE_GATE_ERROR!r})")
    err = lc.BRAKE_GATE_ERROR or ""
    assert "FAIL-CLOSED" in err, f"error must say it failed closed: {err!r}"
    assert "ts parse exited" in err, f"error must name the failing parse: {err!r}"
    # a clean pass clears the named error and still counts honestly
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    monkeypatch.setattr(lc, "_ledger_rows",
                        lambda: [{"ts": now, "lane": "z_ai3", "ok": False, "error": "boom"}] * 3)
    assert lc.brake_after() == 0, "three recent real failures must still allow the brake"
    assert lc.BRAKE_GATE_ERROR is None, "a clean pass must clear BRAKE_GATE_ERROR"


def test_queue_gate_cadence_wrapper_fails_closed(monkeypatch):
    """t85 species (queue gate, t84/t52 convention): mag/queue_gate.preflight wrapped the
    lane-cadence check in 'except Exception: pass', so an errored cadence read left the
    task free to dispatch (the LAST GO path on the gate; t84 already fail-closed
    cooldown()'s internal ts-parse path, and provider_spawn_allowed denies internally on
    budget_unreadable). Safe direction confirmed: this gate's own deny semantics leave a
    cooled lane queued, and the sole production caller mag/swarm_worker.py:400 leaves a
    not-ok gate result queued (visible, not consumed). FAIL CLOSED: an errored cadence
    read denies with reason cadence_gate_error, cause named in CADENCE_GATE_ERROR,
    cleared on a clean read, surfaced by status()."""
    from mag import queue_gate as qg

    def _dead_cadence(lane):
        raise RuntimeError("injected cadence death")

    # hermetic gate: budget wall passes, lane resolves, cadence read raises
    monkeypatch.setattr("mag.swarm_worker.provider_spawn_allowed",
                        lambda p: {"ok": True, "provider": p, "reason": "budget_ok"})
    monkeypatch.setattr(qg, "_lane_for", lambda p: "t85lane")
    monkeypatch.setattr("mag.lane_cadence.cooldown", _dead_cadence)
    pf = qg.preflight({"task_id": "t85-x", "goal": "t85 fail-closed probe",
                       "provider": "t85lane"})
    assert pf["ok"] is False, f"an errored cadence read must deny dispatch: {pf!r}"
    assert pf["reason"] == "cadence_gate_error", f"deny must name the gate: {pf!r}"
    assert "t85lane" in str(pf.get("lane")), f"deny must carry the lane: {pf!r}"
    err = qg.CADENCE_GATE_ERROR or ""
    assert "FAIL-CLOSED" in err, f"error must say it failed closed: {err!r}"
    assert "injected cadence death" in err, f"error must name WHY it failed: {err!r}"
    # a clean read clears the named error and still gates honestly (normal deny, no error)
    monkeypatch.setattr("mag.lane_cadence.cooldown", lambda lane: 7)
    pf2 = qg.preflight({"task_id": "t85-x", "goal": "t85 fail-closed probe",
                        "provider": "t85lane"})
    assert pf2["ok"] is False and pf2["reason"] == "lane_cooling", (
        f"a cooled lane must still deny (normal gate, not an error): {pf2!r}")
    assert qg.CADENCE_GATE_ERROR is None, "a clean read must clear CADENCE_GATE_ERROR"
