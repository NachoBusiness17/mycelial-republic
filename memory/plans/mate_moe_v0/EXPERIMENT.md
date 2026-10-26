# MATE_MOE_v0 falsifier (STAGED, NOT RUN)

Source verdict: watch/inbox/hermes_burn/DG1_moe_mating_door.md, section (3) THE FALSIFIER
(anthropic/claude-opus-5.5, turn 1, adjudicated 2026-10-01). This file stages the
falsifier as a runnable plan. Nothing below has been executed. Cost: ~$0 (local CPU, no
paid dispatch). Gate: the operator says GO. All settings are copied from the verdict;
anything the verdict leaves unnamed is marked DEVIATION with the decision to make at GO.

Purpose (from the verdict): this run is also the falsifier of the DG1 deliverable itself.
It decides whether the mating->MoE door (FFN-expert extraction form) lives or dies, one
sitting, CPU only.

## PREREQS (verified 2026-10-01 by the staging lane; re-verify at GO)

1. Parents live on the hub (curl -sI, 2026-10-01):
   - https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct -> HTTP/1.1 200 OK
   - https://huggingface.co/Qwen/Qwen2.5-Coder-0.5B-Instruct -> HTTP/1.1 200 OK
   Same-base status is NOT proven by a 200 (verdict flag 7); step 0 gates it.
2. Python env (always .\.venv\Scripts\python.exe, never bare python):
   - transformers 5.15.0 PRESENT
   - torch 2.13.0+cpu PRESENT (CPU build, correct for this leg)
   - datasets ABSENT. Pip line: .\.venv\Scripts\python.exe -m pip install datasets
     (the S_prose slice loads wikitext-2 through it)
   - mergekit ABSENT. Pip line (recommended, see W2-L7 steal):
     .\.venv\Scripts\python.exe -m pip install mergekit
     Tool verified at source 2026-10-01: README "The mergekit-moe script supports merging
     multiple dense models into a mixture of experts, either for direct use or for further
     training."; docs/moe.md gate_mode "hidden" "Uses the hidden state representations of
     the positive/negative prompts for MoE gate parameters."; output archs include Qwen MoE.
   - accelerate ABSENT; not required for device="cpu" evaluation loops.
3. Disk: 612 GB free on C: at staging. Run budget ~10 GB if all four artifacts are saved to
   disk (two ~1GB bf16 parent pulls, fp32 merged/MoE checkpoints, HF cache, wikitext-2);
   ~4 GB if A and B are built and evaluated in memory without saving checkpoints.
4. RAM sanity: fp32 0.5B parent ~2 GB resident; B (shared + two FFN sets) ~3.4 GB. Load one
   artifact at a time; do not hold P1+P2+A+B simultaneously.

## STEP 0: gate check (verdict flag 7 rides here; abort on FAIL)

From the export spec gate row: "Reject if architecture, tokenizer, or base hash differ.
Reject if parent-to-parent FFN cosine is above 0.99 (no specialization)."
- Config check: model_type, hidden size, layer count, vocab size identical across parents.
- Tokenizer check: hash the tokenizer files of both parents; must match.
- Base hash check: both parents claim Qwen2.5-0.5B lineage. Record the checkable evidence
  (config equality + tokenizer hash) in the receipt. DEVIATION note: a cryptographic base
  hash is not published for these checkpoints; config+tokenizer equality plus divergent
  FFN cosines is the strongest available same-base witness. If configs differ, STOP.
- FFN cosine: per layer l, cosine similarity between P1 and P2 flattened MLP tensors
  (gate/up/down). Record min, mean, max. STOP if mean > 0.99 (no specialization to keep).
- Output: gate_receipt.json (pass/fail plus the numbers). On FAIL: log it, do not force the
  run; the verdict's example pair must be replaced with a same-base pair and step 0 rerun.

## PARENTS

- P1: Qwen/Qwen2.5-0.5B-Instruct (general instruct specialist).
- P2: Qwen/Qwen2.5-Coder-0.5B-Instruct (code specialist).
Specialist mapping for the feed/kill rules: S_code's specialist parent is P2; S_prose's
specialist parent is P1.

