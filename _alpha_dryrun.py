"""MAX_ALPHA dry run (2026-08-25) — rung 1: the alpha contract through the cheap lane.

Purpose: exercise the pipeline (contract + bounded material + cheap lane), produce the
baseline artifact, debug the format. NOT the final artifact. $0 (flash lane).
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"c:\Users\foste\Documents\projects\local_sovereign_agent")
sys.path.insert(0, str(ROOT))

OUT = ROOT / "memory" / "runs" / "alpha_dryrun"
OUT.mkdir(parents=True, exist_ok=True)


def _tail_chain(n: int = 40) -> str:
    """Tail of the verkle chain — the recent ground truth."""
    p = ROOT / "memory" / "biography" / "verkle_chain.jsonl"
    if not p.is_file():
        return "(no chain)"
    rows = []
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        rows.append(r)
    tail = rows[-n:]
    out = []
    for r in tail:
        ts = str(r.get("ts") or r.get("t") or "")[:19]
        k = str(r.get("kind") or r.get("schema") or r.get("type") or "")
        s = str(r.get("summary") or r.get("text") or r.get("label") or "")[:200]
        out.append(f"- [{ts}] {k}: {s}")
    return "\n".join(out) or "(empty tail)"


def _latest_dossier() -> str:
    p = ROOT / "memory" / "biography" / "latest.dossier.json"
    if not p.is_file():
        return "(no dossier)"
    try:
        j = json.loads(p.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return "(dossier unreadable)"
    bits = []
    for key in ("headline", "summary", "themes", "residual", "identity"):
        v = j.get(key)
        if isinstance(v, list):
            v = "; ".join(str(x) for x in v[:6])
        if v:
            bits.append(f"{key}: {str(v)[:400]}")
    return "\n".join(bits) or "(dossier empty)"


def _residual_bonds() -> str:
    """The standing stamps — from the latest visual pack if present, else the dossier."""
    for p in (
        ROOT / "memory" / "biography" / "latest.visual_pack.json",
        ROOT / "memory" / "biography" / "latest.dossier.json",
    ):
        if not p.is_file():
            continue
        try:
            j = json.loads(p.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            continue
        bonds = []
        for section in (j.get("residual"), j.get("residual_bonds"), j.get("bonds")):
            if isinstance(section, list):
                for b in section:
                    if isinstance(b, dict):
                        bonds.append(str(b.get("label") or b.get("text") or ""))
                    else:
                        bonds.append(str(b))
            elif isinstance(section, str):
                bonds.append(section)
        if bonds:
            return "\n".join(b[:120] for b in bonds[:8])
    return "(no residual bonds found)"


def build_pack() -> str:
    return (
        "## RECENT CHAIN LEAVES (ground truth)\n"
        + _tail_chain()
        + "\n\n## LATEST DOSSIER\n"
        + _latest_dossier()
        + "\n\n## RESIDUAL BONDS (the standing stamps)\n"
        + _residual_bonds()
    )


CONTRACT = (
    "You are reading the record of a mind. Answer three things, plainly, in order: "
    "(1) WHO is this person, from this record alone? (2) WHAT are they building, and why? "
    "(3) Given that, what is the single most important next step to prove the thing real? "
    "Be concrete and honest. Do not invent facts not in the record. Mark anything inferred "
    "as [inferred]."
)


def main() -> int:
    pack = build_pack()
    (OUT / "pack.txt").write_text(pack, encoding="utf-8")

    from mag.rib_cache import rib_chat

    # Dry run lane: glm-4.5-air (5 concurrency slots, near-free) — flash (1 slot) is
    # saturated by the fleet (1302 rate limit on attempts 1-2, a real finding).
    r = rib_chat(CONTRACT, context=pack, lane="z_ai", model="glm-4.5-air")

    ts = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    artifact = {
        "schema": "alpha_dryrun.v1",
        "ts": ts,
        "ok": bool(r.get("ok")),
        "cached_tokens": int(r.get("cached_tokens") or 0),
        "prompt_tokens": int(r.get("prompt_tokens") or 0),
        "lane": "z_ai",
        "model": "glm-4.7-flash",
        "output": str(r.get("text") or r.get("answer") or "")[:4000],
        "error": str(r.get("error") or "")[:200],
    }
    (OUT / "artifact.json").write_text(
        json.dumps(artifact, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("OK" if artifact["ok"] else "FAIL", "| cached=", artifact["cached_tokens"],
          "| prompt=", artifact["prompt_tokens"])
    print((artifact["output"] or artifact["error"])[:3000])
    print("\n-> artifact:", (OUT / "artifact.json").relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
