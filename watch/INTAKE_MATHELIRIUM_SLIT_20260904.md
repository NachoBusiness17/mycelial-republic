# INTAKE — MATHELIRIUM SUB-WAVELENGTH SLIT CARD (2026-09-04 window) — the wave rendered again, still nobody's marble

Genome: docs/ref/verb_genomes/research_socratic.md (six steps) on L0 v1. Seat: zcode, intake lane.

## ITEM
https://x.com/mathelirium/status/2095532563481702870?s=20 — THIRD @mathelirium post
of the window (Smith-Purcell CALIBRATE 9/25, watch/INTAKE_SMITH_PURCELL_20260904.md;
double-well BUILD WINDOWED 14/25, watch/INTAKE_HAMILTON_DOUBLEWELL_20260904.md; same
discriminator each time). 30-second video, posted 3:21 PM Sep 3 2026. Engagement as
rendered: 21.7K views / 14 replies / 63 reposts / 541 likes / 144 bookmarks.
Verbatim text: "A sub-wavelength slit in a dispersive metal turns an incoming
electromagnetic pulse into a strongly structured transmitted field."

## RECEIPTS (what was fetched)
- **webReader on x.com — Supported**: og metadata + root text verbatim, 30s video,
  counts. Whole-conversation step RAN, not skipped.
- **Replies — 3 captured, one technical, none load-bearing** (operator law: replies
  are signal): Drew Ponder (@drew_ponder) quote-style hype expansion, tagged
  "Made with AI", text truncated by the wall; Raymond Bednarz Jr. (@RandyZarz73)
  speculation ("You could encrypt data with this model especially if it could be
  replicated holographically imo") — no opcode; Okular AB (@okularab) asks the one
  technical question, "What are the whitish grains that we see in the simulation?" —
  answerable only from video frames I don't have: **Unproven** (thumbnail shows only
  stylistic volumetric wisps). Full reply set + community notes: **Unproven** (login
  wall — same wall as the two prior cards).
- **Video thumbnail — Supported, and it changes the read**: frame pulled
  (pbs.twimg.com media/HRTrVIca8AAq-fo, 1200x675) and read directly. Title card
  "A TINY SLIT RESHAPES LIGHT"; left half: blue Gaussian-envelope pulse on an axis,
  approaching a dark metal slab with a narrow gap; a bright spark at the slit; right
  half: concentric circular wavefront rings fanning from the slit point. **Zero math
  labels** — no equation, no scales, no readouts, no signed frame (contrast the
  double-well, whose on-frame H(q,p) WAS the spec). The frame is a glow
  illustration, not a map.
