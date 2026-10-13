"""ask_bank tests (AJ2, 2026-09-30).

Covers the contract in bands, house style (synthetic mini-estate in tmp_path,
CLI pinned through main() return codes):
  1. seed/split/verify roundtrip on a synthetic estate: 20 entries, 5 real
     material paths x 4 shapes, manifest shas equal the bytes on disk, 14/6
     partition, disjoint cover, hidden_no sequence.
  2. determinism: a wiped-and-rerun split is byte-identical.
  3. guard rails: seed refuses without --force, split refuses on sha drift,
     verify exits 2 on missing artifacts and 1 on tamper, material drift,
     or a missing .gitignore rule.
  4. draw discipline: hidden preview prints draw id + FIRST LINE only (never
     the material, never the body beyond line one), --reveal prints the full
     rendered ask with the citation on stderr, selection prefers never-drawn
     asks, the ledger records every draw, and a wrong-half --id is exit 2.
  5. provenance laws: no W8/LW9 duel material is reused and no body names
     duel_harness; zero em-dashes in anything the bank writes.
  6. the real estate: the repo .gitignore covers the hidden dir (text rule
     plus git check-ignore); the real hidden half itself is NEVER read here.

Windows note (the bug verify caught on first real run, 2026-09-30): jsonl
artifacts are written newline="" so LF on disk equals the hashed bytes; the
sha tests recompute from Path.read_bytes() for exactly that reason.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools import ask_bank as ab

MARKERS = {  # distinctive per-material tokens for reveal/preview assertions
    "cml": "SYNTH-CML-3f09",
    "mcpman": "SYNTH-MCPMAN-71bb",
    "chainreg": "SYNTH-CHAINREG-52aa",
    "gates": "SYNTH-GATES-9c4d",
    "coremem": "SYNTH-COREMEM-e180",
}


def build_estate(tmp_path: Path) -> Path:
    for mat in ab.MATERIALS:
        p = tmp_path / mat["path"]
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f"# synthetic stand-in {MARKERS[mat['key']]}\n"
                     "clause one: synthetic body for the mini-estate.\n",
                     encoding="utf-8")
    (tmp_path / ".gitignore").write_text(ab.GITIGNORE_RULE + "\n", encoding="utf-8")
    return tmp_path


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def split_out(capsys) -> dict:
    out = json.loads(capsys.readouterr().out)
    return out


@pytest.fixture()
def estate(tmp_path: Path) -> Path:
    root = build_estate(tmp_path)
    assert ab.main(["--root", str(root), "seed"]) == 0
    assert ab.main(["--root", str(root), "split"]) == 0
    return root


def test_roundtrip_partition_and_manifest(tmp_path: Path, estate: Path):
    bank = ab.load_jsonl(ab.hidden_dir(estate) / "bank.jsonl")
    assert len(bank) == 20
    assert {e["shape"] for e in bank} == set(ab.SHAPES)
    assert len({m["path"] for m in ab.MATERIALS}) == 5
    per_material = {}
    for e in bank:
        per_material.setdefault(e["material_path"], set()).add(e["shape"])
    assert all(v == set(ab.SHAPES) for v in per_material.values())
    for e in bank:
        # material sha hashes newline-NORMALIZED text (read_text then encode),
        # so a git autocrlf checkout flip never fakes drift; match that here
        _, sha = ab.read_material(estate, e["material_path"])
        assert sha == e["material_sha256"]
    assert ab.main(["--root", str(estate), "verify"]) == 0

    man = json.loads((ab.bank_root(estate) / "manifest.json").read_text("utf-8"))
    assert man["counts"] == {"total": 20, "train": 14, "hidden": 6}
    train = ab.load_jsonl(ab.bank_root(estate) / "train.jsonl")
    hidden = ab.load_jsonl(ab.hidden_dir(estate) / "hidden.jsonl")
    assert len(train) == 14 and len(hidden) == 6
    t_ids, h_ids = {e["ask_id"] for e in train}, {e["ask_id"] for e in hidden}
    assert not (t_ids & h_ids)
    assert t_ids | h_ids == {e["ask_id"] for e in bank}
    assert [e["hidden_no"] for e in hidden] == [f"hb-{i:02d}" for i in range(1, 7)]
    assert man["sha256"]["train"] == sha_file(ab.bank_root(estate) / "train.jsonl")
    assert man["sha256"]["hidden"] == sha_file(ab.hidden_dir(estate) / "hidden.jsonl")
    assert man["sha256"]["bank"] == sha_file(ab.hidden_dir(estate) / "bank.jsonl")


def test_split_is_deterministic(estate: Path):
    train_p = ab.bank_root(estate) / "train.jsonl"
    hidden_p = ab.hidden_dir(estate) / "hidden.jsonl"
    man_p = ab.bank_root(estate) / "manifest.json"
    before = (train_p.read_bytes(), hidden_p.read_bytes(), man_p.read_bytes())
    train_p.unlink()
    hidden_p.unlink()
    assert ab.main(["--root", str(estate), "split"]) == 0
    assert (train_p.read_bytes(), hidden_p.read_bytes(),
            man_p.read_bytes()) == before


def test_seed_and_split_guards(estate: Path):
    assert ab.main(["--root", str(estate), "seed"]) == 1  # exists, no --force
    assert ab.main(["--root", str(estate), "seed", "--force"]) == 0
    # force reseed wiped split assignment: resplit, then drift the manifest
    assert ab.main(["--root", str(estate), "split", "--force"]) == 0
    man_p = ab.bank_root(estate) / "manifest.json"
    man = json.loads(man_p.read_text("utf-8"))
    man["sha256"]["train"] = "0" * 64
    man_p.write_text(json.dumps(man), encoding="utf-8")
    assert ab.main(["--root", str(estate), "split"]) == 1  # drift, no --force


def test_verify_exit_2_missing_and_exit_1_tamper(tmp_path: Path):
    root = build_estate(tmp_path)
    assert ab.main(["--root", str(root), "verify"]) == 2  # nothing seeded
    ab.main(["--root", str(root), "seed"])
    assert ab.main(["--root", str(root), "verify"]) == 2  # seeded but unsplit
    ab.main(["--root", str(root), "split"])
    hidden_p = ab.hidden_dir(root) / "hidden.jsonl"
    hidden_p.write_bytes(hidden_p.read_bytes() + b'{"tamper": 1}\n')
    assert ab.main(["--root", str(root), "verify"]) == 1  # row without ask_id
    train_p = ab.bank_root(root) / "train.jsonl"
    train_p.write_bytes(train_p.read_bytes() + b"not json at all\n")
    assert ab.main(["--root", str(root), "verify"]) == 1  # unparseable line


def test_verify_flags_material_drift_and_gitignore_gap(estate: Path):
    mat = ab.MATERIALS[0]
    p = estate / mat["path"]
    p.write_text(p.read_text("utf-8") + "post-split edit\n", encoding="utf-8")
    assert ab.main(["--root", str(estate), "verify"]) == 1
    # restore material, break the ignore rule instead
    p.write_text(p.read_text("utf-8").replace("post-split edit\n", ""), encoding="utf-8")
    (estate / ".gitignore").write_text("unrelated/\n", encoding="utf-8")
    assert ab.main(["--root", str(estate), "verify"]) == 1
    (estate / ".gitignore").unlink()
    assert ab.main(["--root", str(estate), "verify"]) == 1


def test_draw_hidden_preview_is_first_line_only(estate: Path, capsys):
    rc = ab.main(["--root", str(estate), "draw", "--hidden",
                  "--note", "unit test"])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["draw_id"] == "v1h-0001" and out["bank"] == "v1"
    assert out["first_line"].startswith("You are")
    dumped = json.dumps(out)
    for marker in MARKERS.values():  # material never leaks into the preview
        assert marker not in dumped
    assert "clause one" not in dumped  # no material body text
    assert ab.LAWS.split(".")[0] not in dumped  # laws only attach at reveal
    body = next(e for e in ab.load_jsonl(ab.hidden_dir(estate) / "hidden.jsonl")
                if e["ask_id"] == out["ask_id"])["body"]
    tail = body.split(". ", 2)[-1]  # a phrase that only exists past line one
    assert tail not in dumped


def test_draw_reveal_renders_full_ask(estate: Path, capsys):
    rc = ab.main(["--root", str(estate), "draw", "--hidden", "--reveal",
                  "--note", "unit test"])
    assert rc == 0
    cap = capsys.readouterr()
    assert "ask_bank v1 draw v1h-0001" in cap.err  # citation on stderr
    assert "<SOURCE path=" in cap.out and "sha256=" in cap.out
    assert "clause one" in cap.out and ab.LAWS in cap.out


def test_draw_selection_and_ledger(estate: Path, capsys):
    ids = []
    for _ in range(2):
        assert ab.main(["--root", str(estate), "draw", "--hidden"]) == 0
        ids.append(json.loads(capsys.readouterr().out)["ask_id"])
    assert ids[0] != ids[1]  # never-drawn first
    ledger = ab.load_jsonl(ab.hidden_dir(estate) / "draws.jsonl")
    assert [r["draw_id"] for r in ledger] == ["v1h-0001", "v1h-0002"]
    assert {r["ask_id"] for r in ledger} == set(ids)
    assert ab.main(["--root", str(estate), "draw", "--hidden",
                    "--id", "not-an-id"]) == 2
    train_id = ab.load_jsonl(ab.bank_root(estate) / "train.jsonl")[0]["ask_id"]
    assert ab.main(["--root", str(estate), "draw", "--hidden",
                    "--id", train_id]) == 2  # train id is not in the hidden half


def test_draw_defaults_to_train(estate: Path, capsys):
    assert ab.main(["--root", str(estate), "draw"]) == 0  # no half flag
    out = json.loads(capsys.readouterr().out)
    assert out["half"] == "train" and out["draw_id"].startswith("v1t-")


def test_no_banked_duel_material_reuse():
    mat_paths = {m["path"] for m in ab.MATERIALS}
    assert not (mat_paths & set(ab.BANKED_DUEL_MATERIALS))
    assert "tools/duel_harness.py" in ab.BANKED_DUEL_MATERIALS
    for mat in ab.MATERIALS:
        for angle in mat["angles"].values():
            assert "duel_harness" not in angle
    for shape, template in ab.SHAPES.items():
        assert "duel_harness" not in template
        assert template.count("{path}") == 1 and template.count("{angle}") == 1


def test_zero_em_dashes_in_bank_text():
    texts = [ab.LAWS, *ab.SHAPES.values()]
    for mat in ab.MATERIALS:
        texts.append(mat["title"])
        texts.extend(mat["angles"].values())
    for t in texts:
        assert chr(0x2014) not in t and chr(0x2013) not in t


def test_real_estate_hidden_dir_is_gitignored():
    # text rule plus git check-ignore; the hidden CONTENT is never read here
    gi = ab.ESTATE_ROOT / ".gitignore"
    assert ab.GITIGNORE_RULE in gi.read_text(encoding="utf-8", errors="replace")
    target = ab.hidden_dir(ab.ESTATE_ROOT) / "hidden.jsonl"
    r = subprocess.run(["git", "check-ignore", "-q", str(target)],
                       cwd=ab.ESTATE_ROOT, capture_output=True)
    if r.returncode not in (0, 1):  # git missing/broken: not a bank verdict
        pytest.skip(f"git check-ignore unavailable: rc={r.returncode}")
    assert r.returncode == 0, f"{target} is NOT gitignored"


def test_only_ask_bank_modules_touch_the_bank():
    # contract: nothing under tools/ but ask_bank.py (machinery) and
    # ask_bank_seed.py (data) may reference the bank or its hidden dir
    for p in (ab.ESTATE_ROOT / "tools").glob("*.py"):
        if p.name in ("ask_bank.py", "ask_bank_seed.py"):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        assert "ask_bank" not in text, f"{p.name} references ask_bank"
