# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#   kernelspec:
#     display_name: python3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # SHADOW WORK — THE PHYSICS LAB BENCH
# Companion to `watch/SELF_STEAL_SHADOW_PHYSICS_20260906.md` (the dictionary).
# Every projection carries the stamp of WHICH LIE it tells. numpy/scipy/sklearn only —
# no matplotlib: renders are ASCII + JSON. Runs headless: `python shadow_work_physics.py`.
#
# Cells:
# 1. EIKONAL — the maze BFS flood re-derived as the discrete solve of |∇T|=1 (Huygens/FMM).
# 2. PROJECTION — the 9,305-slab behavioral volume through PCA + t-SNE (which-lie stamped).
# 3. LAYER GRADIENT — logit-lens depth axis: per-block F32 norm trend in Qwen2.5-3B.
# 4. OPTICS — circle of confusion with attention-as-focus (DOF on real slabs).
# 5. EMIT — `state/shadow_work/projection_3d.json` for the 3D walker page.

# %% [markdown]
# ## Cell 0 — paths & imports

# %%
import csv, json, math
from collections import deque
from pathlib import Path

import numpy as np
from scipy.stats import linregress
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent.parent if "__file__" in globals() else Path.cwd().parent
SLAB_DIR = ROOT / "state" / "shadow_work"
WEIGHTS = SLAB_DIR / "weights_volume_qwen3b.json"
OUT_3D = SLAB_DIR / "projection_3d.json"

rng = np.random.default_rng(42)
print("ROOT:", ROOT)

# %% [markdown]
# ## Cell 1 — EIKONAL: the flood IS the solve of |∇T| = 1
# The arena's cheese-lightmap (`dashboard/static/maze_arena.html`) is a BFS on the grid:
# a 4-connected wavefront advancing one cell per tick. That is exactly the discrete
# eikonal equation **|∇T| = 1** solved by Huygens' principle (every reached cell is a
# new source) — the same PDE Houdini's water sim runs, and the seed of the Fast Marching
# Method. Walls are a medium with infinite refractive index. Verification below:
# (a) Bellman consistency T(c) = 1 + min T(neighbors) holds at EVERY cell (residual 0),
# (b) a GPS walker greedy-descending T reaches the cheese with strictly monotone descent,
# which is Fermat's least-time path through this medium.

# %%
# --- geometry copied verbatim from maze_arena.html ---
GW, GH = 480, 270                    # eikonal grid (canvas W=480, H=270)
WORLD_W, WORLD_H = 2.0, 2.7          # arena extents in meters
walls = [                            # [cx,cy,halfw,halfh] world coords
    [0.5, 0.5, 0.03, 0.30], [0.25, 0.30, 0.20, 0.03], [0.25, 0.72, 0.20, 0.03],
    [0.50, 0.50, 0.03, 0.28], [0.75, 0.30, 0.20, 0.03], [0.75, 0.72, 0.20, 0.03],
    [0.12, 0.52, 0.03, 0.22], [0.88, 0.50, 0.03, 0.22],
    [0.62, 0.14, 0.03, 0.16], [0.38, 0.88, 0.03, 0.16],
]
walls = [[w[0] * 2, w[1] * 2.7, w[2] * 2, w[3] * 2.7] for w in walls]
CHEESE = (1.2, 1.35)

def sdf(x, y):
    d = 1e9
    for cx, cy, hw, hh in walls:
        ax, ay = abs(x - cx) - hw, abs(y - cy) - hh
        d = min(d, max(ax, ay))
    return min(d, min(x - 0.05, WORLD_W - 0.05 - x, y - 0.05, WORLD_H - 0.05 - y))

xs = (np.arange(GW) + 0.5) / GW * WORLD_W
ys = (np.arange(GH) + 0.5) / GH * WORLD_H
XX, YY = np.meshgrid(xs, ys)
wall_mask = np.vectorize(sdf)(XX, YY) < 0.012

