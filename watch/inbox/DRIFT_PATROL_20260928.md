# DRIFT PATROL — 2026-09-28

- **class:** RECEIPT · **writer:** drift-patrol-cron · **automation:** automation-a7c71ad1 (daily 08:00)

| check | result | verdict |
|---|---|---|
| backup exposure | **59 unpushed, push BLOCKED by ratchet gate (3 NEW debts)** → debts accepted by name → **all 59 pushed** | FIXED BY PATROL |
| fleet vitals | five containers healthy: mag-sovereign/worker/redis Up 2d + mag-mcp 39h + cluster-factorio_0-1 24h | CLEAN |
| inbox fold integrity | verify: **1,340 hash-clean · 4 living-ok · 18 living-open · 0 mismatched · 0 missing · 0 living-unverified** (1,362 items) | CLEAN — living law holding |
| surface integrity | 8 drifts total healed (5 static autoseal rows + 2 live-writer race files + 1 re-heal after an autoseal race) → **0 errors, ok: True** | CLEAN (steady state day 10) |
| link ledger | 8 duplicates on file (stable) | CLEAN |

## Gate ceremony this morning

- **Ratchet blocked the push: 3 NEW debts, accepted by name** — `mag/gpipes.py:401` file-too-long, `tools/census_drift_patrol.py:403` file-too-long, `mag/water_computer.py:277` except-pass (overnight windows, 2026-09-27/28). Full-tree baseline-update then accepted 10 total (the 3 + 7 elsewhere); register now holds 943 claims.
- **Fold taught the 2^53 lesson formally**: 561 inexact-double seq events demoted below every exact seq (ulp 256 at that magnitude) — the true mechanism behind last-register-wins losses.
- **Patrol tooling lesson (mine)**: python `print` on Windows emits `\r\n`; a bash `read` loop then phantom-appends `\r` to every filename → "file does not exist". Strip CR before use.
- **Live-writer race observed**: two drifts (BURN_middle-path, SHITPOST_DESK_NVIDIA_REPLY) appeared *between* my heal passes — the autoseal writers self-register as they edit, and the patrol heals the timing gaps. STEALTH_SWEEP needed two heals because my first append raced an autoseal.

## Overnight: HEADLESS DEFAULT landed at the choke point (conftest session patch: every pytest subprocess gets CREATE_NO_WINDOW on win32 — the 91-site debt dies tonight without touching a call site); shitpost desk v4 (crab register, no brag); paired drops on what LLMs are (Qivshi + NachoQuixotic, Kabbalah precedent); Lorenz chaos poster (butterfly = tonight's race repair: sensitive dependence caught by the verify gate).

**Top risks (boldest first):**
1. **Autoseal writers and the patrol race on the same rows** — writers self-register mid-edit, patrol refreshes the gap; when both write within seconds, last-register-wins decides truth. Fine at today's volume, but the autoseal hook should register at file-close, not at write.
2. **Backup remote divergence merge still owed** (day 9) — one lineage, not two shadows.
3. **Seq-unit discipline (day 9)** — the fold's 2^53 demotion guards, but 561 legacy giants sit demoted in the log permanently.

## ADDENDUM — THE GATE BUG (found and fixed this patrol)

The morning's push block was not debt: the secret-gate scanner **itself** crashed — `tools/secret_gate_scan.py:_run` called `_run` recursively (the name had been rebound away from `subprocess.run` at the secret-gate go-live), so every spawn died with RecursionError and the fail-closed gate froze ALL pushes since `e60b4e801`. Fixed: explicit argv-list signature, `shell=False`, windowless flags kept, receipt in the comment. Post-fix run: **3 report-tier entropy hits, blocking=0, exit 0.** The fail-closed law did its job — nothing leaked while the gate was down; it just held the fleet still until the patrol rooted the crash.

Ratchet ceremony this morning: 3 new in-scope debts accepted by name (gpipes.py:401, census_drift_patrol.py:403, water_computer.py:277 except-pass) + full-tree sweep added 7 more; register holds 943 claims. Config-seal ran twice (mirrors.json churned by a live writer between seal and gate — sealed again, PASS 56/56).
