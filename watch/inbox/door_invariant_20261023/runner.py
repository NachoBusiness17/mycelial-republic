# Lane runner: runs from %TEMP%\door_exp; imports repo carriers read-only; never prints keys.
import sys, os, json, subprocess, urllib.request, datetime
REPO = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
sys.path.insert(0, REPO); sys.path.insert(0, os.path.join(REPO, "tools"))
D = os.path.dirname(os.path.abspath(__file__))
P = open(os.path.join(D, "PROMPT.txt"), encoding="utf-8").read()
now = lambda: datetime.datetime.now().astimezone().isoformat()
def save(lane, meta, text):
    open(os.path.join(D, lane + ".txt"), "w", encoding="utf-8").write(text)
    json.dump(meta, open(os.path.join(D, lane + ".meta.json"), "w"), indent=1)
lane = sys.argv[1]; s = now()
try:
    if lane == "ollama":
        m = sys.argv[2]
        b = json.dumps({"model": m, "prompt": P, "stream": False}).encode()
        r = json.load(urllib.request.urlopen(urllib.request.Request("http://localhost:11434/api/generate", b, {"Content-Type": "application/json"}), timeout=1500))
        save("lane6_ollama", {"lane": "ollama local", "model": m, "start": s, "end": now()}, r["response"])
    elif lane == "direct":   # env name, model, out
        import model_garden as mg
        env, model, out = sys.argv[2:5]
        key = mg._api_key(env)
        r = mg._call(model, [{"role": "user", "content": P}], None, key, "https://api.z.ai/api/coding/paas/v4")
        msg = r["choices"][0]["message"]
        save(out, {"lane": "zai coding plan direct via tools/model_garden._api_key/_call (no usage row)", "key_env": env, "model": r.get("model", model), "usage": r.get("usage"), "start": s, "end": now()}, msg.get("content") or "")
    elif lane == "opencode":  # env name, model, out
        import model_garden as mg
        env, model, out = sys.argv[2:5]
        e = dict(os.environ)
        if env != "-": e[env] = mg._api_key(env)
        e["PATH"] = os.path.expandvars(r"%LOCALAPPDATA%\hermes\node;") + e["PATH"]
        r = subprocess.run(["cmd", "/c", "opencode", "run", "-m", model, P], cwd=D, env=e, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1500)
        save(out, {"lane": "opencode run", "model": model, "key_env": env, "exit": r.returncode, "stderr_tail": r.stderr[-1500:], "start": s, "end": now()}, r.stdout)
except Exception as ex:
    save("ERR_" + lane + "_" + "_".join(sys.argv[2:]).replace("/", "-"), {"error": repr(ex)[:800], "start": s, "end": now()}, "")
