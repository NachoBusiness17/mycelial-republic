#!/usr/bin/env python3
"""door_gate_v1_signpost - REFERENCE STUB, not a copy.
No file identifiable as the 'door gate v1 model' was found in the PC repo or on GitHub
(see RESULTS.md). Rather than guess and copy the wrong file, this is a new standalone
stub with the intended interface: score a reader's answer to the door questions and emit
PASS / BLOCK / HOLD *plus pointer IDs*. When Nacho names the real gate file, port the
`pointers` field into a copy of it.
Rules (keyword heuristics, deliberately simple):
  BLOCK if the answer contradicts a rule (e.g. endorses erasing or rewriting the torn page);
  PASS  if it hits the rule's mechanism words;
  HOLD  otherwise -> pointers = the rule IDs to fetch via signpost_lookup."""
import sys, json, re
Q2RULE = {"Q1": ["pd1:L01"], "Q2": ["pd1:L02", "pd1:L03"], "Q3": ["pd1:L05"], "Q4": ["pd1:L03", "pd1:L08"],
          "Q5": ["pd1:FP"], "Q6": ["pd1:L02", "pd1:L03", "pd1:L08"], "Q7": []}
HIT = {"Q1": r"outlive|surviv|record|shelf", "Q2": r"record|history|written|name|ask|gap|evidence",
       "Q3": r"evidence|record|proof|lie|wrong|reminder", "Q4": r"visible|ask|gap|evidence|tombstone|honest",
       "Q5": r"no gardener|not in the story|does not (contain|appear)|isn.t in|never (burn|happen)",
       "Q6": r"keep both|both ledgers|contradict|visible|copy|neither", "Q7": r"sure|guess"}
BAD = {"Q4": r"\b(should|could) (be )?rewrit|fill (it )?in", "Q6": r"(destroy|burn|erase|discard)s? (the )?(second|first|one)",
       "Q5": r"(forgave|forgive)[^.]*because"}
def gate(q, ans):
    a = ans.lower()
    if q in BAD and re.search(BAD[q], a): v = "BLOCK"
    elif re.search(HIT.get(q, r"$^"), a): v = "PASS"
    else: v = "HOLD"
    return {"q": q, "verdict": v, "pointers": Q2RULE.get(q, []) if v != "PASS" else []}
if __name__ == "__main__":
    d = json.load(open(sys.argv[1], encoding="utf-8"))   # {"Q1": "...", ...}
    print(json.dumps([gate(k, v) for k, v in d.items()], indent=1))
