"""MAX_ALPHA multi-lane dry run (2026-08-25) — rung 1 across the near-free shelf.

The baseline should be the FLEET, not one lane. Same contract, same pack, fired at every
near-free model that answers. Output: per-model artifacts + a comparison row.
Uses the proven bench mechanism for OpenRouter free models + rib_chat for z_ai.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"c:\Users\foste\Documents\projects\local_sovereign_agent")
sys.path.insert(0, str(ROOT))
OUT = ROOT / "memory" / "runs" / "alpha_multilane"
OUT.mkdir(parents=True, exist_ok=True)

from mag.rib_cache import FROZEN_RIB  # noqa: E402


# ── pack (bounded, deterministic, from real files) ─────────────────────────
def _read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def _tail_chain(n: int = 25) -> str:
    rows = []
    for line in _read(ROOT / "memory/biography/verkle_chain.jsonl").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except Exception:
            continue
    out = []
    for r in rows[-n:]:
        ts = str(r.get("ts") or r.get("t") or "")[:19]
        k = str(r.get("kind") or r.get("schema") or r.get("type") or "")
        s = str(r.get("summary") or r.get("text") or r.get("label") or "")[:150]
        out.append(f"- [{ts}] {k}: {s}")
    return "\n".join(out) or "(empty)"


def _latest_md() -> str:
    t = _read(ROOT / "memory/biography/latest.md")
    return t[:3000]


def _visual_residual() -> str:
    j = None
    try:
        j = json.loads(_read(ROOT / "memory/biography/latest.visual_pack.json"))
    except Exception:
        pass
    if not j:
        return "(none)"
    v = j.get("residual")
    if isinstance(v, list):
        return "; ".join(str(x.get("label") or x.get("text") or x) for x in v[:6])
    return str(v)[:600] if v else "(none)"


def build_pack() -> str:
    return (
        "## NARRATIVE (latest biography)\n" + _latest_md()[:2000]
        + "\n\n## RESIDUAL STAMPS\n" + _visual_residual()
        + "\n\n## RECENT CHAIN LEAVES\n" + _tail_chain()
    )


CONTRACT = (
    "You are reading the record of a mind. Answer three things, plainly, in order: "
    "(1) WHO is this person, from this record alone? (2) WHAT are they building, and why? "
    "(3) Given that, what is the single most important next step to prove the thing real? "
    "Be concrete and honest. Do not invent facts not in the record. Mark anything inferred "
    "as [inferred]. Under 250 words."
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


# ── z_ai near-free lanes via rib_chat ───────────────────────────────────────
def run_zai(model: str) -> dict:
    from mag.rib_cache import rib_chat
    r = rib_chat(CONTRACT, context=build_pack(), lane="z_ai", model=model)
    return {
        "lane": "z_ai", "model": model, "ok": bool(r.get("ok")),
        "cached": int(r.get("cached_tokens") or 0), "prompt": int(r.get("prompt_tokens") or 0),
        "output": str(r.get("text") or "")[:2500],
        "error": str(r.get("error") or "")[:160],
    }


# ── OpenRouter free lanes via the proven bench mechanism ────────────────────
def _keys() -> tuple[str, str]:
    k1 = k2 = ""
    for line in _read(ROOT / ".env").splitlines():
        line = line.strip()
        if line.startswith("OPENROUTER_API_KEY=") and not line.startswith("#"):
            k1 = line.split("=", 1)[1].strip().strip('"')
        if line.startswith("OPENROUTER_API_KEY_2=") and not line.startswith("#"):
            k2 = line.split("=", 1)[1].strip().strip('"')
    return k1, k2


def or_free_models() -> list[str]:
    try:
        d = json.load(urllib.request.urlopen("https://openrouter.ai/api/v1/models", timeout=15))
        wanted = ("glm-5.2", "minimax-m3", "minimax-m2.7", "nemotron-nano", "nemotron-super",
                  "north-mini-code", "dots-3", "laguna-s")
        return [m["id"] for m in d.get("data", [])
                if m["id"].endswith(":free") and any(w in m["id"] for w in wanted)][:6]
    except Exception as e:
        return [f"ERROR:{e}"]


def run_or(model: str) -> dict:
    k1, k2 = _keys()
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": FROZEN_RIB[:1800]},
            {"role": "user", "content": CONTRACT + "\n\nCONTEXT:\n" + build_pack()[:6000]},
        ],
        "max_tokens": 500,
    }).encode()
    for key in (k1, k2):
        if not key:
            continue
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions", data=body,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        t0 = time.time()
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                j = json.loads(r.read().decode())
                out = j["choices"][0]["message"]["content"]
                u = j.get("usage") or {}
                return {"lane": "openrouter", "model": model, "ok": True,
                        "cached": int(u.get("prompt_tokens_details", {}).get("cached_tokens") or 0),
                        "prompt": int(u.get("prompt_tokens") or 0),
                        "output": str(out)[:2500], "ms": round((time.time() - t0) * 1000),
                        "error": ""}
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
        except Exception as e:
            last = str(e)[:80]
    return {"lane": "openrouter", "model": model, "ok": False, "cached": 0, "prompt": 0,
            "output": "", "error": last}


def main() -> int:
    rows = []
    zai_models = ["glm-4.5-air", "glm-4.7-flashx"]
    for m in zai_models:
        print(f"== z_ai {m} ...")
        rows.append(run_zai(m))

    free = or_free_models()
    print("openrouter free candidates:", free)
    for m in free:
        print(f"== OR {m} ...")
        rows.append(run_or(m))

    (OUT / "comparison.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")

    print("\n=== COMPARISON ===")
    for r in rows:
        print(f"{'OK ' if r['ok'] else '-- '} {r['model']:45} cached={r['cached']:>7} "
              f"prompt={r['prompt']:>6}  {r.get('error','')[:60]}")
    (OUT / "pack.txt").write_text(build_pack(), encoding="utf-8")
    print("-> comparison:", (OUT / "comparison.jsonl").relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
