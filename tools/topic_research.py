"""Topic-driven research runner — the preemptive-steal loop (tesuji-everywhere).

For a topic, pick the next steal item from its cloned source forest, run T1 focused
research (fetch README/docs), archive a research pack, classify it, and fold to the
knowledge base + training rows. Bound: 1 topic/tick, <=2 steals/topic, top-K files.

This is the "steal-first, no new infra before data" loop: research BEFORE direction.

CLI:
  python tools/topic_research.py --topic routing-economics --dry   # plan the next steal
  python tools/topic_research.py --topic routing-economics          # run it (T1 fetch)
  python tools/topic_research.py --status                           # topic coverage map
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml  # type: ignore

from config import ROOT  # noqa: E402

TOPICS_YAML = ROOT / "configs" / "research_topics.yaml"
PACKS = ROOT / "memory" / "research_packs"
DONE = ROOT / "memory" / "runs" / "topic_research"
MUSEUM = ROOT / "memory" / "research_packs" / "raw"  # fix the dead research_rig path
STEAL_LIMIT = 2  # <=2 steals per topic run


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_topics() -> list[dict[str, Any]]:
    if not TOPICS_YAML.is_file():
        return []
    data = yaml.safe_load(TOPICS_YAML.read_text(encoding="utf-8")) or {}
    return list(data.get("topics") or [])


# filename priority: substantive docs first, boilerplate last
_FNAME_RANK = (
    "readme", "usage", "roadmap", "overview", "design", "architecture",
    "protocol", "delegation", "workflow", "memory", "context", "routing", "agent",
)
_BOILERPLATE = ("changelog", "contributing", "code_of_conduct", "security", "license", "privacy", "release_checklist", "troubleshooting", "test_matrix")


def _rank_file(p: Path) -> int:
    n = p.name.lower()
    if any(b in n for b in _BOILERPLATE):
        return 50
    for i, r in enumerate(_FNAME_RANK):
        if r in n:
            return i
    return 40


def _readme_paths(folder: Path) -> list[Path]:
    """Top-K source docs from a cloned steal forest folder (README/docs first)."""
    out: list[Path] = []
    if not folder.is_dir():
        return out
    for pat in ("README*", "readme*", "docs/**/*.md", "docs/*.md", "*.md", "AGENTS.md", "*.txt"):
        for p in sorted(folder.glob(pat)):
            if p.is_file() and p.stat().st_size > 0:
                out.append(p)
    # dedupe + rank: substantive docs first, then shallow-path tiebreak
    seen: set[Path] = set()
    uniq: list[Path] = []
    for p in sorted(out, key=lambda x: (_rank_file(x), len(x.parts), str(x))):
        if p not in seen:
            seen.add(p)
            uniq.append(p)
    return uniq[:STEAL_LIMIT]


def _seen_keys() -> set[str]:
    if not DONE.is_dir():
        return set()
    out: set[str] = set()
    for f in DONE.glob("*.json"):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            out.add(str(data.get("key") or ""))
        except Exception:
            continue
    return out


def _mark_done(key: str, topic: str, path: Path, steal: str) -> None:
    DONE.mkdir(parents=True, exist_ok=True)
    (DONE / f"{topic}-{re.sub(r'[^A-Za-z0-9_-]', '_', steal)[:40]}.json").write_text(
        json.dumps({"key": key, "topic": topic, "steal": steal, "pack": str(path), "ts": _now()},
                   indent=2, ensure_ascii=False), encoding="utf-8")


def _find_repo_folder(forest: Path, src: str) -> Path | None:
    """Locate a cloned repo folder by name (case-insensitive, recursive)."""
    src_l = str(src).lower()
    for p in forest.rglob("*"):
        if p.is_dir() and p.name.lower() == src_l:
            return p
    return None


def pick_next(topic_id: str) -> dict[str, Any]:
    """Pick the next un-done steal item for a topic (top-K README of its sources)."""
    topics = load_topics()
    t = next((x for x in topics if x.get("id") == topic_id), None)
    if not t:
        return {"ok": False, "error": f"topic not found: {topic_id}"}
    forest = ROOT / str(t.get("source_forest") or "")
    sources = t.get("sources") or []
    seen = _seen_keys()
    for src in sources:
        folder = _find_repo_folder(forest, src)
        if not folder:
            continue
        for p in _readme_paths(folder):
            key = f"{topic_id}:{src}:{p.name}"
            if key in seen:
                continue
            return {
                "ok": True, "topic": topic_id, "topic_title": t.get("title"),
                "source": src, "path": p, "key": key,
                "steal_focus": t.get("steal_focus"),
            }
    return {"ok": True, "action": "exhausted", "topic": topic_id, "detail": f"all steals done for {topic_id}"}


def run_topic(topic_id: str, *, dry: bool = False) -> dict[str, Any]:
    """Run one topic: pick next steal -> T1 focused fetch -> archive pack -> classify -> fold."""
    pick = pick_next(topic_id)
    if not pick.get("ok"):
        return pick
    if pick.get("action") == "exhausted":
        return pick
    src_path: Path = pick["path"]
    key = pick["key"]
    try:
        text = src_path.read_text(encoding="utf-8", errors="replace")[:6000]
    except Exception as e:
        return {"ok": False, "error": f"read {src_path}: {e}"}

    # thesis = first meaningful line
    thesis = ""
    for ln in text.splitlines():
        s = ln.strip()
        if s and not s.startswith(("#", ">", "---", "```")):
            thesis = s[:300]
            break

    slug = f"{topic_id}-{pick['source']}-{src_path.stem}"[:80].lower()
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    pack_path = PACKS / f"{ts}_{slug}.md"
    MUSEUM.mkdir(parents=True, exist_ok=True)

    if dry:
        return {"ok": True, "dry": True, **pick, "thesis": thesis,
                "plan": {"archive": f"{pack_path.name}", "raw": f"{MUSEUM.name}/{ts}_{slug}.raw.txt"}}

    # archive pack (synthesis of the stolen README)
    pack = (
        f"# {pick['topic_title']} — steal: {pick['source']} ({src_path.name})\n"
        f"## Research pack · preemptive-steal · {ts}\n"
        f"> **Thesis:** {thesis}\n\n"
        f"## Source\n- repo: `{pick['source']}` · file: `{src_path}`\n"
        f"- topic: `{topic_id}` · steal_focus: {pick.get('steal_focus')}\n\n"
        f"## Stolen content (raw excerpt)\n```\n{text[:4000]}\n```\n\n"
        f"---\n*Companion: topic_research · classified by classify_pack.*\n"
    )
    PACKS.mkdir(parents=True, exist_ok=True)
    pack_path.write_text(pack, encoding="utf-8")
    (MUSEUM / f"{ts}_{slug}.raw.txt").write_text(
        f"# source: {src_path}\n# topic: {topic_id}\n# ts: {ts}\n\n{text}\n", encoding="utf-8")

    # classify + fold
    from tools.classify_pack import classify_pack

    cf = classify_pack(pack=str(pack_path), topic=topic_id, dry=False)
    _mark_done(key, topic_id, pack_path, pick["source"])
    return {
        "ok": True, "topic": topic_id, "source": pick["source"], "key": key,
        "pack": str(pack_path), "raw": str(MUSEUM / f"{ts}_{slug}.raw.txt"),
        "thesis": thesis, "classify": cf,
    }


def status() -> dict[str, Any]:
    from tools.classify_pack import index_packs

    topics = load_topics()
    seen = _seen_keys()
    out = {"ok": True, "topics": []}
    for t in topics:
        done = sum(1 for k in seen if k.startswith(f"{t['id']}:"))
        out["topics"].append({"id": t["id"], "priority": t.get("priority"), "done_steals": done, "status": t.get("status")})
    out["index"] = index_packs()
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="topic-research", description="Preemptive-steal topic research loop.")
    ap.add_argument("--topic", default="")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    if args.status:
        print(json.dumps(status(), indent=2, ensure_ascii=False))
        return 0
    if not args.topic:
        print("usage: topic_research.py --topic <id> [--dry] | --status", file=sys.stderr)
        return 1
    print(json.dumps(run_topic(args.topic, dry=args.dry), indent=2, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
