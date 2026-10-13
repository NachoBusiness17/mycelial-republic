#!/usr/bin/env python3
"""Mag FastAPI backend — handles tool dispatch over HTTP.

The agent CLI (mag/agent_cli.py) makes HTTP requests to this server instead
of executing tools in-process. The backend owns the heavy lifting (filesystem,
shell, python sandbox) and returns a JSON Success/Failure envelope.

Run:
    python -m backend.server            # uvicorn on 127.0.0.1:8000
    python -m backend.server --port 9000
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterator

# Ensure project root on path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi import FastAPI, HTTPException, Request  # noqa: E402
from fastapi.responses import FileResponse, JSONResponse  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402
from pydantic import BaseModel, Field  # noqa: E402

from config import bind_host  # noqa: E402
from tools import TOOL_MAP, dispatch as tool_dispatch  # noqa: E402

DEFAULT_HOST = bind_host()
DEFAULT_PORT = 8000

app = FastAPI(
    title="Mag Tool Backend",
    description="HTTP tool dispatch for the Mag agent CLI.",
    version="1.0.0",
)


class RunTaskRequest(BaseModel):
    """Body for POST /run_task."""

    tool: str = Field(..., description="Tool name, e.g. read_file, run_shell")
    args: dict[str, Any] = Field(default_factory=dict, description="Tool arguments")


class RunTaskResponse(BaseModel):
    """Uniform Success/Failure envelope."""

    ok: bool
    tool: str
    result: dict[str, Any] | None = None
    error: str | None = None


@app.get("/health")
def health() -> dict[str, Any]:
    """Liveness probe."""
    return {
        "ok": True,
        "service": "mag-backend",
        "tools": sorted(TOOL_MAP),
        "version": "1.0.0",
        "semantic": "/healthz",  # process-up says nothing about health
    }


# --- Semantic health (/healthz) — Chair 6/D lane-3 finding -------------------
# /health is hardcoded {"ok": true}: process-up, not health. /healthz reads the
# tail of logs/failure_kb.jsonl (last ~2MB, no full scan) and grades the
# trailing hour: ok=false when >=10 http_tool_fail rows in 1h OR any critical
# tool failed in the last 15 min.
FAILURE_KB_PATH = ROOT / "logs" / "failure_kb.jsonl"
FAILURE_TAIL_BYTES = 2 * 1024 * 1024
FAILURE_KINDS = frozenset(
    {"tool_fail", "http_tool_fail", "warning", "collapse", "swarm_health", "guard_registry"}
)
CRITICAL_TOOLS = frozenset({"run_shell", "run_python", "write_file", "apply_patch", "fence_strike"})
HTTP_FAIL_OK_THRESHOLD = 10  # per hour
CRITICAL_WINDOW_MINUTES = 15


def _tail_rows(path: Path, max_bytes: int = FAILURE_TAIL_BYTES) -> Iterator[dict[str, Any]]:
    """Yield dict rows from the last ~max_bytes of a JSONL file. Cheap tail read."""
    try:
        size = path.stat().st_size
        with path.open("rb") as fh:
            if size > max_bytes:
                fh.seek(size - max_bytes)
                fh.readline()  # drop the partial line cut by the seek
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except Exception:  # noqa: BLE001 — corrupt tail row is not a crash
                    continue
                if isinstance(row, dict):
                    yield row
    except OSError:
        return


def _row_ts(row: dict[str, Any]) -> datetime | None:
    raw = row.get("ts")
    if not isinstance(raw, str) or not raw:
        return None
    try:
        ts = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    return ts


def semantic_health(path: Path = FAILURE_KB_PATH) -> dict[str, Any]:
    """Grade fleet health from the failure_kb tail (trailing hour)."""
    now = datetime.now(timezone.utc)
    hour_ago = now - timedelta(hours=1)
    crit_ago = now - timedelta(minutes=CRITICAL_WINDOW_MINUTES)
    http_fail_1h = 0
    tool_fail_1h = 0
    critical_failure_recent = False
    last_failure_dt: datetime | None = None
    for row in _tail_rows(path):
        ts = _row_ts(row)
        kind = row.get("kind")
        if kind not in FAILURE_KINDS:
            continue
        if ts is not None and (last_failure_dt is None or ts > last_failure_dt):
            last_failure_dt = ts
        if ts is None or ts < hour_ago:
            continue
        if kind == "http_tool_fail":
            http_fail_1h += 1
        elif kind == "tool_fail":
            tool_fail_1h += 1
        if kind in ("tool_fail", "http_tool_fail") and row.get("tool") in CRITICAL_TOOLS and ts >= crit_ago:
            critical_failure_recent = True
    # failure_kb records failures only — attempts are unobservable from this
    # surface, so the rate is null and counts stand in (per endpoint contract).
    tool_error_rate_1h: float | None = None
    ok = http_fail_1h < HTTP_FAIL_OK_THRESHOLD and not critical_failure_recent
    return {
        "ok": ok,
        "tool_error_rate_1h": tool_error_rate_1h,
        "tool_fail_1h": tool_fail_1h,
        "critical_failure_recent": critical_failure_recent,
        "http_tool_fail_1h": http_fail_1h,
        "last_failure_ts": last_failure_dt.isoformat() if last_failure_dt else None,
        "window": {"hours": 1, "critical_minutes": CRITICAL_WINDOW_MINUTES, "tail_bytes": FAILURE_TAIL_BYTES},
    }


@app.get("/healthz")
def healthz() -> JSONResponse:
    """Semantic health — is the fleet actually working, not just up.

    200 when healthy, 503 on breach (>=10 http_tool_fail/1h or a critical
    tool failed in the last 15 min). Body carries the same detail either way,
    so monitors may grade the body, but the status code is the gate signal —
    a monitor that only checks the code still catches a breach.
    """
    report = semantic_health()
    return JSONResponse(status_code=200 if report["ok"] else 503, content=report)
# -----------------------------------------------------------------------------


@app.post("/api/v1/cast/launch")
def cast_launch() -> dict[str, Any]:
    """APPROVAL-FREE launch of the LAN voice/dashboard server (the operator's 'just do shit' — the
    op is a REST route the backend executes, never a terminal prompt). Spawns the cast server
    headless (CREATE_NO_WINDOW, detached) so the phone can reach /voice at http://<PC-IP>:8765."""
    try:
        import subprocess
        flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        proc = subprocess.Popen(
            [sys.executable, "-m", "mag.cast_launch", "launch", "--host", "0.0.0.0", "--port", "8765"],
            cwd=str(ROOT), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            creationflags=flags, close_fds=True)
        return {"ok": True, "service": "mag-backend", "pid": proc.pid,
                "url": "http://<PC-LAN-IP>:8765/voice",
                "note": "LAN voice/dashboard launched headless via the backend REST route (no prompt)"}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "service": "mag-backend", "error": str(e)[:160]}


