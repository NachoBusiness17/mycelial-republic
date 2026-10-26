import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, r"C:\Users\foste\Documents\projects\local_sovereign_agent")
from mag.research_fanout import LANES, call_lane, _env

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
BRIEF = (ROOT / "watch/inbox/JEV_CONSOLIDATED_BRIEF_20260919.md").read_text(encoding="utf-8")
OUT = ROOT / "memory" / "runs" / "jev_salon"
OUT.mkdir(parents=True, exist_ok=True)
RAW = OUT / "raw.jsonl"
if RAW.exists():
    RAW.unlink()

LENSES = [
 ("gate_builder", "You build the gate. Questions 1-2: adopt jev-sift/abide now or wait? Which silence-branch default route is correct for a 16-lane fleet? Give verdicts with reasons."),
 ("sovereignty", "You hold the sovereignty ledger. Question 3: ratify or amend the 3pp-threshold rule for local-replica vs hosted-Jev? What is the degraded-metabolism fallback if pricing x10 overnight?"),
 ("question_linter", "You are the question-format linter. Question 4: from the 20-tips spec, extract the lint rules for well-formed oracle questions (atomic, descriptive criteria, no compound, relevant state only) and write them as enforceable rules."),
 ("economist", "You are the economist. Question on cost: given $0.042/MTok and $0.0004/case, compute the fleet's annual oracle bill at current wave volume and say whether hosted or local replica wins under each scenario."),
 ("cryptographer", "You audit provenance. Question 5: Fleet-Bench public feed design — what is safe to publish (measured labels, environments) and what must never leave (negative doctrine, gate backlogs)? Draft the disclosure rule."),
 ("elder", "You are the elder lens. Question 6: ratify or reject the ignorance budget (six-question justification per new distinction) on the amendment gate. What does it break, what does it save?"),
 ("falsifier", "You run falsifiers. Question 7: pre-register the A/B/C ontology-evolution experiment. Write the pre-registration block: conditions, metrics, decision rules, the critical measurement (tasks missing from initial ontology)."),
 ("myth_scholar", "You are the myth scholar. Question 8: give the parable register its story for the steering stack — the GPS satellites, the silence branch, the ignorance budget, the empty chair. One chronicle paragraph per organ, in the riddler register."),
 ("steering", "You are the steering lens. Integrate: given all eight answers, what is the ONE next stone to build this week and what is its falsifier? Be concrete: files, functions, thresholds."),
]

CONTRACT = (" Answer in under 350 words. Be concrete and adversarial: name the strongest "
            "counter-argument to your own verdict in one line marked COUNTER:.")

env = _env()

def run_one(item):
    lens, ask = item
    q = BRIEF[:11000] + "\n\nYOUR LENS: " + lens + ". " + ask + CONTRACT
    idx = hash(lens) % len(LANES)
    order = LANES[idx % len(LANES):] + LANES[:idx % len(LANES)]
    rec = {"lens": lens, "ok": False, "error": "no_lane_key"}
    for lane in order[:6]:
        key = env.get(lane["key"], "")
        if not key:
            continue
        rec = call_lane(lane, q, key, timeout=150, max_tokens=2200)
        rec.update({"lens": lens})
        if rec.get("ok"):
            break
        time.sleep(2)
    with RAW.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(lens, rec.get("ok"), rec.get("lane") or rec.get("error"), flush=True)
    return rec

rows = []
with ThreadPoolExecutor(max_workers=9) as ex:
    futs = [ex.submit(run_one, it) for it in LENSES]
    for f in as_completed(futs):
        rows.append(f.result())
ok = sum(1 for r in rows if r.get("ok"))
with (OUT / "SALON_PACK.md").open("w", encoding="utf-8") as fh:
    fh.write("# JEV SALON PACK — the consolidated brief graded by nine lenses\n\n")
    for r in sorted(rows, key=lambda r: r.get("lens", "")):
        fh.write("\n## %s via %s ok=%s\n" % (r.get("lens"), r.get("lane", "?"), r.get("ok")))
        fh.write(str(r.get("answer", ""))[:3000] + "\n")
print("SALON DONE rows=%d ok=%d" % (len(rows), ok))
