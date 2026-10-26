# Push staged moto-cron tree once SSH key auth works.
# Usage: powershell -File watch\inbox\moto_cron\stage\push_to_moto.ps1 -User <termux_whoami>
param(
  [Parameter(Mandatory = $true)][string]$User,
  [string]$HostIp = "100.102.34.118",
  [int]$Port = 8022,
  [string]$IdentityFile = "$env:USERPROFILE\.ssh\id_ed25519"
)
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$srcBin = Join-Path $here "moto-cron\bin"
$bootSrc = Join-Path $here "moto-cron\termux-boot-moto-cron.sh"
$target = "${User}@${HostIp}"
$sshBase = @("-p", "$Port", "-o", "BatchMode=yes", "-o", "ConnectTimeout=15", "-o", "IdentitiesOnly=yes", "-i", $IdentityFile)
Write-Host "SSH mkdir..."
& ssh @sshBase $target "mkdir -p ~/moto-cron/jobs ~/moto-cron/running ~/moto-cron/done ~/moto-cron/failed ~/moto-cron/logs ~/moto-cron/bin"
Write-Host "SCP scripts..."
& scp -P $Port -o BatchMode=yes -o IdentitiesOnly=yes -i $IdentityFile `
  (Join-Path $srcBin "poller.sh") (Join-Path $srcBin "heartbeat.sh") (Join-Path $srcBin "start.sh") $bootSrc `
  "${target}:~/moto-cron/bin/"
# move boot script out of bin on remote
& ssh @sshBase $target "mv ~/moto-cron/bin/termux-boot-moto-cron.sh ~/moto-cron/termux-boot-moto-cron.sh 2>/dev/null; chmod +x ~/moto-cron/bin/*.sh; bash ~/moto-cron/bin/start.sh"
$bootCheck = & ssh @sshBase $target 'if [ -d "$HOME/.termux/boot" ]; then cp "$HOME/moto-cron/termux-boot-moto-cron.sh" "$HOME/.termux/boot/moto-cron.sh"; chmod +x "$HOME/.termux/boot/moto-cron.sh"; echo boot_script=installed; else echo boot_script=skipped_no_termux_boot_dir; fi'
Write-Host $bootCheck
Write-Host "Verify:"
& ssh @sshBase $target "ls -la ~/moto-cron/bin; echo ---; cat ~/moto-cron/heartbeat 2>/dev/null || echo heartbeat_pending; echo ---; head -n 5 ~/moto-cron/logs/*.nohup.log 2>/dev/null || true"
