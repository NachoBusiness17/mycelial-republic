# prior_art: tools/mag_relay/mag_relay.py, mag/dispatch.py -- mag_relay carries signed calls node-to-node but routes nothing; mag dispatch routes in-process lanes, not health-gated mesh jobs over the relay (its fleet probe gates are the self-steal, named below)
"""router.py (Bob, 2026-10-25): automatic job routing for the water-computer mesh over mag-relay.
Self-steal: mag_relay.py (envelope/sign/receipts/Ledger), hermes_fleet/fleet.py probe gates (RAM, battery, jobs),
lanes.json fire_verified idea. Rules are data: routing_rules.json. Bob never runs models.
  python router.py route --prompt "..." [--image file] [--browser] [--gpu] [--frontier] [--latency low]
  python router.py serve     # watch router/inbox/*.json -> router/outbox/; create router/STOP to stop
"""
import argparse, base64, json, os, secrets, sys, time, urllib.request
from pathlib import Path
HERE = Path(__file__).resolve().parent
os.environ.setdefault("MAG_RELAY_HOME", str(HERE.parent / "state"))
sys.path.insert(0, str(HERE.parent)); import mag_relay as m
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ME = "bob"
def rules(): return json.loads((HERE / "routing_rules.json").read_text(encoding="utf-8-sig"))
def ledger_append(rec): return m.Ledger(ME).append(dict(rec, kind="route"))

def rcall(to, ip, port, tool, args, timeout):
    env = {"from": ME, "to": to, "ts": time.time(), "nonce": secrets.token_hex(16), "head": m.Ledger(ME).head, "tool": tool, "args": args}
    env["sig"] = m.sign(m.load_seed(ME), m.canon(env)).hex()
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": tool, "arguments": {"mag_relay": env}}}).encode()
    r = json.loads(urllib.request.urlopen(urllib.request.Request(f"http://{ip}:{port}/mcp", body, {"Content-Type": "application/json"}), timeout=timeout).read())
    if "error" in r: raise RuntimeError("relay rejected")
    res = r["result"]; rc = res.get("receipt")
    if rc:
        sig = bytes.fromhex(rc.pop("sig")); pub = m.load_peers().get(to, {}).get("pub", "00")
        rc["receipt_verified"] = m.verify(bytes.fromhex(pub), m.DOMAIN + json.dumps(rc, sort_keys=True, separators=(",", ":")).encode(), sig); rc["sig"] = sig.hex()
        with open(m.HOME / f"receipts_{ME}.jsonl", "a", encoding="utf-8") as f: f.write(json.dumps(rc, sort_keys=True) + "\n")
    return res["structuredContent"], rc

def classify(job, R):
    c = R["classify"]; p = job.get("prompt", "").lower()
    toks = len(job.get("prompt", "")) // c["chars_per_token"]
    k = {"tokens": toks, "vision": bool(job.get("image_b64")), "browser": bool(job.get("browser")) or any(w in p for w in c["browser_keywords"]),
         "gpu": bool(job.get("gpu")), "frontier": bool(job.get("frontier")) or any(w in p for w in c["frontier_keywords"]),
         "latency": job.get("latency", "normal")}
    k["size"] = "large" if toks > c["small_max_tokens"] else "small"
    k["needs"] = "browser" if k["browser"] else "vision" if k["vision"] else "gpu" if k["gpu"] else "frontier" if k["frontier"] else k["size"]
    return k

def gate(name, n, h):
    if n.get("status") == "retired": return "retired"
    if n.get("never_route"): return "never_route"
    g = n.get("gate", {})
    if g.get("requires_paid_backup") and not g.get("paid_backup_present"): return "gate: no paid backup"
    if g.get("free_openrouter_429_locked"): return "gate: free OpenRouter 429-locked"
    if h is None: return "down (no health reply)"
    if not h.get("hermes"): return "no hermes"
    if h.get("jobs", 0) >= n.get("max_jobs", 1): return f"busy jobs={h.get('jobs')}"
    if n.get("min_free_mb") and (h.get("free_mb") or 0) < n["min_free_mb"]: return f"low RAM {h.get('free_mb')}MB"
    b = h.get("battery")
    if n.get("min_battery") and b is not None and b < n["min_battery"] and not (n.get("battery_ok_if_charging") and h.get("charging")):
        return f"battery {b}% not charging"
    return None

def pick(k, R, healths):
    cands, why = [], {}
    for name, n in R["nodes"].items():
        if k["needs"] not in n.get("accepts", []): why[name] = f"does not accept {k['needs']}"; continue
        g = gate(name, n, healths.get(name))
        if g: why[name] = g; continue
        h = healths[name]; score = n.get("priority", 50) + (h.get("free_mb") or 0) / 1000.0
        if k["latency"] == "low" and name == "pc": score += 5
        cands.append((score, name))
    if k["needs"] == "small":  # phones first for small jobs; pc is the backstop
        phones = [c for c in cands if c[1] != "pc"]
        if phones: cands = phones
    cands.sort(reverse=True)
    return (cands[0][1] if cands else None), why, [c[1] for c in cands]

def zai_for(name, h, R):
    z = R["lanes"]["zai"]
    if name in z["applies_to"] and h and any(e in h.get("key_env_names", []) for e in z["key_env_candidates"]): return z["hermes_provider"]
    return None

