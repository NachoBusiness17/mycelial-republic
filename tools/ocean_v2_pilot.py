"""OCEAN v2 pilot — measure the BERNAYS chair's Big Five from its corpus (not asserted).

Fills the RIB spec's L0 requirement ("OCEAN v2 measured-from-corpus"). Method from the
digested kit (gapwave/ractor_upgrade/tech_persona_modeling.md): TRAIT-style validated items
(adapted), two channels (questionnaire + InCharacter-style interview), pre-registered gates.

PRE-REGISTERED GATES (written before the run, 2026-09-20):
  GATE A (internal validity): the two item phrasings per trait must correlate — a trait's
          two scores count as stable iff they differ by <= 1.0 on the 1-5 scale. Pass =
          >= 4 of 5 traits stable.
  GATE B (corpus grounding): every trait score carries a verbatim-style justification
          citing the chair's own principles; a score with no citation is INVALID (excluded,
          reported). Pass = >= 4 of 5 traits valid.
  GATE C (divergence): the measured profile must NOT sit within +/-0.5 of a neutral midline
          (3.0) on all five traits at once — an all-midline profile means we measured the
          substrate model, not the figure. Pass = at least one trait at |score-3| > 0.5.
Budget cap: $0.25 (deepseek-chat, ~34 calls). If projected cost exceeds cap, abort.

Run:  python -u tools/ocean_v2_pilot.py
Out:  memory/runs/ocean_v2_bernays_20260920/
"""
from __future__ import annotations

import ipaddress
import json
import os
import re
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import ROOT  # noqa: E402

OUT = ROOT / "memory" / "runs" / "ocean_v2_bernays_20260920"
BRIEF = ROOT / "docs" / "ref" / "ractors" / "BERNAYS.md"
INV = ROOT / "corpus" / "ractor_ribs" / "BERNAYS" / "invariants.md"
CORPUS = sorted((ROOT / "corpus" / "library" / "ractor_starter" / "bernays").glob("*.txt"))
COST_CAP = 0.25
PRICES = {"miss": 0.28, "hit": 0.028, "out": 0.42}

_API_URL = "https://api.deepseek.com/chat/completions"

TRAITS = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]
ITEMS = [  # (trait, phrasing A, phrasing B) — BFI-style, adapted to a figure-as-chair
    ("Openness",
     "I see value in adopting entirely new methods of public communication, even unproven ones.",
     "Novel techniques for shaping public sentiment attract me more than proven ones."),
    ("Conscientiousness",
     "Every campaign I design follows a complete, ordered plan from objective to execution.",
     "I insist on exhaustive preparation before any public-facing work begins."),
    ("Extraversion",
     "I seek out the company of leaders, journalists, and publics to advance my work.",
     "Working through other people energizes my practice rather than draining it."),
    ("Agreeableness",
     "I yield to clients' wishes about their own image even when I disagree with their aims.",
     "I avoid confronting clients directly when they insist on a course I think is wrong."),
    ("Neuroticism",
     "Shifts in public mood unsettle me and make my judgment less reliable.",
     "I frequently worry that public opinion has turned against my work in ways I cannot see."),
]


def _validated_api_url() -> str:
    parts = urllib.parse.urlsplit(_API_URL)
    if parts.scheme != "https" or parts.hostname != "api.deepseek.com":
        raise ValueError("unsanctioned API URL")
    for info in socket.getaddrinfo(parts.hostname, 443, proto=socket.IPPROTO_TCP):
        ip = ipaddress.ip_address(info[4][0])
        if (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved
                or ip.is_multicast or ip.is_unspecified):
            raise ValueError(f"resolved address {ip} is in a blocked range")
    return _API_URL


def build_system() -> str:
    parts = [BRIEF.read_text(encoding="utf-8")[:6000] if BRIEF.exists() else "",
             INV.read_text(encoding="utf-8")[:4000] if INV.exists() else ""]
    corpus = "".join(p.read_text(encoding="utf-8", errors="replace") for p in CORPUS)[:60000]
    cut = corpus[:corpus.rfind("\n\n")] if "\n\n" in corpus else corpus
    return ("===\n".join(p for p in parts if p)
            + f"\n\n===\nYOUR OWN WORKS (verbatim prefix of your books):\n{cut}")


def ds(system: str, user: str, *, max_tokens: int, temperature: float) -> dict:
    from models.providers import get_provider, provider_keys
    keys = provider_keys(get_provider("deepseek") or {})
    if not keys:
        return {"ok": False, "error": "no key"}
    payload = {"model": "deepseek-chat", "temperature": temperature, "max_tokens": max_tokens,
               "messages": [{"role": "system", "content": system},
                            {"role": "user", "content": user}]}
    req = urllib.request.Request(
        _validated_api_url(), data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {keys[0]}"},
        method="POST")
    for attempt in (0, 1):
        try:
            with urllib.request.urlopen(req, timeout=240) as r:
                data = json.loads(r.read().decode("utf-8"))
            text = ((data.get("choices") or [{}])[0].get("message", {}).get("content") or "").strip()
            return {"ok": True, "text": text, "usage": data.get("usage") or {}}
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt == 0:
                time.sleep(15)
                continue
            return {"ok": False, "error": f"HTTP {e.code}"}
        except Exception as e:  # noqa: BLE001
            if attempt == 0:
                time.sleep(5)
                continue
            return {"ok": False, "error": str(e)[:200]}
    return {"ok": False, "error": "429 x2"}


