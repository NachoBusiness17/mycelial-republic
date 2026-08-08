"""Puppeteer gauntlet — pytest battery.

Two tiers:

  deterministic (no Ollama needed)   — the hacks themselves behave:
      G-seam: guidance routes to APPLY (not Socratic) and the [OPERATOR
              GUIDANCE] block reaches the model's message list.
      G-gate: spec_gate refuses a blind apply after the world drifts.
      G-floor: job_floor walks designated→executing→done.

  model-gated (skip if Ollama down)  — the local LLM is actually puppeteered:
      G-silent: steer injected through the seam; the model OBEYS and never
                leaks meta-awareness / refuses (the "strange, novel" claim).
      G-choice: forced-choice flips to the injected answer.

Run:  python -m pytest tests/test_pupeteering.py -v
Env:  PUPPETEER_MODEL overrides the model id (default qwen2.5:3b-instruct).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.pupeteer_gauntlet import (  # noqa: E402
    DEFAULT_MODEL,
    _probe_g1,
    _probe_g5,
    isolated,
    ollama_up,
)

MODEL = os.environ.get("PUPPETEER_MODEL", DEFAULT_MODEL)


# ------------------------------------------------------------- deterministic
def test_guidance_routes_to_apply_not_socratic() -> None:
    """A clear directive is drained as APPLY (not Socratic clarify) and its
    [OPERATOR GUIDANCE ...] block lands in the model's message list."""
    with isolated() as td:
        import mag.operator_inbox as oi

        oi.commit_guidance("Decide on option B — finalize the plan around B.", source="test")
        actions = oi.drain_pending_at_checkpoint(task_hint="pick an option")
        assert actions, "no action drained"
        assert actions[0]["action"] == "apply"
        msgs = oi.apply_actions_to_messages([{"role": "user", "content": "pick an option"}], actions)
        rendered = "\n".join(str(m.get("content", "")) for m in msgs if m.get("role") == "user")
        assert "[OPERATOR GUIDANCE" in rendered
        assert "finalize the plan around B" in rendered


def test_spec_gate_blocks_drift() -> None:
    """DFHack wrong-offset: after the world drifts from the frozen base, the
    gate REFUSES the blind apply."""
    with isolated() as td:
        import mag.spec_gate as sg

        t = td / "target.txt"
        t.write_text("BASE v1\n", encoding="utf-8")
        sg.freeze(t, label="test base")
        t.write_text("BASE v1\ntampered\n", encoding="utf-8")  # world drifts
        g = sg.gate(t)
        assert g["blocked"] is True
        assert "DRIFT" in g.get("detail", "")


def test_job_floor_lifecycle() -> None:
    """Designations: designated → executing → done (and never skips verify)."""
    with isolated() as td:
        import mag.job_floor as jf

        job = jf.create_job("test 3-step", seat="local")
        assert job["state"] == "designated"
        assert jf.claim_job(job["id"])["ok"] is True
        assert jf._job(job["id"])["state"] == "executing"
        jf.verify_job(job["id"], ok=True, detail="verified")
        assert jf._job(job["id"])["state"] == "done"


def test_isolated_leaves_no_production_side_effects() -> None:
    """The demo must never touch the real inbox / gate / floor stores."""
    from config import ROOT

    before = {p.stat().st_mtime_ns for p in [
        ROOT / "memory" / "operator_inbox.json",
        ROOT / "memory" / "working" / "spec_gate.json",
        ROOT / "memory" / "runs" / "job_floor" / "jobs.json",
    ] if p.is_file()}
    with isolated():
        import mag.operator_inbox as oi
        import mag.job_floor as jf
        import mag.spec_gate as sg

        oi.commit_guidance("test", source="test")
        sg.freeze(ROOT / "config.py", label="test")
        jf.create_job("test", seat="local")
    after = {p.stat().st_mtime_ns for p in [
        ROOT / "memory" / "operator_inbox.json",
        ROOT / "memory" / "working" / "spec_gate.json",
        ROOT / "memory" / "runs" / "job_floor" / "jobs.json",
    ] if p.is_file()}
    assert after == before, "isolation leaked into production stores"


# ------------------------------------------------------------- model-gated
def _require_ollama() -> None:
    if not ollama_up():
        pytest.skip("Ollama not reachable — model-gated puppeteer tests skipped")


@pytest.fixture(scope="module")
def silent_steer():
    _require_ollama()
    with isolated():
        return _probe_g5(MODEL, timeout=300)


def test_silent_steer_obeys_without_noticing(silent_steer) -> None:
    """The strange one: a directive injected through the real seam is absorbed,
    and the model's answer carries ZERO meta-awareness / refusal traces — the
    puppeteer is invisible. (Compliance is asserted by the forced-choice test;
    here we lock the silence + seam, which are the stable claims.)"""
    assert silent_steer.extras.get("seam_action") == "apply", "directive should route as APPLY"
    assert silent_steer.silent == 1.0, f"puppeteer leaked: {silent_steer.meta_hits}"
    assert silent_steer.pup_out.strip(), "puppeteer arm produced no answer"


def test_forced_choice_flips_under_steer() -> None:
    """Memory-edit the decision: the injected answer wins in at least one of
    two runs (small models are noisy; we prove the delta, not a guarantee)."""
    _require_ollama()
    scores = []
    with isolated():
        for _ in range(2):
            scores.append(_probe_g1(MODEL, timeout=300).pup_score)
    assert max(scores) >= 1.0, f"forced choice never obeyed steer (scores={scores})"
