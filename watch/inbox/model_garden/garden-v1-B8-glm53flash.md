# garden-v1-B8-glm53flash (glm-5.3-flash @ zai, turn 1, channel: content)

1. `taskkill /F /IM "ollama app.exe" /T & taskkill /F /IM "ollama.exe" /T`
2. `start "" "C:\Users\%USERNAME%\AppData\Local\Programs\Ollama\ollama app.exe"`
3. `curl -s http://localhost:11434/api/generate -d "{\"model\":\"gemma:2b\",\"prompt\":\"ping\",\"stream\":false}"`

Falsifier: if `taskkill` returns "not found" for either image name or curl returns connection refused after restart, this runbook step does not hold on that host; verify the actual exe paths via `tasklist | findstr ollama` and the install path before retrying.
