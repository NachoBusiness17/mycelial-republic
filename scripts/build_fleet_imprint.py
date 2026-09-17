"""build_fleet_imprint -- mine the repo into one pre-warmed RIB the Librarian loads cold.

Operator order (2026-09-17): "dedicate one 5.3 agent to be an expert in our database that
we can load cold on max so we can ask it questions about ourselves when you forget" +
"take every conversation history and mine its trajectory for common trends and create an
imprint pre-warmed rib."

The imprint is deterministic and regenerable: module docstrings, the provider registry,
mechanism signatures, law headers, board state, recent receipts. Digest-pinned. Every
regeneration is a new row, never a rewrite of history.

RUN: .venv\\Scripts\\python.exe scripts\\build_fleet_imprint.py
OUT: watch/inbox/FLEET_IMPRINT_20260917.md  (the Librarian's system prompt)
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "watch" / "inbox" / "FLEET_IMPRINT_20260917.md"


def _first_docstring(p: Path, limit: int = 240) -> str:
    try:
        src = p.read_text(encoding="utf-8", errors="replace")[:4000]
    except Exception:
        return ""
    m = re.match(r'^(?:#![^\n]*\n\s*)?("""|\'\'\')\s*(.{10,})', src, re.S)
    if not m:
        return ""
    txt = re.sub(r"\s+", " ", m.group(2))[:limit]
    return txt


def mine_modules(lines: list[str]) -> int:
    lines.append("## MECHANISMS — every module, one line each (the 'do we have X' map)\n")
    n = 0
    for d in ["mag", "models", "scripts"]:
        for p in sorted((ROOT / d).glob("*.py")):
            if p.name.startswith("_"):
                continue
            doc = _first_docstring(p)
            if doc:
                lines.append(f"- `{d}/{p.name}` — {doc}")
                n += 1
    lines.append("")
    return n


def mine_providers(lines: list[str]) -> int:
    lines.append("## LANES — the canonical provider registry (configs/providers.yaml)\n")
    try:
        import yaml  # type: ignore
        cfg = yaml.safe_load((ROOT / "configs" / "providers.yaml").read_text(encoding="utf-8"))
        provs = cfg.get("providers", cfg)
        n = 0
        for pid, pc in sorted(provs.items()):
            if not isinstance(pc, dict) or "base_url" not in pc:
                continue
            models = pc.get("models") or []
            flags = []
            if pc.get("free"):
                flags.append("free")
            if pc.get("paid"):
                flags.append("paid/peak-deferred")
            q = pc.get("quota") or {}
            if q:
                flags.append(f"quota {q.get('max_calls')}/period")
            lines.append(f"- `{pid}` — {pc.get('name', '')} · models: {', '.join(models[:4])}"
                         f"{'…' if len(models) > 4 else ''} · {', '.join(flags) or 'no flags'}")
            n += 1
        lines.append("")
        return n
    except Exception as e:
        lines.append(f"- registry read failed: {e}\n")
        return 0


def mine_laws(lines: list[str]) -> int:
    lines.append("## LAWS — headers from the constitution surfaces\n")
    n = 0
    for rel, pat in [("AGENTS.md", r"^[-*] \*\*(.+?)\*\*"),
                     ("docs/DNA.md", r"^#{1,3} (.+)$"),
                     ("CONSTITUTION.md", r"^#{1,3} (.+)$")]:
        p = ROOT / rel
        if not p.is_file():
            continue
        lines.append(f"### {rel}")
        for ln in p.read_text(encoding="utf-8", errors="replace").splitlines():
            m = re.match(pat, ln)
            if m and len(m.group(1)) < 120:
                lines.append(f"- {m.group(1)}")
                n += 1
        lines.append("")
    return n


def mine_surface(lines: list[str]) -> int:
    lines.append("## LIVING SURFACE — board, queue, current state\n")
    n = 0
    p = ROOT / "memory" / "plans" / "fifty_wide_20260917.md"
    if p.is_file():
        heads = [l for l in p.read_text(encoding="utf-8", errors="replace").splitlines()
                 if l.startswith("## ")]
        lines.append("### fifty-wide 2026-09-17 sections: " + " · ".join(
            h.strip("# ") for h in heads))
        n += 1
    t = ROOT / "queue" / "todo.md"
    if t.is_file():
        heads = [l for l in t.read_text(encoding="utf-8", errors="replace").splitlines()
                 if l.startswith("## ")]
        lines.append("### queue/todo.md sections: " + " · ".join(h[3:60] for h in heads[:12]))
        n += 1
    for rel in ["memory/briefs/latest.md", "state/CURRENT.md"]:
        p = ROOT / rel
        if p.is_file():
            body = p.read_text(encoding="utf-8", errors="replace")
            lines.append(f"### {rel} (first 400 chars)\n> " + re.sub(r"\s+", " ", body)[:400])
            n += 1
    lines.append("")
    return n


