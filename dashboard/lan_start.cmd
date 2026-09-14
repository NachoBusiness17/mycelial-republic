@echo off
rem ============================================================
rem lan_start.cmd -- launcher for the persistent LAN proxy.
rem See lan_proxy.py header for full docs.
rem
rem Usage:   lan_start.cmd [start|stop|status|restart]   (default: start)
rem
rem START:   double-click this file, or run it from any shell.
rem          The proxy detaches from this console and survives
rem          after the window (and your agent session) closes.
rem STOP:    lan_start.cmd stop
rem STATUS:  lan_start.cmd status
rem
rem NO ADMIN REQUIRED -- pure Python TCP forwarding, no netsh.
rem
rem SECURITY: LAN-only, not internet. No auth on the 8765 hop;
rem the MCP hop (8001) relies on the gateway's X-API-Key.
rem The perimeter is the router's firewall -- never port-forward
rem 8765/8001 to the internet.
rem ============================================================
setlocal
cd /d "%~dp0"
set PY=python
where python >nul 2>nul
if errorlevel 1 set PY=py -3
set ARG=%1
if "%ARG%"=="" set ARG=start
%PY% "%~dp0lan_proxy.py" %ARG%
endlocal
timeout /t 4 >nul
