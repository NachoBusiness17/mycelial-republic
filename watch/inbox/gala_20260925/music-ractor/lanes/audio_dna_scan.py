"""
audio-dna lane (GALA music-ractor, division B): numeric style profile of a music folder.

Deterministic, $0, all local. No listening, no network, no ML models.

Pipeline:
  1. Enumerate audio files in FOLDER (sorted for determinism).
  2. ffprobe EVERY file: duration_s, bitrate_kbps, artist/title tags (CREATE_NO_WINDOW).
  3. Stratified sample: round-robin across artists (artist asc, title asc), take N_SAMPLE.
  4. Per sampled track: ffmpeg decode first DECODE_SECONDS to {SR} Hz mono s16le PCM,
     piped into numpy. Metrics:
       rms_dbfs     - 20*log10(sqrt(mean(x^2))) loudness proxy
       crest_db     - 20*log10(peak/rms) dynamic-range proxy
       zcr_hz       - zero crossings per second (brightness proxy)
       low_ratio    - spectral power 20-{LOW_HZ} Hz over 20-4000 Hz (low-end energy ratio)
       bpm          - onset-envelope autocorrelation peak in {BPM_MIN}-{BPM_MAX} BPM
       bpm_conf     - ACF peak / lag-0 (0..1, weak < 0.2 flagged)
  5. Folder MEDIAN + spread (p25/p75/min/max) per metric -> audio_dna.json
  6. Per-track markdown table + receipt -> audio-dna.md

Run with this repo's venv python only.
"""
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np

FFPROBE = (r"C:\Users\foste\AppData\Local\Microsoft\WinGet\Packages"
           r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
           r"\ffmpeg-8.1.2-full_build\bin\ffprobe.exe")
FFMPEG = (r"C:\Users\foste\AppData\Local\Microsoft\WinGet\Packages"
          r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
          r"\ffmpeg-8.1.2-full_build\bin\ffmpeg.exe")

FOLDER = Path(r"C:\Users\foste\Desktop\music-ai")
OUT_DIR = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\music")
AUDIO_EXTS = {".mp3", ".m4a", ".flac", ".wav", ".ogg", ".opus", ".wma"}

N_SAMPLE = 30
DECODE_SECONDS = 90
SR = 8000
BPM_MIN, BPM_MAX = 60, 180
LOW_HZ = 150

ENV_HOP_MS = 5.0          # onset-envelope frame hop
ENV_WIN_MS = 50.0         # rms window inside envelope
FFT_N = 2048              # welch frame for low_ratio
MIN_DECODE_S = 30.0       # below this: no bpm claim


def probe(path: Path):
    """ffprobe format json -> dict or raise."""
    cmd = [FFPROBE, "-v", "error", "-print_format", "json", "-show_format", str(path)]
    p = subprocess.run(cmd, capture_output=True, text=True,
                       creationflags=subprocess.CREATE_NO_WINDOW)
    if p.returncode != 0:
        raise RuntimeError(f"ffprobe rc={p.returncode}: {p.stderr.strip()[:200]}")
    fmt = json.loads(p.stdout)["format"]
    tags = fmt.get("tags") or {}
    # some muxers put tags only on stream 0; not handled here, format tags were
    # verified present on this folder's files (probed 1 file by hand first).
    dur = float(fmt["duration"]) if fmt.get("duration") else None
    br = int(fmt["bit_rate"]) if fmt.get("bit_rate") else None
    return {
        "path": str(path),
        "file": path.name,
        "artist": (tags.get("artist") or "").strip() or "(no artist tag)",
        "title": (tags.get("title") or "").strip() or path.stem,
        "duration_s": round(dur, 3) if dur is not None else None,
        "bitrate_kbps": round(br / 1000.0, 1) if br else None,
    }


