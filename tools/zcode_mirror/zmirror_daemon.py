"""zmirror_daemon - read-only, Tailscale-only mirror of ZCode session state.

Source: ZCode's own append-only per-session rollout logs (~/.zcode/cli/rollout/*.jsonl),
read-only. ZCode is NOT patched, NOT restarted, and no ZCode credentials are read:
request/response headers and request bodies (system prompt/tools) are dropped before storage.

Store (SQLite, zmirror.db):
  chunks(session_id, seq, prev_hash, hash, payload)  hash = sha256(prev_hash_bytes || seq_u64be || payload_utf8)
  snapshots(session_id, base_seq, base_hash, blob_hash, created_at, blob)  blob = zlib(JSON list of payloads 1..base_seq)
  sources(session_id, path, offset, head_sig, epoch)
Compaction: every COMPACT_CHUNKS chunks or COMPACT_BYTES bytes beyond the snapshot -> new snapshot, older chunks dropped.
Source rewrite/rotation (ZCode replaces rollout files per call): re-read, dedupe by requestId|attempt|completedAt, append only new.
Invalidation (analog of task_snapshot_invalidated): POST /admin/resnapshot/{id} (tailnet only) or local store loss -> clients get RESET+snapshot.

HTTP (bound ONLY to the Tailscale IP):
  GET  /sessions                 GET /snapshot/{id}
  POST /sync {sessionId, haveSeq, haveHash}  -> {status: OK|RESET, chunks[...], more, headSeq, headHash, snapshot?}
  GET  /subscribe/{id}?haveSeq=  (SSE)       GET /view/{id}  (IndexedDB viewer)
"""
from __future__ import annotations
import base64, hashlib, json, os, sqlite3, sys, threading, time, zlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

HERE = Path(__file__).resolve().parent
BIND = os.environ.get("ZMIRROR_BIND", "100.125.103.60")
PORT = int(os.environ.get("ZMIRROR_PORT", "8790"))
ROLLOUT = Path(os.environ.get("ZMIRROR_SRC", str(Path.home() / ".zcode" / "cli" / "rollout")))
DB = Path(os.environ.get("ZMIRROR_DB", str(HERE / "data" / "zmirror.db")))
STAGE = Path(os.environ.get("ZMIRROR_STAGE", str(HERE / "rib_stage")))
COMPACT_CHUNKS = int(os.environ.get("ZMIRROR_COMPACT_CHUNKS", "500"))
COMPACT_BYTES = int(os.environ.get("ZMIRROR_COMPACT_BYTES", str(32 * 1024 * 1024)))
PAGE_BYTES = 256 * 1024
POLL_S = 2.0
TRAJ_TURNS = 8
GENESIS = "0" * 64

if BIND in ("0.0.0.0", "", "::"):
    sys.exit("refusing to bind to all interfaces")

def chain_hash(prev_hex: str, seq: int, payload: str) -> str:
    return hashlib.sha256(bytes.fromhex(prev_hex) + seq.to_bytes(8, "big") + payload.encode("utf-8")).hexdigest()

def sanitize(rec: dict) -> dict:
    """Keep conversation content only; drop all headers and request body (system/tools)."""
    req = rec.get("request") or {}
    resp = rec.get("response") or {}
    out = {
        "requestId": rec.get("requestId"), "completedAt": rec.get("completedAt"),
        "durationMs": rec.get("durationMs"), "attempt": rec.get("attempt"),
        "model": (rec.get("model") or {}).get("modelId"), "querySource": rec.get("querySource"),
        "messageOffset": req.get("messageOffset"), "messageCount": req.get("messageCount"),
        "messages": req.get("messages"),
    }
    if resp:
        out["response"] = {k: resp.get(k) for k in ("finishReason", "text", "toolCalls", "usage", "reasoningText") if k in resp}
    if rec.get("error") is not None:
        e = rec["error"]
        out["error"] = (e if isinstance(e, str) else json.dumps(e))[:2000]
    return out

_lock = threading.RLock()
_cond = threading.Condition(_lock)

