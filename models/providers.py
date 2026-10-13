"""Multi-platform chat via OpenAI-compatible HTTP APIs + Ollama."""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from config import ROOT

_CFG: dict[str, Any] | None = None
_CFG_MTIME: float = 0.0
_PROVIDERS_PATH: Path | None = None


def _cfg_path() -> Path:
    global _PROVIDERS_PATH
    if _PROVIDERS_PATH is None:
        _PROVIDERS_PATH = ROOT / "configs" / "providers.yaml"
    return _PROVIDERS_PATH


def _cfg_stale() -> bool:
    """True when providers.yaml changed on disk since we cached it.

    Lets a long-running process (dashboard/gateway) pick up .env and
    providers.yaml edits WITHOUT a restart — the operator's 'nothing
    displays meaningfully' complaint was partly this stale cache.
    """
    try:
        return _cfg_path().stat().st_mtime_ns != _CFG_MTIME
    except OSError:
        return False


def _iter_sse_events(r):
    """Read SSE events from a streaming HTTP response (robust to chunk boundaries)."""
    buf = b""
    while True:
        chunk = r.read1(8192)
        if not chunk:
            break
        buf += chunk
        while b"\n\n" in buf:
            raw, buf = buf.split(b"\n\n", 1)
            yield raw.decode("utf-8", errors="replace")
    if buf.strip():
        yield buf.decode("utf-8", errors="replace")



def _strip_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if "#" in line:
            q = False
            buf = []
            for ch in line:
                if ch == '"':
                    q = not q
                if ch == "#" and not q:
                    break
                buf.append(ch)
            line = "".join(buf).rstrip()
        if line.strip():
            lines.append(line)
    return "\n".join(lines)


class ProviderConfigError(RuntimeError):
    """providers.yaml is missing or unreadable; the roster cannot be loaded.

    Raised instead of the old silent empty-roster fallback (gala wave5-repair
    config-hygiene lane, 2026-09-29; evidence
    watch/inbox/burn_reset_20260927/flash50/f-03.md finding 5).
    """


def load_providers() -> dict[str, Any]:
    global _CFG, _CFG_MTIME
    if _CFG is not None and not _cfg_stale():
        return _CFG
    try:
        from models.env_load import load_dotenv

        load_dotenv()
    except Exception:
        pass
    path = _cfg_path()
    if not path.is_file():
        # FAIL LOUD (gala wave5-repair config-hygiene lane, 2026-09-29): the
        # old code returned an empty roster here AND on any parse error, so a
        # corrupted providers.yaml read as "zero providers configured" with
        # rc=0 and every lane died later as "unknown provider". providers.yaml
        # is gitignored (disk is the only copy), so a missing file is roster
        # loss; no default roster exists anywhere in the repo to fall back to,
        # the empty map was the failure dressed as a default, so there is NO
        # marked fallback here. Name the file and the recovery path instead.
        raise ProviderConfigError(
            f"providers roster missing: {path} does not exist "
            "(configs/providers.yaml is gitignored; restore it from the "
            "providers.yaml.bak-* beside it or recreate it)"
        )
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(_strip_comments(path.read_text(encoding="utf-8")))
    except Exception as e:
        raise ProviderConfigError(
            f"providers roster unreadable: {path}: {type(e).__name__}: {e}"
        ) from e
    if not isinstance(data, dict):
        raise ProviderConfigError(
            f"providers roster malformed: {path} must parse to a yaml mapping "
            f"(providers:/defaults:/routing:), got {type(data).__name__}"
        )
    data.setdefault("providers", {})
    data.setdefault("defaults", {})
    data.setdefault("routing", {})
    _CFG = data
    try:
        _CFG_MTIME = path.stat().st_mtime_ns
    except OSError:
        _CFG_MTIME = 0
    return _CFG


def reload_providers() -> None:
    global _CFG
    _CFG = None
    load_providers()


def list_provider_ids() -> list[str]:
    return list((load_providers().get("providers") or {}).keys())


def get_provider(provider_id: str) -> dict[str, Any] | None:
    p = (load_providers().get("providers") or {}).get(provider_id)
    return dict(p) if isinstance(p, dict) else None


def _key_env_names(pcfg: dict[str, Any]) -> list[str]:
    """All env var names that may carry a key for this provider.

    Supports a list via ``api_key_envs`` (multi-key chains) or a single
    ``api_key_env`` string, plus the known alias names.
    """
    envs = pcfg.get("api_key_envs")
    env = pcfg.get("api_key_env")
    names: list[str] = []
    if isinstance(envs, list) and envs:
        names = [str(x) for x in envs if x]
    elif env:
        names = [str(env)]
    if env == "OPENROUTER_API_KEY" and "OR_API_KEY" not in names:
        names.append("OR_API_KEY")
    if env == "GEMINI_API_KEY" and "GOOGLE_API_KEY" not in names:
        names.append("GOOGLE_API_KEY")
    return names


