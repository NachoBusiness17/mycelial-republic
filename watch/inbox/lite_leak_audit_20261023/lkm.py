#!/usr/bin/env python3
"""Lite leak matcher — never prints secret; HIT lines are path + counts only."""
import sys, os, hashlib
def load_key():
    src = sys.argv[1] if len(sys.argv) > 1 else "-"
    if src == "-":
        k = sys.stdin.buffer.readline().rstrip(b"\r\n").decode("utf-8", "replace").strip()
    elif src == "GUARD":
        sys.path.insert(0, r"C:\Users\foste\Documents\projects\local_sovereign_agent")
        from tools.secret_guard.guard import load_secret
        envp = r"C:\Users\foste\Documents\projects\local_sovereign_agent\.env"
        k = load_secret(envp, "ZAI_API_KEY_Lite", caller="lite_leak_audit_20261023")
    else:
        # line N (1-based) of dotenv; default 44
        n = int(os.environ.get("LKM_LINE", "44"))
        lines = open(src, encoding="utf-8", errors="replace").read().splitlines()
        line = lines[n - 1]
        if "=" not in line:
            raise SystemExit("bad dotenv line")
        k = line.split("=", 1)[1].strip().strip('"').strip("'")
    if len(k) < 16:
        raise SystemExit("key too short")
    return k
KEY = load_key()
PATS = [KEY.encode("utf-8"), KEY[:-8].encode("utf-8"), hashlib.sha256(KEY.encode("utf-8")).hexdigest().encode("ascii")]
# drop key from locals for residual
del KEY
MAX = 200_000_000
EXCL = set()
for p in os.environ.get("MX", "").split(os.pathsep):
    if p:
        EXCL.add(os.path.abspath(p).lower() if os.name == "nt" else os.path.abspath(p))
def hits(b):
    return [b.count(p) for p in PATS]
def report(tag, c):
    if any(c):
        print("HIT", tag, "full=%d noLast8=%d sha=%d" % tuple(c), flush=True)
tot = 0
def scan_file(path):
    global tot
    try:
        ap = os.path.abspath(path)
        if (ap.lower() if os.name == "nt" else ap) in EXCL:
            return
        if os.path.getsize(path) > MAX:
            return
        with open(path, "rb") as f:
            b = f.read()
    except Exception:
        return
    tot += 1
    report(path, hits(b))
def scan_git_batch(list_path):
    import subprocess
    n = 0
    with open(list_path, "rb") as lf:
        p = subprocess.Popen(["git", "cat-file", "--batch"], stdin=lf, stdout=subprocess.PIPE)
    while True:
        h = p.stdout.readline()
        if not h:
            break
        parts = h.split()
        if len(parts) < 3:
            continue
        sha, typ, sz = parts[0], parts[1], int(parts[2])
        d = p.stdout.read(sz)
        p.stdout.read(1)
        n += 1
        c = hits(d)
        if any(c):
            print("HIT git", sha.decode(), typ.decode(), "full=%d noLast8=%d sha=%d" % tuple(c), flush=True)
    p.wait()
    print("git_objects_scanned", n, flush=True)
args = sys.argv[2:]
i = 0
while i < len(args):
    root = args[i]
    if root == "GIT":
        i += 1
        scan_git_batch(args[i])
    elif root == "STDIN_BLOB":
        b = sys.stdin.buffer.read()
        report("<stdin>", hits(b))
    elif os.path.isfile(root):
        scan_file(root)
    elif os.path.isdir(root):
        for dp, dns, fns in os.walk(root):
            ap = os.path.abspath(dp)
            if (ap.lower() if os.name == "nt" else ap) in EXCL:
                dns[:] = []
                continue
            for fn in fns:
                scan_file(os.path.join(dp, fn))
        print("DONE", root, "files_read", tot, flush=True)
    else:
        print("SKIP_MISSING", root, flush=True)
    i += 1
print("TOTAL_FILES_READ", tot, flush=True)
