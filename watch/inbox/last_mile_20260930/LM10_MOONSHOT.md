# LM10 — moonshot_engine: self-steal + run + minimal fix

**File:** `mag/moonshot_engine.py` · **Date:** 2026-09-30 · **Seat:** ZCode (last mile) · **Verdict: REWIRE, not retire.**

## 1. Audit research goal (rerun, bytes)

`mag.self_steal.audit()` finding: `moonshot_engine` utilization **stale**, age 299,335 s (~3.5 d), `research_goal`:

> "RESEARCH-PACK self_steal moonshot: the moonshot engine has not advanced recently (no progress in memory/swarm_surface/sent.jsonl for surface moonshot). Research which of MOONSHOT_GOALS is coldest and re-strike it through swarm_surface.route_novel so the WoW/Turtle ingest->manifest proceeds. Produce a concrete routing plan."

## 2. Ran it per its own interface (all live, $0)

- `python mag/moonshot_engine.py moonshot` — snapshot OK; plan (throughput_model) loads; progress was **2/8 goals (25%)**, anchors `9fd392d3…`/`021b129e…` (both enqueued 2026-08-12).
- **Concrete routing plan** (per research goal): computed anchor per goal — goals 0–1 landed, **goals 2–7 cold** (RIB manifest, verkle-knot world, game-as-subtle-work, self-measure wiring, EXTERNAL STEAL MaNGOS/TrinityCore, LIVE GAME FEED).
- `python mag/moonshot_engine.py cold-launch` — **6 newly queued, 2 deduped, 0 errors**; all 6 specs verified in `memory/runs/swarm_worker/queue/` as `queued`. Rerun: 8/8 deduped (idempotence proven live, twice).
- `moonshot_self_steal(fold_back=False)` — full sense→re-strike loop OK; `moonshot_cold: []` afterwards.
- `plan` / `progress` CLI both OK.

## 3. Findings (all byte-checked)

1. **The drain lane is ALIVE**: while this receipt was being written the k8s worker CronJob picked up fresh moonshot specs — census moved 6 queued → 4 queued + **2 failed** (e.g. `sw-3cca30efb1`, the EXTERNAL STEAL goal, provider `groq`, `detail: exit 1`, no result). Routing works; the free groq lane fails research goals (consistent with DRIVING LADDER: free lanes are sensing-only).
2. **Honesty defect found + fixed**: the two 2026-08-12 "landed" anchors have **no spec in the live queue, none in `queue_backup_20260827_preRepoint`, no `results/<id>.json`** — work vanished, yet `progress()` reported them toward `pct_of_target`. The ledger is an ENQUEUE ledger, never a DONE ledger. **verified_done across the surface's entire 48-day history: 0.**
3. `throughput_model` plan is honestly labeled (measured cost/req vs labeled dedup-ratio/tps fallback) — no over-claim there.

## 4. Minimal fix (receipt-commented in code)

`_outcome(task_id)` + outcome join in `progress()`: every ledger row is joined against its live queue-spec status and `results/<id>.json`; new fields `verified_done` and `outcomes` census (`queued`/`failed`/`done`/`result-filed`/`vanished`). Cause + evidence named in the fix comment (LM10, 2026-09-29/30). Post-fix `progress()`: target 8, queued_unique 8, **verified_done 0, outcomes {queued 4, failed 2, vanished 2}** — the truth is now visible instead of silently credited. Ratchet: **0 new hits from this file** (the 13 NEW rows the gate reports are other lanes' working-tree files).

## 5. Verdict — rewire, not retire

**Not a museum piece**: every gear turns — deterministic plan, anchor dedupe, idempotent re-strike, ledger, live in-cluster drain (specs moved to `failed` within minutes of enqueue). **But it has produced zero verified completions in 48 days** because (a) the two oldest strikes evaporated in the 08-27 repoint with no outcome trace, and (b) the drain defaults to free `groq`, which fails these research goals (`exit 1`) — exactly the tier the driving ladder demotes to sensing-only.

**Rewire recommendation (operator call, not executed here):**
1. Route the moonshot surface's provider to the **funded tier (Hermes/Nous, per RIB_DRIVING_LADDER_20260928)** for the two research-shaped goals (EXTERNAL STEAL, LIVE GAME FEED design); keep the rest on the free lane as sensing fan-out only.
2. Keep the new `verified_done` field as the success metric — `pct_of_target` alone credits enqueues, which is how this surface read 25% "progress" for 48 days of zero output.
3. The 4 still-`queued` specs are now in the live queue; next cadence's `moonshot_self_steal()` re-strikes nothing (all deduped) — check `outcomes`, not `pct_of_target`.

**mtime refreshed:** 2026-09-30 13:39 EDT (this run). Self-steal audit will re-age from today.
