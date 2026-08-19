"""Unified routing — one classifier, one seat matrix, honest failures.

All entry points (coordinate, dispatch, governor autorun, REST) should call
``route()`` so the same goal always gets the same seat/provider/mode.

Schema: route.v2
"""
from __future__ import annotations

import os
from typing import Any

from mag.coordination import DEPTH_ROUTES, VALID_DEPTHS, _clip

DEPTH_JOB_MAP: dict[str, str] = {
    "scut": "scut",
    "conversation": "default",
    "simple_code": "default",
    "heavy_code": "hard_code",
    "plan": "hard_reason",
    "overview": "hard_reason",
}

_CURSOR_MARKERS = (
    "via cursor",
    "cursor ide",
    "cursor seat",
    "seat cursor",
    "--seat cursor",
    "[cursor]",
    "[composer]",
)
_HERMES_MARKERS = (
    "via hermes",
    "hermes agent",
    "use hermes",
    "with hermes",
    "seat hermes",
    "hermes seat",
    "--seat hermes",
)
_SECRET_MARKERS = ("secret", "password", ".env", "private", "data/raw", "intimate")
_RESEARCH_MARKERS = (
    "research",
    "scrape",
    "according to",
    "from the pack",
    "research pack",
    "what does the site",
    "compare sources",
)

# RIBs are BARE METAL (2026-08-15, operator): frozen deterministic specs compiled by our OWN
# close-to-compiler machinery (rib_struct / rib_bus / invariant lattice / compiler_lang). This is
# deterministic + $0 work — it must route to the cheapest local tier, NEVER up to plan/overview (Grok).
_RIB_MARKERS = (
    "rib",
    "rib_struct",
    "rib_bus",
    "rib_action",
    "bare metal",
    "baremetal",
    "own compiler",
    "compile",
    "compiler",
    "invariant",
    "frozen spec",
    "declare rib",
    "knot invariant",
)


def gather_signals() -> dict[str, Any]:
    """Runtime probes used for routing (no network unless bridge env set)."""
    out: dict[str, Any] = {
        "drainer": os.environ.get("MAG_DRAINER", "").strip().lower() in ("1", "true", "yes"),
        "pending_breadcrumbs": 0,
        "grok_budget_ok": True,
        "home_reachable": True,
    }
    try:
        from mag.operator_inbox import status as inbox_status

        out["pending_breadcrumbs"] = int(inbox_status().get("pending_n") or 0)
    except Exception:
        pass
    try:
        from mag.lanes import grok_escalations_today, load_lanes

        lanes = load_lanes()
        max_d = int((lanes.get("grok_budget") or {}).get("max_escalations_per_day") or 8)
        used = grok_escalations_today()
        out["grok_escalations_today"] = used
        out["grok_budget_max"] = max_d
        out["grok_budget_ok"] = used < max_d
    except Exception:
        pass
    if os.environ.get("MAG_PUBLIC_URL", "").strip():
        try:
            from watch.cursor_bridge import probe_hq

            out["home_reachable"] = bool(probe_hq().get("reachable"))
        except Exception:
            out["home_reachable"] = False
    return out


def _detect_markers(goal: str) -> dict[str, bool]:
    g = (goal or "").lower()
    return {
        "cursor": any(m in g for m in _CURSOR_MARKERS),
        "hermes": any(m in g for m in _HERMES_MARKERS),
        "secret": any(m in g for m in _SECRET_MARKERS),
        "research": any(m in g for m in _RESEARCH_MARKERS),
        "rib": any(m in g for m in _RIB_MARKERS),
        "priority": any(m in g for m in ("[priority]", "[l2]", "[grok]")),
    }


