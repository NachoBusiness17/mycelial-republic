@echo off
rem AUTH SWITCHBOARD — one-word door (pattern: switchboard_status.cmd)
rem Reads + $0 probes only; never prints key values; never writes auth state.
cd /d "%~dp0"
python -m mag.auth_switchboard status %*
