# DOGFOOD: THE OPERATING ENVIRONMENT — curvature + smith chart, lensed and mapped · 2026-09-22

_The ask: lens the curvature and smith-chart windows through tonight's render lens, map
them onto our existing systems as the DEFAULT operating environment across the mesh, and
answer plainly: what does this buy besides a headache?_

**Method note (meters-not-prose):** both meters were RUN before this card was written —
tonight's readings are in it. A meter with one reading is a photo; two is a trajectory.

---

## 1. Tonight's live readings (the dogfood, already running)

**Smith chart, second reading** (watch/inbox/ESTATE_SMITH_CHART_20260922.json):

| organ | Γ tonight | Γ yesterday | move |
|-------|-----------|-------------|------|
| supervisor | 1.00 | 1.00 | rot persists — reaper still unfixed, now visibly a full day |
| flash_lane_zai3 | 0.62 | 0.71 | **improved, nobody filed a report — the meter caught it** |
| deepseek | 0.00 | 0.00 | still the only delivering heavy lane |
| ollama_lane | 0.93 | — | reflecting hard |
| queue | 0.00 | 0.00 | delivering |
| day_work | 0.88 | 0.88 | stalled, unchanged |
| handoffs | 1.00 | 1.00 | 12 pending, zero delivered |
| checkpoint_apply | 1.00 | 1.00 | unchanged |

**Curvature scan, second reading** (CATHEDRAL_CURVATURE_SCAN_20260922.{json,png}):
5/6 regions SADDLE (contested) — water_computer 0.358, fractal_maze 0.129,
riddler_optics 0.134, audit_dungeon 0.124, adventure_2d6 0.483; riddler_engram DARK by
normal (a blind spot, mapped not hidden); descent vote reproduces: water-first shorter
in the estate's own eigen-metric (0.032 vs 0.036). Game module rewritten
(curvature_tiebreak.v1.json). Same world as yesterday — the instrument is repeatable.

## 2. The mapping — instrument → system surface → default trigger

| instrument | reads (reagents) | answers | becomes default via |
|------------|------------------|---------|---------------------|
| Γ smith chart | queue, logs, inbox bytes per organ | is this organ delivering or reflecting? | **brief generator**: a METERS block in memory/briefs/latest.md |
| curvature scan | game modules + the two build normals | where is the world contested? where is it blind? | window-close ritual (same slot as the audit) |
| descent vote / eigen-map | doctrine corpus TF-IDF LSA | which crossing is shorter, by our own metric? | already hosted; fires only on contested crossings |
| fleet Lyapunov V (candidate) | Γ + queue debt + staleness | is the fleet converging at all? | window close, bar pre-stated before first run |
| entanglement check (handoff Γ) | each handoff's claimed vs delivered | did correlation survive the channel? | 3 extra lines in the handoff template |
| unfolding law | any meter citation | is the number comparable? | one sentence of format law: name the normalization |
| Carleman hurdle list | the record program itself | convergence? condition number? extraction? | the standing risk register for record work |

**Why the brief is the wiring point:** every seat on every machine already boots by
loading `memory/briefs/latest.md` (LOAD→FRAMEWORK→AGENTS→handoff→brief). One generator
change — `mag.session_state_brief` imports ESTATE_SMITH_CHART_JSON +
CATHEDRAL_CURVATURE_SCAN_JSON and prints five lines — and the cockpit ships to the home
PC, the tablet, MagRemote, every remote seat, with zero new surfaces to read. The meters
ride artifacts that exist. The nightly schedule rides the drift-patrol cron, which is $0.

## 3. What it buys (besides the headache) — with today's receipts

1. **Time-to-detection collapses from hours to readings.** This morning's rot (day_work
   stalled=7, zombie slot, z_ai3 429) was found by a human asking, hours late. Tonight
   the same facts are machine readings, and the z_ai3 improvement (0.71→0.62) was caught
   with nobody reporting it. That is the whole product: drift without narration.
2. **The zombie class gets caught at formation.** Zombies formed while the reaper's PATH
   regression errored every ~30s because nothing summed errors into a number. supervisor
   Γ=1.00 is that number, and it has now said the same thing for a day — which is itself
   information: the no-prose list is not self-executing.
3. **Handoffs stop being hope.** Twelve pending handoffs with Γ=1.00: correlation
   between sender and receiver is currently untested. The 3-line entanglement check
   (what can the receiver act on, byte-named) converts each handoff into a measured
   event, and the queued trace-ids become the Bell test.
4. **Curvature is routing rules, not poetry.** All-saddle world ⇒ no straight walks: any
   task crossing a contested region must carry a tiebreak or run the walk-compare
   instead of arguing. β0 islands are where seats go stale — the BOOT_4_7 fossil that
   Clippy cited was an island. The map of blind spots (engram DARK-by-normal) is the
   list of places an agent must not pretend to see.
5. **Meter fights end.** Two meters disagreeing is two unfoldings, not a scandal —
   provided the normalization is named (Abul-Magd: some statistics shrug at bad
   unfolding, others silently absorb it).
6. **The record program gets its risk register for free.** Convergence: the −545 GB
   purge is a passed convergence test (the ghost survived; the record is what remains).
   Condition number: our own memory index just breached its size limit and started
   loading partially — a live instance of index-becomes-unreadable. Extraction: the
   brief generator is the extractor, already one command. Three named failure modes,
   each with a real instance on file, before we spend another dollar on the record.

## 4. What it does NOT buy (ractor chairs, on the record)

- **Detection is not repair.** supervisor has been REFLECTING for a day; the meter sees,
  only a fixer fixes. The reaper PATH fix stays the operator's fold-in item.
- It does not fix the z_ai3 balance, does not replace the referee GO, does not make any
  lane smarter. It changes how fast we know, not what we can do.
- **Meter theater is the standing risk.** If the METERS block is skimmed like weather,
  it is a headache with extra steps. Mitigation is already in the design: five lines in
  the brief, bar-exceeded organs named, no prose.
- Baseline law (logistic floor): a dumb sentinel — "lane silent >24h = RED" — ships in
  the same block. If the fancy Γ ever underperforms the floor, keep the floor and drop
  the chart.

## 5. The wiring bill (one rollover task, $0)

1. `mag.session_state_brief`: +METERS block (import both JSONs, print Γ table + saddle
   count + islands + no-prose list). ~20 lines.
2. Handoff template: +3 lines (claimed / delivered / what the receiver can act on).
3. Drift-patrol cron: +`estate_smith_chart.py --no-plot` and `curvature_scan.py` nightly,
   **each run appending its own register events** — the autoseal hook covers tool
   writes only, not bash-written meter outputs. Found live tonight: the two meter runs
   left 3 unsealed files and the audit flipped to TEETH-MARKS until they were
   registered by hand. The cron wrapper must seal what it writes.
4. Fleet Lyapunov V: stays a candidate until its bar is named; on GO it joins the same
   block as line five.

**Falsifier, pre-stated:** run meters-by-default for 14 days. If no incident in that
window is detected earlier than it would have been by hand, the default is retired and
only the smith chart survives as a manual tool. The meters owe us one early catch, or
they owe us their exit.

---
_Filed by the ZCode seat, 2026-09-22 ~01:3Z. Both meters executed tonight before this
card existed; receipts are the two JSON/PNG pairs in watch/inbox/. Lineage:
curvature worlds + estate smith chart (09-21) → render the system (09-22) → this card,
which is the one that asks them to hold a job._
