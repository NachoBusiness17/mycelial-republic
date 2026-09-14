"""OpenClaw edit steal: apply_patch alias + Mag-governed patch inbox."""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools import dispatch  # noqa: E402
from mag import openclaw_patches as oc  # noqa: E402


def _jail_dir() -> Path:
    return Path(tempfile.mkdtemp(prefix="_oc_patch_", dir=ROOT))


def test_apply_patch_alias_surgical_edit():
    d = _jail_dir()
    try:
        p = d / "a.txt"
        p.write_text("alpha\nbeta\n", encoding="utf-8")
        r = dispatch("apply_patch", {"path": str(p), "search": "beta", "replace": "gamma"})
        assert r["ok"] is True, r
        assert p.read_text(encoding="utf-8") == "alpha\ngamma\n"
        assert r.get("mode") == "diff"
    finally:
        shutil.rmtree(d, ignore_errors=True)


def test_inbox_apply_and_reject():
    d = _jail_dir()
    inbox = d / "PATCHES"
    inbox.mkdir()
    target = d / "t.txt"
    target.write_text("hello world\n", encoding="utf-8")
    good = {
        "path": str(target),
        "search": "world",
        "replace": "fleet",
    }
    bad = {"path": str(target), "search": "NOPE", "replace": "x"}
    (inbox / "ok.json").write_text(json.dumps(good), encoding="utf-8")
    (inbox / "bad.json").write_text(json.dumps(bad), encoding="utf-8")
    old_inbox, old_applied, old_rejected = oc.INBOX, oc.APPLIED, oc.REJECTED
    oc.INBOX, oc.APPLIED, oc.REJECTED = inbox, inbox / "applied", inbox / "rejected"
    try:
        out = oc.apply_inbox()
        assert out["applied"] == 1, out
        assert out["rejected"] == 1, out
        assert target.read_text(encoding="utf-8") == "hello fleet\n"
        assert (inbox / "applied" / "ok.json").is_file()
        assert (inbox / "rejected" / "bad.json").is_file()
    finally:
        oc.INBOX, oc.APPLIED, oc.REJECTED = old_inbox, old_applied, old_rejected
        shutil.rmtree(d, ignore_errors=True)
