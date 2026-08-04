"""Annotate cleaned posts with knot/chord metadata for training."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from mycelial_republic.data.schema import TrainingExample, KNOT_TAGS


from mycelial_republic.cipher_v0 import detect_cipher_heuristics


# Heuristic keyword maps — review manually; heuristics are not gospel.
HEURISTICS: list[tuple[str, re.Pattern[str]]] = [
    ("chord", re.compile(r"strike the chord|chord strike|strike.?the.?chord", re.I)),
    ("refusal", re.compile(r"i do not consent|sovereign refusal|i refuse|do not consent", re.I)),
    ("rope", re.compile(r"\brope\b|invisible chain|standing army of|capture vector", re.I)),
    ("mycelial", re.compile(r"myceli|spore|parallel construction|forkable", re.I)),
    ("parable", re.compile(r"parable|once there was|imagine a|marble and rubber", re.I)),
    ("audit", re.compile(r"\baudit\b|commitment hash|verifiable", re.I)),
    ("meta", re.compile(r"sovereign mirror|vector scaffold|GSTD|mirror protocol", re.I)),
    ("cipher", re.compile(r"\b\d+\s*:\s*\d+\b|chapter\s+\d+.*(verse|line)|book cipher|index pattern", re.I)),
    ("riddle", re.compile(r"\?.*\b(like|as if|metaphor|what am i)\b|\briddle\b", re.I)),
]


def heuristic_tags(text: str) -> list[str]:
    tags: list[str] = []
    for name, pat in HEURISTICS:
        if pat.search(text):
            tags.append(name)
    if not tags and len(text) >= 120:
        tags.append("daily")
    return tags


def estimate_signal(text: str, tags: list[str]) -> str:
    if any(t in tags for t in ("chord", "refusal", "rope", "parable", "meta")):
        return "high"
    if len(text) >= 200:
        return "medium"
    # Operator's own short replies are still the operator's voice.
    # Keep them as medium signal (daily knot tag added separately) so a mirror
    # learns how the operator responds in conversation.
    return "medium"


def run_annotate(inp: str, out: str, auto_heuristics: bool = True) -> int:
    inp_path = Path(inp)
    out_path = Path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not inp_path.is_file():
        print(f"Input not found: {inp_path}", file=sys.stderr)
        return 1

    written = 0
    skipped_low = 0
    with inp_path.open(encoding="utf-8") as fin, out_path.open("w", encoding="utf-8") as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            text = (row.get("text") or "").strip()
            tags = list(row.get("knot_tags") or [])
            if auto_heuristics:
                for t in heuristic_tags(text):
                    if t not in tags:
                        tags.append(t)
                for t in detect_cipher_heuristics(text):
                    if t not in tags and t in ("cipher", "riddle", "acrostic_candidate", "index_pattern"):
                        # map detect tags into knot_tags where allowed
                        knot = "cipher" if t in ("cipher", "index_pattern", "acrostic_candidate") else t
                        if knot not in tags:
                            tags.append(knot)
            signal = row.get("signal") or estimate_signal(text, tags)
            if signal == "daily" and "daily" not in tags:
                tags.append("daily")
            if signal == "low" and not tags:
                skipped_low += 1
                continue

            ex = TrainingExample(
                id=str(row.get("id") or f"ann-{written}"),
                source=row.get("source") or "x_archive",
                text=text,
                instruction=row.get("instruction") or "",
                response=row.get("response") or "",
                knot_tags=[t for t in tags if t in KNOT_TAGS],
                signal=signal,
                rope_note=row.get("rope_note") or "",
                chord_note=row.get("chord_note") or "",
                refusal_note=row.get("refusal_note") or "",
                created_at=row.get("created_at") or "",
                meta=dict(row.get("meta") or {}),
            )
            errs = ex.validate()
            if errs and "too short" in " ".join(errs):
                skipped_low += 1
                continue
            fout.write(json.dumps(ex.to_dict(), ensure_ascii=False) + "\n")
            written += 1

    print(
        f"Annotated {written} examples → {out_path} (skipped {skipped_low} low-signal)",
        file=sys.stderr,
    )
    print(
        "Next: hand-edit high-value rows (rope_note, chord_note, refusal_note) "
        "then run: mycelia validate --in ...",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--auto-heuristics", action="store_true", default=True)
    a = ap.parse_args()
    raise SystemExit(run_annotate(a.inp, a.out, auto_heuristics=a.auto_heuristics))
