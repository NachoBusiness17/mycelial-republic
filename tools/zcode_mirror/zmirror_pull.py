#!/usr/bin/env python3
"""zmirror_pull - Termux/phone client. Keeps ~/zmirror/<session>.db, sends HAVE, pulls only the gap,
verifies the hash chain, prints seq/hash + bytes/chunks transferred.
usage: zmirror_pull.py [--url http://100.125.103.60:8790] [--list] [--truncate N] [--corrupt] SESSION_ID"""
import argparse, base64, hashlib, json, os, sqlite3, sys, urllib.request, zlib
GENESIS = "0" * 64
def chain_hash(prev, seq, payload):
    return hashlib.sha256(bytes.fromhex(prev) + seq.to_bytes(8, "big") + payload.encode("utf-8")).hexdigest()
class Net:
    def __init__(s, url): s.url = url.rstrip("/"); s.bytes = 0; s.reqs = 0
    def call(s, path, body=None):
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(s.url + path, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            b = r.read(); s.bytes += len(b); s.reqs += 1
            return json.loads(b)
def open_db(sid):
    d = os.path.expanduser("~/zmirror"); os.makedirs(d, exist_ok=True)
    c = sqlite3.connect(os.path.join(d, f"{sid}.db"))
    c.executescript("""CREATE TABLE IF NOT EXISTS chunks(seq INTEGER PRIMARY KEY, prev_hash TEXT, hash TEXT, payload TEXT);
    CREATE TABLE IF NOT EXISTS snap(id INTEGER PRIMARY KEY CHECK(id=1), base_seq INTEGER, base_hash TEXT, blob_hash TEXT, blob BLOB);""")
    return c
def have(c):
    r = c.execute("SELECT seq, hash FROM chunks ORDER BY seq DESC LIMIT 1").fetchone()
    if r: return r
    s = c.execute("SELECT base_seq, base_hash FROM snap").fetchone()
    return s if s else (0, GENESIS)
def verify(c):
    s = c.execute("SELECT base_seq, base_hash, blob_hash, blob FROM snap").fetchone()
    seq, prev = (s[0], s[1]) if s else (0, GENESIS)
    if s and hashlib.sha256(s[3]).hexdigest() != s[2]: return False, "snapshot blob hash mismatch"
    n = 0
    for q, p, h, pl in c.execute("SELECT seq, prev_hash, hash, payload FROM chunks WHERE seq>? ORDER BY seq", (seq,)):
        if q != seq + 1 or p != prev or chain_hash(prev, q, pl) != h: return False, f"chain break at {q}"
        seq, prev, n = q, h, n + 1
    return True, f"verified {n} chunks from base {s[0] if s else 0}"
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("session", nargs="?"); ap.add_argument("--url", default=os.environ.get("ZMIRROR_URL", "http://100.125.103.60:8790"))
    ap.add_argument("--list", action="store_true"); ap.add_argument("--truncate", type=int, default=0); ap.add_argument("--corrupt", action="store_true")
    a = ap.parse_args(); net = Net(a.url)
    if a.list or not a.session:
        for s in net.call("/sessions"): print(s["sessionId"], s["headSeq"], s["headHash"][:16])
        return
    c = open_db(a.session)
    if a.truncate:
        top = have(c)[0]; c.execute("DELETE FROM chunks WHERE seq>?", (top - a.truncate,)); c.commit(); print(f"[test] truncated local copy by {a.truncate} chunks (was {top})")
    if a.corrupt:
        top = have(c)[0]; c.execute("UPDATE chunks SET hash=? WHERE seq=?", ("f" * 64, top)); c.commit(); print(f"[test] corrupted local hash at seq {top}")
    seq0, h0 = have(c); print(f"HAVE seq={seq0} hash={h0[:16]}")
    got, resets = 0, 0
    while True:
        seq, h = have(c)
        r = net.call("/sync", {"sessionId": a.session, "haveSeq": seq, "haveHash": h})
        if r.get("status") == "RESET":
            resets += 1
            if resets > 2: sys.exit("repeated RESET")
            s = r.get("snapshot"); c.execute("DELETE FROM chunks"); c.execute("DELETE FROM snap")
            if s:
                blob = base64.b64decode(s["blob"])
                if hashlib.sha256(blob).hexdigest() != s["blobHash"]: sys.exit("snapshot hash mismatch")
                c.execute("INSERT INTO snap VALUES(1,?,?,?,?)", (s["baseSeq"], s["baseHash"], s["blobHash"], blob))
                print(f"RESET -> snapshot baseSeq={s['baseSeq']} blob={len(blob)}B")
            c.commit(); continue
        prev = h
        for ch in r["chunks"]:
            if ch["prevHash"] != prev or chain_hash(prev, ch["seq"], ch["payload"]) != ch["hash"]: sys.exit(f"chain verify FAILED at {ch['seq']}")
            c.execute("INSERT INTO chunks VALUES(?,?,?,?)", (ch["seq"], ch["prevHash"], ch["hash"], ch["payload"])); prev = ch["hash"]; got += 1
        c.commit()
        if not r.get("more"): break
    ok, msg = verify(c); seq, h = have(c)
    print(f"PULLED chunks={got} bytes={net.bytes} requests={net.reqs} resets={resets}")
    print(f"NOW seq={seq} hash={h} server_head={r['headSeq']} match={h == r['headHash']} chain={'OK' if ok else 'FAIL'} ({msg})")
if __name__ == "__main__": main()