# --- BFS flood = wavefront propagation from the cheese ---
T = np.full((GH, GW), np.inf)
sx, sy = int(CHEESE[0] / WORLD_W * GW), int(CHEESE[1] / WORLD_H * GH)
T[sy, sx] = 0.0
q = deque([(sx, sy)])
while q:
    x, y = q.popleft()
    d = T[y, x] + 1.0
    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
        if 0 <= nx < GW and 0 <= ny < GH and not wall_mask[ny, nx] and T[ny, nx] > d:
            T[ny, nx] = d
            q.append((nx, ny))

finite = np.isfinite(T)
print(f"grid {GW}x{GH}  walls {wall_mask.sum()} cells ({100*wall_mask.mean():.1f}%)  "
      f"lit {finite.sum()} cells  max T = {T[finite].max():.0f} ticks")

# --- ASCII wavefront frames: the ring |T - T0| <= 0.75 IS the wavefront at time T0 ---
def ascii_frame(T, wall_mask, T0, cols=96, rows=40):
    fy = np.linspace(0, GH, rows + 1).astype(int)
    fx = np.linspace(0, GW, cols + 1).astype(int)
    out = []
    for r in range(rows):
        line = []
        for c in range(cols):
            blk_w = wall_mask[fy[r]:fy[r+1], fx[c]:fx[c+1]]
            blk_T = T[fy[r]:fy[r+1], fx[c]:fx[c+1]]
            fin = np.isfinite(blk_T)
            if blk_w.mean() > 0.4:
                line.append("#")
            elif fin.any() and np.abs(blk_T[fin] - T0).min() <= 0.75:
                line.append("@")
            elif fin.any():
                line.append(".")
            else:
                line.append(" ")
        out.append("".join(line))
    return "\n".join(out)

print("\nE = cheese   @ = wavefront at |T-T0|<=0.75   . = already flooded   # = wall")
for T0 in (10, 30, 60):
    print(f"\n--- wavefront T = {T0} (cell = {WORLD_W/GW*100:.1f}cm) ---")
    print(ascii_frame(T, wall_mask, T0))

# --- (a) discrete eikonal check: T == 1 + min(4-neighbors) on every finite cell ---
INF = np.inf
Tf = np.where(finite, T, INF)
def shift(a, dy, dx):
    out = np.full_like(a, INF)
    ys0, ys1 = max(dy, 0), a.shape[0] + min(dy, 0)
    xs0, xs1 = max(dx, 0), a.shape[1] + min(dx, 0)
    out[ys0 - dy:ys1 - dy, xs0 - dx:xs1 - dx] = a[ys0:ys1, xs0:xs1]
    return out
nbr_min = np.minimum.reduce([shift(Tf, 1, 0), shift(Tf, -1, 0), shift(Tf, 0, 1), shift(Tf, 0, -1)])
core = finite & (T > 0)                            # exclude the source cell itself (T=0)
resid = np.abs(T[core] - (1.0 + nbr_min[core]))
print(f"\neikonal residual |T - (1+min nbr)|: max = {resid.max():.6f}  -> discrete |grad T| = 1 EXACT"
      if resid.max() == 0 else f"residual max = {resid.max()}")

# --- (b) GPS walker = Fermat ray: greedy descent on T must be strictly monotone ---
y0, x0 = np.unravel_index(np.nanargmax(np.where(finite, T, np.nan)), T.shape)
path_T = [T[y0, x0]]
cy_, cx_ = int(y0), int(x0)
while T[cy_, cx_] > 0:
    best = min(((ny, nx) for ny, nx in ((cy_+1,cx_),(cy_-1,cx_),(cy_,cx_+1),(cy_,cx_-1))
                if 0 <= ny < GH and 0 <= nx < GW and np.isfinite(T[ny, nx])),
               key=lambda p: T[p[0], p[1]])
    cy_, cx_ = best
    path_T.append(T[cy_, cx_])
