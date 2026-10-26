# SELF-STEAL — the light maze through the spectral lens (2026-09-06)

**Commission:** the Operator's deep-self-analysis order, lens = two images: the
spectral ladder (RGB: 3 bands → multispectral: N bands → hyperspectral: continuous
spectrum) and a 20-formula ray-optics sheet (reflection, mirror formula, Snell,
critical angle, TIR, lateral inversion). "Deep self analysis of our light maze via
this lens and its implications — we need to make the next iteration incorporating."

## 1. Where the maze honestly sits on the ladder

| Layer | What it computes | Band axis | Coherence | Wall interaction |
|---|---|---|---|---|
| maze_arena flood | BFS/eikonal distance | **none — one scalar** | incoherent | absorb only |
| B1 odd field | + handed curl term | none | incoherent | absorb |
| B2 eraser maze | complex amplitudes, fringes | **one k** (slider) | **coherent** | absorb + measurement |
| shadow_walk | fog/SEEN | none | — | vision contract |

**The honest audit: we are band-zero.** Not RGB — one scalar with wave decoration on
one surface. The eraser maze took the biggest single step (coherence — phase is what
makes "spectrum" meaningful at all), but we have no band axis, no dispersion, and
walls that only absorb. We named it a light maze a month before it earned the word.

## 2. The deep find: refraction is already in the solver, asleep in a constant

The eikonal equation **is** the mathematics of refraction. Light bending across a
media boundary is Fermat's principle — least time — and our flood solves least-time
with a per-cell cost `c(n,cell)` that we have held **constant everywhere since day
one**. Vary that constant by region and n = 1/c: **Snell's law (sheet #19) emerges
from the flood with zero new optics code.** We spent the day importing physics
through six doors; the oldest law was already in the walls, waiting for us to stop
holding one number constant. Water corridors, prisms, gradients — all price changes.

## 3. The formula→mechanic map (each sheet row becomes a rule)

| Sheet | Formula | Mechanic it buys |
|---|---|---|
| #1 | i = r | specular mirror walls — bounce flood into unseen corridors |
| #19 | n₁sin i = n₂sin r | refraction zones (free, via cost field); prisms when n varies per band |
| #18/#20 | sin C = n₂/n₁, TIR | **waveguide walls**: light enters a guide and stays in it, leaking only at bends sharper than critical — routing without walls |
| #4–#7 | mirror formula, f = R/2 | concave mirror = focusing element: light must CONVERGE on a sensor — the maze grows optical elements, not just walls |
| #5 | m = h_i/h_o | focusing keys: how tight the convergent patch is |
| #16 | v = u, plane mirror | cheap: mirrored corridors show flipped light |
| #17 | lateral inversion | mirrored corridors read as a flipped maze — the room shows you yourself reversed |
| ladder | 3 → N → continuous | v3a: K=3 bands · v3b: K bands + dispersion · v3c: continuous render — the hyperspectral cube is \|A(cell,k)\|² sampled |

## 4. The spectral axis composes with everything shipped today

- **Dispersion separates critical angles** (n per band → different C): a single
  waveguide wall demultiplexes bands — red goes left, blue stays in the guide.
  Prism + TIR = the band-routing puzzle grammar.
- **Measurement goes per-band**: the eraser's SEEN-collapse in band 1 kills band 1's
  fringes while band 2 stays coherent — quantum-eraser demultiplexing. "You cannot
  look at the red without killing the red; the blue never noticed."
- **B1's odd field is a per-band knob**: chirality η can differ per band — the swirl
  itself becomes spectral (optical activity — rotation of polarization, the honest
  next axis after spectrum).
- **B5's ledger already hash-chains frames** — spectral frames chain the same way.

## 5. Implications beyond the game (one paragraph, not overclaimed)

The ladder is the fleet's own shape: tri-state is RGB (three verdict bands), the
grounding wave is multispectral (N claims), and the verkle chain is the
hyperspectral ideal — the continuous record every band aspires to. Tesuji's probes
are monochrome stones; spectral probes (same stone, every k) are the richer field
map. The maze and the fleet keep being the same ladder at different altitudes.

## 6. LAUNCHED — B7: the spectral maze (same turn, background)

New surface `dashboard/static/spectral_maze.html` (no clobber — owns its file):
K=3 bands as real wavelengths (k_R < k_G < k_B), per-band k, dispersion table;
refractive zones via cost = 1/n per band (Snell emerges — and is CHECKED);
specular mirror walls; TIR waveguide walls with band-dependent critical angle;
filter mechanic; band-sensors as win condition; eraser collapse per band optional.
Falsifiers: (1) monochrome regression — single band, flat n ⇒ bit-identical to the
current flood; (2) Snell check — measured bend at a flat boundary matches
n₁sin i = n₂sin r within grid tolerance; (3) TIR — leak ≈ 0 below critical bend,
sharp leak above, per band; (4) mirror law — reflected flood symmetric about the
normal; (5) perf — K=3 within 3× current field cost, 60fps bar; (6) per-band
visibility strip live. Receipt: watch/PURPLE_HARVEST_B7_SPECTRAL_MAZE_20260906.md.

*The tape: we spent a day importing physics through six doors — and the oldest
formula was already in the walls, asleep in one constant we never thought to vary.
Fermat was here first. He just needed the price to change.*

---

## ADDENDUM — the vector-calculus sheet (Operator lens #2, same day)

The Operator followed with the back cover of the electromagnetism book: gradient,
divergence, curl, Laplacian — in Cartesian, spherical, cylindrical coordinates.
Three findings, one new door:

**1. Our code is on the sheet already, under assumed names.** B1's odd field IS a
discrete curl — the η-term is the 90°-rotated gradient, (∇×v)-shaped, per the
Cartesian row. The GPS walkers descend an explicit gradient. The flood's
relaxation relaxes a Laplacian. We have been doing vector calculus all day
without opening the vocabulary. The sheet names the operators; the operators were
already employed.

**2. Curvilinear coordinates are an implicit lens.** On a polar/spherical grid
the metric factors (1/r², r²sinθ, 1/s) compress cells toward the axis and poles —
and a flood propagating through compressed cells CONCENTRATES, exactly as if a
lens were present. **Light bends from geometry alone, no media required** — the
gravitational-lensing mechanic: a "heavy" region of the maze (finer cells, denser
walls) deflects the flood because the coordinates are heavy there. GR's one-line
lesson, playable: matter tells the grid how to curve; the flood follows the grid.

**3. The operator set is the maze physics module's formal vocabulary** — ∇ for
walkers, ∇² for diffusion/lightmap smoothing, ∇× for chirality, ∂/∂t(ρv) for the
dirty-radius refill's conservation law. Worth keeping as the module's naming
layer when the physics consolidates.

**DOOR CURVILINEAR (B8 candidate, queued behind B7):** a polar-grid tower maze
where curvature itself is the optical element — lens-regions made of coordinate
compression, a spherical floor using Girard's excess for cell areas (Triage: the
mathemetica post), gravitational-lens puzzles: place "mass," the flood bends.
Falsifiers: metric-factor regression (flat limit ≡ Cartesian), lens deflection
vs the thin-lens prediction, pole concentration profile vs 1/r². Fires after B7
lands and is verified — one maze build in flight at a time.
