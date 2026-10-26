# STEAL — code team from unused seats (2026-08-14)

Operator: we already have resources we are not rightsizing. Dedicated code team. GLM might be it. Small plan, ramp like Copilot/Codex.

## What was parked
- Hermes parked: true
- qwen2.5-coder:7b named as L0 worker, not a team
- DeepSeek agent + queue_deepseek
- Cursor seat + cursor_bridge
- Z.ai glm-4.6 paas/v4 free tier in Mag providers (not coding plan)
- Grok Bot / Copilot / Codex as parallel glasses
- queue_rightsize existed because 21k DeepSeek calls burned on mis-tier

## What we did
Unparked Hermes as code_team_tools (not router). mag/code_team.py picks local_coder -> deepseek_agent -> hermes tools; grok only architecture. queue_rightsize code/pytest/refactor/implement -> deepseek-v4-flash not grok. GLM Coding Plan Lite hangs on Hermes only when GLM_API_KEY exists. Mag chain stays Mag.

## What we did not
Subscribe. Put coding-plan key in Mag providers. Make GLM the janitor.
