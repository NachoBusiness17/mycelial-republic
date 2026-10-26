# CLEAN RUNBOOK - disk-storm ponytail, operator-GO-gated - 2026-10-09

Lane E deliverable. Numbers basis: corrected measurement pack 2026-10-09T01:28Z
(evidence_pack/digest.md + evidence_pack/exec_forensics.json), superseding the older
~300GB estimate in state/DISK_CRISIS_20261008_CLOSE.md. Exec forest: 11,079 files,
309.12GiB; 7d retention prize 81.22GiB today, growing ~228GiB more within a week.
Free now: 167.3GB.

## HARD RULES (read before touching anything)

1. ONE disk-bound process at a time; never run smith concurrent with a purge.
2. NO deletions while dwf actors live: fleet schtasks stay Disabled through P1-P3 AND no sess_dwf-* exec dir written in the last 15 min (gate in P1).
3. EVERY phase banks a receipt under watch/inbox/disk_audit_20261009/cleanup/.
4. If ANY precondition fails: STOP, file cleanup/BLOCK_<phase>.md; never improvise around a gate.
5. Purges run dry-run first; the dry-run total must match the expected class before --apply.
6. Destructive phases fire only on operator GO. Plain hyphens only (repo lint law).
7. Proof: one tools\disk_smith.py row per phase boundary into logs/disk_smith.jsonl; consecutive-row deltas are the proof; PRE-FLIGHT banks the BEFORE row.

## PRE-FLIGHT (seat, before P0)

```powershell
New-Item -ItemType Directory -Force watch\inbox\disk_audit_20261009\cleanup
.\.venv\Scripts\python.exe tools\disk_smith.py                # banks the BEFORE row
df -h /c                                                      # expect ~167.3GB free
schtasks /Query /TN MagFreeLaneFleet     # must read Status: Disabled
schtasks /Query /TN MagHermesBurn247     # must read Status: Disabled
schtasks /Query /TN MagGauntletFree30    # must read Status: Disabled
```
Gate: cleanup/ exists, BEFORE row banked, all three tasks Disabled.

## P0 - admin prerequisites (operator-run, elevated) - expected ~114GB class

P0.1 AV exclusions FIRST (the IO-storm fix). Roots exactly as the close doc lists
them; it says "five seats" but names four. A fifth (AppData\Local\Temp) is an
operator call: temp holds untrusted downloads, exclusion widens attack surface.
```powershell
Add-MpPreference -ExclusionPath "C:\Users\foste\Documents\projects\local_sovereign_agent"
Add-MpPreference -ExclusionPath "C:\Users\foste\.zcode"
Add-MpPreference -ExclusionPath "C:\Users\foste\.ollama"
Add-MpPreference -ExclusionPath "C:\Users\foste\AppData\Local\hermes"
Get-MpPreference | Select-Object -ExpandProperty ExclusionPath    # receipt line
```
P0.2 fixed-size pagefile 32-48GB (kills the balloon class): 40GB fixed, applies on
reboot, expected ~24GB back (pagefile.sys 63.95GB now per smith alert, 135GB at
crisis per close doc).
```powershell
Set-CimInstance -Query "SELECT * FROM Win32_ComputerSystem" -Property @{AutomaticManagedPagefile=$false}
Set-CimInstance -Query "SELECT * FROM Win32_PageFileSetting WHERE Name='C:\\pagefile.sys'" -Property @{InitialSize=40960;MaximumSize=40960}
```
P0.3 docker vhdx compact (vhdx 132.05GB, ~40GB live, ~90GB dead):
```powershell
# 1. quit Docker Desktop from the tray (or: Stop-Process -Name "Docker Desktop","com.docker.backend" -Force)
wsl --shutdown
# 2. admin PowerShell:
Optimize-VHD -Path "C:\Users\foste\AppData\Local\Docker\wsl\disk\docker_data.vhdx" -Mode Full
# 3. start Docker Desktop, compose the stacks back up
```
P0.4 reboot (pagefile applies, stragglers clear), then re-run PRE-FLIGHT gates.
Safety gate: elevated shell, nothing else disk-bound.
Rollback: pagefile = re-set AutomaticManagedPagefile $true; AV =
Remove-MpPreference -ExclusionPath <root> per root; vhdx compact has no rollback
(it only reclaims dead space, live container data untouched).
Proof: smith row before P0.1 vs after the P0.4 reboot (vhdx + pagefile columns).
Receipt: cleanup/P0_ADMIN.md (exclusion list + before/after sizes).

