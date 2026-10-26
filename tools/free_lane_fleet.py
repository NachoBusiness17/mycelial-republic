#!/usr/bin/env python3
"""free_lane_fleet: the 24/7 free-lane burner (operator order 2026-10-05).

Live surfaces (2026-10-04 audit): OpenRouter :free x2 keys, Mistral, Cohere
free, NVIDIA NIM x2 keys, local Ollama; dead surfaces (Cerebras, Groq,
Together, Google keys) skip until re-provisioned. Driving-ladder law: free
lanes are a SENSING surface; outputs bank as ledger findings, never done or
trusted work; verification climbs to the funded tier.

Work sources, cheapest first:
  1. watch/inbox/free_lane_queue/*.json ask files ({id, kind, prompt,
     max_tokens?, schema?}); a dict schema rides the item, never hardcoded:
     openai seats fire response_format (json_schema), ollama format, cohere as-is.
  2. Probe battery: falsifier / amended_metric / probe candidate rows, the
     master store + stranded watch/inbox windows, newest first; banked-ok
     probe ids never refire.
  3. Corridor watch: the daily-mine frontier areas, one ask per cycle.

Laws carried: keys strip()ed at load (CSV_VERDICT_20261004.md); banked
strings pass _scrub (KEY_SCRUB_20261004.md); SSRF guard - urlopen sees only
the fixed PROVIDERS literals via a redirect-refusing opener (Mimosa
2026-10-05); retry never; dead providers skip per health.json after 5
consecutive fails. Usage: --cycle / --health / --check-liveness (ledger
>90 min stale exits 1, B2-465). Repo venv only, never bare python.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / "watch" / "inbox" / "free_lane_queue"
RUNS = ROOT / "memory" / "runs" / "free_lane_fleet"
LEDGER = RUNS / "ledger.jsonl"
HEALTH = RUNS / "health.json"
CANDIDATES = ROOT / "memory" / "percolator" / "candidates.jsonl"

scrub_re = re.compile(
    r"(sk-[A-Za-z0-9_-]{16,}|xai-[A-Za-z0-9]{16,}|AIza[A-Za-z0-9_-]{16,}|"
    r"gsk_[A-Za-z0-9]{16,}|nvapi-[A-Za-z0-9_-]{20,}|Bearer\s+[A-Za-z0-9_\-\.]{15,})")


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """SSRF guard half 2: a provider endpoint must never bounce us elsewhere."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_OPENER = urllib.request.build_opener(_NoRedirect())


def _scrub(text: str) -> str:
    # KEY_SCRUB_20261004 law: banked strings never carry credential shapes.
    return scrub_re.sub(lambda m: m.group(0)[:12] + "[REDACTED]", str(text or ""))


