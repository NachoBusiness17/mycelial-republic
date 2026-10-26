import sys, os, hashlib
list_path = sys.argv[1]
key = sys.stdin.readline().rstrip("\r\n").strip()
if len(key) < 16:
    print("NOKEY len=%d" % len(key), flush=True)
    raise SystemExit(2)
pats = [key.encode(), key[:-8].encode(), hashlib.sha256(key.encode()).hexdigest().encode()]
del key
def hits(b):
    return [b.count(p) for p in pats]
n=0; hitn=0
with open(list_path, encoding="utf-8", errors="replace") as lf:
    for path in lf:
        path=path.strip()
        if not path: continue
        try:
            if os.path.getsize(path) > 200_000_000: continue
            with open(path,"rb") as f: b=f.read()
        except Exception:
            continue
        n+=1
        c=hits(b)
        if any(c):
            hitn+=1
            print("HIT", path, "full=%d noLast8=%d sha=%d"%tuple(c), flush=True)
print("DONE files_read=%d hits=%d"% (n, hitn), flush=True)