def provider_keys(pcfg: dict[str, Any]) -> list[str]:
    """All non-empty key values for a provider (never log/return the values
    outside this module; callers must treat them as secrets)."""
    out: list[str] = []
    for k in _key_env_names(pcfg):
        v = os.environ.get(k)
        if v and str(v).strip():
            out.append(str(v).strip())
    if not out and pcfg.get("api_key_default"):
        out.append(str(pcfg["api_key_default"]))
    return out


def _api_key(pcfg: dict[str, Any]) -> str | None:
    """First usable key (or the free_local default)."""
    keys = provider_keys(pcfg)
    return keys[0] if keys else None


# --- base_url surface policy (B2-445 spec, pinned 2026-09-26) --------------
# OWNER OF THE POLICY: this doc block, next to the only resolution funnel
# (provider_base_url below). The B2-94 mimosa registration accepted 4 of the
# 12 registered claims on the grounds that base_url is operator-owned config
# with no untrusted input; this block is the spec that decision rests on.
#
# Allowed base_url sources (exhaustive):
#   1. configs/providers.yaml `base_url:` (operator hand-edited config).
#   2. the per-provider `base_url_env:` override (e.g. VAST_OPENAI_BASE_URL),
#      read from the process environment at call time. The env value is set
#      by the operator (or the operator's own tooling), never by a caller,
#      never by model output, and never by watch/inbox content.
# Nothing else feeds a request URL: provider ids from callers resolve through
# configs only; model refs, prompts, and receipts never reach URL space.
#
# Scheme policy: https expected for all remote lanes. Non-loopback http is a
# DECLARED NON-GOAL, not an accident: free/local lanes either speak https or
# live on loopback (ollama 127.0.0.1:11434, bionic 127.0.0.1:1234, lm studio),
# where http-in-URL is the local transport, not a downgrade of a remote call.
# No scheme/host allowlist is enforced in code on purpose: a host allowlist
# would break the designed base_url_env override (fresh endpoint probes,
# seat-scoped base URLs, container-vs-host names) that the operator relies on.
#
# Threat model line (why this is registered-not-fixed in the B2-94/B2-445
# mimosa tails): a caller that could smuggle a URL-shaped provider id or an
# attacker-set env var would bypass this policy; both are declared out of
# scope because provider ids come from estate code and configs/lanes.yaml and
# the environment is operator-owned. The falsifier gate lives in
# configs/providers.yaml review: any new caller that passes a URL (not an id)
# into these chat functions re-opens this policy and must amend this block
# BEFORE the code lands (spec-before-behavior law).
def provider_base_url(pcfg: dict[str, Any]) -> str:
    """Resolve base_url, honoring an env override (e.g. VAST_OPENAI_BASE_URL)."""
    env_name = pcfg.get("base_url_env")
    if env_name:
        v = os.environ.get(str(env_name))
        if v and str(v).strip():
            return str(v).strip().rstrip("/")
    return (pcfg.get("base_url") or "").rstrip("/")


def provider_default_model(pcfg: dict[str, Any]) -> str | None:
    """Resolve default_model, honoring a model env override (e.g. VAST_OPENAI_MODEL)."""
    env_name = pcfg.get("model_env")
    if env_name:
        v = os.environ.get(str(env_name))
        if v and str(v).strip():
            return str(v).strip()
    return pcfg.get("default_model")


def _looks_degenerate(text: str) -> bool:
    """True when a model reply is a repetition loop (e.g. ``ƒ"?ƒ"?ƒ"?…``).

    This is the 'hallucinating agent' signature: DeepSeek/gemma occasionally
    lock onto one token and emit it for the whole budget. Treating it as a
    normal answer would file garbage as the workday, so we flag it for retry.
    """
    if not text or not isinstance(text, str):
        return False
    t = text.strip()
    if len(t) < 48:
        return False
    # Same 2-12 char unit repeated >= 20x and covering > 60% of the text.
    for unit_len in (2, 3, 4, 5, 8, 12):
        unit = t[:unit_len]
        if not unit.strip():
            continue
        n = t.count(unit)
        if n >= 20 and len(unit) * n >= len(t) * 0.6:
            return True
    # Single character repeated (also catches long runs of one byte).
    first = t[0]
    if t.count(first) >= 96 and t.count(first) >= len(t) * 0.6:
        return True
    return False


