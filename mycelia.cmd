@echo off
setlocal
set "ROOT=%~dp0"
set "PY=%ROOT%.venv\Scripts\python.exe"
set "EXE=%ROOT%.venv\Scripts\mycelia.exe"
if not exist "%PY%" (
  echo Missing mycelial venv. Run: powershell -ExecutionPolicy Bypass -File "%ROOT%scripts\bootstrap.ps1"
  exit /b 1
)
if exist "%EXE%" (
  "%EXE%" %*
) else (
  "%PY%" -m mycelial_republic.cli %*
)
exit /b %ERRORLEVEL%