"""track_bpm — pure-python BPM detection for PRIVLIDGE music wiring.

No subprocess: reads 2205 Hz mono 16-bit WAVs that ffmpeg (called from the
shell, fixed paths) pre-decoded into state/fuel/bpm_pcm/. Onset envelope +
autocorrelation over 60-200 BPM; ranks by confidence into
state/fuel/music_bpm.json. BeatClock.SetBPM takes any detected value.
"""
from __future__ import annotations

import json
import struct
import wave
from pathlib import Path

PCM_DIR = Path(__file__).resolve().parent.parent / "state" / "fuel" / "bpm_pcm"
WINDOW_MS = 20
WINDOW = int(2205 * WINDOW_MS / 1000)  # samples per 20ms frame
BPM_MIN, BPM_MAX = 60, 200


def load_mono(path: Path) -> list[float]:
    with wave.open(str(path), "rb") as w:
        rate = w.getframerate()
        channels = w.getnchannels()
        width = w.getsampwidth()
        raw = w.readframes(w.getnframes())
    if rate != 2205 or width != 2:
        raise ValueError("expect 2205Hz s16, got %dHz width %d" % (rate, width))
    n = len(raw) // (2 * channels)
    out = [0.0] * n
    for i in range(n):
        acc = 0.0
        for c in range(channels):
            v = struct.unpack_from("<h", raw, (i * channels + c) * 2)[0]
            acc += v
        out[i] = acc / channels / 32768.0
    return out


def onset_envelope(samples: list[float]) -> list[float]:
    frames = max(1, len(samples) // WINDOW)
    env = [0.0] * frames
    for f in range(frames):
        s = 0.0
        base = f * WINDOW
        for i in range(base, base + WINDOW):
            v = samples[i]
            s += v * v
        env[f] = s / WINDOW
    onset = [0.0] * frames
    for f in range(1, frames):
        d = env[f] - env[f - 1]
        onset[f] = d if d > 0 else 0.0
    return onset


def detect_bpm(onset: list[float]) -> tuple[float, float]:
    frames_per_sec = 1000.0 / WINDOW_MS
    mean = sum(onset) / len(onset)
    x = [v - mean for v in onset]
    n = len(x)
    best_bpm, best_score = 0.0, -1.0
    scores: dict[int, float] = {}
    for bpm in range(BPM_MIN, BPM_MAX + 1):
        lag = frames_per_sec * 60.0 / bpm
        score = 0.0
        for mult in (1, 2):
            l = int(round(lag * mult))
            if l <= 0 or l >= n:
                continue
            s = 0.0
            for i in range(n - l):
                s += x[i] * x[i + l]
            score += s / (n - l)
        scores[bpm] = score
        if score > best_score:
            best_score, best_bpm = score, float(bpm)
    lo = scores.get(int(best_bpm) - 1, 0.0)
    hi = scores.get(int(best_bpm) + 1, 0.0)
    denom = lo - 2 * best_score + hi
    frac = 0.5 * (lo - hi) / denom if denom != 0 else 0.0
    refined = best_bpm + max(-0.5, min(0.5, frac))
    ordered = sorted(scores.values())
    median = ordered[len(ordered) // 2] or 1.0
    conf = best_score / (median * 3)
    return round(refined, 1), round(min(conf, 3.0), 2)


def main() -> None:
    wavs = sorted(PCM_DIR.glob("*.wav"))
    results = []
    for w in wavs:
        try:
            onset = onset_envelope(load_mono(w))
            bpm, conf = detect_bpm(onset)
            name = w.stem + ".mp3"
            results.append({"track": name, "bpm": bpm, "confidence": conf})
            print("%-58s %6.1f BPM  conf %.2f" % (name[:58], bpm, conf), flush=True)
        except Exception as e:
            print("%-58s FAIL %s" % (w.stem[:58], type(e).__name__), flush=True)
            results.append({"track": w.stem + ".mp3", "bpm": 0, "confidence": 0, "error": type(e).__name__})
    out = Path(__file__).resolve().parent.parent / "state" / "fuel" / "music_bpm.json"
    ranked = sorted((r for r in results if r.get("bpm")), key=lambda r: -r["confidence"])
    out.write_text(json.dumps(ranked, indent=1), encoding="utf-8")
    print(json.dumps({"detected": len(ranked), "of": len(wavs), "out": str(out)}, indent=1))


if __name__ == "__main__":
    main()
