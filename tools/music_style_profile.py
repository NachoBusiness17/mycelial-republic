"""music_style_profile.py: the standing style engine behind the music-cut workflow.

Parameterized carry of the proven shared-recipe profiler from the music-ractor
gala run (watch/inbox/gala_20260925/music-ractor/lanes/style-synthesis.profile.py,
110/110 profiled 2026-10-01, receipt watch/inbox/music/STYLE_SPEC.md). Same
recipe, two changes: the corpus folder and output path are arguments (the gala
version hardcoded them), and the aggregates add the folded BPM law from
watch/inbox/music/audio-dna.md (fold raw BPM into [90,180) before comparing:
30 of 110 raw reads are half-time aliases, raw medians are octave-torn).

Recipe per file:
  ffprobe (duration, bitrate, sample rate) +
  ffmpeg 90s decode to 8000 Hz mono s16le ->
  numpy: RMS dBFS, peak dBFS, onset envelope autocorrelation 60-200 BPM
  (1x+2x harmonic sum, parabolic refine), zero-crossing rate, sub-160 Hz
  spectral power share, spectral centroid.

Usage:
  python tools/music_style_profile.py --folder C:/path/to/music --sample 12 --out out.json

Output JSON: {recipe, folder, files_total, sampled, files_profiled, files_failed,
aggregate (raw + folded BPM), bpm_bands, rows}. stdout prints a compact JSON
summary line for the caller to log.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"

DECODE_SECONDS = 90.0
SR = 8000
WIN = 512          # 64 ms window
HOP = 80           # 10 ms hop -> 100 fps
BPM_MIN, BPM_MAX = 60, 200
LOW_HZ = 160.0     # kick band ceiling; bin width 15.625 Hz -> bins 1..10

RECIPE = (
    "ffprobe + ffmpeg -t 90 -ac 1 -ar 8000 s16le -> numpy: rms_dbfs, peak_dbfs, "
    "zcr, onset-BPM (log-energy flux autocorr 60-200, 1x+2x harmonics, parabolic "
    "refine), low_share (<160Hz power fraction, frame median), centroid_hz; "
    "folded BPM = raw doubled into [90,180) per audio-dna.md octave law"
)


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
            lag_i = int(round(lag * mult))
            if lag_i <= 0 or lag_i >= n:
                continue
            score += float(np.dot(onset[: n - lag_i], onset[lag_i:]) / (n - lag_i))
        if score > best_score:
            best_score, best_bpm = score, float(bpm)
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


def fold_bpm(bpm: float) -> float:
    """Octave-fold a raw BPM read into [90,180) per the audio-dna.md law."""
    v = float(bpm)
    while v < 90.0:
        v *= 2.0
    while v >= 180.0:
        v /= 2.0
    return v


def agg(values: list) -> dict:
    v = np.array(values, dtype=float)
    return {"median": round(float(np.median(v)), 3),
            "p25": round(float(np.percentile(v, 25)), 3),
            "p75": round(float(np.percentile(v, 75)), 3),
            "min": round(float(v.min()), 3),
            "max": round(float(v.max()), 3)}


def main() -> int:
    ap = argparse.ArgumentParser(description="Profile a music folder's style DNA (proven music-ractor recipe, parameterized)")
    ap.add_argument("--folder", required=True, help="folder of audio files to profile")
    ap.add_argument("--sample", type=int, default=12, help="stride-sample this many files (0 = all)")
    ap.add_argument("--out", required=True, help="output JSON path")
    args = ap.parse_args()

    folder = Path(args.folder)
    if not folder.is_dir():
        print(json.dumps({"error": "folder not found: %s" % str(folder)}))
        return 2
    files = sorted(list(folder.glob("*.mp3")) + list(folder.glob("*.wav")) + list(folder.glob("*.flac")))
    if not files:
        print(json.dumps({"error": "no mp3/wav/flac files in %s" % str(folder)}))
        return 2
    sample_n = args.sample if args.sample and args.sample > 0 else len(files)
    if len(files) > sample_n:
        stride = len(files) / float(sample_n)
        picked = [files[int(i * stride)] for i in range(sample_n)]
    else:
        picked = files

    rows = []
    for i, f in enumerate(picked, 1):
        try:
            meta = ffprobe_meta(f)
            x = decode(f)
            m = metrics(x)
            rows.append({"file": f.name, **meta, **m})
            print("%3d/%d %6.1f BPM conf %5.2f  rms %6.1f  zcr %.3f  low %.3f  cen %4.0f  %s"
                  % (i, len(picked), m["bpm"], m["bpm_conf"], m["rms_dbfs"],
                     m["zcr"], m["low_share"], m["centroid_hz"], f.name[:52]),
                  flush=True)
        except Exception as e:  # noqa: BLE001 - profile rows must survive one bad file
            print("%3d/%d FAIL %s %s" % (i, len(picked), f.name[:52], e), flush=True)
            rows.append({"file": f.name, "error": str(e)[:200]})

    ok = [r for r in rows if "bpm" in r]
    if not ok:
        print(json.dumps({"error": "every sampled file failed to profile"}))
        return 1
    folded = [fold_bpm(r["bpm"]) for r in ok]
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
        "recipe": RECIPE,
        "folder": str(folder),
        "files_total": len(files),
        "sampled": len(picked),
        "files_profiled": len(ok),
        "files_failed": len(rows) - len(ok),
        "aggregate": {
            "rms_dbfs": agg([r["rms_dbfs"] for r in ok]),
            "peak_dbfs": agg([r["peak_dbfs"] for r in ok]),
            "zcr": agg([r["zcr"] for r in ok]),
            "bpm_raw": agg([r["bpm"] for r in ok]),
            "bpm_folded": agg(folded),
            "low_share": agg([r["low_share"] for r in ok]),
            "centroid_hz": agg([r["centroid_hz"] for r in ok]),
            "duration_s": agg([r["duration_s"] for r in ok if r.get("duration_s")]),
        },
        "bpm_bands": bands,
        "rows": rows,
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps({
        "files_total": out["files_total"], "sampled": out["sampled"],
        "files_profiled": out["files_profiled"], "files_failed": out["files_failed"],
        "bpm_folded_median": out["aggregate"]["bpm_folded"]["median"],
        "bpm_folded_p25": out["aggregate"]["bpm_folded"]["p25"],
        "bpm_folded_p75": out["aggregate"]["bpm_folded"]["p75"],
        "rms_median": out["aggregate"]["rms_dbfs"]["median"],
        "low_share_median": out["aggregate"]["low_share"]["median"],
        "centroid_median": out["aggregate"]["centroid_hz"]["median"],
        "out": str(out_path),
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
