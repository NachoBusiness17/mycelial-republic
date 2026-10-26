# FW-29 — Cube assembly packet (operator gate packet)

- Board item: `watch/inbox/FIFTY_WIDE_BOARD_20260917.md:55` — "corrected BOM ($60–66) + Mon 09-22 checklist + burn-in test plan"
- BOM source: `watch/inbox/physical_computing/receipts/G-J_INSTRUMENT_TIER.md:140-155` (corrected stage-0 BOM, supersedes C17 rows 1-3 + rider)
- Plan source: `watch/inbox/physical_computing/receipts/C17_CUBE_INSTRUMENT_PLAN.md:160-180` (stage 0 registration + gates)
- Packet filed: 2026-09-28, Q-025 queue gopher. Date math re-checked 2026-09-28.

## 1. Corrected BOM (the $60-66 figure, line by line)

From G-J_INSTRUMENT_TIER.md:140-155. Changes vs C17 marked. Stage 0 is ELECTRONICS ONLY; no
fungus exists in stage 0 (CUBE1_SHOPPING_LIST.md rule 1: "If the rig can't measure nothing
cleanly, it never gets to claim something").

| # | Item | Change vs C17 | ~$ |
|---|---|---|---|
| 1 | ESP32-WROOM dev board x1 | unchanged | 9 |
| 2 | ADS1115 x2 — run at 8-16 SPS (was "860 SPS-class"; same part, firmware setting). x2 boards = 4 differential channels, not 2 (C17 undercounted); 4 addresses on the I2C bus = 8-diff scale-out path | spec fix, $ same | 12 |
| 3 | Ag/AgCl ECG electrodes 50-pk + snap leads | unchanged | 13 |
| 4 | Foil Faraday cage kit (foil, tape, clips, continuity-verified) — PROMOTED from optional rider to REQUIRED (FEMS checklist: cage "essential") | was optional | 12 |
| 5 | DIY chloridized Ag wire pair (bleach method) | rider -> required | 6 |
| 6 | Cal resistor + jumpers + LED (mostly drawer stock) | unchanged | 8 |
| 7 | SHT31 temp/RH | stage-0 stretch | +6 |
| | **TOTAL stage 0 with defenses** | | **~$60-66** |

Floor without defenses: $34. C17's "$31" was an arithmetic slip (9+12+13=34) — G-J:155.
Consumables assumed owned: jumper wires, breadboard or solder, isopropyl, tape/zip ties
(CUBE1_SHOPPING_LIST.md:14). Stage 1 (biology: oyster spawn $14 + two tubs + polyfill $6)
does NOT get ordered until stage 0 shows a clean floor (CUBE1_SHOPPING_LIST.md:32-53).

Why the defenses are not optional: skeptic rider puts artifact:signal odds at 95:5 without them
(CUBE1_SHOPPING_LIST.md:17); FEMS checklist adds the Donnan-potential confound on stainless
needles (hence Ag/AgCl, never stainless) and the fungal band 0.0003-0.1 Hz, so 1 Hz logging
suffices — spend on isolation, not speed (PHYSICAL_COMPUTING_PACK_20260916.md §6.7, :282-292).

## 2. Assembly checklist (stage 0, one session)

Scheduled date note: the plan said "assembly proposed Monday 2026-09-22 (fallback 09-29)"
(CUBE1_SHOPPING_LIST.md:52). Verified 2026-09-28: 2026-09-22 was a TUESDAY (the label in the
source docs is off by a day), and it has passed. Today is Monday 2026-09-28; the fallback window
(09-29) is tomorrow. This packet reschedules the checklist to the fallback: Tue 2026-09-29,
or any session this week — the plan has no deadline law, only an order law (stage 0 before stage 1).

- [ ] Order/place stage-0 parts from the BOM above (~$60-66 with defenses; $34 floor if you
      consciously waive defenses — recommended against, 95:5 odds).
- [ ] Build the Faraday cage: foil-lined opaque tub, foil on walls + lid, >=5 cm folded overlaps,
      seams taped; verify continuity with a DMM (< a few ohms any-point-to-any-point) (G-J:131-133).
- [ ] Wire the ear: ESP32 + 2x ADS1115 as 2 differential pairs (4 channels available); twisted-pair
      electrode leads inside the cage, shield grounded at the ADC end only, runs < 50 cm (G-J:135).
- [ ] Single ground bond: one alligator clip, foil -> ESP32 GND (battery minus). NO other ground
      path anywhere in the rig. Battery power only (USB power bank; laptop on battery or
      USB-isolated) (G-J:134).
- [ ] LED stimulus lives INSIDE the cage; its wiring twisted (G-J:137).
- [ ] Chloridize the Ag wire pair (bleach method) and land electrodes.
- [ ] Stage-0 physics setup: shorted-input phantom (electrodes clipped together) + dead-substrate
      control (no spawn) instrumented identically (C17:165-167).
- [ ] Start the 72 h burn-in log (below). Every reading lands in the hash-chained ledger; a
      flatlined sensor files EVIDENCE_DEAD against itself (CUBE1_SHOPPING_LIST.md:44-46).

## 3. Burn-in test plan (this IS C17 stage 0, registered verbatim)

Log 72 h continuous at 1 Hz, 2 differential channels (C17:167). Proceed criteria — ALL must pass:

| Gate | Threshold | Source |
|---|---|---|
| S0.1 noise floor | shorted-input RMS < 1 mV; electrodes-in-dead-substrate RMS < 2 mV (canon fungal spikes are mV-scale, so anything >= 5 mV stands 2.5x+ above floor) | C17:169-171 |
| S0.2 drift | baseline drift < 1 mV/h after 45-min warmup | C17:172-173 |
| S0.3 clock | timestamps monotonic, gap fraction < 1%, all gaps logged as explicit gap rows (never backfilled) | C17:174-175 |
| S0.4 stimulus artifact | GPIO/LED stimulus event visible on the record channel with measured cross-talk amplitude, documented, subtractable | C17:176-177 |

Iron laws for the burn-in (C17:161-163, 178-179):

- Analysis code committed (hash into a trail row) BEFORE the stage's data is touched for inference.
- No re-tuning-and-rerunning a failed stage on the same data; a v2 cube attempt = new registration.
- Kill = rig-kill, not claim-kill: any gate failure -> fix electronics, re-run stage 0.
- Max 2 rig iterations; a 3rd failure kills the rig idea itself (file it honestly).
- Output of record: the stage-0 noise dataset — the baseline that makes stage 2 non-vacuous.

Stage-1 ordering trigger: the day stage 0 shows a clean floor (CUBE1_SHOPPING_LIST.md:53).
Stage-2 verdict stays pre-registered (beat shuffled labels AND the dead twin, n=100, corrected
threshold, or the pack auto-retreats to "physical altar") (CUBE1_SHOPPING_LIST.md:47-48).

## 4. What this packet did NOT do

No parts ordered, no hardware touched, no code written. The gate is the operator's wallet and
hands, per the board section header. Only the date label was corrected (09-22 was a Tuesday, and
it passed; fallback 09-29 is live as of this filing).

Receipt: `watch/inbox/burn_reset_20260927/queue/Q-025.md` (FW-29 section).
