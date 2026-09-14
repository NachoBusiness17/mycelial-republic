# SALON R0 — "The Game at the Right Time" (2026-09-01 ~05:40Z)
> **[AUDIT-TYPED 2026-09-08]** status: PROSE · claims: offpeak.defer_if_peak is the fleet's only enforced wall-clock gate; desk_timing/water_computer are descriptive and the other budget windows are open-loop — SUPPORTED (path-cited source reads with line numbers, stat timestamps) · falsifier: a second organ found consuming a window gate, or the two clock surfaces disagreeing at the same instant (kill criteria K_T1/K_T2 in card)

Chair: round-0 lensed lane (cage-side, deepseek worker). Scope: evidence-only over `/mag`
(read-only, `read` tool + bounded `grep`/`stat`, no python3, no heredocs, no Mag CLIs).
Charter: `/board/inbox/MOONSHOT_RIGHT_TIME_20260901.md`.
Format reference: `/board/MOONSHOT_CHARTER_20260831.md` (§3 milestone table, §4 kill criteria).
Every claim is path-cited or marked **UNVERIFIED**.

---

## Q1 — REFERENT: which organ is "the game at the right time thing"

### Candidate 1: `desk_timing` (`/mag/mag/desk_timing.py`)

**What it does.** A pure in-memory recorder of per-speaker response latency + token estimates.
It never decides anything; it writes and formats. Key lines (head/body, `desk_timing.py`):

> `"""Desk agent response timing — elapsed ms + token estimates per speaker."""`
> `def record_timing(entry): ... _recent = (_recent + [entry])[-_MAX_RECENT:]  return entry`
> `def format_timing_row(...): ... return " | ".join(bits)`  (_UI_, not a gate)

Top-level docstring: desk_timing.py:1. `record_timing`: desk_timing.py:97-100. `format_timing_row`: desk_timing.py:148-158.

**State files.** None. `_recent` is a module-global list capped at `_MAX_RECENT = 24`
(desk_timing.py:15); `reset_timings()` clears it (desk_timing.py:172). No disk persistence.

**Last-modified signal.** `stat` → 2026-08-06 22:28:39 UTC (unchanged since Aug 6).

**Wired or orphaned?** **Wired (recorder).** Imported/used by `desk_dialogue.py` (lines 186, 224-237, 739-741, 847, 1051, 1169-1187), `local_scheduler.py` (191-231), `voice_turn.py` (385-412). Dashboard surface lives at `/mag/dashboard/rest.py` lines 3713-3714 (NOT rest.py:2160 as the charter claims — see note):

> `"timings": __import__("mag.desk_timing", fromlist=["last_by_speaker"]).last_by_speaker(),`
> `"timing_row": __import__("mag.desk_timing", fromlist=["format_timing_row"]).format_timing_row(),`

(dashboard/rest.py:3713-3714, route `POST/GET /api/v1/desk-dialogue` at rest.py:5091-5092.)

> **Charter cite correction (UNVERIFIED-as-stated):** the charter says surfaced "as dashboard
> `timings` at rest.py:2160". The actual `timings` surface is dashboard `rest.py:3713-3714`.
> rest.py:2160 in `/mag/dashboard/rest.py` is inside the loop-control handlers (start_loop/stop_loop),
> not the timings endpoint. The field `timings` does exist as cited at dashboard rest.py:3713 —
> the line number is stale, the field is real. Referent substance unaffected.

### Candidate 2: water clock / `water_computer.py` (+ `water_windows.mjs`)

Two distinct layers, both under the "water clock" family name — **do not conflate them.**

**(2a) Engine module `water_computer.py` (`/mag/mag/water_computer.py`)** — the *game* "you walk
water by gravity; wait is a season" (`SCHEMA = "water_computer.v1"`, water_computer.py:9). It
tracks tank heights + valves as campaign flags and runs one `gravity_tick` per cued `wait`/`work`:

> `def gravity_tick(camp): ... events.append("Gravity. " + ", ".join(moved) + ".")`
> `if atype == "wait": return {"ok": True, "handled": True, "events": ["You wait."] + gravity_tick(camp)}`

gravity_tick: water_computer.py:291-362; `wait`/`work` hubs: water_computer.py:455-459.

**State files.** Water campaign state = campaign flags persisted by `game_campaign` (tank heights
`water:source/work/out`, `valve:*`, phase — water_computer.py:36-88). No standalone clock file;
the "season" is *action-cued*, not wall-clock: an event loop advances state one tick per `wait`.

