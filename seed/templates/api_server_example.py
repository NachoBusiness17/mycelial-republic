"""api_server_example — serve YOUR trails over loopback (STACK tier 3, rebuilt small).

The source estate runs a FastAPI gateway on 127.0.0.1 with an API-key gate and lazy
handlers. This is that SHAPE, rebuilt at minimum size: every meter is a plaintext
file you own; the server just reads them. Nothing here calls out.

    pip install fastapi uvicorn
    UVICORN_API_KEY=some-long-random-string uvicorn api_server_example:app --host 127.0.0.1 --port 8765
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse

ROOT = Path.cwd()
KEY = (os.environ.get("UVICORN_API_KEY", "") or "").strip()
app = FastAPI(title="my-estate-meters")


def _gate(x_api_key: str = Header(default="")) -> None:
    """The one door: if a key is configured, every route demands it."""
    if KEY and x_api_key != KEY:
        raise HTTPException(status_code=401, detail="bad key")


@app.get("/health")
def health() -> dict:
    return {"ok": True, "estate": str(ROOT)}


@app.get("/meters/smith")
def meters_smith(x_api_key: str = Header(default="")):
    _gate(x_api_key)
    hits = sorted((ROOT / "watch" / "inbox").glob("ESTATE_SMITH_CHART_*.json"))
    if not hits:
        return JSONResponse({"status": "DARK", "why": "no smith chart yet — run the engine"})
    return JSONResponse(json.loads(hits[-1].read_text(encoding="utf-8")))


@app.get("/records/{folder}")
def records(folder: str, x_api_key: str = Header(default="")):
    _gate(x_api_key)
    base = (ROOT / folder).resolve()
    if not base.is_relative_to(ROOT):
        raise HTTPException(status_code=400, detail="path escapes estate")
    return JSONResponse({"files": [p.name for p in sorted(base.rglob("*")) if p.is_file()][:200]})
