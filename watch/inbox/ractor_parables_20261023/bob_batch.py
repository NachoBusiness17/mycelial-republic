# bob agy lane: Claude via agy (explicit --model). Isolated dir per call. No keys touched.
import subprocess, os, re, json, datetime, zipfile, shutil
from concurrent.futures import ThreadPoolExecutor
B=r"C:\Users\etfag\ractor_parables"; AGY=r"C:\Users\etfag\AppData\Local\agy\bin\agy.exe"; MODEL="claude-opus-5-5-medium"
zipfile.ZipFile(os.path.join(B,"rp_prompts.zip")).extractall(os.path.join(B,"prompts"))
now=lambda: datetime.datetime.now().astimezone().isoformat()
SHORT="Read the file PROMPT.txt in the current directory and follow its instructions exactly. Output only what it asks for."
R=["FOUCAULT","FERMAT","ELLUL","BERNAYS","MCLUHAN","JUNG","HALL","WALLAS","BAUDRILLARD","PLATO_KIRK","DIOGENES","FREUD"]
os.makedirs(os.path.join(B,"out"),exist_ok=True)
def go(n):
    wd=os.path.join(B,"wd",n); shutil.rmtree(wd,ignore_errors=True); os.makedirs(wd)
    shutil.copy(os.path.join(B,"prompts",n+".txt"),os.path.join(wd,"PROMPT.txt"))
    log=os.path.join(wd,"agy.log"); s=now(); meta={"ractor":n,"mouthpiece":"agy_bob","subject":"who_we_are","start_et":s,"carrier":"agy.exe --mode plan -p (bob)","requested_model":MODEL}
    try:
        r=subprocess.run([AGY,"--model",MODEL,"--mode","plan","--print-timeout","900s","--log-file",log,"-p",SHORT],cwd=wd,capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=1000)
        out=r.stdout; lg=open(log,encoding="utf-8",errors="replace").read() if os.path.exists(log) else ""
        meta.update(exit=r.returncode,stderr_tail=r.stderr[-400:],resolved_label_in_log=sorted(set(re.findall(r'selected model override to backend: label="([^"]+)"',lg))),resolved_model_strings_in_log=sorted(set(re.findall(r"(gemini-[\w.\-]+|claude-[\w.\-]+|gpt-oss-[\w.\-]+)",lg))),resolver_lines=[l[-160:] for l in lg.splitlines() if "resolve" in l.lower()][:6],tokens="not reported")
        meta["status"]="OK" if r.returncode==0 and "---KEY---" in out and len(out)>800 else "FAILED_OR_MALFORMED"
    except Exception as ex:
        out=""; meta.update(status="FAILED",error=repr(ex)[:400])
    meta["end_et"]=now()
    suf=".md" if meta["status"]=="OK" else ".FAILED.md"
    body=out.strip() if meta["status"]=="OK" else "LANE FAILED - no output recorded. Raw stdout tail:\n```\n%s\n```"%out[-2000:]
    open(os.path.join(B,"out",n.lower()+"__agy_bob"+suf),"w",encoding="utf-8").write("<!-- meta: "+json.dumps(meta)+" -->\n\n"+body+"\n")
with ThreadPoolExecutor(3) as f: list(f.map(go,R))
open(os.path.join(B,"out","DONE"),"w").write(now())
