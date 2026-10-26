# PA-S7mates-kimik2 (moonshotai/kimi-k2 @ nous, turn 1, channel: content)

(1) A dead mate leaves a .claim file created at run_mate.ps1:82-84 but never appended with a verdict, because run_mate.ps1:122 writes the verdict only after opencode returns; instrument is a file listing of logs\mates\missions showing a .claim sidecar with zero bytes or lacking the trailing mate=... line, observed after the START timestamp logged at run_mate.ps1:111 but before any END at run_mate.ps1:123. Detection latency equals the operator's polling interval because run_mate.ps1:30-31 removes timeouts and there is no heartbeat organ.

(2) A stuck loop keeps the opencode process alive (visible in Get-Process) while the run log ceases growth at run_mate.ps1:114 and the claim file never receives the verdict at run_mate.ps1:122; instrument is run log size sampled twice, context assumption is the process table still shows the PID logged at run_mate.ps1:111. A key leak appears as substrings matching ZAI_API_KEY or ZAI_API_KEY_2 (the whitelisted names at run_mate.ps1:61) inside the run log produced by run_mate.ps1:112-116, violating mates.yaml:17-20; instrument is Select-String on the UTF-8 run log.

(3) Heartbeat - insert before run_mate.ps1:112:
$pulse = Join-Path $RunsDir "pulse_$MateId.txt"
$hb = {
    param($p,$r)
    while ($true) {
        $sz = if (Test-Path $r) { (Get-Item $r).Length } else { 0 }
        "$(Get-Date -Format 'yyyy-MM-ddTHH:mm:ss') sz=$sz" | Out-File $p -Encoding utf8
        Start-Sleep 30
    }
}
$job = Start-Job -ScriptBlock $hb -ArgumentList $pulse,$RunLog

After the pipe block (run_mate.ps1:112-116) add:
Stop-Job $job -ErrorAction SilentlyContinue
Remove-Job $job

Falsifier: if the session exceeds the PS 5.1 job memory tax and Start-Job fails silently, the pulse file never appears and the watcher must fall back to log mtime.
