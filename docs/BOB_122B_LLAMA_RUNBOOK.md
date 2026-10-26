# BOB 122B LLAMA RUNBOOK -- Ornith-1.5-122B Local MoE Deployment

**Document ID:** RUNBOOK-BOB-122B-LLAMA  
**Classification:** Estate Hardware Runbook  
**Target Host:** Bob (Tailscale host `100.125.103.60` / `bob.tailscale.local`)  
**Hardware Profile:** Single NVIDIA GeForce RTX 3090 (24GB VRAM) + 64GB DDR5 System RAM  
**Target Model:** Ornith-1.5-122B MoE (open weights)  
**Reference Signal:** @ItsmeAjayKV empirical speed test (X: 2112645286057418847)  
**Estate Anchor:** `local_sovereign_agent`  
**Governing Laws:** LAW-001 (Byte Preservation), LAW-002 (Rail Over Direction), LAW-061 (Floor Checks Hash).  
**House Law Compliance:** Strictly zero unicode em-dashes (`--` and `-` only); deterministic configurations.

---

## 1. Executive Summary & Architectural Why

The sovereign estate requires frontier-tier reasoning and evaluation capabilities without cloud API dependencies, telemetry leakage, or recurring per-token SaaS fees.

Ornith-1.5-122B is a 122-billion parameter Mixture-of-Experts (MoE) foundation model. While dense 120B+ models require multi-GPU nodes (e.g. 2x to 4x A100/H100), sparse MoE architectures only activate a small subset of experts per token (e.g. 2 of 16 or 4 of 32 experts).

By pairing `llama.cpp` with sparse CPU offloading (`--n-cpu-moe 36`), quantized KV cache (`-ctk q8_0 -ctv q8_0`), Flash Attention (`-fa on`), and Multi-Token Prediction (`--spec-type draft-mtp`), Bob runs Ornith-1.5-122B directly on a single consumer RTX 3090 (24GB VRAM) and 64GB DDR5 system RAM at viable interactive and batch evaluation speeds.

---

## 2. Memory Budget Allocation (24GB VRAM + 64GB DDR5)

```
+----------------------------------------------------------------------------------+
|                              MEMORY ALLOCATION MATRIX                            |
+----------------------+--------------------+---------------------+----------------+
| Component            | Host Memory (DDR5) | Device VRAM (3090)  | Quantization   |
+----------------------+--------------------+---------------------+----------------+
| MoE Inactive Experts | ~44 GB             | --                  | Q4_K_M / Q3_K_L|
| Dense Attention & FFN| --                 | ~14.5 GB            | Q4_K_M         |
| 132k Context KV-Cache| --                 | ~4.2 GB             | Q8_0 / Q8_0    |
| CUDA Overhead & VMM  | --                 | ~1.8 GB             | FP32 / FP16    |
| Scratchpad / Buffers | ~4 GB              | ~1.5 GB             | Dynamic        |
+----------------------+--------------------+---------------------+----------------+
| Total Footprint      | ~48 GB / 64 GB     | ~22.0 GB / 24.0 GB  | STABLE HEADROOM|
+----------------------+--------------------+---------------------+----------------+
```

* **VRAM Headroom:** 2.0 GB safety margin prevents CUDA out-of-memory (OOM) faults during batch spikes.
* **System RAM Headroom:** 16 GB retained for OS operations, Tailscale tunnel, and file caching.

---

## 3. Bob Host Prerequisites

### 3.1 Software & Drivers
* NVIDIA Driver >= 550.54.14 (CUDA 12.4+)
* Linux Ubuntu 24.04 LTS (kernel 6.8+)
* Tailscale daemon active with SMB/SSH exposure to estate seats
* `build-essential`, `cmake`, `git`, `libcurl4-openssl-dev`

### 3.2 Compilation of llama.cpp on Bob
```bash
# Clone and build llama.cpp with CUDA backend
git clone https://github.com/ggerganov/llama.cpp /opt/llama.cpp
cd /opt/llama.cpp
mkdir build && cd build
cmake .. -DGGML_CUDA=ON -DCMAKE_BUILD_TYPE=Release
cmake --build . --config Release -j$(nproc)
```

