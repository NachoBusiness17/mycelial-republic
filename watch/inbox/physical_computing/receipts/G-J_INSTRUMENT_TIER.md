# G-J: Instrumentation tier — receipt (wave-lane)

- **Gap:** G-J — instrumentation tier decisions for the cube program (ADC tier, Cyton-vs-ADS1115 crossover, shielding).
- **Opened:** 2026-09-16 · agent wave lane · no git, no paid APIs (WebSearch/WebFetch only)
- **Sources budget:** free web only; every load-bearing number gets a URL in this receipt.

## Appended log (chronological)

- [16:5x] Receipt opened. Context load next: `C17_CUBE_INSTRUMENT_PLAN.md` + `CUBE1_SHOPPING_LIST.md` (stage-0 BOM to correct).
- [x] GATHER round 1 attempt 1: 4× WebSearch ALL TIMED OUT at 60s (same degradation C17
  hit). Mitigation per C17 precedent: WebFetch against known free URLs (docs/shop/europepmc),
  space out WebSearch retries.
- [x] GATHER round 2 (WebFetch, live bytes):
  - **OpenBCI pricing repriced UP since the $530 era [V]:** Cyton 8ch = **$1,249**; Cyton+Daisy
    16ch = **$2,499** (shop.openbci.com product pages, fetched 2026-09-16). Specs [V]: ADS1299
    24-bit, 250 Hz/ch (125 Hz/ch with Daisy), gain 1–24, SNR 121 dB, input range ±2.5 V,
    battery-only 3–6 V DC.
  - **FEMS citation resolved [V]:** Buffi et al. 2025, FEMS Microbiol Rev, 10.1093/femsre/fuaf009
    (PMC11995700). Fungal AP-like firing 0.5–5 Hz with amplitudes **5–50 mV** (Olsson & Hansson
    1995, Armillaria/Pleurotus); own recordings +50 to −300 mV. **The review explicitly says a
    Faraday cage "is essential"** — contamination sources observed: incubator door opening,
    automatic window shades. NOTE: the exact "0.0003–0.1 Hz" band is NOT verbatim in this review —
    the slow-rhythm figure it notes is a ~0.005 Hz cyclic signal; treat the band claim as
    canon-consistent (millihertz rhythms) but not byte-quoted.
  - **Adamatzky 2022 RSOS "Language of fungi" (PMC8984380) [V] — the canonical rig:** Pico
    ADC-24 **24-bit** logger, acquisition range **±78 mV** (LSB ≈ 4.6 µV), **1 sample/s stored**
    (internal ~600/s averaged), iridium-coated stainless needle pairs 1–2 cm, **twisted-pair,
    differential, galvanic isolation**. Spike amplitudes **0.03–2.1 mV** (species avgs 0.007–2.1),
    spike durations minutes-to-hours (one burst avg 64 min), inter-spike 41–116 min.
  - **ADS1115 TI product page [V]:** 16-bit, 8–860 SPS, PGA FSR ±0.256 V–±6.144 V (so
    **7.8 µV/LSB at ±0.256 V**), 4 single-ended / 2 differential muxed channels, 4 I²C addresses.
    Noise µVrms table not on product page — datasheet fetch pending.
  - **ADS1220 TI product page [V]:** 24-bit (20-bit effective), 2 kSPS, PGA 1–128, 4 inputs
    (2 differential), 50/60 Hz rejection at 20 SPS. Noise figure pending datasheet.
  - **ADS1299 (the Cyton front end) TI product page [V]:** 24-bit ×8 simultaneous, 250 SPS–16 kSPS,
    input-referred noise **1 µVpp (70 Hz BW)**, built-in bias-drive amplifier, lead-off (impedance)
    detection, SRB pins for referential montage, CMRR −110 dB, input bias 300 pA.
  - WebSearch retries (2×) still timing out — staying on WebFetch.