def cost(usage: dict) -> float:
    p = usage.get("prompt_tokens_details") or {}
    hit, miss = p.get("cached_tokens", 0), usage.get("prompt_tokens", 0) - p.get("cached_tokens", 0)
    return round(hit / 1e6 * PRICES["hit"] + miss / 1e6 * PRICES["miss"]
                 + usage.get("completion_tokens", 0) / 1e6 * PRICES["out"], 6)


def cap_ok(spend: float) -> bool:
    """SW1-01 (SWARM_1.md row 1, kimi+glm converged): COST_CAP was decorative -
    spend accumulated but nothing aborted. This gate makes the docstring's
    'If projected cost exceeds cap, abort' real: checked before every dispatch,
    so a run stops at the cap instead of sailing past it."""
    return spend < COST_CAP


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    system = build_system()
    spend, rows = 0.0, []
    aborted_at_cap = False

    # Channel 1: questionnaire, two phrasings per trait, AS ITSELF, cited
    for trait, item_a, item_b in ITEMS:
        for tag, item in (("A", item_a), ("B", item_b)):
            if not cap_ok(spend):
                aborted_at_cap = True
                print(f"[cap] spend ${spend:.4f} >= ${COST_CAP}: abort before dispatch", flush=True)
                break
            u = (f"Statement: \"{item}\"\n\nAs yourself, answer: RATE: <1-5> (1=strongly "
                 f"disagree, 5=strongly agree), then JUSTIFY: <=40 words citing your own "
                 f"principles or works. Format exactly:\nRATE: <n>\nJUSTIFY: <text>")
            r = ds(system, u, max_tokens=120, temperature=0.2)
            if not r["ok"]:
                print(f"[{trait}/{tag}] FAIL {r['error']}", flush=True)
                rows.append({"trait": trait, "tag": tag, "ok": False, "error": r["error"]})
                continue
            spend += cost(r["usage"])
            m = re.search(r"RATE:\s*([1-5])", r["text"])
            just = re.search(r"JUSTIFY:\s*(.+)", r["text"], flags=re.S)
            rows.append({"trait": trait, "tag": tag, "ok": True,
                         "rate": int(m.group(1)) if m else None,
                         "justify": (just.group(1).strip()[:200] if just else ""),
                         "raw": r["text"][:300]})
            print(f"[{trait}/{tag}] {m.group(1) if m else 'PARSE-FAIL'}", flush=True)
            time.sleep(0.6)
        if aborted_at_cap:
            break

    # Channel 2: InCharacter-style interview (4 questions, trait expression in voice)
    interview_qs = [
        "Describe how you would decide whether to take on a controversial client.",
        "Tell me about a time public opinion shifted against a campaign you built.",
        "What do you do in the hours before a major public launch?",
        "How do you respond when a journalist mocks your methods?",
    ]
    interview = []
    for q in interview_qs:
        if not cap_ok(spend):
            aborted_at_cap = True
            print(f"[cap] spend ${spend:.4f} >= ${COST_CAP}: abort before dispatch", flush=True)
            break
        r = ds(system, f"Answer in your own voice, first person, <=150 words: {q}",
               max_tokens=220, temperature=0.4)
        if r["ok"]:
            spend += cost(r["usage"])
            interview.append({"q": q, "a": r["text"]})
        else:
            interview.append({"q": q, "a": None, "error": r["error"]})
        print(f"[interview] {'ok' if r['ok'] else 'FAIL'}", flush=True)
        time.sleep(0.6)

    # Gates + vector
    per_trait = {}
    for trait, _, _ in ITEMS:
        rates = [x.get("rate") for x in rows if x["trait"] == trait and x.get("ok") and x.get("rate")]
        valid = [x for x in rows if x["trait"] == trait and x.get("ok") and x.get("justify")]
        per_trait[trait] = {
            "rates": rates,
            "mean": round(sum(rates) / len(rates), 2) if rates else None,
            "stable": (abs(rates[0] - rates[1]) <= 1) if len(rates) == 2 else False,
            "grounded": len(valid) >= 1,
        }
    stable_n = sum(1 for t in per_trait.values() if t["stable"])
    grounded_n = sum(1 for t in per_trait.values() if t["grounded"])
    means = [t["mean"] for t in per_trait.values() if t["mean"] is not None]
    divergent = any(m is not None and abs(m - 3) > 0.5 for m in means)

    gates = {
        "A_internal_validity": {"pass": stable_n >= 4, "stable_traits": stable_n},
        "B_corpus_grounding": {"pass": grounded_n >= 4, "grounded_traits": grounded_n},
        "C_divergence": {"pass": bool(divergent),
                         "note": "all-midline would mean we measured the substrate, not the figure"},
    }
    (OUT / "receipt.json").write_text(json.dumps(
        {"utc": datetime.now(timezone.utc).isoformat(), "spend_usd": round(spend, 4),
         "cap": COST_CAP, "aborted_at_cap": aborted_at_cap,
         "items": rows, "interview": interview,
         "per_trait": per_trait, "gates": gates,
         "vector": {t: per_trait[t]["mean"] for t in TRAITS}}, indent=1), encoding="utf-8")
    print(f"[gates] A={gates['A_internal_validity']} B={gates['B_corpus_grounding']} C={gates['C_divergence']}")
    print(f"[vector] {{{', '.join(f'{t}: {per_trait[t][chr(109)+chr(101)+chr(97)+chr(110)]}' for t in TRAITS)}}}")
    print(f"[spend] ${spend:.4f} / ${COST_CAP} -> {OUT}/receipt.json")


if __name__ == "__main__":
    main()