## P1 - giant-junk pass - expected ~100GiB class (estimate; top 8 alone 64.16GiB)

The giants are junk by content class: accidental full-disk `find /c` listings and
FINDSTR error loops. Delete exec files >1GiB whose first 2KB matches that signature
- independent of age, gated on content. Preconditions: PRE-FLIGHT gates green, and:
```powershell
Get-ChildItem C:\Users\foste\.zcode\cli\exec -Directory -Filter "sess_dwf*" | Where-Object { $_.LastWriteTime -gt (Get-Date).AddMinutes(-15) } | Measure-Object | Select-Object -ExpandProperty Count
# MUST print 0. Eyeball for sibling actors too:
Get-Process | Where-Object { $_.ProcessName -match "zcode|node|python" } | Select-Object ProcessName,Id,StartTime
```
Save as cleanup/exec_purge.py (containment guard = harvest_exec_forest.py
safe_child pattern; dry-run default, prints list + total; --retention = age gate):
```python
import re, sys, time
from pathlib import Path
EXEC = Path(r"C:\Users\foste\.zcode\cli\exec"); DAY = 86400.0; now = time.time()
def inside(p):  # containment guard, harvest_exec_forest.py safe_child pattern
    try: return p.resolve().is_relative_to(EXEC.resolve())
    except OSError: return False
def junk(head):  # find-dump listing or FINDSTR-error loop, judged on first 2KB
    ls = [l for l in head.decode("latin1", "ignore").splitlines() if l.strip()][:32] or [""]
    pat = re.compile(r"^([A-Za-z]:[\\/]|/c/)?[\w.\- ]+([\\/][\w.\- ]+)+$")
    return sum("findstr:" in l.lower() for l in ls) >= .5*len(ls) or sum(bool(pat.match(l)) for l in ls) >= .8*len(ls)
def read2k(p):
    with open(p, "rb") as f: return f.read(2048)
mode = "retention" if "--retention" in sys.argv else "giants"; kill, tot = [], 0
for p in EXEC.rglob("*"):
    try:
        if not inside(p) or not p.is_file(): continue
        st = p.stat()
        if mode == "giants" and (st.st_size <= 2**30 or not junk(read2k(p))): continue
        if mode == "retention" and now - st.st_mtime < 7 * DAY: continue
    except OSError: continue
    kill.append((st.st_size, str(p))); tot += st.st_size
for b, p in sorted(kill, reverse=True): print(f"{b/2**30:8.2f} GiB {p}")
print(f"total {tot/2**30:.2f} GiB / {len(kill)} files ({'APPLY' if '--apply' in sys.argv else 'DRY-RUN'})")
if "--apply" in sys.argv:
    for b, p in kill: Path(p).unlink()
```
```powershell
.\.venv\Scripts\python.exe watch\inbox\disk_audit_20261009\cleanup\exec_purge.py > watch\inbox\disk_audit_20261009\cleanup\P1_dryrun.txt
# GO only after every listed file reads as path-dump / FINDSTR loop AND total is ~100GiB class:
.\.venv\Scripts\python.exe watch\inbox\disk_audit_20261009\cleanup\exec_purge.py --apply > watch\inbox\disk_audit_20261009\cleanup\P1_apply.txt
.\.venv\Scripts\python.exe tools\disk_smith.py
```
Safety gate: dwf count 0 + fleet Disabled + dry-run list is 100% signature junk.
Rollback: none possible (irreversible); the banked dry-run list is the record;
exec logs are cache per the shared-surface contract, durable work lives in repo
receipts. Proof: smith row delta ~= dry-run total.
Receipt: cleanup/P1_GIANT_JUNK.md (dry-run + apply totals + smith delta).

## P2 - retention purge (mtime older than 7d) - expected 81.22GiB today

Basis: age histogram d7_14 78.12 + d14_30 3.09 + gt30d 0.01 = 81.22GiB
(evidence_pack/digest.md). Same script with --retention (age gate only); bank the
FRESH number - 81.22GiB-class minus any 7d+ giants P1 already took.
```powershell
.\.venv\Scripts\python.exe watch\inbox\disk_audit_20261009\cleanup\exec_purge.py --retention > watch\inbox\disk_audit_20261009\cleanup\P2_dryrun.txt
.\.venv\Scripts\python.exe watch\inbox\disk_audit_20261009\cleanup\exec_purge.py --retention --apply > watch\inbox\disk_audit_20261009\cleanup\P2_apply.txt
.\.venv\Scripts\python.exe tools\disk_smith.py
```
Younger buckets (d3_7 168.97 + d1_3 50.11 + lt1d 8.82 = ~228GiB, same digest) age
past 7d within a week, so the prize grows toward ~300GiB only if this runs daily -
wire it into the retention law (Lane D spec), do not one-shot it.
Safety gate: same dwf/fleet gates as P1; fresh dry-run banked before apply.
Rollback: none (cache class, same as P1). Proof: smith row delta ~= fresh total.
Receipt: cleanup/P2_RETENTION.md.

