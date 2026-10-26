# row_flow.md — lane-water (flash): the flow layer
OCEAN SALON wave 1 · 2026-08-31 · seats: water_windows / offpeak.v1 / seat_corpus / lane_cadence + afk_cadence organs

## 1. WHAT DO YOU KNOW? (state the ledger misses)

- **`/root/.openclaw/workspace/water_windows.mjs`** (note: NOT `/board/water_windows.mjs` — task pointer was wrong) — 12 reservoirs as rows: `deepseek_offpeak`, `zai_half_price`, `zai_credits`, `grok_a`, `grok_b`, `chatgpt_codex`, `zcode`, `deepseek_direct`, `ollama_local`, `groq_oss`, `cerebras`, `or_free`. It computes live countdowns from wall clock (deepseek BJ peak windows, zai 50%-off until 2026-09-09, zcode hands-off until 09-02 12:52Z). The ledger at `/board/water_ledger.jsonl` has **only 2 lines ever** (both 2026-08-31 zai_credits rate receipts: "5.3 lead ≈ $0.75/hr at 50% off"). So the ledger knows burn-rate lore, but nothing else: no groq/cerebras/or_free usage readings, no desk-seat (grok_a/b, codex) hook feed, no ollama load.
- **POLLED reservoirs are calendar-trust, not measurement**: groq_oss/cerebras/or_free rows say "resets ~00:00 UTC; cage cannot read usage; poll from host" — the file asserts levels it cannot see. The 30 RPM/1K RPD/200K TPD (groq) and 1M TPD (cerebras) ceilings are hardcoded notes, not fed by any poller.
- **`/mag/mag/offpeak.py`** (schema `offpeak.v1`) — deterministic pricing clock: weekday BJ 09–12/14–18 = 2x, weekends all off-peak. `pricing()` returns `local_peak_windows` (operator-local conversion, DST-correct) and `next_offpeak_utc`. The water table **duplicates this peak math inline** (two clocks of the same window — drift risk).
- **`/mag/memory/runs/seat_corpus/latest.json`** (schema `seat_corpus.v1`, ts 2026-08-29T17:46Z — ~2 days stale) — per-lane contracts the routing ledger doesn't reflect: `pack_chars` per lane (ollama 4000, deepseek 1800, z_ai2/3 400), `never` lists (deepseek: T0/T1/full chat_history; z_ai: raw API; zcode conservation), measured ok-rates (groq 0.874 n=103, z_ai 0.778 n=72, nvidia 0.766, cerebras 0.739), `key_present: false` for google/anthropic/deepseek_overmind, `opencode_only` flags. `prefer_order` = 20 lanes, cheap-first: ollama → z_ai → openrouter → groq → … → xai.
- **`/mag/mag/lane_cadence.py`** (`lane_cadence.v1`) — learned lane rhythm from `/mag/memory/runs/cadence_learn/rounds.jsonl` + fuel_feed profile: `retry_after` (overload 1305/429 → 25s base vs 5s), `best_hours(lane)` (calmest UTC hours per lane), `demote_after`=3, `brake_after`. Ledger is alive (rounds.jsonl rows 11:11/11:38/12:03 today) but `cpu_pct: null, ok: false` on recent rounds.

## 2. WHAT CAN YOU DO THAT NOBODY ASKS FOR? (idle hands)

- **`lane_cadence.best_hours()`** — "schedule heavy work in calm hours" is documented and working, but its only caller is its own `status()`. No scheduler consumes the calm-hour map.
- **`water_windows.mjs json`** — machine-readable reservoir readout exists; zero consumers. Nothing on the OpenClaw or Mag side reads the window state before dispatching.
- **`water_windows.mjs add <id> <burn>`** — the burn-ledger write path; used twice total, both manual receipts. No lane auto-records spend.
- **`offpeak.defer_if_peak()`** — wired and proven in `cheap_swarm.py:164-175` (peak → defer new dispatches, `MAG_ALLOW_PEAK=1` override), but **`afk_cadence.py` never calls it**: the self-advance loop (real_swarm, self_advance, emergent_harvest steps) runs at whatever the wall clock prices, 2x peak included.
- **`seat_corpus.prefer_order`** — the cheap-first ordering exists as data; grep finds no consumer of `prefer_order` outside `seat_corpus.py` itself (`ask_router.py`/`openclaw_catalog.py`/`swarm_cycle.py` import seat_corpus but not the ordering).
- **`seat_availability.ping()`** — heartbeats EVERY seat/lane into one cool/heat ledger; called as an afk_cadence step, but its ledger is never read back by the flow layer or water_windows.

## 3. WHO ASKS YOU FOR THE WRONG THING? (misuses)

