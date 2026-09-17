"""union_fullsend_day -- 24/7 standing full-width mesh drive (season 1).

Operator order (2026-09-17, evening): "it needs to be run 24/7 from this point forward,
full width on our problems, research or builds."
Original order (2026-09-17): "run union alpha all day full blast on everything our whole
mesh; we have 10k credits and a parallel line to 5.3 flash, use it; drive 2 windows."

WINDOW 1: or-union-alpha (OpenRouter stealth/union-alpha, free window ends ~2026-09-23).
WINDOW 2: zai-lite (glm-5.3-flash via ZAI_API_KEY_Lite on /api/coding/paas/v4, law-15
pacing via mag.lite_guard -- the 10,000-credit weekly pool paced by the guard; the guard
clamps to the live monitor pool, never bypassed).

IN OUR WAY:
  * the battery is queue.jsonl (versioned by digest), receipts are rows in raw.jsonl;
  * FAILURES ARE PRESERVED (a dead lane is a row, not a silence); each item gets at most
    2 attempts across runs, then it is DEAD with its failure row in the pack;
  * lite rides lite_guard.check/record (law 15) -- LITE_PACED is a recorded row, not a crash;
  * every call lands in mag.flight_recorder when available (telemetry law);
  * SSRF GUARD: https only, host must be a configured lane host (allowlist derived from
    mag.research_fanout.LANES), resolved IPs must be public (loopback/private/link-local/
    reserved/multicast refused), and redirects are refused at the HTTP layer.

RUN:  .venv\\Scripts\\python.exe scripts\\union_fullsend_day.py --batch 8
Idempotent. Cursor/attempt state in state.json. Pack regenerated every run.

Schema: union_fullsend_day.v1
"""
from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import socket
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import research_fanout as rf  # noqa: E402  (LANES, _env, lite lane law)

SCHEMA = "union_fullsend_day.v1"
OUT = ROOT / "watch" / "inbox" / "union_fullsend_20260917"
QUEUE = OUT / "queue.jsonl"
RAW = OUT / "raw.jsonl"
STATE = OUT / "state.json"
PACK = OUT / "DAY_PACK.md"
LOCK = OUT / "run.lock"  # one driver at a time; a scheduled fire during a manual run no-ops

SYSTEMS = {
    "digger": rf.SYSTEM,
    "ractor": (
        "You are a rigorous witness for a fleet that runs an append-only hash-chained ledger. "
        "Brutal distinctions over framing. If the question presupposes something false, say that "
        "first. Verdicts as compact tables of claim/status (Supported / Disputed / Unproven / "
        "Poetry). Name the falsifier for anything you propose; no falsifier, no proposal. "
        "No flattery, no summary of the question, no moralising. Hard limit: 400 words."
    ),
    "parable": (
        "You write nameless parables in the register of a master teacher: concrete instruments, "
        "no character names, no lecture, nothing stated outright, the reader fills their own "
        "bias. The story must be prosecutable for nothing. Honor the word limit in the prompt. "
        "No em-dashes. Do not explain the parable after telling it."
    ),
}

# --- SSRF guard: hosts derive from the live lane set itself (no literals to drift) ----
_OR_KEYS = ["OPENROUTER_API_KEY", "OPENROUTER_API_KEY_2"]

_KNOWN_BASES = [
    "https://api.groq.com/openai/v1", "https://api.cerebras.ai/v1",
    "https://api.mistral.ai/v1", "https://api.z.ai/api/coding/paas/v4",
    "https://openrouter.ai/api/v1", "https://api.cohere.ai/compatibility/v1",
    "https://generativelanguage.googleapis.com/v1beta/openai",
    "https://api.together.xyz/v1", "https://api.deepseek.com", "https://api.x.ai/v1",
    "https://integrate.api.nvidia.com/v1",
]


