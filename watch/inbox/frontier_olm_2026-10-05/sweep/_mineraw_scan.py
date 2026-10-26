"""RQ5 staleness scan for mine/raw scraped rows (sweep-open-local-language-models-arxiv, 2026-10-05)."""
import os, json, datetime

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent\mine\raw"
per_dir = {}
total_rows = 0
newest_mtime = None
newest_file = None
oldest_mtime = None
date_min = None
date_max = None
date_key_hits = 0
sample = {}

for dirpath, dirnames, filenames in os.walk(ROOT):
    for fn in filenames:
        p = os.path.join(dirpath, fn)
        rel = os.path.relpath(p, ROOT)
        sub = rel.split(os.sep)[0]
        st = os.stat(p)
        per_dir.setdefault(sub, [0, 0])
        per_dir[sub][0] += 1
        per_dir[sub][1] += st.st_size
        if newest_mtime is None or st.st_mtime > newest_mtime:
            newest_mtime, newest_file = st.st_mtime, rel
        if oldest_mtime is None or st.st_mtime < oldest_mtime:
            oldest_mtime = st.st_mtime
        rows = 0
        try:
            with open(p, "r", encoding="utf-8", errors="replace") as f:
                head = None
                for i, line in enumerate(f):
                    line = line.strip()
                    if not line:
                        continue
                    rows += 1
                    if head is None:
                        head = line[:400]
                    if date_key_hits < 200000:
                        try:
                            obj = json.loads(line)
                            for k in ("created_utc", "date", "scraped_at", "timestamp", "created", "fetched_at", "published"):
                                if k in obj:
                                    v = obj[k]
                                    if isinstance(v, (int, float)) and 1500000000 < v < 2000000000:
                                        d = datetime.datetime.utcfromtimestamp(v).date().isoformat()
                                        date_min = d if date_min is None or d < date_min else date_min
                                        date_max = d if date_max is None or d > date_max else date_max
                                        date_key_hits += 1
                                    elif isinstance(v, str) and len(v) >= 10 and v[:4] in ("2024", "2025", "2026"):
                                        d = v[:10]
                                        date_min = d if date_min is None or d < date_min else date_min
                                        date_max = d if date_max is None or d > date_max else date_max
                                        date_key_hits += 1
                        except Exception:
                            pass
        except Exception as e:
            head = f"ERROR: {e}"
        total_rows += rows
        if sub not in sample:
            sample[sub] = (rel, rows, head)

print("per_dir (name: files, bytes):")
for k, (c, b) in sorted(per_dir.items()):
    print(f"  {k}: {c} files, {b:,} bytes")
print(f"total rows: {total_rows:,}")
print(f"newest file mtime: {datetime.datetime.utcfromtimestamp(newest_mtime).isoformat()}Z ({newest_file})")
print(f"oldest file mtime: {datetime.datetime.utcfromtimestamp(oldest_mtime).isoformat()}Z")
print(f"date-bearing lines scanned: {date_key_hits:,}; row date range: {date_min} .. {date_max}")
for k, (rel, rows, head) in sample.items():
    print(f"SAMPLE {k}: {rel} rows={rows}")
    print(f"  head: {head[:300]}")
