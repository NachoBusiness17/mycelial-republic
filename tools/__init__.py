from . import code_execution, corpus, filesystem, research, sense_tools, shell, swarm_tools
from mag import vision

TOOL_MAP = {
    "list_dir": lambda **kw: filesystem.list_dir(**kw),
    "read_file": lambda **kw: filesystem.read_file(**kw),
    "write_file": lambda **kw: filesystem.write_file(**kw),
    "apply_patch": lambda **kw: filesystem.apply_patch(**kw),
    "search_files": lambda **kw: filesystem.search_files(**kw),
    "run_shell": lambda **kw: shell.run_shell(**kw),
    "run_python": lambda **kw: code_execution.run_python(**kw),
    # NPC toolbelt — the swarm's sense/communicate/act tools (the castle builds itself)
    "swarm_sense": lambda **kw: swarm_tools.swarm_sense(**kw),
    "pheromone_drop": lambda **kw: swarm_tools.pheromone_drop(**kw),
    "pheromone_trail": lambda **kw: swarm_tools.pheromone_trail(**kw),
    "blackboard_post": lambda **kw: swarm_tools.blackboard_post(**kw),
    "blackboard_read": lambda **kw: swarm_tools.blackboard_read(**kw),
    # deterministic scanner — embedded in the swarm to scan stochastic environments (seeded, $0)
    "scan_measure": lambda **kw: swarm_tools.scan_measure(**kw),
    "scan_probe": lambda **kw: swarm_tools.scan_probe(**kw),
    "scan_grid": lambda **kw: swarm_tools.scan_grid(**kw),
    "mean_field": lambda **kw: swarm_tools.mean_field(**kw),
    "research": lambda **kw: swarm_tools.research(**kw),
    # vision — deepseek-v4-flash-vision-exp (2026-08-25): agents can SEE images now.
    #   vision describe <image_path_or_url> [prompt]  (base64-inline / URL)
    "vision": lambda **kw: vision.describe(**kw),
    # sense bus — voice packets + image-whisper scan for dumb bodies (MCP GPS)
    "voice_turn": sense_tools.voice_turn,
    "whisper_decode": sense_tools.whisper_decode,
    # desk tools — the gateway's four callable organs (P0 master plan, lane R2)
    "biblio_query": lambda **kw: __import__("mag.desk_tools", fromlist=["biblio_query"]).biblio_query(**kw),
    "invariant_sheet": lambda **kw: __import__("mag.desk_tools", fromlist=["invariant_sheet"]).invariant_sheet(**kw),
    "kvos_stats": lambda **kw: __import__("mag.desk_tools", fromlist=["kvos_stats"]).kvos_stats(**kw),
    "fence_strike": lambda **kw: __import__("mag.desk_tools", fromlist=["fence_strike"]).fence_strike(**kw),
    # corpus — the estate catalog surface, read-only, byte-true (salon fold 2026-09-18)
    "corpus_search": lambda **kw: corpus.corpus_search(**kw),
    "corpus_get": lambda **kw: corpus.corpus_get(**kw),
    "corpus_tail": lambda **kw: corpus.corpus_tail(**kw),
    "corpus_stats": lambda **kw: corpus.corpus_stats(**kw),
    # research — the fleet's research corpus surface, read-only (2026-09-18)
    "research_search": lambda **kw: research.research_search(**kw),
    "research_sources": lambda **kw: research.research_sources(**kw),
    "research_stats": lambda **kw: research.research_stats(**kw),
}


# Advertised parameter name -> synonyms models actually emit. Applied only when
# the advertised name is absent, so the mapping is lossless.
_ARG_ALIASES: dict[str, dict[str, str]] = {
    "run_shell": {
        "cmd": "command",
        "command_line": "command",
        "shell_command": "command",
        "script": "command",
    },
    "run_python": {
        "python": "code",
        "code_str": "code",
        "snippet": "code",
        "script": "code",
    },
}


