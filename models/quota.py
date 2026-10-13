"""Per-provider usage + remaining-until-reset tracking.

Platforms rarely expose free-tier remainder via API. We:
  1. Record every remote/local call (calls + estimated tokens)
  2. Apply user-set period limits from providers.yaml
  3. Expose remaining for the router

Reset periods: daily (UTC midnight), monthly (reset_day), none (unlimited).
"""
from __future__ import annotations

import json
import os
from calendar import monthrange
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from config import ROOT

STATE_PATH = ROOT / "logs" / "quota_state.json"
USAGE_DETAIL = ROOT / "logs" / "provider_usage.jsonl"
# (provider, period_start, period_end, mtime_ns, size) -> (billable_tokens, calls)
_BILLABLE_CACHE: dict[tuple, tuple[int, int]] = {}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _period_bounds(period: str, reset_day: int = 1, now: datetime | None = None) -> tuple[datetime, datetime]:
    now = now or _now()
    period = (period or "monthly").lower()
    if period in ("none", "unlimited", ""):
        # far future
        return now - timedelta(days=3650), now + timedelta(days=3650)
    if period == "daily":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        return start, end
    # monthly
    rd = max(1, min(28, int(reset_day or 1)))
    if now.day >= rd:
        start = now.replace(day=rd, hour=0, minute=0, second=0, microsecond=0)
        # next month
        if now.month == 12:
            end = now.replace(year=now.year + 1, month=1, day=rd, hour=0, minute=0, second=0, microsecond=0)
        else:
            end = now.replace(month=now.month + 1, day=rd, hour=0, minute=0, second=0, microsecond=0)
    else:
        # period started last month
        if now.month == 1:
            start = now.replace(year=now.year - 1, month=12, day=rd, hour=0, minute=0, second=0, microsecond=0)
        else:
            start = now.replace(month=now.month - 1, day=rd, hour=0, minute=0, second=0, microsecond=0)
        end = now.replace(day=rd, hour=0, minute=0, second=0, microsecond=0)
    return start, end


def _load_state() -> dict[str, Any]:
    if not STATE_PATH.is_file():
        return {"providers": {}, "updated": None}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"providers": {}, "updated": None}


def _save_state(state: dict[str, Any]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    state["updated"] = _now().isoformat()
    STATE_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")


def record_usage(
    provider_id: str,
    *,
    model: str = "",
    calls: int = 1,
    prompt_tokens: int = 0,
    completion_tokens: int = 0,
    cache_hit_tokens: int = 0,
    cache_miss_tokens: int = 0,
    ok: bool = True,
    session_id: str = "",
    latency_ms: int = 0,
    meta: dict | None = None,
) -> None:
    # Billable tokens: count only cache MISS + completion against quota caps.
    # Cache HIT tokens cost ~$0.0028/M (near free) vs $0.14/M miss — counting
    # hits as full spend tripped the daily cap at 00:25 on ~96%-hit traffic
    # and falsely blocked the whole research lane (quota_state 1,009,217 tok
    # on the moonshot run = cache hits, not real cost). The guardrail must
    # measure dollars, and hit tokens are ~0 dollars. Safe default: when no
    # cache split is provided, count the full prompt as billable (miss=prompt).
    has_split = bool(cache_hit_tokens) or bool(cache_miss_tokens)
    if has_split:
        total_tok = int(cache_miss_tokens or 0) + int(completion_tokens or 0)
    else:
        total_tok = int(prompt_tokens or 0) + int(completion_tokens or 0)
    # estimate if missing
    if total_tok <= 0 and meta and meta.get("chars"):
        total_tok = max(1, int(meta["chars"]) // 4)
    # If only prompt_tokens is given but no cache split, default miss=prompt (safe).
    if not cache_hit_tokens and not cache_miss_tokens:
        cache_miss_tokens = int(prompt_tokens or 0)

    state = _load_state()
    prov = state.setdefault("providers", {}).setdefault(
        provider_id,
        {"calls": 0, "tokens": 0, "period_start": None, "period_end": None},
    )
    # roll period if needed — bounds stored as iso
    from models.providers import get_provider

    pcfg = get_provider(provider_id) or {}
    q = pcfg.get("quota") or {}
    period = str(q.get("period") or "monthly")
    start, end = _period_bounds(period, int(q.get("reset_day") or 1))
    ps = prov.get("period_start")
    # "none"/unlimited: never roll counters on sliding window
    if period not in ("none", "unlimited", ""):
        roll = False
        if not ps:
            roll = True
        else:
            try:
                ps_dt = datetime.fromisoformat(str(ps).replace("Z", "+00:00"))
                if ps_dt < start:
                    roll = True
            except ValueError:
                roll = True
        if roll:
            prov["calls"] = 0
            prov["tokens"] = 0
            prov["period_start"] = start.isoformat()
            prov["period_end"] = end.isoformat()
    else:
        prov.setdefault("period_start", start.isoformat())
        prov.setdefault("period_end", end.isoformat())
    prov["calls"] = int(prov.get("calls") or 0) + calls
    prov["tokens"] = int(prov.get("tokens") or 0) + total_tok
    prov["last_model"] = model
    prov["last_ok"] = ok
    prov["last_ts"] = _now().isoformat()
    _save_state(state)

    USAGE_DETAIL.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "ts": _now().isoformat(),
        "provider": provider_id,
        "model": model,
        "calls": calls,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "cache_hit_tokens": int(cache_hit_tokens or 0),
        "cache_miss_tokens": int(cache_miss_tokens or 0),
        "session_id": (session_id or (meta or {}).get("session_id") or ""),
        "latency_ms": int(latency_ms or 0),
        "tokens": total_tok,
        "ok": ok,
        "meta": meta or {},
    }
    with USAGE_DETAIL.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, default=str) + "\n")

    _BILLABLE_CACHE.clear()
    try:
        from mag.lanes import log_usage

        log_usage(
            lane="L1" if provider_id != "ollama" else "L0",
            action="provider_chat",
            detail=f"{provider_id}:{model}",
            ok=ok,
            meta=row,
        )
    except Exception:
        pass


