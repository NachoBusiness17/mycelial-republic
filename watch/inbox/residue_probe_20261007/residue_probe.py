#!/usr/bin/env python
"""residue_probe.py: minimal falsifiable core of the quaternion-residue doctrine.

Arms (see PREREG.md, frozen before this run):
  1 positive control: Euler 3-2-1 vs quaternion integration near gimbal lock.
  2 reconstruction impossibility: per-component complex projection cut (A) vs
    coupling-keeping features (B), MLP AUROC across 5 coupling levels.
  3 coordination form: cross-spectral coherence on complex projections (A) vs
    joint quaternion-domain correlation (B), AUROC.

Numpy only, no network, deterministic under the seeds fixed in PREREG.md.
Writes rows to results.jsonl (append) and appends a results block to PREREG.md.
"""

import argparse
import datetime as _dt
import json
import math
import os
import platform
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PREREG = os.path.join(HERE, "PREREG.md")
RESULTS_PATH = os.path.join(HERE, "results.jsonl")

G_LEVELS = [0.05, 0.10, 0.20, 0.35, 0.60]
SEEDS = [1000, 2000, 3000, 4000, 5000]
SIG_D = 0.15
T_STREAM = 64
ARM2_BASE = 2_500_000_000  # amended +500,000,000 (seed decontamination, PREREG addendum b)
ARM3_BASE = 3_500_000_000  # amended +500,000,000


# ---------------------------------------------------------------- quaternion helpers
# convention (w, x, y, z)

def qmul(a, b):
    aw, av = a[..., :1], a[..., 1:]
    bw, bv = b[..., :1], b[..., 1:]
    w = aw * bw - np.sum(av * bv, axis=-1, keepdims=True)
    v = aw * bv + bw * av + np.cross(av, bv)
    return np.concatenate([w, v], axis=-1)


def qnormalize(q):
    n = np.linalg.norm(q, axis=-1, keepdims=True)
    return q / np.maximum(n, 1e-12)


def qexp_rot(v):
    # rotation vector -> unit quaternion, stable at small angles
    a = np.linalg.norm(v, axis=-1, keepdims=True)
    half = 0.5 * a
    sinc = np.sinc(half / np.pi)  # sin(half)/half
    return np.concatenate([np.cos(half), v * (0.5 * sinc)], axis=-1)


def q_to_R(q):
    w, x, y, z = q[..., 0], q[..., 1], q[..., 2], q[..., 3]
    R = np.empty(q.shape[:-1] + (3, 3))
    R[..., 0, 0] = 1 - 2 * (y * y + z * z)
    R[..., 0, 1] = 2 * (x * y - w * z)
    R[..., 0, 2] = 2 * (x * z + w * y)
    R[..., 1, 0] = 2 * (x * y + w * z)
    R[..., 1, 1] = 1 - 2 * (x * x + z * z)
    R[..., 1, 2] = 2 * (y * z - w * x)
    R[..., 2, 0] = 2 * (x * z - w * y)
    R[..., 2, 1] = 2 * (y * z + w * x)
    R[..., 2, 2] = 1 - 2 * (x * x + y * y)
    return R


def euler_to_q(yaw, pitch, roll):
    cy, sy = np.cos(yaw / 2), np.sin(yaw / 2)
    cp, sp = np.cos(pitch / 2), np.sin(pitch / 2)
    cr, sr = np.cos(roll / 2), np.sin(roll / 2)
    zero = np.zeros_like(cy)
    qz = np.stack([cy, zero, zero, sy], axis=-1)
    qy = np.stack([cp, zero, sp, zero], axis=-1)
    qx = np.stack([cr, sr, zero, zero], axis=-1)
    return qnormalize(qmul(qz, qmul(qy, qx)))


def euler_to_R(yaw, pitch, roll):
    return q_to_R(euler_to_q(yaw, pitch, roll))


def geodesic_angle(Ra, Rb):
    tr = np.sum(Ra * Rb, axis=(-1, -2))
    return np.arccos(np.clip((tr - 1.0) / 2.0, -1.0, 1.0))


# ---------------------------------------------------------------- statistics helpers

def auroc(pos, neg):
    # Mann-Whitney AUROC with average ranks for ties; pos = scores of positives
    scores = np.concatenate([pos, neg])
    uniq, inv, counts = np.unique(scores, return_inverse=True, return_counts=True)
    ends = np.cumsum(counts)
    starts = ends - counts
    avg = (starts + ends - 1) / 2.0 + 1.0
    ranks = avg[inv]
    n1, n0 = len(pos), len(neg)
    u = ranks[:n1].sum() - n1 * (n1 + 1) / 2.0
    return float(u / (n1 * n0))


def ci95(vals):
    v = np.asarray(vals, dtype=float)
    m = float(v.mean())
    s = float(v.std(ddof=1)) if len(v) > 1 else 0.0
    half = 1.96 * s / math.sqrt(len(v))
    return m, m - half, m + half, [float(x) for x in v]