- **MEASURE RAN, $0 (this card's falsifier, not a described one)**: 2D TM Yee FDTD
  with ADE Drude metal (eps(w0) = -1.25, wp = 1.5*w0, gamma = 0.05*w0), 400x200 grid,
  6-cell slit = lambda/5, plane-wave pulse, sponge absorber, 1600 steps, 9.2s runtime:
  transmitted monitor energy **Drude 38.32 vs identical-geometry PEC control 0.0051
  — ratio 7.45e3**. PEC near-zero receipts Bethe's (d/lambda)^4 suppression
  ((0.2)^4 = 1.6e-3 class); Drude case shows the structured transmitted field
  (cylindrical wavefronts fanning from the slit in the saved snapshot). Artifacts:
  memory/runs/intake_slit_fdtd_20260904/ (falsifier_slit_fdtd.py, field_drude.png,
  field_pec.png, result.json).
- **Corpus sweep — Supported, corpus-absent as item**: zero real hits for plasmon /
  sub-wavelength / slit-optics / FDTD / Yee / Bethe across watch/ + docs/ + memory/
  (grep hits are false positives: meditations.txt, system-prompt leaks, z.ai docs
  mirror). @mathelirium greps resolve to exactly the two prior cards + room.jsonl.
  MEMORY.md index read (205/256 lines, remainder tail-known from the two prior
  sweeps this window). Nearest neighbors are pattern-level only: the standing-wave
  law ("does the wave oscillate?", vram_hologram) and the Smith-Purcell card's
  parked someday-docket cell.

## SCORE — F:2 P:1 C:3 W:1 N:1 = 8/25 → **CALIBRATE band (floor)**

- **FIT 2** — transform we compute: yes, now MEASURED, not asserted ($0 FDTD
  reference, 9.2s). Consumer owed on our board right now: none. The arena consumes
  static FIELD.json operator cells (gradient/div/curl/laplacian, smith constant-r/x
  circles) and a marble integrator; the Room consumes geometric lightmaps; B1
  consumes kaliset/erosion/marble. Nothing on the board is owed a time-domain
  wave-optics FDTD mode. The discriminator's second conjunct fails exactly as it
  did for Smith-Purcell.
- **PULL 1** — advances no live arc (shadow-fields B1/B2, QLoRA spine, legions,
  economist, tale-re-encoder, flight recorder). The shadow-fields rhyme ("slit =
  writing on the film", an aperture IS an occluder) is repetition-as-emphasis: the
  Room's occluders already exist geometrically, and a wave-optical re-derivation
  fills no starved organ.
- **COST 3** — filing pennies; the reference falsifier is measured-cheap ($0, 9.2s,
  numpy). But the arena-grade product is the heaviest of the three mathelirium
  cards: a GLSL wave mode means ping-pong buffers + ADE-Drude + absorbing
  boundaries (~100+ lines and numerical-stability discipline), an order heavier
  than the double-well's 15-line integrator and strictly more machinery than
  Smith-Purcell's one-line dispersion relation. Consumer-undefined unscoped-design
  cost applies on top.
- **WINDOW 1** — feeds no starved lane; queue discipline gates the whole arena door
  behind field_smith.json v0 (committed, unlanded) + the B1 browser falsifier, same
  as both prior cards. A wave-mode family would enter behind them and behind the
  windowed hamilton_cell.
- **NOVELTY 1** — corpus-absent as an item, textbook in the world: single-slit
  diffraction (Huygens), Bethe 1944 aperture theory, extraordinary optical
  transmission (Ebbesen et al. 1998), surface plasmon polaritons — and a
  slit-in-a-screen FDTD is the canonical first example of every computational EM
  course and FDTD tutorial. The one honest nugget: the caption's load-bearing word
  is "dispersive" — remove it and the claim dies (our PEC control is that
  experiment). The post gets the physics right; it just doesn't show the physics.

## READ
The honest why: this is the Smith-Purcell pattern one domain over and one notch
down — a stranger's rendering of textbook wave physics, corpus-absent but standard,
transform genuinely computable (now receipted by our own $0 falsifier), and no
consumer owed anywhere on the board. It is also the third "the wave rendered"
artifact this window (tuning-fork traveling wave, PhilosophyOfPhy plane wave, now
the pulse-through-slit) — repetition as emphasis of a law we already hold
(det-spine + stoch-flesh), each repetition adding zero spine.

Invariant pass:
1. **Map-presents-the-solved-problem**: FAILS here, and that is this card's
   sharpest result. The frame carries no math, no labels, no steps — a glow
   illustration of Huygens rings you could get from any point source in vacuum.
   The entire physics payload (dispersion -> transmission) lives in the caption.
   The Smith chart and the double-well passed this invariant; this account's third
   offering does not. Illustration, not map.
2. **Det-spine + stoch-flesh**: the wave lineage again — tornado family, standing
   wave doctrine, third external echo this window. Rhymes without adding.
3. **Composable-operator-cells**: a time-domain FDTD mode is NOT a cell in the
   existing static-operator grammar; it is a NEW cell family (wave propagation),
   i.e. the exact someday-docket item the Smith-Purcell card already parked ("IF
   the arena ever grows a wave optics mode family"). This card joins that parked
   docket; it opens nothing new.

Stockfish pass — what opcode consumes it? **None exists.** No time-domain wave
opcode, no EOT consumer, no spectrometry surface, nothing owed. Placement failure
is the finding — and it is the same finding as Smith-Purcell, now measured with a
running falsifier instead of asserted.

## TRI-STATE
- Post exists, text verbatim, 30s video, 21.7K views / 541 likes, Sep 3 2026:
  **Supported** (webReader og fetch; single-source counts).
- Physics claim (sub-wavelength slit in dispersive metal -> structured transmitted
  field; dispersion is load-bearing): **Supported twice over** — canonical
  literature (Bethe 1944, Ebbesen 1998) AND our own $0 falsifier (Drude/PEC ratio
  7.45e3; snapshot shows the structured field).
- Frame is a glow illustration with zero math labels: **Supported** (thumbnail
  downloaded and read directly).
- Video is a strict numerical simulation vs stylized/AI-assisted render:
  **Unproven** (single thumbnail frame seen; photoreal glow style + "Made with AI"
  ecosystem in the reply thread flagged, not settled — trust the caption and the
  physics, not the pixels).
- Replies beyond the 3 captured + community notes + Drew Ponder's full text:
  **Unproven** (login wall, third genre/window).
- Okular AB's "whitish grains": **Unproven** (question is about video content
  unseen; thumbnail shows only stylistic wisps — plausibly rendered field speckle
  or noise texture, guessed, not adjudicated).
- Wireability onto the arena: transform computable **Supported** (falsifier ran);
  owed consumer absent **Supported** (board inventory: no wave-time-domain opcode);
  nothing is proposed, so nothing is Unproven-until-built.

## VERDICT — **CALIBRATE** (8/25, CALIBRATE band floor; one point below
Smith-Purcell's 9 because the map invariant fails outright and novelty is equally
floor, partially offset by the measured-$0 falsifier. The genre wall held under
the series' heaviest probe: the transform conjunct is now PROVEN cheap and it
still doesn't matter, because "owed consumer" is the conjunct that pays rent.
Third consecutive mathelirium confirmation: the score tracks the BOARD's needs,
not the account.)

## ROUTE — no wire
1. No build, no organ_queue row, no driver pull. This card is the record.
2. One-line memory row: "mathelirium sub-wavelength slit: Bethe/EOT wave optics,
   caption-correct, frame unlabeled; $0 Drude-FDTD falsifier ran (Drude/PEC = 7.4e3,
   9.2s); no wave-time-domain consumer owed on any board; joins the parked
   wave-optics someday-docket."
3. Calibration row for the intake lane: tenth math-viz card of the window, third
   from this account; new receipt class = falsifier-run-for-a-CALIBRATE item
   (measures the COST axis instead of guessing it — keep for future cards);
   map-invariant failure (unlabeled frame) as a NEGATIVE discriminator against the
   signed-frame cards.
4. Someday-docket: the parked "wave optics mode family" cell now has a working
   reference implementation (memory/runs/intake_slit_fdtd_20260904/) to inherit if
   that family is ever GO'd — the falsifier script IS the first cell draft. Parked
   behind field_smith.json v0, B1 falsifier, and windowed hamilton_cell, in that
   order.

---
*L0 counters — FORBIDS: building any FDTD/wave-optics arena mode before
field_smith.json v0 (committed, unlanded) and the B1 browser falsifier clear the
queue — same forbid as both prior mathelirium cards, now covering a candidate with
the heaviest build of the three. PAID RENT: the $0 falsifier RAN (claim receipted
from first principles, not asserted — the card's COST axis is measured, not
estimated); thumbnail frame rendered (closes the root-frame crop class);
corpus-absence receipted; third-point series data for the genre wall.*

*THE CROP: video motion unseen (single thumbnail frame — the 30s could show
surface-plasmon bound waves on the slab face that the frame's free-space rings do
not); replies past three + community notes unseen (login wall); render provenance
(numerical sim vs AI-assisted illustration) unresolved; falsifier is 2D scalar TM
with lossless-ish Drude — real EOT physics (3D hole arrays, measured Au
permittivity, SPP dispersion) untested; docs/ref/canon not swept page-by-page.
Next chair: a vision-lane seat with X media access if frame sequence ever matters;
whoever inherits the wave-optics docket starts from the falsifier script, not zero.*
