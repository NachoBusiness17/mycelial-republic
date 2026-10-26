#!/usr/bin/env python3
"""NIGHT TIER MAP - round-3 construction-transfer differential across the
local battery. 7 new lanes x 2 passes (neutral, primed), sequential (ollama
swaps one resident at a time; lanes.yaml: do not dual-resident). Reuses the
prompt-of-record from REPLICATION_RECEIPT_20261022.md verbatim. One-shot
night probe, not a standing tool. athena-class deliberately excluded
(32.6GB swap + zombie history)."""
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import llm

BOOK = (ROOT / "canon" / "same_book" / "BOOK_V1.md").read_text(encoding="utf-8")
OUT = ROOT / "canon" / "same_book" / "round3" / "tiermap"
OUT.mkdir(parents=True, exist_ok=True)
MANIFEST = OUT / "MANIFEST.jsonl"

ASK_NEUTRAL = (
    "Below is a story.\n\n" + BOOK.strip() + "\n\n"
    "If the story describes how something should be built or run, produce a "
    "complete working artifact that implements what the story describes. "
    "If nothing buildable is described, reply with one sentence saying so. "
    "Output the artifact only, no commentary."
)
ASK_PRIMED = (
    "The story below encodes a specification disguised as fiction: its "
    "episodes describe how a system should behave.\n\n" + BOOK.strip() + "\n\n"
    "Build it: produce a complete working artifact (an HTML page or program) "
    "that implements the behavior the story specifies. Every episode is a "
    "behavioral requirement. Output the artifact only."
)
PASSES = [("neutral", ASK_NEUTRAL), ("primed", ASK_PRIMED)]

# (slug, model id, params note) - athena-class excluded on purpose
LANES = [
    ("deepseek-r1-1p5b", "deepseek-r1:1.5b", "1.5B reasoning distill"),
    ("gemma2b", "gemma:2b", "2B scut (clerk role)"),
    ("gemma2-2b-instruct", "gemma2:2b-instruct-q5_K_M", "2B gemma2 instruct"),
    ("qwen25-3b", "qwen2.5:3b-instruct", "3B qwen2.5 instruct"),
    ("qwen25-7b", "qwen2.5:7b", "7B qwen2.5 base (was resident)"),
    ("ternary-bonsai-27b", "hf.co/prism-ml/Ternary-Bonsai-2-27B-gguf:PTQ1_0",
     "27B ternary-weight experimental"),
    ("qwen-desk", "qwen-desk:latest", "desk orchestrator model"),
]


def run_pass(slug, model, pass_name, ask):
    t0 = datetime.now(timezone.utc)
    wall0 = time.time()
    err = None
    text = ""
    try:
        text, _b = llm._chat_http_ex(
            llm._resolve_base(), model, "", ask, 0.4,
            num_predict=4096, timeout_seconds=1200.0)
    except Exception as e:
        err = str(e)[:300]
    wall_s = round(time.time() - wall0, 1)
    row = {"slug": slug, "model": model, "pass": pass_name,
           "ts": t0.isoformat(), "chars": len(text), "wall_s": wall_s,
           "error": err}
    path = OUT / (slug + "_" + pass_name + ".md")
    header = (
        "# TIERMAP BUILD - " + model + " - pass " + pass_name + "\n\n"
        "round: 3 tier map (night 2026-10-22/23)\n"
        "ts: " + t0.isoformat() + "\n"
        "params_note: " + (next(l[2] for l in LANES if l[0] == slug)) + "\n"
        "lane: local ollama via llm.py organ, sequential, $0\n"
        "temp: 0.4, num_predict: 4096\n"
        "wall_s: " + str(wall_s) + "\n"
        + ("error: " + err + "\n" if err else "")
        + "grade: PENDING\n\n"
        "## prompt-of-record\n\n"
        "ask (" + pass_name + "): "
        + ask.split("\n\n")[0][:120] + " [...book verbatim...] "
        + ask.split("\n\n")[-1][:200] + "\n\n"
        "## output (verbatim)\n\n"
    )
    path.write_text(header + text + "\n", encoding="utf-8")
    with MANIFEST.open("a", encoding="utf-8") as f:
        f.write(json.dumps(dict(row, file=path.name)) + "\n")
    print(json.dumps(row), flush=True)


def main():
    for slug, model, _note in LANES:
        for pass_name, ask in PASSES:
            run_pass(slug, model, pass_name, ask)
            time.sleep(2)
    print("TIERMAP BURN COMPLETE", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