def at_chance(mean, lo, hi):
    return (lo <= 0.5 <= hi) or abs(mean - 0.5) <= 0.02


# ---------------------------------------------------------------- stream generation

def gen_streams(rng, n, condition, g, arm):
    """Unit-quaternion state streams for two channels, per the PREREG model."""
    T = T_STREAM
    q1 = np.zeros((n, T + 1, 4))
    q2 = np.zeros((n, T + 1, 4))
    q1[:, 0] = np.array([1.0, 0.0, 0.0, 0.0])
    q2[:, 0] = np.array([1.0, 0.0, 0.0, 0.0])
    e1 = rng.standard_normal((n, T, 4))
    eta = rng.standard_normal((n, T, 4))

    if condition == "null":
        e2 = eta
        for t in range(T):
            q1[:, t + 1] = qnormalize(q1[:, t] + SIG_D * e1[:, t])
            q2[:, t + 1] = qnormalize(q2[:, t] + SIG_D * e2[:, t])
        return q1, q2

    if arm == 3:
        # Haar-random unit quaternion per step
        u_all = qnormalize(rng.standard_normal((n, T, 4)))
        e2 = math.sqrt(1.0 - g * g) * eta + g * qmul(u_all, e1)
        for t in range(T):
            q1[:, t + 1] = qnormalize(q1[:, t] + SIG_D * e1[:, t])
            q2[:, t + 1] = qnormalize(q2[:, t] + SIG_D * e2[:, t])
        return q1, q2

    # arm 2: u(t) = (0, v1(t)/|v1(t)|) from channel 1 state at step t
    for t in range(T):
        v1 = q1[:, t, 1:4]
        nrm = np.linalg.norm(v1, axis=1, keepdims=True)
        safe = v1 / np.maximum(nrm, 1e-12)
        fallback = np.tile(np.array([1.0, 0.0, 0.0]), (n, 1))
        u_vec = np.where(nrm > 1e-8, safe, fallback)
        u = np.concatenate([np.zeros((n, 1)), u_vec], axis=1)
        e2_t = math.sqrt(1.0 - g * g) * eta[:, t, :] + g * qmul(u, e1[:, t, :])
        q1[:, t + 1] = qnormalize(q1[:, t] + SIG_D * e1[:, t])
        q2[:, t + 1] = qnormalize(q2[:, t] + SIG_D * e2_t)
    return q1, q2


def innovations(q1, q2):
    return np.diff(q1, axis=1), np.diff(q2, axis=1)


# ---------------------------------------------------------------- arm 2 features

def component_stats(x):
    # x: (n, T, C) -> (n, C*8): mean, std, skew, kurt, ac1, ac2, amp_mean, amp_std
    n, T, C = x.shape
    mu = x.mean(axis=1)
    sd = x.std(axis=1)
    z = (x - mu[:, None, :]) / np.maximum(sd[:, None, :], 1e-12)
    sk = (z ** 3).mean(axis=1)
    ku = (z ** 4).mean(axis=1) - 3.0
    ac1 = (z[:, :-1, :] * z[:, 1:, :]).mean(axis=1)
    ac2 = (z[:, :-2, :] * z[:, 2:, :]).mean(axis=1)
    # analytic signal (per-component complex projection) via FFT Hilbert
    F = np.fft.fft(x, axis=1)
    Z = np.zeros_like(F)
    half = T // 2
    Z[:, 0, :] = F[:, 0, :]
    if T % 2 == 0:
        Z[:, half, :] = F[:, half, :]
        Z[:, 1:half, :] = 2.0 * F[:, 1:half, :]
    else:
        Z[:, 1:half + 1, :] = 2.0 * F[:, 1:half + 1, :]
    amp = np.abs(np.fft.ifft(Z, axis=1))
    feats = np.stack([mu, sd, sk, ku, ac1, ac2, amp.mean(axis=1), amp.std(axis=1)], axis=1)
    return feats.reshape(n, -1)


def features_A(q1, q2):
    d1, d2 = innovations(q1, q2)
    series = np.concatenate([d1, d2], axis=2)
    return component_stats(series)


def features_B(q1, q2):
    fA = features_A(q1, q2)
    d1, d2 = innovations(q1, q2)
    n, T, _ = d1.shape
    cross = np.einsum("nta,ntb->nab", d1, d2) / T
    cross_sq = (cross ** 2).reshape(n, -1)
    comm = qmul(d1, d2) - qmul(d2, d1)
    comm_norm = np.linalg.norm(comm, axis=-1)
    prod_sq = (qmul(d1, d2) ** 2).mean(axis=1)
    s1, v1 = d1[:, :, 0:1], d1[:, :, 1:4]
    s2, v2 = d2[:, :, 0:1], d2[:, :, 1:4]
    antisym = np.linalg.norm(s1 * v2 - s2 * v1, axis=-1)
    extra = np.concatenate([
        cross_sq,
        comm_norm.mean(axis=1, keepdims=True),
        comm_norm.std(axis=1, keepdims=True),
        prod_sq,
        antisym.mean(axis=1, keepdims=True),
        antisym.std(axis=1, keepdims=True),
    ], axis=1)
    return np.concatenate([fA, extra], axis=1)


