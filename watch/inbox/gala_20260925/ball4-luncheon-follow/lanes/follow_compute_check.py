# gala-follow-compute finish-line byte check.
import json, sys
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
REG = ROOT / "watch/inbox/luncheon_watchlist_20260929_signals.jsonl"
RECEIPT = ROOT / "watch/inbox/ball4/compute.md"
W = "gala-follow-compute"
TARGETS = ["lunch-jensen-huang", "lunch-lisa-su", "lunch-hock-tan", "lunch-sanjay-mehrotra", "lunch-elon-musk"]
fails = []

lines = [l for l in REG.read_text(encoding="utf-8").splitlines() if l.strip()]
rows = [json.loads(l) for l in lines]
mine = [r for r in rows if r.get("writer") == W]

print(f"register: {len(lines)} lines total, {len(mine)} rows by writer={W}")
seen = {}
for r in mine:
    wid = r.get("watch_id")
    seen[wid] = seen.get(wid, 0) + 1
    for field in ("ts", "watch_id", "name", "org", "lane", "window", "in_window", "date_honesty_note", "estate_angle", "handle_check", "sources"):
        if not r.get(field):
            fails.append(f"{wid}: missing/empty {field}")
    iw = r.get("in_window") or []
    if not isinstance(iw, list) or not iw:
        fails.append(f"{wid}: in_window empty")
        continue
    for i, item in enumerate(iw):
        for f2 in ("signal", "date", "source"):
            if not item.get(f2):
                fails.append(f"{wid}: in_window[{i}] missing {f2}")
    ea = (r.get("estate_angle") or "").lower()
    if "vram" not in ea or "local" not in ea:
        fails.append(f"{wid}: estate_angle lacks vram/local-economics language")
    if not any("2026" in (item.get("date") or "") for item in iw):
        fails.append(f"{wid}: no dated 2026 in-window item")

for t in TARGETS:
    if seen.get(t, 0) != 1:
        fails.append(f"target {t}: {seen.get(t,0)} rows (expected exactly 1)")

print("targets covered:", {t: seen.get(t, 0) for t in TARGETS})
print(f"receipt: {RECEIPT} exists={RECEIPT.exists()} bytes={RECEIPT.stat().st_size if RECEIPT.exists() else 0}")
if not RECEIPT.exists() or RECEIPT.stat().st_size == 0:
    fails.append("receipt missing or empty")

if fails:
    print("FAIL")
    for f3 in fails:
        print(" -", f3)
    sys.exit(1)
print("PASS: 5 compute register rows (1/target), dated in-window signals with sources, estate_angle names VRAM ladder + local economics, receipt on disk")
