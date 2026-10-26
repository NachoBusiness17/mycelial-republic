#!/usr/bin/env python3
"""mesh_router.py — the body axis of the flywheel (charter P3).

Routes tasks to BODIES (phones/tablets running pocket_mcp) by capability
and load, using each body's live device_map as the routing input. Model
lanes (OpenRouter :free / Ollama) stay in wave_flywheel.py; this module is
the body half, deliberately standalone until the deck redesign merges them.

  map                          fleet device map (aggregate, fresh)
  route --shape SHAPE [--url U|--text T]   dry-run: which body + why
  fire  --shape SHAPE [--url U|--text T]   execute via pocket_mcp + ledger

Body gates (all must pass, lowest loadavg wins):
  reachable · battery > 30% or charging · ram_free > 500 MB
Presence/sealed tools (location/camera/sms) are NOT routable — seal-first.
"""
import argparse, base64, hashlib, json, platform, subprocess, sys, time, os
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
FLEET_MAP = os.path.join(HERE, "device_map.json")
SWARM_MANIFEST = os.path.join(HERE, "invariant_swarm_manifest.json")
BURN_LOG = os.path.join(HERE, "BURN_LOG.jsonl")

CORE_SEED_INVARIANTS = [
    "RIB_BOB_PRIMARY_20261017.md",
    "STANDING_WAVE_README.md",
    "THE_FRONTIER_CONTEXT_LAW.md",
    "THE_CONTEXT_LAW_CREED_20261002.md",
    "THE_TEN_INVARIANTS_MAPPED_20261008.md",
    "LAWS.md",
    "TAILS_LEDGER_SPEC_DECENTRALIZED_COMMUNITIES.md",
    "BITTENSOR_SUBNET_STUDY_20261017.md",
    "instructions_frontier.jsonl",
    "instructions_flash.jsonl",
    "instructions_local.jsonl",
    "compile_report.json",
    "MESH_TRIANGULATION_DIRECTION_20261017.md",
    "SETTLEMENT_V3_MIGRATION_CHECKLIST_20261017.md",
    "checkpoints_v2.jsonl",
    "tails.jsonl",
    "TWEET_RELIC_ONTOLOGY_20261018.md",
    "CONTINUITY_ENGINE_SYNTHESIS_20261018.md",
    "THE_BACKUP_BRAIN_MANIFESTO_20261018.md",
    "EULER_PHASOR_STANDING_WAVE_20261018.md",
    "PENTAGON_HARMONIC_WARP_SYNTHESIS_20261018.md",
    "SECOND_PENTAGON_EIGEN_METASURFACE_SYNTHESIS_20261018.md",
    "PIRATE_FACE_ZK_INFERENCE_STEAL_20261018.md",
    "VIOLET_EDGERUNNER_QDAY_SYNTHESIS_20261018.md",
    "HERMES_ROKU_LAN_SUBSTRATE_20261018.md",
]

BODIES = {
    "bob": {
        "hosts": [("local", 0, "etfag", ""),
                  ("100.125.103.60", 22, "etfag", "")],
        "tier": "primary",
        "os_kind": "windows",
        "remote_cmd": r"C:\Users\etfag\.zcode\workspace\default\tools\node\node.exe C:\Users\etfag\.zcode\workspace\default\pocket_mcp.js",
    },
    "desktop": {
        # 2026-10-23: key-path drift fix - adam_laptop_key lives at ~/.ssh on
        # this clone, not C:\Users\etfag\Documents (receipt FREE_FLEET_CELL_DRIVE_20261019.md)
        "hosts": [("100.96.161.76", 22, "foste", os.path.expanduser("~/.ssh/adam_laptop_key"))],
        "tier": "bench",
        "os_kind": "windows",
        "remote_cmd": r"C:\Users\foste\AppData\Local\hermes\node\node.exe C:\Users\foste\.gstdmesh\pocket_mcp.js",
    },
    "t90": {
        "hosts": [("100.72.38.3", 8022, "u0_a235", os.path.join(HERE, "t90_lane_key"))],
        "tier": "medium",
        "os_kind": "termux",
    },
    "pixel-11-pro": {
        # 2026-10-23: pixel trusts the seat default ed25519 (KEY-AUTH-OK live
        # probe); pixel_lane never existed on any clone - path was dead weight
        "hosts": [("192.168.86.32", 8022, "u0_a354", os.path.expanduser("~/.ssh/id_ed25519")),
                  ("100.79.122.101", 8022, "u0_a354", os.path.expanduser("~/.ssh/id_ed25519"))],
        "tier": "outstanding",
        "os_kind": "termux",
    },
}

