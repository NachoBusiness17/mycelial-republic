# PA-S7mates-gemma4 (gemma4:latest @ local ollama, channel: lane-local-script)

### MATE PROTOCOL AUDIT: STRANGER VIEWPOINT

**Deliverable:** Operational Guardrails Patch (Patch to `run_mate.ps1` and `mates.yaml` logic)
**Falsifier:** The system permits a silent, sustained period (e.g., 48 hours) of successful, low-volume, "honest no-op" calls that consume process time but generate no substantive exit code or new artifact beyond the hourly minimum log pulse.

***

#### (1) Dead Mate Appearance

A dead mate appears as an absence of expected artifacts. The external signature is primarily circumstantial evidence of non-completion.

*   **Appearance:** The mate fails to create the required final receipt and does not update its own `.claim` sidecar with the final exit status. The `run_mates.ps1` runner expects the outcome to be appended to the `.claim` sidecar (line 70-74). A failure to update or a premature termination before these lines execute is the primary indicator.
*   **Detection Timeline:** Noticeable within one full expected cycle (24-48 hours). The runner’s log file (`logs\mates\runs\*_<mate>.log`, line 49) will show a cessation of activity without a corresponding `END mate=...` log entry, or the status check of the claim sidecar reveals an incomplete record.

#### (2) Diverging Mate Appearance

A diverging mate deviates from the established `Seed Thread` parameters in perpetuity.

*   **Stuck Loop:** The process will enter a high-volume, unchanging logging pattern in the run directory (`logs\mates\runs\*_<mate>.log`, line 53). The unique content logged to the run log will repeat without consuming new context or advancing the journey, and the CPU usage will remain high but the corpus utilization curve will flatten instantly.
*   **Key Leakage:** A failure to adhere to the `MINIMAL-EXPOSURE LAW` (line 42) would cause the mate to inadvertently log full environment variables (e.g., `ZAI_API_KEY`) into the final receipt or run log. The manual review of the journaled transcript for variable names not explicitly required by the `Contract` section (line 35) is the guardrail.

#### (3) 10-Line Heartbeat Specification

Heartbeats must prove the mate is actively solving **new** context edge problems, not merely repeating prior work.

```powershell
# Heartbeat.ps1 (Insertion point: Before $Prompt definition, line 60)
# 1. Test-Connection -ComputerName "127.0.0.1" -Count 1 | Out-Null
# 2. Get-Process -Name $ProcessName | Select-Object -ExpandProperty Id
# 3. $RunCycle = Get-Date -Format "yyyyMMdd-HHmmss"
# 4. $HeartbeatFile = Join-Path $RunsDir "hb_$MateId"
# 5. Write-Host "Heartbeat Pulse: $RunCycle."
# 6. Add-Content -Path $HeartbeatFile -Value "$RunCycle successful check-in." -Encoding utf8
# 7. Get-ChildItem $MissionsDir | Where-Object { $_ -LastWriteTime -lt $_.LastWriteTime.AddDays(-3) }
# 8. | Measure-Object | Select-Object -ExpandProperty Count
# 9. Write-MateLog "Heartbeat check: Found {0} stale missions to re-assess." -f { . }
# 10. opencode run --heartbeat-context-only $Prompt
```
