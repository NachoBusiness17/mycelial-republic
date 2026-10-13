"""_g33_deepseek_fewshot.py — MICKEY G3-3 one-shot: fire deepseek-chat on the
top-10 CONTROVERTED lines from watch/INVARIANT_SHEET_V2.md.
Key read from .env, used in headers only, never printed. Stdlib only.
Raw output lands in _g33_ds_raw.txt (scratch); deliverable is the mickey card.
"""
import json
import time
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent
ENV = REPO / ".env"
OUT = REPO / "_g33_ds_raw.txt"

def get_key(path: Path, name: str) -> str:
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith(name + "="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise KeyError(name)

CLAIMS = [
    {"n": 1, "agree": 3, "refute": 12, "src": "memory/runs/astra_convo_20260911/ANSWER_2.md",
     "text": "per family references (the SUPPORTED tri-state row above, quoting her ...) — [the Astra condition-arithmetic family]"},
    {"n": 2, "agree": 2, "refute": 7, "src": "memory/runs/astra_convo_20260911/ANSWER_2.md",
     "text": "4. I4 falsifier re-run — A11 (same file, ledger)."},
    {"n": 3, "agree": 2, "refute": 7, "src": "memory/runs/astra_convo_20260911/ANSWER_2.md",
     "text": "PROMOTION SUPPORTED requires >= 2 INDEPENDENT witnesses with the second at ..."},
    {"n": 4, "agree": 2, "refute": 6, "src": "watch/astra_hold0/NOVELTY_MAP_OUTLINE_20260911.md:53",
     "text": "(deck falsifier F-D1). Dimensions 1-5 are how ANY solution (ours, Astra's, a ...)"},
    {"n": 5, "agree": 2, "refute": 6, "src": "memory/runs/astra_convo_20260911/ANSWER_2.md",
     "text": 'UNPROVEN", hash-witnessed at watch/GROUNDING_WAVE.md) is the DEMOTION ...'},
    {"n": 6, "agree": 2, "refute": 6, "src": "memory/runs/astra_convo_20260911/ANSWER_2.md",
     "text": "any SUPPORTED label the witnesses carry."},
    {"n": 7, "agree": 2, "refute": 6, "src": "memory/runs/astra_convo_20260911/ANSWER_2.md",
     "text": "| C2 | The knot store holds 21,264 knots. |"},
    {"n": 8, "agree": 3, "refute": 4, "src": "memory/runs/astra_convo_20260911/ANSWER_2.md",
     "text": '| CAMP STATE v0 + v1, pinned verbatim | SUPPORTED — watch/ASTRA_CAMPAIGN_LOG.md |'},
    {"n": 9, "agree": 3, "refute": 4, "src": "memory/runs/astra_convo_20260911/ANSWER_2.md",
     "text": "second witness auto-demotes to UNPROVEN); witnesses partitioned across seats."},
    {"n": 10, "agree": 3, "refute": 4, "src": "memory/runs/astra_convo_20260911/ANSWER_2.md",
     "text": "pages unfetched; that cross-check stays UNPROVEN (scan card §4); nothing ..."},
]

def claim_block():
    lines = []
    for c in CLAIMS:
        lines.append(f"{c['n']}. [agreement={c['agree']} refutation={c['refute']}] (source: {c['src']})\n   CLAIM: {c['text']}")
    return "\n".join(lines)

PROMPT = """Each numbered claim below comes from the working corpus of an AI agent fleet. A deterministic classifier found that each claim has BOTH agreement (other corpus lines repeating it) AND refutation (negative-marker lines on the same subject) — so each is a live dispute. The claims are quoted verbatim as corpus fragments; judge the claim each fragment is carrying, not the fragment's grammar.

""" + claim_block() + """

For each claim below, state the strongest argument FOR and the strongest argument AGAINST, then name the specific evidence that would resolve the dispute. Be specific. No hedging.

Format per claim:
### Claim N
- FOR: ...
- AGAINST: ...
- RESOLVING EVIDENCE: ..."""

key = get_key(ENV, "DEEPSEEK_API_KEY")
payload = json.dumps({
    "model": "deepseek-chat",
    "messages": [
        {"role": "user", "content": PROMPT},
    ],
    "max_tokens": 6000,
    "temperature": 0.3,
}).encode("utf-8")
req = urllib.request.Request(
    "https://api.deepseek.com/v1/chat/completions",
    data=payload,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}",
    },
    method="POST",
)
t0 = time.time()
with urllib.request.urlopen(req, timeout=420) as resp:
    body = json.loads(resp.read().decode("utf-8"))
dt = time.time() - t0

content = body["choices"][0]["message"]["content"]
usage = body.get("usage", {})
raw = (
    f"model=deepseek-chat tier=T2 max_tokens=6000 temp=0.3 latency={dt:.1f}s\n"
    f"usage={json.dumps(usage)}\n"
    f"finish={body['choices'][0].get('finish_reason')}\n"
    f"----\n{content}\n"
)
OUT.write_text(raw, encoding="utf-8")
print(f"OK latency={dt:.1f}s completion_tokens={usage.get('completion_tokens')} finish={body['choices'][0].get('finish_reason')} -> {OUT}")
print(f"chars={len(content)}")