# ---------------------------------------------------------------- arm 2 MLP (numpy, Adam)

class MLP:
    def __init__(self, dims, rng):
        self.W, self.b = [], []
        for d_in, d_out in zip(dims[:-1], dims[1:]):
            self.W.append(rng.standard_normal((d_in, d_out)) * math.sqrt(2.0 / d_in))
            self.b.append(np.zeros(d_out))
        self.rng = rng
        self.mW = [np.zeros_like(w) for w in self.W]
        self.vW = [np.zeros_like(w) for w in self.W]
        self.mb = [np.zeros_like(b) for b in self.b]
        self.vb = [np.zeros_like(b) for b in self.b]
        self.t = 0

    def forward(self, X):
        acts = [X]
        h = X
        n = len(self.W)
        for i in range(n):
            z = h @ self.W[i] + self.b[i]
            if i < n - 1:
                h = np.maximum(z, 0.0)
            else:
                h = 1.0 / (1.0 + np.exp(-np.clip(z, -30.0, 30.0)))
            acts.append(h)
        return acts

    def loss(self, X, y):
        p = self.forward(X)[-1][:, 0]
        p = np.clip(p, 1e-9, 1 - 1e-9)
        return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))

    def train(self, X, y, steps=2000, batch=128, lr=1e-3):
        n = X.shape[0]
        for _ in range(steps):
            idx = self.rng.integers(0, n, size=batch)
            acts = self.forward(X[idx])
            out = acts[-1]
            yb = y[idx][:, None]
            dz = (out - yb) / batch
            gW = [None] * len(self.W)
            gb = [None] * len(self.b)
            for i in range(len(self.W) - 1, -1, -1):
                gW[i] = acts[i].T @ dz
                gb[i] = dz.sum(axis=0)
                if i > 0:
                    dz = (dz @ self.W[i].T) * (acts[i] > 0)
            self.t += 1
            b1, b2, eps = 0.9, 0.999, 1e-8
            for lst, grads, ms, vs in ((self.W, gW, self.mW, self.vW),
                                       (self.b, gb, self.mb, self.vb)):
                for i in range(len(lst)):
                    ms[i] = b1 * ms[i] + (1 - b1) * grads[i]
                    vs[i] = b2 * vs[i] + (1 - b2) * grads[i] ** 2
                    mh = ms[i] / (1 - b1 ** self.t)
                    vh = vs[i] / (1 - b2 ** self.t)
                    lst[i] -= lr * mh / (np.sqrt(vh) + eps)


