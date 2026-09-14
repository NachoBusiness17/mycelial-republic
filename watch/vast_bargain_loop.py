"""vast_bargain_loop — always-on $0 bargain watcher + auto-buy (operator order 2026-08-27).

Replaces the ZCode cron (premium tokens must touch judgment only — polling is bulk).
Runs headless via the VBS/schtask pattern (watch/vast_bargain_loop.vbs). Every
POLL_SECONDS: one cheap API probe. Silent unless a bargain crosses the CRAZY-GOOD
bar, in which case: auto-launch (rails below) + CONVO row + alert file for the
phone surface. No webhooks exist on vast's side — this loop IS our async edge.

Rails (unchanged, mandatory): one live instance max, credit > $10 to buy,
destroy never automated, launch fails twice = stop and alert.

SSRF hardening (Mimosa): every request goes through _vast_get/_vast_put — the
host is the literal console.vast.ai constant (no redirects allowed), and any
path parameter must be a plain int. Data from API responses never reaches a URL
unvalidated.
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "state" / "vast"))

from launch_vast import _h, balance  # noqa: E402

POLL_SECONDS = 180
OUT = ROOT / "state" / "vast" / "market_watch.jsonl"
ALERT = ROOT / "state" / "vast" / "BARGAIN_ALERT.txt"
CONVO = ROOT / "queue" / "handoff" / "zcode" / "CONVO.md"
HEARTBEAT = ROOT / "state" / "vast" / "loop.heartbeat"  # touched EVERY pass
VAST_HOST = "https://console.vast.ai"  # literal, the ONLY host this loop talks to

# CRAZY-GOOD bar
REL_MIN, GPU_RAM_MIN, CPU_RAM_MIN, DISK_MIN = 0.98, 24000, 90000, 150
PRICE_FLOOR_STD = 0.12   # <= $0.12/hr on the standard class
BIG_VRAM, PRICE_FLOOR_BIG = 48000, 0.40  # or >=48GB VRAM at <= $0.40/hr

# BUY ARMING (operator order 2026-08-27 ~16:1xZ: watch ~24h FIRST — a full-day feed
# is what makes "crazy good" a measured percentile instead of a guess). While False
# the loop only records; flipping to True restores the auto-buy rails below.
BUY_ARMED = False


def _vast_get(path: str, param: int | None = None) -> dict:
    """GET a fixed path on the literal vast host; param must be an int if present."""
    url = f"{VAST_HOST}{path}" + (f"?id={int(param)}" if param is not None else "")
    r = requests.get(url, headers=_h(), timeout=60, allow_redirects=False)
    if r.status_code != 200:
        raise RuntimeError(f"vast GET {path} -> {r.status_code}")
    return r.json()


def _vast_put_instance(bundle_id: int, body: dict) -> requests.Response:
    """PUT instance create; bundle_id forced int; fixed path; no redirects."""
    url = f"{VAST_HOST}/api/v0/instances/?id={int(bundle_id)}"
    return requests.put(url, headers=_h(), data=json.dumps(body), timeout=60,
                        allow_redirects=False)


def log(msg: str) -> None:
    line = f"[vast-loop {datetime.now(timezone.utc).isoformat(timespec='seconds')}] {msg}"
    print(line, flush=True)
    with (ROOT / "state" / "vast" / "loop.log").open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def is_crazy_good(x: dict) -> bool:
    if (x.get("reliability2") or 0) < REL_MIN: return False
    if (x.get("gpu_ram") or 0) < GPU_RAM_MIN: return False
    if (x.get("cpu_ram") or 0) < CPU_RAM_MIN: return False
    if (x.get("disk_space") or 0) < DISK_MIN: return False
    dph = x.get("dph_total") or 99
    if (x.get("gpu_ram") or 0) >= BIG_VRAM: return dph <= PRICE_FLOOR_BIG
    return dph <= PRICE_FLOOR_STD


def one_pass() -> None:
    HEARTBEAT.write_text(datetime.now(timezone.utc).isoformat(timespec="seconds"), encoding="utf-8")
    offers = _vast_get("/api/v0/bundles/")["offers"]
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    hit = [x for x in offers if x.get("rentable") and is_crazy_good(x)]
    with OUT.open("a", encoding="utf-8") as fh:
        best = sorted((x for x in offers if x.get("rentable")),
                      key=lambda x: x.get("dph_total") or 99)[:3]
        fh.write(json.dumps({"ts": now, "credit": round(balance(), 2),
                             "bargains": [int(x["id"]) for x in hit],
                             "best": [{"id": int(x["id"]), "gpu": x.get("gpu_name"),
                                       "dph": round(x.get("dph_total") or 0, 3)} for x in best]},
                            ensure_ascii=False) + "\n")
    if not hit:
        return
    if not BUY_ARMED:
        log(f"bargain SEEN (watch-only): "
            + ", ".join(f"{x.get('gpu_name')} ${x.get('dph_total'):.3f}" for x in hit[:3]))
        ALERT.write_text(f"watch-only bargain seen: {[x['id'] for x in hit]}\n", encoding="utf-8")
        return
    # rails before buy
    if balance() < 10:
        log("bargain seen but credit < $10 — no buy"); return
    if _vast_get("/api/v0/instances/").get("instances"):
        log("bargain seen but an instance already lives — no buy"); return
    target = sorted(hit, key=lambda x: x.get("dph_total") or 99)[0]
    body = {"client_id": "zcode_rehearsal", "image": "ollama/ollama:latest",
            "disk": 40, "label": "sancho-rehearsal",
            "env": {"OLLAMA_HOST": "0.0.0.0:11434"}}
    for attempt in (1, 2):
        r = _vast_put_instance(int(target["id"]), body)
        if r.status_code in (200, 201):
            receipt = (f"[vast-loop {now}] BARGAIN BOUGHT: id {target['id']} "
                       f"{target.get('gpu_name')} {target.get('geolocation')} "
                       f"${target.get('dph_total'):.3f}/hr rel {target.get('reliability2')} "
                       f"attempts={attempt}")
            log(receipt); CONVO.open("a", encoding="utf-8").write(receipt + "\n")
            ALERT.write_text(receipt + "\n", encoding="utf-8")
            return
        log(f"launch attempt {attempt} failed: {r.status_code} {r.text[:150]}")
    log("two launch failures — stopping buys, alerting")
    ALERT.write_text(f"launch failed twice on bargain id {target['id']} — manual look\n",
                     encoding="utf-8")


if __name__ == "__main__":
    # Schtask-shaped: each trigger runs ONE pass and exits (Task Scheduler kills
    # child trees when the action exits, so a while-True daemon cannot live here —
    # learned 16:1xZ 2026-08-27 after three silent single-pass deaths). The cron
    # cadence IS the heartbeat; no singleton guard needed (runtime << interval).
    if "--once" not in sys.argv:
        sys.exit("run with --once via the schtask; the while-True form needs a real daemon home (docker)")
    log("pass start")
    try:
        one_pass()
    except Exception as e:  # noqa: BLE001 — a watcher never dies on one bad pass
        log(f"pass error: {str(e)[:200]}")
