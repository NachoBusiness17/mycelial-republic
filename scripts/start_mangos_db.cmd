@echo off
rem start_mangos_db.cmd - bring up the mangos (WoW-clone) MariaDB backend on demand (2026-09-30)
rem
rem WHY THIS EXISTS: mysqld ran orphaned ~21h after the SRP6/realmd auth lane finished
rem (receipt watch/inbox/last_mile_20260930/MANGOS_DB_STATE.md). It is NOT a Windows
rem service - nothing auto-starts it. This script is the one command that brings it
rem back when the sovereign-server lanes need realmd/characters/mangos databases.
rem
rem Databases on disk: C:\Program Files\MariaDB 13.0\data\{mangos,characters}
rem Port: 127.0.0.1:3306 (localhost only). Stop with: mysqladmin -u root shutdown

set MARIADB_DIR=C:\Program Files\MariaDB 13.0
tasklist /FI "IMAGENAME eq mysqld.exe" 2>nul | find /I "mysqld.exe" >nul
if %ERRORLEVEL%==0 (
    echo mysqld already running - nothing to do.
    exit /b 0
)
echo Starting mysqld (mangos backend)...
start "" /B "%MARIADB_DIR%\bin\mysqld.exe" --defaults-file="%MARIADB_DIR%\data\my.ini"
timeout /t 3 /nobreak >nul
netstat -ano | findstr "127.0.0.1:3306.*LISTENING" >nul
if %ERRORLEVEL%==0 (
    echo mysqld UP on 127.0.0.1:3306. Stop later with: mysqladmin -u root shutdown
) else (
    echo WARNING: 3306 not listening yet - check "%MARIADB_DIR%\data" logs.
    exit /b 1
)