def run_mlp_cell(q1n, q2n, q1c, q2c, model_rng, shuffled):
    out = {}
    for pipe, ffun, tag in (("A", features_A, 3), ("B", features_B, 4)):
        rng = np.random.default_rng(model_rng + (tag - 3))  # +0 for A, +1 for B
        X = np.concatenate([ffun(q1n, q2n), ffun(q1c, q2c)], axis=0)
        n = X.shape[0]
        y = np.concatenate([np.zeros(n // 2), np.ones(n // 2)])
        if shuffled:
            y = rng.permutation(y)
        idx = rng.permutation(n)
        tr, te = idx[: int(0.8 * n)], idx[int(0.8 * n):]
        mu = X[tr].mean(axis=0)
        sd = X[tr].std(axis=0)
        sd = np.where(sd < 1e-12, 1.0, sd)
        Xs = (X - mu) / sd
        mlp = MLP([X.shape[1], 64, 64, 64, 1], rng)
        mlp.train(Xs[tr], y[tr])
        scores = mlp.forward(Xs[te])[-1][:, 0]
        out[pipe] = auroc(scores[y[te] == 1], scores[y[te] == 0])
    return out


# ---------------------------------------------------------------- arm 3 detectors

def coherence_scores(d1, d2):
    n, T, _ = d1.shape
    seg = T // 4

    def welch_pair(z1, z2):
        a = z1.reshape(n, 4, seg)
        b = z2.reshape(n, 4, seg)
        A = np.fft.fft(a, axis=-1)
        B = np.fft.fft(b, axis=-1)
        S12 = np.mean(A * np.conj(B), axis=1)
        S11 = np.mean(np.abs(A) ** 2, axis=1)
        S22 = np.mean(np.abs(B) ** 2, axis=1)
        coh = np.abs(S12) ** 2 / (S11 * S22 + 1e-18)
        return coh.max(axis=1)

    za1 = d1[:, :, 0] + 1j * d1[:, :, 1]
    za2 = d2[:, :, 0] + 1j * d2[:, :, 1]
    zb1 = d1[:, :, 2] + 1j * d1[:, :, 3]
    zb2 = d2[:, :, 2] + 1j * d2[:, :, 3]
    return 0.5 * (welch_pair(za1, za2) + welch_pair(zb1, zb2))


def quat_corr_scores(d1, d2):
    # amended primary detector B (PREREG addendum a): unnormalized quadratic
    # quaternion correlation plus squared commutator (the ordering term)
    dot = np.sum(d1 * d2, axis=-1)
    comm = qmul(d1, d2) - qmul(d2, d1)
    cn = np.sum(comm * comm, axis=-1)
    return (dot ** 2 + cn).mean(axis=-1)


def quat_corr_norm_scores(d1, d2):
    # former primary, demoted to diagnostic (PREREG addendum a)
    dot = np.sum(d1 * d2, axis=-1)
    n1 = np.sum(d1 * d1, axis=-1)
    n2 = np.sum(d2 * d2, axis=-1)
    return (dot ** 2 / (n1 * n2 + 1e-12)).mean(axis=-1)


def commutator_scores(d1, d2):
    comm = qmul(d1, d2) - qmul(d2, d1)
    return np.linalg.norm(comm, axis=-1).mean(axis=-1)


# ---------------------------------------------------------------- arm 1

def _arm1_core():
    # shared core for arm 1 and its supplementary analysis (identical rng path)
    rng = np.random.default_rng(42)
    pitches = np.linspace(-np.pi / 2, np.pi / 2, 202)[1:-1]
    S = 200
    N = len(pitches) * S
    theta0 = np.repeat(pitches, S)
    L = rng.integers(10, 1001, size=N)
    sig_w = 0.01

    qT = euler_to_q(np.zeros(N), theta0, np.zeros(N))
    qB = qT.copy()
    eul = np.stack([np.zeros(N), theta0.copy(), np.zeros(N)], axis=1)

    errA = np.full(N, np.nan)
    errB = np.full(N, np.nan)
    maxT = 1000

    for t in range(maxT):
        w = rng.standard_normal((N, 3)) * sig_w
        # TRUTH: exact exponential map of the per-step constant body rate
        qT = qnormalize(qmul(qT, qexp_rot(w)))
        # Pipeline B: first-order quaternion integrator with renormalization
        omega = np.concatenate([np.zeros((N, 1)), w], axis=1)
        qB = qnormalize(qB + 0.5 * qmul(qB, omega))
        # Pipeline A: Euler 3-2-1 rate transform, forward Euler
        psi, th, phi = eul[:, 0].copy(), eul[:, 1].copy(), eul[:, 2].copy()
        p, q_, r = w[:, 0], w[:, 1], w[:, 2]
        cth = np.cos(th)
        cth = np.sign(cth) * np.maximum(np.abs(cth), 1e-12)
        psidot = (q_ * np.sin(phi) + r * np.cos(phi)) / cth
        thetadot = q_ * np.cos(phi) - r * np.sin(phi)
        phidot = p + psidot * np.sin(th)
        eul[:, 0] = psi + psidot
        eul[:, 1] = th + thetadot
        eul[:, 2] = phi + phidot
        done = t == (L - 1)
        if np.any(done):
            RT = q_to_R(qT[done])
            RA = euler_to_R(eul[done, 0], eul[done, 1], eul[done, 2])
            RB = q_to_R(qB[done])
            errA[done] = geodesic_angle(RT, RA)
            errB[done] = geodesic_angle(RT, RB)
    return errA, errB, theta0, L


def run_arm1(rows):
    t0 = time.time()
    errA, errB, theta0, L = _arm1_core()
    N = len(theta0)
    band = np.abs(theta0) >= (np.pi / 2 - 0.1)
    off = np.abs(theta0) <= (np.pi / 2 - 0.3)

    def med(e, m):
        return float(np.nanmedian(e[m]))

    mA_b, mA_o = med(errA, band), med(errA, off)
    mB_b, mB_o = med(errB, band), med(errB, off)
    row = {
        "arm": 1,
        "type": "summary",
        "seed": 42,
        "n_streams": int(N),
        "n_band": int(band.sum()),
        "n_off": int(off.sum()),
        "median_err_A_band_rad": round(mA_b, 6),
        "median_err_A_off_rad": round(mA_o, 6),
        "median_err_B_band_rad": round(mB_b, 6),
        "median_err_B_off_rad": round(mB_o, 6),
        "ratio_A_band_over_off": round(mA_b / mA_o, 3),
        "ratio_B_band_over_off": round(mB_b / mB_o, 3),
        "ratio_A_over_B_band": round(mA_b / mB_b, 3),
        "frac_A_err_gt_pi4_band": round(float(np.mean(errA[band] > np.pi / 4)), 4),
        "frac_B_err_gt_pi4_band": round(float(np.mean(errB[band] > np.pi / 4)), 4),
        "nan_A": int(np.isnan(errA).sum()),
        "nan_B": int(np.isnan(errB).sum()),
        "seconds": round(time.time() - t0, 1),
    }
    row["gate_pass"] = bool(row["ratio_A_band_over_off"] > 10 and row["ratio_A_over_B_band"] > 10)
    rows.append(row)
    return row


# ---------------------------------------------------------------- arm 1 supplementary (addendum 2)

def run_arm1b(rows):
    # binned re-analysis of the identical seed-42 data (PREREG addendum 2):
    # bins of d = pi/2 - |theta0| over [0.0078,0.05), [0.05,0.1), [0.1,0.3), [0.3,pi/2)
    t0 = time.time()
    errA, errB, theta0, L = _arm1_core()
    d = np.pi / 2 - np.abs(theta0)
    edges = [0.0, 0.05, 0.1, 0.3, np.pi / 2]
    labels = ["d_lt_0.05", "d_0.05_to_0.1", "d_0.1_to_0.3", "d_ge_0.3"]
    medA, medB = [], []
    row = {"arm": 1, "type": "supplementary_binned", "seed": 42}
    for i in range(4):
        if i < 3:
            m = (d >= edges[i]) & (d < edges[i + 1])
        else:
            m = d >= edges[3]
        ma = float(np.nanmedian(errA[m]))
        mb = float(np.nanmedian(errB[m]))
        medA.append(ma)
        medB.append(mb)
        row[f"median_A_{labels[i]}_rad"] = round(ma, 6)
        row[f"median_B_{labels[i]}_rad"] = round(mb, 6)
        row[f"n_{labels[i]}"] = int(m.sum())
    row["A_over_B_closest_bin"] = round(medA[0] / medB[0], 3)
    row["B_flat_within_3x"] = bool(max(medB) / max(min(medB), 1e-12) < 3.0)
    row["A_monotone_toward_singularity"] = bool(medA[0] > medA[1] > medA[2] > medA[3])
    row["pass_in_substance"] = bool(
        row["A_monotone_toward_singularity"] and row["B_flat_within_3x"] and row["A_over_B_closest_bin"] >= 100
    )
    row["seconds"] = round(time.time() - t0, 1)
    rows.append(row)
    return row


# ---------------------------------------------------------------- arm 2

def run_arm2(rows):
    t0 = time.time()
    per_g = {g: {"A": [], "B": []} for g in G_LEVELS}
    for gi, g in enumerate(G_LEVELS):
        for seed in SEEDS:
            base = ARM2_BASE + 1000 * seed + 10 * gi
            q1n, q2n = gen_streams(np.random.default_rng(base + 1), 500, "null", g, 2)
            q1c, q2c = gen_streams(np.random.default_rng(base + 2), 500, "coupled", g, 2)
            res = run_mlp_cell(q1n, q2n, q1c, q2c, base + 3, shuffled=False)
            for pipe in ("A", "B"):
                rows.append({
                    "arm": 2, "type": "cell", "seed": seed, "g": g,
                    "pipeline": pipe, "auroc": round(res[pipe], 4),
                    "n_train": 800, "n_test": 200,
                })
                per_g[g][pipe].append(res[pipe])
        print(f"arm2 g={g}: A={[round(x,3) for x in per_g[g]['A']]} B={[round(x,3) for x in per_g[g]['B']]}", flush=True)

    # shuffled-label control at g = 0.60
    gi = G_LEVELS.index(0.60)
    shuf = {"A": [], "B": []}
    for seed in SEEDS:
        base = ARM2_BASE + 1000 * seed + 10 * gi
        q1n, q2n = gen_streams(np.random.default_rng(base + 5), 500, "null", 0.60, 2)
        q1c, q2c = gen_streams(np.random.default_rng(base + 6), 500, "coupled", 0.60, 2)
        res = run_mlp_cell(q1n, q2n, q1c, q2c, base + 11, shuffled=True)
        for pipe in ("A", "B"):
            shuf[pipe].append(res[pipe])
            rows.append({
                "arm": 2, "type": "shuffled_control", "seed": seed, "g": 0.60,
                "pipeline": pipe, "auroc": round(res[pipe], 4),
            })
        print(f"arm2 shuffled seed={seed}: {res}", flush=True)

    summaries = []
    for g in G_LEVELS:
        for pipe in ("A", "B"):
            m, lo, hi, seeds_vals = ci95(per_g[g][pipe])
            summaries.append({
                "arm": 2, "type": "cell_summary", "g": g, "pipeline": pipe,
                "auroc_mean": round(m, 4), "ci_lo": round(lo, 4), "ci_hi": round(hi, 4),
                "seeds": [round(x, 4) for x in seeds_vals],
            })
    for s in summaries:
        rows.append(s)
    for pipe in ("A", "B"):
        m, lo, hi, _ = ci95(shuf[pipe])
        rows.append({
            "arm": 2, "type": "shuffled_summary", "pipeline": pipe,
            "auroc_mean": round(m, 4), "ci_lo": round(lo, 4), "ci_hi": round(hi, 4),
            "seeds": [round(x, 4) for x in shuf[pipe]],
        })

    def get(g, pipe):
        for s in summaries:
            if s["g"] == g and s["pipeline"] == pipe:
                return s
        raise KeyError((g, pipe))

    a_chance = all(at_chance(get(g, "A")["auroc_mean"], get(g, "A")["ci_lo"], get(g, "A")["ci_hi"]) for g in G_LEVELS)
    b_top = get(0.60, "B")
    verdict = {
        "arm": 2, "type": "verdict",
        "A_at_chance_all_g": bool(a_chance),
        "A_strong_form_falsified": bool(any(get(g, "A")["ci_lo"] > 0.5 for g in G_LEVELS)),
        "B_at_chance_all_g": bool(all(at_chance(get(g, "B")["auroc_mean"], get(g, "B")["ci_lo"], get(g, "B")["ci_hi"]) for g in G_LEVELS)),
        "B_ci_lo_gt_half_at_g060": bool(b_top["ci_lo"] > 0.5),
        "construction_sanity_B_mean_g060": b_top["auroc_mean"],
        "construction_sanity_pass": bool(b_top["auroc_mean"] > 0.60),
    }
    if not verdict["construction_sanity_pass"]:
        verdict["verdict"] = "construction too weak"
    elif verdict["A_strong_form_falsified"]:
        verdict["verdict"] = "strong-form falsified"
    elif verdict["B_at_chance_all_g"]:
        verdict["verdict"] = "vacuous"
    elif a_chance and verdict["B_ci_lo_gt_half_at_g060"]:
        verdict["verdict"] = "doctrine-supported"
    else:
        verdict["verdict"] = "mixed (see per-g summaries)"
    for pipe in ("A", "B"):
        sm, slo, shi, _ = ci95(shuf[pipe])
        verdict[f"shuffled_control_{pipe}_covers_half"] = bool(at_chance(sm, slo, shi))
    verdict["seconds"] = round(time.time() - t0, 1)
    rows.append(verdict)
    return verdict


# ---------------------------------------------------------------- arm 3

def run_arm3(rows):
    t0 = time.time()
    per_g = {g: {"A_coh": [], "B_quat": []} for g in G_LEVELS}
    diag = {g: {"comm": [], "rawdot": [], "norm": []} for g in G_LEVELS}
    for gi, g in enumerate(G_LEVELS):
        for seed in SEEDS:
            base = ARM3_BASE + 1000 * seed + 10 * gi
            q1n, q2n = gen_streams(np.random.default_rng(base + 1), 500, "null", g, 3)
            q1c, q2c = gen_streams(np.random.default_rng(base + 2), 500, "coupled", g, 3)
            d1n, d2n = innovations(q1n, q2n)
            d1c, d2c = innovations(q1c, q2c)
            sa_n, sa_c = coherence_scores(d1n, d2n), coherence_scores(d1c, d2c)
            sb_n, sb_c = quat_corr_scores(d1n, d2n), quat_corr_scores(d1c, d2c)
            per_g[g]["A_coh"].append(auroc(sa_c, sa_n))
            per_g[g]["B_quat"].append(auroc(sb_c, sb_n))
            diag[g]["comm"].append(auroc(commutator_scores(d1c, d2c), commutator_scores(d1n, d2n)))
            diag[g]["norm"].append(auroc(quat_corr_norm_scores(d1c, d2c), quat_corr_norm_scores(d1n, d2n)))
            diag[g]["rawdot"].append(float(np.mean(np.sum(d1c * d2c, -1) ** 2) - np.mean(np.sum(d1n * d2n, -1) ** 2)))
            rows.append({"arm": 3, "type": "cell", "seed": seed, "g": g, "detector": "A_coh",
                         "auroc": round(per_g[g]["A_coh"][-1], 4)})
            rows.append({"arm": 3, "type": "cell", "seed": seed, "g": g, "detector": "B_quat",
                         "auroc": round(per_g[g]["B_quat"][-1], 4)})
        print(f"arm3 g={g}: A={[round(x,3) for x in per_g[g]['A_coh']]} B={[round(x,3) for x in per_g[g]['B_quat']]}", flush=True)

    # construction sanity at g = 0.60 on 20000 fresh streams (amended seeds, addendum b)
    rng_n = np.random.default_rng(3_900_000_011)
    rng_c = np.random.default_rng(3_900_000_012)
    q1n, q2n = gen_streams(rng_n, 10000, "null", 0.60, 3)
    q1c, q2c = gen_streams(rng_c, 10000, "coupled", 0.60, 3)
    d1n, d2n = innovations(q1n, q2n)
    d1c, d2c = innovations(q1c, q2c)

    def shift(sn, sc):
        mn, mc = float(np.mean(sn)), float(np.mean(sc))
        vn, vc = float(np.var(sn)), float(np.var(sc))
        se = math.sqrt(vn / len(sn) + vc / len(sc))
        return mn, mc, abs(mc - mn) / se if se > 0 else float("inf")

    an, ac, az = shift(coherence_scores(d1n, d2n), coherence_scores(d1c, d2c))
    bn, bc, bz = shift(quat_corr_scores(d1n, d2n), quat_corr_scores(d1c, d2c))
    nn, nc, nz = shift(quat_corr_norm_scores(d1n, d2n), quat_corr_norm_scores(d1c, d2c))
    sanity = {
        "arm": 3, "type": "construction_sanity",
        "n_per_condition": 10000, "g": 0.60,
        "A_coh_mean_null": round(an, 6), "A_coh_mean_coupled": round(ac, 6),
        "A_coh_shift_in_pooled_SE": round(az, 2),
        "B_quat_mean_null": round(bn, 6), "B_quat_mean_coupled": round(bc, 6),
        "B_quat_shift_in_pooled_SE": round(bz, 2),
        "B_quat_norm_mean_null": round(nn, 6), "B_quat_norm_mean_coupled": round(nc, 6),
        "B_quat_norm_shift_in_pooled_SE": round(nz, 2),
        "B_sanity_pass_gt5SE": bool(bz > 5.0),
    }
    rows.append(sanity)

    summaries = []
    for g in G_LEVELS:
        for det in ("A_coh", "B_quat"):
            m, lo, hi, seeds_vals = ci95(per_g[g][det])
            summaries.append({
                "arm": 3, "type": "cell_summary", "g": g, "detector": det,
                "auroc_mean": round(m, 4), "ci_lo": round(lo, 4), "ci_hi": round(hi, 4),
                "seeds": [round(x, 4) for x in seeds_vals],
            })
        m, lo, hi, _ = ci95(diag[g]["comm"])
        rows.append({"arm": 3, "type": "diagnostic_comm", "g": g,
                     "auroc_mean": round(m, 4), "ci_lo": round(lo, 4), "ci_hi": round(hi, 4)})
        m, lo, hi, _ = ci95(diag[g]["norm"])
        rows.append({"arm": 3, "type": "diagnostic_norm_former_primary", "g": g,
                     "auroc_mean": round(m, 4), "ci_lo": round(lo, 4), "ci_hi": round(hi, 4)})
        rows.append({"arm": 3, "type": "diagnostic_rawdot_shift", "g": g,
                     "mean_shift": round(float(np.mean(diag[g]["rawdot"])), 8)})
    for s in summaries:
        rows.append(s)

    def get(g, det):
        for s in summaries:
            if s["g"] == g and s["detector"] == det:
                return s
        raise KeyError((g, det))

    a_chance = all(at_chance(get(g, "A_coh")["auroc_mean"], get(g, "A_coh")["ci_lo"], get(g, "A_coh")["ci_hi"]) for g in G_LEVELS)
    b_top = get(0.60, "B_quat")
    verdict = {
        "arm": 3, "type": "verdict",
        "A_at_chance_all_g": bool(a_chance),
        "A_coherence_leak": bool(any(get(g, "A_coh")["ci_lo"] > 0.5 for g in G_LEVELS)),
        "B_at_chance_all_g": bool(all(at_chance(get(g, "B_quat")["auroc_mean"], get(g, "B_quat")["ci_lo"], get(g, "B_quat")["ci_hi"]) for g in G_LEVELS)),
        "B_ci_lo_gt_half_at_g060": bool(b_top["ci_lo"] > 0.5),
    }
    if not sanity["B_sanity_pass_gt5SE"]:
        verdict["verdict"] = "construction too weak (B sanity shift below 5 SE)"
    elif verdict["A_coherence_leak"]:
        verdict["verdict"] = "coherence leak: projections retain higher-order signal"
    elif verdict["B_at_chance_all_g"]:
        verdict["verdict"] = "vacuous"
    elif a_chance and verdict["B_ci_lo_gt_half_at_g060"]:
        verdict["verdict"] = "doctrine-supported"
    else:
        verdict["verdict"] = "mixed (see per-g summaries)"
    verdict["seconds"] = round(time.time() - t0, 1)
    rows.append(verdict)
    return verdict


# ---------------------------------------------------------------- smoke test (no writes)

def run_smoke():
    print("smoke: arm1 mini")
    rng = np.random.default_rng(42)
    pitches = np.linspace(-np.pi / 2, np.pi / 2, 12)[1:-1]
    S = 20
    N = len(pitches) * S
    theta0 = np.repeat(pitches, S)
    L = rng.integers(10, 61, size=N)
    qT = euler_to_q(np.zeros(N), theta0, np.zeros(N))
    qB = qT.copy()
    eul = np.stack([np.zeros(N), theta0.copy(), np.zeros(N)], axis=1)
    errA = np.full(N, np.nan)
    errB = np.full(N, np.nan)
    for t in range(60):
        w = rng.standard_normal((N, 3)) * 0.01
        qT = qnormalize(qmul(qT, qexp_rot(w)))
        omega = np.concatenate([np.zeros((N, 1)), w], axis=1)
        qB = qnormalize(qB + 0.5 * qmul(qB, omega))
        th = eul[:, 1]
        cth = np.sign(np.cos(th)) * np.maximum(np.abs(np.cos(th)), 1e-12)
        psidot = (w[:, 1] * np.sin(eul[:, 2]) + w[:, 2] * np.cos(eul[:, 2])) / cth
        eul[:, 0] += psidot
        eul[:, 1] += w[:, 1] * np.cos(eul[:, 2]) - w[:, 2] * np.sin(eul[:, 2])
        eul[:, 2] += w[:, 0] + psidot * np.sin(th)
        done = t == (L - 1)
        if np.any(done):
            errA[done] = geodesic_angle(q_to_R(qT[done]), euler_to_R(eul[done, 0], eul[done, 1], eul[done, 2]))
            errB[done] = geodesic_angle(q_to_R(qT[done]), q_to_R(qB[done]))
    print("smoke arm1 medians:", float(np.nanmedian(errA)), float(np.nanmedian(errB)))

    print("smoke: arm2 mini (g=0.6, 1 seed, 200 steps)")
    base = ARM2_BASE + 1000 * 1000 + 10 * 4
    q1n, q2n = gen_streams(np.random.default_rng(base + 1), 100, "null", 0.60, 2)
    q1c, q2c = gen_streams(np.random.default_rng(base + 2), 100, "coupled", 0.60, 2)
    XA, XB = features_A(q1n, q2n), features_B(q1n, q2n)
    print("smoke feature dims A,B:", XA.shape, XB.shape)
    X = np.concatenate([features_B(q1n, q2n), features_B(q1c, q2c)], axis=0)
    y = np.concatenate([np.zeros(100), np.ones(100)])
    rng_m = np.random.default_rng(base + 3)
    mlp = MLP([X.shape[1], 64, 64, 64, 1], rng_m)
    l0 = mlp.loss(X, y)
    mlp.train(X, y, steps=200)
    l1 = mlp.loss(X, y)
    print("smoke mlp loss", round(l0, 4), "->", round(l1, 4))
    assert l1 < l0, "MLP training failed to reduce loss"

    print("smoke: arm3 mini")
    q1n, q2n = gen_streams(np.random.default_rng(3_000_000_001), 200, "null", 0.60, 3)
    q1c, q2c = gen_streams(np.random.default_rng(3_000_000_002), 200, "coupled", 0.60, 3)
    d1n, d2n = innovations(q1n, q2n)
    d1c, d2c = innovations(q1c, q2c)
    print("smoke auroc A_coh:", round(auroc(coherence_scores(d1c, d2c), coherence_scores(d1n, d2n)), 3))
    print("smoke auroc B_quat:", round(auroc(quat_corr_scores(d1c, d2c), quat_corr_scores(d1n, d2n)), 3))
    print("smoke OK (no files written)")


# ---------------------------------------------------------------- output plumbing

def emit(rows, arm_label):
    now = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    env_row = {
        "type": "env", "arm_run": arm_label, "timestamp": now,
        "python": platform.python_version(), "numpy": np.__version__,
    }
    all_rows = [env_row] + rows
    with open(RESULTS_PATH, "a", encoding="utf-8") as f:
        for r in all_rows:
            f.write(json.dumps(r) + "\n")
    block = [f"\n### Arm run {arm_label} (appended {now}, by residue_probe.py)\n"]
    for r in rows:
        block.append("`" + json.dumps(r) + "`\n")
    with open(PREREG, "a", encoding="utf-8") as f:
        f.write("\n".join(block) + "\n")
    for r in all_rows:
        print(json.dumps(r))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", default="all", choices=["1", "1b", "2", "3", "all", "smoke"])
    args = ap.parse_args()
    if args.arm == "smoke":
        run_smoke()
        return
    rows = []
    if args.arm in ("1", "all"):
        run_arm1(rows)
        emit(rows, "1")
        rows = []
    if args.arm == "1b":
        run_arm1b(rows)
        emit(rows, "1b")
    if args.arm in ("2", "all"):
        v = run_arm2(rows)
        emit(rows, "2")
        rows = []
    if args.arm in ("3", "all"):
        v = run_arm3(rows)
        emit(rows, "3")


if __name__ == "__main__":
    main()
