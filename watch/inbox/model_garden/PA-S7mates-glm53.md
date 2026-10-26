# PA-S7mates-glm53 (glm-5.3-flash @ zai, turn 1, channel: content)

## STRANGER AUDIT - S7 mates heartbeat

### (1) Dead mate, from outside

Visible signature: the `.claim` sidecar never gets its end line. `run_mate.ps1` appends `exit=$code` to `$Mission.FullName.claim` only after opencode returns (00, lines near "THE FIXED PROMPT TEMPLATE" tail: `Add-Content -Path "$($Mission.FullName).claim" ... $verdict`). A mate killed mid-run (OOM at 20GB, box swap) leaves a claim file with a creation timestamp but no `mate=... pid=... exit=` tail line. Second signature: `Write-MateLog "END mate=..."` missing from `runner_$Today.log`. Third: no receipt lands under `watch\inbox\mates_leave_protocol\receipts\`.

Detection latency today: UNVERIFIED - nothing reads the claims dir. The only passive limit is the box dying. Until a sensor exists, latency is infinite: a mate dead at 08:15 is noticed at the next human look.

### (2) Divergent mate

- Stuck loop: opencode never exits (script has no timeout by law, 00: "No timeout on opencode"), so `run_<...>.log` stops growing in content but the process holds the claim forever. Signature: log file mtime stale (>N min) while claim has no end line.
- Key leak: the runner loads only ZAI_API_KEY/ZAI_API_KEY_2 (00, AUTH FIX block) and the pack forbids env dumps (01, laws block). Divergence = any line in `logs\mates\runs\run_*.log` or a receipt matching `[A-Za-z0-9_-]{30,}` (z.ai key shape). The transcript hook redacts; the run log tee (00, `& $OpenCode run $Prompt 2>&1 | ... Add-Content`) does NOT - it is the unredacted surface.

### (3) Heartbeat - `tools/mate_pulse.ps1` (scheduled every 10 min)

```
$today = Get-Date -Format "yyyyMMdd"
foreach ($c in Get-ChildItem "logs\mates\missions\mission_$today*.md.claim") {
  $body  = Get-Content $c -Raw
  $alive = $body -match "exit="
  $log   = "logs\mates\runs\run_" + ($c.BaseName -replace '^mission_','').TrimEnd('.') + ".log"
  $stale = ((Get-Date) - (Get-Item $log).LastWriteTime).TotalMinutes -gt 30
  $leak  = (Select-String -Path $log -Pattern "[A-Za-z0-9_\-]{40,}" -Quiet)
  if ($alive -and -not $stale -and -not $leak) { continue }
  $why = if ($leak) {"KEYSHAPE"} elseif (-not $alive -and $stale) {"DEAD"} else {"STALL"}
  Add-Content "logs\mates\pulse_$today.log" "$(Get-Date -Format s) $why $($c.BaseName)"
}
```

Conditions: assumes local clock, claim sidecars untouched post-completion, log mtime is opencode activity proxy. Detection latency: 10 min schedule + 30 min staleness window = worst-case ~40 min for DEAD/STALL, 10 min for KEYSHAPE.

**Falsifier:** if a mate completes normally (claim has `exit=`, receipt filed) yet pulse logs DEAD against it on two consecutive runs, the staleness predicate is wrong and the organ is falsified.
