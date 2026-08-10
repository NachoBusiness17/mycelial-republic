@echo off
REM start_mag_container.cmd — SINGLE-ACTION headless Mag bring-up (Docker = the brain).
REM Replaces the old host-side auto-start (MagLabKit8765 / MagPrivateOffice8765) that
REM ran `main.py lab` on the desktop and spawned python windows.
REM
REM What this does, in one pass (all headless, no python windows):
REM   1. Stops native host Mag loops (platform_kill) so ports 8765/8000/9000 are free.
REM   2. Ensures the Docker engine is up (self-starts Docker Desktop if needed).
REM   3. Builds + starts the container stack (mag-sovereign + mag-redis) via docker_ops up.
REM   4. Waits for the container dashboard :8765 to answer, then reports a verdict.
REM
REM Usage:  double-click, or run  scripts\start_mag_container.cmd   (or point a scheduled task at it)

setlocal
cd /d "%~dp0.."
set "PY=%~dp0..\.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=%~dp0.venv\Scripts\python.exe"
if not exist "%PY%" (
  echo [mag-container] ERROR: missing venv python at "%PY%"
  pause
  exit /b 1
)

echo.
echo [mag-container] ==========================================================
echo [mag-container]  HEADLESS Mag bring-up  (Docker = single brain, no windows)
echo [mag-container] ==========================================================
echo.

echo [mag-container] 1/4  Stopping native host Mag loops (free ports 8765/8000/9000)...
"%PY%" -m mag.platform_kill 2>nul
echo [mag-container]     native host loops stopped.

echo [mag-container] 2/4  Ensuring Docker engine is up (may start Docker Desktop)...
"%PY%" -c "from mag.docker_ops import ensure_engine; import json; print('   engine:', json.dumps(ensure_engine(), default=str))" 2>&1

echo [mag-container] 3/4  Building + starting the container stack...
"%PY%" -m mag.docker_ops up 2>&1

echo [mag-container] 4/4  Waiting for container dashboard :8765...
"%PY%" -c "import urllib.request,time; ok=False
for _ in range(40):
    try:
        if urllib.request.urlopen('http://127.0.0.1:8765/',timeout=2).status==200: ok=True; break
    except Exception: pass
    time.sleep(3)
print('   dashboard :8765', 'UP' if ok else 'NOT REACHED')" 2>&1

echo.
echo [mag-container] status:
docker ps --filter name=mag-sovereign --filter name=mag-redis --format "  {{.Names}}: {{.Status}}" 2>nul || "%PY%" -c "from mag.docker_ops import status; import json; print(json.dumps(status().get('containers'), indent=2, default=str))" 2>&1
echo.
echo [mag-container] Done. Open the Control Room: http://127.0.0.1:8765/
echo.
endlocal