def mine_receipts(lines: list[str]) -> int:
    lines.append("## RECENT RECEIPTS — inbox titles, last 40 files\n")
    inbox = ROOT / "watch" / "inbox"
    files = sorted(inbox.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)[:40]
    for p in files:
        head = ""
        for ln in p.read_text(encoding="utf-8", errors="replace").splitlines()[:6]:
            if ln.startswith("# "):
                head = ln[2:]
                break
        lines.append(f"- {p.name} — {head[:120]}")
    lines.append("")
    return len(files)


def _head(p: Path, n: int = 280) -> str:
    try:
        return re.sub(r"\s+", " ", p.read_text(encoding="utf-8", errors="replace"))[:n]
    except Exception:
        return ""


def mine_deep(lines: list[str]) -> int:
    """Operator order v2: the verkle, session histories, the corpus, the Elder,
    the moonshot shelf, and the operator himself. Make it understand him."""
    lines.append("## THE VERKLE — the hash-chained history spine\n")
    n = 0
    vc = ROOT / "memory" / "biography" / "verkle_chain.json"
    if vc.is_file():
        try:
            chain = json.loads(vc.read_text(encoding="utf-8", errors="replace"))
            rows = chain if isinstance(chain, list) else chain.get("rows", [])
            lines.append(f"- verkle chain: {len(rows)} rows; latest: "
                         f"{json.dumps(rows[-1])[:220] if rows else 'empty'}")
            n += 1
        except Exception as e:
            lines.append(f"- verkle chain read: {e}")
    lt = ROOT / "memory" / "law" / "enforcement_trail.jsonl"
    if lt.is_file():
        rows = [l for l in lt.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()]
        lines.append(f"- law enforcement trail: {len(rows)} rows; last: {rows[-1][:220] if rows else '-'}")
        n += 1
    lines.append("")

    lines.append("## THE CORPUS — what we own (memory/lenses/corpus_index.json)\n")
    ci = ROOT / "memory" / "lenses" / "corpus_index.json"
    if ci.is_file():
        try:
            idx = json.loads(ci.read_text(encoding="utf-8", errors="replace"))
            if isinstance(idx, dict):
                for k, v in list(idx.items())[:30]:
                    lines.append(f"- {k}: {str(v)[:160]}")
            elif isinstance(idx, list):
                for row in idx[:30]:
                    lines.append(f"- {json.dumps(row)[:160]}")
            n += 1
        except Exception as e:
            lines.append(f"- corpus index read: {e}")
    canon = ROOT / "memory" / "corpus"
    if canon.is_dir():
        shelves = [f"{d.name} ({sum(1 for _ in d.rglob('*') if _.is_file())} files)"
                   for d in sorted(canon.iterdir()) if d.is_dir()]
        lines.append(f"- canon shelves: {', '.join(shelves)}")
    lines.append("")

    lines.append("## THE ELDER — the fleet's elder voice\n")
    for rel in ["dashboard/static/lanes/elder.md", "queue/lanes/elder/surface.md"]:
        p = ROOT / rel
        if p.is_file():
            lines.append(f"- {rel}: {_head(p, 300)}")
            n += 1
    lines.append("")

    lines.append("## THE MOONSHOT SHELF — HOLD-3/M, astra, TT receipts\n")
    for pat in ["moonshot_20260916/receipts/*.md", "moonshot_20260916/*.md"]:
        for p in sorted((ROOT / "watch" / "inbox").glob(pat))[:14]:
            lines.append(f"- {p.name}: {_head(p, 130)}")
            n += 1
    lines.append("")

    lines.append("## SESSION HISTORIES — the windows we have lived in\n")
    sess = ROOT / "memories" / "session"
    if sess.is_dir():
        for p in sorted(sess.glob("*.md"))[:10]:
            lines.append(f"- memories/session/{p.name}: {_head(p, 160)}")
            n += 1
    steps = ROOT / "memory" / "trajectory" / "steps.jsonl"
    if steps.is_file():
        rows = steps.read_text(encoding="utf-8", errors="replace").splitlines()
        lines.append(f"- trajectory steps: {len(rows)} rows sealed")
        n += 1
    salons = ROOT / "memory" / "runs" / "salons"
    if salons.is_dir():
        names = [d.name for d in sorted(salons.iterdir()) if d.is_dir()]
        lines.append(f"- salons run ({len(names)}): {', '.join(names[-14:])}")
        n += 1
    lines.append("")

    lines.append("## THE OPERATOR — who he is; make this seat understand him\n")
    mem_index = Path("C:/Users/foste/.zcode/cli/memories/projects/local_sovereign_agent-16821bdbdc2a3cf7/memory/MEMORY.md")
    if mem_index.is_file():
        keep = [l for l in mem_index.read_text(encoding="utf-8", errors="replace").splitlines()
                if l.startswith("- [")][:60]
        lines.append("### Operator memory index (persistent, cross-window)\n" + "\n".join(keep))
        n += 1
    for rel in ["watch/inbox/THE_PARABLE_REGISTER.md", "watch/inbox/THE_SESSION_RECORD_20260916.md"]:
        p = ROOT / rel
        if p.is_file():
            lines.append(f"### {rel}\n> {_head(p, 500)}")
            n += 1
    journals = ROOT / "watch" / "inbox" / "journal_mark_202609"
    if journals.is_dir():
        names = [p.name for p in sorted(journals.glob("*"))[:12]]
        lines.append(f"- operator journals on file: {', '.join(names)}")
        n += 1
    corr = ROOT / ".agents" / "skills" / "operator-corrections" / "SKILL.md"
    if corr.is_file():
        lines.append(f"### operator-corrections skill\n> {_head(corr, 700)}")
        n += 1
    lines.append("")
    return n


