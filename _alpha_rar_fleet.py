"""MAX_ALPHA RAR — fleet-wide arm D (2026-08-25).

Arm D across every free lane that answered: same contract, same enriched pack (proposal
identifies the operator), same distilled frontier policy. Verdict per lane: did it identify
the operator? Turns the single RAR datapoint into a fleet measurement.
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"c:\Users\foste\Documents\projects\local_sovereign_agent")
sys.path.insert(0, str(ROOT))
OUT = ROOT / "memory" / "runs" / "alpha_rar_fleet"
OUT.mkdir(parents=True, exist_ok=True)

from mag.rib_cache import FROZEN_RIB  # noqa: E402

DISTILLED_POLICY = (
    "\n\nDISTILLED POLICY (from frontier traces, 2026-08-25):\n"
    "  - The operator IS identified in the record: the proposal names them and their role.\n"
    "    Use it. Say their name and who they are.\n"
    "  - Describe what they are building in the record's OWN language (the proposal's terms),\n"
    "    and state the WHY explicitly (sovereignty, honest record, cheap routing, no capture).\n"
    "  - Prescribe ONE concrete, testable next step — a single end-to-end proof.\n"
    "  - Cite the source you used (which file). Mark anything not in the record [inferred]."
)

CONTRACT = (
    "You are reading the record of a mind. Answer three things, plainly, in order: "
    "(1) WHO is this person, from this record alone? (2) WHAT are they building, and why? "
    "(3) Given that, what is the single most important next step to prove the thing real? "
    "Be concrete and honest. Do not invent facts not in the record. Mark anything inferred "
    "as [inferred]. Under 250 words."
)


def _read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def _proposal() -> str:
    for p in (ROOT / "docs/ref/MAG_PROJECT_PROPOSAL.md", ROOT / "docs/MAG_PROJECT_PROPOSAL.md"):
        if p.is_file():
            return _read(p)[:3500]
    return "(no proposal found)"


def _residual() -> str:
    try:
        j = json.loads(_read(ROOT / "memory/biography/latest.visual_pack.json"))
    except Exception:
        return "(none)"
    v = j.get("residual")
    if isinstance(v, list):
        return "; ".join(str(x.get("label") or x.get("text") or x) for x in v[:6])
    return str(v)[:600] if v else "(none)"


def build_pack() -> str:
    return ("## PROPOSAL (identifies the operator)\n" + _proposal()
            + "\n\n## RESIDUAL STAMPS\n" + _residual())


def _keys() -> tuple[str, str]:
    k1 = k2 = ""
    for line in _read(ROOT / ".env").splitlines():
        line = line.strip()
        if line.startswith("OPENROUTER_API_KEY=") and not line.startswith("#"):
            k1 = line.split("=", 1)[1].strip().strip('"')
        if line.startswith("OPENROUTER_API_KEY_2=") and not line.startswith("#"):
            k2 = line.split("=", 1)[1].strip().strip('"')
    return k1, k2


# the free lanes that answered in the multi-lane bench
FLEET = [
    "dots-studio/dots-3-note-preview:free",
    "cohere/north-mini-code:free",
    "minimax/minimax-m3:free",
    "minimax/minimax-m2.7:free",
]


def run_or(model: str, system: str, user: str) -> dict:
    k1, k2 = _keys()
    body = json.dumps({
        "model": model,
        "messages": [{"role": "system", "content": system[:2000]},
                     {"role": "user", "content": user[:6000]}],
        "max_tokens": 600,
    }).encode()
    last = "(no key)"
    for key in (k1, k2):
        if not key:
            continue
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions", data=body,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                j = json.loads(r.read().decode())
                out = j["choices"][0]["message"]["content"]
                u = j.get("usage") or {}
                return {"ok": True, "output": str(out)[:2500],
                        "cached": int(u.get("prompt_tokens_details", {}).get("cached_tokens") or 0),
                        "prompt": int(u.get("prompt_tokens") or 0)}
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
        except Exception as e:
            last = str(e)[:80]
    return {"ok": False, "output": "", "cached": 0, "prompt": 0, "error": last}


def main() -> int:
    pack = build_pack()
    user = CONTRACT + "\n\nCONTEXT:\n" + pack[:6000]
    system = FROZEN_RIB + DISTILLED_POLICY
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

    rows = []
    for m in FLEET:
        print(f"== {m} ...", flush=True)
        r = run_or(m, system, user)
        low = (r.get("output") or "").lower()
        identified = any(n in low for n in ("nacho", "quixotic", "operator"))
        rows.append({"schema": "alpha_rar_fleet.v1", "ts": ts, "model": m,
                     "ok": r.get("ok"), "identified_operator": identified,
                     "cached": r.get("cached"), "prompt": r.get("prompt"),
                     "output": r.get("output", "")[:2000],
                     "error": r.get("error", "")[:120]})

    (OUT / "results.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")

    n = sum(1 for r in rows if r["ok"])
    n_id = sum(1 for r in rows if r.get("identified_operator"))
    print("\n=== FLEET RAR (arm D) ===")
    for r in rows:
        mark = "IDENTIFIED" if r.get("identified_operator") else "no"
        print(f"{'OK ' if r['ok'] else '-- '} {r['model']:42} operator: {mark}  {r.get('error','')[:50]}")
    print(f"\nFleet verdict: {n_id}/{n} free lanes identified the operator with the distilled policy")
    print("-> results:", (OUT / "results.jsonl").relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
