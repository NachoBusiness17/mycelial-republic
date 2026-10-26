# BURST PROFILE — rent-to-receipts on vast.ai
BURST-PROFILE-v0 · 2026-09-01 · $0-lane seat, prepaid rental

Goal: rent a GPU, serve an executable, run the 20-probe battery, write a genC receipt,
terminate, inside one rental window (≤10 min rent→receipts).

## Pipeline
RENT (pick image+GPU offer) → STARTUP (paste script into vast's **startup script** field,
runs as root at boot; marks ready + echoes endpoint) → SERVE (script launches vLLM /
axolotl / bare runner bound 0.0.0.0) → CLIENT (`burst_client.mjs` health-checks then runs
20-probe battery in parallel waves of 5, SIGTERM-safe → genC receipt + ledger) →
TERMINATE → destroy instance.

## vast.ai "startup script" field
Shell vast runs as root after image boot — the only exec point before SSH. Rules: run
once/boot; idempotent (guard on marker so restarts don't double-launch); don't exit without
writing the marker (client probes /v1/models, not exit code); pass secrets (HF_TOKEN) via
launch-payload env — never hardcode.

## Profiles
| Profile        | Image              | Model/payload                | Tooling | Port | Purpose |
|----------------|--------------------|------------------------------|---------|------|---------|
| W3-narrative   | vllm/vllm-openai   | DeepSeek-V4-Flash (or GLM-4.7), 32K | vLLM | 8080 | narrative/genC battery |
| lora-burst     | CUDA+pytorch       | HF dataset + LoRA            | axolotl | n/a  | LoRA training burst |
| substrate-test | bare runner        | battery runner only          | node/shell | n/a | HW/throughput smoke |

W3-narrative is primary (flash, 32K ctx, port 8080) — `vast_bootstrap_w3.sh`.

## Readiness (client)
`GET {ep}/v1/models` → 200 + non-empty data → ready. Probes → `POST {ep}/v1/chat/completions`
(vLLM OpenAI schema). 10s timeout, 5 retries.

## Receipt + ledger
- Markdown: `/board/lineage_genC_vastburst_<ts>.md` (genC-compatible).
- Ledger: JSONL row/probe → `/board/vastburst_<ts>_ledger.jsonl`.
- Spend: N/A (prepaid); instance min + destroy proof in footer.

## GPU RULE (added 19:23Z, from the CDI failure post-mortem)
**Vast chooses the physical GPU; the fleet chooses the capability and workload. Never copy a physical device index between hosts.**
- No explicit GPU selectors in instance config: no gpu=N, device=N, CUDA_VISIBLE_DEVICES=N, NVIDIA_VISIBLE_DEVICES=N, device_ids, CDI fields. Platform-managed allocation only.
- Verified hosts only (both working instances: 98.65%/99.32% verified; the one failure: unverified host 70317, CDI injection `gpu=2` on a 1-GPU box).
- Smoke-test rung: 7B model first, verify serving + tokens — THEN pull the 32B workload.
- If a fresh verified host still fails CDI → host-allocation defect, move hosts, don't debug the platform.
- Recovery card: watch/VAST_CDI_FAILURE_SELF_STEAL_20260901.md (other window).
