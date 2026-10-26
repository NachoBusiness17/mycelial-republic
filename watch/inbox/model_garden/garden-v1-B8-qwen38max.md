# garden-v1-B8-qwen38max (qwen/qwen3.8-max-prime @ nous, turn 1, channel: content)

1. **Kill all ollama processes:**
   ```
   taskkill /F /IM ollama.exe /T & taskkill /F /IM ollama_llama_server.exe /T
   ```
   `/F` forces termination; `/T` kills the process tree. Both image names are needed because the llama-server child can survive the parent's death.

2. **Restart the service:**
   ```
   start /B ollama serve
   ```
   This launches the API server in the background. If your estate uses the tray-app wrapper instead, replace with `start "" "%LOCALAPPDATA%\Programs\Ollama\ollama app.exe"`.

3. **Health check:**
   ```
   curl -s http://localhost:11434/api/generate -d "{\"model\":\"gemma:2b\",\"prompt\":\"ping\",\"stream\":false}" | findstr /C:"response"
   ```
   Exit code 0 and a `"response"` substring in stdout confirms the model is serving. A timeout or connection-refused means it is still down.

---

**Falsifier:** if step 3 returns HTTP 200 with a `"response"` key but the harness still reports a stall, the problem is not ollama but the harness's own reconnection logic, and this runbook does not fix it.
