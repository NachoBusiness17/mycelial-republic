import json
import io

rows = []
with io.open(r"memory/corpus/quantized_thought/instructions_flash.jsonl", encoding="utf-8") as fh:
    for line in fh:
        line = line.strip()
        if line:
            rows.append(json.loads(line))

print("rows:", len(rows))
for r in rows:
    rid = r.get("id", "?")
    flash = r.get("flash", "") or ""
    frontier = r.get("frontier", "") or ""
    print(rid,
          "flash_len:", len(flash),
          "frontier_len:", len(frontier),
          "MEASURED_ON_at:", frontier.find("MEASURED ON"),
          "git_diff_in_flash:", ("Verify with git diff" in flash),
          "deliberate_in_flash:", ("Elevate with a deliberate ask" in flash),
          "git_diff_in_frontier:", ("Verify with git diff" in frontier),
          "deliberate_in_frontier:", ("Elevate with a deliberate ask" in frontier))
