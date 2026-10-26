"""THE 50 / W5 / T24: symbol correlation, image-vs-speech.

Question: does the channel's IMAGE output move together with its SPEECH
output month by month? Two independent censuses over the same Mr Pool
corpus the earlier THE 50 tasks worked (watch/inbox/mrpool_export/):

  image census  - media_register.jsonl rows whose file is a still image
                  (jpg/png/gif), counted per month by post date.
  speech census - transcriptions.jsonl rows where whisper measured actual
                  speech (speech_seconds > 0 AND non-empty text), counted
                  per month by post ts. A video with no audio stream has
                  no transcription row (audio_probe.jsonl: 340 has_audio
                  == 340 transcribed files, sets identical), so within
                  months where videos were posted the speech census is
                  complete. Months with images but no posted video are
                  honest zeros in the speech census (nothing measurable,
                  not a measurement of zero speech) -- flagged below.

Verdict comes from tools/drift.py drift_check rules: the metric series is
the image census, the referent series is the speech census, both
zero-filled over the union of months, oldest first. Verdict ladder:
  ALIGNED corr>=0.5 / DRIFTING -0.5<corr<0.5 / INVERTED corr<=-0.5 /
  VACUOUS referent never moved / INSUFFICIENT <3 deltas / DEGENERATE.

Sensitivity pairings (clearly secondary) are filed alongside: the reverse
direction and an audio-present pairing (any audio stream, speech or not).

Usage: .venv/Scripts/python.exe scripts/the50_t24_symbol_correlation.py
Files: memory/runs/the50/w5_t24_symbol_correlation.json
"""

import json
import os
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)

from tools.drift import drift_check  # noqa: E402

EXPORT = os.path.join(REPO, "watch", "inbox", "mrpool_export")
REGISTER = os.path.join(EXPORT, "media_register.jsonl")
AUDIO_PROBE = os.path.join(EXPORT, "audio_probe.jsonl")
TRANSCRIPTS = os.path.join(EXPORT, "transcriptions.jsonl")
ARTIFACT = os.path.join(REPO, "memory", "runs", "the50",
                        "w5_t24_symbol_correlation.json")
ART_REL = "memory/runs/the50/w5_t24_symbol_correlation.json"

IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".gif")
VIDEO_EXTS = (".mp4", ".mov")


def month_of(ts):
    return (ts or "")[:7]


def load_jsonl(path):
    rows = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def build_censuses():
    reg = load_jsonl(REGISTER)
    probe = load_jsonl(AUDIO_PROBE)
    trans = load_jsonl(TRANSCRIPTS)

    images = {}   # month -> count of still-image register rows
    videos = {}   # month -> count of video register rows (mp4+mov)
    undated = 0
    for r in reg:
        m = month_of(r.get("date"))
        if not m:
            undated += 1
            continue
        low = r["file"].lower()
        if low.endswith(IMAGE_EXTS):
            images[m] = images.get(m, 0) + 1
        elif low.endswith(VIDEO_EXTS):
            videos[m] = videos.get(m, 0) + 1

    # transcription file set must equal the has_audio probe file set:
    # otherwise a missing transcription row would be unmeasured, not
    # silent, and the speech census would be incomplete.
    audio_files = set(r["file"] for r in probe if r.get("has_audio"))
    trans_files = set(r["file"] for r in trans)
    coverage_identical = audio_files == trans_files

    speech = {}   # month -> count of speech-bearing videos
    audio_present = {}  # month -> count of videos with any audio stream
    probe_by_file = {r["file"]: r for r in probe}
    for r in trans:
        m = month_of(r.get("ts"))
        if not m:
            continue
        has_audio = probe_by_file.get(r["file"], {}).get("has_audio")
        if has_audio:
            audio_present[m] = audio_present.get(m, 0) + 1
        if (r.get("speech_seconds") or 0) > 0 and (r.get("text") or "").strip():
            speech[m] = speech.get(m, 0) + 1

    months = sorted(set(images) | set(videos) | set(audio_present) | set(speech))
    table = [{"month": m,
              "images": images.get(m, 0),
              "videos_posted": videos.get(m, 0),
              "audio_present": audio_present.get(m, 0),
              "speech": speech.get(m, 0)} for m in months]
    return {
        "register_rows": len(reg),
        "register_undated": undated,
        "image_rows": sum(images.values()),
        "video_rows": sum(videos.values()),
        "probe_rows": len(probe),
        "probe_has_audio": len(audio_files),
        "transcription_rows": len(trans),
        "speech_rows": sum(speech.values()),
        "coverage_identical": coverage_identical,
        "table": table,
        "images_series": [row["images"] for row in table],
        "speech_series": [row["speech"] for row in table],
        "audio_series": [row["audio_present"] for row in table],
    }


