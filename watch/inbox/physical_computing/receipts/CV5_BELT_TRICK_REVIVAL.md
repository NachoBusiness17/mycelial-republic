# CV5 — Belt-Trick Revival (receipt)

- Date: 2026-09-16
- Lane: wave / shadow-asset revival (operator's own math)
- Mission: revive the belt-trick lattice from prose doctrine (`dashboard/static/lanes/elder.md`) + Three.js scene (`belt_domain.js`, sovereign-mirror-scaffold worktree) into a self-contained WebGL2 estate page at `dashboard/static/vislab/belt_trick.html`. Constants are load-bearing; copy exactly from source.

## Log

- [t0] Receipt opened FIRST per wave-lane law. Beginning source hunt (filesystem search for belt_domain.js — no git commands used).
- [t1] SOURCES FOUND (no git commands; plain filesystem search):
  - `C:\Users\foste\Documents\projects\worktrees\sovereign-mirror-scaffold\src\sovereign_mirror\dashboard\static\platform\scenes\belt_domain.js` (140 lines, Three.js scene; a second copy exists under `.venv/Lib/site-packages/` — the `src/` tree is canonical)
  - `C:\Users\foste\Documents\projects\worktrees\sovereign-mirror-scaffold\src\sovereign_mirror\dashboard\static\platform\engine.js` (PALETTE)
  - `C:\Users\foste\Documents\projects\worktrees\sovereign-mirror-scaffold\src\sovereign_mirror\core\idea_catalog.py` (belt_domain entry: "720° true close; Spin cover made visible"; "2π looks closed on the base but leaves belts twisted; only 4π (even holonomy) is true identity")
  - `C:\Users\foste\Documents\projects\worktrees\sovereign-mirror-scaffold\src\sovereign_mirror\dashboard\static\platform\eli5.js` ("turn 360° and the belt is still messed up. Turn another 360° (720° total) and it can lie flat"; "Odd = fake close (2π). Even = true close (4π / belt trick)")
  - `C:\Users\foste\Documents\projects\worktrees\sovereign-mirror-scaffold\src\sovereign_mirror\dashboard\static\platform\readings.js` ("Frame-cycle transport ±1; holonomy H = product. Odd = 2π false close; even = 4π true close")
  - `dashboard/static/lanes/elder.md` (estate copy, RECEIPT 2026-09-06): Lipschitz prose law — "sparse-grid distance field, Lipschitz-bound dirty radius"; "SDF marching with Lipschitz continuity gives provable invalidation radii for free". Numeric L appears NOWHERE (matches G3: no shader carries a Lipschitz constant) → numeric L must be RECONSTRUCTED from the prose doctrine and marked as such.
  - `queue/handoff/zcode/CONVO.md` (09-06 receipt): operator's X draft language "Lipschitz bound = dirty radius"; maze walker precedent for clearance-scaled steps.
- [t2] Provenance classes for the plaque: [SRC] verbatim from belt_domain.js / engine.js · [DOC] prose doctrine quoted from idea_catalog.py / eli5.js / readings.js / elder.md · [RECON] reconstructed (numeric Lipschitz L=1, pack.holonomy frames/transports, liveTwist=0) — all marked on screen per the Isfahan law.
- [t3] Catalog builder inspected: `scripts/build_vislab_catalog.py` walks top-level `dashboard/static/*.html` only — `vislab/*.html` subdirectory is NOT scanned. Trivial fix: add a vislab glob block + STAR_SUMMARIES entry. Will edit + regenerate.
- [t4] ARTIFACT WRITTEN: `dashboard/static/vislab/belt_trick.html` — **40,557 bytes**, self-contained (raw WebGL2, zero dependencies, no three.js import; works from `file://` or `/static/vislab/belt_trick.html`).
  Contents: (a) the 3×3 period-2 domain lattice + spinning cube + frame ring + transport ribbons + holonomy badge, all geometry/color/speed constants verbatim from belt_domain.js and engine.js PALETTE; (b) demo state machine — RUN 360° NAIVE shows the untangle attempt failing (residual twist fights back, badge red, "no homotopy exists, π₁(SO₃)=ℤ/2") vs RUN 720° TRUE where the two turns melt to zero (badge even, "4π ≡ identity"); (c) Lipschitz-bounded SDF march — two live probes on the same ray: a naive cache-trusting marcher that accumulates overshoot violations when the wipeout wobble is on, and a bounded marcher stepping `s = f(p)/L − v·Δt` that never crosses; (d) the bound DISPLAYED on a persistent HUD (`L = 1.0 · v ≤ 0.55 u/s · SAFE STEP = f(p)/L − v·Δt · DIRTY RADIUS r = (d − v·Δt)/L`) with violation counters; (e) the Isfahan plaque: full constant table with per-row provenance chips — [SRC] verbatim source, [DOC] prose doctrine quote, [RECON] reconstructed, [PORT] port note — plus verbatim doctrine quotes (idea_catalog.py, eli5.js, readings.js, elder.md).
- [t5] SYNTAX CHECK: extracted inline script (634 lines) → `node --check` → **SYNTAX OK** (node v22.23.1). WebGL2 context guarded with onerror strip + context-null fallback.
- [t6] CATALOG REGISTERED: `scripts/build_vislab_catalog.py` edited (new VISLAB bucket glob for `dashboard/static/vislab/*.html`, skipping catalog.html/play.html; STAR_SUMMARIES entry for belt_trick) and regenerated with repo venv python: **240 entries / 9 buckets, VISLAB = 1** → catalog.json + catalog.html rewritten.
- [t7] NO git commands used at any point (worktree located by filesystem search; wave-lane law held).

## SOURCE PROVENANCE (which constants came from where)

| Provenance | Constants | Source file |
|---|---|---|
| [SRC] verbatim | tile box (0.9,0.05,0.9) @ 1.05 spacing, y −1.2, checker 0x0f1a17/0x122820 · cube 0.9³ @ y 0.6, tilt 0.35·θ, opacity 0.85 · ring r 2.8, anchor y 0.6, node r 0.1, posts 0x2a4a3a · ribbon r 0.03, 32 segments, Catmull-Rom a→mid→cube, mid-y = a.y + kink·transport · transport colors danger 0xff3d5a / gold 0xffc857 · badge r 0.25 @ y 2.4, odd→danger even→accent · kink law sinθ·0.55 / sinθ/2·0.12 · emissive 0.35+0.25·\|sinθ\| · spin speed 0.45+(odd?0.55:0.2)+twist·0.9 · camera hint (0,4,9) · grid 10 | worktree `…/sovereign-mirror-scaffold/src/sovereign_mirror/dashboard/static/platform/scenes/belt_domain.js` |
| [SRC] verbatim | full PALETTE (bg 0x06040a, accent 0xff2d95, accent2 0x00f0ff, danger 0xff3d5a, gold 0xffc857, residual 0xc89bff, muted 0x4a2460) | worktree `…/platform/engine.js` |
| [DOC] prose | 720° = 4π true close · 360° = 2π false close · "Spin cover made visible" · "2π looks closed on the base but leaves belts twisted; only 4π (even holonomy) is true identity" | worktree `…/core/idea_catalog.py` |
| [DOC] prose | "turn 360° and the belt is still messed up. Turn another 360° (720° total) and it can lie flat" · "Odd = fake close (2π). Even = true close (4π)" | worktree `…/platform/eli5.js` |
| [DOC] prose | "Frame-cycle transport ±1; holonomy H = product. Odd = 2π false close; even = 4π true close" | worktree `…/platform/readings.js` |
| [DOC] prose | Lipschitz march law: "SDF marching with Lipschitz continuity gives provable invalidation radii for free"; dirty-radius invalidation | estate `dashboard/static/lanes/elder.md` (RECEIPT 2026-09-06) |
| [RECON] marked on screen | numeric **L = 1.0** (exact rigid-box SDF; NO source carries a numeric Lipschitz constant — G3 verdict, confirmed by grep across worktree + estate) · surface speed bound v = 0.55 × ω_max (derived: SRC kink amplitude × SRC speed law) · n_anchors = 4, transports (+1,−1,+1,−1), frames f0–f3 (pack.holonomy unavailable) · liveTwist = 0 (pack._live unavailable) | reconstruction, flagged in plaque table with red [RECON] chips |

## DELIVERABLE

- File: `C:\Users\foste\Documents\projects\local_sovereign_agent\dashboard\static\vislab\belt_trick.html` — 40,557 bytes
- Also touched: `scripts\build_vislab_catalog.py` (VISLAB bucket + summary), regenerated `dashboard\static\vislab\catalog.json` / `catalog.html` (240 entries / 9 buckets)
- Syntax: `node --check` → SYNTAX OK (634 extracted lines, node v22.23.1)
- Launch: `/static/vislab/belt_trick.html` (dashboard) or open the file directly

**What the Lipschitz bound PROTECTS in this rendering:** the step. Because the distance field is 1-Lipschitz, stepping s = f(p)/L is a proof — not a hope — that the probe cannot cross the surface; the wobble eats clearance at rate v, and the bound converts that into the exact safe discount (v·Δt) and the dirty invalidation radius (d − v·Δt)/L, so the scene can move fast without a single wipeout — the on-screen counters show the naive marcher eating overshoots while the bounded one stays at zero.
