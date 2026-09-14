# THE PHYSICS OF THE MAP — a plain-language companion (SHADOW WORK, companion volume)
**2026-09-06 · for the operator: "i need to understand the underlying physics and how it already maps to the best interpretations of ideas matching their adjacent shapes"**

## 0. What the thing actually IS (no metaphor yet)
A model is a function. Its "space" is the vector space its internal representations live in —
for a 3B model, ~2,000–4,000 dimensions; for 5.3-flash, more. Everything the model knows is,
as far as the interpretability literature can measure, a DIRECTION in that space (the linear
representation hypothesis) plus circuits: weighted connections between directions. Nobody can
see 4,000 dimensions. Every map of model-space is a PROJECTION, and every projection is a lie
about something — PCA lies about neighborhoods, t-SNE/UMAP lie about global shape, our slab
features lie about meaning. **Cartography is the craft of choosing which lie.** That is
LAW-061 (validate-the-field) wearing a physics coat.

## 1. THE DICTIONARY — our construct → its adjacent shape → who named it
| We built | Its adjacent shape | The name in the literature |
|---|---|---|
| BFS flood / cheese-lightmap | wavefront propagation solving the eikonal equation \|∇T\|=1 | Huygens' principle; Fast Marching Method; **Houdini's water = this exact PDE** |
| GPS walkers descending the field | rays following least-time paths through a medium | **Fermat's principle** — the walkers are photons; the field is a refractive index |
| d(θ) shadow strip | the visibility function of radiative transfer; shadow/horizon mapping | standard computer graphics + atmospheric physics |
| Lensing / gaze bending toward dense regions | gravitational lensing — mass bends geodesics, deflection ∝ mass/impact-parameter | general relativity's weak-lens limit |
| "Shadow work to see models as structures" | reading intermediate layers through the output projection | **the logit lens / tuned lens** (interpretability lit uses the SAME optics words) |
| Mirror tricks (run twice, swap the inside, watch what changes) | **activation patching / causal tracing**; knowledge editing by rank-one updates | ROME; Anthropic's circuits agenda |
| Walls/gates = feature directions packed tight | **superposition** — many features as near-orthogonal directions (Johnson–Lindenstrauss) | Anthropic, Toy Models of Superposition |
| A2 refusal shadow cells | **refusal is literally a direction** in activation space — measurable, ablatable | Arditi et al., refusal-direction work |
| TESUJI lit cells from probes | sparse probing: which directions answer which questions | probing-classifier literature |
| DOF: blur = distance from attention focus | thin-lens optics: circle of confusion ∝ aperture·\|d−f\|/d | camera optics — but OUR f (focus) = the attention target, so blur = attention falloff |
| 50 writers, zero locks, chain absorbed | append-only event log / CRDT-flavored honesty: render the stream, never "current state" | event sourcing; the anti-serialization rule |

**The punchline of the dictionary:** the interpretability field already speaks optics — they
named it the LOGIT LENS, they call their best technique PATCHING, their agenda is literally
called CIRCUITS. We didn't stretch a metaphor tonight; we re-derived their vocabulary from the
arena side. Two independent cultures wavefront-solving their way to the same shapes.

## 2. The physics, plain
- **Flood = light in a medium.** Solving |∇T|=1 gives travel-time from the cheese; the walkers
  walk downhill on T — Fermat's least-time path. Change the medium's speed (walls), the paths
  bend. That is ALL refraction is. Our maze is a desktop of Fermat optics.
- **Attention is mass.** In weak lensing, you never see the mass — you see light bend near it.
  Our gaze field bending toward hit-dense organs is the same contract: we never render "importance"
  directly (unmeasurable), we render its deflection of things we DO measure (where attention spent).
- **DOF is honest only if focus is measured.** A camera blurs what's off the focal plane. Our
  focal plane = the attention target from the trajectory hash chain. Then blur encodes a real
  quantity: how far a region is from what the fleet is currently looking at. Fake focus = fake
  DOF = LAW-061 violation.
- **Why norms rising with depth matters** (walker 50's 3.97x): the residual stream ACCUMULATES —
  each layer adds to a running vector, and its magnitude grows like interest. The logit-lens
  literature reads those intermediate states as the model's evolving guess. Our geometric fit
  (r=0.739) is the first depth-axis of the volume we've held; in the walker, that axis is where
  "when does the model decide" lives.

## 3. The builds (fired same-turn)
1. **`notebooks/shadow_work_physics.ipynb`** — the lab bench (numpy/scipy/sklearn only, no new
   installs; matplotlib optional GO): eikonal wavefront solve on the maze grid, PCA/TSNE
   projection of the 9,305-part behavioral volume, layer-gradient fit vs the logit-lens
   literature, DOF/lensing math with real slab data. Also runs headless as a script.
2. **`dashboard/static/shadow_walk.html`** — the field instrument: self-contained canvas-3D
   walker over the behavioral volume + weights volume — WASD + mouse-look camera, per-point
   DOF falloff (focus = attention), gaze-lensing deflection toward doctrine-dense regions,
   SHADOW cells rendered as true occlusion. three.js vendored upgrade is a one-fetch GO later;
   v1 proves the traversal with zero deps.

## 4. The falsifier that keeps it honest
The VISION-GROUND test scales up: my visual read of a render must predict the computed stats
(≥70%). Every projection carries a stamp of WHICH lie it tells (what it preserves, what it
distorts). A render without its distortion-label is prose, not cartography.
