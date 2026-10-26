# argon_ask.py -- dispatch THE_ARGON_MASTER_DISPATCH_ASK (or a small ad-hoc ask) to Gemini 4 Argon via agy.exe on PC.
# Same carrier as ractor_parables run_lane.py agy_pc. Read-only on repo; writes only to watch/inbox/argon_ask_runs/.
# Usage: python tools/argon_ask.py --prompt "cheap question"     |   python tools/argon_ask.py --full  (the master ask; big call, needs approval)
import sys, os, json, subprocess, datetime, tempfile, re, argparse
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASK = os.path.join(REPO, "watch", "inbox", "THE_ARGON_MASTER_DISPATCH_ASK_20261023.md")
AGY = os.path.expandvars(r"%LOCALAPPDATA%\antigravity\staging\agy.exe")
ap = argparse.ArgumentParser(); g = ap.add_mutually_exclusive_group(required=True)
g.add_argument("--prompt"); g.add_argument("--full", action="store_true")
ap.add_argument("--timeout", type=int, default=900); a = ap.parse_args()
if a.full:
    t = open(ASK, encoding="utf-8").read()
    m = re.search(r"```markdown\s*\n(SYSTEM PROMPT:.*?)```", t, re.S)
    if not m:
        m = re.search(r"## (?:4|6)\..*?```markdown\s*\n(.*?)```", t, re.S)
    P = m.group(1).strip() + "\n\nProduce the parable, then a line ---KEY--- , then the JSON key.\n"
else:
    P = a.prompt
now = lambda: datetime.datetime.now().astimezone().isoformat()
ts = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
wd = os.path.join(tempfile.gettempdir(), "argon_ask", ts); os.makedirs(wd)
open(os.path.join(wd, "PROMPT.txt"), "w", encoding="utf-8").write(P)
log = os.path.join(wd, "agy.log"); meta = {"start_et": now(), "mode": "full" if a.full else "prompt"}
r = subprocess.run([AGY, "--model", "gemini-4-argon-high", "--mode", "plan", "--print-timeout", f"{a.timeout}s", "--log-file", log,
    "-p", "Read the file PROMPT.txt in the current directory and follow its instructions exactly. Output only what it asks for."],
    cwd=wd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=a.timeout + 100)
lg = open(log, encoding="utf-8", errors="replace").read() if os.path.exists(log) else ""
meta.update(end_et=now(), exit=r.returncode, stderr_tail=r.stderr[-400:], log_path=log,
    resolved_label=sorted(set(re.findall(r'selected model override to backend: label="([^"]+)"', lg))))
od = os.path.join(REPO, "watch", "inbox", "argon_ask_runs"); os.makedirs(od, exist_ok=True)
fn = os.path.join(od, f"argon_ask_{ts}.md")
open(fn, "w", encoding="utf-8").write("<!-- meta: " + json.dumps(meta) + " -->\n\n" + r.stdout.strip() + "\n")
print(json.dumps(meta, indent=1)); print("OUT:", fn); print(r.stdout.strip()[:2000])
sys.exit(r.returncode)
