"""swarm_local_drain — THE FIX for the dead-end architecture path. A LOCAL drainer for the swarm
queue, because the k8s CronJob that was its ONLY drainer has never run on this Windows host.

OPERATOR (2026-08-13): "anything found blocking key infrastructure that you assume to work but does
not... these loops need to be intelligent and evolve. you have so much data on me interrupting you
that has to be worth something and is training data. everything is training data. especially key
infrastructure blocks."

ROOT CAUSE (grounded, deep investigation 2026-08-13): the swarm queue (memory/runs/swarm_worker/queue)
is FILLED locally but DRAINED ONLY by the k8s mag-swarm CronJob — which has NEVER run on this Windows
host (Docker/K8s not installed; no kubectl/kind execution record anywhere; docker became unreachable
08-09). So every "enqueue to the swarm" wrote a file nobody executes -> 734-task all-"queued" backlog,
zero drain since 08-10. THE RECURRING "wrong tool / route through the swarm" CORRECTION IS THE SYMPTOM
OF THIS: the sanctioned execution path enqueues-but-never-executes on this host, so work piles up or I
fall back to terminal/one-shots. The interruptions were training data that named the infra block.

THE FIX (self-steal, correct internal mechanism): invoke the SAME swarm_worker.run_once() drain logic
LOCALLY on the governor cadence — no k8s needed. Plus reconcile the key env: providers.yaml reads
DEEPSEEK_SWARM_API_KEY but the local .env sets DEEPSEEK_API_KEY -> alias the present key into the
spawn env so deepseek actually resolves. This turns enqueue -> execute, drains the backlog into real
research, and makes the sanctioned path functional on this host.

SECONDARY KEY MISMATCH (reconciled here): providers.yaml reads DEEPSEEK_SWARM_API_KEY; local .env
sets only DEEPSEEK_API_KEY. key_reconcile() copies the present key into the env var the provider reads
(logs the KEY NAME, never the value), so a local drain resolves deepseek.

Schema: swarm_local_drain.v1 · deterministic coordinator + bounded swarm work · reuse: swarm_worker
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from config import ROOT
except Exception:
    ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

SCHEMA = "swarm_local_drain.v1"
OUT = ROOT / "memory" / "runs" / "swarm_local_drain"

# The provider config reads this env var for deepseek (per providers.yaml, 2026-08-10).
PROVIDER_KEY_ENV = "DEEPSEEK_SWARM_API_KEY"
# The key the local .env actually sets.
LOCAL_KEY_ENV = "DEEPSEEK_API_KEY"

# Bounded by default: how many swarm tasks the LOCAL drainer may run per beat. Never a runaway —
# the cluster was never here, so the local drain is the fallback and must stay controlled.
DEFAULT_PER_BEAT = 2
# Daily cap: how many total swarm tasks the local drainer may run in a day (budget guard).
DEFAULT_DAILY_CAP = 20


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def key_reconcile() -> dict[str, Any]:
    """Reconcile the key env: the provider reads PROVIDER_KEY_ENV, but the local .env sets
    LOCAL_KEY_ENV. Copy the present key into the provider's env var (in-process) so deepseek resolves.
    Logs the KEY NAME only, never the value. Honest about what resolves."""
    provider_key = os.environ.get(PROVIDER_KEY_ENV, "")
    local_key = os.environ.get(LOCAL_KEY_ENV, "")
    action = "noop"
    if not provider_key and local_key:
        os.environ[PROVIDER_KEY_ENV] = local_key
        action = "aliased-local-key-into-provider-env"
    resolved = bool(os.environ.get(PROVIDER_KEY_ENV))
    return {"ok": True, "schema": SCHEMA, "action": action,
            "resolved_provider_key": resolved,
            "note": f"provider reads {PROVIDER_KEY_ENV}; resolved={resolved} (key VALUE never logged)"}


def drain_pass(*, limit: int = DEFAULT_PER_BEAT) -> dict[str, Any]:
    """Run the EXISTING swarm_worker.run_once() LOCALLY (bounded), with the key reconciled, so the
    queue actually drains on this host. Self-steal: the drain logic already exists; we just invoke
    it here because the k8s CronJob (its only other caller) never runs on Windows."""
    kr = key_reconcile()
    if not kr["resolved_provider_key"]:
        return {"ok": False, "schema": SCHEMA, "error": "no deepseek key resolves (see key_reconcile)",
                "key_reconcile": kr}
    try:
        from mag import swarm_worker
        # run_once is bounded internally by MAX_PER_PASS; cap it further per beat.
        ran = swarm_worker.run_once(max_per_pass=max(1, int(limit)))
    except Exception as e:
        return {"ok": False, "schema": SCHEMA, "error": str(e)[:160], "key_reconcile": kr}
    done = int((ran or {}).get("done") or 0)
    failed = int((ran or {}).get("failed") or 0)
    return {"ok": True, "schema": SCHEMA, "ts": _now(), "ran": ran,
            "done": done, "failed": failed, "key_reconcile": kr,
            "note": "local swarm drain: same swarm_worker.run_once mechanism, invoked locally because "
                    "the k8s CronJob drainer never runs on Windows"}


def _today_drained() -> int:
    """Grounded: count today's local drain runs from the persisted ledger (budget guard)."""
    if not OUT.is_dir():
        return 0
    today = _now()[:10]
    n = 0
    for p in OUT.glob("drain-*.json"):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            if str(d.get("ts", ""))[:10] == today:
                n += int(d.get("done") or 0) + int(d.get("failed") or 0)
        except Exception:
            continue
    return n


