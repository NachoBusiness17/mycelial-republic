# prior_art: mag/browser_driver.py, tools/mag_relay/mag_relay.py -- browser_driver drives the local seat's browser, not signed relay tools over a tailnet CDP endpoint; mag_relay is the signed envelope this module extends via register()
"""browser_tools: Steel-backed browser tools for mag-relay (2026-10-25).

Separate module so mag_relay.py is not edited (an auto-router job owns that file).
Registration hook lives HERE, not in mag_relay.py: `register(m)` extends m.ALLOWED_TOOLS and
wraps m.tool_impl at runtime. Launch with:
  python browser_tools.py serve --node pc --bind 100.96.161.76 --port 8767 [--home DIR]
Tools: browser_open, browser_act, browser_snapshot, session_handoff.
Security: calls go through mag_relay's signed envelope, whois/IP pin, per-peer allow list
(phones get these tools only if their peers.json `allow` names them), replay cache and ledger.
This module also keeps an append-only hash-linked log HOME/browser_log.jsonl. Snapshot text is
stored content-addressed at HOME/snapshots/<sha256>.txt; cookies are recorded only as
sha256(value), never plaintext. Steel is reached only on the Tailscale IP.
"""
from __future__ import annotations
import hashlib, json, os, sys, time, urllib.request
from pathlib import Path

STEEL = os.environ.get("MAG_STEEL_URL", "http://100.96.161.76:3000")
TOOLS = ["browser_open", "browser_act", "browser_snapshot", "session_handoff"]
_state = {"session": None}
HOME = None  # set by register()

def _h(b): return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()

def _log(rec):
    p = HOME / "browser_log.jsonl"; prev = "0" * 64; n = 0
    if p.exists():
        lines = p.read_text(encoding="utf-8").splitlines(); n = len(lines)
        if lines: prev = json.loads(lines[-1])["hash"]
    rec = dict(rec, seq=n, prev=prev, t=time.time())
    rec["hash"] = _h(json.dumps(rec, sort_keys=True, separators=(",", ":")))
    with open(p, "a", encoding="utf-8") as f: f.write(json.dumps(rec, sort_keys=True) + "\n")
    return rec["hash"]

def _http(path, body=None, method=None):
    data = None if body is None else json.dumps(body).encode()
    r = urllib.request.Request(STEEL + path, data, {"Content-Type": "application/json"}, method=method or ("POST" if data else "GET"))
    return json.loads(urllib.request.urlopen(r, timeout=60).read() or b"{}")

def _session():
    s = _state["session"]
    if s:
        try:
            if _http(f"/v1/sessions/{s['id']}").get("status") == "live": return s
        except Exception: _state["session"] = None
    _state["session"] = _http("/v1/sessions", {})
    return _state["session"]

class CDP:
    def __init__(self, ws):
        from websockets.sync.client import connect
        self.c = connect(ws, max_size=50_000_000, open_timeout=30); self.i = 0
        t = [x for x in self.cmd("Target.getTargets")["targetInfos"] if x["type"] == "page"]
        tid = t[0]["targetId"] if t else self.cmd("Target.createTarget", url="about:blank")["targetId"]
        self.sid = self.cmd("Target.attachToTarget", targetId=tid, flatten=True)["sessionId"]
    def cmd(self, method, sid=None, **params):
        self.i += 1; m = {"id": self.i, "method": method, "params": params}
        if sid: m["sessionId"] = sid
        self.c.send(json.dumps(m))
        while True:
            r = json.loads(self.c.recv(timeout=60))
            if r.get("id") == self.i:
                if "error" in r: raise RuntimeError(r["error"].get("message", "cdp error"))
                return r.get("result", {})
    def page(self, method, **p): return self.cmd(method, sid=self.sid, **p)
    def js(self, expr): return self.page("Runtime.evaluate", expression=expr, returnByValue=True, awaitPromise=True).get("result", {}).get("value")
    def close(self): self.c.close()

def _cdp(): return CDP(_session()["websocketUrl"])

def _settle(c, secs=15):
    end = time.time() + secs
    while time.time() < end and c.js("document.readyState") != "complete": time.sleep(0.3)

def browser_open(a):
    url = str(a.get("url", ""))
    if not url.startswith(("http://", "https://")): return {"error": "url must be http(s)"}
    c = _cdp()
    try:
        c.page("Page.navigate", url=url); time.sleep(0.5); _settle(c)
        out = {"session_id": _state["session"]["id"], "url": c.js("location.href"), "title": c.js("document.title")}
    finally: c.close()
    return out

