"""Fan-out write-strip compiler tests (no remote calls, no file writes).

Covers the MICKEY-17 owed chore "strip write tools at fan-out" (lanes
write-delegation#0 + orchestrator-war-stories#0): schema-level omission at
fan-out, the agent_cli activation/backstop, and the orchestrator's
read-only-by-default spawn contract.
"""
from __future__ import annotations

import inspect
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag import write_strip  # noqa: E402
from mag.write_strip import (  # noqa: E402
    READ_ONLY_ARG,
    classify_tool,
    is_write_tool,
    read_only_from_env,
    strip_write_tools,
)


# --- classification ----------------------------------------------------------

def test_estate_names_classified():
    assert classify_tool("write_file") == "write"
    assert classify_tool("Write") == "write"          # harness name
    assert classify_tool("Edit") == "write"
    assert classify_tool("MultiEdit") == "write"
    assert classify_tool("NotebookEdit") == "write"
    assert classify_tool("apply_patch") == "write"
    assert classify_tool("pheromone_drop") == "write"  # shared-state writer
    assert classify_tool("blackboard_post") == "write"
    assert classify_tool("run_shell") == "dual_use"
    assert classify_tool("Bash") == "dual_use"
    assert classify_tool("run_python") == "dual_use"
    assert classify_tool("read_file") == "read"
    assert classify_tool("list_dir") == "read"
    assert classify_tool("search_files") == "read"
    assert classify_tool("blackboard_read") == "read"
    assert is_write_tool("write_file") and not is_write_tool("read_file")


# --- the real estate grant ----------------------------------------------------

def test_estate_schema_strips_write_file_keeps_reads():
    from mag.agent_cli import TOOL_SCHEMAS

    names = [write_strip._tool_name(t) for t in TOOL_SCHEMAS]
    assert "write_file" in names, "precondition: estate grant carries write_file"
    result = strip_write_tools(TOOL_SCHEMAS)
    kept_names = [write_strip._tool_name(t) for t in result["tools"]]
    assert "write_file" not in kept_names
    for read_tool in ("list_dir", "read_file", "search_files"):
        assert read_tool in kept_names, f"read tool {read_tool} must survive"
    assert "write_file" in result["receipt"]["stripped_names"]
    assert "pheromone_drop" in result["receipt"]["stripped_names"]
    # dual-use survives default mode (lanes need the fetch/compute path)
    assert "run_shell" in kept_names and "run_python" in kept_names
    assert result["receipt"]["total"] == len(names)


def test_estate_grant_not_mutated():
    from mag.agent_cli import TOOL_SCHEMAS

    before = [write_strip._tool_name(t) for t in TOOL_SCHEMAS]
    snapshot = [dict(t) for t in TOOL_SCHEMAS]
    strip_write_tools(TOOL_SCHEMAS, strict=True)
    after = [write_strip._tool_name(t) for t in TOOL_SCHEMAS]
    assert before == after
    assert snapshot == TOOL_SCHEMAS


# --- harness-style schema fixture --------------------------------------------

def _zcode_style_fixture():
    """OpenAI-function format, the shape a harness agent() spawn carries."""
    def fn(name, desc):
        return {
            "type": "function",
            "function": {"name": name, "description": desc, "parameters": {"type": "object"}},
        }

    return [
        fn("Read", "read a file"),
        fn("Grep", "search"),
        fn("Glob", "glob"),
        fn("Bash", "run a command"),
        fn("Write", "write a file"),
        fn("Edit", "edit a file"),
        fn("NotebookEdit", "edit a notebook"),
        fn("Task", "spawn a subagent"),
    ]


def test_harness_fixture_write_tools_omitted():
    src = _zcode_style_fixture()
    result = strip_write_tools(src)
    kept = [write_strip._tool_name(t) for t in result["tools"]]
    assert kept == ["Read", "Grep", "Glob", "Bash", "Task"]
    assert sorted(result["receipt"]["stripped_names"]) == ["Edit", "NotebookEdit", "Write"]
    # kept entries are the same objects; nothing was copied/mutated
    assert result["tools"][0] is src[0]


def test_strict_mode_strips_dual_use():
    result = strip_write_tools(_zcode_style_fixture(), strict=True)
    kept = [write_strip._tool_name(t) for t in result["tools"]]
    assert "Bash" not in kept
    assert "Grep" in kept
    kinds = {s["name"]: s["kind"] for s in result["receipt"]["stripped"]}
    assert kinds["Bash"] == "dual_use" and kinds["Write"] == "write"


