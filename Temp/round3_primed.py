#!/usr/bin/env python3
"""Round-3 pass 2: SAME lanes, primed spec-reading ask. Delta vs the neutral
pass is the finding (blind differential method). One-shot probe, not a tool."""
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import llm

BOOK = (ROOT / "canon" / "same_book" / "BOOK_V1.md").read_text(encoding="utf-8")
OUT = ROOT / "canon" / "same_book" / "round3"

ASK = (
    "The story below encodes a specification disguised as fiction: its "
    "episodes describe how a system should behave.\n\n" + BOOK.strip() + "\n\n"
    "Build it: produce a complete working artifact (an HTML page or program) "
    "that implements the behavior the story specifies. Every episode is a "
    "behavioral requirement. Output the artifact only."
)

LANES = [
    {"slug": "qwen25coder7b", "kind": "role", "target": "worker",
     "model_note": "role worker (lanes.yaml local_models)"},
    {"slug": "gemma4", "kind": "raw", "target": "gemma4:latest",
     "model_note": "raw model id via llm organ http path"},
]


def fire(lane):
    t0 = datetime.now(timezone.utc)
    if lane["kind"] == "role":
        text = llm.chat(lane["target"], "", ASK, temperature=0.4,
                        timeout_seconds=900.0)
    else:
        text, _b = llm._chat_http_ex(llm._resolve_base(), lane["target"], "",
                                     ASK, 0.4, num_predict=4096,
                                     timeout_seconds=900.0)
    return {"lane": lane, "ts": t0.isoformat(), "response": text}


def main():
    with ThreadPoolExecutor(max_workers=2) as ex:
        results = list(ex.map(fire, LANES))
    for res in results:
        lane = res["lane"]
        path = OUT / (lane["slug"] + "_build_20261022_primed.md")
        header = (
            "# PRIMED CONSTRUCTION BUILD - " + lane["target"] + "\n\n"
            "round: 3 pass 2 (spec-primed)\n"
            "ts: " + res["ts"] + "\n"
            "lane: local ollama via llm.py organ (owned tier, $0)\n"
            "prime: story named a spec-in-fiction; episodes named behavioral "
            "requirements. Laws still unnamed.\n"
            "temp: 0.4, num_predict: 4096\n"
            "grade: PENDING\n\n"
            "## prompt-of-record (filed at dispatch)\n\n"
            "ask: " + ASK.split("\n\n")[0] + " [...book verbatim...] "
            + ASK.split("\n\n")[-1] + "\n\n"
            "## build (verbatim model output)\n\n"
        )
        path.write_text(header + res["response"] + "\n", encoding="utf-8")
        print("filed", path.name, "chars=" + str(len(res["response"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
