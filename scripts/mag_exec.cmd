@echo off
REM Cage CLI without PowerShell ExecutionPolicy. Needs Docker engine access.
setlocal
cd /d "%~dp0.."
if "%~1"=="" (
  docker compose exec mag python main.py --help
  exit /b %ERRORLEVEL%
)
docker compose exec mag python main.py %*
exit /b %ERRORLEVEL%
