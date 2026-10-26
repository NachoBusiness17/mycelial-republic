# CUBE 1 — Shopping list (stage 0 now, stage 1 with the spawn)

Street prices from the C17 survey (±, ~$55 total; $31 touches the register today).
Stage 0 = electronics only. Stage 1 = biology. Nothing in stage 1 exists until the ear works.

## STAGE 0 — the ear (~$31)

| Part | What it is | Why | ~$ |
|---|---|---|---|
| ESP32 dev board (1x) | pocket WiFi microcontroller | the logger: reads the converters, timestamps, posts to the trail | 9 |
| ADS1115 16-bit ADC breakout (2x) | precision analog-to-digital converters | the signals are tiny (nV–mV range); the ESP32's own pins are too deaf — these are the magnifying ears. Two = differential pairs | 12 |
| Ag/AgCl ECG electrodes (pack) | hospital heart-monitor gel pads | the probes. Silver/silver-chloride is the chemistry that doesn't poison the reading — the FEMS checklist explicitly warns stainless needles put a metal-salt confound in the signal | 13 |

Consumables assumed owned: jumper wires, breadboard or solder, isopropyl, tape/zip ties.
Add ~$8 wire/LED if the drawer is bare (part of the $55 full-BOM figure).

### The skeptic's rider (S3 lane, 2026-09-16) — artifact:signal odds ≈ 95:5 without defenses

Three cheap additions that make the difference between hearing the room and hearing the
fungus — recommended before stage 0's floor is called "clean":

| Defense | Kills | ~$ |
|---|---|---|
| Foil-lined box (Faraday cage) + battery power | EM pickup — the #1 false signal | 10–15 |
| Chloridized silver wire pair (DIY Ag/AgCl) | electrode-interface chemistry | 5–10 |
| ~$6 calibration resistor + signal injection, $5 DHT22 temp/humidity logger | analysis overfit + moisture transients (whose band matches the claimed fungal band exactly) | 11 |

Stage-0 total with defenses: ~$45–60. The dead twin stays the primary control — the skeptic's
own words: only a twin-subtracted, stimulus-locked, kill-switchable difference counts.
"We detected something" is the least interesting outcome; that sentence is the design.

## STAGE 1 — the body (~$20-24, only after stage 0 proves the ear)

| Part | What it is | Why | ~$ |
|---|---|---|---|
| Oyster mushroom spawn (1 bag) | living mycelium on grain | the substrate inhabitant; oyster = fast, forgiving, and the species with the most published sensing data | 14 |
| Clear storage tubs (2) + polyfill | the container + humidity fill | one live cube, one killed control (same tubs, same everything — the control is the experiment) | 6 |

## The rules the rig obeys (from the pre-registered plan)

1. Stage 0 runs with NO fungus: days of noise-floor logs. If the rig can't measure
   nothing cleanly, it never gets to claim something.
2. Stage 1: two identical tubs — one inoculated, one cooked. Both wired identically.
   The dead twin is the baseline the live one must beat.
3. Every reading lands in the fleet's hash-chained ledger; a flatlined sensor files
   EVIDENCE_DEAD against itself. No invisible failures.
4. Stage 2 verdict is pre-registered: beat shuffled labels AND the dead twin, n=100,
   corrected threshold — or the pack auto-retreats to "physical altar."

## Buy timing

Order stage 0 whenever; assembly proposed Monday 2026-09-22 (fallback 09-29).
Stage 1 order goes in the day stage 0 shows a clean floor.