**Last-modified signal.** `stat` → 2026-08-29 22:36:01 UTC (most recently touched of the three).

**Wired or orphaned?** **Wired (rule handler).** `game_campaign.py` imports none/some by line:
786 (`is_module`/`seed`), 1624 (`extra_paths`), 1670 (`extra_legal`), 2122 (`glance`), 2200
(`handle` — the water-verb dispatcher), 2587 (`after`). So `water_computer.handle` intercepts
water verbs inside the campaign engine. Wired, functional, mid-run.

**(2b) Wall-clock budget clock `water_windows.mjs` (`/mag/mag` has NO copy; the pointer live copy
is `/board/water_windows.mjs`, header `v0`)** — the operator's *countdown* cron for every
quota/window (deepseek offpeak, zai_half_price to 09-09, groq 30RPM, cerebras 5RPM, or_free,
zai_credits $20 burn). It **reads** `/board/water_ledger.jsonl` (the burn ledger) and prints
countdowns; `add` appends a burn row. Key evidence:

> `const LEDGER = "/board/water_ledger.jsonl";` (water_windows.mjs)
> `const spent = (id) => burn.filter(...).reduce((s,b) => s + (b.amount||0), 0);` (water_windows.mjs)

`stat /board/water_ledger.jsonl` → 2026-09-01 03:39Z (actively written). This is a **descriptive
meter**: it reports windows and records spend, it does not block an action.

### Candidate 3: `game_freeze.py` (`/mag/mag/game_freeze.py`)

**What it does.** Builds "Socratic freeze packs" — high-fidelity snapshot of a campaign so any
seat can LOAD it (`SCHEMA = "mag_game_freeze.v1"`, game_freeze.py:12). "Timing as memory
boundary": capture state at exactly the right moment mid-run, layered L0/L1/L2. Key lines:

> `def build_freeze(camp, *, brawl=None): ...` (game_freeze.py:151)
> `def slice_layer(freeze, layer="L1"): ... """Socratic progressive disclosure."""` (game_freeze.py:306)
> `def freeze_campaign(campaign_id, *, brawl_id="", brawl=None): ... st["freeze_id"] = freeze["freeze_id"]` (game_freeze.py:369, 397)

**State files.** `FREEZE_DIR = ROOT/"memory/working/game_freezes"` (game_freeze.py:15), with a
`LATEST.json` tip pointer (game_freeze.py:112-128). Real JSON on disk — `LATEST.json` → points to
`gf-6fb4c8074c.json` (ts **2026-08-14T18:04:05Z**, campaign `gc-1b6bdffd05`, module
`dnd_classic_stub`).

**Last-modified signal.** `stat game_freeze.py` → 2026-08-07 05:14:57 UTC (code untouched since
Aug 7). **State is stale:** newest freeze pack is 2026-08-14 — ~18 days before today (09-01);
the two older packs are 2026-08-07. So the organ *exists and is wired* but has not frozen
anything in ~2.5 weeks. That is a notable "went quiet" signal.

**Wired or orphaned?** **Wired (action + Socratic help).** `game_campaign.py:2380-2405` routes
`atype == "freeze"` to `game_freeze.freeze_campaign(...)` and offers L0/L1 Socratic help
(`format_socratic_help`), `game_brawl.py` also imports it (brawl state). Live but idle lately.

### VERDICT (explicit referent)

**The unifier is `mag/offpeak.py` — the only wall-clock *authority* organ in the fleet — and the
charter's "temporal-authority frame" is the right target, with one correction:** the three named
organs are *capture/format* organs (desk_timing = descriptive recorder, water_computer = gated-
but-action-cued game physics, game_freeze = snapshot boundary), whereas the organ that actually
decides **WHEN** and gates an effect by the wall clock is `offpeak.py`:

> `def defer_if_peak(dt=None, *, allow_peak=None):`
> `    return {"ok": True, "defer": True, "action": "deferred_peak", "is_peak": True, ...}` (offpeak.py:101-106)

Invoked as an **enforcement** gate at:
> `cheap_swarm.py:168` `from mag.offpeak import defer_if_peak; d = defer_if_peak()`
> `lane_salon.py:81-84` `if defer_if_peak().get("defer"): ... "error": "deferred_peak — paid lane off-peak only (MAG_ALLOW_PEAK=1 overrides)"`

