# Grok 4.5 advice on RIB_RUNAWAY_PYTHON

model=grok-3-mini

1. CIM attribution (no psutil):  
Query `Win32_Process` with `Get-CimInstance`, follow `ParentProcessId` upward to first non-python ancestor. Use:  
```powershell
Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Select-Object ProcessId,ParentProcessId,CommandLine
```  
Build tree via recursive ParentProcessId walk; store root PID + MAG_SOURCE env as canonical key. This is stricter than per-parent 1:1 and survives shim/uv pairs.

2. seat-exit=-1 root fix:  
Spawn uv python directly from ghost/supervisor (bypass venv shim entirely). Change spawners to:  
`uv run --python-preference system python -m mag...`  
or hardcode the uv python.exe path. This eliminates the double-PID + reap mismatch.

3. Sentinel kill:  
Use source-tree only: `taskkill /PID <root> /T /F`. Never blanket `/IM python.exe`. Wire the root from the CIM tree walk above.

4. Structural vs dedup:  
Make doubling impossible: all launch paths must exec the uv python.exe directly (no venv/Scripts/python.exe shim). Remove or replace the venv entry point; keep flocking dedup only as belt-and-suspenders.
