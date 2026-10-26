# r-auk-voice: Tencent AuK voice generation deep-dive

Dug 2026-09-28, gopher-r-auk-voice (flash50, burn_reset_20260927). All facts below come from three primary sources fetched live this session, cited per section. The estate's earlier FAN dig (`watch/inbox/burn_reset_20260927/work/fan_auk-voice_meta_muse-glimmer-30b.md`, lane meta/muse-glimmer-30b, ts 2026-09-28T02:29:47Z) filed every field OWED because its lane knowledge cutoff is 2026-01-04 and AuK released after that; this dig supersedes that OWED with primary sources. No em-dashes used, per law.

## What it is

AuK is Tencent's open-weight 1.5B foundation model for speech generation and editing, released under the Tencent-Hunyuan org (GitHub README: "AuK is a 1.5B foundation model for speech generation and editing", "Trained on millions of hours of diverse audio data"; ~1.4k stars / 102 forks / 30 commits at fetch time). A unified natural-language instruction interface drives every task: zero-shot TTS, Instruct TTS (voice from a text description, no reference audio), speech/lyric content editing, acoustic editing (pitch in semitones, speed, volume in dB), paralinguistic editing (emotion, timbre, de-accent, nonverbal sounds, whisper conversion), denoise/dereverb, speech separation by talking order, music/vocal separation, and target speaker extraction.

Two variants ship:
- **AuK** (base): `tencent/AuK`, weights `auk_base.safetensors`, 32 function evaluations.
- **AuK-Flash**: `tencent/AuK-Flash`, distilled for 4-step inference (NFE=4, CFG=0), paper-claimed 4.5x wall-clock speedup over the full model under matched conditions.

## Architecture and params

From the arXiv abstract (2609.08936) and HF model card:
- A multimodal LLM for semantic conditioning: the runtime encoder is **Qwen2.5-Omni-3B**, downloaded separately (`hf download Qwen/Qwen2.5-Omni-3B`). Note: the GitHub README states "Qwen3-Omni is not currently supported by --qwen_path".
- A **VAE jointly trained on speech, general audio, and music**: 64-dim latent space at 50 Hz; loaded separately at runtime (the README says missing `text_encoder.*` keys during weight loading are expected for this reason).
- A **hybrid rectified-flow Transformer**: dual-stream MMDiT blocks followed by unified single-stream DiT blocks.
- AuK itself: **1.5B parameters**. Total resident footprint is larger than 1.5B because the 3B encoder and VAE co-load.
- Training scale: ~3.03 billion instruction-audio instances, ~1.95 million hours of effective supervision, then human-feedback preference optimization (818 informative groups, 9,080 rated candidates, editing only) and reward-based RL for generation; Flash distilled via consistency initialization plus task-routed Decoupled DMD.

## License

**MIT.** Both primary sources state it plainly: GitHub README, "AuK is released under the MIT License"; HF model card license field, "MIT License (exact name as stated; full terms in the repo's LICENSE file)". MIT means commercial game integration (paid NPC voice lines) is permitted with attribution; no copyleft and no non-commercial clause. This is the most permissive license of the major open TTS families (CosyVoice and Fish Speech carry Apache-2.0-family terms with their own addenda; several competitors are CC-BY-NC, which would block a shipped game outright).

## VRAM

The only published numbers are the GitHub README's own measurements on **NVIDIA A800-SXM4-80GB, bf16, torch.cuda.max_memory_allocated**:

| Model | Input | Offload off | Offload on | Saved |
|---|---|---|---|---|
| AuK | text only, 1.5 s output | 24.78 GiB | 16.75 GiB | 8.03 GiB (32.4%) |
| AuK | 5 s reference audio | 25.00 GiB | 16.98 GiB | 8.02 GiB (32.1%) |
| AuK-Flash | text only, 1.5 s output | 24.77 GiB | 16.75 GiB | 8.02 GiB (32.4%) |
| AuK-Flash | 5 s reference audio | 24.97 GiB | 16.98 GiB | 7.99 GiB (32.0%) |

