# DRIFT PATROL — 2026-09-23 — FLEET DOWN INCIDENT, RESTORED

- **class:** RECEIPT · **writer:** drift-patrol-cron · **automation:** automation-a7c71ad1 (daily 08:00)

## INCIDENT: all three containers dead ~22 hours

`docker ps` came back EMPTY — mag-sovereign/mag-worker had `Exited (137)` (SIGKILL), mag-redis `Exited (0)`, since ~22h ago (host slept or Docker Desktop restarted; containers did not auto-restart — **restart policy gap, see risks**).

**Restore sequence (runbook worked, plus two port squatters):**
1. `docker compose up -d` → worker + redis healthy; **mag-sovereign refused: port 8765 squatted**.
2. Squatters: two host `python.exe` listeners on 8765 — the forbidden second supervisors (DOCKER_ONLY law violation, pre-existing since before today).
3. After killing those, **port 8000 squatted** by another host python — swept all four mapped ports (8765/8000/8001/9000), killed python squatters only.
4. `docker start mag-sovereign` → **healthy**; dashboard serves 200 via container.

| check | result | verdict |
|---|---|---|
| backup exposure | 1 unpushed — pushed (`b2b3f638c`) | CLEAN |
| fleet vitals | **DOWN → RESTORED**: all three Up + healthy; 8765 serving 200 | **INCIDENT CLOSED** |
| inbox fold | self-healed: 2,271→2,279 events → 727 active items | CLEAN |
| surface integrity | 8 post-edit hash drifts → refreshed → **0 errors, ok: True** | CLEAN (steady state day 5) |
| link ledger | 3 duplicates on file (stable) | CLEAN |

**Overnight:** light — scout daily with three ALERTs: **Groq free-plan changes** (llama dropped, compound decommissioned Sep 21 — our lanes healthy, qwen/gpt-oss unaffected), **Cerebras free tier now requires a card** (operator decision on the standing key gap), **GitHub Models shutting down** (free-resource loss), and **NVIDIA acquired Groq ($20B)** — lane longevity note.

**Top risks (boldest first):**
1. **Containers did not auto-restart after the host event** (22h dark) — compose needs `restart: unless-stopped` on all three services so the next host sleep/restart self-heals; today it took the patrol to notice.
2. **Host port squatters (the forbidden second supervisors) were blocking the fleet's own ports** — they'll come back if some launcher keeps spawning host dashboards; the launcher habit needs killing at the source.
3. **Groq free-plan churn + Cerebras card-wall + GitHub Models shutdown** — the free-resource floor is shrinking on three fronts the same week; lane re-probe due.