- [x] GATHER round 3 (web_reader on TI PDF datasheets — WebFetch rejects application/pdf):
  - **ADS1115 datasheet Table 7-1 [V] (SBAS926K, FSR ±0.256 V): input-referred noise is
    7.81 µV RMS at EVERY data rate** — 8 SPS: 7.81 µVpp (noise-free res 16 bits) → 860 SPS:
    35.83 µVpp (13.8 bits noise-free). RMS noise = exactly 1 LSB at all rates: the part is
    LSB-limited, not sampling-limited. 860 SPS buys zero RMS improvement; it only triples pp
    noise. 8–16 SPS is the correct setting for this band. CMRR 105 dB typ DC [V].
  - **ADS1220 datasheet Table 7-1 [V] (SBAS501D, rev 2026):** 20 SPS × gain 128
    (FSR ±16 mV): **0.09 µV RMS (0.41 µVpp)**, 16.3 bits noise-free; gain 32 (±64 mV,
    the Adamatzky range): 0.23 µV RMS; gain 8 (±256 mV): 0.80 µV RMS. Simultaneous 50/60 Hz
    rejection at 20 SPS, NMRR 105 dB [V]. → the right 24-bit analog board class (ADS1220;
    ADS1256 overkill at 30 kSPS). **HX711 rejected [F]:** load-cell-only front end — fixed
    ×32/×128 gains into ±40 mV bridge stage, 10/80 SPS only, no line-rejection config.
  - WebSearch retired for this session (4/6 attempts timed out); Backyard Brains hobby-cage
    page located in their experiment index but fetch timed out — cage spec below is
    engineering synthesis grounded in the [V] FEMS/Adamatzky requirements, not a copy of a
    hobby build.

---

## FINAL REPORT — G-J instrument tier (receipt closure 2026-09-16)

### Answer 1 — ADC tier: is 16-bit @ 860 SPS overkill?

**860 SPS: yes, 100× overkill — and free to keep. 16-bit: adequate for cube 1, NOT the
limiting factor. The limit is the electrodes + the room, not the ADC.**
- The band is sub-Hz: canon spiking is inter-spike 41–116 min with spike durations of
  minutes–hours (Adamatzky 2022 [V]); AP-like firing 0.5–5 Hz at the fast end (Olsson &
  Hansson via Buffi 2025 [V]). 8–20 SPS sampling with 1 Hz logged averages fully covers
  it — the canonical lab logs exactly 1 sample/s [V]. At 860 SPS the ADS1115's RMS noise
  is unchanged (7.81 µV) — nothing gained, only pp noise tripled. Run it at 8–16 SPS:
  same cost, 16-bit noise-free resolution, sinc-filter line rejection.
- Signal scale vs floors: Pleurotus-class spikes are 5–50 mV (640–6400 LSB of the
  ADS1115 @ ±0.256 V) — 16-bit has 3 orders of margin. The smallest published species
  average is ~30 µV (S. commune; O. nidiformis ~7 µV) — 1–4 LSB at ±0.256 V: resolvable
  but marginal. **A 24-bit part is a measured upgrade, not a stage-0 purchase**: ADS1220
  @ g32/g128 floors at 0.23/0.09 µV RMS [V] — 30–90× below the ADS1115 — but only helps
  if electrode noise is already that low.
- What actually limits us: electrode half-cell noise + drift, mains common-mode pickup,
  environmental artifacts. The FEMS review's own recordings were contaminated by an
  incubator door and automatic window shades, and concludes a Faraday cage "is
  essential" [V]. Adamatzky's rig spends its engineering on galvanic isolation +
  twisted-pair differential electrodes, not raw bit depth [V]. C17's S0.1 gate (<1 mV RMS
  dead-substrate) is 100× above any ADC floor here — correct gate, correctly aimed.

### Answer 2 — Cyton+Daisy vs N×ADS1115: the crossover

