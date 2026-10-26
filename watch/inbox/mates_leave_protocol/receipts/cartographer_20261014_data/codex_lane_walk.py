import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
POOL = os.path.join(ROOT, "corpus", "oral_history", "seat_pools", "codex_sessions")
IDX = os.path.join(ROOT, "corpus", "oral_history", "seat_pools", "session_index.jsonl")
OUT = os.path.dirname(os.path.abspath(__file__))
TITAN = "01a052ca"

PREAMBLE_RE = re.compile(r"^\s*<")
ASK_MAX = 4000
TURN_MAX = 1500
LAW_RE = re.compile(r"\b(never|always|law\b|debt\b|sacred|rule\b|decision\b|verdict\b|do not|don't)\b", re.I)
PATCH_RE = re.compile(r"\*\*\* (Update|Add|Delete) File: ([^\n\\]+)")

rollouts = []
for dirpath, _dirs, files in os.walk(POOL):
    for fn in files:
        if fn.endswith(".jsonl"):
            rollouts.append(os.path.join(dirpath, fn))

rows = [json.loads(l) for l in open(IDX, encoding="utf-8") if l.strip()]
asks_f = open(os.path.join(OUT, "codex_lane_asks.jsonl"), "w", encoding="utf-8")
turns_f = open(os.path.join(OUT, "codex_lane_turns.jsonl"), "w", encoding="utf-8")
patch_f = open(os.path.join(OUT, "codex_lane_patches.jsonl"), "w", encoding="utf-8")
summary = []

def emit(f, obj):
    f.write(json.dumps(obj, ensure_ascii=False) + "\n")

for r in rows:
    rid, label = r["id"], r["thread_name"]
    match = [fn for fn in rollouts if rid in fn]
    if not match:
        summary.append({"id": rid, "label": label, "status": "no_codex_file"})
        continue
    path = os.path.join(POOL, match[0])
    if TITAN in match[0]:
        summary.append({"id": rid, "label": label, "status": "titan_reused_20261011_bank",
                        "file": match[0], "bytes": os.path.getsize(path)})
        continue
    asks, turns, patches = [], [], []
    n_lines = n_user = n_asst = n_patch = 0
    first_ts = last_ts = None
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line_no, line in enumerate(fh, 1):
            n_lines += 1
            if len(line) > 3_000_000:
                continue
            m = re.search(r'"timestamp":"([^"]+)"', line)
            if m:
                last_ts = m.group(1)
                if first_ts is None:
                    first_ts = m.group(1)
            if '"role":"user"' in line and '"input_text"' in line:
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                p = obj.get("payload", {})
                texts = [c.get("text", "") for c in p.get("content", []) if isinstance(c, dict)]
                text = "\n".join(t for t in texts if t)
                n_user += 1
                if PREAMBLE_RE.match(text):
                    continue
                asks.append({"id": rid, "label": label, "ask_no": len(asks) + 1,
                             "line_no": line_no, "ts": obj.get("timestamp"),
                             "text": text[:ASK_MAX]})
            elif '"role":"assistant"' in line and '"output_text"' in line:
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                p = obj.get("payload", {})
                texts = [c.get("text", "") for c in p.get("content", []) if isinstance(c, dict)]
                text = "\n".join(t for t in texts if t)
                n_asst += 1
                if not text.strip():
                    continue
                turns.append({"id": rid, "turn_no": len(turns) + 1, "line_no": line_no,
                              "ts": obj.get("timestamp"), "lawful": bool(LAW_RE.search(text)),
                              "text": text[:TURN_MAX]})
            elif '"custom_tool_call"' in line and "apply_patch" in line:
                for kind, target in PATCH_RE.findall(line):
                    patches.append({"id": rid, "line_no": line_no, "kind": kind,
                                    "target": target.strip()})
                    n_patch += 1
    for a in asks:
        emit(asks_f, a)
    keep = [t for t in turns if t["lawful"]][-12:] + turns[-8:]
    seen, kept = set(), []
    for t in keep:
        key = t["line_no"]
        if key in seen:
            continue
        seen.add(key)
        kept.append(t)
    for t in sorted(kept, key=lambda x: x["line_no"]):
        emit(turns_f, t)
    for p in patches:
        emit(patch_f, p)
    targets = {}
    for p in patches:
        targets[p["target"]] = targets.get(p["target"], 0) + 1
    summary.append({"id": rid, "label": label, "status": "walked", "file": match[0],
                    "bytes": os.path.getsize(path), "lines": n_lines,
                    "user_rows": n_user, "asst_rows": n_asst, "asks": len(asks),
                    "turns": len(turns), "patch_calls": n_patch,
                    "patch_targets": len(targets), "first_ts": first_ts, "last_ts": last_ts})

asks_f.close()
turns_f.close()
patch_f.close()
with open(os.path.join(OUT, "codex_lane_summary.json"), "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=1)
walked = [s for s in summary if s["status"] == "walked"]
print(json.dumps({"rows": len(rows), "walked": len(walked),
                  "titan": len([s for s in summary if s["status"].startswith("titan")]),
                  "no_file": len([s for s in summary if s["status"] == "no_codex_file"]),
                  "total_asks": sum(s["asks"] for s in walked),
                  "total_patch_calls": sum(s["patch_calls"] for s in walked)}))