def _thinking_off(pcfg: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    """Top-level ``thinking: {type: disabled}`` for providers that need it.

    DeepSeek v4 defaults thinking ON; reasoning tokens count against
    max_tokens, so small budgets return EMPTY content. Disabling at the top
    level (NOT inside message objects) is ~10-15x cheaper and returns real
    text. Verified live 2026-08-03 (12 tokens vs 120 for 'PONG').
    """
    if pcfg.get("disable_thinking"):
        payload["thinking"] = {"type": "disabled"}
    return payload


# ── B2-62 (2026-09-26): overload backoff + reasoning floor for the z.ai lanes ──
# SPEC: docs/ref/ZAI_API_EXPERT_REFERENCE.md §5.1. MEASURED (B2-04 live probe,
# watch/inbox/burn_wave_20260926/B2_04_probe_results2.json): 429 code 1305
# "temporarily overloaded" hit ~1 in 3 calls at 6s spacing on the funded z.ai
# lanes; one 429 survived a single 15s wait, so the wait STRETCHES per attempt.
OVERLOAD_BASE_S = 15     # the wait the B2-04 probe measured recovering the lane
OVERLOAD_ATTEMPTS = 2    # 15s then 30s, then the paid burst path stays last resort
OVERLOAD_CAP_S = 60      # hard cap on any single wait
# The receipted minimum budget for thinking-on work (EXP-A 08-29, §3 cache doctrine:
# frozen prefix + max_tokens>=1536). B2-04: 2 of 7 burns at 600 ended completion=600,
# content empty because default thinking ate the whole budget.
REASONING_FLOOR = 1536


def _is_overload_body(err: str) -> bool:
    """True when a 429 body names the z.ai overload family (1305/1302/overloaded)."""
    e = (err or "").lower()
    return "1305" in e or "1302" in e or "overloaded" in e


def _thinking_disable_ok(model: str | None) -> bool:
    """glm-5.3 + glm-5.3-flash FORCE thinking (disabled -> 1210 error, §10.1 lived
    scar); 4.7-flash/4.5-flash and the auto-decide family allow it."""
    return "5.3" not in (model or "")


def _apply_reasoning_floor(
    payload: dict[str, Any], *, thinking: bool | None, max_tokens: int, model: str | None
) -> tuple[dict[str, Any], bool]:
    """REASONING FLOOR (spec §5.1 law 2): below the receipted thinking-on minimum
    (1536, EXP-A), UNDECIDED thinking (thinking=None, provider left it on) is
    disabled so the caller's budget serves content instead of being eaten by
    reasoning (B2-04: 2 of 7 burns ended completion=600, content empty). Explicit
    thinking=True keeps the honest empty_reasoning failure; forced-thinking models
    (5.3) are never sent thinking:disabled (1210). Never raises the budget."""
    if thinking is not None or payload.get("thinking"):
        return payload, False
    if max_tokens >= REASONING_FLOOR or not _thinking_disable_ok(model):
        return payload, False
    payload["thinking"] = {"type": "disabled"}
    return payload, True


def status_table() -> dict[str, Any]:
    from models.quota import all_budgets

    rows = []
    for pid in list_provider_ids():
        p = get_provider(pid) or {}
        key = _api_key(p)
        key_envs = _key_env_names(p)
        n_keys = len([k for k in key_envs if os.environ.get(k)])
        rows.append(
            {
                "id": pid,
                "name": p.get("name"),
                "configured": bool(key) or p.get("free_local"),
                "key_env": p.get("api_key_env"),
                "key_envs": key_envs,
                "key_count": max(n_keys, 1 if p.get("free_local") else 0),
                "multi_key": n_keys > 1,
                "default_model": p.get("default_model"),
                "tier_max": p.get("tier_max"),
                "free_local": bool(p.get("free_local")),
            }
        )
    budgets = all_budgets()
    return {
        "ok": True,
        "providers": rows,
        "budgets": budgets.get("providers"),
        "how_to_add_key": (
            "PowerShell: setx OPENROUTER_API_KEY your_key  (new shell after setx). "
            "Same for OPENAI_API_KEY, GROQ_API_KEY, DEEPSEEK_API_KEY, GEMINI_API_KEY, XAI_API_KEY, TOGETHER_API_KEY."
        ),
        "note": "Quota remaining is Mag-tracked from configs/providers.yaml limits, not scraped from vendor dashboards.",
    }


def chat_provider(
    provider_id: str,
    system: str,
    user: str,
    *,
    model: str | None = None,
    temperature: float = 0.2,
    # 08-29 operator order: mine the ceiling by default — the API allows 131072,
    # default 65536. Callers opt DOWN (JSON verbs, probes); never up from crumbs.
    max_tokens: int = 65536,
    tier: str = "T1",
    session_id: str = "",
    thinking: bool | None = None,
    timeout: int | None = None,
    allow_peak: bool = False,
) -> dict[str, Any]:
    """Chat a named provider; records quota usage.

    Callers must explicitly label public remote-safe work T2. The private T1
    default makes omitted classification fail closed for non-local providers.

    ``thinking`` overrides the provider's disable_thinking flag per call:
      None -> respect provider config (default),
      True  -> keep thinking ON (creative/DM turns need coherence),
      False -> force thinking OFF (cheap scut).
    """
    from models.quota import pick_provider, provider_budget, record_usage

    pcfg = get_provider(provider_id)
    if not pcfg:
        return {"ok": False, "error": f"unknown provider {provider_id}"}

    # Coding-plan keys (Lite/Pro/Max) hang on raw /paas/v4 (90s timeout, 1305/1302).
    # They are OpenCode/Claude-Code harness only. Fail fast so the fleet can burst.
    if pcfg.get("opencode_only"):
        return {
            "ok": False,
            "error": "opencode_only: coding-plan key refused on raw /paas/v4 "
                     "(hangs/1305). Use harness.opencode_coder or burst_mill(deepseek).",
            "provider": provider_id,
            "burst_hint": "deepseek",
        }

    # tier gate
    never = set((load_providers().get("defaults") or {}).get("never_remote_tiers") or ["T0", "T1"])
    if tier in never and not pcfg.get("free_local"):
        return {"ok": False, "error": f"refused: tier {tier} cannot use remote {provider_id}"}

    # PEAK GATE (2026-08-24, operator: paid deepseek should land in the cheap window):
    # genuinely PAID providers (paid:true in providers.yaml) defer during DeepSeek peak hours
    # (weekday Beijing 09-12/14-18 = 2x) so paid volume naturally falls in the off-peak window
    # and free lanes carry peak. MAG_ALLOW_PEAK=1 overrides. Never breaks the loop (try/except).
    # Burst-on-timeout (2026-08-28) passes allow_peak=True so a stalled Z.ai mill can fire.
    if pcfg.get("paid") and not allow_peak:
        try:
            from mag.offpeak import defer_if_peak
            d = defer_if_peak()
            if d.get("defer"):
                return {"ok": False, "error": f"deferred_peak: {provider_id} is paid and it is "
                                               f"peak pricing (2x) — off-peak only; MAG_ALLOW_PEAK=1 "
                                               f"overrides (next_offpeak_utc={d.get('next_offpeak_utc')})"}
        except Exception:  # noqa: BLE001 — the guard must never break a call
            pass

    b = provider_budget(provider_id)
    if not b.get("budget_ok"):
        return {
            "ok": False,
            "error": "quota exhausted",
            "budget": b,
            "hint": "Wait for reset or raise max_calls/max_tokens in configs/providers.yaml",
        }

    keys = provider_keys(pcfg)
    if not keys and not pcfg.get("free_local"):
        envs = " / ".join(_key_env_names(pcfg)) or pcfg.get("api_key_env") or "?"
        return {"ok": False, "error": f"missing API key ({envs})"}

    model = model or provider_default_model(pcfg)
    # B2-286 (2026-09-26): a null model is a named refusal, never a live call.
    # MEASURED (the B2-286 brief disease, B2-62 first probe): a bare call on a
    # lane with no default_model (z_ai2/z_ai3 carried none) sent "model": null
    # and got HTTP 200 with empty content + empty usage, so a dead lane read ok.
    # Applies to BOTH chat paths (chat_provider and chat_messages).
    if model is None and not pcfg.get("free_local"):
        return {
            "ok": False,
            "error": f"null_model_refused: {provider_id} resolved no model "
                     "(no default_model in configs/providers.yaml, none passed); "
                     "pass model= or set default_model",
            "provider": provider_id,
        }
    kind = (pcfg.get("kind") or "openai_compat").lower()

    if kind == "anthropic_messages":
        return _chat_anthropic(
            provider_id,
            pcfg,
            keys[0] if keys else "",
            system,
            user,
            model=str(model),
            temperature=temperature,
            max_tokens=max_tokens,
        )

    if kind == "gemini_native":
        # B2-194 (2026-09-26): the express key's native home is Vertex
        # generateContent (B2-63 receipt); openai_compat lanes stay on the
        # generic path below, untouched.
        return _chat_gemini_native(
            provider_id,
            pcfg,
            keys[0] if keys else "",
            system,
            user,
            model=str(model),
            temperature=temperature,
            max_tokens=max_tokens,
        )

    base = provider_base_url(pcfg)
    url = f"{base}/chat/completions"
    last_err = "unknown error"
    # Multi-key failover: try each configured key in order; move on for
    # auth/rate-limit codes (401/403/429). Free-local providers use one pass.
    for ki, key in enumerate(keys or ["ollama"]):
        max_tok_key = "max_completion_tokens" if pcfg.get("use_max_completion_tokens") else "max_tokens"
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": temperature,
            max_tok_key: max_tokens,
        }
        if thinking is None:
            payload = _thinking_off(pcfg, payload)
        elif thinking is False:
            payload["thinking"] = {"type": "disabled"}
        # thinking True -> leave DeepSeek v4's default thinking ON (coherence)
        # B2-62 REASONING FLOOR (spec §5.1): an undecided call under the thinking-on
        # minimum gets thinking disabled so the budget serves content (see helper).
        payload, floor_applied = _apply_reasoning_floor(
            payload, thinking=thinking, max_tokens=max_tokens, model=str(model))
        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key or 'ollama'}",
            # browser-like UA: Cloudflare (groq) returns HTTP 403/1010 to bare
            # Python-urllib signatures — a real UA passes the edge check (2026-08-24).
            "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                           "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"),
        }
        for hk, hv in (pcfg.get("extra_headers") or {}).items():
            headers[str(hk)] = str(hv)
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        to = timeout if timeout is not None else int(pcfg.get("timeout_seconds") or 90)
        # B2-62 OVERLOAD BACKOFF (spec docs/ref/ZAI_API_EXPERT_REFERENCE.md §5.1 law 1):
        # on 429 + overload body (1305/1302/"overloaded"), a retry_overload provider
        # retries the SAME request after 15s then 30s (B2-04 measured recovery wait,
        # stretched because one Lite 429 survived a single 15s wait) before failing.
        # Every failed attempt is recorded below, so the cadence keeps learning. After
        # exhaustion the normal failover/burst paths run unchanged (paid burst = last
        # resort). Providers without retry_overload never sleep.
        attempt = 0
        while True:
            t0 = time.perf_counter()
            try:
                with urllib.request.urlopen(req, timeout=to) as r:
                    data = json.loads(r.read().decode("utf-8"))
                lat_ms = int((time.perf_counter() - t0) * 1000)
                choice = (data.get("choices") or [{}])[0]
                msg = choice.get("message") or {}
                text = (msg.get("content") or "")
                # EMPTY-CONTENT HONESTY (2026-08-24): a reasoning model that spends the whole
                # budget thinking returns ok-but-empty (content "", finish_reason length). That is
                # NOT a successful empty answer — it is a budget failure. Report it honestly so the
                # loop treats it as retryable, not as a dead lane. (Reasoning fields vary: some
                # providers put it in message.reasoning, others message.reasoning_details.)
                if not text and (choice.get("finish_reason") == "length"
                                 or msg.get("reasoning") or msg.get("reasoning_details")):
                    return {"ok": False,
                            "error": "empty content — reasoning model consumed the budget "
                                     "(max_tokens too small; raise it or disable thinking)",
                            "provider": provider_id, "model": model, "empty_reasoning": True}
                if _looks_degenerate(text):
                    record_usage(
                        provider_id, model=str(model), ok=False,
                        session_id=session_id,
                        meta={"degenerate": True, "key_idx": ki},
                    )
                    return {
                        "ok": False,
                        "error": "degenerate repetition output (model lock loop) - retry",
                        "provider": provider_id,
                        "model": model,
                        "degenerate": True,
                    }
                usage = data.get("usage") or {}
                pt = int(usage.get("prompt_tokens") or 0)
                ct = int(usage.get("completion_tokens") or 0)
                # Cache split: DeepSeek exposes prompt_cache_hit/miss at top level;
                # OpenAI-compat exposes prompt_tokens_details.cached_tokens. Capture both so the
                # ledger carries hit/miss on EVERY call (cache_map hit ratio becomes self-contained).
                details = usage.get("prompt_tokens_details") or {}
                ch = int(usage.get("prompt_cache_hit_tokens") or details.get("cached_tokens") or 0)
                cm = int(usage.get("prompt_cache_miss_tokens") or max(0, pt - ch) or 0)
                record_usage(
                    provider_id,
                    model=str(model),
                    prompt_tokens=pt,
                    completion_tokens=ct,
                    cache_hit_tokens=ch,
                    cache_miss_tokens=cm,
                    ok=True,
                    session_id=session_id,
                    latency_ms=lat_ms,
                    meta={"chars": len(text), "key_idx": ki, "multi_key": len(keys) > 1,
                          "key_env": (_key_env_names(pcfg)[ki] if ki < len(_key_env_names(pcfg)) else "")},
                )
                out = {
                    "ok": True,
                    "text": text,
                    "provider": provider_id,
                    "model": model,
                    "usage": usage,
                    "budget_after": provider_budget(provider_id),
                    "key_idx": ki,
                }
                if floor_applied:
                    out["reasoning_floor_applied"] = True
                return out
            except urllib.error.HTTPError as e:
                err = e.read().decode("utf-8", errors="replace")[:300]
                last_err = f"HTTP {e.code}: {err}"
                record_usage(
                    provider_id, model=str(model or ""), ok=False,
                    session_id=session_id,
                    meta={"http": e.code, "key_idx": ki},
                )
                if (e.code == 429 and pcfg.get("retry_overload")
                        and attempt < OVERLOAD_ATTEMPTS and _is_overload_body(err)):
                    time.sleep(min(OVERLOAD_BASE_S * (2 ** attempt), OVERLOAD_CAP_S))
                    attempt += 1
                    continue  # retry the SAME request on the SAME key
                if e.code in (401, 403, 429) and ki + 1 < len(keys):
                    break  # exit the backoff loop: try next key in the chain
                return {"ok": False, "error": last_err, "provider": provider_id, "key_idx": ki}
            except Exception as e:
                last_err = str(e)[:200]
                record_usage(
                    provider_id, model=str(model or ""), ok=False,
                    session_id=session_id,
                    meta={"error": str(e)[:200], "key_idx": ki},
                )
                if ki + 1 < len(keys):
                    break
                return {"ok": False, "error": last_err, "provider": provider_id, "key_idx": ki}
    return {"ok": False, "error": last_err, "provider": provider_id}


