"""Classify research-pack answers by topic -> knowledge base + training rows.

The missing research->training loop: research_rig archives packs flat, but nothing
labels them by topic or folds them into case law. This tool takes a research-pack
answer, tags it with a topic, and folds to:
  - `mag.idea_graph.add_node` (claim/evidence node, edge -> topic)
  - `memory/pile/training_rows.jsonl` (instruction = pack thesis, output = {topic, category, tags})
  - `mag.skill_ledger.record_decision` (case law, task_shape="research-pack")

Mirrors tools/pile_classify STRICT-JSON pattern. Idempotent by pack id.

CLI:
  python tools/classify_pack.py --pack <pack-id-or-path> --topic routing-economics [--dry]
  python tools/classify_pack.py --index                      # list research_packs by topic
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config import ROOT  # noqa: E402

PACKS = ROOT / "memory" / "research_packs"
TRAINING = ROOT / "memory" / "pile" / "training_rows.jsonl"
FOLDED = ROOT / "memory" / "pile" / "classified_packs.jsonl"
VALID_TOPICS = {
    "routing-economics", "memory-context", "observability", "tool-design", "self-correction",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_folded() -> set[str]:
    if not FOLDED.is_file():
        return set()
    out = set()
    for line in FOLDED.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.strip():
            try:
                out.add(json.loads(line).get("pack_id"))
            except json.JSONDecodeError:
                continue
    return out


def _append_folded(pack_id: str, topic: str) -> None:
    FOLDED.parent.mkdir(parents=True, exist_ok=True)
    with FOLDED.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"pack_id": pack_id, "topic": topic, "ts": _now()}, ensure_ascii=False) + "\n")


def _find_pack(pack: str) -> dict[str, Any] | None:
    """Resolve a pack id/slug to its answer text (prefer answer.remote.md / .md / .json)."""
    candidates: list[Path] = []
    if pack.endswith(".md") or pack.endswith(".json"):
        p = Path(pack)
        if p.is_file():
            candidates.append(p)
    for p in PACKS.rglob("*"):
        if p.is_file() and pack.lower() in p.name.lower():
            candidates.append(p)
    if not candidates:
        return None
    # prefer the richest artifact: answer.remote.md > answer.local.md > .md > .json
    def rank(p: Path) -> int:
        n = p.name.lower()
        if "answer.remote" in n:
            return 0
        if "answer.local" in n:
            return 1
        if n.endswith(".md"):
            return 2
        if n.endswith(".json"):
            return 3
        return 4
    p = min(candidates, key=rank)
    try:
        txt = p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None
    return {"path": p, "name": p.stem, "text": txt[:6000]}


def _infer_topic(text: str) -> str:
    low = (text or "").lower()
    for tid, pats in {
        "routing-economics": [r"rout", r"model.picker", r"cascade", r"budget", r"cost", r"provider"],
        "memory-context": [r"memor", r"context", r"recall", r"archiv", r"embed", r"compress"],
        "observability": [r"observ", r"trace", r"span", r"telemetry", r"monitor", r"anomaly"],
        "tool-design": [r"tool", r"serializ", r"mcp", r"edit format", r"function call"],
        "self-correction": [r"correct", r"verif", r"self.?check", r"credit", r"reflection", r"test.time"],
    }.items():
        if any(re.search(p, low) for p in pats):
            return tid
    return ""


def classify_pack(*, pack: str, topic: str | None = None, dry: bool = False) -> dict[str, Any]:
    """Tag a research pack by topic and fold it to KB + training + case law."""
    found = _find_pack(pack)
    if not found:
        return {"ok": False, "error": f"pack not found: {pack}"}
    pack_id = found["name"]
    folded = _load_folded()
    if pack_id in folded:
        return {"ok": True, "skipped": True, "reason": "already folded", "pack_id": pack_id}

    text = found["text"]
    if not topic:
        topic = _infer_topic(text)
    if topic and topic not in VALID_TOPICS:
        return {"ok": False, "error": f"bad topic {topic!r}; want one of {sorted(VALID_TOPICS)}"}
    if not topic:
        return {"ok": False, "error": "could not infer topic; pass --topic"}

    # thesis = first non-heading line
    thesis = ""
    for ln in text.splitlines():
        s = ln.strip()
        if s and not s.startswith(("#", ">", "---", "```")):
            thesis = s[:300]
            break

    result: dict[str, Any] = {"ok": True, "pack_id": pack_id, "topic": topic, "dry": dry}
    if dry:
        result["plan"] = {
            "thesis": thesis,
            "idea_node": {"type": "claim", "title": thesis[:80], "body": thesis, "refs": [str(found["path"])]},
            "training_row": {"instruction": thesis, "output": {"topic": topic, "category": "research", "tags": [topic]}},
        }
        return result

    # 1) idea_graph node (claim) + edge to the topic node
    from mag import idea_graph as ig

    try:
        node = ig.add_node(
            title=thesis[:80] or f"research-pack {pack_id}",
            ntype="claim", status="open",
            body=thesis or text[:1000],
            refs=[str(found["path"])],
            tags=[topic, "research-pack"],
            source="classify_pack",
        )
    except ValueError as e:
        return {"ok": False, "error": f"idea_graph: {e}"}
    # link claim -> topic node (create topic node if missing)
    topic_node = None
    for n in ig.list_nodes(ntype="topic", limit=50):
        if str(n.get("title") or "").strip().lower() == topic:
            topic_node = n
            break
    if not topic_node:
        topic_node = ig.add_node(title=topic, ntype="topic", status="open", source="classify_pack")
    try:
        ig.link(node["id"], topic_node["id"], etype="supports", note=f"research pack {pack_id}", ref=str(found["path"]))
    except ValueError as e:
        result["link_error"] = str(e)
    result["idea_node"] = node["id"]

    # 2) training row
    TRAINING.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "instruction": thesis or f"Classify research pack {pack_id}",
        "output": json.dumps({"topic": topic, "category": "research", "tags": [topic]}),
        "meta": {"source": "classify_pack", "id": pack_id, "tier": "T1"},
    }
    with TRAINING.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    result["training_row"] = row

    # 3) case law
    from mag.skill_ledger import record_decision

    record_decision(
        goal=f"classify research pack {pack_id}",
        task_shape="research-pack", provider="local", model="classify_pack",
        reasoning_level="none", outcome="ok", detail=f"topic={topic} thesis={thesis[:120]}",
        source="classify_pack",
    )
    result["case_law"] = True
    _append_folded(pack_id, topic)
    return result


def index_packs() -> dict[str, Any]:
    """Map research_packs -> topics (folded only) + total counts."""
    folded = _load_folded()
    by_topic: dict[str, int] = {}
    by_topic_rows: dict[str, list[str]] = {}
    for line in FOLDED.read_text(encoding="utf-8", errors="replace").splitlines() if FOLDED.is_file() else []:
        if line.strip():
            try:
                r = json.loads(line)
                t = r.get("topic") or "?"
                by_topic[t] = by_topic.get(t, 0) + 1
                by_topic_rows.setdefault(t, []).append(r.get("pack_id"))
            except json.JSONDecodeError:
                continue
    total = sum(by_topic.values())
    return {"ok": True, "total_folded": total, "folded_ids": len(folded), "by_topic": by_topic, "rows": by_topic_rows}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="classify-pack", description="Classify research packs by topic -> KB + training.")
    ap.add_argument("--pack", default="")
    ap.add_argument("--topic", default="")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--index", action="store_true")
    args = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    if args.index:
        print(json.dumps(index_packs(), indent=2, ensure_ascii=False))
        return 0
    if not args.pack:
        print("usage: classify_pack.py --pack <id-or-path> [--topic X] [--dry] | --index", file=sys.stderr)
        return 1
    print(json.dumps(classify_pack(pack=args.pack, topic=args.topic, dry=args.dry), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
