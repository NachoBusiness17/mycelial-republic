@echo off
rem GAME MODE - the standing pause (operator: "just do it i want it to be a standing thing i can ask")
rem Freezes the twin + software pause + eye down (ollama stop + stealth driver flag) + auto receipt.
cd /d C:\Users\foste\Documents\projects\local_sovereign_agent
.venv\Scripts\python.exe -m mag.desktop_mode game --seat nacho %*
