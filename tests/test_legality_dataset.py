"""legality_dataset tests — W3K receipts (Mickey17 W3 lane, 2026-09-29).

Two laws from the lane card:
  1. Determinism: same seed -> byte-identical train/val splits (sha256).
  2. Label correctness: samples spot-checked against the REAL engine
     (mag/water_graph.py) by independent re-derivation — the test rebuilds
     each board, re-validates per server/world.py's rules, re-applies the
     action, re-ticks, and re-measures the crown delta without ever
     calling the generator's own labeler.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag.water_graph import from_spec  # noqa: E402
from server.protocol import VERBS  # noqa: E402
from tools.legality_dataset import generate, render_tokens, write_dataset  # noqa: E402


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _engine_verdict(row: dict) -> tuple[str | None, bool]:
    """Independent re-derivation of (illegal_reason, crown_gain) using the
    engine directly. Mirrors MountainWorld.validate/_apply semantics as
    written in server/world.py — NOT tools.legality_dataset's copies."""
    spec = row["graph"]
    g = from_spec(spec)
    # from_spec drops node.steam and pipe.primed; restore for fidelity
    for name, nd in spec["nodes"].items():
        g.nodes[name].steam = int(nd.get("steam", 0))
    for name, pp in spec["pipes"].items():
        g.pipes[name].primed = bool(pp.get("primed", False))

    verb, target = row["verb"], row["target"]
    if verb not in VERBS:
        return "unknown_verb", False
    if verb == "valve":
        if target not in g.pipes:
            return "unknown_target", False
    else:
        if target not in g.nodes:
            return "unknown_target", False
        if verb in ("boil", "tag") and g.nodes[target].volume <= 0:
            return "dry_pool", False

    before = g.volume("crown")
    if verb == "boil":
        g.boil(target, 1)
    elif verb == "valve":
        g.pipes[target].open = not g.pipes[target].open
    # join/tag: social verbs, no hydraulics
    g.tick()
    return None, g.volume("crown") > before


def _pick_spot_rows(rows: list[dict], k: int = 10) -> list[dict]:
    """First occurrence of each distinct label, then fill from the head."""
    picked: list[dict] = []
    seen: set[str] = set()
    for r in rows:
        if r["label"] not in seen:
            seen.add(r["label"])
            picked.append(r)
    for r in rows:
        if len(picked) >= k:
            break
        if r not in picked:
            picked.append(r)
    return picked[:k]


# ---------------------------------------------------------------- laws ----
def test_determinism_same_seed_identical_file_hashes(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    write_dataset(a, n=200, seed=17)
    write_dataset(b, n=200, seed=17)
    for split in ("train", "val"):
        ha, hb = _sha(a / f"{split}.jsonl"), _sha(b / f"{split}.jsonl")
        assert ha == hb, f"{split}: same seed must give identical bytes"
        assert (a / f"{split}.jsonl").stat().st_size > 0


def test_different_seed_changes_bytes(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    write_dataset(a, n=200, seed=17)
    write_dataset(b, n=200, seed=18)
    assert _sha(a / "train.jsonl") != _sha(b / "train.jsonl")


def test_splits_counts_and_valid_jsonl(tmp_path):
    out = tmp_path / "ds"
    manifest = write_dataset(out, n=200, seed=17, val_frac=0.1)
    rows = {}
    for split in ("train", "val"):
        path = out / f"{split}.jsonl"
        rows[split] = [json.loads(line) for line in
                       path.read_text(encoding="utf-8").splitlines() if line]
    assert len(rows["train"]) + len(rows["val"]) == 200
    assert 0 < len(rows["val"]) < 200
    dists = manifest["files"]
    assert dists["train"]["rows"] == len(rows["train"])
    assert dists["val"]["rows"] == len(rows["val"])
    for split in ("train", "val"):
        counted: dict[str, int] = {}
        for r in rows[split]:
            counted[r["label"]] = counted.get(r["label"], 0) + 1
        assert counted == dists[split]["labels"]


def test_label_spot_check_against_real_engine():
    train, val = generate(n=60, seed=1234)
    pool = train + val
    labels = {r["label"] for r in pool}
    assert len(labels) >= 4, (
        f"60 samples should exercise at least 4 of the 5 labels, saw {labels}")
    for row in _pick_spot_rows(pool, k=10):
        reason, gain = _engine_verdict(row)
        assert row["illegal_reason"] == reason, (
            f"{row['id']}: stored reason {row['illegal_reason']!r} "
            f"!= engine reason {reason!r}")
        assert row["crown_gain"] == gain, (
            f"{row['id']}: stored crown_gain {row['crown_gain']} "
            f"!= engine crown_gain {gain}")
        expected = (f"illegal_{reason}" if reason
                    else ("legal_gain" if gain else "legal_no_gain"))
        assert row["label"] == expected


def test_token_render_is_flat_state_action_label():
    train, _ = generate(n=10, seed=99)
    row = train[0]
    toks = row["tokens"]
    assert toks[0] == "[STATE]"
    assert toks.count("[ACTION]") == 1 and toks.count("[LABEL]") == 1
    assert toks.index("[STATE]") < toks.index("[ACTION]") < toks.index("[LABEL]")
    assert toks[-1] == row["label"]
    assert f"verb:{row['verb']}" in toks and f"tgt:{row['target']}" in toks
    # render_tokens is pure: same inputs, same tokens
    assert render_tokens(row["graph"], row["verb"], row["target"],
                         row["label"]) == toks