def db() -> sqlite3.Connection:
    c = sqlite3.connect(DB, check_same_thread=False, timeout=30)
    c.execute("PRAGMA journal_mode=WAL")
    return c

CONN: sqlite3.Connection

def init():
    global CONN
    DB.parent.mkdir(parents=True, exist_ok=True)
    CONN = db()
    CONN.executescript("""
    CREATE TABLE IF NOT EXISTS chunks(session_id TEXT, seq INTEGER, prev_hash TEXT, hash TEXT, payload TEXT, PRIMARY KEY(session_id, seq));
    CREATE TABLE IF NOT EXISTS snapshots(session_id TEXT PRIMARY KEY, base_seq INTEGER, base_hash TEXT, blob_hash TEXT, created_at REAL, blob BLOB);
    CREATE TABLE IF NOT EXISTS seen(session_id TEXT, rec_key TEXT, PRIMARY KEY(session_id, rec_key));
    CREATE TABLE IF NOT EXISTS sources(session_id TEXT PRIMARY KEY, path TEXT, offset INTEGER, head_sig TEXT, epoch INTEGER, updated REAL);
    """)
    CONN.commit()

def head(sid):
    r = CONN.execute("SELECT seq, hash FROM chunks WHERE session_id=? ORDER BY seq DESC LIMIT 1", (sid,)).fetchone()
    if r: return r[0], r[1]
    s = CONN.execute("SELECT base_seq, base_hash FROM snapshots WHERE session_id=?", (sid,)).fetchone()
    return (s[0], s[1]) if s else (0, GENESIS)

def snapshot_row(sid):
    return CONN.execute("SELECT base_seq, base_hash, blob_hash, created_at, blob FROM snapshots WHERE session_id=?", (sid,)).fetchone()

def wipe(sid):
    CONN.execute("DELETE FROM chunks WHERE session_id=?", (sid,))
    CONN.execute("DELETE FROM snapshots WHERE session_id=?", (sid,))

def compact(sid, force=False):
    snap = snapshot_row(sid)
    base = snap[0] if snap else 0
    n, size = CONN.execute("SELECT COUNT(*), COALESCE(SUM(LENGTH(payload)),0) FROM chunks WHERE session_id=? AND seq>?", (sid, base)).fetchone()
    if not force and n < COMPACT_CHUNKS and size < COMPACT_BYTES:
        return False
    if n == 0: return False
    prev = json.loads(zlib.decompress(snap[4])) if snap else []
    rows = CONN.execute("SELECT seq, hash, payload FROM chunks WHERE session_id=? AND seq>? ORDER BY seq", (sid, base)).fetchall()
    allp = prev + [json.loads(p) for _, _, p in rows]
    blob = zlib.compress(json.dumps(allp, separators=(",", ":")).encode(), 6)
    bseq, bhash = rows[-1][0], rows[-1][1]
    CONN.execute("INSERT OR REPLACE INTO snapshots VALUES(?,?,?,?,?,?)", (sid, bseq, bhash, hashlib.sha256(blob).hexdigest(), time.time(), blob))
    # keep the newest chunk window so small gaps still sync without RESET; drop older ones
    keep_from = max(base, bseq - 64)
    CONN.execute("DELETE FROM chunks WHERE session_id=? AND seq<=?", (sid, keep_from))
    return True