def _row_billable_tokens(row: dict[str, Any]) -> int:
    """Billable tokens for one usage row: cache MISS + completion.

    Cache hits are near-free and must not trip the Mag cap. Rows without a
    hit/miss split fall back to the recorded tokens field (legacy).
    """
    hits = int(row.get("cache_hit_tokens") or 0)
    miss = int(row.get("cache_miss_tokens") or 0)
    comp = int(row.get("completion_tokens") or 0)
    if hits or miss:
        return max(0, miss) + max(0, comp)
    return int(row.get("tokens") or 0) or (
        int(row.get("prompt_tokens") or 0) + max(0, comp)
    )


def period_billable(provider_id: str, start: datetime, end: datetime) -> dict[str, Any] | None:
    """Sum billable spend for a provider in [start, end) from usage jsonl."""
    if not USAGE_DETAIL.is_file():
        return None
    try:
        st = USAGE_DETAIL.stat()
        key = (provider_id, start.isoformat(), end.isoformat(), st.st_mtime_ns, st.st_size)
    except OSError:
        return None
    cached = _BILLABLE_CACHE.get(key)
    if cached is not None:
        return {"tokens": cached[0], "calls": cached[1], "source": "usage_billable"}
    billable = calls = 0
    try:
        with USAGE_DETAIL.open(encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if row.get("provider") != provider_id:
                    continue
                ts = row.get("ts")
                if not ts:
                    continue
                try:
                    dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
                except ValueError:
                    continue
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                if dt < start or dt >= end:
                    continue
                calls += int(row.get("calls") or 1)
                billable += _row_billable_tokens(row)
    except OSError:
        return None
    _BILLABLE_CACHE.clear()
    _BILLABLE_CACHE[key] = (billable, calls)
    return {"tokens": billable, "calls": calls, "source": "usage_billable"}


def provider_budget(provider_id: str) -> dict[str, Any]:
    from models.providers import get_provider

    pcfg = get_provider(provider_id) or {}
    q = pcfg.get("quota") or {}
    period = str(q.get("period") or "monthly")
    start, end = _period_bounds(period, int(q.get("reset_day") or 1))
    state = _load_state()
    prov = (state.get("providers") or {}).get(provider_id) or {}
    # roll display counters only for finite periods
    if period not in ("none", "unlimited", ""):
        ps = prov.get("period_start")
        if ps:
            try:
                ps_dt = datetime.fromisoformat(str(ps).replace("Z", "+00:00"))
                if ps_dt < start:
                    prov = {"calls": 0, "tokens": 0}
            except ValueError:
                pass
    ledger_c = int(prov.get("calls") or 0)
    ledger_t = int(prov.get("tokens") or 0)
    # Constraint: Mag period cap in providers.yaml. Check billable spend
    # (usage jsonl), not the dirty quota_state token total that mixed cache hits.
    billed = period_billable(provider_id, start, end)
    if billed is not None:
        used_c = int(billed["calls"])
        used_t = int(billed["tokens"])
        usage_source = "usage_billable"
    else:
        used_c, used_t = ledger_c, ledger_t
        usage_source = "quota_state"
    max_c = q.get("max_calls")
    max_t = q.get("max_tokens")
    unlimited = period in ("none", "unlimited") or (max_c is None and max_t is None)

    rem_c = None if max_c is None else max(0, int(max_c) - used_c)
    rem_t = None if max_t is None else max(0, int(max_t) - used_t)
    ok = True
    if not unlimited:
        if rem_c is not None and rem_c <= 0:
            ok = False
        if rem_t is not None and rem_t <= 0:
            ok = False

    seconds_left = max(0, int((end - _now()).total_seconds()))
    return {
        "provider": provider_id,
        "name": pcfg.get("name") or provider_id,
        "period": period,
        "period_start": start.isoformat(),
        "period_end": end.isoformat(),
        "seconds_until_reset": seconds_left,
        "reset_in_hours": round(seconds_left / 3600, 1),
        "used_calls": used_c,
        "used_tokens": used_t,
        "ledger_calls": ledger_c,
        "ledger_tokens": ledger_t,
        "usage_source": usage_source,
        "max_calls": max_c,
        "max_tokens": max_t,
        "remaining_calls": rem_c,
        "remaining_tokens": rem_t,
        "budget_ok": ok or unlimited,
        "unlimited": unlimited,
        "configured": _provider_configured(provider_id, pcfg),
        "note": q.get("note") or "",
    }


def _provider_configured(pid: str, pcfg: dict) -> bool:
    if pcfg.get("free_local"):
        return True
    env = pcfg.get("api_key_env")
    if not env:
        return bool(pcfg.get("api_key_default"))
    import os

    keys = [env]
    if env == "OPENROUTER_API_KEY":
        keys.append("OR_API_KEY")
    if env == "GEMINI_API_KEY":
        keys.append("GOOGLE_API_KEY")
    return any(os.environ.get(k) for k in keys)


def all_budgets() -> dict[str, Any]:
    from models.providers import list_provider_ids

    rows = [provider_budget(pid) for pid in list_provider_ids()]
    return {
        "ok": True,
        "ts": _now().isoformat(),
        "providers": rows,
        "routing_hint": "Prefer providers with budget_ok and configured; ollama first for private.",
    }


def remote_provider_policy() -> dict[str, Any]:
    """Runtime policy for remote provider default lock behavior."""
    disable_raw = str(os.environ.get("MAG_DISABLE_REMOTE_PROVIDER_LOCK", "") or "").strip().lower()
    disabled = disable_raw in ("1", "true", "yes")
    lock_raw = str(os.environ.get("MAG_REMOTE_PROVIDER_LOCK", "deepseek") or "").strip().lower()
    lock = "" if disabled else lock_raw
    return {
        "schema": "remote_provider_policy.v1",
        "enabled": bool(lock),
        "lock_provider": lock or None,
        "default_lock_provider": "deepseek",
        "disable_env": "MAG_DISABLE_REMOTE_PROVIDER_LOCK",
        "lock_env": "MAG_REMOTE_PROVIDER_LOCK",
    }


def pick_provider(
    job: str = "default",
    *,
    tier: str = "T2",
    prefer: list[str] | None = None,
) -> dict[str, Any]:
    """Pick first provider with key + budget, respecting tier and job list."""
    from models.providers import get_provider, load_providers, list_provider_ids

    cfg = load_providers()
    never = set((cfg.get("defaults") or {}).get("never_remote_tiers") or ["T0", "T1"])
    order = prefer or (cfg.get("routing") or {}).get(job) or (cfg.get("defaults") or {}).get("prefer_order") or list_provider_ids()

    # Cost guardrail: unless explicitly disabled, keep remote picks on a locked
    # cheap provider so operators do not need to keep forcing it per request.
    policy = remote_provider_policy()
    lock = str(policy.get("lock_provider") or "")
    local_preferred = "ollama" in order
    if lock and tier not in never and not local_preferred:
        ids = set(list_provider_ids())
        if lock in ids:
            order = [lock] + [pid for pid in order if pid != lock]
            # DeepSeek lock gets explicit overmind fallback right after primary.
            if lock == "deepseek" and "deepseek_overmind" in ids and "deepseek_overmind" not in order:
                order.insert(1, "deepseek_overmind")

    candidates = []
    for pid in order:
        p = get_provider(pid)
        if not p:
            continue
        b = provider_budget(pid)
        tier_max = p.get("tier_max") or "T2"
        # B2-204 (2026-09-26): a dormant lane is NEVER pickable, key or no key.
        # Until now the only enforcement was hand-edited routing lists (the
        # B2-61/B2-36 roster purges removed the dead lanes from prefer_order),
        # so anyone re-adding cerebras/nvidia/gemini/mistral/saelis to a
        # routing list would get a 401/404-dead provider handed back as ok.
        # Skip at the seam; doctor already classifies these DORMANT.
        if p.get("dormant"):
            candidates.append({**b, "skip": "dormant", "eligible": False})
            continue
        # private tiers: only free_local
        if tier in never and not p.get("free_local"):
            candidates.append({**b, "skip": "tier_block", "eligible": False})
            continue
        if not b.get("configured"):
            candidates.append({**b, "skip": "no_api_key", "eligible": False})
            continue
        if not b.get("budget_ok"):
            candidates.append({**b, "skip": "quota_exhausted", "eligible": False})
            continue
        # ok
        return {
            "ok": True,
            "provider": pid,
            "model": p.get("default_model"),
            "budget": b,
            "candidates": candidates,
        }
    return {
        "ok": False,
        "error": "no provider with key+budget",
        "candidates": candidates,
        "hint": "Set an API key env var or raise quota in configs/providers.yaml; or use ollama",
    }
