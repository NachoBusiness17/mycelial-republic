"""Local inference path (Sprint 0.3 S4) - call the seed-mirror model via ollama.

Implements the seed-mirror plan (2026-08-02) S4 step:
  mycelia infer "<prompt>" -> ollama chat(seed-mirror) -> print response

Optionally --fixture <eval_fixtures.jsonl> to score responses against the
N-bin fixtures (the "what NOT to do" smoking guns) using the existing scorer.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DEFAULT_MODEL = "seed-mirror"


def _ollama_chat(model: str, prompt: str) -> str:
    """Call ollama chat via the ollama CLI (no SDK dependency)."""
    import urllib.request

    payload = json.dumps(
        {"model": model, "messages": [{"role": "user", "content": prompt}], "stream": False}
    ).encode("utf-8")
    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("message", {}).get("content", "")


def run_infer(prompt: str, model: str = DEFAULT_MODEL, fixture: str | None = None) -> int:
    try:
        response = _ollama_chat(model, prompt)
    except Exception as e:  # noqa: BLE001 - surface ollama errors clearly
        print(f"ollama error: {e}", file=sys.stderr)
        return 1

    print(response)

    if fixture:
        fx_path = Path(fixture)
        if not fx_path.is_file():
            print(f"Fixture not found: {fx_path}", file=sys.stderr)
            return 1
        try:
            from mycelial_republic.selftest.scorer import score_response
        except ImportError:
            print("scorer not importable; skipping fixture scoring", file=sys.stderr)
            return 0
        n = 0
        for line in fx_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            n += 1
            s = score_response(response, row.get("text") or "")
            print(f"  fixture {row.get('id')}: score={s:.3f}")
        print(f"scored {n} fixtures")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Run seed-mirror model via ollama")
    ap.add_argument("prompt")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--fixture", default="")
    a = ap.parse_args(argv)
    return run_infer(a.prompt, model=a.model, fixture=a.fixture or None)


if __name__ == "__main__":
    raise SystemExit(main())
