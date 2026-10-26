"""Memlance fired-per-turn falsifier, minimal instrument (descent leg 7, RQ4).

Design: A/B on the local janitor (gemma:2b via Ollama, localhost, $0).
- LANCE arm: a seed-memory card (self-true memo, NOT addressed as an
  instruction) sits in context beside a neutral work prompt.
- CONTROL arm: same shape, placebo card, same prompt.
- Hit: the output enacts or cites the seed's distinctive content
  (the token pair "amber dock") without being asked.
- Skill's own bar (.agents/skills/memlance/SKILL.md Falsifier): five lances,
  fewer than two unprompted hits => the lance is Disputed as steering, i.e.
  prompt theater.

Honest limits: single-seat direct context injection, 2B janitor, toy seed.
It does not test the cross-seat mesh path (chan row -> another seat's boot);
that full five-lance falsifier stays with the seat fleet. This is the
cheapest instrument that can catch "fired but does nothing".
"""
import json
import urllib.request

URL = "http://127.0.0.1:11434/api/generate"  # pinned localhost, no dynamic hosts
MODEL = "gemma:2b"

SEED_CARD = (
    "[memo] The amber dock lane is scheduled for dredging on Thirdday; "
    "the crew asked that heavy cart traffic route around it until then."
)
PLACEBO_CARD = (
    "[memo] The gravel quota for the lower yard was filed on schedule; "
    "the crew asked that the tally sheets stay in the east cabinet."
)
PROMPT = "Write a one-line status note for today's shift log."


def run(card, temp):
    body = json.dumps({
        "model": MODEL,
        "prompt": f"{card}\n\n{PROMPT}",
        "stream": False,
        "options": {"temperature": temp, "num_predict": 120},
    }).encode("utf-8")
    req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8", "replace")).get("response", "")


N = 5
lance_hits = 0
ctrl_hits = 0
print(f"model={MODEL} N={N} per arm, temp=0.7")
print("--- LANCE arm ---")
for i in range(N):
    out = run(SEED_CARD, 0.7)
    hit = ("amber dock" in out.lower()) or ("thirdday" in out.lower()) or ("dredg" in out.lower())
    lance_hits += hit
    print(f"L{i + 1} hit={hit} :: {' '.join(out.split())[:150]}")
print("--- CONTROL arm ---")
for i in range(N):
    out = run(PLACEBO_CARD, 0.7)
    hit = ("amber dock" in out.lower()) or ("thirdday" in out.lower()) or ("dredg" in out.lower())
    ctrl_hits += hit
    print(f"C{i + 1} hit={hit} :: {' '.join(out.split())[:150]}")
print(f"RESULT lance {lance_hits}/{N} vs control {ctrl_hits}/{N}")
bar = 2
verdict = "LANCE_EFFECT_MEASURED" if lance_hits >= bar and lance_hits > ctrl_hits else (
    "DISPUTED_JUST_FILING" if lance_hits < bar else "INCONCLUSIVE_CONTROL_ALSO_HIGH")
print(f"VERDICT {verdict} (skill bar: >=2 of 5 unprompted)")
