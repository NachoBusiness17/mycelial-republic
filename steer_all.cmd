@echo off
REM ===========================================================================
REM  steer_all.cmd — control ALL seats (copilot, grok, chatgpt, the swarm)
REM  from ONE terminal. Emits to the shared steer bus every surface injects.
REM  Usage:  steer_all.cmd "message for every seat"
REM ===========================================================================
cd /d "%~dp0"
if "%~1"=="" (
  echo usage: steer_all.cmd "message for every seat"
  exit /b 1
)
.\.venv\Scripts\python.exe tools\steer_all.py %*
