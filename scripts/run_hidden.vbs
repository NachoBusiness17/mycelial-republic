' run_hidden.vbs — estate hidden task launcher (2026-10-05)
' Cure for headed windows: Task Scheduler tasks with LogonType Interactive pop a
' console on the operator's desktop every fire. Point the task action at this
' script instead:  wscript.exe //B //Nologo run_hidden.vbs <exe> [args...]
' Runs the command with window style 0 (fully hidden, no flash) and WAITS so
' MultipleInstances policy and Last Run Result keep working. Exit code passes
' through from the child.
' Precedent: watch/docker_watchdog.vbs, watch/vast_bargain_loop.vbs (same shape).
Dim sh, cmd, i
Set sh = CreateObject("WScript.Shell")
If WScript.Arguments.Count = 0 Then WScript.Quit 2
cmd = """" & WScript.Arguments(0) & """"
For i = 1 To WScript.Arguments.Count - 1
  cmd = cmd & " """ & WScript.Arguments(i) & """"
Next
WScript.Quit sh.Run(cmd, 0, True)
