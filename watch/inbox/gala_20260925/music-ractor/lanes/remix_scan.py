# remix_scan.py - lane: remix-mechanics (division B), gala music-ractor
# Pairs every original with its remix(es) in C:/Users/foste/Desktop/music-ai and
# computes what the remix DOES: duration delta, energy delta, dynamics delta,
# spectral band deltas, BPM drift, onset(chop) rate delta.
#
# Recipe: SAME ffmpeg+numpy recipe as sibling lanes/audio_dna_scan.py
#   (ffmpeg decode -> 8000 Hz mono s16le -> numpy; rms_dbfs, crest_db, zcr_hz,
#    welch low_ratio 20-150 Hz over 20-4000 Hz hann-2048; rms onset envelope
#    5 ms hop -> autocorrelation BPM 60-180 with parabolic interp + conf).
# Delta vs sibling: pairs are decoded FULL LENGTH (audio-dna sampled first 90s)
# because the ask says sample the pairs fully.
#
# Writes watch/inbox/music/remix_mechanics.json (raw numbers) and prints the
# pair tables to stdout (caller redirects stdout to remix-mechanics.check.txt).
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
OUT_JSON = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent"
                r"\watch\inbox\music\remix_mechanics.json")

SR = 8000
BPM_MIN, BPM_MAX = 60, 180
LOW_HZ = 150
ENV_HOP_MS = 5.0
ENV_WIN_MS = 50.0
FFT_N = 2048
DYN_FRAME_S = 0.25          # window for dyn_range_db (frame RMS percentiles)

# (label, original file, remix file, class)
PAIRS = [
    ("Aerodynamic / Daft Punk Remix", "Aerodynamic_spotdown.org.mp3",
     "Aerodynamic - Daft Punk Remix_spotdown.org.mp3", "SELF-TAGGED"),
    ("Animal / Mark Ronson Remix", "Animal_spotdown.org.mp3",
     "Animal - Mark Ronson Remix_spotdown.org.mp3", "CROSS-ARTIST"),
    ("D.A.N.C.E. / MSTRKRFT Remix", "D.A.N.C.E._spotdown.org.mp3",
     "D.A.N.C.E. - MSTRKRFT Remix_spotdown.org.mp3", "CROSS-ARTIST"),
    ("NY Excuse / Justice Remix", "NY Excuse_spotdown.org.mp3",
     "NY Excuse - Justice Remi_spotdown.org.mp3", "CROSS-ARTIST"),
    ("Phantom Pt. II / Soulwax Remix", "Phantom Pt. II_spotdown.org.mp3",
     "Phantom Pt II - Soulwax Remix_spotdown.org.mp3", "CROSS-ARTIST"),
    ("Phantom Pt. II / Boys Noize Remix", "Phantom Pt. II_spotdown.org.mp3",
     "Phantom Pt II - Boys Noize Remix_spotdown.org.mp3", "CROSS-ARTIST"),
    ("Flat Beat / Radio Edit", "Flat Beat_spotdown.org.mp3",
     "Flat Beat - Radio Edit_spotdown.org.mp3", "SELF-VERSION"),
    ("Rez / Remastered", "Rez_spotdown.org.mp3",
     "Rez - Remastered_spotdown.org.mp3", "SELF-VERSION"),
    ("Psychic City Radio Edit / Classixx Remix",
     "Psychic City - Radio Edit_spotdown.org.mp3",
     "Psychic City - Classixx Remix_spotdown.org.mp3", "CROSS-ARTIST"),
    ("Time To Dance Extended / Sebastian Remix",
     "Time To Dance - Extended Version_spotdown.org.mp3",
     "Time To Dance - SebastiAn Remix_spotdown.org.mp3", "CROSS-ARTIST"),
]

# remix-class files with no in-folder original; measured for grammar breadth only
ORPHANS = [
    "Let It Happen - Soulwax Remix_spotdown.org.mp3",
    "What Moves - Soulwax Remix_spotdown.org.mp3",
    "Another Excuse - Dfa Remix_spotdown.org.mp3",
    "Paris - Aeroplane Remix_spotdown.org.mp3",
    "C-C (You Set The Fire In Me) - Dave Glass Animals Remix_spotdown.org.mp3",
    "Testarossa - SebastiAn Remix_spotdown.org.mp3",
    "The Hand That Feeds - Photek Straight Mix_spotdown.org.mp3",
    "We Are Your Friends - Justice Vs Simian_spotdown.org.mp3",
    "Signatune - Thomas Bangalter Short Edit_spotdown.org.mp3",
]


