# garden-v1-A1-sonnet55-B8 (anthropic/claude-sonnet-5.5 @ nous, turn 1, channel: content)

1. **Force-terminate every ollama process.** Run in cmd.exe, as the same user or elevated. Kill the tray supervisor first, or it respawns the server:
   ```
   taskkill /F /T /IM "ollama app.exe" & taskkill /F /T /IM ollama.exe & taskkill /F /T /IM ollama_llama_server.exe
   ```
   - `/F` forces termination and `/T` also kills child processes, such as the wedged runner holding the CPU core.
   - Exit code 128 ("process not found") for any one image name is harmless. Newer builds have no `ollama_llama_server.exe`, and older ones differ.
   - Confirm nothing survived with `tasklist | findstr /I ollama`. Empty output means success. Any remaining line means repeat with `taskkill /F /PID <pid>`.
   - Assumption: a default Windows install (tray app plus `ollama.exe`). The image names are UNVERIFIED against this host, because the evidence file (A1_B8_ask_frozen.md:1-3) contains no process listing.

2. **Restart.** Default installs have no Windows service, only the tray app, so start the server directly:
   ```
   start "" /B ollama serve
   ```
   - If this host wraps ollama as a real service (for example via NSSM), use `net start <ServiceName>` instead. The name is UNVERIFIED, so look it up with `sc query state= all | findstr /I ollama`.
   - Negative example: do not run a bare `ollama serve` in the shell you need afterwards. It blocks that shell, and closing it kills the server.

3. **Health check.** One line, run about 5 seconds after item 2:
   ```
   curl.exe -s --max-time 120 http://127.0.0.1:11434/api/generate -d "{\"model\":\"gemma:2b\",\"prompt\":\"ping\",\"stream\":false,\"options\":{\"num_predict\":1}}"
   ```
   - **Pass:** a JSON body containing `"response"` and `"done":true`.
   - **Fail:** empty output, a connection error, or a timeout.
   - **Conditions:**
     - Instrument: curl.exe, built into Windows 10 1803 and later.
     - Moment: right after restart, so the first call includes the cold model load and may take several seconds. The 120 s cap allows for that.
     - Context: assumes the default `127.0.0.1:11434`. If `OLLAMA_HOST` is set, substitute that address.
   - Negative example: `curl http://127.0.0.1:11434/` returning "Ollama is running" proves only that the HTTP server is up. It does not prove gemma:2b can generate, which is the part that wedged.
   - **Falsifier:** if item 3 fails after items 1 and 2 pass cleanly, the restart did not fix the fault. Suspect a corrupt model blob or a port still held, which `netstat -ano | findstr 11434` would show.
