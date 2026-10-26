#!/usr/bin/env python3
"""break-logic replication rerun of the comic_spec probe (hostile pass, 2026-10-07).

Imports the banked probe module verbatim (same SCHEMA / SOURCES / PROMPT /
scoring) and re-fires only the claims that carry the logic lens's findings:
  - gemma:2b both arms (the 0/3 -> 3/3 schema_ok flip, finding 2)
  - gemma4:latest FORMAT-SCHEMA arm (the headline perfect 3/3, finding 2;
    the banked rows for this arm carry no `sample` field, so this rerun is
    the first banked-script reproduction of that arm)
Writes ONLY to break_logic_rerun.json; never touches comic_spec_probe.json.
urllib only, no subprocess (no CREATE_NO_WINDOW duty). $0 local ollama.
"""
import json
import re
import sys
import time

DIR = ("watch/inbox/ractor_engine/2026-10-07-stupidmodel-comics")
sys.path.insert(0, DIR)
import comic_spec_probe as csp  # noqa: E402

ROWS = []
SUMMARY = {}
PLAN = [
    ("gemma:2b", "UNCONSTRAINED", None),
    ("gemma:2b", "FORMAT-SCHEMA", csp.SCHEMA),
    ("gemma4:latest", "FORMAT-SCHEMA", csp.SCHEMA),
]

for seat, arm, schema in PLAN:
    hits = {"parseable": 0, "schema_ok": 0, "in_character": 0, "minimal": 0}
    for sid, fact, kws in csp.SOURCES:
        t0 = time.time()
        text = csp.ask(seat, csp.PROMPT.format(fact=fact), schema)
        r, sample = csp.score(text, set(re.findall(r"\d+", fact)), kws)
        r["elapsed_s"] = round(time.time() - t0, 1)
        for k in hits:
            hits[k] += 1 if r[k] else 0
        ROWS.append({"seat": seat, "arm": arm, "source": sid, **r,
                     "sample": sample[:160]})
        print(seat, arm, sid, r, flush=True)
        time.sleep(1.0)
    SUMMARY[seat + " | " + arm] = dict(hits, n=len(csp.SOURCES))

out = {"schema": "break_logic_rerun.v1", "rows": ROWS, "summary": SUMMARY,
       "note": "replication of comic_spec_probe claims, banked-script import"}
with open(DIR + "/break_logic_rerun.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print("BANKED", DIR + "/break_logic_rerun.json")
print(json.dumps(SUMMARY, indent=1))
