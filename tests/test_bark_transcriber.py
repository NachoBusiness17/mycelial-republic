"""tests/test_bark_transcriber.py - Verification for Bark 3.0 audio transcriber."""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from tools.bark_transcriber import (
    format_markdown_transcript,
    mock_transcribe_audio,
    process_audio_file,
)


def test_mock_transcription():
    asr = mock_transcribe_audio("/tmp/fake_episode_01.wav", duration_sec=120.0)
    assert asr["model"] == "underdog-bark-3.0-163mb"
    assert len(asr["segments"]) == 3
    assert "floor hash" in asr["full_text"]


def test_markdown_formatting():
    asr = mock_transcribe_audio("/tmp/fake_episode_01.wav", duration_sec=60.0)
    md = format_markdown_transcript(asr, title="Test Episode")
    assert "# TRANSCRIPT -- TEST EPISODE" in md
    assert "**[00.0 - 04.5] Speaker 1:**" in md
    assert "—" not in md, "Forbidden unicode em-dash in transcript markdown"


def test_transcription_pipeline(tmp_path=None):
    dummy_wav = os.path.join(ROOT, "canon", "podcast_corpus", "test_run.wav")
    os.makedirs(os.path.dirname(dummy_wav), exist_ok=True)
    with open(dummy_wav, "wb") as fp:
        fp.write(b"RIFFdummydata1234567890")

    out_dir = os.path.join(ROOT, "canon", "podcast_corpus", "test_run_output")
    res = process_audio_file(dummy_wav, output_dir=out_dir, dry_run=True)
    assert res["status"] == "TRANSCRIPTION_COMPLETE"
    assert os.path.exists(res["transcript_md"])
    assert os.path.exists(res["meta_json"])

    # Clean up test artifacts
    if os.path.exists(dummy_wav):
        os.remove(dummy_wav)
    if os.path.exists(res["transcript_md"]):
        os.remove(res["transcript_md"])
    if os.path.exists(res["meta_json"]):
        os.remove(res["meta_json"])
    if os.path.exists(out_dir):
        os.rmdir(out_dir)


def test_em_dash_cleanliness():
    tool_file = os.path.join(ROOT, "tools", "bark_transcriber.py")
    content = open(tool_file, "r", encoding="utf-8").read()
    assert "—" not in content, "Forbidden unicode em-dash found in bark_transcriber.py"


if __name__ == "__main__":
    test_mock_transcription()
    test_markdown_formatting()
    test_transcription_pipeline()
    test_em_dash_cleanliness()
    print("ALL TESTS PASSED in test_bark_transcriber.py")