def main():
    c = build_censuses()
    months = [row["month"] for row in c["table"]]
    span = "%s..%s (%d months)" % (months[0], months[-1], len(months))

    primary = drift_check(c["images_series"], c["speech_series"],
                          label="w5_t24 image-vs-speech (metric=images, referent=speech)")
    secondary = {
        "reverse_direction": drift_check(
            c["speech_series"], c["images_series"],
            label="sensitivity: metric=speech, referent=images"),
        "audio_pairing": drift_check(
            c["images_series"], c["audio_series"],
            label="sensitivity: metric=images, referent=any-audio-videos"),
    }

    artifact = {
        "program": "THE50",
        "task": "W5 T24 symbol correlation image-vs-speech",
        "when": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "question": ("do monthly image postings and monthly detected speech "
                     "move together month over month?"),
        "corpus": {
            "register": "watch/inbox/mrpool_export/media_register.jsonl",
            "register_rows": c["register_rows"],
            "register_undated_rows": c["register_undated"],
            "image_rows": c["image_rows"],
            "video_rows": c["video_rows"],
            "audio_probe": "watch/inbox/mrpool_export/audio_probe.jsonl",
            "audio_probe_rows": c["probe_rows"],
            "audio_probe_has_audio": c["probe_has_audio"],
            "transcriptions": "watch/inbox/mrpool_export/transcriptions.jsonl",
            "transcription_rows": c["transcription_rows"],
            "speech_rows": c["speech_rows"],
        },
        "definitions": {
            "image_census": "register rows with jpg/jpeg/png/gif file, counted per month by date",
            "speech_census": ("transcription rows with speech_seconds > 0 AND non-empty text, "
                              "counted per month by ts"),
            "audio_census": "transcription rows whose audio_probe row has has_audio=true",
        },
        "coverage": {
            "month_span": span,
            "transcription_set_equals_has_audio_set": c["coverage_identical"],
            "note": ("every video with an audio stream has a transcription row, so within "
                     "video-posting months the speech census is complete; a month with images "
                     "but no posted video scores speech=0 because speech was unmeasurable "
                     "there, not measured absent -- interpret referent zeros accordingly"),
        },
        "monthly_census": c["table"],
        "metric_image_series": c["images_series"],
        "referent_speech_series": c["speech_series"],
        "verdict": primary,
        "verdict_rule": "tools/drift.py drift_check: ALIGNED corr>=+0.5, INVERTED corr<=-0.5, "
                        "DRIFTING between, VACUOUS referent never moved, INSUFFICIENT <3 deltas",
        "sensitivity_secondary": secondary,
        "companion_code": "scripts/the50_t24_symbol_correlation.py",
        "run_command": ".venv/Scripts/python.exe scripts/the50_t24_symbol_correlation.py",
        "notes": [
            "speech census is video-gated: speech can only register in months where the "
            "channel posted an mp4/mov; image counts have no such gate",
            "delta correlation is scale-free, so the image series being much larger does not "
            "by itself force the verdict",
            "secondary pairings are filed for sensitivity only; the verdict of record is "
            "verdict, metric=images vs referent=speech as named by the task",
        ],
    }

    os.makedirs(os.path.dirname(ARTIFACT), exist_ok=True)
    with open(ARTIFACT, "w", encoding="utf-8") as fh:
        json.dump(artifact, fh, indent=1)
    text = open(ARTIFACT, encoding="utf-8").read()
    artifact["em_dash_check"] = "em-dash count in artifact bytes = %d" % text.count("\u2014")
    with open(ARTIFACT, "w", encoding="utf-8") as fh:
        json.dump(artifact, fh, indent=1)

    print("months: %s" % span)
    print("images: %s" % c["images_series"])
    print("speech: %s" % c["speech_series"])
    print("PRIMARY verdict: %s corr=%s deltas=%d" % (
        primary["verdict"], primary.get("corr_dm_dr"), primary.get("deltas_used", 0)))
    for k, v in secondary.items():
        print("sensitivity %-16s %s corr=%s" % (k, v["verdict"], v.get("corr_dm_dr")))
    print("filed: %s" % ART_REL)
    return artifact


if __name__ == "__main__":
    main()