**Pricing reality check [V, fetched 2026-09-16]: Cyton 8ch = $1,249; Cyton+Daisy 16ch =
$2,499.** The ~$530 era assumed by the gap statement is dead — OpenBCI repriced. The
crossover question inverts: at 2026 prices **Cyton never wins on price at any channel
count a hobby cube program can fund** (16ch via ADS1115+TCA9548A ≈ $100–200; even 64ch
≈ $400–500 < one Cyton). At the historical $530 the crossover would have been ~16ch.
- What neuroscience-mode features buy for fungal signals: **bias drive** (active
  common-mode cancellation) matters for dry/high-impedance electrodes on a subject —
  gelled Ag/AgCl on substrate with 1 MΩ bias resistors already controls common-mode;
  **SRB2** shared reference is montage economics for many electrodes (halves electrode
  count per channel) — relevant only to the 16ch future; **1 µVpp input noise** [V,
  ADS1299] matters only when electrodes+room are quieter than ~10 µV; **simultaneous
  250 Hz/ch** is meaningless for minute-long spikes logged at 1 Hz (ADS1115 mux skew at
  8–16 SPS is milliseconds); **impedance check** is replaceable by a DMM + DC-offset
  monitor. Battery-only power is the one Cyton principle worth copying — we already
  mandate it.
- **The 16ch future** = N×ADS1115 (4 boards/I²C bus, TCA9548A mux beyond; ESP32 has 2
  I²C buses → 16 diff channels without extra parts) OR bare ADS1299 modules (~$60–120
  [F]) if stage-1 ever proves µV-scale simultaneous sampling is needed. OpenBCI is
  priced out of the hobby tier, not out of the science.

### Answer 3 — what a working hobby Faraday cage for this band actually is

**A closed conductive box + battery power + clean leads. The cage is the cheapest,
highest-leverage defense; the leads are where the war is actually won.**
- Physics: at 50/60 Hz the aperture rule (openings < λ/10) is satisfied by anything —
  λ ≈ 5,000 km. The box only needs continuity and closure around cube + first 10–20 cm
  of cable. Foil works; mesh works; a metal filing cabinet works.
- **Battery, not mains** [V-adjacent]: Cyton itself mandates 3–6 V battery-only — same
  principle. Battery power eliminates ground loops and mains injection entirely; the
  cage then ties to **circuit ground (battery −) at ONE point**. Grounding the cage to
  mains earth is for static boxes; the moment any mains-powered gear (laptop charger,
  PSU brick) touches the rig, that bond becomes a loop antenna. Rule: rig + logger all
  on battery (USB power bank for ESP32; laptop on battery or via USB isolator).
- Environmental realism [V]: Buffi's contamination incidents (incubator door, window
  shades) show the band's killers are mundane — the cage plus lead discipline (twisted
  pairs, shield grounded at the ADC end only, short runs, > 0.5 m from routers/bricks)
  addresses them.

### TIER DECISION TABLE (the deliverable)

| Tier | Rig | Cost (2026 street) | Verdict |
|---|---|---|---|
| **Cube 1** (2–4 diff ch, stage 0+1+2) | ESP32 + 2× ADS1115 @ **8–16 SPS** (log 1 Hz avg) + Ag/AgCl pads + foil cage + battery | ≈ $34 electronics / ≈ $66 with defenses | **STAY.** 16-bit @ 8–16 SPS has ≥3 orders of margin on Pleurotus-class mV spikes; 860 SPS is overkill (free to disable). No 24-bit purchase. |
| **Cube 2** (4–8 diff ch, stimulus+resp) | + 1–2× ADS1115 more (4 boards max/I²C bus) or 1× **ADS1220** if the upgrade trigger fires | +$6–12/board; ADS1220 ~$6–10 | **CONDITIONAL UPGRADE (registered trigger):** dead-substrate RMS < ~30 µV AND observed live spikes < 30 µV → swap in ADS1220 @ g32 (0.23 µV RMS). Otherwise stay 16-bit. |
| **16ch future** | N×ADS1115 + TCA9548A (≤16 diff) or bare ADS1299 module if µV-scale simultaneous proven needed | ≈ $100–200 / ≈ $60–120 [F] | **Cyton+Daisy ($2,499 [V]) rejected on price — $530 era is dead.** Revisit only with stage-1 evidence that channel count or noise floor demands it. |

### SHIELDING SPEC (stage-0 required, promoted from rider)

