#!/bin/sh
set -e
mkdir -p /root/.openclaw
# Repo config is declarative and always wins; the named volume only persists
# sessions/auth state written by the gateway itself.
cp /opt/openclaw.container.json /root/.openclaw/openclaw.json
exec openclaw gateway --auth none --bind lan
