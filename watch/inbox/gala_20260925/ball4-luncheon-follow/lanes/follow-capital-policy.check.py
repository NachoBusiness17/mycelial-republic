import json, io, os, sys
from collections import Counter

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
reg = os.path.join(ROOT, "watch", "inbox", "luncheon_watchlist_20260929_signals.jsonl")
rec = os.path.join(ROOT, "watch", "inbox", "ball4", "capital-policy.md")
lane = os.path.join(ROOT, "watch", "inbox", "gala_20260925", "ball4-luncheon-follow", "lanes", "follow-capital-policy.json")

targets = [
    "lunch-scott-kupor", "lunch-brad-gerstner", "lunch-chamath-palihapitiya",
    "lunch-david-sacks", "lunch-secretary-lutnick", "lunch-scott-bessent",
    "lunch-andrew-ferguson", "lunch-michael-kratsios", "lunch-vpotus",
    "lunch-speaker-johnson", "lunch-director-clayton", "lunch-susie-wiles",
    "lunch-will-scharf", "lunch-sean-cairncross",
]
MINE = "gala-ball4-follow-capital-policy"
results = []
fails = []

def check(name, ok, detail):
    results.append((name, ok, detail))
    if not ok:
        fails.append(name)

rows, bad = [], []
with io.open(reg, encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except Exception as e:
            bad.append((i, str(e)))

check("register_json_valid", not bad, "bad lines: %r" % bad)
c = Counter(r.get("watch_id", "?") for r in rows)
mine = [r for r in rows if r.get("writer") == MINE]
mc = Counter(r.get("watch_id") for r in mine)
missing = [t for t in targets if mc.get(t, 0) == 0]
check("register_one_row_per_target", not missing,
      "%d/%d lane rows present, writer=%s, missing=%r" % (len(targets) - len(missing), len(targets), MINE, missing))

rec_bytes = b""
if os.path.isfile(rec):
    with open(rec, "rb") as f:
        rec_bytes = f.read()
check("receipt_exists", len(rec_bytes) > 0, "path=%s" % rec)
rec_text = rec_bytes.decode("utf-8", errors="replace")
for needle in ["Is-Informed", "2026-06-12", "2026-09-21", "2026-09-24", "open-weight", "export-control", "AI-czar"]:
    check("receipt_names_%s" % needle.replace(" ", "_"), needle in rec_text, "needle=%r" % needle)

em_reg = [i for i, r in enumerate(rows, 1) if chr(0x2014) in json.dumps(r, ensure_ascii=False)]
em_rec = chr(0x2014) in rec_text
check("no_em_dash_register", not em_reg, "rows with em-dash: %r" % em_reg)
check("no_em_dash_receipt", not em_rec, "receipt contains U+2014: %r" % em_rec)

check("lane_json_exists", os.path.isfile(lane), "path=%s" % lane)

print("=== finish-line check: gala-ball4-follow-capital-policy ===")
print("register:", reg)
print("register total rows:", len(rows), "lane rows:", len(mine), "lane targets covered:", len(targets) - len(missing), "/", len(targets))
print("receipt:", rec, "bytes:", len(rec_bytes))
for name, ok, detail in results:
    print("%s %s :: %s" % ("PASS" if ok else "FAIL", name, detail))
print("OVERALL:", "PASS" if not fails else "FAIL (%s)" % ", ".join(fails))
sys.exit(0 if not fails else 1)
