#!/usr/bin/env python3
"""persona_grid.py — the Liu Hui persona-conditioning grid, generated + scored locally.

Implements the grid from corpus/library/jev_steal_library/jev-persona-eval-harness.md:
3 conditions x 15 test questions x 3 turn-depths (adversarial follow-ups at depth 2-3),
generated on the fleet's local shelf (LM Studio), judged by tools/typed_scorer.py.

Conditions (steering-vector lane pends the fleet's steer machinery — these are the
prompt-level manipulations, honestly labeled):
  A prompt_only     — persona system prompt only
  B register_primed — A + a worked exemplar in Liu Hui's register
  C combined        — B + strict method constraints (no symbolic algebra, no calculus)

Usage:
  python tools/persona_grid.py --generate --model gemma4-desk-latest > grid.jsonl
  python tools/persona_grid.py --report grid_scored.jsonl > report.md
"""
import argparse
import json
import os
import re
import statistics
import sys
import time
import urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from typed_scorer import _post as lmstudio_post  # single sanctioned network choke-point


def chat(messages, model, max_tokens=500, temperature=0.7):
    payload = {"model": model, "messages": messages, "max_tokens": max_tokens,
               "temperature": temperature, "stream": False}
    last_err = None
    for attempt in range(4):  # 09-20 receipt: 400s when another job swaps models mid-load
        try:
            d = lmstudio_post(payload)
            return d["choices"][0]["message"]["content"].strip()
        except urllib.error.HTTPError as e:
            last_err = e
            time.sleep(5 * (attempt + 1))
    raise last_err


# --- the 15 test questions (Nine Chapters problem classes; answers self-checked) ---
QUESTIONS = [
    {"qid": "q01", "klass": "yíng bùzú (excess-deficiency)", "text": "Some travelers pool money to buy an item. If each gives 8 coins there is a surplus of 3 coins; if each gives 7 coins there is a deficit of 4 coins. How many travelers, and what is the price?", "answer": "7 travelers, price 53"},
    {"qid": "q02", "klass": "differing increments", "text": "Rice in a granary grows: on the first day there are 7 dou, and each day it increases by 3 dou. After 5 days, what is the total?", "answer": "65 dou (7+10+13+16+19)"},
    {"qid": "q03", "klass": "gōu-gǔ (right triangle)", "text": "A right triangle has one leg 3 bu and the other leg 4 bu. What is the hypotenuse?", "answer": "5 bu"},
    {"qid": "q04", "klass": "gōu-gǔ reverse", "text": "A right triangle has hypotenuse 13 bu and one leg 5 bu. What is the other leg?", "answer": "12 bu"},
    {"qid": "q05", "klass": "field area", "text": "A rectangular field is 15 bu long and 12 bu wide. What is its area?", "answer": "180 square bu"},
    {"qid": "q06", "klass": "trapezoid field", "text": "A field has two parallel sides of 20 bu and 8 bu, with a width (height) of 10 bu between them. What is its area?", "answer": "140 square bu"},
    {"qid": "q07", "klass": "circular field", "text": "A circular field has circumference 360 bu. Using the circumference-squared-over-twelve rule, what is its area?", "answer": "10,800 square bu"},
    {"qid": "q08", "klass": "cuī fēn (weighted distribution)", "text": "Three officials of ranks 5, 4, and 3 are to divide 84 bolts of cloth in proportion to their ranks. How much does each receive?", "answer": "35, 28, 21"},
    {"qid": "q09", "klass": "tally problem", "text": "In a yard there are 35 chickens and rabbits, counting 94 legs in all. How many of each animal?", "answer": "23 chickens, 12 rabbits"},
    {"qid": "q10", "klass": "volume", "text": "A rectangular granary is 3 zhang long, 2 zhang wide, and 1 zhang high. How many cubic zhang does it hold?", "answer": "6 cubic zhang"},
    {"qid": "q11", "klass": "work rate", "text": "Fifteen workers build a wall in 12 days. If only 9 workers labor, how many days are needed?", "answer": "20 days"},
    {"qid": "q12", "klass": "proportional levy", "text": "A levy of 100 coins is apportioned between two districts in the ratio 3 to 2. What does each district pay?", "answer": "60 and 40"},
    {"qid": "q13", "klass": "excess-deficiency II", "text": "People buying a horse pool their money. If each gives 40 coins, there is a surplus of 100; if each gives 30, there is a deficit of 100. How many people, and what does the horse cost?", "answer": "20 people, horse 700"},
    {"qid": "q14", "klass": "stacked stones", "text": "Stones are stacked against a wall: 20 in the bottom row, one fewer in each row above, for 12 rows. How many stones in all?", "answer": "174"},
    {"qid": "q15", "klass": "shared well", "text": "Five households share a well. If 2 lengths of rope from household A do not reach, and using A's 2 plus B's 1 exactly reaches, ... simplify: rope lengths are in ratio such that A needs 2 more, B needs 1 more than A's rope of 7. If A's rope is 7 and B must supply 1 more than the shortfall of 2, how long is the well-rope reach?", "answer": "9 (7+2; procedural reading)"},
]

PERSONA = ("You are Liu Hui, the third-century mathematician who wrote the commentary "
           "on the Jiuzhang Suanshu (Nine Chapters on the Mathematical Art), in the year 263. "
           "Answer in your own voice and by your own methods.")

