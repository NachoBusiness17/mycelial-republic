import json, re, pathlib
R = pathlib.Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
def rd(p): return (R/p).read_text(encoding="utf-8")
def wr(p, s): (R/p).write_text(s, encoding="utf-8", newline="")
def sub1(p, old, new):
    s = rd(p); assert s.count(old) == 1, (p, old[:60], s.count(old)); wr(p, s.replace(old, new))

# 1. lease resource
cfgp = R/"configs/restricted_leases.json"
doc = json.loads(cfgp.read_text(encoding="utf-8"))
doc["resources"]["expose:lan"] = {
  "description": "FISH_TANK_REMEDIATE_20261019: any LAN-wide (0.0.0.0) Mag listener for untrusted display peers (Roku/phones): gstd_beacon serve with GSTD_BEACON_LAN=1, main.py cast --lan. No live lease = loopback only; listeners shut themselves down at expiry (mag.cast_guard.lan_lease_watchdog) and platform_kill --lan-expired reaps stragglers.",
  "paths": [], "enforce": "conflict", "default_ttl_s": 3600, "max_ttl_s": 14400}
cfgp.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

# 2. cast_guard additions
s = rd("mag/cast_guard.py")
s += '''

# ---------------------------------------------------------------------------
# FISH_TANK_REMEDIATE_20261019 - untrusted LAN peer law (watch/LIBRARY/STEAL_FISH_TANK_IOT_20261019.md)
# Any non-tailnet, non-loopback device (Roku, phone on Wi-Fi, IoT) is an UNTRUSTED PEER: it may
# READ display/beacon routes only. Deny by default, probe-log, NOTICE on first sight. Reuses the
# cast_probes.jsonl log above; leases via mag.leases resource "expose:lan".
# ---------------------------------------------------------------------------
import threading

LAN_LEASE = "expose:lan"
LAN_PEERS_PATH = ROOT / "memory" / "security" / "lan_peers.json"
TAILNET_V4 = ipaddress.ip_network("100.64.0.0/10")
TAILNET_V6 = ipaddress.ip_network("fd7a:115c:a1e0::/48")
DISPLAY_ROUTES = ("/", "/beacon", "/beacon.json", "/health", "/display", "/cast")
# host ports an untrusted LAN peer must never reach (Ollama, sshd, dashboard portproxy, gstd-node)
NON_DISPLAY_PORTS = (11434, 22, 8765, 8080)


def peer_class(ip: str) -> str:
    """loopback | tailnet | lan_untrusted | public."""
    try:
        a = ipaddress.ip_address((ip or "").split("%")[0])
    except ValueError:
        return "public"
    if a.is_loopback:
        return "loopback"
    if (a.version == 4 and a in TAILNET_V4) or (a.version == 6 and a in TAILNET_V6):
        return "tailnet"
    if a.is_private or a.is_link_local:
        return "lan_untrusted"
    return "public"


def _notice_new_peer(ip: str, path: str, service: str) -> bool:
    """NOTICE row (cast_probes.jsonl, reason=new_lan_peer) the first time an untrusted LAN ip shows."""
    try:
        seen = json.loads(LAN_PEERS_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        seen = {}
    if ip in seen:
        return False
    seen[ip] = {"first_seen": _now(), "service": service, "path": path}
    LAN_PEERS_PATH.parent.mkdir(parents=True, exist_ok=True)
    LAN_PEERS_PATH.write_text(json.dumps(seen, indent=2), encoding="utf-8")
    _log_probe(ip, path, f"notice:new_lan_peer:{service}")
    return True


def display_gate(ip: str, path: str, *, service: str = "display") -> dict[str, Any]:
    """Read-only gate for display/beacon servers. Untrusted peers: display routes only, GET only."""
    cls = peer_class(ip)
    if cls in ("loopback", "tailnet"):
        return {"ok": True, "peer": cls}
    if cls == "public":
        _log_probe(ip, path, f"non_lan:{service}")
        return {"ok": False, "deny": "non_lan", "peer": cls}
    if blocked(ip):
        return {"ok": False, "deny": "blocked", "peer": cls}
    _notice_new_peer(ip, path, service)
    route = (path or "/").split("?", 1)[0]
    if route not in DISPLAY_ROUTES:
        _log_probe(ip, path, f"notice:non_display_route:{service}")
        _register_fail(ip)
        return {"ok": False, "deny": "display_only", "peer": cls}
    return {"ok": True, "peer": cls, "read_only": True}


def lan_lease_live() -> bool:
    try:
        from mag import leases
        return bool((leases.status(resource=LAN_LEASE).get("lease") or {}).get("live"))
    except Exception:
        return False


def is_wildcard(host: str) -> bool:
    return host in ("0.0.0.0", "::", "")


def lan_lease_watchdog(on_expire, *, interval_s: float = 30.0, service: str = "lan") -> threading.Thread:
    """Daemon thread: calls on_expire() once the expose:lan lease is no longer live."""
    def _loop() -> None:
        while True:
            time.sleep(interval_s)
            if not lan_lease_live():
                _log_probe("self", service, "notice:lan_lease_expired_shutdown")
                try:
                    on_expire()
                finally:
                    return
    t = threading.Thread(target=_loop, name=f"lan-lease-{service}", daemon=True)
    t.start()
    return t
'''
wr("mag/cast_guard.py", s)

