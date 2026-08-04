"""Prepare mirror_train -> S-bin train.jsonl + N-bin eval_fixtures.jsonl.

Implements the seed-mirror plan (2026-08-02) S2 step:
  - S-bin (signal=high) rows -> train.jsonl {instruction, response}
    instruction synthesized from the annotation (rope/chord/refusal notes + theme);
    response = the operator's own thread text (grounded, source URL kept in meta).
  - N-bin (signal=medium/low) rows -> eval_fixtures.jsonl (the "what NOT to do"
    smoking guns - eval only, never train).

Law: S-bin rows carry source URL in meta (grounded-seed law). N-bin rows are
eval fixtures, never training. No privileged rank fields are emitted.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from mycelial_republic.data.schema import TrainingExample, KNOT_TAGS

# Default paths (repo-relative)
DEFAULT_TRAIN = "data/annotated/mirror_train.jsonl"
DEFAULT_TRAIN_OUT = "data/train/train.jsonl"
DEFAULT_FIXTURE_OUT = "data/train/eval_fixtures.jsonl"

# Instruction templates keyed by knot tag (fall back to theme).
INSTRUCTION_BY_TAG = {
    "chord": "Strike the chord on this tension the way the operator would.",
    "refusal": "Refuse this without founding a new church, in the operator's voice.",
    "rope": "Name the rope / invisible structure at play, as the operator does.",
    "parable": "Tell the story that teaches this, the way the operator tells it.",
    "audit": "Audit this honestly, the way the operator audits.",
    "mycelial": "Explain the mycelial / forkable move, in the operator's voice.",
    "daily": "Continue in the operator's ordinary sovereign-mirror voice.",
    "meta": "Speak about the mirror / protocol itself, as the operator does.",
}

INSTRUCTION_BY_THEME = {
    "philosophical": "Reflect on this the way the operator reflects.",
    "informational": "Explain this the way the operator explains it.",
    "rebuttal": "Push back on this the way the operator pushes back.",
    "joke": "Land the joke the way the operator lands it.",
}


def _synthesize_instruction(row: dict) -> str:
    tags = list(row.get("knot_tags") or [])
    for t in tags:
        if t in INSTRUCTION_BY_TAG:
            return INSTRUCTION_BY_TAG[t]
    theme = row.get("theme") or ""
    if theme in INSTRUCTION_BY_THEME:
        return INSTRUCTION_BY_THEME[theme]
    return "Continue in the operator's sovereign mirror voice."


def _clean_text(text: str) -> str:
    """Strip chrome/links/media junk; keep prose only."""
    lines = []
    for ln in text.splitlines():
        s = ln.strip()
        if not s:
            continue
        if s.startswith("[") and s.endswith(")"):  # media/link lines
            continue
        if s.startswith(("## ", "### ")) or s.startswith("#"):
            continue
        if re.match(r"^(Video \d+|PHOTO \d+|GIF \d+|Media attached)", s, re.I):
            continue
        lines.append(s)
    return "\n\n".join(lines)


def _urls_from_text(text: str) -> list[str]:
    return re.findall(r"https?://[^\s\)\]\"]+", text)


def run_prepare(
    train_in: str = DEFAULT_TRAIN,
    train_out: str = DEFAULT_TRAIN_OUT,
    fixture_out: str = DEFAULT_FIXTURE_OUT,
) -> int:
    inp = Path(train_in)
    if not inp.is_file():
        print(f"Input not found: {inp}", file=sys.stderr)
        return 1

    train_rows: list[dict] = []
    fixtures: list[dict] = []
    skipped = []

    for i, line in enumerate(inp.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as e:
            skipped.append((i, f"invalid JSON: {e}"))
            continue

        signal = row.get("signal") or "medium"
        text = _clean_text(row.get("text") or "")
        if len(text) < 30:
            skipped.append((i, "text too short after clean"))
            continue

        tags = [t for t in (row.get("knot_tags") or []) if t in KNOT_TAGS]
        meta = dict(row.get("meta") or {})
        urls = _urls_from_text(row.get("text") or "")
        if urls:
            meta["source_urls"] = urls[:3]

        if signal == "high":
            # S-bin -> training row
            instruction = _synthesize_instruction(row)
            train_rows.append(
                {
                    "id": str(row.get("id") or f"train-{i}"),
                    "source": row.get("source") or "x_archive",
                    "instruction": instruction,
                    "response": text,
                    "text": text,
                    "knot_tags": tags,
                    "signal": "high",
                    "rope_note": row.get("rope_note") or "",
                    "chord_note": row.get("chord_note") or "",
                    "refusal_note": row.get("refusal_note") or "",
                    "created_at": row.get("created_at") or "",
                    "meta": meta,
                }
            )
        else:
            # N-bin -> eval fixture (never training)
            fixtures.append(
                {
                    "id": f"fixture-{row.get('id') or i}",
                    "source": row.get("source") or "x_archive",
                    "text": text,
                    "knot_tags": tags,
                    "signal": signal,
                    "meta": {
                        **meta,
                        "fixture_role": "eval only - what NOT to do / refuse queue",
                    },
                }
            )

    # write train
    Path(train_out).parent.mkdir(parents=True, exist_ok=True)
    with open(train_out, "w", encoding="utf-8") as f:
        for r in train_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # write fixtures
    Path(fixture_out).parent.mkdir(parents=True, exist_ok=True)
    with open(fixture_out, "w", encoding="utf-8") as f:
        for r in fixtures:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"S-bin train rows:   {len(train_rows)} -> {train_out}")
    print(f"N-bin eval fixtures:{len(fixtures)} -> {fixture_out}")
    print(f"skipped:            {len(skipped)}")
    for s in skipped[:10]:
        print(f"  - {s}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Prepare mirror_train -> train + eval fixtures")
    ap.add_argument("--in", dest="inp", default=DEFAULT_TRAIN)
    ap.add_argument("--train-out", default=DEFAULT_TRAIN_OUT)
    ap.add_argument("--fixture-out", default=DEFAULT_FIXTURE_OUT)
    a = ap.parse_args(argv)
    return run_prepare(a.inp, a.train_out, a.fixture_out)


if __name__ == "__main__":
    raise SystemExit(main())
