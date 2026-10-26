"""r06_free_probe -- the r06#2 resolving instrument (2026-10-05).

Corpus/steal/MASTER_READ_ESTATE.md D3 (r06#2): RIB_FREE_USAGE_POLICY_20260823 says
"the moment you try to force them, they throttle into empty (429)" while the banked
instrument row (RIB_MODEL_GARDEN_ROUTING.md:192, animals/stealth_free_lanes.jsonl) measured
"459 rows, ZERO 429, 69h+ sustained forced mining" -- CONTRADICTION OPEN, with its own
resolution order: "resolve with instruments, not by editing either rib silently". This
script IS that instrument: a forced-width cool/heat re-probe of the stealth free lanes.

Design:
  COOL   width 1, sequential, 4s spacing -- the policy rib's own sanctioned shape
         ("use them when they're cool").
  HEAT   instantaneous width = full roster fired in parallel, zero spacing, 3 waves
         back to back -- the policy rib's named anti-pattern ("force them") at a width the
         4-8 rows/hour banked evidence never tested (its own caveat: register may log
         successes only; this probe logs every outcome including failures).

Every ask: POST to the one literal allowlisted endpoint below, max_tokens 16, prompt
"Reply with the single word: ALIVE" (the sanctioned tools/openrouter_free_gate.py gate
shape), single key (OPENROUTER_API_KEY from env or .env, never printed). URL safety per the
allowlist law (tools/stealth_driver.py: scheme checked, allowlisted hosts, enforced in
code): literal https URL constant, _guard() re-checked on every request AND every redirect,
private/loopback/link-local hosts impossible by construction.

Roster: the earned configs/providers.yaml free block + stealth/space-bunny-alpha. Results:
one JSONL row per ask, {phase, wave, model, http, ok, content_head, finish, detail, ts}.
Verdict lives in the receipt beside this file; the ribs get the verdict row only AFTER this
instrument has fired.
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

# THE one endpoint, a literal constant: no dynamic URL construction anywhere in this file.
CHAT_URL = "https://openrouter.ai/api/v1/chat/completions"
ALLOWLIST_SCHEMES = {"https"}
ALLOWLIST_HOSTS = {"openrouter.ai"}


class _GuardedRedirect(urllib.request.HTTPRedirectHandler):
    """Redirects must re-pass the same guard or the request dies (anti-rebinding)."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        _guard(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _guard(url: str) -> None:
    u = urlparse(url)
    if u.scheme not in ALLOWLIST_SCHEMES or u.hostname not in ALLOWLIST_HOSTS:
        raise ValueError(f"blocked non-allowlisted URL: scheme={u.scheme} host={u.hostname}")


_guard(CHAT_URL)
_OPENER = urllib.request.build_opener(_GuardedRedirect)

KEY_ENVS = ("OPENROUTER_API_KEY", "OPENROUTER_API_KEY_2", "OR_API_KEY", "OR_API_KEY_2")
PROMPT = "Reply with the single word: ALIVE"
COOL_SPACING_S = 4.0
HEAT_WAVES = 3
TIMEOUT_S = 45

ROSTER = [
    "cohere/north-mini-code:free",
    "stealth/space-bunny-alpha",
    "nvidia/nemotron-3.5-lightning:free",
    "liquid/lfm-2.5-2.6b:free",
    "poolside/laguna-xs-2.1:free",
    "dots-studio/dots-3-note-preview:free",
    "inclusionai/ling-3.0-flash-fin:free",
    "inclusionai/ling-3.0-flash-sante:free",
    "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "nvidia/nemotron-3-ultra-550b-a55b:free",
    "nvidia/nemotron-3.5-content-safety:free",
    "poolside/laguna-s-2.1:free",
]

HERE = Path(__file__).resolve().parent
OUT = HERE / "probe_results.jsonl"


def key() -> str:
    for name in KEY_ENVS:
        v = os.environ.get(name)
        if v and v.strip():
            return v.strip()
    env = Path(__file__).resolve().parents[3] / ".env"
    if env.is_file():
        for line in env.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if line.startswith(f"{KEY_ENVS[0]}="):
                v = line.split("=", 1)[1].strip().strip('"')
                if v:
                    return v
    raise SystemExit("no OpenRouter key in env or .env")


def fire(model: str, phase: str, wave: int) -> dict:
    body = json.dumps({"model": model,
                       "messages": [{"role": "user", "content": PROMPT}],
                       "max_tokens": 16}).encode("utf-8")
    req = urllib.request.Request(
        CHAT_URL, data=body,
        headers={"Authorization": f"Bearer {key()}", "Content-Type": "application/json",
                 "HTTP-Referer": "https://localhost.local/mag-r06-probe",
                 "X-Title": "mag-r06-probe"})
    row = {"phase": phase, "wave": wave, "model": model,
           "ts": datetime.now(timezone.utc).isoformat()}
    try:
        with _OPENER.open(req, timeout=TIMEOUT_S) as r:
            data = json.loads(r.read().decode("utf-8"))
        msg = ((data.get("choices") or [{}])[0].get("message") or {})
        row.update({"http": 200,
                    "ok": bool((msg.get("content") or "").strip()),
                    "content_head": (msg.get("content") or "").strip()[:60],
                    "finish": (data.get("choices") or [{}])[0].get("finish_reason")})
    except urllib.error.HTTPError as e:
        detail = ""
        try:
            detail = e.read().decode("utf-8", errors="replace")[:200]
        except Exception:
            pass
        row.update({"http": e.code, "ok": False, "content_head": "", "finish": None,
                    "detail": detail})
    except Exception as e:                                   # transport failure is an outcome
        row.update({"http": None, "ok": False, "content_head": "", "finish": None,
                    "detail": f"{type(e).__name__}: {e}"})
    return row


def main() -> None:
    rows: list[dict] = []
    # COOL: width 1, sequential, spaced.
    for i, model in enumerate(ROSTER):
        if i:
            time.sleep(COOL_SPACING_S)
        row = fire(model, "cool", 1)
        rows.append(row)
        print(f"cool  {model:55s} http={row['http']} ok={row['ok']}")
        OUT.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    # HEAT: full roster in parallel, zero spacing, 3 waves.
    for wave in range(1, HEAT_WAVES + 1):
        with ThreadPoolExecutor(max_workers=len(ROSTER)) as ex:
            futs = [ex.submit(fire, m, "heat", wave) for m in ROSTER]
            for fut in as_completed(futs):
                row = fut.result()
                rows.append(row)
                print(f"heat  w{wave} {row['model']:50s} http={row['http']} ok={row['ok']}")
        OUT.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    # Summary, every outcome classed (the honest census the banked caveat asked for).
    cool = [r for r in rows if r["phase"] == "cool"]
    heat = [r for r in rows if r["phase"] == "heat"]
    summary = {
        "moment": datetime.now(timezone.utc).isoformat(),
        "cool_asks": len(cool), "cool_200_ok": sum(1 for r in cool if r["ok"]),
        "cool_429": sum(1 for r in cool if r["http"] == 429),
        "cool_other_fail": sum(1 for r in cool if r["http"] != 429 and not r["ok"]),
        "heat_asks": len(heat), "heat_200_ok": sum(1 for r in heat if r["ok"]),
        "heat_429": sum(1 for r in heat if r["http"] == 429),
        "heat_other_fail": sum(1 for r in heat if r["http"] != 429 and not r["ok"]),
        "peak_instant_width": len(ROSTER),
        "heat_429_models": sorted({r["model"] for r in heat if r["http"] == 429}),
    }
    print(json.dumps(summary, indent=2))
    (HERE / "probe_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
