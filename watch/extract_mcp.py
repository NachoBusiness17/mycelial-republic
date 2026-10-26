import re

txt = open("watch/MCP_AWESOME_DIGEST.md", encoding="utf-8", errors="ignore").read()
# Category headers: lines like "### 🔎 <something>" or "## ..." sections
cats = re.findall(r"^###\s+(.+)$", txt, re.M)
# Server entries: "- [name](url) - description" bullets
entries = re.findall(r"^- \[([^\]]+)\]\((https?://[^)]+)\)", txt, re.M)
stars = re.findall(r"-\s*\[([^\]]+)\]\([^)]+\)([^!\n]*?)(!\[[^\]]*\]\([^)]*\))?\s*-\s*(.{0,90})", txt)

print("categories:", len(cats))
print("server entries:", len(entries))
print()
print("TOP CATEGORY HEADERS:")
for c in cats[:60]:
    c2 = re.sub(r"[*`]", "", c).strip()
    if c2 and not c2.startswith("!"):
        print(" -", c2[:80])
