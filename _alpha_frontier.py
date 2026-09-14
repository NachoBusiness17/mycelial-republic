"""MAX_ALPHA frontier baselines (2026-08-25) — the "Max" side of the RAR comparison.

The operator proved codex + grok CLIs launch natively in PowerShell. Same alpha contract +
pack, run through both frontier seats, saved next to the cheap-fleet baselines.
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"c:\Users\foste\Documents\projects\local_sovereign_agent")
sys.path.insert(0, str(ROOT))
OUT = ROOT / "memory" / "runs" / "alpha_frontier"
OUT.mkdir(parents=True, exist_ok=True)


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


def _run(cmd: list[str], timeout: int) -> str:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                           cwd=str(ROOT))
        return (p.stdout or "")[-6000:] + (f"\n[stderr] {p.stderr[-600:]}" if p.stderr else "")
    except subprocess.TimeoutExpired:
        return "(timeout)"
    except Exception as e:
        return f"(error) {str(e)[:200]}"


def main() -> int:
    pack = build_pack()
    prompt = CONTRACT + "\n\nCONTEXT:\n" + pack[:6000]
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    rows = []

    # 1) codex CLI (native)
    print("== codex exec ...", flush=True)
    codex_out = _run(["codex", "exec", "--skip-git-repo-check", prompt], timeout=600)
    rows.append({"schema": "alpha_frontier.v1", "ts": ts, "seat": "codex",
                 "ok": bool(codex_out and "error" not in codex_out[:40]),
                 "output": codex_out[-4000:], "error": ""})

    # 2) grok CLI via the proven seat burner (nacho seat, GROK_HOME isolation)
    print("== grok (nacho seat) ...", flush=True)
    from mag.grok_seat_burner import _launch_one
    r = _launch_one("nacho", prompt, model="", max_turns=4, timeout=600, no_subagents=True)
    grok_out = str(r.get("output") or "")
    rows.append({"schema": "alpha_frontier.v1", "ts": ts, "seat": "grok-nacho",
                 "ok": bool(r.get("ok")), "output": grok_out[-4000:],
                 "error": str(r.get("error") or r.get("stderr") or "")[:200]})

    (OUT / "baselines.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
    (OUT / "prompt.txt").write_text(prompt, encoding="utf-8")

    for r in rows:
        print(f"\n===== {r['seat']} {'OK' if r['ok'] else 'FAIL'} =====")
        print(r["output"][:2500])
    print("\n-> baselines:", (OUT / "baselines.jsonl").relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