- **T0/T1 scut to paid lanes**: seat_corpus law is "T0/T1 never remote" and ollama's `never` is "pay a remote for scut" — yet OpenClaw's default model is `deepseek/deepseek-v4-flash` (this very seat), so file-read/janitor-tier asks ride a paid lane with `never: T0, T1` on its contract. The ask is fine; the tier is wrong.
- **Asking the flow layer for live free-tier levels**: callers assume groq/cerebras/or_free "POLLED" means polled — it doesn't; no host-side poller writes those levels. Any routing decision made on those rows trusts a calendar, not a gauge.
- **Asking water_windows about desk seats**: grok_a/grok_b/chatgpt_codex rows are static text ("idle seat — hook-tracked") — no hook actually updates them, so burn/rate questions about desk seats get static answers.
- **Asking zcode before 09-02 12:52Z**: conservation law ("hands-off") is noted in the water table; requests routed to zcode before then violate the window by construction.
- **Asking afk_cadence to be price-aware**: it's asked to advance the self-advance machine but was never given the offpeak verdict — expecting cheap runs from it today is asking the wrong tier of that organ.

## 4. WHAT WOULD CONNECT YOU TO THE ADJACENT LAYERS? (the one wire)

- **One missing wire: a shared snapshot file.** If `water_windows json` + `offpeak.defer_if_peak()` + `seat_availability.status()` + `lane_cadence.status()` were folded (by one afk_cadence step or a cron line) into e.g. `/board/water_state.json`, the probe fleet gets a pre-flight gate: check the reservoir is OPEN + lane cooldown 0 + multiplier 1.0 before firing a probe. Today each organ writes its own private ledger and the probe fleet reads none of them.
- Second wire, same shape: **feed seat_availability heartbeats into water_windows' POLLED rows** so groq/cerebras/or_free levels become measured instead of asserted — the ping already exists (`seat_availability.ping()`), it just writes to a ledger water_windows never reads.
- Third: **`prefer_order` → ask_router/ladder**: the cheap-first ladder exists (`ladder.py` cites lane_cadence as "the curve's shape"); wiring the corpus ordering into lane selection makes the corpus contract load-bearing instead of documentation.

## 5. WARM-PACK: 3 just-in-time facts for a fresh driver

1. **DeepSeek time pricing is real and locally computable**: weekday Beijing 09:00–12:00 & 14:00–18:00 = 2x price, weekends all off-peak (`/mag/mag/offpeak.py`, `offpeak.v1`, CLI `python -m mag.offpeak pricing`); gate heavy NEW work with `defer_if_peak()`, override with `MAG_ALLOW_PEAK=1`. Don't trust a separate peak calculation — this is the one clock (water_windows.mjs duplicates the math).
2. **The reservoir map is 12 windows with honesty labels** (`water_windows.mjs`, run `node water_windows.mjs now|json`): OPEN/BURN/DESKTOP/POLLED — but only deepseek/zai windows are computed truth; groq_oss/cerebras/or_free levels are calendar-trust (no host poller), desk seats are static text, and the burn ledger `/board/water_ledger.jsonl` records only what someone manually `add`s (2 lines total). zcode is conservation-locked until 2026-09-02 12:52Z. (Verified live 2026-08-31 12:07Z: table runs clean, deepseek_offpeak OPEN 12h53m, zai_credits $19.25 of $20.)
3. **Lane contracts live in one JSON** (`/mag/memory/runs/seat_corpus/latest.json`, `seat_corpus.v1`): per-lane `pack_chars`, `never` lists, measured ok-rates, and `prefer_order` (cheap-first: ollama local before any remote; T0/T1 never remote). Read it before picking a lane — it's ~2 days stale (ts 2026-08-29), so re-verify key_present before trusting a lane.

## SELF-ATTACK (one pass, 2026-08-31)

- **Pointer drift**: the task said `/board/water_windows.mjs`; the real file is `/root/.openclaw/workspace/water_windows.mjs`. Claim adjusted above — but a second seat could cite the board path and both would be half-right; the map should record the actual path. Ledger IS at `/board/water_ledger.jsonl` (verified, 2 lines).
- **"prefer_order has no consumer"** is calibrated as a grep negative over `/mag/mag/*.py` today — absence of evidence, not proof; ask_router may honor cheap-first by its own logic without reading prefer_order (ladder.py exists and cites the same idea). Risk: overstating idleness.
- **"afk_cadence ignores offpeak"** — verified by grep (no offpeak import in afk_cadence.py), but afk_cadence's real_swarm step may itself defer; I did not trace real_swarm. The claim is about the cadence layer, not the swarm lane. Weaken to "not enforced at the cadence boundary" if challenged.
- **Staleness math**: seat_corpus ts 2026-08-29T17:46Z vs now 2026-08-31 ≈ 2 days old — fair; but its `fuel_ok_rate` fields are labeled as measured windows, so staleness degrades rates, not contracts.
- **Ran and verified**: `node water_windows.mjs now` executes clean at 2026-08-31T12:07Z (weekend BJ ⇒ OPEN path, 12 windows render, countdowns sane). Self-attack nit retired. The remaining uncertainty is only about real_swarm's internal behavior, not the row's claims.
