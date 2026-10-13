"""B2-296 pins: the mistral key names are canonical exact-case on every surface.

Falsifier under repair: .env declared the mistral keys mixed case
(Mistral_API_KEY / Mistral_API_KEY_2) while configs/providers.yaml names
MISTRAL_API_KEY, so the lane resolved only through Windows case-insensitive
env lookup and the exact-case lookup under WSL found no key at all
(B2_296_falsifier_pre_wsl.json, live 2026-09-26). The load-bearing guarantee
is byte-level: under POSIX, os.environ is a case-sensitive plain dict, so the
only thing that makes every surface resolve is .env declaring the canonical
spelling itself. The load_dotenv pin proves the loader path end-to-end; the
plain-dict pin reproduces POSIX semantics on any host OS.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest
import yaml

from config import ROOT
from models.env_load import load_dotenv

CANONICAL = ("MISTRAL_API_KEY", "MISTRAL_API_KEY_2")
MIXED = ("Mistral_API_KEY", "Mistral_API_KEY_2")


def _env_pairs() -> dict[str, str]:
    """Parse .env the same way models/env_load.py does."""
    out: dict[str, str] = {}
    for line in (ROOT / ".env").read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k:
            out[k] = v
    return out


@pytest.fixture()
def clean_env():
    """Keep ambient env out of the pins and put back whatever dotenv sets."""
    saved = {k: os.environ[k] for k in CANONICAL + MIXED if k in os.environ}
    for k in CANONICAL + MIXED:
        os.environ.pop(k, None)
    yield
    for k in CANONICAL + MIXED:
        os.environ.pop(k, None)
    os.environ.update(saved)


def test_env_declares_canonical_names_only() -> None:
    pairs = _env_pairs()
    for name in CANONICAL:
        assert name in pairs, f".env must declare {name} exactly (POSIX exact-case)"
        assert pairs[name].strip(), f"{name} must carry a value"
    for name in MIXED:
        assert name not in pairs, (
            f".env must not re-introduce the mixed-case spelling {name} "
            "(B2-296: it only resolved via Windows case-insensitive lookup)"
        )


def test_providers_yaml_name_resolves_exact_case() -> None:
    cfg = yaml.safe_load((ROOT / "configs" / "providers.yaml").read_text(encoding="utf-8"))
    api_key_env = cfg["providers"]["mistral"]["api_key_env"]
    assert api_key_env == "MISTRAL_API_KEY"
    pairs = _env_pairs()
    assert pairs.get(api_key_env, "").strip(), (
        "providers.yaml api_key_env must resolve against a POSIX plain dict of .env"
    )


def test_keys_json_manifest_names_resolve_exact_case() -> None:
    import json

    manifest = json.loads((ROOT / "configs" / "keys.json").read_text(encoding="utf-8"))
    pairs = _env_pairs()
    for seat in ("mistral_1", "mistral_2"):
        env_name = manifest[seat]["env"]
        assert env_name in CANONICAL, f"{seat} env name drifted from the canonical set"
        assert pairs.get(env_name, "").strip(), (
            f"keys.json {seat} -> {env_name} must resolve exact-case in .env"
        )


def test_load_dotenv_sets_canonical_names(clean_env) -> None:
    load_dotenv()
    for name in CANONICAL:
        assert os.environ.get(name, "").strip(), (
            f"load_dotenv must expose {name} exact-case"
        )


def test_research_fanout_rows_use_canonical_name() -> None:
    src = (ROOT / "mag" / "research_fanout.py").read_text(encoding="utf-8")
    for name in MIXED:
        assert f'"key": "{name}"' not in src, (
            f"research_fanout endpoint rows must not carry the mixed-case name {name}"
        )
    assert src.count('"key": "MISTRAL_API_KEY"') >= 2


def test_falsifier_artifact_post_state_is_green() -> None:
    post = ROOT / "watch" / "inbox" / "burn_wave_20260926" / "B2_296_falsifier_post_wsl.json"
    if not post.is_file():
        pytest.skip("post-fix falsifier artifact not on disk yet")
    import json

    data = json.loads(post.read_text(encoding="utf-8"))
    assert data["posix_lane_resolves"] is True
    assert all(data["exact_canonical"].values())
    assert not any(data["exact_mixed"].values())