def should_burst(err: str) -> bool:
    """True when a free/Z.ai lane failed in a way that should fire the paid mill."""
    e = (err or "").lower()
    return any(
        s in e
        for s in (
            "timed out",
            "timeout",
            "opencode_only",
            "1305",
            "1302",
            "concurrency timeout",
            "overloaded",
            "empty content",
        )
    )


def burst_mill(
    system: str,
    user: str,
    *,
    # same 08-29 rightsize: default to the ceiling, callers opt down
    max_tokens: int = 65536,
    reason: str = "",
) -> dict[str, Any]:
    """Paid DeepSeek-v4-flash mill when Z.ai coding-plan/Lite stalls.

    Operator 2026-08-28: Max/Lite plans hang on raw API and never burst to
    models we already pay for. allow_peak=True so a stall during 2x hours
    still ships; timeout 45s so a second hang cannot eat the beat.
    """
    r = chat_provider(
        "deepseek",
        system,
        user,
        model="deepseek-v4-flash",
        thinking=False,
        max_tokens=max_tokens,
        tier="T2",
        allow_peak=True,
        timeout=45,
    )
    r["burst"] = True
    r["burst_reason"] = (reason or "")[:160]
    r["burst_provider"] = "deepseek"
    return r


def _consume_sse(r, on_stream) -> dict[str, Any]:
    """Parse SSE stream; accumulate content + tool_calls; call on_stream(delta) per content delta.

    Returns the merged final chunk shape (choices[0].message + usage if present).
    """
    text_parts: list[str] = []
    tool_acc: dict[int, dict[str, Any]] = {}
    usage: dict[str, Any] = {}
    for raw in _iter_sse_events(r):
        line = raw.strip()
        if not line.startswith("data:"):
            continue
        payload = line[len("data:"):].strip()
        if payload == "[DONE]":
            break
        try:
            chunk = json.loads(payload)
        except Exception:
            continue
        if chunk.get("usage"):
            usage = chunk["usage"]
        for c in chunk.get("choices") or []:
            delta = c.get("delta") or {}
            d = delta.get("content")
            if isinstance(d, str) and d:
                text_parts.append(d)
                on_stream(d)
            for tc in delta.get("tool_calls") or []:
                idx = int(tc.get("index") or 0)
                acc = tool_acc.setdefault(
                    idx, {"id": None, "type": "function", "function": {"name": "", "arguments": ""}}
                )
                fn = tc.get("function") or {}
                if tc.get("id"):
                    acc["id"] = tc["id"]
                if fn.get("name"):
                    acc["function"]["name"] = fn["name"]
                if fn.get("arguments"):
                    acc["function"]["arguments"] += fn["arguments"]
            fr = c.get("finish_reason")
            if fr and fr != "null":
                pass  # final chunk marker; content already captured
    tool_calls = [tool_acc[k] for k in sorted(tool_acc)] or None
    msg: dict[str, Any] = {"role": "assistant", "content": "".join(text_parts)}
    if tool_calls:
        msg["tool_calls"] = tool_calls
    choice = {"message": msg, "finish_reason": "stop"}
    if tool_calls:
        choice["finish_reason"] = "tool_calls"
    return {"choices": [choice], "usage": usage or None}