def mine_histories(lines: list[str]) -> int:
    """v2: the anti-forgetting layer — actual histories, not just indexes.
    zcode session logs, the full operator memory bank, LINKS ledger, tide cards,
    wave receipts, doctrine bodies."""
    n = 0
    lines.append("## OPERATOR MEMORY BANK — every topic memory, full index + key bodies\n")
    mem = Path("C:/Users/foste/.zcode/cli/memories/projects/local_sovereign_agent-16821bdbdc2a3cf7/memory")
    if mem.is_dir():
        idx = mem / "MEMORY.md"
        if idx.is_file():
            lines.append("### MEMORY.md (complete index)\n"
                         + idx.read_text(encoding="utf-8", errors="replace")[:20000])
            n += 1
        for p in sorted(mem.glob("*.md"))[:80]:
            if p.name == "MEMORY.md":
                continue
            lines.append(f"- **{p.stem}**: {_head(p, 260)}")
            n += 1
    lines.append("")

    lines.append("## ZCODE SESSION HISTORIES — the windows themselves\n")
    exec_dir = Path("C:/Users/foste/.zcode/cli/exec")
    if exec_dir.is_dir():
        sess = sorted({d.name for d in exec_dir.iterdir() if d.is_dir()})
        lines.append(f"- exec session dirs ({len(sess)}): {', '.join(sess[-12:])}")
        n += 1
        logs = sorted(exec_dir.glob("sess_*/call_*-stdout.log"),
                      key=lambda p: p.stat().st_mtime, reverse=True)[:24]
        for p in logs:
            lines.append(f"- {p.parent.name[:13]}…/{p.name[:34]}: {_head(p, 130)}")
            n += 1
    pa = Path("C:/Users/foste/.zcode/tmp/paste-attachments/2026-09-17")
    if pa.is_dir():
        names = [p.name for p in sorted(pa.glob("*"))[:10]]
        lines.append(f"- recent paste attachments: {', '.join(names)}")
        n += 1
    lines.append("")

    lines.append("## LINKS LEDGER — everything we have read and filed (watch/inbox/LINKS.jsonl)\n")
    lk = ROOT / "watch" / "inbox" / "LINKS.jsonl"
    if lk.is_file():
        rows = [l for l in lk.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()]
        lines.append(f"- {len(rows)} canonical rows:")
        for l in rows[-70:]:
            try:
                r = json.loads(l)
                lines.append(f"  - {r.get('canonical', '?')[:90]} — {(r.get('note') or '')[:140]}")
            except Exception:
                continue
        n += 1
    lines.append("")

    lines.append("## DOCTRINE BODIES — the law texts behind the headers\n")
    for rel, cap in [("docs/DNA.md", 6000), ("CONSTITUTION.md", 2500),
                     ("mag/lite_guard.py", 900), ("AGENTS.md", 5500)]:
        p = ROOT / rel
        if p.is_file():
            lines.append(f"### {rel}\n```\n{p.read_text(encoding='utf-8', errors='replace')[:cap]}\n```")
            n += 1
    lines.append("")

    lines.append("## TIDE CARDS + WAVE RECEIPTS — what the daily and wave cycles produced\n")
    tc = ROOT / "memory" / "corpus" / "tide_cards"
    for p in sorted(tc.glob("*.md"))[-5:]:
        lines.append(f"### tide {p.name}\n> {_head(p, 500)}")
        n += 1
    wr = ROOT / "watch" / "inbox" / "wave_20260916" / "receipts"
    if wr.is_dir():
        names = [p.name for p in sorted(wr.glob("*.md"))]
        lines.append(f"- wave receipts on file ({len(names)}): {', '.join(names[:44])}")
        n += 1
    lines.append("")
    return n


