# prior_art: mag/mcp_http.py, mag/seat_handshake.py -- mcp_http serves one seat in-process; seat_handshake signs the domain-tagged strings this relay envelopes cross-node (its own self-steal sources, named in the docstring below)
"""mag_relay: stateless signed JSON-RPC (MCP Streamable HTTP style) relay between Mag nodes.

Built 2026-10-25. 2026-10-25 later: + health tool, hermes provenance (agent.log parse), STOP-file kill switch.
Self-steal sources (PC repo local_sovereign_agent):
  - mag/mcp_http.py (2026-10-17): stateless POST, one JSON-RPC per request, 202 for notifications.
  - mag/seat_handshake.py (2026-10-17): Ed25519 over a domain-tagged canonical string,
    allowlist of PUBLIC keys only, skew window, ReplayCache, bare reject with no detail.
  - scripts/verify_knot_v2.py (2026-10-17): pure-Python RFC 8032 Ed25519 (used when the
    `cryptography` package is absent, as on the Termux phones).
  - hermes_fleet/fleet.py on Bob (2026-10-25): hermes chat --query-file invocation shape.
Not touched: the Mag verkle chain, its tip, its ACL. The relay ledger is a separate JSONL file.

Usage:
  python mag_relay.py keygen --node NAME            # private seed stays in ~/.mag_relay, prints pubkey only
  python mag_relay.py serve --node NAME --bind IP [--port 8765]   # foreground only
  python mag_relay.py call --node NAME --to URL --tool T --args JSON
  python mag_relay.py merge --out merged_ledger.jsonl RECEIPTS.jsonl...   (Bob)
"""
from __future__ import annotations
import argparse, hashlib, json, os, secrets, shutil, subprocess, sys, time, urllib.request, uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

DOMAIN = b"mag-relay.v1\n"
SKEW_S = 120
HOME = Path(os.environ.get("MAG_RELAY_HOME", Path.home() / ".mag_relay"))
ALLOWED_TOOLS = ["submit_task", "get_result", "append_record", "read_chain_head", "describe_image", "health"]

