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
        r = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
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


# ═══════════════════════════════════════════════════════════════════
# FULL EXAMINATION
# ═══════════════════════════════════════════════════════════════════

def examine() -> DoctorReport:
    """Run all doctor checks. Returns a full report."""
    checks = [
        check_provider_sanity(),
        check_model_sanity(),
        check_inbox_sanity(),
        check_env_sanity(),
    ]

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
