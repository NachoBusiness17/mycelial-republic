# T1W2_S7_mates (anthropic/claude-opus-5.5, turn 1, channel: content)

# Stranger Audit: run_mate.ps1 Liveness

**Line numbers:** I counted them from the pasted evidence, not from disk.
**The ~20GB RAM figure:** UNVERIFIED. No instrument, moment, or box state was named.

## (1) What a dead mate looks like

- The runner writes `START ... pid=$PID` (run_mate.ps1:111).
- The outcome is only written after opencode returns (:117-123).
- There is no timeout by design (:30-31).
- If the box kills the process (OOM, task kill), the `.claim` sidecar stays empty, with no `exit=` line ever.
- A hung opencode process looks the same as a thinking mate, because the run log only grows on output (:112-114).

**Time to notice:** unbounded. Nothing reads the claims.

- Positive (noticed): `.claim` contains `exit=2` (:118, :122).
- Negative (invisible): an empty `.claim` with the pid gone.

## (2) What a diverging mate looks like

**Stuck loop**
- The run log keeps growing with the same lines repeated.
- No receipt appears in `watch\inbox\mates_leave_protocol\receipts\` (:107).

**Key leak**
- The keys sit in the process env (:64).
- opencode stdout and stderr are copied to the log verbatim (:112-114).
- "Values never logged" (:57) covers only the runner's own lines.
- mates.yaml:19 says the redaction hook does not cover transcripts.
- Result: a mate running `env` writes the live key into `run_*.log`.

## (3) Heartbeat: `scripts/mate_heartbeat.ps1`

Constant argv, no parameters (:3-12 law). Run it from a scheduled task every 5 minutes.

```powershell
$Root=Split-Path $PSScriptRoot -Parent; $T=Get-Date -Format yyyyMMdd; $M="$Root\logs\mates"; $HB="$M\heartbeat_$T.log"
$keys=@("ZAI_API_KEY","ZAI_API_KEY_2")|%{(Select-String "$Root\.env" "^\s*$_=(.*)$" -EA 0|select -f 1).Matches.Groups[1].Value.Trim()}|?{$_}
foreach($c in Get-ChildItem "$M\missions\mission_$T*.md.claim" -EA 0){
  if((Get-Content $c.FullName -Raw) -match 'exit='){continue}; $id=$c.Name -replace '^mission_|\.md\.claim$',''; $log="$M\runs\run_$id.log"
  $p=(Select-String "$M\runner_$T.log" "$([regex]::Escape("mission_$id.md")) .*pid=(\d+)" -EA 0|select -l 1).Matches.Groups[1].Value
  $alive=[bool]($p -and (Get-Process -Id $p -EA 0)); $age=if(Test-Path $log){[int]((Get-Date)-(gi $log).LastWriteTime).TotalMinutes}else{-1}
  $rep=(Get-Content $log -Tail 200 -EA 0|?{$_.Trim()}|group|sort Count -desc|select -f 1).Count
  $leak=[bool]($keys|?{Select-String $log -SimpleMatch $_ -Quiet -EA 0})
  $st=if(-not $alive){"DEAD"}elseif($leak){"LEAK"}elseif($age -gt 20 -or $rep -gt 50){"STUCK"}else{"OK"}
  Add-Content $HB "[$(Get-Date -f 'yyyy-MM-dd HH:mm:ss')] $id pid=$p alive=$alive logage_min=$age maxrep=$rep leak=$leak state=$st" -Encoding utf8 }
```

**How it works**
- It reports only the filename and state. Key values are never written.
- It inherits the whitelist pattern (:61).
- Detection time: DEAD and LEAK within 5 minutes, STUCK within 25 minutes.
- The thresholds of 20 minutes and 50 repeats are untuned (UNVERIFIED).

**Falsifier**
1. During a live run, `Stop-Process` one runner pid.
2. The next heartbeat must log `state=DEAD` for that mate.
3. Separately, append a key value to a copy of a run log. The heartbeat must log `state=LEAK`.
4. If either case logs `OK` or nothing, this deliverable fails.
