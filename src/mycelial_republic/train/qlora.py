"""QLoRA fine-tune entrypoint (Sprint 0.3) - real LoRA fit on gemma-2b.

Implements the seed-mirror plan (2026-08-02) S3 step:
  unsloth LoRA on gemma-2b -> GGUF -> ollama create seed-mirror

This is a REAL trainer (no dry-run stub). It fails fast if train deps are
missing. Run:
  pip install -e ".[train]"
  python -m mycelial_republic.train.qlora --data data/train/train.jsonl

Outputs:
  models/seed-mirror-gguf/  (GGUF export)
  models/Modelfile          (for `ollama create seed-mirror`)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# Repo root: .../mycelial-republic
ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DATA = ROOT / "data" / "train" / "train.jsonl"
DEFAULT_MODEL = "gemma-2b"
DEFAULT_OUT = ROOT / "models" / "seed-mirror-gguf"
DEFAULT_MODELFILE = ROOT / "models" / "Modelfile"
DEFAULT_OLLAMA_NAME = "seed-mirror"


def _require_deps() -> None:
    missing = []
    for mod in ("torch", "datasets", "transformers", "peft", "unsloth"):
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod)
    if missing:
        print(
            "Missing train deps: " + ", ".join(missing) + "\n"
            "Run: pip install -e \".[train]\"",
            file=sys.stderr,
        )
        raise SystemExit(1)


def _load_rows(data: Path) -> list[dict]:
    rows = []
    for line in data.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _to_chat_text(row: dict) -> str:
    instruction = row.get("instruction") or "Continue in the operator's sovereign mirror voice."
    response = row.get("response") or row.get("text") or ""
    return f"### User\n{instruction}\n\n### Assistant\n{response}"


def run_train(
    data: str = str(DEFAULT_DATA),
    base_model: str = DEFAULT_MODEL,
    out_dir: str = str(DEFAULT_OUT),
    modelfile: str = str(DEFAULT_MODELFILE),
    ollama_name: str = DEFAULT_OLLAMA_NAME,
    r: int = 8,
    epochs: int = 1,
) -> int:
    data_path = Path(data)
    if not data_path.is_file():
        print(f"Data not found: {data_path}", file=sys.stderr)
        return 1

    _require_deps()

    from unsloth import FastLanguageModel  # type: ignore
    from trl import SFTTrainer  # type: ignore
    from transformers import TrainingArguments  # type: ignore
    from datasets import Dataset  # type: ignore

    rows = _load_rows(data_path)
    print(f"Data: {data_path} ({len(rows)} rows)")
    print(f"Base: {base_model} | r={r} | epochs={epochs}")

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=base_model,
        max_seq_length=2048,
        dtype=None,
        load_in_4bit=True,
    )
    model = FastLanguageModel.get_peft_model(
        model,
        r=r,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
        lora_alpha=16,
        lora_dropout=0,
        bias="none",
        use_gradient_checkpointing="unsloth",
        random_state=42,
        use_rslora=False,
        loftq_config=None,
    )

    ds = Dataset.from_list([{"text": _to_chat_text(r)} for r in rows])

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=ds,
        dataset_text_field="text",
        max_seq_length=2048,
        dataset_num_proc=2,
        packing=False,
        args=TrainingArguments(
            per_device_train_batch_size=2,
            gradient_accumulation_steps=4,
            warmup_steps=5,
            num_train_epochs=epochs,
            learning_rate=2e-4,
            fp16=not sys.platform.startswith("linux"),
            logging_steps=1,
            optim="adamw_8bit",
            weight_decay=0.01,
            lr_scheduler_type="linear",
            seed=3407,
            output_dir=str(ROOT / "models" / "seed-mirror-checkpoints"),
            report_to="none",
        ),
    )
    trainer.train()

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    model.save_pretrained_gguf(str(out), tokenizer, quantization_method="q4_k_m")
    print(f"GGUF exported -> {out}")

    # Write Modelfile for ollama create
    mf = Path(modelfile)
    mf.parent.mkdir(parents=True, exist_ok=True)
    gguf = next(out.glob("*.gguf"), None)
    if not gguf:
        print("No .gguf found in output dir", file=sys.stderr)
        return 1
    mf.write_text(
        f"FROM {gguf.resolve().as_posix()}\n"
        f"TEMPLATE \"{{{{ .Prompt }}}}\n\"\n"
        f"PARAMETER temperature 0.7\n",
        encoding="utf-8",
    )
    print(f"Modelfile -> {mf}")
    print(f"Next (operator): ollama create {ollama_name} -f {mf}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Seed Mirror QLoRA trainer (real fit)")
    ap.add_argument("--data", default=str(DEFAULT_DATA))
    ap.add_argument("--base-model", default=DEFAULT_MODEL)
    ap.add_argument("--out-dir", default=str(DEFAULT_OUT))
    ap.add_argument("--modelfile", default=str(DEFAULT_MODELFILE))
    ap.add_argument("--ollama-name", default=DEFAULT_OLLAMA_NAME)
    ap.add_argument("--r", type=int, default=8)
    ap.add_argument("--epochs", type=int, default=1)
    a = ap.parse_args(argv)
    return run_train(
        data=a.data,
        base_model=a.base_model,
        out_dir=a.out_dir,
        modelfile=a.modelfile,
        ollama_name=a.ollama_name,
        r=a.r,
        epochs=a.epochs,
    )


if __name__ == "__main__":
    raise SystemExit(main())
