@echo off
rem BURN MODE - the standing resume (unpause + health verify + eye up + software resume).
cd /d C:\Users\foste\Documents\projects\local_sovereign_agent
.venv\Scripts\python.exe -m mag.desktop_mode burn --seat nacho %*
