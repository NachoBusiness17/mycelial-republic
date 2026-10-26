# SELF-STEAL: PSEUDOSPECTRUM / SMITH CHART — the estate is a non-normal operator
**Schema:** selfsteal.pseudospectrum.v1 · **ts:** 2026-09-21T10:45Z
**Trigger:** operator directive — "eliminate sacred cows; if shit isn't healthy we don't answer it with prose. self steal"
**Wave:** 4 X specimens (fetched, decoded below)

## The specimens
1. **@dunyasalbilim** 2101687830132994198 — "Trigonometri birim çemberi" (rotating unit circle) **+ smith chart** (operator pairing)
2. **@mathelirium** 2101653821965369584 — "Eigenvalues do not always tell the whole story… the pseudo-spectrum reveals hidden regions where tiny changes produce surprisingly large responses." **Operator: "this seems like what we are doing for some reason…"** — the tweet's own slip: it says *normal* matrices; the hidden-response region is the **non-normal** case (normal ⇒ pseudospectrum = fat eigenvalue dots, nothing hidden). Reply thread caught it. We decode the corrected doctrine.
3. **@PhilosophyOfPhy** 2101861302771855624 — orbit equation r(θ), eccentricity e classifies the whole trajectory: one number, not a description
4. **@SciencesKL** 2101422960028307693 — "Electron in Atom": the drawable Bohr picture — comfortable, wrong, survives because it is drawable

## The decode
- **The fleet is a non-normal operator.** Modules are not orthogonal — boots cite handoffs cite laws cite crons (nearly parallel eigenmodes). The spectrum (sealed chain, invariants, "97 done") reads healthy while a unit perturbation — one update, one 404, one PATH change — produces a massive transient. Today's live proof: chain perfect; reaper dead since morning; one queue slot zombie 9h; two agents looping on checkpoint-apply.
- **The Smith chart is a pseudospectrum plot on the unit disk.** Center = matched (power delivered), rim = total reflection. Constant-|Γ| rings = health contours. Prose status answers are reflections: |Γ|→1 means all power bounced, none delivered.
- **Orbit law:** health gets ONE number with a pre-stated bar, like e classifies the orbit. **Bohr law:** the org-chart/status-brief picture of the estate is the Bohr atom — drawable, wrong, sacred.

## The law (codified)
**Health is a |Γ| coordinate, not a sentence. Γ = 1 − delivered/claimed, computed from bytes. |Γ| > 0.5 ⇒ the organ may NOT be answered with prose — fixes only. An unmetered organ is DARK, and dark is its own finding.**

## The meter (built this session — not proposed)
`tools/estate_smith_chart.py` → `watch/inbox/ESTATE_SMITH_CHART_20260921.{json,png}`
Sources: logs/provider_usage.jsonl, logs/supervisor.jsonl, logs/orchestrator/*.out.log, logs/lane_scheduler.log, mag.orchestrator.queue_status, mag.peer_handoff.list_peer_handoffs.

### First reading 10:41Z → post-fix 10:45Z
| organ | Γ | verdict |
|---|---|---|
| supervisor (reaper) | **1.00** | reflecting — reaper-enumerate-error every ~30s: "no powershell on PATH or System32" |
| flash_lane_zai3 | **0.71** | reflecting — deaths end in **HTTP 429 code 1113 "Insufficient balance"** |
| deepseek_lane | 0.00 | delivering (sole healthy lane; carrying the loopers) |
| ollama_lane | 0.93 | reflecting — 27/30 attempts failed; family-box law expects day-dark, but wasted attempts against a dark lane are still theater |
| queue | 1.00 → **0.00** | **FIXED this session** (see fixes) |
| day_work | **0.88** | stalled=7 on last mirror |
| handoffs | **1.00** | 12 pending (bar: >10 = rot) |
| checkpoint_apply | **1.00** | orc-t01ed9419a5 + te733d21bee looping "checkpoint (apply)" since 06:15/06:30Z |

**DARK: none** (was queue+handoffs before the sys.path fix — the meter metered itself).

## Fixes executed this session (receipts, not prose)
1. **Zombie running slot settled** — t64aaa9a4cf (game-flow test): task record was already terminal (exit 1, z_ai3 429 code 1113, workday filed 05:29Z) but the running entry never vacated because **the reaper that clears dead pids is the broken organ**. Settled via the orchestrator's own write pattern (`_finalize` + `_queue_save` + `_trail`, mirroring `_settle_unreachable_queued`). Queue now 97 done / 3 failed / **0 running**.
2. **The 429 code 1113 receipt** — the flash lane's z_ai3 key is **out of balance**. No software fix exists; operator action: recharge or rotate key. Until then the "flash-first" tier ladder is dead prose.

## Fixes NOT executed (named, with why)
- **Reaper PATH repair** — needs the supervisor's launch environment (where its PATH is set); touching it blind risks killing the heartbeat that IS working. Operator-window job.
- **Killing the two checkpoint-loop agents** — they are alive and calling deepseek successfully; the sick organ is the **checkpoint-apply plumbing** (deliberate-ask has no timeout/dead-letter, so asks loop forever on an idle operator). Fix is design, not a kill: dead-letter + proceed-on-timeout.
- **day_work stalled=7, 12 handoffs** — inventory exists; burn belongs to a work window, not the meter pass.

## Sacred cows struck
- "97 done" as health (eigenvalue bookkeeping hiding transient rot)
- "drainer ON" in prose briefs while the reaper under it is dead
- The Bohr org-chart of seats (drawable ≠ true)
- Prose status answers for anything with a computable Γ
