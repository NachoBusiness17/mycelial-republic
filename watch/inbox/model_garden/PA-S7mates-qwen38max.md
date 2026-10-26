# PA-S7mates-qwen38max (qwen/qwen3.8-max-prime @ nous, turn 1, channel: content)

## 1. Dead mate: external signature and detection latency

- The `.claim` sidecar is created empty at `00__run_mate.ps1:82` (CreateNew) and receives its only content at line 122, after opencode exits.
- `runner_$Today.log` gets a START line at line 111 and an END line at line 123.
- A dead mate (crash, OOM kill, host failure) leaves: an empty `.claim` file, a START with no matching END in the dispatch log, and a RunLog that stops mid-stream.
- Detection latency is unbounded. Line 30-31: "No timeout on opencode." No watchdog polls the `.claim` files or the dispatch log. The only observer is a human who happens to look.

## 2. Diverging mate: stuck loop and key leak

**Stuck loop:**
- opencode runs forever (line 30, no timeout). RunLog grows without bound (line 114, Add-Content per output line). RAM grows with the process. No ceiling enforced in-script; the RAM gate in `01__mates.yaml` is a prompt-level law, not a code check.

**Key leak:**
- Keys enter the process env at line 64 (`Set-Item -Path ("Env:" + $name)`).
- Line 56 comment confirms: "opencode snapshots shell env into its session store."
- The `2>&1` redirect at line 112 captures all stdout and stderr into RunLog with zero redaction.
- If the mate's LLM output echoes env (the exact failure mode the mates.yaml law at "NEVER dump environment variables" addresses), the key lands verbatim in `logs/mates/runs/run_*.log`.
- The law is prompt-level only. No post-hoc scan, no output filter, no redaction hook on the RunLog path.

## 3. Deliverable: 10-line heartbeat (drop into run_mate.ps1 after line 111)

```powershell
$HeartbeatFile = Join-Path $MatesDir "heartbeat_$MateId.json"
$HeartbeatJob = Start-Job -ScriptBlock {
    param($HB, $PID)
    while (Get-Process -Id $PID -ErrorAction SilentlyContinue) {
        Set-Content -Path $HB -Value (@{pid=$PID;ts=(Get-Date -Format 'o');ram=(Get-Process -Id $PID).WorkingSet64} | ConvertTo-Json) -Encoding utf8
        Start-Sleep -Seconds 30
    }
} -ArgumentList $HeartbeatFile, $PID
```

External monitor checks: if `heartbeat_<mate>.json` is older than 90 seconds, the mate is dead or stuck.

**Falsifier:** if the heartbeat job itself is killed by the same OOM event that kills opencode, this design fails. Mitigation: run the heartbeat as a separate scheduled task outside the mate's process tree.
