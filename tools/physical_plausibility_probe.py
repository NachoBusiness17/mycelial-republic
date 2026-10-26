"""Dry-run sizing stub for the nvidia/physical-plausibility-evaluator dogfood.

CONSUMER (Anti-Cow clause, AGENTS.md): the mag probe cadence / geometric probe
instrument. Queue row [probe] Physical-Plausibility Dogfood at
queue/todo.md:312 consumes this module tomorrow: the dogfood lane calls
load_manifest() for the pull list, plan_render() to turn dashboard exhibit
captures into contract mp4s, and score() for the (not yet implemented)
inference step. Card: watch/inbox/PHYSICAL_PLAUSIBILITY_EVAL_CATCH_20261019.md.

VERIFIER: tests/test_physical_plausibility_probe.py (runs in the standing
pytest suite) plus the dogfood falsifier filed on the queue row: estate
renders scoring indistinguishably from the Cosmos-generated noise floor means
the probe manifold is dead and the instrument returns to the shelf (no cow,
F5 live). The pairs-with artifact is the hand-rolled conservation beat at
state/probe_water.json; this learned grader either adds signal over it or dies.

== Sizing verdict (2026-10-19 night shift, byte-backed) ==

HF repo total storage: 316,313 bytes (usedStorage from the API read). The only
weight file is finevideo-attention-linear-v1/model.pt (316,313 bytes, LFS):
the trained attention query + linear head, normalization and calibration
thresholds. The V-JEPA 2.1 ViT-L/16 backbone is NOT bundled; the card states
"V-JEPA 2.1 weights will not be bundled or redistributed with this release"
and names the separate Meta checkpoint vjepa2_1_vitl_dist_vitG_384.pt
(https://github.com/facebookresearch/vjepa2, MIT with Apache-2.0 exceptions).

Local host facts (2026-10-19 census):
- GPU: AMD Radeon RX 5600 XT (WMI Win32_VideoController; AdapterRAM reads
  4,293,918,720 bytes but that field is a 32-bit uint cap, the board is a
  6GB GDDR6 part). nvidia-smi is absent from PATH and C:\Windows\System32.
- venv torch: 2.13.0+cpu (.venv/Lib/site-packages/torch), torch.version.cuda
  is None, torch.cuda.is_available() is False. No CUDA build in the venv.
- Disk: 305 GB free on C: (plenty for a ~1.2GB fp32 backbone when the
  download law permits).

Verdict: CANNOT run on the local GPU, and honest about why: (1) the GPU is
AMD, not NVIDIA, so the CUDA 12.8 stack the card pins is unreachable on this
host at all; (2) the card pins PyTorch 2.10.0+cu128, tested on H100, with
"Supported Operating System(s): Linux" - this host is Windows with torch
2.13.0+cpu, both version and platform off-card; (3) the card certifies no
other GPU architecture. The only theoretical local door is CPU inference of
the frozen encoder (300M params, input [1, 3, 64, 384, 384], 18,432 tokens
per video before pooling): a single ViT-L forward on CPU is minutes per clip,
survivable for a 3-clip dogfood but explicitly off-card. VRAM math for the
record (if a CUDA box is ever pointed at this): FP32 weights ~1.2GB, BF16
autocast activations over 18,432 tokens x 1024 dim across 24 ViT-L layers
roughly 1 to 3GB with SDPA, so ~2.5 to 4.5GB peak - light, as the card says;
the 6GB AMD board would have had room if it spoke CUDA. The card itself
offers the alt door: bob (per the catch card, watch/inbox/
PHYSICAL_PLAUSIBILITY_EVAL_CATCH_20261019.md, "Local shelf" wire item).

== Synthetic fixture plan (do NOT generate tonight; dogfood lane runs it) ==

The input contract is 64 frames at 384x384 (H.264 mp4). A 2-second clip at
32 fps is exactly 64 frames, so the smoke fixture is:

    ffmpeg -y -f lavfi -i "testsrc2=duration=2:size=384x384:rate=32" \
        -pix_fmt yuv420p -c:v libx264 -frames:v 64 \
        tests/fixtures/probe_smoke_2s.mp4

testsrc2 carries motion and a timestamp burn-in (better than plain color for
spotting frame-order bugs). The lane asserts decodable frame count == 64
before scoring; fewer than 64 frames is a hard reject per the model card.
The fixture file is intentionally NOT committed tonight (sizing lane laws).

== Install plan carried by score() (raises until the lane executes it) ==

1. Wait for / pull the 10/20 GitHub release: https://github.com/nvidia-cosmos/cosmos-evaluator
2. Head bundle (309KB, under the 1MB law): huggingface-cli download
   nvidia/physical-plausibility-evaluator finevideo-attention-linear-v1/model.pt
3. Backbone separately from Meta per its own terms (~1.2GB fp32, needs an
   operator-sized download decision): https://github.com/facebookresearch/vjepa2
4. Environment: the card pins torch 2.10.0 + CUDA 12.8 on Linux/H100. This
   venv holds torch 2.13.0+cpu. Either run CPU-only off-card locally, or
   dispatch to bob. Do NOT pip-upgrade this venv to chase the pin (venv drift
   is tracked by the 10-16 patrol, see AGENTS.md census bullet).
5. FFmpeg must be on PATH for decode (the card decodes via FFmpeg).
"""

from __future__ import annotations

