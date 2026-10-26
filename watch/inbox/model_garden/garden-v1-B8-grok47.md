# garden-v1-B8-grok47 (grok-4.7 @ xai, turn 1, channel: content)

1. `taskkill /F /IM ollama.exe /T & taskkill /F /IM "ollama app.exe" /T`
2. `start "" "%LOCALAPPDATA%\Programs\Ollama\ollama app.exe"`
3. `curl -s http://127.0.0.1:11434/api/generate -d "{\"model\":\"gemma:2b\",\"prompt\":\"ping\",\"stream\":false}"`

Falsifier: after (1), `tasklist /FI "IMAGENAME eq ollama.exe"` still lists a process, or after (2) and (3) the curl line does not return a JSON body with a non-empty `response` field. Assumption: default install path and port 11434, owner-authorized local recovery only. Process names beyond those two images are UNVERIFIED against this host.
