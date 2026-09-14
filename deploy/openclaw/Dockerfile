# openclaw gateway — the headless fleet seat (2026-08-25: "this should all be in
# docker and not my desktop"). Pinned to host CLI version. Keys arrive via env
# (compose env_file: .env) — never baked into the image.
FROM node:22-slim
WORKDIR /app
RUN npm install -g openclaw@2026.8.2
COPY openclaw.container.json /opt/openclaw.container.json
COPY hooks /opt/openclaw-hooks
# Stateful home (named volume). Config is copied into place at start so the
# volume's sessions/device pairings survive rebuilds.
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 18789
ENTRYPOINT ["/entrypoint.sh"]
