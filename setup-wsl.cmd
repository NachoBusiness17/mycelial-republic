@echo off
title Mag - Enable WSL2 + Docker backend
rem Double-click this file. It will ask for admin (UAC) - click Yes.
rem It installs the WSL2 Linux distro Docker needs, then tells you to reboot.

REM --- Self-elevate to admin (this is the only part that needs admin) ---
net session >nul 2>&1
if %errorlevel% neq 0 (
  echo Requesting administrator privileges...
  powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
  exit /b
)

echo ============================================
echo  Mag - Enabling WSL2 + Ubuntu (for Docker)
echo ============================================
echo.

echo Installing Windows Subsystem for Linux (WSL2) + Ubuntu...
echo You may see Windows install Ubuntu - this is expected.
echo.
wsl --install -d Ubuntu

echo.
echo ------------------------------------------------------------
echo  STEP COMPLETE.
echo  IMPORTANT: Please REBOOT your machine now.
echo  After reboot, Docker Desktop should start automatically.
echo  Then run:  docker info   to confirm it works.
echo ------------------------------------------------------------
echo.
pause