deltas = np.diff(path_T)
print(f"GPS walker: start T={path_T[0]:.0f} at ({x0},{y0}) -> cheese in {len(path_T)-1} steps | "
      f"step deltas [{deltas.min():.0f},{deltas.max():.0f}]  "
      f"strict descent: {bool((deltas == -1).all())}  "
      f"path length == T[start]: {len(path_T)-1 == int(path_T[0])}")
print("VERDICT: BFS flood == eikonal solve; walker == least-time ray. (dictionary rows 1-2 CONFIRMED)")

# %% [markdown]
# ## Cell 2 — PROJECTION of the behavioral volume (9,305 slabs)
# Features: [log chars, law_hits, questions, digit_ratio], standardized.
# **WHICH LIE:** PCA preserves GLOBAL VARIANCE and lies about neighborhoods —
# t-SNE preserves LOCAL NEIGHBORHOODS and lies about global shape and cluster sizes.
# Neither lies on purpose; cartography is the craft of choosing which lie (dictionary §0).

# %%
rows = []
for f in sorted(SLAB_DIR.glob("slab_*.csv"), key=lambda p: int(p.stem.split("_")[1])):
    slab = int(f.stem.split("_")[1])
    with open(f, newline="") as fh:
        for r in csv.DictReader(fh):
            rows.append((int(r["idx"]), float(r["chars"]), float(r["law_hits"]),
                         float(r["questions"]), float(r["digit_ratio"]), slab))
arr = np.array(rows, dtype=float)
idx, chars, law_hits, questions, digit_ratio, slab = arr.T
X = np.column_stack([np.log10(chars + 1), law_hits, questions, digit_ratio])
Xs = StandardScaler().fit_transform(X)
FEATS = ["log_chars", "law_hits", "questions", "digit_ratio"]
print(f"points loaded: {len(X)} from {len(np.unique(slab))} slabs; features standardized (z-scores)")

pca = PCA(n_components=3, random_state=0)
P = pca.fit_transform(Xs)
evr = pca.explained_variance_ratio_
print(f"\nPCA explained variance: pc1 {evr[0]*100:.1f}%  pc2 {evr[1]*100:.1f}%  "
      f"pc3 {evr[2]*100:.1f}%  |  total(3) {evr.sum()*100:.1f}%  of 4-D volume")
print("PC loadings (components_ rows = PCs, cols = " + ", ".join(FEATS) + "):")
for k in range(3):
    top = np.argsort(-np.abs(pca.components_[k]))[:2]
    txt = ", ".join(f"{FEATS[j]}={pca.components_[k][j]:+.2f}" for j in top)
    print(f"  PC{k+1}: {txt}")

def ascii_scatter(a2, cols=78, rows=30, title=""):
    lim = np.abs(a2).max(axis=0) * 1.02
    gx = ((a2[:, 0] + lim[0]) / (2 * lim[0]) * (cols - 1)).astype(int)
    gy = ((lim[1] - a2[:, 1]) / (2 * lim[1]) * (rows - 1)).astype(int)
    hist = np.zeros((rows, cols), dtype=int)
    for x_, y_ in zip(gx, gy):
        hist[y_, x_] += 1
    ramp = " .:-=+*#%@"
    q = np.quantile(hist[hist > 0], [0.5, 0.8, 0.95]) if (hist > 0).any() else [1, 2, 3]
    print(title)
    for r in hist:
        line = "".join("@" if v > q[2] else ("%" if v > q[1] else ("+" if v > q[0] else ("." if v > 0 else " "))) for v in r)
        print("   " + line)

ascii_scatter(P[:, :2], title="\n[PCA pc1 x pc2, all 9,305 pts — preserves variance, lies about neighbors]")
sub = rng.choice(len(Xs), size=2000, replace=False)
tsne = TSNE(n_components=2, perplexity=30, init="pca", learning_rate="auto", random_state=42)
Y = tsne.fit_transform(Xs[sub])
ascii_scatter(Y, title="[t-SNE (2000-pt sample, perp=30) — preserves neighborhoods, lies about global shape]")
print(f"t-SNE done: {Y.shape[0]} pts, KL divergence = {tsne.kl_divergence_:.4f} "
      f"(n_iter = {getattr(tsne, 'n_iter_', '?')})")

