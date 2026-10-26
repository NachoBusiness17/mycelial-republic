# Cadence organs daily run (rows 3/4/5 of the promise pile): runs the five
# meters organs plus the room_state lightmap render, exactly as specified in
#   watch/inbox/CADENCE_DOOR_SPEC_20261010_locksmith.md (5 lines)
#   watch/inbox/ROOM_STATE_DOOR_SPEC_20261012_locksmith.md (1 line)
#
# Consumer: the MagCadenceOrgansDaily scheduled task, registered by
#   scripts/register_cadence_organs_task.ps1 (operator-gated; nothing here
#   runs until the operator registers it, per both spec docs).
# Verifier: the locksmith census instruments (Get-ScheduledTask Mag* action
#   dump names the six organs after registration; each organ self-banks its
#   output: pricing_diff and meters_nightly write watch/inbox/index_events.jsonl,
#   memory_gauge appends watch/inbox/MEMORY_GAUGE.jsonl, rotate_kpi archives
#   to attic/kpi/, room_state writes dashboard/static/room_state.json) plus
#   PROMISE_PILE_LEDGER_20261013_locksmith.md rows 3/4/5.
#
# Law-13 design-cite (corrections-design-cite), inherited from the two spec
# docs which are the citation of record:
#   docker-not-desktop: CITED-WITH-EXEMPTION (joins the existing host-process
#     daily-task fleet; no new runtime class).
#   headless-only (also law 48): CITED-AND-COMPLIANT (rides run_hidden.vbs,
#     wscript //B //Nologo, same as MagFtsIndexDaily).
#   one-supervisor (also law 11): CITED-AND-COMPLIANT (one task, one script,
#     no daemon).
#   Egress: pricing_diff self-enforces https-only + host allowlist
#     (tools/pricing_diff.py:61-97); all other organs are local-only.
#
# EXIT-CODE CONTRACT: organs run sequentially, one failure does not stop the
# rest; the script exits nonzero if any organ failed so schtasks Last Result
# carries it. Log: logs/cadence_organs.log (appended each run).
#
# Run now:  powershell -ExecutionPolicy Bypass -File scripts\cadence_organs_daily.ps1
# Register: powershell -ExecutionPolicy Bypass -File scripts\register_cadence_organs_task.ps1

$ErrorActionPreference = "Continue"
$Root = Split-Path $PSScriptRoot -Parent
$Py = Join-Path $Root ".venv\Scripts\python.exe"
$Log = Join-Path $Root "logs\cadence_organs.log"

$Organs = @(
    @{ Name = "meters_nightly";          Args = @("tools\meters_nightly.py") },
    @{ Name = "pricing_diff";            Args = @("tools\pricing_diff.py") },
    @{ Name = "memory_gauge";            Args = @("tools\memory_gauge.py") },
    @{ Name = "provider_snapshot_differ";Args = @("tools\provider_snapshot_differ.py") },
    @{ Name = "rotate_kpi";              Args = @("tools\rotate_kpi.py", "--apply") },
    @{ Name = "room_state";              Args = @("mag\room_state.py", "--window", "200") }
)

$failed = 0
foreach ($o in $Organs) {
    $stamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    $out = & $Py @($o.Args) 2>&1
    $code = $LASTEXITCODE
    $line = "{0} | {1} | exit {2}" -f $stamp, $o.Name, $code
    Add-Content -LiteralPath $Log -Value $line
    if ($code -ne 0) {
        $failed++
        $tail = ($out | Select-Object -Last 5) -join " / "
        Add-Content -LiteralPath $Log -Value ("  FAIL detail: " + $tail)
    }
}

$stamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
Add-Content -LiteralPath $Log -Value ("{0} | summary | {1} of {2} organs failed" -f $stamp, $failed, $Organs.Count)
exit $(if ($failed -gt 0) { 1 } else { 0 })
