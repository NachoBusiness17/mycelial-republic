import json, sys

REG = r"C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/luncheon_watchlist_20260929_signals.jsonl"
MY_TARGETS = ["lunch-greg-brockman","lunch-tom-brown","lunch-dario-amodei","lunch-mark-zuckerberg","lunch-sundar-pichai","org-openai","org-anthropic","org-meta","org-google"]

lines = open(REG, encoding="utf-8").read().splitlines()
print(f"register total lines: {len(lines)}")
fails = []
seen = {}
for i, ln in enumerate(lines, 1):
    if not ln.strip():
        fails.append(f"line {i}: EMPTY LINE")
        continue
    try:
        row = json.loads(ln)
    except Exception as e:
        fails.append(f"line {i}: NOT VALID JSON: {e}")
        continue
    wid = row.get("watch_id","?")
    if wid in MY_TARGETS:
        seen[wid] = seen.get(wid, 0) + 1
        if not row.get("estate_angle"):
            fails.append(f"line {i} ({wid}): MISSING estate_angle")
        items = row.get("in_window") or []
        if not items:
            fails.append(f"line {i} ({wid}): EMPTY in_window")
        for j, it in enumerate(items, 1):
            g = it.get("grade","")
            if g not in ("search","fetch") and not str(g).startswith(("search","fetch")):
                fails.append(f"line {i} ({wid}) item {j}: BAD GRADE {g!r}")
            if not it.get("signal"):
                fails.append(f"line {i} ({wid}) item {j}: MISSING signal")
            if not it.get("date"):
                fails.append(f"line {i} ({wid}) item {j}: MISSING date")
            if not it.get("source"):
                fails.append(f"line {i} ({wid}) item {j}: MISSING source")
missing = [t for t in MY_TARGETS if t not in seen]
dupes = {t: c for t, c in seen.items() if c > 1}
if missing: fails.append(f"MISSING TARGET ROWS: {missing}")
if dupes: fails.append(f"DUPLICATE TARGET ROWS: {dupes}")
print(f"my target rows found: {len(seen)}/9, counts: {seen}")
print(f"other-lane rows in register: {len(lines) - sum(seen.values())}")
if fails:
    print("FAIL")
    for f_ in fails: print(" -", f_)
    sys.exit(1)
print("PASS: 9/9 targets present exactly once; every in_window item carries grade in {search,fetch} + signal + date + source; every target row carries estate_angle; every register line parses as JSON")