def probe(path: Path):
    cmd = [FFPROBE, "-v", "error", "-print_format", "json", "-show_format", str(path)]
    p = subprocess.run(cmd, capture_output=True, text=True,
                       creationflags=subprocess.CREATE_NO_WINDOW)
    if p.returncode != 0:
        raise RuntimeError(f"ffprobe rc={p.returncode}: {p.stderr.strip()[:200]}")
    fmt = json.loads(p.stdout)["format"]
    tags = fmt.get("tags") or {}
    dur = float(fmt["duration"]) if fmt.get("duration") else None
    br = int(fmt["bit_rate"]) if fmt.get("bit_rate") else None
    return {
        "duration_s": round(dur, 3) if dur is not None else None,
        "bitrate_kbps": round(br / 1000.0, 1) if br else None,
        "artist": (tags.get("artist") or "").strip() or "(no artist tag)",
        "title": (tags.get("title") or "").strip() or path.stem,
        "album": (tags.get("album") or "").strip() or "(no album tag)",
    }


def decode_full(path: Path) -> np.ndarray:
    """Whole file -> float64 mono at SR in [-1, 1)."""
    cmd = [FFMPEG, "-hide_banner", "-loglevel", "error", "-i", str(path),
           "-map", "0:a:0", "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"]
    p = subprocess.run(cmd, capture_output=True,
                       creationflags=subprocess.CREATE_NO_WINDOW)
    if p.returncode != 0 or not p.stdout:
        raise RuntimeError(f"ffmpeg rc={p.returncode}: "
                           f"{p.stderr.decode(errors='replace')[:200]}")
    return np.frombuffer(p.stdout, dtype=np.int16).astype(np.float64) / 32768.0


def band_ratio(power, freqs, lo, hi, tot):
    sel = (freqs >= lo) & (freqs < hi)
    return round(float(power[sel].sum() / tot), 4) if tot > 0 else None


