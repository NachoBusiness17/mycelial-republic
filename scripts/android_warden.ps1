# android_warden.ps1 — keeps the headless android bodies alive.
# Fleet law fit: loopback-only (adb binds 127.0.0.1), headless (no GUI),
# restart-on-exit, logs to watch/. NOT a scheduled task; started by a seat
# or the day-drive rig, and safe to run alongside mag-docker-watchdog.
# redroid-in-docker is BLOCKED on this Win10 host (no /dev/kvm in WSL2) —
# receipted in watch/ANDROID_EMULATOR_SELF_STEAL_20260904.md. These host
# bodies are the sanctioned exception (AutoClaw precedent).

$Sdk = "$env:LOCALAPPDATA\Android\Sdk"
$Emu = "$Sdk\emulator\emulator.exe"
$Adb = "$Sdk\platform-tools\adb.exe"
$Wanted = @("medium_phone", "watcher_2")
$Log = "C:\Users\foste\Documents\projects\local_sovereign_agent\watch\android_warden.log"

function Log($m) { Add-Content -Path $Log -Value "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $m" }

Log "warden start: wanted = $($Wanted -join ', ')"

while ($true) {
    try {
        & $Adb start-server 2>$null | Out-Null
        $running = @()
        $lines = (& $Adb devices) -match "emulator-\d+\s+device"
        foreach ($line in $lines) {
            $serial = ($line -split "\s+")[0]
            $name = (& $Adb -s $serial emu avd name 2>$null | Select-Object -First 1)
            if ($name) { $running += $name.Trim() }
        }
        foreach ($w in $Wanted) {
            if ($running -notcontains $w) {
                Log "starting $w (headless)"
                Start-Process -FilePath $Emu -ArgumentList `
                    "-avd", $w, "-no-window", "-no-audio", "-no-boot-anim", `
                    "-gpu", "swiftshader_indirect", "-no-snapshot-save" `
                    -WindowStyle Hidden
                Start-Sleep -Seconds 25
            }
        }
    } catch {
        Log "warden error: $_"
    }
    Start-Sleep -Seconds 30
}
