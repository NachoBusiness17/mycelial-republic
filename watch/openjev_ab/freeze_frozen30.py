"""freeze_frozen30.py - build the openjev A/B frozen test set (GO row 9, MICKEY17_V2).

Freezes exactly 30 judge items from the estate's wave-1 tier-1 judge corpus
(memory/runs/mickey17_v2/runs/agent-engineering-frontier-sweep-40/lanes/*.checks.json,
joined positionally to the same-dir lane JSONs for premise quotes).

Deterministic by construction: given the corpus bytes on disk, the output bytes
are a pure function of SEED below. Run it twice, diff the outputs: they must be
byte-identical. The set is FROZEN once filed: the night-window runner refuses to
score any file whose per-item hashes or set hash differ from the manifest.

Item shape (openjev typed-decision / NLI form, JSON with options + rubrics):
  premise   = the lane row's verbatim source quote  (the evidence)
  hypothesis = the judged claim text                (the assertion)
  options    = ["no", "yes"]  (does the premise entail the hypothesis?)
  prior_judge = the tier-1 verifier's verdict + reason (reference only; it is
  stripped from every prompt both arms see, so it cannot leak into the A/B).

Selection rules (pre-registered, mirrored in OPENJEV_AB_PROTOCOL_20260925.md):
  1. Universe: every (lane, field, idx) row from the 40 checks files with
     prior supports in {yes,no}, claim length >= 40 chars, and a premise
     available: either an embedded quote in the checks row, or a positionally
     aligned lane row (checks idx -> lane rows[idx]) whose claim similarity
     (difflib ratio, whitespace-normalized) is >= 0.60.
  2. Dedupe on whitespace-normalized claim (first in canonical order wins).
  3. Stratify: 15 with prior supports=yes, 15 with prior supports=no.
  4. Within each stratum take the 15 lowest
     sha256(SEED|lane|field|idx|claim120) hashes; output order = hash ascending.

Run:  ./.venv/Scripts/python.exe watch/openjev_ab/freeze_frozen30.py
Out:  watch/openjev_ab/frozen30_20260925.jsonl  (+ prints the set sha256)
"""
from __future__ import annotations

import difflib
import glob
import hashlib
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "memory" / "runs" / "mickey17_v2" / "runs" / \
    "agent-engineering-frontier-sweep-40" / "lanes"
OUT = ROOT / "watch" / "openjev_ab" / "frozen30_20260925.jsonl"
SEED = "openjev-ab-frozen-20260925"
N_PER_CLASS = 15
MIN_CLAIM_CHARS = 40
MIN_ALIGN_RATIO = 0.60
CHECKS_FIELDS = ("supports", "checks", "rows", "entries")


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip().lower()


def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def load_universe() -> list[dict]:
    lane_rows: dict[str, list[dict]] = {}
    for f in sorted(glob.glob(str(CORPUS / "*.json"))):
        name = os.path.basename(f)[:-5]
        if name.endswith(".checks"):
            continue
        d = json.load(open(f, encoding="utf-8"))
        rows = d.get("rows", []) if isinstance(d, dict) else d
        lane_rows[name] = rows

    items: list[dict] = []
    seen_claims: set[str] = set()
    for f in sorted(glob.glob(str(CORPUS / "*.checks.json"))):
        lane = os.path.basename(f)[:-12]
        d = json.load(open(f, encoding="utf-8"))
        lrows = lane_rows.get(lane, [])
        for field in CHECKS_FIELDS:
            v = d.get(field) if isinstance(d, dict) else None
            if not isinstance(v, list):
                continue
            for idx, r in enumerate(v):
                if not isinstance(r, dict):
                    continue
                prior = r.get("supports")
                if prior not in ("yes", "no"):
                    continue
                claim = (r.get("claim") or "").strip()
                if len(claim) < MIN_CLAIM_CHARS:
                    continue
                reason = (r.get("reason") or "").strip()
                quote = (r.get("quote") or "").strip()
                align = None
                src_url = ""
                lane_row_idx = None
                if not quote and idx < len(lrows):
                    lr = lrows[idx]
                    ratio = difflib.SequenceMatcher(
                        None, norm(claim), norm(lr.get("claim"))).ratio()
                    if ratio >= MIN_ALIGN_RATIO:
                        quote = (lr.get("quote") or "").strip()
                        src_url = (lr.get("source") or "").strip()
                        lane_row_idx = idx
                        align = round(ratio, 3)
                elif quote and idx < len(lrows):
                    src_url = (lrows[idx].get("source") or "").strip()
                    lane_row_idx = idx
                    align = round(difflib.SequenceMatcher(
                        None, norm(claim), norm(lrows[idx].get("claim"))).ratio(), 3)
                if not quote:
                    continue
                key = norm(claim)
                if key in seen_claims:
                    continue
                seen_claims.add(key)
                h = sha(f"{SEED}|{lane}|{field}|{idx}|{key[:120]}")
                items.append({
                    "hash": h,
                    "lane": lane,
                    "field": field,
                    "idx": idx,
                    "claim": claim,
                    "quote": quote,
                    "reason": reason,
                    "prior": prior,
                    "src_url": src_url,
                    "lane_row_idx": lane_row_idx,
                    "align": align,
                })
    return items


