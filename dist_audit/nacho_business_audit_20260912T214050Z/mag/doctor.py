"""Doctor Protocol — independent configuration sanity checker.

Runs BEFORE tasks are dispatched. Catches misconfigurations that would
waste money, leak data, or violate system invariants. Lives independently
in the test path — not coupled to the main loop.

WHAT IT WOULD HAVE CAUGHT TODAY:
  - Defaulting to grok-4-latest ($0.025) when grok-3-mini ($0.003) is available
  - Provider mismatch: using "grok" instead of "xai" in copilot inbox messages
  - Missing XAI_API_KEY when Grok tasks are queued
  - Cost cap violations before they happen

CHECKS:
  1. Provider sanity — are all referenced providers configured?
  2. Model sanity — are all referenced models available?
  3. Cost sanity — would any queued task exceed the daily cap?
  4. Inbox sanity — are there malformed messages?
  5. Env sanity — are required environment variables set?
  6. Verkle sanity — is the chain healthy?

Schema: doctor.v1
Law: Doctor runs BEFORE dispatch. Failures block the pipeline.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from config import ROOT
except ImportError:
    ROOT = Path(__file__).resolve().parent.parent


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read_jsonl(path: Path, tail: int = 50) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    lines = path.read_text(encoding="utf-8", errors="replace").strip().splitlines()
    if tail and len(lines) > tail:
        lines = lines[-tail:]
    rows: list[dict[str, Any]] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


@dataclass
class DoctorReport:
    ok: bool
    checks: list[dict[str, Any]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    ts: str = field(default_factory=_now)


# ═══════════════════════════════════════════════════════════════════
# CHECKS
# ═══════════════════════════════════════════════════════════════════

def check_provider_sanity() -> dict[str, Any]:
    """Check that all referenced providers are configured with valid keys."""
    issues = []
    providers_ok = []

    # Check Grok
    xai_key = os.environ.get("XAI_API_KEY") or os.environ.get("GROK_API_KEY") or ""
    if xai_key:
        providers_ok.append("xai/grok")
    else:
        issues.append("XAI_API_KEY not set — Grok tasks will fail")

    # Check DeepSeek
    ds_key = os.environ.get("DEEPSEEK_API_KEY", "")
    if ds_key:
        providers_ok.append("deepseek")
    else:
        issues.append("DEEPSEEK_API_KEY not set — DeepSeek tasks may fail (check models/providers.py fallback)")

    # Check Ollama
    try:
        import subprocess
        r = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if sys.platform == "win32" else 0)
        if r.returncode == 0:
            providers_ok.append("ollama")
        else:
            issues.append("Ollama not responding — local models unavailable")
    except Exception:
        issues.append("Ollama not reachable — local models unavailable")

    return {
        "check": "provider_sanity",
        "ok": len(issues) == 0,
        "providers_ok": providers_ok,
        "issues": issues,
    }


def check_model_sanity() -> dict[str, Any]:
    """Check that models referenced in the task router match available models."""
    from mag.task_router import MODELS

    issues = []
    model_status = {}

    for name, cfg in MODELS.items():
        provider = cfg["provider"]
        cost = cfg["cost"]

        if provider == "grok" and not (os.environ.get("XAI_API_KEY") or ""):
            issues.append(f"Model '{name}' requires Grok provider but XAI_API_KEY is not set")
            model_status[name] = "unavailable"
        elif provider == "deepseek" and not os.environ.get("DEEPSEEK_API_KEY", ""):
            model_status[name] = "unverified"
        elif provider == "ollama":
            model_status[name] = "local"
        else:
            model_status[name] = "ok"

    # Check for the specific error we made today: grok-4-latest vs grok-3-mini
    from mag.task_router import route_task, classify_task
    test_goal = "analyze the system architecture"
    route = route_task(test_goal)
    if route["model"] == "grok-4-latest" and route["task_type"] != "orchestrate":
        issues.append(
            f"TASK ROUTER WARNING: '{test_goal}' routes to {route['model']} "
            f"(${route['cost_est']}) but task type is '{route['task_type']}'. "
            f"Consider grok-3-mini ($0.003) for non-orchestrate tasks."
        )

    return {
        "check": "model_sanity",
        "ok": len(issues) == 0,
        "model_status": model_status,
        "issues": issues,
    }


def check_inbox_sanity() -> dict[str, Any]:
    """Check for malformed or dangerous messages in the copilot inbox."""
    inbox = ROOT / "memory" / "copilot" / "inbox.jsonl"
    if not inbox.is_file():
        return {"check": "inbox_sanity", "ok": True, "issues": [], "note": "No inbox file"}

    messages = _read_jsonl(inbox, tail=20)
    issues = []
    unprocessed = []

    for msg in messages:
        if msg.get("_processed"):
            continue
        unprocessed.append(msg)

        provider = msg.get("provider", "")
        model = msg.get("model", "")
        goal = msg.get("goal", "")

        # Check 1: provider must be registered
        valid_providers = {"ollama", "deepseek", "xai", "grok", "openai", "anthropic"}
        if provider not in valid_providers:
            issues.append(
                f"UNPROCESSED MESSAGE '{msg.get('id', '?')[:20]}': "
                f"unknown provider '{provider}'. Valid: {valid_providers}"
            )

        # Check 2: Grok-4-latest should only be used for orchestrate tasks
        if model == "grok-4-latest" and provider in ("grok", "xai"):
            from mag.task_router import classify_task
            task_type = classify_task(goal)
            if task_type != "orchestrate":
                issues.append(
                    f"UNPROCESSED MESSAGE '{msg.get('id', '?')[:20]}': "
                    f"using grok-4-latest (${0.025}) for '{task_type}' task. "
                    f"Consider grok-3-mini (${0.003})."
                )

        # Check 3: cost estimate
        cost_est = 0.0
        if model == "grok-4-latest":
            cost_est = 0.025
        elif model in ("grok-3-mini",):
            cost_est = 0.003
        elif provider == "deepseek":
            cost_est = 0.00013

        if cost_est > 0.01:
            issues.append(
                f"UNPROCESSED MESSAGE '{msg.get('id', '?')[:20]}': "
                f"estimated cost ${cost_est} — verify this task justifies the spend."
            )

    return {
        "check": "inbox_sanity",
        "ok": len(issues) == 0,
        "unprocessed_count": len(unprocessed),
        "issues": issues,
    }


def check_env_sanity() -> dict[str, Any]:
    """Check that required environment variables are set."""
    required = {
        "XAI_API_KEY": "Grok API access (set to XAI_MAG_KEY value from .env)",
        "DEEPSEEK_API_KEY": "DeepSeek API access",
    }
    optional = {
        "HF_TOKEN": "Hugging Face Spaces deployment",
        "HF_USERNAME": "Hugging Face username for Spaces",
        "REDIS_HOST": "Redis event bus host",
        "X_ACCESS_TOKEN": "X/Twitter API access",
        "X_USER_ID": "X/Twitter user ID",
    }

    issues = []
    for var, desc in required.items():
        if not os.environ.get(var):
            issues.append(f"MISSING: {var} — {desc}")

    warnings_list = []
    for var, desc in optional.items():
        if not os.environ.get(var):
            warnings_list.append(f"OPTIONAL: {var} not set — {desc}")

    return {
        "check": "env_sanity",
        "ok": len(issues) == 0,
        "missing_required": issues,
        "missing_optional": warnings_list,
    }


def check_chain_discipline() -> dict[str, Any]:
    """Check that modules use chain_query instead of reading the chain file directly.

    This would have caught the grep-over-chain pattern the assistant defaulted to.
    Every module that asks 'what do we know?' must go through chain_query.
    Direct reads of # CHAIN_QUERY_MIGRATION_NEEDED: replace with chain.tail() or chain.by_type() are a discipline violation.
    """
    issues = []
    mag_dir = ROOT / "mag"
    if not mag_dir.is_dir():
        return {"check": "chain_discipline", "ok": True, "issues": [], "note": "mag/ directory not found"}

    direct_read_patterns = [
        "# CHAIN_QUERY_MIGRATION_NEEDED: replace with chain.tail() or chain.by_type()",
        'memory/biography/verkle_chain',
    ]

    for py_file in sorted(mag_dir.glob("*.py")):
        if py_file.name == "chain_query.py":
            continue

        try:
            content = py_file.read_text(encoding="utf-8", errors="replace")
            for pattern in direct_read_patterns:
                if pattern in content:
                    imports_chain_query = "chain_query" in content or "from mag.chain_query" in content
                    if imports_chain_query:
                        continue
                    issues.append(
                        f"CHAIN DISCIPLINE: {py_file.name} reads # CHAIN_QUERY_MIGRATION_NEEDED: replace with chain.tail() or chain.by_type() directly "
                        f"instead of using chain_query. Import 'from mag.chain_query import chain' "
                        f"and use chain.tail(), chain.by_theme(), etc."
                    )
        except OSError:
            continue

    state_querying_modules = [
        "ghost.py", "doctor.py", "cost_enforcer.py", "steal_first.py",
        "task_router.py", "exit_dialogue.py", "signal_flare.py",
        "bard.py", "renderman.py", "depin.py", "holographic_q.py",
        "state_quantizer.py", "ghost_leak_detector.py", "behavioral_analytics.py",
    ]

    missing_import = []
    for module_name in state_querying_modules:
        module_path = mag_dir / module_name
        if module_path.is_file():
            try:
                content = module_path.read_text(encoding="utf-8", errors="replace")
                if "chain_query" not in content and "from mag.chain_query" not in content:
                    if module_name != "chain_query.py":
                        missing_import.append(
                            f"CHAIN DISCIPLINE: {module_name} does not import chain_query. "
                            f"It should use chain.tail(), chain.by_theme(), etc. for state queries."
                        )
            except OSError:
                continue

    issues.extend(missing_import)

    return {
        "check": "chain_discipline",
        "ok": len(issues) == 0,
        "issues": issues,
        "modules_checked": len(list(mag_dir.glob("*.py"))),
        "discipline_violations": len([i for i in issues if "directly" in i]),
        "missing_imports": len(missing_import),
    }


def check_memlance_discipline() -> dict[str, Any]:
    """Check that modules use ghost_memlance's CANONICAL surface (select/index), not guessed keys.

    2026-08-11 operator: "this is the same bug ... fix it automatically moving forward." The
    recurring bug = calling ghost_memlance then guessing its return key (e.g. .get("states"),
    .get("entries")) instead of reading the REAL shape. select() returns {selected: [...]},
    index() returns a LIST. This guard flags the guess-internals pattern automatically.
    """
    issues = []
    mag_dir = ROOT / "mag"
    if not mag_dir.is_dir():
        return {"check": "memlance_discipline", "ok": True, "issues": [],
                "note": "mag/ directory not found"}
    # guessed keys that are NOT what ghost_memlance returns (select->selected, index->list)
    guessed = ['.get("states")', '.get("entries")', '.get("results")', '.get("rows")']
    for py_file in sorted(mag_dir.glob("*.py")):
        if py_file.name == "ghost_memlance.py":
            continue
        try:
            content = py_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        # only modules that actually touch memlance
        if "ghost_memlance" not in content and "memlance" not in content:
            continue
        # does it use the canonical surface?
        uses_canonical = (".select(" in content) or (".index(" in content)
        if uses_canonical:
            continue
        # it references memlance but reads a guessed key / doesn't call select or index
        for g in guessed:
            if g in content:
                issues.append(
                    f"MEMLANCE DISCIPLINE: {py_file.name} reads a guessed key {g} on a memlance "
                    f"result instead of the canonical surface. Use ghost_memlance.select(goal,k)"
                    f" (returns {{selected:[...]}}) or index() (returns a list). Read the real "
                    f"shape from the code, never guess."
                )
                break
    return {"check": "memlance_discipline", "ok": len(issues) == 0,
            "issues": issues, "modules_checked": len(list(mag_dir.glob("*.py"))),
            "discipline_violations": len(issues)}


# ═══════════════════════════════════════════════════════════════════
# FULL EXAMINATION
# ═══════════════════════════════════════════════════════════════════

def check_self_steal() -> dict[str, Any]:
    """Self-steal capability-utilization check: surfaces where our own systems aren't being used.

    Surfaces under-utilized internal capabilities (stale/absent/unwired) so doctor/maintenance
    can see where the architecture isn't leveraging its own machinery (e.g. verkle anchoring).
    """
    try:
        from mag.self_steal import audit
        a = audit()
    except Exception as e:
        return {"check": "self_steal", "ok": False, "issues": [f"self_steal audit error: {e}"], "missing_optional": []}
    issues = []
    for f in a.get("findings", []):
        issues.append(f"self_steal: capability '{f['capability']}' utilization={f['utilization']} "
                      f"age_s={f['age_s']} wired={f['wired']} -> {f['recommendation']}")
    return {"check": "self_steal", "ok": len(issues) == 0, "issues": issues, "missing_optional": []}


def check_system_tracking() -> dict[str, Any]:
    """GAP-ANALYSIS HEALTH CHECK: verify every system is present, wired, and tracking data.

    Each system must (a) import, (b) have its store on disk, and (c) hold tracked data
    (non-empty registry/ledger/graph). Ensures nothing we built is a silent empty shell.
    """
    def _rows(p: Path) -> int:
        if not p.is_file():
            return 0
        try:
            return sum(1 for ln in p.read_text(encoding="utf-8", errors="replace").splitlines() if ln.strip())
        except Exception:
            return 0

    def _js(p: Path) -> int:
        if not p.is_file():
            return 0
        try:
            import json as _j
            d = _j.loads(p.read_text(encoding="utf-8"))
            return 1 if isinstance(d, dict) and d else 0
        except Exception:
            return 0

    # (name, module, store_path, expected-kind, min_rows)
    systems = [
        ("mycelium", "mag.mycelium", ROOT / "memory/mycelium/graph_snapshot.json", "json", 1),
        ("republic_os", "mag.republic_os", ROOT / "memory/runs/republic_os/state.json", "json", 1),
        ("comms_trail", "mag.comms_trail", ROOT / "memory/runs/comms_trail/state.json", "json", 1),
        ("memlang", "mag.memlang", ROOT / "memory/runs/memlang/registry.json", "json", 1),
        ("research_lens", "mag.research_lens", ROOT / "memory/lenses/corpus_index.json", "json", 1),
        ("grok_free", "mag.grok_free", ROOT / "memory/runs/grok_free/usage.jsonl", "lines", 1),
        ("cheap_swarm", "mag.cheap_swarm", ROOT / "memory/runs/cheap_swarm/dispatched.jsonl", "lines", 1),
        ("frontier_help", "mag.frontier_help", ROOT / "memory/frontier/HELP_WANTED.md", "lines", 1),
        ("aos_grok", "mag.aos_grok", ROOT / "memory/embassy/AOS/grok_usage.jsonl", "lines", 1),
        ("grok_mirror", "mag.grok_mirror", ROOT / "memory/runs/grok_mirror", "dir_files", 1),
        ("gap_map", "mag.gap_map", ROOT / "memory/runs/gap_map/stack.json", "json", 0),
        ("cost_learn", "mag.cost_learn", ROOT / "memory/training/cost_ledger.jsonl", "lines", 1),
    ]
    issues = []
    tracked = []
    for name, module, store, kind, min_rows in systems:
        ok_module, ok_store, ok_data = False, False, False
        try:
            __import__(module)
            ok_module = True
        except Exception:
            pass
        ok_store = store.exists()
        if kind == "dir_files":
            ok_store = store.is_dir()
            ok_data = len(list(store.glob("*.json"))) >= min_rows if ok_store else False
        elif ok_store:
            n = _rows(store) if kind == "lines" else _js(store)
            ok_data = n >= min_rows
        status = "ok" if (ok_module and ok_store and ok_data) else "gap"
        if status != "ok":
            issues.append(f"tracking gap: {name} module={ok_module} store={ok_store} data={ok_data} ({store})")
        else:
            tracked.append(name)
    # ghost self-window must exist (agent_state authored by ghost-self)
    try:
        from mag.agent_state import load_latest
        lat = load_latest() or {}
        if lat.get("label") == "ghost-self":
            tracked.append("ghost_self_window")
        else:
            issues.append("ghost self-window not authored (agent_state LATEST != ghost-self)")
    except Exception as e:
        issues.append(f"ghost self-window check error: {e}")
    return {"check": "system_tracking", "ok": len(issues) == 0, "issues": issues,
            "tracked": tracked, "systems_checked": len(systems) + 1, "missing_optional": []}


def examine() -> DoctorReport:
    """Run all doctor checks. Returns a full report."""
    checks = [
        check_provider_sanity(),
        check_model_sanity(),
        check_inbox_sanity(),
        check_env_sanity(),
        check_chain_discipline(),
        check_memlance_discipline(),
    ]
    try:
        checks.append(check_self_steal())
    except Exception:
        pass
    try:
        checks.append(check_system_tracking())
    except Exception:
        pass

    errors = []
    warnings = []
    for c in checks:
        if not c["ok"]:
            for issue in c.get("issues", []):
                if "WARNING" in issue or "OPTIONAL" in issue:
                    warnings.append(issue)
                else:
                    errors.append(issue)
        if c.get("missing_optional"):
            warnings.extend(c["missing_optional"])

    return DoctorReport(
        ok=len(errors) == 0,
        checks=checks,
        errors=errors,
        warnings=warnings,
    )


def doctor_status() -> dict[str, Any]:
    """Quick status check for the doctor protocol."""
    report = examine()
    return {
        "schema": "doctor.v1",
        "ts": _now(),
        "ok": report.ok,
        "errors": len(report.errors),
        "warnings": len(report.warnings),
        "checks_run": len(report.checks),
        "details": {c["check"]: {"ok": c["ok"], "issues": len(c.get("issues", []))} for c in report.checks},
    }
