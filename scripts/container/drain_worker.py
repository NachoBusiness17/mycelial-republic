"""Bounded swarm-drain worker — runs INSIDE the mag-worker container (2026-08-27).

The sane-container doctrine: no loose host pythons. This replaces background bash
drain beats that die with sessions or spin unbounded. Every beat is limited;
state/worker.off pauses it without docker commands (operator off-switch).

Env knobs:
  WORKER_BEAT   tasks per beat  (default 8)
  WORKER_SLEEP  seconds between beats (default 45)
"""
import json
import multiprocessing as mp
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, "/app")

LIMIT = int(os.environ.get("WORKER_BEAT", "8"))
SLEEP = int(os.environ.get("WORKER_SLEEP", "45"))
OFF_FLAG = "/app/state/worker.off"
HEARTBEAT = Path(os.environ.get("WORKER_HEARTBEAT", "/app/state/worker_heartbeat.json"))
MAX_BEAT_SECONDS = int(os.environ.get("WORKER_MAX_BEAT_SECONDS", "600"))


def _operator_pause_reason() -> str | None:
    """Read the shared control plane; remain compatible with old images."""
    try:
        from mag.operator_mode import pause_reason

        return pause_reason()
    except Exception:
        return None


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _heartbeat(beat: int, phase: str, **extra: object) -> None:
    """Write the worker's durable liveness surface atomically.

    The worker has no HTTP server by design. Docker health therefore reads this
    receipt instead of probing the dashboard process that lives in another
    container.
    """
    try:
        HEARTBEAT.parent.mkdir(parents=True, exist_ok=True)
        payload = {"schema": "worker_heartbeat.v1", "beat": beat,
                   "phase": phase, "updated_at": _now(), **extra}
        tmp = HEARTBEAT.with_suffix(".tmp")
        tmp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        tmp.replace(HEARTBEAT)
    except Exception as e:  # noqa: BLE001 — telemetry must never kill the worker
        print(f"[heartbeat] write failed: {type(e).__name__}: {str(e)[:100]}", flush=True)


def _drain_child(limit: int, result_queue: object) -> None:
    """Run one drain in an isolated child so a hung beat can be terminated."""
    try:
        from mag.swarm_local_drain import drain_pass
        out = drain_pass(limit=limit)
        summary = {k: v for k, v in (out or {}).items() if k != "results"}
        result_queue.put({"ok": bool((out or {}).get("ok")), "out": summary})
    except Exception as e:  # noqa: BLE001 — parent records the failed beat
        result_queue.put({"ok": False, "error": f"{type(e).__name__}: {str(e)[:160]}"})


def _run_bounded(limit: int, timeout: int) -> dict[str, object]:
    """Run a beat with a real wall-clock ceiling, terminating a stuck child."""
    methods = mp.get_all_start_methods()
    ctx = mp.get_context("fork" if "fork" in methods else methods[0])
    result_queue = ctx.Queue(maxsize=1)
    proc = ctx.Process(target=_drain_child, args=(limit, result_queue), daemon=True)
    proc.start()
    proc.join(timeout=max(1, timeout))
    if proc.is_alive():
        proc.terminate()
        proc.join(10)
        return {"ok": False, "timed_out": True,
                "error": f"beat exceeded WORKER_MAX_BEAT_SECONDS={timeout}"}
    try:
        return result_queue.get_nowait()
    except Exception:
        return {"ok": False, "error": f"drain child exited without a result (exit={proc.exitcode})"}


def main() -> None:
    beat = 0
    _heartbeat(beat, "starting", max_beat_seconds=MAX_BEAT_SECONDS)
    print(f"drain worker up: beat={LIMIT} sleep={SLEEP}s max={MAX_BEAT_SECONDS}s", flush=True)
    while True:
        beat += 1
        pause_reason = _operator_pause_reason()
        if os.path.exists(OFF_FLAG) or pause_reason:
            _heartbeat(beat, "paused", reason=pause_reason or "state/worker.off present")
            print(f"[beat {beat}] paused ({pause_reason or 'state/worker.off present'})", flush=True)
            time.sleep(SLEEP)
            continue
        t0 = time.time()
        out: dict[str, object] = {}
        _heartbeat(beat, "draining", max_beat_seconds=MAX_BEAT_SECONDS)
        try:
            result = _run_bounded(LIMIT, MAX_BEAT_SECONDS)
            out = result.get("out") if isinstance(result.get("out"), dict) else result
            shown = json.dumps({k: out[k] for k in out if k != "results"}, default=str)[:300]
            print(f"[beat {beat}] ok={out.get('ok')} {shown}", flush=True)
        except Exception as e:  # noqa: BLE001 — never die on one bad beat
            print(f"[beat {beat}] error {type(e).__name__}: {str(e)[:160]}", flush=True)
        elapsed = time.time() - t0
        _heartbeat(beat, "sleeping", elapsed_seconds=round(elapsed, 2),
                   ok=bool(out.get("ok")) if isinstance(out, dict) else False)
        if elapsed > MAX_BEAT_SECONDS:
            print(f"[beat {beat}] WARN beat took {elapsed:.0f}s", flush=True)
            continue  # beat already used its full budget — do not add sleep
        time.sleep(SLEEP)


if __name__ == "__main__":
    main()
