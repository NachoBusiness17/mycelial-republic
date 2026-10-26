"""style-synthesis shared-recipe music profile.

Recipe (per the lane ask, shared with sibling lanes):
  ffprobe (duration, bitrate, sample rate) +
  ffmpeg 90s decode to 8000 Hz mono s16le ->
  numpy: RMS (dBFS), onset-BPM (rectified log-energy flux, autocorr 60-200,
         1x+2x harmonic sum, parabolic refine), ZCR, low-end share (<160 Hz
         spectral power fraction), spectral centroid.

Corpus: C:/Users/foste/Desktop/music-ai/*.mp3
Outputs:
  this dir / style-synthesis.profile.json   (per-track + aggregates)
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np

FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"
CORPUS = Path(r"C:/Users/foste/Desktop/music-ai")
OUT = Path(__file__).resolve().parent / "style-synthesis.profile.json"

DECODE_SECONDS = 90.0
SR = 8000
WIN = 512          # 64 ms window
HOP = 80           # 10 ms hop -> 100 fps
BPM_MIN, BPM_MAX = 60, 200
LOW_HZ = 160.0     # kick band ceiling; bin width 15.625 Hz -> bins 1..10


def ffprobe_meta(path: Path) -> dict:
    cmd = [
        FFPROBE, "-v", "error", "-select_streams", "a:0",
        "-show_entries", "stream=sample_rate,channels,bit_rate:format=duration,bit_rate",
        "-of", "json", str(path),
    ]
    raw = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    meta = json.loads(raw.stdout or "{}")
    stream = (meta.get("streams") or [{}])[0]
    fmt = meta.get("format") or {}
    def _f(v):
        try:
            return float(v)
        except (TypeError, ValueError):
            return None
    return {
        "sample_rate": int(stream.get("sample_rate") or 0) or None,
        "channels": int(stream.get("channels") or 0) or None,
        "duration_s": _f(fmt.get("duration")),
        "bitrate_kbps": round(_f(fmt.get("bit_rate")) / 1000.0, 0) if _f(fmt.get("bit_rate")) else None,
    }


def decode(path: Path) -> np.ndarray:
    cmd = [
        FFMPEG, "-v", "error", "-i", str(path),
        "-t", str(DECODE_SECONDS), "-ac", "1", "-ar", str(SR),
        "-f", "s16le", "-c:a", "pcm_s16le", "pipe:1",
    ]
    raw = subprocess.run(cmd, capture_output=True, timeout=120)
    x = np.frombuffer(raw.stdout, dtype=np.int16).astype(np.float32) / 32768.0
    return x


def stft_power(x: np.ndarray) -> np.ndarray:
    n_frames = 1 + (len(x) - WIN) // HOP
    idx = np.arange(WIN)[None, :] + HOP * np.arange(n_frames)[:, None]
    frames = x[idx] * np.hanning(WIN).astype(np.float32)
    spec = np.abs(np.fft.rfft(frames, axis=1)) ** 2  # power
    return spec


def metrics(x: np.ndarray) -> dict:
    x = x[: int(DECODE_SECONDS * SR)]
    if len(x) < SR * 10:
        raise ValueError("decoded only %.1fs" % (len(x) / SR))
    rms = float(np.sqrt(np.mean(x * x)))
    rms_dbfs = 20.0 * np.log10(max(rms, 1e-9))
    peak_dbfs = 20.0 * np.log10(max(float(np.max(np.abs(x))), 1e-9))

    signs = np.signbit(x)
    zcr = float(np.mean(signs[1:] != signs[:-1]))

    spec = stft_power(x)                       # [frames, 257]
    total = spec.sum(axis=1)                   # per-frame power
    e_db = 10.0 * np.log10(total + 1e-12)      # log-energy envelope
    flux = np.diff(e_db)
    onset = np.clip(flux, 0.0, None)           # rectified positive flux
    onset = onset - onset.mean()

    fps = SR / HOP                             # 100
    n = len(onset)
    best_score, best_bpm = -1.0, 0.0
    for bpm in range(BPM_MIN, BPM_MAX + 1):
        lag = fps * 60.0 / bpm
        score = 0.0
        for mult in (1, 2):
            l = int(round(lag * mult))
            if l <= 0 or l >= n:
                continue
            score += float(np.dot(onset[: n - l], onset[l:]) / (n - l))
        if score > best_score:
            best_score, best_bpm = score, float(bpm)
    lo_i, hi_i = int(best_bpm) - BPM_MIN, int(best_bpm) + 1 - BPM_MIN
    conf = best_score / (np.median(np.abs(onset)) + 1e-9)

    freqs = np.fft.rfftfreq(WIN, 1.0 / SR)     # 257 bins, 15.625 Hz step
    low_bins = (freqs > 0) & (freqs < LOW_HZ)  # bins 1..10
    share = spec[:, low_bins].sum(axis=1) / (total + 1e-12)
    low_share = float(np.median(share))

    mag = np.sqrt(spec) + 1e-9
    centroid = float(np.mean((mag * freqs[None, :]).sum(axis=1) / mag.sum(axis=1)))

    return {
        "rms_dbfs": round(rms_dbfs, 2),
        "peak_dbfs": round(peak_dbfs, 2),
        "zcr": round(zcr, 4),
        "bpm": round(best_bpm, 1),
        "bpm_conf": round(float(min(conf, 99.0)), 2),
        "low_share": round(low_share, 4),
        "centroid_hz": round(centroid, 0),
    }


def main() -> int:
    files = sorted(CORPUS.glob("*.mp3"))
    rows = []
    for i, f in enumerate(files, 1):
        try:
            meta = ffprobe_meta(f)
            x = decode(f)
            m = metrics(x)
            rows.append({"file": f.name, **meta, **m})
            print("%3d/%d %6.1f BPM conf %5.2f  rms %6.1f  zcr %.3f  low %.3f  cen %4.0f  %s"
                  % (i, len(files), m["bpm"], m["bpm_conf"], m["rms_dbfs"],
                     m["zcr"], m["low_share"], m["centroid_hz"], f.name[:52]),
                  flush=True)
        except Exception as e:
            print("%3d/%d FAIL %s %s" % (i, len(files), f.name[:52], e), flush=True)
            rows.append({"file": f.name, "error": str(e)[:200]})

    ok = [r for r in rows if "bpm" in r]
    def agg(key):
        v = np.array([r[key] for r in ok], dtype=float)
        return {"median": round(float(np.median(v)), 3),
                "p25": round(float(np.percentile(v, 25)), 3),
                "p75": round(float(np.percentile(v, 75)), 3),
                "min": round(float(v.min()), 3),
                "max": round(float(v.max()), 3)}
    bands = {"under90": 0, "b90_109": 0, "b110_129": 0, "b130_149": 0, "b150plus": 0,
             "halftime_60_79": 0}
    for r in ok:
        b = r["bpm"]
        if 60 <= b < 80:
            bands["halftime_60_79"] += 1
        if b < 90:
            bands["under90"] += 1
        elif b < 110:
            bands["b90_109"] += 1
        elif b < 130:
            bands["b110_129"] += 1
        elif b < 150:
            bands["b130_149"] += 1
        else:
            bands["b150plus"] += 1

    out = {
        "recipe": "ffprobe + ffmpeg -t 90 -ac 1 -ar 8000 s16le -> numpy: rms_dbfs, peak_dbfs, zcr, "
                  "onset-BPM (log-energy flux autocorr 60-200, 1x+2x harmonics, parabolic refine), "
                  "low_share (<160Hz power fraction, frame median), centroid_hz",
        "corpus": str(CORPUS),
        "files_total": len(files),
        "files_profiled": len(ok),
        "files_failed": len(rows) - len(ok),
        "aggregate": {k: agg(k) for k in
                      ("rms_dbfs", "peak_dbfs", "zcr", "bpm", "low_share", "centroid_hz")},
        "bpm_bands": bands,
        "rows": rows,
    }
    OUT.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps({"files_profiled": len(ok), "files_failed": len(rows) - len(ok),
                      "aggregate_bpm": out["aggregate"]["bpm"],
                      "aggregate_rms": out["aggregate"]["rms_dbfs"],
                      "aggregate_zcr": out["aggregate"]["zcr"],
                      "aggregate_low": out["aggregate"]["low_share"],
                      "aggregate_centroid": out["aggregate"]["centroid_hz"],
                      "bands": bands, "out": str(OUT)}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
