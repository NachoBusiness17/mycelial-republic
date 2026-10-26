# B2-326 QLoRA 100-step smoke, 2026-09-26

## Verdict

OWED, blocked on hardware bytes, not on will: this box has NO NVIDIA GPU. Win32_VideoController names exactly one adapter, "AMD Radeon RX 5600 XT" (AdapterRAM 4,293,918,720 = 4 GB, the 32-bit WMI cap), nvidia-smi is absent from PATH, and the repo venv's torch is CPU-only (2.13.0+cpu, torch.cuda.is_available() False). The stack is further missing the pieces the recipe needs: peft, bitsandbytes, datasets, trl all absent (transformers 5.15.0 present). 4-bit QLoRA via bitsandbytes requires CUDA; an AMD 4 GB card cannot run it, and a CPU 100-step run of a 4-bit model is not a QLoRA smoke, it is theater. Per the no-fabrication law the run is filed as OWED instead of executed or invented, with the loss-curve bands carried forward unchanged (0.5-1.0 good, below 0.2 overfit tripwire, 0.0 with no validation probe = dead run) and the exact unblock path named. No training-loss number in this receipt: none was measured. The falsifier (training loss reaches 0.0 with no validation probe) stays armed for whoever fires the run.

## Evidence file:line quotes

- Hardware: powershell Get-CimInstance Win32_VideoController -> "Name : AMD Radeon RX 5600 XT", "AdapterRAM : 4293918720"; bash "nvidia-smi: command not found"; python probe "torch 2.13.0+cpu cuda_available False".
- Stack probe: "transformers 5.15.0"; "peft MISSING"; "datasets MISSING"; "bitsandbytes MISSING"; "trl MISSING".
- The recipe and bands (watch/inbox/burn_wave_20260926/B2_74_qlora_recipe_20260926.md Evidence): "start r=16, alpha=32"; "2e-4 as the vendor default"; "per_device_train_batch_size = 2", "gradient_accumulation_steps = 8"; "max_seq_length = 2048"; packing posture OFF for a 10K corpus ("the conservative 2026 posture for this corpus is packing OFF"); "take 20% of your training data and use that for testing", "evaluation_steps = 100"; bands "around 0.5 to 1.0 is a good sign", "below 0.2, your model is likely overfitting", loss 0 means check validation.
- Thought-bank location: not found under memory/ or corpus/ by quick glob this lane (searched "thought|bank|rocinante" in memory/runs and corpus/); the corpus slice for the smoke is part of the owed work, not assumed to exist.
- No GPU lane exists in configs/providers.yaml for compute (the fleet's GPU references are remote vendor APIs); the local-GPU premise came into the brief from the B2-74 Rocinante plan, which names the hardware class, not this host.

## Work done

- Probed hardware three ways (nvidia-smi, torch.cuda, WMI video controller) and the Python training stack for the five modules the recipe needs; recorded versions and misses exactly.
- Read the B2-74 receipt's Evidence section for the recipe constants and bands so the owed run is fully specified without re-derivation.
- Decided owed-not-theater: no run, no synthetic loss curve, no untested smoke script dressed up as ready; the B2-74 recipe is the spec, this receipt is the blocker record.
- Filed this receipt, the LEDGER row (verdict OWED), and the QUEUE row pointer with the unblock path.

## Falsifier

- Unblock path (any one fires the run): (a) a CUDA GPU with >= 12 GB on this box plus pip install peft bitsandbytes datasets trl into the repo venv; (b) the free Colab T4 route per fleet canon row 6 (unsloth notebooks, B2-183) running the same constants; (c) a rented 12-24 GB hour. The run is then: 4-bit QLoRA, r=16, alpha=32, lr 2e-4, batch 2 accum 8, max_seq 2048, packing off, 20 percent held-out, evaluation_steps 100, 100 steps on a small thought-bank slice; receipt carries the loss curve against the bands.
- Any claim of a completed local run without the hardware bytes above changing (torch build gains +cu, nvidia-smi appears) is fabrication and void on its face.
- A run whose training loss reaches 0.0 with no validation probe filed is the brief's falsifier: the run is dead, not good.
- If the thought-bank corpus does not exist in machine-usable form by run time, that is a second blocker to file, not to paper over.

## Bibliography closed

watch/inbox/burn_wave_20260926/B2_74_qlora_recipe_20260926.md (Evidence 1-5, bands); live hardware probes (nvidia-smi, torch, WMI) quoted above; fleet canon row 6 (watch/inbox/FLEET_CANON_COOL_SHIT_20260926.md, unsloth free-Colab route). No web sources. Em-dash count 0.
