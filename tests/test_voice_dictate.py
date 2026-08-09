"""Tests for mag.voice_dictate — per-surface dictation cleanup (VS Code voice steal)."""
from __future__ import annotations

from mag.voice_dictate import SURFACES, cleanup, cleanup_for_terminal, handle_dictate


def test_chat_cleanup_strips_filler_and_prefers_numerals():
    assert cleanup("um what was i doing", "chat") == "What was i doing."
    assert cleanup("show me three files", "chat") == "Show me 3 files."


def test_terminal_dash_becomes_flag():
    # VS Code 1.132 headline: "git commit dash m hello world" -> git commit -m "Hello World"
    assert cleanup("git commit dash m hello world", "terminal") == 'git commit -m "hello world"'
    assert cleanup("git status dash dash short", "terminal") == "git status --short"


def test_terminal_flag_prefix_splitting():
    assert cleanup("run pytest dash dash failed dash first", "command") == "run pytest --failed -first"


def test_symbol_mapping():
    assert cleanup("cd backslash home slash user", "terminal").replace(" ", "") == "cd\\home/user"


def test_cleanup_for_terminal_alias():
    assert cleanup_for_terminal("git commit dash m hello world") == 'git commit -m "hello world"'


def test_handle_dictate_rest_shape():
    out = handle_dictate({"text": "git commit dash m hello world", "surface": "terminal"})
    assert out["ok"] is True
    assert out["cleaned"] == 'git commit -m "hello world"'
    assert out["surface"] == "terminal"


def test_handle_dictate_requires_text():
    out = handle_dictate({})
    assert out["ok"] is False
    assert out["cleaned"] == ""


def test_surfaces_contract():
    assert set(SURFACES) == {"chat", "terminal", "command"}


def test_unknown_surface_falls_back_to_chat():
    assert cleanup("um show me two", "banana") == "Show me 2."
