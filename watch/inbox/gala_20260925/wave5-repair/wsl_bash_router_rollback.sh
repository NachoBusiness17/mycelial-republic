#!/bin/sh
# Rollback: run as root inside WSL Ubuntu. Restores the original /bin/bash.
#   MSYS_NO_PATHCONV=1 wsl -d Ubuntu -u root -- sh /mnt/c/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/gala_20260925/wave5-repair/wsl_bash_router_rollback.sh
set -e
if [ -f /bin/bash.real ]; then
  rm -f /bin/bash
  mv /bin/bash.real /bin/bash
  echo "RESTORED:"
  ls -la /bin/bash
else
  echo "no /bin/bash.real backup found; nothing done"
fi
