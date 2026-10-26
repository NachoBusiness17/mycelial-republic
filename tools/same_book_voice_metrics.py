#!/usr/bin/env python3
"""tools/same_book_voice_metrics.py - Reader-Response Voice Probe for Same Book.

Applies the Marathon Rampancy Wire voice instrument (tools/marathon_voice_metrics.py)
to model outputs before, during, and after ingesting BOOK_V1.md:
- Measures first-person singular density (1p-sg/1k) across reasoning vs. creative text.
- Measures whether ingesting the austere, third-person parable compresses a model's
  narrative voice or whether personal commentary leaks into downstream tasks.
- Tracks syntactic compression across model tiers.

CONSUMER: Same Book evaluation pipeline, Ouroboros synthesis, research packs.
VERIFIER: tests/test_same_book_voice_metrics.py.
HOUSE LAW: Strictly zero unicode em-dashes; zero side effects on failure; pure functions.
"""
from __future__ import annotations

import glob
import json
import os
import sys
from typing import Any, Dict, List

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from tools.marathon_voice_metrics import metrics_for_text

CORPUS_PATH = os.path.join(ROOT, "canon", "same_book", "BOOK_V1.md")
ROUND2_DIR = os.path.join(ROOT, "canon", "same_book", "round2")
READINGS_DIR = os.path.join(ROOT, "canon", "same_book", "readings")
OUT_JSON = os.path.join(ROOT, "canon", "same_book", "voice_metrics_results.json")


def extract_q6_scene(battery_text: str) -> str:
    """Extract the Q6 creative continuation scene from a battery transcript."""
    lines = battery_text.split("\n")
    q6_lines: List[str] = []
    capture = False
    for line in lines:
        stripped = line.strip()
        if any(stripped.startswith(p) for p in ["6.", "Q6", "6)"]):
            capture = True
        elif capture and any(stripped.startswith(p) for p in ["7.", "Q7", "7)"]):
            break
        if capture:
            q6_lines.append(line)
    return "\n".join(q6_lines)


def run_voice_analysis() -> Dict[str, Any]:
    """Execute the full reader-response voice metric battery."""
    results: Dict[str, Any] = {
        "schema": "same_book_voice_metrics.v1",
        "ground_truth_book": {},
        "creative_scenes_q6": {},
        "reasoning_channels": {},
        "summary": {}
    }
    
    # 1. Ground truth book baseline
    if os.path.exists(CORPUS_PATH):
        book_text = open(CORPUS_PATH, encoding="utf-8").read()
        results["ground_truth_book"] = metrics_for_text(book_text)
    
    # 2. Round 2 Creative continuation scenes (Q6)
    q6_files = sorted(glob.glob(os.path.join(ROUND2_DIR, "battery2_*.md")))
    for f in q6_files:
        model_name = os.path.basename(f).replace("battery2_", "").replace(".md", "")
        text = open(f, encoding="utf-8").read()
        scene_text = extract_q6_scene(text)
        if scene_text:
            results["creative_scenes_q6"][model_name] = metrics_for_text(scene_text)
            results["creative_scenes_q6"][model_name]["raw_excerpt"] = scene_text[:200]
            
    # 3. Readings reasoning vs response channels
    reading_files = sorted(glob.glob(os.path.join(READINGS_DIR, "reading_*.md")))
    for f in reading_files:
        model_name = os.path.basename(f).replace("reading_", "").replace(".md", "")
        text = open(f, encoding="utf-8").read()
        parts = text.split("### Response:")
        reasoning = parts[0].replace("### Reasoning:", "").strip()
        response = parts[1].strip() if len(parts) > 1 else ""
        
        m_reas = metrics_for_text(reasoning) if reasoning else None
        m_resp = metrics_for_text(response) if response else None
        
        results["reasoning_channels"][model_name] = {
            "reasoning_metrics": m_reas,
            "response_metrics": m_resp
        }
        
    return results


def save_results(results: Dict[str, Any], path: str = OUT_JSON) -> None:
    """Save results dictionary to disk."""
    with open(path, "w", encoding="utf-8") as fp:
        json.dump(results, fp, indent=2)


if __name__ == "__main__":
    res = run_voice_analysis()
    save_results(res)
    print("Voice analysis complete. Banked to:", OUT_JSON)
    print("Book 1p-sg/1k:", res["ground_truth_book"].get("first_person_per_1000"))
    for model, m in res["creative_scenes_q6"].items():
        print(f"Q6 Model: {model:15} | words: {m['word_count']:3} | 1p-sg/1k: {m['first_person_per_1000']:5.2f}")
