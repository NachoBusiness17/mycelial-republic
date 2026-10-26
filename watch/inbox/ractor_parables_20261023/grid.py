import subprocess, sys, os, re, datetime, threading, concurrent.futures as cf, json
D=os.path.dirname(os.path.abspath(__file__))
B=open(os.path.join(D,"SUBJECT_BRIEFS.md"),encoding="utf-8").read()
subs=[(int(n),s) for n,s in re.findall(r"^## (\d+) (\S+)",B,re.M) if int(n)>1]
R=["FOUCAULT","FERMAT","ELLUL","BERNAYS","MCLUHAN","JUNG","HALL","WALLAS","BAUDRILLARD","PLATO_KIRK","DIOGENES","FREUD"]
for n,s in subs: subprocess.run([sys.executable,os.path.join(D,"build2.py"),str(n),s],check=True)
L=threading.Lock(); log=open(os.path.join(D,"grid.log"),"a",encoding="utf-8")
def w(m):
    with L: log.write(datetime.datetime.now().astimezone().isoformat()+" "+m+"\n"); log.flush()
def call(s,r,mp):
    fn=os.path.join(D,s,f"{r.lower()}__{mp}.md")
    if os.path.exists(fn): return "SKIP"
    for k in range(2):
        f=fn.replace(".md",".FAILED.md")
        if os.path.exists(f): os.replace(f,fn.replace(".md",".run%d_FAILED.md"%(k-1)))
        p=subprocess.run([sys.executable,os.path.join(D,"run_lane.py"),s,r,mp],capture_output=True,text=True,timeout=3000)
        st=p.stdout.strip().split()[-1] if p.stdout.strip() else "NOOUT:"+p.stderr[-200:]
        w(f"{s} {r} {mp} try{k+1} {st}")
        if os.path.exists(fn): return "OK"
    return "FAILED"
w("GRID START")
jobs={"fostertron_max":4,"agy_pc":3}
def lane(mp,n):
    with cf.ThreadPoolExecutor(n) as ex: list(ex.map(lambda t: call(t[0],t[1],mp),[(s,r) for _,s in subs for r in R]))
    w("LANE DONE "+mp)
ts=[threading.Thread(target=lane,args=(m,n)) for m,n in jobs.items()]
[t.start() for t in ts]; [t.join() for t in ts]; w("GRID END")