def _env(name: str) -> str:
    # CR law (CSV_VERDICT_20261004.md): the .env on this box once carried CRLF;
    # strip at load forever.
    for line in (ROOT / ".env").read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith(name + "="):
            return line.split("=", 1)[1].strip()
    return ""


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_health() -> dict:
    if HEALTH.exists():
        try:
            return json.loads(HEALTH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_health(h: dict) -> None:
    RUNS.mkdir(parents=True, exist_ok=True)
    HEALTH.write_text(json.dumps(h, indent=1), encoding="utf-8")


def bank(row: dict) -> None:
    RUNS.mkdir(parents=True, exist_ok=True)
    row["detail"] = _scrub(str(row.get("detail", "")))
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


# PROVIDERS ALIVE-sweep 2026-10-05: 7/7 healthy (ouroboros r2 row 5 A6 stamp).
PROVIDERS: list[dict] = [
    {"id": "openrouter-free-1", "kind": "openai",
     "url": "https://openrouter.ai/api/v1/chat/completions",
     "key_env": "OPENROUTER_API_KEY", "model": "inclusionai/ling-3.1-flash"},
    {"id": "openrouter-free-2", "kind": "openai",
     "url": "https://openrouter.ai/api/v1/chat/completions",
     "key_env": "OPENROUTER_API_KEY_2", "model": "liquid/lfm-2.5-2.6b:free"},
    {"id": "mistral", "kind": "openai",
     "url": "https://api.mistral.ai/v1/chat/completions",
     "key_env": "MISTRAL_API_KEY", "model": "open-mistral-nemo"},
    {"id": "cohere-free", "kind": "cohere",
     "url": "https://api.cohere.com/v2/chat",
     "key_env": "COHERE_API_KEY_FREE", "model": "command-r7b-12-2024"},
    {"id": "nvidia-1", "kind": "openai",
     "url": "https://integrate.api.nvidia.com/v1/chat/completions",
     "key_env": "NVIDIABuild", "model": "meta/llama-3.2-11b-vision-instruct"},
    {"id": "nvidia-2", "kind": "openai",
     "url": "https://integrate.api.nvidia.com/v1/chat/completions",
     "key_env": "NVIDIABuild2", "model": "meta/llama-3.2-11b-vision-instruct"},
    {"id": "ollama-local", "kind": "ollama",
     "url": "http://localhost:11434/api/generate",
     "key_env": "", "model": "qwen2.5:7b"},
]
# SSRF guard half 1: the only URLs urlopen may ever see, byte-exact.
_ALLOWED_URLS = frozenset(p["url"] for p in PROVIDERS)

CORRIDOR_AREAS = [
    "open and local language models",
    "quantization and compression",
    "agent memory and continuity",
    "kv cache and context engineering",
    "swarm orchestration and multi-agent failures",
    "finetuning and adaptation for small models",
    "inference efficiency and speculative decoding",
    "evals and self-improvement loops",
    # A4 (ouroboros r2 row 5): sense the fleet's own domain - this fold proved it.
    "fleet operations: schedulers, health checks, silent failure modes",
]


def corridor_ask(area: str) -> str:
    return (
        "SENSING PROBE (free lane, output banks as a finding, never as done work). "
        "Frontier corridor: " + area + ". From your own knowledge, name the single "
        "most load-bearing open question in this area RIGHT NOW for a fleet that runs "
        "small local models (2B-8B) plus cheap API lanes, and one concrete signal the "
        "fleet could measure this week to answer it. Two sentences maximum. "
        "No preamble, no markdown.")


def _banked_probe_ids() -> set[str]:
    # A1 (ouroboros r2 row 5, 2026-10-05): probes banked ok never refire (43 rows shared one id).
    done: set[str] = set()
    if not LEDGER.exists():
        return done
    try:
        for line in LEDGER.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
            except Exception:
                continue
            wid = str(r.get("work_id") or "")
            if r.get("ok") and wid.startswith("probe-"):
                done.add(wid)
    except Exception:
        return done
    return done


def probe_items(limit: int) -> list[dict]:
    # The percolator candidates owe falsifiable probes; free lanes pay for the
    # cheap first cut. A2 (ouroboros r2 row 5, 2026-10-05): also senses the
    # stranded watch/inbox/*/percolator_candidates.jsonl window files, newest
    # first, read-only; the sanctioned writer stays the only ingest door.
    done = _banked_probe_ids()
    out: list[dict] = []
    sources: list[tuple[str, Path]] = []
    inbox = ROOT / "watch" / "inbox"
    if inbox.exists():
        wins = [p for p in inbox.glob("*/percolator_candidates.jsonl") if p.is_file()]
        wins.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        sources.extend(("win:" + p.parent.name, p) for p in wins)
    sources.append(("master", CANDIDATES))
    for tag, pth in sources:
        if not pth.exists():
            continue
        try:
            rows = [json.loads(l) for l in pth.read_text(encoding="utf-8").splitlines() if l.strip()]
        except Exception:
            continue
        if tag == "master":
            rows = rows[-12:]
        for r in rows:
            # A3 (ouroboros r2 row 5, 2026-10-05): "probe" is the third
            # source; executor rows carry probe keys, not falsifier.
            key = next((k for k in ("falsifier", "amended_metric", "probe") if r.get(k)), "")
            fals = str(r[key]) if key else ""
            claim = str(r.get("claim") or r.get("title") or r.get("id") or "")
            if not (fals and claim):
                continue
            named = str(r.get("source") or r.get("id") or "")
            # Id-less rows (window rows carry none): content hash, never
            # positional - len(out) fallback ids deadlocked the pool (16:33Z fire).
            wid = "probe-" + (named[:48].replace(" ", "-") if named else "h-" + hashlib.sha1(
                (claim[:160] + "|" + fals[:160]).encode("utf-8")).hexdigest()[:16])
            if wid in done:
                continue
            out.append({
                "id": wid,
                "kind": "probe",
                "prompt": ("CHEAP PROBE FIRST CUT (free lane; banks as a finding row, judgment "
                    "climbs to the funded tier). Candidate claim: " + claim[:400] + " " + ("Probe"
                    if key == "probe" else "Falsifier") + ": " + fals[:400] + " Answer in <=4 "
                    "sentences: (1) is this falsifier executable with only local models and free "
                    "API lanes; (2) the cheapest concrete measurement that could kill or support "
                    "the claim this week; (3) the single confound to guard against. No preamble, "
                    "no markdown."),
            })
            if len(out) >= limit:
                return out
    return out


def queue_items() -> list[dict]:
    out: list[dict] = []
    if QUEUE.exists():
        for p in sorted(QUEUE.glob("*.json")):
            try:
                item = json.loads(p.read_text(encoding="utf-8"))
                if item.get("id") and item.get("prompt"):
                    out.append(item)
            except Exception:
                continue
    return out


def fire(p: dict, prompt: str, schema: dict | None = None) -> tuple[bool, str]:
    url = p["url"]
    if url not in _ALLOWED_URLS:  # defense in depth: literals only
        return False, "url not in fixed allowlist"
    if not url.startswith("https://") and not url.startswith("http://localhost:11434/"):
        return False, "scheme refused"
    key = _env(p["key_env"]) if p["key_env"] else ""
    if p["key_env"] and not key:
        return False, "no key in .env"
    if p["kind"] == "openai" or p["kind"] == "cohere":
        body_d: dict = {"model": p["model"], "stream": False,
                        "max_tokens": 700, "temperature": 0.3,
                        "messages": [{"role": "user", "content": prompt}]}
        # Schema door (comics lane 2026-10-07), keyed off the queue item:
        # openai seats get response_format (json_schema); cohere as-is.
        if schema is not None and p["kind"] == "openai":
            body_d["response_format"] = {"type": "json_schema", "json_schema": {
                "name": "spec", "strict": False, "schema": schema}}
        body = json.dumps(body_d).encode()
        headers = {"Content-Type": "application/json", "Authorization": "Bearer " + key}
    elif p["kind"] == "ollama":
        body_d = {"model": p["model"], "prompt": prompt, "stream": False,
                  "options": {"num_predict": 300, "temperature": 0.3}}
        if schema is not None:  # ollama native door: format = the schema
            body_d["format"] = schema
        body = json.dumps(body_d).encode()
        headers = {"Content-Type": "application/json"}
    else:
        return False, "unknown provider kind"
    req = urllib.request.Request(url, data=body, headers=headers)
    t0 = time.time()
    try:
        with _OPENER.open(req, timeout=90) as r:
            d = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return False, "HTTP " + str(e.code) + " " + str(e.reason)[:80]
    except Exception as e:
        return False, type(e).__name__ + ": " + str(e)[:80]
    dtms = int((time.time() - t0) * 1000)
    if p["kind"] == "ollama":
        text = str(d.get("response", ""))
    else:
        msg = (d.get("choices") or [{}])[0].get("message") or {}
        # d4 law (2026-10-04): empty content + reasoning_content banks, not
        # voids. Cohere v2 never takes the choices path (blocks sit on the
        # top-level message.content), so the join runs after the chain on
        # whichever path produced the list (arm-A a03/a04/a13 repr fix).
        content = (msg.get("content") or msg.get("reasoning_content")
                   or (d.get("message") or {}).get("content") or "")
        if isinstance(content, list):
            # Cohere v2 returns content blocks; join the text parts.
            content = " ".join(str(b.get("text", "")) for b in content
                               if isinstance(b, dict))
        text = str(content)
    if not text.strip():
        return False, "empty completion (" + str(dtms) + "ms)"
    return True, text.strip()[:1200]


def cycle(max_per_provider: int = 2) -> str:
    health = load_health()
    queue = queue_items()
    probes = probe_items(6)
    fired = 0
    banked_rows = 0
    for p in PROVIDERS:
        fails = int(health.get(p["id"], {}).get("consecutive_fails", 0))
        if fails >= 5:
            continue  # dead provider; re-provision at the console, then reset health
        work: list[tuple[str, str, dict | None]] = []
        while len(work) < max_per_provider and queue:
            item = queue.pop(0)
            sch = item.get("schema")
            work.append((str(item["id"]), str(item["prompt"]),
                         sch if isinstance(sch, dict) else None))
        if len(work) < max_per_provider:
            area = CORRIDOR_AREAS[fired % len(CORRIDOR_AREAS)]
            work.append(("corridor:" + area, corridor_ask(area), None))
        if len(work) < max_per_provider and probes:
            pr = probes[fired % len(probes)]
            work.append((pr["id"], pr["prompt"], None))
        for wid, prompt, schema in work:
            ok, out = fire(p, prompt, schema)
            fired += 1
            if ok:
                health[p["id"]] = {"consecutive_fails": 0, "last_ok": _now()}
                bank({"ts": _now(), "provider": p["id"], "model": p["model"],
                      "work_id": wid, "ok": True, "chars": len(out),
                      "schema": bool(schema), "detail": out})
                banked_rows += 1
            else:
                h = health.get(p["id"], {})
                h["consecutive_fails"] = int(h.get("consecutive_fails", 0)) + 1
                h["last_fail"] = _now()
                health[p["id"]] = h
                bank({"ts": _now(), "provider": p["id"], "model": p["model"],
                      "work_id": wid, "ok": False, "detail": out})
            time.sleep(1.0)
    # retire queue items that fired ok somewhere this cycle
    if QUEUE.exists():
        done_ids = set()
        if LEDGER.exists():
            cutoff = dt.datetime.now(dt.timezone.utc).timestamp() - 900
            for line in LEDGER.read_text(encoding="utf-8").splitlines()[-40:]:
                try:
                    r = json.loads(line)
                    ts = str(r.get("ts", "")).replace("Z", "+00:00")
                    if r.get("ok") and ts and dt.datetime.fromisoformat(ts).timestamp() >= cutoff:
                        done_ids.add(str(r.get("work_id")))
                except Exception:
                    continue
        for pth in list(QUEUE.glob("*.json")):
            try:
                if str(json.loads(pth.read_text(encoding="utf-8")).get("id")) in done_ids:
                    pth.unlink()
            except Exception:
                continue
    save_health(health)
    healthy = sum(1 for pid in [p["id"] for p in PROVIDERS]
                  if int(health.get(pid, {}).get("consecutive_fails", 0)) < 5)
    return f"FREE-LANE CYCLE: fired {fired}, banked {banked_rows} findings, providers healthy {healthy}/{len(PROVIDERS)}"


LIVENESS_MAX_AGE_MIN = 90  # hourly schtask; 90 min stale = 2+ fires went dark


def check_liveness() -> tuple[int, str]:
    # Ouroboros r2 row 1 remainder (2026-10-05), B2-465 no-START-stamp shape:
    # ledger >90 min stale while the hourly schtask owed 2+ fires is green-but-dead. Fail loudly.
    if not LEDGER.exists():
        return 1, "LIVENESS FAIL: no ledger at " + str(LEDGER)
    age_min = (time.time() - LEDGER.stat().st_mtime) / 60.0
    if age_min > LIVENESS_MAX_AGE_MIN:
        return 1, ("LIVENESS FAIL: ledger mtime age %.0f min exceeds %d min; "
                   "hourly MagFreeLaneFleet should have fired 2+ times since "
                   "the last bank" % (age_min, LIVENESS_MAX_AGE_MIN))
    return 0, "LIVENESS OK: ledger mtime age %.0f min (limit %d min)" % (age_min, LIVENESS_MAX_AGE_MIN)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cycle", action="store_true")
    ap.add_argument("--health", action="store_true")
    ap.add_argument("--check-liveness", action="store_true")
    a = ap.parse_args()
    if a.health:
        h = load_health()
        for p in PROVIDERS:
            print(p["id"], json.dumps(h.get(p["id"], {"consecutive_fails": 0})))
        return 0
    if a.cycle:
        print(cycle())
        return 0
    if a.check_liveness:
        code, msg = check_liveness()
        print(msg)
        return code
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
