# vast_provision.ps1 - PLAN SKELETON, not executed by any lane (LANE VAST-1 prep 2026-10-01)
# Companion to watch/inbox/model_garden/VAST_LAUNCH_PLAN.md. Default run = dry print.
# ONLY the operator may pass -Go (the rent is operator-gated; see plan section 6).
# LAWS carried from the 08-27..09-05 campaign (state/vast/):
#   - destroy after use; stopped boxes still bill storage ($0.10/GB/mo)
#   - zero fleet secrets travel to the box (.env-less box; public weights only)
#   - bearer key generated ON THE BOX, surfaced via SSH channel only
#   - two launch failures = stop and alert
#   - hard ceiling per trial; kill-word anytime
# SCHEMA: vast_provision.v1 (skeleton)

param(
    [switch]$Go,                       # ONLY the operator sets this
    [ValidateSet('scout','salon','judgment')]
    [string]$Tier = 'scout',           # scout=24GB (3090), salon=32GB (5090), judgment=A100/H100
    [double]$CeilingUsd = 5.00,        # hard spend ceiling for the trial
    [int]$TrialHours = 10,
    [int]$DiskGb = 50
)

$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot   # repo root (scripts/ parent)
$Py = Join-Path $Root '.venv\Scripts\python.exe'

# Tier table (planning bands 2026-10; live dph re-read at GO):
#   scout:    gpu_ram>=24, target dph<=0.20 interruptible (3090 band $0.09-0.18)
#   salon:    gpu_ram>=32, target dph<=0.45 interruptible (5090 band $0.34-0.60)
#   judgment: gpu_ram>=40, target dph<=1.60 interruptible (A100/H100 band)
$TierSpec = @{
    scout    = @{ minram = 24; maxdph = 0.20; image = 'vllm/vllm-openai:latest' }
    salon    = @{ minram = 32; maxdph = 0.45; image = 'vllm/vllm-openai:latest' }
    judgment = @{ minram = 40; maxdph = 1.60; image = 'pytorch/pytorch:2.6.0-cuda12.4-cudnn-devel' }
}

function Print-Plan {
    Write-Host "== vast_provision PLAN (dry; -Go to execute, OPERATOR ONLY) =="
    Write-Host "Tier: $Tier  ceiling: `$$CeilingUsd  trial: ${TrialHours}h  disk: ${DiskGb}GB"
    Write-Host "Phase 0  credit gate    : $Py -m mag.vast_launcher credit   (>= 10 USD required)"
    Write-Host "Phase 1  search         : reliability>=0.98 verified rentable, inet_down>=500"
    Write-Host "Phase 2  create ONE box : interruptible, image $($TierSpec[$Tier].image), -p 8000:8000 -p 11434:11434"
    Write-Host "          onstart       : vllm serve <model> --api-key <generated-on-box>; key via SSH only"
    Write-Host "Phase 3  verify         : first 200 with bearer key; nvidia-smi into receipt; vast_paces ladders"
    Write-Host "Phase 4  salons         : SSH tunnel -> lane-local runner (fence untouched; plan section 4)"
    Write-Host "Phase 5  teardown       : results -> watch/inbox/model_garden + memory/runs; then DESTROY"
    Write-Host "Kill-word: powershell -File `$PSCommandPath -Teardown -InstanceId <id>"
    Write-Host "Ceiling math: max hours = ceiling / dph (enforced by teardown timer + manual kill-word)"
}

# --- teardown mode (uncomment at GO; kept inert in the skeleton): ---
#   add [switch]$Teardown + [int]$InstanceId to param, then:
#   if ($Teardown) { vast destroy instance $InstanceId; exit 0 }

if (-not $Go) { Print-Plan; exit 0 }

# ================= OPERATOR-GO PATH (nothing below here runs from a lane) =================
# 0. credit gate (GET only)
& $Py -m mag.vast_launcher credit
#    parse credit; if < 10 -> abort with "top up first" (operator action)

# 1. search (prefer vast CLI if installed; else paste-ready API block below)
#    vast search offers "gpu_ram >= $($TierSpec[$Tier].minram) reliability > 0.98 rentable=true verified=true inet_down >= 500 disk_space >= $DiskGb" --order dph --limit 5
#    API equivalent: GET https://console.vast.ai/api/v0/bundles?q=... with Authorization: Bearer $env:VASTAI_API_KEY
#    pick cheapest offer with dph <= $($TierSpec[$Tier].maxdph); two launch failures = stop (09-05 rule)

# 2. create ONE interruptible instance
#    vast create instance <ID> --image $($TierSpec[$Tier].image) --disk $DiskGb -p 8000:8000 -p 11434:11434 --onstart-cmd 'bash /root/onstart.sh'
#    onstart.sh (sketch; generated at GO, bearer key created ON BOX):
#      KEY=$(openssl rand -hex 24); echo "$KEY" > /root/.service_key; chmod 600 /root/.service_key
#      vllm serve Qwen/Qwen2.5-7B-Instruct-AWQ --port 8000 --api-key "$KEY" &
#      # ollama lane instead if GGUF/MoE legs: ollama serve on 11434, no key -> tunnel-only
#    record instance_id; max_hours = CeilingUsd / dph; print exact teardown time

# 3. verify
#    ssh -N -L 8000:localhost:8000 root@<ip> -p <port>   (proxy port from IP Port Info popup)
#    curl -H "Authorization: Bearer <key-from-ssh>" http://127.0.0.1:8000/v1/models
#    nvidia-smi -> receipt; python scripts/vast_paces.py --endpoint http://127.0.0.1:8000

# 4. salons: lane-local runner against the tunneled endpoint (NO fence edit; plan section 4)

# 5. teardown (auto at max_hours + kill-word anytime)
#    pull results: scp -r root@<ip>:/root/results watch\inbox\model_garden\vast_trial_<date>\
#    vast destroy instance <ID>   (destroy, never stop: storage bills while stopped)