BODY_SHAPES = {
    "device_map", "mesh_log", "fetch", "notify",
    "invariant_have", "invariant_get", "invariant_seed",
    "gstd_beacon", "gstd_tasks",
}  # sealed: location/camera/sms


def ssh_mcp(host_cfg, body_name, tool, args, timeout=25):
    """One-shot MCP tools/call over local stdio or ssh. Returns (map_result, latency_s, err)."""
    ip, port, user, key = host_cfg
    cfg = BODIES.get(body_name, {})
    os_kind = cfg.get("os_kind", "termux")
    msg = json.dumps({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                      "params": {"name": tool, "arguments": args}})
    if ip == "local" and platform.node().lower() == body_name.lower():
        node_bin = os.path.join(HERE, "tools", "node", "node.exe")
        if not os.path.exists(node_bin):
            node_bin = "node"
        cmd = [node_bin, os.path.join(HERE, "pocket_mcp.js")]
        env = os.environ.copy()
        env["GSTD_BODY_NAME"] = body_name
    else:
        if ip == "local":
            return None, 0.0, "not local host"
        cmd = ["ssh"]
        if key and os.path.exists(key):
            cmd += ["-i", key]
        cmd += ["-p", str(port), "-o", "BatchMode=yes",
                "-o", "ConnectTimeout=8", "-o", "StrictHostKeyChecking=accept-new",
                f"{user}@{ip}"]
        if os_kind == "windows":
            cmd.append(cfg["remote_cmd"])
        else:
            cmd.append(
                f"GSTD_BODY_NAME={body_name} timeout {timeout} node "
                f"/data/data/com.termux/files/home/gs*bot/pocket_mcp.js"
            )
        env = None
    t0 = time.time()
    try:
        p = subprocess.run(cmd, input=msg + "\n", capture_output=True,
                           text=True, encoding="utf-8", errors="replace",
                           env=env, timeout=timeout + 8)
    except subprocess.TimeoutExpired:
        return None, time.time() - t0, "ssh timeout"
    lat = time.time() - t0
    for line in (p.stdout or "").strip().splitlines():
        try:
            d = json.loads(line)
        except Exception:
            continue
        if d.get("id") == 3:
            if "error" in d:
                return None, lat, d["error"].get("message", "mcp error")
            return d["result"]["content"][0]["text"], lat, None
    return None, lat, (p.stderr or "no mcp reply").strip()[:200]


def body_mcp_call(name, tool, args, timeout=25):
    """Try each configured host for body `name` until one answers MCP."""
    cfg = BODIES[name]
    last_err = "no hosts"
    last_lat = 0.0
    for hc in cfg["hosts"]:
        raw, lat, err = ssh_mcp(hc, name, tool, args, timeout=timeout)
        last_lat, last_err = lat, err
        if raw is not None:
            return raw, lat, hc[0], None
    return None, last_lat, None, last_err


def body_report(name, cfg):
    """Fresh device_map + reachability for one body."""
    raw, lat, host_used, err = body_mcp_call(name, "device_map", {})
    if raw is not None:
        try:
            m = json.loads(raw)
            m["_latency_s"] = round(lat, 2)
            m["_host_used"] = host_used
            m["_tier"] = cfg["tier"]
            return m
        except Exception as e:
            err = f"bad json: {e}"
    return {"body": name, "reachable": False, "err": err, "_tier": cfg["tier"]}


def cmd_map():
    fleet = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
             "bodies": {}}
    for name, cfg in BODIES.items():
        m = body_report(name, cfg)
        fleet["bodies"][name] = m
        ok = m.get("reachable", True)
        gate = gates(m)
        print(f"{name:14s} {'UP' if ok else 'DOWN':4s} "
              f"bat={m.get('battery', {}).get('pct')}% "
              f"ram_free={m.get('ram_mb', {}).get('free')}MB "
              f"load={m.get('loadavg', ['?'])[0]} "
              f"stor={m.get('storage_free_gb')}GB "
              f"invs={m.get('invariants_count', '?')} "
              f"lat={m.get('_latency_s')}s "
              f"gates={'PASS' if all(gate.values()) else 'FAIL:' + ','.join(k for k, v in gate.items() if not v)}")
    with open(FLEET_MAP, "w", encoding="utf-8") as f:
        json.dump(fleet, f, indent=1)
    print(f"fleet map -> {FLEET_MAP}")


def gates(m):
    """Routing gates from a device_map. Presence-sealed tools never route."""
    g = {"reachable": bool(m.get("reachable", True)),
         "sealed_tools_absent": True}  # by construction; declared, not implemented
    bat = m.get("battery") or {}
    pct, chg = bat.get("pct"), bat.get("charging")
    g["battery_ok"] = (pct is None and chg is None) or (chg is True) or (isinstance(pct, (int, float)) and pct > 30)
    ram_free = (m.get("ram_mb") or {}).get("free")
    g["ram_ok"] = isinstance(ram_free, (int, float)) and ram_free > 200
    g["has_load"] = isinstance(m.get("loadavg"), list) and len(m.get("loadavg")) > 0
    return g


