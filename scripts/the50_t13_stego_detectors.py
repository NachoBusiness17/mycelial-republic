"""THE 50 / W3 / T13 - locally runnable steganalysis detectors.

Companion script for memory/research_packs/THE50_W3_T13_STEGANALYSIS.md.
Runs on this machine's venv (stdlib + numpy + Pillow, no scipy, no torch needed).

Detectors implemented here:
  1. chi_square_lsb  - Westfeld/Pfitzmann 1999 pairs-of-values chi-square attack.
  2. rs_estimate     - RS analysis (Fridrich/Goljan/Du 2001), simplified
                       single-mask variant with the linear-variation estimator
                       derived in the survey pack.
  3. palette_twins   - palette near-twin analyzer for indexed-color images
                       (GIF / PNG-8): counts used palette entries at L-inf
                       distance <= 1, the artifact palette-LSB tools leave.

Usage:
  .venv/Scripts/python.exe scripts/the50_t13_stego_detectors.py --demo

--demo builds a ground-truth corpus under memory/runs/the50/stego_corpus/
(clean cover vs LSB stego at 100% and 50% rates, palette GIF vs twin-palette
GIF), then scans every file from disk and prints a results table plus
results.json.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[1]
CORPUS = REPO / "memory" / "runs" / "the50" / "stego_corpus"

SEED = 50
SIZE = 256


# ---------------------------------------------------------------------------
# incomplete gamma (Numerical Recipes style) so we can score chi-square
# p-values without scipy
# ---------------------------------------------------------------------------

def _gser(a: float, x: float, itmax: int = 300, eps: float = 3e-9) -> float:
    """Regularized lower incomplete gamma P(a, x) by series."""
    ap = a
    total = 1.0 / a
    term = 1.0 / a
    for _ in range(itmax):
        ap += 1.0
        term *= x / ap
        total += term
        if abs(term) < abs(total) * eps:
            break
    return total * math.exp(-x + a * math.log(x) - math.lgamma(a))


def _gcf(a: float, x: float, itmax: int = 300, eps: float = 3e-9) -> float:
    """Regularized upper incomplete gamma Q(a, x) by continued fraction."""
    b = x + 1.0 - a
    c = 1e300
    d = 1.0 / b
    h = d
    for i in range(1, itmax + 1):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < 1e-300:
            d = 1e-300
        c = b + an / c
        if abs(c) < 1e-300:
            c = 1e-300
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return math.exp(-x + a * math.log(x) - math.lgamma(a)) * h


def chi2_sf(x: float, k: int) -> float:
    """Survival function of the chi-square distribution with k dof."""
    if x <= 0:
        return 1.0
    a = k / 2.0
    if x < a + 1.0:
        return max(0.0, 1.0 - _gser(a, x))
    return _gcf(a, x)


# ---------------------------------------------------------------------------
# detector 1: chi-square pairs-of-values attack on LSB planes
# ---------------------------------------------------------------------------

def chi_square_lsb(arr: np.ndarray) -> dict:
    """Westfeld/Pfitzmann chi-square attack on one 8-bit channel.

    LSB embedding randomizes values within each PoV (2i, 2i+1), driving
    h[2i] -> h[2i+1]. p near 1 means the pairing is fully equalized
    (embedded), p near 0 means the adjacent-bin imbalance of a clean image.
    """
    h = np.bincount(np.asarray(arr).ravel(), minlength=256).astype(float)
    n_pair = h[0::2] + h[1::2]
    use = n_pair > 0
    obs = h[0::2][use]
    exp = n_pair[use] / 2.0
    chi2 = float(((obs - exp) ** 2 / exp).sum())
    dof = int(use.sum()) - 1
    imb = float((np.abs(obs - exp) / np.maximum(exp, 1.0)).mean())
    # sliding-window variant (Westfeld's actual profile): fraction of windows
    # whose local p exceeds 0.5 separates embedded from clean more robustly
    # than one whole-image p on large samples.
    flat = np.asarray(arr).ravel()
    win = 8192
    nwin = max(1, len(flat) // win)
    frac_hi = 0.0
    if nwin > 1:
        hits = 0
        for wi in range(nwin):
            sub = flat[wi * win:(wi + 1) * win]
            hw = np.bincount(sub, minlength=256).astype(float)
            nw = hw[0::2] + hw[1::2]
            uw = nw > 0
            if uw.sum() < 2:
                continue
            cw = float(((hw[0::2][uw] - nw[uw] / 2.0) ** 2 / (nw[uw] / 2.0)).sum())
            if chi2_sf(cw, int(uw.sum()) - 1) > 0.5:
                hits += 1
        frac_hi = hits / nwin
    return {"chi2": round(chi2, 1), "dof": dof, "p_embed": round(chi2_sf(chi2, dof), 6),
            "pair_imbalance": round(imb, 4), "win_frac_p_gt_0.5": round(frac_hi, 3)}


# ---------------------------------------------------------------------------
# detector 2: RS analysis, simplified single-mask variant
# ---------------------------------------------------------------------------

RS_MASK = (1, 0, 0, 1)  # classic RS mask


def _rs_groups(a: np.ndarray) -> np.ndarray:
    """Shape flat channel values into non-overlapping groups of 4.
    Cast to int32: uint8 subtraction would wrap (120-128 -> 248) and wreck
    the discrimination function."""
    n = (len(a) // 4) * 4
    return a[:n].reshape(-1, 4).astype(np.int32)


def _disc(g: np.ndarray) -> np.ndarray:
    """Discrimination function f = |x0-x1| + |x1-x2| + |x2-x3|."""
    return np.abs(g[:, 0] - g[:, 1]) + np.abs(g[:, 1] - g[:, 2]) + np.abs(g[:, 2] - g[:, 3])


def _apply_mask(g: np.ndarray, mask) -> np.ndarray:
    out = g.copy()
    for j, m in enumerate(mask):
        if m:
            out[:, j] ^= 1
    return out


def _rs_D(channel_flat: np.ndarray) -> float:
    g = _rs_groups(channel_flat)
    f0 = _disc(g)
    f1 = _disc(_apply_mask(g, RS_MASK))
    R = int((f1 > f0).sum())
    S = int((f1 < f0).sum())
    return (R - S) / float(len(g))


def rs_estimate(arr: np.ndarray) -> dict:
    """RS-style R-S statistic (Fridrich/Goljan/Du 2001), simplified variant.

    D = R - S over groups of 4 with the classic (1,0,0,1) mask; R counts
    groups whose local variance f rises under LSB flipping, S those where it
    falls. On the demo corpus D_meas ranks embedding rate monotonically
    (clean ~ D0, 50% ~ D0/4, 100% ~ 0 under the empirical quadratic
    D(q) ~ D0 (1 - 2q)^2).

    KNOWN LIMIT (documented in the survey pack): converting D_meas into a
    closed-form rate p needs the full Fridrich estimator with mask-complement
    (-M) measurements. The quadratic model is symmetric under q <-> 1-q, so
    the two-measurement variant (D_meas, D after global flip) cannot resolve
    p on its own; we therefore report the validated detection statistic, not
    a calibrated p.
    """
    a = np.asarray(arr).ravel().astype(np.uint8)
    d_meas = _rs_D(a)
    d_flip = _rs_D(a ^ 1)
    return {"D_meas": round(d_meas, 4), "D_flip": round(d_flip, 4)}


# ---------------------------------------------------------------------------
# detector 3: palette near-twin analyzer (indexed-color images)
# ---------------------------------------------------------------------------

def palette_twins(path: Path) -> dict:
    """Count USED palette entries sitting at L-inf distance <= 1 from
    another used entry. Palette LSB stego tools extend the palette with
    twin colors (c, c+1) so an index bit flip stays visually identical;
    clean quantized palettes rarely hold systematic unit-distance twins.
    """
    img = Image.open(path)
    if img.mode != "P":
        return {"file": path.name, "mode": img.mode, "applicable": False}
    pal = np.array(img.getpalette() or [], dtype=np.int64).reshape(-1, 3)
    used_mask = np.bincount(np.asarray(img).ravel(), minlength=len(pal)) > 0
    used_idx = np.nonzero(used_mask)[0]
    twins = 0
    twin_examples = []
    for ii in range(len(used_idx)):
        for jj in range(ii + 1, len(used_idx)):
            i, j = int(used_idx[ii]), int(used_idx[jj])
            if int(np.max(np.abs(pal[i] - pal[j]))) <= 1:
                twins += 1
                if len(twin_examples) < 3:
                    twin_examples.append((i, int(j), pal[i].tolist(), pal[j].tolist()))
    return {"file": path.name, "mode": "P", "applicable": True,
            "palette_entries": int(len(pal)), "used_entries": int(len(used_idx)),
            "twin_pairs": twins, "examples": twin_examples}


# ---------------------------------------------------------------------------
# ground-truth corpus builder
# ---------------------------------------------------------------------------

def _cover_image(rng: np.random.Generator) -> np.ndarray:
    """Synthetic photo-like cover: low-frequency fields plus CORRELATED
    (block-upsampled) noise, so neighboring pixels are locally similar like
    in a natural image. White noise kills LSB-structure detectors (RS needs
    small adjacent differences); real photos are locally smooth."""
    xs = np.arange(SIZE)
    x, y = np.meshgrid(xs, xs)
    base = (
        112.0
        + 38.0 * np.sin(x / 17.0) * np.cos(y / 23.0)
        + 18.0 * np.sin((x + y) / 31.0)
        + 9.0 * np.cos(x / 7.0 - y / 11.0)
    )
    grid = rng.normal(0.0, 6.0, (SIZE // 16, SIZE // 16))
    noise = np.kron(grid, np.ones((16, 16)))  # piecewise-constant, sigma 6
    img = np.dstack([base + noise, base * 0.92 + noise * 0.9, base * 1.05 + noise * 1.1])
    img = np.clip(img, 0, 255).astype(np.uint8)
    # mild posterization (>>2<<2): natural images hold runs of equal
    # adjacent values; those plateaus are exactly the structure RS reads
    # (flipping one endpoint of an equal pair can only raise local variance)
    return (img >> 2) << 2


def _embed_lsb(img: np.ndarray, rate: float, rng: np.random.Generator) -> np.ndarray:
    out = img.copy()
    bits = rng.integers(0, 2, size=img.shape, dtype=np.uint8)
    sel = rng.random(img.shape) < rate
    out = (out & np.uint8(0xFE)) | np.where(sel, bits, out & np.uint8(1)).astype(np.uint8)
    return out.astype(np.uint8)


def _palette_cover(rng: np.random.Generator):
    """Smooth-gradient image quantized to a 128-color palette spaced so that
    consecutive colors sit at L-inf distance 2 (no accidental twins)."""
    xs = np.arange(SIZE)
    g = np.meshgrid(xs, xs)[0] + np.arange(SIZE)[:, None]
    ramp = ((g % SIZE) / (SIZE - 1) * 127).astype(np.uint8)  # 0..127
    pal = np.zeros((128, 3), dtype=np.uint8)
    pal[:, 0] = np.arange(128, dtype=np.uint8) * 2           # step 2: red
    pal[:, 1] = 64 + np.arange(128, dtype=np.uint8)          # step 1 in green? -> keep >=2 spacing
    pal[:, 1] = np.clip(60 + np.arange(128, dtype=np.int64) * 1, 0, 255).astype(np.uint8)
    pal[:, 2] = 255 - np.arange(128, dtype=np.uint8) * 1
    # force L-inf spacing of the *palette* itself to 2 by using step 2 in all
    # channels that vary:
    pal[:, 1] = np.clip(40 + np.arange(128, dtype=np.int64) * 2, 0, 255).astype(np.uint8)
    pal[:, 2] = (255 - np.arange(128, dtype=np.int64) * 2).astype(np.uint8)
    idx = ramp.copy()
    noise = rng.integers(0, 2, size=idx.shape) * (rng.random(idx.shape) < 0.02)
    idx = np.clip(idx.astype(np.int64) + noise, 0, 127).astype(np.uint8)
    return idx, pal


def build_corpus() -> list[Path]:
    CORPUS.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)
    cover = _cover_image(rng)

    paths = {}
    paths["cover"] = CORPUS / "cover.png"
    Image.fromarray(cover).save(paths["cover"])

    paths["stego_full"] = CORPUS / "stego_full.png"
    Image.fromarray(_embed_lsb(cover, 1.0, rng)).save(paths["stego_full"])

    paths["stego_half"] = CORPUS / "stego_half.png"
    Image.fromarray(_embed_lsb(cover, 0.5, rng)).save(paths["stego_half"])

    idx, pal = _palette_cover(rng)
    pimg = Image.fromarray(idx, mode="L").convert("P")
    pimg.putpalette(pal.reshape(-1).tolist())
    paths["cover_p"] = CORPUS / "cover_p.gif"
    pimg.save(paths["cover_p"])

    twins = pal.astype(np.int64).copy()
    twins[:, 2] = np.clip(twins[:, 2] + 1, 0, 255)  # blue +1 twin
    pal2 = np.vstack([pal.astype(np.int64), twins]).astype(np.uint8)
    bits = rng.integers(0, 2, size=idx.shape)
    idx2 = np.where(bits == 1, idx.astype(np.int64) + 128, idx.astype(np.int64)).astype(np.uint8)
    simg = Image.fromarray(idx2, mode="L").convert("P")
    simg.putpalette(pal2.reshape(-1).tolist())
    paths["stego_p"] = CORPUS / "stego_p.gif"
    simg.save(paths["stego_p"])

    return list(paths.values())


# ---------------------------------------------------------------------------
# scan + report
# ---------------------------------------------------------------------------

def scan_all() -> dict:
    results = {}
    for f in sorted(CORPUS.iterdir()):
        if f.suffix.lower() not in {".png", ".gif"}:
            continue
        img = np.array(Image.open(f).convert("RGB"))
        entry = {}
        for ci, cname in enumerate("RGB"):
            entry[f"chi2_{cname}"] = chi_square_lsb(img[:, :, ci])
            entry[f"rs_{cname}"] = rs_estimate(img[:, :, ci])
        entry["palette"] = palette_twins(f)
        results[f.name] = entry
    return results


def print_table(results: dict) -> None:
    hdr = (f"{'file':<16} {'chi2 p R/G/B':<22} {'chi2 win-frac R/G/B':<24} "
           f"{'RS D R/G/B':<22} {'palette twins':<14}")
    print(hdr)
    print("-" * len(hdr))
    for name, e in results.items():
        ps = "/".join(f"{e[f'chi2_{c}']['p_embed']:.3f}" for c in "RGB")
        wf = "/".join(f"{e[f'chi2_{c}']['win_frac_p_gt_0.5']:.3f}" for c in "RGB")
        rs = "/".join(f"{e[f'rs_{c}']['D_meas']:.3f}" for c in "RGB")
        pal = f"{e['palette']['twin_pairs']}" if e["palette"]["applicable"] else "n/a"
        print(f"{name:<16} {ps:<22} {wf:<24} {rs:<22} {pal:<14}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true", help="build corpus then scan")
    ap.add_argument("--scan-only", action="store_true")
    args = ap.parse_args()
    if args.demo:
        files = build_corpus()
        print(f"built corpus: {[f.name for f in files]}")
        print(f"corpus dir: {CORPUS}")
    elif not CORPUS.exists():
        print("no corpus; run with --demo", file=sys.stderr)
        return 2
    results = scan_all()
    print_table(results)
    out = CORPUS / "results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"results.json -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