1. Foil-lined opaque tub (the cube's own container class): foil on walls + lid, ≥5 cm
   folded overlaps, seams taped; verify continuity with DMM (< a few Ω any-point-to-any-point).
2. Single ground bond: one alligator clip, foil → ESP32 GND (battery −). No other ground
   path exists anywhere in the rig. Battery power ONLY (USB power bank; laptop on battery
   or USB-isolated).
3. Electrode leads: twisted pair per channel inside the cage, shield/sleeve grounded at
   the ADC end only; runs < 50 cm; cage > 0.5 m from routers, PSU bricks, monitors.
4. LED stimulus lives INSIDE the cage (light passes; its wiring is twisted).
5. Stage-0 gate S0.1 unchanged (< 1 mV RMS) — it is the honest arbiter of whether the
   cage + leads did their job.

### CORRECTED STAGE-0 BOM (defends the ~$50 claim; supersedes C17 BOM §"BOM — cube01" rows 1–3 + rider)

| # | Item | Change vs C17 | ~$ |
|---|---|---|---|
| 1 | ESP32-WROOM dev board ×1 | unchanged | 9 |
| 2 | ADS1115 ×2 — **run at 8–16 SPS (was "860 SPS-class"; same part, firmware setting)**; note ×2 boards = **4** diff channels, not 2 (C17 undercounted); 4 addresses/I²C bus = 8 diff scale-out path | spec fix, $ same | 12 |
| 3 | Ag/AgCl ECG electrodes 50-pk + snap leads | unchanged | 13 |
| 4 | **Foil Faraday cage kit (foil, tape, clips, continuity-verified) — PROMOTED rider defense, now required** (FEMS [V]: cage "essential") | was optional rider | 12 |
| 5 | DIY chloridized Ag wire pair (bleach method) | rider → required | 6 |
| 6 | Cal resistor + jumpers + LED (mostly drawer stock) | unchanged | 8 |
| 7 | SHT31 temp/RH | stage-0 stretch (concert made it stage-1 required) | +6 |
| | **TOTAL stage 0 with defenses** | | **≈ $60–66** (floor without defenses $34 — C17's "$31" was an arithmetic slip: 9+12+13=34) |

Defenses carried forward unchanged: dead twin as primary control, EVIDENCE_DEAD row law,
registered thresholds — this receipt changes ONLY the instrument tier, sampling mode,
shielding status, and channel-count arithmetic.

### Sources (all free-tier, fetched 2026-09-16)

[V] = byte-verified this session · [F] = flagged, canon-consistent, not byte-verified.
1. TI ADS1115 datasheet SBAS926K (noise Table 7-1): ti.com/lit/ds/symlink/ads1115.pdf
2. TI ADS1220 datasheet SBAS501D rev 2026 (Tables 7-1/7-2, NMRR): ti.com/lit/ds/symlink/ads1220.pdf
3. TI ADS1115 / ADS1220 / ADS1299 product pages: ti.com/product/{ADS1115,ADS1220,ADS1299}
4. OpenBCI shop: Cyton $1,249 (shop.openbci.com/products/cyton-biosensing-board-8-channel);
   Cyton+Daisy $2,499 (…/cyton-daisy-biosensing-boards-16-channel); docs.openbci.com/Cyton/CytonSpecs/
5. Buffi et al. 2025, "Electrical signaling in fungi," FEMS Microbiol Rev, 10.1093/femsre/fuaf009
   (PMC11995700) — amplitudes 5–50 mV / +50 to −300 mV; cage "essential"; door/shade artifacts.
6. Adamatzky 2022, "Language of fungi derived from their electrical spiking activity,"
   R Soc Open Sci, 10.1098/rsos.211926 (PMC8984380) — Pico ADC-24 24-bit ±78 mV, 1 sample/s,
   twisted-pair iridium-coated needles, spikes 0.03–2.1 mV, ISI 41–116 min.
[F] HX711 limits; ADS1299 clone-module prices; historical OpenBCI ~$530 pricing; the verbatim
"0.0003–0.1 Hz" band string (consistent with canon millihertz rhythms but not found verbatim
in Buffi 2025 — treat as folklore-adjacent until someone pulls the original source).

**Status: FILED 2026-09-16.** WebSearch degradation (6 attempts, 5 timeouts) worked around
via WebFetch + web_reader per C17 precedent. Nothing purchased; stage-0 spend still gated on
operator word. No git.
- [ ] Final: tier decision table (cube 1 / cube 2 / 16ch future) + shielding spec + corrected stage-0 BOM.