# ---------------- Ed25519 (cryptography if present, else RFC 8032 pure, from verify_knot_v2.py)
_P = 2 ** 255 - 19
_L = 2 ** 252 + 27742317777372353535851937790883648493
def _inv(x): return pow(x, _P - 2, _P)
_D = -121665 * _inv(121666) % _P
_SQRT_M1 = pow(2, (_P - 1) // 4, _P)
def _add(P, Q):
    A = (P[1] - P[0]) * (Q[1] - Q[0]) % _P; B = (P[1] + P[0]) * (Q[1] + Q[0]) % _P
    C = 2 * P[3] * Q[3] * _D % _P; D = 2 * P[2] * Q[2] % _P
    E, F, G, H = B - A, D - C, D + C, B + A
    return (E * F % _P, G * H % _P, F * G % _P, E * H % _P)
def _mul(s, P):
    Q = (0, 1, 1, 0)
    while s > 0:
        if s & 1: Q = _add(Q, P)
        P = _add(P, P); s >>= 1
    return Q
def _eq(P, Q): return (P[0]*Q[2]-Q[0]*P[2]) % _P == 0 and (P[1]*Q[2]-Q[1]*P[2]) % _P == 0
def _recover_x(y, sign):
    if y >= _P: return None
    x2 = (y*y - 1) * _inv(_D*y*y + 1)
    if x2 == 0: return None if sign else 0
    x = pow(x2, (_P + 3) // 8, _P)
    if (x*x - x2) % _P: x = x * _SQRT_M1 % _P
    if (x*x - x2) % _P: return None
    if (x & 1) != sign: x = _P - x
    return x
_GY = 4 * _inv(5) % _P; _GX = _recover_x(_GY, 0); _G = (_GX, _GY, 1, _GX * _GY % _P)
def _compress(P):
    zi = _inv(P[2]); x, y = P[0]*zi % _P, P[1]*zi % _P
    return int.to_bytes(y | ((x & 1) << 255), 32, "little")
def _decompress(s):
    if len(s) != 32: return None
    y = int.from_bytes(s, "little"); sign = y >> 255; y &= (1 << 255) - 1
    x = _recover_x(y, sign)
    return None if x is None else (x, y, 1, x*y % _P)
def _h(b): return int.from_bytes(hashlib.sha512(b).digest(), "little") % _L
def _expand(seed):
    h = hashlib.sha512(seed).digest(); a = int.from_bytes(h[:32], "little")
    a &= (1 << 254) - 8; a |= 1 << 254
    return a, h[32:]
def _crypto():
    try:
        from cryptography.hazmat.primitives.asymmetric import ed25519
        return ed25519
    except ImportError:
        return None
def pub_from_seed(seed):
    c = _crypto()
    if c:
        from cryptography.hazmat.primitives import serialization as s
        return c.Ed25519PrivateKey.from_private_bytes(seed).public_key().public_bytes(s.Encoding.Raw, s.PublicFormat.Raw)
    return _compress(_mul(_expand(seed)[0], _G))
def sign(seed, msg):
    c = _crypto()
    if c: return c.Ed25519PrivateKey.from_private_bytes(seed).sign(msg)
    a, prefix = _expand(seed); A = _compress(_mul(a, _G)); r = _h(prefix + msg)
    R = _compress(_mul(r, _G)); s = (r + _h(R + A + msg) * a) % _L
    return R + int.to_bytes(s, 32, "little")
def verify(pub, msg, sig):
    if len(pub) != 32 or len(sig) != 64: return False
    c = _crypto()
    if c:
        try: c.Ed25519PublicKey.from_public_bytes(pub).verify(sig, msg); return True
        except Exception: return False
    A = _decompress(pub); R = _decompress(sig[:32]); s = int.from_bytes(sig[32:], "little")
    if A is None or R is None or s >= _L: return False
    return _eq(_mul(s, _G), _add(R, _mul(_h(sig[:32] + pub + msg), A)))

# ---------------- keys, peers
def key_path(node): return HOME / f"{node}.seed"
def load_seed(node): return key_path(node).read_bytes()
def keygen(node):
    HOME.mkdir(parents=True, exist_ok=True); p = key_path(node)
    if not p.exists():
        fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0), 0o600)
        os.write(fd, secrets.token_bytes(32)); os.close(fd)
    print(json.dumps({"node": node, "pub": pub_from_seed(load_seed(node)).hex()}))
def load_peers():
    p = HOME / "peers.json"
    return json.loads(p.read_text(encoding="utf-8-sig")) if p.exists() else {}

