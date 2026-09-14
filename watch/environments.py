#!/usr/bin/env python3
"""environments.py — THE HYPERVISOR registry (2026-08-29): every environment
the fleet runs on, one file. Fuses:
  - docker containers (docker ps)
  - desktop seats (calls watch/seats.py)
  - API lanes + plans (from .env key presence + fleet-known state)
  - vast (covenant gate + last buyer log line)
  - local hardware (desk GPU known-unwired)
Writes watch/environments.json. Run-once, no daemon.
"""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "watch" / "environments.json"


def containers() -> list[dict]:
    try:
        r = subprocess.run(["docker", "ps", "-a", "--format",
                            "{{json .}}"], capture_output=True, text=True, timeout=20)
        rows = []
        for line in r.stdout.splitlines():
            if not line.strip():
                continue
            try:
                c = json.loads(line)
            except json.JSONDecodeError:
                continue
            rows.append({"name": c.get("Names"), "state": c.get("State"),
                         "status": c.get("Status"), "image": c.get("Image")})
        return rows
    except Exception as e:  # noqa: BLE001
        return [{"name": "docker-unreachable", "state": "error", "status": str(e)[:80]}]


def seats() -> dict:
    try:
        subprocess.run(["python", str(ROOT / "watch" / "seats.py")],
                       capture_output=True, text=True, timeout=20)
        p = ROOT / "watch" / "seats.json"
        return json.loads(p.read_text(encoding="utf-8")).get("seats", {})
    except Exception:  # noqa: BLE001
        return {}


def lanes() -> list[dict]:
    env = {}
    env_path = ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8", errors="replace").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    have = lambda *ks: any(env.get(k) for k in ks)  # noqa: E731
    return [
        {"lane": "z_ai free (4.7/4.5-flash)", "kind": "api-key",
         "state": "ok (harness-only: coding keys refuse raw API)",
         "keys": sum(1 for k in ("ZAI_API_KEY", "ZAI_API_KEY_2") if env.get(k))},
        {"lane": "zcode plan A (Pro key)", "kind": "coding-plan",
         "state": "BURNED 08-29 (1305 wall; standing swarm grind) — resets Sep 1",
         "keys": sum(1 for k in ("ZAI_API_KEY_Pro",) if env.get(k))},
        {"lane": "zcode plan B (Lite key)", "kind": "coding-plan",
         "state": "live — judgment seat (this window, spend gently)",
         "keys": sum(1 for k in ("ZAI_API_KEY_Lite",) if env.get(k))},
        {"lane": "deepseek (flash+pro)", "kind": "api-key",
         "state": "ok — pennies, the Watcher + JIT + night cadence ride here",
         "keys": sum(1 for k in ("DEEPSEEK_API_KEY",) if env.get(k))},
        {"lane": "grok/xai + groq + openrouter + together", "kind": "api-key",
         "state": "keys present — free-tier pool (groq daily cap applies)",
         "keys": sum(1 for k in ("XAI_API_KEY", "GROK_API_KEY", "GROK_API_KEY_2",
                                 "GROQ_API_KEY", "GROQ_API_KEY_2",
                                 "OPENROUTER_API_KEY", "OPENROUTER_API_KEY_2",
                                 "TOGETHER_API_KEY") if env.get(k))},
        {"lane": "vast.ai blades", "kind": "gpu-rental",
         "state": "GATED (buyer_enabled=false, operator GO pending; 7-template registry ready; balance $33.18)",
         "keys": 1 if env.get("VASTAI_API_KEY") else 0},
        {"lane": "desk GPU RX 5600 XT", "kind": "local-hardware",
         "state": "unwired (CPU-only ollama; ROCm experiment pending)"},
        {"lane": "local ollama (docker)", "kind": "local-model",
         "state": "container mag-ollama up — qwen3:8b resident"},
    ]


def main() -> int:
    doc = {
        "schema": "environments.v1",
        "ts": datetime.now(timezone.utc).isoformat(),
        "containers": containers(),
        "seats": seats(),
        "lanes": lanes(),
    }
    OUT.write_text(json.dumps(doc, indent=1), encoding="utf-8")
    up = sum(1 for c in doc["containers"] if c.get("state") == "running")
    print(json.dumps({"containers_up": up, "lanes": len(doc["lanes"]),
                      "seats": len(doc["seats"])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
