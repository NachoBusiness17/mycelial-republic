@echo off
REM ===========================================================================
REM  backup_to_drive.cmd — FULL OFFLINE disaster-recovery backup to another drive
REM  Created 2026-08-19. For catastrophic-failure protection.
REM
REM  WHAT IT DOES (private + offline, NEVER pushes to GitHub):
REM   1. Robocopy the ENTIRE local_sovereign_agent folder to <DEST> — code,
REM      .git history, AND the gitignored memory/ (verkle chain, campaigns,
REM      runtime state) — so nothing is lost if the primary drive dies.
REM   2. Create a git bundle of full history at <DEST> as a second layer.
REM
REM  WHY THE FULL FOLDER (not just git): memory/ is gitignored BY DESIGN, so a
REM  git bundle alone would lose the durable runtime ledger. Robocopy /E gets it.
REM
REM  USAGE:  backup_to_drive.cmd ["D:\backups\local_sovereign_agent"]
REM          (defaults to D:\backups\local_sovereign_agent if no arg)
REM ===========================================================================
setlocal
cd /d "%~dp0"
set DEST=%~1
if "%DEST%"=="" set DEST=D:\backups\local_sovereign_agent

echo [backup] destination : %DEST%
echo [backup] copying FULL folder (code + memory + .git history)...
echo [backup] excluding recreatable: .venv, __pycache__, logs, state, node_modules

REM /E = all subdirs incl empty; /XJ = no junctions (prevents loops);
REM /XD = exclude recreatable dirs; /R:2 /W:2 = retry 2x / wait 2s;
REM /NFL /NDL = quiet file/dir list; /MT = multithread
robocopy "%~dp0" "%DEST%" /E /XJ /XD .venv __pycache__ logs state node_modules models .git ^
  /COPY:DAT /DCOPY:DAT /R:2 /W:2 /NFL /NDL /MT:8
set RC=%errorlevel%
if %RC% GEQ 8 (
  echo [backup] ROBOCOPY FAILED (exit %RC%) - aborting
  exit /b %RC%
)
echo [backup] folder copy OK (robocopy exit %RC% = 0-7 success)

echo [backup] creating git bundle of full history...
git bundle create "%DEST%\local_sovereign_agent.bundle" --all
if errorlevel 1 (
  echo [backup] git bundle FAILED
  exit /b 1
)
echo [backup] bundle: %DEST%\local_sovereign_agent.bundle

echo.
echo [backup] DONE. Verify: plug in the drive, then open %DEST% and confirm
echo [backup] the folder + .bundle are present. Backup is private + offline.
endlocal
