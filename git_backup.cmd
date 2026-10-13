@echo off
REM ===========================================================================
REM  git_backup.cmd — one-command snapshot backup (best practice, 2026-08-14)
REM  Commits ALL tracked + untracked (non-ignored) changes with a dated message
REM  so we always know what is where and why. Pushes to origin if a remote exists.
REM  Usage:  git_backup.cmd ["optional description"]
REM  NOTE:   memory/ (runtime state incl. verkle chain) is gitignored BY DESIGN —
REM          the code + notebooks + config are what we back up. The verkle chain
REM          is the durable runtime ledger, not source.
REM ===========================================================================
setlocal
cd /d "%~dp0"
set DESC=%~1
if "%DESC%"=="" set DESC=backup snapshot

for /f "tokens=1-3 delims=/ " %%a in ('echo %date%') do set D=%%c%%a%%b
set MSG=backup %D%: %DESC%

git add -A
git commit -m "%MSG%" >nul 2>&1
if errorlevel 1 echo [git_backup] nothing to commit or commit failed (see above)
else echo [git_backup] committed: %MSG%

REM push if a remote exists (best effort)
git remote -v | findstr /i "origin" >nul 2>&1
if not errorlevel 1 (
  git push -q 2>nul && echo [git_backup] pushed to origin
)
endlocal
