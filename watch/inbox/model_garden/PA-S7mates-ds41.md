# PA-S7mates-ds41 (deepseek-chat @ deepseek, turn 1, channel: content)

**1. Dead mate from outside**

A dead mate leaves: an orphaned `.claim` sidecar with no outcome line appended (run_mate.ps1:104 writes the verdict only after `$LASTEXITCODE` returns), a `logs\mates\runs\run_<...>.log` that stops mid-stream with no `END` line, and a `runner_<date>.log` entry `START mate=X ...` with no matching `END mate=X` (run_mate.ps1:99, 106). PID is in both lines (run_mate.ps1:99): a stranger can `Get-Process -Id <pid>` and get nothing, which is the confirmation.

**How long until we notice: never, today.** Nothing polls. No timeout by law tells the runner to wait forever, and there is no external watcher named in this file. Noticeability = next human reads the missions dir. That is the hole.

**2. Diverging mate**

- Stuck loop: `run_<...>.log` grows monotonically with repeating line shapes; `START` timestamp to `END` timestamp blows past every sibling run for the same day. Detectable by line-hash repeat and wall-clock delta vs peer median.
- Key leak: a line matching the two whitelisted names' values (run_mate.ps1:66-69) appearing in `run_*.log` or in a receipt under `watch\inbox\mates_leave_protocol\receipts\`. The law exists (mates.yaml, "NEVER dump environment variables"), the transcript hook redacts only the trajectory, not this log. An outside observer greps the run log for the loaded values; a hit is the whole alarm.

**3. Ten-line heartbeat** (append per mate, to `logs\mates\heartbeat_<date>.jsonl`)

```powershell
$hb = Join-Path $MatesDir "heartbeat_$Today.jsonl"
function Heartbeat([string]$mate, [string]$state) {
    $row = [ordered]@{
        t     = (Get-Date -Format 'yyyy-MM-ddTHH:mm:ss')
        mate  = $mate
        pid   = $PID
        state = $state                       # start|tick|end|dead
        ramMB = [int]((Get-Process -Id $PID).WorkingSet64/1MB)
        logTailSha = (Get-FileHash $RunLog -Algorithm SHA256).Hash.Substring(0,12)
    }
    Add-Content -Path $hb -Value ($row | ConvertTo-Json -Compress) -Encoding utf8
}
```

Call `Heartbeat $MateId start` after claim, `Heartbeat $MateId tick` on an internal 60s timer (background job inside the runner), `Heartbeat $MateId end` before exit. A separate 2-line watcher: for each mate whose last `t` is older than 180s and whose `state` is not `end`, append `state=dead` and page.

Falsifier for this deliverable: run the 8/8 stretch again; if the heartbeat file contains any mate with `state=dead` under normal completion, or any mate with no `tick` gap over 180s while alive, the design is wrong.
