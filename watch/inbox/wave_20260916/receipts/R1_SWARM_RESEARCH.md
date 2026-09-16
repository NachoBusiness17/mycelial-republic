# R1_SWARM_RESEARCH — wave_20260916

- Agent: ZCode swarm-research lane
- Date: 2026-09-16
- Budget: $0 (free lanes / local only — abort at any paid wall)
- Interpreter rule: `.venv\Scripts\python.exe` / `mag.cmd` only. No git commands.
- Status: IN PROGRESS — receipt opened before work; appended as I go.

## Plan
1. Read `main.py` swarm subcommand (~L201) + `mag/swarm_run.py` etc. to learn options, lanes, cost guards.
2. Brief: mycelium as memory hierarchy — implementable read/write mechanisms for an instrumented mycelium cube (biological computing, reservoir computing, slime-mold routing, OhmSh/phase-change memristors, OECTs). Cite mechanisms, not visions.
3. ONE bounded pass: `main.py swarm --once` (or equivalent) free lanes only; fallback `research_fanout.run` 12-question battery if machinery is paid-provider-entangled. Record path taken.
4. Fold: per-answer one-liners, 5 steals → `DESIGN_MYCO_MEMORY_20260916.md`, dead lanes.

## Machinery inspected
- `main.py` L200-206: `swarm` subcommand → `mag.task_router.fire_swarm(goal, --size 2-5, --dry)`.
- `mag/task_router.py` L200-231 `build_parallel_swarm`: angles (code/architecture/data_flow/patterns/risks) + synthesize; **hardwired `provider: "deepseek", model: "deepseek-v4-flash"`** (paid wall).
- `fire_swarm` L234-281: does NOT execute inline — appends tasks to `memory/copilot/inbox.jsonl` for a Ghost to pick up on its next cycle. No answers tonight unless a ghost worker runs.
- **Verdict: paid-provider entanglement + deferred execution → fallback taken per mission step 3.**
- Evidence: `mag.cmd swarm "…" --dry` → `SWARM PREVIEW: 4 agents, $0.00052` (preview only; nothing fired).
- Fallback: `mag/research_fanout.py` (schema `research_fanout.v1`) — free lanes only (groq ×3, cerebras ×2, mistral ×2, zai-lite w/ lite_guard pacing, OpenRouter :free ×4 incl. time-boxed union-alpha). Paid keys XAI/ANTHROPIC/OPENAI deliberately excluded by the module's own header. `call_lane` never raises; every call = one JSONL receipt row.

## Calls
- `mag.cmd swarm "…" --dry` — preview, $0, nothing fired.
- `r1_swarm_research_driver.py` (wave dir): monkeypatches 12-question myco battery (M01-M12) onto `research_fanout`, redirects OUT/RAW/PACK into `wave_20260916/r1_fanout_runs/` (keeps `memory/runs/research_50_wow/` clean), `probe_lanes()` FIRST → live lanes only → ONE `run(workers=6, timeout=150)` pass. Free lanes only; paid-wall errors recorded as dead lanes, not retried.

