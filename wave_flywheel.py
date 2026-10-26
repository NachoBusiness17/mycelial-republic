#!/usr/bin/env python
"""wave_flywheel - the WAV protocol as a standing free-tier flywheel (2026-10-11)

Nous portal doctrine, restored: free-tier agent rotations only (:free models),
fired as concurrent Mickey17 instances - every instance expendable, the run ID
is the reprint series. Waves inherit the overnight-wave anatomy:
waves/flywheel/WAVE_<ts>/ = prompt.txt + results + WAVE_FOLD.md.

Lanes: OpenRouter :free models (backbone), Groq (retested), DeepSeek direct
(CONTROL lane - near-free, tagged, never counted as $0). The hermes portal's
metered models are BANNED here by law ($11.40/$22 cap lesson).

Usage:
  python wave_flywheel.py probe                       # alive-check all lanes
  python wave_flywheel.py discover [--max N]          # refresh :free rotation from OpenRouter
  python wave_flywheel.py fire --task "one question"  # 1 instance per free lane
  python wave_flywheel.py fire --in prompt.txt --instances 2
  python wave_flywheel.py fold                        # fold the latest wave
"""
import argparse, concurrent.futures, json, os, sys, time, urllib.request, urllib.error
from datetime import datetime

try:
    from tools.sovereign.http_client import clean_reasoning_bleed
except Exception:
    def clean_reasoning_bleed(x): return x

WS = os.path.dirname(os.path.abspath(__file__))
ROTATION = os.path.join(WS, "waves", "flywheel", "rotation.json")
COOLDOWN = os.path.join(WS, "waves", "flywheel", "lane_cooldown.json")
COOLDOWN_SECONDS = 600  # lanes that 429'd sit out this long


