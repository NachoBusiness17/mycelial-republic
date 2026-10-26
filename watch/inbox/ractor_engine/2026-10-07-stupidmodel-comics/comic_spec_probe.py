#!/usr/bin/env python3
"""comic_spec_probe: the stupid-model comics falsifier (pilot, $0 local, 2026-10-07).

Ask: can the free seats emit valid xkcd-minimal panel specs through the
format-schema door (the M1 grammar-bench shape, tools/m1_grammar_bench.py),
scored mechanically: parseable / in-character / minimal?

Shape: 3 local seats x 2 arms (UNCONSTRAINED vs FORMAT-SCHEMA) x 3 session
excerpts = 18 calls, temperature 0, /api/generate non-stream, urllib (no
subprocess, so no CREATE_NO_WINDOW duty). PILOT SCALE, honestly narrower than
the m1 30-prompt bench; the full trial rides the gauntlet feeder once fire()
carries the format door.

Scored:
  parseable   - strict json.loads OR one {...} regex extract (m1 rule)
  schema_ok   - 3..4 panels; who subset of VOCAB; every caption non-empty
  in_character- >=1 caption carries a digit that appears in the source AND
                >=1 keyword from the source keyword list (fidelity to session)
  minimal     - every caption <= 140 chars
Banked: watch/inbox/ractor_engine/2026-10-07-stupidmodel-comics/comic_spec_probe.json
"""
import json
import re
import time
import urllib.request

URL = "http://localhost:11434/api/generate"
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
                    "action": {"type": "string"},
                    "caption": {"type": "string"},
                },
                "required": ["who", "action", "caption"],
            },
        },
    },
    "required": ["title", "panels"],
}
VOCAB = {"operator", "seat", "janitor", "onlooker"}

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
          "janitor|onlooker, \"action\": short verb phrase, \"caption\": the "
          "panel's punchline or narration, under 140 chars}}}}. No markdown.")


def ask(model, prompt, schema, timeout=240):
    body = {"model": model, "prompt": prompt, "stream": False, "temperature": 0,
            "options": {"num_predict": 350}}
    if schema:
        body["format"] = schema
    req = urllib.request.Request(
        URL, data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return str(json.loads(r.read().decode("utf-8")).get("response", ""))
    except Exception as e:
        return "PROBE_ERROR: " + type(e).__name__ + ": " + str(e)[:80]


def score(text, src_digits, keywords):
    row = {"parseable": False, "schema_ok": False, "in_character": False,
           "minimal": False}
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
        return row, (obj if obj is not None else text)[:120]
    panels = obj.get("panels")
    if not isinstance(panels, list) or not (3 <= len(panels) <= 4):
        return row, str(obj)[:120]
    ok = True
    caps = []
    for p in panels:
        if not isinstance(p, dict):
            ok = False
            break
        who = p.get("who")
        cap = str(p.get("caption") or "")
        caps.append(cap)
        if (not isinstance(who, list) or not who
                or not set(map(str, who)) <= VOCAB or not cap.strip()):
            ok = False
            break
    if not ok:
        return row, str(obj)[:120]
    row["schema_ok"] = True
    joined = " | ".join(caps)
    digits = set(re.findall(r"\d+", joined))
    row["in_character"] = bool(digits & src_digits) and any(
        k.lower() in joined.lower() for k in keywords)
    row["minimal"] = all(len(c) <= 140 for c in caps)
    return row, str(obj)[:120]


def main():
    seats = ["gemma:2b", "qwen2.5:7b", "qwen2.5:3b-instruct"]
    out = {"schema": "comic_spec_probe.v1", "rows": [], "summary": {}}
    for seat in seats:
        for arm, schema in (("UNCONSTRAINED", None), ("FORMAT-SCHEMA", SCHEMA)):
            hits = {"parseable": 0, "schema_ok": 0, "in_character": 0,
                    "minimal": 0}
            for sid, fact, kws in SOURCES:
                text = ask(seat, PROMPT.format(fact=fact), schema)
                r, sample = score(text, set(re.findall(r"\d+", fact)), kws)
                for k in hits:
                    hits[k] += 1 if r[k] else 0
                out["rows"].append({"seat": seat, "arm": arm, "source": sid,
                                    **r, "sample": sample[:160]})
                time.sleep(1.0)
            out["summary"][seat + " | " + arm] = dict(
                hits, n=len(SOURCES))
            print(seat, arm, hits, flush=True)
    path = ("watch/inbox/ractor_engine/2026-10-07-stupidmodel-comics/"
            "comic_spec_probe.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("BANKED", path)


if __name__ == "__main__":
    main()
