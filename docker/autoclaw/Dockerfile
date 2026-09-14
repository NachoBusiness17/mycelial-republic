FROM node:22-alpine

RUN apk add --no-cache git curl bash

# Install opencode globally
RUN npm install -g opencode@latest 2>/dev/null || npm install -g opencode || echo 'opencode install attempted'

# Create working directories
RUN mkdir -p /workspace /root/.opencode /board

# Copy the opencode config
COPY opencode.json /root/.opencode/config.json

# Environment variables (set at runtime, not baked in)
ENV ZAI_CODING_KEY_1=""
ENV ZAI_CODING_KEY_2=""
ENV NODE_ENV=production

# The board mount point for output
VOLUME ["/board"]

WORKDIR /workspace

# Default: run opencode in headless mode
CMD ["opencode", "--help"]
