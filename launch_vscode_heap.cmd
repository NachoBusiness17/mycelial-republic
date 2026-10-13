@echo off
REM Launch VS Code with an 8GB JS heap for the auto-router chat window.
REM The router accumulates: giant transcripts (35-73MB sessions) + 19 terminals + 5 MCP servers
REM in one extension host. Default heap eventually OOMs. This buys 3-4x headroom.
REM SESSION HYGIENE RULE (the real fix): start a NEW CHAT when Context window usage
REM passes ~80%% or every few hours of routing. Old sessions persist on disk; the
REM live heap only carries the active one.
start "" "C:\Users\foste\AppData\Local\Programs\Microsoft VS Code\Code.exe" --max-memory=8192 "C:\Users\foste\Documents\projects"
