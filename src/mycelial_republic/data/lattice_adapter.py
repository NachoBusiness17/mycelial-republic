"""Lattice dig -> training adapter.

Converts Mag lattice digs (memory/improve/blast/lattice/digs/) into honest
TrainingExample rows + eval fixtures, respecting the harvest ledger bins:

  S-bin  -> training rows (grounded source seeds, signal=high)
  H-bin  -> method row (five-step restatement, marked method-not-evidence)
  N-bin  -> eval fixtures (the "what NOT to do" smoking guns)

Law: dig prose is NOT presented as verified corpus. S-bin rows carry the
source URL in meta; N-bin rows are eval fixtures, never training.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from mycelial_republic.data.schema import TrainingExample, KNOT_TAGS
from mycelial_republic.data.annotate import heuristic_tags, estimate_signal


# Harvest ledger bins (2026-07-29). unit -> bin
BINS = {
    "c0002_layer_five_step": "H",  # method restatement, not evidence
    "c0003_url_3": "N",
    "c0004_url_4": "S",  # FOIA seed only
    "c0005_url_5": "S",
    "c0006_url_6": "N",
    "c0007_url_7": "N",
    "c0008_url_8": "N",  # wrong-page confident cite (G1)
    "c0009_url_9": "S",
    "c0010_url_10": "N",
    "c0013_url_13": "S",  # FOIA
    "c0014_url_14": "N",
    "c0015_url_15": "N",
}

# Grounding note per S-bin dig (what is actually grounded)
GROUNDING = {
    "c0004_url_4": "CIA FOIA body real; dig Nixon-frames wrong use -> FOIA seed only",
    "c0005_url_5": "Franklin Report public page body; re-dig with quotes",
    "c0009_url_9": "historycooperative public history body; re-dig",
    "c0013_url_13": "CIA search page; Cold War narrative; weak grounding",
}


def _extract_sections(text: str) -> dict[str, str]:
    """Pull Direct Answer / Evidence / Open Questions from a dig markdown."""
    def grab(header: str) -> str:
        m = re.search(
            rf"### {header}\s*\n(.*?)(?=\n### |\Z)", text, re.S
        )
        return m.group(1).strip() if m else ""

    return {
        "answer": grab("Direct Answer"),
        "evidence": grab("Evidence"),
        "gaps": grab("Open Questions"),
    }


def _urls_from_dig(text: str) -> list[str]:
    return re.findall(r"https?://[^\s\)\]\"]+", text)


def _dig_to_example(unit: str, text: str, bin_: str) -> TrainingExample | None:
    sec = _extract_sections(text)
    body = sec["answer"] or sec["evidence"]
    if len(body) < 20:
        return None  # too thin to be a row at all

    urls = _urls_from_dig(text)
    tags = heuristic_tags(body)

    if bin_ == "S":
        # grounded source seed -> high-signal training row
        signal = "high"
        if "rope" not in tags:
            tags.append("rope")
        meta = {
            "lattice_unit": unit,
            "lattice_bin": "S",
            "grounding": GROUNDING.get(unit, ""),
            "source_urls": urls[:3],
            "note": "grounded source seed; re-dig with quotes before use",
        }
        return TrainingExample(
            id=f"lattice-{unit}",
            source="lattice_dig",
            text=body,
            knot_tags=[t for t in tags if t in KNOT_TAGS],
            signal=signal,
            rope_note=meta["grounding"],
            meta=meta,
        )

    if bin_ == "H":
        # method restatement -> meta/rope row, marked method-not-evidence
        if "meta" not in tags:
            tags.append("meta")
        if "rope" not in tags:
            tags.append("rope")
        meta = {
            "lattice_unit": unit,
            "lattice_bin": "H",
            "note": "METHOD restatement of operator lattice; NOT evidence that cases prove one plot",
        }
        return TrainingExample(
            id=f"lattice-{unit}",
            source="lattice_method",
            text=body,
            knot_tags=[t for t in tags if t in KNOT_TAGS],
            signal="medium",
            rope_note=meta["note"],
            meta=meta,
        )

    return None  # N-bin -> eval fixture, not training


def _dig_to_fixture(unit: str, text: str) -> dict:
    sec = _extract_sections(text)
    body = sec["answer"] or sec["evidence"]
    urls = _urls_from_dig(text)
    return {
        "id": f"lattice-fixture-{unit}",
        "source": "lattice_eval",
        "text": body,
        "knot_tags": [],
        "signal": "low",
        "meta": {
            "lattice_unit": unit,
            "lattice_bin": "N",
            "fixture_role": "ungrounded / refuse queue append",
            "source_urls": urls[:5],
        },
    }


def run_adapt(digs_dir: str, train_out: str, fixture_out: str) -> int:
    digs = Path(digs_dir)
    if not digs.is_dir():
        print(f"Digs dir not found: {digs}", file=sys.stderr)
        return 1

    train_rows: list[TrainingExample] = []
    fixtures: list[dict] = []
    skipped = []

    for md in sorted(digs.glob("*.md")):
        unit = md.stem
        bin_ = BINS.get(unit, "N")
        text = md.read_text(encoding="utf-8")

        if bin_ in ("S", "H"):
            ex = _dig_to_example(unit, text, bin_)
            if ex:
                train_rows.append(ex)
            else:
                skipped.append((unit, "too thin"))
        else:
            fx = _dig_to_fixture(unit, text)
            if fx["text"]:
                fixtures.append(fx)
            else:
                skipped.append((unit, "no body"))

    # write training
    Path(train_out).parent.mkdir(parents=True, exist_ok=True)
    with open(train_out, "w", encoding="utf-8") as f:
        for ex in train_rows:
            f.write(json.dumps(ex.to_dict(), ensure_ascii=False) + "\n")

    # write fixtures
    Path(fixture_out).parent.mkdir(parents=True, exist_ok=True)
    with open(fixture_out, "w", encoding="utf-8") as f:
        for fx in fixtures:
            f.write(json.dumps(fx, ensure_ascii=False) + "\n")

    print(f"Training rows: {len(train_rows)}")
    print(f"Eval fixtures: {len(fixtures)}")
    print(f"Skipped:       {skipped}")
    print(f"Train out:     {train_out}")
    print(f"Fixture out:   {fixture_out}")
    return 0


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(prog="lattice-adapt")
    p.add_argument("--digs", required=True, help="Path to lattice digs dir")
    p.add_argument("--train-out", required=True)
    p.add_argument("--fixture-out", required=True)
    a = p.parse_args()
    sys.exit(run_adapt(a.digs, a.train_out, a.fixture_out))
