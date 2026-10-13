#!/usr/bin/env python3
"""Mag v5 QLoRA fine-tune — gemma-2-2b-it, 4-bit, LoRA r=16.

Runs on a rented Vast.ai GPU instance. Input: train_data.jsonl (150 examples,
instruction/input/output). Output: lora_output/ adapter + eval log.

Law (docs/ref/MAG_v5_VAST_TRAINING.md):
  - Curriculum stays home; this is a redacted T2 export.
  - Weights return to operator disk; instance destroyed after job.
  - Cost every job in cost_ledger.
"""
import json
import os
import sys
import time
from pathlib import Path

import torch
from datasets import Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer

BASE_MODEL = os.environ.get("BASE_MODEL", "google/gemma-2-2b-it")
DATA_PATH = Path(os.environ.get("DATA_PATH", "train_data.jsonl"))
OUT_DIR = Path(os.environ.get("OUT_DIR", "lora_output"))
LORA_R = int(os.environ.get("LORA_R", "16"))
LORA_ALPHA = int(os.environ.get("LORA_ALPHA", "32"))
LORA_DROPOUT = float(os.environ.get("LORA_DROPOUT", "0.05"))
BATCH_SIZE = int(os.environ.get("BATCH_SIZE", "4"))
LEARNING_RATE = float(os.environ.get("LEARNING_RATE", "2.0e-4"))
EPOCHS = int(os.environ.get("EPOCHS", "3"))
MAX_SEQ_LEN = int(os.environ.get("MAX_SEQ_LEN", "512"))


def load_data(path: Path):
    rows = []
    for line in path.read_text(encoding="utf-8").strip().split("\n"):
        if not line.strip():
            continue
        d = json.loads(line)
        rows.append(
            {
                "instruction": d["instruction"],
                "input": d.get("input", ""),
                "output": d["output"],
            }
        )
    print(f"[train] loaded {len(rows)} examples from {path}")
    return rows


def format_example(example):
    """Gemma chat template: <start_of_turn>user ... <end_of_turn> model ..."""
    prompt = example["instruction"]
    if example["input"]:
        prompt += "\n\n" + example["input"]
    text = (
        f"<start_of_turn>user\n{prompt}<end_of_turn>\n"
        f"<start_of_turn>model\n{example['output']}<end_of_turn>\n"
    )
    return {"text": text}


def main():
    t0 = time.time()
    rows = load_data(DATA_PATH)
    formatted = [format_example(r) for r in rows]
    dataset = Dataset.from_list(formatted)

    print(f"[train] base model: {BASE_MODEL}")
    print(f"[train] QLoRA 4-bit, r={LORA_R}, alpha={LORA_ALPHA}, "
          f"dropout={LORA_DROPOUT}, bs={BATCH_SIZE}, lr={LEARNING_RATE}, "
          f"epochs={EPOCHS}")

    # 4-bit quantization config
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )

    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
    )
    model = prepare_model_for_kbit_training(model)

    lora_config = LoraConfig(
        r=LORA_R,
        lora_alpha=LORA_ALPHA,
        lora_dropout=LORA_DROPOUT,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    training_args = TrainingArguments(
        output_dir=str(OUT_DIR),
        per_device_train_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=2,
        num_train_epochs=EPOCHS,
        learning_rate=LEARNING_RATE,
        fp16=False,
        bf16=True,
        logging_steps=10,
        save_strategy="epoch",
        save_total_limit=2,
        report_to=[],
        remove_unused_columns=False,
    )

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        tokenizer=tokenizer,
        max_seq_length=MAX_SEQ_LEN,
        dataset_text_field="text",
    )

    trainer.train()

    # Save adapter (not full model) — small, fast to download
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(str(OUT_DIR))
    tokenizer.save_pretrained(str(OUT_DIR))

    # Eval log
    elapsed = time.time() - t0
    with open(OUT_DIR / "eval_log.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "base_model": BASE_MODEL,
                "lora_r": LORA_R,
                "lora_alpha": LORA_ALPHA,
                "lora_dropout": LORA_DROPOUT,
                "batch_size": BATCH_SIZE,
                "learning_rate": LEARNING_RATE,
                "epochs": EPOCHS,
                "n_examples": len(rows),
                "elapsed_seconds": round(elapsed, 1),
                "status": "complete",
            },
            f,
            indent=2,
        )
    print(f"[train] DONE in {elapsed:.1f}s — adapter at {OUT_DIR}")
    print(f"[train] eval_log.json written")


if __name__ == "__main__":
    sys.exit(main())
