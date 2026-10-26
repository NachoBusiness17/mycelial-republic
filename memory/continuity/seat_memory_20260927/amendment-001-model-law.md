---
name: amendment-001-model-law
description: Amendment 001 (transport-deaths-never-count-as-attempts) filed to
  the amendments ledger + the MODEL LAW after the cron silently downgraded the
  build lane to glm — fallback never persists
metadata:
  node_type: memory
  type: project
  originSessionId: sess_199e4b14-3a8b-46e9-ba5e-57c166fc2967
---

2026-09-17 two structural laws born from operator anger:

**Amendment 001** (state/fuel/amendments.jsonl row 2, the tide's first substantive amendment, FILED 2026-09-17): transport deaths never count as attempts — HTTP 4xx/5xx, empty_content, 200-error-bodies, SSRF refusals are infra failures, never merit failures; they must not consume a task/brief attempt budget and must reset the counter when discovered. Only gate rejections and schema failures are merit deaths. Reason: four briefs burned real attempts on OpenRouter 200-with-error-body responses. Falsifier: any task dying with fewer than two MERIT attempts violates the law. The implementation (prune-then-reset in _load_state) was proven live: transport-victim briefs P-sentry-weave and P-scale-finale revived and passed gen-1 on their real attempts.

**MODEL LAW** (scripts/build_lane_game.py, after the cron fire silently migrated the sticky model union-alpha → glm-5.3-flash on a transient probe miss): PRIMARY is stealth/union-alpha ALWAYS; a transient probe failure gets a retry, and the fallback (glm-5.3-flash, law-15 paced) serves THE CURRENT RUN ONLY — never persisted to state. Post-11:00 local, glm-5.3-flash is a SCHEDULED co-primary (rotation with union) because it is free in that window. The only value ever persisted as the model is the primary.

Related: [[lite-free-window-schedule]], [[ox-alpha-was-glm53-flash]], [[union-fullsend-day-20260917]].
