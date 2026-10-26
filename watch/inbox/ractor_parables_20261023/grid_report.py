import os,re,json,glob,collections,datetime
D=os.path.dirname(os.path.abspath(__file__))
B=open(os.path.join(D,"SUBJECT_BRIEFS.md"),encoding="utf-8").read()
subs=[s for n,s in re.findall(r"^## (\d+) (\S+)",B,re.M)]
R=["FOUCAULT","FERMAT","ELLUL","BERNAYS","MCLUHAN","JUNG","HALL","WALLAS","BAUDRILLARD","PLATO_KIRK","DIOGENES","FREUD"]
MP=["fostertron_max","agy_pc"]
NAMES=["Sancho","Bob","T90","Pixel","Hermes","Moto","Nacho","Fostertron","Antigravity","Claude","GLM","Gemini","DeepSeek","Opencode","Ractor"]
TECH=["seat","lane","ledger","hash","model","API"]
STOP=set("the a an and or of to in on at by for with is are was were be it its that this from as not no never but who what when one each their they his her he she them into only than then there which out up all any own so if before after must can".split())
prog=json.load(open(os.path.join(D,"GRID_PROGRESS.json")))
P=prog.get("pairs",{})
def meta(t):
    m=re.match(r"<!-- meta: (.*?) -->",t); 
    try: return json.loads(m.group(1)) if m else {}
    except: return {}
def et(s):
    try: return datetime.datetime.fromisoformat(s).strftime("%H:%M:%S")
    except: return "?"
o=["# GRID REPORT - ractor parables 2026-10-23","",f"Generated {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} ET. Lanes: fostertron_max (opencode zai-sd/glm-5.3, 4 conc) and agy_pc (agy.exe gemini-4-argon-high, 3 conc). Grid2 runner start {et(prog.get('started_et',''))} ET, finish {et(prog.get('finished_et',''))} ET. Pairs produced earlier (batch1 / interrupted grid.py) were skipped, not re-run.","","## Counts (valid outputs / 12)","","| subject | fostertron_max | agy_pc | produced this resume (max/agy) |","|---|---|---|---|"]
fails=[];models=collections.Counter();leaks=[];quota=[];conv=[];durs=collections.defaultdict(list)
tot=collections.Counter()
for s in subs:
    row=[s];new=[]
    keys={m:[] for m in MP}
    for m in MP:
        c=0;n=0
        for r in R:
            fn=os.path.join(D,s,f"{r.lower()}__{m}.md")
            if os.path.exists(fn):
                t=open(fn,encoding="utf-8",errors="replace").read()
                if "---KEY---" not in t: continue
                c+=1; md=meta(t)
                if P.get(f"{s}|{r}|{m}",{}).get("status")=="OK": n+=1
                mod=md.get("resolved_model") or ",".join(md.get("resolved_label_in_log",[]) or md.get("resolved_model_strings_in_log",[]) or ["unrecorded"])
                models[(m,mod)]+=1
                try: durs[m].append((datetime.datetime.fromisoformat(md["end_et"])-datetime.datetime.fromisoformat(md["start_et"])).total_seconds())
                except: pass
                body=t.split("-->",1)[-1]; story,key=body.split("---KEY---",1)
                hit=[x for x in NAMES if re.search(r"\b"+re.escape(x)+r"\b",story)]
                th=[x for x in TECH if re.search(r"\b"+x+r"s?\b",story,re.I)]
                if hit or th: leaks.append(f"{s}/{r.lower()}__{m}: names={hit} techwords={th}")
                st=md.get("stderr_tail","")
                if re.search(r"429|quota|rate.?limit|exhaust|resource_exhausted",st,re.I): quota.append(f"{s}/{r.lower()}__{m}: "+re.sub(r"\s+"," ",st)[-200:])
                keys[m]+= [w for w in re.findall(r"[a-z]{4,}",key.lower()) if w not in STOP]
        tot[m]+=c; row.append(f"{c}"); new.append(str(n))
    row.append("/".join(new)); o.append("| "+" | ".join(row)+" |")
    ca=collections.Counter(keys["fostertron_max"]);cb=collections.Counter(keys["agy_pc"])
    sa=set(w for w,_ in ca.most_common(40));sb=set(w for w,_ in cb.most_common(40))
    j=len(sa&sb)/max(1,len(sa|sb))
    conv.append(f"- **{s}**: key-vocab Jaccard(top40) max vs agy = {j:.2f}. Shared: {', '.join(sorted(sa&sb)[:14])}. Max-only: {', '.join([w for w,_ in ca.most_common(40) if w not in sb][:8])}. Agy-only: {', '.join([w for w,_ in cb.most_common(40) if w not in sa][:8])}.")
o.append(f"| **total** | {tot['fostertron_max']} | {tot['agy_pc']} | |")
o+=["","## Failures (verbatim, this resume)",""]
for k,v in P.items():
    if v.get("status")=="FAILED":
        s,r,m=k.split("|"); o.append(f"### {k}  tries={v.get('tries')}")
        for f in sorted(glob.glob(os.path.join(D,s,f"{r.lower()}__{m}*FAILED.md"))): o+=["```",open(f,encoding="utf-8",errors="replace").read()[:1500],"```"]
if not any(v.get("status")=="FAILED" for v in P.values()): o.append("None.")
o+=["","Older failure files in tree (pre-resume, kept): "+", ".join(os.path.relpath(f,D) for f in glob.glob(os.path.join(D,"*","*FAILED.md")) if "claude_sample" not in f and not any(k.split("|")[0] in f and P[k].get("status")=="FAILED" for k in P if "|" in k)),""]
o+=["## Models per log (from each output's meta)",""]+[f"- {m}: `{mod}` x{n}" for (m,mod),n in sorted(models.items())]
o+=["","## Timings (per call, seconds)",""]
for m,v in durs.items():
    v=sorted(v); o.append(f"- {m}: n={len(v)} median={v[len(v)//2]:.0f}s min={v[0]:.0f}s max={v[-1]:.0f}s")
o+=["","## Convergence / divergence per subject (heuristic: KEY-section vocabulary overlap between mouthpieces; read the files for real judgement)",""]+conv
o+=["","## Leaks (proper names or banned tech words inside the parable body; whole-word scan)",""]+(leaks or ["None found."])
o+=["","## Quota signals (stderr of successful+failed calls)",""]+(quota or ["None seen in stderr tails."])
open(os.path.join(D,"GRID_REPORT.md"),"w",encoding="utf-8").write("\n".join(o)+"\n"); print("ok",dict(tot))
