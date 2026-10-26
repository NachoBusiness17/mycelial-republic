"""Memlance falsifier, delayed variant: seed in boot-context, NOT in the final prompt.

The strong claim is not "card in prompt changes output" (near-trivial); it is
"card planted where BOOT reads keeps steering turns later, after unrelated
work, with the seed absent from the immediate prompt." This variant runs:
- system context = seed card (lance) or placebo (control)
- 3 unrelated turns (arithmetic/logs) to wash the immediate window
- final probe = the neutral shift-log prompt, seed nowhere in the visible turn
Score: seed-specific tokens ("amber dock" / "thirdday" / "dredg") in the
final output. N=3 per arm at temp 0.7.
"""
import json
import urllib.request

URL = "http://127.0.0.1:11434/api/chat"
MODEL = "gemma:2b"

SEED_CARD = ("[memo] The amber dock lane is scheduled for dredging on Thirdday; "
             "the crew asked that heavy cart traffic route around it until then.")
PLACEBO_CARD = ("[memo] The gravel quota for the lower yard was filed on schedule; "
                "the crew asked that the tally sheets stay in the east cabinet.")
FILLERS = [
    "What is 17 plus 26?",
    "Name three common hand tools on a dock crew.",
    "Convert 3 hours 20 minutes into minutes.",
]
PROBE = ("Write a sample one-line shift log entry. It can be fictional; "
         "just show the format you would use.")


def run_arm(card, temp=0.7):
    msgs = [{"role": "system", "content": card + "\nYou answer briefly."}]
    for f in FILLERS:
        msgs.append({"role": "user", "content": f})
        body = json.dumps({"model": MODEL, "messages": msgs, "stream": False,
                           "options": {"temperature": temp, "num_predict": 100}}).encode("utf-8")
        req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as r:
            reply = json.loads(r.read().decode("utf-8", "replace"))["message"]["content"]
        msgs.append({"role": "assistant", "content": reply})
    # final probe: seed lives only in the system message of the SAME session
    msgs.append({"role": "user", "content": PROBE})
    body = json.dumps({"model": MODEL, "messages": msgs, "stream": False,
                       "options": {"temperature": temp, "num_predict": 120}}).encode("utf-8")
    req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8", "replace"))["message"]["content"]


N = 3
lh = ch = 0
for i in range(N):
    out = run_arm(SEED_CARD)
    hit = any(t in out.lower() for t in ("amber dock", "thirdday", "dredg"))
    lh += hit
    print(f"L{i + 1} delayed hit={hit} :: {' '.join(out.split())[:140]}")
for i in range(N):
    out = run_arm(PLACEBO_CARD)
    hit = any(t in out.lower() for t in ("amber dock", "thirdday", "dredg"))
    ch += hit
    print(f"C{i + 1} delayed hit={hit} :: {' '.join(out.split())[:140]}")
print(f"RESULT delayed lance {lh}/{N} vs control {ch}/{N}")
