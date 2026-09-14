"""MAX_ALPHA — full z_ai shelf bench (2026-08-25).

The z_ai account holds ~a dozen models; the fleet baseline should bench them ALL with the
same contract + pack, not two. Free/near-free first, then the rest (each call is fractions
of a cent). Filters vision-only models out of the text contract.
"""
from __future__ import annotations

import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"c:\Users\foste\Documents\projects\local_sovereign_agent")
sys.path.insert(0, str(ROOT))
OUT = ROOT / "memory" / "runs" / "alpha_zai"
OUT.mkdir(parents=True, exist_ok=True)


def _read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def _env(name: str) -> str:
    for line in _read(ROOT / ".env").splitlines():
        line = line.strip()
        if line.startswith(name + "=") and not line.startswith("#"):
            return line.split("=", 1)[1].strip().strip('"')
    return ""


def zai_models() -> list[str]:
    key = _env("ZAI_API_KEY")
    req = urllib.request.Request(
        "https://api.z.ai/api/paas/v4/models",
        headers={"Authorization": f"Bearer {key}"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            j = json.loads(r.read().decode())
        ids = [m.get("id") for m in j.get("data", [])]
    except Exception as e:
        ids = []
        print("models endpoint error:", str(e)[:120])
    # the known free/near-free + the endpoint list, deduped, text-only
    known = ["glm-4.7-flash", "glm-4.5-flash", "glm-4.7-flashx", "glm-4.5-air",
             "glm-4.7", "glm-4.6", "glm-4.5", "glm-5", "glm-5-turbo", "glm-5.1",
             "glm-5.2", "glm-5.3"]
    all_ids = list(dict.fromkeys(ids + known))
    # filter: keep text models only (drop vision/vlm/image/audio names)
    skip = ("v", "image", "ocr", "asr", "video", "audio", "flashx-v", "glm-4v")
    return [m for m in all_ids if not any(s in m.lower() for s in skip)]


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


def _visual_residual() -> str:
    try:
        j = json.loads(_read(ROOT / "memory/biography/latest.visual_pack.json"))
    except Exception:
        return "(none)"
    v = j.get("residual")
    if isinstance(v, list):
        return "; ".join(str(x.get("label") or x.get("text") or x) for x in v[:6])
    return str(v)[:600] if v else "(none)"


def build_pack() -> str:
    md = _read(ROOT / "memory/biography/latest.md")[:2000]
    return ("## NARRATIVE (latest biography)\n" + md
            + "\n\n## RESIDUAL STAMPS\n" + _visual_residual()
            + "\n\n## RECENT CHAIN LEAVES\n" + _tail_chain())


CONTRACT = (
    "You are reading the record of a mind. Answer three things, plainly, in order: "
    "(1) WHO is this person, from this record alone? (2) WHAT are they building, and why? "
    "(3) Given that, what is the single most important next step to prove the thing real? "
    "Be concrete and honest. Do not invent facts not in the record. Mark anything inferred "
    "as [inferred]. Under 250 words."
)


def main() -> int:
    models = zai_models()
    print("z_ai text models to bench:", models)

    from mag.rib_cache import rib_chat
    pack = build_pack()
    rows = []
    for m in models:
        print(f"== {m} ...", flush=True)
        r = rib_chat(CONTRACT, context=pack, lane="z_ai", model=m)
        rows.append({
            "schema": "alpha_zai.v1", "ts": datetime.now(timezone.utc).isoformat(),
            "lane": "z_ai", "model": m, "ok": bool(r.get("ok")),
            "cached": int(r.get("cached_tokens") or 0), "prompt": int(r.get("prompt_tokens") or 0),
            "completion": int(r.get("completion_tokens") or 0),
            "output": str(r.get("text") or "")[:2500],
            "error": str(r.get("error") or "")[:160],
        })

    (OUT / "comparison.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
    (OUT / "pack.txt").write_text(pack, encoding="utf-8")

    print("\n=== z_ai SHELF COMPARISON ===")
    for r in rows:
        print(f"{'OK ' if r['ok'] else '-- '} {r['model']:18} cached={r['cached']:>7} "
              f"prompt={r['prompt']:>6}  {r.get('error','')[:70]}")
    print("-> comparison:", (OUT / "comparison.jsonl").relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
