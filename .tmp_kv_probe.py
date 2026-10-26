import json, urllib.request, urllib.parse, sys, io, time, socket, ipaddress
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Mimosa SSRF guard: https-only, fixed allowlist host, resolve + block private/loopback/link-local
ALLOWED_HOST = "arctic-shift.photon-reddit.com"  # public Reddit archive API, only host this tool may touch
_addrs = {ai[4][0] for ai in socket.getaddrinfo(ALLOWED_HOST, 443, proto=socket.IPPROTO_TCP)}
for a in _addrs:
    ip = ipaddress.ip_address(a)
    assert not (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved), f"blocked {a}"
print("host resolved OK:", ALLOWED_HOST, "->", len(_addrs), "public addrs", flush=True)
BASE = "https://" + ALLOWED_HOST + "/api"

def get(path, params, timeout=40):
    assert path.startswith("/posts") or path.startswith("/comments")
    qs = urllib.parse.urlencode(params)
    url = "https://" + ALLOWED_HOST + "/api" + path + "?" + qs  # host is the allowlisted constant above
    req = urllib.request.Request(url, headers={"User-Agent": "estate-frontier-sweep/1.0"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            d = json.load(r)
        n = len(d.get("data", [])) if isinstance(d, dict) else -1
        print(f"OK {path} {params} -> {n} rows in {time.time()-t0:.1f}s", flush=True)
        return d
    except Exception as e:
        print(f"FAIL {path} {params} -> {e} ({time.time()-t0:.1f}s)", flush=True)
        return None

# probe param shapes (minimal calls, polite 3s gaps)
get("/posts/search", {"subreddit": "LocalLLaMA", "after": "2026-10-01", "limit": 5}); time.sleep(3)
get("/posts/search", {"subreddit": "LocalLLaMA", "after": 1788566400, "limit": 5}); time.sleep(3)
get("/posts/search", {"subreddit": "LocalLLaMA", "after": "2026-10-01", "limit": 5, "sort": "desc"}); time.sleep(3)
get("/posts/search", {"subreddit": "LocalLLaMA", "after": "2026-10-01", "limit": 5, "sort": "desc", "sort_type": "score"}); time.sleep(3)
get("/comments/search", {"link_id": "1wkdu98", "limit": 10})
