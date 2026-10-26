#!/bin/sh
# Installer: run as root inside WSL Ubuntu.
#   MSYS_NO_PATHCONV=1 wsl -d Ubuntu -u root -- sh /mnt/c/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/gala_20260925/wave5-repair/wsl_bash_router_install.sh
# Backs up the real bash to /bin/bash.real and installs the C:/... router in its
# place. Rollback: wsl_bash_router_rollback.sh (same directory).
set -e
ROUTER=/mnt/c/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/gala_20260925/wave5-repair/wsl_bash_router.sh
if [ ! -f /bin/bash.real ]; then
  cp -p /bin/bash /bin/bash.real
fi
cp "$ROUTER" /bin/bash.new
chmod 755 /bin/bash.new
mv /bin/bash.new /bin/bash
echo "INSTALLED:"
ls -la /bin/bash /bin/bash.real
head -3 /bin/bash
