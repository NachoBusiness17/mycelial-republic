"""B2-262 adjacency-vs-window design probe (probe-then-edit per B2_219).

Question: can the QUANTITY near-window (12 chars each side, whole-word unit
anywhere in the window kills the candidate) be replaced by strict
candidate-number-then-unit adjacency without changing any ledger outcome?

Method: reimplement ONLY the two guard decisions over the same sentences the
extractor sees (NUM_NOY path, DOT_NOY path), under both rules:
  window    = QUANTITY.search(sent[m.start()-12 : m.end()+12])   (+ "$" in
              window on the DOT_NOY path)  -> candidate dies
  adjacency = a QUANTITY unit token touching the number (one space of
              separation allowed on either side), or "$" touching the
              number on the DOT_NOY path                   -> candidate dies
For every site where the verdicts differ, classify the effect on the live
ledger (watch/inbox/qdrop_export/q_caption_ledger.jsonl, the check7
byte-equal surface) and on the three named pin drops.

Run: .venv/Scripts/python.exe watch/inbox/burn_wave_20260926/B2_262_adjacency_probe.py
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

import the50_t21_q_caption_ledger as L  # noqa: E402

SRC = ROOT / "watch" / "inbox" / "qdrop_export" / "qdrops.jsonl"
LEDGER = ROOT / "watch" / "inbox" / "qdrop_export" / "q_caption_ledger.jsonl"

# unit token touching the number: (optional single space)(unit)(boundary)
UNIT_BEFORE = re.compile(
    r"(?:^|\s)(" + L.QUANTITY.pattern + r")\s*$", re.IGNORECASE)
UNIT_AFTER = re.compile(
    r"^\s*(" + L.QUANTITY.pattern + r")(?![a-z])", re.IGNORECASE)


def _touching_after(after: str) -> bool:
    """QUANTITY unit begins within 2 touching chars (space/hyphen/bracket) of
    the number, compound units included (search semantics over the near span,
    so 'megabytes' fires via its bytes alternative like the window does)."""
    span = after[:24]
    m = L.QUANTITY.search(span)
    return bool(m and m.start() <= 2 and not (m.start() == 0 and False))


def _touching_before(before: str) -> bool:
    span = before[-24:]
    m = L.QUANTITY.search(span)
    return bool(m and (len(span) - m.end()) <= 2)


def window_kill(sent, m, dollar=False):
    near = sent[max(0, m.start() - 12): m.end() + 12]
    return bool(L.QUANTITY.search(near) or (dollar and "$" in near))


def adjacency_kill(sent, m, dollar=False):
    before = sent[: m.start()]
    after = sent[m.end():]
    # two variants, reported separately by the caller:
    #  strict: match-at-anchored unit token (naive adjacency)
    strict = bool(UNIT_BEFORE.search(before) or UNIT_AFTER.search(after))
    #  touching: search semantics over the touching span (compound units
    #  like "megabytes" fire, hyphen/bracket joins count)
    touching = bool(_touching_after(after) or _touching_before(before))
    if dollar and ("$" in sent[max(0, m.start() - 1): m.start()]
                   or "$" in sent[m.end(): m.end() + 1]):
        strict = touching = True
    return strict, touching


def main():
    ledger_rows = [json.loads(l) for l in LEDGER.open(encoding="utf-8") if l.strip()]
    ledger_keys = {(r["id"], r["date"]) for r in ledger_rows}

    diff_sites = []          # (id, path, sent, text, window, adjacency)
    stats = defaultdict(int)
    pin = {"1416139": None, "7643939": None}

    with SRC.open(encoding="utf-8") as f:
        drops = [json.loads(l) for l in f if l.strip()]

    for drop in drops:
        did = str(drop.get("id") or drop.get("post") or "")
        raw = drop.get("text") or ""
        if not raw.strip():
            continue
        text = L.clean_text(raw)
        for sent in L.sentences(text):
            for m in L.NUM_NOY.finditer(sent):
                stats["num_sites"] += 1
                w = window_kill(sent, m)
                a = adjacency_kill(sent, m)
                if w != a:
                    diff_sites.append((did, "NUM_NOY", sent, str(m.group(0)), w, a))
                    stats["num_diff"] += 1
                if did in pin and pin[did] is None:
                    pin[did] = (sent, w, a)
            for m in L.DOT_NOY.finditer(sent):
                stats["dot_sites"] += 1
                w = window_kill(sent, m, dollar=True)
                a = adjacency_kill(sent, m, dollar=True)
                if w != a:
                    diff_sites.append((did, "DOT_NOY", sent, str(m.group(0)), w, a))
                    stats["dot_diff"] += 1
                if did in pin and pin[did] is None:
                    pin[did] = (sent, w, a)

    # Which differing sites touch ledger rows? A keeper whose site the window
    # KEEPS but adjacency KILLS would delete a ledger row (hard fail). A site
    # the window kills but adjacency keeps would ADD a row (ledger mutation).
    ledger_ids = {i for (i, _) in ledger_keys}
    affected_ledger_ids = sorted({d for (d, *_rest) in diff_sites if d in ledger_ids})

    out = {
        "drops": len(drops),
        "sites": dict(stats),
        "diff_sites": len(diff_sites),
        "diff_affecting_ledger_drops": affected_ledger_ids[:40],
        "diff_affecting_ledger_count": len(affected_ledger_ids),
        "pins": {k: {"sent": v[0] if v else None,
                     "window_kill": v[1] if v else None,
                     "adjacency_kill": v[2] if v else None}
                 for k, v in pin.items()},
        "samples_kept_by_adjacency_killed_by_window": [
            {"id": d, "path": p, "token": t, "sent": s}
            for (d, p, s, t, w, a) in diff_sites if w and not a
        ][:25],
        "samples_killed_by_adjacency_kept_by_window": [
            {"id": d, "path": p, "token": t, "sent": s}
            for (d, p, s, t, w, a) in diff_sites if a and not w
        ][:25],
    }
    print(json.dumps(out, indent=1)[:6000])


if __name__ == "__main__":
    main()
