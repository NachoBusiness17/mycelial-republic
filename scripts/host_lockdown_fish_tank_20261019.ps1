# FISH_TANK_REMEDIATE_20261019 - run ONCE in an elevated PowerShell (Run as administrator).
# Idempotent. Does not touch sshd service, mag-sovereign, or any secrets.
$ErrorActionPreference = 'Continue'
"== BEFORE =="; netsh interface portproxy show all
# A2: drop dashboard portproxy 8765 (no repo script re-adds it; registry key cleared by delete)
netsh interface portproxy delete v4tov4 listenport=8765 listenaddress=0.0.0.0
# A3: sshd - allow 22 only from loopback + tailnet; disable any other inbound allow on 22
Get-NetFirewallPortFilter -Protocol TCP | ? LocalPort -eq '22' | Get-NetFirewallRule | ? { $_.Direction -eq 'Inbound' -and $_.Action -eq 'Allow' -and $_.Name -ne 'MAG-sshd-tailnet' } | % { "disabling $($_.Name) ($($_.DisplayName))"; Disable-NetFirewallRule -Name $_.Name }
if (-not (Get-NetFirewallRule -Name 'MAG-sshd-tailnet' -EA SilentlyContinue)) { New-NetFirewallRule -Name 'MAG-sshd-tailnet' -DisplayName 'MAG sshd tailnet only (fish tank 20261019)' -Direction Inbound -Protocol TCP -LocalPort 22 -Action Allow -RemoteAddress 100.64.0.0/10,fd7a:115c:a1e0::/48,127.0.0.1 -Profile Any | Out-Null }
# A1 belt+braces: block LAN to Ollama even if OLLAMA_HOST regresses
Get-NetFirewallPortFilter -Protocol TCP | ? LocalPort -eq '11434' | Get-NetFirewallRule | ? { $_.Direction -eq 'Inbound' -and $_.Action -eq 'Allow' } | % { "disabling $($_.Name)"; Disable-NetFirewallRule -Name $_.Name }
# A4: gstd-node :8080 - compose files are gone so it cannot be rebound in place; block LAN inbound (loopback unaffected)
if (-not (Get-NetFirewallRule -Name 'MAG-block-lan-8080' -EA SilentlyContinue)) { New-NetFirewallRule -Name 'MAG-block-lan-8080' -DisplayName 'MAG block LAN to gstd-node 8080 (fish tank 20261019)' -Direction Inbound -Protocol TCP -LocalPort 8080 -Action Block -RemoteAddress LocalSubnet,192.168.0.0/16,10.0.0.0/8,172.16.0.0/12 -Profile Any | Out-Null }
"== AFTER =="; netsh interface portproxy show all
Get-NetFirewallRule -Name 'MAG-*' | ft Name,Enabled,Action