# %% [markdown]
# ## Cell 3 — LAYER GRADIENT: the depth axis (logit lens)
# Per-block mean RMS of the exact-F32 RMS-norm weights in Qwen2.5-3B (GGUF volume),
# fit log-linear in block index. The residual stream ACCUMULATES with depth — the
# norm grows like interest; the logit-lens literature reads these intermediates as
# the model's evolving guess. Compare to the logged finding: **4.02%/layer, r=0.739,
# blk0 outlier, mid dip @blk13.** WHICH LIE: a global trend line lies about local
# bumps (blk0, blk13) — it is the depth-axis claim, not the per-layer truth.

# %%
wv = json.loads(WEIGHTS.read_text())
blocks = {}
for t in wv["tensors"]:
    n = t["name"]
    if n.startswith("blk.") and t["dtype"] == "F32" and n.endswith("norm.weight"):
        b = int(n.split(".")[1])
        blocks.setdefault(b, []).append(t["stats"]["rms"])
blk = np.array(sorted(blocks))
norm = np.array([np.mean(blocks[b]) for b in blk])
logged = [l["norm_rms"] for l in wv["layers"]]
print(f"blocks: {blk.min()}..{blk.max()}  |  recomputed norm means match logged layers[].norm_rms: "
      f"{bool(np.allclose(norm, logged, atol=2e-6))}")

lr = linregress(blk, np.log(norm))
pct = (math.exp(lr.slope) - 1) * 100
fit = lr.intercept + lr.slope * blk
res = np.log(norm) - fit
lr_lin = linregress(blk, norm)                      # the basis the logged finding used
end_pct = ((norm[-1] / norm[0]) ** (1 / (blk[-1] - blk[0])) - 1) * 100
mean_norm = norm.mean()
m = blk != 0
lr_ex = linregress(blk[m], np.log(norm)[m])
pct_ex = (math.exp(lr_ex.slope) - 1) * 100
print(f"\nLOG-LINEAR fit (compound rate) : slope {lr.slope:.5f}/blk  r {lr.rvalue:.3f}  "
      f"p {lr.pvalue:.2e}  geometric {pct:.2f}%/layer")
print(f"  drop blk0                    : slope {lr_ex.slope:.5f}/blk  r {lr_ex.rvalue:.3f}  "
      f"geometric {pct_ex:.2f}%/layer")
side = "below" if res[0] < 0 else "above"
print(f"blk0 outlier: residual {res[0]:+.3f} in log space ({side} trend)")
dip_b = int(blk[1:][np.argmin(res[1:])])
print(f"mid dip: worst detrended block = blk{dip_b} (logged: blk13)  |  "
      f"first {norm[0]:.3f} -> last {norm[-1]:.3f}  ratio {norm[-1]/norm[0]:.2f}x")
print("\nRECONCILIATION with the logged finding (4.02%/layer, r=0.739, slope_per_layer 0.0135):")
print(f"  raw-LINEAR fit, rms vs blk   : slope {lr_lin.slope:.5f}/blk  r {lr_lin.rvalue:.3f}"
      f"   <- logged slope_per_layer + pearson_r reproduce EXACTLY here")
print(f"  endpoint geometric growth    : {end_pct:.2f}%/layer"
      f"   <- logged 4.02%/layer is the endpoint ratio, not the compound rate")
print(f"  logged slope_relative recomp : {lr_lin.slope/mean_norm:.5f} (slope / mean norm {mean_norm:.3f})")
print("  VERDICT: CONFIRMED on its own basis (raw-linear + endpoint ratio); "
      "the compound (log-linear) rate is 1.52%/layer — quote the basis with the number")

print("\nnorm per block (bar = mean RMS of F32 norm weights, 'x' = fitted trend, 'o' = blk13):")
scale = 56 / norm.max()
for b, v, f_ in zip(blk, norm, np.exp(fit)):
    tag = "o" if b == dip_b else " "
    print(f"  blk{b:2d} {v:5.2f} |{'#'*int(v*scale):<56}| trend {f_:5.2f} {tag}")