def chat_messages(
    provider_id: str,
    messages: list[dict[str, Any]],
    *,
    tools: list[dict[str, Any]] | None = None,
    model: str | None = None,
    temperature: float = 0.2,
    max_tokens: int = 2048,
    tier: str = "T1",
    tool_choice: str | dict | None = "auto",
    stream: bool = False,
    on_stream=None,
    timeout: int | None = None,
    session_id: str = "",
) -> dict[str, Any]:
    """Multi-turn OpenAI-compat chat with optional tools (DeepSeek / Ollama / etc.).

    messages: OpenAI-style list (system/user/assistant/tool).
    tools: OpenAI tools array, or None for plain chat.
    Returns: ok, text, tool_calls (list), message (raw assistant msg), provider, model, usage
    """
    from models.quota import provider_budget, record_usage

    pcfg = get_provider(provider_id)
    if not pcfg:
        return {"ok": False, "error": f"unknown provider {provider_id}"}

    never = set((load_providers().get("defaults") or {}).get("never_remote_tiers") or ["T0", "T1"])
    if tier in never and not pcfg.get("free_local"):
        return {"ok": False, "error": f"refused: tier {tier} cannot use remote {provider_id}"}

    b = provider_budget(provider_id)
    if not b.get("budget_ok"):
        return {
            "ok": False,
            "error": "quota exhausted",
            "budget": b,
            "hint": "Wait for reset or raise max_calls/max_tokens in configs/providers.yaml",
        }

    keys = provider_keys(pcfg)
    if not keys and not pcfg.get("free_local"):
        envs = " / ".join(_key_env_names(pcfg)) or pcfg.get("api_key_env") or "?"
        return {"ok": False, "error": f"missing API key ({envs})"}

    model = model or provider_default_model(pcfg)
    # B2-286 (2026-09-26): a null model is a named refusal, never a live call.
    # MEASURED (the B2-286 brief disease, B2-62 first probe): a bare call on a
    # lane with no default_model (z_ai2/z_ai3 carried none) sent "model": null
    # and got HTTP 200 with empty content + empty usage, so a dead lane read ok.
    # Applies to BOTH chat paths (chat_provider and chat_messages).
    if model is None and not pcfg.get("free_local"):
        return {
            "ok": False,
            "error": f"null_model_refused: {provider_id} resolved no model "
                     "(no default_model in configs/providers.yaml, none passed); "
                     "pass model= or set default_model",
            "provider": provider_id,
        }
    kind = (pcfg.get("kind") or "openai_compat").lower()
    if kind == "anthropic_messages":
        return {"ok": False, "error": "tool loop not wired for anthropic in agent v1 — use deepseek"}
    if kind == "gemini_native":
        # B2-194: gemini_native is a SPEAKING lane; the tool loop stays
        # openai_compat. A named refusal here beats posting openai-shaped
        # bodies at a generateContent endpoint and calling the 404 an answer.
        return {"ok": False,
                "error": "tool loop not wired for gemini_native in agent v1 — speaking lanes only (B2-194)"}

    base = provider_base_url(pcfg)
    url = f"{base}/chat/completions"
    last_err = "unknown error"
    # Multi-key failover: same shape as chat_provider (401/403/429 -> next key).
    for ki, key in enumerate(keys or ["ollama"]):
        payload: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if tools:
            payload["tools"] = tools
            if tool_choice is not None:
                payload["tool_choice"] = tool_choice
        if stream and on_stream is not None:
            payload["stream"] = True
        payload = _thinking_off(pcfg, payload)
        # B2-62 REASONING FLOOR (spec docs/ref/ZAI_API_EXPERT_REFERENCE.md §5.1): same
        # undecided-call protection as chat_provider. chat_messages has no thinking
        # param, so the floor only sees the undecided case by construction.
        payload, floor_applied = _apply_reasoning_floor(
            payload, thinking=None, max_tokens=max_tokens, model=str(model))
        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key or 'ollama'}",
            # browser-like UA (2026-08-25): chat_provider got this on 08-24, chat_messages
            # DIDN'T — Cloudflare 1010-blocks the bare urllib signature, so every AGENT run
            # (which rides chat_messages + tools) failed with "HTTP 403: error code: 1010".
            "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                           "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"),
        }
        for hk, hv in (pcfg.get("extra_headers") or {}).items():
            headers[str(hk)] = str(hv)

        to = timeout or int(pcfg.get("timeout_seconds") or 180)
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        t0 = time.perf_counter()
        try:
            if stream and on_stream is not None:
                with urllib.request.urlopen(req, timeout=to) as r:
                    data = _consume_sse(r, on_stream)
            else:
                with urllib.request.urlopen(req, timeout=to) as r:
                    data = json.loads(r.read().decode("utf-8"))
            lat_ms = int((time.perf_counter() - t0) * 1000)
            choice = (data.get("choices") or [{}])[0]
            msg = choice.get("message") or {}
            text = msg.get("content") or ""
            if isinstance(text, list):
                # some models return content parts
                text = "".join(
                    (p.get("text") or "") if isinstance(p, dict) else str(p) for p in text
                )
            tool_calls = msg.get("tool_calls") or []
            usage = data.get("usage") or {}
            pt = int(usage.get("prompt_tokens") or 0)
            ct = int(usage.get("completion_tokens") or 0)
            details = usage.get("prompt_tokens_details") or {}
            ch = int(usage.get("prompt_cache_hit_tokens") or details.get("cached_tokens") or 0)
            cm = int(usage.get("prompt_cache_miss_tokens") or max(0, pt - ch) or 0)
            if _looks_degenerate(text or ""):
                record_usage(
                    provider_id, model=str(model), ok=False,
                    session_id=session_id,
                    meta={"degenerate": True, "key_idx": ki},
                )
                return {
                    "ok": False,
                    "error": "degenerate repetition output (model lock loop) - retry",
                    "provider": provider_id,
                    "model": model,
                    "degenerate": True,
                }
            record_usage(
                provider_id,
                model=str(model),
                prompt_tokens=pt,
                completion_tokens=ct,
                cache_hit_tokens=ch,
                cache_miss_tokens=cm,
                ok=True,
                session_id=session_id,
                latency_ms=lat_ms,
                meta={"chars": len(text or ""), "tool_calls": len(tool_calls), "key_idx": ki,
                      "key_env": (_key_env_names(pcfg)[ki] if ki < len(_key_env_names(pcfg)) else "")},
            )
            out = {
                "ok": True,
                "text": text or "",
                "tool_calls": tool_calls,
                "message": msg,
                "finish_reason": choice.get("finish_reason"),
                "provider": provider_id,
                "model": model,
                "usage": usage,
                "budget_after": provider_budget(provider_id),
                "key_idx": ki,
            }
            if floor_applied:
                out["reasoning_floor_applied"] = True
            return out
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8", errors="replace")[:600]
            last_err = f"HTTP {e.code}: {err}"
            record_usage(
                provider_id, model=str(model or ""), ok=False,
                session_id=session_id,
                meta={"http": e.code, "key_idx": ki},
            )
            if e.code in (401, 403, 429) and ki + 1 < len(keys):
                continue  # next key in the chain
            return {"ok": False, "error": last_err, "provider": provider_id, "key_idx": ki}
        except Exception as e:
            last_err = str(e)[:200]
            record_usage(
                provider_id, model=str(model or ""), ok=False,
                session_id=session_id,
                meta={"error": str(e)[:200], "key_idx": ki},
            )
            if ki + 1 < len(keys):
                continue
            return {"ok": False, "error": last_err, "provider": provider_id, "key_idx": ki}
    return {"ok": False, "error": last_err, "provider": provider_id}


