"""corpus_selfsteal -- index our own gaming corpus, plans and directories, then mark every
research lead as ALREADY HELD or GAP.

Operator (2026-09-15): "self steal our gaming corpus, our plans our directories etc" and then
"this is all solved problems".

That is the right frame and it changes the deliverable. A 50-wide fan-out that digs up what we
already own is waste. So this module does the other half deterministically, at $0, with no model:

  1. WALK the in-house surfaces that hold game/steal/plan material.
  2. HASH every file (sha256) -- because the same note often exists in three directories, and
     "we already have this" is only credible with a hash.
  3. CLASSIFY each file into a theme by its own words, and keep the title + date.
  4. MAP the 50-question research battery onto the index by keyword overlap.
     ALREADY_HELD  -- the corpus has >= 3 files on the question's terms
     PARTIAL       -- 1-2 files
     GAP           -- nothing in-house
  5. Report duplicates by digest: the same content living twice is a solved problem twice.

RUN:
  python -m mag.corpus_selfsteal index    # walk + hash + classify -> INDEX.json
  python -m mag.corpus_selfsteal map      # battery -> ALREADY_HELD / PARTIAL / GAP
  python -m mag.corpus_selfsteal status

Schema: corpus_selfsteal.v1 . deterministic, $0, READ-ONLY (writes only its own index + pack)
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from config import ROOT
except Exception:
    ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT))

SCHEMA = "corpus_selfsteal.v1"
OUT = ROOT / "memory" / "runs" / "corpus_selfsteal"
INDEX = OUT / "INDEX.json"
PACK = OUT / "CORPUS_SELFSTEAL.md"

# the in-house surfaces that hold game / steal / plan material
SURFACES = [
    "research/gaming_corpus",
    "watch/corpus",
    "memory/steal",
    "memory/game",
    "memory/game_modules",
    "memory/narrative_corpus",
    "campaigns",
    "docs/ref/steals",
    "resource",
]
SURFACE_GLOBS = ["watch/*.md", "docs/ref/*GAME*.md", "docs/ref/*STEAL*.md", "docs/ref/*SQUASH*.md",
                 "memory/improve/*.md", "jobs/*/seat_contract.json", "queue/*.md"]
TEXT_EXT = {".md", ".txt", ".json", ".jsonl", ".yaml", ".yml", ".py"}

THEMES: dict[str, tuple[str, ...]] = {
    "L0-contract": ("l0", "contract", "six function", "verifier", "reason code", "legal("),
    "L1-engine": ("l1", "engine", "fixture", "mechanics", "sowing", "race/dice", "capture"),
    "L2-static": ("l2", "static", "sudoku", "hitori", "kakuro", "nonogram", "riichi", "nikoli"),
    "L3-pack": ("l3", "pack", "variant", "provenance", "cultural", "uncertainty"),
    "L4-instance": ("l4", "instance", "campaign", "dungeon", "room"),
    "rpg/narrative": ("rpg", "narrative", "story", "hero", "oracle", "2d6", "dnd"),
    "steal/gwaps": ("steal", "gwap", "work", "fun", "loot", "agreement"),
    "world/verkle": ("verkle", "world_state", "knot", "root", "chain", "replay"),
    "hosting/ops": ("host", "server", "deploy", "docker", "mysql", "port", "bandwidth"),
    "modding/tools": ("mpq", "dbc", "noggit", "modding", "map extractor", "vmaps", "client"),
    "legal/preservation": ("license", "gpl", "agpl", "copyright", "preservation", "dmca"),
    "raises/casts": ("ractor", "kabuki", "salon", "persona", "ocean", "conductor"),
    "research/meta": ("research", "corpus", "index", "atlas", "brief", "plan"),
}

_STOP = set("""the a an and or of to in for on with by is are was were be been that this these those it its as at from we our you your they their he she his her not no do does did how what which who whom when where why all any both each few more most other some such only own same so than too very can will just should now also into over after before under above between out up down off again further then once here there about against during without within across per via using use used make made get got give given take taken see seen say said know known think thought want wanted need needed may might must shall would could""".split())


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _tokens(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9_]{3,}", text.lower())
    return {w for w in words if w not in _STOP}


def _title(text: str, path: Path) -> str:
    for ln in text.splitlines()[:40]:
        s = ln.strip()
        if s.startswith("# "):
            return s[2:].strip()[:90]
    for ln in text.splitlines()[:6]:
        s = ln.strip()
        if s and not s.startswith(("---", "/*", "//")):
            return s[:90]
    return path.stem


def _date(text: str, path: Path) -> str | None:
    m = re.search(r"(20\d{2})[-_./](\d{2})[-_./](\d{2})", text[:400] + path.name)
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else None


def _files() -> list[Path]:
    out: list[Path] = []
    for s in SURFACES:
        d = ROOT / s
        if d.is_dir():
            out += [p for p in d.rglob("*") if p.is_file() and p.suffix.lower() in TEXT_EXT]
    for g in SURFACE_GLOBS:
        out += [p for p in ROOT.glob(g) if p.is_file() and p.suffix.lower() in TEXT_EXT]
    return sorted(set(out))


def index() -> dict[str, Any]:
    rows = []
    for p in _files():
        try:
            raw = p.read_bytes()
        except Exception:
            continue
        if len(raw) > 3_000_000:
            continue
        text = raw.decode("utf-8", errors="replace")
        toks = _tokens(text)
        themes = sorted(t for t, keys in THEMES.items() if any(k in text.lower() for k in keys))
        spec = _specific_tokens(text)
        rows.append({
            "path": str(p.relative_to(ROOT)).replace("\\", "/"),
            "bytes": len(raw),
            "sha256_12": hashlib.sha256(raw).hexdigest()[:12],
            "title": _title(text, p),
            "date": _date(text, p),
            "themes": themes[:3],
            "tokens": len(toks),
            "specific_terms": sorted(spec)[:400],
            "keyword_sample": sorted(toks)[:12],
        })
    dup: dict[str, list[str]] = {}
    for r in rows:
        dup.setdefault(r["sha256_12"], []).append(r["path"])
    dups = {h: ps for h, ps in dup.items() if len(ps) > 1}
    by_theme: dict[str, int] = {}
    for r in rows:
        for t in r["themes"]:
            by_theme[t] = by_theme.get(t, 0) + 1
    result = {
        "ok": True, "schema": SCHEMA, "ts": _now(),
        "root": str(ROOT), "surfaces": SURFACES, "files": len(rows),
        "total_bytes": sum(r["bytes"] for r in rows),
        "by_theme": dict(sorted(by_theme.items(), key=lambda kv: -kv[1])),
        "duplicate_groups": len(dups),
        "duplicate_files": sum(len(v) for v in dups.values()),
        "duplicates": dups,
        "index": rows,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    INDEX.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    return result


def _battery() -> list[tuple[str, str, str]]:
    from mag.research_fanout import BATTERY
    return BATTERY


def _specific_tokens(text: str) -> set[str]:
    """Only terms that can actually identify an answer: identifiers, tech terms with digits or
    hyphens, proper nouns, and long words. Generic game/research vocabulary is excluded, because
    a keyword overlap on 'server' or 'content' is noise, not a held answer."""
    generic = {
        "server", "servers", "content", "game", "games", "world", "player", "players", "data",
        "system", "systems", "design", "project", "projects", "engine", "engines", "state",
        "states", "test", "tests", "testing", "which", "these", "those", "their", "there",
        "should", "would", "could", "about", "after", "before", "between", "where", "while",
        "list", "name", "give", "describe", "compare", "summarise", "summarize", "explain",
        "what", "when", "with", "from", "into", "than", "then", "them", "they", "this", "that",
    }
    out: set[str] = set()
    for w in re.findall(r"[A-Za-z][A-Za-z0-9_\-]{4,}", text):
        low = w.lower()
        if low in generic:
            continue
        # proper nouns mid-sentence, identifiers, hyphenated/digit-bearing tech terms, long words
        if (re.search(r"[A-Z]", w[1:]) or "-" in w or re.search(r"\d", w) or len(w) >= 8):
            out.add(low)
    return out


def map_battery(threshold: int = 3) -> dict[str, Any]:
    """Mark every research question ALREADY_HELD / PARTIAL / GAP against our own corpus.

    Scored on SPECIFIC terms only. `best` counts distinct specific terms the file actually
    contains -- so a hit means the file talks about *this* thing, not about games in general.
    """
    if not INDEX.is_file():
        index()
    d = json.loads(INDEX.read_text(encoding="utf-8"))
    rows = d["index"]
    out, held, partial, gap = [], [], [], []
    for qid, theme, q in _battery():
        qt = _specific_tokens(q)
        scored = []
        for r in rows:
            hay = set(r.get("specific_terms") or [])
            if not hay:
                hay = _specific_tokens(r["title"] + " " + " ".join(r["keyword_sample"]))
            score = len(qt & hay)
            if score:
                scored.append((score, r["path"], r["title"]))
        scored.sort(reverse=True)
        top = scored[:3]
        best = top[0][0] if top else 0
        # normalise: 3 hits out of 40 question-terms is overlap, not a held answer
        ratio = round(best / max(1, len(qt)), 3)
        verdict = ("ALREADY_HELD" if ratio >= 0.25 else
                   "PARTIAL" if ratio >= 0.12 else "GAP")
        {"ALREADY_HELD": held, "PARTIAL": partial, "GAP": gap}[verdict].append(qid)
        out.append({"qid": qid, "theme": theme, "verdict": verdict, "best_score": best,
                    "terms_in_question": len(qt), "ratio": ratio,
                    "specific_terms": sorted(qt)[:8],
                    "top": [{"score": s, "path": p, "title": t} for s, p, t in top]})
    return {"ok": True, "schema": SCHEMA, "ts": _now(),
            "questions": len(out), "already_held": len(held), "partial": len(partial),
            "gap": len(gap), "verdicts": {"ALREADY_HELD": held, "PARTIAL": partial, "GAP": gap},
            "map": out, "corpus_files": d["files"], "corpus_bytes": d["total_bytes"],
            "method": "specific-term overlap only (proper nouns, identifiers, digits/hyphens, "
                      "words >=8 chars); generic game vocabulary excluded"}


def held() -> dict[str, Any]:
    """The in-house files that actually carry game/steal/world material, by name."""
    if not INDEX.is_file():
        index()
    d = json.loads(INDEX.read_text(encoding="utf-8"))
    keys = ("wow", "game", "steal", "mud", "mmo", "play", "corpus", "l0", "l1", "l2", "l3",
            "campaign", "dungeon", "world")
    rows = [r for r in d["index"]
            if any(k in r["path"].lower() for k in keys)]
    rows.sort(key=lambda r: r["path"])
    return {"ok": True, "schema": SCHEMA, "files": len(rows),
            "total_bytes": sum(r["bytes"] for r in rows),
            "files_detail": [{"path": r["path"], "bytes": r["bytes"], "title": r["title"],
                              "date": r["date"]} for r in rows]}


def pack() -> dict[str, Any]:
    """Write the human-facing self-steal pack."""
    d = json.loads(INDEX.read_text(encoding="utf-8")) if INDEX.is_file() else index()
    m = map_battery()
    L = ["# CORPUS SELF-STEAL — what we already hold (and what we do not)", "",
         f"*{d['files']} files · {d['total_bytes']/1048576:.1f} MB · "
         f"{d['duplicate_groups']} duplicate groups · generated {d['ts']}*", "",
         "> Deterministic, $0, no model. Every row is a file on disk with a sha256. A question is "
         "`ALREADY_HELD` when at least a quarter of its SPECIFIC terms (proper nouns, identifiers, "
         "digit/hyphen terms, words ≥8 chars — generic game vocabulary excluded) appear in one "
         "in-house file; `PARTIAL` at an eighth; otherwise `GAP`. The theme counts below are "
         "keyword tags, not a classification — one loose term can tag hundreds of files.", "",
         "## Files by theme", ""]
    for t, n in d["by_theme"].items():
        L.append(f"- **{t}** — {n} files")
    L += ["", "## Duplicates (same content, more than one home)", ""]
    if d["duplicates"]:
        for h, ps in list(d["duplicates"].items())[:25]:
            L.append(f"- `{h}` ×{len(ps)}: " + " · ".join(f"`{p}`" for p in ps))
    else:
        L.append("- none")
    L += ["", "## The 50 questions against our own corpus", "",
          f"**{m['already_held']} already held · {m['partial']} partial · {m['gap']} gap**", "",
          "| id | verdict | best | nearest in-house |", "|---|---|---:|---|"]
    for r in m["map"]:
        near = r["top"][0]["path"] if r["top"] else "—"
        L.append(f"| {r['qid']} | {r['verdict']} | {r['best_score']} | `{near}` |")
    L += ["", "## GAP list (the only questions worth asking anyone)", ""]
    for r in m["map"]:
        if r["verdict"] == "GAP":
            L.append(f"- **{r['qid']}** — {next(q for i, t, q in _battery() if i == r['qid'])}")
    PACK.write_text("\n".join(L), encoding="utf-8")
    return {"ok": True, "schema": SCHEMA, "pack": str(PACK), "files": d["files"],
            "already_held": m["already_held"], "partial": m["partial"], "gap": m["gap"],
            "gap_ids": m["verdicts"]["GAP"],
            "receipt": str(OUT / "receipt.json")}


def status() -> dict[str, Any]:
    return {"ok": True, "schema": SCHEMA, "surfaces": len(SURFACES),
            "index_exists": INDEX.is_file(), "pack_exists": PACK.is_file(),
            "out": str(OUT),
            "cost": "deterministic + $0 (walks local files only)"}


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="corpus-selfsteal")
    ap.add_argument("cmd", nargs="?", default="status",
                    choices=["index", "map", "held", "pack", "status"])
    a = ap.parse_args(argv)
    if a.cmd == "index":
        out = index()
        out = {"ok": True, "schema": SCHEMA, "files": out["files"],
               "total_bytes": out["total_bytes"], "by_theme": out["by_theme"],
               "duplicate_groups": out["duplicate_groups"], "index": str(INDEX)}
    elif a.cmd == "held":
        h = held()
        out = {"ok": True, "schema": SCHEMA, "files": h["files"],
               "total_bytes": h["total_bytes"],
               "sample": [f["path"] for f in h["files_detail"][:40]]}
    else:
        out = {"map": map_battery, "pack": pack, "status": status}[a.cmd]()
    print(json.dumps(out, ensure_ascii=False, indent=2, default=str)[:3500])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