# 3. beacon
p = "tools/gstd_beacon.py"
sub1(p, 'SERVE_HOST = os.environ.get("GSTD_BEACON_HOST", "0.0.0.0")  # all interfaces: tailnet + LAN (the Roku reads the LAN side)',
 '# FISH_TANK_REMEDIATE_20261019: loopback by default. LAN (Roku) exposure = GSTD_BEACON_LAN=1 AND a live\n'
 '# mag.leases "expose:lan" lease; the server stops itself when the lease ends (cast_guard.lan_lease_watchdog).\n'
 'SERVE_HOST = "0.0.0.0" if os.environ.get("GSTD_BEACON_LAN") == "1" else os.environ.get("GSTD_BEACON_HOST", "127.0.0.1")')
sub1(p, '''        def do_GET(self) -> None:
            if self.path in''', '''        def do_GET(self) -> None:
            from mag import cast_guard
            if not cast_guard.display_gate(self.client_address[0], self.path, service="beacon")["ok"]:
                self.send_response(403)
                self.end_headers()
                return
            if self.path in''')
sub1(p, '''    print(f"serving the beacon on {SERVE_HOST}:{SERVE_PORT} (tailnet only) - ctrl-c to stop")
    ThreadingHTTPServer((SERVE_HOST, SERVE_PORT), Handler).serve_forever()''',
'''    from mag import cast_guard
    if cast_guard.is_wildcard(SERVE_HOST) and not cast_guard.lan_lease_live():
        print("refused: LAN beacon needs a live 'expose:lan' lease (python scripts/lease.py acquire ...)")
        return 2
    httpd = ThreadingHTTPServer((SERVE_HOST, SERVE_PORT), Handler)
    if cast_guard.is_wildcard(SERVE_HOST):
        cast_guard.lan_lease_watchdog(httpd.shutdown, service="beacon")
    print(f"serving the beacon on {SERVE_HOST}:{SERVE_PORT} - ctrl-c to stop")
    httpd.serve_forever()''')
s = rd(p)
if "sys.path.insert" not in s:
    s = s.replace("\nSERVE_HOST", "\nimport sys as _sys\n_sys.path.insert(0, str(Path(__file__).resolve().parents[1]))\nSERVE_HOST", 1)
    wr(p, s)

# 4. cast_server
p = "mag/cast_server.py"
sub1(p, "DEFAULT_PORT = 8766", "DEFAULT_PORT = 8766\n# C (FISH_TANK_REMEDIATE_20261019): host 127.0.0.1:8766 is OWNED by compose mag-mcp. Loopback cast\n# keeps 8766 for back-compat only when mag-mcp is down; --lan cast moves to LAN_PORT.\nLAN_PORT = 8767")
sub1(p, '''    httpd = ThreadingHTTPServer((host, port), Handler)
    print_bind_banner''', '''    from mag import cast_guard
    if cast_guard.is_wildcard(host) and not cast_guard.lan_lease_live():
        raise SystemExit("refused: cast --lan needs a live 'expose:lan' lease (python scripts/lease.py acquire ...)")
    httpd = ThreadingHTTPServer((host, port), Handler)
    if cast_guard.is_wildcard(host):
        cast_guard.lan_lease_watchdog(httpd.shutdown, service="cast")
    print_bind_banner''')

# 5. main.py cast --lan port
p = "main.py"
sub1(p, '''        run_cast(host=host, port=args.port)''', '''        port = args.port
        if bool(getattr(args, "lan", False)) and port == 8766:
            from mag.cast_server import LAN_PORT
            port = LAN_PORT  # 8766 belongs to compose mag-mcp (FISH_TANK_REMEDIATE_20261019 C)
        run_cast(host=host, port=port)''')

# 6. platform_kill
p = "mag/platform_kill.py"
sub1(p, '''def kill_all(*, dry: bool = False) -> dict[str, Any]:''', '''LAN_EXPOSE_MARKERS = ("gstd_beacon.py serve", "main.py cast --lan", "--cast-lan")


def kill_lan_expired(*, dry: bool = False, force: bool = False) -> dict[str, Any]:
    """Stop LAN-exposing processes (beacon serve, cast --lan) when the expose:lan lease is not live."""
    import os
    import subprocess
    try:
        from mag.cast_guard import lan_lease_live
        live = lan_lease_live()
    except Exception:
        live = False
    hits: list[dict[str, Any]] = []
    if live and not force:
        return {"ok": True, "lease_live": True, "killed": hits}
    try:
        import psutil  # type: ignore
        for proc in psutil.process_iter(["pid", "name", "cmdline"]):
            cmd = " ".join(proc.info.get("cmdline") or [])
            if any(m in cmd for m in LAN_EXPOSE_MARKERS) and "platform_kill" not in cmd:
                hits.append({"pid": proc.info["pid"], "cmd": cmd[:200], "dry": dry})
    except ImportError:
        pass
    for h in hits:
        if dry:
            continue
        try:
            if os.name == "nt":
                subprocess.run(["taskkill", "/PID", str(h["pid"]), "/T", "/F"], capture_output=True, timeout=30)
            else:
                import signal
                os.kill(h["pid"], signal.SIGKILL)
        except Exception as e:
            h["error"] = str(e)[:100]
    return {"ok": True, "lease_live": live, "killed": hits}


def kill_all(*, dry: bool = False) -> dict[str, Any]:''')
sub1(p, '''    dry = "--dry" in argv
''', '''    dry = "--dry" in argv
    if "--lan-expired" in argv:
        print(json.dumps(kill_lan_expired(dry=dry), indent=2, default=str))
        return 0
''')
sub1(p, '''    return {
        "schema": SCHEMA, "ts": _now(), "ok": not errors, "dry": dry,''', '''    lan = kill_lan_expired(dry=dry, force=True)
    return {
        "schema": SCHEMA, "ts": _now(), "ok": not errors, "dry": dry, "lan_exposure": lan,''')
print("patched")