# ---------------- canonical + envelope
def canon(env):
    f = {k: env[k] for k in ("from", "to", "ts", "nonce", "head", "tool")}
    f["payload_sha"] = hashlib.sha256(json.dumps(env["args"], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return DOMAIN + json.dumps(f, sort_keys=True, separators=(",", ":")).encode()
def sha(s): return hashlib.sha256(s.encode() if isinstance(s, str) else s).hexdigest()

# ---------------- node-local hash-linked ledger
class Ledger:
    def __init__(self, node):
        self.path = HOME / f"relay_ledger_{node}.jsonl"; self.head = "0" * 64; self.nonces = set(); self.n = 0
        if self.path.exists():
            for line in self.path.read_text(encoding="utf-8").splitlines():
                r = json.loads(line); self.head = r["hash"]; self.n += 1
                if r.get("kind") == "call": self.nonces.add((r["from"], r["nonce"]))
    def append(self, rec):
        rec = dict(rec, seq=self.n, prev=self.head, t=time.time())
        rec["hash"] = sha(json.dumps(rec, sort_keys=True, separators=(",", ":")))
        with open(self.path, "a", encoding="utf-8") as f: f.write(json.dumps(rec, sort_keys=True) + "\n")
        self.head = rec["hash"]; self.n += 1
        return rec

# ---------------- tools
def tool_impl(node, ledger, name, args):
    tasks = HOME / "tasks"; tasks.mkdir(exist_ok=True)
    if name == "read_chain_head": return {"node": node, "head": ledger.head, "seq": ledger.n}
    if name == "append_record":
        r = ledger.append({"kind": "record", "record": args.get("record")}); return {"seq": r["seq"], "hash": r["hash"]}
    if name == "health": return health(node)
    if name == "submit_task":
        tid = uuid.uuid4().hex[:12]
        (tasks / f"{tid}.json").write_text(json.dumps({"prompt": args.get("prompt", ""), "state": "queued"}))
        hb = shutil.which("hermes") or (str(Path.home() / ".local/bin/hermes") if (Path.home() / ".local/bin/hermes").exists() else None)
        if args.get("run") and hb:  # opt-in; runs in the request; provenance parsed from hermes agent.log
            qf = tasks / f"{tid}.prompt"; qf.write_text(args["prompt"], encoding="utf-8")
            argv = [hb, "chat", "--query-file", str(qf), "-Q"]
            if args.get("provider") in PROVIDER_OK: argv += ["--provider", args["provider"]]
            if args.get("model") and all(c.isalnum() or c in "-_./:" for c in args["model"]): argv += ["-m", args["model"]]
            log = hermes_home() / "logs" / "agent.log"; off = log.stat().st_size if log.exists() else 0
            t0 = time.time()
            try:
                p = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=int(args.get("timeout", 300)))
                ex, out = p.returncode, p.stdout
            except subprocess.TimeoutExpired: ex, out = "timeout", ""
            qf.unlink(missing_ok=True)
            prov = provenance(log, off)
            (tasks / f"{tid}.json").write_text(json.dumps({"prompt": args["prompt"], "state": "done", "exit": ex, "secs": round(time.time() - t0, 1), "out": out[-4000:], "provenance": prov}))
        return {"task_id": tid}
    if name == "get_result":
        p = tasks / f"{args.get('task_id','')}.json"
        return json.loads(p.read_text()) if p.exists() and args.get("task_id", "").isalnum() else {"error": "unknown task"}
    if name == "describe_image":
        model = os.environ.get("MAG_RELAY_VISION_MODEL")  # e.g. a local ollama vision model; no paid keys
        if not model: return {"error": "no vision model on this node", "node": node}
        body = json.dumps({"model": model, "prompt": args.get("prompt", "Describe this image."), "images": [args["image_b64"]], "stream": False}).encode()
        r = urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:11434/api/generate", body, {"Content-Type": "application/json"}), timeout=300)
        return {"model": model, "text": json.loads(r.read())["response"], "provenance": {"node": node, "provider": "ollama", "base_url_host": "127.0.0.1:11434", "model": model, "fallback": False, "chain": []}}
    return {"error": "tool not allowed"}


# ---------------- health + provenance (router support, 2026-10-25). Names only, never values.
import re
PROVIDER_OK = {"zai", "deepseek", "openrouter", "nous", "custom", "nous-nacho", "nous-sdd"}
def hermes_home(): return Path(os.environ.get("HERMES_HOME") or (Path.home() / ".hermes"))
def _hermes_cfg():
    y = hermes_home() / "config.yaml"; out = {"primary": {}, "fallbacks": []}
    if not y.exists(): return out
    sec = None
    for l in y.read_text(encoding="utf-8", errors="replace").splitlines():
        if re.match(r"^\S", l): sec = l.split(":")[0].strip()
        m = re.match(r"^\s+-?\s*(provider|default|model|base_url)\s*:\s*\"?([^\"#\s]+)", l)
        if not m: continue
        k, v = m.group(1), m.group(2)
        if sec == "model": out["primary"]["model" if k == "default" else k] = v
        elif sec == "fallback_model":
            if k == "provider": out["fallbacks"].append({"provider": v})
            elif out["fallbacks"]: out["fallbacks"][-1][k] = v
    return out
def _env_names():
    e = hermes_home() / ".env"; names = set(k for k in os.environ if re.search("ZAI|ZHIPU|GLM", k))
    if e.exists():
        for l in e.read_text(encoding="utf-8", errors="replace").splitlines():
            m = re.match(r"^\s*(?:export\s+)?([A-Z_0-9]+)=", l)
            if m: names.add(m.group(1))
    return sorted(n for n in names if re.search("ZAI|ZHIPU|GLM|NOUS|OPENROUTER|DEEPSEEK|NVIDIA", n))
def health(node):
    h = {"node": node, "ts": time.time(), "free_mb": None, "battery": None, "charging": None, "jobs": 0, "gpu": None, "ollama": []}
    try:
        if os.name == "nt":
            o = subprocess.run(["powershell", "-NoProfile", "-Command", "[int]((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1024)"], capture_output=True, text=True, timeout=20)
            h["free_mb"] = int(o.stdout.strip() or 0); h["charging"] = True
        else:
            for l in open("/proc/meminfo"):
                if l.startswith("MemAvailable"): h["free_mb"] = int(l.split()[1]) // 1024
            b = subprocess.run(["timeout", "8", "termux-battery-status"], capture_output=True, text=True).stdout
            if b:
                b = json.loads(b); h["battery"] = b.get("percentage"); h["charging"] = b.get("plugged", "UNPLUGGED") != "UNPLUGGED"
        tasks = HOME / "tasks"
        h["jobs"] = sum(1 for f in tasks.glob("*.prompt")) if tasks.exists() else 0
    except Exception as e: h["err"] = type(e).__name__
    if shutil.which("nvidia-smi"):
        try: h["gpu"] = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.free", "--format=csv,noheader"], capture_output=True, text=True, timeout=15).stdout.strip()
        except Exception as e: h["gpu_err"] = type(e).__name__
    try: h["ollama"] = [m["name"] for m in json.loads(urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=3).read())["models"]]
    except Exception as e: h["ollama_err"] = type(e).__name__
    h["hermes"] = bool(shutil.which("hermes") or (Path.home() / ".local/bin/hermes").exists())
    h["hermes_cfg"] = _hermes_cfg(); h["key_env_names"] = _env_names()
    h["vision_model"] = os.environ.get("MAG_RELAY_VISION_MODEL")
    return h