def stamp(node, prov, queued=False):
    if queued: return f"[QUEUED: {queued}]"
    f = prov.get("final") or prov
    s = f"[routed node={node} provider={f.get('provider')} host={f.get('base_url_host')} model={f.get('model')}"
    if prov.get("fallback"):
        chain = " -> ".join(f"{a['provider']}@{a['base_url_host']}:{a['model']}" for a in prov.get("attempts", []))
        s += f" | FALLBACK HAPPENED: {chain}"
        ev = [e for e in prov.get("events", []) if "404" in e or "429" in e or "refused" in e]
        if ev: s += f" | cause: {ev[0][:90]}"
    else:
        r = [e for e in prov.get("events", []) if "429" in e or "404" in e]
        if r: s += f" | no fallback, but {len(r)} upstream error(s) retried on same model: {r[0][:60]}"
    return s + "]"

def route(job):
    R = rules(); port = R["relay_port"]; jid = job.get("id") or secrets.token_hex(6); t0 = time.time()
    k = classify(job, R)
    healths = {}
    for name, n in R["nodes"].items():
        if n.get("never_route") or k["needs"] not in n.get("accepts", []): continue
        if n.get("gate", {}).get("requires_paid_backup") and not n["gate"].get("paid_backup_present"): continue
        try: healths[name], _ = rcall(name, n["ip"], n.get("port", port), "health", {}, 25)
        except Exception as e: healths[name] = None
    node, why, ranked = pick(k, R, healths)
    dec = {"job": jid, "class": k, "chosen": node, "ranked": ranked, "skipped": why,
           "health": {n: (None if h is None else {x: h.get(x) for x in ("free_mb", "battery", "charging", "jobs", "gpu")}) for n, h in healths.items()}}
    if node is None:
        q = HERE / "queue"; q.mkdir(exist_ok=True); (q / f"{jid}.json").write_text(json.dumps(job))
        msg = "browser job: PC is down, queued (never routed to Bob)" if k["needs"] == "browser" else f"no healthy node for {k['needs']}, queued"
        ledger_append(dict(dec, outcome="queued")); return {"job": jid, "reply": stamp(None, {}, msg), "decision": dec}
    n = R["nodes"][node]; rec = ledger_append(dict(dec, outcome="dispatch"))
    if k["needs"] == "vision":
        res, rc = rcall(node, n["ip"], n.get("port", port), "describe_image", {"image_b64": job["image_b64"], "prompt": job.get("prompt") or "Describe this image."}, 400)
        text, prov = res.get("text", res.get("error", "")), res.get("provenance", {})
    else:
        a = {"prompt": job["prompt"], "run": True, "timeout": int(job.get("timeout", 300))}
        z = zai_for(node, healths.get(node), R)
        if z: a["provider"] = z
        elif R.get("hermes_pin"): a["provider"], a["model"] = R["hermes_pin"]["provider"], R["hermes_pin"]["model"]
        sub, rc = rcall(node, n["ip"], n.get("port", port), "submit_task", a, a["timeout"] + 30)
        res = {}
        for _ in range(60):
            res, _r = rcall(node, n["ip"], n.get("port", port), "get_result", {"task_id": sub["task_id"]}, 30)
            if res.get("state") == "done": break
            time.sleep(5)
        text, prov = res.get("out", ""), res.get("provenance", {})
        if res.get("exit") not in (0, None): text = f"(hermes exit {res.get('exit')}) " + text
    st = stamp(node, prov)
    out = {"job": jid, "node": node, "reply": f"{st}\n{text.strip()}", "provenance": prov, "decision": dec, "secs": round(time.time() - t0, 1),
           "receipt": {"node": rc.get("node"), "seq": rc.get("seq"), "verified": rc.get("receipt_verified")} if rc else None}
    ledger_append({"job": jid, "outcome": "done", "node": node, "stamp": st, "fallback": prov.get("fallback"), "dispatch_hash": rec["hash"], "secs": out["secs"]})
    return out

def serve():
    inbox, outbox, stop = HERE / "inbox", HERE / "outbox", HERE / "STOP"
    inbox.mkdir(exist_ok=True); outbox.mkdir(exist_ok=True); (HERE / "router.pid").write_text(str(os.getpid()))
    print(time.strftime("%H:%M:%S"), "router serving inbox", inbox, flush=True)
    while not stop.exists():
        for f in sorted(inbox.glob("*.json")):
            try: job = json.loads(f.read_text(encoding="utf-8-sig")); f.unlink()
            except Exception: continue
            try: r = route(job)
            except Exception as e: r = {"job": job.get("id"), "reply": f"[router error {type(e).__name__}: {e}]"}
            (outbox / f"{r.get('job') or f.stem}.json").write_text(json.dumps(r, indent=1), encoding="utf-8")
            print(time.strftime("%H:%M:%S"), r.get("job"), r.get("reply", "")[:200].replace("\n", " "), flush=True)
        time.sleep(2)
    print(time.strftime("%H:%M:%S"), "STOP file seen, exiting", flush=True)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("cmd"); ap.add_argument("--prompt", default=""); ap.add_argument("--image")
    for f in ("browser", "gpu", "frontier"): ap.add_argument("--" + f, action="store_true")
    ap.add_argument("--latency", default="normal"); ap.add_argument("--id"); a = ap.parse_args()
    if a.cmd == "serve": serve()
    else:
        job = {"id": a.id, "prompt": a.prompt, "browser": a.browser, "gpu": a.gpu, "frontier": a.frontier, "latency": a.latency}
        if a.image: job["image_b64"] = base64.b64encode(Path(a.image).read_bytes()).decode()
        print(json.dumps(route(job), indent=1))