## ARTIFACTS (four, per the verdict)

- A: TIES dense merge of P1 and P2. Build with mergekit (method ties) or hand-rolled TIES
  (trim + sign-consistent elect + weighted mean); record which in the receipt.
- B: MATE_MOE_v0, E=2, top-1. Build per the export spec table:
  - Shared (one copy): embed, attn, norms, lm_head from a TIES or linear merge of both
    parents (record which).
  - Experts: expert i at layer l is parent i's MLP (gate/up/down), verbatim.
  - Router W_r[l], shape [E x d]: mean layer-l hidden state of parent i on its
    top-fitness prompts (mergekit "hidden" mode equivalent; gate_mode hidden verified in
    mergekit docs/moe.md 2026-10-01). If mergekit is installed, prefer building B's
    skeleton with mergekit-moe (gate_mode: hidden, architecture: qwen) and steal its gate
    weights rather than hand-rolling.
  - Routing: top-1 (verdict rule: top-2 only when E >= 3).
  - Container for this CPU leg: Qwen2-MoE layout in transformers (keeps attention bias).
    GGUF / Q4_K_M conversion is NOT part of this leg; it belongs to the feed rerun only.
- P1: Qwen/Qwen2.5-0.5B-Instruct alone.
- P2: Qwen/Qwen2.5-Coder-0.5B-Instruct alone.

## INSTRUMENT (copied from the verdict)

- transformers, fp32, CPU, context 512, 20k tokens per slice, with
  output_router_logits=True on B.
- Log the date, commit hashes, and CPU model with every number.
- Router-init prompts (B build only): each parent's top-fitness prompts. DEVIATION note:
  the verdict does not name the prompts. Fix at GO: a small fixed prompt set per parent
  (code prompts for P2, general instruct prompts for P1), recorded verbatim in the receipt
  so the router init is reproducible; these prompts must not overlap the eval slices.

## SLICES

- S_code: held-out Python files. Source files outside anything used to build A/B or to init
  the router (this repo's own tree is allowed as source provided the files are not part of
  the build inputs). Record the file list plus a sha256 of the concatenated 20k-token slice
  in the receipt so the slice is reproducible.
- S_prose: wikitext-2 test (datasets: Salesforce/wikitext, wikitext-2-raw-v1, split test;
  first 20k tokens under the same context-512 windowing).

## METRICS

- Perplexity per slice for each artifact (A, B, P1, P2): sliding-window mean NLL over the
  20k-token slice at context 512; report ppl and the exact token count scored.
- B's expert-usage share per slice: from output_router_logits, the top-1 argmax expert per
  token; report the share of tokens routed to expert 1 vs expert 2 on each slice.

## FEEDS (door lives; all three must hold, verdict wording)

- On each slice, B's perplexity is within 3% of that slice's specialist parent.
- A is more than 5% worse than the specialist on at least one slice.
- Expert usage differs between slices by more than 30 points, showing the router routes by
  capability.

## KILLS (any one kills, verdict wording)

- Kill: dense suffices. B is at or above A's perplexity on both slices.
- Kill: router is not specializing. Expert usage is within 10 points across slices.
- Kill: shared attention broke the experts. B is more than 3% worse than the specialist on
  its own slice.

## FEED RERUN (only if it feeds; carries verdict flag 5, still UNVERIFIED)

"If it feeds, rerun at 2B, E=4, on Q4_K_M in llama.cpp (Vulkan, gfx1010). Log tok/s against
the best dense parent at the same quant." Plan this leg only after the CPU leg feeds; it
needs the llama.cpp Mixtral/Qwen2-MoE GGUF arch-support check done first.

## RECEIPT

- Numbers: memory/runs/mate_moe_v0/results.jsonl, one JSON line per artifact x slice
  carrying date, commit hashes, CPU model, and the instrument settings above.
- Verdict text: memory/runs/mate_moe_v0/VERDICT.md quoting the feed or kill that fired,
  plus the gate_receipt.json outcome from step 0.
- Cite the receipt, not memory, on any board or rib that references this run.
