# garden-v1-B8 (anthropic/claude-fable-5.1 @ nous, turn 1, channel: content)

1. **Force-kill every ollama process (cmd.exe, run as Administrator):**
   ```
   taskkill /F /T /IM "ollama app.exe"
   taskkill /F /T /IM ollama.exe
   taskkill /F /T /IM ollama_llama_server.exe
   tasklist | findstr /I ollama
   ```
   Conditions: `/F` is mandatory because the ask states the process is pinned at 100% CPU and its REST port answers nothing (memory/plans/garden_battery/B8/ASK_TEXT.md:1, "pinned at 100% CPU on one core, its REST port answers nothing"); a graceful close request will be ignored by a wedged runner. `/T` kills the child tree (the `ollama_llama_server.exe` runner spawned by `ollama.exe`). The last line is the confirmation: an empty result means nothing named ollama survived. The three image names are the standard Windows Ollama install layout; they are UNVERIFIED against this estate's install (no process list or install path appears in the evidence), so if `tasklist | findstr /I ollama` still prints a row, kill that exact image name with `taskkill /F /T /IM <name>`. Negative example (do not use): `ollama stop gemma:2b` or `ollama ps` - both talk to the dead REST port and will hang. Negative example: `taskkill /IM ollama.exe` without `/F` - returns success but the pinned process stays up.

2. **Restart the service (cmd.exe):**
   ```
   start "" "%LOCALAPPDATA%\Programs\Ollama\ollama app.exe"
   ```
   Conditions: on a default Windows 10 install, Ollama is not a Windows Service; the tray app starts the `ollama.exe` server on `127.0.0.1:11434`. Path is UNVERIFIED against this host; if the executable is not there, use the detached fallback `start "" /B ollama serve` from any shell where `ollama` is on PATH. Only if the estate wrapped it as a real service (e.g. via NSSM, not evidenced) would `net start ollama` apply - UNVERIFIED, so do not assume it. Negative example: running `ollama serve` in the foreground of the same shell you need for step 3 - it blocks the shell and dies when the window closes.

3. **One-line health check (cmd.exe, bounded to 90 s so a re-wedge cannot stall the operator):**
   ```
   curl -s -m 90 http://127.0.0.1:11434/api/generate -d "{\"model\":\"gemma:2b\",\"prompt\":\"Reply with the single word OK.\",\"stream\":false}"
   ```
   Pass condition: JSON containing a non-empty `"response"` field and `"done":true` within 90 s, measured with the stock Windows 10 `curl.exe`, at the moment immediately after step 2 (first call includes model load, so allow the full 90 s; subsequent calls should return in low seconds). Falsifier for this whole deliverable: if step 1's `tasklist` line is empty, step 2 is executed, and this command still times out or returns connection refused, the runbook as given here is wrong for this host and the fault is not a wedged process (check `OLLAMA_HOST` overriding the port, or a different install path). Negative example of a weak check: `curl http://127.0.0.1:11434/` returns "Ollama is running" even when the model runner itself is dead; it proves the port, not that gemma:2b answers, which is what the ask requires (ASK_TEXT.md:3, "confirms the model answers again").