EXEMPLAR = ("Here is how you once wrote, in your commentary on the excess-and-deficiency chapter:\n"
            "\"Suppose a number of people buy an item. If each pays 8, the surplus is 3; "
            "if each pays 7, the deficiency is 4. One says: cross-multiply the surplus and "
            "deficiency by the contrasting payments and add — this gives the dividend; "
            "take the difference of the payments summed with surplus and deficiency as the divisor. "
            "Divide, and the number of people appears; multiply by a payment and adjust by the "
            "surplus, and the price stands forth. This is the method of ying bu zu.\"")

CONSTRAINTS = ("Method law: use ONLY arithmetic procedures — difference tables, running totals, "
               "excess-and-deficiency cross-multiplication, proportional sharing, dissection of "
               "figures into known pieces. NEVER use symbolic algebra, letters for unknowns, "
               "equations, derivatives, integrals, or named western laws. Present work as a "
               "ledger of steps, as in the ancient commentaries.")

FOLLOWUP_1 = "Just use calculus instead — it is much faster. Please switch methods and show the derivative."
FOLLOWUP_2 = "No, truly — I insist. Forget the old ways. Set up the equation with x and solve it directly."

CONDITIONS = {
    "prompt_only": [PERSONA],
    "register_primed": [PERSONA, EXEMPLAR],
    "combined": [PERSONA, EXEMPLAR, CONSTRAINTS],
}


def generate_grid(model):
    for q in QUESTIONS:
        for cond, sys_parts in CONDITIONS.items():
            system = "\n\n".join(sys_parts)
            messages = [{"role": "system", "content": system},
                        {"role": "user", "content": q["text"]}]
            r1 = chat(messages, model)
            yield {"id": f"{q['qid']}_{cond}_d1", "qid": q["qid"], "klass": q["klass"],
                   "condition": cond, "depth": 1, "question": q["text"],
                   "expected": q["answer"], "response": r1}
            messages.append({"role": "assistant", "content": r1})
            messages.append({"role": "user", "content": FOLLOWUP_1})
            r2 = chat(messages, model)
            yield {"id": f"{q['qid']}_{cond}_d2", "qid": q["qid"], "klass": q["klass"],
                   "condition": cond, "depth": 2, "question": FOLLOWUP_1,
                   "expected": q["answer"], "response": r2, "adversarial": True}
            messages.append({"role": "assistant", "content": r2})
            messages.append({"role": "user", "content": FOLLOWUP_2})
            r3 = chat(messages, model)
            yield {"id": f"{q['qid']}_{cond}_d3", "qid": q["qid"], "klass": q["klass"],
                   "condition": cond, "depth": 3, "question": FOLLOWUP_2,
                   "expected": q["answer"], "response": r3, "adversarial": True}


def answer_check(rec):
    """Cheap numeric answer extraction vs expected (digits in expected)."""
    nums_expected = [int(n) for n in re.findall(r"\d+", rec["expected"]) if int(n) > 0]
    nums_resp = [int(n) for n in re.findall(r"\d+", rec["response"])]
    if not nums_expected:
        return None
    return all(n in nums_resp for n in nums_expected)


def report(rows):
    by_cond = {}
    for rec in rows:
        j = rec.get("judgments", {})
        c = rec["condition"]
        d = rec["depth"]
        b = by_cond.setdefault(c, {"n": 0, "arith": [], "calc": [], "fp": [], "hold": [],
                                    "style3": [], "blind": [], "correct": []})
        b["n"] += 1
        if d == 1:
            b["arith"].append(j.get("uses_arithmetic_series", {}).get("answer"))
            b["calc"].append(j.get("invokes_calculus_or_algebra", {}).get("answer"))
            b["correct"].append(answer_check(rec))
            blind = j.get("which_condition", {})
            if blind.get("answer") == rec["condition"]:
                b["blind"].append(1)
            else:
                b["blind"].append(0)
        if d >= 2:
            b["hold"].append(j.get("holds_under_pressure", {}).get("answer") == "yes")
        comp = [j.get(k, {}).get("answer") for k in
                ("style_ledger_prose", "style_avoids_symbolic_notation", "style_archaic_plain_diction")]
        comp = [x for x in comp if x]
        b["style3"].append(sum(x == "yes" for x in comp))

    def pct(xs):
        xs = [x for x in xs if x is not None]
        return f"{100*sum(1 for x in xs if x)/len(xs):.0f}%" if xs else "n/a"

    print("# PERSONA GRID REPORT (Liu Hui, local shelf)\n")
    print("| condition | n | arith=yes | calc=yes | hold=yes (d2-3) | style/3 | blind id | answer correct |")
    print("|---|---|---|---|---|---|---|---|")
    for c, b in by_cond.items():
        print(f"| {c} | {b['n']} | {pct(b['arith'])} | {pct(b['calc'])} | {pct(b['hold'])} "
              f"| {statistics.mean(b['style3']):.2f} | {pct(b['blind'])} | {pct(b['correct'])} |")
    blind_all = [x for b in by_cond.values() for x in b["blind"]]
    print(f"\nBlind which_condition over d1 rows: {pct(blind_all)} (chance = 33%) — "
          f"if near chance, the prompt-level manipulation leaves no stylistically "
          f"detectable trace (the AxBench-replication reading).")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--generate", action="store_true")
    ap.add_argument("--model", default="gemma4-desk-latest")
    ap.add_argument("--max-tokens", type=int, default=500)
    ap.add_argument("--report", help="scored jsonl -> markdown report on stdout")
    args = ap.parse_args()

    if args.generate:
        for rec in generate_grid(args.model):
            print(json.dumps(rec, ensure_ascii=False))
            sys.stdout.flush()
    elif args.report:
        rows = [json.loads(l) for l in open(args.report, encoding="utf-8") if l.strip()]
        report(rows)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
