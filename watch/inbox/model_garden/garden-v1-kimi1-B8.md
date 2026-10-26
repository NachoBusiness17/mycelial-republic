# garden-v1-kimi1-B8 (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

1. `taskkill /F /IM ollama.exe & taskkill /F /IM ollama_llama_server.exe`
2. `net start ollama`
3. `curl -s http://localhost:11434/api/generate -d '{"model":"gemma:2b","prompt":"hi","stream":false}' -w "%{http_code}" -o nul | findstr "200"`