def metrics(x: np.ndarray):
    m = {}
    n = len(x)
    dur = n / SR
    m["decoded_s"] = round(dur, 2)
    if n < SR * 5 or np.max(np.abs(x)) < 1e-6:
        m["error"] = f"decoded {dur:.1f}s / near-silence: metrics skipped"
        return m

    rms = float(np.sqrt(np.mean(x * x)))
    peak = float(np.max(np.abs(x)))
    m["rms_dbfs"] = round(20 * math.log10(max(rms, 1e-12)), 2)
    m["peak_dbfs"] = round(20 * math.log10(max(peak, 1e-12)), 2)
    m["crest_db"] = round(20 * math.log10(peak / max(rms, 1e-12)), 2)
    m["zcr_hz"] = round(float(np.count_nonzero(np.diff(np.signbit(x)))) / dur, 1)

    # welch average periodogram, hann 2048, 50 percent hop (same as audio-dna)
    hop = FFT_N // 2
    frames = 1 + (n - FFT_N) // hop
    if frames > 0:
        win = np.hanning(FFT_N)
        idx = np.arange(FFT_N)[None, :] + hop * np.arange(frames)[:, None]
        seg = x[idx] * win[None, :]
        spec = np.abs(np.fft.rfft(seg, axis=1)) ** 2
        power = spec.mean(axis=0)
        freqs = np.fft.rfftfreq(FFT_N, d=1.0 / SR)
        tot = power[(freqs >= 20) & (freqs < SR / 2)].sum()
        m["low_ratio"] = band_ratio(power, freqs, 20, LOW_HZ, tot)
        m["lowmid_ratio"] = band_ratio(power, freqs, LOW_HZ, 500, tot)
        m["mid_ratio"] = band_ratio(power, freqs, 500, 2000, tot)
        m["high_ratio"] = band_ratio(power, freqs, 2000, 4000, tot)
    else:
        for k in ("low_ratio", "lowmid_ratio", "mid_ratio", "high_ratio"):
            m[k] = None

    # dyn_range_db: p90-p10 of frame RMS in dB (250 ms frames, 50 percent hop)
    fw = int(SR * DYN_FRAME_S)
    fh = fw // 2
    fframes = 1 + (n - fw) // fh
    if fframes >= 8:
        fidx = np.arange(fw)[None, :] + fh * np.arange(fframes)[:, None]
        frms = np.sqrt((x[fidx] ** 2).mean(axis=1))
        fdb = 20 * np.log10(np.maximum(frms, 1e-12))
        m["dyn_range_db"] = round(float(np.percentile(fdb, 90)
                                        - np.percentile(fdb, 10)), 2)
    else:
        m["dyn_range_db"] = None

    # onset envelope + autocorrelation BPM (same as audio-dna, full length)
    hop_e = int(SR * ENV_HOP_MS / 1000.0)
    win_e = int(SR * ENV_WIN_MS / 1000.0)
    n_frames = 1 + (n - win_e) // hop_e
    if n_frames >= 40:
        idx = np.arange(win_e)[None, :] + hop_e * np.arange(n_frames)[:, None]
        env = np.sqrt((x[idx] ** 2).mean(axis=1))
        sr_e = SR / hop_e
        d = np.diff(env)
        pos = d.clip(min=0.0)
        # chop proxy: strong upward onsets per second
        thr = pos.mean() + 1.5 * pos.std()
        interior = pos[1:-1]
        peaks = (interior > thr) & (interior >= pos[:-2]) & (interior >= pos[2:])
        m["onset_rate"] = round(float(np.count_nonzero(peaks)) / dur, 3)

        onset = pos - pos.mean()
        nfft = 1 << (2 * onset.size - 1).bit_length()
        S = np.fft.rfft(onset, nfft)
        acf = np.fft.irfft(S * np.conj(S), nfft)[:onset.size]
        acf /= max(acf[0], 1e-30)
        lag_lo = int(math.floor(60.0 * sr_e / BPM_MAX))
        lag_hi = int(math.ceil(60.0 * sr_e / BPM_MIN))
        if lag_hi < onset.size:
            seg = acf[lag_lo:lag_hi + 1]
            k = int(np.argmax(seg)) + lag_lo
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
    if "onset_rate" not in m:
        m["onset_rate"] = None
    return m


def measure(path: Path):
    row = {"file": path.name}
    row.update(probe(path))
    row.update(metrics(decode_full(path)))
    return row


def fold_bpm(bpm_o, bpm_r):
    """Fold remix bpm into [0.75, 1.5] of original, report fold in octaves."""
    if not bpm_o or not bpm_r:
        return None, None
    r = bpm_r / bpm_o
    f, octaves = r, 0
    while f > 1.5:
        f /= 2.0
        octaves -= 1
    while f < 0.75:
        f *= 2.0
        octaves += 1
    return round(f, 3), octaves