def load_cooldown():
    try:
        with open(COOLDOWN, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def note_cooldown(lane_name, is_429):
    """Record a 429 so the next wave (15 min cadence) skips the lane while hot."""
    if not is_429:
        return
    cd = load_cooldown()
    cd[lane_name] = datetime.now().isoformat(timespec="seconds")
    try:
        with open(COOLDOWN, "w", encoding="utf-8") as f:
            json.dump(cd, f, indent=1)
    except OSError:
        pass


def is_cooling(lane_name):
    cd = load_cooldown()
    ts = cd.get(lane_name)
    if not ts:
        return False
    try:
        age = (datetime.now() - datetime.fromisoformat(ts)).total_seconds()
        if age > COOLDOWN_SECONDS:
            return False
        return True
    except ValueError:
        return False
LANES = {
    "or-nemotron":  {"provider": "openrouter", "model": "nvidia/nemotron-3-ultra-550b-a55b:free", "key_env": "OPENROUTER_API_KEY", "free": True},
    "or-laguna":    {"provider": "openrouter", "model": "poolside/laguna-s-2.1:free",             "key_env": "OPENROUTER_API_KEY", "free": True},
    "or-longcat":   {"provider": "openrouter", "model": "meituan/longcat-2.0:free",               "key_env": "OPENROUTER_API_KEY", "free": True},
    "groq-oss120":  {"provider": "groq",      "model": "llama-3.3-70b-versatile",                 "key_env": "GROQ_API_KEY",       "free": True},
    "ds-control":   {"provider": "deepseek",  "model": "deepseek-chat",                           "key_env": "DEEPSEEK_API_KEY",   "free": False},
}
URLS = {
    "openrouter": "https://openrouter.ai/api/v1/chat/completions",
    "groq":       "https://api.groq.com/openai/v1/chat/completions",
    "deepseek":   "https://api.deepseek.com/chat/completions",
}


def discover(max_n=8):
    """Refresh the :free rotation from OpenRouter's live model list. The free
    tier churns (longcat 404'd, laguna 429s) - the rotation is whatever exists
    TODAY, not hardcoded ids."""
    os.makedirs(os.path.dirname(ROTATION), exist_ok=True)
    with urllib.request.urlopen("https://openrouter.ai/api/v1/models", timeout=30) as r:
        data = json.loads(r.read())
    free = [m for m in data.get("data", []) if m.get("id", "").endswith(":free")]
    free.sort(key=lambda m: m.get("context_length") or 0, reverse=True)
    picked = [m["id"] for m in free[:max_n]]
    rot = {"ts": datetime.now().isoformat(timespec="seconds"), "free_models_found": len(free),
           "rotation": picked}
    with open(ROTATION, "w", encoding="utf-8") as f:
        json.dump(rot, f, indent=1)
    print(f"DISCOVER: {len(free)} :free models on OpenRouter; rotation ({len(picked)}):")
    for m in picked:
        print(f"  {m}")
    return picked


def load_rotation():
    """Rotation lanes replace/augment the hardcoded openrouter free lanes."""
    if not os.path.exists(ROTATION):
        return dict(LANES)
    with open(ROTATION, encoding="utf-8") as f:
        rot = json.load(f)
    lanes = {n: l for n, l in LANES.items() if l["provider"] != "openrouter"}
    for i, mid in enumerate(rot.get("rotation", [])):
        lanes[f"or{i}"] = {"provider": "openrouter", "model": mid,
                           "key_env": "OPENROUTER_API_KEY", "free": True}
    return lanes


def load_keys():
    keys = {}
    try:
        with open(os.path.join(WS, ".env"), encoding="utf-8-sig") as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    keys[k.strip()] = v.strip()
    except OSError:
        pass
    return keys


def call(lane_name, prompt, key, max_tokens, timeout=120, lanes=None):
    """One call. Returns dict(lane, model, text, elapsed_s, error, usage, ok)."""
    lanes = lanes or LANES
    lane = lanes[lane_name]
    body = json.dumps({
        "model": lane["model"], "max_tokens": max_tokens, "temperature": 0.6,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")
    req = urllib.request.Request(URLS[lane["provider"]], data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {key}")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
        elapsed = round(time.time() - t0, 1)
        raw_text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        text = clean_reasoning_bleed(raw_text)
        usage = data.get("usage") or {}
        err = None if text.strip() else "empty response"
        return {"lane": lane_name, "model": lane["model"], "text": text,
                "elapsed_s": elapsed, "error": err, "usage": usage, "ok": bool(text.strip())}
    except urllib.error.HTTPError as e:
        note_cooldown(lane_name, e.code == 429)
        return {"lane": lane_name, "model": lane["model"], "text": "",
                "elapsed_s": round(time.time() - t0, 1),
                "error": f"HTTP {e.code}", "usage": {}, "ok": False}
    except Exception as e:
        return {"lane": lane_name, "model": lane["model"], "text": "",
                "elapsed_s": round(time.time() - t0, 1),
                "error": str(e)[:120], "usage": {}, "ok": False}


def probe(keys, lanes):
    print("FLYWHEEL PROBE (concurrent, 16-token pings):")
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(lanes)) as ex:
        futs = {ex.submit(call, name, "Reply with the single word: alive", keys.get(l["key_env"], ""), 16, 30, lanes): name
                for name, l in lanes.items()}
        alive = []
        for f in concurrent.futures.as_completed(futs):
            r = f.result()
            tag = "ALIVE" if r["ok"] else f"DEAD ({r['error']})"
            free = "free" if lanes[r["lane"]]["free"] else "CONTROL"
            print(f"  {r['lane']:14s} {lanes[r['lane']]['model']:44s} {free:8s} {tag:22s} {r['elapsed_s']}s")
            if r["ok"]:
                alive.append(r["lane"])
    print(f"  -> {len(alive)} alive: {', '.join(alive)}")
    return alive


PROFILE_DIR = os.path.join(WS, "model_profiles")


def provider_profile_text(provider):
    """Behavioral layer: per-provider profile (quirks, floors, cache law)
    attached to every instance of that provider. No interaction fires naked."""
    p = os.path.join(PROFILE_DIR, provider + ".md")
    if os.path.exists(p):
        with open(p, encoding="utf-8-sig") as f:
            return f.read().strip() + "\n\nTASK:\n"
    return ""


def fire(keys, prompt, instances, only_free=True, out_dir=None, lanes=None, rib=None):
    """Fire a wave. rib = path to a RIB file; its text boots every instance
    (prompt = RIB + task), so Mickeys wake ractored instead of naked."""
    if rib:
        with open(rib, encoding="utf-8-sig") as f:
            prompt = f.read().strip() + "\n\nTASK:\n" + prompt
    lanes = lanes or LANES
    lanes_sel = [n for n, l in lanes.items()
                 if (l["free"] or not only_free) and not is_cooling(n)]
    skipped = [n for n, l in lanes.items()
               if (l["free"] or not only_free) and is_cooling(n)]
    if skipped:
        print(f"  (cooldown skip: {', '.join(skipped)})")
    jobs = [(ln, i) for ln in lanes_sel for i in range(1, instances + 1)]
    wave_id = f"WAVE_{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    out_dir = out_dir or os.path.join(WS, "waves", "flywheel", wave_id)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "prompt.txt"), "w", encoding="utf-8") as f:
        f.write(prompt)
    print(f"FLYWHEEL {wave_id}: {len(jobs)} instances across {len(lanes)} lanes...")

    def run_one(job):
        ln, inst = job
        inst_prompt = provider_profile_text(lanes[ln]["provider"]) + prompt
        r = call(ln, inst_prompt, keys.get(lanes[ln]["key_env"], ""), 2000, lanes=lanes)
        r["instance"] = inst
        r["mickey_id"] = f"{ln}-{inst}"
        if r["ok"]:
            with open(os.path.join(out_dir, f"{r['mickey_id']}.md"), "w", encoding="utf-8") as f:
                f.write(f"# {r['mickey_id']} — {lanes[ln]['model']}\n\n{r['text']}\n")
        try:
            from burn_ledger import log_burn
            log_burn(kind="burn", body="bob", caller="wave_flywheel",
                     model=r["model"], elapsed_s=r["elapsed_s"],
                     out_bytes=len(r["text"].encode("utf-8")), ok=r["ok"],
                     result_ref=os.path.relpath(os.path.join(out_dir, r["mickey_id"] + ".md"), WS) if r["ok"] else "",
                     tokens_in=r["usage"].get("prompt_tokens"),
                     tokens_out=r["usage"].get("completion_tokens"),
                     note=f"flywheel {wave_id} mickey {r['mickey_id']}" +
                          ("" if lanes[ln]["free"] else " [CONTROL LANE, near-free]"))
        except Exception:
            pass
        return r

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(jobs)) as ex:
        for r in ex.map(run_one, jobs):
            tag = f"ok {r['elapsed_s']}s" if r["ok"] else f"FAIL {r['error']}"
            tok = f" {r['usage'].get('prompt_tokens')}/{r['usage'].get('completion_tokens')}tok" if r["usage"] else ""
            print(f"  [{r['mickey_id']:16s}] {tag:24s}{tok}")
            results.append(r)

    ok = [r for r in results if r["ok"]]
    with open(os.path.join(out_dir, "WAVE_FOLD.md"), "w", encoding="utf-8") as f:
        f.write(f"# {wave_id} fold\n\nfired {len(results)}, landed {len(ok)}\n\n")
        for r in sorted(ok, key=lambda x: x["elapsed_s"]):
            head = r["text"][:160].replace("\n", " ")
            f.write(f"- {r['mickey_id']} ({r['elapsed_s']}s): {head}...\n")
    print(f"  -> fold written: {os.path.join(out_dir, 'WAVE_FOLD.md')}")
    return results


def fold_latest():
    base = os.path.join(WS, "waves", "flywheel")
    waves = sorted(d for d in os.listdir(base) if d.startswith("WAVE_")) if os.path.isdir(base) else []
    if not waves:
        print("no waves yet")
        return
    p = os.path.join(base, waves[-1], "WAVE_FOLD.md")
    print(open(p, encoding="utf-8").read() if os.path.exists(p) else f"no fold in {waves[-1]}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("probe")
    dp = sub.add_parser("discover")
    dp.add_argument("--max", type=int, default=8)
    fp = sub.add_parser("fire")
    fp.add_argument("--task")
    fp.add_argument("--in", dest="in_file")
    fp.add_argument("--instances", type=int, default=1)
    fp.add_argument("--rib", help="boot every instance from this RIB file")
    fp.add_argument("--all-lanes", action="store_true", help="include the CONTROL lane")
    sub.add_parser("fold")
    a = ap.parse_args()
    keys = load_keys()
    if a.cmd == "discover":
        discover(a.max)
    elif a.cmd == "probe":
        probe(keys, load_rotation())
    elif a.cmd == "fold":
        fold_latest()
    else:
        prompt = open(a.in_file, encoding="utf-8-sig").read() if a.in_file else a.task
        fire(keys, prompt, a.instances, only_free=not a.all_lanes,
             lanes=load_rotation(), rib=a.rib)
