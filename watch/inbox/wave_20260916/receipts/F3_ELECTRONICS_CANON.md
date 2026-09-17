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

### [3] ADI (Analog Devices) — DONE (13 PDFs, ~25.6 MB)
- analog.com hard-resets curl/schannel and times out PowerShell (Akamai edge blocking this network's TLS fingerprints). **node v22 fetch passed** — full ADI set pulled straight from analog.com:
  - `ADI_OpAmpApplicationsHandbook_Jung_full.pdf` (17.12 MB, 895p) — Walt Jung, Op Amp Applications Handbook, complete (mirror: archive.org item Op_Amp_Applications_Handbook_Newnes_Walt_Jung; ADI distributes free).
  - `ADI_OpAmpApplicationsHandbook_Sec1_OpAmpBasics_Jung.pdf` (1.62 MB, 130p) + `Sec2_SpecialtyAmplifiers_Jung.pdf` (0.68 MB, 54p) — the legendary seminar sections from analog.com (Sec2 lost once after download — sync/AV hiccup — re-fetched and verified).
  - `ADI_BasicLinearDesign_Ch1_TheOpAmp.pdf` (3.83 MB, 104p) — Zumbahlen lineage, analog.com.
  - `ADI_SensorSignalConditioning_Sec2_BridgeCircuits.pdf` (0.17 MB, 19p) + `Sec3_Amplifiers.pdf` (0.40 MB, 58p) — Kester's "Practical Design Techniques for Sensor Signal Conditioning" seminar book, the exact sections the cube front end needs.
  - MT tutorial set: `MT-001` (SNR=6.02N+1.76dB), `MT-032` (ideal VFB op amp), `MT-033` (VFB basics), `MT-060` (instrumentation amp), `MT-061` (in-amp DC errors), `MT-062` (in-amp noise) — 0.66 MB total.
- Note: full sensor-book scan on archive.org (bwb_S0-ABP-308, 21 MB) is controlled-loan (401); OCR-text copies exist but scans restricted → sections fetched direct from ADI instead.

### [6] NI / Keysight — DONE (2 docs, 1.43 MB) with one pointer
- `Keysight_5989-5732EN_Evaluating_Oscilloscope_Sample_Quality.pdf` (1.40 MB, 16p) — the ENOB ("effective number of bits") analysis app note. keysight.com 403s all direct asset paths from this network; fetched from TestUnlimited's public mirror of Keysight's freely-distributed PDF.
- `NI_cDAQ_EffectiveNumberOfBits_ENOB_KB.html` (0.04 MB) — NI knowledge base "cDAQ Effective Number of Bits (ENOB)" article body captured (14 ENOB mentions verified in-file).
- Pointer: newer Keysight white paper 5992-3675 "Understanding ADC Bits and ENOB in Oscilloscopes" exists but keysight.com serves only a JS shell to non-browsers — not captured.

### [7] OpenBCI Cyton — DONE (4 files, 1.72 MB) — openbci_cyton/
- No public PDFs exist: OpenBCI publishes schematics as images on docs.openbci.com/Cyton/CytonSpecs/. Captured: `OpenBCI_Cyton_32bit_Schematic.jpg` (1.03 MB — the Cyton-era board), `OpenBCI_Daisy_Schematic.jpg` (0.51 MB), `OpenBCI_USB_Dongle_Schematic.jpg` (0.17 MB), `CytonSpecs_page.html` (0.04 MB).

### [8] Adafruit / SparkFun — DONE (2 PDFs + 2 HTML, 9.87 MB)
- `Adafruit_ADS1115_4ChannelADC_Breakout_Guide.pdf` (4.16 MB, 26p) — ADS1015/ADS1115 I2C ADC guide (learn.adafruit.com PDF export).
- `Adafruit_TCA9548A_I2C_Mux_Guide.pdf` (4.95 MB, 26p) — 1-to-8 I2C multiplexer guide.
- `SparkFun_Qwiic_12Bit_ADC_ADS1015_HookupGuide.html` (0.04 MB) + `SparkFun_Qwiic_Mux_TCA9548A_HookupGuide.html` (0.10 MB) — SparkFun's ADS1x15 guide is the ADS1015 (12-bit), not ADS1115; Adafruit's covers the 16-bit part.

### [5] All About Circuits textbook — POINTER (0 bytes, Cloudflare 403)
- allaboutcircuits.com/textbook/ 403s non-browser fetches. Materially covered anyway: AAC's textbook IS the modernized web edition of Kuphaldt's LIEC (same open license), and all 6 LIEC volumes are in this canon. Canonical URL recorded for human browsing: https://www.allaboutcircuits.com/textbook/

## Fetched table + totals

| # | Artifact | MB | Pages | Source |
|---|----------|-----|-------|--------|
| 1 | TI_OpAmpsForEveryone_DesignGuide_SLOD006B.pdf | 1.97 | 464 | e2echina.ti.com (TI retired lit path) |
| 2 | TI_OpAmpHandbook_SBOA092B.pdf | 2.89 | 94 | ti.com |
| 3 | TI_UBA_IdealOpAmps_SLAA068B.pdf | 0.64 | 10 | ti.com |
| 4 | TI_UBA_CircuitEquations_SLAA067.pdf | 0.07 | 14 | ti.com |
| 5 | ADI_OpAmpApplicationsHandbook_Jung_full.pdf | 17.12 | 895 | archive.org |
| 6 | ADI_BasicLinearDesign_Ch1_TheOpAmp.pdf | 3.83 | 104 | analog.com (node) |
| 7 | ADI_OpAmpApplicationsHandbook_Sec1_OpAmpBasics_Jung.pdf | 1.62 | 130 | analog.com (node) |
| 8 | ADI_OpAmpApplicationsHandbook_Sec2_SpecialtyAmplifiers_Jung.pdf | 0.68 | 54 | analog.com (node) |
| 9 | ADI_SensorSignalConditioning_Sec3_Amplifiers.pdf | 0.40 | 58 | analog.com (node) |
| 10 | ADI_SensorSignalConditioning_Sec2_BridgeCircuits.pdf | 0.17 | 19 | analog.com (node) |
| 11 | ADI_MT-033_VoltageFeedbackOpAmpBasics.pdf | 0.25 | 8 | analog.com (node) |
| 12 | ADI_MT-001_SNR_6.02N_plus_1.76dB.pdf | 0.09 | 7 | analog.com (node) |
| 13 | ADI_MT-061_InAmpDCErrors.pdf | 0.12 | 5 | analog.com (node) |
| 14 | ADI_MT-032_IdealVoltageFeedbackOpAmp.pdf | 0.06 | 6 | analog.com (node) |
| 15 | ADI_MT-062_InAmpNoise.pdf | 0.08 | 5 | analog.com (node) |
| 16 | ADI_MT-060_InstrumentationAmplifier.pdf | 0.06 | 6 | analog.com (node) |
| 17 | LIEC_Vol2_AC_Kuphaldt.pdf | 4.55 | 574 | ibiblio.org |
| 18 | LIEC_Vol1_DC_Kuphaldt.pdf | 4.50 | 557 | ibiblio.org |
| 19 | LIEC_Vol3_Semiconductors_Kuphaldt.pdf | 4.19 | 535 | ibiblio.org |
| 20 | LIEC_Vol6_Experiments_Kuphaldt.pdf | 4.02 | 425 | ibiblio.org |
| 21 | LIEC_Vol4_Digital_Kuphaldt.pdf | 3.66 | 516 | ibiblio.org |
| 22 | LIEC_Vol5_Reference_Kuphaldt.pdf | 1.06 | 172 | ibiblio.org |
| 23 | Adafruit_TCA9548A_I2C_Mux_Guide.pdf | 4.95 | 26 | cdn-learn.adafruit.com |
| 24 | Adafruit_ADS1115_4ChannelADC_Breakout_Guide.pdf | 4.16 | 26 | cdn-learn.adafruit.com |
| 25 | Keysight_5989-5732EN_Evaluating_Oscilloscope_Sample_Quality.pdf | 1.40 | 16 | TestUnlimited mirror (Keysight 403s direct) |
| 26 | openbci_cyton/OpenBCI_Cyton_32bit_Schematic.jpg | 1.03 | - | docs.openbci.com |
| 27 | openbci_cyton/OpenBCI_Daisy_Schematic.jpg | 0.51 | - | docs.openbci.com |
| 28 | openbci_cyton/OpenBCI_USB_Dongle_Schematic.jpg | 0.17 | - | docs.openbci.com |
| 29 | SparkFun_Qwiic_Mux_TCA9548A_HookupGuide.html | 0.10 | - | learn.sparkfun.com |
| 30 | openbci_cyton/CytonSpecs_page.html | 0.04 | - | docs.openbci.com |
| 31 | SparkFun_Qwiic_12Bit_ADC_ADS1015_HookupGuide.html | 0.04 | - | learn.sparkfun.com |
| 32 | NI_cDAQ_EffectiveNumberOfBits_ENOB_KB.html | 0.04 | - | knowledge.ni.com |

**TOTAL: 61.72 MB · 32 files · 24 PDFs (~4,800 pages) · 3 schematics · 5 HTML captures.** Every PDF byte-verified: %PDF signature + pypdf page-count pass. All sources free to access; no paywalls, no logins, no git. All durable copies at `memory/corpus/electronics_canon/`; this receipt at `watch/inbox/wave_20260916/receipts/`.

## Best doc for the cube's differential front end

**Verdict: TI "Op Amps For Everyone" Design Guide (SLOD006B, Mancini) — `TI_OpAmpsForEveryone_DesignGuide_SLOD006B.pdf`.**
It is the one book written explicitly to take a non-specialist from "what is an op amp" to a working signal chain, and its chapters map 1:1 onto the cube rig's needs: single-supply circuit design (battery cube reality), signal conditioning for sensors, and instrumentation-amp topology — while every other candidate here assumes you already know why. Working path for the mycology builder: read SLOD006B for the foundation, then the ADI MT-060/061/062 in-amp trio (19 pages total) for exactly how a differential/instrumentation front end rejects the common-mode mush a moist fruiting chamber produces, then crib the OpenBCI Cyton 32-bit schematic (in `openbci_cyton/`) as the proven reference build, with Jung Sec2 + Kester Sec3 as the deep reference. Runner-up for fastest start: Adafruit's ADS1115 guide — a 16-bit I2C ADC that replaces the entire discrete front end if the hobbyist accepts digital-side sampling.

*Receipt closed 2026-09-16 · F3 complete · trust bytes: every artifact listed above was re-verified on disk before close.*

## Fetched table + totals

*(filled at close)*

## Best doc for the cube's differential front end

*(filled at close)*
