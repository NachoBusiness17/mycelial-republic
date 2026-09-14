# Mag v5 Vast.ai QLoRA fine-tune package

**Commitment:** `mag-v5-vast-training-001` · **As-of:** 2026-08-09
**Task:** gemma-2-2b-it, QLoRA 4-bit, LoRA r=16, 150 examples, est. $0.12.

## Contents

| File | Role |
|------|------|
| `train_data.jsonl` | 150 examples (instruction/input/output) — redacted T2 export |
| `train_lora.py` | QLoRA training script (gemma-2-2b-it, 4-bit nf4, r=16) |
| `setup_and_train.sh` | Entrypoint: installs stack + runs training |
| `job.yaml` | Vast.ai job spec (base model, hyperparams, cost guard) |

## Run (operator — requires `vastai` CLI)

```bash
# 1. Install vastai CLI (one-time)
pip install vastai

# 2. Search cheapest GPU with >=16GB VRAM (gemma-2-2b QLoRA needs ~8-12GB)
vastai search offers 'gpu_ram>=16 num_gpus=1 reliability>0.98' \
  --order 'dph_total' --limit 5

# 3. Create instance (pick cheapest offer id)
vastai create instance <offer_id> \
  --image vastai/base-image:cuda-12.4.1-cudnn-devel-ubuntu22.04 \
  --disk 40 --direct --onstart-cmd 'bash /workspace/setup_and_train.sh'

# 4. Upload package
scp -r -P <port> memory/training/vast_package/* <user>@<host>:/workspace/

# 5. Poll status
vastai show instance <id>

# 6. Download adapter when done
scp -r -P <port> <user>@<host>:/workspace/lora_output/ ./memory/training/runs/<run_id>/

# 7. Destroy instance (always — interruptible disk)
vastai destroy instance <id>
```

## Config (env overrides)

| Env | Default | Meaning |
|-----|---------|---------|
| `BASE_MODEL` | `google/gemma-2-2b-it` | Base model |
| `LORA_R` | `16` | LoRA rank |
| `LORA_ALPHA` | `32` | LoRA alpha |
| `LORA_DROPOUT` | `0.05` | LoRA dropout |
| `BATCH_SIZE` | `4` | Per-device batch |
| `LEARNING_RATE` | `2.0e-4` | LR |
| `EPOCHS` | `3` | Epochs |
| `OUT_DIR` | `lora_output` | Adapter output dir |

## Cost estimate

- gemma-2-2b QLoRA: ~8-12GB VRAM → cheapest 16GB GPU (~$0.10-0.20/hr).
- 150 examples × 3 epochs ≈ 450 steps at bs=4 → ~10-20 min on a 16GB GPU.
- **Est. total: ~$0.12** (well under `max_usd_per_job` in `configs/vast_train.yaml`).

## Law

- Curriculum stays home; this is a redacted T2 export (never T0/T1).
- Weights return to operator disk; instance destroyed after job.
- Cost every job in `memory/training/cost_ledger.jsonl`.
- Promote weights through human gate only (`docs/ref/MAG_v5_VAST_TRAINING.md`).
