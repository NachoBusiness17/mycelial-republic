# garden-v1-A1-haiku45-B8 (anthropic/claude-haiku-4.5 @ nous, turn 1, channel: content)

# DELIVERABLE: Ollama Service Recovery on Windows 10

## Conditions and Context
- Instrument: Windows 10 command-line operations (CMD or PowerShell)
- Moment: Service hung at 100% CPU, REST port non-responsive
- Authorization: Machine owner has approved kill-and-restart procedure
- Assumption: Ollama installed with system PATH or standard installation directory
- Falsifier: If commands execute without error but service does not respond to health check within 30 seconds, the restart has failed and requires manual diagnosis

## Recovery Commands

**1. Forcibly terminate every ollama process:**
```
taskkill /F /IM ollama.exe /T
```
- `/F` - force termination (no graceful shutdown)
- `/IM` - match image name exactly
- `/T` - terminate child processes

**2. Restart the service:**
```
net start ollama
```
- Assumes Ollama is registered as Windows service named "ollama"
- NEGATIVE EXAMPLE: `start ollama.exe` alone (foreground-only, does not register as service restart)

**3. One-line health check confirming model responds:**
```
powershell -Command "(Invoke-WebRequest -Uri 'http://localhost:11434/api/generate' -Method Post -Body '{\"model\":\"gemma:2b\",\"prompt\":\".\"}' -ContentType 'application/json' -TimeoutSec 5 -ErrorAction Stop).StatusCode"
```
- POSITIVE RESULT: Outputs `200` (HTTP success)
- NEGATIVE RESULT: Timeout, connection refused, or non-2xx status (model still wedged)
- Alternative shorter form: `curl -s http://localhost:11434/api/tags` returns JSON list including gemma:2b

---

**Verification note:** Commands assume default Windows Ollama installation. If service name differs, substitute actual name from `services.msc` or `Get-Service` output.
