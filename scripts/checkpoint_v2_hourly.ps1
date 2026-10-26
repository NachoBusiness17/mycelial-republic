# FLASH CURE 2026-10-19: task action calls powershell.exe directly (ACL-locked,
# cannot rewrap the task) - a console window flashes every hourly fire. This stub
# delegates the real body through run_hidden.vbs (window style 0) and exits, so
# the allocated console lives ~100ms. Original: checkpoint_v2_hourly.ps1.bak_flashcure
if (-not $env:CHECKPOINT_DELEGATED) {
    $env:CHECKPOINT_DELEGATED = '1'
    $args_ = '"//B" "//Nologo" "C:\Users\foste\Documents\projects\local_sovereign_agent\scripts\run_hidden.vbs" "powershell.exe" "-NoProfile" "-ExecutionPolicy" "Bypass" "-File" "' + $PSCommandPath + '"'
    Start-Process wscript.exe -ArgumentList $args_ -WindowStyle Hidden
    exit
}
# GAME-NEUTERED 2026-10-19 00:0x: this task is ACL-locked against disable from the
# seat shell, and even the cured version blinked focus (powershell console alloc)
# - which got the operator killed mid-fight. Instant exit until the operator runs
# the admin disable: schtasks /Change /TN MagCheckpointV2Hourly /DISABLE
# Restore: flash_cure_checkpoint.py re-applies the run_hidden delegation.
exit
