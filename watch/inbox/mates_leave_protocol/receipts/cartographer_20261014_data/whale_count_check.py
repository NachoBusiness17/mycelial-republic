import io
import json

n_whales = n_empty = n_hit = 0
samples = []
for line in io.open("logs/mates/cartographer/grok_lane_decisions.jsonl", encoding="utf-8"):
    if "whales" not in line:
        continue
    r = json.loads(line)
    last = r.get("last_text") or ""
    if "whales" in last:
        n_whales += 1
        s = last.strip()
        if s.startswith("{"):
            head = s[:30]
            if '"whales":[]' in head or '"whales": []' in head:
                n_empty += 1
            else:
                n_hit += 1
        if len(samples) < 3:
            samples.append(s[:70])

print("chats with whales in last_text:", n_whales, "empty:", n_empty, "hit:", n_hit)
for s in samples:
    print(repr(s))
