from pathlib import Path
t = Path("/app/dashboard/rest.py").read_text(encoding="utf-8")
i = t.find("def h_table_view")
print("CONTAINER h_table_view:")
print(t[i:i+900])
print("---ENV---")
import os
for k,v in os.environ.items():
    if "DF" in k or "TILE" in k:
        print(k, v)
