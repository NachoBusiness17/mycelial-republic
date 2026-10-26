"""w4-16 instrument: modality census over catalog/catalog.jsonl (read-only)."""
import json, os, sys
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
CAT = os.path.join(REPO, "catalog", "catalog.jsonl")

IMG = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg", ".ico",
       ".tif", ".tiff"}
AUD = {".mp3", ".wav", ".m4a", ".flac", ".ogg", ".opus", ".aac", ".wma",
       ".mid", ".midi"}
VID = {".mp4", ".mov", ".webm", ".mkv", ".avi", ".gifv"}
TEXT = {".md", ".txt", ".rst", ".html", ".htm", ".json", ".jsonl", ".py",
        ".js", ".ts", ".yaml", ".yml", ".toml", ".csv"}

kinds = Counter()
img_zones = Counter()
img_owners = Counter()
aud_rows, vid_rows = [], []
img_bytes = 0
total_bytes = 0
ext_top = Counter()
oracle_rows = 0
sample_titles = []

with open(CAT, encoding="utf-8") as fh:
    for line in fh:
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        path = str(row.get("path", ""))
        ext = (row.get("ext") or "").lower()
        b = row.get("bytes") or 0
        total_bytes += b
        ext_top[ext] += 1
        kinds[row.get("kind", "?")] += 1
        if row.get("oracle"):
            oracle_rows += 1
        if ext in IMG:
            img_zones[row.get("zone", "?")] += 1
            img_owners[str(path).replace("\\", "/").split("/")[0]] += 1
            img_bytes += b
            if len(sample_titles) < 8:
                sample_titles.append(path[:110])
        elif ext in AUD:
            aud_rows.append((path[:110], b))
        elif ext in VID:
            vid_rows.append((path[:110], b))

out = {
    "rows_total": sum(kinds.values()),
    "kinds": dict(kinds.most_common()),
    "image_rows": sum(img_zones.values()),
    "image_bytes": img_bytes,
    "image_by_zone": dict(img_zones.most_common(10)),
    "image_by_owner_top": dict(img_owners.most_common(10)),
    "audio_rows": aud_rows[:15],
    "audio_count": len(aud_rows),
    "video_rows": vid_rows[:15],
    "video_count": len(vid_rows),
    "ext_top20": dict(ext_top.most_common(20)),
    "total_bytes_gb": round(total_bytes / 1e9, 2),
    "oracle_rows": oracle_rows,
    "image_title_samples": sample_titles,
}
print(json.dumps(out, indent=1, ensure_ascii=False))