_RX_CLIENT = re.compile(r"OpenAI client created \(chat_completion\w*.*?provider=(\S+) base_url=(\S+) model=(\S+)")
_RX_CALL = re.compile(r"API call #\d+: model=(\S+) provider=(\S+)")
_RX_FB = re.compile(r"(Fallback (?:to|skip)[^\n]{0,160}|refused for billing[^\n]{0,80}|Error code: (?:404|429|401|402)[^\n]{0,120})")
def provenance(log, off):
    """Parse the hermes agent.log lines written during this run: every endpoint attempted, fallbacks, final model."""
    try:
        with open(log, "rb") as f: f.seek(off); txt = f.read().decode("utf-8", "replace")
    except Exception: return {"error": "no agent.log"}
    tries = []
    for m in _RX_CLIENT.finditer(txt):
        t = {"provider": m.group(1), "base_url_host": re.sub(r"^https?://", "", m.group(2)).split("/")[0], "model": m.group(3)}
        if not tries or tries[-1] != t: tries.append(t)
    calls = _RX_CALL.findall(txt)
    events = [re.sub(r"(?i)(key|token|bearer)\S*", "[redacted]", e[:200]) for e in _RX_FB.findall(txt)][:12]
    final = dict(tries[-1]) if tries else {}
    if calls: final["model"], final["provider"] = calls[-1][0], calls[-1][1]
    for t in tries:
        if t["provider"] == final.get("provider") and t["model"] == final.get("model"): final["base_url_host"] = t["base_url_host"]
    fb = len(tries) > 1 or any("Fallback to" in e for e in events)
    return {"final": final, "attempts": tries, "fallback": fb, "events": events, "api_calls": len(calls)}