def stratify(probes, n):
    """Round-robin one track per artist per round, artists asc, tracks asc."""
    by_artist = {}
    for p in probes:
        by_artist.setdefault(p["artist"], []).append(p)
    for a in by_artist:
        by_artist[a].sort(key=lambda p: p["file"].lower())
    artists = sorted(by_artist)
    picked, round_i = [], 0
    while len(picked) < n:
        took_any = False
        for a in artists:
            if round_i < len(by_artist[a]) and len(picked) < n:
                picked.append(by_artist[a][round_i])
                took_any = True
        if not took_any:
            break
        round_i += 1
    return picked, artists


def decode(path: Path) -> np.ndarray:
    """First DECODE_SECONDS -> float64 mono at SR in [-1, 1)."""
    cmd = [FFMPEG, "-hide_banner", "-loglevel", "error",
           "-t", str(DECODE_SECONDS), "-i", str(path),
           "-map", "0:a:0", "-ac", "1", "-ar", str(SR),
           "-f", "s16le", "-"]
    p = subprocess.run(cmd, capture_output=True,
                       creationflags=subprocess.CREATE_NO_WINDOW)
    if p.returncode != 0 or not p.stdout:
        raise RuntimeError(f"ffmpeg rc={p.returncode}: {p.stderr.decode(errors='replace')[:200]}")
    x = np.frombuffer(p.stdout, dtype=np.int16).astype(np.float64) / 32768.0
    return x


def metrics(x: np.ndarray):
    m = {}
    n = len(x)
    dur = n / SR
    m["decoded_s"] = round(dur, 2)
    if n < int(SR * 5) or np.max(np.abs(x)) < 1e-6:
        m["error"] = f"decoded {dur:.1f}s / near-silence: metrics skipped"
        return m

    rms = float(np.sqrt(np.mean(x * x)))
    peak = float(np.max(np.abs(x)))
    m["rms_dbfs"] = round(20 * math.log10(max(rms, 1e-12)), 2)
    m["crest_db"] = round(20 * math.log10(peak / max(rms, 1e-12)), 2)

    m["zcr_hz"] = round(float(np.count_nonzero(np.diff(np.signbit(x)))) / dur, 1)

    # low-end ratio: Welch average periodogram
    hop = FFT_N // 2
    frames = 1 + (n - FFT_N) // hop
    if frames > 0:
        win = np.hanning(FFT_N)
        idx = np.arange(FFT_N)[None, :] + hop * np.arange(frames)[:, None]
        seg = x[idx] * win[None, :]
        spec = np.abs(np.fft.rfft(seg, axis=1)) ** 2
        power = spec.mean(axis=0)
        freqs = np.fft.rfftfreq(FFT_N, d=1.0 / SR)
        low = power[(freqs >= 20) & (freqs < LOW_HZ)].sum()
        tot = power[(freqs >= 20) & (freqs < SR / 2)].sum()
        m["low_ratio"] = round(float(low / tot), 4) if tot > 0 else None
    else:
        m["low_ratio"] = None

    # onset envelope + autocorrelation BPM
    hop_e = int(SR * ENV_HOP_MS / 1000.0)          # 40 samples = 5 ms
    win_e = int(SR * ENV_WIN_MS / 1000.0)          # 400 samples = 50 ms
    n_frames = 1 + (n - win_e) // hop_e
    if n_frames >= 40:
        idx = np.arange(win_e)[None, :] + hop_e * np.arange(n_frames)[:, None]
        env = np.sqrt((x[idx] ** 2).mean(axis=1))   # rms envelope, rate = SR/hop_e
        sr_e = SR / hop_e
        onset = np.diff(env).clip(min=0.0)
        onset -= onset.mean()
        if onset.size > sr_e * 4:
            nfft = 1 << (2 * onset.size - 1).bit_length()
            S = np.fft.rfft(onset, nfft)
            acf = np.fft.irfft(S * np.conj(S), nfft)[:onset.size]
            acf /= max(acf[0], 1e-30)
            lag_lo = int(math.floor(60.0 * sr_e / BPM_MAX))
            lag_hi = int(math.ceil(60.0 * sr_e / BPM_MIN))
            if lag_hi < onset.size:
                seg = acf[lag_lo:lag_hi + 1]
                k = int(np.argmax(seg)) + lag_lo
                # parabolic interpolation for sub-lag bpm
                if 0 < k < onset.size - 1:
                    a, b, c = acf[k - 1], acf[k], acf[k + 1]
                    denom = a - 2 * b + c
                    delta = 0.5 * (a - c) / denom if abs(denom) > 1e-30 else 0.0
                    delta = float(np.clip(delta, -1.0, 1.0))
                else:
                    delta = 0.0
                m["bpm"] = round(60.0 * sr_e / (k + delta), 1)
                m["bpm_conf"] = round(float(b), 3)
        if "bpm" not in m:
            m["bpm"] = None
            m["bpm_conf"] = None
            m["bpm_note"] = "envelope too short for stable autocorrelation"
        if dur < MIN_DECODE_S:
            m["bpm_note"] = f"decoded only {dur:.1f}s (<{MIN_DECODE_S:.0f}s): bpm weak-evidence"
    else:
        m["bpm"] = None
        m["bpm_conf"] = None
        m["bpm_note"] = "track too short for onset envelope"
    return m


