"""u2_union_astra13 -- the 13TH COLUMN of the Astra smoke (wave 20260916, lane U2).

Witness: stealth/union-alpha on OpenRouter (free this week, time-boxed lane
`or-union-alpha` in mag/research_fanout.py LANES). Same F1-F12 family text as
a4_astra_smoke_12.py (imported byte-identical); OUTPUT CONTRACT extended with a
confidence cell per family. 12 families x 2 seeds, temperature 0.4, sequential.
Key via mag.flight_recorder.load_env, never printed, never written to a row.
Raw rows -> watch/salon_responses/astra_union_alpha/raw.jsonl (append-only).
Schema: astra_union_alpha.v1. $0 budget; 402/403 -> record and stop.
"""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]  # watch/inbox/wave_20260916/u2_union_astra13.py -> repo root
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE.parent))

from mag.flight_recorder import load_env, guard_endpoint  # noqa: E402
from a4_astra_smoke_12 import families, parse_verdicts  # byte-identical family text + parser  # noqa: E402

OUT = ROOT / "watch" / "salon_responses" / "astra_union_alpha"
OUT.mkdir(parents=True, exist_ok=True)
RAW = OUT / "raw.jsonl"

MODEL = "stealth/union-alpha"
BASE = "https://openrouter.ai/api/v1"
ALLOWED_HOSTS = {"openrouter.ai"}
TEMP = 0.4
MAX_TOKENS = 4000
SEEDS = (1, 2)

# OUTPUT CONTRACT: same as A4 plus a confidence cell (high|medium|low)
PROMPT = families().replace(
    "OUTPUT CONTRACT - exactly 12 lines, no preamble, no markdown:\n"
    "F1 | Supported|Disputed|Unproven | <one line of evidence>",
    "OUTPUT CONTRACT - exactly 12 lines, no preamble, no markdown:\n"
    "F1 | Supported|Disputed|Unproven | high|medium|low | <one line of evidence>",
)
assert PROMPT != families(), "contract splice failed"

SYSTEM = ("You are an independent systems-research referee. Judge strictly from your own "
          "knowledge of the published literature; do not try to please anyone. Be terse "
          "and concrete. Output only the 12 contract lines, no preamble, no closing.")

A4_MAJORITY = {  # lane-majority consensus per A4 receipt table
    1: "Supported", 2: "Disputed", 3: "Supported", 4: "Supported", 5: "Supported",
    6: "Supported", 7: "Supported", 8: "Supported", 9: "Supported", 10: "Supported",
    11: "Supported", 12: "Supported",
}


def call(prompt: str, key: str, seed: int) -> dict:
    t0 = time.time()
    rec: dict = {"lane": "or-union-alpha", "model": MODEL, "ts_seed": seed}
    try:
        guard_endpoint(BASE + "/chat/completions", ALLOWED_HOSTS)
    except ValueError as e:
        rec.update({"ok": False, "error": f"guard: {e}"})
        return rec
    body = {"model": MODEL, "temperature": TEMP, "max_tokens": MAX_TOKENS,
            "seed": seed * 1000 + 13,
            "messages": [{"role": "system", "content": SYSTEM},
                         {"role": "user", "content": prompt}]}
    req = urllib.request.Request(
        BASE.rstrip("/") + "/chat/completions", data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                 "User-Agent": "mag-u2-union-astra13/1.0",
                 "HTTP-Referer": "https://local-sovereign-agent.invalid",
                 "X-Title": "U2 Union Astra 13th Column"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            d = json.loads(r.read().decode("utf-8", "replace"))
        msg = d["choices"][0]["message"]
        txt = (msg.get("content") or "").strip()
        if txt:
            rec.update({"ok": True, "answer": txt, "chars": len(txt),
                        "usage": d.get("usage") or {},
                        "finish_reason": d["choices"][0].get("finish_reason")})
        else:
            rec.update({"ok": False, "error": "empty_content",
                        "detail": (msg.get("reasoning") or msg.get("reasoning_content") or "")[:200],
                        "finish_reason": d["choices"][0].get("finish_reason")})
    except urllib.error.HTTPError as e:
        rec.update({"ok": False, "error": f"HTTP {e.code}",
                    "detail": e.read().decode("utf-8", "replace")[:300]})
    except Exception as e:
        rec.update({"ok": False, "error": f"{type(e).__name__}: {str(e)[:140]}"})
    rec["latency_ms"] = int((time.time() - t0) * 1000)
    return rec


CONF_RE = re.compile(r"(high|medium|low|moderate)", re.I)


def parse_confidence(answer: str) -> dict[int, str]:
    out: dict[int, str] = {}
    for ln in answer.splitlines():
        m = re.match(r"^F(\d{1,2})\s*\|", ln.strip())
        if not m:
            continue
        fam = int(m.group(1))
        if fam in out:
            continue
        cells = [c.strip() for c in ln.split("|")]
        cm = next((CONF_RE.match(c) for c in cells[2:5] if CONF_RE.match(c)), None)
        out[fam] = (cm.group(1).lower().replace("moderate", "medium") if cm else "none")
    return out


def main() -> int:
    env = load_env()
    key = env.get("OPENROUTER_API_KEY")
    if not key:
        print("NO OPENROUTER_API_KEY in load_env - abort before firing", flush=True)
        return 1
    print(f"key present (len {len(key)}), firing {MODEL} x{len(SEEDS)} seeds T={TEMP}", flush=True)

    results: list[dict] = []
    for seed in SEEDS:
        r = call(PROMPT, key, seed)
        r["seed"] = seed
        results.append(r)
        tag = "OK " if r.get("ok") else "ERR"
        print(f"  seed{seed}: {tag} {r.get('chars', '')} chars {r['latency_ms']}ms"
              + ("" if r.get("ok") else f"  {str(r.get('error'))[:120]}"), flush=True)
        with RAW.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({"schema": "astra_union_alpha.v1", **r}, ensure_ascii=False) + "\n")
        body = (r.get("answer") if r.get("ok") else
                f"FAILED: {r.get('error')} :: {str(r.get('detail', ''))[:300]}")
        (OUT / f"union_alpha_seed{seed}.md").write_text(
            f"# stealth/union-alpha seed {seed} T={TEMP} — {'OK' if r.get('ok') else 'FAILED'}"
            f" — {r['latency_ms']}ms\n\n{body}\n", encoding="utf-8")
        if r.get("ok") is False and str(r.get("error", "")).startswith("HTTP 40"):
            print("paid-wall class error (40x) - budget law: stop after recording", flush=True)
            break
        time.sleep(3)  # polite gap between seeds

    # verdict summary vs A4
    for r in results:
        if not r.get("ok"):
            continue
        v = parse_verdicts(r["answer"])
        c = parse_confidence(r["answer"])
        agree = sum(1 for f, verd in v.items() if A4_MAJORITY.get(f) == verd)
        print(f"seed{r['seed']}: {len(v)}/12 verdicts, {agree}/{len(v)} agree with A4 majority", flush=True)
        for f in sorted(v):
            mark = "=" if A4_MAJORITY.get(f) == v[f][0] else "FLIP"
            print(f"  F{f:<2} {v[f][0]:<9} conf={c.get(f, 'none'):<6} [{mark}] {v[f][1][:90]}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