def whois_ok(ip, peer):
    """Tailscale whois where the CLI exists (Bob/PC); else source IP must equal the peer's pinned tailnet IP."""
    if ip != peer.get("ip"): return False
    ts = shutil.which("tailscale")
    if not ts or not peer.get("ts_host"): return True
    try:
        o = json.loads(subprocess.run([ts, "whois", "--json", ip], capture_output=True, text=True, timeout=10).stdout)
        return o.get("Node", {}).get("ComputedName", "").lower() == peer["ts_host"].lower()
    except Exception:
        return False

def serve(node, bind, port):
    if not bind.startswith("100."): sys.exit("refusing: bind must be a Tailscale 100.x address")
    seed = load_seed(node); ledger = Ledger(node); peers = load_peers()
    class H(BaseHTTPRequestHandler):
        def log_message(self, *a): pass
        def _send(self, code, obj):
            b = json.dumps(obj).encode(); self.send_response(code)
            self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(b)))
            self.end_headers(); self.wfile.write(b)
        def do_GET(self): self._send(405, {})
        def do_POST(self):
            if self.path != "/mcp": return self._send(404, {})
            try: msg = json.loads(self.rfile.read(min(int(self.headers.get("Content-Length", 0)), 8_000_000)))
            except Exception: return self._send(400, {})
            rid = msg.get("id"); method = msg.get("method")
            if rid is None: return self._send(202, {})
            if method == "initialize":
                return self._send(200, {"jsonrpc": "2.0", "id": rid, "result": {"protocolVersion": "2025-03-26", "capabilities": {"tools": {}}, "serverInfo": {"name": "mag-relay", "version": "0.1"}}})
            if method == "tools/list":
                return self._send(200, {"jsonrpc": "2.0", "id": rid, "result": {"tools": [{"name": t, "inputSchema": {"type": "object"}} for t in ALLOWED_TOOLS]}})
            if method != "tools/call": return self._send(200, {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "method not found"}})
            env = (msg.get("params") or {}).get("arguments", {}).get("mag_relay") or {}
            ip = self.client_address[0]; reason = None
            try:
                peer = peers.get(env["from"]); now = time.time()
                if not peer: reason = "unknown sender"
                elif env["to"] != node: reason = "wrong recipient"
                elif not whois_ok(ip, peer): reason = "whois/ip mismatch"
                elif abs(now - float(env["ts"])) > SKEW_S: reason = "stale"
                elif env["tool"] not in ALLOWED_TOOLS or env["tool"] not in peer.get("allow", []): reason = "policy"
                elif env["tool"] != msg["params"].get("name"): reason = "tool mismatch"
                elif (env["from"], env["nonce"]) in ledger.nonces: reason = "replay"
                elif not verify(bytes.fromhex(peer["pub"]), canon(env), bytes.fromhex(env["sig"])): reason = "bad signature"
            except Exception: reason = "malformed"
            if reason:
                ledger.append({"kind": "reject", "from": env.get("from") if isinstance(env, dict) else None, "ip": ip, "reason": reason})
                return self._send(200, {"jsonrpc": "2.0", "id": rid, "error": {"code": -32001, "message": "rejected"}})
            ledger.nonces.add((env["from"], env["nonce"]))
            call = ledger.append({"kind": "call", "from": env["from"], "nonce": env["nonce"], "tool": env["tool"], "ip": ip,
                                  "caller_head": env["head"], "req_sha": sha(canon(env)), "sig": env["sig"]})
            try: result = tool_impl(node, ledger, env["tool"], env["args"])
            except Exception as e: result = {"error": type(e).__name__}
            res = ledger.append({"kind": "result", "call_hash": call["hash"], "result_sha": sha(json.dumps(result, sort_keys=True))})
            receipt = {"node": node, "from": env["from"], "nonce": env["nonce"], "tool": env["tool"], "call_hash": call["hash"],
                       "result_hash": res["hash"], "result_sha": res["result_sha"], "ledger_head": ledger.head, "seq": res["seq"], "ts": time.time()}
            receipt["sig"] = sign(seed, DOMAIN + json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode()).hex()
            self._send(200, {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(result)}], "structuredContent": result, "receipt": receipt}})
    print(f"mag-relay {node} listening {bind}:{port} (foreground, Ctrl-C to stop)", flush=True)
    srv = ThreadingHTTPServer((bind, port), H)
    import threading
    def _watch():  # kill switch: create HOME/STOP to shut down
        while not (HOME / "STOP").exists(): time.sleep(3)
        srv.shutdown()
    threading.Thread(target=_watch, daemon=True).start()
    (HOME / f"serve_{node}.pid").write_text(str(os.getpid()))
    try: srv.serve_forever()
    except KeyboardInterrupt: (HOME / f"serve_{node}.pid").unlink(missing_ok=True)

