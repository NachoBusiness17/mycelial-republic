import json, os, collections

OUT = os.path.dirname(os.path.abspath(__file__))

asks = [json.loads(l) for l in open(os.path.join(OUT, "codex_lane_asks.jsonl"), encoding="utf-8")]
turns = [json.loads(l) for l in open(os.path.join(OUT, "codex_lane_turns.jsonl"), encoding="utf-8")]
patches = [json.loads(l) for l in open(os.path.join(OUT, "codex_lane_patches.jsonl"), encoding="utf-8")]
summary = json.load(open(os.path.join(OUT, "codex_lane_summary.json"), encoding="utf-8"))

# titan bank reuse
TITAN_DIR = os.path.join(OUT, "..", "..", "..", "watch", "inbox", "mates_leave_protocol",
                         "receipts", "cartographer_20261011_data")
titan_asks = []
titan_summary = {}
try:
    titan_asks = [json.loads(l) for l in open(os.path.join(TITAN_DIR, "titan_asks.jsonl"), encoding="utf-8")]
    titan_summary = json.load(open(os.path.join(TITAN_DIR, "titan_summary.json"), encoding="utf-8"))
except Exception as e:
    titan_note = f"titan bank read failed: {e}"
else:
    titan_note = f"titan bank: {len(titan_asks)} asks"

# dedupe by id (3 double-named ids), keep first label per id
seen_id = {}
order = []
for s in summary:
    if s["status"] not in ("walked", "titan_reused_20261011_bank"):
        continue
    if s["id"] in seen_id:
        continue
    seen_id[s["id"]] = s
    order.append(s["id"])

asks_by = collections.defaultdict(list)
for a in asks:
    asks_by[a["id"]].append(a)
turns_by = collections.defaultdict(list)
for t in turns:
    turns_by[t["id"]].append(t)
patch_by = collections.defaultdict(list)
for p in patches:
    patch_by[p["id"]].append(p)

view = open(os.path.join(OUT, "codex_fold_view.txt"), "w", encoding="utf-8")
for rid in order:
    s = seen_id[rid]
    view.write(f"\n{'='*100}\nTHREAD {rid} | {s['label']} | {s['status']} | asks={s.get('asks')} patches={s.get('patch_calls')} | {s.get('first_ts')} .. {s.get('last_ts')}\n")
    if rid not in asks_by and s["status"].startswith("titan"):
        view.write(f"[titan: decision arc banked cycle 20261011, {titan_note}; see titan_asks.jsonl]\n")
        continue
    for a in asks_by[rid]:
        txt = a["text"].replace("\r", "")
        view.write(f"\n--- ASK {a['ask_no']} (line {a['line_no']}, {a['ts']})\n{txt[:3000]}\n")
    pt = collections.Counter(p["target"] for p in patch_by[rid])
    if pt:
        view.write("\nPATCH TARGETS: " + ", ".join(f"{k}({v})" for k, v in pt.most_common(30)) + "\n")
    lt = turns_by[rid]
    for t in lt[-6:]:
        txt = t["text"].replace("\r", "")
        view.write(f"\n>>> TURN {t['turn_no']} (line {t['line_no']}, {'L' if t['lawful'] else '-'})\n{txt[:1200]}\n")
view.close()
print(json.dumps({"threads_in_view": len(order),
                  "view_bytes": os.path.getsize(os.path.join(OUT, "codex_fold_view.txt")),
                  "titan_note": titan_note}))
