"""Cartographer cycle 20261010: walk session_index.jsonl codex threads.

Extracts per thread: first user ask, last assistant word, filed markers.
Writes rows to logs/mates/cartographer/codex_walk.jsonl. Read-only on corpus.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
POOL = ROOT / "corpus" / "oral_history" / "seat_pools"
OUT = ROOT / "logs" / "mates" / "cartographer" / "codex_walk.jsonl"

FILED_MARKERS = [
    "watch/inbox", "watch\\inbox",
    "state/", "state\\",
    "docs/", "docs\\",
    "memory/", "memory\\",
    "queue/",
]

WRITE_MARKERS = ["apply_patch", "set_file_contents", "write_file", "> ", "Out-File", "Set-Content"]


def text_of(payload):
    parts = payload.get("content") or []
    out = []
    if isinstance(parts, dict):
        parts = [parts]
    for p in parts:
        if isinstance(p, dict):
            t = p.get("text") or p.get("input_text") or ""
            if t:
                out.append(t)
    return "\n".join(out)


def walk_rollout(path):
    first_user = None
    last_assistant = None
    n_lines = 0
    n_user = 0
    n_assistant = 0
    n_calls = 0
    patch_hits = 0
    filed_hits = {}
    with path.open("r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            n_lines += 1
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            p = rec.get("payload") or {}
            t = rec.get("type")
            if t == "response_item":
                pt = p.get("type")
                if pt == "message":
                    role = p.get("role")
                    body = text_of(p)
                    if role == "user" and body:
                        n_user += 1
                        if first_user is None:
                            first_user = body
                    elif role == "assistant" and body:
                        n_assistant += 1
                        last_assistant = body
                elif pt in ("function_call", "custom_tool_call", "local_shell_call"):
                    n_calls += 1
                    raw = json.dumps(p)[:4000]
                    if "apply_patch" in raw:
                        patch_hits += 1
                    for m in FILED_MARKERS:
                        if m in raw:
                            filed_hits[m] = filed_hits.get(m, 0) + 1
            elif t == "event_msg":
                pt = p.get("type")
                if pt == "agent_message":
                    body = p.get("message") or ""
                    if body:
                        n_assistant += 1
                        last_assistant = body
                elif pt == "user_message":
                    body = p.get("message") or ""
                    if body:
                        n_user += 1
                        if first_user is None:
                            first_user = body
    return {
        "lines": n_lines,
        "user_msgs": n_user,
        "assistant_msgs": n_assistant,
        "tool_calls": n_calls,
        "apply_patch_calls": patch_hits,
        "filed_markers": filed_hits,
        "first_user": (first_user or "")[:600],
        "last_assistant": (last_assistant or "")[:900],
    }


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rollouts = {}
    for f in (POOL / "codex_sessions").rglob("rollout-*.jsonl"):
        m = re.search(r"-([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\.jsonl$", f.name)
        if m:
            rollouts.setdefault(m.group(1), []).append(f)

    idx_rows = []
    with (POOL / "session_index.jsonl").open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if not r.get("pool"):
                idx_rows.append(r)

    n_written = 0
    with OUT.open("w", encoding="utf-8") as out:
        for r in idx_rows:
            tid = r["id"]
            files = rollouts.get(tid, [])
            row = {
                "id": tid,
                "thread_name": r.get("thread_name"),
                "updated_at": r.get("updated_at"),
                "rollouts_found": len(files),
            }
            if files:
                f = files[0]
                row["rollout"] = str(f.relative_to(POOL))
                row["bytes"] = f.stat().st_size
                row.update(walk_rollout(f))
            else:
                row["rollout"] = None
                row["note"] = "no rollout file matched id"
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
            n_written += 1

    indexed_ids = {r["id"] for r in idx_rows}
    print(json.dumps({
        "index_codex_rows": len(idx_rows),
        "unique_ids": len(indexed_ids),
        "rows_written": n_written,
        "rollout_files_on_disk": len(rollouts),
        "unindexed_rollout_ids": sorted(set(rollouts) - indexed_ids),
    }, indent=2))


if __name__ == "__main__":
    main()
