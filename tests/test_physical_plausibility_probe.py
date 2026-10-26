"""Tests for the dry-run physical-plausibility probe stub.

Covers the pure parts only (manifest URLs, ffmpeg plan strings, the
NotImplementedError plan carrier). No network, no ffmpeg execution, no
model download: score() must stay unimplemented until the 10/20 GitHub
release lands and the sizing verdict is acted on (queue/todo.md:312).
Verifier pairing: tools/physical_plausibility_probe.py module docstring.
"""

from __future__ import annotations

import pytest

from tools.physical_plausibility_probe import (
    BACKBONE_CHECKPOINT,
    FRAME_CONTRACT,
    HEAD_BUNDLE_RELPATH,
    KNOWN_EXHIBITS,
    LOCAL_TORCH_CENSUS,
    MANIFEST_URLS,
    load_manifest,
    plan_render,
    score,
)


class TestLoadManifest:
    def test_manifest_is_urls_only(self):
        manifest = load_manifest()
        assert manifest, "manifest must not be empty"
        for key, value in manifest.items():
            assert value.startswith("https://"), f"{key} is not an https URL: {value}"

    def test_manifest_covers_pull_targets(self):
        assert MANIFEST_URLS["head_bundle"].endswith(HEAD_BUNDLE_RELPATH)
        assert "huggingface.co/nvidia/physical-plausibility-evaluator" in MANIFEST_URLS["model_card"]
        assert MANIFEST_URLS["release_repo"] == "https://github.com/nvidia-cosmos/cosmos-evaluator"
        assert MANIFEST_URLS["backbone_source"] == "https://github.com/facebookresearch/vjepa2"

    def test_backbone_is_separate_from_head(self):
        # The card: V-JEPA weights are NOT bundled. The manifest must not
        # point the backbone at the nvidia repo.
        assert BACKBONE_CHECKPOINT not in MANIFEST_URLS["head_bundle"]
        assert "facebookresearch" in MANIFEST_URLS["backbone_source"]

    def test_frame_contract_matches_card(self):
        assert FRAME_CONTRACT == {"frames": 64, "height": 384, "width": 384, "fps": 32}


class TestPlanRender:
    def test_known_exhibit_builds_contract_cmd(self):
        cmd = plan_render("standing_wave_strip", source="captures/sws.png_seq")
        assert cmd.startswith("ffmpeg")
        assert '"captures/sws.png_seq"' in cmd
        assert "-frames:v 64" in cmd
        assert "scale=384:384" in cmd
        assert "format=yuv420p" in cmd
        assert "libx264" in cmd
        assert cmd.rstrip('"').endswith(".mp4")

    def test_fps_math_yields_exactly_64_frames(self):
        # 32 fps x 64 frames = 2.0 seconds, the fixture window.
        cmd = plan_render("maze_arena", source="captures/maze.mp4")
        assert "fps=32" in cmd
        assert FRAME_CONTRACT["frames"] / FRAME_CONTRACT["fps"] == pytest.approx(2.0)

    def test_known_roster_matches_card(self):
        assert set(KNOWN_EXHIBITS) == {
            "smith_race_descent",
            "standing_wave_strip",
            "erosion_field",
            "maze_arena",
        }

    def test_missing_source_is_rejected(self):
        with pytest.raises(ValueError, match="explicit source path"):
            plan_render("erosion_field", source="")

    def test_unknown_exhibit_is_rejected(self):
        with pytest.raises(ValueError, match="unknown exhibit"):
            plan_render("not_a_real_exhibit", source="captures/x.mp4")

    def test_out_path_override(self):
        cmd = plan_render("smith_race_descent", source="a.mp4", out_path="b.mp4")
        assert '"b.mp4"' in cmd
        assert "state/probe_clips" not in cmd


class TestScoreStub:
    def test_score_raises_not_implemented(self):
        with pytest.raises(NotImplementedError):
            score("state/probe_clips/maze_arena.mp4")

    def test_plan_names_model_pull_and_pin(self):
        with pytest.raises(NotImplementedError) as excinfo:
            score("x.mp4")
        msg = str(excinfo.value)
        assert "huggingface-cli download" in msg
        assert HEAD_BUNDLE_RELPATH in msg
        assert BACKBONE_CHECKPOINT in msg
        assert "torch 2.10.0" in msg
        assert LOCAL_TORCH_CENSUS in msg
        assert "AMD Radeon RX 5600 XT" in msg
        assert MANIFEST_URLS["release_repo"] in msg

    def test_plan_names_the_threshold(self):
        # The calibrated logit threshold from the model card.
        with pytest.raises(NotImplementedError, match="0.5438173"):
            score("x.mp4")
