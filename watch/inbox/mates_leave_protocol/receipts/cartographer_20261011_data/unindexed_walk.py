"""Cartographer cycle 20261011: walk the codex rollouts absent from session_index.jsonl.

Same walker shape as cycle 20261010's walk_codex_threads.py, pointed at the
UNINDEXED ids instead, plus patch targets, first/last timestamps, and a
law-or-debt text signal. Read-only on corpus.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
POOL = ROOT / "corpus" / "oral_history" / "seat_pools"
OUT = ROOT / "watch" / "inbox" / "mates_leave_protocol" / "receipts" / "cartographer_20261011_data"

FILED_MARKERS = ["watch/inbox", "state/", "docs/", "memory/", "queue/", "corpus/"]

DEBT_WORDS = ["TODO", "todo", "not done", "follow-up", "followup", "deferred",
              "next time", "left as", "out of scope", "didn't finish", "unresolved"]
LAW_WORDS = ["receipt", "RIB", "rib ", "law", "docs/", "state/", "watch/inbox", "registered"]

SKIP_PREFIXES = ("<recommended_plugins", "<user_instructions", "<environment_context",
                 "<system_reminder", "<turn_context", "<permissions")


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


def patch_targets(raw):
    targets = []
    for m in re.finditer(r"\*\*\* (Add|Update|Delete) File: (.+)", raw):
        targets.append(m.group(2).strip())
    return targets


def walk_rollout(path):
    first_user = None
    last_assistant = None
    first_ts = None
    last_ts = None
    n_lines = 0
    n_user = 0
    n_assistant = 0
    n_calls = 0
    patch_hits = 0
    targets = []
    filed_hits = {}
    debt_hits = {}
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
            ts = rec.get("timestamp")
            if ts:
                if first_ts is None:
                    first_ts = ts
                last_ts = ts
            p = rec.get("payload") or {}
            t = rec.get("type")
            if t == "response_item":
                pt = p.get("type")
                if pt == "message":
                    role = p.get("role")
                    body = text_of(p)
                    if role == "user" and body:
                        n_user += 1
                        if first_user is None and not any(body.startswith(s) for s in SKIP_PREFIXES):
                            first_user = body
                    elif role == "assistant" and body:
                        n_assistant += 1
                        last_assistant = body
                elif pt in ("function_call", "custom_tool_call", "local_shell_call"):
                    n_calls += 1
                    raw = json.dumps(p)
                    if "apply_patch" in raw:
                        patch_hits += 1
                        targets.extend(patch_targets(raw))
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
                        if first_user is None and not any(body.startswith(s) for s in SKIP_PREFIXES):
                            first_user = body
    tail = (last_assistant or "")[-1500:]
    for w in DEBT_WORDS:
        if w in tail:
            debt_hits[w] = debt_hits.get(w, 0) + 1
    law_hits = {w: tail.count(w) for w in LAW_WORDS if w in tail}
    if patch_hits > 0:
        shape = "patched"
    elif n_calls > 0 or filed_hits:
        shape = "audit"
    else:
        shape = "bare"
    return {
        "lines": n_lines,
        "first_ts": first_ts,
        "last_ts": last_ts,
        "user_msgs": n_user,
        "assistant_msgs": n_assistant,
        "tool_calls": n_calls,
        "apply_patch_calls": patch_hits,
        "distinct_patch_targets": len(set(targets)),
        "sample_patch_targets": sorted(set(targets))[:10],
        "filed_markers": filed_hits,
        "debt_signal": sorted(debt_hits),
        "law_signal": sorted(law_hits),
        "shape": shape,
        "first_user": (first_user or "")[:600],
        "last_assistant": (last_assistant or "")[:900],
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rollouts = {}
    for f in (POOL / "codex_sessions").rglob("rollout-*.jsonl"):
        m = re.search(r"-([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\.jsonl$", f.name)
        if m:
            rollouts[m.group(1)] = f

    indexed_ids = set()
    with (POOL / "session_index.jsonl").open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if not r.get("pool"):
                indexed_ids.add(r["id"])

    unindexed = {tid: f for tid, f in rollouts.items() if tid not in indexed_ids}
    out_path = OUT / "unindexed_walk.jsonl"
    shapes = {"patched": 0, "audit": 0, "bare": 0}
    total_bytes = 0
    with out_path.open("w", encoding="utf-8") as out:
        for tid in sorted(unindexed, key=lambda k: str(unindexed[k])):
            f = unindexed[tid]
            total_bytes += f.stat().st_size
            row = {"id": tid, "rollout": str(f.relative_to(POOL)),
                   "bytes": f.stat().st_size}
            row.update(walk_rollout(f))
            shapes[row["shape"]] += 1
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps({
        "rollout_ids_on_disk": len(rollouts),
        "indexed_ids": len(indexed_ids),
        "unindexed_walked": len(unindexed),
        "unindexed_bytes": total_bytes,
        "shapes": shapes,
    }, indent=2))


if __name__ == "__main__":
    main()
