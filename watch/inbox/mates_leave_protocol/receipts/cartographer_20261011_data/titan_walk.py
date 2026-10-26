"""Cartographer cycle 20261011: segment-walk the titan rollout 01a052ca.

Streams the 306,992,843-byte rollout once. Captures real user asks (preamble
skipped), assistant turns, apply_patch targets, an hour histogram, and the
retraction block. Read-only on corpus.
"""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
POOL = ROOT / "corpus" / "oral_history" / "seat_pools"
OUT = ROOT / "watch" / "inbox" / "mates_leave_protocol" / "receipts" / "cartographer_20261011_data"

TITAN = POOL / "codex_sessions" / "2026" / "08" / "30" / (
    "rollout-2026-08-30T09-09-46-01a052ca-543c-76f2-bf93-53a538bf5b3e.jsonl"
)

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
        targets.append((m.group(1), m.group(2).strip()))
    return targets


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    asks_path = OUT / "titan_asks.jsonl"
    turns_path = OUT / "titan_turns.jsonl"
    patches_path = OUT / "titan_patches.jsonl"
    summary_path = OUT / "titan_summary.json"

    meta = {}
    hour_hist = Counter()
    day_patch = Counter()
    n_lines = 0
    n_user = 0
    n_assistant = 0
    n_calls = 0
    n_patch_calls = 0
    patch_target_counts = Counter()
    retraction_lines = []
    first_ts = None
    last_ts = None

    with TITAN.open("r", encoding="utf-8", errors="replace") as fh, \
         asks_path.open("w", encoding="utf-8") as asks_out, \
         turns_path.open("w", encoding="utf-8") as turns_out, \
         patches_path.open("w", encoding="utf-8") as patches_out:
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
                hour_hist[ts[:13]] += 1
            p = rec.get("payload") or {}
            t = rec.get("type")
            if t == "session_meta":
                meta = {k: p.get(k) for k in ("cwd", "originator", "cli_version", "source")}
            elif t == "response_item":
                pt = p.get("type")
                if pt == "message":
                    role = p.get("role")
                    body = text_of(p)
                    if role == "user" and body:
                        n_user += 1
                        if not any(body.startswith(s) for s in SKIP_PREFIXES):
                            asks_out.write(json.dumps({
                                "line": n_lines, "ts": ts, "text": body[:800],
                            }, ensure_ascii=False) + "\n")
                    elif role == "assistant" and body:
                        n_assistant += 1
                        turns_out.write(json.dumps({
                            "line": n_lines, "ts": ts, "text": body[:400],
                        }, ensure_ascii=False) + "\n")
                        if "stopping all action" in body:
                            retraction_lines.append({"line": n_lines, "ts": ts, "text": body[:2000]})
                elif pt in ("function_call", "custom_tool_call", "local_shell_call"):
                    n_calls += 1
                    raw = json.dumps(p)
                    if "apply_patch" in raw:
                        n_patch_calls += 1
                        if ts:
                            day_patch[ts[:10]] += 1
                        for kind, tgt in patch_targets(raw):
                            patch_target_counts[tgt] += 1
                            patches_out.write(json.dumps({
                                "line": n_lines, "ts": ts, "kind": kind, "target": tgt,
                            }, ensure_ascii=False) + "\n")
            elif t == "event_msg":
                pt = p.get("type")
                if pt == "agent_message":
                    body = p.get("message") or ""
                    if body:
                        n_assistant += 1
                        turns_out.write(json.dumps({
                            "line": n_lines, "ts": ts, "text": body[:400],
                        }, ensure_ascii=False) + "\n")
                        if "stopping all action" in body:
                            retraction_lines.append({"line": n_lines, "ts": ts, "text": body[:2000]})

    summary = {
        "rollout": str(TITAN.relative_to(POOL)),
        "bytes": TITAN.stat().st_size,
        "lines": n_lines,
        "first_ts": first_ts,
        "last_ts": last_ts,
        "meta": meta,
        "user_msgs_total": n_user,
        "assistant_msgs_total": n_assistant,
        "tool_calls": n_calls,
        "apply_patch_calls": n_patch_calls,
        "distinct_patch_targets": len(patch_target_counts),
        "patch_calls_by_day": dict(sorted(day_patch.items())),
        "records_by_hour": dict(sorted(hour_hist.items())),
        "retraction_turns": retraction_lines,
    }
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    with (OUT / "titan_patch_targets.txt").open("w", encoding="utf-8") as out:
        for tgt, cnt in patch_target_counts.most_common():
            out.write(f"{cnt}\t{tgt}\n")
    print(json.dumps({
        "lines": n_lines, "user_total": n_user, "assistant_total": n_assistant,
        "tool_calls": n_calls, "patch_calls": n_patch_calls,
        "distinct_patch_targets": len(patch_target_counts),
        "retraction_turns": len(retraction_lines),
        "first_ts": first_ts, "last_ts": last_ts,
    }, indent=2))


if __name__ == "__main__":
    main()
