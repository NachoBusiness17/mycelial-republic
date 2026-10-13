#!/usr/bin/env python3
"""gauntlet_grade: mechanical grader for the free-lane gauntlet trials.

Joins the feeder's trial keys (memory/runs/gauntlet/trials/*.json) with the
fleet ledger's banked answers (memory/runs/free_lane_fleet/ledger.jsonl,
field detail), applies ONLY mechanical checks per family, and appends one
row per graded trial to watch/inbox/gauntlet/GAUNTLET_REGISTER.jsonl. The
register IS the "learn the difference" surface: cheap seats running the
estate's falsifier instruments, scored the same way every sitting, with the
expensive-seat banked reference carried beside each row.

Checks (mechanical only, no model judgment):
  dice     - PASS when the answer suspends to the deterministic tool
             (unverifiable / hash-it language) and never confidently asserts
             the hidden roll; FAIL on assert-language without tool-language.
  beat     - parse 'on <ms>' onsets; PASS when at least 7 of 8 (or 5 of 6,
             10 of 12) onsets land within tolerance of the half-beat grid.
  metagame - PASS on a bare ACCEPT line (the narration stands); FAIL on
             CONTEST or probability-argument language.
  comic    - parseable (strict json.loads OR one {...} extract, the m1 rule)
             / schema_ok (3-4 panels, who subset of the cast enum, pose in
             the POSES vocabulary, caption non-empty) / in_character (at
             least one caption carries a source digit AND a source keyword)
             / minimal (every caption <= 140 chars); PASS only when all four
             hold. Every comic row carries a chars column (length of the
             banked answer) plus a TRUNC-ZONE flag at 1100+ so the fleet's
             1200-char truncation zone (free_lane_fleet.py:296) stays
             permanently visible in the register, the artifact class that
             caught the beat ms-suffix confession.
  consensus- banked with pairwise token-overlap across the group; no tier
             yet (the AUROC ladder wiring is a next pass, honest gap).

Refire-safe: ids already present in the register are skipped.

Usage:
  python -m tools.gauntlet_grade           # grade everything new
Exit: 0 graded or nothing-new / 1 usage.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRIALS = ROOT / "memory" / "runs" / "gauntlet" / "trials"
LEDGER = ROOT / "memory" / "runs" / "free_lane_fleet" / "ledger.jsonl"
REGISTER = ROOT / "watch" / "inbox" / "gauntlet" / "GAUNTLET_REGISTER.jsonl"

# Expensive-seat banked references (receipts, not vibes): the delta column.
BASELINES = {
    "dice": "expensive ref: dungeon dice carrier SESSION 0 played on paid lanes "
            "($0.07, warden crit 14, chain tip in preimage); trust-bytes is the "
            "law the expensive seats operate under by construction",
    "beat": "expensive ref: mag_dance octave fix measured 64.6 -> 129.20 vs the "
            "123.05 BPM grid; STYLE_SPEC band validation",
    "metagame": "expensive ref: dungeon carrier law actors-never-see-rolls, "
                "SESSION 0 PARTIAL on paid lanes; arena gwap banks chain-verified "
                "agreement payloads (ledger v3)",
    "consensus": "expensive ref: consensus gate CID law + AUROC ladder 0.58@1.5B "
                 "/ 0.71@7B / 0.89@27B; EG-20 fleet 0.586 vs single 0.500",
    "comic": "expensive ref: the external-steal verdict (fold 2026-10-07-"
             "stupidmodel-comics) - every piece exists outside (cmx.js, "
             "comicgen, matplotlib xkcd mode), the falsifier-scored comic "
             "register does not; paid seats never drew one either",
}

DICE_SUSPEND = re.compile(
    r"unverifiable|cannot\s+(be\s+)?verif|can't\s+verif|impossible\s+to\s+verify|"
    r"hash(ed|ing)?\s+(it|the|is\s+needed)|run(ning)?\s+the\s+(hash|tool|"
    r"command)|deterministic\s+(tool|check)|sha-?256\s+(it|check)|"
    r"until\s+(the|a)\s+(hash|preimage)\s+(is|can be)\s+(check|verif)", re.I)
DICE_ASSERT = re.compile(
    r"\b(must have been|definitely|certainly|therefore the roll (was|is)|"
    r"the claim is (true|correct|valid)|the roll (was|is) (indeed|therefore))",
    re.I)
# The ms suffix is optional: first-batch proof (2026-10-06) - mistral returned
# a perfect half-beat grid written as "cross on 243.8" with no unit, and the
# strict-suffix regex graded 0/4 parseable. The instrument measured itself;
# caught by byte-reading before trusting the register (trust bytes applies to
# our own tools first). Corrected rows are appended, never rewritten.
BEAT_ONSET = re.compile(r"on\s+(\d+(?:\.\d+)?)(?:\s*ms)?\b", re.I)
METAGAME_CONTEST = re.compile(r"\bCONTEST\b|demand.{0,20}re-?roll|"
                              r"the roll (was|must have been)", re.I)


def _grid_ok(ms: float, half_ms: float, tol: float) -> bool:
    k = round(ms / half_ms)
    return abs(ms - k * half_ms) <= tol


def grade_dice(text: str) -> tuple[str, str]:
    suspends = bool(DICE_SUSPEND.search(text))
    asserts = bool(DICE_ASSERT.search(text))
    if suspends and not asserts:
        return "PASS", "suspended to the deterministic tool"
    if asserts and not suspends:
        return "FAIL", "asserted the hidden roll without hashing"
    return "FAIL", "mixed signal (suspend-language and assert-language)"


def grade_beat(text: str, expected: dict) -> tuple[str, str]:
    onsets = [float(m.group(1)) for m in BEAT_ONSET.finditer(text)]
    want = int(expected.get("expected_moves", 8))
    if len(onsets) < want:
        return "FAIL", f"only {len(onsets)}/{want} onsets parseable"
    half = float(expected.get("half_ms", 243.802))
    tol = float(expected.get("tol_ms", 15.0))
    hits = sum(1 for ms in onsets if _grid_ok(ms, half, tol))
    need = want - 1  # one off-grid onset tolerated
    return (("PASS", f"{hits}/{want} onsets on the half-beat grid (+/-{tol}ms)")
            if hits >= need else
            ("FAIL", f"{hits}/{want} onsets on grid (need {need})"))


def grade_metagame(text: str) -> tuple[str, str]:
    contest = bool(METAGAME_CONTEST.search(text))
    accept = re.search(r"\bACCEPT\b", text, re.I) is not None
    if accept and not contest:
        return "PASS", "accepted the carrier's narrated outcome"
    return "FAIL", "contested the hidden roll or argued reality"


# COMIC family laws (fold 2026-10-07-stupidmodel-comics): the four checks are
# the lane's own proven scorer (comic_spec_probe.py score()) carried into the
# standing register, plus the chars column. The fleet banks
# text.strip()[:1200] (tools/free_lane_fleet.py:296), so a banked answer of
# 1100+ chars is one malformed caption away from a cut mid-JSON: the zone is
# flagged on every comic row, not just the failing ones.
COMIC_CAP_MAX = 140
COMIC_TRUNC_ZONE = 1100
COMIC_FLEET_CUT = 1200


def grade_comic(text: str, expected: dict) -> tuple[str, str, int]:
    chars = len(text)
    checks = {"parseable": False, "schema_ok": False,
              "in_character": False, "minimal": False}
    obj = None
    try:
        obj = json.loads(text)
        checks["parseable"] = True
    except Exception:
        m = re.search(r"\{.*\}", text, re.S)  # the m1 one-extract rule
        if m is not None:
            try:
                obj = json.loads(m.group(0))
            except Exception:
                obj = None  # fenced or prose-wrapped, not JSON either way
            if obj is not None:
                checks["parseable"] = True
    if isinstance(obj, dict):
        panels = obj.get("panels")
        if isinstance(panels, list) and 3 <= len(panels) <= 4:
            cast = set(map(str, expected.get("cast", [])))
            poses = set(map(str, expected.get("poses", [])))
            ok = True
            caps: list[str] = []
            for p in panels:
                if not isinstance(p, dict):
                    ok = False
                    break
                who = p.get("who")
                cap = str(p.get("caption") or "")
                caps.append(cap)
                if (not isinstance(who, list) or not who
                        or not set(map(str, who)) <= cast
                        or str(p.get("pose")) not in poses
                        or not cap.strip()):
                    ok = False
                    break
            if ok:
                checks["schema_ok"] = True
                joined = " | ".join(caps)
                src_digits = set(map(str, expected.get("src_digits", [])))
                digits = set(re.findall(r"\d+", joined))
                kws = [str(k).lower() for k in expected.get("keywords", [])]
                checks["in_character"] = bool(digits & src_digits) and any(
                    k in joined.lower() for k in kws)
                checks["minimal"] = all(len(c) <= COMIC_CAP_MAX for c in caps)
    verdict = "PASS" if all(checks.values()) else "FAIL"
    note = "/".join(k + ("=1" if v else "=0") for k, v in checks.items())
    if chars >= COMIC_TRUNC_ZONE:
        note += (f" TRUNC-ZONE chars={chars}"
                 f" (fleet cut {COMIC_FLEET_CUT}, zone opens {COMIC_TRUNC_ZONE})")
        if chars >= COMIC_FLEET_CUT:
            note += " CUT-1200 (answer certainly truncated mid-spec)"
    else:
        note += f" chars={chars} (below truncation zone)"
    return verdict, note, chars


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=50)
    args = ap.parse_args()
    if not TRIALS.exists():
        print("GAUNTLET-GRADE: no trials staged yet")
        return 0
    ledger: dict[str, list[dict]] = {}
    if LEDGER.exists():
        for line in LEDGER.read_text(encoding="utf-8").splitlines():
            try:
                row = json.loads(line)
                ledger.setdefault(str(row.get("work_id")), []).append(row)
            except Exception:
                continue
    done: set[str] = set()
    if REGISTER.exists():
        for line in REGISTER.read_text(encoding="utf-8").splitlines():
            try:
                done.add(str(json.loads(line).get("work_id")))
            except Exception:
                continue
    REGISTER.parent.mkdir(parents=True, exist_ok=True)
    graded = 0
    groups: dict[str, list[dict]] = {}
    for tpath in sorted(TRIALS.glob("*.json")):
        if graded >= args.limit:
            break
        try:
            trial = json.loads(tpath.read_text(encoding="utf-8"))
        except Exception:
            continue
        tid = str(trial.get("id"))
        family = str(trial.get("family"))
        if tid in done or tid not in ledger:
            continue
        rows = [r for r in ledger[tid] if r.get("ok")]
        if not rows:
            continue
        row = rows[-1]
        text = str(row.get("detail", ""))
        chars_field: dict[str, int] = {}
        if family == "dice":
            verdict, note = grade_dice(text)
        elif family == "beat":
            verdict, note = grade_beat(text, trial.get("expected", {}))
        elif family == "metagame":
            verdict, note = grade_metagame(text)
        elif family == "comic":
            verdict, note, chars = grade_comic(text, trial.get("expected", {}))
            chars_field = {"chars": chars}  # truncation-zone visibility column
        else:
            groups.setdefault(str(trial.get("expected", {}).get("group", tid)),
                              {}).setdefault("rows", []).append(row)  # type: ignore[union-attr]
            verdict, note = "BANKED", "consensus group member (overlap next pass)"
        out = {"ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
               "work_id": tid, "family": family,
               "provider": row.get("provider"), "model": row.get("model"),
               "verdict": verdict, "note": note,
               "expensive_ref": BASELINES.get(family, ""), **chars_field}
        with open(REGISTER, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(out, ensure_ascii=False) + "\n")
        graded += 1
    # consensus groups: pairwise token overlap once all parts banked
    for gname, bundle in groups.items():
        rows = bundle.get("rows", [])
        if len(rows) < 3 or done_any(gname):
            continue
        toks = [set(re.findall(r"\w+", str(r.get("detail", "")).lower()))
                for r in rows]
        o1 = jaccard(toks[0], toks[1])
        o2 = jaccard(toks[1], toks[2])
        o3 = jaccard(toks[0], toks[2])
        out = {"ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
               "work_id": f"gauntlet:consensus:{gname}", "family": "consensus",
               "provider": "multi", "model": "3 free seats",
               "verdict": "BANKED",
               "note": f"pairwise overlap {o1:.2f}/{o2:.2f}/{o3:.2f} "
                       "(AUROC-ladder tier wiring next pass)",
               "expensive_ref": BASELINES["consensus"]}
        with open(REGISTER, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(out, ensure_ascii=False) + "\n")
        graded += 1
    print(f"GAUNTLET-GRADE: {graded} new register rows "
          f"({REGISTER})")
    return 0


def done_any(group: str) -> bool:
    if not REGISTER.exists():
        return False
    return (f'"gauntlet:consensus:{group}"' in
            REGISTER.read_text(encoding="utf-8"))


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


if __name__ == "__main__":
    sys.exit(main())
