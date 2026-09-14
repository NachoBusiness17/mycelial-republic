' Hidden launcher: runs the docker watchdog with no window flash.
CreateObject("Wscript.Shell").Run "powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File ""C:\Users\foste\Documents\projects\local_sovereign_agent\watch\docker_watchdog.ps1""", 0, False