def call(node, url, tool, args, to, nonce=None, head=None):
    ledger = Ledger(node)
    env = {"from": node, "to": to, "ts": time.time(), "nonce": nonce or secrets.token_hex(16), "head": head or ledger.head, "tool": tool, "args": args}
    env["sig"] = sign(load_seed(node), canon(env)).hex()
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": tool, "arguments": {"mag_relay": env}}}).encode()
    r = json.loads(urllib.request.urlopen(urllib.request.Request(url, body, {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}), timeout=600).read())
    rc = (r.get("result") or {}).get("receipt")
    if rc:
        peer = load_peers().get(to, {}); sig = bytes.fromhex(rc.pop("sig"))
        ok = verify(bytes.fromhex(peer.get("pub", "00")), DOMAIN + json.dumps(rc, sort_keys=True, separators=(",", ":")).encode(), sig)
        rc["sig"] = sig.hex(); rc["receipt_verified"] = ok
        with open(HOME / f"receipts_{node}.jsonl", "a", encoding="utf-8") as f: f.write(json.dumps(rc, sort_keys=True) + "\n")
    print(json.dumps(r, indent=1)); return r, env

def merge(out, files):
    """Bob: fold verified receipts into an append-only merged ledger (dedupe by node+call_hash). Never touches verkle."""
    out = Path(out); head, seen, n = "0" * 64, set(), 0
    if out.exists():
        for line in out.read_text(encoding="utf-8").splitlines():
            r = json.loads(line); head = r["hash"]; seen.add((r["receipt"]["node"], r["receipt"]["call_hash"])); n += 1
    added = 0
    with open(out, "a", encoding="utf-8") as f:
        for fn in files:
            for line in Path(fn).read_text(encoding="utf-8").splitlines():
                rc = json.loads(line); k = (rc["node"], rc["call_hash"])
                if k in seen or not rc.get("receipt_verified"): continue
                rec = {"seq": n, "prev": head, "receipt": rc}; rec["hash"] = sha(json.dumps(rec, sort_keys=True, separators=(",", ":")))
                f.write(json.dumps(rec, sort_keys=True) + "\n"); head = rec["hash"]; seen.add(k); n += 1; added += 1
    print(json.dumps({"merged_added": added, "total": n, "head": head}))

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("cmd"); ap.add_argument("--node"); ap.add_argument("--bind")
    ap.add_argument("--port", type=int, default=8765); ap.add_argument("--to"); ap.add_argument("--url"); ap.add_argument("--tool")
    ap.add_argument("--args", default="{}"); ap.add_argument("--nonce"); ap.add_argument("--out"); ap.add_argument("files", nargs="*")
    a = ap.parse_args()
    if a.cmd == "keygen": keygen(a.node)
    elif a.cmd == "serve": serve(a.node, a.bind, a.port)
    elif a.cmd == "call": call(a.node, a.url, a.tool, json.loads(a.args), a.to, a.nonce)
    elif a.cmd == "merge": merge(a.out, a.files)
