#!/usr/bin/env python3
"""comic_imaging_probe: the comic as the light maze's imaging mode (moonshot-2, $0, 2026-10-07).

Delta vs sibling probes (comic_spec_probe.py local format door, probe_moonshot_gemma4.py
seat ranking): THIS probe measures CROSS-SEAT AUTHORIAL AGREEMENT. Same session fact,
4 free seats, one typed schema (with the POSE enum stolen from mag_dance POSES per
moonshot-1 M5). If the strips converge on the same facts (digit/keyword overlap) while
style diverges (pose/action spread), the comic page IS a roll-shape fingerprint:
the light maze imaging walkers by their paths (ROLL_SHAPE_TURING_CASTLE_20261007.md:107-111).

12 calls (4 seats x 3 sources), FORMAT-SCHEMA arm only (the door is settled by three
sibling probes), temp 0, urllib only, no subprocess so no CREATE_NO_WINDOW duty.

Scored per row: parseable / schema_ok / pose_ok (enum) / digit_fidelity (which source
digits landed in captions) / keyword_coverage. Cross-seat per source: digit-set Jaccard,
keyword-set Jaccard, mean caption length spread, pose vocabulary spread.
Banked: probe_moonshot2_imaging_results.json beside this file.
"""
import json
import re
import time
import urllib.request
from itertools import combinations

URL = "http://localhost:11434/api/generate"
POSES = ["flail", "kick", "shimmy", "strut", "pointy", "spirit", "stomp"]
SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "panels": {
            "type": "array", "minItems": 3, "maxItems": 4,
            "items": {
                "type": "object",
                "properties": {
                    "who": {"type": "array", "items": {"type": "string",
                             "enum": ["operator", "seat", "janitor", "onlooker"]}},
                    "pose": {"type": "string", "enum": POSES},
                    "action": {"type": "string"},
                    "caption": {"type": "string"},
                },
                "required": ["who", "pose", "action", "caption"],
            },
        },
    },
    "required": ["title", "panels"],
}

SOURCES = [
    ("gauntlet-selfstrike",
     "Session fact: the free-lane grader's first regex required an 'ms' suffix "
     "the format never mandated. Mistral returned a perfect half-beat grid at "
     "243.8 with no unit and graded 0/4 parseable. Caught by byte-reading; the "
     "regex was fixed and corrected rows appended.",
     ["regex", "grid", "ms", "graded", "parseable"]),
    ("merkle-collision",
     "Session fact: arrays [a,b,c] and [a,b,c,c] share root 922f2912 via "
     "odd-level last-node duplication in verkle_knot.py line 216. Content "
     "forgery stays blocked by leaf-domain separation; the severity is "
     "trailing-duplicate length ambiguity.",
     ["root", "duplicate", "leaf", "verkle", "blocked"]),
    ("gstd-wallet-gate",
     "Session fact: the fleet provider live --cycle run with zero wallets "
     "exited code 3 WALLET GATE BLOCKED with zero network calls. The no-live-"
     "submits law proven on-box; 13 tests passed.",
     ["wallet", "gate", "cycle", "exit", "network"]),
]
PROMPT = ("You draw a minimal stick-figure comic (xkcd style) of an agent-estate "
          "work session. Read this session fact: {fact}\n"
          "Reply with ONLY a JSON object: {{\"title\": string, \"panels\": array of "
          "3 to 4 items, each {{\"who\": array of one or more of operator|seat|"
          "janitor|onlooker, \"pose\": one of flail|kick|shimmy|strut|pointy|spirit|"
          "stomp, \"action\": short verb phrase, \"caption\": the panel's punchline "
          "or narration, under 140 chars}}}}. No markdown.")


