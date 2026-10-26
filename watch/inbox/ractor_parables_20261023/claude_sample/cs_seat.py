# python cs_seat.py <seat> <slug:RACTOR> ...  seats: agy_pc_claude | claude_code_pc. Sequential; stops at first quota error.
import sys,os,json,subprocess,datetime,tempfile,re,shutil
D=os.path.dirname(os.path.abspath(__file__)); P0=os.path.dirname(D)
now=lambda: datetime.datetime.now().astimezone().isoformat(timespec="seconds")
SHORT="Read the file PROMPT.txt in the current directory and follow its instructions exactly. Output only what it asks for."
ADD="\n\nADDITIONAL RULE: use no real device, seat, machine, or person names from the facts anywhere in the parable (invent neutral period names instead)."
seat=sys.argv[1]
for job in sys.argv[2:]:
    slug,rac=job.split(":")
    P=open(os.path.join(P0,"prompts",slug,rac+".txt"),encoding="utf-8").read()+ADD
    wd=os.path.join(tempfile.gettempdir(),"rp_claude_sample",slug+"__"+rac+"__"+seat); shutil.rmtree(wd,ignore_errors=True); os.makedirs(wd)
    open(os.path.join(wd,"PROMPT.txt"),"w",encoding="utf-8").write(P)
    meta={"ractor":rac,"subject":slug,"seat":seat,"start_et":now()}
    try:
        if seat=="agy_pc_claude":
            log=os.path.join(wd,"agy.log"); M="claude-opus-5-5-medium"
            r=subprocess.run([os.path.expandvars(r"%LOCALAPPDATA%\antigravity\staging\agy.exe"),"--model",M,"--mode","plan","--print-timeout","900s","--log-file",log,"-p",SHORT],cwd=wd,capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=1000)
            out=r.stdout; lg=open(log,encoding="utf-8",errors="replace").read() if os.path.exists(log) else ""
            meta.update(carrier="agy.exe --mode plan -p (PC)",requested_model=M,resolved_label_in_log=sorted(set(re.findall(r'selected model override to backend: label="([^"]+)"',lg))),errors_in_log=[l[-300:] for l in lg.splitlines() if re.search(r"code 429|RESOURCE_EXHAUSTED|Individual quota",l,re.I)][:4])
            err=r.stderr+" "+" ".join(meta["errors_in_log"])
        else:
            r=subprocess.run(["cmd","/c","claude","-p",SHORT,"--model","opus","--output-format","json","--allowedTools","Read"],cwd=wd,capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=1200)
            try:
                j=json.loads(r.stdout); out=j.get("result","") or ""
                meta.update(model_usage=list((j.get("modelUsage") or {}).keys()),usage=j.get("usage"),cost_usd=j.get("total_cost_usd"),is_error=j.get("is_error"))
            except Exception: out=r.stdout
            meta.update(carrier="Claude Code CLI 2.1.245 claude -p (PC)",requested_model="opus")
            err=r.stderr+" "+(out if "---KEY---" not in out else "")
        meta.update(exit=r.returncode,stderr_tail=r.stderr[-500:])
        meta["status"]="OK" if r.returncode==0 and "---KEY---" in out and len(out)>800 else "FAILED_OR_MALFORMED"
    except Exception as ex:
        out="";err=repr(ex);meta.update(status="FAILED",error=repr(ex)[:500])
    meta["end_et"]=now()
    fn=os.path.join(D,f"{slug}__{rac.lower()}__{seat}"+(".md" if meta["status"]=="OK" else ".FAILED.md"))
    open(fn,"w",encoding="utf-8").write("<!-- meta: "+json.dumps(meta)+" -->\n\n"+(out.strip() if meta["status"]=="OK" else "FAILED. stdout tail:\n```\n"+out[-2500:]+"\n```\n")+"\n")
    print(job,seat,meta["status"],flush=True)
    if meta["status"]!="OK" and re.search(r"code 429|RESOURCE_EXHAUSTED|Individual quota|usage limit",err,re.I): print("QUOTA STOP",flush=True); break