Notes verified from the same README: `--cpu_offload` is the CUDA flag; a merged PR claims a further ~7.5 GiB encoder-memory reduction (not reflected in the table above); MLX support exists for Apple Silicon; the base and Flash checkpoints can sit on different devices in the Gradio launcher (`--base_device` / `--flash_device`). Not published and therefore not verified here: consumer-GPU (RTX 3090/4090) measurements, batch throughput, RTF/latency figures. Honest reading for an NPC gateway host: budget ~17 GiB with offload on, ~25 GiB without, per process; a 24 GB card can hold one process with offload on.

## Zero-shot voice cloning quality

The README only links leaderboard badges and a `performance.png` (no numbers in page text). Exact numbers come from the paper's HTML full text (arxiv.org/html/2609.08936v1), Table 3, Seed-TTS-Eval ("Higher is better everywhere except WER"):

WER, lower is better (test-en | test-zh | test-zh-hard | avg):
- Qwen3-TTS: 1.23 | 1.22 | 6.76 | 3.07
- Seed-TTS: 2.25 | 1.12 | 7.59 | 3.65
- VoxCPM2: 1.84 | 0.97 | 8.13 | 3.65
- AuK-Flash: 1.03 | 1.10 | 6.43 | 2.85
- AuK: 1.02 | 1.02 | 5.91 | **2.65** (best average in the table)

Speaker similarity SIM, higher is better (same subsets):
- Qwen3-TTS: 0.717 | 0.770 | 0.748 | 0.745
- Seed-TTS: 0.762 | 0.796 | 0.776 | 0.778
- VoxCPM2: 0.753 | 0.795 | 0.753 | 0.767
- AuK-Flash: 0.772 | 0.814 | 0.784 | 0.790
- AuK: 0.788 | 0.814 | 0.782 | **0.795** (best average in the table)

InstructTTSEval DSD accuracy (ZH | EN): AuK 83.37 | 81.60; AuK-Flash 78.80 | 82.40; best competitors in that table reach 81.10 | 82.40 (Qwen3-TTS-VD) and 82.00 EN (MOSS-VoiceGenerator).

Reading for cloning: **SIM avg 0.795 / 0.790 (base / Flash) with the best average WER in its comparison set** means the distilled Flash variant keeps almost all of the base's voice-similarity (0.790 vs 0.795) while running 4.5x faster, so Flash is the right default for NPC lines. Caveats that the paper does NOT provide: no UTMOS/MOS for TTS generation (UTMOS appears only for enhancement tasks, e.g. AuK-Flash 4.05 on DNS Challenge / VCTK-SR), no RTF/latency table, no human-preference win rates for generation, and the eval subsets are en/zh/zh-hard only. The TTS corpus is described as bilingual Chinese/English; other languages are unverified. I ran no local inference, so no first-party quality check exists beyond these published numbers.

## Integration shape behind an HTTP NPC gateway

Verified serving facts first (GitHub README + HF card):
- **No first-party HTTP server.** Official serving paths are: SGLang-Omni (day-0: `python -m sglang_omni.cli serve --model-path tencent/AuK`), vLLM-Omni (two-stage pipeline, "on a single H100"), Gradio (`auk-gradio`, host 0.0.0.0, port 7860, `--dtype` default bf16, `--preload`), ComfyUI nodes, Xinference, audio.cpp GGUF (`--family auk`) for offline CPU inference, and MLX.
- The **Python API is the stable seam** (README example): `from auk.infer.infer_auk import AukInfer, save_audio`; `engine = AukInfer("ckpts/AuK/config.yaml", "ckpts/AuK/auk_base.safetensors")`; `audio, sample_rate = engine.generate(messages, gen_seconds=7.0)`; messages are chat-style with `{"type": "text", "text": ...}` and `{"type": "audio", "audio": path}` parts; `save_audio(audio, sample_rate, out.wav)`. Output sampling rate is 24 kHz.
- CLI `auk-infer` flags: `--audio`, `--instruction` (always required), `--output`, `--gen_seconds`, `--gen_text`, optional `--ref_text`, `--ckpt`, `--cpu_offload`.
- Install is Python 3.10 via uv or conda on a git clone; weights via `hf download tencent/AuK [--Flash]` plus the separate Qwen2.5-Omni-3B encoder. No Windows-specific install path is documented (uv/conda/Linux-flavored; MLX is the Apple path). Untested on this machine; do not assume WSL2+CUDA works without a probe.

