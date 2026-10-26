import json, sys, io, collections
from datetime import datetime, timezone

SRC = r"corpus\oral_history\marathon_body\marathon_25fbcaab_20260815_20260820.jsonl"
OUT_ASKS = r"logs\mates\cartographer\marathon_asks.jsonl"
OUT_TOOLS = r"logs\mates\cartographer\marathon_tools.jsonl"
OUT_EDITS = r"logs\mates\cartographer\marathon_edits.jsonl"
OUT_SUM = r"logs\mates\cartographer\marathon_summary.json"

def ts_str(ms):
    if not ms:
        return ""
    return datetime.fromtimestamp(ms / 1000.0, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def resp_parts(resp):
    if resp is None:
        return []
    if isinstance(resp, list):
        return resp
    if isinstance(resp, dict):
        rp = resp.get("response")
        return rp if isinstance(rp, list) else []
    return []

def walk():
    header_req_count = 0
    asks_out = open(OUT_ASKS, "w", encoding="utf-8")
    tools_out = open(OUT_TOOLS, "w", encoding="utf-8")
    edits_out = open(OUT_EDITS, "w", encoding="utf-8")
    reqs = []
    session_id = ""
    creation = ""
    append_events = 0
    appended_reqs = 0
    with open(SRC, "r", encoding="utf-8", errors="replace") as f:
        for line_no, line in enumerate(f):
            if line_no == 0:
                header = json.loads(line)
                session_id = header["v"].get("sessionId", "")
                creation = ts_str(header["v"].get("creationDate"))
                hdr = header["v"].get("requests", [])
                header_req_count = len(hdr)
                reqs = list(hdr)
                continue
            if len(line) < 40:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            if rec.get("kind") == 2 and rec.get("k") == ["requests"]:
                v = rec["v"]
                if isinstance(v, list):
                    append_events += 1
                    appended_reqs += len(v)
                    reqs.extend(v)

    n = len(reqs)
    tool_counts = collections.Counter()
    day_counts = collections.Counter()
    ask_total_chars = 0
    think_parts = 0
    think_chars = 0
    text_parts = 0
    text_chars = 0
    inline_refs = collections.Counter()
    compact_events = 0
    edit_targets = collections.Counter()
    edit_ops = 0
    tool_rows = 0
    tool_err_rows = 0
    ts_first = None
    ts_last = None

    for i, r in enumerate(reqs):
        ts = r.get("timestamp")
        if ts:
            if ts_first is None or ts < ts_first:
                ts_first = ts
            if ts_last is None or ts > ts_last:
                ts_last = ts
            day_counts[ts_str(ts)[:10]] += 1
        msg = r.get("message")
        text = ""
        if isinstance(msg, dict):
            text = msg.get("text") or ""
        elif isinstance(msg, str):
            text = msg
        elif isinstance(msg, list):
            text = "\n".join(p.get("text", "") for p in msg if isinstance(p, dict))
        ask_total_chars += len(text)
        asks_out.write(json.dumps({
            "n": i, "ts": ts_str(ts), "requestId": r.get("requestId"),
            "ask_chars": len(text), "ask": text[:2000],
        }, ensure_ascii=False) + "\n")

        for p in resp_parts(r.get("response")):
            if not isinstance(p, dict):
                continue
            k = p.get("kind")
            if k == "toolInvocationSerialized":
                tool_id = p.get("toolId") or "?"
                tool_counts[tool_id] += 1
                tool_rows += 1
                is_err = bool(p.get("isError")) or (p.get("isConfirmed", {}) or {}).get("type") == 0
                if p.get("isError"):
                    tool_err_rows += 1
                detail = ""
                pt = p.get("pastTenseMessage")
                if isinstance(pt, dict):
                    detail = pt.get("value", "")[:200]
                tools_out.write(json.dumps({
                    "n": i, "ts": ts_str(ts), "tool": tool_id, "detail": detail,
                }, ensure_ascii=False) + "\n")
            elif k == "thinking":
                think_parts += 1
                think_chars += len(p.get("value", "") or "")
            elif k == "textEditGroup":
                uri = (p.get("uri") or {}).get("fsPath", "?")
                groups = p.get("edits") or []
                cnt = sum(len(g) for g in groups if isinstance(g, list))
                edit_ops += cnt
                edit_targets[uri] += 1
                edits_out.write(json.dumps({
                    "n": i, "ts": ts_str(ts), "file": uri, "edit_ops": cnt,
                }, ensure_ascii=False) + "\n")
            elif k == "notebookEditGroup":
                uri = (p.get("uri") or {}).get("fsPath", "?")
                edit_targets[uri] += 1
                edits_out.write(json.dumps({
                    "n": i, "ts": ts_str(ts), "file": uri, "edit_ops": 0, "notebook": True,
                }, ensure_ascii=False) + "\n")
            elif k == "inlineReference":
                uri = (p.get("inlineReference") or {}).get("fsPath", "?")
                inline_refs[uri] += 1
            elif k == "progressTaskSerialized":
                val = (p.get("content") or {}).get("value", "")
                if "Compacted" in val:
                    compact_events += 1
            elif k is None and "value" in p:
                text_parts += 1
                text_chars += len(p.get("value", "") or "")

    asks_out.close()
    tools_out.close()
    edits_out.close()
    summary = {
        "sessionId": session_id,
        "creationDate": creation,
        "header_requests": header_req_count,
        "kind2_append_events": append_events,
        "appended_requests": appended_reqs,
        "requests_total": n,
        "ts_first": ts_str(ts_first),
        "ts_last": ts_str(ts_last),
        "ask_total_chars": ask_total_chars,
        "thinking_parts": think_parts,
        "thinking_chars": think_chars,
        "assistant_text_parts": text_parts,
        "assistant_text_chars": text_chars,
        "compaction_events": compact_events,
        "tool_rows": tool_rows,
        "tool_error_rows": tool_err_rows,
        "tool_counts": dict(tool_counts.most_common()),
        "edit_ops_total": edit_ops,
        "edit_target_groups": sum(edit_targets.values()),
        "edited_files_distinct": len(edit_targets),
        "edited_files_top": dict(edit_targets.most_common(50)),
        "inline_ref_distinct": len(inline_refs),
        "inline_refs_top": dict(inline_refs.most_common(30)),
        "by_day": dict(sorted(day_counts.items())),
    }
    with open(OUT_SUM, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=1)
    print(json.dumps({k: summary[k] for k in (
        "sessionId", "creationDate", "header_requests", "kind2_append_events",
        "appended_requests", "requests_total", "ts_first", "ts_last",
        "ask_total_chars", "thinking_parts", "thinking_chars",
        "assistant_text_parts", "assistant_text_chars", "compaction_events",
        "tool_rows", "tool_error_rows", "edit_ops_total", "edited_files_distinct",
        "inline_ref_distinct")}, indent=1))
    print("tools:", json.dumps(summary["tool_counts"], indent=1))
    print("by_day:", summary["by_day"])
    print("edited files top 15:", json.dumps(dict(list(summary["edited_files_top"].items())[:15]), indent=1))

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    walk()