---

## 4. Launch Flags & Service Configuration

### 4.1 Production Launch Command
The canonical execution command as proven by @ItsmeAjayKV:

```bash
/opt/llama.cpp/build/bin/llama-server \
  -m /data/models/ornith-1.5-122b/ornith-1.5-122b-Q4_K_M.gguf \
  --host 0.0.0.0 \
  --port 8080 \
  -c 131072 \
  -fa on \
  -ctk q8_0 \
  -ctv q8_0 \
  -ngl 999 \
  --n-cpu-moe 36 \
  -np 1 \
  --spec-type draft-mtp \
  --n-max-pred 3 \
  --parallel 1 \
  --cont-batching \
  --embedding false \
  --log-file /var/log/ornith-122b-bob.log
```

### 4.2 Parameter Breakdown & Rationale
1. `-fa on`: Flash Attention enabled to reduce VRAM consumption from $O(N^2)$ to $O(N)$ across long context windows.
2. `-ctk q8_0 -ctv q8_0`: Quantizes key and value cache tensors to 8-bit precision, halving memory bandwidth and VRAM requirements for 132k contexts with minimal perplexity degradation.
3. `-ngl 999`: Offloads all candidate model layers to GPU device VRAM.
4. `--n-cpu-moe 36`: Offloads 36 MoE expert weights to DDR5 system RAM, pulling them across PCIe bus on-demand while keeping active attention heads in 24GB VRAM.
5. `--spec-type draft-mtp --n-max-pred 3`: Multi-Token Prediction speculative drafting generates up to 3 tokens per forward pass, overcoming PCIe bandwidth bottlenecks during sparse expert retrieval.
6. `-c 131072`: Allocates support for 132k token context window.

---

## 5. Systemd Service Definition (`/etc/systemd/system/ornith-bob.service`)

```ini
[Unit]
Description=Ornith 122B MoE llama.cpp Server on Bob
After=network.target nvidia-persistenced.service
Wants=network-online.target

[Service]
Type=simple
User=mag
Group=mag
WorkingDirectory=/data/models/ornith-1.5-122b
ExecStart=/opt/llama.cpp/build/bin/llama-server \
  -m /data/models/ornith-1.5-122b/ornith-1.5-122b-Q4_K_M.gguf \
  --host 100.125.103.60 \
  --port 8080 \
  -c 131072 \
  -fa on \
  -ctk q8_0 \
  -ctv q8_0 \
  -ngl 999 \
  --n-cpu-moe 36 \
  -np 1 \
  --spec-type draft-mtp \
  --n-max-pred 3
Restart=on-failure
RestartSec=10s
LimitNOFILE=65536
Environment="CUDA_VISIBLE_DEVICES=0"

[Install]
WantedBy=multi-user.target
```

---

## 6. Estate Client Wiring & Failover

### 6.1 Dispatch via `tools/bob_bridge.py`
The estate communicates with Bob via Tailscale HTTP endpoint: `http://100.125.103.60:8080/v1/chat/completions`.

When Bob is online:
* High-context evaluations, First-Order Logic extraction, and heavy multi-model referee sweeps route to Bob.

When Bob is offline:
* Probes on TCP port 8080 / 445 timeout gracefully within 500ms.
* Estate falls back cleanly to local CPU static retrieval (`tools/bekko_cpu_retriever.py`) and fast local models without halting or crashing.

### 6.2 Health Check Probe
```bash
curl -s -m 2 http://100.125.103.60:8080/health | jq .
```
Expected response:
```json
{
  "status": "ok",
  "slots_idle": 1,
  "slots_processing": 0
}
```

---

## 7. Verification & House Law Checklist

- [x] Zero unicode em-dashes verified in file contents (`--` and `-` only).
- [x] Memory footprint bounded within 24GB VRAM and 64GB DDR5 system RAM.
- [x] Speculative MTP and MoE CPU offload flags aligned with @ItsmeAjayKV empirical receipt.
- [x] Clean failover protocol integrated with existing Tailscale SMB/SSH estate architecture.