## Results
- Probe: 9 live / 3 dead. Dead lanes: `mistral-small` (probe fail), `or-union-alpha` (probe fail), `or-glm52` (probe fail).
- Pass 1: 7/12 answered (M01, M02, M04, M06, M08, M11, M12). Failures: M03/M05/M07/M09 `empty_content` (reasoning models spent the budget), M10 HTTP 429 (groq rate limit, NOT a paid wall).
- Bounded retry round (module's own `retry()`, winners-only lanes, appends only): all 5 remaining myco qids recovered → **12/12 myco answered**.
- **Overshoot disclosure (lane-law slip, $0 impact):** first retry invocation forgot to re-patch `BATTERY` in the fresh process, so the module's default 50-question WoW battery fired (~55 extra rows, free lanes only, receipts in wave dir). Corrected: second retry loaded the myco battery from `r1_swarm_research_out.json` (single source of truth) and touched only the 5 failed myco qids. No paid lane contacted; no budget breached; discipline breach recorded here.
- Per-answer one-liners (LEADS, not facts — one lane even produced a rickroll citation; see design file):
  - M01 (spikes): skeptical lane — claims no true APs in mycelium, slow potentials only; directly contradicts M09. Falsifiable fast, which is useful.
  - M02 (habituation): Physarum habituation onset ~3-4 repeated stimuli; recovery ~45-60 min; physiological memory = minutes-hours.
  - M03 (reservoir): reservoir readout = linear ridge/logistic regression over electrode/camera streams; Physarum reservoirs published; mycelium reservoir claim needs DOI check.
  - M04 (routing): Tero rule dD/dt = a|Q|^γ/D − bD; reroute 30-90 min; ~5 min thickening under strong gradient; electrical resistance hysteresis 10-30 s.
  - M05 (memristors): fungal memristor lead: set/reset ±0.55 V, on/off 5-22, retention ≥10^4 s, endurance ~120 cycles; bit = ion redistribution + hydration. DOIs unverified.
  - M06 (OECT): PEDOT:PSS ionic→electronic transduction, sub-1 V ionic gating, Clevios PH1000-class materials — the head for the ionic substrate.
  - M07 (instrumentation): Ag/AgCl / Pt / stainless electrodes; SpikerBox 4ch ~15 µVrms; OpenBCI Cyton 8ch 24-bit ~5 µVrms; Intan 32ch ~1.5 µVrms.
  - M08 (memory): trained-tube imprint in Physarum = memory in tube architecture itself, persists past habituation recovery; medium = tube-diameter history.
  - M09 (coding): Zipf "fungi language" claims vs surrogate-data critiques (shuffle, dead-mycelium baseline, ISI permutation) — adopt as the stack's built-in falsifier.
  - M10 (growth): Pleurotus 1.5-4.2 mm/day depending on substrate/temp; growth halts <10°C; barriers deflect growth — L3 write mechanism. Citation quality poor (rickroll link, court-case cite) — magnitudes plausible, sources must be re-derived.
  - M11 (BOM): OpenBCI Cyton+Daisy 16ch stack ≈ $530 all-in; micro-SD logging; under $600 for full cube instrumentation.
  - M12 (comparison): spike read ~1 bit/s; impedance sweep non-destructive, >10^6 cycles, seconds per sweep; imaging ~1 bit/hour; hybrid OECT/memristor fastest. Plausible pairs today: impedance-read + growth/environment-write; OECT-read + ionic/electrical-write.
- Fold artifacts: `watch/inbox/wave_20260916/DESIGN_MYCO_MEMORY_20260916.md` (5 steals + memory-hierarchy table + verification queue).
- Raw artifacts: `watch/inbox/wave_20260916/r1_fanout_runs/raw.jsonl` (73 rows), `r1_swarm_research_out.json`, `pack.md`, `receipt.json`; drivers `r1_swarm_research_driver.py`, `r1_retry_driver.py`.

## Final confirmation
- **Machinery used:** `main.py swarm` inspected and dry-previewed → paid-entangled (deepseek) + ghost-queue only → **fallback taken**: `mag/research_fanout.py` (`research_fanout.v1`) with 12-question myco battery monkeypatched in, probe-first, live lanes only, one bounded `run()` + one bounded `retry()` round.
- **Calls:** 85 free-lane HTTP calls total = 12 probe + 12 pass-1 + 55 accidental WoW overshoot (disclosed above) + 6 myco retry. All free tiers (groq, cerebras, mistral-lite lane, zai-lite w/ lite_guard, OpenRouter :free).
- **$0 confirmation: $0.00 spent.** No paid provider contacted; no key of a paid provider (XAI/ANTHROPIC/OPENAI/deepseek) touched; HTTP 429 was a rate limit, not a paid wall; no paid wall was hit, so nothing needed aborting.
- **The 5 steals:** (1) mycelium memristance as L1 register (±0.55 V write, hours retention); (2) reservoir readout = linear ridge layer over the same electrode stack; (3) Tero-rule tube topology as L2 state variable, impedance-readable; (4) PEDOT:PSS OECT as the ionic↔electronic head; (5) surrogate-data falsifier (shuffle + dead-mycelium controls) built into the signal stack.
- **The one mechanism that changes cube build order if true:** electrical write + electrical read inside living mycelium (memristive hysteresis at ~±0.55 V, hours-scale retention) — if verified, build electrodes + impedance/OECT head FIRST and the cube is a layered memory hierarchy from week one; if falsified, the project collapses to structural (growth-scale) memory and slows to days-long feedback loops. This is experiment #1 for the ~$530 rig.

Status: DONE.
