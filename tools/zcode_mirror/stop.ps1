$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$pid_ = [int](Get-Content "$here\data\zmirror.pid"); Stop-Process -Id $pid_ -Force; "stopped $pid_"