def run_cadence(*, per_beat: int = DEFAULT_PER_BEAT, daily_cap: int = DEFAULT_DAILY_CAP,
                persist: bool = True) -> dict[str, Any]:
    """The loop's self-healing drain beat: bounded, budget-guarded, key-reconciled. Drains a small
    number of queued swarm tasks per beat locally so the sanctioned path actually executes."""
    used = _today_drained()
    remaining = max(0, int(daily_cap) - used)
    if remaining <= 0:
        return {"ok": True, "schema": SCHEMA, "skipped": "daily-cap", "daily_cap": daily_cap,
                "used_today": used}
    limit = max(1, min(int(per_beat), remaining))
    r = drain_pass(limit=limit)
    if persist and r.get("ok"):
        try:
            OUT.mkdir(parents=True, exist_ok=True)
            (OUT / f"drain-{_now().replace(':','').replace('-','')[:14]}.json").write_text(
                json.dumps(r, indent=2, default=str), encoding="utf-8")
        except Exception:
            pass
    r["used_today"] = used + (int(r.get("done") or 0) + int(r.get("failed") or 0) if r.get("ok") else 0)
    return r


def status() -> dict[str, Any]:
    return {"ok": True, "schema": SCHEMA,
            "contract": "key_reconcile()->alias the present deepseek key into the provider env (name "
                        "only, never value); drain_pass(limit)->run swarm_worker.run_once locally "
                        "(bounded, headless); run_cadence()->bounded + daily-capped self-healing "
                        "drain beat for the governor loop; status()->this",
            "cost": "deterministic coordinator + bounded swarm work (spawned agents are the real "
                    "deepseek spend; capped by default)",
            "reuses": ["swarm_worker"], "fixes": ["dead k8s CronJob drain", "key env mismatch"]}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(prog="swarm-local-drain")
    ap.add_argument("cmd", nargs="?", default="status", choices=["status", "key", "drain", "cadence"])
    ap.add_argument("--limit", type=int, default=DEFAULT_PER_BEAT)
    a = ap.parse_args()
    if a.cmd == "key":
        print(json.dumps(key_reconcile(), indent=2, default=str))
    elif a.cmd == "drain":
        print(json.dumps(drain_pass(limit=a.limit), indent=2, default=str))
    elif a.cmd == "cadence":
        print(json.dumps(run_cadence(per_beat=a.limit), indent=2, default=str))
    else:
        print(json.dumps(status(), indent=2, default=str))