def classify_depth(goal: str, *, depth: str | None = None) -> dict[str, Any]:
    """Unified depth classifier (replaces parallel keyword lists)."""
    if depth and depth in VALID_DEPTHS:
        route = dict(DEPTH_ROUTES[depth])
        return {
            "ok": True,
            "schema": "depth_class.v1",
            "depth": depth,
            "goal": _clip(goal, 300),
            "forced": True,
            **route,
        }

    markers = _detect_markers(goal)
    g = (goal or "").lower()
    n = len(goal or "")

    if markers["secret"]:
        depth = "scut"
    elif markers["rib"]:
        # RIBs are bare metal — compiled by our own close-to-compiler machinery, deterministic + $0.
        # Never route RIB work up to plan/overview (Grok TUI, frontier $); keep it local L0.
        depth = "scut"
    elif markers["research"]:
        depth = "simple_code"
    elif any(
        k in g
        for k in (
            "big picture",
            "interlink",
            "ecosystem map",
            "how does",
            "relate to",
            "overview",
            "two houses",
            "republic chain",
            "architecture map",
            "full stack",
        )
    ):
        depth = "overview"
    elif any(
        k in g
        for k in (
            "plan ",
            "design ",
            "tradeoff",
            "strategy",
            "roadmap",
            "architecture for",
            "how should we",
            "code planning",
            "critique plan",
            "analyze deeply",
        )
    ):
        depth = "plan"
    # Life / ideas dig — not code. Before scut/simple_code so Bernays ≠ simple_code.
    elif any(
        k in g
        for k in (
            "talk about",
            "talk to you about",
            "want to talk",
            "about life",
            "propaganda",
            "philosophy",
            "berna",
            "edward bernays",
            "who benefits",
            "what do you think about",
            "tell me about",
            "curious about",
            "meaning of",
            "ideas about",
        )
    ) or (
        n >= 20
        and not any(
            k in g
            for k in (
                "implement",
                "refactor",
                "pytest",
                "deploy",
                "pull request",
                "bios",
                "sam settings",
                "fix lint",
            )
        )
        and any(
            k in g
            for k in (
                "life",
                "people",
                "society",
                "culture",
                "history",
                "politics",
                "media",
                "power",
                "freedom",
                "attention",
            )
        )
    ):
        depth = "conversation"
    elif any(
        k in g
        for k in (
            "doctor",
            "health",
            "multi-smoke",
            "status",
            "what was i",
            "brief",
            "bonds",
            "list ",
            "show ",
            "ls ",
            "recall",
            "open loop",
            "biograph",
            "quota",
            "providers",
            "hear me",
            "can you hear",
            "hello",
            "good morning",
            "good night",
            "thank you",
            "thanks",
        )
    ) or (n < 80 and "?" in g) or (n < 36 and any(k in g for k in ("hey", "hi ", "hi,", "yo "))):
        depth = "scut"
    elif any(
        k in g
        for k in (
            "rename",
            "typo",
            "one line",
            "single file",
            "add import",
            "fix lint",
            "small fix",
        )
    ) or (n < 120 and any(k in g for k in ("fix ", "patch ", "tweak "))):
        depth = "simple_code"
    elif any(
        k in g
        for k in (
            "implement",
            "refactor",
            "multi-file",
            "orchestrat",
            "write tests",
            "migrate",
            "build feature",
            "heavy",
            "tool loop",
        )
    ) or n > 350:
        depth = "heavy_code"
    elif any(k in g for k in ("implement", "refactor", "add ", "create ", "update ")):
        depth = "simple_code" if n < 200 else "heavy_code"
    elif any(k in g for k in ("summarize", "translate", "draft", "public", "readme")):
        depth = "simple_code"
    else:
        depth = "simple_code" if n < 180 else "plan"

    route = dict(DEPTH_ROUTES[depth])
    return {
        "ok": True,
        "schema": "depth_class.v1",
        "depth": depth,
        "goal": _clip(goal, 300),
        "forced": False,
        **route,
    }


