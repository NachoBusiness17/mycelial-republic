' vast_bargain_loop.vbs — hidden launcher for the $0 vast bargain watcher
' (same headless pattern as watch/docker_watchdog.vbs, operator law: never pop windows)
CreateObject("Wscript.Shell").Run """" & CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName) & "\vast_bargain_loop.cmd""", 0, False
