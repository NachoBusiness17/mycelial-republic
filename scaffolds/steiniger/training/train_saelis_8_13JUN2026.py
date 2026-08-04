#!/usr/bin/env python3
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

import torch
from unsloth import FastModel
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset
from unsloth.chat_templates import get_chat_template

# ================== YOUR PARAMETERS ==================
MODEL_NAME = "unsloth/gemma-4-31B-it"
DATASET_PATH = "./saelis_v8_dataset_13JUN2026.jsonl"
OUTPUT_DIR = "./saelis_v8_adapter_13JUN2026"
MAX_SEQ_LENGTH = 8192
RANK = 128
ALPHA = 256
# ====================================================

print("🚀 Loading Gemma 4 31B on 2×3090 + 2×3060...")

max_memory = {
    0: "23GiB", 1: "23GiB",
    2: "11GiB", 3: "11GiB",
}

model, tokenizer = FastModel.from_pretrained(
    model_name = MODEL_NAME,
    max_seq_length = MAX_SEQ_LENGTH,
    dtype = None,
    load_in_4bit = True,
    device_map = "balanced",
    max_memory = max_memory,
)

tokenizer = get_chat_template(tokenizer, chat_template = "gemma-4-thinking")

def formatting_func(examples):
    texts = []
    for convo in examples["messages"]:
        text = tokenizer.apply_chat_template(
            convo,
            tokenize=False,
            add_generation_prompt=True   # ← This adds the "model is about to speak" token
        )
        texts.append(text)
    return {"text": texts}

print("📚 Loading and formatting dataset...")
dataset = load_dataset("json", data_files=DATASET_PATH, split="train")
dataset = dataset.map(formatting_func, batched=True, num_proc=8)

# ========== DEBUG: Show exactly what the model sees ==========
print("\n" + "="*80)
print("SAMPLE FORMATTED TEXT (first example — first 1200 characters)")
print("="*80)
print(dataset[0]["text"][:1200])
print("...")
print("="*80 + "\n")

model = FastModel.get_peft_model(
    model,
    finetune_vision_layers     = False,
    finetune_language_layers   = True,
    finetune_attention_modules = True,
    finetune_mlp_modules       = True,
    r = RANK,
    lora_alpha = ALPHA,
    lora_dropout = 0,
    bias = "none",
    use_gradient_checkpointing = "unsloth",
    random_state = 3407,
)

trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    args = SFTConfig(
        dataset_text_field = "text",
        per_device_train_batch_size = 1,
        gradient_accumulation_steps = 8,
        warmup_steps = 12,
        num_train_epochs = 2,
        learning_rate = 2e-5,
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 1,
        optim = "adamw_8bit",
        weight_decay = 0.03,
        lr_scheduler_type = "cosine",
        seed = 3407,
        output_dir = OUTPUT_DIR,
        report_to = "none",
        save_strategy = "steps",
        save_steps = 30,
    ),
)

print("🔥 Starting training...")
trainer.train()

model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
print(f"✅ Done! Adapter saved to {OUTPUT_DIR}")