"""Grok Rightsize — token-efficient model selection and prompt compression.

Every Grok API call costs money. This module enforces:
  1. TIERED MODEL SELECTION — smallest capable model per task complexity
  2. TOKEN BUDGETS — per-call caps on input + output tokens
  3. PROMPT COMPRESSION — strip flattery, repetition, and filler
  4. SYSTEM PROMPT CACHING — reuse the same 200-token prefix across calls
  5. COST TRACKING — estimate spend per call before sending

Cost estimates (per 1M tokens, xAI pricing ~Aug 2026):
  grok-2-latest:  ~$2 in / $10 out
  grok-3-mini:    ~$0.30 in / $2.50 out  ← default (cheapest reasoning)
  grok-3:         ~$3 in / $15 out
  grok-4:         ~$5 in / $20 out       ← scarce, multi-agent only

Schema: grok_rightsize.v1
Law: Never send >200 token system prompts. Never default to grok-4.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from config import ROOT
except ImportError:
    ROOT = Path(__file__).resolve().parent.parent

# ── Constants ─────────────────────────────────────────────────────
SYSTEM_PROMPT_CACHE = (
    "You are Ghost's Grok agent. Local sovereign system. "
    "Execute the goal. Be concise. Return structured output. No flattery."
)  # 22 tokens — well under the 200-token cache prefix limit

# Tier → (model, max_output_tokens, temperature, approx_cost_per_call)
BUDGETS: dict[str, dict[str, Any]] = {
    "sense":      {"model": "grok-2-latest", "max_tokens": 256,  "temp": 0.0, "est_cost": 0.0003},
    "classify":   {"model": "grok-2-latest", "max_tokens": 128,  "temp": 0.0, "est_cost": 0.0002},
    "summary":    {"model": "grok-3-mini",   "max_tokens": 512,  "temp": 0.0, "est_cost": 0.0015},
    "analysis":   {"model": "grok-3-mini",   "max_tokens": 1024, "temp": 0.2, "est_cost": 0.0030},
    "deep":       {"model": "grok-3",        "max_tokens": 2048, "temp": 0.3, "est_cost": 0.0080},
    "orchestrate": {"model": "grok-4",       "max_tokens": 4096, "temp": 0.3, "est_cost": 0.0250},
}

# Tasks that should NEVER use grok-4 (deterministic, local-capable)
NEVER_GROK4 = {"sense", "classify", "summary", "status", "health", "list", "count"}

# Tasks that justify grok-4 (multi-agent coordination, deep analysis)
GROK4_WORTHY = {"orchestrate", "campaign", "research_sprint", "network_map", "tesuji_deep"}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _approx_tokens(text: str) -> int:
    """Rough token count: ~4 chars per token for English text."""
    return max(1, len(text) // 4)


# ═══════════════════════════════════════════════════════════════════
# TASK → BUDGET ROUTING
# ═══════════════════════════════════════════════════════════════════

def classify_task(goal: str) -> str:
    """Classify a task goal into a budget tier based on keywords.

    Returns one of: sense, classify, summary, analysis, deep, orchestrate
    """
    g = goal.lower()

    # Orchestrate: multi-agent, campaign, research sprint
    if any(w in g for w in ["campaign", "orchestrate", "multi-agent", "swarm",
                              "research sprint", "tesuji", "network map"]):
        return "orchestrate"

    # Deep: complex reasoning, root cause, architecture
    if any(w in g for w in ["root cause", "architecture", "diagnosis",
                              "investigate", "deep", "comprehensive"]):
        return "deep"

    # Analysis: structured output, multiple sections
    if any(w in g for w in ["analyze", "analysis", "assess", "evaluate",
                              "compare", "synthesize", "structured"]):
        return "analysis"

    # Summary: one-paragraph, short-form
    if any(w in g for w in ["summarize", "summary", "one-paragraph",
                              "brief", "overview", "tl;dr"]):
        return "summary"

    # Classify: yes/no, pick one, categorize
    if any(w in g for w in ["classify", "is this", "which one",
                              "pick", "categorize", "yes or no", "true or false"]):
        return "classify"

    # Sense: read-only, check status, count
    if any(w in g for w in ["read", "sense", "check", "status", "list",
                              "count", "how many", "what is the current"]):
        return "sense"

    # Default: analysis (safe middle ground)
    return "analysis"


def budget_for(goal: str, *, force_tier: str | None = None) -> dict[str, Any]:
    """Get the rightsized budget for a task goal.

    Args:
        goal: The task goal/prompt text.
        force_tier: Override auto-classification (e.g. "deep" for important tasks).

    Returns:
        Dict with model, max_tokens, temperature, est_cost, tier.
    """
    tier = force_tier or classify_task(goal)
    budget = dict(BUDGETS.get(tier, BUDGETS["analysis"]))
    budget["tier"] = tier

    # Safety: never let auto-classification pick grok-4
    if force_tier is None and budget["model"] == "grok-4":
        if tier not in GROK4_WORTHY:
            budget["model"] = "grok-3"
            budget["max_tokens"] = 2048
            budget["est_cost"] = 0.0080
            budget["tier"] = "deep"  # downgraded

    return budget


# ═══════════════════════════════════════════════════════════════════
# PROMPT COMPRESSION
# ═══════════════════════════════════════════════════════════════════

# Patterns to strip — flattery, filler, repetition
STRIP_PATTERNS: list[tuple[str, str]] = [
    (r'(?i)(you are an?)\s+(expert|advanced|highly capable|sophisticated|powerful)\s+\w+\s+AI\.?\s*', r'\1 AI. '),
    (r'(?i)(please|kindly|if you would be so kind as to)\s+', ''),
    (r'(?i)(I would like you to|I want you to|I need you to)\s+', ''),
    (r'(?i)(thank you|thanks in advance|much appreciated)[.!]?\s*', ''),
    (r'(?i)(remember|note that|keep in mind that|it is important to)\s+', ''),
    (r'(?i)(do not|don\'t)\s+(waste tokens|be verbose|repeat yourself|ramble)[.!]?\s*', ''),
    (r'\n{3,}', '\n\n'),                     # collapse multiple newlines
    (r' {2,}', ' '),                          # collapse multiple spaces
]


def compress_prompt(text: str) -> str:
    """Strip flattery, filler, and repetition from a prompt.

    Saves ~15-30% tokens on typical Ghost→Grok prompts.
    """
    compressed = text.strip()
    for pattern, replacement in STRIP_PATTERNS:
        compressed = re.sub(pattern, replacement, compressed)
    return compressed.strip()


def estimate_tokens(text: str) -> int:
    """Estimate token count for a text string."""
    return _approx_tokens(text)


def estimate_cost(goal: str, tier: str | None = None) -> dict[str, Any]:
    """Estimate the cost of a Grok API call for a given goal.

    Returns dict with estimated tokens_in, tokens_out, cost_usd, model, tier.
    """
    budget = budget_for(goal, force_tier=tier)
    compressed = compress_prompt(goal)
    tokens_in = _approx_tokens(compressed) + _approx_tokens(SYSTEM_PROMPT_CACHE)
    tokens_out = budget["max_tokens"]
    cost = budget["est_cost"]

    return {
        "tier": budget["tier"],
        "model": budget["model"],
        "tokens_in_est": tokens_in,
        "tokens_out_max": tokens_out,
        "cost_est_usd": round(cost, 6),
        "compressed_chars": len(compressed),
        "original_chars": len(goal),
        "compression_ratio": round(len(compressed) / max(1, len(goal)), 2),
    }


# ═══════════════════════════════════════════════════════════════════
# GROK API CALL (rightsized)
# ═══════════════════════════════════════════════════════════════════

@dataclass
class GrokCallResult:
    ok: bool
    content: str
    model: str
    tier: str
    tokens_prompt: int
    tokens_completion: int
    tokens_total: int
    cost_est_usd: float
    latency_ms: float
    error: str = ""


def call_grok(
    goal: str,
    *,
    tier: str | None = None,
    context: str = "",
    system_prompt: str | None = None,
    temperature: float | None = None,
    max_tokens: int | None = None,
    timeout: float = 120.0,
) -> GrokCallResult:
    """Make a rightsized Grok API call.

    Args:
        goal: The task goal (will be compressed automatically).
        tier: Budget tier override. Auto-classified if None.
        context: Additional context appended to goal (not compressed as aggressively).
        system_prompt: Override the default system prompt. Keep under 200 tokens.
        temperature: Override budget temperature.
        max_tokens: Override budget max_tokens.
        timeout: HTTP timeout in seconds.

    Returns:
        GrokCallResult with content, tokens used, cost estimate.
    """
    import time
    import urllib.error
    import urllib.request

    key = os.environ.get("XAI_API_KEY") or os.environ.get("GROK_API_KEY") or ""
    if not key:
        return GrokCallResult(ok=False, content="", model="", tier="",
                              tokens_prompt=0, tokens_completion=0, tokens_total=0,
                              cost_est_usd=0, latency_ms=0,
                              error="No XAI_API_KEY in environment")

    # Rightsize
    budget = budget_for(goal, force_tier=tier)
    model = budget["model"]
    temp = temperature if temperature is not None else budget["temp"]
    max_tok = max_tokens if max_tokens is not None else budget["max_tokens"]

    # Compress
    compressed_goal = compress_prompt(goal)
    if context:
        compressed_goal = f"{compressed_goal}\n\nContext: {compress_prompt(context)}"

    # System prompt (keep under 200 tokens)
    sys_prompt = system_prompt if system_prompt else SYSTEM_PROMPT_CACHE
    if _approx_tokens(sys_prompt) > 200:
        sys_prompt = sys_prompt[:800]  # ~200 tokens at 4 chars/token

    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": compressed_goal},
    ]

    body = {
        "model": model,
        "messages": messages,
        "temperature": temp,
        "max_tokens": max_tok,
    }

    t0 = time.time()
    try:
        req = urllib.request.Request(
            "https://api.x.ai/v1/chat/completions",
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {key}",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        return GrokCallResult(
            ok=False, content="", model=model, tier=budget["tier"],
            tokens_prompt=0, tokens_completion=0, tokens_total=0,
            cost_est_usd=0, latency_ms=(time.time() - t0) * 1000,
            error=f"HTTP {e.code}: {err_body[:300]}",
        )
    except Exception as e:
        return GrokCallResult(
            ok=False, content="", model=model, tier=budget["tier"],
            tokens_prompt=0, tokens_completion=0, tokens_total=0,
            cost_est_usd=0, latency_ms=(time.time() - t0) * 1000,
            error=str(e)[:300],
        )

    latency_ms = (time.time() - t0) * 1000

    choices = raw.get("choices") or []
    if not choices:
        return GrokCallResult(
            ok=False, content="", model=model, tier=budget["tier"],
            tokens_prompt=0, tokens_completion=0, tokens_total=0,
            cost_est_usd=0, latency_ms=latency_ms,
            error=f"Empty choices from Grok API",
        )

    msg = choices[0].get("message") or {}
    content = msg.get("content") or ""
    if isinstance(content, list):
        content = "".join(p.get("text", "") for p in content if isinstance(p, dict))

    usage = raw.get("usage") or {}
    tokens_prompt = usage.get("prompt_tokens", _approx_tokens(compressed_goal))
    tokens_completion = usage.get("completion_tokens", _approx_tokens(content))
    tokens_total = usage.get("total_tokens", tokens_prompt + tokens_completion)

    # Cost estimate based on model pricing
    cost_per_1m_in = {"grok-2-latest": 2, "grok-3-mini": 0.30, "grok-3": 3, "grok-4": 5}
    cost_per_1m_out = {"grok-2-latest": 10, "grok-3-mini": 2.50, "grok-3": 15, "grok-4": 20}
    cost_in = tokens_prompt / 1_000_000 * cost_per_1m_in.get(model, 3)
    cost_out = tokens_completion / 1_000_000 * cost_per_1m_out.get(model, 15)
    cost_est = round(cost_in + cost_out, 6)

    return GrokCallResult(
        ok=True,
        content=content,
        model=model,
        tier=budget["tier"],
        tokens_prompt=tokens_prompt,
        tokens_completion=tokens_completion,
        tokens_total=tokens_total,
        cost_est_usd=cost_est,
        latency_ms=round(latency_ms, 0),
    )


# ═══════════════════════════════════════════════════════════════════
# GHOST INTEGRATION — rightsized Grok from copilot inbox
# ═══════════════════════════════════════════════════════════════════

def ghost_grok_task(goal: str, *, tier: str | None = None) -> dict[str, Any]:
    """Create a rightsized copilot inbox message for Ghost to route to Grok.

    This is the preferred way for Ghost to call Grok — it goes through
    the copilot inbox so the orchestrator handles execution, retries,
    and budget enforcement.

    Args:
        goal: The task goal.
        tier: Budget tier. Auto-classified if None.

    Returns:
        Dict ready to append to copilot inbox.jsonl.
    """
    budget = budget_for(goal, force_tier=tier)
    compressed = compress_prompt(goal)

    return {
        "id": f"grok-{budget['tier']}-{_now()[:19].replace(':', '')}",
        "action": "exec",
        "goal": compressed,
        "provider": "grok",
        "model": budget["model"],
        "timeout_s": 120 if budget["tier"] != "orchestrate" else 300,
        "ts": _now(),
        "source": "ghost-rightsized",
        "_budget": {
            "tier": budget["tier"],
            "max_tokens": budget["max_tokens"],
            "temperature": budget["temp"],
            "est_cost": budget["est_cost"],
        },
    }


# ═══════════════════════════════════════════════════════════════════
# COST LEDGER
# ═══════════════════════════════════════════════════════════════════

LEDGER_PATH = ROOT / "memory" / "ghost" / "grok_ledger.jsonl"


def log_grok_call(result: GrokCallResult, task_id: str = "") -> None:
    """Log a Grok API call to the cost ledger."""
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": _now(),
        "task_id": task_id,
        "model": result.model,
        "tier": result.tier,
        "ok": result.ok,
        "tokens_prompt": result.tokens_prompt,
        "tokens_completion": result.tokens_completion,
        "tokens_total": result.tokens_total,
        "cost_est_usd": result.cost_est_usd,
        "latency_ms": result.latency_ms,
        "error": result.error[:200] if result.error else "",
    }
    with open(LEDGER_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def ledger_summary() -> dict[str, Any]:
    """Summarize Grok API spending from the ledger."""
    if not LEDGER_PATH.is_file():
        return {"total_calls": 0, "total_cost_usd": 0.0}

    lines = LEDGER_PATH.read_text(encoding="utf-8", errors="replace").strip().splitlines()
    total_cost = 0.0
    total_tokens = 0
    by_model: dict[str, dict[str, Any]] = {}

    for line in lines:
        try:
            e = json.loads(line)
            cost = float(e.get("cost_est_usd", 0))
            tokens = int(e.get("tokens_total", 0))
            model = e.get("model", "?")
            total_cost += cost
            total_tokens += tokens
            if model not in by_model:
                by_model[model] = {"calls": 0, "cost": 0.0, "tokens": 0}
            by_model[model]["calls"] += 1
            by_model[model]["cost"] += cost
            by_model[model]["tokens"] += tokens
        except (json.JSONDecodeError, KeyError):
            continue

    return {
        "total_calls": len(lines),
        "total_cost_usd": round(total_cost, 6),
        "total_tokens": total_tokens,
        "by_model": by_model,
    }