## P3 - HF purge - expected ~58.2GB (20 + 16 + 16 + 6.2 per the close doc)

Targets under C:\Users\foste\.cache\huggingface\hub (names verified on disk):
models--unsloth--gemma-4-31B-it-GGUF (20G), models--slashreboot--saelis-31b (16G),
models--Qwen--Qwen3-8B (16G), models--google--tabfm-1.0.0-pytorch (6.2G).
STEP 1 bank the re-download manifest BEFORE deleting (model id + pinned revision):
```powershell
$h = "C:\Users\foste\.cache\huggingface\hub"
$targets = "models--unsloth--gemma-4-31B-it-GGUF","models--slashreboot--saelis-31b","models--Qwen--Qwen3-8B","models--google--tabfm-1.0.0-pytorch"
$m = "watch\inbox\disk_audit_20261009\cleanup\HF_REDOWNLOAD_MANIFEST.md"
foreach ($t in $targets) {
  $repo = ($t -replace "^models--","") -replace "--","/"
  $rev  = (Get-Content "$h\$t\refs\main" -ErrorAction Stop).Trim()
  Add-Content $m "repo: $repo | revision: $rev | dir: $t"
}
Get-Content $m   # receipt check: four rows, each carrying a hex revision
```
STEP 2 delete, only after the manifest check passes:
```powershell
foreach ($t in $targets) { Remove-Item -Recurse -Force "$h\$t" }
.\.venv\Scripts\python.exe tools\disk_smith.py
```
Safety gate: manifest exists with four revision-bearing rows BEFORE any delete.
Rollback: huggingface-cli download <repo> --revision <rev> per manifest row restores
the exact snapshot.
Proof: smith row delta ~58GB. Receipt: cleanup/P3_HF_PURGE.md (manifest + deletes).

## P4 - re-enable the fleet - expected 0 GiB (re-adds load, frees nothing)

```powershell
schtasks /Change /TN MagFreeLaneFleet /ENABLE
schtasks /Change /TN MagHermesBurn247 /ENABLE
schtasks /Change /TN MagGauntletFree30 /ENABLE
schtasks /Query /TN MagFreeLaneFleet     # Enabled / Ready
schtasks /Query /TN MagHermesBurn247     # Enabled / Ready
schtasks /Query /TN MagGauntletFree30    # Enabled / Ready
```
Safety gate: only AFTER P2 retention is landed, smith free-gb well above the 15GB
floor, and P0.1 AV exclusions in place (else the fleet re-creates the IO storm).
NOT part of P4: the ZCode-side hourly free-burn churn was DELETED 2026-10-09 during
the freeze; its verbatim restore recipe is banked in
watch/inbox/disk_audit_20261009/CRON_FREEZE_20261009.md and stays down until the
operator gives GO after the retention law lands.
Rollback: `schtasks /Change /TN <name> /DISABLE` x3.
Proof: query output + smith row (mild free-gb drop as the fleet resumes is honest
load; watch it against the floor). Receipt: cleanup/P4_REENABLE.md.

## P5 - verification - expected 0 GiB (this phase IS the receipt)

```powershell
.\.venv\Scripts\python.exe tools\disk_smith.py                 # the AFTER row
.\.venv\Scripts\python.exe tools\disk_smith.py --history 8     # the whole strip
df -h /c
```
PRE-FLIGHT row = BEFORE; strip delta (free-gb, vhdx, pagefile columns) is the
sequence receipt. Expected free-gb gain across P0-P3: ~353GB class (114 + 100 + 81
+ 58) on top of 167.3GB at start, i.e. free after in the 480-520GB class. Any phase
whose smith delta disagrees with its banked dry-run total by more than a few GB
gets named in its receipt - never quietly re-run.
Safety gate: n/a (read-only). Rollback: n/a. Proof: this phase is the proof.
Receipt: cleanup/P5_VERIFY.md (BEFORE row, AFTER row, delta table, df output).

Order: PRE-FLIGHT -> P0 (operator, admin, reboot) -> P1 -> P2 -> P3 -> P4 -> P5;
serial, one disk process at a time, operator GO before each destructive phase.