def test_flat_format_and_empty_and_unnamed():
    flat = [{"name": "read_file"}, {"name": "write_file"}]
    r1 = strip_write_tools(flat)
    assert [write_strip._tool_name(t) for t in r1["tools"]] == ["read_file"]
    assert r1["receipt"]["stripped_names"] == ["write_file"]

    r2 = strip_write_tools([])
    assert r2["tools"] == [] and r2["receipt"]["total"] == 0

    junk = [{"description": "no name here"}, {"name": "read_file"}]
    r3 = strip_write_tools(junk)
    assert r3["receipt"]["unnamed_kept"] == 1
    # the unnamed schema is kept, not dropped
    assert len(r3["tools"]) == 2
    assert r3["receipt"]["kept"] == ["(unnamed)", "read_file"]


def test_read_only_from_env(monkeypatch=None):
    import os

    old = {k: os.environ.get(k) for k in (write_strip.ENV_READ_ONLY, write_strip.ENV_READ_ONLY_STRICT)}
    try:
        os.environ.pop(write_strip.ENV_READ_ONLY, None)
        os.environ.pop(write_strip.ENV_READ_ONLY_STRICT, None)
        assert read_only_from_env() == (False, False)
        os.environ[write_strip.ENV_READ_ONLY] = "1"
        assert read_only_from_env() == (True, False)
        os.environ[write_strip.ENV_READ_ONLY_STRICT] = "true"
        assert read_only_from_env() == (True, True)
        os.environ[write_strip.ENV_READ_ONLY] = "yes"
        assert read_only_from_env() == (True, True)
        os.environ[write_strip.ENV_READ_ONLY] = ""
        assert read_only_from_env() == (False, True)
    finally:
        for k, v in old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


# --- agent_cli activation + backstop -----------------------------------------

def test_activate_read_only_and_backstop():
    from mag import agent_cli

    try:
        receipt = agent_cli.activate_read_only()
        assert "write_file" in receipt["stripped_names"]
        schemas = agent_cli._schemas()
        kept = [write_strip._tool_name(t) for t in schemas]
        assert "write_file" not in kept
        assert "read_file" in kept

        # provider call sites use the compiled grant
        src = inspect.getsource(agent_cli)
        assert "tools=TOOL_SCHEMAS" not in src
        assert "tool_schemas=TOOL_SCHEMAS" not in src

        # backstop: an invented write call is refused, never executed
        out = agent_cli._run_tool("write_file", {"path": "x.txt", "content": "no"})
        assert out["ok"] is False
        assert "read-only seat" in str(out["error"])
        assert not (ROOT / "x.txt").exists()

        # dual-use backstop under strict
        agent_cli.activate_read_only(strict=True)
        assert "run_shell" in agent_cli._DENIED_TOOL_NAMES
        out2 = agent_cli._run_tool("run_shell", {"command": "echo hi"})
        assert out2["ok"] is False
    finally:
        agent_cli.restore_full_grant()
    assert "write_file" in [write_strip._tool_name(t) for t in agent_cli._schemas()]
    assert agent_cli._DENIED_TOOL_NAMES == frozenset()


def test_repack_messages_uses_compiled_grant():
    """With the strip active, the frozen system body carries the read-only
    notice and the canonical schema grant the provider receives is stripped."""
    from mag import agent_cli
    from mag.context_pack import _canonical_schemas_text

    try:
        agent_cli.activate_read_only()
        msgs = agent_cli.repack_messages(
            [{"role": "user", "content": "goal"}],
            user_text="goal",
            traces=[],
            provider="deepseek",
            session_id="write-strip-test-repack",
        )
        assert msgs and msgs[0]["role"] == "system"
        # the seat is told its grant is read-only (prose honesty)
        assert "Read-only seat (fan-out write-strip)" in msgs[0]["content"]
        # the actual tool-schema grant compiled into the prefix is stripped
        schema_text = _canonical_schemas_text(agent_cli._schemas())
        assert '"write_file"' not in schema_text
        assert '"read_file"' in schema_text
    finally:
        agent_cli.restore_full_grant()


# --- orchestrator spawn contract ---------------------------------------------

def test_spawn_task_defaults_read_only():
    from mag import orchestrator

    sig = inspect.signature(orchestrator.spawn_task)
    assert "read_only" in sig.parameters
    assert sig.parameters["read_only"].default is True


def test_read_only_flag_constant_matches_cli():
    assert READ_ONLY_ARG == "--read-only"


def test_flag_wired_through_cli_parsers(capsys):
    """--read-only must be a real option on the main.py `agent` entrypoint."""
    import main as main_module  # noqa: E402

    raised = False
    try:
        main_module.main(["agent", "--help"])
    except SystemExit as e:
        raised = e.code in (0, None)
    assert raised, "agent --help must exit clean"
    out = capsys.readouterr().out
    assert "--read-only" in out
