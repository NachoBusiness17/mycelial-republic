# ONE-CLICK ZERO-BLINK FIX - rewrap the last 4 headed tasks (elevated)
# Triggered via Start-Process -Verb RunAs; the operator clicks UAC once.
$ErrorActionPreference = 'Continue'
$vbs = 'C:\Users\foste\Documents\projects\local_sovereign_agent\scripts\run_hidden.vbs'
$log = 'C:\Users\foste\Documents\projects\local_sovereign_agent\logs\zero_blink_admin_fix.log'

function Wrap($name, $inner) {
    try {
        $a = New-ScheduledTaskAction -Execute 'wscript.exe' -Argument ('//B //Nologo "' + $vbs + '" ' + $inner)
        Set-ScheduledTask -TaskName $name -Action $a -ErrorAction Stop | Out-Null
        Add-Content $log ("FIXED " + $name)
    } catch {
        Add-Content $log ("FAIL " + $name + " : " + $_.Exception.Message)
    }
}

$innerCua = 'powershell.exe -NoProfile -WindowStyle Hidden -NonInteractive -Command "Start-Process -FilePath ''C:\Users\foste\AppData\Local\Programs\Cua\cua-driver\bin\cua-driver.exe'' -ArgumentList ''serve'' -WindowStyle Hidden -WorkingDirectory ''C:\Users\foste''"'

Wrap 'MagCheckpointV2Hourly' 'powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File C:\Users\foste\Documents\projects\local_sovereign_agent\scripts\checkpoint_v2_hourly.ps1'
Wrap 'MagHermesBurn247' 'cmd /c C:\Users\foste\hermes247_headless.cmd'
Wrap 'MagGstdDrainDaily' 'C:\Users\foste\gstddrain_headless.cmd'
Wrap 'cua-driver-serve' $innerCua

Add-Content $log '--- gate after fix ---'
$gate = & 'C:\Users\foste\Documents\projects\local_sovereign_agent\.venv\Scripts\python.exe' 'C:\Users\foste\Documents\projects\local_sovereign_agent\tools\zero_blink_gate.py' 2>&1
Add-Content $log ($gate -join "`r`n")
Add-Content $log '--- done ---'
