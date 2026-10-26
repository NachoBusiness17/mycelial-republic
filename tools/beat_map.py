"""beat_map - MAG DANCE layer 1: soundtrack -> beat grid (2026-10-04).

Operator vision (verbatim, 2026-10-04): "LETS MAKE MAG DANCE FR. IMAGINE OUR
SOUNDTRACK TEACHING YOU TO MAKE A SKELETON DANCE ... each model having an
examina [Exanima] style control scheme and literally have chunk physics and
damage mapped to the body."

Layers this tool seeds: (1) decode an estate track (ffmpeg -> mono f32 PCM),
(2) onset envelope = positive low-band + full-band energy flux (numpy), (3)
tempo by autocorrelation of the envelope, (4) beat grid phased on the
strongest onset, (5) per-beat strength + downbeat flag. Output JSON is the
CHOREOGRAPHY CONTRACT: anything that can read {t, strength, downbeat} can
dance - the dashboard skeleton (dashboard/static/mag_dance.html), the
Mountain's Ossuary Luau skeleton, or a future physics rig (the MuscleMimic
anchor: amathislab/musclemimic, Apache-2.0, Hill-muscle actuation - reference
model only, v0 needs no JAX).
Receipt: watch/inbox/MAG_DANCE_SPEC_20261004.md
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SR = 22050
HOP = 512


def decode_mono(path: Path) -> np.ndarray:
    """ffmpeg -> float32 mono PCM. Any input format ffmpeg reads."""
    raw = subprocess.run(
        ["ffmpeg", "-v", "quiet", "-i", str(path), "-ac", "1",
         "-ar", str(SR), "-f", "f32le", "-"],
        capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def onset_envelope(x: np.ndarray) -> np.ndarray:
    """Positive energy flux in dB-ish log domain, full band. hop = HOP."""
    n = 1 + len(x) // HOP
    frames = np.lib.stride_tricks.as_strided(
        x[: n * HOP], shape=(n - 1, HOP), strides=(HOP * 4, 4))
    rms = np.sqrt((frames.astype(np.float64) ** 2).mean(axis=1) + 1e-12)
    log_e = 20.0 * np.log10(rms + 1e-9)
    flux = np.diff(log_e, prepend=log_e[0])
    return np.maximum(flux, 0.0)


def estimate_bpm(env: np.ndarray, lo=80.0, hi=180.0) -> tuple[float, np.ndarray]:
    """Autocorrelate the onset envelope over lag range [lo, hi] BPM.

    v2 octave resolution (the v1 defect: one-way doubling bounded against
    lags[-1] = the SIGNAL LENGTH, not the tempo window, so a 90-BPM lock with
    a strong 2P correlation could report 45 BPM, below lo; and a half-tempo
    lock could never resolve up). v2 rule: candidates are b0/2, b0, b0*2
    clipped to the [lo, hi] window; each candidate is scored by the mean
    onset z-score over its own beat grid (the alignment test); walking from
    slowest to fastest, a faster candidate is adopted only while it keeps
    FAST_KEEP of the slower candidate's score. A true octave-up grid lands
    every beat on a real onset (score holds); a ghost octave-up drops half
    its beats into silence (score collapses below the keep ratio).
    """
    e = env - env.mean()
    ac = np.correlate(e, e, mode="full")[len(e) - 1:]
    ac /= (ac[0] + 1e-12)
    lags = np.arange(len(ac)) * HOP / SR
    mask = (lags >= 60.0 / hi) & (lags <= 60.0 / lo)
    if not mask.any():
        return 120.0, ac
    lag = lags[mask][np.argmax(ac[mask])]
    cands = sorted({b for b in (60.0 / lag / 2, 60.0 / lag, 60.0 / lag * 2)
                    if lo <= b <= hi})
    best = cands[0]
    best_score = _grid_score(env, best)
    for c in cands[1:]:
        s = _grid_score(env, c)
        if s >= FAST_KEEP * best_score:
            best, best_score = c, s
    return best, ac


FAST_KEEP = 0.7


def _grid_score(env: np.ndarray, bpm: float) -> float:
    """Mean onset z-score over the beat grid for bpm (same phasing as beat_grid)."""
    period = 60.0 / bpm * SR / HOP
    if period < 1.0:
        return 0.0
    peak = int(np.argmax(env))
    i0 = peak % int(round(period))
    mu, sd = env.mean(), env.std() + 1e-9
    n = int((len(env) - i0) // period)
    if n <= 0:
        return 0.0
    total = 0.0
    for k in range(n):
        idx = i0 + int(round(k * period))
        a, b = max(0, idx - 2), min(len(env), idx + 3)
        total += (env[a:b].max() - mu) / sd
    return total / n


def beat_grid(env: np.ndarray, bpm: float) -> list[dict]:
    """Phase the grid on the strongest onset; strength = local env z-score."""
    period = 60.0 / bpm * SR / HOP
    peak = int(np.argmax(env))
    beats, i = [], peak % int(round(period))
    span = max(env.max(), 1e-9)
    mu, sd = env.mean(), env.std() + 1e-9
    n = int((len(env) - i) // period)
    for k in range(n):
        idx = i + int(round(k * period))
        lo, hi = max(0, idx - 2), min(len(env), idx + 3)
        s = env[lo:hi].max()
        beats.append({"t": round(idx * HOP / SR, 4),
                      "strength": round(float(min((s - mu) / sd, 9.0)), 3),
                      "downbeat": k % 4 == 0})
    return beats


def grid_from_envelope(env: np.ndarray, bpm: float) -> list[dict]:
    """Pure seam for tests: grid over a synthetic envelope, no audio."""
    return beat_grid(env, bpm)


# zone keys match dashboard/static/mag_dance.html PARTS exactly
ZONES_HEAVY = ("head", "torso")
ZONES_LIMB = ("armL", "armR", "legL", "legR")


def damage_map(beats: list[dict]) -> list[dict]:
    """THE DAMAGE MAP CONTRACT (v0.2, 2026-10-04): the beat grid IS the combat
    round tick grid; every beat banks one hit on the skeleton - zone (which
    body part), hp (chunk damage), imp (impulse vector, magnitude = hp).

    Rules, deterministic by construction (dice-law discipline: outcomes live
    in the carrier, never in runtime chance - no RNG import, the golden-angle
    walk k*137.50776405 deg makes impulses unique-per-beat and
    rerun-byte-identical):
    - downbeat: heavy zone, alternating head/torso per measure ((k//4)%2),
      hp = 3 + int(clip(strength, 0, 9)) - the big round-opening hit
    - off-beat: limb rotation stepping one slot per measure ((k%4 + k//4)%4
      over armL, armR, legL, legR - plain k%4 would only ever reach 3 of the
      4 limbs because slot 0 is the downbeat; the measure-stepped rotation
      cycles all four), hp = 1 + int(clip(strength, 0, 9)) // 2 - the
      pitter-patter
    - imp direction = golden-angle walk, magnitude = hp (physics rig food;
      the MuscleMimic anchor consumes these when layer 3 grows a runtime)
    """
    rows = []
    for k, b in enumerate(beats):
        s = min(max(b["strength"], 0.0), 9.0)
        if b["downbeat"]:
            zone = ZONES_HEAVY[(k // 4) % 2]
            hp = 3 + int(s)
        else:
            zone = ZONES_LIMB[(k % 4 + k // 4) % 4]
            hp = 1 + int(s) // 2
        ang = ((k * 137.50776405) % 360.0) * math.pi / 180.0
        rows.append({"t": b["t"], "zone": zone, "hp": hp,
                     "imp": [round(hp * math.cos(ang), 3),
                             round(hp * math.sin(ang), 3)],
                     "downbeat": b["downbeat"],
                     "strength": b["strength"]})
    return rows


def build(track: Path) -> dict:
    x = decode_mono(track)
    env = onset_envelope(x)
    bpm, _ = estimate_bpm(env)
    beats = beat_grid(env, bpm)
    return {"track": track.name, "duration": round(len(x) / SR, 3),
            "bpm": round(bpm, 2), "sr": SR, "hop": HOP,
            "beats": beats, "n_beats": len(beats),
            "damage_map": damage_map(beats),
            "generator": "tools/beat_map.py v2 (onset-flux + autocorr tempo "
                         "+ window-bounded octave resolution + damage map)"}


def main() -> int:
    ap = argparse.ArgumentParser(prog="beat_map",
                                 description="estate track -> beat grid JSON")
    ap.add_argument("track", help="audio file path")
    ap.add_argument("--out", default=None, help="output JSON path")
    a = ap.parse_args(sys.argv[1:] if len(sys.argv) > 1 else None)
    track = Path(a.track)
    if not track.is_file():
        print(f"beat_map: no track at {track}")
        return 2
    m = build(track)
    out = Path(a.out) if a.out else track.with_suffix(".beats.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(m, indent=1), encoding="utf-8")
    print(f"beat_map: {track.name} -> {out} | {m['bpm']} bpm, "
          f"{m['n_beats']} beats over {m['duration']}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
