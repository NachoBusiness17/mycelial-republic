# One call: python run_lane.py <slug> <RACTOR> <mouthpiece>. Mouthpieces: fostertron_max | agy_pc. Never prints keys.
import sys, os, json, subprocess, datetime, tempfile, re, shutil
REPO = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
sys.path.insert(0, REPO); sys.path.insert(0, os.path.join(REPO,"tools"))
D = os.path.dirname(os.path.abspath(__file__))
slug, rac, mp = sys.argv[1:4]
P = open(os.path.join(D,"prompts",slug,rac+".txt"),encoding="utf-8").read()
now = lambda: datetime.datetime.now().astimezone().isoformat()
wd = os.path.join(tempfile.gettempdir(),"ractor_parables",slug,rac+"__"+mp); shutil.rmtree(wd,ignore_errors=True); os.makedirs(wd)
open(os.path.join(wd,"PROMPT.txt"),"w",encoding="utf-8").write(P)
SHORT = "Read the file PROMPT.txt in the current directory and follow its instructions exactly. Output only what it asks for."
s = now(); meta = {"ractor": rac, "mouthpiece": mp, "subject": slug, "start_et": s}
try:
    if mp == "fostertron_max":
        import model_garden as mg
        e = dict(os.environ); e["ZAI_API_KEY_2"] = mg._api_key("ZAI_API_KEY_2")
        e["PATH"] = os.path.expandvars(r"%LOCALAPPDATA%\hermes\node;") + e["PATH"]
        att=[]
        for i in range(2):
            r = subprocess.run(["cmd","/c","opencode","run","-m","zai-sd/glm-5.3",SHORT],cwd=wd,env=e,capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=1500)
            att.append({"attempt":i+1,"exit":r.returncode,"stdout_len":len(r.stdout),"at":now()})
            if r.returncode==0 and "---KEY---" in r.stdout: break
        meta["attempts"]=att
        out = r.stdout; resolved = "zai-sd/glm-5.3" if "glm-5.3" in r.stderr else "unconfirmed"
        m = re.findall(r"build \u00b7 (\S+)", r.stderr); resolved = m[-1] if m else resolved
        meta.update(carrier="opencode run (provider zai-sd 'sd / Max', key env ZAI_API_KEY_2 via model_garden._api_key)", requested_model="zai-sd/glm-5.3", resolved_model=resolved, exit=r.returncode, stderr_tail=r.stderr[-600:], tokens="not reported by opencode run")
    elif mp == "agy_pc":
        log = os.path.join(wd,"agy.log")
        r = subprocess.run([os.path.expandvars(r"%LOCALAPPDATA%\antigravity\staging\agy.exe"),"--model","gemini-4-argon-high","--mode","plan","--print-timeout","900s","--log-file",log,"-p",SHORT],cwd=wd,capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=1000)
        out = r.stdout; lg = open(log,encoding="utf-8",errors="replace").read() if os.path.exists(log) else ""
        ms = sorted(set(re.findall(r"(gemini-[\w.\-]+|claude-[\w.\-]+|gpt-oss-[\w.\-]+)", lg)))
        meta["resolved_label_in_log"] = sorted(set(re.findall(r'selected model override to backend: label="([^"]+)"', lg)))
        meta["resolver_lines"] = [l[-160:] for l in lg.splitlines() if "resolve" in l.lower()][:6]
        meta.update(carrier="agy.exe --mode plan -p (PC)", requested_model="gemini-4-argon-high", resolved_model_strings_in_log=ms, exit=r.returncode, stderr_tail=r.stderr[-600:], log_path=log, tokens="not reported")
    meta["end_et"] = now()
    ok = meta.get("exit")==0 and "---KEY---" in out and len(out) > 800
    meta["status"] = "OK" if ok else "FAILED_OR_MALFORMED"
except Exception as ex:
    out = ""; meta.update(status="FAILED", error=repr(ex)[:600], end_et=now())
od = os.path.join(D,slug); os.makedirs(od,exist_ok=True)
fn = os.path.join(od, f"{rac.lower()}__{mp}.md")
if meta["status"]=="OK":
    open(fn,"w",encoding="utf-8").write("<!-- meta: "+json.dumps(meta)+" -->\n\n"+out.strip()+"\n")
else:
    open(fn.replace(".md",".FAILED.md"),"w",encoding="utf-8").write("<!-- meta: "+json.dumps(meta)+" -->\n\nLANE FAILED - no output recorded. Raw stdout length %d.\n\n```\n%s\n```\n"%(len(out),out[-3000:]))
print(rac, mp, meta["status"])
