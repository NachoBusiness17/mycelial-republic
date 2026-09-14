"""host_browser — managed HOST-loopback Chromium seat (2026-08-14).

The container browser CDP forwarding is broken on Docker Desktop (host->container CDP
resets the handshake; works in-container only). The WORKING transport is host Chromium
bound to 127.0.0.1:9222, which browser_driver already connects to by default. This module
launches / stops / ensures that seat as a supervised, headless (CREATE_NO_WINDOW) process.

Schema: host_browser.v1 · deterministic $0 · CLI: python -m mag.host_browser status|start|stop|ensure
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

try:
    from config import ROOT
except Exception:
    ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

SCHEMA = "host_browser.v1"
PORT = 9222
CDP = f"http://127.0.0.1:{PORT}/json/version"
STATE = ROOT / "memory" / "runs" / "host_browser" / "state.json"
PROFILE = ROOT / "memory" / "runs" / "host_browser" / "profile"  # fixed dir => logins persist

CREATE_NO_WINDOW = 0x08000000


def _chrome() -> str | None:
    base = Path(os.environ.get("LOCALAPPDATA", "")) / "ms-playwright"
    for p in sorted(base.glob("chromium-*/chrome-win64/chrome.exe")) if base.is_dir() else []:
        if p.is_file():
            return str(p)
    # fall back to headless shell if full chromium absent
    for p in sorted(base.glob("chromium_headless_shell-*/chrome-headless-shell-win64/chrome-headless-shell.exe")) if base.is_dir() else []:
        if p.is_file():
            return str(p)
    return None


def _probe(timeout: float = 4.0) -> dict:
    try:
        d = json.loads(urllib.request.urlopen(CDP, timeout=timeout).read().decode())
        return {"ok": True, "browser": d.get("Browser")}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": str(e)[:120]}


def _read_pid():
    try:
        return json.loads(STATE.read_text(encoding="utf-8")).get("pid")
    except Exception:
        return None


def _write_pid(pid: int) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps({"pid": pid, "ts": time.time()}), encoding="utf-8")


def status() -> dict:
    return {"schema": SCHEMA, "cdp": CDP, "probe": _probe(), "pid": _read_pid()}


def start() -> dict:
    ch = _chrome()
    if not ch:
        return {"ok": False, "error": "host chromium not installed (playwright install chromium)"}
    if _probe().get("ok"):
        return {"ok": True, "note": "already up", "probe": _probe(), "pid": _read_pid()}
    PROFILE.mkdir(parents=True, exist_ok=True)
    proc = subprocess.Popen(
        [ch, "--headless=new", f"--remote-debugging-port={PORT}",
         "--remote-debugging-address=127.0.0.1", "--remote-allow-origins=*",
         "--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage",
         f"--user-data-dir={PROFILE}"],
        creationflags=CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    _write_pid(proc.pid)
    for _ in range(15):
        time.sleep(1)
        p = _probe()
        if p.get("ok"):
            return {"ok": True, "pid": proc.pid, "probe": p}
    return {"ok": False, "pid": proc.pid, "error": "cdp did not come up"}


def stop() -> dict:
    pid = _read_pid()
    if pid:
        try:
            subprocess.run(["taskkill", "/F", "/PID", str(pid)], capture_output=True, timeout=30)
        except Exception:  # noqa: BLE001
            pass
    return {"ok": True, "stopped_pid": pid}


def ensure() -> dict:
    if _probe().get("ok"):
        return {"ok": True, "note": "already up", "probe": _probe()}
    return start()


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    cmd = argv[0] if argv else "status"
    r = {"start": start, "stop": stop, "ensure": ensure, "status": status}.get(cmd, status)()
    print(json.dumps(r, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
