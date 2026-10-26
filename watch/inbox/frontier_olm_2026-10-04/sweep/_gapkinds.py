import json, collections, re

pat = re.compile(r"GRPO|RLVR|verifiable reward|unsloth|axolotl|QLoRA", re.I)
paths = collections.defaultdict(collections.Counter)
with open("catalog/catalog.jsonl", encoding="utf-8", errors="replace") as f:
    for line in f:
        m = pat.search(line)
        if not m:
            continue
        try:
            j = json.loads(line)
        except Exception:
            j = {}
        p = j.get("path", "?")
        key = m.group(0).lower()
        # bucket by top 3 path segments
        parts = p.replace("\\", "/").split("/")
        bucket = "/".join(parts[:4])
        paths[key][bucket] += 1

for key in sorted(paths):
    print(f"== {key} ==")
    for bucket, n in paths[key].most_common(6):
        print(f"   {bucket}: {n}")
