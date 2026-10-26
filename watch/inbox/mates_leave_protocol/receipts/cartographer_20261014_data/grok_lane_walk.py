import json, os, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
POOL = os.path.join(ROOT, "corpus", "oral_history", "seat_pools", "grok_sessions")
SURVEY = os.path.join(ROOT, "watch", "inbox", "mates_leave_protocol", "receipts",
                      "cartographer_20261010_data", "grok_survey.jsonl")
OUT = os.path.dirname(os.path.abspath(__file__))

PREAMBLE_RE = re.compile(r"^\s*<")
UQ_RE = re.compile(r"<user_query>(.*?)</user_query>", re.S)
LAW_RE = re.compile(r"\b(never|always|law\b|debt\b|sacred|rule\b|decision\b|verdict\b|do not|don't)\b", re.I)
ASK_MAX = 1200
MAX_ASKS = 20
TURN_MAX = 1000
LAW_LINES_MAX = 8

rows = [json.loads(l) for l in open(SURVEY, encoding="utf-8") if l.strip()]
lanes = collections.defaultdict(list)
for r in rows:
    lanes[r["lane"]].append(r)

out_f = open(os.path.join(OUT, "grok_lane_decisions.jsonl"), "w", encoding="utf-8")
view = open(os.path.join(OUT, "grok_fold_view.txt"), "w", encoding="utf-8")
stats = {"chats_read": 0, "chats_missing": 0, "asks": 0, "law_lines": 0, "lanes": 0}

def user_texts(payload):
    if isinstance(payload, str):
        return [payload]
    if isinstance(payload, list):
        return [c.get("text", "") for c in payload if isinstance(c, dict) and c.get("type") == "text"]
    return []

for lane in sorted(lanes):
    stats["lanes"] += 1
    view.write(f"\n{'='*100}\nLANE {lane} | {len(lanes[lane])} unique chats\n")
    for row in sorted(lanes[lane], key=lambda x: x.get("created_at") or ""):
        path = os.path.join(POOL, row["lane"], row["dir"], "chat_history.jsonl")
        if not os.path.exists(path):
            stats["chats_missing"] += 1
            continue
        stats["chats_read"] += 1
        asks, turns, law_lines = [], [], []
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line_no, line in enumerate(fh, 1):
                if len(line) > 2_000_000:
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                t = obj.get("type")
                if t == "user":
                    for text in user_texts(obj.get("content")):
                        if not text or PREAMBLE_RE.match(text):
                            continue
                        m = UQ_RE.search(text)
                        if m:
                            text = m.group(1)
                        text = text.strip()
                        if not text or PREAMBLE_RE.match(text):
                            continue
                        if len(asks) < MAX_ASKS:
                            asks.append({"line_no": line_no, "text": text[:ASK_MAX]})
                            stats["asks"] += 1
                elif t == "assistant":
                    text = obj.get("content")
                    if not isinstance(text, str) or not text.strip():
                        continue
                    turns.append({"line_no": line_no, "text": text[:TURN_MAX]})
                    for ln in text.splitlines():
                        if LAW_RE.search(ln) and len(law_lines) < LAW_LINES_MAX:
                            law_lines.append({"line_no": line_no, "text": ln.strip()[:400]})
                            stats["law_lines"] += 1
        rec = {"lane": lane, "dir": row["dir"], "title": row.get("title"),
               "agent": row.get("agent_name"), "model": row.get("model"),
               "created": row.get("created_at"), "num_messages": row.get("num_messages"),
               "asks": asks, "last_turns": turns[-3:], "law_lines": law_lines}
        out_f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        view.write(f"\nCHAT {row['dir'][:8]} | {row.get('title')} | {row.get('agent_name')} | {row.get('created_at','')[:19]} | msgs={row.get('num_messages')}\n")
        for a in asks:
            view.write(f"  ASK(l{a['line_no']}): {a['text'][:400]}\n".replace("\n", " ") + "\n")
        if law_lines:
            view.write("  LAW LINES:\n")
            for ll in law_lines:
                view.write(f"    L(l{ll['line_no']}): {ll['text'][:300]}\n")
        if turns:
            view.write(f"  LAST: {turns[-1]['text'][:400]}\n".replace("\n", " ") + "\n")

out_f.close()
view.close()
stats["view_bytes"] = os.path.getsize(os.path.join(OUT, "grok_fold_view.txt"))
print(json.dumps(stats))