def _tier_for_depth(depth: str, *, secret: bool) -> str:
    if secret:
        return "T1"
    if depth in ("overview", "plan", "heavy_code"):
        return "T2"
    if depth == "scut":
        return "T2"
    return "T2"


def _match_skills(goal: str, depth: str, job: str) -> list[str]:
    skills: list[str] = []
    try:
        from mag.skills_pack import load_skills_cfg

        cfg = load_skills_cfg()
        job_map = cfg.get("job_to_skills") or {}
        skills.extend(list(job_map.get(job) or job_map.get("default") or []))
    except Exception:
        pass
    try:
        from ijl_core import skill_excerpt_for_goal

        if skill_excerpt_for_goal(goal, max_chars=40).strip():
            skills.append("ijl:matched")
    except Exception:
        pass
    if depth in ("heavy_code", "simple_code") and "patch-verify" not in skills:
        g = (goal or "").lower()
        if any(k in g for k in ("fix", "patch", "refactor", "implement")):
            skills.append("patch-verify")
    return skills


def route(
    goal: str,
    *,
    depth: str | None = None,
    force_seat: str | None = None,
    force_provider: str | None = None,
    signals: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Single routing decision for a goal."""
    from models.quota import pick_provider, provider_budget

    goal = (goal or "").strip()
    if not goal:
        return {"ok": False, "schema": "route.v2", "error": "empty goal"}

    sig = signals if signals is not None else gather_signals()
    markers = _detect_markers(goal)
    classified = classify_depth(goal, depth=depth)
    d = str(classified.get("depth") or "simple_code")
    job = DEPTH_JOB_MAP.get(d, "default")
    tier = _tier_for_depth(d, secret=markers["secret"])
    why: list[str] = [f"depth={d}"]

    force_seat = force_seat.strip().lower() if force_seat else None
    force_provider = force_provider.strip().lower() if force_provider else None

    # --- explicit seats (markers win) ---
    if force_seat:
        seat = force_seat
        why.append(f"force_seat={seat}")
    elif markers["hermes"]:
        seat = "hermes"
        why.append("marker=hermes")
    elif markers["cursor"]:
        seat = "cursor"
        why.append("marker=cursor")
    elif d in ("overview", "plan"):
        seat = "grok_tui"
        why.append("planning=pack_only")
    elif d in ("scut", "simple_code"):
        seat = "local"
        why.append("janitor=local")
    elif d == "heavy_code":
        seat = "deepseek"
        why.append("execution=heavy")
    else:
        seat = str(classified.get("seat") or "local")

    mode = str(classified.get("mode") or "dispatch")
    launch = bool(classified.get("launch", True))
    provider: str | None = None
    pick: dict[str, Any] = {"ok": False, "skipped": True}
    rental = False
    executable = False
    ok = True
    error: str | None = None
    hint = str(classified.get("token_hint") or "")

    if force_provider:
        provider = force_provider
        why.append(f"force_provider={provider}")
        if provider == "ollama":
            seat = "local"
        elif provider in ("groq", "openrouter", "deepseek", "deepseek_overmind", "anthropic", "vast"):
            seat = "remote"
        else:
            why.append("force_provider=unknown")

    if force_seat and force_provider:
        if force_seat == "local" and provider != "ollama":
            why.append("force_seat_ignored_for_nonlocal_provider")
        if force_seat == "remote" and provider == "ollama":
            why.append("force_provider_ignored_for_remote_seat")
    if d in ("overview", "plan"):
        if not markers["priority"] and not sig.get("grok_budget_ok", True):
            ok = False
            error = "grok_budget_exhausted"
            hint = "Grok daily budget exhausted — wait or raise lanes.yaml max_escalations_per_day"
            why.append("grok_budget=blocked")
        else:
            launch = False
            mode = "plan"
            executable = False
            hint = classified.get("token_hint") or "File pack for Grok TUI — do not auto-run"
            why.append("launch=false")
        return _route_payload(
            goal, d, job, tier, seat, provider, mode, launch, executable, ok, error, hint,
            why, pick, classified, sig, markers, skills=_match_skills(goal, d, job),
        )

    # --- defer seats ---
    if seat in ("cursor", "hermes", "grok_tui"):
        launch = False
        executable = False
        if seat == "cursor":
            mode = "defer_cursor"
            hint = "Use Cursor IDE or cursor_bridge steer when home is reachable"
        elif seat == "hermes":
            mode = "defer_hermes"
            hint = "Hermes is parked — explicit opt-in only"
        return _route_payload(
            goal, d, job, tier, seat, provider, mode, launch, executable, ok, error, hint,
            why, pick, classified, sig, markers, skills=_match_skills(goal, d, job),
        )

    # --- local janitor ---
    if seat == "local" or (not force_seat and d in ("scut", "simple_code")):
        seat = "local"
        prefer = ["deepseek", "deepseek_overmind", "ollama", "groq", "openrouter"]
        pick = pick_provider(job=job if job != "default" else "scut", tier=tier, prefer=prefer)
        if pick.get("ok"):
            if not force_provider:
                provider = str(pick.get("provider") or "ollama")
            else:
                provider = force_provider
            if provider != "ollama":
                seat = "remote"
                why.append(f"pick={provider}")
            else:
                provider = "ollama"
                why.append("provider=ollama")
        else:
            provider = "ollama"
            why.append("fallback=ollama")
        mode = "dispatch"
        launch = True
        executable = True
        return _route_payload(
            goal, d, job, tier, seat, provider, mode, launch, executable, ok, error, hint,
            why, pick, classified, sig, markers, skills=_match_skills(goal, d, job),
        )

    # --- heavy execution ---
    if d == "heavy_code" or seat == "deepseek":
        vast = provider_budget("vast")
        prefer: list[str] | None = None
        if vast.get("configured") and vast.get("budget_ok"):
            prefer = ["vast", "deepseek", "deepseek_overmind", "anthropic"]
            rental = True
            why.append("rental=vast")
        else:
            prefer = ["deepseek", "deepseek_overmind", "anthropic", "vast"]

        pick = pick_provider(job="hard_code", tier=tier, prefer=prefer)
        if pick.get("ok"):
            provider = str(pick.get("provider"))
            seat = "local" if provider == "ollama" else "remote"
            mode = "queue" if sig.get("drainer") else "delegate"
            launch = True
            executable = True
            why.append(f"pick={provider}")
            if sig.get("drainer"):
                why.append("drainer=queue")
        else:
            ok = False
            error = "no_execution_provider"
            launch = False
            executable = False
            provider = "deepseek"
            mode = "delegate"
            hint = (
                pick.get("hint")
                or "Set DEEPSEEK_API_KEY (or vast/openrouter) — heavy work cannot run"
            )
            why.append("pick=failed")
            if markers["cursor"]:
                seat = "cursor"
                ok = True
                error = None
                launch = False
                executable = False
                mode = "defer_cursor"
                hint = "No API execution provider — use Cursor seat on git clone"
                why.append("fallback=cursor_defer")

        return _route_payload(
            goal, d, job, tier, seat, provider, mode, launch, executable, ok, error, hint,
            why, pick, classified, sig, markers, skills=_match_skills(goal, d, job),
            rental=rental,
        )

    # --- remote summarize / default ---
    pick = pick_provider(job=job, tier=tier)
    if pick.get("ok"):
        provider = str(pick.get("provider"))
        seat = "remote"
        mode = "dispatch"
        launch = True
        executable = True
    else:
        provider = "ollama"
        seat = "local"
        mode = "dispatch"
        launch = True
        executable = True
        why.append("fallback=ollama")

    return _route_payload(
        goal, d, job, tier, seat, provider, mode, launch, executable, ok, error, hint,
        why, pick, classified, sig, markers, skills=_match_skills(goal, d, job),
    )


_HANDOFF_MARKERS = (
    "handoff", "hand off", "continue", "resume", "pick up", "as discussed",
    "as we discussed", "deep-handoff", "carry on", "carry over", "following up",
    "following on", "take over", "where we left off", "the run we started",
)


def _context_plan(
    goal: str, depth: str, job: str, tier: str, mode: str, provider: str | None,
) -> dict[str, Any]:
    """Decide the ASK'S REPRESENTATION: handoff vs fresh, and which model shape to call.

    The router today picks a DESTINATION (tier/seat/provider) but not the ask's
    representation. This fills that gap so we think about WHAT MODEL we're calling and
    WHAT CONTEXT rides in the prompt (the 'spend on the spec, not the tier' doctrine):
      - is_handoff   : does the receiving model need the session MAZE / frozen RIB to
                       CONTINUE (map-is-the-territory), vs a fresh context pack?
      - context_plan : 'handoff_maze' | 'fresh_context_pack' (what to attach).
      - model_shape  : cheap/heavy/reasoning/balanced — choose the model by TASK SHAPE,
                       not the provider's default_model.
      - model_hint   : which actual model to call for that shape.
    """
    g = (goal or "").lower()
    is_handoff = any(m in g for m in _HANDOFF_MARKERS) or mode in ("deep-handoff", "handoff")
    if depth in ("plan", "overview"):
        model_shape = "reasoning"
    elif depth == "heavy_code":
        model_shape = "heavy"
    elif depth in ("scut", "simple_code"):
        model_shape = "cheap"
    else:
        model_shape = "balanced"
    context_plan = "handoff_maze" if is_handoff else "fresh_context_pack"
    hint_map = {
        "cheap": "cheapest flash/edge model of the provider — exec scores 1.00 on all tiers (tier_probe)",
        "balanced": "default balanced model of the provider",
        "heavy": "pro/heavy model of the provider (hard_code)",
        "reasoning": "reasoning-capable model (grok TUI / deepseek pro) — plan/reason, do not auto-run",
    }
    return {
        "is_handoff": is_handoff,
        "context_plan": context_plan,
        "model_shape": model_shape,
        "model_hint": hint_map[model_shape],
    }


def _route_payload(
    goal: str,
    depth: str,
    job: str,
    tier: str,
    seat: str,
    provider: str | None,
    mode: str,
    launch: bool,
    executable: bool,
    ok: bool,
    error: str | None,
    hint: str,
    why: list[str],
    pick: dict[str, Any],
    classified: dict[str, Any],
    signals: dict[str, Any],
    markers: dict[str, bool],
    *,
    skills: list[str] | None = None,
    rental: bool = False,
) -> dict[str, Any]:
    ctx = _context_plan(goal, depth, job, tier, mode, provider)
    return {
        "ok": ok,
        "schema": "route.v2",
        "goal": _clip(goal, 300),
        "depth": depth,
        "job": job,
        "tier": tier,
        "seat": seat,
        "provider": provider,
        "model_shape": ctx["model_shape"],
        "context_plan": ctx["context_plan"],
        "is_handoff": ctx["is_handoff"],
        "model_hint": ctx["model_hint"],
        "mode": mode,
        "launch": launch,
        "executable": executable,
        "error": error,
        "hint": hint,
        "why": why,
        "pick": pick,
        "classification": classified,
        "signals": signals,
        "markers": markers,
        "skills": skills or [],
        "rental": rental,
    }


def route_task(goal: str, *, depth: str | None = None) -> dict[str, Any]:
    """Governor/autorun compat — route.v1 shape backed by route.v2."""
    r = route(goal, depth=depth)
    provider = r.get("provider") or "ollama"
    depth_s = str(r.get("depth") or "simple_code")
    mult = {"scut": 1, "simple_code": 2, "heavy_code": 8, "plan": 3, "overview": 2}
    base = max(500, len(goal or "") * 4)
    return {
        "ok": r.get("ok", False),
        "schema": "route.v1",
        "goal": r.get("goal"),
        "depth": depth_s,
        "job": r.get("job"),
        "provider": provider,
        "mode": r.get("mode"),
        "launch": r.get("launch"),
        "rental": r.get("rental", False),
        "classification": r.get("classification"),
        "pick": r.get("pick"),
        "cost_estimate": {
            "tokens_est": base * mult.get(depth_s, 2),
            "depth": depth_s,
            "provider": provider,
        },
        "skills": r.get("skills") or [],
        "executable": r.get("executable"),
        "error": r.get("error"),
        "hint": r.get("hint"),
        "why": r.get("why"),
    }


def route_with_snapshot(
    goal: str,
    *,
    snapshot: dict[str, Any] | None = None,
    depth: str | None = None,
    force_seat: str | None = None,
    force_provider: str | None = None,
) -> dict[str, Any]:
    """Route with session-state awareness.

    When a frozen session snapshot is provided, the router adjusts
    seat/provider selection based on the agent's current execution context:

    - Status 'blocked' or 'escalated' → auto-escalate one tier up
    - Status 'done' → route to wait (no auto-run)
    - Goal keywords matching 'design/architect/refactor' + heavy depth →
      escalate to DeepSeek with frozen RIB
    - Scut/simple tasks → stay local ollama
    - Agent state has pending next_moves → prefer local execution
    """
    # Base routing decision
    result = route(goal, depth=depth, force_seat=force_seat, force_provider=force_provider)

    if snapshot is None:
        return result

    # Extract session context
    session_ctx = snapshot.get("layers", {}).get("session_context", {})
    if not session_ctx:
        # Try summary-level fields
        summary = snapshot.get("summary", {})
        session_ctx = {
            "current_status": summary.get("status"),
            "current_goal": summary.get("goal"),
            "_keywords": summary.get("keywords", []),
        }

    status = (session_ctx.get("current_status") or "").lower()
    keywords = session_ctx.get("_keywords", [])
    agent_state = snapshot.get("layers", {}).get("agent_state", {})
    has_pending = (agent_state.get("next_moves") or []).get("length" if isinstance(agent_state.get("next_moves"), list) else 0) > 0 if agent_state.get("next_moves") else False

    # ── Session-aware adjustments ──
    why_session: list[str] = []

    # Status-based escalation
    if "blocked" in status:
        why_session.append("session_status=blocked→escalate")
        result["tier"] = "T3"
        if result.get("provider") == "ollama":
            result["provider"] = "deepseek"
            result["seat"] = "remote"
            result["mode"] = "queue"
    elif "escalat" in status:
        why_session.append("session_status=escalated→force_remote")
        if result.get("provider") == "ollama":
            result["provider"] = "deepseek"
            result["seat"] = "remote"
    elif "done" in status or "closed" in status:
        why_session.append("session_status=done→wait")
        result["launch"] = False
        result["executable"] = False
        result["mode"] = "wait"

    # Keyword-based escalation (design/architect tasks → DeepSeek)
    heavy_kw = {"design", "architect", "refactor", "implement", "migrate", "orchestrat"}
    if any(kw in heavy_kw for kw in keywords):
        current_depth = result.get("depth", "")
        if current_depth in ("heavy_code", "plan"):
            why_session.append("keywords=heavy_design→deepseek")
            if result.get("provider") == "ollama":
                result["provider"] = "deepseek"
                result["seat"] = "remote"
                result["mode"] = "queue"

    # Pending agent_state next_moves → prefer local execution (don't escalate)
    if has_pending and result.get("provider") != "ollama":
        why_session.append("agent_has_pending→stay_local")
        # Don't override if already explicitly routed

    # Append session-aware reasoning
    if why_session:
        result["why"] = (result.get("why") or []) + why_session
        result["session_aware"] = True

    return result
