# SALON RIGHT-TIME R1 — LESSIG lens (law-as-architecture) — CORRECTED by parent

> Provenance: lane salon-rt-r1-lessig-retry (gpt-oss-120b @ cerebras, 4m40s) delivered the
> schema design but failed byte-verification (no output file; offpeak quote line numbers
> fabricated 99–106 → real 121–141; "smallest experiment" cited .js modules that don't
> exist). Per two-strike law, parent reconstructs below with verified cites. Schema design
> is the lane's; cites are parent-fixed. Every line number below was read from disk.

## 1 — Gate contract (the lane's schema, kept because it's sound)

| Field | Type | Values |
|---|---|---|
| `window` | string id | `deepseek_offpeak` · `zai_halfprice` · `zai_offpeak` · `groq_rpm/rpd` · `cerebras_tpd` · `or_free_rpd` · `water:<reservoir>` |
| `scope` | enum | `lane` · `model` · `campaign` |
| `action` | enum | `defer` (delay new work) · `deny` (reject) · `shape` (modify params, e.g. price multiplier) · `freeze` (snapshot + halt) |

Worked example (real, mirrors the existing gate):

```json
{"window": "deepseek_offpeak", "scope": "lane", "action": "defer"}
```

Ellul amendment adopted into the schema: every row MUST carry `meter: invoiced | polled | none`
— no gate may fire on a meter it cannot read (garbage-in drift, K_T2 sharpened).

## 2 — Chokepoint and bypass (adversarial view)

- **Primary chokepoint:** `cheap_swarm.py:165-175` — the dispatch pre-check that consumes
  `defer_if_peak()` and returns `deferred_peak` before queuing new work (parent-verified:
  multiplier 2.0, next_offpeak_utc in payload). Secondary: `lane_salon.py:81-84` (R0-cited).
- **The gate law:** evaluate the rule table BEFORE the `MAG_ALLOW_PEAK` env override is
  inspected. Real override lives at `offpeak.py:121-141`:
  `allow_peak = os.environ.get("MAG_ALLOW_PEAK",...)` → `if allow_peak or not peak: run`
  else `deferred_peak`. Today one env var is the whole constitution — the bypass IS the knob.
- **Bypass extension (adversary's move):** spoof the wall clock / tz (`is_peak` is BJ-based)
  or set the env var in any caller's environment. Defense: gate reads one authoritative
  clock source (host time + explicit tz config), and privileged overrides require an
  operator-blessed receipt, not an env var.

## 3 — Q5 verdict (lane's: YES; parent accepts with corrected experiment)

**Verdict: YES** — temporal authority (the gate table), prompts-as-games (freeze packs as
rules-before-play), and the ractive loop (RolePacket scene) are one program: the game board
is the rule table, the freeze pack is the dealt state, the ractor is the human in the loop.

Smallest playable experiment (corrected, real paths only):
1. Temporal: at a peak-priced hour, dispatch one cheap deepseek task with metering on →
   PASS = receipt row with literal `deferred_peak` action (the gate refused by wall clock).
2. Ractive: one RolePacket scene per Diamond Age pack step #5 (local model → human ractor →
   frontier), freeze pack loaded before play.
3. Composition: the deferred task's receipt is the "move" the ractor re-plays in the scene —
   one artifact proving both halves talk to each other.
