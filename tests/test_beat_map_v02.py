"""MAG DANCE v0.2 tests: window-bounded octave resolution + damage map contract.

v1 defect under test (2026-10-04): estimate_bpm preferred the double-period
when its autocorr was 0.75x the primary, bounded against lags[-1] = the SIGNAL
LENGTH, not the [lo, hi] tempo window - a 90-BPM lock with strong 2P
correlation could report 45 BPM, below lo, and a half-tempo lock could never
resolve up. v2: symmetric candidates b0/2, b0, b0*2 clipped to the window,
scored by mean onset z over each candidate's own grid, adopt-faster-only
while the faster keeps FAST_KEEP of the slower's score.
Receipt: watch/inbox/MAG_DANCE_V02_20261004.md
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import beat_map  # noqa: E402

FPS = beat_map.SR / beat_map.HOP  # envelope frame rate, ~43.07 fps


def click_env(n_seconds: float, hits: list[tuple[float, float]]) -> np.ndarray:
    """Synthetic onset envelope: (time_s, amp) spikes over a low floor."""
    n = int(n_seconds * FPS)
    env = np.full(n, 0.01)
    for t, amp in hits:
        env[int(t * FPS)] = amp
    return env


def metronome(n_seconds: float, period: float, amp=lambda k: 1.0) -> list[tuple[float, float]]:
    return [(k * period, amp(k)) for k in range(int(n_seconds / period))]


def test_octave_window_is_hard_bound():
    """90 BPM with accented every-other-beat: 2P sits at 45 BPM (below lo=80).
    Whatever the autocorr prefers, the answer must stay inside [lo, hi]."""
    env = click_env(20.0, metronome(20.0, 60.0 / 90.0, amp=lambda k: 1.3 if k % 2 == 0 else 1.0))
    bpm, _ = beat_map.estimate_bpm(env, lo=80.0, hi=180.0)
    assert 80.0 <= bpm <= 180.0, bpm


def test_half_tempo_lock_resolves_up():
    """Alternating accents 1.0 / 0.65 at true 120 BPM: the envelope is exactly
    2P-periodic, so the raw autocorr lock is 60 BPM. The 0.65 sub-onsets are
    real beats, so the 120 grid keeps >= FAST_KEEP of the 60 grid's score and
    must win."""
    env = click_env(20.0, metronome(20.0, 0.5, amp=lambda k: 1.0 if k % 2 == 0 else 0.65))
    bpm, _ = beat_map.estimate_bpm(env, lo=40.0, hi=180.0)
    assert 110.0 <= bpm <= 130.0, bpm


def test_ghost_octave_rejected():
    """True 60 BPM with faint 0.05-amp ghosts at the midpoints: doubling to 120
    would drop half the beats onto ghosts - score collapses, 60 must hold."""
    hits = metronome(20.0, 1.0, amp=lambda k: 1.0)
    hits += [(k * 1.0 + 0.5, 0.05) for k in range(19)]
    env = click_env(20.0, hits)
    bpm, _ = beat_map.estimate_bpm(env, lo=40.0, hi=180.0)
    assert 55.0 <= bpm <= 65.0, bpm


def test_damage_map_rules_and_determinism():
    beats = [{"t": round(k * 0.5, 4), "strength": min(1.0 + k * 0.4, 9.0),
              "downbeat": k % 4 == 0} for k in range(24)]
    rows = beat_map.damage_map(beats)
    assert len(rows) == len(beats)
    assert [r["t"] for r in rows] == [b["t"] for b in beats]
    for k, r in enumerate(rows):
        if r["downbeat"]:
            assert r["zone"] in ("head", "torso"), (k, r)
            # head on measures 0,2 ; torso on measures 1,3
            assert r["zone"] == ("head" if (k // 4) % 2 == 0 else "torso"), (k, r)
            assert r["hp"] == 3 + int(min(beats[k]["strength"], 9.0)), (k, r)
        else:
            # measure-stepped rotation reaches all 4 limbs (plain k%4 would
            # strand armL: slot 0 is always the downbeat)
            assert r["zone"] == beat_map.ZONES_LIMB[(k % 4 + k // 4) % 4], (k, r)
        mag = (r["imp"][0] ** 2 + r["imp"][1] ** 2) ** 0.5
        assert abs(mag - r["hp"]) < 0.01, (k, r)
    # no RNG: identical output on a second call, and per-beat angles distinct
    again = beat_map.damage_map(beats)
    assert rows == again
    angles = {(r["imp"][0], r["imp"][1]) for r in rows}
    assert len(angles) == 24
    # all 4 limbs + both heavy zones appear across 24 beats (6 measures)
    seen = {r["zone"] for r in rows}
    assert seen == {"head", "torso", "armL", "armR", "legL", "legR"}, seen


def test_damage_map_strength_clip():
    beats = [{"t": 0.0, "strength": -3.2, "downbeat": True},
             {"t": 0.5, "strength": 99.0, "downbeat": False}]
    rows = beat_map.damage_map(beats)
    assert rows[0]["hp"] == 3          # negative strength floors to 0
    assert rows[1]["hp"] == 1 + 9 // 2  # 9 is the clip ceiling


def test_build_shape_on_real_loop():
    """Integration: the flat_beat_loop.mp3 in the Suno library maps with the
    damage map present and aligned. Skipped when ffmpeg or the track is away."""
    import shutil
    import subprocess

    track = ROOT / "dashboard" / "static" / "suno" / "flat_beat_loop.mp3"
    if not track.is_file() or not shutil.which("ffmpeg"):
        import pytest

        pytest.skip("ffmpeg or flat_beat_loop.mp3 not present")
    m = beat_map.build(track)
    assert 80.0 <= m["bpm"] <= 180.0, m["bpm"]
    assert len(m["damage_map"]) == m["n_beats"]
    assert {r["zone"] for r in m["damage_map"]} <= {"head", "torso", "armL", "armR", "legL", "legR"}
    assert "v2" in m["generator"]
    # the two v1 seams still hold
    assert m["beats"][0]["downbeat"] is True
    _ = subprocess.run(["ffmpeg", "-v", "quiet", "-version"], capture_output=True)
