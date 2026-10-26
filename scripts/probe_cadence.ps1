# probe_cadence.ps1 - one water-computer beat per fire (MagProbeCadence, every 10 min).
# The 10-min cadence IS the window timing: free-tier per-model windows refill in
# ~1-2 min, so a drip of 1 cycle per model per beat never bursts a window.
$repo = "C:\Users\foste\Documents\projects\local_sovereign_agent"
$py = "$repo\.venv\Scripts\python.exe"
$log = "$repo\logs\geometric_probe.log"
Add-Content $log ("{0} BEAT START" -f (Get-Date -Format o))
& $py "$repo\tools\geometric_probe.py" --water >> $log 2>&1
Add-Content $log ("{0} BEAT END exit={1}" -f (Get-Date -Format o), $LASTEXITCODE)
