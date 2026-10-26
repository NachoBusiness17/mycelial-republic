"""Cartographer cycle 20261012: walk the nacho_archaeology shelf (92 threads).

Streams every chat-transcript .jsonl once. Per thread: role, bytes, lines,
first/last user timestamp, real asks, assistant turns, tool census, write
signals (STEAL_/produced/memory/steer paths touched), law/debt text signals.
Read-only on corpus.
"""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SHELF = ROOT / "corpus" / "oral_history" / "nacho_archaeology"
CT = SHELF / "extracted" / "nacho-archaeology-part1-chats-produced" / "chat-transcripts"
OUT = ROOT / "watch" / "inbox" / "mates_leave_protocol" / "receipts" / "cartographer_20261012_data"

WRITE_TOOL_RE = re.compile(
    r"(STEAL_[A-Za-z0-9_]+\.md|speak_proof[_A-Za-z0-9]*\.md|party_subchain[/\\]steer"
    r"|steer_line\.txt|afk_speak_proof[_A-Za-z0-9]*\.py|memory[/\\]steal"
    r"|produced[/\\][A-Za-z0-9_-]+|dashboard[/\\]static[/\\][A-Za-z0-9_/-]+)"
)
LAW_RE = re.compile(r"\b(law|fiat|rib|receipt|debt|ghost|organ|lane|verkle|memlance|self-steal)\b", re.I)
TS_RE = re.compile(r"<timestamp>([^<]+)</timestamp>")


def content_list(msg):
    c = msg.get("content") or []
    if isinstance(c, dict):
        c = [c]
    return c


def walk_file(path):
    row = {
        "id": path.parent.name,
        "file": str(path.relative_to(CT)),
        "bytes": path.stat().st_size,
        "lines": 0,
        "first_ts": None,
        "last_ts": None,
        "user_msgs": 0,
        "assistant_msgs": 0,
        "first_ask": None,
        "asks_sample": [],
        "tools": {},
        "write_targets": Counter(),
        "law_hits": 0,
        "last_assistant_tail": None,
    }
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            row["lines"] += 1
            try:
                rec = json.loads(line)
            except Exception:
                continue
            role = rec.get("role")
            msg = rec.get("message") or {}
            for part in content_list(msg):
                ptype = part.get("type")
                if ptype == "text":
                    body = part.get("text") or ""
                    if role == "user":
                        row["user_msgs"] += 1
                        m = TS_RE.search(body)
                        if m:
                            if row["first_ts"] is None:
                                row["first_ts"] = m.group(1)
                            row["last_ts"] = m.group(1)
                        if row["first_ask"] is None:
                            row["first_ask"] = body[:220]
                        if len(row["asks_sample"]) < 12:
                            row["asks_sample"].append(body[:220])
                        for wm in WRITE_TOOL_RE.finditer(body):
                            row["write_targets"][wm.group(1)] += 1
                        if LAW_RE.search(body):
                            row["law_hits"] += 1
                    elif role == "assistant":
                        row["assistant_msgs"] += 1
                        row["last_assistant_tail"] = body[-400:]
                        for wm in WRITE_TOOL_RE.finditer(body):
                            row["write_targets"][wm.group(1)] += 1
                        if LAW_RE.search(body):
                            row["law_hits"] += 1
                elif ptype == "tool_use":
                    name = part.get("name") or "?"
                    row["tools"][name] = row["tools"].get(name, 0) + 1
                    raw = json.dumps(part.get("input") or {}, ensure_ascii=False)
                    for wm in WRITE_TOOL_RE.finditer(raw):
                        row["write_targets"][wm.group(1)] += 1
    row["write_targets"] = dict(row["write_targets"].most_common(20))
    return row


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    transcripts = sorted(CT.glob("*/*.jsonl"))
    rows = []
    for p in transcripts:
        rows.append(walk_file(p))
    out_path = OUT / "nacho_walk.jsonl"
    with out_path.open("w", encoding="utf-8") as out:
        for r in rows:
            out.write(json.dumps(r, ensure_ascii=False) + "\n")
    tool_totals = Counter()
    for r in rows:
        for k, v in r["tools"].items():
            tool_totals[k] += v
    summary = {
        "threads": len(rows),
        "total_bytes": sum(r["bytes"] for r in rows),
        "total_lines": sum(r["lines"] for r in rows),
        "user_msgs": sum(r["user_msgs"] for r in rows),
        "assistant_msgs": sum(r["assistant_msgs"] for r in rows),
        "tool_totals": dict(tool_totals.most_common()),
        "threads_with_writes": sum(1 for r in rows if r["write_targets"]),
        "threads_zero_writes": sum(1 for r in rows if not r["write_targets"]),
    }
    (OUT / "nacho_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: summary[k] for k in (
        "threads", "total_bytes", "total_lines", "user_msgs", "assistant_msgs",
        "threads_with_writes", "threads_zero_writes")}, indent=2))


if __name__ == "__main__":
    main()
