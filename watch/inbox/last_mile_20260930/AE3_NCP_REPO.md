# AE3 — LUMIA-Group/ncp_olmo_eval repo mine (2026-09-30)

Seat: Explore (read-only), banked by orchestrator. Source: github.com/LUMIA-Group/ncp_olmo_eval (README + src tree).

**(1) Contents.** Eval toolkit only (`ncp-olmo-eval` v0.1.1 pip package, src/tests/configs/docker). No training code; weights are HF pointers: NCP_ArchPreview_dolma3_8.9B Stage1 + Stage2 v1-v3 + DFlash2 draft (8.9B, Dolma3).

**(2) Methodology.** vLLM-based, scheduler-neutral (emits JSON task specs; local/Slurm/K8s adapters; register->infer->score->final lifecycle). Benchmarks: GSM8K (8-shot), SciQ (likelihood), Core88 (88 tasks incl. BigCodeBench/DS-1000/MultiPL-E, no-network sealed sandbox), RULER + HELMET (long context). "Concept quality" = per-task accuracy plus fail-closed token-parity checks for DFlash speculative drafts.

**(3) Runs locally?** NO. All checkpoints are 8.9B (~18GB bf16) on 8-GPU nodes; Core88 wants 32 GPUs; vLLM 0.13.0 is Linux-only. Harness code installs on Python 3.10+, but no inference on the estate's 12GB Windows box.

**(4) Steal list.** `task_spec.py` (executor-emit JSON specs), `source_identity.py`/`assets.py` (sealed, verified artifacts), `unified_eval_results.py`, `core_native_cached_finalize.py` (resumable scoring), `device_layout.py`, and especially `dflash_contract.py` — fail-closed parity-or-flag, the pattern for the estate's propagator agreement sweeps.

**(5) License.** Apache-2.0 (weights/benchmarks separately licensed; MultiPL-E restricts ML training).

## Estate verdict

No local run possible — this is a pattern mine, not a compute steal. The dflash_contract.py parity-or-flag pattern is the direct import: our propagator-vs-engine agreement sweep is the same shape (draft must match exact oracle or flag). The task_spec JSON-spec convention rhymes with AD3's env_contract work (manifest.json + reward.json).