Gateway shape I recommend, built strictly on those verified interfaces:

1. **Thin FastAPI (or aiohttp) wrapper over `AukInfer` in-process**, not a proxy to the Gradio UI. One process owns the model; HTTP just fronts `engine.generate`. Endpoint contract: `POST /v1/voice { npc_id, text, emotion?, speed?, gen_seconds? }` returning 24 kHz WAV (or opus after an ffmpeg hop).
2. **NPC voice profile store**: per `npc_id`, hold reference audio path + `ref_text` (transcript of the reference clip, the same field the CLI exposes) + default instruction. Zero-shot cloning is then a per-request message pair: text part = instruction ("Speak the target text in the voice of the reference audio", plus emotion/speed directives), audio part = the NPC's reference clip. Swapping a voice is a file swap, no retraining; fine-tuning exists (JSONL pairs, `scripts/train.sh`) but is unnecessary for line-level NPC work.
3. **Use AuK-Flash for interactive lines, base for canned cinematics.** Flash keeps SIM 0.790 vs base 0.795 at 4.5x speed; players will not hear that delta, but they will feel 4.5x latency.
4. **Cache hard.** Key on sha256(npc_id + text + instruction + ref audio hash); NPC lines repeat across sessions, so the second hit is disk I/O. This is the same LRU-shaped move the repo's own gates use.
5. **VRAM budget**: run with `--cpu_offload` semantics (the Python engine takes the equivalent config) to sit near 17 GiB and keep headroom on a 24 GB card shared with the game server; pin `--dtype bf16`. If two engines (base + Flash) must co-reside, use the documented `--base_device` / `--flash_device` split.
6. **Keep the encoder pinned to Qwen2.5-Omni-3B** (`--qwen_path` rejects Qwen3-Omni per README) and expect the `text_encoder.*` missing-key warnings at load; they are documented as normal.
7. **Latency honesty**: no RTF is published, so the gateway should stream-or-buffer decision awaits a local benchmark; until measured, treat first-token latency as unknown and keep `gen_seconds` short for barks, long for monologues.

## Verification ledger

Ran this session:
- `grep -ri "auk" ...` over the repo (backgrounded bash): matches were vendored-package substring noise plus the catalog entries pointing at the prior FAN artifact; no prior AuK engineering in the estate beyond that OWED.
- `grep` on `catalog/tags.jsonl` / `catalog/catalog.jsonl`: tag `auk-voice_meta_muse-glimmer-30b.md`, catalog file `watch/inbox/burn_reset_20260927/work/fan_auk-voice_meta_muse-glimmer-30b.md` (read in full; it is the OWED this file closes).
- Live fetches: `https://huggingface.co/tencent/AuK` (model card: tasks, license, install, SGLang-Omni line, stats 365 likes / ~4,457 downloads last month); `https://github.com/Tencent-Hunyuan/AuK` (README: VRAM table, Python API, CLI flags, serving options, install, MIT statement); `https://arxiv.org/abs/2609.08936` (abstract: architecture, training scale, Flash 4.5x); `https://arxiv.org/html/2609.08936v1` (Table 3 WER/SIM, InstructTTSEval, 24 kHz, 64-dim/50 Hz latent, bilingual corpus).

Not run / not verifiable this session: local inference (no GPU probe, no weights downloaded), consumer-GPU VRAM, RTF/latency, languages beyond zh/en, Windows install path. All published numbers above are quoted from the fetched sources; anything outside them is labeled unverified.
