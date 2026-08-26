#!/bin/sh
set -e
mkdir -p /root/.openclaw
# Repo config is declarative and always wins; the named volume persists gateway state.
cp /opt/openclaw.container.json /root/.openclaw/openclaw.json
# Plain "openclaw gateway" runs it in-process ("gateway start" is the systemd
# service manager, wrong verb in a container). Auth: OPENCLAW_GATEWAY_TOKEN via
# env_file. In-container bind defaults to 0.0.0.0 for port-forward compat.
exec openclaw gateway