def spread(vals):
    vals = sorted(v for v in vals if v is not None)
    if not vals:
        return None
    a = np.array(vals, dtype=float)

    def pct(p):
        return round(float(np.percentile(a, p)), 4)
    return {"n": len(vals), "median": pct(50), "p25": pct(25), "p75": pct(75),
            "min": pct(0), "max": pct(100)}


def main():
    files = sorted([p for p in FOLDER.iterdir()
                    if p.is_file() and p.suffix.lower() in AUDIO_EXTS],
                   key=lambda p: p.name.lower())
    print(f"files in folder: {len(files)}")
    probes, probe_errors = [], []
    for f in files:
        try:
            probes.append(probe(f))
        except Exception as e:  # noqa: BLE001 - per-file resilience, error banked
            probe_errors.append({"file": f.name, "error": str(e)})
    print(f"probed ok: {len(probes)}  probe errors: {len(probe_errors)}")

    sample, artists = stratify(probes, N_SAMPLE)
    print(f"artists: {len(artists)}; sampled {len(sample)} tracks "
          f"round-robin across {len({s['artist'] for s in sample})} artists")

    tracks = []
    for i, pr in enumerate(sample):
        row = dict(pr)
        try:
            row.update(metrics(decode(Path(pr["path"]))))
        except Exception as e:  # noqa: BLE001
            row["error"] = str(e)
        tracks.append(row)
        done = sum(1 for t in tracks if "error" not in t or t.get("error") is None)
        print(f"[{i + 1}/{len(sample)}] {pr['file']} -> "
              f"{row.get('bpm')} bpm conf={row.get('bpm_conf')} "
              f"rms={row.get('rms_dbfs')} crest={row.get('crest_db')} "
              f"zcr={row.get('zcr_hz')} low={row.get('low_ratio')}"
              + (f" ERR {row.get('error')}" if row.get("error") else ""))

    prof = {}
    for k in ("duration_s", "bitrate_kbps", "rms_dbfs", "crest_db",
              "zcr_hz", "low_ratio", "bpm", "bpm_conf"):
        prof[k] = spread([t.get(k) for t in tracks])

    bpm_med = prof["bpm"]["median"] if prof["bpm"] else None
    doc = {
        "lane": "audio-dna",
        "generated": "gala_20260925 music-ractor division B",
        "folder": str(FOLDER),
        "method": {
            "probe": "ffprobe -show_format on every audio file",
            "decode": (f"ffmpeg -t {DECODE_SECONDS} -map 0:a:0 -ac 1 -ar {SR} "
                       f"-f s16le piped to numpy, CREATE_NO_WINDOW"),
            "sampling": (f"stratified round-robin across artist tags, {N_SAMPLE} tracks, "
                         "deterministic (artist asc, filename asc)"),
            "rms_dbfs": "20*log10(rms of full decoded window)",
            "crest_db": "20*log10(peak/rms)",
            "zcr_hz": "sign-change count per decoded second",
            "low_ratio": ("welch power 20-150 Hz over 20-4000 Hz, hann 2048 @8kHz, 50% hop"),
            "bpm": ("rms onset envelope (5ms hop), autocorrelation peak 60-180 BPM, "
                    "parabolic interp; bpm_conf = acf_peak/lag0"),
            "caveats": [
                "bpm is octave-ambiguous by construction (halving/doubling preserves the beat)",
                "bpm_conf < 0.2 = weak beat evidence, treat bpm as unproven for that track",
                "metrics are on the first 90 seconds only, loudness intros may bias rms low",
            ],
        },
        "folder_summary": {
            "audio_files_total": len(files),
            "probe_errors": probe_errors,
            "artist_count_tagged": len(artists),
            "artists_sampled_from": len({s["artist"] for s in sample}),
            "sampled": len(tracks),
        },
        "profile_median_spread": prof,
        "headline": {
            "bpm_median": bpm_med,
            "rms_dbfs_median": prof["rms_dbfs"]["median"] if prof["rms_dbfs"] else None,
            "low_ratio_median": prof["low_ratio"]["median"] if prof["low_ratio"] else None,
        },
        "tracks": tracks,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = OUT_DIR / "audio_dna.json"
    json_path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"wrote {json_path}")

    # markdown per-track table
    lines = [
        "# audio-dna: folder numeric style profile",
        "",
        f"Folder: `{FOLDER}` - {len(files)} audio files, {len(artists)} tagged artists. "
        f"Sampled {len(sample)} tracks, stratified round-robin across artists. "
        f"Every number below came from ffprobe/ffmpeg runs executed during this lane "
        f"(ffmpeg 8.1.2-full_build, numpy 2.4.6 on the repo venv).",
        "",
        "## Folder median (spread = p25 / p75, min / max)",
        "",
        "| metric | median | p25 | p75 | min | max | n |",
        "|---|---|---|---|---|---|---|",
    ]
    names = {"duration_s": "duration (s)", "bitrate_kbps": "bitrate (kbps)",
             "rms_dbfs": "RMS (dBFS)", "crest_db": "crest (dB)",
             "zcr_hz": "zero-crossings (/s)", "low_ratio": "low-end ratio (20-150Hz)",
             "bpm": "BPM", "bpm_conf": "BPM confidence"}
    for k in ("duration_s", "bitrate_kbps", "rms_dbfs", "crest_db",
              "zcr_hz", "low_ratio", "bpm", "bpm_conf"):
        s = prof[k]
        if s:
            lines.append(f"| {names[k]} | {s['median']} | {s['p25']} | {s['p75']} "
                         f"| {s['min']} | {s['max']} | {s['n']} |")
    lines += ["", "## Per-track table (sample)", "",
              "| # | file | artist | dur s | kbps | rms | crest | zcr/s | low | bpm | conf |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, t in enumerate(tracks):
        lines.append(
            f"| {i + 1} | {t['file']} | {t['artist']} | {t['duration_s']} "
            f"| {t['bitrate_kbps']} | {t.get('rms_dbfs', '')} | {t.get('crest_db', '')} "
            f"| {t.get('zcr_hz', '')} | {t.get('low_ratio', '')} "
            f"| {t.get('bpm', '')} | {t.get('bpm_conf', '')} |")
    lines += ["", "## Notes", ""]
    lines += [f"- {c}" for c in doc["method"]["caveats"]]
    md_path = OUT_DIR / "audio-dna.md"
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {md_path}")


if __name__ == "__main__":
    sys.exit(main())
