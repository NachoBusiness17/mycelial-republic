# BOB BOOTSTRAP - run ON bob (one sitting, hostname-guarded)

Bob: 100.125.103.60 (tailnet), repo cloned at the identical path, own Hermes,
SMB-walled (no remote exec) - so this runs in bob's own seat/terminal.
Desktop side is already armed: mesh_delta seed + the gauntlet + the fleet.

## Step 0 - prove you are on bob (hostname guard)

    hostname   # must print the bob hostname, not DESKTOP-7C70KSC

## Step 1 - GPU detect (the operator's question)

    # NVIDIA:
    nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
    # AMD:
    powershell -NoProfile -Command "Get-CimInstance Win32_VideoController | Select Name, AdapterRAM"

Bank the output to watch/inbox/BOB_GPU_<date>.md (one line is enough).
Decision table: NVIDIA -> llama.cpp RPC join + CUDA Ollama (the mesh's
second compute lung). AMD RDNA2+ -> ROCm Ollama possible. AMD RDNA1 ->
LM Studio Vulkan path (the desktop's own cure). No dGPU -> CPU peer only.

## Step 2 - join the inference pool (if NVIDIA or Vulkan-capable)

    # desktop already holds llama-b11457 binaries: copy the zip from the
    # estate share or download the same release; then on bob:
    ggml-rpc-server.exe -p 50052 -H 0.0.0.0
    # desktop side (the pooled client):
    LLAMA_ARG_RPC=100.125.103.60:50052 llama-server.exe -m <model.gguf>
    # measure: same battery as the P3 spike, cross-machine tok/s vs local

## Step 3 - join the memory standing wave

    cd C:\Users\foste\Documents\projects\local_sovereign_agent
    .venv\Scripts\python.exe -m tools.mesh_delta scan
    .venv\Scripts\python.exe -m tools.mesh_delta pull --peer http://<desktop-tailnet-ip>:8767 --apply
    # desktop must be seeding: python -m tools.mesh_delta serve --bind <desktop-tailnet-ip> --port 8767

## Step 4 - arm bob's drain task (the lane plane)

    powershell -ExecutionPolicy Bypass -File scripts\register_gauntlet_task.ps1
    powershell -ExecutionPolicy Bypass -File scripts\register_free_lane_fleet_task.ps1
    # then the second Ollama provider row (desktop fleet PROVIDERS) gains:
    #   {"id": "ollama-bob", "kind": "ollama", "url": "http://100.125.103.60:11434/...", ...}
    # (allowlist literal added desktop-side; bob's ollama binds 0.0.0.0)

## Step 5 - bank it

One receipt: watch/inbox/BOB_JOIN_<date>.md with steps 1-4 outputs.
The mesh then reads: two compute lungs, one memory wave, lane drain x2.
