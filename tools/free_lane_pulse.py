#!/usr/bin/env python3
"""tools/free_lane_pulse.py - Dynamic Free Fleet Autopilot & Model-Level Liveness Probe.

Discovers, probes, and ranks free-tier model lanes across OpenRouter and Nous Research:
- Dynamically queries provider catalogs for active free-tier endpoints.
- Runs concurrent 1-token health probes with strict 5-second timeouts.
- Classifies models into:
    ALIVE (HTTP 200, valid latency, ready for dispatch)
    RATE_LIMITED (HTTP 429, temporary backoff)
    DEAD_OR_ROTATED (HTTP 404/400, model rotated out)
- Caches live ranked roster to state/live_free_roster.json.
- Provides get_live_free_models() for zero-404 dispatch in Task Wall and Same Book.

CONSUMER: tools/task_wall.py, tools/hermes_burn.py, Same Book wave runners.
VERIFIER: tests/test_free_lane_pulse.py.
HOUSE LAW: Strictly zero unicode em-dashes; pure functions where possible; zero spend.
"""
from __future__ import annotations

import concurrent.futures
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

STATE_PATH = os.path.join(ROOT, "state", "live_free_roster.json")
ENV_PATH = os.path.join(ROOT, ".env")


def load_env_keys(path: str = ENV_PATH) -> Dict[str, str]:
    """Parse environment keys from .env safely without printing values."""
    keys = {}
    if not os.path.exists(path):
        return keys
    with open(path, "r", encoding="utf-8", errors="ignore") as fp:
        for line in fp:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                keys[k.strip()] = v.strip().strip("\"'").strip()
    return keys


def fetch_openrouter_free_candidates(api_key: str) -> List[str]:
    """Retrieve list of free-tier models from OpenRouter catalog API."""
    if not api_key:
        return []
    url = "https://openrouter.ai/api/v1/models"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {api_key}"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return [
                m["id"] for m in data.get("data", [])
                if m.get("pricing", {}).get("prompt") == "0"
            ]
    except Exception:
        return []


def probe_single_model(
    endpoint: str,
    api_key: str,
    model_id: str,
    timeout: float = 5.0
) -> Dict[str, Any]:
    """Perform a 1-token liveness ping against a specific model endpoint."""
    t0 = time.time()
    body = {
        "model": model_id,
        "messages": [{"role": "user", "content": "ping"}],
        "max_tokens": 1
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        data=data
    )
    
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            lat = time.time() - t0
            res = json.loads(resp.read().decode("utf-8"))
            status = "ALIVE" if res.get("choices") else "EMPTY_CHOICES"
            return {
                "model_id": model_id,
                "status": status,
                "latency_sec": round(lat, 3),
                "http_code": resp.getcode()
            }
    except urllib.error.HTTPError as e:
        lat = time.time() - t0
        status = "RATE_LIMITED" if e.code == 429 else "DEAD_OR_ROTATED"
        return {
            "model_id": model_id,
            "status": status,
            "latency_sec": round(lat, 3),
            "http_code": e.code
        }
    except Exception as e:
        lat = time.time() - t0
        return {
            "model_id": model_id,
            "status": "TIMEOUT_OR_NET_ERR",
            "latency_sec": round(lat, 3),
            "http_code": None,
            "error_hint": str(e)
        }


def run_fleet_pulse(max_workers: int = 8) -> Dict[str, Any]:
    """Run full concurrent pulse across Nous Beam and OpenRouter free lanes."""
    env = load_env_keys()
    openrouter_key = env.get("OPENROUTER_API_KEY") or env.get("OPENROUTER_API_KEY_2", "")
    nous_key = env.get("HERMES_API_KEY_1") or env.get("HERMES_API_KEY_2", "")
    
    tasks: List[Tuple[str, str, str]] = []
    
    # 1. Nous Beam free week
    if nous_key:
        tasks.append((
            "https://inference-api.nousresearch.com/v1/chat/completions",
            nous_key,
            "reflection/beam-1.0-501b-a23b:free"
        ))
        
    # 2. OpenRouter free catalog candidates
    if openrouter_key:
        or_models = fetch_openrouter_free_candidates(openrouter_key)
        # Select top candidates (limit to first 12 to bound concurrency)
        for m in or_models[:12]:
            tasks.append((
                "https://openrouter.ai/api/v1/chat/completions",
                openrouter_key,
                m
            ))
            
    results: List[Dict[str, Any]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {
            executor.submit(probe_single_model, ep, key, mid): mid
            for ep, key, mid in tasks
        }
        for future in concurrent.futures.as_completed(future_map):
            try:
                results.append(future.result())
            except Exception as e:
                mid = future_map[future]
                results.append({
                    "model_id": mid,
                    "status": "EXCEPTION",
                    "latency_sec": 999.0,
                    "http_code": None
                })
                
    # Sort alive models by latency
    alive = [r for r in results if r["status"] == "ALIVE"]
    alive.sort(key=lambda x: x["latency_sec"])
    
    rate_limited = [r for r in results if r["status"] == "RATE_LIMITED"]
    dead = [r for r in results if r["status"] in ("DEAD_OR_ROTATED", "TIMEOUT_OR_NET_ERR", "EXCEPTION")]
    
    payload = {
        "schema": "live_free_roster.v1",
        "updated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "alive_count": len(alive),
        "rate_limited_count": len(rate_limited),
        "dead_count": len(dead),
        "alive_ladder": alive,
        "rate_limited": rate_limited,
        "dead_or_rotated": dead
    }
    
    # Ensure state dir exists
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as fp:
        json.dump(payload, fp, indent=2)
        
    return payload


def get_live_free_models(min_alive: int = 1) -> List[Dict[str, Any]]:
    """Retrieve active list of alive free models from cached state, refreshing if stale."""
    if not os.path.exists(STATE_PATH):
        payload = run_fleet_pulse()
        return payload.get("alive_ladder", [])
        
    try:
        with open(STATE_PATH, "r", encoding="utf-8") as fp:
            data = json.load(fp)
            # Check staleness (refresh if older than 30 minutes)
            ts = data.get("updated_utc")
            if ts:
                updated = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                age_sec = (datetime.now(timezone.utc) - updated).total_seconds()
                if age_sec > 1800:
                    data = run_fleet_pulse()
            return data.get("alive_ladder", [])
    except Exception:
        return run_fleet_pulse().get("alive_ladder", [])


if __name__ == "__main__":
    print("Running free lane pulse across fleet...")
    res = run_fleet_pulse()
    print(f"Pulse complete at {res['updated_utc']}")
    print(f"Alive: {res['alive_count']} | 429: {res['rate_limited_count']} | Dead: {res['dead_count']}")
    print("\nAlive Ladder (Sorted by Latency):")
    for a in res["alive_ladder"]:
        print(f"  [ALIVE] {a['model_id']:45} {a['latency_sec']}s")
    if res["rate_limited"]:
        print("\nRate-Limited (Temporary):")
        for r in res["rate_limited"]:
            print(f"  [429]   {r['model_id']}")
    if res["dead_or_rotated"]:
        print("\nDead or Rotated:")
        for d in res["dead_or_rotated"][:5]:
            print(f"  [DEAD]  {d['model_id']} (HTTP {d.get('http_code')})")
