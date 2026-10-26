#!/bin/sh
# ZCode gate-repair router (2026-09-29): WSL bash cannot open Windows-style script
# paths (C:/...), which made estate gates die 127 ("No such file or directory").
# Route C:/... script invocations to Git Bash via WSL interop; everything else
# runs the untouched real binary (/bin/bash.real).
# Installed by wsl_bash_router_install.sh; rollback via wsl_bash_router_rollback.sh.
case "$1" in
  [A-Za-z]:[/\\]*)
    GBB="/mnt/c/Program Files/Git/bin/bash.exe"
    if [ -x "$GBB" ]; then
      "$GBB" "$@"
      exit $?
    fi
    echo "bash-router: Git Bash not found at $GBB" >&2
    exit 127 ;;
  *) exec /bin/bash.real "$@" ;;
esac
