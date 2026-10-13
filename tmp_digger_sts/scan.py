import json, sys, re

path = sys.argv[1]
keywords = [k.lower() for k in sys.argv[2:]]
with open(path, encoding="utf-8") as f:
    data = json.load(f)
text = data["parse"]["wikitext"]["*"]
lines = text.split("\n")
for i, line in enumerate(lines):
    low = line.lower()
    if any(k in low for k in keywords):
        print(f"{i}: {line}")