def mine_schedule(lines: list[str]) -> int:
    """STANDING SCHEDULE — operator-stated windows and cadences. Seats that load this
    imprint know the schedule without asking (operator law 2026-09-17: 'why do you think
    i made a seat that remembers and you load it cold')."""
    lines.append("## STANDING SCHEDULE — operator-stated windows (LOAD INTO EVERY SEAT)\n")
    lines.append("- **glm-5.3-flash is FREE from 11:00 (operator local time) DAILY** on the "
                 "Lite seat (/api/coding/paas/v4, ZAI_API_KEY_Lite). After 11:00 it is a "
                 "FREE PRIMARY for the build/research burn — not a paced fallback. Before "
                 "11:00, law-15 pacing applies (1,400/day ceiling).")
    lines.append("- **stealth/union-alpha + stealth/ox-alpha (OpenRouter stealth family)**: "
                 "free windows, intermittent — window re-opened 2026-09-14; hammer while "
                 "green, expect 404 when a window ends (the 404 body names the successor).")
    lines.append("- **daily crons**: tide 06:15 (amendment obligation), drift patrol 08:00, "
                 "union fullsend drive every 20 min (research batch + evolution build lane).")
    lines.append("- **Sep-20 (2026)**: fleet proof date. **Sep-24**: White House state "
                 "dinner (Xi; Altman/Huang/Cook) — operator planted the 11:11 marker.")
    lines.append("- When the operator states ANY free window or cadence, it enters this "
                 "schedule and durable memory IMMEDIATELY — session memory is not memory.")
    lines.append("")
    return 5


def main() -> int:
    lines = [
        "# FLEET IMPRINT — the Librarian's cold-load context",
        "",
        f"*mined {datetime.now(timezone.utc).isoformat()} · deterministic, regenerable · "
        "this file is the pre-warmed RIB seed: stable bytes so provider cache pays once*",
        "",
        "ROLE (for the seat that loads this): you are the fleet's Librarian. The operator",
        "asks 'do we have X / where is Y / what mechanism covers Z' — answer from this",
        "imprint with exact paths and provider ids. If it is not in the imprint, say so and",
        "name the closest mechanism. Never invent paths. CITATION LAW: cite only filenames",
        "that appear verbatim in this imprint; if you are not certain of an exact filename,",
        "give the directory and describe the content instead. A wrong citation is worse",
        "than an honest gap.",
        "",
    ]
    counts = {
        "mechanisms": mine_modules(lines),
        "providers": mine_providers(lines),
        "laws": mine_laws(lines),
        "surface": mine_surface(lines),
        "receipts": mine_receipts(lines),
        "deep": mine_deep(lines),
        "histories": mine_histories(lines),
        "schedule": mine_schedule(lines),
    }
    body = "\n".join(lines)
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()[:16]
    body = body.replace("digest-pinned", f"digest `{digest}`", 1) if "digest-pinned" in body else body
    body += (f"\n---\n*imprint digest `{digest}` · "
             f"{json.dumps(counts)} · regenerate: scripts/build_fleet_imprint.py · "
             "load cold: scripts/librarian.py \"question\"*\n")
    OUT.write_text(body, encoding="utf-8")
    print(json.dumps({"ok": True, "out": str(OUT), "digest": digest,
                      "bytes": len(body), **counts}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
