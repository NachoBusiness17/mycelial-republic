import json, urllib.request, urllib.parse, sys, io, time, socket, ipaddress, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Mimosa SSRF guard: https-only, fixed allowlist host, resolve + block private/loopback/link-local
ALLOWED_HOST = "arctic-shift.photon-reddit.com"
_addrs = {ai[4][0] for ai in socket.getaddrinfo(ALLOWED_HOST, 443, proto=socket.IPPROTO_TCP)}
for a in _addrs:
    ip = ipaddress.ip_address(a)
    assert not (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved), f"blocked {a}"

OUT = ".tmp_kv_deep"
os.makedirs(OUT, exist_ok=True)
IDS = ["1wd4xxv", "1whx5xi", "1weolwq", "1wbgqnp", "1wn6vwm", "1wlss89", "1wdaq1v", "1wtg12r", "1wiu7xj"]

def get(path, params, timeout=60):
    assert path.startswith("/posts") or path.startswith("/comments")
    url = "https://" + ALLOWED_HOST + "/api" + path + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "estate-frontier-sweep/1.0"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.load(r)
        except Exception as e:
            print(f"  attempt {attempt} FAIL {path} {params} -> {e}", flush=True)
            time.sleep(10 * (attempt + 1))
    return None

# batch submissions
d = get("/posts/ids", {"ids": ",".join(IDS)}) or {}
rows = d.get("data", [])
print("submissions fetched:", len(rows), flush=True)
for s in rows:
    with open(f"{OUT}/sub_{s['id']}.json", "w", encoding="utf-8") as f:
        json.dump(s, f, indent=1)

# comments per id
for sid in IDS:
    d = get("/comments/search", {"link_id": sid, "limit": 100})
    rows = d.get("data", []) if d else []
    with open(f"{OUT}/com_{sid}.json", "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=1)
    print(f"comments {sid}: {len(rows)}", flush=True)
    time.sleep(3)
print("DEEP FETCH DONE", flush=True)
