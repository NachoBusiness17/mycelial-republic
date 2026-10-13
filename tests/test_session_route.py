"""Session routing preamble tests — the data-backed invariant injected into every session."""
from __future__ import annotations

import os

import pytest

from mag.session_route import (
    default_agent_state,
    formatting_block,
    learned_block,
    preamble,
    read_seed,
    render,
)


def test_default_agent_state_is_coding_agent():
    old = os.environ.pop("MAG_AGENT_STATE", None)
    try:
        assert default_agent_state() == "coding-agent"
    finally:
        if old is not None:
            os.environ["MAG_AGENT_STATE"] = old


def test_default_agent_state_env_override(monkeypatch):
    monkeypatch.setenv("MAG_AGENT_STATE", "janitor-agent")
    assert default_agent_state() == "janitor-agent"


def test_read_seed_present():
    # SESSION_SEED.md ships in the repo → should exist and be non-empty.
    seed = read_seed()
    assert isinstance(seed, str)
    assert len(seed) > 0


def test_formatting_block_has_spec():
    block = formatting_block("coding-agent")
    assert "coding-agent" in block
    assert "model=" in block or "model" in block.lower()


def test_preamble_shape_with_model_hint():
    pre = preamble("fix the done-filter in governor_autorun", with_model=True)
    assert pre["agent_state"] == "coding-agent"
    assert pre["model_hint"] in ("deepseek-v4-flash", "deepseek-v4-pro")
    assert pre["model_shape"] in ("cheap", "balanced", "heavy", "reasoning")
    # the three invariant layers
    assert pre["seed"]
    assert pre["formatting"]
    # learned may be empty on a fresh ledger, but must be a str
    assert isinstance(pre["learned"], str)


def test_render_includes_seed_and_formatting():
    pre = preamble("some goal", with_model=False)
    text = render(pre)
    assert "Session seed" in text
    assert "Agent state" in text


def test_render_skips_empty_sections():
    text = render({"formatting": "", "seed": "", "learned": ""})
    assert text == ""


def test_system_prompt_injects_invariant():
    """Every surface's system prompt carries the seed + agent-state block by default."""
    from mag.agent_cli import _system_prompt

    sp = _system_prompt("PACK", goal="")
    assert "Session seed" in sp
    assert "Agent state" in sp
    assert "Context pack" in sp
