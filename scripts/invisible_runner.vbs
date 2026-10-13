' invisible_runner.vbs - headless launcher for scheduled tasks (2026-09-30)
'
' WHY: schtasks actions that run .venv\Scripts\python.exe directly each open a
' VISIBLE console window on every fire (operator: "you're launching headed
' python windows" - the 08:00 mates / 08:30 census / 09:00 FTS windows).
' The headless-spawn law (CREATE_NO_WINDOW 0x08000000) covers in-process
' spawns; Task Scheduler needs this wrapper instead: wscript runs the command
' with a zero-window, no console flash.
'
' Usage as a task action:
'   wscript.exe "C:\...\scripts\invisible_runner.vbs" "C:\...\scripts\census_patrol_daily.ps1" [args...]
' It shells the first argument hidden with the rest as arguments, waits, and
' exits with the child's exit code (propagated via WshShell.ExitCode is not
' available in wscript; the code is written to %TEMP%\invisible_runner_rc.log).

Option Explicit
Dim shell, args, i, cmd, first, fso, f
If WScript.Arguments.Count = 0 Then WScript.Quit 2
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
first = WScript.Arguments(0)
cmd = """" & first & """"
For i = 1 To WScript.Arguments.Count - 1
    cmd = cmd & " """ & WScript.Arguments(i) & """"
Next
Dim rc
rc = shell.Run("cmd /c " & cmd, 0, True)  ' 0 = hidden window, True = wait
Set f = fso.CreateTextFile(shell.ExpandEnvironmentStrings("%TEMP%") & "\invisible_runner_rc.log", True)
f.WriteLine rc
f.Close
WScript.Quit rc
