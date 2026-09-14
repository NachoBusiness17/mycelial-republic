#!/usr/bin/env bash
# vast_bootstrap_w3.sh — W3-narrative burst boot (run as root by vast.ai startup script)
# BURST-PROFILE-v0
#
# Assumes the instance was rented with the `vllm/vllm-openai` image (vLLM + its OpenAI
# server entrypoint are already installed — we install nothing here).
# Boot steps: pull the flash model via huggingface-cli, launch vLLM bound to 0.0.0.0:8080
# with an explicit 32K context, write a ready marker, echo the endpoint for the client.
set -euo pipefail

MARKER="/root/.burst_ready"
MODEL_DIR="/root/.cache/huggingface/hub/models--deepseek-ai--DeepSeek-V4-Flash-0731"
MODEL_ID="deepseek-ai/DeepSeek-V4-Flash-0731"
PORT=8080
MAX_LEN=32768

# Idempotent by design: if the marker is already present (previous boot / retry),
# assume vLLM is (or was) served and do not re-pull or re-launch.
if [ -f "$MARKER" ]; then
  echo "burst already ready ($MARKER present) — exiting."
  exit 0
fi

echo "[burst-w3] boot start: $(date -u +%FT%TZ)"

# 1) Pull the model weights. Requires HF_TOKEN; swap the placeholder at launch time
#    (vast.ai interpolates env before running this script). hf/glm both served by vLLM
#    OpenAI server, so the pull path is the same for either flash model.
if [ -d "$MODEL_DIR" ]; then
  echo "[burst-w3] model already cached, skipping pull."
else
  echo "[burst-w3] pulling ${MODEL_ID}…"
  # placeholder — replace with a real token in the launch payload; never hardcode.
  export HF_TOKEN="${HF_TOKEN:-__BURST_PLACEHOLDER_HF_TOKEN__}"
  huggingface-cli download "$MODEL_ID" || {
    echo "[burst-w3] WARN model pull failed; vLLM may lazy-download instead." >&2
  }
fi

# 2) Launch the OpenAI-compatible server. `vllm serve` is the documented entrypoint on
#    the vllm-openai image; if it's missing, fall back to `python -m vllm.entrypoints.openai.api_server`.
PORT="${PORT}" MAX_LEN="${MAX_LEN}" MODEL_ID="${MODEL_ID}" \
nohup bash -c '
  if   command -v vllm >/dev/null 2>&1; then
    vllm serve                   \
      --model "$MODEL_ID"        \
      --host 0.0.0.0             \
      --port  "$PORT"            \
      --max-model-len "$MAX_LEN" ;
  elif [ -x /usr/local/bin/python ]; then
    python /usr/local/bin/python -m vllm.entrypoints.openai.api_server \
      --model "$MODEL_ID" --host 0.0.0.0 --port "$PORT" --max-model-len "$MAX_LEN" ;
  else
    echo "[burst-w3] ERROR: no vllm executable found on vllm-openai image" >&2 ;
    exit 1 ;
  fi
' >/root/burst_vllm.log 2>&1 &

# 3) Wait up to ~180s for the endpoint to report ready, then write the marker.
for i in $(seq 1 90); do
  if curl -sf --max-time 3 "http://0.0.0.0:${PORT}/v1/models" >/dev/null 2>&1; then
    echo "[burst-w3] vLLM ready after ~$((i*2))s."
    break
  fi
  sleep 2
done

echo "[burst-w3] endpoint: http://<INSTANCE_ADDR>:${PORT}/v1/models"
echo "[burst-w3] ready-time: $(date -u +%FT%TZ)" > "$MARKER"
echo "[burst-w3] marker written: $MARKER"
exit 0
