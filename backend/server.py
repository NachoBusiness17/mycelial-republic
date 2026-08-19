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
import sys
from pathlib import Path
from typing import Any

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
    }


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


@app.post("/run_task", response_model=RunTaskResponse)
def run_task(req: RunTaskRequest) -> RunTaskResponse:
    """Dispatch a tool call. Returns Success/Failure JSON envelope."""
    if req.tool not in TOOL_MAP:
        return RunTaskResponse(
            ok=False,
            tool=req.tool,
            error=f"unknown tool: {req.tool}",
            result={"tools": sorted(TOOL_MAP)},
        )
    try:
        result = tool_dispatch(req.tool, req.args or {})
        ok = bool(result.get("ok", False))
        return RunTaskResponse(ok=ok, tool=req.tool, result=result)
    except Exception as e:  # noqa: BLE001
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