def browser_snapshot(a):
    c = _cdp()
    try:
        _settle(c, 5)
        text = c.js("document.body ? document.body.innerText : ''") or ""
        html_sha = _h(c.js("document.documentElement.outerHTML") or "")
        url, title = c.js("location.href"), c.js("document.title")
        cookies = c.cmd("Storage.getCookies").get("cookies", [])
    finally: c.close()
    d = HOME / "snapshots"; d.mkdir(exist_ok=True); sh = _h(text)
    (d / f"{sh}.txt").write_text(text, encoding="utf-8")
    ck = [{"name_sha": _h(k["name"]), "domain": k.get("domain"), "value_sha": _h(k.get("value", ""))} for k in cookies]
    return {"url": url, "title": title, "text_sha256": sh, "html_sha256": html_sha, "chars": len(text),
            "excerpt": text[: int(a.get("max_chars", 600))], "cookies": ck}

def browser_act(a):
    act = a.get("action"); sel = json.dumps(str(a.get("selector", ""))); txt = json.dumps(str(a.get("text", "")))
    c = _cdp()
    try:
        if act == "click": r = c.js(f"(()=>{{const e=document.querySelector({sel}); if(!e) return 'not found'; e.click(); return 'ok'}})()")
        elif act == "type": r = c.js(f"(()=>{{const e=document.querySelector({sel}); if(!e) return 'not found'; e.focus(); e.value={txt}; e.dispatchEvent(new Event('input',{{bubbles:true}})); return 'ok'}})()")
        elif act == "press":
            k = str(a.get("key", "Enter"))
            for t in ("keyDown", "keyUp"): c.page("Input.dispatchKeyEvent", type=t, key=k, code=k, windowsVirtualKeyCode=13 if k == "Enter" else 0)
            r = "ok"
        elif act == "scroll": r = c.js(f"(window.scrollBy(0,{int(a.get('dy', 600))}),'ok')")
        else: return {"error": "action must be click|type|press|scroll"}
        time.sleep(0.5); _settle(c, 10)
        out = {"action": act, "result": r, "url": c.js("location.href"), "title": c.js("document.title")}
    finally: c.close()
    return out

def session_handoff(a):
    s = _session(); v = s.get("sessionViewerUrl") or STEEL + "/"
    host = v.split("//", 1)[-1].split(":")[0].split("/")[0]
    if not host.startswith("100."): return {"error": "viewer not on tailnet; refusing"}
    return {"session_id": s["id"], "viewer_url": v, "debug_url": s.get("debugUrl"), "tailnet_only": True,
            "note": "open on a device signed into the tailnet; agent should stop acting until handed back"}

IMPL = {"browser_open": browser_open, "browser_act": browser_act, "browser_snapshot": browser_snapshot, "session_handoff": session_handoff}

def register(m):
    """Hook: extend mag_relay's allowlist and wrap its tool_impl. No edits to mag_relay.py."""
    global HOME; HOME = Path(m.HOME); HOME.mkdir(parents=True, exist_ok=True)
    for t in TOOLS:
        if t not in m.ALLOWED_TOOLS: m.ALLOWED_TOOLS.append(t)
    base = m.tool_impl
    def tool_impl(node, ledger, name, args):
        if name not in IMPL: return base(node, ledger, name, args)
        args = args or {}
        try: res = IMPL[name](args)
        except Exception as e: res = {"error": type(e).__name__}
        _log({"tool": name, "args_sha": _h(json.dumps(args, sort_keys=True)), "result_sha": _h(json.dumps(res, sort_keys=True)),
              "snapshot_sha": res.get("text_sha256"), "ok": "error" not in res})
        return res
    m.tool_impl = tool_impl

if __name__ == "__main__":
    import argparse
    sys.path.insert(0, str(Path(__file__).parent)); import mag_relay as m
    ap = argparse.ArgumentParser(); ap.add_argument("cmd"); ap.add_argument("--node", default="pc")
    ap.add_argument("--bind", default="100.96.161.76"); ap.add_argument("--port", type=int, default=8767); ap.add_argument("--home")
    a = ap.parse_args()
    if a.home:  # separate ledger/peers dir; signing key still read in-process from the node's own key dir, never printed
        kh = Path(m.HOME); m.key_path = lambda node: kh / f"{node}.seed"; m.HOME = Path(a.home)
    register(m)
    if a.cmd == "serve": m.serve(a.node, a.bind, a.port)
