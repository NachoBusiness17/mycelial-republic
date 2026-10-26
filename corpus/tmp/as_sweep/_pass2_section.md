

---

# PASS 2: finetuning-adaptation via reddit, second sweep seat (2026-10-11 evening)

source-fetched: adhoc

This section AMENDS the 2026-10-10/01:57 sweep above (amend, never rewrite): that
sweep's five banked items and its held list stand untouched. This pass re-ran the
recipe doors, re-swept, deep-read six threads, and banks only items verified absent
from catalog/catalog.jsonl, memory/, and watch/inbox/frontier_olm_adhoc/register.jsonl
(greps this session; scratch corpus/tmp/as_sweep/).

Doors this pass, honestly recorded. Same degradation as the 01:57 sweep, confirmed
again: old.reddit.com/r/LocalLLaMA/top.json login wall ("Log in to use old Reddit",
webReader + WebFetch both); www.reddit.com top.json HTTP 403 Blocked (WebFetch) and
"blocked by network security" (webReader); www.reddit.com thread pages return a JS
shell or "Prove your humanity"; api.pullpush.io 429 with curl. Recipe fallback
WebSearch site:reddit.com worked partially (several 1302 rate-limit errors; it yielded
thread URLs including the TTT set but no readable bodies). The door that carried this
pass, same as the 01:57 sweep: the arctic-shift archive API
(arctic-shift.photon-reddit.com/api/posts/search, /api/posts/ids,
/api/comments/search), throttled (422 "Timeout. Maybe slow down a bit" under about
30 s spacing; 32-40 s spacing held).

Pass 1 (broad, last 30 days): keyword pulls lora/finetune/qlora/unsloth over
r/LocalLLaMA since 2026-09-11 (4 successful queries; training/ttt/gemma/test/verl/
trl/adapter all 422-throttled, same under-sampling caveat as the 01:57 OWED list).
34 unique posts in the merged pool plus 7 WebSearch-door URLs and 12 shortlist bodies
fetched: about 45 distinct candidates considered this pass. r/LocalLLM, r/ollama,
r/MachineLearning stayed unswept (throttle budget spent on r/LocalLLaMA; recorded as
door-side negative, not absence).

Pass 2 (deep reads): six threads read as full selftext plus comment trees via the
archive API: 1x0xkk7 Castmates (selftext + 4/4 comments), 1wujtbj Victoria/Maple
(selftext + 9/9 comments), 1q5kokx PonderTTT (selftext + 2/2 comments), 1wnrh76
Unsloth Studio vs LM Studio (title + 100/123 comments; OP body not fetched, stated),
1wr0p3n TensorSharp (selftext + 8/8 comments), 1wybqq3 easycommand (selftext only;
its 5 comments not fetched, OWED). Two corpses confirmed again (1wr469w, 1x0egcy:
bodies [removed]). One candidate dropped as thin (1x10r5t VeriLoop-E2 pointer post).

## Banked items (new, strongest first; all quotes verbatim from fetched archive JSON)

6. Castmates: 3B roleplay finetune fully on iPhone, measured
   https://www.reddit.com/r/LocalLLaMA/comments/1x0xkk7/ (2026-10-08).
   Own rank-16 LoRA on Impish Llama 3B, fused and requantized to Q4_K_M from fp16
   (about 2.0 GB, 4 GB phones the floor, about 6 tok/s on A18, KV q8_0 at about
   60 KB/token). Measured laws: history-trim budget, not n_ctx, was binding (trim at
   0.68 x n_ctx took long-conversation fact recall from 25% to 75%); BM25 retrieval
   re-injected superseded facts (says-stale +20.8pp; filtering hits whose rare
   entities still live in the window fixed it, -18.8pp CI [-35.4,-6.2]); prompt
   wording tweaks measured as zero under N=16 same-seed fixed-history controls;
   placement beat wording (scene direction 0/16 in the reminder slot vs 16/16
   elsewhere). RQ1 (what a 3B absorbs on-device, at what cost) and RQ4 (prompt-only
   vs structural changes) in one artifact. Verbatim: "Prompt tweaks mostly measured
   as zero. Single 3-4 seed runs were noise. Fixed-history micro-tests with N=16 and
   same-seed controls were the only thing we trusted."

7. Victoria + Maple: post-quantization retraining, trained for the shipped format
   https://www.reddit.com/r/LocalLLaMA/comments/1wujtbj/ (2026-09-30).
   Qwen3.8-Flash-Next cut 44% by REAP (512 to 288 experts per layer), then RETRAINED
   at NVFP4 so the weights learn the format they ship in: Terminal-Bench 2.1 70.0%
   avg-of-3 (previous NVFP4 build 62.5%); GGUF Q4_K_M 75.3% single run; draft head
   280 vs 135 tok/s on one B300. Serving law for adapted artifacts: mainline
   llama.cpp rejects their GGUF draft head ("expected 1256, got 1224") until patched.
   Maple (Canadian-default finetune on top): official-source citation 6.0% to 62.9%,
   fully-correct 6.6% to 21.8% on 600 held-out questions; coding held (157/164
   HumanEval). Extends the LoRA-over-GGUF law family the estate banked from 1x1bdvl:
   adaptation artifacts carry stack contracts; "quantize after the fact" leaves
   points on the table vs training at the shipped format. Verbatim: "Retrained at
   4-bit (NVFP4) afterwards, so it's trained for the format it ships in rather than
   just quantized after the fact."

