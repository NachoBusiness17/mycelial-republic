import json, time, urllib.request, urllib.parse, sys, os

IDS = sys.argv[1].split(",")
OUTDIR = ".tmp_sweep_deep"
os.makedirs(OUTDIR, exist_ok=True)

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "research-sweep/1.0 (estate frontier sweep)"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.load(r)
        except Exception as e:
            print(f"  attempt {attempt} error {e}", flush=True)
            time.sleep(20 * (attempt + 1))
    return None

# batch fetch submissions
subs = {}
for i in range(0, len(IDS), 5):
    batch = IDS[i:i+5]
    d = fetch("https://api.pullpush.io/reddit/search/submission/?ids=" + ",".join(batch) + "&size=10")
    time.sleep(12)
    if d:
        for s in d.get("data", []):
            subs[s["id"]] = s
    print(f"submissions batch {batch}: got {len(d.get('data', [])) if d else 0}", flush=True)

for sid, s in subs.items():
    with open(f"{OUTDIR}/sub_{sid}.json", "w", encoding="utf-8") as f:
        json.dump(s, f, indent=1)

# fetch comments per id
for sid in IDS:
    d = fetch(f"https://api.pullpush.io/reddit/search/comment/?link_id={sid}&size=100&sort=asc")
    time.sleep(12)
    rows = d.get("data", []) if d else []
    with open(f"{OUTDIR}/com_{sid}.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=1)
    print(f"comments {sid}: {len(rows)}", flush=True)

print("DONE", flush=True)
