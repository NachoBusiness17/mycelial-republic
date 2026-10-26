# g38_report.py - rewrite the "Gemini 3.8 lanes" section of GRID_REPORT.md from gemini38/PROGRESS.json; fixes the old quota note. Idempotent.
import os,json,re,collections
D=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); G=os.path.join(D,"gemini38"); RP=os.path.join(D,"GRID_REPORT.md")
t=open(RP,encoding="utf-8").read()
old="None seen in stderr tails."
new=("CORRECTION (2026-10-23 evening): the line previously here said \"None seen in stderr tails\" - that was WRONG. The scan only read the stderr tail; "
     "the agy_pc FAILED cells actually died on HTTP 429 / Gemini 4 Argon quota exhaustion (quota resets ~2026-10-30). 64/144 agy_pc cells missing for that reason. "
     "Gaps are being filled by the Gemini 3.8 lane below (separate files, Argon outputs untouched).")
t=t.replace(old,new)
p=json.load(open(os.path.join(G,"PROGRESS.json")))
c=collections.Counter(); bys=collections.defaultdict(collections.Counter)
for k,v in p["cells"].items():
    ph,s,r=k.split("|"); c[(ph,v["status"])]+=1; bys[s][ph+"_"+v["status"]]+=1
q=[e for e in p["events"] if "QUOTA" in e]
o=["","## Gemini 3.8 lanes (gemini38_acctA = fill of agy_pc gaps; gemini38_acctA_r2 = fresh full round)","",
 f"Model id `gemini-3.8-flash-high` (label \"Gemini 3.8 Flash (High)\" confirmed in agy log), carrier agy.exe --mode plan -p on PC, 3 concurrent, existing consumer login (acctA). Runner gemini38/gemini38.py, progress gemini38/PROGRESS.md. Last update {p.get('updated_et')}.","",
 "Files: `<subject>/<lens>__gemini38_acctA.md` (fill) and `<subject>/<lens>__gemini38_acctA_r2.md` (round 2). Failures: gemini38/fail/.","",
 "Second account (acctB): NOT RUN. The Gemini CLI (gemini 0.64.0, oauth-personal) refuses with IneligibleTierError (\"client no longer supported for Gemini Code Assist for individuals - migrate to Antigravity\"); agy on PC exposes only one signed-in account and has no account-select flag. Needs operator decision (switch account in Antigravity, or run agy from bob).","",
 "| phase | OK | FAILED | QUOTA |","|---|---|---|---|"]
for ph in ("fill","r2"): o.append(f"| {ph} | {c[(ph,'OK')]} | {c[(ph,'FAILED')]} | {c[(ph,'QUOTA')]} |")
o+=["","Quota stop: "+("; ".join(q) if q else "none hit so far."),"",
 "Leak scan: these new files are NOT yet covered by grid_report.py's leak scan (grid_report.py only knows the two original lanes); run a name/tech-word scan before feeding them to the blind judge.",""]
m="\n## Gemini 3.8 lanes"
t=t.split(m)[0].rstrip("\n")+"\n"+"\n".join(o)
open(RP,"w",encoding="utf-8").write(t); print("ok")