So, mapping the charter's question: the *phrase* "the game at the right time thing" reads most
naturally over the **water-clock family (candidate 2b/offpeak)** — it is the one that literally
pays/defers by the right window ("wait is a season"; deepseek 2x peak). But the **monolithic
temporal-authority frame is the load-bearing finding**: desk_timing records WHEN answers landed,
water_computer makes moves legal in-season, game_freeze captures state at the right instant, and
offpeak is the only one that *refuses an action* by the clock. The R0 thesis (one scheduler-
authority layer) survives contact with the source — it is currently *distributed, partial, and
half-enforced* rather than absent.

---

## Q2 — DELTA: descriptive-only vs enforced (strongest candidate = temporal authority / water-clock)

**Answer: mixed — mostly descriptive, with ONE enforced wall-clock gate (`offpeak`).** The
charter's Q2 premise ("open-loop, descriptors written, never enforced — like switchboard before
CLASSIFY") is **true for two of the three named organs and false for offpeak**.

**Descriptive-only evidence:**

1. **desk_timing** — writes to an in-memory `_recent` list and returns it; nothing consumes it
   to *block* anything. `desk_dialogue.py:235-236`:
   > `timing = fill_token_estimates(...); timing = record_timing(timing); return raw, mode, timing`
   The `timing` dict rides the return value; no branch uses `is_peak`/window to alter the reply.
   **Descriptive.**

2. **water_computer engine (2a)** — timing is *cued*, not wall-clock enforced: `wait`/`work` both
   always execute one `gravity_tick` regardless of the real clock:
   > `if atype == "wait": return {"ok": True, "handled": True, "events": ["You wait."] + gravity_tick(camp)}`
   > `if atype == "work": return {"ok": True, "handled": True, "events": ["You crank the pump."] + gravity_tick(camp)}`
   (water_computer.py:455-458). There is no `datetime` import in water_computer.py's heads I read;
   the "season" is a *simulated* turn sequence (rain→steam→ice→liquid), not Beijing time.
   **Descriptive/cued, not wall-clock-forced.**

3. **water_windows.mjs (2b)** — reports windows and appends to `/board/water_ledger.jsonl`
   (`add <id> <burn>`); nothing in the mjs gates a runner. **Descriptive meter.**

**Enforced evidence (the delta that matters):**

`mag/offpeak.py` **is** an enforced wall-clock authority — it *defers heavy NEW work* during DeepSeek
peak (weekday Beijing 09-12 / 14-18, 2x price):

> `def defer_if_peak(dt=None, *, allow_peak=None):`
>   `if allow_peak or not peak: return {... "defer": False, "action": "run", ...}`
>   `return {"ok": True, "defer": True, "action": "deferred_peak", "is_peak": True, "multiplier": 2.0, ...}`
   (offpeak.py:93-106)

Consumers treat `defer` as a gate that stops work:
- `cheap_swarm.py:168-173` — `d = defer_if_peak()`; on peak reports `"note": "peak pricing — new
  dispatches deferred to off-peak (MAG_ALLOW_PEAK=1 overrides)"`. So new dispatches are held.
- `lane_salon.py:81-84` — `if defer_if_peak().get("defer"):` returns `"error": "deferred_peak —
  paid lane off-peak only (MAG_ALLOW_PEAK=1 overrides)"`.
- `verified_clock.py:132` also imports `pricing` (readout, descriptive).

