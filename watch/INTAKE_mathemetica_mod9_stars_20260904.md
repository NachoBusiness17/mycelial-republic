# INTAKE — mathemetica / mod-9 digit-star circles, Fibonacci 2&7 schedule (2026-09-04)

NAME — @mathemetica: doubling each digit of 123456789 mod 9 gives 246813579; on a
circle the x↦2x map is one 6-cycle through the units + a 2-cycle through multiples
of 3; companion map x↦7x (7≡2⁴ mod 9) gives 753186429 in two 3-cycles — every star
is an iterate of one generator of (Z/9Z)*; Fibonacci visits the same diagrams on a
rigid schedule (Fₙ even ⇔ 3|n; 7|Fₙ ⇔ 8|n).
Source: x.com/mathemetica/status/2096115343890731244 (2026-09-05 05:56Z, 32 likes,
image receipt: "Fibonacci 2&7 Multiples", 8x8 grid of mod-9 multiplication circles,
rows k∈{5,1,6,2,7,3,8,4} = +5 steps, right labels = k·(1..9) digit strings).

SCORE — F:2 P:1 C:5 W:1 N:2 = 11/25 CALIBRATE
- FIT 2: no organ runs digit-circles today, but a free-lane generator bolts on the
  same way mag/lattice_distance.py did (matplotlib/PIL, ~60 lines); salon viz-adjacent.
- PULL 1: claims are CLOSED by hand below — nothing left for the falsifier
  workbench to eat; light/shadow-fields adjacency thin (star polygons ≠ light transport).
- COST 5: hand-verified, $0; any build is free-lane pennies.
- WINDOW 1: feeds no starved lane tonight; queue-restock candidate only.
- NOVELTY 2: new tweet in watch/ (no prior mod-9/times-table card) but classic
  Mathologer-era modular-times-table material.

VERDICT — REMEMBER (file the law), score lands CALIBRATE band.
Tri-state:
- SUPPORTED (hand-verified, digital-root convention 0≡9): 2x map 123456789→246813579;
  strict mod-9 {0..8} would write the last digit 0 — convention nitpick, not an error.
- SUPPORTED: units of (Z/9Z)* = C6, 2 generates; doubling cycle (1 2 4 8 7 5);
  (3 6) 2-cycle with 9 fixed (tweet's "2-cycle through the multiples of 3" is loose —
  9 is a fixed point, not in the cycle).
- SUPPORTED: 7≡2⁴ (16 mod 9); x↦7x = 4th iterate of doubling → 753186429, two
  3-cycles (1 7 4)(2 5 8), multiples of 3 all fixed. Image row labels
  (369369369/483726159/516273849/639639639/876543219) all recompute correctly.
- SUPPORTED: Fₙ even ⇔ 3|n (rank of apparition of 2 is 3); 7|Fₙ ⇔ 8|n (F₈=21,
  no earlier Fₖ divisible by 7; rank divides every multiple).
- UNPROVEN (scope note): "Fibonacci numbers visit the same diagrams on a rigid
  schedule" — column mapping in the image is asserted, not derived in-tweet;
  consistent with F₃,F₆,F₉,... and F₈,F₁₆,... columns but we did not decode all 8 columns.

DOGFOOD — Test 1: no fleet invariant touched; pure closed math. Test 4: places as
shelf/reference opcode, not a build opcode. Tests 2/3/5 skipped: low stakes, math
closed by hand. Optional hook, NOT a wire: if the operator ever wants a salon viz
B-item, a mod-9 star-circle generator is a one-hour free-lane build.

FILED — watch/INTAKE_mathemetica_mod9_stars_20260904.md + room.jsonl thread
"intake". No driver wire (not BUILD NOW). Third mathemetica paste: all three
landed REMEMBER/CALIBRATE — pattern noted, keep scoring honestly.