def _chat_anthropic(
    provider_id: str,
    pcfg: dict[str, Any],
    key: str,
    system: str,
    user: str,
    *,
    model: str,
    temperature: float,
    max_tokens: int,
) -> dict[str, Any]:
    """Native Anthropic Messages API (Claude)."""
    from models.quota import provider_budget, record_usage

    if not key:
        return {"ok": False, "error": "missing ANTHROPIC_API_KEY"}
    base = (pcfg.get("base_url") or "https://api.anthropic.com/v1").rstrip("/")
    url = f"{base}/messages"
    body = json.dumps(
        {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "system": system,
            "messages": [{"role": "user", "content": user}],
        }
    ).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
    }
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = json.loads(r.read().decode("utf-8"))
        parts = data.get("content") or []
        text = ""
        for p in parts:
            if isinstance(p, dict) and p.get("type") == "text":
                text += str(p.get("text") or "")
        usage = data.get("usage") or {}
        pt = int(usage.get("input_tokens") or 0)
        ct = int(usage.get("output_tokens") or 0)
        record_usage(
            provider_id,
            model=model,
            prompt_tokens=pt,
            completion_tokens=ct,
            ok=True,
            meta={"chars": len(text)},
        )
        return {
            "ok": True,
            "text": text,
            "provider": provider_id,
            "model": model,
            "usage": {"prompt_tokens": pt, "completion_tokens": ct},
            "budget_after": provider_budget(provider_id),
        }
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")[:400]
        record_usage(provider_id, model=model, ok=False, meta={"http": e.code})
        return {"ok": False, "error": f"HTTP {e.code}: {err}", "provider": provider_id}
    except Exception as e:
        record_usage(provider_id, model=model, ok=False, meta={"error": str(e)[:200]})
        return {"ok": False, "error": str(e), "provider": provider_id}


