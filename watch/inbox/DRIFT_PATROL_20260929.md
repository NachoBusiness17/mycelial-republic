# DRIFT PATROL — 2026-09-29

- **class:** RECEIPT · **writer:** drift-patrol-cron · **automation:** automation-a7c71ad1 (daily 08:00)

| check | result | verdict |
|---|---|---|
| backup exposure | **127 unpushed** — push gate-blocked (4 NEW ratchet debts) → accepted by name (register 945) → re-sealed → **pushed** | FIXED BY PATROL |
| fleet vitals | **mag-sovereign UNHEALTHY (12h)** → `docker compose restart mag` per runbook → recovering (health: starting at receipt time; worker/redis/mcp/factorio healthy throughout) | RESTORED, WATCH |
| inbox fold integrity | verify: **1,919 hash-clean · 5 living-ok · 18 living-open · 0 mismatched · 0 missing** (1,942 items); INDEX derived 2026-09-29T11:01 — fresh; **event log 6,408 lines (tripled in 4 days)** | CLEAN, SCALE WATCH |
| surface integrity | 9 drifts (wave5-repair + gala lanes + beats) → refreshed via fold add → **0 errors, ok: True** | CLEAN (steady state day 11) |
| link ledger | 8 duplicates on file (stable) | CLEAN |

## Ratchet ceremony

4 NEW debts accepted by name: `mag/corpus_gap_research.py:663` + `mag/corpus_selfsteal.py:550` + `mag/link_library.py:413` file-too-long (research/mcp census wave — link_library is the patrol's own module, fleet-extended past 400 lines), `tools/fossil_check.py:73` shell-true (**fix owed: convert to argv list**). Register: 945 claims.

## Overnight (large): ladder-02 behavior-cards compliance audit (scorecard FIRED 3 / PARTIAL 3 / IGNORED 3 against the main session — the deck tests the seat); mcp-mapbox dogfood (P1-P8 patterns); estate-to-Z.ai MCP bridge design (no new protocol; R1-R5 rollout, operator-GO gates); MCP security surface census (mcp_pin drift-check ZERO callers = rug-pull gate dormant — headline gap); dashboard census f-19 (597 files/4.36GB, 5 orphan pages, /static serves 9 generator .py — hardening list).

**Top risks (boldest first):**
1. **mag-sovereign ran unhealthy for ~12h before the patrol restart** — the healthcheck detects but nothing auto-restarts on unhealthy; a watchdog (compose `autoheal` label or the doctor's own loop) should close that gap.
2. **The 2^53 quantized-seq band keeps growing with the log** (6.4K events) — every demoted giant is a permanent last-register-wins hazard; writer seq discipline remains unwritten (day 10).
3. **mcp_pin rug-pull gate dormant** (zero callers) + /static serving generator .py — the security census's top two hardening items, unfixed.

## ADDENDUM — GHOST WEDGE (the unhealthy truth)

`mag-sovereign` ran **unhealthy ~12h** before this patrol's restart — and the restart did NOT cure it. Findings: dashboard 8765 healthy (200), backend 8000 alive (404-on-root is its no-root-route), api_server 8001 auth-gated alive, worker/redis/mcp/factorio healthy. The wedge is **mag.ghost on 9000**: process alive (pid 420, respawned fresh by the supervisor after a SIGKILL test), but never binds — connection refused 90s+ after boot, consistent across a full container restart. The healthcheck (`/api/v1/health`) aggregates ghost and 500s on its timeout → container flagged unhealthy while every work organ (lanes, drainer, dashboard) runs fine.

**Verdict: ghost boot wedge, persistent across restarts — likely a state-file load hang in mag/ghost's boot path. Filed as owed for a fix session (not a patrol patch): instrument ghost boot (log-before/after state load), then bisect its state files. Escalation available: full container recycle (`down`+`up`, not just restart) if ghost state is in a volume that survived the restarts.**

Config-churn note: mirrors.json + fleet configs churned twice between seal and gate; double-seal ceremony used.

## ADDENDUM 2 — SECRET GATE CAUGHT A REAL ONE (test debris class)

The gate blocked the push on an **sk-ant-shaped key (len 67)** in `burn_reset_20260927/flash50/_s219_basetemp/test_secret_blocks_provid0/creds.txt` — pytest basetemp debris from the gate's own test suite, swept into the inbox by the burn_reset wave. Excised (5.8MB basetemp dir, disposable by definition); gate now exit 0. **Lesson: basetemp dirs must never be filed into the inbox — they carry the test suite's synthetic credentials by design.** Same class as the SKEPTIC's 1,324-dir finding; sweep candidates exist across the wave dirs.
