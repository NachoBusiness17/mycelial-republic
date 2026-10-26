# Resumable full grid. Skips pairs with a valid output; retry once; progress -> GRID_PROGRESS.json. Lanes: fostertron_max(4), agy_pc(3) only.
import subprocess, sys, os, re, datetime, threading, json, concurrent.futures as cf
D=os.path.dirname(os.path.abspath(__file__))
B=open(os.path.join(D,"SUBJECT_BRIEFS.md"),encoding="utf-8").read()
subs=[s for n,s in re.findall(r"^## (\d+) (\S+)",B,re.M)]
R=["FOUCAULT","FERMAT","ELLUL","BERNAYS","MCLUHAN","JUNG","HALL","WALLAS","BAUDRILLARD","PLATO_KIRK","DIOGENES","FREUD"]
for i,s in enumerate(subs,1):
    if not os.path.exists(os.path.join(D,"prompts",s,"FREUD.txt")): subprocess.run([sys.executable,os.path.join(D,"build2.py"),str(i),s],check=True)
L=threading.Lock(); PF=os.path.join(D,"GRID_PROGRESS.json")
prog=json.load(open(PF)) if os.path.exists(PF) else {"pairs":{}}
now=lambda: datetime.datetime.now().astimezone().isoformat()
log=open(os.path.join(D,"grid.log"),"a",encoding="utf-8")
def valid(fn):
    if not os.path.exists(fn): return False
    t=open(fn,encoding="utf-8",errors="replace").read(); return "---KEY---" in t and len(t)>800
def save(k,v):
    with L:
        prog["pairs"][k]=v; prog["updated_et"]=now()
        tmp=PF+".tmp"; json.dump(prog,open(tmp,"w"),indent=1); os.replace(tmp,PF)
        log.write(now()+" GRID2 "+k+" "+v["status"]+"\n"); log.flush()
def call(s,r,mp):
    k=f"{s}|{r}|{mp}"; fn=os.path.join(D,s,f"{r.lower()}__{mp}.md")
    if valid(fn):
        if prog["pairs"].get(k,{}).get("status") not in ("OK","SKIP_EXISTING"): save(k,{"status":"SKIP_EXISTING"})
        return
    t0=now(); tries=[]
    for a in range(2):
        f=fn.replace(".md",".FAILED.md")
        if os.path.exists(f): os.replace(f,fn.replace(".md",".grid2_try%d_FAILED.md"%a))
        try:
            p=subprocess.run([sys.executable,os.path.join(D,"run_lane.py"),s,r,mp],capture_output=True,text=True,timeout=3000)
            tries.append((p.stdout.strip().split() or ["NOOUT"])[-1])
        except Exception as e: tries.append("EXC "+repr(e)[:200])
        if valid(fn): save(k,{"status":"OK","tries":tries,"start_et":t0,"end_et":now()}); return
    save(k,{"status":"FAILED","tries":tries,"start_et":t0,"end_et":now()})
prog["started_et"]=prog.get("started_et") or now(); log.write(now()+" GRID2 START\n"); log.flush()
def lane(mp,n):
    with cf.ThreadPoolExecutor(n) as ex: list(ex.map(lambda t: call(t[0],t[1],mp),[(s,r) for s in subs for r in R]))
    log.write(now()+" GRID2 LANE DONE "+mp+"\n"); log.flush()
ts=[threading.Thread(target=lane,args=a) for a in (("fostertron_max",4),("agy_pc",3))]
[t.start() for t in ts]; [t.join() for t in ts]
prog["finished_et"]=now(); save("_END",{"status":"DONE"})
