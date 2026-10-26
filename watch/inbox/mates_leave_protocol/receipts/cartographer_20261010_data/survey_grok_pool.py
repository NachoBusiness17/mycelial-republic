"""Cartographer cycle 20261010: survey grok_sessions pool.

Dedupe census (unique chat_history.jsonl hashes), per-chat metadata rows.
Read-only on corpus. Writes logs/mates/cartographer/grok_survey.jsonl.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
POOL = ROOT / "corpus" / "oral_history" / "seat_pools" / "grok_sessions"
OUT = ROOT / "logs" / "mates" / "cartographer" / "grok_survey.jsonl"


def first_user_text(chat_path):
    try:
        with chat_path.open("r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                if rec.get("type") != "user":
                    continue
                c = rec.get("content")
                texts = []
                if isinstance(c, str):
                    texts = [c]
                elif isinstance(c, list):
                    for part in c:
                        if isinstance(part, dict) and part.get("type") == "text":
                            texts.append(part.get("text") or "")
                for t in texts:
                    s = t.strip()
                    if s and not s.startswith("<user_info>") and not s.startswith("<environment>"):
                        return s
    except Exception:
        return None
    return None


def main():
    hash_to_chat = {}
    total_chats = 0
    total_files = 0
    bytes_total = 0
    name_counts = {}
    lanes = {}
    rows = []
    for f in POOL.rglob("*"):
        if not f.is_file():
            continue
        total_files += 1
        bytes_total += f.stat().st_size
        name_counts[f.name] = name_counts.get(f.name, 0) + 1
        lane = f.relative_to(POOL).parts[0] if len(f.relative_to(POOL).parts) > 1 else "(root)"
        lanes[lane] = lanes.get(lane, 0) + 1
        if f.name != "chat_history.jsonl":
            continue
        total_chats += 1
        b = f.read_bytes()
        h = hashlib.sha256(b).hexdigest()
        if h in hash_to_chat:
            continue
        hash_to_chat[h] = f
        meta = {}
        sp = f.parent / "summary.json"
        if sp.exists():
            try:
                meta = json.loads(sp.read_text(encoding="utf-8", errors="replace"))
            except Exception:
                meta = {}
        info = meta.get("info") or {}
        rows.append({
            "hash": h[:16],
            "lane": lane,
            "dir": f.parent.name,
            "bytes": len(b),
            "title": (meta.get("generated_title") or meta.get("session_summary") or "")[:200],
            "agent_name": meta.get("agent_name"),
            "model": meta.get("current_model_id"),
            "created_at": meta.get("created_at"),
            "updated_at": meta.get("updated_at"),
            "num_messages": meta.get("num_messages"),
            "cwd": info.get("cwd"),
            "first_user": (first_user_text(f) or "")[:400],
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as out:
        for r in rows:
            out.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(json.dumps({
        "grok_files_total": total_files,
        "grok_bytes_total": bytes_total,
        "chat_history_files": total_chats,
        "unique_chat_hashes": len(hash_to_chat),
        "duplicate_chat_copies": total_chats - len(hash_to_chat),
        "lanes": len([k for k in lanes if k != "(root)"]),
        "file_name_top": sorted(name_counts.items(), key=lambda kv: -kv[1])[:12],
        "per_lane_files": lanes,
    }, indent=2))


if __name__ == "__main__":
    main()