MANIFEST_URLS = {
    "model_card": "https://huggingface.co/nvidia/physical-plausibility-evaluator",
    "model_api": "https://huggingface.co/api/models/nvidia/physical-plausibility-evaluator",
    "head_bundle": (
        "https://huggingface.co/nvidia/physical-plausibility-evaluator/resolve/main/"
        "finevideo-attention-linear-v1/model.pt"
    ),
    "release_repo": "https://github.com/nvidia-cosmos/cosmos-evaluator",
    "backbone_source": "https://github.com/facebookresearch/vjepa2",
    "backbone_license": (
        "https://github.com/facebookresearch/vjepa2/blob/"
        "204698b45b3712590f06245fbfba32d3be539812/LICENSE"
    ),
}

HEAD_BUNDLE_RELPATH = "finevideo-attention-linear-v1/model.pt"
BACKBONE_CHECKPOINT = "vjepa2_1_vitl_dist_vitG_384.pt"
FRAME_CONTRACT = {"frames": 64, "height": 384, "width": 384, "fps": 32}
LOCAL_TORCH_CENSUS = "2.13.0+cpu"  # .venv read 2026-10-19; refresh before trusting

KNOWN_EXHIBITS = (
    "smith_race_descent",
    "standing_wave_strip",
    "erosion_field",
    "maze_arena",
)


def load_manifest() -> dict:
    """Return the pull manifest: URLs only, no downloads, no local paths.

    The sizing-law constraint lives here: every value is an https URL. The
    lane decides what to download later; this function never fetches.
    """
    return dict(MANIFEST_URLS)


def plan_render(exhibit_name: str, source: str, out_path: str | None = None) -> str:
    """Build the ffmpeg command that turns a captured exhibit render into a
    contract mp4 (64 frames, 384x384, H.264 yuv420p).

    exhibit_name: one of KNOWN_EXHIBITS (the estate probe roster from the
        catch card) or any label when source is provided explicitly.
    source: path to the captured render (screen recording or frame export of
        the dashboard exhibit). This module fabricates no input paths: the
        estate has no pre-rendered exhibit videos as of 2026-10-19, the
        exhibits live as dashboard renders in the lab UI (:8765) with their
        state beats in state/probe_water.json and kin.
    out_path: defaults to state/probe_clips/<exhibit_name>.mp4.

    32 fps over 64 frames is a 2.0 second window, so a 2s capture fills the
    contract exactly; longer captures are trimmed to the first 64 frames by
    -frames:v. Returns the command string; nothing is executed here.
    """
    if not source:
        raise ValueError(
            "plan_render needs an explicit source path: the estate has no "
            "pre-rendered exhibit videos; capture the dashboard exhibit first "
            "(see module docstring, consumer queue/todo.md:312)."
        )
    if exhibit_name not in KNOWN_EXHIBITS:
        raise ValueError(
            f"unknown exhibit {exhibit_name!r}; known roster: {', '.join(KNOWN_EXHIBITS)}"
        )
    out = out_path or f"state/probe_clips/{exhibit_name}.mp4"
    vf = (
        "fps=32,"
        "scale=384:384:force_original_aspect_ratio=decrease,"
        "pad=384:384:(ow-iw)/2:(oh-ih)/2:black,"
        "format=yuv420p"
    )
    return (
        f'ffmpeg -y -i "{source}" -vf "{vf}" -frames:v 64 '
        f'-c:v libx264 -preset veryfast -crf 18 "{out}"'
    )


def score(video_path: str) -> dict:
    """Score a contract mp4 with the physical-plausibility evaluator.

    NOT implemented tonight (sizing lane law: no downloads >1MB, no pip, no
    GPU compute). This stub exists so the import surface and the manifest /
    render plan are testable before the 10/20 GitHub release lands. Raises
    NotImplementedError carrying the exact install/step plan.
    """
    plan = (
        "physical-plausibility scoring is not installed on this host. "
        "Execution plan, in order: "
        f"(1) pull the Cosmos Evaluator release from {MANIFEST_URLS['release_repo']} "
        "(planned 10/20/2026 per the model card); "
        f"(2) fetch the head bundle only ({HEAD_BUNDLE_RELPATH}, 316,313 bytes) via "
        f"'huggingface-cli download nvidia/physical-plausibility-evaluator {HEAD_BUNDLE_RELPATH}' "
        f"from {MANIFEST_URLS['model_card']}; "
        f"(3) fetch the V-JEPA 2.1 backbone SEPARATELY from {MANIFEST_URLS['backbone_source']} "
        f"(checkpoint {BACKBONE_CHECKPOINT}, ~1.2GB fp32, not bundled with the "
        "release, Meta terms apply - this exceeds the 1MB night-shift law, needs "
        "an operator-sized decision); "
        "(4) environment: the card pins torch 2.10.0 + CUDA 12.8 on Linux/H100 "
        f"but this venv holds torch {LOCAL_TORCH_CENSUS} (no CUDA, torch.version.cuda "
        "is None) and the local GPU is an AMD Radeon RX 5600 XT, so the pinned "
        "CUDA path is unreachable here: run CPU-only off-card, or dispatch to bob "
        "(alt door per watch/inbox/PHYSICAL_PLAUSIBILITY_EVAL_CATCH_20261019.md); "
        "(5) FFmpeg on PATH for decode; "
        "(6) only then implement this body: decode 64 frames at 384x384, run the "
        "frozen ViT-L encoder, attention-pool to 1024 dims, linear head, sigmoid "
        "to bad_score, threshold at the calibrated logit 0.5438173 (cap 0.3)."
    )
    raise NotImplementedError(f"{plan} (input was: {video_path})")