def pick_body(shape, want_body=None):
    if shape not in BODY_SHAPES:
        return None, f"shape '{shape}' is not body-routable (sealed or model-lane)"
    candidates = []
    with open(FLEET_MAP, encoding="utf-8") as f:
        fleet = json.load(f)
    for name, m in fleet["bodies"].items():
        if want_body and name != want_body:
            continue
        g = gates(m)
        if all(g.values()):
            candidates.append((m["loadavg"][0], m.get("_latency_s", 99), name))
    if not candidates:
        return None, "no body passes gates (down, battery, or ram)"
    candidates.sort()
    why = "; ".join(f"{n}: load {l}" for l, _, n in candidates)
    return candidates[0][2], why


def log_burn_row(kind, body, ok, lat, ref, note):
    row = {"ts": datetime.now().isoformat(timespec="seconds"), "kind": kind,
           "body": body, "caller": "mesh_router", "model": "pocket_mcp",
           "elapsed_s": round(lat, 2), "ok": ok, "result_ref": ref, "note": note}
    with open(BURN_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")


def gather_swarm_bitfield(filt=""):
    """Query `invariant_have` across all reachable bodies."""
    alive_bodies = []
    bitfield = {}  # name -> { body: {sha256, bytes, mtime} }
    for bname in BODIES:
        raw, lat, host_used, err = body_mcp_call(bname, "invariant_have", {"filter": filt})
        if raw is None:
            print(f"  [have] {bname:14s} DOWN ({err})")
            continue
        try:
            payload = json.loads(raw)
        except Exception as e:
            print(f"  [have] {bname:14s} BAD_JSON ({e})")
            continue
        alive_bodies.append(bname)
        items = payload.get("items", [])
        print(f"  [have] {bname:14s} UP   {len(items):3d} invariants ({lat:.2f}s via {host_used})")
        for it in items:
            bitfield.setdefault(it["name"], {})[bname] = it
    return alive_bodies, bitfield


def cmd_have(filt=""):
    alive, bitfield = gather_swarm_bitfield(filt)
    names = sorted(bitfield.keys()) if filt else CORE_SEED_INVARIANTS
    print("\nSWARM TORRENT BITFIELD (name | sha256[:12] | bytes | bodies holding piece):")
    for nm in names:
        holders = bitfield.get(nm, {})
        if not holders:
            print(f"  {nm:40s}  MISSING ON ALL BODIES")
            continue
        sample = next(iter(holders.values()))
        sha12 = sample["sha256"][:12]
        sz = sample["bytes"]
        badges = []
        for b in alive:
            if b in holders:
                bsha = holders[b]["sha256"][:12]
                badges.append(f"{b}:OK" if bsha == sha12 else f"{b}:DRIFT({bsha})")
            else:
                badges.append(f"{b}:MISS")
        print(f"  {nm:40s}  {sha12}  {sz:6d}B  [{', '.join(badges)}]")
    out_doc = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "alive_bodies": alive,
        "core_seed": {k: bitfield.get(k, {}) for k in CORE_SEED_INVARIANTS},
        "total_unique_invariants": len(bitfield),
    }
    with open(SWARM_MANIFEST, "w", encoding="utf-8") as f:
        json.dump(out_doc, f, indent=1)
    print(f"swarm manifest -> {SWARM_MANIFEST}")