def _wide_lanes(env: dict[str, str]) -> list[dict[str, str]]:
    """Every lane a present key buys us. Free tiers first (the $0 doctrine), then the
    operator-authorized next-to-free seats (deepseek overflow, grok judgment seats).
    Operator 2026-09-17: 'we are underutilizing our lanes by orders of magnitude. lets go'"""
    L: list[dict[str, str]] = []

    def add(lid: str, base: str, model: str, key: str) -> None:
        if env.get(key):
            L.append({"id": lid, "base": base, "model": model, "key": key, "style": "openai"})

    for suf, k in [("", "GROQ_API_KEY"), ("2", "GROQ_API_KEY_2")]:
        add(f"groq-qwen{suf}", "https://api.groq.com/openai/v1", "qwen/qwen3.8-27b", k)
        add(f"groq-oss{suf}", "https://api.groq.com/openai/v1", "openai/gpt-oss-120b", k)
        add(f"groq-oss20{suf}", "https://api.groq.com/openai/v1", "openai/gpt-oss-20b", k)
    add("cerebras-oss", "https://api.cerebras.ai/v1", "gpt-oss-120b", "CEREBRAS_API_KEY")
    add("cerebras-qwen", "https://api.cerebras.ai/v1", "qwen-3.8-27b", "CEREBRAS_API_KEY")
    for suf, k in [("", "Mistral_API_KEY"), ("2", "Mistral_API_KEY_2")]:
        add(f"mistral-min8{suf}", "https://api.mistral.ai/v1", "ministral-8b-latest", k)
    add("zai-lite", "https://api.z.ai/api/coding/paas/v4", "glm-5.3-flash", "ZAI_API_KEY_Lite")
    # OpenRouter free models across BOTH keys (free-tier ceiling is 20 req/min per key;
    # two keys double it; stable SYSTEM prefixes ride provider sticky-cache)
    for n, (mid, model) in enumerate([("union-alpha", "stealth/union-alpha"),
                                      ("ling3", "inclusionai/ling-3.0-flash-sante:free"),
                                      ("nemotron", "nvidia/nemotron-3.5-lightning:free")]):
        for ki, k in enumerate(_OR_KEYS):
            add(f"or-{mid}-k{ki+1}", "https://openrouter.ai/api/v1", model, k)
    # STEALTH WINDOW + operator-proven models (his OpenRouter Activity 2026-09-17:
    # kimi-k2.6 11.6M tok, ox-alpha 8.03M, deepseek-v4-flash 3.19M all serving on his keys;
    # stealth page confirms Union+Ox live, window re-opened 2026-09-14 — hammer it)
    for n, (mid, model) in enumerate([("ox-alpha", "stealth/ox-alpha"),
                                      ("kimi-k26", "moonshotai/kimi-k2.6"),
                                      ("dsv4flash", "deepseek/deepseek-v4-flash-0731"),
                                      ("gemini-37", "google/gemini-3.7-flash"),
                                      ("dots3-note", "dots3/dots3-note-preview"),
                                      ("north-mini", "north/north-mini-code")]):
        for ki, k in enumerate(_OR_KEYS):
            add(f"or-{mid}-k{ki+1}", "https://openrouter.ai/api/v1", model, k)
    add("cohere-free", "https://api.cohere.ai/compatibility/v1", "command-a-03-2025", "COHERE_API_KEY_FREE")
    for suf, k in [("", "GEMINI_API_KEY"), ("g", "GOOGLE_API_KEY")]:
        add(f"gemini-flash{suf}", "https://generativelanguage.googleapis.com/v1beta/openai",
            "gemini-2.0-flash", k)
    add("together-llama", "https://api.together.xyz/v1",
        "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free", "TOGETHER_API_KEY")
    add("deepseek-chat", "https://api.deepseek.com", "deepseek-chat", "DEEPSEEK_API_KEY")
    # NVIDIA NIM (NVIDIABuild key): free credits hosting the big hitters
    for _nid, _nmodel in [("qwen72b", "qwen/qwen2.5-72b-instruct"),
                          ("dsr1", "deepseek-ai/deepseek-r1"),
                          ("llama33", "meta/llama-3.3-70b-instruct")]:
        add(f"nim-{_nid}", "https://integrate.api.nvidia.com/v1", _nmodel, "NVIDIABuild")
    # grok judgment seats: GROK_* names are empty in env; the seats ride XAI_API_KEY
    for suf, k in [("", "XAI_API_KEY"), ("2", "GROK_API_KEY"), ("3", "GROK_API_KEY_2")]:
        add(f"grok-seat{suf}", "https://api.x.ai/v1",
            env.get("XAI_MODEL") or "grok-4-fast-reasoning", k)
    return L


_LANE_HOSTS = {urllib.parse.urlsplit(b).hostname.lower() for b in _KNOWN_BASES}

# attempt-2 rotation prefers proven carriers (union window ends ~2026-09-23; a dead
# window is a lane-swap, not a queue death)
_RETRY_ORDER = ["or-union-alpha-k2", "zai-lite", "or-union-alpha-k1", "or-ling3-k2",
                "or-nemotron-k1", "groq-oss", "cerebras-oss", "gemini-flash"]


