"""ghost_voice_boot - read-only warm pack for Ghost (Grok Bot voice front door).

Mounts, before Ghost speaks: (1) party subchain transcript (verified, tail),
(2) rib_bus domains grokbot / doctrine / party_subchain (read straight from
memory/rib_bus/*.json, no publish), (3) rib_boot.json warm snapshot (brief +
chain + laws). Writes ONE file: watch/inbox/ghost_boot/GHOST_BOOT_PACK.md.
No chain writes, no network, no secrets. Spec: memory/rib/RIB_allseat_comms_ghost_2026-08-14.md
(rule 1: no seat answers without the transcript; rule 4: one bus on disk).
Run: .venv\Scripts\python.exe scripts\ghost_voice_boot.py
"""
from __future__ import annotations
import json, sys, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
OUT = ROOT / "watch" / "inbox" / "ghost_boot" / "GHOST_BOOT_PACK.md"
DOMAINS = ("grokbot", "doctrine", "party_subchain", "nacho-shape")


def _transcript() -> str:
    try:
        from mag import party_subchain
        m = party_subchain.mount(limit=24, max_chars=6000)
        return (m.get("transcript") or "nothing yet") if m.get("ok") else f"[unmounted: {m.get('error')}]"
    except Exception as e:  # noqa: BLE001
        return f"[unmounted: {type(e).__name__}: {e}]"


def _ribs(domain: str, cap: int = 2500) -> str:
    p = ROOT / "memory" / "rib_bus" / f"{domain}.json"
    if not p.exists():
        return "[missing]"
    try:
        d = json.loads(p.read_text(encoding="utf-8", errors="replace"))
    except Exception as e:  # noqa: BLE001
        return f"[unreadable: {e}]"
    items = sorted((d.get("ribs") or {}).values(), key=lambda r: str(r.get("ts", "")), reverse=True)
    out, n = [], 0
    for r in items:
        line = "- " + str(r.get("invariant", "")).replace("\n", " ")[:400]
        n += len(line)
        if n > cap:
            break
        out.append(line)
    return "\n".join(out) or "[empty]"


def _rib_boot() -> str:
    p = ROOT / "memory" / "rib_boot.json"
    if not p.exists():
        return "[missing - run python -m mag.rib_boot]"
    d = json.loads(p.read_text(encoding="utf-8", errors="replace"))
    brief = d.get("brief") or {}
    head = brief.get("head", "") if isinstance(brief, dict) else str(brief)
    return (f"ts: {d.get('ts')}  rib_count: {d.get('rib_count')}  chain: {json.dumps(d.get('chain'))[:300]}\n\n"
            f"core_laws: {json.dumps(d.get('core_laws'))[:1500]}\n\nbrief head:\n{head[:2500]}")


def build() -> Path:
    now = datetime.datetime.now().isoformat(timespec="seconds")
    parts = [f"# GHOST BOOT PACK ({now} local)", "Read-only mount. Chain is the record; this is the warm view.",
             "## 1. Party transcript (presented, not interpreted)", _transcript(),
             "## 2. Rib bus"]
    for d in DOMAINS:
        parts += [f"### {d}", _ribs(d, cap=12000 if d == "doctrine" else 2500)]
    parts += ["## 3. rib_boot warm snapshot", _rib_boot()]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n\n".join(parts), encoding="utf-8")
    return OUT


if __name__ == "__main__":
    p = build()
    print(f"wrote {p} ({p.stat().st_size} bytes)")