def _log_http_failure(tool: str, error: str, result: dict | None) -> None:
    """Count direct-API tool failures into failure_kb (cross-session pressure alarm).

    Buried-signal probe (2026-09-11): 12 direct-API failures produced zero rows —
    the HTTP seam the organ router uses was invisible to the counter. Closes the
    seam Chair 3 verified; the CLI path was already counted."""
    try:
        from mag.failure_kb import log_failure

        log_failure(
            kind="http_tool_fail",
            detail=f"direct-API /run_task failure: {(result or {}).get('error') or error}"[:500],
            tool=tool,
            error=error[:300],
            phase="http_dispatch",
            session_id=None,
            provider=None,
        )
    except Exception:
        pass


@app.post("/run_task", response_model=RunTaskResponse)
def run_task(req: RunTaskRequest) -> RunTaskResponse:
    """Dispatch a tool call. Returns Success/Failure JSON envelope."""
    if req.tool not in TOOL_MAP:
        _log_http_failure(req.tool, f"unknown tool: {req.tool}", None)
        return RunTaskResponse(
            ok=False,
            tool=req.tool,
            error=f"unknown tool: {req.tool}",
            result={"tools": sorted(TOOL_MAP)},
        )
    try:
        result = tool_dispatch(req.tool, req.args or {})
        ok = bool(result.get("ok", False))
        if not ok:
            # Count HTTP-seam failures: without this, direct-API loops are
            # invisible to failure_kb (the 25,007-row blind spot, 08-06..09-11).
            _log_http_failure(
                req.tool,
                str((result or {}).get("error") or "")[:300],
                result if isinstance(result, dict) else None,
            )
        # error-loss-chain fix (2026-09-23): propagate the real error into the
        # envelope. This line was the top still-live FKB fault — the seat fell
        # back to "backend reported failure" because result.error never crossed
        # the HTTP seam, so the model could not self-correct (FKB 38,885 rows).
        return RunTaskResponse(ok=ok, tool=req.tool, result=result,
                               error=str((result or {}).get("error") or "")[:500] or None)
    except Exception as e:  # noqa: BLE001
        _log_http_failure(req.tool, str(e)[:300], None)
        return RunTaskResponse(
            ok=False,
            tool=req.tool,
            error=str(e),
            result={"exception": True},
        )



WAVE_HTML = ROOT / "dashboard" / "static" / "wave.html"
STATIC_DIR = ROOT / "dashboard" / "static"


@app.get("/wave")
def wave_page():
    """Desk face. Same bytes the ThreadingHTTPServer served. One FastAPI process."""
    if not WAVE_HTML.is_file():
        raise HTTPException(404, "wave.html missing")
    return FileResponse(WAVE_HTML, headers={"Cache-Control": "no-store"})


@app.get("/api/v1/wave")
def wave_get(session_id: str = ""):
    from mag.wave import snapshot
    return snapshot(session_id=session_id)


@app.post("/api/v1/voice/turn")
async def voice_turn(request: Request):
    from mag.table_turn import handle
    try:
        body = await request.json()
    except Exception:
        body = {}
    if not isinstance(body, dict):
        body = {}
    return handle(body)



if STATIC_DIR.is_dir() and not any(getattr(r, "path", "") == "/static" for r in app.routes):
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

def main(argv: list[str] | None = None) -> int:
    # Windows detached spawn uses cp1252 stderr; startup print must not crash.
    for _stream in (sys.stdout, sys.stderr):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    parser = argparse.ArgumentParser(description="Mag FastAPI tool backend")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--reload", action="store_true", help="uvicorn auto-reload")
    args = parser.parse_args(argv)

    import uvicorn

    print(f"Mag backend -> http://{args.host}:{args.port}/  (tools: {len(TOOL_MAP)})")
    uvicorn.run(
        "backend.server:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
