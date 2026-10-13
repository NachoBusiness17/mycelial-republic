@echo off
REM ============================================================
REM  STOP THE WINDOW POPUPS — ollama desktop -> cluster cutover
REM  Build: debug/train seat 2026-08-10 (steal: stateless fix)
REM  SAFE: verifies cluster ollama is UP before switching OLLAMA_HOST.
REM  Does NOT delete models; keeps desktop ollama as fallback if cluster down.
REM ============================================================
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo [1/4] Checking cluster ollama is up...
powershell -NoProfile -Command "try { $r = Invoke-WebRequest -Uri 'http://127.0.0.1:11434/api/tags' -UseBasicParsing -TimeoutSec 4; 'cluster_up' } catch { 'cluster_down' }" > "%TEMP%\ollama_cluster_probe.txt" 2>&1
set /p PROBE=<"%TEMP%\ollama_cluster_probe.txt"
echo   probe: %PROBE%

if /I "%PROBE%"=="cluster_down" (
    echo   [SAFE] Cluster ollama is DOWN - NOT switching. Keeping desktop ollama.
    echo   Deploy cluster ollama first (deploy\k8s\ollama.yaml), then rerun.
    pause
    exit /b 1
)

echo [2/4] Setting OLLAMA_HOST to cluster...
setx OLLAMA_HOST "http://127.0.0.1:11434" >nul
echo   OLLAMA_HOST=http://127.0.0.1:11434 (setx, new shells pick it up)

echo [3/4] Stopping the desktop ollama app / runner (the window firer)...
taskkill /IM "ollama.exe" /F >nul 2>&1
taskkill /IM "ollama app.exe" /F >nul 2>&1
taskkill /IM "ollama_llama_server.exe" /F >nul 2>&1
echo   desktop ollama + runners stopped

echo [4/4] Note: restart python processes to pick up sitecustomize (stateless no-window).
echo   The widened window-audit (mag.window_audit) will name any remaining firer.

echo.
echo Done. Windows should stop popping; models now serve from the cluster.
pause
