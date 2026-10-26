import subprocess, sys, os
from concurrent.futures import ThreadPoolExecutor
R=["FOUCAULT","FERMAT","ELLUL","BERNAYS","MCLUHAN","JUNG","HALL","WALLAS","BAUDRILLARD","PLATO_KIRK","DIOGENES","FREUD"]
D=os.path.dirname(os.path.abspath(__file__))
def go(a): 
    r=subprocess.run([sys.executable,os.path.join(D,"run_lane.py"),"who_we_are",a[0],a[1]],capture_output=True,text=True); open(os.path.join(D,"batch1.log"),"a").write(r.stdout+r.stderr[-300:])
with ThreadPoolExecutor(4) as f1, ThreadPoolExecutor(3) as f2:
    list(f1.map(go,[(r,"fostertron_max") for r in R])); list(f2.map(go,[(r,"agy_pc") for r in R[1:]]))
open(os.path.join(D,"batch1.log"),"a").write("DONE\n")