8. PonderTTT: gated test-time training at 124M-1.5B (out-of-window gem, Jan 2026)
   https://www.reddit.com/r/LocalLLaMA/comments/1q5kokx/ (2026-01-06).
   TTT-layer weight updates gated by the layer's own self-supervised reconstruction
   loss (threshold + EMA, no extra training): 82-89% oracle recovery on GPT-2 code
   LM, up to 16% lower loss OOD vs random skip; v1 JAX/Flax, v2 targeting Gemma 3.
   RQ3 fit: the first TTT shape surfaced that matches the living-weights two-tier
   contract: selective, threshold-gated updates (reversible by raising the
   threshold), no separate training run, tested at janitor scale (124M-1.5B).
   Caveat from the thread: TTT "does not massively reduce memory requirements
   compared to ssm". arXiv 2601.00894, code github.com/deveworld/ponderTTT.
   Verbatim: "PonderTTT uses the TTT layer's self-supervised reconstruction loss to
   decide when to update weights: high loss = struggling = UPDATE, low loss =
   confident = SKIP."

9. easycommand: 1.5B Qwen folded to gpt-4o-level bash on 400k synthetic examples
   https://www.reddit.com/r/LocalLLaMA/comments/1wybqq3/ (2026-10-05).
   Fully open: dataset (HF dirac-run/ec-training-data), GGUF models 1.5B and 0.6B,
   CLI. RQ4 evidence that a narrow behavioral fold from a fully synthetic controlled
   corpus carries a 1.5B to frontier-level on one task; no prompt-only baseline
   stated in the thread (OWED; the ten-minute-self falsifier still needs that arm).
   COORDINATION NOTE: a sibling seat's scratch (_ft2_easycommand.html, fetched
   15:48 local today) shows it is mid-read on the same artifact; if that seat banks
   it too, dedupe on the register. Verbatim: "Purely a hobby side project to see how
   far I can push a really small model, using (mostly) automated training pipelines."

10. Unsloth Studio vs LM Studio: the local lane is consolidating around one app
    https://www.reddit.com/r/LocalLLaMA/comments/1wnrh76/ (2026-09-23, 123 comments;
    100 read). Community migration LM Studio to Unsloth Studio: chat router plus
    LoRA training plus quantization/export in one local app; LM Studio exit reasons
    are RAM bloat and update cadence; Unsloth Studio complaints are its persisting
    sandbox and context management. RQ1/RQ5 signal: for a 1-8B local adaptation
    lane the de-facto integrated stack is Unsloth (train, quantize, serve), while
    trl/verl stay the scripted-lane picks; nothing here displaces the W-queue
    verdict in the 01:57 section. Verbatim (top comment, psychohistorian8): "I
    stopped using LM Studio because of how much RAM it was sucking up. Unsloth does
    all the same things I need, and is leaner."

11. TensorSharp: LoRA adapters over GGUF served in a second engine
    https://www.reddit.com/r/LocalLLaMA/comments/1wr0p3n/ (2026-09-26).
    C#/.NET local inference engine running Qwen-Image 2.1 GGUF with its LoRA
    adapters (about 12 GB VRAM with LoRA; RTX 3080 16GB / M5 Pro 48GB test rigs),
    author-maintained adapter configs incl. DoRA and accelerated (8-step/6-pass)
    adapters, honestly labeled. RQ2-adjacent: LoRA-over-GGUF is not llama.cpp-only;
    adapter serving is a multi-engine skill, which matters when the estate tests
    whether banked adapter laws transfer off their source stack. Verbatim: "Those
    are fewer model passes, not a claim of a measured end-to-end speedup on
    particular hardware."

## Not re-banked (verified held; this pass's dedup beyond the 01:57 list)

- 1x1bdvl LoRA over GGUF 40G VRAM: catalog 3 rows (frontier_olm_2026-10-09 sweep).
- 1wywscq MedGemma, 1wv05u1 Jeff router, 1wdjk0y AgileRL: banked by the 01:57 sweep
  of this file; catalog rows confirm.
- 1wuj70v magnitude self-tuning engine: read and rejected off-question by the 01:57
  sweep; unchanged.
- 1wr469w LoRA 11/90 vs 90/90: body [removed] again this pass (the title-law stays
  appealing for RQ2 but there is no readable body; do not bank titles).

## OWED (never asserted as done)

- easycommand blog (dirac.run/posts/easycommand) not fetched by this seat (sibling
  has it in flight); its prompt-only comparison arm unverified.
- 1wybqq3 comment tree (5 comments) not fetched (throttle).
- r/LocalLLM, r/ollama, r/MachineLearning unswept this pass.
- verl/trl acronym title queries 422-rejected by the archive door (systematic
  under-sampling, same as 01:57); no 2026 release threads for either surfaced.

Scratch receipts: corpus/tmp/as_sweep/ (lca_*.json keyword pulls, shortlist_posts.json
12-id batch, comments_1x0xkk7/1wujtbj/1wr0p3n/1wnrh76/1q5kokx.json, post_1x10r5t.json,
as_test.json).
