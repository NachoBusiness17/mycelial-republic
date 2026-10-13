"""olm_tokenizer_probe - durable one-shot for the OLM steal card (2026-09-30).

Measures the token cost of the SAME corpus slice through locally pulled janitor
families via the local Ollama server: POST /api/generate with num_predict 1 and
read prompt_eval_count - the server tokenizer the janitor pipeline actually pays.
Adds an offline HF tokenizer count for a Qwen3-family data point when the cached
snapshot and transformers are present.

Provenance: born from the round-1 card whose probe script was deleted after
banking (round-2 critique defect 2); this file is the durable artifact so any
future seat can rerun the measurement byte-for-byte.

Known server quirk (ollama 0.34.3, verified 2026-09-30): per-request
options.num_ctx is NOT honored - a full-file run returns prompt_eval_count 4098
(the truncation cap) regardless of the requested window, so full-file model
comparisons through this server are INVALID. Default mode is therefore the
8000-byte slice; --full exists only to re-demonstrate the cap. Downstream flag
raised by the round-2 critique and NOT re-verified here: mag/lattice_loop.py:280
passes per-request num_ctx=32768 to ChatOllama on this same server build.

Usage:
  .venv/Scripts/python.exe tools/olm_tokenizer_probe.py
  .venv/Scripts/python.exe tools/olm_tokenizer_probe.py --full
  .venv/Scripts/python.exe tools/olm_tokenizer_probe.py --models gemma:2b,gemma4:latest
No subprocess spawns; single-process urllib only.
"""
from __future__ import annotations

import argparse
import json
import time
import urllib.request

SAMPLE = r"corpus\tmp\oni_dig\Breathability.html"  # 580090 bytes, real corpus HTML
SLICE_BYTES = 8000
QWEN3_SNAPSHOT = (
    r"C:\Users\foste\.cache\huggingface\hub"
    r"\models--Qwen--Qwen3-8B"
    r"\snapshots\b968826d9c46dd6066d109eabc6255188de91218"
)
DEFAULT_MODELS = ["gemma:2b", "qwen2.5:3b-instruct"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true",
                    help="run the FULL file to re-demonstrate the 4098 truncation cap")
    ap.add_argument("--models", default=",".join(DEFAULT_MODELS))
    ap.add_argument("--offline-qwen3", action="store_true", default=True)
    args = ap.parse_args()

    with open(SAMPLE, encoding="utf-8", errors="replace") as f:
        text = f.read()
    print(f"sample {SAMPLE} bytes {len(text)}")

    prompts = [("FULL", text)] if args.full else [("slice", text[:SLICE_BYTES])]
    for label, prompt in prompts:
        for model in [m.strip() for m in args.models.split(",") if m.strip()]:
            body = json.dumps({
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {"num_predict": 1},
            }).encode()
            t0 = time.time()
            req = urllib.request.Request(
                "http://localhost:11434/api/generate",
                data=body,
                headers={"Content-Type": "application/json"},
            )
            try:
                d = json.loads(urllib.request.urlopen(req, timeout=420).read())
                print(f"{label} {model} prompt_eval_count {d.get('prompt_eval_count')} "
                      f"gen_tokens {d.get('eval_count')} "
                      f"wall_s {round(time.time() - t0, 1)} "
                      f"load_s {round(d.get('load_duration', 0) / 1e9, 1)}")
            except Exception as e:  # noqa: BLE001 - probe must report, not crash
                print(f"{label} {model} ERROR {type(e).__name__}: {e}")

    if args.offline_qwen3:
        try:
            from transformers import AutoTokenizer

            tok = AutoTokenizer.from_pretrained(QWEN3_SNAPSHOT, local_files_only=True)
            ids = tok(text[:SLICE_BYTES])["input_ids"]
            print(f"slice qwen3-8B tokenizer.json (offline) count {len(ids)}")
        except Exception as e:  # noqa: BLE001
            print(f"offline qwen3 tokenizer SKIPPED {type(e).__name__}: {e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
