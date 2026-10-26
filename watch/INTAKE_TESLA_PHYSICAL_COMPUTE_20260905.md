# INTAKE — TESLA PHYSICAL COMPUTE (2026-09-05, card-worker)

Commission: "Steal Nikola Tesla design originals — all historical documents of his work
as interpreted through our systems. Get his help on our physical compute research."
Lens: Lukyanov water integrator (INTAKE_BATCH_POPMATH_20260904b), NNUE accumulator sidecar
(NNUE_SIDECAR_BRIEF_20260904), operator algebra (EMIT/STORE/DISSIPATE/GATE/INTEGRATE/
DIFFERENTIATE/GROUND — fleet_symbols.html).

**Score: 21/25 BUILD.** Primary sources preserved, quotes verified in-file, three concrete
steals named and windowed. Docked 4: Wardenclyffe-as-power-plant stays Unproven (Tesla's
own receipts don't close), and the modern-analog-kernel comparisons below are training-
knowledge, not fetched this window.

## PRESERVATION (operator preservation law) — 9 files, 52MB, corpus/training_materials/tesla/

All rows in corpus/training_materials/MANIFEST.md with sha256. Public domain, primary.

1. my_inventions_wikisource.txt (146KB) — autobiography, Electrical Experimenter 1919.
2. lecture_experiments_alt_currents_1892_gutenberg_13476.txt (251KB) — 1892 IEE lecture.
3. martin_inventions_researches_writings_1894_gutenberg_39272.txt (1MB) — T.C. Martin 1894
   compilation, includes the Franklin Institute 1893 lecture material (the "one lecture
   transcript" ask, plus the rest of the book).
4. colorado_springs_notes_1899_1900_djvu.txt (824KB) — full text, NOLIT 1978 museum edition.
5. colorado_springs_notes_1899_1900_scan.pdf (48MB) — the actual lab notebook scan.
6-9. patent_US613809.pdf, patent_US787412.pdf, patent_US645576.pdf, patent_US1119732.pdf —
   telautomaton, World System, magnifying transmitter, receiver apparatus.

Fetch honesty: first two Gutenberg ID guesses (51673, 13415) were WRONG — Chekhov and a
Finnish novel. Caught by header check (read the row, not the zone: read the file, not the
URL). Correct IDs recovered from the search page. Two wrong IDs, zero polluted files.

## LINEAGE 1 — THE ACCUMULATOR: Tesla's circuits as analog operators

**Supported** (in preserved texts): Tesla's resonant transformer and tuned receiver are the
operator algebra in copper. INTEGRATE = the condenser accumulating charge between disruptive
discharges; DIFFERENTIATE = the coil opposing di/dt, sharpening the spark; the magnifying
transmitter (US645576) is a physical GAIN-of-integration ladder driving a resonant secondary.
Colorado Springs Notes is a measurement log of standing waves on the planetary medium —
he solved a wave PDE in the physical substrate instead of in arithmetic, the same move as
the Lukyanov water integrator (hydraulic head ~ his earth potential; pre-digital analog
computation, same family, Tesla a generation earlier).
Quote, verified in my_inventions_wikisource.txt: "the Earth is responsive to electrical
vibrations of definite pitch just as a tuning fork to certain waves of sound."
**Unproven**: whether his oscillator-era physics transfers to meso-scale compute substrates
without measurement — needs the PNN/iontronic rig before any promotion.

## LINEAGE 2 — THE LIGHT THESIS: Wardenclyffe as one EMIT, many STOREs

**Supported** (patent text verified in the fetched page for US787412A, PDF preserved):
"electrical disturbances may be transmitted through portions of the earth by grounding only
one of the poles of the source" and "it is practicable to transmit intelligible signals or
to control or actuate at will any one or all of such apparatus" — remote apparatus drawing
energy from the field, no generator of their own. That is the light thesis in copper:
broadcast into a medium, dumb receivers STORE what the tuned field carries. One EMIT
(magnifying transmitter), many STOREs (receiver condensers, US1119732), GROUND as the shared
return — literally the operator we named GROUND is Tesla's earth pole.
**Unproven, stated honestly**: Wardenclyffe as a POWER plant (megawatts through the earth)
never closed as a claim — his receipts prove signal + control, not bulk power. Steal the
architecture, not the megawatts.

## LINEAGE 3 — THE TELEAUTOMATION: US613809 and the golem law, in Tesla's own words

**Supported** (quote verified in the US613809A page text and patent PDF): claim 2/3 language:
"establishing a region of waves or disturbances, and actuating by their influence exerted at
a distance the devices on said vessel or vehicle." The boat obeys whatever fills its region —
Tesla's own binding language, verified in my_inventions_wikisource.txt:
- "my boats were controlled thru the joint action of several circuits and interference of
  every kind was excluded" (individualization = tuned lock)
- "Each signal is like an individual of unmistakable identity and there is virtually no limit
  to the number of stations or instruments which can be simultaneously operated"
The operator's golem warning maps exactly: an automaton without its binding operator answers
ANY transmitter in its region. Tesla's tuned-lock IS the GATE — binding by frequency
individualization, not by obedience. His deepest line is about himself: "I was merely an
automaton endowed with power of movement, responding to the stimuli of the sense organs and
thinking and acting accordingly" — he modeled the human first, then built the machine. Fleet
law already had this: the room's walls (files + chain) are our tuning; chat is an untuned
region, anyone can transmit into it.

## PHYSICAL COMPUTE PAYOFF — 3 concrete steals (windowed, per launch law)

**S1 — TESLA_RESONATOR_BANK (windowed: builder spec next quiet window).** A bank of tuned
LC resonators at distinct pitches, driven by a pulse train, state read at taps = a physical
reservoir-computing kernel. Tesla's coupled tuned circuits (US645576 primary/secondary)
are the reservoir; "electrical vibrations of definite pitch" are the feature space. Pairs
with the analog-revival arc: same role as a reservoir computer's recurrent kernel, zero
transistors. Spec: N resonators, Q and pitch as hyperparameters, spark-gap exciter as input
injector. [interpretation: Supported as design reading; performance: Unproven until built]

**S2 — CHARGE-ACCUMULATOR NNUE (windowed: NNUE sidecar brief gets an analog column).**
Tesla's receiver stores field energy in condensers for later use (US1119732 receiver
apparatus). Steal: the NNUE accumulator as charge integration on a capacitor — incremental
updates accumulate in charge, GATE'd by a tuned lock, read as voltage. The 16-bit accumulator
row becomes a physical condenser row. This is the literal NNUE accumulator in copper.
[Supported as mapping; Unproven as benchmark]

**S3 — EARTH-RETURN BROADCAST BUS (windowed: field-surface doctrine note).** "Grounding only
one of the poles of the source" (US787412) = the shared medium as the bus. For physical
compute: treat cross-coupling through a shared substrate (capacitive/inductive crosstalk
between iontronic channels) as a deliberate broadcast channel, tuned and addressed like
Tesla's individualized signals — crosstalk is not noise, it is free fanout. Fleet rhyme: one
EMIT, many STOREs — the shared blackboard/room surfaces already run this topology in software.
[Supported as architecture; Unproven as hardware]

## ROOM RECEIPT

Row appended to watch/room.jsonl (thread intake, seat card-worker, 21/25 BUILD).

## SOURCES (all fetched literal URLs this window)

- https://en.wikisource.org/wiki/My_Inventions
- https://www.gutenberg.org/cache/epub/13476/pg13476.txt
- https://www.gutenberg.org/cache/epub/39272/pg39272.txt
- https://archive.org/download/nikola-tesla-colorado-springs-notes-with-bookmarks/
  Nikola_Tesla_Colorado_Springs_Notes_%20with%20bookmarks_djvu.txt (+ .pdf)
- https://patents.google.com/patent/{US613809A,US787412A,US645576A,US1119732A}/en
- https://patentimages.storage.googleapis.com/.../{US613809,US787412,US645576,US1119732}.pdf
