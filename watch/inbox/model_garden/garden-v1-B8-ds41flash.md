# garden-v1-B8-ds41flash (deepseek-chat @ deepseek, turn 1, channel: content)

1. `taskkill /F /IM ollama.exe /T` then, if any survive, `wmic process where "name='ollama.exe'" delete` and `wmic process where "name='ollama app.exe'" delete`
2. `start "" /b "C:\Users\%USERNAME%\AppData\Local\Programs\Ollama\ollama app.exe"` (or `sc start ollama` if installed as service)
3. `curl -s http://127.0.0.1:11434/api/generate -d "{\"model\":\"gemma:2b\",\"prompt\":\"ping\",\"stream\":false}"` returns a JSON body containing `"response"`.

Falsifier: if item 1's output shows no matching process, the wedge is not an ollama.exe on this host and the recovery runbook step is inapplicable.
