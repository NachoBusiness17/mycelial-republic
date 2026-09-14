#!/bin/sh
set -e
mkdir -p /root/.openclaw
# Mag .env names → OpenClaw canonical env. Never print values.
# Compose drops hyphenated names (NVIDIABuild-Autogen-46); read those from /mag/.env.
alias_from_env() {
  src="$1"
  dest="$2"
  eval "cur=\${$dest:-}"
  [ -n "$cur" ] && return 0
  v=$(printenv "$src" 2>/dev/null || true)
  if [ -z "$v" ] && [ -f /mag/.env ]; then
    while IFS= read -r line || [ -n "$line" ]; do
      line=$(printf '%s' "$line" | tr -d '\r')
      case "$line" in
        "$src"=*)
          v="${line#*=}"
          break
          ;;
      esac
    done < /mag/.env
  fi
  [ -n "$v" ] && export "$dest=$v"
  return 0
}
alias_from_env CEREBAS_API_KEY CEREBRAS_API_KEY
alias_from_env NVIDIABuild-Autogen-46 NVIDIA_API_KEY
alias_from_env ZAI_API_KEY_Pro ZAI_API_KEY_PRO
alias_from_env ZAI_API_KEY_Lite ZAI_API_KEY_LITE
alias_from_env COHERE_API_KEY_PAID COHERE_API_KEY
# Mistral remains host-side until its provider capability consent is explicit.
export OLLAMA_HOST="${OLLAMA_HOST:-http://host.docker.internal:11434}"
# Repo config is declarative and always wins; the named volume persists gateway state.
# Clobber guard (2026-09-02): the live volume config may hold repairs newer than the
# baked copy — snapshot it (timestamped, bounded to 10) before the declarative overwrite.
if [ -f /root/.openclaw/openclaw.json ]; then
  ts=$(date +%Y%m%dT%H%M%S)
  cp /root/.openclaw/openclaw.json "/root/.openclaw/openclaw.json.pre-start-$ts" || true
  ls -1t /root/.openclaw/openclaw.json.pre-start-* 2>/dev/null | tail -n +11 | xargs -r rm -f
fi
cp /opt/openclaw.container.json /root/.openclaw/openclaw.json
# Workspace identity files from Mag repo (sessions stay in the volume).
WS=/mag/deploy/openclaw/workspace
if [ -d "$WS" ]; then
  mkdir -p /root/.openclaw/workspace
  for f in AGENTS.md TOOLS.md IDENTITY.md USER.md SOUL.md HEARTBEAT.md PRIMER.md; do
    [ -f "$WS/$f" ] && cp "$WS/$f" /root/.openclaw/workspace/"$f"
  done
  # Mag project skills (AgentSkills) → workspace/skills (highest OpenClaw precedence)
  mkdir -p /root/.openclaw/workspace/skills
  if [ -d /mag/.agents/skills ]; then
    for d in /mag/.agents/skills/*/; do
      [ -f "${d}SKILL.md" ] && cp -a "$d" /root/.openclaw/workspace/skills/
    done
  fi
  if [ -d "$WS/skills" ]; then
    cp -a "$WS/skills/." /root/.openclaw/workspace/skills/
  fi
fi
mkdir -p /patches /board
mkdir -p /root/.openclaw/hooks
if [ -d /opt/openclaw-hooks ]; then
  cp -a /opt/openclaw-hooks/. /root/.openclaw/hooks/
fi
# OpenClaw 2026.8.x requires the explicit foreground verb in a container;
# plain "gateway" is the service-management command. Auth:
# OPENCLAW_GATEWAY_TOKEN via env_file. The Gateway shares a network namespace
# with the Tailscale sidecar; the sidecar's Serve config proxies the private
# tailnet HTTPS surface to this local listener.
exec openclaw gateway run