def ask(model, prompt, timeout=300):
    body = {"model": model, "prompt": prompt, "stream": False, "temperature": 0,
            "options": {"num_predict": 400}, "format": SCHEMA}
    req = urllib.request.Request(
        URL, data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return str(json.loads(r.read().decode("utf-8")).get("response", ""))
    except Exception as e:
        return "PROBE_ERROR: " + type(e).__name__ + ": " + str(e)[:80]


def jaccard(a, b):
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def score(text, src_digits, keywords):
    row = {"parseable": False, "schema_ok": False, "pose_ok": False,
           "caption_digits": [], "keywords_hit": [], "caption_lens": [],
           "poses_used": []}
    obj = None
    try:
        obj = json.loads(text)
        row["parseable"] = True
    except Exception:
        m = re.search(r"\{.*\}", text, re.S)
        if m:
            try:
                obj = json.loads(m.group(0))
                row["parseable"] = True
            except Exception:
                pass
    if not isinstance(obj, dict):
        row["sample"] = text[:120]
        return row
    panels = obj.get("panels")
    if not isinstance(panels, list) or not (3 <= len(panels) <= 4):
        row["sample"] = str(obj)[:120]
        return row
    ok, poses_ok = True, True
    caps = []
    for p in panels:
        if not isinstance(p, dict):
            ok = False
            break
        who = p.get("who")
        cap = str(p.get("caption") or "")
        pose = p.get("pose")
        caps.append(cap)
        row["poses_used"].append(str(pose))
        if pose not in POSES:
            poses_ok = False
        if (not isinstance(who, list) or not who or not cap.strip()):
            ok = False
            break
    row["sample"] = str(obj)[:150]
    if not ok:
        return row
    row["schema_ok"] = True
    row["pose_ok"] = poses_ok
    joined = " | ".join(caps)
    row["caption_digits"] = sorted(set(re.findall(r"\d+", joined)) & src_digits)
    row["keywords_hit"] = [k for k in keywords if k.lower() in joined.lower()]
    row["caption_lens"] = [len(c) for c in caps]
    return row


def main():
    seats = ["gemma:2b", "qwen2.5:3b-instruct", "qwen2.5:7b", "gemma4:latest"]
    out = {"schema": "comic_imaging_probe.v1", "rows": [], "summary": {},
           "agreement": {}}
    for seat in seats:
        hits = {"parseable": 0, "schema_ok": 0, "pose_ok": 0, "n": 0}
        for sid, fact, kws in SOURCES:
            text = ask(seat, PROMPT.format(fact=fact))
            r = score(text, set(re.findall(r"\d+", fact)), kws)
            r.update({"seat": seat, "source": sid})
            out["rows"].append(r)
            hits["parseable"] += 1 if r["parseable"] else 0
            hits["schema_ok"] += 1 if r["schema_ok"] else 0
            hits["pose_ok"] += 1 if r["pose_ok"] else 0
            hits["n"] += 1
            time.sleep(1.0)
        out["summary"][seat] = dict(hits)
        print(seat, hits, flush=True)
    # cross-seat agreement per source: do the seats image the SAME facts?
    for sid, fact, kws in SOURCES:
        per = [r for r in out["rows"] if r["source"] == sid and r["schema_ok"]]
        digit_js, kw_js = [], []
        for a, b in combinations(per, 2):
            da = {d for d in a["caption_digits"]}
            db = {d for d in b["caption_digits"]}
            digit_js.append(round(jaccard(da, db), 2))
            ka, kb = set(a["keywords_hit"]), set(b["keywords_hit"])
            kw_js.append(round(jaccard(ka, kb), 2))
        all_poses = sorted({p for r in per for p in r["poses_used"]})
        out["agreement"][sid] = {
            "seats_ok": len(per),
            "digit_jaccard_pairs": digit_js,
            "keyword_jaccard_pairs": kw_js,
            "mean_digit_jaccard": (round(sum(digit_js) / len(digit_js), 3)
                                   if digit_js else None),
            "mean_keyword_jaccard": (round(sum(kw_js) / len(kw_js), 3)
                                     if kw_js else None),
            "pose_vocab_across_seats": all_poses,
        }
        print(sid, out["agreement"][sid], flush=True)
    path = ("watch/inbox/ractor_engine/2026-10-07-stupidmodel-comics/"
            "probe_moonshot2_imaging_results.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("BANKED", path)


if __name__ == "__main__":
    main()
