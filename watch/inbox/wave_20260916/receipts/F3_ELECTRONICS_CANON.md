# F3 — ELECTRONICS CANON (wave 2026-09-16)

- **Lane:** F3 · free+legal only · no git
- **Mission:** instrumentation/electronics free canon → `memory/corpus/electronics_canon/` for the cube rig's builders
- **Law:** receipt FIRST, append as you go (this file)
- **Targets:** TI Op Amps For Everyone (Mancini) · TI Understanding Basic Analog series · ADI seminar notes (op amp basics, sensor signal conditioning) · Lessons In Electric Circuits (Kuphaldt, 6 vols) · All About Circuits textbook · NI/Keysight ADC-noise & ENOB white papers · OpenBCI Cyton schematics · Adafruit/SparkFun ADS1115 + I2C mux tutorials

## Plan

| # | Target | Source | Status |
|---|--------|--------|--------|
| 1 | TI "Op Amps For Everyone" (slyb143/SLOD006 lineage) | ti.com | pending |
| 2 | TI "Understanding Basic Analog" series | ti.com | pending |
| 3 | ADI seminar notes: op amp basics + sensor signal conditioning | analog.com | pending |
| 4 | Lessons In Electric Circuits (6 volumes) | ibiblio.org | pending |
| 5 | All About Circuits free textbook | allaboutcircuits.com | pending |
| 6 | NI/Keysight ADC noise + effective bits | ni.com / keysight.com | pending |
| 7 | OpenBCI Cyton schematic PDFs | docs.openbci.com | pending |
| 8 | Adafruit/SparkFun ADS1115 + I2C mux tutorials | cdn-learn.adafruit.com / learn.sparkfun.com | pending |

## Fetch log (append as you go)

*(start 2026-09-16, receipt filed before first byte fetched)*

### [1+2] TI — DONE (4 docs, ~5.6 MB)
- `TI_OpAmpsForEveryone_DesignGuide_SLOD006B.pdf` (2.06 MB) — Ron Mancini design guide Rev. B. TI retired `/lit/an/slod006b/` path (404); fetched from TI's own E2E attachment mirror (e2echina.ti.com).
- `TI_OpAmpHandbook_SBOA092B.pdf` (2.89 MB) — TI Handbook of Op Amp Applications (Bruce Carter; the current TI-hosted full book of the Op Amps For Everyone lineage).
- `TI_UBA_IdealOpAmps_SLAA068B.pdf` (0.64 MB) — Understanding Basic Analog – Ideal Op Amps, Mancini.
- `TI_UBA_CircuitEquations_SLAA067.pdf` (0.07 MB) — Understanding Basic Analog – Circuit Equations, Mancini.
- Note: SLYB143 direct + `/lit/pdf/slyb143` both 404 on ti.com today (literature purged); SLOD006B/SBOA092B + UBA series cover the slyb143 lineage. Titles verified via pypdf metadata/first page.

### [4] Lessons In Electric Circuits — DONE (6 volumes, ~22 MB, ibiblio.org, Kuphaldt)
- `LIEC_Vol1_DC_Kuphaldt.pdf` (4.50 MB) · `LIEC_Vol2_AC_Kuphaldt.pdf` (4.55 MB) · `LIEC_Vol3_Semiconductors_Kuphaldt.pdf` (4.19 MB) · `LIEC_Vol4_Digital_Kuphaldt.pdf` (3.66 MB) · `LIEC_Vol5_Reference_Kuphaldt.pdf` (1.06 MB) · `LIEC_Vol6_Experiments_Kuphaldt.pdf` (4.02 MB)
- Source: ibiblio.org/kuphaldt/electricCircuits/ (open content). All six %PDF-verified.

## Fetched table + totals

*(filled at close)*

## Best doc for the cube's differential front end

*(filled at close)*
