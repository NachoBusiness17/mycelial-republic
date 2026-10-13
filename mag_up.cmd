@echo off
REM mag_up.cmd - One-command boot that brings up ALL seven swarm agents (self-heal as law).
REM The drainer/autorun loop now defaults ON (mag_launch._drainer_wanted), so a single
REM start brings up ghost daemon + dashboard + backend + scribe + the autorun loop that
REM EXECUTES the laws (swarm-health apply, law registry enforce, steer consume).
setlocal
cd /d "%~dp0"
echo [mag_up] Booting the republic (ghost + dashboard + backend + drainer/autorun)...
call "%~dp0start_everything.cmd" --no-mirror
echo.
echo [mag_up] Stack up. Law + steer + swarm-health cadences run in the autorun loop.
echo          Home: http://127.0.0.1:8765/
endlocal
