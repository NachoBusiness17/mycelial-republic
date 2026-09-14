# VAST CDI FAILURE — SELF-STEAL AND RECOVERY CARD

**Incident:** instance `49569680`, label `e7dogfood2`  
**Observed:** single RTX 3090, 24 GB, host `70317`, “Unverified”, `$0.017/hr`, `Inactive`, intended `Stopped`  
**Failure:** Docker could not create the container because CDI injection requested `D.<hash>/gpu=2`, which the host could not resolve.

## Verdict

This is a **pre-vLLM container allocation failure**. The image did not start, the model did not pull, and the server did not bind a port. Changing model flags, context length, quantization, or the on-start script cannot fix this particular failure.

The bad selector is incompatible with the visible allocation: the instance has one assigned GPU, but the runtime was asked for device index `2` or a stale device alias containing `gpu=2`. Treat the instance specification/host assignment as poisoned and recreate it.

## What the next launch must do

1. Keep `49569680` stopped. Destroy it after preserving this error receipt; it has no useful running workload or attached volume.
2. Create a **new** instance, not a restart or edit of the failed one.
3. Choose `RTX_3090`, `num_gpus=1`, and a verified/reliable offer. Do not reuse this “Unverified” host if a verified offer is available.
4. Use `vllm/vllm-openai:latest` if desired; the image is not the failure point.
5. In the Vast template/options, remove all manual device selectors:

   - `--gpus device=2`
   - `--gpus 2`
   - `--runtime=nvidia` when Vast supplies the runtime
   - `CUDA_VISIBLE_DEVICES=2`
   - `NVIDIA_VISIBLE_DEVICES=2`
   - any `device_ids`, `gpu_ids`, or CDI `gpu=2` field

   Do not override `GPU_COUNT`. Vast allocates the assigned GPU. If a process-level mask is needed inside a one-GPU container, `CUDA_VISIBLE_DEVICES=0` is the only valid local index—but first try with no mask.

6. Expose only the service port needed by the job, for example internal TCP `8080`.
7. Start with a small smoke model and prove the GPU path before pulling a 19 GB class model:

```text
vllm serve Qwen/Qwen2.5-7B-Instruct \
  --host 0.0.0.0 \
  --port 8080 \
  --max-model-len 8192 \
  --gpu-memory-utilization 0.90
```

The on-start log must show, in order: `nvidia-smi` sees one 3090 → vLLM starts → `/v1/models` returns 200 → one tiny completion succeeds. Only then switch to the intended quantized 32B workload, with a conservative context limit and a predeclared spend cap.

## Why this is the correct Vast interpretation

Vast documents that its Docker instances receive their allocated GPU resources automatically. Its template settings are intended for image, ports, and environment variables; arbitrary Docker runtime options are not a reliable place to select a physical GPU. The official CLI also treats `gpu_name` and `num_gpus` as the allocation request, not a manually chosen device index.

Therefore the portable contract is:

```text
offer: gpu_name + num_gpus + reliability/verified filter
container: image + ports + app environment
process: vLLM model/server flags
never: physical CDI selector copied between hosts
```

## If the fresh instance repeats `gpu=2`

Stop retrying. That would be a Vast host/runtime allocation defect, not an application defect. Capture:

- new instance ID;
- offer ID and host ID;
- exact CDI error;
- `num_gpus=1` request;
- confirmation that no manual GPU selector was present.

Then move to another verified offer and send the bundle to Vast support asking them to regenerate CDI metadata or repair the host’s GPU allocation. Do not spend another boot window on the same poisoned host.

## Self-steal lessons for Mag

- **The allocator owns physical identity.** Mag may request capability; it must not invent device identity.
- **Smoke before payload.** Prove the runtime with a tiny model before spending time or bandwidth on corpus workloads.
- **Container failure is a different taxonomy class from model failure.** Route it to infrastructure repair, not vLLM tuning.
- **“Inactive” is not “free.”** Destroy failed instances with no needed volume and verify the instance list is empty; stopped disks can still incur charges.
- **Every burst job needs an offer receipt, launch receipt, readiness receipt, workload receipt, and destroy receipt.**

## Sources

- Local canonical recipe: `scripts/vast/TEMPLATE.md`
- Local unified recipe: `watch/VAST_TEMPLATE_V2_20260901.md`
- Local workload: `watch/STAGED_JOB_5090_20260901.md`
- [Vast Docker execution environment](https://docs.vast.ai/guides/instances/docker-environment)
- [Vast technical FAQ: Docker options and GPU environment](https://docs.vast.ai/guides/reference/faq/technical)
- [Vast CLI: launch instance](https://docs.vast.ai/cli/reference/launch-instance)

**No remote lifecycle action was taken by this audit.**