**Same** precedent the charter cites (switchboard before CLASSIFY): `offpeak` started as a pricing
readout (`pricing()`) and *became* an enforcement gate when cheap_swarm + lane_salon consumed
`defer`. So the temporal-payment layer is **already half-closed-loop**: the *DeepSeek-paid-lane*
axis is enforced; the *other* windows (groq RPM, cerebras TPD, or_free RPD, zai_credits) remain
descriptive polls in water_windows.mjs with **no gate consuming them** (they're "POLLED" rows;
the mjs itself cannot read usage cage-side: groq_oss row note "cage cannot read usage; poll from
host or trust deferrals").

**Conclusion (Q2):** not uniformly open-loop. **One temporal authority organ is enforced**
(offpeak on the deepseek peak window); **two named organs are descriptive** (desk_timing records,
water_computer cues); **the other budget windows are open-loop** (groq/cerebras/or_free/zai_credits
in water_windows.mjs are metered but not consumed by any gate). The moonshot's true charge is
**extending the enforced branch from "one window" to "all windows / one scheduler-authority".**

---

## Q3 — M1 one-command test for the temporal-authority moonshot

Mirroring `MOONSHOT_CHARTER_20260831 §3 M1` (`python -m mag.ask_router --record ...` →
PASS = marker-bearing outcome row). The temporal moonshot's M1 must prove a **single authority
organ** gates an effect by wall-clock window, not just reports it.

**M1 test (one command):**

```
node /board/water_windows.mjs add moonshot_temporal_p1 1 "M1 probe"
node --eval /board/water_windows.mjs  # (already the countdown readout; see note below on runner)
```

> **Runner note (UNVERIFIED-by-me, no Mag CLI):** the M1 harness command that *consumes* a window
> gate is the load-bearing piece. Candidate is the existing lane_salon/cheap_swarm defer path:
> `python -m mag.lane_salon round --pack ...` in a state where the "paid lane" is gated and
> `MAG_ALLOW_PEAK` unset → expect `"error": "deferred_peak"` during peak hours. I did not run it.
> Mark the exact one-liner as the operator-approval gate, consistent with §3 M1's staged-apply
> pattern.

**PASS criteria (all must hold):**
1. **One authority, two surfaces agree.** Against the wall clock, `mag.offpeak.pricing()`
   and `water_windows.mjs now` (deepseek_offpeak row) return the *same* open/closed verdict for
   the same instant — no clock drift between the two half-closed loops.
2. **Enforced, not just reported.** During peak, an actual heavy dispatch is *deferred* — a
   receipt row (per M1's marker-bearing-outcome style) appears with `action == "deferred_peak"`
   and `next_offpeak_utc`, i.e. the gate *refused work*, not merely logged a price.
3. **Override is explicit and operator-owned.** With `MAG_ALLOW_PEAK=1` (or equivalent operator
   blessing), the same call runs and writes a `run` row — proving the override path is intended,
   not a silent bypass.
4. **Ledger/meter rides the row.** The resulting outcome/ledger row carries cost (water-clock
   axis) — closing the "meter rides the row, not a side ledger" law from §2/§5, so
   `water_windows.mjs` can visually confirm spend.

**M1 shape target (mirroring §3 M1 semantics):** one command → PASS = a marker-bearing outcome
row whose class proves the gate fired on the clock. Same "closure defined by read-back, never by
apply intent" law as `MOONSHOT_CHARTER_20260831 §3 self-attack` — M1 is not done on the command
being staged; it is done on the receipt proving the gate deferred by wall-clock.

---

## Q4 — Kill criteria (measured facts that kill the temporal-authority thesis)

Drafted in `MOONSHOT_CHARTER_20260831 §4` style (K1-K5). Temporal-specific:

- **K_T1 — No clock authority, only timestamps.** If the audit finds every "timing" write is
  descriptive (desk_timing) and the only gate (offpeak) is a single hardcoded Beijing window
  consumed by just 2 call sites, THEN the phenomenon collapses to "one pricing guard," not a
  scheduler-authority layer. **Kill measuring fact:** after M1, no *second* organ consumes a
  window gate beyond cheap_swarm/lane_salon. Kill.
- **K_T2 — Wall-clock drift, two clocks disagree.** If `mag.offpeak.is_peak()` and
  `water_windows.mjs deepseek_offpeak` return conflicting open/closed for the same instant
  (the two half-closed loops disagree on Beijing time), the "one authority" frame is fiction.
  **Measured fact:** a probe of both surfaces at N staggered instants over 24h shows ≥1
  disagreement. Kill (or merge clocks first).
- **K_T3 — Gate never fires in practice.** If the deferred_peak error path has zero receipt
  rows in a week of normal cadence (i.e. heavy work never actually lands in peak), the gate is
  decoration — enforcement inferred from code, not witnessed from bytes. **Measured fact:** 0
  `action == "deferred_peak"` rows over 7 cadence days. Kill.
- **K_T4 — Water-clock meters stay open-loop** (mirrors §4 K5). If `water_windows.mjs` windows
  (groq RPD, cerebras TPD, or_free RPD) remain "POLLED — cave cannot read usage" and no gate
  consumes them (same as today), the "extends to all windows" promise is unmet. **Measured
  fact:** after M2, ≥1 non-deepseek window still has no consuming gate. Descope to the deepseek
  axis or kill the "unify all windows" claim.
- **K_T5 — No memory boundary, no freeze reuse.** game_freeze is the memory-side leg; if freeze
  packs remain stale (last pack 2026-08-14 as found) and no LOAD resume occurs, the "freeze at
  the right moment" leg is aspirational, not operational. **Measured fact:** no new freeze pack
  in the M1-M2 window while a campaign is active. Kill the memory-boundary clause (not the whole
  thesis).

**Not a kill:** desk_timing being in-memory descriptive — that's expected (presentation), but it
must not be *counted* as authority. Kill bias preserved: same as parent charter — a measured
negative *kills the shape*, never retrofit a new supervisor to pass (M2/M3 law).

---

## LENS (Lessig) — what the law-as-architecture lens adds

Lawrence Lessig's *Code* distinguishes four regulation modalities — law, norms, market, and
**architecture** (the physical/technical constraints that make some behavior literally impossible
vs merely costly). Applied to temporal authority:

1. **Architecture is the only genuine authority.** desk_timing is *norms* (shapes presentation,
   nudges, nothing stops). water_windows.mjs is *market* (prices windows, meters spend, reads a
   ledger; doesn't forbid the call). game_freeze is *law/language* (a contract a seat "must LOAD"
   — but a model can ignore it and imagine HP, which is why freeze packs wrap `slow_must_not`).
   **Only `offpeak.defer_if_peak` consumed by cheap_swarm/lane_salon is architecture**: it makes
   the peak-paid dispatch *not happen* (returns the effect, skips the work) unless an operator
   env flips. That is the difference the lens demands we name: **the fleet already runs on
   prices and norms (weak) and one architecture gate (strong).**

2. **"The game at the right time" as an architecture problem, not a law problem.** Writing a law
   ("thou shalt only run in-season") fails because the seat may ignore it. The design that
   *binds* the clock into the effect path — the authority organ that returns "deferred_peak"
   *instead of* the work — is the difference between a sign on the door (norms) and a door that
   is locked at 14:05 (architecture). Q3's M1 implicitly tests exactly this: does the gate
   *refuse*, or merely whisper?

3. **Architecture is the transferable lesson for freezing memory too.** The same Lessig frame
   diagnoses game_freeze: a freeze pack is a *law* object (LOAD me), easily violated by a warm
   model that invents HP. The moonshot's memory boundary only becomes architecture when the
   engine *enforces* `engine_owns` (fails the action, doesn't just docstring it) — same
   closed-loop pattern offpeak already proves on the price axis.

4. **Redundancy risk.** Having three separate organs each carry a private rule (norms in
   desk_timing, market in water_windows, architecture in offpeak) reproduces exactly the
   multi-authority fog the unifying frame is meant to dissolve. Lessig's sharpest cut: a single
   temporal-architecture layer (one organ whose *output* the effect broker honors, like
   switchboard/effect-broker authorize) is preferable to three partial organs that vet the clock
   at different strengths and can drift apart (K_T2). This strengthens — does not weaken — the
   R0 working thesis: **the missing organ decides WHEN in the *effect path* (architecture), not
   in a chart (norms/market).**

---

### Sources consulted (all quoted or observed above)
- `/mag/mag/desk_timing.py` (read, full — 173 lines)
- `/mag/mag/water_computer.py` (read, head/mid/tail — 577 lines)
- `/mag/mag/game_freeze.py` (read, head/mid — 432 lines)
- `/mag/mag/offpeak.py` (read, full)
- `/board/water_windows.mjs` (read, full — v0)
- `/board/water_ledger.jsonl` (tail — 5 rows, 2026-09-01T02:09–03:39Z)
- `/mag/dashboard/rest.py` (+ stat; `timings` at 3713-3714, not 2160)
- `stat` timestamps for desk_timing/water_computer/game_freeze/offpeak/dashboard rest.py
- `grep` call sites: desk_dialogue.py, local_scheduler.py, voice_turn.py, game_campaign.py
  (786/1624/1670/2122/2200/2587 for water; 2380-2405 for freeze), cheap_swarm.py:168-173,
  lane_salon.py:81-84, verified_clock.py:132
- `/mag/memory/working/game_freezes/LATEST.json` + `gf-6fb4c8074c.json` (head)

### Rejected paths (two-strike bail logs)
- Full-tree `find /mag -name environments.json` + `find /mag ...` over the whole tree were slow/
  hung; killed, re-scoped to bounded `ls`/`find -maxdepth 3` (found `/mag/watch/environments.json`
  and `/board/environments.json`). No content invented from the incomplete scan.
- Full-tree `grep -rln water_windows ... /mag /board` hung; killed, re-scoped to targeted
  `ls /board/water_windows.mjs` + ledger tail. No third attempt made.
