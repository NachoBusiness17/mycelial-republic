from pathlib import Path
import json, time
from dashboard.rest import dispatch

t0 = time.time()
hit = dispatch("GET", "/api/v1/table/view", None, {})
print("dispatch", time.time()-t0, "status", hit[0])
body = hit[1]
print("keys", list(body)[:30])
# size of dumps
t0 = time.time()
s = json.dumps(body, indent=2, default=str)
print("dumps", time.time()-t0, "len", len(s))

# which route matched — inspect _COMPILED
import dashboard.rest as rest
print("compiled", len(getattr(rest, "_COMPILED", [])))
for m, cre, names, fn in rest._COMPILED:
    if m != "GET":
        continue
    if cre.match("/api/v1/table/view"):
        print("MATCH", cre.pattern, fn.__name__, names)
