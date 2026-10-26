from . import code_execution, corpus, drift, filesystem, research, sense_tools, shell, swarm_tools, thrash_meter, verb_anchor
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
    # drift — the metric-referent instrument (2026-09-18): corr(delta-M, delta-R)
    "drift_check": lambda **kw: drift.drift_check_cmd(**kw),
    # thrash_meter (THE 50 W6 T27, 2026-09-19): multi-front interleaving over the trajectory log
    "thrash_meter": lambda **kw: thrash_meter.thrash_cmd(**kw),
    # verb_anchor (THE 50 W9 T43, 2026-09-19): verb kifu tail -> one live verkle chain anchor row
    "verb_anchor": lambda **kw: verb_anchor.anchor(**kw),
    # estate bridge R1 (2026-09-29): the estate verbs on the house MCP surface.
    # Design + per-tool rulings: watch/inbox/burn_reset_20260927/flash50/
    # mcp-bridge.md section 3. One tool per verb; chain REPAIR, dirac BANK and
    # the driver control words are NEVER registered (verkle blast radius,
    # broker-gated R4, funded keys never cross). Static entries, not the
    # ephemeral overlay: standing organs. Wrappers live in mag/estate_bridge.
    "estate_water_graph_tick": lambda **kw: __import__("mag.estate_bridge", fromlist=["water_graph_tick"]).water_graph_tick(**kw),
    "estate_dirac_scan": lambda **kw: __import__("mag.estate_bridge", fromlist=["dirac_scan"]).dirac_scan(**kw),
    "estate_dirac_rank": lambda **kw: __import__("mag.estate_bridge", fromlist=["dirac_rank"]).dirac_rank(**kw),
    "estate_chain_verify": lambda **kw: __import__("mag.estate_bridge", fromlist=["chain_verify"]).chain_verify(**kw),
    "estate_thought_compile": lambda **kw: __import__("mag.estate_bridge", fromlist=["thought_compile"]).thought_compile(**kw),
    "estate_driver_status": lambda **kw: __import__("mag.estate_bridge", fromlist=["driver_status"]).driver_status(**kw),
    # R2.5 (2026-10-01, watch/inbox/ractor50/mcp.md section 9): the receipt
    # write path under the shared-surface contract - watch/inbox/<wave>/
    # only, append-only (rotate to .bak), never INDEX.json.
    "estate_receipt_append": lambda **kw: __import__("mag.estate_bridge", fromlist=["receipt_append"]).receipt_append(**kw),
    # shared surface (2026-10-17): warm-pack read (fixed mag://warm/* URIs) and
    # the seat receipt writer (watch/receipts/ only, server-named files).
    "estate_warm_read": lambda **kw: __import__("mag.estate_bridge", fromlist=["warm_read"]).warm_read(**kw),
    "estate_shared_receipt": lambda **kw: __import__("mag.estate_bridge", fromlist=["shared_receipt_append"]).shared_receipt_append(**kw),
    "estate_propose": lambda **kw: __import__("mag.proposals", fromlist=["tool_propose"]).tool_propose(**kw),
    "estate_review": lambda **kw: __import__("mag.proposals", fromlist=["tool_review"]).tool_review(**kw),
    "estate_proposals": lambda **kw: __import__("mag.proposals", fromlist=["tool_proposals"]).tool_proposals(**kw),
    # fleet coordination (2026-10-17): fleet_report.v1 + notices (mag/fleet_report.py)
    # and restricted-list leases (mag/leases.py, configs/restricted_leases.json).
    "estate_fleet_report": lambda **kw: __import__("mag.fleet_report", fromlist=["file_report"]).file_report(**kw),
    "estate_notices": lambda **kw: __import__("mag.fleet_report", fromlist=["tool_notices"]).tool_notices(**kw),
    "estate_lease_acquire": lambda **kw: __import__("mag.leases", fromlist=["acquire"]).acquire(**kw),
    "estate_lease_renew": lambda **kw: __import__("mag.leases", fromlist=["renew"]).renew(**kw),
    "estate_lease_release": lambda **kw: __import__("mag.leases", fromlist=["release"]).release(**kw),
    "estate_lease_transfer": lambda **kw: __import__("mag.leases", fromlist=["transfer"]).transfer(**kw),
    "estate_leases": lambda **kw: __import__("mag.leases", fromlist=["tool_leases"]).tool_leases(**kw),
        "estate_queue_closes": lambda **kw: __import__("mag.estate_bridge", fromlist=["queue_closes"]).queue_closes(**kw),
    }

# Static registry baseline, frozen at import: the ephemeral overlay (below) can
# add and remove entries in TOOL_MAP, but a static tool can never be shadowed
# or removed through it. mag/skill_lifecycle.py is the only intended writer of
# the overlay; it gates every write behind ADK_ENABLE_SKILL_LIFECYCLE (default
# OFF), so with the gate unset this module behaves exactly as before.
STATIC_TOOLS = frozenset(TOOL_MAP)

# name -> {"fn": callable, "meta": dict}. Tools registered here are visible in
# TOOL_MAP for a bounded lease and are removed by unregister_ephemeral /
# unload_ephemeral_all. Empty by default, so default-off behavior is unchanged.
_EPHEMERAL: dict[str, dict] = {}


