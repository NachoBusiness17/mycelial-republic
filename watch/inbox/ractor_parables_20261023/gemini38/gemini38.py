# gemini38.py - Gemini 3.8 Flash (High) lanes via agy.exe (PC, existing consumer login). New lanes only; never touches agy_pc files.
# Phase 1: fill agy_pc gaps -> <lens>__gemini38_acctA.md ; Phase 2: full 144 round -> <lens>__gemini38_acctA_r2.md. Stops lane on 429/quota.
import os,re,json,subprocess,datetime,tempfile,shutil,threading,concurrent.futures as cf,sys
D=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); G=os.path.join(D,"gemini38")
AGY=os.path.expandvars(r"%LOCALAPPDATA%\antigravity\staging\agy.exe"); MODEL="gemini-3.8-flash-high"; ACCT="acctA"
B=open(os.path.join(D,"SUBJECT_BRIEFS.md"),encoding="utf-8").read(); subs=[s for n,s in re.findall(r"^## (\d+) (\S+)",B,re.M)]
R=["FOUCAULT","FERMAT","ELLUL","BERNAYS","MCLUHAN","JUNG","HALL","WALLAS","BAUDRILLARD","PLATO_KIRK","DIOGENES","FREUD"]
SHORT="Read the file PROMPT.txt in the current directory and follow its instructions exactly. Output only what it asks for."
now=lambda: datetime.datetime.now().astimezone().isoformat(timespec="seconds")
L=threading.Lock(); PF=os.path.join(G,"PROGRESS.json"); STOP=threading.Event()
prog=json.load(open(PF)) if os.path.exists(PF) else {"model":MODEL,"account":ACCT,"cells":{},"events":[]}
def valid(fn):
    return os.path.exists(fn) and (lambda t:"---KEY---" in t and len(t)>800)(open(fn,encoding="utf-8",errors="replace").read())
def md():
    c=prog["cells"]; ph={}
    for k,v in c.items(): p=k.split("|")[0]; ph.setdefault(p,{}); ph[p][v["status"]]=ph[p].get(v["status"],0)+1
    o=["# Gemini 3.8 lanes - PROGRESS","",f"Updated: {prog.get('updated_et')}  |  model `{MODEL}` via agy.exe PC  |  account label `{ACCT}`","",
       "Second account: NOT RUN - see GRID_REPORT.md section (gemini CLI login rejected: IneligibleTierError; no second agy profile found).",""]
    for p,d in ph.items(): o.append(f"- **{p}**: "+", ".join(f"{a}={b}" for a,b in sorted(d.items())))
    o+=["","## Events",""]+[f"- {e}" for e in prog["events"][-40:]]
    open(os.path.join(G,"PROGRESS.md"),"w",encoding="utf-8").write("\n".join(o)+"\n")
def save(k=None,v=None,ev=None):
    with L:
        if k: prog["cells"][k]=v
        if ev: prog["events"].append(now()+" "+ev)
        prog["updated_et"]=now(); t=PF+".tmp"; json.dump(prog,open(t,"w"),indent=1); os.replace(t,PF); md()
QRE=re.compile(r"\b429\b|RESOURCE_EXHAUSTED|quota (exceeded|exhausted)|rate.?limit|exhausted your",re.I)
def call(phase,s,r,lane):
    if STOP.is_set(): return
    k=f"{phase}|{s}|{r}"; fn=os.path.join(D,s,f"{r.lower()}__{lane}.md")
    if valid(fn): 
        if prog["cells"].get(k,{}).get("status")!="OK": save(k,{"status":"OK","note":"existing"})
        return
    P=open(os.path.join(D,"prompts",s,r+".txt"),encoding="utf-8").read()
    wd=os.path.join(tempfile.gettempdir(),"ractor_g38",phase,s,r); shutil.rmtree(wd,ignore_errors=True); os.makedirs(wd)
    open(os.path.join(wd,"PROMPT.txt"),"w",encoding="utf-8").write(P); log=os.path.join(wd,"agy.log"); t0=now()
    try:
        p=subprocess.run([AGY,"--model",MODEL,"--mode","plan","--print-timeout","900s","--log-file",log,"-p",SHORT],cwd=wd,capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=1000)
        out,err,ex=p.stdout,p.stderr,p.returncode
    except Exception as e: out,err,ex="",repr(e),-9
    lg=open(log,encoding="utf-8",errors="replace").read() if os.path.exists(log) else ""
    labels=sorted(set(re.findall(r'selected model override to backend: label="([^"]+)"',lg)))
    meta={"ractor":r,"mouthpiece":lane,"subject":s,"phase":phase,"carrier":"agy.exe --mode plan -p (PC)","requested_model":MODEL,"resolved_label_in_log":labels,"account":ACCT,"start_et":t0,"end_et":now(),"exit":ex}
    if ex==0 and "---KEY---" in out and len(out)>800:
        open(fn,"w",encoding="utf-8").write("<!-- meta: "+json.dumps(meta)+" -->\n\n"+out.strip()+"\n"); save(k,{"status":"OK","end_et":now(),"labels":labels}); return
    q=QRE.search(out+err+lg[-20000:])
    open(os.path.join(G,"fail",f"{phase}__{s}__{r.lower()}.txt"),"w",encoding="utf-8").write(json.dumps(meta)+"\nSTDOUT_TAIL:\n"+out[-1500:]+"\nSTDERR_TAIL:\n"+err[-1500:])
    if q:
        save(k,{"status":"QUOTA","sig":q.group(0)},ev=f"QUOTA hit on {ACCT} at {k} ({q.group(0)}) - stopping lane"); STOP.set()
    else: save(k,{"status":"FAILED","exit":ex})
os.makedirs(os.path.join(G,"fail"),exist_ok=True)
gaps=[(s,r) for s in subs for r in R if not valid(os.path.join(D,s,f"{r.lower()}__agy_pc.md"))]
save(ev=f"START pid={os.getpid()} gaps={len(gaps)}")
for phase,lane,cells in (("fill",f"gemini38_{ACCT}",gaps),("r2",f"gemini38_{ACCT}_r2",[(s,r) for s in subs for r in R])):
    if STOP.is_set(): break
    for attempt in (1,2):
        with cf.ThreadPoolExecutor(3) as ex: list(ex.map(lambda t: call(phase,t[0],t[1],lane),cells))
        if STOP.is_set(): break
    save(ev=f"PHASE {phase} end (stop={STOP.is_set()})")
save(ev="DONE" if not STOP.is_set() else "STOPPED on quota")