def _chat_gemini_native(
    provider_id: str,
    pcfg: dict[str, Any],
    key: str,
    system: str,
    user: str,
    *,
    model: str,
    temperature: float,
    max_tokens: int,
) -> dict[str, Any]:
    """Native Vertex/Gemini generateContent (B2-194, spec: B2-63 receipt).

    Wire contract (fixture-pinned in tests/test_gemini_native.py):
    POST {base_url}/publishers/google/models/{model}:generateContent with
    x-goog-api-key auth (both auth shapes measured in
    B2_63_vertex_probe_results.json; the header shape is canonical here).
    Live traffic stays 403 PERMISSION_DENIED until the operator enables
    aiplatform.googleapis.com on the key's project (B2-63 GO card); the
    brief's live falsifier is a 200 with candidates[0].content from the
    B2_63_vertex_probe.py rerun.
    """
    from models.quota import provider_budget, record_usage

    if not key:
        return {"ok": False, "error": "missing gemini express/Vertex API key"}
    base = (pcfg.get("base_url") or "https://aiplatform.googleapis.com/v1").rstrip("/")
    url = f"{base}/publishers/google/models/{model}:generateContent"
    payload = {
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "systemInstruction": {"parts": [{"text": system}]},
        "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens},
    }
    body = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json", "x-goog-api-key": key}
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = json.loads(r.read().decode("utf-8"))
        cands = data.get("candidates") or []
        parts = ((cands[0].get("content") or {}).get("parts") or []) if cands else []
        text = ""
        for p in parts:
            if isinstance(p, dict):
                text += str(p.get("text") or "")
        usage = data.get("usageMetadata") or {}
        pt = int(usage.get("promptTokenCount") or 0)
        ct = int(usage.get("candidatesTokenCount") or 0)
        record_usage(
            provider_id,
            model=model,
            prompt_tokens=pt,
            completion_tokens=ct,
            ok=True,
            meta={"chars": len(text)},
        )
        return {
            "ok": True,
            "text": text,
            "provider": provider_id,
            "model": model,
            "usage": {"prompt_tokens": pt, "completion_tokens": ct},
            "budget_after": provider_budget(provider_id),
        }
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")[:400]
        record_usage(provider_id, model=model, ok=False, meta={"http": e.code})
        return {"ok": False, "error": f"HTTP {e.code}: {err}", "provider": provider_id}
    except Exception as e:
        record_usage(provider_id, model=model, ok=False, meta={"error": str(e)[:200]})
        return {"ok": False, "error": str(e), "provider": provider_id}


def chat_routed(
    system: str,
    user: str,
    *,
    job: str = "default",
    tier: str = "T2",
    model: str | None = None,
    temperature: float = 0.2,
    max_tokens: int = 1024,
) -> dict[str, Any]:
    """Pick provider by job+budget then chat."""
    from models.quota import pick_provider

    pick = pick_provider(job, tier=tier)
    if not pick.get("ok"):
        return pick
    return chat_provider(
        pick["provider"],
        system,
        user,
        model=model or pick.get("model"),
        temperature=temperature,
        max_tokens=max_tokens,
        tier=tier,
    )


# Keep old OpenRouter helper working
def openrouter_configured() -> bool:
    return bool(os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OR_API_KEY"))


def chat_openrouter(system: str, user: str, **kwargs: Any) -> dict[str, Any]:
    return chat_provider("openrouter", system, user, **kwargs)