def register_ephemeral(name: str, fn, meta: dict | None = None) -> dict:
    """Register a lease-bound tool into TOOL_MAP. Returns a receipt."""
    if name in STATIC_TOOLS:
        return {
            "ok": False,
            "reason": "name_conflict",
            "tool": name,
            "hint": "refusing to shadow a static registry tool",
        }
    if name in _EPHEMERAL:
        return {
            "ok": False,
            "reason": "already_registered",
            "tool": name,
            "hint": "unload it first (tools.unregister_ephemeral)",
        }
    _EPHEMERAL[name] = {"fn": fn, "meta": dict(meta or {})}
    TOOL_MAP[name] = fn
    return {"ok": True, "tool": name, "registered": True}


def unregister_ephemeral(name: str) -> dict:
    """Remove a lease-bound tool. Idempotent; never removes a static tool."""
    rec = _EPHEMERAL.pop(name, None)
    if rec is None:
        if name in STATIC_TOOLS:
            return {
                "ok": False,
                "reason": "not_ephemeral",
                "tool": name,
                "hint": "static registry tools are never unloaded via the overlay",
            }
        return {"ok": True, "tool": name, "already_gone": True}
    TOOL_MAP.pop(name, None)
    return {"ok": True, "tool": name, "unregistered": True}


def unload_ephemeral_all() -> list[str]:
    """Drop every lease-bound tool (used by tests and the lifecycle sweeper)."""
    for name in sorted(_EPHEMERAL):
        TOOL_MAP.pop(name, None)
    gone = sorted(_EPHEMERAL)
    _EPHEMERAL.clear()
    return gone


def ephemeral_tool_names() -> list[str]:
    return sorted(_EPHEMERAL)


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
    # estate bridge R1 (2026-09-29): the synonyms models actually emit for the
    # bridge tools' advertised parameters (mcp-bridge.md 4.2.2).
    "estate_water_graph_tick": {
        "graph": "spec",
        "water_spec": "spec",
        "steps": "ticks",
        "n_ticks": "ticks",
    },
    "estate_dirac_scan": {"graph_scope": "scope"},
    "estate_dirac_rank": {"graph_scope": "scope"},
    "estate_driver_status": {"lines": "tail", "n": "tail"},
    # R2.5 (ractor50 mcp.md section 9): the synonyms a receipt-filing model
    # emits for the advertised wave/name/payload parameters.
    "estate_receipt_append": {"file": "name", "text": "payload"},
    "estate_shared_receipt": {"text": "body", "payload": "body", "content": "body",
                              "seat_name": "seat", "model_id": "model"},
    # fleet coordination (2026-10-17)
    "estate_fleet_report": {"type": "kind", "fields": "report", "body": "report",
                            "seat_name": "seat", "model_id": "model"},
    "estate_lease_acquire": {"holder": "seat", "reason": "purpose", "ttl": "ttl_s"},
    "estate_lease_renew": {"token": "lease_token", "holder": "seat", "ttl": "ttl_s"},
    "estate_lease_release": {"token": "lease_token", "holder": "seat"},
    "estate_lease_transfer": {"token": "lease_token", "holder": "seat", "to": "to_seat",
                              "ttl": "ttl_s"},
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
    # drift (2026-09-18)
    "drift_check": drift.drift_check_cmd,
    # thrash_meter (THE 50 W6 T27, 2026-09-19)
    "thrash_meter": thrash_meter.thrash_cmd,
    # verb_anchor (THE 50 W9 T43, 2026-09-19)
    "verb_anchor": verb_anchor.anchor,
    # estate bridge R1 (2026-09-29): real callables for signature introspection
    # and honest error messages (see TOOL_MAP comment above).
    "estate_water_graph_tick": __import__("mag.estate_bridge", fromlist=["water_graph_tick"]).water_graph_tick,
    "estate_dirac_scan": __import__("mag.estate_bridge", fromlist=["dirac_scan"]).dirac_scan,
    "estate_dirac_rank": __import__("mag.estate_bridge", fromlist=["dirac_rank"]).dirac_rank,
    "estate_chain_verify": __import__("mag.estate_bridge", fromlist=["chain_verify"]).chain_verify,
    "estate_thought_compile": __import__("mag.estate_bridge", fromlist=["thought_compile"]).thought_compile,
    "estate_driver_status": __import__("mag.estate_bridge", fromlist=["driver_status"]).driver_status,
    "estate_receipt_append": __import__("mag.estate_bridge", fromlist=["receipt_append"]).receipt_append,
    "estate_warm_read": __import__("mag.estate_bridge", fromlist=["warm_read"]).warm_read,
    "estate_shared_receipt": __import__("mag.estate_bridge", fromlist=["shared_receipt_append"]).shared_receipt_append,
    "estate_propose": __import__("mag.proposals", fromlist=["tool_propose"]).tool_propose,
    "estate_review": __import__("mag.proposals", fromlist=["tool_review"]).tool_review,
    "estate_proposals": __import__("mag.proposals", fromlist=["tool_proposals"]).tool_proposals,
    "estate_fleet_report": __import__("mag.fleet_report", fromlist=["file_report"]).file_report,
    "estate_notices": __import__("mag.fleet_report", fromlist=["tool_notices"]).tool_notices,
    "estate_lease_acquire": __import__("mag.leases", fromlist=["acquire"]).acquire,
    "estate_lease_renew": __import__("mag.leases", fromlist=["renew"]).renew,
    "estate_lease_release": __import__("mag.leases", fromlist=["release"]).release,
    "estate_lease_transfer": __import__("mag.leases", fromlist=["transfer"]).transfer,
    "estate_leases": __import__("mag.leases", fromlist=["tool_leases"]).tool_leases,
        "estate_queue_closes": __import__("mag.estate_bridge", fromlist=["queue_closes"]).queue_closes,
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
