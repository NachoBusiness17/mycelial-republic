#!/usr/bin/env python3
"""organ_forge v0.4 — 5.3 designs, gophers build, the gate demands substance.

Night's earned lessons, all wired in:
  * conductor = glm-5.3-flash on the z.ai API credit pool (KEY LAW)
  * gopher    = cage Bounded Worker, docker exec, named forge-* session
  * WALL      : /mag is read-only 9p in-container -> gopher writes its own
                workspace, forge copies the artifact out (docker exec cat)
  * SPEC HANDOFF: pass the gopher the CODE BLOCK ITSELF (never a truncated
                prose spec — the 6000-char cap once cut off every line of code)
  * GATE      : file must be >200 bytes, contain real code markers, AND
                py_compile clean. "PLACEHOLDER" does not pass. (QC lesson)
  * fallback  = conductor's code written directly, receipt says so honestly.
"""
import json, os, subprocess, sys, time, datetime, re, urllib.request

ROOT = os.path.realpath(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
QUEUE = os.path.join(ROOT, "watch", "organ_queue.jsonl")
BOARD = os.path.join(ROOT, "dashboard", "data", "ractor_board.jsonl")
SPECS = os.path.join(ROOT, "watch", "organ_specs")
LOG = os.path.join(ROOT, "watch", "organ_forge.log")
GWORK = "/root/.openclaw/workspace/organs"

def env_key(name):
    for line in open(os.path.join(ROOT, ".env"), encoding="utf-8", errors="replace"):
        if line.startswith(name + "="):
            return line.split("=", 1)[1].strip()
    return None

def ts():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def log(m):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(ts() + " " + m + "\n")

def board_row(kind, title, detail, status, evidence):
    row = {"organ": "forge", "kind": kind, "title": title, "detail": detail[:220],
           "status": status, "evidence": evidence, "ts": ts()}
    with open(BOARD, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

def contained(p):
    rp = os.path.realpath(os.path.join(ROOT, p))
    if not rp.startswith(ROOT + os.sep):
        raise ValueError("escapes repo")
    return rp

def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")[:40]

def conductor_spec(brief):
    key = env_key("ZAI_API_KEY")
    sysmsg = ("You are the fleet conductor. Emit ONE complete, runnable single-file "
              "Python module per the brief. Style: stdlib only, no third-party imports, "
              "module docstring states the law it serves, functions small, fail loud. "
              "Reply with ONLY the python code wrapped in one ```python block. "
              "No prose before or after. No VERIFY line.")
    body = json.dumps({
        "model": "glm-5.3-flash",
        "messages": [{"role": "system", "content": sysmsg},
                     {"role": "user", "content": brief}],
        "temperature": 0.3, "max_tokens": 8192, "reasoning_effort": "low",
    }).encode()
    req = urllib.request.Request(
        "https://api.z.ai/api/paas/v4/chat/completions", data=body,
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + (key or "")})
    with urllib.request.urlopen(req, timeout=180) as r:
        data = json.loads(r.read().decode())
    return data["choices"][0]["message"]["content"]

def code_of(spec_text):
    blocks = re.findall(r"```(?:python)?\s*(.*?)```", spec_text, re.S)
    for b in blocks:
        if len(b.strip()) > 200 and ("def " in b or "import " in b):
            return b.strip() + "\n"
    return None

def gate(build_p):
    """Substance gate: real size, real code markers, compiles."""
    if not os.path.isfile(build_p):
        return False, "file missing"
    txt = open(build_p, encoding="utf-8", errors="replace").read()
    if len(txt) < 200:
        return False, f"too small ({len(txt)} bytes)"
    if "def " not in txt or "import " not in txt:
        return False, "no code markers"
    v = subprocess.run([sys.executable, "-m", "py_compile", build_p],
                       capture_output=True, text=True, timeout=60)
    if v.returncode != 0:
        return False, "py_compile FAIL: " + v.stderr[:120]
    return True, f"py_compile PASS ({len(txt)} bytes)"

def cage_write(sid, code, container_rel):
    task_text = ("Write this EXACT code to the file " + container_rel + " (that path "
                 "is inside your own workspace and writable; /mag is read-only — do "
                 "not use it). Create parent dirs if needed. Then reply DONE.\n\n"
                 "```python\n" + code + "```")
    r = subprocess.run(
        [sys.executable, "-m", "mag.seat_dispatch", "task", task_text,
         "--seat", "openclaw-worker"],
        cwd=ROOT, capture_output=True, text=True, timeout=420)
    try:
        return json.loads(r.stdout.strip()).get("detail", r.stdout[:1500])
    except json.JSONDecodeError:
        return r.stdout[:1500]

def copy_out(container_path, host_path):
    r = subprocess.run(["docker", "exec", "mag-openclaw", "cat", container_path],
                       capture_output=True, text=True, timeout=60)
    if r.returncode != 0 or not r.stdout.strip():
        return False
    with open(host_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(r.stdout)
    return True

def main():
    os.makedirs(SPECS, exist_ok=True)
    log("forge v0.4 awake")
    for t in [json.loads(l) for l in open(QUEUE, encoding="utf-8") if l.strip()]:
        sid = slug(t["id"])
        spec_p = contained(os.path.join("watch", "organ_specs", sid + ".md"))
        build_p = contained(t["build"])
        if os.path.isfile(build_p):
            ok, why = gate(build_p)
            if ok:
                log(sid + " already built - skip")
                continue
            os.remove(build_p)
            log(sid + " removed unsubstantial build: " + why)
        spec_text = ""
        if os.path.isfile(spec_p):
            spec_text = open(spec_p, encoding="utf-8").read()
        code = code_of(spec_text)
        if not code:
            log(sid + " -> conductor (5.3 spec)")
            try:
                spec_text = conductor_spec(t["brief"])
                with open(spec_p, "w", encoding="utf-8") as f:
                    f.write("# ORGAN SPEC: " + t["title"] + "\n\n" + spec_text + "\n")
            except Exception as e:
                board_row("task.receipt", "forge: spec FAILED - " + t["title"],
                          str(e), "BLOCKED", "watch/organ_specs/" + sid + ".md")
                log(sid + " spec failed: " + str(e))
                continue
            code = code_of(spec_text)
            if not code:
                board_row("task.receipt", "forge: spec FAILED - " + t["title"],
                          "conductor emitted no usable python block", "BLOCKED",
                          "watch/organ_specs/" + sid + ".md")
                log(sid + " spec had no code")
                continue
            board_row("milestone", "forge: spec landed - " + t["title"],
                      "glm-5.3-flash emitted the organ (" + str(len(code)) + " chars).",
                      "DONE", "watch/organ_specs/" + sid + ".md")
        cref = GWORK + "/" + sid + ".py"
        log(sid + " -> gopher build (forge session)")
        detail = cage_write(sid, code, cref)
        ok = copy_out(cref, build_p)
        if not ok:
            with open(build_p, "w", encoding="utf-8", newline="\n") as f:
                f.write(code)
            detail = "[conductor fallback — gopher artifact missing; gopher said: " + detail[:120] + "]"
        ok, why = gate(build_p)
        board_row("task.receipt", "forge: build " + t["title"], why + " | " + detail,
                  "DONE" if ok else "BLOCKED", t["build"])
        log(sid + " build " + ("ok" if ok else "BLOCKED: " + why))
        time.sleep(20)

if __name__ == "__main__":
    main()