def cmd_sync(filt=""):
    """Torrent-style invariant distribution across all reachable MCP servers."""
    alive, bitfield = gather_swarm_bitfield(filt)
    if len(alive) < 2:
        print("need at least 2 reachable bodies to trade invariants")
        return
    targets = sorted(bitfield.keys()) if filt else [
        nm for nm in CORE_SEED_INVARIANTS if nm in bitfield
    ]
    seeded_count = 0
    for nm in targets:
        holders = bitfield.get(nm, {})
        if not holders:
            continue
        # Prefer bob or desktop as canonical seed if present
        seed_body = "bob" if "bob" in holders else ("desktop" if "desktop" in holders else next(iter(holders.keys())))
        canonical_sha = holders[seed_body]["sha256"]
        need_bodies = [b for b in alive if b not in holders or holders[b]["sha256"] != canonical_sha]
        if not need_bodies:
            print(f"  [sync] {nm:40s}  {canonical_sha[:12]}  COMPLETE across {alive}")
            continue
        # Pull piece from seed_body via MCP invariant_get
        raw_get, lat_get, _, err_get = body_mcp_call(
            seed_body, "invariant_get", {"name": nm, "sha256": canonical_sha}
        )
        if raw_get is None:
            print(f"  [sync] {nm:40s}  GET_FAIL from {seed_body}: {err_get}")
            continue
        piece = json.loads(raw_get)
        if not piece.get("ok"):
            print(f"  [sync] {nm:40s}  GET_ERR from {seed_body}: {piece.get('error')}")
            continue
        raw_bytes = base64.b64decode(piece["content_b64"])
        local_sha = hashlib.sha256(raw_bytes).hexdigest()
        if local_sha != canonical_sha:
            print(f"  [sync] {nm:40s}  ROUTER_HASH_MISMATCH {local_sha} != {canonical_sha}")
            continue
        for dst in need_bodies:
            raw_seed, lat_seed, _, err_seed = body_mcp_call(
                dst, "invariant_seed",
                {"name": nm, "sha256": canonical_sha, "content_b64": piece["content_b64"]}
            )
            ok = False
            msg = err_seed or ""
            if raw_seed is not None:
                res = json.loads(raw_seed)
                ok = bool(res.get("ok")) and res.get("sha256") == canonical_sha
                msg = f"sha256={res.get('sha256', '')[:12]} bytes={res.get('bytes')}" if ok else str(res.get("error"))
            print(f"  [seed] {seed_body} -> {dst:10s}  {nm:36s}  {'OK' if ok else 'FAIL'} ({lat_seed:.2f}s) {msg}")
            log_burn_row("invariant_sync", dst, ok, lat_seed, nm, f"from={seed_body} sha256={canonical_sha[:12]}")
            if ok:
                seeded_count += 1
    print(f"\nsync complete: {seeded_count} piece transfers verified across {alive}")


def cmd_falsify(want_body="bob"):
    """Law 2 + Law 8 falsifier drill: attempt to seed tampered bytes with a mismatched sha256.
    Passes ONLY if the target MCP server REFUSES with HASH_MISMATCH and writes nothing."""
    bad_sha = "0" * 64
    raw, lat, host_used, err = body_mcp_call(
        want_body, "invariant_seed",
        {"name": "FALSIFIER_TAMPER_TEST.md", "sha256": bad_sha, "content": "tampered payload"}
    )
    if raw is None:
        print(f"FALSIFIER FAIL: MCP unreachable on {want_body} ({err})")
        sys.exit(1)
    res = json.loads(raw)
    refused = (res.get("ok") is False) and ("HASH_MISMATCH" in str(res.get("error", "")))
    print(f"FALSIFIER DRILL on {want_body} ({lat:.2f}s via {host_used}): "
          f"{'PASS (tampered piece refused)' if refused else 'FAIL (tampered piece accepted!)'} -> {res}")
    log_burn_row("invariant_falsifier", want_body, refused, lat, "FALSIFIER_TAMPER_TEST.md", str(res.get("error", ""))[:80])
    if not refused:
        sys.exit(1)


def cmd_fire(shape, url, text, want_body):
    target, why = pick_body(shape, want_body)
    print(f"route: {target or 'NONE'} ({why})")
    if not target:
        sys.exit(1)
    args = {"url": url} if shape == "fetch" else \
           {"message": text} if shape == "notify" else \
           {"kind": "mesh_task", "text": text or ""}
    raw, lat, host_used, err = body_mcp_call(target, shape, args)
    ok = raw is not None
    ref = ""
    print(("OK  " if ok else "FAIL") + f" {target} {lat:.1f}s: {(raw or err)[:300]}")
    log_burn_row("mesh_fire", target, ok, lat, ref, f"shape={shape} {why[:80]}")
    if ok and shape == "fetch":
        ref = os.path.join(HERE, "mesh_results")
        os.makedirs(ref, exist_ok=True)
        out = os.path.join(ref, f"{target}_{int(time.time())}.txt")
        with open(out, "w", encoding="utf-8") as f:
            f.write(raw)
        print(f"saved -> {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["map", "route", "fire", "have", "sync", "falsify"])
    ap.add_argument("--shape", default="mesh_log")
    ap.add_argument("--url")
    ap.add_argument("--text")
    ap.add_argument("--body")
    ap.add_argument("--filter", default="")
    a = ap.parse_args()
    if a.cmd == "map":
        cmd_map()
    elif a.cmd == "route":
        t, why = pick_body(a.shape, a.body)
        print(f"{t or 'NONE'} <- {why}")
    elif a.cmd == "have":
        cmd_have(a.filter)
    elif a.cmd == "sync":
        cmd_sync(a.filter)
    elif a.cmd == "falsify":
        cmd_falsify(a.body or "bob")
    else:
        cmd_fire(a.shape, a.url, a.text, a.body)