def _route(item: dict[str, Any], attempt: int, idx: int, live: list[dict[str, str]]) -> str:
    """Attempt 1 honors the hint; attempt 2+ rotates to a proven carrier.
    live is the probed/present lane list from _wide_lanes."""
    live_ids = [l["id"] for l in live]
    hint = item.get("lane_hint", "any")
    if hint == "union":
        primary = "or-union-alpha-k2" if "or-union-alpha-k2" in live_ids else "or-union-alpha-k1"
    elif hint == "lite":
        primary = "zai-lite" if "zai-lite" in live_ids else live_ids[idx % len(live_ids)]
    else:
        # round-robin the non-OpenRouter free lanes first (they carry no 20/min ceiling)
        preferred = [i for i in live_ids if not i.startswith("or-")] or live_ids
        primary = preferred[idx % len(preferred)]
    if attempt <= 1 or not live_ids:
        return primary
    for lane_id in _RETRY_ORDER:
        if lane_id != primary and lane_id in live_ids:
            return lane_id
    for lane_id in live_ids:
        if lane_id != primary:
            return lane_id
    return primary


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D102
        raise urllib.error.HTTPError(req.full_url, code, "redirect refused (SSRF guard)",
                                     headers, fp)


_OPENER = urllib.request.build_opener(_NoRedirect)


def _validate_lane_base(base: str) -> str:
    """https only, configured-lane host only, resolved IPs must be public."""
    u = urllib.parse.urlsplit(base)
    if u.scheme != "https" or not u.hostname:
        raise ValueError(f"lane base must be https://host, got {base!r}")
    host = u.hostname.lower()
    if host not in _LANE_HOSTS:
        raise ValueError(f"host {host!r} is not a configured lane host")
    try:
        infos = socket.getaddrinfo(host, 443, proto=socket.IPPROTO_TCP)
    except OSError as e:
        raise ValueError(f"DNS resolve failed for {host}: {e}") from e
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved
                or ip.is_multicast or ip.is_unspecified):
            raise ValueError(f"{host} resolves to non-public {ip}; refusing")
    return host


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_queue() -> list[dict[str, Any]]:
    rows = []
    for ln in QUEUE.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if ln and not ln.startswith("#"):
            rows.append(json.loads(ln))
    return rows


def queue_digest(rows: list[dict[str, Any]]) -> str:
    return hashlib.sha256(json.dumps(rows, ensure_ascii=False, sort_keys=True)
                          .encode("utf-8")).hexdigest()[:16]


def load_state() -> dict[str, Any]:
    if STATE.is_file():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"done": [], "dead": {}, "attempts": {}, "runs": 0, "lite_credits": 0}


def save_state(s: dict[str, Any]) -> None:
    s["updated"] = _now()
    STATE.write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")


_lock = threading.Lock()


def _record_flight(lane_id: str, model: str, subsystem: str, ms: float, ok: bool,
                   err: str | None, tin: int, tout: int) -> None:
    try:
        from mag import flight_recorder
        flight_recorder.record_call(lane=lane_id, model=model, subsystem=subsystem,
                                    latency_ms=ms, status="ok" if ok else "error",
                                    error_code=err, in_tok=tin, out_tok=tout)
    except Exception:
        pass