def ingest_file(p: Path):
    sid = p.stem.replace("model-io-", "")
    st = p.stat()
    with open(p, "rb") as f:
        sig = hashlib.sha256(f.read(4096)).hexdigest()
    src = CONN.execute("SELECT offset, head_sig, epoch FROM sources WHERE session_id=?", (sid,)).fetchone()
    offset, epoch = (src[0], src[2]) if src else (0, 0)
    if src and (st.st_size < offset or src[1] != sig):
        # ZCode rewrites/rotates rollout files (observed: file replaced per model call). Treat as a new
        # generation: re-read from 0 and append only records not yet seen. Our chain stays append-only.
        offset = 0; epoch += 1
    if st.st_size == offset and src:
        return 0
    added = 0
    with open(p, "rb") as f:
        f.seek(offset)
        seq, prev = head(sid)
        while True:
            line = f.readline()
            if not line or not line.endswith(b"\n"):
                break  # partial line: wait for writer
            offset += len(line)
            try:
                rec = json.loads(line)
            except Exception:
                continue
            key = hashlib.sha256(f"{rec.get('requestId')}|{rec.get('attempt')}|{rec.get('completedAt')}".encode()).hexdigest()
            if CONN.execute("INSERT OR IGNORE INTO seen VALUES(?,?)", (sid, key)).rowcount == 0:
                continue
            payload = json.dumps(sanitize(rec), separators=(",", ":"), ensure_ascii=False)
            seq += 1
            h = chain_hash(prev, seq, payload)
            CONN.execute("INSERT INTO chunks VALUES(?,?,?,?,?)", (sid, seq, prev, h, payload))
            prev = h; added += 1
    CONN.execute("INSERT OR REPLACE INTO sources VALUES(?,?,?,?,?,?)", (sid, str(p), offset, sig, epoch, time.time()))
    if added and not snapshot_row(sid):
        compact(sid, force=True)  # initial snapshot
    else:
        compact(sid)
    return added

def trajectory(sid) -> dict:
    """Plain extraction (no LLM): last N completed turns."""
    rows = CONN.execute("SELECT seq, payload FROM chunks WHERE session_id=? ORDER BY seq DESC LIMIT 200", (sid,)).fetchall()
    turns = []
    for seq, pl in rows:
        d = json.loads(pl)
        r = d.get("response")
        if not r: continue
        user = ""
        for m in reversed(d.get("messages") or []):
            if isinstance(m, dict) and m.get("role") == "user":
                c = m.get("content")
                if isinstance(c, list):
                    c = " ".join(x.get("text", "") for x in c if isinstance(x, dict) and x.get("type") == "text")
                user = str(c or "").strip().replace("\n", " ")[:240]
                if user: break
        tools = [(t.get("toolName") or t.get("name")) for t in (r.get("toolCalls") or []) if isinstance(t, dict)]
        turns.append({"seq": seq, "at": d.get("completedAt"), "model": d.get("model"),
                      "user": user, "reply": str(r.get("text") or "").strip().replace("\n", " ")[:300],
                      "tools": tools[:12], "finish": r.get("finishReason")})
        if len(turns) >= TRAJ_TURNS: break
    hs, hh = head(sid)
    return {"schema": "zcode_mirror.trajectory.v1", "sessionId": sid, "headSeq": hs, "headHash": hh,
            "generatedAt": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "turns": list(reversed(turns))}

def stage_trajectory(sid):
    STAGE.mkdir(parents=True, exist_ok=True)
    t = trajectory(sid)
    (STAGE / f"{sid}.trajectory.json").write_text(json.dumps(t, indent=1, ensure_ascii=False), encoding="utf-8")

def scanner():
    while True:
        try:
            changed = []
            with _lock:
                for p in sorted(ROLLOUT.glob("*.jsonl")):
                    try:
                        if ingest_file(p): changed.append(p.stem.replace("model-io-", ""))
                    except Exception as e:
                        print("ingest error", p.name, e, flush=True)
                CONN.commit()
                for sid in changed: stage_trajectory(sid)
                if changed: _cond.notify_all()
        except Exception as e:
            print("scan error", e, flush=True)
        time.sleep(POLL_S)

def sessions():
    out = []
    for sid, path, upd in CONN.execute("SELECT session_id, path, updated FROM sources ORDER BY updated DESC").fetchall():
        hs, hh = head(sid); s = snapshot_row(sid)
        out.append({"sessionId": sid, "headSeq": hs, "headHash": hh, "snapshotBaseSeq": s[0] if s else None,
                    "updated": upd})
    return out

def snapshot_obj(sid, with_blob=True):
    s = snapshot_row(sid)
    if not s: return None
    o = {"sessionId": sid, "baseSeq": s[0], "baseHash": s[1], "blobHash": s[2], "createdAt": s[3]}
    if with_blob: o["blob"] = base64.b64encode(s[4]).decode()
    return o