def build(items: list[dict]) -> list[dict]:
    out = []
    for prior in ("yes", "no"):
        pool = sorted((i for i in items if i["prior"] == prior),
                      key=lambda i: i["hash"])
        out.extend(pool[:N_PER_CLASS])
    out.sort(key=lambda i: i["hash"])
    rows = []
    for n, i in enumerate(out, 1):
        payload = {
            "item_id": f"ojab-{i['hash'][:8]}",
            "set": "openjev-ab-frozen-20260925",
            "n": n,
            "state": {"premise": i["quote"], "hypothesis": i["claim"]},
            "question": "Does the premise quote entail the hypothesis claim?",
            "options": ["no", "yes"],
            "rubric": {
                "no": "The quote does not entail the claim: it is silent on the "
                      "claim's load-bearing assertions, or contradicts them.",
                "yes": "The quote, read alone, entails the claim's load-bearing "
                       "assertions as written.",
            },
            "prior_judge": {
                "seat": "mickey17-v2 wave-1 tier-1 lane verifier (model id not "
                        "persisted in the estate; see corpus/steal/MASTER_MICKEY17_V2.md "
                        "preamble)",
                "supports": i["prior"],
                "reason": i["reason"],
            },
            "provenance": {
                "corpus_dir": str(CORPUS.relative_to(ROOT)).replace("\\", "/"),
                "lane": i["lane"],
                "checks_file": f"{i['lane']}.checks.json",
                "checks_field": i["field"],
                "checks_index": i["idx"],
                "lane_row_index": i["lane_row_idx"],
                "source_url": i["src_url"],
                "claim_alignment_ratio": i["align"],
            },
        }
        blob = json.dumps(
            {"state": payload["state"], "question": payload["question"],
             "options": payload["options"], "rubric": payload["rubric"]},
            sort_keys=True, ensure_ascii=False)
        payload["item_sha256"] = sha(blob)
        rows.append(payload)
    return rows


def main() -> int:
    if not CORPUS.is_dir():
        print(f"CORPUS MISSING: {CORPUS}", file=sys.stderr)
        return 2
    items = load_universe()
    by_class = {p: sum(1 for i in items if i["prior"] == p) for p in ("yes", "no")}
    rows = build(items)
    if len(rows) != 2 * N_PER_CLASS:
        print(f"UNIVERSE TOO SMALL: got {len(rows)} items "
              f"(universe={len(items)}, by_class={by_class})", file=sys.stderr)
        return 3
    OUT.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    OUT.write_text(text, encoding="utf-8", newline="\n")
    yes_n = sum(1 for r in rows if r["prior_judge"]["supports"] == "yes")
    print(f"wrote {OUT}")
    print(f"items={len(rows)} prior_yes={yes_n} prior_no={len(rows) - yes_n} "
          f"universe={len(items)} by_class={by_class}")
    print(f"set_sha256={sha(text)}")
    print(f"per_item_sha256_first_last="
          f"{rows[0]['item_sha256'][:12]}..{rows[-1]['item_sha256'][:12]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