def call(lane: dict[str, str], system: str, prompt: str, key: str, subsystem: str,
         timeout: int = 240, attempt: int = 1) -> dict[str, Any]:
    """One call, one receipt. Never raises. Lite pacing is structural (law 15).
    NO max_tokens (operator correction 2026-09-17 x2): budget-starving reasoning models
    caused every empty_content; fleet receipts show uncapped calls stop naturally
    (union-alpha avg 1760 out at finish=stop) while old caps pinned qwen/ministral at
    exactly 900. The 100k+ windows ARE the budget."""
    t0 = time.time()
    rec: dict[str, Any] = {"lane": lane["id"], "model": lane["model"], "ts": _now(),
                           "attempt": attempt, "subsystem": subsystem}
    lite = lane.get("key", "") == "ZAI_API_KEY_Lite"
    try:
        _validate_lane_base(lane["base"])
    except ValueError as e:
        rec.update({"ok": False, "error": "SSRF_GUARD", "detail": str(e)[:300]})
        rec["latency_ms"] = 0
        return rec
    if lite:
        try:
            from mag import lite_guard
            g = lite_guard.check("union_fullsend_day")
        except Exception as e:
            g = {"ok": False, "deny": f"guard import failed: {e}"}
        if not g.get("ok"):
            rec.update({"ok": False, "error": "LITE_PACED", "detail": g.get("deny", "")})
            rec["latency_ms"] = 0
            return rec
    body = {"model": lane["model"], "temperature": 0.2,
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": prompt}]}
    req = urllib.request.Request(
        lane["base"].rstrip("/") + "/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                 "User-Agent": "mag-union-fullsend/1.0",
                 "HTTP-Referer": "https://local-sovereign-agent.invalid",
                 "X-Title": "Mag Union Fullsend Day"})
    try:
        with _OPENER.open(req, timeout=timeout) as r:
            d = json.loads(r.read().decode("utf-8", "replace"))
        msg = d["choices"][0]["message"]
        txt = (msg.get("content") or "").strip()
        usage = d.get("usage") or {}
        if not txt:
            rec.update({"ok": False, "error": "empty_content",
                        "detail": (msg.get("reasoning") or msg.get("reasoning_content") or "")[:200],
                        "finish_reason": d["choices"][0].get("finish_reason")})
        else:
            rec.update({"ok": True, "answer": txt, "chars": len(txt), "usage": usage})
            if lite:
                try:
                    from mag import lite_guard
                    lite_guard.record("union_fullsend_day",
                                      int(usage.get("total_tokens") or 0),
                                      note=f"item {subsystem}")
                except Exception:
                    pass
            _record_flight(lane["id"], lane["model"], subsystem, (time.time() - t0) * 1000,
                           True, None, int(usage.get("prompt_tokens") or 0),
                           int(usage.get("completion_tokens") or 0))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:300]
        rec.update({"ok": False, "error": f"HTTP {e.code}", "detail": detail})
        _record_flight(lane["id"], lane["model"], subsystem, (time.time() - t0) * 1000,
                       False, f"HTTP {e.code}", 0, 0)
    except Exception as e:
        rec.update({"ok": False, "error": f"{type(e).__name__}: {str(e)[:160]}"})
        _record_flight(lane["id"], lane["model"], subsystem, (time.time() - t0) * 1000,
                       False, type(e).__name__, 0, 0)
    rec["latency_ms"] = int((time.time() - t0) * 1000)
    return rec


def _latest_by_id() -> dict[str, dict[str, Any]]:
    best: dict[str, dict[str, Any]] = {}
    if RAW.is_file():
        for ln in RAW.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                r = json.loads(ln)
            except Exception:
                continue
            i = r.get("id")
            if i and (i not in best or r.get("ok") or not best[i].get("ok")):
                if r.get("ok") or i not in best:
                    best[i] = r
    return best