def main():
    files = {}
    for _, fo, fr, cls in PAIRS:
        files[fo] = None
        files[fr] = None
    for fo in ORPHANS:
        files[fo] = None
    missing = [f for f in files if not (FOLDER / f).is_file()]
    if missing:
        print("MISSING FILES:")
        for f in missing:
            print(f"  {f}")
        sys.exit(2)

    print(f"corpus folder: {FOLDER}")
    print(f"pair files: {len(PAIRS) * 2 - 1} unique (Phantom Pt. II original shared)"
          f" + {len(ORPHANS)} orphan remixes = {len(files)} files, all decoded FULL LENGTH")
    print(f"recipe: ffmpeg -> {SR} Hz mono s16le -> numpy "
          f"(same as lanes/audio_dna_scan.py, full length instead of first 90s)")
    print()

    table = {}
    for i, name in enumerate(sorted(files)):
        p = FOLDER / name
        try:
            table[name] = measure(p)
            t = table[name]
            print(f"[{i + 1}/{len(files)}] {name}")
            print(f"    artist={t['artist']!r} album={t['album']!r}")
            print(f"    dur={t['duration_s']}s kbps={t['bitrate_kbps']} "
                  f"rms={t['rms_dbfs']}dBFS peak={t['peak_dbfs']}dBFS "
                  f"crest={t['crest_db']}dB dyn={t['dyn_range_db']}dB")
            print(f"    zcr={t['zcr_hz']}/s low={t['low_ratio']} "
                  f"lowmid={t['lowmid_ratio']} mid={t['mid_ratio']} "
                  f"high={t['high_ratio']}")
            print(f"    bpm={t['bpm']} conf={t['bpm_conf']} "
                  f"onset_rate={t['onset_rate']}/s")
        except Exception as e:  # noqa: BLE001 - bank the error, keep going
            table[name] = {"file": name, "error": str(e)}
            print(f"[{i + 1}/{len(files)}] {name} ERROR: {e}")
        print()

    print("=" * 100)
    print("PAIR DIFFS (remix minus original; positive = remix higher)")
    print("=" * 100)
    pair_rows = []
    for label, fo, fr, cls in PAIRS:
        o, r = table.get(fo, {}), table.get(fr, {})
        if any(k in o for k in ("error",)) or any(k in r for k in ("error",)) \
                or "duration_s" not in o or "duration_s" not in r:
            print(f"{label}: measurement error, pair skipped")
            pair_rows.append({"label": label, "class": cls, "error": "measurement error"})
            continue
        fold, octv = fold_bpm(o.get("bpm"), r.get("bpm"))
        row = {
            "label": label, "class": cls,
            "orig_file": fo, "remix_file": fr,
            "dur_delta_s": round(r["duration_s"] - o["duration_s"], 2),
            "dur_delta_pct": round(100 * (r["duration_s"] / o["duration_s"] - 1), 2),
            "rms_delta_db": round(r["rms_dbfs"] - o["rms_dbfs"], 2),
            "peak_delta_db": round(r["peak_dbfs"] - o["peak_dbfs"], 2),
            "crest_delta_db": round(r["crest_db"] - o["crest_db"], 2),
            "dyn_delta_db": (round(r["dyn_range_db"] - o["dyn_range_db"], 2)
                             if o.get("dyn_range_db") is not None
                             and r.get("dyn_range_db") is not None else None),
            "zcr_rel_pct": round(100 * (r["zcr_hz"] / o["zcr_hz"] - 1), 2),
            "low_rel_pct": (round(100 * (r["low_ratio"] / o["low_ratio"] - 1), 2)
                            if o["low_ratio"] and r["low_ratio"] else None),
            "mid_rel_pct": (round(100 * (r["mid_ratio"] / o["mid_ratio"] - 1), 2)
                            if o["mid_ratio"] and r["mid_ratio"] else None),
            "high_rel_pct": (round(100 * (r["high_ratio"] / o["high_ratio"] - 1), 2)
                             if o["high_ratio"] and r["high_ratio"] else None),
            "bpm_orig": o.get("bpm"), "bpm_remix": r.get("bpm"),
            "bpm_raw_ratio": (round(r["bpm"] / o["bpm"], 3)
                              if o.get("bpm") and r.get("bpm") else None),
            "bpm_folded_ratio": fold, "bpm_fold_octaves": octv,
            "bpm_conf_orig": o.get("bpm_conf"), "bpm_conf_remix": r.get("bpm_conf"),
            "onset_rel_pct": (round(100 * (r["onset_rate"] / o["onset_rate"] - 1), 2)
                              if o.get("onset_rate") and r.get("onset_rate") else None),
        }
        row["dup_suspect"] = bool(
            abs(row["dur_delta_s"]) <= 1.5
            and abs(row["rms_delta_db"]) <= 0.7
            and abs(row["zcr_rel_pct"]) <= 3.0)
        pair_rows.append(row)
        print(f"{label}  [{cls}]")
        print(f"    dur {o['duration_s']} -> {r['duration_s']} s "
              f"(delta {row['dur_delta_s']} s, {row['dur_delta_pct']}%)")
        print(f"    rms {o['rms_dbfs']} -> {r['rms_dbfs']} dBFS "
              f"(delta {row['rms_delta_db']} dB)   "
              f"crest {o['crest_db']} -> {r['crest_db']} dB "
              f"(delta {row['crest_delta_db']} dB)   "
              f"dyn {o.get('dyn_range_db')} -> {r.get('dyn_range_db')} dB "
              f"(delta {row['dyn_delta_db']} dB)")
        print(f"    zcr {o['zcr_hz']} -> {r['zcr_hz']}/s ({row['zcr_rel_pct']}% rel)   "
              f"low {o['low_ratio']} -> {r['low_ratio']} ({row['low_rel_pct']}% rel)   "
              f"mid {o['mid_ratio']} -> {r['mid_ratio']} ({row['mid_rel_pct']}% rel)   "
              f"high {o['high_ratio']} -> {r['high_ratio']} ({row['high_rel_pct']}% rel)")
        print(f"    bpm {o.get('bpm')} (conf {o.get('bpm_conf')}) -> "
              f"{r.get('bpm')} (conf {r.get('bpm_conf')})   "
              f"raw ratio {row['bpm_raw_ratio']}  folded {row['bpm_folded_ratio']} "
              f"({row['bpm_fold_octaves']} octaves)")
        print(f"    onset_rate {o.get('onset_rate')} -> {r.get('onset_rate')}/s "
              f"({row['onset_rel_pct']}% rel)"
              + ("   DUP-SUSPECT: same audio within measurement noise"
                 if row["dup_suspect"] else ""))
        print()

    # summary medians by class
    print("=" * 100)
    print("SUMMARY (median delta per pair class)")
    print("=" * 100)
    summary = {}

    def med(rs, key):
        vals = sorted(r[key] for r in rs if r.get(key) is not None)
        if not vals:
            return None
        a = np.array(vals, dtype=float)
        return {"median": round(float(np.median(a)), 2),
                "min": round(float(a.min()), 2), "max": round(float(a.max()), 2),
                "n": len(vals)}

    for cls in sorted({p[3] for p in PAIRS}):
        rs = [r for r in pair_rows if r.get("class") == cls and "error" not in r]
        if not rs:
            continue
        summary[cls] = {k: med(rs, k) for k in
                        ("dur_delta_pct", "rms_delta_db", "crest_delta_db",
                         "dyn_delta_db", "zcr_rel_pct", "low_rel_pct",
                         "mid_rel_pct", "high_rel_pct", "bpm_folded_ratio",
                         "onset_rel_pct")}
        print(f"{cls} ({len(rs)} pairs):")
        for k, v in summary[cls].items():
            print(f"    {k}: {v}")
        print()

    doc = {
        "lane": "remix-mechanics",
        "generated": "gala_20260925 music-ractor division B",
        "corpus": str(FOLDER),
        "method": {
            "decode": f"ffmpeg full file -> 1ch {SR} Hz s16le -> numpy float64",
            "rms_dbfs": "20*log10(rms of full decoded track)",
            "peak_dbfs": "20*log10(max |x|)",
            "crest_db": "20*log10(peak/rms)",
            "dyn_range_db": "p90-p10 of 250 ms frame RMS in dB",
            "zcr_hz": "sign changes per second",
            "low_ratio": "welch power 20-150 Hz over 20-4000 Hz (hann 2048 @8 kHz, 50% hop)",
            "lowmid_ratio": "150-500 Hz over 20-4000 Hz, same welch",
            "mid_ratio": "500-2000 Hz over 20-4000 Hz, same welch",
            "high_ratio": "2000-4000 Hz over 20-4000 Hz, same welch (Nyquist 4 kHz)",
            "bpm": "rms onset envelope 5 ms hop, autocorrelation 60-180 BPM, "
                   "parabolic interp, full track; conf = acf peak / lag0",
            "onset_rate": "upward onsets/s above mean+1.5std of positive envelope diff",
            "bpm_folded_ratio": "remix/orig bpm ratio folded by octaves into 0.75-1.5",
            "caveats": [
                "bpm is octave-ambiguous by construction; folded ratio + conf reported",
                "rms is loudness proxy, not LUFS; mastering variance rides on every delta",
                "Aerodynamic 'Daft Punk Remix' is tagged SELF-REMIX (album Daft Club); "
                "secondary sources commonly attribute the actual production to Soulwax; "
                "this lane reports tags and numbers, not lore",
                "dup_suspect = duration within 1.5 s AND rms within 0.7 dB AND zcr "
                "within 3% rel: same-audio suspicion, needs ears to confirm",
            ],
        },
        "files": [table[k] for k in sorted(table)],
        "pairs": pair_rows,
        "summary": summary,
        "orphans": [table[o] for o in sorted(ORPHANS)],
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    print(f"wrote {OUT_JSON}")


if __name__ == "__main__":
    sys.exit(main())
