# R7 — LIGHT THE EYE (2026-09-10)

## Status: LIT

- Eye was DARK: no `ollama.exe` in tasklist, no response on `127.0.0.1:11434` (flagged in morning standup, dark since before 07:46).
- Fix applied: `ollama serve` started in background at ~R7 dispatch time.
- Verified: `GET /api/version` → `{"version":"0.32.7"}` — eye responds.

## Models available (13, from /api/tags)

| Model | Params | Quant | Capabilities |
|---|---|---|---|
| qwen2.5:7b | 7.6B | Q4_K_M | completion, tools |
| maze-keeper:latest | 32.8B (parent qwen2.5:32b) | Q4_K_M | completion, tools |
| gemma:2b | 3B | Q4_0 | completion |
| deepseek-r1:1.5b | 1.8B | Q4_K_M | completion, thinking |
| **qwen2.5vl:3b** | **3.8B** | Q4_K_M | **vision**, completion (128k ctx) |
| qwen2.5:32b | 32.8B | Q4_K_M | completion, tools |
| qwen2.5-coder:7b | 7.6B | Q4_K_M | completion, tools, insert |
| qwen-desk:latest | 3.1B | Q4_K_M | completion, tools |
| qwen2.5:3b-instruct | 3.1B | Q4_K_M | completion, tools |
| gemma4-desk:latest | 8.0B | Q4_K_M | completion, tools, thinking |
| gemma4:latest | 8.0B | Q4_K_M | completion, tools, thinking |
| gemma4-hermes:latest | 8.0B | Q4_K_M | completion, tools, thinking |
| nomic-embed-text:latest | 137M | F16 | embedding |

The eye can SEE: `qwen2.5vl:3b` (vision) is present — the dumb-agent-with-eyes surface is live again at host.docker.internal:11434 from inside the cage.

## Errors / caveats

- No errors on startup or probe.
- CAVEAT: this serve was started as a background child of the R7 seat session, NOT by the sanctioned autostart path. If this seat goes dark, the serve may die with it. If the eye goes dark again, the durable fix is restoring ollama's normal host autostart (per the 09-07 eye-to-host doctrine, watch/OLLAMA_EYE_TO_HOST_20260907.md) — flagging, not acting, inside lane bounds.
