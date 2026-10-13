#!/bin/bash
# Vast.ai setup + training script
set -e

echo "=== Ghost LoRA Training ==="
echo "Starting at $(date)"

# Install dependencies
pip install -q unsloth torch transformers datasets peft accelerate bitsandbytes

# Verify GPU
nvidia-smi

# Train
echo "Starting training..."
python train_ghost.py

# Package results
echo "Training complete. Results in lora_output/"
ls -la lora_output/

echo "Done at $(date)"
