Ghost LoRA Training Package
============================

This package trains a LoRA adapter to reinforce the Ghost sovereign identity.

Files:
  - formatted_data.jsonl: 150 instruction-fine-tuning examples
  - train_ghost.py: Training script (unsloth or transformers+peft)
  - setup_and_train.sh: One-command setup + training
  - requirements.txt: Python dependencies

Output: lora_output/ — the LoRA adapter weights (~50-100 MB)
