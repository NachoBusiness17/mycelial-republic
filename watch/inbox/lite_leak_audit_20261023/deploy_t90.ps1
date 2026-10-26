param($AuditDir,$BobKey)
$ErrorActionPreference = "Continue"
Write-Host "STEP scp bob"
scp -i $BobKey -o BatchMode=yes -o IdentitiesOnly=yes "$AuditDir\lkm.py" "etfag@100.125.103.60:C:/Users/etfag/AppData/Local/Temp/lkm_audit.py"
Write-Host "scp_bob=$LASTEXITCODE"
Write-Host "STEP scp t90"
ssh -i $BobKey -o BatchMode=yes -o IdentitiesOnly=yes etfag@100.125.103.60 "scp -i %USERPROFILE%\.ssh\pixel_lane -P 8022 -o BatchMode=yes -o IdentitiesOnly=yes %TEMP%\lkm_audit.py u0_a235@100.72.38.3:/data/data/com.termux/files/usr/tmp/lkm_audit.py"
Write-Host "scp_t90=$LASTEXITCODE"
$inv = 'export PREFIX=/data/data/com.termux/files/usr; ls -la $PREFIX/tmp/lkm_audit.py; whoami; date; echo PRIOR; find $HOME $PREFIX/tmp -maxdepth 3 \( -name lkm\* -o -name \*leak\*audit\* -o -name scan_key\* \) 2>/dev/null; echo LITE; ls -la $HOME/lite-caller 2>&1 | head -40; echo KEYGONE; ls -la $HOME/lite-caller/.zai_lite_key $HOME/lite-caller/.last.json 2>&1; echo HB; ls -la $HOME/lite-caller/heartbeat.log $HOME/lite-caller/parse.py $HOME/lite-caller/heartbeat.sh 2>&1; echo HIST; ls -la $HOME/.bash_history 2>&1; wc -c $HOME/.bash_history $HOME/lite-caller/heartbeat.log 2>/dev/null'
# Write inv to bob then run
$invB64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($inv))
ssh -i $BobKey -o BatchMode=yes -o IdentitiesOnly=yes etfag@100.125.103.60 "cmd /c echo $invB64> %TEMP%\inv.b64 & powershell -NoProfile -Command \"$b=[IO.File]::ReadAllText($env:TEMP+'\inv.b64').Trim(); $c=[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($b)); $c | ssh -i $env:USERPROFILE\.ssh\pixel_lane -p 8022 -o BatchMode=yes -o IdentitiesOnly=yes u0_a235@100.72.38.3 'sh -s'\""