def sync(sid, have_seq, have_hash):
    hs, hh = head(sid)
    snap = snapshot_row(sid)
    ok = False
    if have_seq == 0 and have_hash in ("", GENESIS):
        ok = CONN.execute("SELECT 1 FROM chunks WHERE session_id=? AND seq=1", (sid,)).fetchone() is not None or hs == 0
    elif snap and have_seq == snap[0]:
        ok = have_hash == snap[1]
    else:
        r = CONN.execute("SELECT hash FROM chunks WHERE session_id=? AND seq=?", (sid, have_seq)).fetchone()
        ok = bool(r and r[0] == have_hash)
    if not ok:
        return {"status": "RESET", "sessionId": sid, "headSeq": hs, "headHash": hh, "snapshot": snapshot_obj(sid)}
    chunks, size = [], 0
    for seq, prev, h, pl in CONN.execute("SELECT seq, prev_hash, hash, payload FROM chunks WHERE session_id=? AND seq>? ORDER BY seq", (sid, have_seq)):
        b = len(pl.encode())
        if chunks and size + b > PAGE_BYTES: break
        chunks.append({"seq": seq, "prevHash": prev, "hash": h, "payload": pl}); size += b
    more = bool(chunks) and chunks[-1]["seq"] < hs
    return {"status": "OK", "sessionId": sid, "headSeq": hs, "headHash": hh, "chunks": chunks, "more": more, "pageBytes": size}

VIEW = (HERE / "view.html")

class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    def log_message(self, *a): pass
    def _json(self, obj, code=200):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        u = urlparse(self.path); parts = [x for x in u.path.split("/") if x]
        with _lock:
            if parts == ["sessions"]: return self._json(sessions())
            if parts == ["health"]: return self._json({"ok": True, "bind": f"{BIND}:{PORT}"})
            if len(parts) == 2 and parts[0] == "snapshot":
                s = snapshot_obj(parts[1]); return self._json(s or {"error": "not found"}, 200 if s else 404)
            if len(parts) == 2 and parts[0] == "trajectory":
                return self._json(trajectory(parts[1]))
        if len(parts) == 2 and parts[0] == "view":
            b = VIEW.read_bytes().replace(b"__SID__", parts[1].encode())
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b); return
        if len(parts) == 2 and parts[0] == "subscribe":
            return self.sse(parts[1], int((parse_qs(u.query).get("haveSeq") or ["0"])[0]))
        self._json({"error": "not found"}, 404)
    def do_POST(self):
        u = urlparse(self.path)
        if u.path.startswith("/admin/resnapshot/"):
            with _lock:
                ok = compact(u.path.rsplit("/", 1)[1], force=True); CONN.commit()
            return self._json({"ok": ok})
        if u.path != "/sync": return self._json({"error": "not found"}, 404)
        n = int(self.headers.get("Content-Length") or 0)
        try:
            req = json.loads(self.rfile.read(n) or b"{}")
            with _lock:
                return self._json(sync(str(req["sessionId"]), int(req.get("haveSeq") or 0), str(req.get("haveHash") or "")))
        except Exception as e:
            return self._json({"error": str(e)[:200]}, 400)
    def sse(self, sid, have):
        self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.send_header("Cache-Control", "no-cache"); self.end_headers()
        last = have
        try:
            while True:
                with _cond:
                    hs, hh = head(sid)
                    if hs <= last: _cond.wait(timeout=15); hs, hh = head(sid)
                ev = {"sessionId": sid, "headSeq": hs, "headHash": hh} if hs > last else None
                msg = f"event: head\ndata: {json.dumps(ev)}\n\n" if ev else ": keepalive\n\n"
                self.wfile.write(msg.encode()); self.wfile.flush(); last = max(last, hs)
        except Exception:
            return

def main():
    init()
    threading.Thread(target=scanner, daemon=True).start()
    srv = ThreadingHTTPServer((BIND, PORT), H)
    (HERE / "data" / "zmirror.pid").write_text(str(os.getpid()))
    print(f"zmirror listening on http://{BIND}:{PORT} src={ROLLOUT}", flush=True)
    srv.serve_forever()

if __name__ == "__main__":
    main()