def _normalize_args(name: str, args: dict | None) -> dict | None:
    """Defense against the recurring single-`arguments`-blob shape collapse.

    Models sometimes emit the whole call as one nested dict under the key
    `arguments` (or `params`/`kwargs`) instead of flat named parameters.
    Unwrap that single-key shape so `write_file` binds correctly instead of
    raising a cryptic TypeError that the collapse detector then has to catch
    after 5 identical failures. Returns None on unknown tool.
    """
    args = dict(args or {})
    if name not in TOOL_MAP:
        return None
    # Single-key nested blob: {"arguments": {...}} -> {...}
    # Also unwrap when the value is a JSON *string* (harness captures the
    # parameter value as raw text, so a model emitting one `arguments` param
    # yields {"arguments": '{"path": ...}'} — a string, not a dict).
    for key in ("arguments", "parameters", "params", "kwargs", "kw"):
        if len(args) == 1 and key in args:
            val = args[key]
            if isinstance(val, dict):
                args = dict(val)
                break
            if isinstance(val, str):
                try:
                    import json

                    parsed = json.loads(val)
                    if isinstance(parsed, dict):
                        args = parsed
                        break
                except (ValueError, TypeError):
                    pass
    # Same drift, one level down: models emit the OpenAI code-interpreter
    # parameter names (`cmd`, `code_str`) instead of the advertised ones
    # (`command`, `code`). The advertised name is absent, so the rename is
    # unambiguous — accept it rather than spending a round trip on a TypeError
    # the model may never read (the 2026-08-06 run_shell loop, 25k rows).
    for wrong, right in _ARG_ALIASES.get(name, {}).items():
        if wrong in args and right not in args:
            args[right] = args.pop(wrong)
    return args


# Real callables for signature introspection — the TOOL_MAP lambdas hide
# signatures behind **kw, which would make error messages useless.
_FN = {
    "list_dir": filesystem.list_dir,
    "read_file": filesystem.read_file,
    "write_file": filesystem.write_file,
    "apply_patch": filesystem.apply_patch,
    "search_files": filesystem.search_files,
    "run_shell": shell.run_shell,
    "run_python": code_execution.run_python,
    "swarm_sense": swarm_tools.swarm_sense,
    "pheromone_drop": swarm_tools.pheromone_drop,
    "pheromone_trail": swarm_tools.pheromone_trail,
    "blackboard_post": swarm_tools.blackboard_post,
    "blackboard_read": swarm_tools.blackboard_read,
    "scan_measure": swarm_tools.scan_measure,
    "scan_probe": swarm_tools.scan_probe,
    "scan_grid": swarm_tools.scan_grid,
    "mean_field": swarm_tools.mean_field,
    "research": swarm_tools.research,
    "voice_turn": sense_tools.voice_turn,
    "whisper_decode": sense_tools.whisper_decode,
    # desk tools (P0 master plan)
    "biblio_query": __import__("mag.desk_tools", fromlist=["biblio_query"]).biblio_query,
    "invariant_sheet": __import__("mag.desk_tools", fromlist=["invariant_sheet"]).invariant_sheet,
    "kvos_stats": __import__("mag.desk_tools", fromlist=["kvos_stats"]).kvos_stats,
    "fence_strike": __import__("mag.desk_tools", fromlist=["fence_strike"]).fence_strike,
    # corpus (salon fold 2026-09-18)
    "corpus_search": corpus.corpus_search,
    "corpus_get": corpus.corpus_get,
    "corpus_tail": corpus.corpus_tail,
    "corpus_stats": corpus.corpus_stats,
    # research (2026-09-18)
    "research_search": research.research_search,
    "research_sources": research.research_sources,
    "research_stats": research.research_stats,
}


def _expected_params(name: str) -> str:
    import inspect

    fn = _FN.get(name) or TOOL_MAP[name]
    try:
        sig = inspect.signature(fn)
    except (TypeError, ValueError):
        return "(unknown signature)"
    parts = []
    for p in sig.parameters.values():
        if p.kind in (p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY):
            default = "" if p.default is inspect.Parameter.empty else f"={p.default!r}"
            parts.append(f"{p.name}{default}")
        elif p.kind == p.VAR_KEYWORD:
            parts.append(f"**{p.name}")
    return ", ".join(parts) or "(no params)"


def dispatch(name: str, args: dict | None = None) -> dict:
    if name not in TOOL_MAP:
        return {"ok": False, "exit_code": 127, "error": f"unknown tool: {name}", "tools": list(TOOL_MAP)}
    args = _normalize_args(name, args)
    try:
        return TOOL_MAP[name](**args)
    except TypeError as e:
        # Convert the cryptic binding error into an actionable shape error so
        # the model recovers on the FIRST attempt instead of looping until the
        # collapse detector fires (bug #2 in the 2026-08-03 12h sovereign run).
        return {
            "ok": False,
            "exit_code": 2,
            "error": (
                f"bad arguments for {name}: {e}. "
                f"Expected flat named parameters: {_expected_params(name)}. "
                "Emit ONE <parameter name='X'> element per argument as SIBLINGS — "
                "never nest them under a single 'arguments' blob."
            ),
            "expected_params": _expected_params(name),
            "received_args": sorted(args),
        }


__all__ = ["TOOL_MAP", "dispatch"]
