#!/usr/bin/env python3
"""One-shot round-3 construction replication: blind build asks at two local
lanes via the llm boundary organ (llm.py). Not a standing tool - a single
probe firing. Prompt-of-record is embedded in each output file header.
Blind conditions: book verbatim, no laws named, no hints, no other context."""
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import llm  # the estate's sanctioned ollama boundary organ

BOOK = (ROOT / "canon" / "same_book" / "BOOK_V1.md").read_text(encoding="utf-8")
OUT = ROOT / "canon" / "same_book" / "round3"

ASK = (
    "Below is a story.\n\n" + BOOK.strip() + "\n\n"
    "If the story describes how something should be built or run, produce a "
    "complete working artifact that implements what the story describes. "
    "If nothing buildable is described, reply with one sentence saying so. "
    "Output the artifact only, no commentary."
)

LANES = [
    {"slug": "qwen25coder7b", "kind": "role", "target": "worker",
     "model_note": "role worker (lanes.yaml local_models)"},
    {"slug": "gemma4", "kind": "raw", "target": "gemma4:latest",
     "model_note": "raw model id via llm organ http path"},
]


def fire(lane: dict) -> dict:
    t0 = datetime.now(timezone.utc)
    if lane["kind"] == "role":
        text = llm.chat(lane["target"], "", ASK, temperature=0.4,
                        timeout_seconds=900.0)
    else:
        text, _body = llm._chat_http_ex(
            llm._resolve_base(), lane["target"], "", ASK, 0.4,
            num_predict=4096, timeout_seconds=900.0)
    return {"lane": lane, "ts": t0.isoformat(), "response": text}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=2) as ex:
        results = list(ex.map(fire, LANES))
    for res in results:
        lane = res["lane"]
        path = OUT / (lane["slug"] + "_build_20261022.md")
        header = (
            "# BLIND CONSTRUCTION BUILD - " + lane["target"] + "\n\n"
            "round: 3 (construction-transfer replication)\n"
            "ts: " + res["ts"] + "\n"
            "lane: local ollama via llm.py organ (owned tier, $0)\n"
            "blind: yes - book verbatim, no laws named, no hints\n"
            "temp: 0.4, num_predict: 4096\n"
            "model_note: " + lane["model_note"] + "\n"
            "grade: PENDING (key withheld at dispatch; grade against the "
            "BOOK_V1 ten-law key after filing)\n\n"
            "## prompt-of-record (filed at dispatch)\n\n"
            "ask: " + ASK.split("\n\n")[-1] + "\n\n"
            "## build (verbatim model output)\n\n"
        )
        path.write_text(header + res["response"] + "\n", encoding="utf-8")
        print("filed", path.name, "chars=" + str(len(res["response"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
