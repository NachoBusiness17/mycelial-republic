# Starts the daemon detached (WMI-created process, survives the launching shell).
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
New-Item -ItemType Directory -Force "$here\data" | Out-Null
$py = (Get-Command python).Source
$cmd = "cmd.exe /c `"`"$py`" -u `"$here\zmirror_daemon.py`" >> `"$here\data\daemon.log`" 2>&1`""
$r = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine=$cmd; CurrentDirectory=$here}
"wrapper PID $($r.ProcessId); daemon PID -> data\zmirror.pid"