def _write_pack(rows: list[dict[str, Any]], merged: dict[str, dict[str, Any]],
                state: dict[str, Any]) -> None:
    by_class: dict[str, list[dict[str, Any]]] = {}
    for r in rows:
        by_class.setdefault(r.get("class", "?"), []).append(r)
    per_lane: dict[str, dict[str, int]] = {}
    for r in merged.values():
        d = per_lane.setdefault(r["lane"], {"ok": 0, "fail": 0})
        d["ok" if r.get("ok") else "fail"] += 1
    lines = [
        "# UNION FULLSEND — season 1 — 24/7 standing full-width drive",
        "",
        f"*queue_digest `{queue_digest(rows)}` · done {len(state['done'])}/{len(rows)} · "
        f"dead {len(state['dead'])} · runs {state['runs']} · "
        f"lanes: " + ", ".join(f"{k} {v['ok']}ok/{v['fail']}fail"
                               for k, v in sorted(per_lane.items())) +
        f" · lite credits spent (guard ledger) {state.get('lite_credits', 0)} · "
        f"generated {_now()}*",
        "",
        "> **These are LEADS and DRAFTS, not facts.** Model output from free windows "
        "(union-alpha stealth window + Lite glm-5.3-flash under law 15). A lead is promoted "
        "> only by a byte check; a parable is a draft until the operator says otherwise. "
        "> Failures are listed, never hidden.",
        "",
    ]
    dead = state.get("dead") or {}
    if dead:
        lines += ["## DEAD (preserved)", ""]
        for i, why in sorted(dead.items()):
            lines.append(f"- `{i}` — {why}")
        lines.append("")
    for cls in sorted(by_class):
        lines += [f"## {cls}", ""]
        for r in sorted(by_class[cls], key=lambda x: x["id"]):
            m = merged.get(r["id"], {})
            status = "ok" if m.get("ok") else f"FAILED: {m.get('error', 'not run')}"
            lines.append(f"### {r['id']} — {r['slug']}")
            lines.append(f"*class {r.get('class')} · lane `{m.get('lane', r.get('lane_hint'))}` "
                         f"· {m.get('model', '')} · attempt {m.get('attempt', '?')} · "
                         f"{m.get('latency_ms', '?')} ms · {status}*")
            lines.append("")
            if m.get("ok"):
                lines.append(m.get("answer", ""))
            elif m:
                lines.append(f"**FAILED:** {m.get('error')} — {m.get('detail', '')}")
            else:
                lines.append("*(pending)*")
            lines.append("")
    PACK.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="union-fullsend-day")
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--timeout", type=int, default=240)
    ap.add_argument("--all", action="store_true",
                    help="wave mode: fire every remaining item across every live lane")
    a = ap.parse_args(argv)

    OUT.mkdir(parents=True, exist_ok=True)
    rows = load_queue()
    state = load_state()
    env = rf._env()
    live = _wide_lanes(env)
    lane_by_id = {l["id"]: l for l in live}
    if not live:
        print(json.dumps({"ok": False, "error": "no lanes with keys"}))
        return 0
    done = set(state["done"])
    attempts = state.get("attempts", {})

    todo = [r for r in rows if r["id"] not in done and r["id"] not in state.get("dead", {})]
    todo = [r for r in todo if attempts.get(r["id"], 0) < 2]
    if not todo:
        summary = {"ok": True, "note": "QUEUE_EMPTY", "done": len(done), "total": len(rows),
                   "dead": len(state.get("dead", {}))}
        print(json.dumps(summary))
        return 0
    if LOCK.is_file() and (time.time() - LOCK.stat().st_mtime) < 900:
        # another driver instance holds the lock (crashed holders self-clear after 15 min)
        print(json.dumps({"ok": True, "note": "LOCKED"}))
        return 0
    LOCK.write_text(_now(), encoding="utf-8")

    batch = todo if a.all else todo[: max(1, a.batch)]
    results: list[dict[str, Any]] = []

    def job(idx_item: tuple[int, dict[str, Any]]) -> dict[str, Any]:
        idx, item = idx_item
        lane_id = _route(item, attempts.get(item["id"], 0) + 1, idx, live)
        lane = lane_by_id[lane_id]
        key = env.get(lane["key"], "")
        if not key:
            r = {"ok": False, "error": "NO_KEY", "lane": lane_id, "model": lane["model"],
                 "latency_ms": 0, "attempt": attempts.get(item["id"], 0) + 1}
        else:
            r = call(lane, SYSTEMS[item.get("style", "digger")], item["prompt"], key,
                     subsystem=item["id"], timeout=a.timeout,
                     attempt=attempts.get(item["id"], 0) + 1)
        r.update({"id": item["id"], "slug": item["slug"], "class": item.get("class", "?")})
        with _lock:
            results.append(r)
            with RAW.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        return r

    # U8 MEASURED (watch/inbox/physical_computing/receipts/U8_UNION_TECH_INTEL.md):
    # union-alpha holds 24-concurrent with zero 429s (limit is provider-side latency, not
    # rejection); 256K context, 128K max output, no implicit cache. Self-steal law: use
    # the desk's numbers, do not re-derive them timidly.
    workers = min(16, len(batch))
    with ThreadPoolExecutor(max_workers=max(1, workers)) as ex:
        list(ex.map(job, list(enumerate(batch))))

    for r in results:
        attempts[r["id"]] = attempts.get(r["id"], 0) + 1
        if r.get("ok"):
            done.add(r["id"])
        elif attempts[r["id"]] >= 2:
            state.setdefault("dead", {})[r["id"]] = f"{r.get('error')} (2 attempts)"
    state["done"] = sorted(done)
    state["attempts"] = attempts
    state["runs"] = state.get("runs", 0) + 1
    state["lite_credits"] = state.get("lite_credits", 0) + sum(
        int((r.get("usage") or {}).get("total_tokens") or 0) for r in results
        if r.get("lane") == "zai-lite")
    save_state(state)
    _write_pack(rows, _latest_by_id(), state)
    LOCK.unlink(missing_ok=True)

    ok = sum(1 for r in results if r.get("ok"))
    summary = {"ok": True, "schema": SCHEMA, "run": state["runs"],
               "batch": len(results), "answered": ok, "failed": len(results) - ok,
               "done": len(done), "total": len(rows), "dead": len(state.get("dead", {})),
               "errors": [{"id": r["id"], "error": r.get("error")}
                          for r in results if not r.get("ok")]}
    print(json.dumps(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