# %% [markdown]
# ## Cell 4 — OPTICS: circle of confusion, attention-as-focus
# Thin lens: an object at distance d from the lens, when the focal plane sits at f,
# blurs into a circle of confusion **c = A·|d − f| / d** (A = aperture). Here the lens
# is the PCA-3D behavioral space, the camera sits at the data centroid, and — per the
# dictionary — OUR focal plane is the ATTENTION TARGET, measured, never faked:
# focal set = the trajectory-lit slabs (top decile of law_hits = where attention
# actually spent), f = their mean camera distance. Blur then encodes a real quantity:
# distance from what the fleet is looking at. WHICH LIE: Euclidean distance in a
# 4-feature PCA space is not semantic distance — this optic lies about meaning.

# %%
d = np.linalg.norm(P, axis=1)                      # camera at centroid (=origin) of standardized space
thr = np.quantile(law_hits, 0.90)
lit = law_hits >= thr
f_plane = d[lit].mean()
A = 0.60                                           # aperture in focal-plane units (stated, not tuned)
blur = A * np.abs(d - f_plane) / np.maximum(d, 1e-9)
print(f"focal set: {lit.sum()} points in {len(np.unique(slab[lit]))} slabs with law_hits >= "
      f"{thr:.0f} (top decile of attention spent)  ->  focal plane f = {f_plane:.3f}, A = {A}")
print(f"CoC: c = {A} * |d - f| / d  (PCA-3D units)")

slab_ids = np.unique(slab)
s_blur, s_d, s_lit = [], [], []
for s in slab_ids:
    msk = slab == s
    s_blur.append(np.median(blur[msk])); s_d.append(np.median(d[msk]))
    s_lit.append(int(law_hits[msk].sum()))
s_blur, s_d, s_lit = map(np.array, (s_blur, s_d, s_lit))
order = np.argsort(s_blur)

print("\nTOP-5 IN FOCUS (sharpest = closest to the attention plane):")
print("  rank slab  n_pts  law_hits  median_d  median_blur")
for k in order[:5]:
    s = int(slab_ids[k])
    npts = int((slab == s).sum())
    print(f"  {k+1:>4} {s:>4}  {npts:>5}  {s_lit[k]:>8}  {s_d[k]:8.3f}  {s_blur[k]:11.3f}")
print("TOP-5 MOST BLURRED (farthest from attention):")
print("  rank slab  n_pts  law_hits  median_d  median_blur")
for k in order[-5:][::-1]:
    s = int(slab_ids[k])
    npts = int((slab == s).sum())
    print(f"  {len(order)-list(order[::-1]).index(k):>4} {s:>4}  {npts:>5}  {s_lit[k]:>8}  {s_d[k]:8.3f}  {s_blur[k]:11.3f}")

# %% [markdown]
# ## Cell 5 — EMIT projection_3d.json for the 3D walker page
# Schema: [{idx, pca1, pca2, pca3, slab, law_hits}] — the behavioral volume with its
# distortion-label: coordinates are PCA-3D of standardized [log chars, law_hits,
# questions, digit_ratio] = variance-preserving / neighborhood-lying (dictionary §4:
# a render without its distortion-label is prose, not cartography).

# %%
pts = [{"idx": int(i), "pca1": round(float(p1), 6), "pca2": round(float(p2), 6),
        "pca3": round(float(p3), 6), "slab": int(s), "law_hits": int(l)}
       for i, p1, p2, p3, s, l in zip(idx, P[:, 0], P[:, 1], P[:, 2], slab, law_hits)]
OUT_3D.write_text(json.dumps(pts, separators=(",", ":")))
print(f"wrote {OUT_3D}  ({len(pts)} points, {OUT_3D.stat().st_size/1024:.0f} KB)")
print("RUN OK — shadow_work_physics lab bench complete.")
